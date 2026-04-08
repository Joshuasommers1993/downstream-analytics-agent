"""
All LangGraph node functions.
Each node prints its own status line so the terminal shows progress clearly.

Architecture (3 active nodes):
  reasoning_node  — decomposes question into FETCH/COMPUTE plan; COMPUTE steps embed SQL directly
  mcp_fetch_node  — calls Downstream API directly, saves CSV, advances current_idx
  execution_node  — substitutes FETCH_N placeholders in SQL, executes with DuckDB, advances current_idx
  synthesize_node — writes final answer from accumulated step results
"""

import os
import json
import uuid
import textwrap
import pandas as pd
import duckdb
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from agent.state import AgentState
from agent.schema_rag import get_relevant_schema
from agent.tool_selector import get_relevant_tools

load_dotenv()

console = Console()

SESSION_DIR = f"/tmp/analytics_session_{uuid.uuid4().hex[:8]}"
os.makedirs(SESSION_DIR, exist_ok=True)

# ─────────────────────────────────────────────
# LLM
# ─────────────────────────────────────────────
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
)

# Faster/cheaper model for simple tool selection (Stage 1)
llm_mini = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
)


# ─────────────────────────────────────────────
# Direct HTTP client (read-only / GET tools)
# ─────────────────────────────────────────────
import asyncio
import threading
import requests

_API_BASE         = os.getenv("DOWNSTREAM_API_URL", "https://api.trydownstream.com")
_API_KEY          = os.getenv("MCP_API_KEY", "")
_INSIGHT_HUB_KEY  = os.getenv("INSIGHT_HUB_API_KEY", "")
_API_HEADERS      = {"X-API-KEY": _API_KEY, "Content-Type": "application/json"}
_INSIGHT_HEADERS  = {"X-API-KEY": _INSIGHT_HUB_KEY, "Content-Type": "application/json"}


def _headers_for(path: str) -> dict:
    """Return the correct auth headers based on the API path."""
    if path.startswith("/api/insight-hub/"):
        return _INSIGHT_HEADERS
    return _API_HEADERS

MAX_FETCH_ROWS = 10_000     # cap to avoid multi-minute fetches on large tables

def fetch_all_pages(path: str, params: dict | None = None) -> list[dict]:
    """Fetch all pages from a cursor-paginated Downstream API endpoint."""
    rows: list[dict] = []
    query = dict(params or {})
    query["limit"] = 100
    headers = _headers_for(path)

    while True:
        resp = requests.get(f"{_API_BASE}{path}", headers=headers, params=query, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, list):
            # Bare array response
            rows.extend(data)
            break

        # Try known paginated list keys first
        page = None
        for list_key in ("data", "results", "rows"):
            if list_key in data and isinstance(data[list_key], list):
                page = data[list_key]
                break

        # Fall back: scan all values for the first non-empty list
        # (covers insight-hub custom keys: months, states, categories, etc.)
        if page is None:
            for value in data.values():
                if isinstance(value, list):
                    page = value
                    break

        if page is None:
            # Single-object response — wrap as one row
            rows.append(data)
            break

        rows.extend(page)

        if len(rows) >= MAX_FETCH_ROWS:
            break       # cap reached - return what we have so far

        if not data.get("has_more") or not page:
            break
        query["starting_after"] = page[-1]["id"]

    return rows


# ─────────────────────────────────────────────
# MCP client (non-read-only / mutating tools)
# ─────────────────────────────────────────────
# Runs in a background thread to avoid conflicting with LangGraph's event loop.
_bg_loop = asyncio.new_event_loop()
threading.Thread(target=_bg_loop.run_forever, daemon=True).start()

_mcp_tools = None


def _run(coro):
    """Submit a coroutine to the background event loop and block until done."""
    return asyncio.run_coroutine_threadsafe(coro, _bg_loop).result()


