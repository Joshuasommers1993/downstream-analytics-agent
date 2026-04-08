"""
RAG tool selection answers for manual review — 20 questions.
Shows question, top-3 RAG tools, and why each tool is relevant.

Run: venv/bin/python3 checks/check_rag_answers.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from agent.schema_rag import get_relevant_tools as rag_tools
from agent.mcp_catalog import MCP_TOOL_CATALOG

QUESTIONS = [
    "What percentage of user groups place a second order within 30 days of their first?",
    "How many orders were placed last month?",
    "What is the average order value by product type?",
    "Which orders are currently scheduled but not yet completed?",
    "Which cities have the most seller locations?",
    "How many active sellers are there per state?",
    "Which sellers have the most product listings?",
    "What is the total GMV month-over-month for the last 6 months?",
    "What is the platform take rate trend over the past year?",
    "Which sales reps are hitting their quota this month?",
    "What is the drop-off rate at each stage of the sales funnel?",
    "Which products are most popular in the construction industry?",
    "What are the top waste types by order volume?",
    "Which product categories generate the most revenue?",
    "Which customer accounts have the highest monthly spend?",
    "How many new accounts were acquired this quarter?",
    "Which accounts have churned in the last 90 days?",
    "What is the total outstanding invoice balance across all accounts?",
    "Which accounts have overdue invoices?",
    "What is the conversion rate from cart to confirmed order?",
]

for i, q in enumerate(QUESTIONS, 1):
    print(f"Q{i:02d}: {q}")
    block = rag_tools(q, top_k=3)
    rank = 1
    for line in block.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("->"):
            # trim long descriptions
            desc = line[2:].strip()
            if len(desc) > 120:
                desc = desc[:120] + "..."
            print(f"       {desc}")
        else:
            print(f"  [{rank}] {line}")
            rank += 1
    print()
