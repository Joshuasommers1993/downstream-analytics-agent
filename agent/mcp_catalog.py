# MCP tool catalog — 141 tools from downstream-mcp
# Descriptions written from TG-API-proxy source (views, serializers, services) + DB schema.
# Richer descriptions improve Chroma RAG accuracy for analytics tool selection.

MCP_TOOL_CATALOG = {

    # ── ENRICHMENT ────────────────────────────────────────────────────────────

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
        "fields": "month (str), gmv (float)",
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
        "fields": "id (str), name (str), first_order_date (str), last_order_date (str)",
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
        "fields": "rep_id (str), rep_name (str), commission_eligible (float), commission (float), in_cart (float), scheduled (float)",
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
        "fields": "user_group_id (str), user_group_name (str), month (str), spend (float)",
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
        "fields": "state (str), gmv (float), order_count (int)",
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
        "fields": "month (str), gmv (float), supplier_cost (float), net_revenue (float), take_rate_percent (float), aov (float), order_count (int)",
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
        "fields": "category (str), order_count (int), percent (float)",
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
        "fields": "rep_id (str), rep_name (str), month (str), gmv_target (float), gmv_actual (float), attainment_percent (float), new_accounts_target (int), new_accounts_actual (int), orders_target (int), orders_actual (int)",
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
    
        "fields": "id (int), rep_id (str), month (str), gmv_target (float), new_accounts_target (int), orders_target (int)",
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
        "fields": "stage (str), count (int), gmv (float)",
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
        "fields": "seller_id (str), seller_name (str), gmv (float)",
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
        "fields": "rep_id (str), rep_name (str), month (str), customer_total (float), seller_total (float), net_revenue (float), take_rate_percent (float)",
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
    "api_v1_admin_sales_target_vs_actuals_list": {
        "path": "/api/v1/admin/sales/target-vs-actuals/",
        "description": (
            "Admin-only. Returns aggregate GMV pacing metrics and cumulative daily comparison against the prior month. "
            "Includes current month actuals, target, and prior-month comparison on a daily basis. "
            "Use this for daily sales pacing dashboards, are-we-on-track analysis, "
            "or current month vs prior month performance."
        ),
    
        "fields": "period.month (str), period.as_of (str), period.current_month_start (str), period.current_month_end (str), period.previous_month_start (str), period.previous_month_end (str), period.days_elapsed (int), gmv.target (float), gmv.actual_mtd (float), gmv.previous_month_mtd_aligned (float), gmv.delta_vs_previous_month_mtd (float), gmv.delta_vs_previous_month_mtd_percent (float), gmv.expected_to_date (float), gmv.attainment_percent (float), gmv.projected_month_end (float), gmv.on_track (bool), gmv.booked_month_total (float), gmv.future_booked_this_month (float), daily_progress.actual_complete_cumulative (JSON), daily_progress.booked_total_cumulative (JSON), daily_progress.expected_pace_cumulative (JSON), daily_progress.previous_month_cumulative_aligned (JSON), definitions.actual_mtd (str), definitions.booked_month_total (str), definitions.future_booked_this_month (str), definitions.actual_complete_cumulative_basis (str), definitions.booked_total_cumulative_basis (str), definitions.expected_pace_cumulative_basis (str)",
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
    
        "fields": "period.as_of (str), period.current_month_start (str), period.previous_month_start (str), gmv.goal (float), gmv.current (float), gmv.previous_month (float), gmv.gap (float), gmv.attainment_percent (float), users.goal (int), users.current (int), users.gap (int), users.attainment_percent (float), job_site_starts.goal (int), job_site_starts.current (int), job_site_starts.gap (int), job_site_starts.attainment_percent (float), project_start_funnel.target_monthly_project_starts (int), project_start_funnel.expected_to_date (int), project_start_funnel.month_start (str), project_start_funnel.month_end (str), project_start_funnel.as_of (str), project_start_funnel.addresses_starting_this_month (int), project_start_funnel.due_by_now (int), project_start_funnel.later_this_month (int), project_start_funnel.due_by_now_with_populated_cart (int), project_start_funnel.due_by_now_with_checked_out_cart (int), project_start_funnel.due_by_now_added_to_cart_pct (float), project_start_funnel.due_by_now_cart_to_checkout_pct (float), project_start_funnel.due_by_now_added_to_checkout_pct (float)",
        "method": "GET",
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

    # ── ADVERTISEMENTS ────────────────────────────────────────────────────────

    "api_v1_advertisements_list": {
        "path": "/api/v1/advertisements/",
        "description": (
            "Returns all advertisements (promotional banners/placements) configured in the platform. "
            "Fields: id, title, image_url, target_url, seller, placement, is_active, start_date, end_date. "
            "Filters: seller_id, placement, is_active. "
            "Use this to list active promotions, see which sellers are advertising, or audit ad inventory."
        ),
    
        "fields": "id (str), text (str), image (str), background_color (str), text_color (str), object_type (str), object_id (str), sort (int), is_active (bool), start_date (str), end_date (str)",
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

    # ── DAY OF WEEKS ──────────────────────────────────────────────────────────

    "api_v1_day_of_weeks_list": {
        "path": "/api/v1/day-of-weeks/",
        "description": (
            "Returns the lookup table of day-of-week records used by seller open hours. "
            "Fields: id, name (e.g. MONDAY, TUESDAY). "
            "Use this to get the UUID for a day name when setting or querying open hours."
        ),
    
        "fields": "id (str), created_on (str), updated_on (str), is_deleted (bool), name (str), number (int), created_by (str), updated_by (str)",
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

    # ── IDENTITY VERIFICATION ─────────────────────────────────────────────────

    "api_v1_identity_verification_list": {
        "path": "/api/v1/identity-verification/",
        "description": (
            "Returns identity verification status for the authenticated user's account. "
            "Fields: status, verified_at, provider. "
            "Use this to check if an account has completed KYC/identity verification."
        ),
    
        "fields": "id (str), object (str), client_reference_id (str), client_secret (str), created (int), last_error (str), last_verification_report (str), livemode (bool), redaction (str), related_customer (str), related_customer_account (str), status (str), type (str), url (str), ephemeral_key (str), publishable_key (str), metadata.user_id (str)",
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
    
        "fields": "id (str), main_product_categories (JSON), name (str), description (str), image (str), slug (str), sort (int)",
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
    
        "fields": "id (str), object (str), account (str), account_type (str), type (str), status (str), effective_at (int), expires_at (int), insurance_provider (str), policy_number (str), is_valid (bool), invalid_reasons (JSON), deactivated_at (str), deactivation_reason (str), created (int), coverage.each_occurrence_limit (float), coverage.general_aggregate_limit (float), coverage.additional_insured (bool), coverage.waiver_of_subrogation (bool), document.file_url (str), document.ocr_status (str), coverage.equipment_coverage_limit (float)",
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
        "fields": "id (str), object (str), created (int), updated (int), user_address (str), display_total (float), has_outstanding_payment (bool), items (JSON), groups (JSON), pre_payment_credit (str), post_payment_credit (str), order (str), main_product (str), product_add_ons (JSON), refunds (JSON), payment_info (str), created_on (str), updated_on (str), is_deleted (bool), invoice_id (str), amount_due (float), amount_paid (float), amount_remaining (float), due_date (str), hosted_invoice_url (str), invoice_pdf (str), pdf (str), number (str), paid (bool), status (str), total (float), check_sent_at (str), created_by (str), updated_by (str), group_invoice (str)",
        "method": "GET",
    },
    "api_v1_invoices_metrics_list": {
        "path": "/api/v1/invoices/metrics/",
        "description": (
            "Returns aggregate invoice totals for the current scope: "
            "past_due_total (overdue amount), outstanding_total (open unpaid), paid_total (collected). "
            "Use this for AR summary, total outstanding balance, or collections health at a glance."
        ),
        "fields": "past_due (float), outstanding (float), paid (float)",
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

    # ── LEADS ─────────────────────────────────────────────────────────────────

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
    
        "fields": "id (str), industry (JSON), created_on (str), updated_on (str), is_deleted (bool), name (str), description (str), image (str), icon (str), popularity (float), slug (str), sort (int), main_product_category_code (str), created_by (str), updated_by (str), group (str)",
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
    
        "fields": "id (str), main_product_categories (JSON), created_on (str), updated_on (str), is_deleted (bool), name (str), sort (int), icon (str), slug (str), created_by (str), updated_by (str)",
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
    
        "fields": "id (str), main_product_category (str), main_product_infos (JSON), images (JSON), add_ons (JSON), tags (JSON), listings_count (int), likes_count (int), main_product_waste_types (JSON), products (JSON), related_products (JSON), created_on (str), updated_on (str), is_deleted (bool), name (str), ar_url (str), description (str), image_del (str), slug (str), sort (int), popularity (float), default_take_rate (float), dynamic_max_take_rate (float), minimum_take_rate (float), dynamic_min_take_rate (float), minimum_take_rate_hour (str), minimum_take_rate_day (str), minimum_take_rate_week (str), minimum_take_rate_two_weeks (str), minimum_take_rate_month (str), included_tonnage_quantity (float), max_tonnage_quantity (float), main_product_code (str), has_rental (bool), has_rental_one_step (bool), has_rental_multi_step (bool), has_service (bool), has_service_times_per_week (bool), has_material (bool), allows_pick_up (bool), has_bundled_qty (bool), has_winterization (bool), can_bundle_freight (bool), texas_surcharge_applies (bool), has_rpp (bool), estimated_replacement_value (str), is_related (bool), created_by (str), updated_by (str)",
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
    
        "fields": "cart_count (int), active_bookings (int), past_due_invoices (int), last_order (str)",
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
    
        "fields": "id (str), order_group (str), file_name (str), file_type (str)",
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
    
        "fields": "id (str), user (str), on_site_contact (str), user_address (str), seller_product_seller_location (str), main_product (str), waste_type (str), time_slot (str), service_recurring_frequency (str), preferred_service_days (JSON), service (float), rental (float), material (float), orders (JSON), active (bool), created_on (str), updated_on (str), is_deleted (bool), access_details (str), placement_details (str), delivered_to_street (bool), start_date (str), end_date (str), estimated_end_date (str), take_rate (float), tonnage_quantity (float), times_per_week (float), shift_count (float), is_delivery (bool), delivery_fee (float), removal_fee (float), created_by (str), updated_by (str), conversation (str), status (str), attachments (JSON), code (str), agreement (str), agreement_signed_by (str), agreement_signed_on (str), asset (str), service.id (str), service.order_group (str), service.created_on (str), service.updated_on (str), service.is_deleted (str), service.price_per_mile (float), service.flat_rate_price (float), service.rate (float), service.miles (float), service.created_by (float), service.updated_by (float), rental.id (str), rental.order_group (str), rental.created_on (str), rental.updated_on (str), rental.is_deleted (str), rental.included_days (float), rental.price_per_day_included (float), rental.price_per_day_additional (float), rental.created_by (float), rental.updated_by (float), material.id (str), material.order_group (str), material.created_on (str), material.updated_on (str), material.is_deleted (str), material.price_per_ton (float), material.tonnage_included (float), material.created_by (float), material.updated_by (float)",
        "method": "GET",
    },
    "api_v1_order_groups_filter_options_list": {
        "path": "/api/v1/order-groups/filter-options/",
        "description": (
            "Returns available filter options for the order groups list (bookings). "
            "Returns distinct values for status, seller, product type, date ranges. "
            "Use this to populate filter dropdowns for booking lists."
        ),
    
        "fields": "value (str), label (str), count (int)",
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
    
        "fields": "id (str), created_on (str), updated_on (str), code (str), start_date (str), end_date (str), submitted_on (str), accepted_on (str), completed_on (str), status (str), order_type (str), schedule_window (str), sent_auto_renewal_message (bool), disposal_location (str), order_group (str), main_product (str), seller (str), account_owner (str), submitted_by (str), created_by (str), price (float)",
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
        "fields": "id (str), created_on (str), updated_on (str), code (str), start_date (str), end_date (str), submitted_on (str), accepted_on (str), completed_on (str), status (str), order_type (str), schedule_window (str), sent_auto_renewal_message (bool), disposal_location (str), order_group (str), main_product (str), seller (str), account_owner (str), submitted_by (str), created_by (str), price (float)",
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
    
        "fields": "month (str), user (str), company.month_to_date.in_cart (float), company.month_to_date.scheduled (float), company.month_to_date.invoiced (float), company.month_to_date.commission_eligible (float)",
        "method": "GET",
    },
    "api_v1_orders_get": {
        "path": "/api/v1/orders/{id}/",
        "description": "Returns a single order by ID with full details.",
        "fields": "id (int), status (str), created_on (datetime), start_date (date), end_date (date), customer_total (float), seller_total (float), order_group_id (int)",
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
    
        "fields": "id (str), user (str), user_group (str), active (bool), reason (str), type (str), card.number (str), card.name (str), card.brand (str), card.expiration_month (int), card.expiration_year (int), data.brand (str), data.last4 (str), data.checks.cvc_check (str), data.checks.address_line1_check (str), data.checks.address_postal_code_check (str), data.wallet (str), data.country (str), data.funding (str), data.exp_year (int), data.networks.available (JSON), data.networks.preferred (str), data.exp_month (int), data.fingerprint (str), data.display_brand (str), data.generated_from (str), data.regulated_status (str), data.three_d_secure_usage.supported (bool)",
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
    
        "fields": "total.count (int), total.amount (float), pending.count (int), pending.amount (float), this_week.count (int), this_week.amount (float)",
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
        "fields": "location.stateSlug (str), location.stateName (str), location.citySlug (str), location.cityName (str), location.county (str), location.lat (float), location.lng (float), coverage.isServiced (bool), coverage.coverageScore (float), coverage.supplierCount (int), coverage.listingCount (int), coverage.topCategories (JSON), seo.title (str), seo.description (str), seo.canonicalPath (str), seo.indexable (bool), seo.faqItems (JSON), content.heroCopy (str), content.benefits (JSON), content.serviceHighlights (JSON), content.trustSignals (JSON), internalLinks.nearbyCities (JSON), internalLinks.statePagePath (str), meta.updatedAt (str)",
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
        "fields": "id (str), object (str), created (int), updated (int), seller (str), open_days (JSON), open_hours (JSON), users (JSON), created_by (str), updated_by (str), is_compliant (bool), created_on (str), updated_on (str), is_deleted (bool), name (str), public_subdomain_enabled (bool), public_subdomain (str), street (str), city (str), state (str), postal_code (str), country (str), latitude (float), longitude (float), geo_point (str), open_time (str), close_time (str), lead_time_hrs (str), announcement (str), live_menu_is_active (bool), location_logo_image (str), sends_invoices (bool), do_not_rent (bool), payee_name (str), order_email (str), order_phone (str), gl_coi (str), gl_coi_expiration_date (str), gl_limit (str), auto_coi (str), auto_coi_expiration_date (str), auto_limit (str), workers_comp_coi (str), workers_comp_coi_expiration_date (str), workers_comp_limit (str), w9 (str), ein (str), company_type (str), payout_delay (int), timezone (str)",
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
        "fields": "id (str), seller_product (str), seller_location (str), quote (str), service (float), material (float), rental (float), rental_multi_step (str), service_times_per_week (str), created_by (str), updated_by (str), is_complete (bool), created_on (str), updated_on (str), is_deleted (bool), active (bool), needs_approval (bool), total_inventory (str), min_price (str), max_price (str), service_radius (float), service_area_polygon (str), delivery_fee (float), removal_fee (float), fuel_environmental_markup (str), allows_pick_up (bool), winterization_fee (str), rental_one_step.id (str), rental_one_step.created_on (str), rental_one_step.updated_on (str), rental_one_step.is_deleted (str), rental_one_step.rate (float), rental_one_step.created_by (str), rental_one_step.updated_by (str), rental_one_step.seller_product_seller_location (str), rental_one_step (float), service.id (str), service.created_on (str), service.updated_on (str), service.is_deleted (str), service.price_per_mile (float), service.flat_rate_price (float), service.created_by (str), service.updated_by (str), service.seller_product_seller_location (str), material.id (str), material.waste_types (JSON), material.created_on (str), material.updated_on (str), material.is_deleted (str), material.created_by (str), material.updated_by (str), material.seller_product_seller_location (str), rental.id (str), rental.created_on (str), rental.updated_on (str), rental.is_deleted (str), rental.included_days (float), rental.price_per_day_included (float), rental.price_per_day_additional (float), rental.created_by (str), rental.updated_by (str), rental.seller_product_seller_location (str)",
        "method": "GET",
    },
    "api_v1_seller_product_seller_locations_metrics_list": {
        "path": "/api/v1/seller-product-seller-locations/metrics/",
        "description": (
            "Returns performance metrics for seller-product-at-location listings: "
            "order_count, total_gmv, average_rating, conversion_rate. "
            "Use this to analyze which product-location combinations generate the most orders or revenue."
        ),
    
        "fields": "active (int), needs_attention (int), inactive (int)",
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
    
        "fields": "id (str), seller (str), product (str), created_by (str), updated_by (str), created_on (str), updated_on (str), is_deleted (bool), active (bool)",
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
    
        "fields": "id (str), seller_location (str), location_mail_item (str), user_address (str), resolved_by (str), parent_invoice (str), child_invoices (JSON), line_items (JSON), created_on (str), updated_on (str), is_deleted (bool), invoice_file (str), supplier_invoice_id (str), invoice_date (str), due_date (str), amount (float), status (str), account_number (str), ocr_status (str), service_address_raw (str), vendor_address_raw (str), fuel_fee (str), env_fee (str), tax_amount (str), matched_user_address_confidence (int), variance_total (float), resolution_notes (str), resolved_at (str), ingestion_source (str), created_by (str), updated_by (str), parsed_data.product_description (str)",
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
        "fields": "id (str), created_by (str), updated_by (str), open_days (JSON), created_on (str), updated_on (str), is_deleted (bool), name (str), public_subdomain_enabled (bool), public_subdomain (str), phone (str), website (str), order_email (str), order_phone (str), type (str), location_type (str), status (str), lead_time (str), type_display (str), marketplace_display_name (str), open_time (str), close_time (str), lead_time_hrs (str), announcement (str), live_menu_is_active (bool), location_logo_url (str), logo (str), downstream_insurance_requirements_met (bool), badge (str), salesforce_seller_id (str), about_us (str), do_not_rent (bool)",
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
    
        "fields": "id (str), object (str), allow_redisplay (str), created (int), customer (str), customer_account (str), livemode (bool), type (str), billing_details.address.city (str), billing_details.address.country (str), billing_details.address.line1 (str), billing_details.address.line2 (str), billing_details.address.postal_code (str), billing_details.address.state (str), billing_details.email (str), billing_details.name (str), billing_details.phone (str), billing_details.tax_id (str), card.brand (str), card.checks.address_line1_check (str), card.checks.address_postal_code_check (str), card.checks.cvc_check (str), card.country (str), card.display_brand (str), card.exp_month (int), card.exp_year (int), card.fingerprint (str), card.funding (str), card.generated_from (str), card.last4 (str), card.networks.available (JSON), card.networks.preferred (str), card.regulated_status (str), card.three_d_secure_usage.supported (bool), card.wallet (str), metadata.payment_method_id (str), metadata.token (str)",
        "method": "GET",
    },

    # ── TASKS ─────────────────────────────────────────────────────────────────

    # ── TIME SLOTS ────────────────────────────────────────────────────────────

    "api_v1_time_slots_list": {
        "path": "/api/v1/time-slots/",
        "description": (
            "Returns available delivery/pickup time slots offered by sellers. "
            "Fields: id, label (e.g. Morning 7am-12pm), start_time, end_time. "
            "Lookup table only — no order data, no counts, no analytics. "
            "Use only to get time slot IDs for order creation or display labels in UI."
        ),
    
        "fields": "id (str), created_on (str), updated_on (str), is_deleted (bool), name (str), start (str), end (str), created_by (str), updated_by (str)",
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
    
        "fields": "id (str), created_on (str), updated_on (str), is_deleted (bool), name (str), sort (int), created_by (str), updated_by (str)",
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
    
        "fields": "id (str), object (str), created (int), updated (int), users (JSON), order_groups (JSON), invoices (JSON), has_past_due_invoices (bool), created_on (str), updated_on (str), is_deleted (bool), name (str), project_id (str), street (str), street2 (str), city (str), state (str), postal_code (str), country (str), latitude (float), longitude (float), access_details (str), description (str), autopay (bool), is_archived (bool), allow_saturday_delivery (bool), allow_sunday_delivery (bool), tax_exempt_status (str), estimated_start_date (str), estimated_end_date (str), source (str), source_id (str), product_wish_list (str), bid_due_date (str), estimated_project_value (float), first_touch_sent_at (str), created_by (str), updated_by (str), user_group (str), user (str), user_address_type (str), default_payment_method (str), brand (str), on_site_contact (str)",
        "method": "GET",
    },
    "api_v1_user_addresses_filter_options_list": {
        "path": "/api/v1/user-addresses/filter_options/",
        "description": (
            "Returns available filter options for the user addresses (job sites) list. "
            "Returns distinct city/state values for building filter UI."
        ),
    
        "fields": "value (str), label (str), count (int)",
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
    
        "fields": "id (str), redirect_url (str), updated_by (str), created_by (str), created_on (str), updated_on (str), is_deleted (bool), email (str), phone (str), type (str), first_name (str), last_name (str), status (str), user_group (str), role (str), user.id (str), user.user_id (str), user.phone (str), user.phone_revealed (bool), user.phone_revealed_on (str), user.email (str), user.push_id (str), user.date_joined (str), user.first_name (str), user.last_name (str), user.username (str), user.photo_url (str), user.photo (str), user.identity_verified (bool), user.is_onboarded (bool), user.is_staff (bool), user.is_superuser (bool), user.is_admin (bool), user.is_archived (bool), user.is_active (bool), user.source (str), user.terms_accepted (str), user.type (str), user.last_active (str), user.last_login (str), user.timezone (str), user.send_new_invoice_emails (bool), user.redirect_url (str), user.user_group (str), user.role (str)",
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
    
        "fields": "id (str), created_on (str), updated_on (str), is_deleted (bool), requested_credit_limit (float), status (str), estimated_monthly_revenue (float), estimated_monthly_spend (float), accepts_credit_authorization (bool), credit_report (str), assessment (str), balance (str), run_rate (str), cashflow (str), created_by (str), updated_by (str), user_group (str)",
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
        "fields": "id (str), seller (str), credit_applications (JSON), net_terms (int), users (JSON), user_id (str), account_owner (str), owner_pod (str), identity_verified (bool), pending_credit_determination (bool), latest_policies (JSON), sales_status (str), lifecycle_status (str), first_confirmed_order_date (str), last_confirmed_order_date (str), days_since_last_order (int), created_on (str), updated_on (str), is_deleted (bool), name (str), domain (str), phone (str), is_superuser (bool), parent_account_id (str), credit_line_limit (float), compliance_status (str), tax_exempt_status (str), do_not_rent (bool), send_account_summary_emails (bool), leased_and_rented_equipment_insurance_type (str), owned_and_rented_equiptment_coi (str), leased_and_rented_equipment_insurance_limit (str), RPP_COI_Exp_Date (str), apollo_account_id (str), tax_exempt_document (str), tax_exempt_expiration_date (str), master_service_agreement (str), source (str), source_id (str), is_unverified_domain (bool), linkedin_url (str), website_url (str), twitter_url (str), facebook_url (str), logo_url (str), short_description (str), founded_year (float), languages (JSON), keywords (JSON), street_address (str), city (str), state (str), postal_code (str), country (str), raw_address (str), annual_revenue (float), annual_revenue_printed (str), market_cap (str), publicly_traded_symbol (str), publicly_traded_exchange (str), total_funding (str), total_funding_printed (str), latest_funding_stage (str), latest_funding_round_date (str), sic_codes (JSON), naics_codes (JSON), technology_names (JSON), current_technologies (JSON), num_suborganizations (float), suborganizations (JSON), created_by (str), updated_by (str), industry (int), default_payment_method (str), superadmin_user (str), branding.id (str), branding.display_name (str), branding.logo (str), branding.primary (str), branding.secondary (str), branding.account (str), billing.id (str), billing.email (str), billing.tax_id (str), billing.street (str), billing.city (str), billing.state (str), billing.postal_code (str), billing.country (str), billing.latitude (float), billing.longitude (float), billing.send_new_invoice_emails (bool), legal.id (str), legal.name (str), legal.tax_id (float), legal.accepted_net_terms (str), legal.years_in_business (float), legal.doing_business_as (str), legal.structure (str), legal.industry (str), legal.street (str), legal.city (str), legal.state (str), legal.postal_code (str), legal.country (str), legal.latitude (float), legal.longitude (float), departmental_head_count.legal (float), departmental_head_count.sales (float), departmental_head_count.finance (float), departmental_head_count.support (float), departmental_head_count.education (float), departmental_head_count.marketing (float), departmental_head_count.accounting (float), departmental_head_count.consulting (float), departmental_head_count.operations (float), departmental_head_count.engineering (float), departmental_head_count.data_science (float), departmental_head_count.administrative (float), departmental_head_count.arts_and_design (float), departmental_head_count.human_resources (float), departmental_head_count.entrepreneurship (float), departmental_head_count.product_management (float), departmental_head_count.business_development (float), departmental_head_count.information_technology (float), departmental_head_count.media_and_commmunication (float), enrichment_data.apollo.id (str), enrichment_data.apollo.city (str), enrichment_data.apollo.name (str), enrichment_data.apollo.phone (str), enrichment_data.apollo.state (str), enrichment_data.apollo.account.id (str), enrichment_data.apollo.account.city (str), enrichment_data.apollo.account.name (str), enrichment_data.apollo.account.phone (str), enrichment_data.apollo.account.state (str), enrichment_data.apollo.account.domain (str), enrichment_data.apollo.account.source (str), enrichment_data.apollo.account.country (str), enrichment_data.apollo.account.team_id (str), enrichment_data.apollo.account.modality (str), enrichment_data.apollo.account.owner_id (str), enrichment_data.apollo.account.label_ids (JSON), enrichment_data.apollo.account.created_at (str), enrichment_data.apollo.account.creator_id (str), enrichment_data.apollo.account.hubspot_id (float), enrichment_data.apollo.account.postal_code (str), enrichment_data.apollo.account.raw_address (str), enrichment_data.apollo.account.show_intent (str), enrichment_data.apollo.account.twitter_url (float), enrichment_data.apollo.account.crm_owner_id (float), enrichment_data.apollo.account.facebook_url (float), enrichment_data.apollo.account.linkedin_url (float), enrichment_data.apollo.account.phone_status (str), enrichment_data.apollo.account.salesforce_id (float), enrichment_data.apollo.account.crm_record_url (float), enrichment_data.apollo.account.street_address (str), enrichment_data.apollo.account.existence_level (str), enrichment_data.apollo.account.intent_strength (float), enrichment_data.apollo.account.organization_id (str), enrichment_data.apollo.account.original_source (str), enrichment_data.apollo.account.sanitized_phone (str), enrichment_data.apollo.account.account_stage_id (str), enrichment_data.apollo.account.parent_account_id (float), enrichment_data.apollo.account.last_activity_date (str), enrichment_data.apollo.account.source_display_name (str), enrichment_data.apollo.account.typed_custom_fields.68043bc245357e001902a93a (str), enrichment_data.apollo.account.typed_custom_fields.680bda11ca8381001cb1d86a (str), enrichment_data.apollo.account.typed_custom_fields.680bdaf4c118880019961b5f (str), enrichment_data.apollo.account.typed_custom_fields.680bdb63c0590800117c311c (float), enrichment_data.apollo.account.typed_custom_fields.680bdc13dba4db0015acbf62 (str), enrichment_data.apollo.account.typed_custom_fields.680bde0ccc2ef60011fb8832 (str), enrichment_data.apollo.account.typed_custom_fields.680bde3249f6f7001dfc9c23 (str), enrichment_data.apollo.account.typed_custom_fields.680bde4d65b8c10018d6bbac (str), enrichment_data.apollo.account.typed_custom_fields.680be9321c637b001dac86b7 (str), enrichment_data.apollo.account.typed_custom_fields.68123ea44ab550001d773733 (float), enrichment_data.apollo.account.godmode_apollo_creator (float), enrichment_data.apollo.account.account_playbook_statuses (JSON), enrichment_data.apollo.account.suggested_from_rule_engine_config_id (float), enrichment_data.apollo.account.organization_headcount_six_month_growth (float), enrichment_data.apollo.account.organization_headcount_twelve_month_growth (float), enrichment_data.apollo.account.organization_headcount_twenty_four_month_growth (float), enrichment_data.apollo.country (str), enrichment_data.apollo.blog_url (float), enrichment_data.apollo.industry (str), enrichment_data.apollo.keywords (JSON), enrichment_data.apollo.logo_url (str), enrichment_data.apollo.languages (JSON), enrichment_data.apollo.sic_codes (JSON), enrichment_data.apollo.account_id (str), enrichment_data.apollo.industries (JSON), enrichment_data.apollo.postal_code (str), enrichment_data.apollo.raw_address (str), enrichment_data.apollo.twitter_url (str), enrichment_data.apollo.website_url (str), enrichment_data.apollo.facebook_url (str), enrichment_data.apollo.founded_year (float), enrichment_data.apollo.linkedin_uid (str), enrichment_data.apollo.linkedin_url (str), enrichment_data.apollo.alexa_ranking (float), enrichment_data.apollo.angellist_url (float), enrichment_data.apollo.primary_phone.number (str), enrichment_data.apollo.primary_phone.source (str), enrichment_data.apollo.primary_phone.sanitized_number (str), enrichment_data.apollo.total_funding (float), enrichment_data.apollo.annual_revenue (float), enrichment_data.apollo.crunchbase_url (float), enrichment_data.apollo.funding_events (JSON), enrichment_data.apollo.primary_domain (str), enrichment_data.apollo.street_address (str), enrichment_data.apollo.industry_tag_id (str), enrichment_data.apollo.sanitized_phone (str), enrichment_data.apollo.snippets_loaded (str), enrichment_data.apollo.org_chart_sector (str), enrichment_data.apollo.suborganizations (JSON), enrichment_data.apollo.technology_names (JSON), enrichment_data.apollo.industry_tag_hash.construction (str), enrichment_data.apollo.org_chart_removed (float), enrichment_data.apollo.short_description (str), enrichment_data.apollo.current_technologies (JSON), enrichment_data.apollo.latest_funding_stage (float), enrichment_data.apollo.num_suborganizations (float), enrichment_data.apollo.organization_revenue (float), enrichment_data.apollo.secondary_industries (JSON), enrichment_data.apollo.retail_location_count (float), enrichment_data.apollo.total_funding_printed (float), enrichment_data.apollo.annual_revenue_printed (str), enrichment_data.apollo.publicly_traded_symbol (str), enrichment_data.apollo.departmental_head_count.legal (float), enrichment_data.apollo.departmental_head_count.sales (float), enrichment_data.apollo.departmental_head_count.finance (float), enrichment_data.apollo.departmental_head_count.support (float), enrichment_data.apollo.departmental_head_count.education (float), enrichment_data.apollo.departmental_head_count.marketing (float), enrichment_data.apollo.departmental_head_count.accounting (float), enrichment_data.apollo.departmental_head_count.consulting (float), enrichment_data.apollo.departmental_head_count.operations (float), enrichment_data.apollo.departmental_head_count.engineering (float), enrichment_data.apollo.departmental_head_count.data_science (float), enrichment_data.apollo.departmental_head_count.administrative (float), enrichment_data.apollo.departmental_head_count.arts_and_design (float), enrichment_data.apollo.departmental_head_count.human_resources (float), enrichment_data.apollo.departmental_head_count.entrepreneurship (float), enrichment_data.apollo.departmental_head_count.product_management (float), enrichment_data.apollo.departmental_head_count.business_development (float), enrichment_data.apollo.departmental_head_count.information_technology (float), enrichment_data.apollo.departmental_head_count.media_and_commmunication (float), enrichment_data.apollo.estimated_num_employees (float), enrichment_data.apollo.owned_by_organization_id (float), enrichment_data.apollo.publicly_traded_exchange (str), enrichment_data.apollo.latest_funding_round_date (float), enrichment_data.apollo.org_chart_root_people_ids (JSON), enrichment_data.apollo.organization_revenue_printed (str), enrichment_data.apollo.org_chart_show_department_filter (float), legal (float), enrichment_data.apollo.market_cap (str), enrichment_data.apollo.naics_codes (JSON), enrichment_data.apollo.industry_tag_hash.retail (str)",
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
    
        "fields": "id (str), user_group (str), identity_verified (bool), identity_verification_session.id (str), identity_verification_session.stripe_session_id (str), identity_verification_session.status (str), identity_verification_session.created_on (str), identity_verification_session.updated_on (str), identity_verification_session.user (str)",
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
    
        "fields": "id (str), user_id (str), phone (str), phone_revealed (bool), phone_revealed_on (str), email (str), push_id (str), date_joined (str), first_name (str), last_name (str), username (str), photo_url (str), photo (str), identity_verified (bool), is_onboarded (bool), is_staff (bool), is_superuser (bool), is_admin (bool), is_archived (bool), is_active (bool), source (str), terms_accepted (str), type (str), last_active (str), last_login (str), timezone (str), send_new_invoice_emails (bool), redirect_url (str), user_group (str), role (str)",
        "method": "GET",
    },
    "api_v1_users_me_list": {
        "path": "/api/v1/users/me/",
        "description": (
            "Returns the currently authenticated user's full profile. "
            "Use this to identify who is making requests (role, account, type)."
        ),
    
        "fields": "id (str), user_id (str), phone (str), phone_revealed (bool), phone_revealed_on (str), email (str), push_id (str), date_joined (str), first_name (str), last_name (str), username (str), photo_url (str), photo (str), identity_verified (bool), is_onboarded (bool), is_staff (bool), is_superuser (bool), is_admin (bool), is_archived (bool), is_active (bool), source (str), terms_accepted (str), type (str), last_active (str), last_login (str), timezone (str), send_new_invoice_emails (bool), redirect_url (str), user_group (str), role (str)",
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
    
        "fields": "id (str), created_on (str), updated_on (str), is_deleted (bool), name (str), created_by (str), updated_by (str)",
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
    
        "fields": "cart (JSON), subtotal (float), cart_count (int)",
        "method": "GET",
    },
    "checkout_v1_cart_count_list": {
        "path": "/checkout/v1/cart/count/",
        "description": (
            "Returns the total number of items in the authenticated user's active cart. "
            "Fields: count. "
            "Use this for the cart badge count in the navbar."
        ),
    
        "fields": "cart_count (int)",
        "method": "GET",
    },
    "checkout_v1_carts_list": {
        "path": "/checkout/v1/carts/",
        "description": (
            "Returns a list of carts with lightweight summary data. "
            "Fields: id, user_address_id, item_count, total_price, created_on, updated_on. "
            "Use this to list carts by job site, count carts per account, or track cart activity."
        ),
    
        "fields": "id (str), code (str), created_on (str), updated_on (str), payment_method (str), pay_later (bool), to_emails (str), quote_expiration (str), quote_accepted_at (str), submitted_on (str), lost_on (str), lost_reason (str), first_touch_email_id (str), first_touch_open_count (int), first_touch_click_count (int), orders (JSON), user_address.id (str), user_address.object (str), user_address.created (int), user_address.updated (int), user_address.users (JSON), user_address.order_groups (JSON), user_address.invoices (JSON), user_address.has_past_due_invoices (bool), user_address.created_on (str), user_address.updated_on (str), user_address.is_deleted (bool), user_address.name (str), user_address.project_id (str), user_address.street (str), user_address.street2 (str), user_address.city (str), user_address.state (str), user_address.postal_code (str), user_address.country (str), user_address.latitude (float), user_address.longitude (float), user_address.access_details (str), user_address.description (str), user_address.autopay (bool), user_address.is_archived (bool), user_address.allow_saturday_delivery (bool), user_address.allow_sunday_delivery (bool), user_address.tax_exempt_status (str), user_address.estimated_start_date (str), user_address.estimated_end_date (str), user_address.source (str), user_address.source_id (str), user_address.product_wish_list (str), user_address.bid_due_date (str), user_address.estimated_project_value (str), user_address.first_touch_sent_at (str), user_address.created_by (str), user_address.updated_by (str), user_address.user_group (str), user_address.user (str), user_address.user_address_type (str), user_address.default_payment_method (str), user_address.brand (str), user_address.on_site_contact (str)",
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
    # ── IMPERSONATION ─────────────────────────────────────────────────────────

    "impersonation_start": {
        "path": None,
        "description": (
            "Start impersonating a specific user by UUID. "
            "All subsequent API calls will be scoped to that user's data. "
            "Use when switching context to act on behalf of a specific user."
        ),
        "fields": "",
        "method": "POST",
    },
    "impersonation_end": {
        "path": None,
        "description": (
            "Stop impersonating the current user and revert to normal authentication. "
            "Use after finishing work scoped to an impersonated user."
        ),
        "fields": "",
        "method": "POST",
    },
    "impersonation_status": {
        "path": None,
        "description": (
            "Check whether impersonation is currently active and which user is being impersonated. "
            "Use when you need to know the current impersonation state."
        ),
        "fields": "is_active (bool), user_id (str)",
        "method": "GET",
    },

}


def get_tool_catalog_text() -> str:
    lines = []
    for name, info in MCP_TOOL_CATALOG.items():
        lines.append("  " + name + "\n    -> " + info["description"])
    return "\n".join(lines)
