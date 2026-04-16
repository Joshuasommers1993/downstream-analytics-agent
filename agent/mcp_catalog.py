# MCP tool catalog — 141 tools from downstream-mcp
# Descriptions written from TG-API-proxy source (views, serializers, services) + DB schema.
# Richer descriptions improve Chroma RAG accuracy for analytics tool selection.

MCP_TOOL_CATALOG = {

    # ── ENRICHMENT ────────────────────────────────────────────────────────────

    # ── INSIGHT HUB (pre-computed sales analytics) ────────────────────────────

    "api_insight_hub_account_classification_list": {
        "entity": "InsightHub:AccountClassification",
        "gotchas": [
            "'Net New' = UserGroup whose first *confirmed* order's created_on falls in the period; 'Expansion' = all other active accounts; 'Backlog' = SCHEDULED orders only (not COMPLETE).",
            "Date range filters on order end_date (service date), not created_on.",
            "rep_id param maps to account_owner_id on UserGroup — this is the sales rep FK, not the customer.",
        ],
        "path": "/api/insight-hub/account-classification/",
        "description": (
            "Pre-computed revenue breakdown for a date range by account classification: "
            "Net New GMV (first-time customers), Expansion GMV (returning customers), and Backlog GMV (scheduled/pipeline orders). "
            "Summary fields: net_new_gmv, expansion_gmv, backlog_gmv, total_gmv, net_new_accounts, expansion_accounts, backlog_orders. "
            "Also returns monthly_trend array with month + gmv per month. "
            "Use this for revenue attainment vs target, new vs returning customer revenue split, pipeline value, "
            "monthly GMV trend, or sales territory performance."
        ),
        "filters": "start_date, end_date, rep_id, team, industry_id, company_size_min, company_size_max, lead_source",
        "method": "GET",
        "no_ids": True,
    },
    "api_insight_hub_account_growth_list": {
        "entity": "InsightHub:AccountGrowth",
        "gotchas": [
            "CHURN_DAYS = 30: an account is 'churned' when last_order_date + 30 days crosses into the reporting period.",
            "first_order_date uses order created_on; last_order_date uses order end_date — two different date semantics mixed.",
            "Date filters apply to order end_date (service date), not created_on.",
        ],
        "path": "/api/insight-hub/account-growth/",
        "description": (
            "Pre-computed customer acquisition and churn metrics for a date range. "
            "Summary fields: net_new (new customers), churned (lost customers), retained, net_growth. "
            "Also returns net_new_accounts list (id, name, first_order_date), churned_accounts list (id, name, last_order_date), "
            "and monthly_trend with net_new per month. "
            "Use this for customer acquisition rate, churn rate, net customer growth, retention analysis, "
            "or to identify which specific accounts were won or lost in a period."
        ),
        "filters": "start_date, end_date, rep_id, team, industry_id, company_size_min, company_size_max, lead_source",
        "method": "GET",
        "no_ids": True,
    },
    "api_insight_hub_commissions_list": {
        "entity": "InsightHub:Commissions",
        "gotchas": [
            "FLAT_COMMISSION_RATE = 3.25%. Base = Invoice total minus insurance line items, refunds, credits, and sales tax (URS and SALES_TAX line item types excluded).",
            "In-cart and SCHEDULED orders appear as pipeline (not yet earned); only COMPLETE = earned.",
            "Uses Invoice.with_total_invoiced() — excludes DRAFT, VOID, UNCOLLECTIBLE invoices from the base.",
            "rep_id maps to account_owner_id on UserGroup (sales rep, not customer).",
        ],
        "path": "/api/insight-hub/commissions/",
        "description": (
            "Pre-computed commission calculations for all sales reps for a given month. "
            "Returns commission_rate_percent, summary (total_commission_eligible, total_commission, total_in_cart, total_scheduled), "
            "reps array (rep_id, rep_name, commission_eligible, commission, in_cart, scheduled), "
            "and monthly_trend (month, total commission). "
            "Use this for sales rep compensation analysis, commission payout totals, "
            "or to see how much GMV is in-cart vs scheduled vs already completed for commission purposes."
        ),
        "filters": "start_date, end_date, rep_id, team, industry_id, company_size_min, company_size_max, lead_source",
        "method": "GET",
        "no_ids": True,
    },
    "api_insight_hub_customer_spend_mom_list": {
        "entity": "InsightHub:CustomerSpendMoM",
        "gotchas": [
            "Only COMPLETE orders are included — SCHEDULED orders do not count toward spend.",
            "Grouped by user_group per calendar month using TruncMonth on end_date.",
            "Date filters on end_date (service date), not created_on or submitted_on.",
        ],
        "path": "/api/insight-hub/customer-spend-mom/",
        "description": (
            "Pre-computed month-over-month spend breakdown by customer (user group / account). "
            "Returns customers array (user_group_id, user_group_name, month, spend) "
            "and monthly_totals array (month, total_spend). "
            "Use this for customer spend trends, top-spending accounts by month, "
            "spend concentration (which customers drive most revenue), "
            "or to identify accounts with declining or growing spend over time."
        ),
        "filters": "start_date, end_date, rep_id, team, industry_id, company_size_min, company_size_max, lead_source",
        "method": "GET",
        "no_ids": True,
    },
    "api_insight_hub_first_touch_to_order_list": {
        "entity": "InsightHub:FirstTouchToOrder",
        "gotchas": [
            "first_touch_date = UserAddress.first_touch_sent_at if set, otherwise earliest Cart created_on for that user address.",
            "End point = earliest COMPLETE order start_date (not end_date, not submitted_on).",
            "Measures marketing-to-revenue lag, not order-creation-to-delivery.",
        ],
        "path": "/api/insight-hub/first-touch-to-order/",
        "description": (
            "Sales cycle speed metric — how many days from first email outreach to first order. "
            "Returns average_days (mean days), total_conversions, and details per account. "
            "Use this for outreach-to-order speed, sales cycle length, or email response latency. "
            "Not suitable for funnel stage drop-off or cart-to-order rate — use api_insight_hub_sales_funnel_list for those."
        ),
    
        "filters": "start_date, end_date, rep_id, team, industry_id, company_size_min, company_size_max, lead_source",
        "method": "GET",
        "no_ids": True,
    },
    "api_insight_hub_gmv_by_state_list": {
        "entity": "InsightHub:GMVByState",
        "gotchas": [
            "Only SCHEDULED and COMPLETE order statuses are included.",
            "State is derived from the UserAddress (job site), not the billing address.",
            "Date filters on end_date (service date).",
        ],
        "path": "/api/insight-hub/gmv-by-state/",
        "description": (
            "Pre-computed gross merchandise value (GMV) aggregated by US state for a date range. "
            "Returns states array with: state (two-letter code), gmv (total order value), order_count. "
            "Use this for geographic revenue distribution, top states by GMV, "
            "state-level market penetration, or regional sales comparison."
        ),
        "filters": "start_date, end_date, rep_id, team, industry_id, company_size_min, company_size_max, lead_source",
        "method": "GET",
        "no_ids": True,
    },
    "api_insight_hub_gmv_mom_list": {
        "entity": "InsightHub:GMVMoM",
        "gotchas": [
            "Only SCHEDULED and COMPLETE orders included — pending, cancelled, in-cart excluded.",
            "Grouped by TruncMonth('end_date') — months are based on service date, not order creation date.",
            "rep_id maps to account_owner_id on UserGroup (sales rep, not customer).",
        ],
        "path": "/api/insight-hub/gmv-mom/",
        "description": (
            "Pre-computed gross merchandise value (GMV) and platform economics month-over-month. "
            "Returns months array with: month (YYYY-MM), gmv (total customer spend), supplier_cost (total paid to sellers), "
            "net_revenue (Downstream margin = gmv - supplier_cost), take_rate_percent (net_revenue / gmv * 100), "
            "aov (average order value), order_count. "
            "Use this for revenue trends, platform margin trends, average order value trends, "
            "order volume trends, or MoM growth rate calculations."
        ),
        "filters": "start_date, end_date, rep_id, team, industry_id, company_size_min, company_size_max, lead_source",
        "method": "GET",
        "no_ids": True,
    },
    "api_insight_hub_product_mix_list": {
        "entity": "InsightHub:ProductMix",
        "gotchas": [
            "Date filters on order end_date (service date), not created_on.",
            "rep_id maps to account_owner_id on UserGroup (sales rep, not customer).",
        ],
        "path": "/api/insight-hub/product-mix/",
        "description": (
            "Order volume by waste type or service category. "
            "Top waste types ranked by how many orders were placed for each. "
            "Which material categories are ordered most. Frequency and share of each service type. "
            "Pre-computed: category name, order_count, percent of total orders, total_orders. "
        ),
        "filters": "start_date, end_date, rep_id, team, industry_id, company_size_min, company_size_max, lead_source",
        "method": "GET",
        "no_ids": True,
    },
    "api_insight_hub_quota_vs_actual_list": {
        "entity": "InsightHub:QuotaVsActual",
        "gotchas": [
            "Actuals = COMPLETE orders only (SCHEDULED not counted as actual).",
            "'New accounts' = UserGroups whose first confirmed order falls in the period.",
            "SalesQuota.month must be the first-of-month (DateField); non-first-of-month values will produce no quota row.",
            "rep_id maps to account_owner_id on UserGroup (sales rep, not customer).",
        ],
        "path": "/api/insight-hub/quota-vs-actual/",
        "description": (
            "Pre-computed sales rep quota attainment vs actual performance, per rep per month. "
            "Returns rows array with: rep_id, rep_name, month (YYYY-MM), "
            "gmv_target, gmv_actual, attainment_percent (gmv_actual / gmv_target * 100), "
            "new_accounts_target, new_accounts_actual, orders_target, orders_actual. "
            "Use this for sales rep performance review, quota attainment ranking, "
            "which reps are hitting or missing targets, or team-level attainment rollup."
        ),
        "filters": "start_date, end_date, rep_id, team, industry_id, company_size_min, company_size_max, lead_source",
        "method": "GET",
        "no_ids": True,
    },
    "api_insight_hub_quotas_list": {
        "entity": "InsightHub:Quota",
        "gotchas": [
            "SalesQuota.month is a DateField that must be set to the first day of the month; non-first-of-month values silently fail to match quota_vs_actual lookups.",
            "gmv_target, new_accounts_target, orders_target are all nullable.",
        ],
        "path": "/api/insight-hub/quotas/",
        "description": (
            "Returns the raw sales quota targets set for each sales rep by month. "
            "Use this to retrieve the quota plan for a rep, check what targets are set for a given month, "
            "or verify quota coverage across the team."
        ),
        "filters": "rep_id, month",
        "method": "GET",
        "no_ids": True,
    },
    "api_insight_hub_sales_funnel_list": {
        "entity": "InsightHub:SalesFunnel",
        "gotchas": [
            "Classifies Cart objects, not Order objects. Stages in priority order: 'Closed Won' (submitted_on set), 'Closed Lost' (lost_on set), 'Quote Sent' (quote_expiration or to_emails present), 'Cart Updated' (has orders), 'Cart Created' (else).",
            "A Cart is one-per-UserAddress; a single Cart transitions through all stages.",
            "Date filters are on Cart's own timestamps, not on order end_date.",
        ],
        "path": "/api/insight-hub/sales-funnel/",
        "description": (
            "Conversion rate from cart to confirmed order. Drop-off rate at each stage of the sales funnel. "
            "Cart-to-quote rate, quote-to-close rate, overall win rate, which stage loses the most deals. "
            "Pre-computed funnel with stage-by-stage counts and GMV: cart, quote, order, invoice, payment. "
            "Returns stages array (stage name, count, gmv) and conversion_rates (cart_to_quote, quote_to_close, overall). "
        ),
        "filters": "start_date, end_date, rep_id, team, industry_id, company_size_min, company_size_max, lead_source",
        "method": "GET",
        "no_ids": True,
    },
    "api_insight_hub_spend_by_product_list": {
        "entity": "InsightHub:SpendByProduct",
        "gotchas": [
            "Date filters on order end_date (service date), not created_on.",
            "rep_id maps to account_owner_id on UserGroup (sales rep, not customer).",
            "Do NOT join this to raw order tables for product name lookup — different grain and aggregation.",
        ],
        "path": "/api/insight-hub/spend-by-product/",
        "description": (
            "Pre-computed revenue (GMV) and average order value aggregated by product category / waste type. "
            "Best tool for: which product categories generate the most revenue, average order value by product type, "
            "top products by GMV, product revenue ranking, product-level AOV comparison, revenue breakdown by service type. "
            "Returns products array with: main_product_name, gmv (total revenue), order_count, aov (average order value). "
            "Use this whenever the question asks about revenue, GMV, or AOV broken down by product or service type."
        ),
        "filters": "start_date, end_date, rep_id, team, industry_id, company_size_min, company_size_max, lead_source",
        "method": "GET",
        "no_ids": True,
    },
    "api_insight_hub_spend_by_supplier_list": {
        "entity": "InsightHub:SpendBySupplier",
        "gotchas": [
            "Date filters on order end_date (service date), not created_on.",
            "rep_id maps to account_owner_id on UserGroup (sales rep, not customer).",
        ],
        "path": "/api/insight-hub/spend-by-supplier/",
        "description": (
            "Pre-computed customer spend aggregated by supplier (seller). "
            "Returns suppliers array with: seller_id, seller_name, gmv (total spend routed to this seller). "
            "Use this for supplier concentration analysis, top sellers by GMV, "
            "how much spend goes to each vendor, or supplier diversification metrics."
        ),
        "filters": "start_date, end_date, rep_id, team, industry_id, company_size_min, company_size_max, lead_source",
        "method": "GET",
        "no_ids": True,
    },
    "api_insight_hub_take_rate_mom_list": {
        "entity": "InsightHub:TakeRateMoM",
        "gotchas": [
            "Take rate formula: (customer_price - seller_price) / customer_price * 100.",
            "COMPLETE orders only — SCHEDULED excluded.",
            "Grouped per rep per month; rep_id maps to account_owner_id on UserGroup.",
        ],
        "path": "/api/insight-hub/take-rate-mom/",
        "description": (
            "Platform take rate trend over time. Downstream margin percentage month-over-month or year-over-year. "
            "Net revenue and take rate percent per rep per month. Annual/monthly platform margin trend. "
            "Returns rows: rep_id, rep_name, month (YYYY-MM), customer_total (GMV), "
            "seller_total (supplier cost), net_revenue, take_rate_percent. "
        ),
        "filters": "start_date, end_date, rep_id, team, industry_id, company_size_min, company_size_max, lead_source",
        "method": "GET",
        "no_ids": True,
    },

    # ── ADMIN / INTERNAL ──────────────────────────────────────────────────────

    "api_v1_admin_communications_list": {
        "entity": "Communication",
        "gotchas": [
            "Requires `user` UUID query param — returns empty queryset without it.",
        ],
        "path": "/api/v1/admin/communications/",
        "description": (
            "Admin-only. Returns communication timeline entries for a single user ordered most-recent-first. "
            "Includes emails sent, calls logged, and notes. "
            "Filter: user_id. "
            "Use this to audit outreach history for a specific rep or customer."
        ),
        "method": "GET",
    },
    "api_v1_admin_sales_target_vs_actuals_list": {
        "entity": "Aggregated:SalesTargetVsActual",
        "path": "/api/v1/admin/sales/target-vs-actuals/",
        "description": (
            "Admin-only. Returns aggregate GMV pacing metrics and cumulative daily comparison against the prior month. "
            "Includes current month actuals, target, and prior-month comparison on a daily basis. "
            "Use this for daily sales pacing dashboards, are-we-on-track analysis, "
            "or current month vs prior month performance."
        ),
        "method": "GET",
    },
    "api_v1_admin_transactional_emails_list": {
        "entity": "TransactionalEmail",
        "gotchas": [
            "Requires `user` UUID query param — returns empty queryset without it.",
        ],
        "path": "/api/v1/admin/transactional-emails/",
        "description": (
            "Admin-only. Returns sent transactional emails addressed to a specific user, ordered most-recent-first. "
            "Filter: user_id. "
            "Use this to check which system emails were sent to a user (order confirmations, invoices, etc.)."
        ),
        "method": "GET",
    },
    "api_v1_admin_user_addresses_goal_progress_list": {
        "entity": "Aggregated:UserAddressGoalProgress",
        "path": "/api/v1/admin/user-addresses/{user_address_id}/goal-progress/",
        "description": (
            "Admin-only. Returns value and count metrics for a specific project (UserAddress): "
            "cart value, order group count, order count, invoice totals. "
            "Use this to track progress of a specific job site toward its spend goal."
        ),
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_admin_user_groups_goal_progress_aggregate_list": {
        "entity": "Aggregated:UserGroupGoalProgress",
        "path": "/api/v1/admin/user-groups/goal-progress/aggregate/",
        "description": (
            "Admin-only. Returns aggregate goal progress across all user groups: "
            "total target GMV, total actual GMV, attainment percentage, account count. "
            "Use this for platform-wide goal attainment rollup or pipeline health overview."
        ),
        "method": "GET",
    },
    "api_v1_admin_user_groups_goal_progress_list": {
        "entity": "Aggregated:UserGroupGoalProgress",
        "path": "/api/v1/admin/user-groups/{user_group_id}/goal-progress/",
        "description": (
            "Admin-only. Returns goal, current value, and supporting metrics for a specific user group (account): "
            "target GMV, actual GMV, attainment percent, order count, invoice totals. "
            "Use this to check how a specific account is tracking against its spend goal."
        ),
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_admin_user_groups_notes_list": {
        "entity": "UserGroupNote",
        "gotchas": [
            "Notes attached to a UserGroup. Requires `user_group` UUID param to scope results.",
        ],
        "path": "/api/v1/admin/user-groups/{user_group_id}/notes/",
        "description": (
            "Admin-only. Returns all CRM notes recorded for a specific account (user group) in descending creation order. "
            "Use this to retrieve account notes or activity log for a customer."
        ),
        "method": "GET",
        "requires_id": True,
    },

    # ── ADVERTISEMENTS ────────────────────────────────────────────────────────

    "api_v1_advertisements_list": {
        "entity": "Advertisement",
        "path": "/api/v1/advertisements/",
        "description": (
            "Returns all advertisements (promotional banners/placements) configured in the platform. "
            "Use this to list active promotions, see which sellers are advertising, or audit ad inventory."
        ),
    
        "filters": "id, is_active",
        "method": "GET",
    },
    "api_v1_advertisements_get": {
        "entity": "Advertisement",
        "path": "/api/v1/advertisements/{id}/",
        "description": (
            "Returns a single advertisement by ID. "
            "Use this to retrieve details of a specific ad placement."
        ),
        "method": "GET",
        "requires_id": True,
    },

    # ── BRANDS ────────────────────────────────────────────────────────────────

    # ── DAY OF WEEKS ──────────────────────────────────────────────────────────

    "api_v1_day_of_weeks_list": {
        "entity": "DayOfWeek",
        "path": "/api/v1/day-of-weeks/",
        "description": (
            "Returns the lookup table of day-of-week records used by seller open hours. "
            "Use this to get the UUID for a day name when setting or querying open hours."
        ),
    
        "filters": "id",
        "method": "GET",
    },
    "api_v1_day_of_weeks_get": {
        "entity": "DayOfWeek",
        "path": "/api/v1/day-of-weeks/{id}/",
        "description": "Returns a single day-of-week record by ID.",
        "method": "GET",
        "requires_id": True,
    },

    # ── FINANCIAL CONNECTION ──────────────────────────────────────────────────

    "api_v1_financial_connection_list": {
        "entity": "FinancialConnection",
        "gotchas": [
            "Scoped to the user's user_group if they have one; otherwise scoped to the user directly.",
        ],
        "path": "/api/v1/financial-connection/",
        "description": (
            "Returns Plaid financial connection records linked to the authenticated user group. "
            "Use this to check if an account has connected their bank account."
        ),
    
        "method": "GET",
    },

    # ── GROUP INVOICES ────────────────────────────────────────────────────────

    # ── IDENTITY VERIFICATION ─────────────────────────────────────────────────

    "api_v1_identity_verification_list": {
        "entity": "IdentityVerification",
        "path": "/api/v1/identity-verification/",
        "description": (
            "Returns identity verification status for the authenticated user's account. "
            "Use this to check if an account has completed KYC/identity verification."
        ),
    
        "method": "GET",
    },

    # ── INDUSTRIES ────────────────────────────────────────────────────────────

    "api_v1_industries_list": {
        "entity": "Industry",
        "path": "/api/v1/industries/",
        "description": (
            "Returns all industry classifications used to categorize customer accounts (user groups). "
            "Examples: construction, landscaping, demolition, roofing, plumbing. "
            "Use this to get industry IDs for filtering accounts, or to list all supported industries."
        ),
    
        "method": "GET",
    },
    "api_v1_industries_get": {
        "entity": "Industry",
        "path": "/api/v1/industries/{id}/",
        "description": "Returns a single industry by ID or slug.",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_industries_popular_products_list": {
        "entity": "Industry",
        "gotchas": [
            "Returns popular MainProducts for an industry, not industry records themselves.",
        ],
        "path": "/api/v1/industries/{id}/popular-products/",
        "description": (
            "Returns the most popular products (waste/service types) for a given industry, ranked by order COUNT (not revenue). "
            "Requires an industry_id — not suitable for cross-industry revenue comparisons. "
            "Use this to understand which products are most frequently ordered within a specific industry, "
            "for industry-specific product recommendations, or to identify demand patterns per vertical. "
            "Do NOT use this for product revenue ranking — use api_insight_hub_spend_by_product_list for revenue."
        ),
        "method": "GET",
        "requires_id": True,
    },

    # ── INSURANCE POLICIES ────────────────────────────────────────────────────

    "api_v1_insurance_policies_list": {
        "entity": "InsurancePolicy",
        "path": "/api/v1/insurance-policies/",
        "description": (
            "Returns insurance policies on file for accounts. "
            "Use this to check insurance compliance, find expired policies, or count accounts with valid coverage."
        ),
        "filters": "account, type, status",
        "filter_enums": {
            "type": ["general_liability", "equipment_liability", "umbrella_liability"],
            "status": ["processing", "parsing_failed", "needs_attention", "active", "expiring_soon", "expired", "deactivated"],
        },
        "method": "GET",
    },
    "api_v1_insurance_policies_get": {
        "entity": "InsurancePolicy",
        "path": "/api/v1/insurance-policies/{insurance_policy_id}/",
        "description": "Returns a single insurance policy by ID.",
        "method": "GET",
        "requires_id": True,
    },

    # ── INVOICES ──────────────────────────────────────────────────────────────

    "api_v1_invoices_list": {
        "entity": "Invoice",
        "gotchas": [
            "DRAFT invoices excluded by default — pass `include_draft=true` to include them.",
            "`month`/`year` filters apply to due_date, not created_on.",
            "`past_due` filter = status=OPEN AND due_date < now AND amount_remaining > 0.",
            "`items`, `groups`, `pre_payment_credit`, `post_payment_credit` only populated when expanded via ?expand[].",
            "`display_total` is a computed property, not a stored field.",
        ],
        "path": "/api/v1/invoices/",
        "description": (
            "Returns invoices visible to the authenticated context (customer sees their invoices; "
            "staff/admin with allow_all=true sees all invoices). "
            "Supports ordering by: created_on, due_date, total, amount_due, amount_paid, status. "
            "Use this for invoice aging analysis, outstanding balance tracking, payment collection metrics, "
            "or to list unpaid invoices for an account."
        ),
        "filters": "id, user_address, month, year, status, search, created_after, created_before, due_after, due_before, amount_min, amount_max, categories, locations, users, user_group, past_due, order",
        "filter_enums": {
            "status": ["draft", "open", "paid", "void", "uncollectible", "deleted"],
        },
        "method": "GET",
    },
    "api_v1_invoices_metrics_list": {
        "entity": "Invoice",
        "gotchas": [
            "Scoped by `user_group` query param.",
            "Uses Invoice.with_total_invoiced() which excludes DRAFT, VOID, UNCOLLECTIBLE.",
        ],
        "path": "/api/v1/invoices/metrics/",
        "description": (
            "Returns aggregate invoice totals for the current scope: "
            "past_due_total (overdue amount), outstanding_total (open unpaid), paid_total (collected). "
            "Use this for AR summary, total outstanding balance, or collections health at a glance."
        ),
        "method": "GET",
    },
    "api_v1_invoices_get": {
        "entity": "Invoice",
        "gotchas": [
            "DRAFT invoices excluded by default — pass `include_draft=true` to include them.",
            "`items`, `groups`, `pre_payment_credit`, `post_payment_credit` only populated when expanded.",
            "`display_total` is a computed property.",
        ],
        "path": "/api/v1/invoices/{id}/",
        "description": "Returns a single invoice by ID with full details.",
        "method": "GET",
        "requires_id": True,
    },

    # ── KNOWLEDGE ─────────────────────────────────────────────────────────────
    "api_v1_knowledge_search_list": {
        "entity": "KnowledgeDocument",
        "gotchas": [
            "POST endpoint (not GET) — requires mandatory `query` param in the request body.",
            "Semantic/docs search returning document chunks, NOT queryable data records.",
            "Do not use for analytics or data queries — use for 'how do I' / policy / documentation questions only.",
        ],
        "path": "/api/v1/knowledge/search/",
        "description": (
            "Semantic vector search over the Downstream knowledge base. "
            "Returns ranked knowledge_document chunks matching the query. "
            "Fields per result: document_id, slug, heading, score, excerpt, metadata. "
            "Parameters: query (string). "
            "Use this to find documentation, policies, or internal knowledge relevant to a topic. "
            "Note: this is a docs search, NOT a data query — it searches help content, not transactional data."
        ),
    
        "method": "POST",
    },

    # ── LEADS ─────────────────────────────────────────────────────────────────

    # ── MAIN PRODUCTS ─────────────────────────────────────────────────────────

    "api_v1_main_product_categories_list": {
        "entity": "MainProductCategory",
        "path": "/api/v1/main-product-categories/",
        "description": (
            "Returns product categories in the Downstream catalog. "
            "Examples: roll-off dumpsters, portable toilets, temporary fencing, storage containers. "
            "Use this to get category IDs for filtering products, list available service categories, "
            "or understand the product taxonomy."
        ),
    
        "method": "GET",
    },
    "api_v1_main_product_categories_get": {
        "entity": "MainProductCategory",
        "path": "/api/v1/main-product-categories/{id}/",
        "description": "Returns a single product category by ID or slug.",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_main_product_category_groups_list": {
        "entity": "MainProductCategoryGroup",
        "path": "/api/v1/main-product-category-groups/",
        "description": (
            "Returns top-level product category groups that bundle multiple categories. "
            "Examples: Waste Removal, Site Services, Storage. "
            "Use this for top-level product taxonomy, marketplace navigation, or filtering available services."
        ),
    
        "filters": "id, name, seller_location, allows_pickup",
        "method": "GET",
    },
    "api_v1_main_product_category_groups_get": {
        "entity": "MainProductCategoryGroup",
        "path": "/api/v1/main-product-category-groups/{id}/",
        "description": "Returns a single product category group by ID.",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_main_products_list": {
        "entity": "MainProduct",
        "path": "/api/v1/main-products/",
        "description": (
            "Returns the master product catalog — the canonical list of all waste/service products offered on the platform. "
            "Examples: 10-yard dumpster, 20-yard dumpster, portable toilet, temporary fence, storage container. "
            "Use this to look up product IDs, get the full product catalog, find which products are available, "
            "map product names to IDs, or resolve main_product UUID foreign keys from orders into human-readable product names. "
            "Required whenever order data contains main_product UUIDs that need to be joined to product names."
        ),
        "filters": "id, main_product_category__id, main_product_category__slug, is_related, seller_location, allows_pickup, search",
        "method": "GET",
    },
    "api_v1_main_products_get": {
        "entity": "MainProduct",
        "path": "/api/v1/main-products/{id}/",
        "description": "Returns a single main product by ID or slug with full details.",
        "method": "GET",
        "requires_id": True,
    },

    # ── MOBILE WIDGET ─────────────────────────────────────────────────────────

    "api_v1_mobile_widget_list": {
        "entity": "Aggregated:UserDashboard",
        "gotchas": [
            "`cart_count` = number of unsubmitted orders (submitted_on is null), not number of Cart objects.",
            "`active_bookings` = OrderGroups where end_date is null or future AND has at least one submitted, non-cancelled order.",
            "end_date=null on an OrderGroup means equipment is still on-site (active rental), not missing data.",
        ],
        "path": "/api/v1/mobile-widget/",
        "description": (
            "Returns summary data for the mobile homepage widget: "
            "active orders count, upcoming deliveries, recent activity. "
            "Not suitable for analytics — use order endpoints for raw data."
        ),
    
        "method": "GET",
    },

    # ── ORDER GROUPS (BOOKINGS) ───────────────────────────────────────────────

    "api_v1_order_group_attachments_list": {
        "entity": "OrderGroupAttachment",
        "path": "/api/v1/order-group-attachments/",
        "description": (
            "Returns file attachments associated with order groups (bookings). "
            "Use this to list documents or files attached to a booking."
        ),
    
        "filters": "id, order_group",
        "method": "GET",
    },
    "api_v1_order_groups_list": {
        "entity": "OrderGroup",
        "gotchas": [
            "end_date=null means equipment is on-site (still rented) — the `active` filter treats null end_date as active.",
            "`status` filter checks orders__status (any order in the group matching), not a status field on OrderGroup itself.",
            "`active` filter: end_date null OR end_date > today, AND group has at least one non-cancelled submitted order.",
            "`date` filter maps to end_date (service/return date), not created_on.",
            "`include_not_submitted=true` required to see in-cart OrderGroups — default excludes them.",
        ],
        "path": "/api/v1/order-groups/",
        "description": (
            "Returns order groups (bookings / service agreements) accessible to the authenticated user. "
            "An OrderGroup is the top-level booking entity that contains one or more Orders (individual service deliveries). "
            "Ordering: created_on, updated_on, start_date, end_date (default: -start_date). "
            "Use this to count bookings by date, track booking volume trends, "
            "find bookings by job site, or calculate total booking value."
        ),
        "filters": "id, active, code, status, date_after, date_before, search, exclude_canceled, supplier, product_category, user, user_address, user_group, invoice_status",
        "filter_enums": {
            "status": ["PENDING", "SCHEDULED", "COMPLETE", "CANCELLED", "ADMIN_APPROVAL_PENDING", "ADMIN_APPROVAL_DECLINED", "CREDIT_APPLICATION_APPROVAL_PENDING", "CREDIT_APPLICATION_DECLINED"],
            "invoice_status": ["draft", "open", "paid", "void", "uncollectible", "deleted"],
        },
        "method": "GET",
    },
    "api_v1_order_groups_filter_options_list": {
        "entity": "OrderGroup",
        "gotchas": [
            "Returns filter option enumerations (states, suppliers, categories) for the OrderGroup list UI — not OrderGroup records.",
        ],
        "path": "/api/v1/order-groups/filter-options/",
        "description": (
            "Returns available filter options for the order groups list (bookings). "
            "Returns distinct values for status, seller, product type, date ranges. "
            "Use this to populate filter dropdowns for booking lists."
        ),
    
        "method": "GET",
    },
    "api_v1_order_groups_get": {
        "entity": "OrderGroup",
        "gotchas": [
            "end_date=null means on-site (active rental), not missing data.",
        ],
        "path": "/api/v1/order-groups/{id}/",
        "description": "Returns a single order group (booking) by ID with full details.",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_order_groups_removal_checkout_list": {
        "entity": "OrderGroup",
        "gotchas": [
            "Removal checkout flow — creates removal/pickup orders, not standard service orders.",
        ],
        "path": "/api/v1/order-groups/{order_group_id}/removal-checkout/",
        "description": (
            "Returns checkout preview for removing/cancelling a service from an order group. "
            "Use this to see pricing implications of removing a product from a booking."
        ),
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_order_groups_swap_checkout_list": {
        "entity": "OrderGroup",
        "gotchas": [
            "Swap checkout flow — replaces one SellerProductSellerLocation with another within an existing OrderGroup.",
        ],
        "path": "/api/v1/order-groups/{order_group_id}/swap-checkout/",
        "description": (
            "Returns checkout preview for swapping a service provider in an order group. "
            "Use this to see pricing implications of changing the supplier for a booking."
        ),
        "method": "GET",
        "requires_id": True,
    },

    # ── ORDERS ────────────────────────────────────────────────────────────────

    "api_v1_orders_for_seller_list": {
        "entity": "Order",
        "gotchas": [
            "Cart orders (submitted_on=null) excluded by default — pass `tab=in_cart` to see them.",
            "`price` returns total_seller_price (supplier payout amount) in this context, NOT the customer price.",
            "`on_rent` filter maps to order_group__end_date__isnull (null end_date = still on-site).",
            "`service_date` filter maps to end_date.",
            "`tab` filter applies complex multi-status logic to bucket orders into workflow tabs.",
        ],
        "path": "/api/v1/orders-for-seller/",
        "description": (
            "Supplier-facing view only. Returns orders scoped to the authenticated seller's own incoming orders. "
            "NOT suitable for platform-wide order counts, buyer analytics, or cross-seller analysis. "
            "Use this only from the supplier side to see their own delivery schedule or incoming order queue."
        ),
        "filters": "id, order_group, status, code, seller_location, seller, product_category, on_rent, tab, order_type, service_date_after, service_date_before, assignment, search, allow_all",
        "filter_enums": {
            "status": ["PENDING", "SCHEDULED", "COMPLETE", "CANCELLED", "ADMIN_APPROVAL_PENDING", "ADMIN_APPROVAL_DECLINED", "CREDIT_APPLICATION_APPROVAL_PENDING", "CREDIT_APPLICATION_DECLINED"],
            "order_type": ["DELIVERY", "PICKUP", "RETURN", "SWAP", "REMOVAL", "AUTO_RENEWAL", "ONE_TIME"],
            "tab": ["new", "scheduled", "history", "in_cart", "cancelled"],
            "assignment": ["initial", "reassigning", "needs_sourcing"],
        },
        "method": "GET",
    },
    "api_v1_orders_for_seller_get": {
        "entity": "Order",
        "gotchas": [
            "`price` returns total_seller_price (supplier payout amount), NOT customer price.",
        ],
        "path": "/api/v1/orders-for-seller/{id}/",
        "description": "Returns a single seller-facing order by ID.",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_orders_list": {
        "entity": "Order",
        "gotchas": [
            "Default ordering is -end_date (most recent service date first), NOT created_on.",
            "`date` / `date_before` / `date_after` filters map to end_date (service date), not created_on.",
            "`submitted_on` boolean filter is inverted: `submitted_on=true` returns UNSUBMITTED (in-cart) orders where submitted_on IS NULL.",
            "`account_owner` field is the sales rep User FK set at order creation time — NOT the customer. Use 'user' or join user_address→user_group for the customer.",
            "Order statuses ADMIN_APPROVAL_PENDING, CREDIT_APPLICATION_APPROVAL_PENDING, NO_PAYMENT_METHOD = placed but blocked — not yet fulfillable.",
            "The API paginates at 100 rows/page. The agent fetch loop has its own cap (MAX_FETCH_ROWS) — always pass date_after to reduce total result set size for historical analysis.",
        ],
        "path": "/api/v1/orders/",
        "description": (
            "Primary platform-wide order data source. Returns all orders (buyer perspective). "
            "Best tool for: how many orders were placed last month, order count by date range, "
            "orders placed in a period, scheduled vs completed orders, orders not yet completed, "
            "cohort analysis (repeat orders, second order within 30 days), order status breakdown. "
            "An Order is an individual service delivery within a booking (OrderGroup). "
            "Filter notes: submitted_on is Boolean (True = unsubmitted/in-cart, False = submitted); "
            "date_after/date_before filter on end_date (service date), not created_on."
        ),
        "filters": "id, order_group, submitted_on, date_after, date_before, code, status, type, user_group, user_address, seller",
        "filter_enums": {
            "status": ["PENDING", "SCHEDULED", "COMPLETE", "CANCELLED", "ADMIN_APPROVAL_PENDING", "ADMIN_APPROVAL_DECLINED", "CREDIT_APPLICATION_APPROVAL_PENDING", "CREDIT_APPLICATION_DECLINED"],
            "type": ["DELIVERY", "PICKUP", "RETURN", "SWAP", "REMOVAL", "AUTO_RENEWAL", "ONE_TIME"],
        },
        "method": "GET",
    },
    "api_v1_orders_internal_sales_data_list": {
        "entity": "Order",
        "gotchas": [
            "Staff/internal endpoint returning sales data annotations on orders.",
            "`account_owner` is the sales rep, not the customer.",
        ],
        "path": "/api/v1/orders/internal/sales-data/",
        "description": (
            "Internal sales dashboard data for the current calendar month. "
            "Returns aggregated metrics for sales reps and managers: "
            "total GMV, order count, new accounts, GMV by rep, daily pacing. "
            "Access restricted to sales users and managers. "
            "Use this for current-month sales performance snapshots."
        ),
    
        "method": "GET",
    },
    "api_v1_orders_get": {
        "entity": "Order",
        "gotchas": [
            "`account_owner` is the sales rep, not the customer.",
            "Submitted orders cannot be deleted — perform_destroy raises PermissionDenied.",
        ],
        "path": "/api/v1/orders/{id}/",
        "description": "Returns a single order by ID with full details.",
        "method": "GET",
        "requires_id": True,
    },

    # ── PAYMENT METHODS ───────────────────────────────────────────────────────

    "api_v1_payment_methods_list": {
        "entity": "PaymentMethod",
        "gotchas": [
            "Scoped via list_payment_methods_for_user — returns only payment methods accessible to the authenticated user.",
        ],
        "path": "/api/v1/payment-methods/",
        "description": (
            "Returns payment methods on file for the authenticated user group. "
            "Use this to check what payment methods an account has, or count accounts with specific payment types."
        ),
        "filters": "user_group",
        "method": "GET",
    },
    "api_v1_payment_methods_get": {
        "entity": "PaymentMethod",
        "path": "/api/v1/payment-methods/{id}/",
        "description": "Returns a single payment method by ID.",
        "method": "GET",
        "requires_id": True,
    },

    # ── PAYOUTS ───────────────────────────────────────────────────────────────

    "api_v1_payouts_list": {
        "entity": "Payout",
        "gotchas": [
            "Staff must pass `allow_all=true` to see payouts across all sellers; default scopes to the user's own seller.",
        ],
        "path": "/api/v1/payouts/",
        "description": (
            "Returns payouts to sellers (supplier payments) visible to the authenticated context. "
            "A Payout represents money transferred to a seller for completed orders. "
            "Ordering: created_on (default: -created_on). "
            "Use this for supplier payment history, payout volume analysis, "
            "outstanding payments to sellers, or reconciliation."
        ),
    
        "filters": "id, order, allow_all, is_check, date_after, date_before, amount_min, amount_max, locations, search",
        "method": "GET",
    },
    "api_v1_payouts_metrics_list": {
        "entity": "Payout",
        "gotchas": [
            "Uses Order.objects.for_seller_user() — scoped to the seller user's orders.",
        ],
        "path": "/api/v1/payouts/metrics/",
        "description": (
            "Returns aggregate payout metrics for the current scope: "
            "total_paid, total_pending, total_failed, payout_count. "
            "Use this for supplier payment summary or reconciliation totals."
        ),
    
        "method": "GET",
    },
    "api_v1_payouts_get": {
        "entity": "Payout",
        "path": "/api/v1/payouts/{id}/",
        "description": "Returns a single payout record by ID.",
        "method": "GET",
        "requires_id": True,
    },

    # ── PUBLIC LOCATION PAGES ─────────────────────────────────────────────────

    "api_v1_public_location_pages_list": {
        "entity": "PublicLocationPage",
        "path": "/api/v1/public/location-pages/",
        "description": (
            "Returns public-facing SEO location pages for Downstream's US city coverage. "
            "Use this to list all cities Downstream serves, count coverage by state, "
            "or find which markets have seller presence."
        ),
        "filters": "state, indexable_only, updated_after",
        "method": "GET",
    },
    "api_v1_public_location_pages_get": {
        "entity": "PublicLocationPage",
        "path": "/api/v1/public/location-pages/{state_slug}/{city_slug}/",
        "description": "Returns the public location page for a specific city by state and city slug.",
        "method": "GET",
        "requires_id": True,
    },

    # ── RBAC ──────────────────────────────────────────────────────────────────

    "api_v1_rbac_role_templates_list": {
        "entity": "RBACRoleTemplate",
        "path": "/api/v1/rbac/role-templates/",
        "description": (
            "Returns hard-coded role templates (Admin, Member, View-Only, etc.) that can be used when creating account roles. "
            "Use this to list available permission templates for user management."
        ),
    
        "method": "GET",
    },
    "api_v1_rbac_roles_list": {
        "entity": "RBACRole",
        "path": "/api/v1/rbac/roles/",
        "description": (
            "Returns custom roles defined within the current account (user group). "
            "Use this to list permission roles in an account."
        ),
    
        "method": "GET",
    },
    "api_v1_rbac_scopes_list": {
        "entity": "RBACScope",
        "path": "/api/v1/rbac/scopes/",
        "description": (
            "Returns all available permission scopes that can be assigned to roles. "
            "Use this to list what granular permissions exist in the system."
        ),
    
        "method": "GET",
    },

    # ── SELLER DASHBOARD ──────────────────────────────────────────────────────

    "api_v1_seller_dashboard_metrics_list": {
        "entity": "Aggregated:SellerDashboard",
        "gotchas": [
            "Requires both `start_date` and `end_date` query params.",
            "Only submitted orders (submitted_on__isnull=False) — in-cart excluded.",
            "Revenue figures use total_seller_price (supplier payout amount), not customer price.",
            "Returns top-N entries with an 'Other' rollup bucket for the remainder.",
        ],
        "path": "/api/v1/seller-dashboard/metrics/",
        "description": (
            "Returns aggregated metrics for a seller's dashboard view: "
            "total orders, revenue, upcoming deliveries, outstanding payouts, customer count. "
            "Scoped to the authenticated seller. "
            "Use this for supplier-side performance summaries."
        ),
    
        "method": "GET",
    },

    # ── SELLER LOCATIONS ──────────────────────────────────────────────────────

    "api_v1_seller_locations_list": {
        "entity": "SellerLocation",
        "gotchas": [
            "Seller users see only their own seller's locations by default; customer read access requires `allow_all=true`.",
        ],
        "path": "/api/v1/seller-locations/",
        "description": (
            "Primary source for geographic supplier analysis. "
            "Best tool for: how many active sellers per state, which cities have the most seller locations, "
            "seller density by geography, market coverage by state or city. "
            "A SellerLocation represents a specific operational site of a seller — "
            "state and city fields live here, not on the Seller entity. "
            "Pass allow_all=true to see all locations platform-wide."
        ),
        "filters": "id, seller, allow_all, search, latitude, longitude, radius, zoom_level, open, pickup, exclude_ds, product_category, active_only, status",
        "filter_enums": {
            "status": ["compliant", "insurance", "tax", "insurance_expiring", "payouts"],
        },
        "method": "GET",
    },
    "api_v1_seller_locations_get": {
        "entity": "SellerLocation",
        "path": "/api/v1/seller-locations/{id}/",
        "description": "Returns a single seller location by ID with full details including open hours.",
        "method": "GET",
        "requires_id": True,
    },

    # ── SELLER PRODUCT SELLER LOCATIONS ───────────────────────────────────────

    "api_v1_seller_product_seller_locations_list": {
        "entity": "SellerProductSellerLocation",
        "gotchas": [
            "SPSL = the join of SellerProduct × SellerLocation — represents a specific product listed at a specific supplier location.",
            "List is scoped to the seller user's locations by default.",
        ],
        "path": "/api/v1/seller-product-seller-locations/",
        "description": (
            "Returns seller-product-at-location listings (the inventory of which products each seller location offers). "
            "A SellerProductSellerLocation (SPSL) is the junction of a SellerProduct and a SellerLocation, "
            "representing a specific product offered at a specific depot with its own pricing. "
            "Use this to see which products a specific location offers, compare pricing across suppliers, "
            "or count active product listings per market."
        ),
        "filters": "id, seller, seller_product, product, main_product_category, main_product, seller_location, search, status, allow_all",
        "filter_enums": {
            "status": ["active", "inactive", "needs_attention"],
        },
        "method": "GET",
    },
    "api_v1_seller_product_seller_locations_metrics_list": {
        "entity": "SellerProductSellerLocation",
        "gotchas": [
            "Returns aggregate counts (active, needs_attention, inactive) for SPSL listings — not individual records.",
        ],
        "path": "/api/v1/seller-product-seller-locations/metrics/",
        "description": (
            "Returns performance metrics for seller-product-at-location listings: "
            "order_count, total_gmv, average_rating, conversion_rate. "
            "Use this to analyze which product-location combinations generate the most orders or revenue."
        ),
    
        "method": "GET",
    },
    "api_v1_seller_product_seller_locations_get": {
        "entity": "SellerProductSellerLocation",
        "path": "/api/v1/seller-product-seller-locations/{id}/",
        "description": "Returns a single seller-product-at-location listing by ID.",
        "method": "GET",
        "requires_id": True,
    },

    # ── SELLER PRODUCTS ───────────────────────────────────────────────────────

    "api_v1_seller_products_list": {
        "entity": "SellerProduct",
        "gotchas": [
            "Non-staff users only see products belonging to their own seller; staff must pass `allow_all=true`.",
        ],
        "path": "/api/v1/seller-products/",
        "description": (
            "Returns seller products (a seller's specific product offerings, mapped to main products). "
            "A SellerProduct links a Seller to a MainProduct with seller-specific configuration. "
            "Use this to list what products a seller offers, find sellers that offer a specific product, "
            "or analyze product coverage per supplier."
        ),
    
        "filters": "seller, product, allow_all",
        "method": "GET",
    },
    "api_v1_seller_products_get": {
        "entity": "SellerProduct",
        "path": "/api/v1/seller-products/{id}/",
        "description": "Returns a single seller product by ID.",
        "method": "GET",
        "requires_id": True,
    },

    # ── SELLER INVOICE PAYABLES ───────────────────────────────────────────────

    "api_v1_sellerinvoicepayable_list": {
        "entity": "SellerInvoicePayable",
        "gotchas": [
            "AP automation viewset. Exception queue status values: ESCALATED, DISPUTED, ERROR.",
            "Scoped to the acting user's seller.",
        ],
        "path": "/api/v1/sellerinvoicepayable/",
        "description": (
            "Returns invoices payable by the authenticated seller to Downstream (AP side). "
            "Use this for supplier accounts-payable tracking or outstanding seller liabilities."
        ),
        "filters": "seller_location, status, received_date_after, received_date_before, due_date_after, due_date_before, amount_min, amount_max, ocr_status, ingestion_source, has_variance, seller_id",
        "filter_enums": {
            "status": ["PENDING_OCR", "OCR_FAILED", "PENDING_MATCH", "PENDING_VALIDATION", "AUTO_APPROVED", "READY_FOR_PAYOUT", "ESCALATED", "HUMAN_APPROVED", "DISPUTED", "ERROR", "PAID", "UNPAID"],
            "ocr_status": ["pending", "processing", "completed", "failed"],
            "ingestion_source": ["MANUAL", "STABLE_MAIL", "ZOHO_EMAIL"],
        },
        "method": "GET",
    },
    "api_v1_sellerinvoicepayable_get": {
        "entity": "SellerInvoicePayable",
        "path": "/api/v1/sellerinvoicepayable/{id}/",
        "description": "Returns a single seller invoice payable by ID.",
        "method": "GET",
        "requires_id": True,
    },

    # ── SELLERS ───────────────────────────────────────────────────────────────

    "api_v1_sellers_list": {
        "entity": "Seller",
        "gotchas": [
            "Seller has no city/state/zip fields — geographic data lives on SellerLocation. Geographic queries against this endpoint will always produce wrong results; use api_v1_seller_locations_list instead.",
            "A single Seller can have many SellerLocations (one per service area).",
        ],
        "path": "/api/v1/sellers/",
        "description": (
            "Returns company-level seller records. "
            "A Seller is the company entity; geographic fields (city, state) are on SellerLocation, not here. "
            "NOT suitable for state/city breakdowns — use api_v1_seller_locations_list for geography. "
            "Use this to list all suppliers by name, count total active sellers, "
            "look up a seller by name, or get seller IDs for joining with other data."
        ),
        "filters": "id",
        "method": "GET",
    },
    "api_v1_sellers_get": {
        "entity": "Seller",
        "path": "/api/v1/sellers/{id}/",
        "description": "Returns a single seller by ID with full details.",
        "method": "GET",
        "requires_id": True,
    },

    # ── SETUP INTENTS / STRIPE ────────────────────────────────────────────────

    "api_v1_setup_intents_list": {
        "entity": "StripeSetupIntent",
        "gotchas": [
            "Uses request.user.stripe_customer_id — user-level, not UserGroup-level. Different users in the same account have separate Stripe customers.",
        ],
        "path": "/api/v1/setup-intents/",
        "description": (
            "Returns Stripe SetupIntents for the authenticated user group (used to add payment methods). "
            "Not useful for analytics."
        ),
    
        "method": "GET",
    },
    "api_v1_stripe_payment_methods_list": {
        "entity": "StripePaymentMethod",
        "gotchas": [
            "Uses request.user.stripe_customer_id — user-level, not UserGroup-level.",
        ],
        "path": "/api/v1/stripe/payment-methods/",
        "description": (
            "Returns Stripe payment method objects for the authenticated account. "
            "Use this to list saved Stripe payment methods."
        ),
    
        "method": "GET",
    },

    # ── TASKS ─────────────────────────────────────────────────────────────────

    # ── TIME SLOTS ────────────────────────────────────────────────────────────

    "api_v1_time_slots_list": {
        "entity": "TimeSlot",
        "path": "/api/v1/time-slots/",
        "description": (
            "Returns available delivery/pickup time slots offered by sellers. "
            "Lookup table only — no order data, no counts, no analytics. "
            "Use only to get time slot IDs for order creation or display labels in UI."
        ),
    
        "filters": "id",
        "method": "GET",
    },
    "api_v1_time_slots_get": {
        "entity": "TimeSlot",
        "path": "/api/v1/time-slots/{id}/",
        "description": "Returns a single time slot by ID.",
        "method": "GET",
        "requires_id": True,
    },

    # ── USER ADDRESS TYPES ────────────────────────────────────────────────────

    "api_v1_user_address_types_list": {
        "entity": "UserAddressType",
        "path": "/api/v1/user-address-types/",
        "description": (
            "Returns lookup types for user addresses (job sites). "
            "Use this to get address type IDs for filtering or categorizing job sites."
        ),
    
        "filters": "id",
        "method": "GET",
    },
    "api_v1_user_address_types_get": {
        "entity": "UserAddressType",
        "path": "/api/v1/user-address-types/{id}/",
        "description": "Returns a single user address type by ID.",
        "method": "GET",
        "requires_id": True,
    },

    # ── USER ADDRESSES (JOB SITES) ────────────────────────────────────────────

    "api_v1_user_addresses_list": {
        "entity": "UserAddress",
        "gotchas": [
            "UserAddress = a job site / project location, NOT a billing or mailing address.",
            "One UserGroup has many UserAddresses.",
        ],
        "path": "/api/v1/user-addresses/",
        "description": (
            "Returns user addresses (job sites / project locations) accessible to the authenticated user. "
            "A UserAddress is a specific delivery site associated with a user group (account). "
            "Use this to list job sites for an account, find sites by geography, "
            "count active projects per account, or get site IDs for order filtering."
        ),
        "filters": "id, search, state, city, product_category, is_archived, active_only, latitude, longitude, radius, zoom_level, user_group, user, status, suppliers",
        "filter_enums": {
            "status": ["upcoming", "complete"],
        },
        "method": "GET",
    },
    "api_v1_user_addresses_filter_options_list": {
        "entity": "UserAddress",
        "gotchas": [
            "Returns filter option enumerations (states, cities, brands, categories, suppliers) for the job site list UI — not UserAddress records.",
        ],
        "path": "/api/v1/user-addresses/filter_options/",
        "description": (
            "Returns available filter options for the user addresses (job sites) list. "
            "Returns distinct city/state values for building filter UI."
        ),
    
        "method": "GET",
    },
    "api_v1_user_addresses_get": {
        "entity": "UserAddress",
        "gotchas": [
            "UserAddress = a job site / project location, NOT a billing or mailing address.",
        ],
        "path": "/api/v1/user-addresses/{id}/",
        "description": "Returns a single user address (job site) by ID.",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_user_addresses_recommendations_list": {
        "entity": "UserAddressRecommendation",
        "gotchas": [
            "Returns active staged recommendations for a specific UserAddress (project). Generated asynchronously — may take up to 30 seconds after project creation to appear.",
        ],
        "path": "/api/v1/user-addresses/{id}/recommendations/",
        "description": (
            "Returns active product recommendations staged for a specific job site (UserAddress). "
            "Recommendations are generated asynchronously based on project type and history. "
            "Use this to see what products are recommended for a project."
        ),
        "method": "GET",
        "requires_id": True,
    },

    # ── USER GROUP ADMIN APPROVALS ────────────────────────────────────────────

    "api_v1_user_group_admin_approval_user_invite_list": {
        "entity": "UserGroupAdminApprovalUserInvite",
        "gotchas": [
            "Scoped to the user's user_group by default; superuser with `allow_all=true` sees all.",
        ],
        "path": "/api/v1/user-group-admin-approval-user-invite/",
        "description": (
            "Returns pending user invite approval requests for accounts that require admin approval to add new users. "
            "Use this to list pending invitations awaiting admin approval."
        ),
    
        "filters": "allow_all",
        "method": "GET",
    },
    "api_v1_user_group_admin_approval_user_invite_get": {
        "entity": "UserGroupAdminApprovalUserInvite",
        "path": "/api/v1/user-group-admin-approval-user-invite/{id}/",
        "description": "Returns a single user invite approval request by ID.",
        "method": "GET",
        "requires_id": True,
    },

    # ── USER GROUP CREDIT APPLICATIONS ────────────────────────────────────────

    "api_v1_user_group_credit_applications_list": {
        "entity": "UserGroupCreditApplication",
        "gotchas": [
            "Scoped to request.user.user_group_id — users without a user_group get an empty queryset.",
        ],
        "path": "/api/v1/user-group-credit-applications/",
        "description": (
            "Returns net-terms (trade credit) applications associated with the authenticated account. "
            "Use this to list credit applications, track approval status, or count pending reviews."
        ),
    
        "method": "GET",
    },
    "api_v1_user_group_credit_applications_get": {
        "entity": "UserGroupCreditApplication",
        "path": "/api/v1/user-group-credit-applications/{id}/",
        "description": "Returns a single credit application by ID.",
        "method": "GET",
        "requires_id": True,
    },

    # ── USER GROUPS (ACCOUNTS) ────────────────────────────────────────────────

    "api_v1_user_groups_list": {
        "entity": "UserGroup",
        "gotchas": [
            "UserGroup = a customer account (company). NOT an individual user.",
            "UserGroup.seller being set (OneToOne FK) means this is a SUPPLIER account, not a customer.",
            "`account_owner` on UserGroup is the sales rep (User FK), NOT the account's own admin or primary contact.",
            "Default ordering is by last calendar-month customer spend descending; pass `ordering=biggest_gap` to sort by target_monthly_gmv gap.",
            "Scoping uses user_groups_user_can_access_q — under impersonation, returns the impersonated user's accessible accounts.",
            "UserGroup.source = account creation origin (USER-GENERATED, PLANHUB) — NOT the marketing acquisition channel. Marketing channel (GOOGLE, META_ADS, SALES, etc.) lives on User.source. To filter accounts by acquisition channel, fetch api_v1_users_list and join via created_by.",
        ],
        "path": "/api/v1/user-groups/",
        "description": (
            "Returns accounts (UserGroups / companies) accessible to the authenticated context. "
            "A UserGroup is the company-level account entity that groups users and addresses together. "
            "Expandable: seller, account_owner, users, credit_applications, credit_limit_utilized, "
            "insurance_summary, latest_policies. "
            "Ordering: last calendar-month spend descending (default), or biggest_gap (target - actual spend). "
            "Use this to list all customer accounts, filter by industry or company size, "
            "count accounts with net terms, find accounts by name, "
            "or rank accounts by spend for prioritization."
        ),
        "filters": "id, search, has_seller, sales_status, lifecycle_status",
        "filter_enums": {
            "sales_status": ["icebox", "prospecting", "winback", "managed", "junk"],
            "lifecycle_status": ["never_ordered", "active", "at_risk", "churned"],
        },
        "method": "GET",
    },
    "api_v1_user_groups_get": {
        "entity": "UserGroup",
        "gotchas": [
            "`account_owner` is the sales rep, NOT the account admin.",
            "UserGroup.seller being set means this is a supplier account.",
            "Expandable fields: seller, account_owner, users, credit_applications, credit_limit_utilized, insurance_summary, latest_policies.",
        ],
        "path": "/api/v1/user-groups/{user_group_id}/",
        "description": (
            "Returns a single account (UserGroup) by ID with full details. "
            "Use expand[] params to include: seller, account_owner, users, credit_applications, "
            "credit_limit_utilized, insurance_summary, latest_policies."
        ),
        "method": "GET",
        "requires_id": True,
    },

    # ── USER IDENTITY ─────────────────────────────────────────────────────────

    "api_v1_user_identity_list": {
        "entity": "User|IdentityVerificationSession",
        "gotchas": [
            "Not a standalone model — combines User fields with IdentityVerificationSession data.",
            "Do not use this for user listing or cohort analysis; use api_v1_users_list for that.",
        ],
        "path": "/api/v1/user/identity/",
        "description": (
            "Returns identity verification state for the authenticated user and their account. "
            "Use this to check if the current user has completed identity verification."
        ),
    
        "method": "GET",
    },

    # ── USERS ─────────────────────────────────────────────────────────────────

    "api_v1_users_list": {
        "entity": "User",
        "gotchas": [
            "User = an individual person, NOT a company. For customer/account-level analysis always group at UserGroup level, not User level — multiple users from the same company share one UserGroup.",
            "Cohort and retention analysis partitioned by User will overcount distinct customers; partition by user_group instead.",
        ],
        "path": "/api/v1/users/",
        "description": (
            "Returns users scoped to the authenticated request context. "
            "Expandable: role, user_group.seller, user_group.account_owner, user_group.users, etc. "
            "Use this to count users per account, list users by type, "
            "find which accounts have onboarded users, or get user IDs for cohort analysis."
        ),
    
        "filters": "id, search, type, has_seller, user_group, user_address, email",
        "filter_enums": {
            "type": ["ADMIN", "BILLING", "MEMBER"],
        },
        "method": "GET",
    },
    "api_v1_users_me_list": {
        "entity": "User",
        "gotchas": [
            "Returns the currently authenticated user. Under impersonation, request.user is the impersonated user — /me returns the impersonated user's data, not the acting staff member.",
        ],
        "path": "/api/v1/users/me/",
        "description": (
            "Returns the currently authenticated user's full profile. "
            "Use this to identify who is making requests (role, account, type)."
        ),
    
        "method": "GET",
    },
    "api_v1_users_get": {
        "entity": "User",
        "path": "/api/v1/users/{user_id}/",
        "description": "Returns a single user by ID.",
        "method": "GET",
        "requires_id": True,
    },

    # ── WASTE TYPES ───────────────────────────────────────────────────────────

    "api_v1_waste_types_list": {
        "entity": "WasteType",
        "path": "/api/v1/waste-types/",
        "description": (
            "Static reference lookup — returns IDs and names for accepted material categories. "
            "Contains no transactional data, no order counts, no usage frequency, no rankings. "
            "Use only to get an ID or display label."
        ),
    
        "method": "GET",
    },
    "api_v1_waste_types_get": {
        "entity": "WasteType",
        "path": "/api/v1/waste-types/{id}/",
        "description": "Returns a single waste type by ID or slug.",
        "method": "GET",
        "requires_id": True,
    },

    # ── CHECKOUT ──────────────────────────────────────────────────────────────

    "checkout_v1_list": {
        "entity": "Cart",
        "gotchas": [
            "Returns a paginated list of Cart objects (not a checkout action). Path /checkout/v1/ is the Cart list view.",
        ],
        "path": "/checkout/v1/",
        "description": (
            "Returns a paginated list of Cart objects for the authenticated user. "
            "A Cart is a pre-order container — items added before checkout. "
            "Use this to count carts, track cart creation trends, or list active shopping sessions."
        ),
    
        "method": "GET",
    },
    "checkout_v1_cart_list": {
        "entity": "Cart",
        "gotchas": [
            "Lists open (non-submitted) Carts. One Cart per UserAddress.",
            "A submitted Cart (submitted_on set) is a placed order — no longer appears here.",
        ],
        "path": "/checkout/v1/cart/",
        "description": (
            "Returns the active cart for the authenticated user, structured as CartGroups of CartItems. "
            "Use this to inspect the contents of the current user's active cart."
        ),
    
        "method": "GET",
    },
    "checkout_v1_cart_count_list": {
        "entity": "Cart",
        "gotchas": [
            "Returns count of open (non-submitted) Carts only.",
        ],
        "path": "/checkout/v1/cart/count/",
        "description": (
            "Returns the total number of items in the authenticated user's active cart. "
            "Use this for the cart badge count in the navbar."
        ),
    
        "method": "GET",
    },
    "checkout_v1_carts_list": {
        "entity": "Cart",
        "gotchas": [
            "Returns grouped cart DTO with subtotal. allow_staff_all_access=False — staff cannot see all users' carts through this endpoint.",
        ],
        "path": "/checkout/v1/carts/",
        "description": (
            "Returns a list of carts with lightweight summary data. "
            "Use this to list carts by job site, count carts per account, or track cart activity."
        ),
        "filters": "search, delivery_range_after, delivery_range_before, user, past_deliveries, empty, user_group, user_address",
        "method": "GET",
    },
    "checkout_v1_carts_get": {
        "entity": "Cart",
        "gotchas": [
            "Returns grouped cart DTO for a specific UserAddress. allow_staff_all_access=False.",
        ],
        "path": "/checkout/v1/carts/{cart_id}/",
        "description": "Returns a single cart by ID with full CartGroup and CartItem details.",
        "method": "GET",
        "requires_id": True,
    },
    "checkout_v1_quote_accept_list": {
        "entity": "CartQuote",
        "gotchas": [
            "Accepting a quote transitions the cart toward checkout. Staff actors cannot accept quotes on behalf of users via this endpoint.",
        ],
        "path": "/checkout/v1/quote/accept/",
        "description": (
            "Returns the result of accepting a quote (converting a quote to a confirmed order). "
            "Use this to trigger quote acceptance in the checkout flow."
        ),
        "method": "POST",
    },
    "checkout_v1_quote_get": {
        "entity": "CartQuote",
        "gotchas": [
            "Quote is stored as a JSON blob on Cart.quote — not a separate model. Fields: to_emails, quote_expiration.",
        ],
        "path": "/checkout/v1/quote/{cart_id}/",
        "description": (
            "Price preview tool. Shows itemized cost before a buyer completes a purchase: "
            "line items, taxes, delivery fees, subtotal, total. Single-session use only."
        ),
        "method": "GET",
        "requires_id": True,
    },
    "checkout_v1_get": {
        "entity": "Cart",
        "gotchas": [
            "Returns a single Cart object by ID. Path /checkout/v1/<id>/ is the Cart detail view.",
        ],
        "path": "/checkout/v1/{id}/",
        "description": "Returns a single cart by ID.",
        "method": "GET",
        "requires_id": True,
    },

    # ── EXPLORE / SEARCH ──────────────────────────────────────────────────────

    "explore_v1_main_product_match_list": {
        "entity": "MainProduct",
        "gotchas": [
            "Returns MainProduct matches for a query — not Product (variant/SKU) records.",
        ],
        "path": "/explore/v1/main-product/match/",
        "description": (
            "Add-on configurator for the shop flow. "
            "Given a base item ID and a set of add-on selections, returns the matching variant. "
            "Transactional UI helper — no historical data, no aggregation, no reporting."
        ),
    
        "method": "POST",
    },
    "explore_v1_search_list": {
        "entity": "MainProduct|MainProductCategory|MainProductCategoryGroup",
        "gotchas": [
            "AllowAny permission — no authentication required.",
            "Results cached for 1 hour.",
            "Searches across MainProduct, MainProductCategory, and MainProductCategoryGroup — not order or transaction data.",
        ],
        "path": "/explore/v1/search/",
        "description": (
            "Full-text search over the Downstream product catalog: MainProducts, MainProductCategories, MainProductCategoryGroups. "
            "Parameters: q (search query, required), seller_location (filter to location), allows_pickup (boolean filter). "
            "Returns: main_products (id, name, category, images, tags), "
            "main_product_categories (id, name, slug, group), "
            "main_product_category_groups (id, name, icon). "
            "Use this to search for products by name, find what categories match a query, "
            "or look up products available at a specific location."
        ),
    
        "method": "GET",
    },

    # ── FINANCIAL ACCOUNTS ────────────────────────────────────────────────────

    "financial_accounts_v1_financial_connection_account_list": {
        "entity": "FinancialConnectionAccount",
        "gotchas": [
            "Scoped to the user's user_group if they have one; otherwise scoped to the user directly.",
        ],
        "path": "/financial-accounts/v1/financial-connection-account/",
        "description": (
            "Returns Plaid-linked financial connection accounts (bank accounts) for the authenticated user group. "
            "Use this to list connected bank accounts for an account."
        ),
    
        "method": "GET",
    },
    "financial_accounts_v1_financial_connection_account_get": {
        "entity": "FinancialConnectionAccount",
        "path": "/financial-accounts/v1/financial-connection-account/{id}/",
        "description": "Returns a single financial connection account by ID.",
        "method": "GET",
        "requires_id": True,
    },
    "financial_accounts_v1_financial_statement_list": {
        "entity": "FinancialStatement",
        "path": "/financial-accounts/v1/financial-statement/",
        "description": (
            "Returns financial statements (bank transaction data) for connected accounts via Plaid. "
            "Use this to retrieve bank transaction history for an account."
        ),
    
        "method": "GET",
    },
    "financial_accounts_v1_financial_statement_get": {
        "entity": "FinancialStatement",
        "path": "/financial-accounts/v1/financial-statement/{id}/",
        "description": "Returns a single financial statement by ID.",
        "method": "GET",
        "requires_id": True,
    },

    # ── MATCHING ENGINE ───────────────────────────────────────────────────────

    "matching_engine_v1_product_match_list": {
        "entity": "SellerProductSellerLocation",
        "gotchas": [
            "POST endpoint. Supply `main_product` ID plus optional `main_product_add_on_choices`. Returns matched SellerProductSellerLocation records — supplier-product-location combinations, not abstract MainProduct records.",
        ],
        "path": "/matching-engine/v1/product-match/",
        "description": (
            "Returns supplier matches for a given product request. "
            "Input: product_id, user_address (delivery location), waste_type (optional). "
            "Returns ranked list of SellerProductSellerLocations that can fulfill the request. "
            "Use this to find which suppliers can fulfill a product request at a given address."
        ),
    
        "method": "POST",
    },
    "matching_engine_v1_seller_product_seller_locations_by_lat_long_list": {
        "entity": "SellerProductSellerLocation",
        "gotchas": [
            "Geospatial SPSL lookup by latitude/longitude — returns listings near a given coordinate.",
        ],
        "path": "/matching-engine/v1/seller-product-seller-locations-by-lat-long/",
        "description": (
            "Returns supplier matches for a product request using lat/long coordinates instead of address. "
            "Input: product ID, latitude, longitude, waste_type (optional). "
            "Returns ranked SellerProductSellerLocations sorted by distance and price. "
            "Use this when you have coordinates but not a structured address."
        ),
    
        "method": "POST",
    },

    # ── NOTIFICATIONS ─────────────────────────────────────────────────────────

    "notifications_v1_push_notifications_list": {
        "entity": "PushNotification",
        "path": "/notifications/v1/push-notifications/",
        "description": (
            "Returns push notification records sent to the authenticated user. "
            "Use this to list recent notifications for a user."
        ),
    
        "method": "GET",
    },
    "notifications_v1_push_notifications_get": {
        "entity": "PushNotification",
        "path": "/notifications/v1/push-notifications/{id}/",
        "description": "Returns a single push notification by ID.",
        "method": "GET",
        "requires_id": True,
    },

    # ── PRICING ENGINE ────────────────────────────────────────────────────────

    "pricing_engine_v1_seller_product_seller_location_pricing_by_lat_long_list": {
        "entity": "SellerProductSellerLocation",
        "gotchas": [
            "Pricing lookup by lat/long instead of user_address ID — used for unauthenticated or pre-address-creation pricing estimates.",
            "Returns computed pricing only — not a stored record.",
        ],
        "path": "/pricing-engine/v1/seller-product-seller-location-pricing-by-lat-long/",
        "description": (
            "Returns pricing for a specific seller-product-at-location listing, calculated for delivery to given coordinates. "
            "Input: seller_product_seller_location ID, latitude, longitude. "
            "Returns: base_price, delivery_fee, total_price, rental_period, fuel_surcharge. "
            "Use this to get the exact price a customer at given coordinates would pay for a listing."
        ),
    
        "method": "POST",
    },
    "pricing_engine_v1_seller_product_seller_location_pricing_list": {
        "entity": "SellerProductSellerLocation",
        "gotchas": [
            "POST endpoint. Requires: seller_product_seller_location, user_address, waste_type, start_date, end_date, times_per_week, shift_count.",
            "Returns computed pricing for a specific SPSL at a specific job site — not a stored record.",
        ],
        "path": "/pricing-engine/v1/seller-product-seller-location-pricing/",
        "description": (
            "Returns pricing for a specific seller-product-at-location listing, calculated for delivery to a given address. "
            "Input: seller_product_seller_location ID, user_address (string). "
            "Returns: base_price, delivery_fee, total_price, rental_period, fuel_surcharge. "
            "Use this to get the price a customer at a specific address would pay."
        ),
        "method": "POST",
    },
    "pricing_engine_v1_supplier_insights_list": {
        "entity": "SellerLocation",
        "gotchas": [
            "Returns insights aggregated per SellerLocation — performance and pricing signals scoped to a supplier's specific service location.",
        ],
        "path": "/pricing-engine/v1/supplier-insights/",
        "description": (
            "Local market competitiveness check for a single buyer address. "
            "How many vendors serve a specific delivery location and what the local benchmark cost is. "
            "Requires a specific location — not an analytics or reporting endpoint."
        ),
    
        "method": "POST",
    },
    # ── IMPERSONATION ─────────────────────────────────────────────────────────

    "impersonation_start": {
        "entity": "User",
        "gotchas": [
            "Staff-only. After impersonation starts: request.user = impersonated user, request.auth = acting staff.",
            "All scoped endpoints will return data as seen by the impersonated user.",
        ],
        "path": None,
        "description": (
            "Start impersonating a specific user by UUID. "
            "All subsequent API calls will be scoped to that user's data. "
            "Use when switching context to act on behalf of a specific user."
        ),
        "method": "POST",
    },
    "impersonation_end": {
        "entity": "User",
        "gotchas": [
            "Ends impersonation session. Restores request.user to the acting staff user.",
        ],
        "path": None,
        "description": (
            "Stop impersonating the current user and revert to normal authentication. "
            "Use after finishing work scoped to an impersonated user."
        ),
        "method": "POST",
    },
    "impersonation_status": {
        "entity": "User",
        "gotchas": [
            "Under active impersonation, request.user is the impersonated user — check request.auth (not request.user) to identify the acting staff member.",
        ],
        "path": None,
        "description": (
            "Check whether impersonation is currently active and which user is being impersonated. "
            "Use when you need to know the current impersonation state."
        ),
        "method": "GET",
    },

}


def get_tool_catalog_text() -> str:
    lines = []
    for name, info in MCP_TOOL_CATALOG.items():
        lines.append("  " + name + "\n    -> " + info["description"])
    return "\n".join(lines)
