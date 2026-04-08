"""
All LangGraph node functions.
Each node prints its own status line so the terminal shows progress clearly.
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


# ─────────────────────────────────────────────
# MCP tools (loaded once)
# ─────────────────────────────────────────────
_mcp_tools = None

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
    _mcp_tools = client.get_tools()
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


# ─────────────────────────────────────────────
# NODE 1 — REASONING AGENT
# ─────────────────────────────────────────────
def reasoning_node(state: AgentState) -> AgentState:
    _print_step("🧠  REASONING AGENT", "blue")

    # First call: decompose the question
    if not state["logic_sentences"]:
        console.print("[blue]  → Decomposing question into logic sentences...[/]")

        prompt = f"""
You are a reasoning agent. Decompose this analytics question into an ordered list of logic sentences.

Rules:
- Each sentence starts with FETCH: or COMPUTE:
- FETCH sentences must name the exact MCP tool to call, chosen from the list below
- COMPUTE sentences describe a calculation on data already saved to temp files — no tool calls
- FETCH sentences always come before the COMPUTE sentences that depend on them
- Only add FETCH steps for data you actually need — do not fetch unnecessary tables
- Keep each sentence short and specific (one action)
- Output ONLY a JSON array of strings, nothing else

AVAILABLE MCP TOOLS most relevant to this question (use exact tool name in every FETCH sentence):
{get_relevant_tools(state["question"], top_k=8)}

Question: {state["question"]}

Output JSON array only:
""".strip()

        response = llm.invoke(prompt)
        raw = response.content.strip()

        # Strip markdown code fences if present
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

    # Error recovery: rephrase current sentence
    if state["error"] and state["ra_retries"] < 3:
        current = _current_sentence(state)
        console.print(f"[yellow]  → Rephrasing step {state['current_idx']+1} after error: {state['error'][:80]}[/]")

        prompt = f"""
The following logic sentence failed with an error.
Rephrase it or choose a different MCP tool.

Original: {current}
Error: {state["error"]}
Already fetched files: {state["temp_files"]}

AVAILABLE MCP TOOLS relevant to this step (use exact tool name):
{get_relevant_tools(current, top_k=8)}

Output only the rephrased sentence (starting with FETCH: or COMPUTE:):
""".strip()

        response = llm.invoke(prompt)
        new_sentence = response.content.strip()
        sentences = state["logic_sentences"].copy()
        sentences[state["current_idx"]] = new_sentence
        console.print(f"[yellow]  → Rephrased: {new_sentence}[/]")

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

    tools = get_mcp_tools()
    agent_llm = llm.bind_tools(tools)

    prompt = f"""
You are a data fetcher. Call the most appropriate MCP tool to fulfill this request.
Fetch ALL pages if the response is paginated.
Return the raw result as-is.

Request: {sentence}
""".strip()

    response = agent_llm.invoke(prompt)

    # Execute tool calls
    all_rows = []
    if hasattr(response, "tool_calls") and response.tool_calls:
        from langchain_core.messages import ToolMessage

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            console.print(f"[green]  → Calling tool: [bold]{tool_name}[/] with {tool_args}[/]")

            # Find and invoke the tool
            tool_fn = next((t for t in tools if t.name == tool_name), None)
            if tool_fn:
                try:
                    result = tool_fn.invoke(tool_args)
                    # Parse result into rows
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

                    all_rows.extend(rows)
                    console.print(f"[green]  → Got {len(rows)} rows[/]")
                except Exception as e:
                    return {**state, "error": f"MCP tool error: {e}"}
    else:
        console.print("[yellow]  → No tool call made, using LLM response as data[/]")
        all_rows = [{"response": response.content}]

    # Save to temp CSV
    idx = state["current_idx"]
    filename = f"{SESSION_DIR}/fetch_{idx}.csv"
    df = pd.json_normalize(all_rows)
    df.to_csv(filename, index=False)
    console.print(f"[green]  → Saved {len(df)} rows → {filename}[/]")

    return {
        **state,
        "temp_files": state["temp_files"] + [filename],
        "error": None,
    }


# ─────────────────────────────────────────────
# NODE 3 — CODING AGENT
# ─────────────────────────────────────────────
def coding_node(state: AgentState) -> AgentState:
    sentence = _current_sentence(state)
    _print_step(f"✍️   CODING AGENT  [step {state['current_idx']+1}]", "magenta", sentence)

    # RAG: retrieve relevant schema
    schema_context = get_relevant_schema(sentence, top_k=5)
    console.print(f"[magenta]  → Retrieved schema context from Chroma[/]")

    # Build file reference string for the prompt
    file_list = "\n".join(
        f"  - '{f}'" for f in state["temp_files"]
    )

    retry_note = ""
    if state["error"] and state["cod_retries"] > 0:
        retry_note = f"\n\nPrevious SQL failed with: {state['error']}\nFix the issue."

    prompt = f"""
You are a SQL coding agent. Write a DuckDB SQL query for this logic:

LOGIC: {sentence}

AVAILABLE CSV FILES (use read_csv_auto() to query them):
{file_list}

RELEVANT SCHEMA (for column name reference):
{schema_context}

Rules:
- Use DuckDB syntax: read_csv_auto('<path>') as the table source
- SELECT only — no INSERT/UPDATE/DELETE
- If computing a percentage, return a single numeric result
- Return ONLY the SQL query, no explanation, no markdown fences
{retry_note}
""".strip()

    response = llm.invoke(prompt)
    sql = response.content.strip()

    # Strip markdown if present
    if sql.startswith("```"):
        parts = sql.split("```")
        sql = parts[1]
        if sql.startswith("sql"):
            sql = sql[3:]
    sql = sql.strip()

    console.print(f"[magenta]  → Generated SQL:[/]")
    console.print(Panel(sql, style="magenta dim", padding=(0, 2)))

    return {**state, "current_sql": sql}


# ─────────────────────────────────────────────
# NODE 4 — EXECUTION LAYER
# ─────────────────────────────────────────────
def execution_node(state: AgentState) -> AgentState:
    _print_step(f"🔧  EXECUTION  [step {state['current_idx']+1}]", "cyan")

    try:
        conn = duckdb.connect()
        result_df = conn.execute(state["current_sql"]).fetchdf()
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
            "cod_retries": 0,
        }

    except Exception as e:
        error_msg = str(e)
        console.print(f"[red]  → Execution error: {error_msg}[/]")
        return {
            **state,
            "error": error_msg,
            "cod_retries": state["cod_retries"] + 1,
        }


# ─────────────────────────────────────────────
# NODE 5 — SYNTHESIZE
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
