"""
RAG vs Agent reliability check — 20 analytics questions.

For each question:
  - RAG:   top-3 tools from Chroma (local, ~50ms)
  - Agent: tool names returned by the tool-selector agent (~1-2s)

Prints a side-by-side comparison and a final agreement summary.

Run: venv/bin/python3 checks/check_rag_vs_agent.py
"""
import sys, os, time, re
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import httpx
from dotenv import load_dotenv
load_dotenv()

from agent.schema_rag import get_relevant_tools as rag_tools
from agent.tool_selector import _ask_agent
from agent.mcp_catalog import MCP_TOOL_CATALOG

QUESTIONS = [
    # Orders / retention
    "What percentage of user groups place a second order within 30 days of their first?",
    "How many orders were placed last month?",
    "What is the average order value by product type?",
    "Which orders are currently scheduled but not yet completed?",

    # Sellers / geography
    "Which cities have the most seller locations?",
    "How many active sellers are there per state?",
    "Which sellers have the most product listings?",

    # Revenue / finance
    "What is the total GMV month-over-month for the last 6 months?",
    "What is the platform take rate trend over the past year?",
    "Which sales reps are hitting their quota this month?",
    "What is the drop-off rate at each stage of the sales funnel?",

    # Products / catalog
    "Which products are most popular in the construction industry?",
    "What are the top waste types by order volume?",
    "Which product categories generate the most revenue?",

    # Accounts / users
    "Which customer accounts have the highest monthly spend?",
    "How many new accounts were acquired this quarter?",
    "Which accounts have churned in the last 90 days?",

    # Invoices / billing
    "What is the total outstanding invoice balance across all accounts?",
    "Which accounts have overdue invoices?",

    # Mixed
    "What is the conversion rate from cart to confirmed order?",
]

_MCP_SUFFIX = re.compile(r"_mcp_\w+$")

AGENT_URL   = os.getenv("TOOL_SELECTOR_URL")
AGENT_KEY   = os.getenv("TOOL_SELECTOR_KEY")
AGENT_MODEL = os.getenv("TOOL_SELECTOR_MODEL")

def ask_agent_raw(question: str) -> list[str]:
    prompt = (
        "Without calling or executing any tools, list the MCP tool names that "
        "would provide the raw data to answer this question. "
        "Reply with tool names only, one per line:\n"
        f"{question}"
    )
    try:
        r = httpx.post(
            AGENT_URL,
            headers={"Authorization": f"Bearer {AGENT_KEY}", "Content-Type": "application/json"},
            json={"model": AGENT_MODEL, "messages": [{"role": "user", "content": prompt}], "stream": False},
            timeout=30,
        )
        r.raise_for_status()
        content = r.json()["choices"][0]["message"].get("content") or ""
        names = []
        for line in content.splitlines():
            line = line.strip()
            if not line or line.lower() in ("none", "n/a", ""):
                continue
            clean = _MCP_SUFFIX.sub("", line)
            if clean:
                names.append(clean)
        return names
    except Exception as e:
        return [f"ERROR: {e}"]


def rag_top3(question: str) -> list[str]:
    block = rag_tools(question, top_k=3)
    names = []
    for line in block.splitlines():
        line = line.strip()
        if line and not line.startswith("->"):
            names.append(line)
    return names


AGREE  = "✅"
PARTIAL = "🟡"
MISS   = "❌"

def compare(rag: list[str], agent: list[str]) -> str:
    if not agent:
        return "⚪ agent returned nothing"
    rag_set   = set(rag)
    agent_set = set(agent)
    overlap   = rag_set & agent_set
    if overlap == agent_set or overlap == rag_set:
        return f"{AGREE}  full match: {sorted(overlap)}"
    if overlap:
        return f"{PARTIAL} partial ({len(overlap)}/{len(agent_set)} agent tools in RAG top-3): {sorted(overlap)}"
    return f"{MISS}  no overlap  RAG={sorted(rag_set)}  Agent={sorted(agent_set)}"


agree_count   = 0
partial_count = 0
miss_count    = 0
no_agent      = 0

print(f"\n{'='*70}")
print(f"  RAG vs Agent — {len(QUESTIONS)} questions")
print(f"{'='*70}\n")

for i, q in enumerate(QUESTIONS, 1):
    t0 = time.time()
    rag   = rag_top3(q)
    t_rag = time.time() - t0

    t0 = time.time()
    agent = ask_agent_raw(q)
    t_agent = time.time() - t0

    verdict = compare(rag, agent)

    print(f"Q{i:02d}: {q}")
    print(f"  RAG   ({t_rag*1000:.0f}ms): {rag}")
    print(f"  Agent ({t_agent*1000:.0f}ms): {agent}")
    print(f"  → {verdict}")
    print()

    if "full match" in verdict:
        agree_count += 1
    elif "partial" in verdict:
        partial_count += 1
    elif "agent returned nothing" in verdict:
        no_agent += 1
    else:
        miss_count += 1

total = len(QUESTIONS)
print(f"{'='*70}")
print(f"  SUMMARY ({total} questions)")
print(f"  ✅  Full match:          {agree_count:2d} / {total}")
print(f"  🟡  Partial match:       {partial_count:2d} / {total}")
print(f"  ❌  No overlap:          {miss_count:2d} / {total}")
print(f"  ⚪  Agent returned none: {no_agent:2d} / {total}")
print(f"{'='*70}\n")
