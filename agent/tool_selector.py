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


def get_relevant_tools(question: str, top_k: int = 8) -> str:
    """
    Combine downstream agent tool selection with Chroma RAG.
    - Agent provides domain-aware primary tools
    - RAG fills in related/supporting tools the agent may miss
    Returns a formatted string: tool_name + description.
    """
    from agent.mcp_catalog import MCP_TOOL_CATALOG
    from agent.schema_rag import get_relevant_tools as rag_get

    agent_names = _ask_agent(question)
    rag_result = rag_get(question, top_k=top_k)

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
        return rag_result  # full fallback

    from agent.prompt_builder import format_tool_block

    lines = [format_tool_block(name, MCP_TOOL_CATALOG[name]) for name in merged]
    return "\n".join(lines)


def _ask_agent(question: str) -> list[str]:
    """
    Ask the tool-selector agent to name the relevant MCP tools without
    executing them. Parses tool names from the response content.
    Strips the '_mcp_*' suffix the agent appends (e.g. '_mcp_User').
    Returns an empty list on any error.
    """
    prompt = question

    try:
        response = httpx.post(
            TOOL_SELECTOR_URL,
            headers={
                "Authorization": f"Bearer {TOOL_SELECTOR_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": TOOL_SELECTOR_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
            timeout=30,
        )
        response.raise_for_status()
        message = response.json()["choices"][0]["message"]
        print(message)

        names = []

        # Primary: extract tool names from tool_calls (agent actually chose these)
        for tc in message.get("tool_calls") or []:
            fn_name = tc.get("function", {}).get("name", "")
            clean = _MCP_SUFFIX.sub("", fn_name)
            if clean:
                names.append(clean)

        return names

    except Exception as e:
        print(f"[tool_selector] Agent call failed: {e}, falling back to RAG")
        return []
