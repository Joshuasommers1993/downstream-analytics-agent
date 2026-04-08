from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    # Input
    question: str

    # Reasoning layer
    logic_sentences: List[str]          # ["FETCH: tool_name ...", "COMPUTE: SELECT ..."]
    current_idx: int                    # which sentence we're on

    # MCP fetch layer
    temp_files: List[str]               # paths of saved CSVs, indexed by fetch order (FETCH_0, FETCH_1, ...)

    # Execution layer
    step_results: List[str]             # accumulated results per COMPUTE step

    # Retry counter
    ra_retries: int                     # reasoning agent retries (covers both FETCH and SQL errors)

    # Error passing
    error: Optional[str]

    # Final
    final_answer: Optional[str]