def get_mcp_tools():
    global _mcp_tools
    if _mcp_tools is not None:
        return _mcp_tools
    from langchain_mcp_adapters.client import MultiServerMCPClient
    client = MultiServerMCPClient({
        "downstream": {
            "url": os.getenv("MCP_SERVER_URL", "https://mcp.trydownstream.com/mcp"),
            "transport": "streamable_http",
            "headers": {"X-API-Key": _API_KEY},
        }
    })
    _mcp_tools = _run(client.get_tools())
    return _mcp_tools


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def _print_step(title: str, color: str, body: str = ""):
    console.print(f"\n[bold {color}]{'━'*60}[/]")
    console.print(f"[bold {color}]{title}[/]")
    if body:
        console.print(f"[dim]{textwrap.fill(body, width=70)}[/]")


def _current_sentence(state: AgentState) -> str:
    idx = state["current_idx"]
    sentences = state["logic_sentences"]
    if idx < len(sentences):
        return sentences[idx]
    return ""


def _format_tool_block(name: str, info: dict) -> str:
    """Format one tool entry for the reasoning prompt (description + CSV fields if available)."""
    lines = [f"  {name}", f"    -> {info['description']}"]
    if "fields" in info:
        lines.append(f"    -> CSV columns: {info['fields']}")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# NODE 1 — REASONING AGENT
