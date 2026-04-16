"""
Tool selector: calls the downstream agent to determine which MCP tools
to use for a given analytics question.

The agent responds with tool_calls[] containing the tools it would invoke.
We extract those names, strip the '_mcp_*' suffix, and match against our
local catalog to return a formatted tool list for the Reasoning Agent prompt.

Falls back to Chroma RAG if the agent returns no tool_calls.
"""

import os
import re
import httpx
from dotenv import load_dotenv

load_dotenv()

TOOL_SELECTOR_URL = os.getenv("TOOL_SELECTOR_URL", "https://chat.trydownstream.com/api/agents/v1/chat/completions")
TOOL_SELECTOR_KEY = os.getenv("TOOL_SELECTOR_KEY", "")
TOOL_SELECTOR_MODEL = os.getenv("TOOL_SELECTOR_MODEL", "")

_MCP_SUFFIX = re.compile(r"_mcp_\w+$")

_PROMPT_TEMPLATE = """\
You are an analytics planning assistant for the Downstream platform.

Your job: given an analytics question, output a structured analytical plan that a SQL execution engine will use. The engine has access to the actual database schema — do NOT include column names, table names, or SQL syntax. Describe pure intent only.

Output this exact format, nothing else:

Metric: [one sentence — what value is being measured and why it answers the question]

Grain: [one sentence — unit of analysis; what one row in the final result represents]

Logic:
  step 1 — [plain English description of the first data transformation needed]
  step 2 — [next transformation]
  step 3 — [continue until the final output is fully described]
  final  — [output shape: what columns, what order]

RAG query: [1-2 phrases describing the data sources needed, written to match API tool descriptions — e.g. "completed order history per customer, product catalog for UUID resolution"]

Rules:
- No column names, no table names, no SQL keywords
- No offers, no options, no questions back to the user
- No hedging ("you could", "one approach is") — one definitive plan
- If a rate or percentage is the right metric, say so explicitly in Logic final step
- If the question requires joining data from multiple sources, name those sources in plain English (e.g. "orders" and "product catalog"), not as table names
- RAG query must be compact (1-2 phrases), specific to the data sources needed, not a restatement of the question

Question: {question}"""


def _build_prompt(question: str) -> str:
    return _PROMPT_TEMPLATE.format(question=question)


def get_relevant_tools(question: str, top_k: int = 8) -> tuple[str, str]:
    """
    Combine downstream agent tool selection with Chroma RAG.
    - Agent provides domain-aware primary tools
    - RAG fills in related/supporting tools the agent may miss

    Returns (tool_blocks, agent_reasoning):
      tool_blocks    — formatted string: tool_name + fields + filters
      agent_reasoning — full Metric/Grain/Logic from Stage 1 (may be empty string)
    """
    from agent.mcp_catalog import MCP_TOOL_CATALOG
    from agent.schema_rag import get_relevant_tools as rag_get

    agent_names, agent_reasoning, rag_query = _ask_agent(question)
    # RAG query: use dedicated compact line from Stage 1 > full reasoning > raw question
    rag_result = rag_get(rag_query or agent_reasoning or question, top_k=top_k)

    # Parse RAG tool names from its formatted output
    rag_names = [
        line.strip()
        for line in rag_result.splitlines()
        if line.strip() and not line.strip().startswith("->")
    ]

    # Merge: agent first, then RAG additions, deduplicated, capped at top_k
    seen = set()
    merged = []
    for name in agent_names + rag_names:
        if name not in seen and name in MCP_TOOL_CATALOG:
            seen.add(name)
            merged.append(name)
        if len(merged) >= top_k:
            break

    if not merged:
        return rag_result, agent_reasoning  # full fallback (two-tuple: tool_blocks, reasoning)

    from agent.prompt_builder import format_tool_block

    lines = [format_tool_block(name, MCP_TOOL_CATALOG[name]) for name in merged]
    return "\n".join(lines), agent_reasoning


def _ask_agent(question: str) -> tuple[list[str], str]:
    """
    Ask the tool-selector agent to name the relevant MCP tools without
    executing them. Parses tool names from tool_calls and captures any
    analytical reasoning from the content field.

    Returns (names, reasoning):
      names     — list of MCP tool name strings (may be empty)
      reasoning — prose/SQL from the agent's content field (may be empty string)
    """
    try:
        response = httpx.post(
            TOOL_SELECTOR_URL,
            headers={
                "Authorization": f"Bearer {TOOL_SELECTOR_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": TOOL_SELECTOR_MODEL,
                "messages": [{"role": "user", "content": _build_prompt(question)}],
                "stream": False,
            },
            timeout=30,
        )
        response.raise_for_status()
        message = response.json()["choices"][0]["message"]

        names = []
        # Primary: extract tool names from tool_calls (agent actually chose these)
        for tc in message.get("tool_calls") or []:
            fn_name = tc.get("function", {}).get("name", "")
            clean = _MCP_SUFFIX.sub("", fn_name)
            if clean:
                names.append(clean)

        content = (message.get("content") or "").strip()

        # Extract dedicated RAG query line if present (separate from full reasoning)
        rag_query = ""
        if content:
            for line in content.splitlines():
                if line.lower().startswith("rag query:"):
                    rag_query = line[len("rag query:"):].strip()
                    break

        return names, content, rag_query

    except Exception as e:
        print(f"[tool_selector] Agent call failed: {e}, falling back to RAG")
        return [], "", ""
