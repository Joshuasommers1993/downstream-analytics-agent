# Analytics Agent

A natural language analytics system that turns questions into data pipelines. Ask a question in plain English — the agent finds the right API endpoints, fetches the data, runs SQL, and returns a human-readable answer.

```
> ask "Which product categories have the most sellers?"

  ✅ Final Answer
  The top 3 product categories by seller count are:
  1. Roll Off Dumpsters — 1,842 sellers
  2. Portable Restrooms — 1,205 sellers
  3. Storage Containers — 987 sellers
```

## How It Works

```
Question
  │
  ▼
RAG (Chroma) → top-8 relevant tools
  │
  ▼
Stage 1 (gpt-4o-mini) → select needed tools
  │
  ▼
Stage 2 (gpt-4o) → build FETCH/COMPUTE plan with embedded SQL
  │
  ├── FETCH steps  → direct HTTP to Downstream API → CSV
  └── COMPUTE steps → DuckDB SQL on CSVs (FETCH_N placeholders)
  │
  ▼
Synthesize (gpt-4o) → human-readable answer
```

**Error recovery:** if a FETCH or SQL step fails, the reasoning agent rewrites that step and retries (max 3 times).

## Setup

```bash
python -m venv venv
venv/bin/pip install -r requirements.txt
cp .env.example .env  # fill in API keys
```

Required `.env` values:

```
OPENAI_API_KEY=...
MCP_SERVER_URL=https://mcp.trydownstream.com/mcp
MCP_API_KEY=...
DOWNSTREAM_API_URL=https://api.trydownstream.com
INSIGHT_HUB_API_KEY=...
CHROMA_PERSIST_DIR=./schema_db
```

## Usage

```bash
# Interactive REPL
./ask

# One-shot
./ask "How many products are there?"

# Or directly
venv/bin/python3 main.py "Which cities have the most seller locations?"
```

Add to PATH for use from anywhere:

```bash
export PATH="/path/to/analytics-agent:$PATH"
```

## Architecture

### Nodes

| Node | Role |
|------|------|
| `reasoning_node` | Decomposes question into FETCH/COMPUTE plan; recovers from errors |
| `mcp_fetch_node` | Fetches data from Downstream API (direct HTTP for GET, MCP for mutations) |
| `execution_node` | Substitutes FETCH_N placeholders and runs DuckDB SQL |
| `synthesize_node` | Writes final answer from accumulated step results |

### Graph Flow

```
reasoning → route → mcp_fetch → reasoning → ...
reasoning → route → execution → reasoning → ...
reasoning → route → synthesize → END
```

### MCP Tool Catalog

141 Downstream API endpoints annotated with:
- Path, HTTP method
- Description (used for RAG embeddings)
- CSV field schema (column names + types)
- `requires_id` flag for per-resource endpoints

Tools fall into 4 groups:
- **Enrichment** — phone reveal, suggested coworkers
- **Insight Hub** — pre-computed analytics (revenue, funnel, take rate, cohorts)
- **Raw data** — orders, sellers, products, users, locations
- **Operations** — user groups, compliance, inventory

### RAG Index

Two Chroma collections built at startup:
- `schema` — 87 DB table definitions (for schema-aware SQL)
- `tools` — 141 MCP tool descriptions (for tool selection)

Embeddings: `sentence-transformers/all-MiniLM-L6-v2` (~50ms query latency)

### Data Fetching

- **Pagination:** cursor-based (`starting_after` + `limit=100`), capped at 10,000 rows
- **Auth routing:** insight-hub endpoints use `INSIGHT_HUB_API_KEY`; all others use `MCP_API_KEY`
- **Response shapes handled:** Stripe-style `{data: [...]}`, DRF `{results: [...]}`, insight-hub `{rows: [...]}`, bare arrays, single objects
- **Output:** `pd.json_normalize()` → flat CSV per fetch step

## Project Structure

```
analytics-agent/
├── main.py                  # Entry point
├── ask                      # CLI (interactive + one-shot)
├── requirements.txt
├── agent/
│   ├── graph.py             # LangGraph state machine
│   ├── nodes.py             # Node implementations
│   ├── state.py             # AgentState TypedDict
│   ├── schema_rag.py        # Chroma index build + query
│   ├── tool_selector.py     # RAG wrapper for tool retrieval
│   └── mcp_catalog.py       # 141 annotated MCP tools
├── schema/
│   └── tables.py            # Downstream DB schema definitions
└── checks/                  # Debugging scripts
    ├── check_rag.py
    ├── check_reasoning.py
    └── check_rag_answers.py
```

## Debugging

```bash
# Check RAG retrieval for a question
venv/bin/python3 checks/check_rag.py "your question"

# Check full reasoning output (plan + validation)
venv/bin/python3 checks/check_reasoning.py "your question"
```