# ─────────────────────────────────────────────
def reasoning_node(state: AgentState) -> AgentState:
    _print_step("🧠  REASONING AGENT", "blue")

    # ── First call: build the full FETCH/COMPUTE plan ─────────────────────────
    if not state["logic_sentences"]:
        from agent.mcp_catalog import MCP_TOOL_CATALOG

        # ── Stage 0: decompose question into atomic data needs ────────────────
        console.print("[blue]  → Stage 0: decomposing question into data needs...[/]")

        decompose_prompt = f"""
You are an analytics planner. Break this question into atomic data needs — each need
is a specific metric or dimension that must be fetched from a data source.

Rules:
- Each need should be a short phrase describing one piece of data (e.g. "take_rate by product_category")
- Be specific about dimensions (what it's grouped by)
- 1-5 needs max
- Output a JSON array of strings, nothing else

Question: {state["question"]}

Output JSON array of data needs only:
""".strip()

        decomp_raw = llm_mini.invoke(decompose_prompt).content.strip()
        if decomp_raw.startswith("```"):
            decomp_raw = decomp_raw.split("```")[1]
            if decomp_raw.startswith("json"):
                decomp_raw = decomp_raw[4:]
        decomp_raw = decomp_raw.strip()
        try:
            data_needs = json.loads(decomp_raw)
        except Exception:
            data_needs = [n.strip(" -•") for n in decomp_raw.splitlines() if n.strip()]

        console.print(f"[blue]  → Data needs:[/]")
        for n in data_needs:
            console.print(f"[blue]     • {n}[/]")

        # ── Stage 1: RAG per data need → collect candidate tools ─────────────
        console.print("[blue]  → Stage 1: RAG lookup per data need...[/]")

        need_candidates: dict[str, str] = {}
        for need in data_needs:
            candidates = get_relevant_tools(need, top_k=3)
            need_candidates[need] = candidates
            console.print(f"[dim]     [{need}][/]")
            for line in candidates.splitlines():
                stripped = line.strip()
                if not stripped:
                    continue
                if stripped.startswith("->"):
                    console.print(f"[dim]         {stripped}[/]")
                else:
                    console.print(f"[blue]       {stripped}[/]")

        # ── Stage 2: validate — does a tool exist for each need? ─────────────
        console.print("[blue]  → Stage 2: validating tool coverage and join keys...[/]")

        all_candidates_block = "\n\n".join(
            f"Need: {need}\nCandidates:\n{tools}"
            for need, tools in need_candidates.items()
        )

        validation_prompt = f"""
You are an analytics planner. For each data need below, decide if one of the candidate
tools can satisfy it. Then check if all selected tools share a join key.

For each need, output:
- "tool": the exact tool name that best satisfies it, or null if none can
- "join_key": the column name that connects this tool to others (e.g. "user_address_id"), or null if standalone

Then output:
- "joinable": true if all selected tools can be joined, false if they have no shared key
- "verdict": "ok" if the question can be answered, "partial" if only some needs are covered,
  or "impossible" if no tools cover the core needs
- "reason": one sentence explaining any limitation

Output valid JSON only:
{{
  "needs": [
    {{"need": "...", "tool": "...", "join_key": "..."}},
    ...
  ],
  "joinable": true/false,
  "verdict": "ok"|"partial"|"impossible",
  "reason": "..."
}}

DATA NEEDS AND CANDIDATES:
{all_candidates_block}

Question: {state["question"]}
""".strip()

        val_raw = llm.invoke(validation_prompt).content.strip()
        if val_raw.startswith("```"):
            val_raw = val_raw.split("```")[1]
            if val_raw.startswith("json"):
                val_raw = val_raw[4:]
        val_raw = val_raw.strip()

        try:
            validation = json.loads(val_raw)
        except Exception:
            validation = {"verdict": "ok", "needs": [], "joinable": True, "reason": ""}

        verdict = validation.get("verdict", "ok")
        reason = validation.get("reason", "")

        console.print(f"[blue]  → Verdict: {verdict}[/]")
        if reason:
            console.print(f"[dim]     {reason}[/]")

        joinable = validation.get("joinable", True)
        if verdict == "impossible" or (not joinable and len(data_needs) > 1):
            # Surface the limitation as the final answer instead of producing bad SQL
            answer = f"This question cannot be answered with the available data. {reason}"
            console.print(Panel(answer, title="[bold yellow]⚠️  Cannot Answer[/]", border_style="yellow", padding=(1, 2)))
            return {**state, "logic_sentences": ["DONE"], "current_idx": 1, "final_answer": answer}

        # Collect confirmed tools (skip needs with null tool)
        confirmed = [
            n["tool"] for n in validation.get("needs", [])
            if n.get("tool") and n["tool"] in MCP_TOOL_CATALOG
        ]
        # Deduplicate while preserving order
        seen = set()
        selected_tools = [t for t in confirmed if not (t in seen or seen.add(t))]

        if not selected_tools:
            # Fallback: use RAG on the full question
            fallback = get_relevant_tools(state["question"], top_k=5)
            sel_raw2 = llm_mini.invoke(f"""
Choose the tools needed to answer this question. Output a JSON array of tool names only.
TOOLS:\n{fallback}\nQuestion: {state["question"]}
""").content.strip()
            if sel_raw2.startswith("```"):
                sel_raw2 = sel_raw2.split("```")[1].lstrip("json").strip()
            try:
                selected_tools = json.loads(sel_raw2)
            except Exception:
                selected_tools = []

        console.print(f"[blue]  → Selected tools: {selected_tools}[/]")

        focused_tools = "\n".join(
            _format_tool_block(t, MCP_TOOL_CATALOG[t])
            for t in selected_tools if t in MCP_TOOL_CATALOG
        )

        # ── Stage 3: build FETCH/COMPUTE plan with SQL ────────────────────────
        console.print("[blue]  → Stage 3: building execution plan with SQL...[/]")

        prompt = f"""
You are a reasoning agent. Decompose this analytics question into an ordered execution plan.

Rules:
- Each step is either FETCH or COMPUTE
- FETCH steps: "FETCH: <exact_tool_name> [optional filter description]"
  * Use the exact tool name from the list below
  * Mention any filters (e.g. status=SCHEDULED, start_date=6 months ago)
- COMPUTE steps: "COMPUTE: <valid DuckDB SQL query>"
  * Use read_csv_auto('FETCH_N') where N = 0-indexed FETCH step number
    (FETCH_0 = result of the 1st FETCH, FETCH_1 = result of the 2nd FETCH, etc.)
  * Use only the column names listed in each tool's "CSV columns"
  * For JSON array columns, use json_extract(col, '$[*].field') to access items
  * For dot-notation columns (e.g. conversion_rates.overall), quote them: "conversion_rates.overall"
  * SELECT only — no INSERT/UPDATE/DELETE
  * Return a concise, focused result
  * When joining two tables, use an explicit JOIN ... ON condition — never a cartesian product
- FETCH steps must come before COMPUTE steps that depend on them
- Only fetch data you actually need
- Output ONLY a JSON array of strings, nothing else

AVAILABLE MCP TOOLS:
{focused_tools}

Question: {state["question"]}

Output JSON array only:
""".strip()

        response = llm.invoke(prompt)
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        try:
            sentences = json.loads(raw)
        except Exception:
            sentences = [line.strip() for line in raw.splitlines() if line.strip().startswith(("FETCH:", "COMPUTE:"))]

        console.print(f"[blue]  → Plan ({len(sentences)} steps):[/]")
        for i, s in enumerate(sentences):
            console.print(f"[blue]    {i+1}. {s}[/]")

        return {**state, "logic_sentences": sentences, "current_idx": 0}

    # ── Error recovery: rephrase current sentence ─────────────────────────────
    if state["error"] and state["ra_retries"] < 3:
        current = _current_sentence(state)
        console.print(f"[yellow]  → Fixing step {state['current_idx']+1} after error: {state['error'][:80]}[/]")

        if current.upper().startswith("COMPUTE:"):
            # SQL error — rewrite the SQL
            file_info = "\n".join(
                f"  FETCH_{n} = {p}" for n, p in enumerate(state["temp_files"])
            )
            prompt = f"""
The following SQL query failed. Rewrite it to fix the error.

Original COMPUTE step:
{current}

Error:
{state["error"]}

Available CSV files (use read_csv_auto(path)):
{file_info}

Rules:
- Use only columns that exist in the CSV (check the error for actual column names)
- Quote dot-notation column names with double quotes (e.g. "conversion_rates.overall")
- Use json_extract for JSON array columns

Output only the corrected sentence starting with "COMPUTE: SELECT ..." — nothing else.
""".strip()
        else:
            # FETCH error — rephrase or switch tool
            prompt = f"""
The following FETCH step failed. Rephrase it or choose a different MCP tool.

Original: {current}
Error: {state["error"]}
Already fetched files: {state["temp_files"]}

AVAILABLE MCP TOOLS relevant to this step:
{get_relevant_tools(current, top_k=5)}

Output only the rephrased sentence (starting with FETCH:):
""".strip()

        response = llm.invoke(prompt)
        new_sentence = response.content.strip()
        sentences = state["logic_sentences"].copy()
        sentences[state["current_idx"]] = new_sentence
        console.print(f"[yellow]  → Rephrased: {new_sentence[:120]}[/]")

        return {
            **state,
            "logic_sentences": sentences,
            "ra_retries": state["ra_retries"] + 1,
            "error": None,
        }

    return state


