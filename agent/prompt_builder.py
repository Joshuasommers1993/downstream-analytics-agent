"""
Shared formatting helpers for building LLM prompts.

Kept in a separate module to avoid circular imports between nodes.py and tool_selector.py.
"""

from agent.api_fields import API_FIELDS
from agent.schema_fk import FK_MAP


def format_tool_block(name: str, info: dict) -> str:
    """Format one tool entry for the reasoning prompt.

    Outputs:
      tool_name
        -> description
        -> Filters: ...
        -> [source_table]: field, fk_field→target_table, ...

    FK fields are annotated with their target table so the agent understands
    which fields are join keys, e.g.:
        [api_ordergroup]: id, user_address→api_useraddress, user→api_user, ...
    """
    lines = [f"  {name}", f"    -> {info['description']}"]
    if info.get("filters"):
        lines.append(f"    -> Filters: {info['filters']}")

    fields = API_FIELDS.get(name)
    if fields:
        # Group fields by source DB table; annotate FK fields with their target
        by_table: dict[str, list[str]] = {}
        for field_name, source_table in fields.items():
            table_key = source_table or "?"
            # Strip dot-notation prefix to get bare field name for FK lookup
            bare = field_name.split(".")[-1] if "." in field_name else field_name
            fk_target = FK_MAP.get((table_key, bare))
            label = f"{field_name}→{fk_target}" if fk_target else field_name
            by_table.setdefault(table_key, []).append(label)
        for table, cols in by_table.items():
            lines.append(f"    -> [{table}]: {', '.join(cols)}")
    elif info.get("fields"):
        lines.append(f"    -> CSV columns: {info['fields']}")

    return "\n".join(lines)
