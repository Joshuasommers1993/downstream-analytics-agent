"""
Tool selector: returns RAG candidates from Chroma for a given analytics question.

Uses the local Chroma vector store (~50ms) rather than the external agent (1-5s).
The Reasoning Agent then runs a second GPT-4o-mini pass to select the right subset.
"""

from agent.schema_rag import get_relevant_tools as rag_get_relevant_tools


def get_relevant_tools(question: str, top_k: int = 8) -> str:
    """
    Returns top-k tool candidates from Chroma RAG as a formatted string.
    Shape: tool_name + description, one tool per block.
    """
    return rag_get_relevant_tools(question, top_k=top_k)