# ─────────────────────────────────────────────
# NODE 2 — FETCH
# ─────────────────────────────────────────────
def mcp_fetch_node(state: AgentState) -> AgentState:
    sentence = _current_sentence(state)
    _print_step(f"📥  FETCH  [step {state['current_idx']+1}]", "green", sentence)

    # Extract tool name from "FETCH: <tool_name> [optional description]"
    tool_name = sentence[len("FETCH:"):].strip().split()[0]

    from agent.mcp_catalog import MCP_TOOL_CATALOG
    tool_info = MCP_TOOL_CATALOG.get(tool_name)
    if not tool_info:
        return {**state, "error": f"Unknown tool: {tool_name}"}

    is_readonly = tool_info.get("method", "GET").upper() == "GET"

    if is_readonly:
        # Read-only: call Downstream API directly (fast, no size limits)
        path = tool_info["path"]
        console.print(f"[green]  → Direct API: GET {_API_BASE}{path}[/]")
        try:
            all_rows = fetch_all_pages(path)
        except Exception as e:
            return {**state, "error": f"API fetch error ({path}): {e}"}
    else:
        # Mutating tool: route through MCP (handles auth + side effects)
        console.print(f"[green]  → MCP call: {tool_name}[/]")
        try:
            tools = get_mcp_tools()
            tool_fn = next((t for t in tools if t.name == tool_name), None)
            if not tool_fn:
                return {**state, "error": f"Tool not found in MCP: {tool_name}"}
            result = _run(tool_fn.ainvoke({}))
            raw = result[0].get("text", "") if isinstance(result, list) and result else json.dumps(result)
            data = json.loads(raw) if raw else {}
            all_rows = data.get("data", data.get("results", [data] if isinstance(data, dict) else data))
        except Exception as e:
            return {**state, "error": f"MCP tool error: {e}"}

    cap_note = f" [yellow](capped at {MAX_FETCH_ROWS})[/]" if len(all_rows) >= MAX_FETCH_ROWS else ""
    console.print(f"[green] → Got {len(all_rows)} rows[/]")

    # Save to temp CSV — named by fetch order (not sentence index)
    fetch_idx = len(state["temp_files"])
    filename = f"{SESSION_DIR}/fetch_{fetch_idx}.csv"
    df = pd.json_normalize(all_rows)
    df.to_csv(filename, index=False)
    console.print(f"[green]  → Saved {len(df)} rows → {filename}[/]")
    console.print(f"[green]  → Columns: {list(df.columns)}[/]")

    return {
        **state,
        "temp_files": state["temp_files"] + [filename],
        "current_idx": state["current_idx"] + 1,
        "error": None,
    }


