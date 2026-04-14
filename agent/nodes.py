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
import re
import json
import uuid
import atexit
import shutil
import textwrap
import glob as _glob
from datetime import datetime, timezone
import pandas as pd
import duckdb
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from agent.state import AgentState
from agent.schema_rag import get_relevant_schema
from agent.tool_selector import get_relevant_tools
from agent.prompt_builder import format_tool_block

load_dotenv()

console = Console()

SESSION_DIR = f"/tmp/analytics_session_{uuid.uuid4().hex[:8]}"
os.makedirs(SESSION_DIR, exist_ok=True)

# Clean up this session's temp dir on exit
atexit.register(shutil.rmtree, SESSION_DIR, True)

# Clean up stale sessions older than 2 hours from previous crashed runs
_stale_cutoff = datetime.now(timezone.utc).timestamp() - 2 * 3600
for _stale in _glob.glob("/tmp/analytics_session_*"):
    try:
        if os.path.getmtime(_stale) < _stale_cutoff:
            shutil.rmtree(_stale, ignore_errors=True)
    except OSError:
        pass

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

MAX_FETCH_ROWS = 100_000    # cap to avoid multi-minute fetches on large tables

# Measured throughput: ~100 rows per request, ~0.9s per request
# NOTE: Downstream API uses cursor-based pagination (starting_after), not offset-based.
# Parallel fetching is not possible — the API ignores offset= and always returns from the start.
_ROWS_PER_PAGE = 100
_SECS_PER_PAGE = 0.9


