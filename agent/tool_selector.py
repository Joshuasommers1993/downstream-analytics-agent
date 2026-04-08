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
    Ask the tool-selector agent which MCP tools to call for this question.
    Returns a formatted string: tool_name + description, same shape as the
    old Chroma RAG output so the Reasoning Agent prompt is unchanged.
    """
    from agent.mcp_catalog import MCP_TOOL_CATALOG

    tool_names = _ask_agent(question)

    # Fallback to Chroma RAG if agent returned nothing
    if not tool_names:
        from agent.schema_rag import get_relevant_tools as rag_fallback
        return rag_fallback(question, top_k=top_k)

    lines = []
    for name in tool_names[:top_k]:
        if name in MCP_TOOL_CATALOG:
            desc = MCP_TOOL_CATALOG[name]["description"]
            lines.append(f"  {name}\n    -> {desc}")
        else:
            # Include even if not in catalog so the agent is aware
            lines.append(f"  {name}\n    -> (no description available)")

    return "\n".join(lines)


def _ask_agent(question: str) -> list[str]:
    """
    Ask the tool-selector agent to name the relevant MCP tools without
    executing them. Parses tool names from the response content.
    Strips the '_mcp_*' suffix the agent appends (e.g. '_mcp_User').
    Returns an empty list on any error.
    """
    prompt = (
        "Without calling or executing any tools, list the MCP tool names that "
        "would provide the raw data to answer this question. "
        "Reply with tool names only, one per line:\n"
        f"{question}"
    )

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
        content = response.json()["choices"][0]["message"].get("content") or ""

        names = []
        for line in content.splitlines():
            line = line.strip()
            if not line or line.lower() == "none":
                continue
            clean = _MCP_SUFFIX.sub("", line)
            if clean:
                names.append(clean)

        return names

    except Exception as e:
        print(f"[tool_selector] Agent call failed: {e}, falling back to RAG")
        return []