# ─────────────────────────────────────────────
# NODE 3 — EXECUTION LAYER
# ─────────────────────────────────────────────
def execution_node(state: AgentState) -> AgentState:
    sentence = _current_sentence(state)
    _print_step(f"⚙️   EXECUTE  [step {state['current_idx']+1}]", "cyan", sentence)

    # Extract SQL from the COMPUTE sentence
    sql = sentence[len("COMPUTE:"):].strip()

    # Substitute FETCH_N placeholders with actual file paths
    for n, path in enumerate(state["temp_files"]):
        sql = sql.replace(f"FETCH_{n}", path)

    console.print(f"[cyan]  → SQL:[/]")
    console.print(Panel(sql, style="cyan dim", padding=(0, 2)))

    try:
        conn = duckdb.connect()
        result_df = conn.execute(sql).fetchdf()
        conn.close()

        result_str = result_df.to_string(index=False)
        console.print(f"[cyan]  → Result:[/]")
        console.print(Panel(result_str, style="cyan dim", padding=(0, 2)))

        return {
            **state,
            "step_results": state["step_results"] + [
                f"Step {state['current_idx']+1}: {result_str}"
            ],
            "current_idx": state["current_idx"] + 1,
            "error": None,
        }

    except Exception as e:
        error_msg = str(e)
        console.print(f"[red]  → Execution error: {error_msg}[/]")
        return {
            **state,
            "error": error_msg,
        }


# ─────────────────────────────────────────────
# NODE 4 — SYNTHESIZE
# ─────────────────────────────────────────────
def synthesize_node(state: AgentState) -> AgentState:
    _print_step("💡  SYNTHESIZING FINAL ANSWER", "yellow")

    results_block = "\n".join(state["step_results"])

    prompt = f"""
You are an analytics assistant. The user asked:
"{state["question"]}"

Each step produced the following results:
{results_block}

Write a clear, concise final answer to the user's question.
Use numbers and percentages where available.
""".strip()

    response = llm.invoke(prompt)
    answer = response.content.strip()

    console.print("\n")
    console.print(Panel(
        Text(answer, style="bold white"),
        title="[bold yellow]✅ Final Answer[/]",
        border_style="yellow",
        padding=(1, 2),
    ))

    return {**state, "final_answer": answer}
