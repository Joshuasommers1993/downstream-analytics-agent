"""
Step 3: Run the Reasoning Agent in isolation (two-stage, SQL-embedded COMPUTE).

Stage 1: gpt-4o-mini selects relevant tools from RAG top-8 candidates.
Stage 2: gpt-4o builds FETCH/COMPUTE plan where COMPUTE steps contain DuckDB SQL with FETCH_N placeholders.

Run: venv/bin/python3 checks/check_reasoning.py "your question here"
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from dotenv import load_dotenv
from agent.tool_selector import get_relevant_tools
from agent.mcp_catalog import MCP_TOOL_CATALOG

load_dotenv()

from langchain_openai import ChatOpenAI

llm_mini = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), temperature=0)
llm      = ChatOpenAI(model="gpt-4o",      api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

question = sys.argv[1] if len(sys.argv) > 1 else "Which cities have the most sellers?"

print(f"\n{'='*60}")
print(f"QUESTION: {question}")
print(f"{'='*60}")


def _format_tool_block(name, info):
    lines = [f"  {name}", f"    -> {info['description']}"]
    if "fields" in info:
        lines.append(f"    -> CSV columns: {info['fields']}")
    return "\n".join(lines)


# ── Stage 1: RAG candidates → mini selects ───────────────────────────────────
candidates = get_relevant_tools(question, top_k=8)

print("\n─── STAGE 1: RAG CANDIDATES (top-8) ────────────────────")
for line in candidates.splitlines():
    if line.strip().startswith("->"):
        desc = line.strip()[2:].strip()
        print(f"       {desc[:100]}{'...' if len(desc) > 100 else ''}")
    else:
        print(f"  {line.strip()}")

selection_prompt = f"""
You are a tool selector. Given an analytics question and a list of candidate MCP tools,
choose only the tools actually needed to answer the question.

Rules:
- Read each tool description carefully
- Select only tools whose data directly answers the question
- Prefer pre-computed analytics endpoints (insight_hub) when available
- Output a JSON array of tool names only, nothing else
- Include all tools if multiple fetches are needed

CANDIDATE TOOLS:
{candidates}

Question: {question}

Output JSON array of selected tool names only:
""".strip()

sel_raw = llm_mini.invoke(selection_prompt).content.strip()
if sel_raw.startswith("```"):
    sel_raw = sel_raw.split("```")[1]
    if sel_raw.startswith("json"):
        sel_raw = sel_raw[4:]
sel_raw = sel_raw.strip()
try:
    selected_tools = json.loads(sel_raw)
except Exception:
    selected_tools = [t.strip() for t in sel_raw.splitlines() if t.strip()]

print(f"\n─── STAGE 1 RESULT: SELECTED TOOLS ─────────────────────")
for t in selected_tools:
    status = "✅" if t in MCP_TOOL_CATALOG else "❌ NOT IN CATALOG"
    print(f"  {status}  {t}")

# Build focused tool block with field schemas
focused_tools = "\n".join(
    _format_tool_block(t, MCP_TOOL_CATALOG[t])
    for t in selected_tools if t in MCP_TOOL_CATALOG
) or candidates

# ── Stage 2: build FETCH/COMPUTE plan with SQL ────────────────────────────────
plan_prompt = f"""
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

Question: {question}

Output JSON array only:
""".strip()

print(f"\n─── STAGE 2 FOCUSED TOOLS ───────────────────────────────")
print(focused_tools)

raw = llm.invoke(plan_prompt).content.strip()
if raw.startswith("```"):
    raw = raw.split("```")[1]
    if raw.startswith("json"):
        raw = raw[4:]
raw = raw.strip()

try:
    sentences = json.loads(raw)
except Exception:
    sentences = [l.strip() for l in raw.splitlines() if l.strip().startswith(("FETCH:", "COMPUTE:"))]

print(f"\n─── FINAL LOGIC PLAN ────────────────────────────────────")
for i, s in enumerate(sentences):
    print(f"  {i+1}. {s}")

# Validate
print(f"\n─── VALIDATION ──────────────────────────────────────────")
valid_tools = set(MCP_TOOL_CATALOG.keys())
for s in sentences:
    if s.upper().startswith("FETCH:"):
        found = [t for t in valid_tools if t in s]
        if found:
            print(f"  ✅ FETCH → tool: {found[0]}")
        else:
            print(f"  ❌ FETCH → WARNING: no valid tool name in: {s}")
    elif s.upper().startswith("COMPUTE:"):
        sql = s[len("COMPUTE:"):].strip()
        has_select = "SELECT" in sql.upper()
        has_fetch = any(f"FETCH_{n}" in sql for n in range(10))
        status = "✅" if has_select else "⚠️ "
        fetch_note = "(uses FETCH_N placeholder)" if has_fetch else "(no FETCH_N placeholder — may use hardcoded path?)"
        print(f"  {status} COMPUTE SQL: {sql[:80]}{'...' if len(sql) > 80 else ''}")
        print(f"     {fetch_note}")
