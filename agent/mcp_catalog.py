# MCP tool catalog — 141 tools from downstream-mcp
# Descriptions written from TG-API-proxy source (views, serializers, services) + DB schema.
# Richer descriptions improve Chroma RAG accuracy for analytics tool selection.

MCP_TOOL_CATALOG = {

    # ── ENRICHMENT ────────────────────────────────────────────────────────────

    "api_enrichment_phone_reveal_account_usage_get": {
        "path": "/api/enrichment/phone-reveal/account-usage/{user_group_id}/",
        "description": (
            "Returns the phone-reveal usage count for a specific user group (account) against its monthly cap. "
            "Fields: reveals_used, reveals_cap, user_group_id. "
            "Use this to check how many phone numbers have been revealed for a given account and whether the quota is exhausted."
        ),
        "fields": "reveals_used (int), reveals_cap (int), user_group_id (int)",
        "method": "GET",
        "requires_id": True,
    },
    "api_enrichment_phone_reveal_quota_list": {
        "path": "/api/enrichment/phone-reveal/quota/",
        "description": (
            "Returns the current monthly phone-reveal quota status for the authenticated org. "
            "Fields: quota_used, quota_total, quota_remaining, reset_date. "
            "Use this to check org-wide phone reveal limits and remaining capacity."
        ),
    
        "fields": "quota_used (int), quota_total (int), quota_remaining (int), reset_date (date)",
        "method": "GET",
    },
    "api_enrichment_user_groups_suggested_coworkers_list": {
        "path": "/api/enrichment/user-groups/{user_group_id}/suggested-coworkers/",
        "description": (
            "Returns Apollo-sourced people at the same company domain as the given user group, suitable for invite suggestions. "
            "Fields: first_name, last_name, email, title, linkedin_url. "
            "Use this to find potential new users to invite to an account based on company email domain."
        ),
        "fields": "first_name (str), last_name (str), email (str), title (str), linkedin_url (str)",
        "method": "GET",
        "requires_id": True,
    },

    # ── INSIGHT HUB (pre-computed sales analytics) ────────────────────────────

    "api_insight_hub_account_classification_list": {
        "path": "/api/insight-hub/account-classification/",
        "description": (
            "Pre-computed revenue breakdown for a date range by account classification: "
            "Net New GMV (first-time customers), Expansion GMV (returning customers), and Backlog GMV (scheduled/pipeline orders). "
            "Summary fields: net_new_gmv, expansion_gmv, backlog_gmv, total_gmv, net_new_accounts, expansion_accounts, backlog_orders. "
            "Also returns monthly_trend array with month + gmv per month. "
            "Filters: start_date, end_date, rep_id, team_id, industry, company_size. "
            "Use this for revenue attainment vs target, new vs returning customer revenue split, pipeline value, "
            "monthly GMV trend, or sales territory performance."
        ),
        "fields": (
            "net_new_gmv (float), expansion_gmv (float), backlog_gmv (float), total_gmv (float), "
            "net_new_accounts (int), expansion_accounts (int), backlog_orders (int), "
            "monthly_trend (JSON str: [{month (YYYY-MM), gmv}])"
        ),
        "method": "GET",
    },
    "api_insight_hub_account_growth_list": {
        "path": "/api/insight-hub/account-growth/",
        "description": (
            "Pre-computed customer acquisition and churn metrics for a date range. "
            "Summary fields: net_new (new customers), churned (lost customers), retained, net_growth. "
            "Also returns net_new_accounts list (id, name, first_order_date), churned_accounts list (id, name, last_order_date), "
            "and monthly_trend with net_new per month. "
            "Filters: start_date, end_date. "
            "Use this for customer acquisition rate, churn rate, net customer growth, retention analysis, "
            "or to identify which specific accounts were won or lost in a period."
        ),
        "fields": (
            "net_new (int), churned (int), retained (int), net_growth (int), "
            "net_new_accounts (JSON str: [{id, name, first_order_date}]), "
            "churned_accounts (JSON str: [{id, name, last_order_date}]), "
            "monthly_trend (JSON str: [{month (YYYY-MM), net_new}])"
        ),
        "method": "GET",
    },
    "api_insight_hub_commissions_list": {
        "path": "/api/insight-hub/commissions/",
        "description": (
            "Pre-computed commission calculations for all sales reps for a given month. "
            "Returns commission_rate_percent, summary (total_commission_eligible, total_commission, total_in_cart, total_scheduled), "
            "reps array (rep_id, rep_name, commission_eligible, commission, in_cart, scheduled), "
            "and monthly_trend (month, total commission). "
            "Filters: month (YYYY-MM format). "
            "Use this for sales rep compensation analysis, commission payout totals, "
            "or to see how much GMV is in-cart vs scheduled vs already completed for commission purposes."
        ),
        "fields": (
            "commission_rate_percent (float), "
            "summary.total_commission_eligible (float), summary.total_commission (float), "
            "summary.total_in_cart (float), summary.total_scheduled (float), "
            "reps (JSON str: [{rep_id, rep_name, commission_eligible, commission, in_cart, scheduled}]), "
            "monthly_trend (JSON str: [{month, total_commission}])"
        ),
        "method": "GET",
    },
    "api_insight_hub_customer_spend_mom_list": {
        "path": "/api/insight-hub/customer-spend-mom/",
        "description": (
            "Pre-computed month-over-month spend breakdown by customer (user group / account). "
            "Returns customers array (user_group_id, user_group_name, month, spend) "
            "and monthly_totals array (month, total_spend). "
            "Filters: start_date, end_date, user_group_id. "
            "Use this for customer spend trends, top-spending accounts by month, "
            "spend concentration (which customers drive most revenue), "
            "or to identify accounts with declining or growing spend over time."
        ),
        "fields": "user_group_id (int), user_group_name (str), month (str YYYY-MM), spend (float)",
        "method": "GET",
    },
    "api_insight_hub_first_touch_to_order_list": {
        "path": "/api/insight-hub/first-touch-to-order/",
        "description": (
            "Sales cycle speed metric — how many days from first email outreach to first order. "
            "Returns average_days (mean days), total_conversions, and details per account. "
            "Filters: start_date, end_date. "
            "Use this for outreach-to-order speed, sales cycle length, or email response latency. "
            "Not suitable for funnel stage drop-off or cart-to-order rate — use api_insight_hub_sales_funnel_list for those."
        ),
    
        "fields": "average_days (float), total_conversions (int)",
        "method": "GET",
    },
    "api_insight_hub_gmv_by_state_list": {
        "path": "/api/insight-hub/gmv-by-state/",
        "description": (
            "Pre-computed gross merchandise value (GMV) aggregated by US state for a date range. "
            "Returns states array with: state (two-letter code), gmv (total order value), order_count. "
            "Filters: start_date, end_date. "
            "Use this for geographic revenue distribution, top states by GMV, "
            "state-level market penetration, or regional sales comparison."
        ),
        "fields": "state (str, two-letter code), gmv (float), order_count (int)",
        "method": "GET",
    },
    "api_insight_hub_gmv_mom_list": {
        "path": "/api/insight-hub/gmv-mom/",
        "description": (
            "Pre-computed gross merchandise value (GMV) and platform economics month-over-month. "
            "Returns months array with: month (YYYY-MM), gmv (total customer spend), supplier_cost (total paid to sellers), "
            "net_revenue (Downstream margin = gmv - supplier_cost), take_rate_percent (net_revenue / gmv * 100), "
            "aov (average order value), order_count. "
            "Filters: start_date, end_date. "
            "Use this for revenue trends, platform margin trends, average order value trends, "
            "order volume trends, or MoM growth rate calculations."
        ),
        "fields": "month (str YYYY-MM), gmv (float), supplier_cost (float), net_revenue (float), take_rate_percent (float), aov (float), order_count (int)",
        "method": "GET",
    },
    "api_insight_hub_product_mix_list": {
        "path": "/api/insight-hub/product-mix/",
        "description": (
            "Order volume by waste type or service category. "
            "Top waste types ranked by how many orders were placed for each. "
            "Which material categories are ordered most. Frequency and share of each service type. "
            "Pre-computed: category name, order_count, percent of total orders, total_orders. "
            "Filters: start_date, end_date."
        ),
        "fields": "name (str), order_count (int), percent (float), total_orders (int)",
        "method": "GET",
    },
    "api_insight_hub_quota_vs_actual_list": {
        "path": "/api/insight-hub/quota-vs-actual/",
        "description": (
            "Pre-computed sales rep quota attainment vs actual performance, per rep per month. "
            "Returns rows array with: rep_id, rep_name, month (YYYY-MM), "
            "gmv_target, gmv_actual, attainment_percent (gmv_actual / gmv_target * 100), "
            "new_accounts_target, new_accounts_actual, orders_target, orders_actual. "
            "Filters: start_date, end_date, rep_id. "
            "Use this for sales rep performance review, quota attainment ranking, "
            "which reps are hitting or missing targets, or team-level attainment rollup."
        ),
        "fields": "rep_id (int), rep_name (str), month (str YYYY-MM), gmv_target (float), gmv_actual (float), attainment_percent (float), new_accounts_target (int), new_accounts_actual (int), orders_target (int), orders_actual (int)",
        "method": "GET",
    },
    "api_insight_hub_quotas_list": {
        "path": "/api/insight-hub/quotas/",
        "description": (
            "Returns the raw sales quota targets set for each sales rep by month. "
            "Fields: id, rep_id, month (YYYY-MM date), gmv_target, new_accounts_target, orders_target. "
            "Use this to retrieve the quota plan for a rep, check what targets are set for a given month, "
            "or verify quota coverage across the team."
        ),
    
        "fields": "id (int), rep_id (int), month (str YYYY-MM), gmv_target (float), new_accounts_target (int), orders_target (int)",
        "method": "GET",
    },
    "api_insight_hub_sales_funnel_list": {
        "path": "/api/insight-hub/sales-funnel/",
        "description": (
            "Conversion rate from cart to confirmed order. Drop-off rate at each stage of the sales funnel. "
            "Cart-to-quote rate, quote-to-close rate, overall win rate, which stage loses the most deals. "
            "Pre-computed funnel with stage-by-stage counts and GMV: cart, quote, order, invoice, payment. "
            "Returns stages array (stage name, count, gmv) and conversion_rates (cart_to_quote, quote_to_close, overall). "
            "Filters: start_date, end_date."
        ),
        "fields": (
            "stages (JSON str: [{stage, count, gmv}]), "
            "conversion_rates.cart_to_quote (float), conversion_rates.quote_to_close (float), conversion_rates.overall (float)"
        ),
        "method": "GET",
    },
    "api_insight_hub_spend_by_product_list": {
        "path": "/api/insight-hub/spend-by-product/",
        "description": (
            "Pre-computed revenue (GMV) and average order value aggregated by product category / waste type. "
            "Best tool for: which product categories generate the most revenue, average order value by product type, "
            "top products by GMV, product revenue ranking, product-level AOV comparison, revenue breakdown by service type. "
            "Returns products array with: main_product_name, gmv (total revenue), order_count, aov (average order value). "
            "Filters: start_date, end_date, user_group_id. "
            "Use this whenever the question asks about revenue, GMV, or AOV broken down by product or service type."
        ),
        "fields": "main_product_name (str), gmv (float), order_count (int), aov (float)",
        "method": "GET",
    },
    "api_insight_hub_spend_by_supplier_list": {
        "path": "/api/insight-hub/spend-by-supplier/",
        "description": (
            "Pre-computed customer spend aggregated by supplier (seller). "
            "Returns suppliers array with: seller_id, seller_name, gmv (total spend routed to this seller). "
            "Filters: start_date, end_date, user_group_id. "
            "Use this for supplier concentration analysis, top sellers by GMV, "
            "how much spend goes to each vendor, or supplier diversification metrics."
        ),
        "fields": "seller_id (int), seller_name (str), gmv (float)",
        "method": "GET",
    },
    "api_insight_hub_take_rate_mom_list": {
        "path": "/api/insight-hub/take-rate-mom/",
        "description": (
            "Platform take rate trend over time. Downstream margin percentage month-over-month or year-over-year. "
            "Net revenue and take rate percent per rep per month. Annual/monthly platform margin trend. "
            "Returns rows: rep_id, rep_name, month (YYYY-MM), customer_total (GMV), "
            "seller_total (supplier cost), net_revenue, take_rate_percent. "
            "Filters: start_date, end_date, rep_id."
        ),
        "fields": "rep_id (int), rep_name (str), month (str YYYY-MM), customer_total (float), seller_total (float), net_revenue (float), take_rate_percent (float)",
        "method": "GET",
    },

    # ── ADMIN / INTERNAL ──────────────────────────────────────────────────────

    "api_v1_admin_communications_list": {
        "path": "/api/v1/admin/communications/",
        "description": (
            "Admin-only. Returns communication timeline entries for a single user ordered most-recent-first. "
            "Includes emails sent, calls logged, and notes. "
            "Filter: user_id. "
            "Use this to audit outreach history for a specific rep or customer."
        ),
    
        "fields": "id (int), type (str: email/call/note), subject (str), body (str), created_by (str), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_admin_internal_hierarchy_org_chart_list": {
        "path": "/api/v1/admin/internal-hierarchy/org-chart/",
        "description": (
            "Admin-only. Returns the canonical Downstream internal org chart: teams, managers, and rep assignments. "
            "Use this to look up team structure, find which rep belongs to which team, "
            "or identify reporting relationships."
        ),
    
        "fields": "team_id (int), team_name (str), manager_id (int), manager_name (str), reps (JSON str: [{rep_id, rep_name}])",
        "method": "GET",
    },
    "api_v1_admin_sales_target_vs_actuals_list": {
        "path": "/api/v1/admin/sales/target-vs-actuals/",
        "description": (
            "Admin-only. Returns aggregate GMV pacing metrics and cumulative daily comparison against the prior month. "
            "Includes current month actuals, target, and prior-month comparison on a daily basis. "
            "Use this for daily sales pacing dashboards, are-we-on-track analysis, "
            "or current month vs prior month performance."
        ),
    
        "fields": "date (date), actual_gmv (float), target_gmv (float), prior_month_gmv (float), cumulative_actual (float), cumulative_target (float)",
        "method": "GET",
    },
    "api_v1_admin_transactional_emails_list": {
        "path": "/api/v1/admin/transactional-emails/",
        "description": (
            "Admin-only. Returns sent transactional emails addressed to a specific user, ordered most-recent-first. "
            "Filter: user_id. "
            "Use this to check which system emails were sent to a user (order confirmations, invoices, etc.)."
        ),
    
        "fields": "id (int), subject (str), template (str), sent_at (datetime), status (str)",
        "method": "GET",
    },
    "api_v1_admin_user_addresses_goal_progress_list": {
        "path": "/api/v1/admin/user-addresses/{user_address_id}/goal-progress/",
        "description": (
            "Admin-only. Returns value and count metrics for a specific project (UserAddress): "
            "cart value, order group count, order count, invoice totals. "
            "Use this to track progress of a specific job site toward its spend goal."
        ),
        "fields": "cart_value (float), order_group_count (int), order_count (int), invoice_total (float)",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_admin_user_groups_goal_progress_aggregate_list": {
        "path": "/api/v1/admin/user-groups/goal-progress/aggregate/",
        "description": (
            "Admin-only. Returns aggregate goal progress across all user groups: "
            "total target GMV, total actual GMV, attainment percentage, account count. "
            "Use this for platform-wide goal attainment rollup or pipeline health overview."
        ),
    
        "fields": "total_target_gmv (float), total_actual_gmv (float), attainment_percent (float), account_count (int)",
        "method": "GET",
    },
    "api_v1_admin_user_groups_spend_potential_list": {
        "path": "/api/v1/admin/user-groups/spend-potential/",
        "description": (
            "Admin-only. Returns advisory monthly spend-potential estimates for all user groups. "
            "Uses conservative product-fit heuristics and recent order history to estimate how much each account could spend. "
            "Fields: user_group_id, user_group_name, estimated_monthly_spend, confidence. "
            "Use this for account prioritization, TAM estimation per account, or whitespace analysis."
        ),
    
        "fields": "user_group_id (int), user_group_name (str), estimated_monthly_spend (float), confidence (str)",
        "method": "GET",
    },
    "api_v1_admin_user_groups_enrichment_list": {
        "path": "/api/v1/admin/user-groups/{user_group_id}/enrichment/",
        "description": (
            "Admin-only. Returns enrichment data stored for a user group from third-party providers (Apollo, Clearbit, etc.). "
            "Includes company size, employee count, industry, revenue range, LinkedIn URL, and raw provider payloads. "
            "Use this to look up firmographic data for an account."
        ),
        "fields": "company_size (str), employee_count (int), industry (str), revenue_range (str), linkedin_url (str)",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_admin_user_groups_goal_progress_list": {
        "path": "/api/v1/admin/user-groups/{user_group_id}/goal-progress/",
        "description": (
            "Admin-only. Returns goal, current value, and supporting metrics for a specific user group (account): "
            "target GMV, actual GMV, attainment percent, order count, invoice totals. "
            "Use this to check how a specific account is tracking against its spend goal."
        ),
        "fields": "user_group_id (int), user_group_name (str), target_gmv (float), actual_gmv (float), attainment_percent (float), order_count (int)",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_admin_user_groups_notes_list": {
        "path": "/api/v1/admin/user-groups/{user_group_id}/notes/",
        "description": (
            "Admin-only. Returns all CRM notes recorded for a specific account (user group) in descending creation order. "
            "Fields: id, content, created_by, created_on. "
            "Use this to retrieve account notes or activity log for a customer."
        ),
        "fields": "id (int), content (str), created_by (str), created_on (datetime)",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_admin_user_groups_sales_state_list": {
        "path": "/api/v1/admin/user-groups/{user_group_id}/sales-state/",
        "description": (
            "Admin-only. Returns the current manual sales status and derived lifecycle metadata for an account: "
            "sales_state (prospect/active/churned/etc.), days_since_last_order, lifecycle_stage. "
            "Use this to check the CRM status of a customer or identify accounts at risk."
        ),
        "fields": "sales_state (str), days_since_last_order (int), lifecycle_stage (str)",
        "method": "GET",
        "requires_id": True,
    },

    # ── ADVERTISEMENTS ────────────────────────────────────────────────────────

    "api_v1_advertisements_list": {
        "path": "/api/v1/advertisements/",
        "description": (
            "Returns all advertisements (promotional banners/placements) configured in the platform. "
            "Fields: id, title, image_url, target_url, seller, placement, is_active, start_date, end_date. "
            "Filters: seller_id, placement, is_active. "
            "Use this to list active promotions, see which sellers are advertising, or audit ad inventory."
        ),
    
        "fields": "id (int), title (str), image_url (str), target_url (str), placement (str), is_active (bool), start_date (date), end_date (date)",
        "method": "GET",
    },
    "api_v1_advertisements_get": {
        "path": "/api/v1/advertisements/{id}/",
        "description": (
            "Returns a single advertisement by ID. "
            "Fields: id, title, image_url, target_url, seller, placement, is_active, start_date, end_date. "
            "Use this to retrieve details of a specific ad placement."
        ),
        "fields": "id (int), title (str), image_url (str), target_url (str), placement (str), is_active (bool), start_date (date), end_date (date)",
        "method": "GET",
        "requires_id": True,
    },

    # ── BRANDS ────────────────────────────────────────────────────────────────

    "api_v1_brands_list": {
        "path": "/api/v1/brands/",
        "description": (
            "Returns all product brands in the catalog. Supports name search. "
            "Fields: id, name, slug, logo_url. "
            "Use this to list brands, search for a specific brand, or get brand IDs for filtering products."
        ),
    
        "fields": "id (int), name (str), slug (str), logo_url (str)",
        "method": "GET",
    },
    "api_v1_brands_get": {
        "path": "/api/v1/brands/{id}/",
        "description": (
            "Returns a single brand by ID. "
            "Fields: id, name, slug, logo_url. "
        ),
        "fields": "id (int), name (str), slug (str), logo_url (str)",
        "method": "GET",
        "requires_id": True,
    },

    # ── DAY OF WEEKS ──────────────────────────────────────────────────────────

    "api_v1_day_of_weeks_list": {
        "path": "/api/v1/day-of-weeks/",
        "description": (
            "Returns the lookup table of day-of-week records used by seller open hours. "
            "Fields: id, name (e.g. MONDAY, TUESDAY). "
            "Use this to get the UUID for a day name when setting or querying open hours."
        ),
    
        "fields": "id (int), name (str: MONDAY/TUESDAY/WEDNESDAY/THURSDAY/FRIDAY/SATURDAY/SUNDAY)",
        "method": "GET",
    },
    "api_v1_day_of_weeks_get": {
        "path": "/api/v1/day-of-weeks/{id}/",
        "description": "Returns a single day-of-week record by ID.",
        "fields": "id (int), name (str)",
        "method": "GET",
        "requires_id": True,
    },

    # ── FINANCIAL CONNECTION ──────────────────────────────────────────────────

    "api_v1_financial_connection_list": {
        "path": "/api/v1/financial-connection/",
        "description": (
            "Returns Plaid financial connection records linked to the authenticated user group. "
            "Fields: id, institution_name, status, linked_accounts_count, created_on. "
            "Use this to check if an account has connected their bank account."
        ),
    
        "fields": "id (int), institution_name (str), status (str), linked_accounts_count (int), created_on (datetime)",
        "method": "GET",
    },

    # ── GROUP INVOICES ────────────────────────────────────────────────────────

    "api_v1_group_invoices_list": {
        "path": "/api/v1/group_invoices/",
        "description": (
            "Returns grouped invoices (consolidated billing statements) visible to the authenticated customer context. "
            "A GroupInvoice bundles multiple individual invoices into one statement. "
            "Fields: id, user_group, total, status, invoice_count, due_date, created_on. "
            "Use this for account-level billing summaries or consolidated payment tracking."
        ),
    
        "fields": "id (int), total (float), status (str), invoice_count (int), due_date (date), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_group_invoices_get": {
        "path": "/api/v1/group_invoices/{id}/",
        "description": "Returns a single grouped invoice by ID with its constituent invoices.",
        "fields": "id (int), total (float), status (str), invoice_count (int), due_date (date), created_on (datetime)",
        "method": "GET",
        "requires_id": True,
    },

    # ── IDENTITY VERIFICATION ─────────────────────────────────────────────────

    "api_v1_identity_verification_list": {
        "path": "/api/v1/identity-verification/",
        "description": (
            "Returns identity verification status for the authenticated user's account. "
            "Fields: status, verified_at, provider. "
            "Use this to check if an account has completed KYC/identity verification."
        ),
    
        "fields": "status (str), verified_at (datetime), provider (str)",
        "method": "GET",
    },

    # ── INDUSTRIES ────────────────────────────────────────────────────────────

    "api_v1_industries_list": {
        "path": "/api/v1/industries/",
        "description": (
            "Returns all industry classifications used to categorize customer accounts (user groups). "
            "Fields: id, name, slug, icon, sort_order. "
            "Examples: construction, landscaping, demolition, roofing, plumbing. "
            "Use this to get industry IDs for filtering accounts, or to list all supported industries."
        ),
    
        "fields": "id (int), name (str), slug (str), sort_order (int)",
        "method": "GET",
    },
    "api_v1_industries_get": {
        "path": "/api/v1/industries/{id}/",
        "description": "Returns a single industry by ID or slug.",
        "fields": "id (int), name (str), slug (str), sort_order (int)",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_industries_popular_products_list": {
        "path": "/api/v1/industries/{id}/popular-products/",
        "description": (
            "Returns the most popular products (waste/service types) for a given industry, ranked by order COUNT (not revenue). "
            "Fields: main_product_id, main_product_name, order_count, rank. "
            "Requires an industry_id — not suitable for cross-industry revenue comparisons. "
            "Use this to understand which products are most frequently ordered within a specific industry, "
            "for industry-specific product recommendations, or to identify demand patterns per vertical. "
            "Do NOT use this for product revenue ranking — use api_insight_hub_spend_by_product_list for revenue."
        ),
        "fields": "main_product_id (int), main_product_name (str), order_count (int), rank (int)",
        "method": "GET",
        "requires_id": True,
    },

    # ── INSURANCE POLICIES ────────────────────────────────────────────────────

    "api_v1_insurance_policies_list": {
        "path": "/api/v1/insurance-policies/",
        "description": (
            "Returns insurance policies on file for accounts. "
            "Fields: id, account, account_type (seller/buyer), type (general_liability/equipment_liability/umbrella), "
            "status (valid/expired/pending), effective_date, expiration_date, insurer, coverage_amount. "
            "Filters: account, account_type, type, status. "
            "Use this to check insurance compliance, find expired policies, or count accounts with valid coverage."
        ),
    
        "fields": "id (int), account_type (str: seller/buyer), type (str), status (str: valid/expired/pending), effective_date (date), expiration_date (date), insurer (str), coverage_amount (float)",
        "method": "GET",
    },
    "api_v1_insurance_policies_get": {
        "path": "/api/v1/insurance-policies/{insurance_policy_id}/",
        "description": "Returns a single insurance policy by ID.",
        "fields": "id (int), account_type (str), type (str), status (str), effective_date (date), expiration_date (date), insurer (str), coverage_amount (float)",
        "method": "GET",
        "requires_id": True,
    },

    # ── INVOICES ──────────────────────────────────────────────────────────────

    "api_v1_invoices_list": {
        "path": "/api/v1/invoices/",
        "description": (
            "Returns invoices visible to the authenticated context (customer sees their invoices; "
            "staff/admin with allow_all=true sees all invoices). "
            "Fields: id, number, status (open/paid/void/past_due), total, amount_due, amount_paid, "
            "amount_remaining, due_date, created_on, updated_on, user_address, order_group, user_group. "
            "Supports ordering by: created_on, due_date, total, amount_due, amount_paid, status. "
            "Filters: status, user_address_id, order_group_id, user_group_id. "
            "Use this for invoice aging analysis, outstanding balance tracking, payment collection metrics, "
            "or to list unpaid invoices for an account."
        ),
        "fields": "id (int), number (str), status (str: open/paid/void/past_due), total (float), amount_due (float), amount_paid (float), amount_remaining (float), due_date (date), created_on (datetime), user_group_id (int)",
        "method": "GET",
    },
    "api_v1_invoices_metrics_list": {
        "path": "/api/v1/invoices/metrics/",
        "description": (
            "Returns aggregate invoice totals for the current scope: "
            "past_due_total (overdue amount), outstanding_total (open unpaid), paid_total (collected). "
            "Use this for AR summary, total outstanding balance, or collections health at a glance."
        ),
        "fields": "past_due_total (float), outstanding_total (float), paid_total (float)",
        "method": "GET",
    },
    "api_v1_invoices_get": {
        "path": "/api/v1/invoices/{id}/",
        "description": "Returns a single invoice by ID with full details.",
        "fields": "id (int), number (str), status (str), total (float), amount_due (float), amount_remaining (float), due_date (date), created_on (datetime)",
        "method": "GET",
        "requires_id": True,
    },

    # ── KNOWLEDGE ─────────────────────────────────────────────────────────────

    "api_v1_knowledge_list": {
        "path": "/api/v1/knowledge/",
        "description": (
            "Returns the list of knowledge documents (help articles, internal docs) in the Downstream knowledge base. "
            "Fields: id, slug, title, visibility (public/internal), created_on. "
            "Use this to browse available documentation."
        ),
    
        "fields": "id (int), slug (str), title (str), visibility (str: public/internal), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_knowledge_search_list": {
        "path": "/api/v1/knowledge/search/",
        "description": (
            "Semantic vector search over the Downstream knowledge base. "
            "Returns ranked knowledge_document chunks matching the query. "
            "Fields per result: document_id, slug, heading, score, excerpt, metadata. "
            "Parameters: query (string). "
            "Use this to find documentation, policies, or internal knowledge relevant to a topic. "
            "Note: this is a docs search, NOT a data query — it searches help content, not transactional data."
        ),
    
        "fields": "document_id (int), slug (str), heading (str), score (float), excerpt (str)",
        "method": "POST",
    },
    "api_v1_knowledge_get": {
        "path": "/api/v1/knowledge/{knowledge_document_id}/",
        "description": "Returns a single knowledge document by ID, including full content.",
        "fields": "id (int), slug (str), title (str), content (str), visibility (str), created_on (datetime)",
        "method": "GET",
        "requires_id": True,
    },

    # ── LEADS ─────────────────────────────────────────────────────────────────

    "api_v1_leads_list_list": {
        "path": "/api/v1/leads/list/",
        "description": (
            "Admin-only. Returns inbound leads captured from the platform. "
            "Fields: id, email, name, company, phone, source, created_on, status. "
            "Use this to list new leads, track lead volume by source, or audit CRM intake."
        ),
    
        "fields": "id (int), email (str), name (str), company (str), phone (str), source (str), status (str), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_leads_meta_webhook_list": {
        "path": "/api/v1/leads/meta/webhook/",
        "description": (
            "Webhook verification endpoint for Meta (Facebook/Instagram) lead forms. "
            "Not useful for analytics — used for integration setup only."
        ),
    
        "fields": "hub.mode (str), hub.challenge (str), hub.verify_token (str)",
        "method": "GET",
    },

    # ── MAIN PRODUCTS ─────────────────────────────────────────────────────────

    "api_v1_main_product_categories_list": {
        "path": "/api/v1/main-product-categories/",
        "description": (
            "Returns product categories in the Downstream catalog. "
            "Fields: id, name, slug, group (category group), icon, sort, popularity. "
            "Examples: roll-off dumpsters, portable toilets, temporary fencing, storage containers. "
            "Use this to get category IDs for filtering products, list available service categories, "
            "or understand the product taxonomy."
        ),
    
        "fields": "id (int), name (str), slug (str), sort (int), popularity (int)",
        "method": "GET",
    },
    "api_v1_main_product_categories_get": {
        "path": "/api/v1/main-product-categories/{id}/",
        "description": "Returns a single product category by ID or slug.",
        "fields": "id (int), name (str), slug (str), sort (int), popularity (int)",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_main_product_category_groups_list": {
        "path": "/api/v1/main-product-category-groups/",
        "description": (
            "Returns top-level product category groups that bundle multiple categories. "
            "Fields: id, name, slug, icon, sort, main_product_categories (nested list). "
            "Examples: Waste Removal, Site Services, Storage. "
            "Filters: seller_location (limits to products available at that location), allows_pickup. "
            "Use this for top-level product taxonomy, marketplace navigation, or filtering available services."
        ),
    
        "fields": "id (int), name (str), slug (str), sort (int), main_product_categories (JSON str: [{id, name, slug}])",
        "method": "GET",
    },
    "api_v1_main_product_category_groups_get": {
        "path": "/api/v1/main-product-category-groups/{id}/",
        "description": "Returns a single product category group by ID.",
        "fields": "id (int), name (str), slug (str), sort (int), main_product_categories (JSON str: [{id, name, slug}])",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_main_products_list": {
        "path": "/api/v1/main-products/",
        "description": (
            "Returns the master product catalog — the canonical list of all waste/service products offered on the platform. "
            "Fields: id, name, slug, main_product_category, allows_pick_up, sort, images, tags, related_products. "
            "Examples: 10-yard dumpster, 20-yard dumpster, portable toilet, temporary fence, storage container. "
            "Use this to look up product IDs, get the full product catalog, "
            "find which products are available, or map product names to IDs."
        ),
    
        "fields": "id (int), name (str), slug (str), main_product_category_id (int), allows_pick_up (bool)",
        "method": "GET",
    },
    "api_v1_main_products_get": {
        "path": "/api/v1/main-products/{id}/",
        "description": "Returns a single main product by ID or slug with full details.",
        "fields": "id (int), name (str), slug (str), main_product_category_id (int), allows_pick_up (bool)",
        "method": "GET",
        "requires_id": True,
    },

    # ── MOBILE WIDGET ─────────────────────────────────────────────────────────

    "api_v1_mobile_widget_list": {
        "path": "/api/v1/mobile-widget/",
        "description": (
            "Returns summary data for the mobile homepage widget: "
            "active orders count, upcoming deliveries, recent activity. "
            "Not suitable for analytics — use order endpoints for raw data."
        ),
    
        "fields": "active_orders_count (int), upcoming_deliveries_count (int)",
        "method": "GET",
    },

    # ── ORDER GROUPS (BOOKINGS) ───────────────────────────────────────────────

    "api_v1_order_group_attachments_list": {
        "path": "/api/v1/order-group-attachments/",
        "description": (
            "Returns file attachments associated with order groups (bookings). "
            "Fields: id, order_group_id, file_url, filename, uploaded_by, created_on. "
            "Use this to list documents or files attached to a booking."
        ),
    
        "fields": "id (int), order_group_id (int), file_url (str), filename (str), uploaded_by (str), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_order_groups_list": {
        "path": "/api/v1/order-groups/",
        "description": (
            "Returns order groups (bookings / service agreements) accessible to the authenticated user. "
            "An OrderGroup is the top-level booking entity that contains one or more Orders (individual service deliveries). "
            "Fields: id, user_address (job site), seller, main_product, status, start_date, end_date, "
            "created_on, updated_on, total_value, order_count. "
            "Ordering: created_on, updated_on, start_date, end_date (default: -start_date). "
            "Filters: status, user_address_id, seller_id, created_on__gte, created_on__lte. "
            "Use this to count bookings by date, track booking volume trends, "
            "find bookings by job site, or calculate total booking value."
        ),
    
        "fields": "id (int), status (str), start_date (date), end_date (date), created_on (datetime), total_value (float), order_count (int), user_address_id (int), seller_id (int)",
        "method": "GET",
    },
    "api_v1_order_groups_filter_options_list": {
        "path": "/api/v1/order-groups/filter-options/",
        "description": (
            "Returns available filter options for the order groups list (bookings). "
            "Returns distinct values for status, seller, product type, date ranges. "
            "Use this to populate filter dropdowns for booking lists."
        ),
    
        "fields": "statuses (JSON str: [str]), sellers (JSON str: [{id, name}]), products (JSON str: [{id, name}])",
        "method": "GET",
    },
    "api_v1_order_groups_get": {
        "path": "/api/v1/order-groups/{id}/",
        "description": "Returns a single order group (booking) by ID with full details.",
        "fields": "id (int), status (str), start_date (date), end_date (date), total_value (float), order_count (int), user_address_id (int)",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_order_groups_removal_checkout_list": {
        "path": "/api/v1/order-groups/{order_group_id}/removal-checkout/",
        "description": (
            "Returns checkout preview for removing/cancelling a service from an order group. "
            "Use this to see pricing implications of removing a product from a booking."
        ),
        "fields": "refund_amount (float), cancellation_fee (float), net_refund (float)",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_order_groups_swap_checkout_list": {
        "path": "/api/v1/order-groups/{order_group_id}/swap-checkout/",
        "description": (
            "Returns checkout preview for swapping a service provider in an order group. "
            "Use this to see pricing implications of changing the supplier for a booking."
        ),
        "fields": "price_difference (float), new_total (float), old_total (float)",
        "method": "GET",
        "requires_id": True,
    },

    # ── ORDERS ────────────────────────────────────────────────────────────────

    "api_v1_orders_for_seller_list": {
        "path": "/api/v1/orders-for-seller/",
        "description": (
            "Supplier-facing view only. Returns orders scoped to the authenticated seller's own incoming orders. "
            "NOT suitable for platform-wide order counts, buyer analytics, or cross-seller analysis. "
            "Fields: id, status, start_date, end_date, user_address, product, customer_name, "
            "seller_location, price, created_on, submitted_on. "
            "Use this only from the supplier side to see their own delivery schedule or incoming order queue."
        ),
    
        "fields": "id (int), status (str), start_date (date), end_date (date), product (str), customer_name (str), seller_location_id (int), price (float), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_orders_for_seller_get": {
        "path": "/api/v1/orders-for-seller/{id}/",
        "description": "Returns a single seller-facing order by ID.",
        "fields": "id (int), status (str), start_date (date), end_date (date), product (str), customer_name (str), seller_location_id (int), price (float)",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_orders_list": {
        "path": "/api/v1/orders/",
        "description": (
            "Primary platform-wide order data source. Returns all orders (buyer perspective). "
            "Best tool for: how many orders were placed last month, order count by date range, "
            "orders placed in a period, scheduled vs completed orders, orders not yet completed, "
            "cohort analysis (repeat orders, second order within 30 days), order status breakdown. "
            "An Order is an individual service delivery within a booking (OrderGroup). "
            "Fields: id, status (SCHEDULED/COMPLETE/CANCELLED/PENDING/DENIED), "
            "start_date, end_date, created_on, submitted_on, updated_on, "
            "order_group_id, user_address_id, seller_location_id, product, price, customer_total, seller_total. "
            "Filters: status, order_group_id, user_address_id. Filter by created_on for date-range counts."
        ),
        "fields": "id (int), status (str: SCHEDULED/COMPLETE/CANCELLED/PENDING/DENIED), created_on (datetime), start_date (date), end_date (date), customer_total (float), seller_total (float), order_group_id (int), user_address_id (int), seller_location_id (int)",
        "method": "GET",
    },
    "api_v1_orders_internal_sales_data_list": {
        "path": "/api/v1/orders/internal/sales-data/",
        "description": (
            "Internal sales dashboard data for the current calendar month. "
            "Returns aggregated metrics for sales reps and managers: "
            "total GMV, order count, new accounts, GMV by rep, daily pacing. "
            "Access restricted to sales users and managers. "
            "Use this for current-month sales performance snapshots."
        ),
    
        "fields": "total_gmv (float), order_count (int), new_accounts (int), gmv_by_rep (JSON str: [{rep_id, rep_name, gmv}]), daily_pacing (JSON str: [{date, gmv}])",
        "method": "GET",
    },
    "api_v1_orders_get": {
        "path": "/api/v1/orders/{id}/",
        "description": "Returns a single order by ID with full details.",
        "fields": "id (int), status (str), created_on (datetime), start_date (date), end_date (date), customer_total (float), seller_total (float), order_group_id (int)",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_orders_change_supplier_list": {
        "path": "/api/v1/orders/{order_id}/change-supplier/",
        "description": (
            "Returns eligible alternative suppliers for an existing order. "
            "Fields: seller_id, seller_name, price, availability, distance_miles. "
            "Use this to see which suppliers could fulfil a given order if the current one needs to be swapped."
        ),
        "fields": "seller_id (int), seller_name (str), price (float), distance_miles (float)",
        "method": "GET",
        "requires_id": True,
    },

    # ── PAYMENT METHODS ───────────────────────────────────────────────────────

    "api_v1_payment_methods_list": {
        "path": "/api/v1/payment-methods/",
        "description": (
            "Returns payment methods on file for the authenticated user group. "
            "Fields: id, type (card/bank_account/net_terms), last4, brand, is_default, created_on. "
            "Use this to check what payment methods an account has, or count accounts with specific payment types."
        ),
    
        "fields": "id (int), type (str: card/bank_account/net_terms), last4 (str), brand (str), is_default (bool), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_payment_methods_get": {
        "path": "/api/v1/payment-methods/{id}/",
        "description": "Returns a single payment method by ID.",
        "fields": "id (int), type (str), last4 (str), brand (str), is_default (bool), created_on (datetime)",
        "method": "GET",
        "requires_id": True,
    },

    # ── PAYOUTS ───────────────────────────────────────────────────────────────

    "api_v1_payouts_list": {
        "path": "/api/v1/payouts/",
        "description": (
            "Returns payouts to sellers (supplier payments) visible to the authenticated context. "
            "A Payout represents money transferred to a seller for completed orders. "
            "Fields: id, seller, seller_location, amount, status (pending/paid/failed), "
            "order_count, created_on, paid_on. "
            "Ordering: created_on (default: -created_on). "
            "Use this for supplier payment history, payout volume analysis, "
            "outstanding payments to sellers, or reconciliation."
        ),
    
        "fields": "id (int), seller_id (int), amount (float), status (str: pending/paid/failed), order_count (int), created_on (datetime), paid_on (datetime)",
        "method": "GET",
    },
    "api_v1_payouts_metrics_list": {
        "path": "/api/v1/payouts/metrics/",
        "description": (
            "Returns aggregate payout metrics for the current scope: "
            "total_paid, total_pending, total_failed, payout_count. "
            "Use this for supplier payment summary or reconciliation totals."
        ),
    
        "fields": "total_paid (float), total_pending (float), total_failed (float), payout_count (int)",
        "method": "GET",
    },
    "api_v1_payouts_get": {
        "path": "/api/v1/payouts/{id}/",
        "description": "Returns a single payout record by ID.",
        "fields": "id (int), seller_id (int), amount (float), status (str), order_count (int), created_on (datetime)",
        "method": "GET",
        "requires_id": True,
    },

    # ── PUBLIC LOCATION PAGES ─────────────────────────────────────────────────

    "api_v1_public_location_pages_list": {
        "path": "/api/v1/public/location-pages/",
        "description": (
            "Returns public-facing SEO location pages for Downstream's US city coverage. "
            "Fields: state_slug, city_slug, state_name, city_name, is_indexed, seller_location_count, updated_at. "
            "Filters: state_slug, is_indexed. "
            "Use this to list all cities Downstream serves, count coverage by state, "
            "or find which markets have seller presence."
        ),
        "fields": "state_slug (str), city_slug (str), state_name (str), city_name (str), seller_location_count (int), is_indexed (bool)",
        "method": "GET",
    },
    "api_v1_public_location_pages_get": {
        "path": "/api/v1/public/location-pages/{state_slug}/{city_slug}/",
        "description": "Returns the public location page for a specific city by state and city slug.",
        "fields": "state_slug (str), city_slug (str), state_name (str), city_name (str), seller_location_count (int)",
        "method": "GET",
        "requires_id": True,
    },

    # ── RBAC ──────────────────────────────────────────────────────────────────

    "api_v1_rbac_role_templates_list": {
        "path": "/api/v1/rbac/role-templates/",
        "description": (
            "Returns hard-coded role templates (Admin, Member, View-Only, etc.) that can be used when creating account roles. "
            "Use this to list available permission templates for user management."
        ),
    
        "fields": "id (int), name (str), scopes (JSON str: [str])",
        "method": "GET",
    },
    "api_v1_rbac_roles_list": {
        "path": "/api/v1/rbac/roles/",
        "description": (
            "Returns custom roles defined within the current account (user group). "
            "Fields: id, name, scopes, user_count, created_on. "
            "Use this to list permission roles in an account."
        ),
    
        "fields": "id (int), name (str), user_count (int), scopes (JSON str: [str]), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_rbac_scopes_list": {
        "path": "/api/v1/rbac/scopes/",
        "description": (
            "Returns all available permission scopes that can be assigned to roles. "
            "Use this to list what granular permissions exist in the system."
        ),
    
        "fields": "id (int), name (str), description (str)",
        "method": "GET",
    },

    # ── SELLER DASHBOARD ──────────────────────────────────────────────────────

    "api_v1_seller_dashboard_metrics_list": {
        "path": "/api/v1/seller-dashboard/metrics/",
        "description": (
            "Returns aggregated metrics for a seller's dashboard view: "
            "total orders, revenue, upcoming deliveries, outstanding payouts, customer count. "
            "Scoped to the authenticated seller. "
            "Use this for supplier-side performance summaries."
        ),
    
        "fields": "total_orders (int), revenue (float), upcoming_deliveries (int), outstanding_payouts (float), customer_count (int)",
        "method": "GET",
    },

    # ── SELLER LOCATIONS ──────────────────────────────────────────────────────

    "api_v1_seller_locations_list": {
        "path": "/api/v1/seller-locations/",
        "description": (
            "Primary source for geographic supplier analysis. "
            "Best tool for: how many active sellers per state, which cities have the most seller locations, "
            "seller density by geography, market coverage by state or city. "
            "A SellerLocation represents a specific operational site of a seller — "
            "state and city fields live here, not on the Seller entity. "
            "Fields: id, seller_id, name, address, city, state, zip_code, latitude, longitude, "
            "is_active, service_radius_miles, open_hours, created_on. "
            "Filters: seller_id, city, state, is_active. "
            "Pass allow_all=true to see all locations platform-wide."
        ),
        "fields": "id (int), seller_id (int), name (str), city (str), state (str), zip_code (str), is_active (bool), latitude (float), longitude (float), service_radius_miles (float), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_seller_locations_get": {
        "path": "/api/v1/seller-locations/{id}/",
        "description": "Returns a single seller location by ID with full details including open hours.",
        "fields": "id (int), seller_id (int), name (str), city (str), state (str), zip_code (str), is_active (bool), service_radius_miles (float)",
        "method": "GET",
        "requires_id": True,
    },

    # ── SELLER PRODUCT SELLER LOCATIONS ───────────────────────────────────────

    "api_v1_seller_product_seller_locations_list": {
        "path": "/api/v1/seller-product-seller-locations/",
        "description": (
            "Returns seller-product-at-location listings (the inventory of which products each seller location offers). "
            "A SellerProductSellerLocation (SPSL) is the junction of a SellerProduct and a SellerLocation, "
            "representing a specific product offered at a specific depot with its own pricing. "
            "Fields: id, seller_location_id, seller_product_id, main_product_name, "
            "is_active, base_price, rental_rate, allows_pickup, created_on. "
            "Filters: seller_location_id, seller_product_id, is_active, main_product. "
            "Use this to see which products a specific location offers, compare pricing across suppliers, "
            "or count active product listings per market."
        ),
        "fields": "id (int), seller_location_id (int), seller_product_id (int), main_product_name (str), is_active (bool), base_price (float), rental_rate (float), allows_pickup (bool), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_seller_product_seller_locations_metrics_list": {
        "path": "/api/v1/seller-product-seller-locations/metrics/",
        "description": (
            "Returns performance metrics for seller-product-at-location listings: "
            "order_count, total_gmv, average_rating, conversion_rate. "
            "Use this to analyze which product-location combinations generate the most orders or revenue."
        ),
    
        "fields": "order_count (int), total_gmv (float), average_rating (float), conversion_rate (float)",
        "method": "GET",
    },
    "api_v1_seller_product_seller_locations_get": {
        "path": "/api/v1/seller-product-seller-locations/{id}/",
        "description": "Returns a single seller-product-at-location listing by ID.",
        "fields": "id (int), seller_location_id (int), seller_product_id (int), main_product_name (str), is_active (bool), base_price (float)",
        "method": "GET",
        "requires_id": True,
    },

    # ── SELLER PRODUCTS ───────────────────────────────────────────────────────

    "api_v1_seller_products_list": {
        "path": "/api/v1/seller-products/",
        "description": (
            "Returns seller products (a seller's specific product offerings, mapped to main products). "
            "A SellerProduct links a Seller to a MainProduct with seller-specific configuration. "
            "Fields: id, seller_id, main_product_id, main_product_name, name, is_active, created_on. "
            "Filters: seller_id, main_product_id, is_active. "
            "Use this to list what products a seller offers, find sellers that offer a specific product, "
            "or analyze product coverage per supplier."
        ),
    
        "fields": "id (int), seller_id (int), main_product_id (int), main_product_name (str), name (str), is_active (bool), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_seller_products_get": {
        "path": "/api/v1/seller-products/{id}/",
        "description": "Returns a single seller product by ID.",
        "fields": "id (int), seller_id (int), main_product_id (int), main_product_name (str), name (str), is_active (bool)",
        "method": "GET",
        "requires_id": True,
    },

    # ── SELLER INVOICE PAYABLES ───────────────────────────────────────────────

    "api_v1_sellerinvoicepayable_list": {
        "path": "/api/v1/sellerinvoicepayable/",
        "description": (
            "Returns invoices payable by the authenticated seller to Downstream (AP side). "
            "Fields: id, seller, amount, status (pending/paid), due_date, order_group, created_on. "
            "Use this for supplier accounts-payable tracking or outstanding seller liabilities."
        ),
    
        "fields": "id (int), seller_id (int), amount (float), status (str: pending/paid), due_date (date), order_group_id (int), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_sellerinvoicepayable_get": {
        "path": "/api/v1/sellerinvoicepayable/{id}/",
        "description": "Returns a single seller invoice payable by ID.",
        "fields": "id (int), seller_id (int), amount (float), status (str), due_date (date), order_group_id (int)",
        "method": "GET",
        "requires_id": True,
    },

    # ── SELLERS ───────────────────────────────────────────────────────────────

    "api_v1_sellers_list": {
        "path": "/api/v1/sellers/",
        "description": (
            "Returns company-level seller records. "
            "A Seller is the company entity; geographic fields (city, state) are on SellerLocation, not here. "
            "NOT suitable for state/city breakdowns — use api_v1_seller_locations_list for geography. "
            "Fields: id, name, slug, type, website, phone, email, is_active, open_days, created_on, location_count. "
            "Filters: id, is_active. "
            "Use this to list all suppliers by name, count total active sellers, "
            "look up a seller by name, or get seller IDs for joining with other data."
        ),
        "fields": "id (int), name (str), slug (str), is_active (bool), location_count (int), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_sellers_get": {
        "path": "/api/v1/sellers/{id}/",
        "description": "Returns a single seller by ID with full details.",
        "fields": "id (int), name (str), slug (str), is_active (bool), location_count (int), created_on (datetime)",
        "method": "GET",
        "requires_id": True,
    },

    # ── SETUP INTENTS / STRIPE ────────────────────────────────────────────────

    "api_v1_setup_intents_list": {
        "path": "/api/v1/setup-intents/",
        "description": (
            "Returns Stripe SetupIntents for the authenticated user group (used to add payment methods). "
            "Not useful for analytics."
        ),
    
        "fields": "id (str), client_secret (str), status (str)",
        "method": "GET",
    },
    "api_v1_stripe_payment_methods_list": {
        "path": "/api/v1/stripe/payment-methods/",
        "description": (
            "Returns Stripe payment method objects for the authenticated account. "
            "Fields: id, type, card (last4, brand, exp_month, exp_year), created. "
            "Use this to list saved Stripe payment methods."
        ),
    
        "fields": "id (str), type (str), card.last4 (str), card.brand (str), card.exp_month (int), card.exp_year (int), created (datetime)",
        "method": "GET",
    },

    # ── TASKS ─────────────────────────────────────────────────────────────────

    "api_v1_tasks_list": {
        "path": "/api/v1/tasks/",
        "description": (
            "Returns CRM tasks (to-dos) assigned to the authenticated user or their team. "
            "Fields: id, title, description, status (open/in_progress/done), due_date, "
            "assigned_to, created_by, related_user_group, created_on. "
            "Use this to list open tasks, track task completion rates, or audit CRM activity."
        ),
    
        "fields": "id (int), title (str), status (str: open/in_progress/done), due_date (date), assigned_to_id (int), created_by_id (int), related_user_group_id (int), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_tasks_get": {
        "path": "/api/v1/tasks/{id}/",
        "description": "Returns a single task by ID.",
        "fields": "id (int), title (str), description (str), status (str), due_date (date), assigned_to_id (int), created_on (datetime)",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_tasks_activities_list": {
        "path": "/api/v1/tasks/{id}/activities/",
        "description": "Returns the activity log (status changes, edits) for a specific task.",
        "fields": "id (int), action (str), changed_by (str), created_on (datetime)",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_tasks_attachments_list": {
        "path": "/api/v1/tasks/{id}/attachments/",
        "description": "Returns file attachments for a specific task.",
        "fields": "id (int), file_url (str), filename (str), uploaded_by (str), created_on (datetime)",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_tasks_comments_list": {
        "path": "/api/v1/tasks/{id}/comments/",
        "description": "Returns comments on a specific task.",
        "fields": "id (int), content (str), author_id (int), author_name (str), created_on (datetime)",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_tasks_watchers_list": {
        "path": "/api/v1/tasks/{id}/watchers/",
        "description": "Returns users watching a specific task for notifications.",
        "fields": "id (int), user_id (int), user_name (str), email (str)",
        "method": "GET",
        "requires_id": True,
    },

    # ── TIME SLOTS ────────────────────────────────────────────────────────────

    "api_v1_time_slots_list": {
        "path": "/api/v1/time-slots/",
        "description": (
            "Returns available delivery/pickup time slots offered by sellers. "
            "Fields: id, label (e.g. Morning 7am-12pm), start_time, end_time. "
            "Lookup table only — no order data, no counts, no analytics. "
            "Use only to get time slot IDs for order creation or display labels in UI."
        ),
    
        "fields": "id (int), label (str), start_time (time), end_time (time)",
        "method": "GET",
    },
    "api_v1_time_slots_get": {
        "path": "/api/v1/time-slots/{id}/",
        "description": "Returns a single time slot by ID.",
        "fields": "id (int), label (str), start_time (time), end_time (time)",
        "method": "GET",
        "requires_id": True,
    },

    # ── USER ADDRESS TYPES ────────────────────────────────────────────────────

    "api_v1_user_address_types_list": {
        "path": "/api/v1/user-address-types/",
        "description": (
            "Returns lookup types for user addresses (job sites). "
            "Fields: id, name (e.g. construction_site, residential, commercial). "
            "Use this to get address type IDs for filtering or categorizing job sites."
        ),
    
        "fields": "id (int), name (str)",
        "method": "GET",
    },
    "api_v1_user_address_types_get": {
        "path": "/api/v1/user-address-types/{id}/",
        "description": "Returns a single user address type by ID.",
        "fields": "id (int), name (str)",
        "method": "GET",
        "requires_id": True,
    },

    # ── USER ADDRESSES (JOB SITES) ────────────────────────────────────────────

    "api_v1_user_addresses_list": {
        "path": "/api/v1/user-addresses/",
        "description": (
            "Returns user addresses (job sites / project locations) accessible to the authenticated user. "
            "A UserAddress is a specific delivery site associated with a user group (account). "
            "Fields: id, name, address, city, state, zip_code, latitude, longitude, "
            "user_group_id, address_type, is_active, created_on. "
            "Filters: user_group_id, city, state, is_active. "
            "Use this to list job sites for an account, find sites by geography, "
            "count active projects per account, or get site IDs for order filtering."
        ),
    
        "fields": "id (int), name (str), address (str), city (str), state (str), zip_code (str), latitude (float), longitude (float), user_group_id (int), is_active (bool), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_user_addresses_filter_options_list": {
        "path": "/api/v1/user-addresses/filter_options/",
        "description": (
            "Returns available filter options for the user addresses (job sites) list. "
            "Returns distinct city/state values for building filter UI."
        ),
    
        "fields": "cities (JSON str: [str]), states (JSON str: [str])",
        "method": "GET",
    },
    "api_v1_user_addresses_get": {
        "path": "/api/v1/user-addresses/{id}/",
        "description": "Returns a single user address (job site) by ID.",
        "fields": "id (int), name (str), address (str), city (str), state (str), zip_code (str), user_group_id (int), is_active (bool)",
        "method": "GET",
        "requires_id": True,
    },
    "api_v1_user_addresses_recommendations_list": {
        "path": "/api/v1/user-addresses/{id}/recommendations/",
        "description": (
            "Returns active product recommendations staged for a specific job site (UserAddress). "
            "Recommendations are generated asynchronously based on project type and history. "
            "Fields: id, main_product_id, main_product_name, reason, confidence_score. "
            "Use this to see what products are recommended for a project."
        ),
        "fields": "id (int), main_product_id (int), main_product_name (str), reason (str), confidence_score (float)",
        "method": "GET",
        "requires_id": True,
    },

    # ── USER GROUP ADMIN APPROVALS ────────────────────────────────────────────

    "api_v1_user_group_admin_approval_user_invite_list": {
        "path": "/api/v1/user-group-admin-approval-user-invite/",
        "description": (
            "Returns pending user invite approval requests for accounts that require admin approval to add new users. "
            "Fields: id, user_group, invited_email, invited_by, status, created_on. "
            "Use this to list pending invitations awaiting admin approval."
        ),
    
        "fields": "id (int), user_group_id (int), invited_email (str), invited_by (str), status (str), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_user_group_admin_approval_user_invite_get": {
        "path": "/api/v1/user-group-admin-approval-user-invite/{id}/",
        "description": "Returns a single user invite approval request by ID.",
        "fields": "id (int), user_group_id (int), invited_email (str), invited_by (str), status (str)",
        "method": "GET",
        "requires_id": True,
    },

    # ── USER GROUP CREDIT APPLICATIONS ────────────────────────────────────────

    "api_v1_user_group_credit_applications_list": {
        "path": "/api/v1/user-group-credit-applications/",
        "description": (
            "Returns net-terms (trade credit) applications associated with the authenticated account. "
            "Fields: id, user_group, status (pending/approved/denied), "
            "first_name, last_name, email, requested_credit_limit, created_on. "
            "Use this to list credit applications, track approval status, or count pending reviews."
        ),
    
        "fields": "id (int), user_group_id (int), status (str: pending/approved/denied), first_name (str), last_name (str), email (str), requested_credit_limit (float), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_user_group_credit_applications_get": {
        "path": "/api/v1/user-group-credit-applications/{id}/",
        "description": "Returns a single credit application by ID.",
        "fields": "id (int), user_group_id (int), status (str), first_name (str), last_name (str), email (str), requested_credit_limit (float)",
        "method": "GET",
        "requires_id": True,
    },

    # ── USER GROUPS (ACCOUNTS) ────────────────────────────────────────────────

    "api_v1_user_groups_list": {
        "path": "/api/v1/user-groups/",
        "description": (
            "Returns accounts (UserGroups / companies) accessible to the authenticated context. "
            "A UserGroup is the company-level account entity that groups users and addresses together. "
            "Fields: id, name, superadmin_user, stripe_customer_id, net_terms, pay_later, autopay, "
            "industry, company_size, is_active, created_on. "
            "Expandable: seller, account_owner, users, credit_applications, credit_limit_utilized, "
            "insurance_summary, latest_policies. "
            "Ordering: last calendar-month spend descending (default), or biggest_gap (target - actual spend). "
            "Use this to list all customer accounts, filter by industry or company size, "
            "count accounts with net terms, find accounts by name, "
            "or rank accounts by spend for prioritization."
        ),
        "fields": "id (int), name (str), industry (str), company_size (str), net_terms (bool), pay_later (bool), is_active (bool), created_on (datetime)",
        "method": "GET",
    },
    "api_v1_user_groups_get": {
        "path": "/api/v1/user-groups/{user_group_id}/",
        "description": (
            "Returns a single account (UserGroup) by ID with full details. "
            "Use expand[] params to include: seller, account_owner, users, credit_applications, "
            "credit_limit_utilized, insurance_summary, latest_policies."
        ),
        "fields": "id (int), name (str), industry (str), company_size (str), net_terms (bool), is_active (bool), created_on (datetime)",
        "method": "GET",
        "requires_id": True,
    },

    # ── USER IDENTITY ─────────────────────────────────────────────────────────

    "api_v1_user_identity_list": {
        "path": "/api/v1/user/identity/",
        "description": (
            "Returns identity verification state for the authenticated user and their account. "
            "Fields: is_verified, verification_status, verified_at. "
            "Use this to check if the current user has completed identity verification."
        ),
    
        "fields": "is_verified (bool), verification_status (str), verified_at (datetime)",
        "method": "GET",
    },

    # ── USERS ─────────────────────────────────────────────────────────────────

    "api_v1_users_list": {
        "path": "/api/v1/users/",
        "description": (
            "Returns users scoped to the authenticated request context. "
            "Fields: id, email, first_name, last_name, type (ADMIN/MEMBER/VIEW_ONLY), "
            "is_onboarded, is_active, is_archived, timezone, role, user_group (id + name). "
            "Expandable: role, user_group.seller, user_group.account_owner, user_group.users, etc. "
            "Filters: user_group_id, type, is_active, is_archived. "
            "Use this to count users per account, list users by type, "
            "find which accounts have onboarded users, or get user IDs for cohort analysis."
        ),
    
        "fields": "id (int), email (str), first_name (str), last_name (str), type (str: ADMIN/MEMBER/VIEW_ONLY), is_onboarded (bool), is_active (bool), is_archived (bool), user_group.id (int), user_group.name (str)",
        "method": "GET",
    },
    "api_v1_users_me_list": {
        "path": "/api/v1/users/me/",
        "description": (
            "Returns the currently authenticated user's full profile. "
            "Use this to identify who is making requests (role, account, type)."
        ),
    
        "fields": "id (int), email (str), first_name (str), last_name (str), type (str), user_group.id (int), user_group.name (str)",
        "method": "GET",
    },
    "api_v1_users_get": {
        "path": "/api/v1/users/{user_id}/",
        "description": "Returns a single user by ID.",
        "fields": "id (int), email (str), first_name (str), last_name (str), type (str), is_active (bool), user_group.id (int), user_group.name (str)",
        "method": "GET",
        "requires_id": True,
    },

    # ── WASTE TYPES ───────────────────────────────────────────────────────────

    "api_v1_waste_types_list": {
        "path": "/api/v1/waste-types/",
        "description": (
            "Static reference lookup — returns IDs and names for accepted material categories. "
            "Fields: id, name, slug, description, is_hazardous. "
            "Contains no transactional data, no order counts, no usage frequency, no rankings. "
            "Use only to get an ID or display label."
        ),
    
        "fields": "id (int), name (str), slug (str), description (str), is_hazardous (bool)",
        "method": "GET",
    },
    "api_v1_waste_types_get": {
        "path": "/api/v1/waste-types/{id}/",
        "description": "Returns a single waste type by ID or slug.",
        "fields": "id (int), name (str), slug (str), description (str), is_hazardous (bool)",
        "method": "GET",
        "requires_id": True,
    },

    # ── CHECKOUT ──────────────────────────────────────────────────────────────

    "checkout_v1_list": {
        "path": "/checkout/v1/",
        "description": (
            "Returns a paginated list of Cart objects for the authenticated user. "
            "A Cart is a pre-order container — items added before checkout. "
            "Use this to count carts, track cart creation trends, or list active shopping sessions."
        ),
    
        "fields": "id (int), user_address_id (int), item_count (int), total_price (float), created_on (datetime)",
        "method": "GET",
    },
    "checkout_v1_cart_list": {
        "path": "/checkout/v1/cart/",
        "description": (
            "Returns the active cart for the authenticated user, structured as CartGroups of CartItems. "
            "Fields: cart_groups (grouped by seller_location), cart_items (product, quantity, price, delivery_date). "
            "Use this to inspect the contents of the current user's active cart."
        ),
    
        "fields": "cart_groups (JSON str: [{seller_location_id, items: [{product, quantity, price}]}])",
        "method": "GET",
    },
    "checkout_v1_cart_count_list": {
        "path": "/checkout/v1/cart/count/",
        "description": (
            "Returns the total number of items in the authenticated user's active cart. "
            "Fields: count. "
            "Use this for the cart badge count in the navbar."
        ),
    
        "fields": "count (int)",
        "method": "GET",
    },
    "checkout_v1_carts_list": {
        "path": "/checkout/v1/carts/",
        "description": (
            "Returns a list of carts with lightweight summary data. "
            "Fields: id, user_address_id, item_count, total_price, created_on, updated_on. "
            "Use this to list carts by job site, count carts per account, or track cart activity."
        ),
    
        "fields": "id (int), user_address_id (int), item_count (int), total_price (float), created_on (datetime), updated_on (datetime)",
        "method": "GET",
    },
    "checkout_v1_carts_get": {
        "path": "/checkout/v1/carts/{cart_id}/",
        "description": "Returns a single cart by ID with full CartGroup and CartItem details.",
        "fields": "id (int), user_address_id (int), item_count (int), total_price (float), cart_groups (JSON str)",
        "method": "GET",
        "requires_id": True,
    },
    "checkout_v1_quote_accept_list": {
        "path": "/checkout/v1/quote/accept/",
        "description": (
            "Returns the result of accepting a quote (converting a quote to a confirmed order). "
            "Use this to trigger quote acceptance in the checkout flow."
        ),
    
        "fields": "order_group_id (int), status (str), total (float)",
        "method": "GET",
    },
    "checkout_v1_quote_get": {
        "path": "/checkout/v1/quote/{cart_id}/",
        "description": (
            "Price preview tool. Shows itemized cost before a buyer completes a purchase: "
            "line items, taxes, delivery fees, subtotal, total. Single-session use only."
        ),
        "fields": "subtotal (float), delivery_fee (float), taxes (float), total (float), line_items (JSON str: [{product, quantity, price}])",
        "method": "GET",
        "requires_id": True,
    },
    "checkout_v1_get": {
        "path": "/checkout/v1/{id}/",
        "description": "Returns a single cart by ID.",
        "fields": "id (int), user_address_id (int), item_count (int), total_price (float)",
        "method": "GET",
        "requires_id": True,
    },

    # ── EXPLORE / SEARCH ──────────────────────────────────────────────────────

    "explore_v1_main_product_match_list": {
        "path": "/explore/v1/main-product/match/",
        "description": (
            "Add-on configurator for the shop flow. "
            "Given a base item ID and a set of add-on selections, returns the matching variant. "
            "Transactional UI helper — no historical data, no aggregation, no reporting."
        ),
    
        "fields": "main_product_id (int), variant_id (int), name (str), price (float)",
        "method": "POST",
    },
    "explore_v1_search_list": {
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
    
        "fields": "main_products (JSON str: [{id, name, category}]), main_product_categories (JSON str: [{id, name, slug}]), main_product_category_groups (JSON str: [{id, name}])",
        "method": "GET",
    },

    # ── FINANCIAL ACCOUNTS ────────────────────────────────────────────────────

    "financial_accounts_v1_financial_connection_account_list": {
        "path": "/financial-accounts/v1/financial-connection-account/",
        "description": (
            "Returns Plaid-linked financial connection accounts (bank accounts) for the authenticated user group. "
            "Fields: id, institution_name, account_name, account_type, mask (last 4 digits), status. "
            "Use this to list connected bank accounts for an account."
        ),
    
        "fields": "id (int), institution_name (str), account_name (str), account_type (str), mask (str), status (str)",
        "method": "GET",
    },
    "financial_accounts_v1_financial_connection_account_get": {
        "path": "/financial-accounts/v1/financial-connection-account/{id}/",
        "description": "Returns a single financial connection account by ID.",
        "fields": "id (int), institution_name (str), account_name (str), account_type (str), mask (str), status (str)",
        "method": "GET",
        "requires_id": True,
    },
    "financial_accounts_v1_financial_statement_list": {
        "path": "/financial-accounts/v1/financial-statement/",
        "description": (
            "Returns financial statements (bank transaction data) for connected accounts via Plaid. "
            "Fields: id, account_id, date, description, amount, transaction_type. "
            "Use this to retrieve bank transaction history for an account."
        ),
    
        "fields": "id (int), account_id (int), date (date), description (str), amount (float), transaction_type (str)",
        "method": "GET",
    },
    "financial_accounts_v1_financial_statement_get": {
        "path": "/financial-accounts/v1/financial-statement/{id}/",
        "description": "Returns a single financial statement by ID.",
        "fields": "id (int), account_id (int), date (date), description (str), amount (float), transaction_type (str)",
        "method": "GET",
        "requires_id": True,
    },

    # ── MATCHING ENGINE ───────────────────────────────────────────────────────

    "matching_engine_v1_product_match_list": {
        "path": "/matching-engine/v1/product-match/",
        "description": (
            "Returns supplier matches for a given product request. "
            "Input: product_id, user_address (delivery location), waste_type (optional). "
            "Returns ranked list of SellerProductSellerLocations that can fulfill the request. "
            "Fields: seller_location_id, seller_name, price, delivery_fee, availability, distance_miles. "
            "Use this to find which suppliers can fulfill a product request at a given address."
        ),
    
        "fields": "seller_location_id (int), seller_name (str), price (float), delivery_fee (float), distance_miles (float)",
        "method": "POST",
    },
    "matching_engine_v1_seller_product_seller_locations_by_lat_long_list": {
        "path": "/matching-engine/v1/seller-product-seller-locations-by-lat-long/",
        "description": (
            "Returns supplier matches for a product request using lat/long coordinates instead of address. "
            "Input: product ID, latitude, longitude, waste_type (optional). "
            "Returns ranked SellerProductSellerLocations sorted by distance and price. "
            "Use this when you have coordinates but not a structured address."
        ),
    
        "fields": "seller_location_id (int), seller_name (str), price (float), delivery_fee (float), distance_miles (float)",
        "method": "POST",
    },

    # ── NOTIFICATIONS ─────────────────────────────────────────────────────────

    "notifications_v1_push_notifications_list": {
        "path": "/notifications/v1/push-notifications/",
        "description": (
            "Returns push notification records sent to the authenticated user. "
            "Fields: id, title, body, type, read_at, created_on. "
            "Use this to list recent notifications for a user."
        ),
    
        "fields": "id (int), title (str), body (str), type (str), read_at (datetime), created_on (datetime)",
        "method": "GET",
    },
    "notifications_v1_push_notifications_get": {
        "path": "/notifications/v1/push-notifications/{id}/",
        "description": "Returns a single push notification by ID.",
        "fields": "id (int), title (str), body (str), type (str), read_at (datetime), created_on (datetime)",
        "method": "GET",
        "requires_id": True,
    },

    # ── PRICING ENGINE ────────────────────────────────────────────────────────

    "pricing_engine_v1_seller_product_seller_location_pricing_by_lat_long_list": {
        "path": "/pricing-engine/v1/seller-product-seller-location-pricing-by-lat-long/",
        "description": (
            "Returns pricing for a specific seller-product-at-location listing, calculated for delivery to given coordinates. "
            "Input: seller_product_seller_location ID, latitude, longitude. "
            "Returns: base_price, delivery_fee, total_price, rental_period, fuel_surcharge. "
            "Use this to get the exact price a customer at given coordinates would pay for a listing."
        ),
    
        "fields": "base_price (float), delivery_fee (float), total_price (float), rental_period (str), fuel_surcharge (float)",
        "method": "POST",
    },
    "pricing_engine_v1_seller_product_seller_location_pricing_list": {
        "path": "/pricing-engine/v1/seller-product-seller-location-pricing/",
        "description": (
            "Returns pricing for a specific seller-product-at-location listing, calculated for delivery to a given address. "
            "Input: seller_product_seller_location ID, user_address (string). "
            "Returns: base_price, delivery_fee, total_price, rental_period, fuel_surcharge. "
            "Use this to get the price a customer at a specific address would pay."
        ),
        "fields": "base_price (float), delivery_fee (float), total_price (float), rental_period (str), fuel_surcharge (float)",
        "method": "POST",
    },
    "pricing_engine_v1_supplier_insights_list": {
        "path": "/pricing-engine/v1/supplier-insights/",
        "description": (
            "Local market competitiveness check for a single buyer address. "
            "How many vendors serve a specific delivery location and what the local benchmark cost is. "
            "Fields: supplier_count_nearby, average_price, price_range (min/max), competitive_index. "
            "Requires a specific location — not an analytics or reporting endpoint."
        ),
    
        "fields": "supplier_count_nearby (int), average_price (float), price_range.min (float), price_range.max (float), competitive_index (float)",
        "method": "POST",
    },
}


def get_tool_catalog_text() -> str:
    lines = []
    for name, info in MCP_TOOL_CATALOG.items():
        lines.append("  " + name + "\n    -> " + info["description"])
    return "\n".join(lines)
