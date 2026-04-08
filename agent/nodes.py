"""
All LangGraph node functions.
Each node prints its own status line so the terminal shows progress clearly.

Architecture (3 active nodes):
  reasoning_node  — decomposes question into FETCH/COMPUTE plan; COMPUTE steps embed SQL directly
  mcp_fetch_node  — calls MCP tool, saves CSV, advances current_idx
  execution_node  — substitutes FETCH_N placeholders in SQL, executes with DuckDB, advances current_idx
  synthesize_node — writes final answer from accumulated step results
"""

import asyncio
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
# Dedicated async thread + MCP tools (loaded once)
# ─────────────────────────────────────────────
# LangGraph runs its own event loop internally, so we isolate all MCP async
# calls in a background thread with its own persistent event loop.
import threading

_bg_loop = asyncio.new_event_loop()
threading.Thread(target=_bg_loop.run_forever, daemon=True).start()

_mcp_tools = None


def _run(coro):
    """Submit a coroutine to the background thread's event loop and block until done."""
    future = asyncio.run_coroutine_threadsafe(coro, _bg_loop)
    return future.result()


def get_mcp_tools():
    global _mcp_tools
    if _mcp_tools is not None:
        return _mcp_tools

    from langchain_mcp_adapters.client import MultiServerMCPClient

    mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8787/mcp")
    api_key = os.getenv("MCP_API_KEY", "")

    client = MultiServerMCPClient({
        "downstream": {
            "url": mcp_url,
            "transport": "streamable_http",
            "headers": {"Authorization": f"Bearer {api_key}"},
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

        # Stage 1: RAG candidates → gpt-4o-mini selects only needed tools
        console.print("[blue]  → Stage 1: selecting tools from RAG candidates...[/]")

        candidates = get_relevant_tools(state["question"], top_k=8)

        selection_prompt = f"""
You are a tool selector. Given an analytics question and a list of candidate MCP tools,
choose only the tools actually needed to answer the question.

Rules:
- Read each tool description carefully
- Select only tools whose data directly answers the question
- Prefer pre-computed analytics endpoints (insight_hub) over raw data endpoints when available
- Output a JSON array of tool names only, nothing else
- If multiple fetches are needed (e.g. orders + users), include all required tools

CANDIDATE TOOLS:
{candidates}

Question: {state["question"]}

Output JSON array of selected tool names only:
""".strip()

        sel_response = llm_mini.invoke(selection_prompt)
        sel_raw = sel_response.content.strip()
        if sel_raw.startswith("```"):
            sel_raw = sel_raw.split("```")[1]
            if sel_raw.startswith("json"):
                sel_raw = sel_raw[4:]
        sel_raw = sel_raw.strip()

        try:
            selected_tools = json.loads(sel_raw)
        except Exception:
            selected_tools = [t.strip() for t in sel_raw.splitlines() if t.strip()]

        console.print(f"[blue]  → Selected tools: {selected_tools}[/]")

        # Build focused tool block with descriptions + CSV field schemas
        from agent.mcp_catalog import MCP_TOOL_CATALOG
        focused_tools = "\n".join(
            _format_tool_block(t, MCP_TOOL_CATALOG[t])
            for t in selected_tools if t in MCP_TOOL_CATALOG
        ) or candidates  # fallback to full candidates if selection fails

        # Stage 2: build FETCH/COMPUTE plan with SQL embedded in COMPUTE steps
        console.print("[blue]  → Stage 2: building execution plan with SQL...[/]")

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
# NODE 2 — MCP FETCH
# ─────────────────────────────────────────────
def mcp_fetch_node(state: AgentState) -> AgentState:
    sentence = _current_sentence(state)
    _print_step(f"🔌  MCP FETCH  [step {state['current_idx']+1}]", "green", sentence)

    # Extract tool name directly from the sentence — no LLM needed
    # Format: "FETCH: <tool_name> [optional filter description]"
    after_fetch = sentence[len("FETCH:"):].strip()
    tool_name = after_fetch.split()[0]

    tools = get_mcp_tools()
    tool_fn = next((t for t in tools if t.name == tool_name), None)

    if tool_fn is None:
        return {**state, "error": f"Tool not found: {tool_name}"}

    console.print(f"[green]  → Calling tool: [bold]{tool_name}[/][/]")

    try:
        result = _run(tool_fn.ainvoke({}))
        if isinstance(result, str):
            try:
                data = json.loads(result)
            except Exception:
                data = result
        else:
            data = result

        if isinstance(data, dict):
            rows = data.get("results", data.get("data", [data]))
        elif isinstance(data, list):
            rows = data
        else:
            rows = [{"result": str(data)}]
    except Exception as e:
        return {**state, "error": f"MCP tool error: {e}"}

    all_rows = rows
    console.print(f"[green]  → Got {len(all_rows)} rows[/]")

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
