"""
Step 3: Run the Reasoning Agent in isolation (two-stage).

Stage 1: GPT-4o selects relevant tools from RAG top-8 candidates.
Stage 2: GPT-4o builds FETCH/COMPUTE plan using only selected tools.

Run: venv/bin/python3 checks/check_reasoning.py "your question here"
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import json
from dotenv import load_dotenv
from agent.tool_selector import get_relevant_tools
from agent.mcp_catalog import MCP_TOOL_CATALOG

load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

question = sys.argv[1] if len(sys.argv) > 1 else "Which cities have the most sellers?"

print(f"\n{'='*60}")
print(f"QUESTION: {question}")
print(f"{'='*60}")

# ── Stage 1: get RAG candidates, then select with GPT-4o ──────────────────────
candidates = get_relevant_tools(question, top_k=8)

print("\n─── STAGE 1: RAG CANDIDATES (top-8) ────────────────────")
print(candidates)

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

Question: {question}

Output JSON array of selected tool names only:
""".strip()

sel_response = llm.invoke(selection_prompt)
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

print(f"\n─── STAGE 1 RESULT: SELECTED TOOLS ─────────────────────")
for t in selected_tools:
    status = "✅" if t in MCP_TOOL_CATALOG else "❌ NOT IN CATALOG"
    print(f"  {status}  {t}")

# Build focused tool block
focused_tools = "\n".join(
    f"  {t}\n    -> {MCP_TOOL_CATALOG[t]['description']}"
    for t in selected_tools if t in MCP_TOOL_CATALOG
) or candidates  # fallback to full candidates if selection fails

# ── Stage 2: build FETCH/COMPUTE plan ────────────────────────────────────────
plan_prompt = f"""
You are a reasoning agent. Decompose this analytics question into an ordered list of logic sentences.

Rules:
- Each sentence starts with FETCH: or COMPUTE:
- FETCH sentences must name the exact MCP tool to call, chosen from the list below
- COMPUTE sentences describe a calculation on data already saved to temp files — no tool calls
- FETCH sentences always come before the COMPUTE sentences that depend on them
- Only add FETCH steps for data you actually need — do not fetch unnecessary tables
- Keep each sentence short and specific (one action)
- Output ONLY a JSON array of strings, nothing else

AVAILABLE MCP TOOLS (use exact tool name in every FETCH sentence):
{focused_tools}

Question: {question}

Output JSON array only:
""".strip()

print("\n─── STAGE 2 PROMPT ──────────────────────────────────────")
print(plan_prompt)

response = llm.invoke(plan_prompt)
raw = response.content.strip()

print("\n─── STAGE 2 RAW RESPONSE ────────────────────────────────")
print(raw)

if raw.startswith("```"):
    raw = raw.split("```")[1]
    if raw.startswith("json"):
        raw = raw[4:]
raw = raw.strip()

try:
    sentences = json.loads(raw)
except Exception:
    sentences = [l.strip() for l in raw.splitlines() if l.strip().startswith(("FETCH:", "COMPUTE:"))]

print("\n─── FINAL LOGIC PLAN ────────────────────────────────────")
for i, s in enumerate(sentences):
    print(f"  {i+1}. {s}")

# Validate tool names
print("\n─── TOOL NAME VALIDATION ────────────────────────────────")
valid_tools = set(MCP_TOOL_CATALOG.keys())

for s in sentences:
    if not s.upper().startswith("FETCH:"):
        continue
    found = [t for t in valid_tools if t in s]
    if found:
        print(f"  ✅  {s}")
        print(f"       tool: {found[0]}")
    else:
        print(f"  ❌  {s}")
        print(f"       WARNING: no valid tool name found in this sentence")
