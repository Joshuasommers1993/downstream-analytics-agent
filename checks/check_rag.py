"""
Step 2: Test RAG tool retrieval directly.
Run: venv/bin/python3 checks/check_rag.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from agent.schema_rag import get_relevant_tools

questions = [
    "Which cities have the most sellers?",
    "What percentage of users place a second order within 30 days?",
    "What is the drop-off rate from recommendation to payment?",
    "Which products are most popular by industry?",
    "What are the top waste types by order volume?",
]

for q in questions:
    print(f"\n{'='*60}")
    print(f"Q: {q}")
    print(f"{'─'*60}")
    print(get_relevant_tools(q, top_k=5))
