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

## Golden Dataset

Track progress per branch — update ✅ / ❌ as you test each question.

| # | Question | Status |
|---|----------|:------:|
| 1 | What percentage of UserGroups place a second OrderGroup within 30 days of their first? | ❌ |
| 2 | How does retention vary by first MainProduct ordered? | ❌ |
| 3 | Do UserGroups from META_ADS have higher invoice delinquency rates than GOOGLE? | ❌ |
| 4 | Which Sellers have the best performance on high-confidence recommendations? | ❌ |
| 5 | What is the drop-off rate from recommendation -> OrderGroup -> Invoice -> Payment? | ❌ |
| 6 | Where is the biggest bottleneck in the order lifecycle? | ❌ |
| 7 | Which metrics changed the most week-over-week? | ❌ |
| 8 | Which SellerLocations had an abnormal spike in cancellations this month? | ❌ |
| 9 | Which zip codes have the highest ratio of UserAddresses to SellerLocations? | ❌ |
| 10 | Where are we supply constrained for dumpsters vs toilets? | ❌ |
| 11 | How does take_rate impact conversion rate by MainProductCategory? | ❌ |
| 12 | At what take_rate do we see conversion start to drop off? | ❌ |
| 13 | Which MainProducts have the highest average take_rate on their OrderGroups? | ❌ |
| 14 | Show me OrderGroups where the take_rate is below the MainProduct's minimum_take_rate. | ❌ |
| 15 | What is our blended take rate across all completed OrderGroups this fiscal year? | ❌ |
| 16 | How many OrderGroups have inconsistent pricing (customer_rate < seller_rate)? | ❌ |
| 17 | Are there completed Orders without corresponding Invoices? | ❌ |
| 18 | Summarize Downstream's equipment share agreement and terms of service. | ❌ |
| 19 | Generate a redline for the master subcontractor agreements between the customer and supplier. | ❌ |
| 20 | What accounts are churning in my pod? | ❌ |
| 21 | Show the relationship between this user and the different pods and accounts they have. | ❌ |
| 22 | How many orders were completed by this specific user? | ❌ |
| 23 | Which accounts should I be contacting right now? | ❌ |
| 24 | What is my current product mix? | ❌ |
| 25 | How many orders has downstream done today compared to my pod? | ❌ |
| 26 | How many orders did my pod complete last week? | ❌ |
| 27 | Which accounts have the most carts that have a conversion rate of 80% or higher? | ❌ |
| 28 | Who is the customer logged in right now? Connect me to the last logged-in customer from my pod. | ❌ |
| 29 | Who are our main competitors? | ❌ |
| 30 | How do I add a credit card and upload insurance to the platform? | ❌ |
| 31 | If a customer wants fulfillment today but the supplier can only do tomorrow, how do we identify if the customer accepted the end date change? | ❌ |
| 32 | What are the supplier health metrics and fulfillment rate for a supplier that is declining every order? | ❌ |
| 33 | How many OrderGroups are currently in PENDING status across all UserAddresses? | ❌ |
| 34 | What is the average estimated_value of OrderGroups for 30 Cubic Yard Dumpsters vs Standard Toilets over the last 12 months? | ❌ |
| 35 | Which UserGroups have the most OrderGroups with a lost_reason in Q1? | ❌ |
| 36 | Show me all OrderGroups where the added_via is RECOMMENDATION_ENGINE and their current status breakdown. | ❌ |
| 37 | What is the total tonnage_quantity across all completed waste disposal OrderGroups this quarter? | ❌ |
| 38 | How many Orders moved from PENDING to SCHEDULED within 24 hours last month? | ❌ |
| 39 | List OrderGroups that have been in IN_PROGRESS status for more than 30 days without an end_date. | ❌ |
| 40 | What is our overall Order cancellation rate by MainProductCategory? | ❌ |
| 41 | Which SellerLocations have the highest rate of Orders stuck in ADMIN_APPROVAL_PENDING? | ❌ |
| 42 | How many auto-renewal Orders (type=AUTO_RENEWAL) were created this month compared to last month? | ❌ |
| 43 | What is our total platform revenue (customer_rate minus seller_rate) from OrderLineItems this quarter? | ❌ |
| 44 | Compare delivery_fee and removal_fee revenue across the top 10 MainProducts by volume. | ❌ |
| 45 | What is the average customer_rate per OrderLineItem for RENTAL vs SERVICE line item types? | ❌ |
| 46 | Which MainProductCategories generate the most revenue from FUEL_AND_ENV line items? | ❌ |
| 47 | How does the estimated_value of OrderGroups compare to actual invoiced amounts by product category? | ❌ |
| 48 | What is the month-over-month trend in average estimated_value per OrderGroup? | ❌ |
| 49 | Which bandit pricing arm (DISCOUNT_10 through BUMP_40) has the highest conversion rate this quarter? | ❌ |
| 50 | How much total balance_due is outstanding across all Invoices right now? | ❌ |
| 51 | Which UserGroups on NET_30 terms have Invoices past due by more than 15 days? | ❌ |
| 52 | What is the average time between Order completion and Invoice payment by net_terms tier? | ❌ |
| 53 | Show me the top 10 UserGroups by total unpaid Invoice balance. | ❌ |
| 54 | How many Invoices were sent but have zero InvoicePayments recorded in the last 60 days? | ❌ |
| 55 | What is our Invoice collection rate (amount_paid / amount_due) broken down by net_terms? | ❌ |
| 56 | Which Sellers have the most OrderGroups in PAST_DUE status? | ❌ |
| 57 | Compare the payment velocity of UserGroups using card vs us_bank_account PaymentMethods. | ❌ |
| 58 | How many UserGroups have a credit_line_limit and what percentage are currently over 80% utilization? | ❌ |
| 59 | What is the total tax_collected on Invoices by state this quarter? | ❌ |
| 60 | How many UserGroups have a lifecycle_status of AT_RISK and what is their average monthly order volume? | ❌ |
| 61 | Which UserGroups transitioned from ACTIVE to CHURNED in the last 90 days? | ❌ |
| 62 | List all UserGroups with do_not_rent=True and the reason they were flagged. | ❌ |
| 63 | What is the average lifetime order count for UserGroups by industry? | ❌ |
| 64 | Which account_owner has the most UserGroups in MANAGED sales_status? | ❌ |
| 65 | How many UserGroups have sales_status=PROSPECTING with zero OrderGroups? | ❌ |
| 66 | Show me UserGroups whose lifecycle_status is NEVER_ORDERED but were created more than 30 days ago. | ❌ |
| 67 | What is the distribution of net_terms across active UserGroups? | ❌ |
| 68 | Which UserGroups have the highest total estimated_value across all their OrderGroups this year? | ❌ |
| 69 | How many UserGroups have compliance_status=NEEDS_REVIEW? | ❌ |
| 70 | How many active UserAddresses have an estimated_start_date in the next 14 days but no OrderGroups yet? | ❌ |
| 71 | What is the average number of OrderGroups per UserAddress for commercial construction projects? | ❌ |
| 72 | Which UserAddresses have the highest estimated_project_value with no recommendations materialized? | ❌ |
| 73 | Show me UserAddressRecommendations with effective_confidence above 80 that are still in PENDING materialization_status. | ❌ |
| 74 | What is the recommendation-to-order conversion rate (MATERIALIZED vs total staged) by MainProduct? | ❌ |
| 75 | How many UserAddresses were sourced from PLANHUB vs BUILDINGCONNECTED this quarter? | ❌ |
| 76 | Which zip codes have the most active UserAddresses right now? | ❌ |
| 77 | What is the average confidence score from the PredictionAgent across all recommendations this month? | ❌ |
| 78 | List UserAddresses with a product_wish_list that have no matching UserAddressRecommendations staged. | ❌ |
| 79 | How does the lost-order confidence penalty impact recommendation acceptance rates? | ❌ |
| 80 | Which Sellers have the highest Order completion rate (COMPLETE / total Orders)? | ❌ |
| 81 | What is the average time from Order PENDING to SCHEDULED by SellerLocation? | ❌ |
| 82 | Which SellerLocations have the most active SellerProductSellerLocation listings? | ❌ |
| 83 | Show me Sellers where do_not_rent=True and when they were last active. | ❌ |
| 84 | What is the geographic coverage gap — zip codes with UserAddresses but no nearby SellerLocations? | ❌ |
| 85 | Which Sellers have the widest product catalog (most distinct MainProducts offered)? | ❌ |
| 86 | Compare the average seller_rate for 20 Cubic Yard Dumpsters across the top 10 SellerLocations by volume. | ❌ |
| 87 | Which SellerLocations have the highest cancellation rate on their Orders? | ❌ |
| 88 | How many SellerProductSellerLocations are currently active vs inactive? | ❌ |
| 89 | What is the average service_radius across all active SellerLocations? | ❌ |
| 90 | What are the top 10 MainProducts by OrderGroup count this quarter? | ❌ |
| 91 | Which MainProducts have the lowest popularity score but growing order volume? | ❌ |
| 92 | Show me the rental vs service vs material breakdown of OrderLineItems by MainProductCategory. | ❌ |
| 93 | What is the average rental duration (end_date minus start_date) for Storage Containers vs Roll-Off Dumpsters? | ❌ |
| 94 | Which MainProducts are most commonly ordered together on the same UserAddress? | ❌ |
| 95 | How does 19 Ft Scissor Lift order volume compare to 24-27 Ft Scissor Lift month over month? | ❌ |
| 96 | What percentage of OrderGroups include both a dumpster and a portable toilet? | ❌ |
| 97 | Which MainProductCategories have the highest dynamic_max_take_rate spread? | ❌ |
| 98 | Show me MainProducts that have never been ordered but are listed by 5+ SellerLocations. | ❌ |
| 99 | What is the search-to-cart conversion rate for Telehandlers on the marketplace? | ❌ |
| 100 | How many LeadProfiles are in PENDING review_status right now? | ❌ |
| 101 | What is the lead-to-first-order conversion rate by source_type (WEBSITE_FORM vs META_LEAD_AD vs CSV_IMPORT)? | ❌ |
| 102 | Which Meta ad campaign_id has generated the most LeadProfiles this month? | ❌ |
| 103 | Show me the FirstTouchAttribution channel breakdown for UserGroups that placed an order in Q1. | ❌ |
| 104 | What is our cost per acquisition by ChannelMetric channel (Google Ads vs Meta vs LinkedIn)? | ❌ |
| 105 | Which utm_campaign has the highest revenue attribution in the LastTouchAttribution view? | ❌ |
| 106 | How many LeadProfiles have product_interest including ROLL_OFF_DUMPSTER vs PORTABLE_TOILET? | ❌ |
| 107 | What is the average time from LeadProfile creation to first OrderGroup by rental_timeframe? | ❌ |
| 108 | Show me ChannelMetric spend vs conversions trend for Google Ads over the last 6 months. | ❌ |
| 109 | Which user acquisition source (SALES, GOOGLE, META_ADS, PLANHUB, etc.) produces the highest LTV UserGroups? | ❌ |
| 110 | What is our total GMV for Q3 broken down by region? | ❌ |
| 111 | Compare the revenue from 40-yard roll-off dumpsters vs. standard portable toilets for the last fiscal year. | ❌ |
| 112 | Which sales region saw the highest year-over-year growth in Q1? | ❌ |
| 113 | What is the average order value (AOV) for commercial construction clients compared to residential clients? | ❌ |
| 114 | Show me the top 5 highest-grossing rental accounts for the Southwest region this quarter. | ❌ |
| 115 | What was our profit margin on hazardous waste disposal rentals last month? | ❌ |
| 116 | Forecast our Q4 GMV based on current Q3 booking trends. | ❌ |
| 117 | How much revenue is currently tied up in unpaid invoices over 30 days past due? | ❌ |
| 118 | What is the month-over-month growth rate for our subscription-based waste management services? | ❌ |
| 119 | Generate a breakdown of rental revenue by equipment type for the past 12 months. | ❌ |
| 120 | [Uploaded Image of a Timesheet] Can you calculate the total overtime hours for this week? | ❌ |
| 121 | [Uploaded PDF of a Doctor's Note] Does this qualify for paid medical leave under our current policy? | ❌ |
| 122 | [Uploaded Image of a Fuel Receipt] Extract the date, amount, and vendor for my expense report. | ❌ |
| 123 | I lost my W-2; how do I request a new one from the payroll portal? | ❌ |
| 124 | [Uploaded Image of a driver's log] Verify if this dispatch driver exceeded the maximum allowed continuous driving hours. | ❌ |
| 125 | When is the next payday, and does it include the quarterly performance bonus? | ❌ |
| 126 | [Uploaded Photo of a damaged hard hat] Does this qualify for an immediate PPE replacement according to HR guidelines? | ❌ |
| 127 | How many PTO days do I have left this year? | ❌ |
| 128 | [Uploaded Image of a Paystub] Can you explain why my state tax withholding changed on this paycheck? | ❌ |
| 129 | What is the process for submitting mileage reimbursement for traveling to a construction site? | ❌ |
| 130 | What is the company's policy on remote work for dispatchers and customer support? | ❌ |
| 131 | How much notice do I need to give before taking a two-week vacation? | ❌ |
| 132 | What are the core hours everyone is expected to be online and available? | ❌ |
| 133 | What is the procedure for reporting a workplace safety violation at a client's construction site? | ❌ |
| 134 | Are employees allowed to rent company dumpsters for personal use at a discount? | ❌ |
| 135 | What is the bereavement leave policy? | ❌ |
| 136 | Who do I contact if my company laptop is stolen or damaged? | ❌ |
| 137 | What are the observed company holidays for this calendar year? | ❌ |
| 138 | Explain the 401(k) matching schedule detailed in the handbook. | ❌ |
| 139 | What is the dress code for client-facing account executives when visiting a site? | ❌ |

## Debugging

```bash
# Check RAG retrieval for a question
venv/bin/python3 checks/check_rag.py "your question"

# Check full reasoning output (plan + validation)
venv/bin/python3 checks/check_reasoning.py "your question"
```