def _preflight_check(path: str, params: dict, has_filters: bool) -> int | None:
    """
    Fire limit=1 probe(s) to get server-side count before a full fetch.

    When filters are present, fires two probes:
      1. with filters    → count_filtered
      2. without filters → count_unfiltered

    If count_filtered == count_unfiltered, the API silently ignored the filter
    (unknown param) — warns the agent so it can correct the filter key.

    Returns the filtered count (or unfiltered if no filters), or None if the
    API doesn't expose a count field (e.g. insight-hub summary endpoints).
    """

    def _probe(probe_params: dict) -> int | None:
        try:
            resp = requests.get(
                f"{_API_BASE}{path}",
                headers=_headers_for(path),
                params={**probe_params, "limit": 1},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            console.print(f"[dim green]  → Pre-flight failed ({e}), proceeding without count estimate.[/]")
            return None
        if not isinstance(data, dict):
            return None
        for key in ("count", "total", "num_results", "total_count"):
            val = data.get(key)
            if isinstance(val, int):
                return val
        return None

    count = _probe(params)
    if count is None:
        return None  # bare array or summary endpoint — skip

    # If filters were passed, also probe without them to detect silent no-ops
    if has_filters:
        count_unfiltered = _probe({})
        if count_unfiltered is not None and count == count_unfiltered:
            filter_keys = ", ".join(k for k in params)
            console.print(f"[bold yellow]  ⚠ Pre-flight: filtered count ({count:,}) == unfiltered count ({count_unfiltered:,}) — filter param(s) [{filter_keys}] may not be recognized by this endpoint and are being silently ignored.[/]")
        elif count == 0:
            console.print(f"[bold yellow]  ⚠ Pre-flight: 0 rows with current filters — no matching data or filters are too restrictive.[/]")

    # Estimate fetch time (sequential cursor pagination)
    pages = max(1, -(-min(count, MAX_FETCH_ROWS) // _ROWS_PER_PAGE))
    est_secs = pages * _SECS_PER_PAGE
    est_str = f"~{est_secs:.0f}s" if est_secs < 60 else f"~{est_secs/60:.1f}min"

    if count >= MAX_FETCH_ROWS:
        console.print(f"[bold yellow]  ⚠ Pre-flight: {count:,} rows — will hit {MAX_FETCH_ROWS:,}-row cap. Add filters to narrow the dataset. Estimated fetch time: {est_str}[/]")
    else:
        console.print(f"[green]  → Pre-flight: {count:,} rows — estimated fetch time {est_str}[/]")

    return count


def _extract_page(data: dict | list) -> list[dict] | None:
    """Extract the row list from an API response envelope. Returns None for single-object responses."""
    if isinstance(data, list):
        return data
    for list_key in ("data", "results", "rows"):
        if list_key in data and isinstance(data[list_key], list):
            return data[list_key]
    # Fall back: first list value (covers insight-hub custom keys)
    for value in data.values():
        if isinstance(value, list):
            return value
    return None  # single-object response


def fetch_all_pages(path: str, params: dict | None = None, total_count: int | None = None) -> list[dict]:
    """
    Fetch all rows from a Downstream API endpoint using cursor-based pagination.

    The Downstream API uses starting_after cursor pagination — offset-based parallel
    fetching is not possible as the API ignores the offset param and always returns
    from the beginning.
    """
    params = dict(params or {})
    headers = _headers_for(path)
    rows = []
    query = {**params, "limit": _ROWS_PER_PAGE}

    while True:
        resp = requests.get(f"{_API_BASE}{path}", headers=headers, params=query, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        page = _extract_page(data)

        if page is None:
            # Single-object response — wrap as one row
            rows.append(data)
            break

        if isinstance(data, list):
            rows.extend(data)
            break

        rows.extend(page)

        if len(rows) >= MAX_FETCH_ROWS:
            import warnings
            warnings.warn(f"fetch_all_pages: hit {MAX_FETCH_ROWS} row cap for {path}. Results are incomplete.")
            break

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
_step_start_times: dict[str, float] = {}


def _print_step(title: str, color: str, body: str = ""):
    import time
    ts = datetime.now().strftime("%H:%M:%S")

    # Print elapsed time since the previous step
    if _step_start_times:
        last_key = next(reversed(_step_start_times))
        elapsed = time.time() - _step_start_times[last_key]
        console.print(f"[dim]  ↳ {last_key} took {elapsed:.1f}s[/]")

    _step_start_times[title] = time.time()

    console.print(f"\n[bold {color}]{'━'*60}[/]")
    console.print(f"[bold {color}]{title}[/]  [dim]{ts}[/]")
    if body:
        console.print(f"[dim]{textwrap.fill(body, width=70)}[/]")


def _current_sentence(state: AgentState) -> str:
    idx = state["current_idx"]
    sentences = state["logic_sentences"]
    if idx < len(sentences):
        return sentences[idx]
    return ""



# ─────────────────────────────────────────────
# NODE 1 — REASONING AGENT
# ─────────────────────────────────────────────
def reasoning_node(state: AgentState) -> AgentState:
    _print_step("🧠  REASONING AGENT", "blue")

    # ── First call: build the full FETCH/COMPUTE plan ─────────────────────────
    if not state["logic_sentences"]:

        # Stage 1: downstream agent selects relevant tools + emits analytical reasoning
        console.print("[blue]  → Stage 1: asking downstream agent for relevant tools...[/]")
        focused_tools, stage1_reasoning = get_relevant_tools(state["question"], top_k=8)

        # Print selected tool names
        for line in focused_tools.splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("->"):
                console.print(f"[blue]     {stripped}[/]")

        if stage1_reasoning:
            console.print(f"\n[bold blue]  💬 Stage 1 analytical reasoning:[/]")
            console.print(Panel(stage1_reasoning, style="blue dim", padding=(0, 2)))

        # Stage 2: build FETCH/COMPUTE plan with SQL embedded in COMPUTE steps
        console.print("[blue]  → Stage 2: building execution plan with SQL...[/]")

        # Inject Stage 1 analytical plan if present — Stage 2 maps intent to actual columns
        reasoning_block = ""
        if stage1_reasoning:
            reasoning_block = f"""
Analytical plan (what to compute — no column names; map intent to actual column names from the tool fields listed above):
{stage1_reasoning}

"""

        prompt = f"""
You are a reasoning agent. Decompose this analytics question into an ordered execution plan.

Rules:
- Each step is either FETCH or COMPUTE
- FETCH steps: "FETCH: <exact_tool_name> [key=value ...]"
  * Use the exact tool name from the list below
  * Pass API-supported filters as key=value pairs directly after the tool name
  * Example: "FETCH: api_v1_orders_list status=COMPLETE created_on__gte=2024-01-01"
  * Example: "FETCH: api_v1_seller_locations_list is_active=true"
  * Use each tool's "Filters:" list — only pass params the tool actually supports
  * Dates use ISO format YYYY-MM-DD. Today is {datetime.now().strftime("%Y-%m-%d")}.
  * Filtering server-side is MUCH faster than downloading all rows and filtering in SQL — always prefer it
  * IMPORTANT: Large tables (orders, user_addresses, seller_products, etc.) can have hundreds of thousands of rows. The fetch is capped at 100,000 rows. For any question involving order history, cohort analysis, or retention, ALWAYS add a date range filter (e.g. created_on__gte=2024-01-01) to avoid hitting the cap and getting incomplete data.
  * You can reference a field from a previous FETCH result as a filter value using FETCH_N.field_name
    - Example: "FETCH: api_v1_user_groups_list id=FETCH_0.user_group"
    - Example: "FETCH: api_v1_users_list user_group=FETCH_0.user_group"
    - The field must exist in that FETCH step's listed columns
    - This reads the first row's value from that column at runtime — use only for scalar FK fields
    - FETCH_N resolves exactly ONE value (the first row). Never use it to pass a list of IDs.
      For multi-value lookups, fetch the full dataset and filter in a COMPUTE step instead.
- COMPUTE steps: "COMPUTE: <valid DuckDB SQL query>"
  * Use read_csv_auto('FETCH_N') where N = 0-indexed position in the temp_files list
    - FETCH_0 = result of the 1st FETCH step
    - FETCH_1 = result of the 2nd FETCH step OR result of the 1st COMPUTE step (if it was saved)
    - Each FETCH and each COMPUTE step that produces output adds one entry to temp_files in order
  * Use CTEs (WITH clauses) to handle multi-step logic inside a single COMPUTE step
    - PREFER one COMPUTE step with CTEs over multiple chained COMPUTE steps
    - Example: WITH a AS (...), b AS (...) SELECT ... FROM a JOIN b ...
  * Use only the column names listed in each tool's "CSV columns"
  * For JSON array columns, use json_extract(col, '$[*].field') to access items
  * For dot-notation columns (e.g. conversion_rates.overall), quote them: "conversion_rates.overall"
  * Use epoch() for date arithmetic: epoch(col::TIMESTAMP) gives Unix seconds; divide by 86400 for days
  * When combining two independently fetched datasets on any key that is not guaranteed to exist in both sources, ALWAYS use FULL OUTER JOIN with COALESCE, never INNER JOIN — INNER JOIN silently drops rows present in only one source and produces incomplete results with no error or warning. Only use INNER JOIN when you explicitly want to restrict results to rows that exist in both datasets (e.g. filtering orders to only those with a matching seller).
  * SELECT only — no INSERT/UPDATE/DELETE
  * Return a concise, focused result
- FETCH steps must come before COMPUTE steps that depend on them
- Only fetch data you actually need
- Output ONLY a JSON array of strings, nothing else

AVAILABLE MCP TOOLS:
{focused_tools}
{reasoning_block}Question: {state["question"]}

Output JSON array only:
""".strip()

        response = llm.invoke(prompt)
        raw = response.content.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        # LLM sometimes uses backslash-newline continuation inside JSON strings — strip them
        raw_clean = re.sub(r'\\\n\s*', ' ', raw)
        try:
            sentences = json.loads(raw_clean)
        except Exception:
            # Fallback: extract quoted or unquoted FETCH/COMPUTE lines
            sentences = []
            for line in raw_clean.splitlines():
                s = line.strip().strip('"').rstrip('",').strip()
                if s.startswith(("FETCH:", "COMPUTE:")):
                    sentences.append(s)

        if not sentences:
            console.print(f"[red]  → Stage 2 returned empty plan — raw response:[/]")
            console.print(Panel(raw[:500], style="red dim", padding=(0, 2)))

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
- CTEs (WITH clauses) are valid and preferred — do NOT split them into separate files
- NEVER reference tables by name (first_product, first_order, etc.) — only read_csv_auto(path) or CTEs defined in the same query

Output only the corrected sentence starting with "COMPUTE: " followed by valid DuckDB SQL (may start with WITH for CTEs) — nothing else.
""".strip()
        else:
            # FETCH error — rephrase or switch tool
            prompt = f"""
The following FETCH step failed. Rephrase it or choose a different MCP tool.

Original: {current}
Error: {state["error"]}
Already fetched files: {state["temp_files"]}

AVAILABLE MCP TOOLS relevant to this step:
{get_relevant_tools(current, top_k=5)[0]}

Output only the rephrased sentence (starting with FETCH:):
""".strip()

        response = llm.invoke(prompt)
        new_sentence = response.content.strip()
        # Strip markdown fences the LLM sometimes wraps around its output
        if new_sentence.startswith("```"):
            new_sentence = new_sentence.split("```")[1]
            if new_sentence.startswith(("sql", "json")):
                new_sentence = new_sentence[new_sentence.index("\n")+1:]
            new_sentence = new_sentence.strip()
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

    # Extract tool name and optional key=value API filters from FETCH sentence
    # Format: "FETCH: tool_name key=value key2=value2"
    parts = sentence[len("FETCH:"):].strip().split()
    tool_name = parts[0]
    api_params = {}
    for part in parts[1:]:
        if "=" in part:
            k, v = part.split("=", 1)
            api_params[k] = v

    # Resolve FETCH_N.field_name references in filter values
    for k, v in list(api_params.items()):
        if v.startswith("FETCH_") and "." in v:
            ref_part, col = v.split(".", 1)
            ref_idx_str = ref_part[len("FETCH_"):]
            if ref_idx_str.isdigit():
                ref_idx = int(ref_idx_str)
                if ref_idx < len(state["temp_files"]):
                    ref_df = pd.read_csv(state["temp_files"][ref_idx], nrows=1)
                    if col in ref_df.columns:
                        resolved = str(ref_df[col].iloc[0])
                        console.print(f"[green]  → Resolved {v} → {resolved}[/]")
                        api_params[k] = resolved
                    else:
                        console.print(f"[yellow]  → Warning: column '{col}' not found in FETCH_{ref_idx}[/]")
                else:
                    console.print(f"[yellow]  → Warning: FETCH_{ref_idx} not yet available[/]")

    from agent.mcp_catalog import MCP_TOOL_CATALOG
    tool_info = MCP_TOOL_CATALOG.get(tool_name)
    if not tool_info:
        return {**state, "error": f"Unknown tool: {tool_name}"}

    if api_params:
        console.print(f"[green]  → API filters: {api_params}[/]")

    is_readonly = tool_info.get("method", "GET").upper() == "GET"

    if is_readonly:
        # Read-only: call Downstream API directly with optional server-side filters
        path = tool_info["path"]
        console.print(f"[green]  → Direct API: GET {_API_BASE}{path}[/]")

        # Pre-flight: get row count, estimate time, validate filters
        total_count = _preflight_check(path, api_params, has_filters=bool(api_params))

        try:
            all_rows = fetch_all_pages(path, params=api_params, total_count=total_count)
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

    capped = len(all_rows) >= MAX_FETCH_ROWS
    cap_note = f" [yellow](capped at {MAX_FETCH_ROWS})[/]" if capped else ""
    console.print(f"[green] → Got {len(all_rows)} rows{cap_note}[/]")
    if capped:
        console.print(f"[bold yellow]  ⚠ WARNING: fetch hit the {MAX_FETCH_ROWS}-row cap — results are INCOMPLETE. Add server-side date/status filters to get full data.[/]")

    # Save to temp CSV — named by fetch order (not sentence index)
    fetch_idx = len(state["temp_files"])
    filename = f"{SESSION_DIR}/fetch_{fetch_idx}.csv"
    df = pd.json_normalize(all_rows)
    df.to_csv(filename, index=False)
    console.print(f"[green]  → Saved {len(df)} rows → {filename}[/]")
    # console.print(f"[green]  → Columns: {list(df.columns)}[/]")

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

        # Save COMPUTE result to CSV so later steps can reference it as FETCH_N
        compute_idx = len(state["temp_files"])
        compute_file = f"{SESSION_DIR}/compute_{compute_idx}.csv"
        result_df.to_csv(compute_file, index=False)

        return {
            **state,
            "temp_files": state["temp_files"] + [compute_file],
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

    if not state["step_results"]:
        console.print("[red]  → No step results — cannot synthesize answer.[/]")
        return {**state, "final_answer": "Could not answer: no data was fetched or computed. The execution plan may have been empty or all steps failed."}

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
