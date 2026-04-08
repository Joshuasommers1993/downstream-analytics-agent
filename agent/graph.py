"""
Builds and compiles the LangGraph state machine.
"""

from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import (
    reasoning_node,
    mcp_fetch_node,
    coding_node,
    execution_node,
    synthesize_node,
)

MAX_RA_RETRIES  = 3
MAX_COD_RETRIES = 3


# ─────────────────────────────────────────────
# ROUTING FUNCTIONS  (the diamonds in the diagram)
# ─────────────────────────────────────────────

def route_sentence_type(state: AgentState) -> str:
    """After reasoning: decide FETCH vs COMPUTE for current sentence."""
    sentences = state["logic_sentences"]
    idx = state["current_idx"]

    if idx >= len(sentences):
        return "synthesize"

    sentence = sentences[idx]
    if sentence.upper().startswith("FETCH"):
        return "mcp_fetch"
    return "coding"


def route_after_reasoning(state: AgentState) -> str:
    """After reasoning node: give up if too many retries, else route sentence."""
    if state["error"] and state["ra_retries"] >= MAX_RA_RETRIES:
        return "fail"
    return "route_sentence"


def route_after_execution(state: AgentState) -> str:
    """After execution: retry coding, escalate to reasoning, or advance."""
    if state["error"]:
        if state["cod_retries"] < MAX_COD_RETRIES:
            return "coding"          # fix SQL, retry
        return "reasoning"           # escalate — RA rephrases the logic

    idx = state["current_idx"]
    if idx < len(state["logic_sentences"]):
        return "reasoning"           # next sentence
    return "synthesize"              # all steps done


def route_after_fetch(state: AgentState) -> str:
    """After MCP fetch: error → reasoning escalation, else next step."""
    if state["error"]:
        return "reasoning"
    return "reasoning"               # always back to RA to send next sentence


# ─────────────────────────────────────────────
# BUILD THE GRAPH
# ─────────────────────────────────────────────

def build_graph():
    g = StateGraph(AgentState)

    g.add_node("reasoning",  reasoning_node)
    g.add_node("mcp_fetch",  mcp_fetch_node)
    g.add_node("coding",     coding_node)
    g.add_node("execution",  execution_node)
    g.add_node("synthesize", synthesize_node)

    # Entry point
    g.set_entry_point("reasoning")

    # Reasoning → route or fail
    g.add_conditional_edges("reasoning", route_after_reasoning, {
        "route_sentence": "route_sentence_type",   # virtual routing node
        "fail": END,
    })

    # Routing diamond: FETCH or COMPUTE?
    g.add_conditional_edges("route_sentence_type", route_sentence_type, {
        "mcp_fetch":  "mcp_fetch",
        "coding":     "coding",
        "synthesize": "synthesize",
    })

    # MCP fetch → back to reasoning (to process next sentence or handle error)
    g.add_conditional_edges("mcp_fetch", route_after_fetch, {
        "reasoning": "reasoning",
    })

    # Coding → execution
    g.add_edge("coding", "execution")

    # Execution → coding retry | reasoning escalate | synthesize
    g.add_conditional_edges("execution", route_after_execution, {
        "coding":    "coding",
        "reasoning": "reasoning",
        "synthesize":"synthesize",
    })

    # Synthesize → done
    g.add_edge("synthesize", END)

    # Add virtual routing node (needed for conditional edge source)
    g.add_node("route_sentence_type", lambda s: s)   # pass-through

    return g.compile()
