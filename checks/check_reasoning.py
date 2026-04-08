"""
Step 3: Run the Reasoning Agent in isolation.
Prints the full prompt sent to GPT-4o and the logic sentences returned.
Run: venv/bin/python3 checks/check_reasoning.py "your question here"
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import json
from dotenv import load_dotenv
from agent.tool_selector import get_relevant_tools

load_dotenv()

import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

question = sys.argv[1] if len(sys.argv) > 1 else "Which cities have the most sellers?"

print(f"\n{'='*60}")
print(f"QUESTION: {question}")
print(f"{'='*60}")

# Build the exact same prompt as reasoning_node
tool_context = get_relevant_tools(question, top_k=8)

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
{tool_context}

Question: {question}

Output JSON array only:
""".strip()

print("\n─── PROMPT SENT TO GPT-4o ───────────────────────────────")
print(prompt)

response = llm.invoke(prompt)
raw = response.content.strip()

print("\n─── RAW RESPONSE ────────────────────────────────────────")
print(raw)

# Parse
if raw.startswith("```"):
    raw = raw.split("```")[1]
    if raw.startswith("json"):
        raw = raw[4:]
raw = raw.strip()

try:
    sentences = json.loads(raw)
except Exception:
    sentences = [l.strip() for l in raw.splitlines() if l.strip().startswith(("FETCH:", "COMPUTE:"))]

print("\n─── LOGIC PLAN ──────────────────────────────────────────")
for i, s in enumerate(sentences):
    print(f"  {i+1}. {s}")

# Step 4 preview: validate tool names
print("\n─── TOOL NAME VALIDATION ────────────────────────────────")
from agent.mcp_catalog import MCP_TOOL_CATALOG
valid_tools = set(MCP_TOOL_CATALOG.keys())

for s in sentences:
    if not s.upper().startswith("FETCH:"):
        continue
    # Try to find a tool name in the sentence
    found = [t for t in valid_tools if t in s]
    if found:
        print(f"  ✅  {s}")
        print(f"       tool: {found[0]}")
    else:
        print(f"  ❌  {s}")
        print(f"       WARNING: no valid tool name found in this sentence")
