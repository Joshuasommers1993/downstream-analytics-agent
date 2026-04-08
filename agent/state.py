from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    # Input
    question: str

    # Reasoning layer
    logic_sentences: List[str]          # e.g. ["FETCH: get all sellers", "COMPUTE: count by city"]
    current_idx: int                    # which sentence we're on

    # MCP fetch layer
    temp_files: List[str]               # paths of saved CSVs per FETCH step

    # Coding layer
    current_sql: str                    # SQL written for current COMPUTE step

    # Execution layer
    step_results: List[str]             # accumulated scalar results per step

    # Retry counters
    ra_retries: int                     # reasoning agent retries
    cod_retries: int                    # coding agent retries

    # Error passing
    error: Optional[str]

    # Final
    final_answer: Optional[str]
