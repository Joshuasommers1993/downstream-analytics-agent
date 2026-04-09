"""
Chroma RAG for two collections:
  - "schema"  : DB table definitions  → used by Coding Agent
  - "tools"   : MCP tool catalog      → used by Reasoning Agent

Build both indexes:
    python -m agent.schema_rag

Query at runtime:
    from agent.schema_rag import get_relevant_schema, get_relevant_tools
"""

import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./schema_db")


# ── shared Chroma client + embedding function ─────────────────────────────────

def _get_ef():
    from chromadb.utils import embedding_functions
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )


def _get_schema_collection():
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_or_create_collection("schema", embedding_function=_get_ef())


def _get_tools_collection():
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_or_create_collection("tools", embedding_function=_get_ef())


# ── BUILD INDEXES ─────────────────────────────────────────────────────────────

def build_schema_index():
    from schema.tables import SCHEMA

    collection = _get_schema_collection()
    existing = set(collection.get()["ids"])

    docs, ids, metas = [], [], []
    for table_name, info in SCHEMA.items():
        if table_name in existing:
            continue
        cols = "\n  ".join(info["columns"])
        text = f"Table: {table_name}\nDescription: {info['description']}\nColumns:\n  {cols}"
        docs.append(text)
        ids.append(table_name)
        metas.append({"table": table_name})

    if docs:
        collection.add(documents=docs, ids=ids, metadatas=metas)
        print(f"[schema_rag] Indexed {len(docs)} tables → {CHROMA_DIR}/schema")
    else:
        print(f"[schema_rag] Schema index up to date ({len(existing)} tables)")


def build_tools_index():
    from agent.mcp_catalog import MCP_TOOL_CATALOG

    collection = _get_tools_collection()
    existing = set(collection.get()["ids"])

    docs, ids, metas = [], [], []
    for tool_name, info in MCP_TOOL_CATALOG.items():
        if tool_name in existing:
            continue
        # embed: tool name + path + description together for richer matching
        text = f"Tool: {tool_name}\nPath: {info['path']}\nDescription: {info['description']}"
        docs.append(text)
        ids.append(tool_name)
        metas.append({"tool": tool_name, "path": info["path"] or ""})

    if docs:
        collection.add(documents=docs, ids=ids, metadatas=metas)
        print(f"[schema_rag] Indexed {len(docs)} tools → {CHROMA_DIR}/tools")
    else:
        print(f"[schema_rag] Tools index up to date ({len(existing)} tools)")


def build_index():
    build_schema_index()
    build_tools_index()


# ── QUERY HELPERS ─────────────────────────────────────────────────────────────

def get_relevant_schema(logic_sentence: str, top_k: int = 5) -> str:
    """Return a compact schema block for the top-k tables relevant to a logic sentence."""
    from schema.tables import SCHEMA

    collection = _get_schema_collection()
    results = collection.query(query_texts=[logic_sentence], n_results=top_k)
    table_names = results["ids"][0]

    lines = []
    for t in table_names:
        if t not in SCHEMA:
            continue
        cols = ", ".join(SCHEMA[t]["columns"])
        lines.append(f"  {t}: {cols}")

    return "\n".join(lines)


def get_relevant_tools(question: str, top_k: int = 8) -> str:
    """Return a short tool list (name + description) relevant to the question.

    Injects ~10 lines into the Reasoning Agent prompt instead of 500.
    """
    from agent.mcp_catalog import MCP_TOOL_CATALOG

    collection = _get_tools_collection()
    results = collection.query(query_texts=[question], n_results=top_k)
    tool_names = results["ids"][0]

    lines = []
    for t in tool_names:
        if t not in MCP_TOOL_CATALOG:
            continue
        desc = MCP_TOOL_CATALOG[t]["description"]
        lines.append(f"  {t}\n    -> {desc}")

    return "\n".join(lines)


if __name__ == "__main__":
    build_index()
