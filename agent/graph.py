"""
Builds and compiles the LangGraph state machine.

Flow:
  reasoning → route → mcp_fetch (FETCH steps) → reasoning → ...
  reasoning → route → execution (COMPUTE steps) → reasoning → ...
  reasoning → synthesize (when all steps done)

SQL is embedded in COMPUTE sentences by the reasoning agent.
The coding node has been removed — no separate SQL generation step.
"""

from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import (
    reasoning_node,
    mcp_fetch_node,
    execution_node,
    synthesize_node,
)

MAX_RA_RETRIES = 3


# ─────────────────────────────────────────────
# ROUTING FUNCTIONS
# ─────────────────────────────────────────────

def route_sentence_type(state: AgentState) -> str:
    """Decide FETCH vs COMPUTE vs done for the current sentence."""
    sentences = state["logic_sentences"]
    idx = state["current_idx"]

    if idx >= len(sentences):
        return "synthesize"

    sentence = sentences[idx]
    if sentence.upper().startswith("FETCH"):
        return "mcp_fetch"
    return "execution"  # COMPUTE goes directly to execution (SQL is already in the sentence)


def route_after_reasoning(state: AgentState) -> str:
    """After reasoning: give up on too many retries, else route to next sentence."""
    if state.get("final_answer"):
        return "fail"  # impossible verdict — final_answer already set, skip to END
    if state["error"] and state["ra_retries"] >= MAX_RA_RETRIES:
        return "fail"
    return "route_sentence"


def route_after_fetch(state: AgentState) -> str:
    """After MCP fetch: error → reasoning (for rephrase), else check next sentence."""
    if state["error"]:
        return "reasoning"
    if state["current_idx"] < len(state["logic_sentences"]):
        return "reasoning"
    return "synthesize"


def route_after_execution(state: AgentState) -> str:
    """After execution: error → reasoning (to fix SQL), else next sentence or done."""
    if state["error"]:
        return "reasoning"
    if state["current_idx"] < len(state["logic_sentences"]):
        return "reasoning"
    return "synthesize"


# ─────────────────────────────────────────────
# BUILD THE GRAPH
# ─────────────────────────────────────────────

def build_graph():
    g = StateGraph(AgentState)

    g.add_node("reasoning",           reasoning_node)
    g.add_node("mcp_fetch",           mcp_fetch_node)
    g.add_node("execution",           execution_node)
    g.add_node("synthesize",          synthesize_node)
    g.add_node("route_sentence_type", lambda s: s)   # pass-through routing node

    # Entry point
    g.set_entry_point("reasoning")

    # Reasoning → route or fail
    g.add_conditional_edges("reasoning", route_after_reasoning, {
        "route_sentence": "route_sentence_type",
        "fail": END,
    })

    # Routing: FETCH, COMPUTE (execution), or done
    g.add_conditional_edges("route_sentence_type", route_sentence_type, {
        "mcp_fetch":  "mcp_fetch",
        "execution":  "execution",
        "synthesize": "synthesize",
    })

    # MCP fetch → reasoning (next sentence or rephrase on error)
    g.add_conditional_edges("mcp_fetch", route_after_fetch, {
        "reasoning":  "reasoning",
        "synthesize": "synthesize",
    })

    # Execution → reasoning (next sentence or fix SQL) or synthesize
    g.add_conditional_edges("execution", route_after_execution, {
        "reasoning":  "reasoning",
        "synthesize": "synthesize",
    })

    # Synthesize → done
    g.add_edge("synthesize", END)

    return g.compile()
