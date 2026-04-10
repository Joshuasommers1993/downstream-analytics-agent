# API Response Field Mappings

Each leaf value is the DB table where the column is physically defined (`app_model` convention).
Special values: `"pagination"`, `"computed"`, `"ghost"`.

---

## api_v1_industries_list
`GET /api/v1/industries/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_industry",
            "name": "api_industry",
            "description": "api_industry",
            "image": "api_industry",
            "slug": "api_industry",
            "sort": "api_industry",
            "main_product_categories": "computed"  # SerializerMethodField; IDs by default, expanded objects with expand[]
        }
    ]
}
```

---

## api_v1_waste_types_list
`GET /api/v1/waste-types/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_wastetype",
            "created_on": "api_wastetype",
            "updated_on": "api_wastetype",
            "is_deleted": "api_wastetype",
            "name": "api_wastetype",
            "created_by": "api_wastetype",
            "updated_by": "api_wastetype"
        }
    ]
}
```

---

## api_v1_main_products_list
`GET /api/v1/main-products/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_mainproduct",
            "main_product_category": "api_mainproduct",
            "name": "api_mainproduct",
            "ar_url": "api_mainproduct",
            "description": "api_mainproduct",
            "image_del": "api_mainproduct",
            "slug": "api_mainproduct",
            "sort": "api_mainproduct",
            "popularity": "api_mainproduct",
            "default_take_rate": "api_mainproduct",
            "dynamic_max_take_rate": "api_mainproduct",
            "minimum_take_rate": "api_mainproduct",
            "dynamic_min_take_rate": "api_mainproduct",
            "minimum_take_rate_hour": "api_mainproduct",
            "minimum_take_rate_day": "api_mainproduct",
            "minimum_take_rate_week": "api_mainproduct",
            "minimum_take_rate_two_weeks": "api_mainproduct",
            "minimum_take_rate_month": "api_mainproduct",
            "included_tonnage_quantity": "api_mainproduct",
            "max_tonnage_quantity": "api_mainproduct",
            "main_product_code": "api_mainproduct",
            "has_rental": "api_mainproduct",
            "has_rental_one_step": "api_mainproduct",
            "has_rental_multi_step": "api_mainproduct",
            "has_service": "api_mainproduct",
            "has_service_times_per_week": "api_mainproduct",
            "has_material": "api_mainproduct",
            "allows_pick_up": "api_mainproduct",
            "has_bundled_qty": "api_mainproduct",
            "has_winterization": "api_mainproduct",
            "can_bundle_freight": "api_mainproduct",
            "texas_surcharge_applies": "api_mainproduct",
            "has_rpp": "api_mainproduct",
            "estimated_replacement_value": "api_mainproduct",
            "is_related": "api_mainproduct",
            "created_on": "api_mainproduct",
            "updated_on": "api_mainproduct",
            "is_deleted": "api_mainproduct",
            "created_by": "api_mainproduct",
            "updated_by": "api_mainproduct",
            "listings_count": "computed",
            "likes_count": "computed",
            "main_product_infos": [
                {
                    "id": "api_mainproductinfo",
                    "name": "api_mainproductinfo",
                    "description": "api_mainproductinfo",
                    "sort": "api_mainproductinfo",
                    "main_product": "api_mainproductinfo",
                    "created_on": "api_mainproductinfo",
                    "updated_on": "api_mainproductinfo",
                    "is_deleted": "api_mainproductinfo",
                    "created_by": "api_mainproductinfo",
                    "updated_by": "api_mainproductinfo"
                }
            ],
            "images": ["computed"],   # flat list of URL strings (SerializerMethodField → image.image.url)
            "add_ons": [
                {
                    "id": "api_addon",
                    "main_product": "api_addon",
                    "name": "api_addon",
                    "sort": "api_addon",
                    "choices": [
                        {
                            "id": "api_addonchoice",
                            "add_on": "api_addonchoice",
                            "name": "api_addonchoice",
                        }
                    ],
                }
            ],
            "tags": [
                {
                    "id": "api_mainproducttag",
                    "name": "api_mainproducttag",
                    "active": "api_mainproducttag",
                    "created_on": "api_mainproducttag",
                    "updated_on": "api_mainproducttag",
                    "is_deleted": "api_mainproducttag",
                    "created_by": "api_mainproducttag",
                    "updated_by": "api_mainproducttag"
                }
            ],
            "main_product_waste_types": [
                {
                    "id": "api_mainproductwastetype",
                    "main_product": "api_mainproductwastetype",
                    "popularity": "api_mainproductwastetype",
                    "created_on": "api_mainproductwastetype",
                    "updated_on": "api_mainproductwastetype",
                    "is_deleted": "api_mainproductwastetype",
                    "created_by": "api_mainproductwastetype",
                    "updated_by": "api_mainproductwastetype",
                    "waste_type": {
                        "id": "api_wastetype",
                        "name": "api_wastetype",
                        "created_on": "api_wastetype",
                        "updated_on": "api_wastetype",
                        "is_deleted": "api_wastetype",
                        "created_by": "api_wastetype",
                        "updated_by": "api_wastetype"
                    }
                }
            ],
            "products": [
                {
                    "id": "api_product",
                    "main_product": "api_product",
                    "product_code": "api_product",
                    "description": "api_product",
                    "removal_price": "api_product",
                    "popularity": "api_product",
                    "created_on": "api_product",
                    "updated_on": "api_product",
                    "is_deleted": "api_product",
                    "created_by": "api_product",
                    "updated_by": "api_product",
                    "product_add_on_choices": [
                        {
                            "id": "api_productaddonchoice",
                            "product": "api_productaddonchoice",
                            "name": "api_productaddonchoice",
                            "created_on": "api_productaddonchoice",
                            "updated_on": "api_productaddonchoice",
                            "is_deleted": "api_productaddonchoice",
                            "created_by": "api_productaddonchoice",
                            "updated_by": "api_productaddonchoice",
                            "add_on_choice": {
                                "id": "api_addonchoice",
                                "add_on": "api_addonchoice",
                                "name": "api_addonchoice",
                                "created_on": "api_addonchoice",
                                "updated_on": "api_addonchoice",
                                "is_deleted": "api_addonchoice",
                                "created_by": "api_addonchoice",
                                "updated_by": "api_addonchoice"
                            }
                        }
                    ]
                }
            ],
            "related_products": [
                # same structure as top-level main product (recursive MainProductSerializer)
            ]
        }
    ]
}
```

---

## api_v1_sellers_list
`GET /api/v1/sellers/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_seller",
            "created_on": "api_seller",
            "updated_on": "api_seller",
            "is_deleted": "api_seller",
            "created_by": "api_seller",
            "updated_by": "api_seller",
            "open_days": "api_seller",
            "name": "api_seller",
            "public_subdomain_enabled": "api_seller",
            "public_subdomain": "api_seller",
            "phone": "api_seller",
            "website": "api_seller",
            "order_email": "api_seller",
            "order_phone": "api_seller",
            "type": "api_seller",
            "location_type": "api_seller",
            "status": "api_seller",
            "lead_time": "api_seller",
            "type_display": "api_seller",
            "marketplace_display_name": "api_seller",
            "open_time": "api_seller",
            "close_time": "api_seller",
            "lead_time_hrs": "api_seller",
            "announcement": "api_seller",
            "live_menu_is_active": "api_seller",
            "location_logo_url": "api_seller",
            "logo": "api_seller",
            "downstream_insurance_requirements_met": "api_seller",
            "badge": "api_seller",
            "salesforce_seller_id": "api_seller",
            "about_us": "api_seller",
            "do_not_rent": "api_seller"
            # excluded: stripe_connect_id
        }
    ]
}
```

---

## api_v1_seller_locations_list
`GET /api/v1/seller-locations/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_sellerlocation",
            "object": "computed",
            "created": "computed",
            "updated": "computed",
            "created_on": "api_sellerlocation",
            "updated_on": "api_sellerlocation",
            "is_deleted": "api_sellerlocation",
            "created_by": "api_sellerlocation",
            "updated_by": "api_sellerlocation",
            "seller": "api_sellerlocation",
            "is_compliant": "computed",
            "open_days": "api_sellerlocation",
            "open_hours": [  # empty array when not expanded
                {
                    "id": "api_sellerlocationopenhours",
                    "seller_location": "api_sellerlocationopenhours",
                    "day_of_week": {
                        "id": "api_dayofweek",
                        "name": "api_dayofweek",
                        "number": "api_dayofweek",
                        "created_on": "api_dayofweek",
                        "updated_on": "api_dayofweek",
                        "is_deleted": "api_dayofweek",
                        "created_by": "api_dayofweek",
                        "updated_by": "api_dayofweek",
                    },
                    "open_time": "api_sellerlocationopenhours",
                    "close_time": "api_sellerlocationopenhours"
                }
            ],
            "users": [],  # empty array when not expanded
            "name": "api_sellerlocation",
            "public_subdomain_enabled": "api_sellerlocation",
            "public_subdomain": "api_sellerlocation",
            "street": "api_sellerlocation",
            "city": "api_sellerlocation",
            "state": "api_sellerlocation",
            "postal_code": "api_sellerlocation",
            "country": "api_sellerlocation",
            "latitude": "api_sellerlocation",
            "longitude": "api_sellerlocation",
            "geo_point": "api_sellerlocation",
            "open_time": "api_sellerlocation",
            "close_time": "api_sellerlocation",
            "lead_time_hrs": "api_sellerlocation",
            "announcement": "api_sellerlocation",
            "live_menu_is_active": "api_sellerlocation",
            "location_logo_image": "api_sellerlocation",
            "sends_invoices": "api_sellerlocation",
            "do_not_rent": "api_sellerlocation",
            "payee_name": "api_sellerlocation",
            "order_email": "api_sellerlocation",
            "order_phone": "api_sellerlocation",
            "gl_coi": "api_sellerlocation",
            "gl_coi_expiration_date": "api_sellerlocation",
            "gl_limit": "api_sellerlocation",
            "auto_coi": "api_sellerlocation",
            "auto_coi_expiration_date": "api_sellerlocation",
            "auto_limit": "api_sellerlocation",
            "workers_comp_coi": "api_sellerlocation",
            "workers_comp_coi_expiration_date": "api_sellerlocation",
            "workers_comp_limit": "api_sellerlocation",
            "w9": "api_sellerlocation",
            "ein": "api_sellerlocation",
            "company_type": "api_sellerlocation",
            "payout_delay": "api_sellerlocation",
            "timezone": "api_sellerlocation"
            # excluded: stripe_connect_account_id, zoho_vendor_id
        }
    ]
}
```

---

## api_v1_invoices_list
`GET /api/v1/invoices/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "billing_invoice",
            "created_on": "billing_invoice",
            "updated_on": "billing_invoice",
            "is_deleted": "billing_invoice",
            "created_by": "billing_invoice",
            "updated_by": "billing_invoice",
            "created": "computed",
            "updated": "computed",
            "invoice_id": "billing_invoice",
            "amount_due": "billing_invoice",
            "amount_paid": "billing_invoice",
            "amount_remaining": "billing_invoice",
            "due_date": "billing_invoice",
            "hosted_invoice_url": "billing_invoice",
            "invoice_pdf": "billing_invoice",
            "pdf": "billing_invoice",
            "metadata": "billing_invoice",
            "number": "billing_invoice",
            "paid": "billing_invoice",
            "status": "billing_invoice",
            "total": "billing_invoice",
            "check_sent_at": "billing_invoice",
            "display_total": "computed",
            "has_outstanding_payment": "computed",
            "user_address": "billing_invoice",      # FK ID
            "order": "billing_invoice",             # FK ID
            "items": "computed",                    # from Stripe API
            "groups": "computed",                   # from Stripe API
            "pre_payment_credit": "computed",
            "post_payment_credit": "computed",
            "object": "computed",                   # hardcoded "invoice"
            "main_product": "computed",
            "product_add_ons": [],                  # expanded only
            "refunds": [
                {
                    "id": "billing_invoicerefund",
                    "created_on": "billing_invoicerefund",
                    "updated_on": "billing_invoicerefund",
                    "is_deleted": "billing_invoicerefund",
                    "created_by": "billing_invoicerefund",
                    "updated_by": "billing_invoicerefund",
                    "invoice": "billing_invoicerefund",
                    "invoice_payment": "billing_invoicerefund",
                    "amount": "billing_invoicerefund",
                    "description": "billing_invoicerefund",
                    "reason": "billing_invoicerefund",
                    "status": "billing_invoicerefund",
                    "failure_reason": "billing_invoicerefund",
                    "reference": "billing_invoicerefund",
                    "reference_type": "billing_invoicerefund",
                    "reference_status": "billing_invoicerefund"
                }
            ],
            "payment_info": "ghost",
            "group_invoice": "ghost"
        }
    ]
}
```

---

## api_v1_payouts_list
`GET /api/v1/payouts/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_payout",
            "created_on": "api_payout",
            "updated_on": "api_payout",
            "is_deleted": "api_payout",
            "created_by": "api_payout",
            "updated_by": "api_payout",
            "checkbook_payout_id": "api_payout",
            "lob_check_id": "api_payout",
            "check_number": "api_payout",
            "amount": "api_payout",
            "description": "api_payout",
            "order": "api_payout",      # FK ID
            "object": "computed",
            "invoice_id": "computed",   # derived from order → seller_invoice_payable_line_items
            "check": "computed"         # from Lob external API; null when not requested
        }
    ]
}
```

---

## api_v1_orders_list
`GET /api/v1/orders/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_order",
            "created_on": "api_order",
            "updated_on": "api_order",
            "created_by": "api_order",
            "code": "api_order",
            "start_date": "api_order",
            "end_date": "api_order",
            "submitted_on": "api_order",
            "accepted_on": "api_order",
            "completed_on": "api_order",
            "status": "api_order",
            "schedule_window": "api_order",
            "sent_auto_renewal_message": "api_order",
            "disposal_location": {
                "id": "api_disposallocation",
                "name": "api_disposallocation",
                "street": "api_disposallocation",
                "city": "api_disposallocation",
                "state": "api_disposallocation",
                "postal_code": "api_disposallocation",
                "country": "api_disposallocation",
                "latitude": "api_disposallocation",
                "longitude": "api_disposallocation",
                "created_on": "api_disposallocation",
                "updated_on": "api_disposallocation",
                "is_deleted": "api_disposallocation",
                "created_by": "api_disposallocation",
                "updated_by": "api_disposallocation",
            },
            "order_group": "api_order",          # FK ID
            "main_product": "computed",
            "seller": "computed",
            "account_owner": "api_order",        # FK ID
            "submitted_by": "api_order",         # FK ID
            "order_type": "computed",
            "price": "computed"
        }
    ]
}
```

---

## api_v1_order_groups_list
`GET /api/v1/order-groups/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_ordergroup",
            "created_on": "api_ordergroup",
            "updated_on": "api_ordergroup",
            "is_deleted": "api_ordergroup",
            "created_by": "api_ordergroup",
            "updated_by": "api_ordergroup",
            "code": "api_ordergroup",
            "start_date": "api_ordergroup",
            "end_date": "api_ordergroup",
            "estimated_end_date": "api_ordergroup",
            "is_delivery": "api_ordergroup",
            "access_details": "api_ordergroup",
            "placement_details": "api_ordergroup",
            "delivered_to_street": "api_ordergroup",
            "take_rate": "api_ordergroup",
            "times_per_week": "api_ordergroup",
            "shift_count": "api_ordergroup",
            "delivery_fee": "api_ordergroup",
            "removal_fee": "api_ordergroup",
            "status": "api_ordergroup",
            "tonnage_quantity": "api_ordergroup",
            "agreement": "api_ordergroup",
            "agreement_signed_on": "api_ordergroup",
            "agreement_signed_by": "api_ordergroup",  # FK ID
            "user": "api_ordergroup",                 # FK ID
            "on_site_contact": "api_ordergroup",      # FK ID
            "user_address": "api_ordergroup",         # FK ID
            "seller_product_seller_location": "api_ordergroup",  # FK ID
            "main_product": "computed",
            "waste_type": "api_ordergroup",           # FK ID
            "time_slot": "api_ordergroup",            # FK ID
            "service_recurring_frequency": {
                "id": "api_servicerecurringfrequency",
                "name": "api_servicerecurringfrequency",
                "created_on": "api_servicerecurringfrequency",
                "updated_on": "api_servicerecurringfrequency",
                "is_deleted": "api_servicerecurringfrequency",
                "created_by": "api_servicerecurringfrequency",
                "updated_by": "api_servicerecurringfrequency",
            },
            "preferred_service_days": [
                {
                    "id": "api_dayofweek",
                    "name": "api_dayofweek",
                    "number": "api_dayofweek",
                    "created_on": "api_dayofweek",
                    "updated_on": "api_dayofweek",
                    "is_deleted": "api_dayofweek",
                    "created_by": "api_dayofweek",
                    "updated_by": "api_dayofweek",
                }
            ],
            "active": "computed",
            "conversation": "computed",
            "asset": "computed",
            "orders": [],                             # array of FK IDs
            "attachments": [
                {
                    "id": "api_ordergroupattachment",
                    "order_group": "api_ordergroupattachment",
                    "file_name": "computed",   # read_only CharField derived from file
                    "file_type": "computed",   # read_only CharField derived from file
                    # "file" is write_only — not returned in GET responses
                }
            ],
            "service": {
                "id": "api_ordergroupservice",
                "order_group": "api_ordergroupservice",
                "created_on": "api_ordergroupservice",
                "updated_on": "api_ordergroupservice",
                "is_deleted": "api_ordergroupservice",
                "price_per_mile": "api_ordergroupservice",
                "flat_rate_price": "api_ordergroupservice",
                "rate": "api_ordergroupservice",
                "miles": "api_ordergroupservice",
                "created_by": "api_ordergroupservice",
                "updated_by": "api_ordergroupservice"
            },
            "rental": {
                "id": "api_ordergrouprental",
                "order_group": "api_ordergrouprental",
                "created_on": "api_ordergrouprental",
                "updated_on": "api_ordergrouprental",
                "is_deleted": "api_ordergrouprental",
                "included_days": "api_ordergrouprental",
                "price_per_day_included": "api_ordergrouprental",
                "price_per_day_additional": "api_ordergrouprental",
                "created_by": "api_ordergrouprental",
                "updated_by": "api_ordergrouprental"
            },
            "material": {
                "id": "api_ordergroupmaterial",
                "order_group": "api_ordergroupmaterial",
                "created_on": "api_ordergroupmaterial",
                "updated_on": "api_ordergroupmaterial",
                "is_deleted": "api_ordergroupmaterial",
                "price_per_ton": "api_ordergroupmaterial",
                "tonnage_included": "api_ordergroupmaterial",
                "created_by": "api_ordergroupmaterial",
                "updated_by": "api_ordergroupmaterial"
            }
        }
    ]
}
```

---

## api_v1_user_addresses_list
`GET /api/v1/user-addresses/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_useraddress",
            "object": "computed",
            "created": "computed",
            "updated": "computed",
            "created_on": "api_useraddress",
            "updated_on": "api_useraddress",
            "is_deleted": "api_useraddress",
            "created_by": "api_useraddress",
            "updated_by": "api_useraddress",
            "name": "api_useraddress",
            "project_id": "api_useraddress",
            "street": "api_useraddress",
            "street2": "api_useraddress",
            "city": "api_useraddress",
            "state": "api_useraddress",
            "postal_code": "api_useraddress",
            "country": "api_useraddress",
            "latitude": "api_useraddress",
            "longitude": "api_useraddress",
            "access_details": "api_useraddress",
            "description": "api_useraddress",
            "autopay": "api_useraddress",
            "is_archived": "api_useraddress",
            "allow_saturday_delivery": "api_useraddress",
            "allow_sunday_delivery": "api_useraddress",
            "tax_exempt_status": "api_useraddress",
            "estimated_start_date": "api_useraddress",
            "estimated_end_date": "api_useraddress",
            "source": "api_useraddress",
            "source_id": "api_useraddress",
            "product_wish_list": "api_useraddress",
            "bid_due_date": "api_useraddress",
            "estimated_project_value": "api_useraddress",
            "first_touch_sent_at": "api_useraddress",
            "user_group": "api_useraddress",        # FK ID
            "user": "api_useraddress",              # FK ID
            "user_address_type": "api_useraddress", # FK ID
            "default_payment_method": "api_useraddress",  # FK ID
            "brand": "api_useraddress",             # FK ID
            "on_site_contact": "api_useraddress",   # FK ID
            "users": "computed",
            "order_groups": "computed",
            "invoices": "computed",
            "has_past_due_invoices": "computed"
        }
    ]
}
```

---

## api_v1_user_groups_list
`GET /api/v1/user-groups/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_usergroup",
            "created_on": "api_usergroup",
            "updated_on": "api_usergroup",
            "is_deleted": "api_usergroup",
            "created_by": "api_usergroup",
            "updated_by": "api_usergroup",
            "seller": "api_usergroup",          # FK ID by default
            "branding": {
                "id": "api_branding",
                "display_name": "api_branding",
                "logo": "api_branding",
                "primary": "api_branding",
                "secondary": "api_branding",
                "account": "api_branding"
            },
            "billing": {
                "id": "api_usergroupbilling",
                "email": "api_usergroupbilling",
                "tax_id": "api_usergroupbilling",
                "street": "api_usergroupbilling",
                "city": "api_usergroupbilling",
                "state": "api_usergroupbilling",
                "postal_code": "api_usergroupbilling",
                "country": "api_usergroupbilling",
                "latitude": "api_usergroupbilling",
                "longitude": "api_usergroupbilling",
                "send_new_invoice_emails": "api_usergroupbilling"
            },
            "legal": {
                "id": "api_usergrouplegal",
                "name": "api_usergrouplegal",
                "tax_id": "api_usergrouplegal",
                "accepted_net_terms": "api_usergrouplegal",
                "years_in_business": "api_usergrouplegal",
                "doing_business_as": "api_usergrouplegal",
                "structure": "api_usergrouplegal",
                "industry": "api_usergrouplegal",
                "street": "api_usergrouplegal",
                "city": "api_usergrouplegal",
                "state": "api_usergrouplegal",
                "postal_code": "api_usergrouplegal",
                "country": "api_usergrouplegal",
                "latitude": "api_usergrouplegal",
                "longitude": "api_usergrouplegal"
            },
            "credit_applications": "computed",  # array of IDs by default
            "net_terms": "api_usergroup",
            "users": "computed",                # array of IDs by default
            "user_id": "computed",              # serializer-side field, no DB column
            "account_owner": "api_usergroup",   # FK ID by default
            "owner_pod": "ghost",
            "identity_verified": "api_usergroup",
            "pending_credit_determination": "computed",
            "latest_policies": "computed",
            "sales_status": "api_usergroup",
            "lifecycle_status": "computed",
            "first_confirmed_order_date": "computed",
            "last_confirmed_order_date": "computed",
            "days_since_last_order": "computed",
            "name": "api_usergroup",
            "domain": "api_usergroup",
            "phone": "api_usergroup",
            "is_superuser": "api_usergroup",
            "parent_account_id": "api_usergroup",
            "credit_line_limit": "api_usergroup",
            "compliance_status": "api_usergroup",
            "tax_exempt_status": "api_usergroup",
            "do_not_rent": "api_usergroup",
            "send_account_summary_emails": "api_usergroup",
            "leased_and_rented_equipment_insurance_type": "api_usergroup",
            "owned_and_rented_equiptment_coi": "api_usergroup",
            "leased_and_rented_equipment_insurance_limit": "api_usergroup",
            "RPP_COI_Exp_Date": "api_usergroup",
            "apollo_account_id": "api_usergroup",
            "tax_exempt_document": "api_usergroup",
            "tax_exempt_expiration_date": "api_usergroup",
            "master_service_agreement": "api_usergroup",
            "source": "api_usergroup",
            "source_id": "api_usergroup",
            "is_unverified_domain": "api_usergroup",
            "linkedin_url": "api_usergroup",
            "website_url": "api_usergroup",
            "twitter_url": "api_usergroup",
            "facebook_url": "api_usergroup",
            "logo_url": "api_usergroup",
            "short_description": "api_usergroup",
            "founded_year": "api_usergroup",
            "languages": "api_usergroup",
            "keywords": "api_usergroup",
            "street_address": "api_usergroup",
            "city": "api_usergroup",
            "state": "api_usergroup",
            "postal_code": "api_usergroup",
            "country": "api_usergroup",
            "raw_address": "api_usergroup",
            "annual_revenue": "api_usergroup",
            "annual_revenue_printed": "api_usergroup",
            "market_cap": "api_usergroup",
            "publicly_traded_symbol": "api_usergroup",
            "publicly_traded_exchange": "api_usergroup",
            "total_funding": "api_usergroup",
            "total_funding_printed": "api_usergroup",
            "latest_funding_stage": "api_usergroup",
            "latest_funding_round_date": "api_usergroup",
            "sic_codes": "api_usergroup",
            "naics_codes": "api_usergroup",
            "technology_names": "api_usergroup",
            "current_technologies": "api_usergroup",
            "departmental_head_count": "api_usergroup",
            "num_suborganizations": "api_usergroup",
            "suborganizations": "api_usergroup",
            "enrichment_data": "api_usergroup",
            "industry": "api_usergroup",
            "default_payment_method": "api_usergroup",
            "superadmin_user": "api_usergroup",
            "stage": "api_usergroup",
            "pay_later": "api_usergroup",
            "autopay": "api_usergroup",
            "invoice_frequency": "api_usergroup",
            "intercom_id": "api_usergroup",
            "apollo_id": "api_usergroup",
            "number_of_employees": "api_usergroup",
            "credit_application_form": "api_usergroup",
            # excluded: stripe_customer_id, zoho_account_id, target_monthly_gmv,
            #           target_user_count, target_monthly_project_count
        }
    ]
}
```

---

## api_v1_users_list
`GET /api/v1/users/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_user",
            "user_id": "api_user",
            "phone": "api_user",
            "email": "api_user",
            "push_id": "api_user",
            "date_joined": "api_user",
            "first_name": "api_user",
            "last_name": "api_user",
            "username": "api_user",
            "photo_url": "api_user",
            "photo": "api_user",
            "identity_verified": "api_user",
            "is_onboarded": "api_user",
            "is_staff": "api_user",
            "is_superuser": "api_user",
            "is_admin": "api_user",
            "is_archived": "api_user",
            "is_active": "api_user",
            "source": "api_user",
            "terms_accepted": "api_user",
            "type": "api_user",
            "last_active": "api_user",
            "last_login": "api_user",
            "timezone": "api_user",
            "send_new_invoice_emails": "api_user",
            "redirect_url": "api_user",
            "user_group": "api_user",   # FK ID
            "role": "computed"
        }
    ]
}
```

---

## api_v1_users_me_list
`GET /api/v1/users/me/`

```python
{
    "id": "api_user",
    "user_id": "api_user",
    "phone": "api_user",
    "email": "api_user",
    "push_id": "api_user",
    "date_joined": "api_user",
    "first_name": "api_user",
    "last_name": "api_user",
    "username": "api_user",
    "photo_url": "api_user",
    "photo": "api_user",
    "identity_verified": "api_user",
    "is_onboarded": "api_user",
    "is_staff": "api_user",
    "is_superuser": "api_user",
    "is_admin": "api_user",
    "is_archived": "api_user",
    "is_active": "api_user",
    "source": "api_user",
    "terms_accepted": "api_user",
    "type": "api_user",
    "last_active": "api_user",
    "last_login": "api_user",
    "timezone": "api_user",
    "send_new_invoice_emails": "api_user",
    "redirect_url": "api_user",
    "user_group": "api_user",   # FK ID
    "role": "computed"
}
```

---

## api_v1_user_identity_list
`GET /api/v1/user/identity/`

```python
{
    "id": "api_user",
    "user_group": "api_user",   # FK ID
    "identity_verified": "api_user",
    "identity_verification_session": {
        "id": "identity_verification_identityverificationsession",
        "user": "identity_verification_identityverificationsession",
        "stripe_session_id": "identity_verification_identityverificationsession",
        "status": "identity_verification_identityverificationsession",
        "created_on": "identity_verification_identityverificationsession",
        "updated_on": "identity_verification_identityverificationsession"
    }
}
```

---

## api_v1_user_group_credit_applications_list
`GET /api/v1/user-group-credit-applications/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_usergroupcreditapplication",
            "created_on": "api_usergroupcreditapplication",
            "updated_on": "api_usergroupcreditapplication",
            "is_deleted": "api_usergroupcreditapplication",
            "created_by": "api_usergroupcreditapplication",
            "updated_by": "api_usergroupcreditapplication",
            "user_group": "api_usergroupcreditapplication",
            "requested_credit_limit": "api_usergroupcreditapplication",
            "status": "api_usergroupcreditapplication",
            "estimated_monthly_revenue": "api_usergroupcreditapplication",
            "estimated_monthly_spend": "api_usergroupcreditapplication",
            "accepts_credit_authorization": "api_usergroupcreditapplication",
            "credit_report": "api_usergroupcreditapplication",
            "assessment": "api_usergroupcreditapplication",
            "balance": "api_usergroupcreditapplication",
            "run_rate": "api_usergroupcreditapplication",
            "cashflow": "api_usergroupcreditapplication"
        }
    ]
}
```

---

## api_v1_user_group_credit_applications_get
`GET /api/v1/user-group-credit-applications/{id}/`

```python
{
    "id": "api_usergroupcreditapplication",
    "created_on": "api_usergroupcreditapplication",
    "updated_on": "api_usergroupcreditapplication",
    "is_deleted": "api_usergroupcreditapplication",
    "created_by": "api_usergroupcreditapplication",
    "updated_by": "api_usergroupcreditapplication",
    "user_group": "api_usergroupcreditapplication",
    "requested_credit_limit": "api_usergroupcreditapplication",
    "status": "api_usergroupcreditapplication",
    "estimated_monthly_revenue": "api_usergroupcreditapplication",
    "estimated_monthly_spend": "api_usergroupcreditapplication",
    "accepts_credit_authorization": "api_usergroupcreditapplication",
    "credit_report": "api_usergroupcreditapplication",
    "assessment": "api_usergroupcreditapplication",
    "balance": "api_usergroupcreditapplication",
    "run_rate": "api_usergroupcreditapplication",
    "cashflow": "api_usergroupcreditapplication"
}
```

---

## api_v1_insurance_policies_list
`GET /api/v1/insurance-policies/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "computed",        # encoded as ins_{type_short}_{policy_id}
            "object": "computed",    # "insurance_policy"
            "account": "certificates_of_insurance_usergroupinsurance",   # FK user_group_id
            "account_type": "computed",   # always "user_group"
            "type": "computed",      # equipment_liability | general_liability | umbrella_liability
            "status": "certificates_of_insurance_usergroupinsurance",
            "effective_at": "certificates_of_insurance_usergroupinsurance",   # as unix timestamp
            "expires_at": "certificates_of_insurance_usergroupinsurance",     # as unix timestamp
            "insurance_provider": "certificates_of_insurance_usergroupinsurance",
            "policy_number": "certificates_of_insurance_usergroupinsurance",
            "is_valid": "computed",
            "invalid_reasons": "computed",
            "deactivated_at": "certificates_of_insurance_usergroupinsurance",
            "deactivation_reason": "certificates_of_insurance_usergroupinsurance",
            "coverage": "computed",   # dict of policy-type-specific limits/flags
            "document": {
                "file_url": "certificates_of_insurance_usergroupinsurance",
                "ocr_status": "certificates_of_insurance_usergroupinsurance"
            },
            "created": "certificates_of_insurance_usergroupinsurance"  # unix timestamp
        }
    ]
}
```

Note: Polymorphic model — actual tables are `certificates_of_insurance_usergroupinsurancegeneralliability`, `certificates_of_insurance_usergroupinsuranceequipmentliability`, `certificates_of_insurance_usergroupinsuranceumbrellaliability`.

---

## api_v1_payment_methods_list
`GET /api/v1/payment-methods/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "payment_methods_paymentmethod",
            "user": "payment_methods_paymentmethod",
            "user_group": "payment_methods_paymentmethod",
            "type": "payment_methods_paymentmethod",
            "metadata": "payment_methods_paymentmethod",
            "data": "payment_methods_paymentmethod",
            "active": "computed",
            "reason": "computed",
            "card": {
                "number": "computed",       # masked from data['last4']
                "name": "computed",
                "brand": "computed",
                "expiration_month": "computed",
                "expiration_year": "computed"
            }
        }
    ]
}
```

---

## api_v1_setup_intents_list
`GET /api/v1/setup-intents/`

All fields come directly from Stripe API — none stored in local DB.

```python
{
    # all Stripe SetupIntent fields (id, object, client_secret, status, etc.)
    "ephemeral_key": "computed",    # generated via stripe.EphemeralKey.create()
    "publishable_key": "computed"   # from settings.STRIPE_PUBLISHABLE_KEY
}
```

---

## api_v1_stripe_payment_methods_list
`GET /api/v1/stripe/payment-methods/`

Returns raw array (no pagination wrapper) from Stripe API. All fields are Stripe-native — none stored locally.

```python
[
    {
        # all Stripe PaymentMethod fields (id, object, card, billing_details, etc.)
        "metadata": "computed"  # may contain local payment_method_id pointer
    }
]
```

---

## api_v1_seller_products_list
`GET /api/v1/seller-products/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_sellerproduct",
            "created_on": "api_sellerproduct",
            "updated_on": "api_sellerproduct",
            "is_deleted": "api_sellerproduct",
            "created_by": "api_sellerproduct",
            "updated_by": "api_sellerproduct",
            "seller": "api_sellerproduct",   # FK ID by default
            "product": "api_sellerproduct",  # FK ID by default
            "active": "api_sellerproduct"
        }
    ]
}
```

---

## api_v1_seller_product_seller_locations_list
`GET /api/v1/seller-product-seller-locations/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_sellerproductsellerlocation",
            "created_on": "api_sellerproductsellerlocation",
            "updated_on": "api_sellerproductsellerlocation",
            "is_deleted": "api_sellerproductsellerlocation",
            "created_by": "api_sellerproductsellerlocation",
            "updated_by": "api_sellerproductsellerlocation",
            "seller_product": "api_sellerproductsellerlocation",  # FK ID by default
            "seller_location": "api_sellerproductsellerlocation", # FK ID by default
            "quote": "api_sellerproductsellerlocation",
            "active": "api_sellerproductsellerlocation",
            "needs_approval": "api_sellerproductsellerlocation",
            "total_inventory": "api_sellerproductsellerlocation",
            "min_price": "api_sellerproductsellerlocation",
            "max_price": "api_sellerproductsellerlocation",
            "service_radius": "api_sellerproductsellerlocation",
            "service_area_polygon": "api_sellerproductsellerlocation",
            "delivery_fee": "api_sellerproductsellerlocation",
            "removal_fee": "api_sellerproductsellerlocation",
            "fuel_environmental_markup": "api_sellerproductsellerlocation",
            "allows_pick_up": "api_sellerproductsellerlocation",
            "winterization_fee": "api_sellerproductsellerlocation",
            "is_complete": "computed",
            "service": {
                "id": "api_sellerproductsellerlocationservice",
                "seller_product_seller_location": "api_sellerproductsellerlocationservice",
                "price_per_mile": "api_sellerproductsellerlocationservice",
                "flat_rate_price": "api_sellerproductsellerlocationservice",
                "created_on": "api_sellerproductsellerlocationservice",
                "updated_on": "api_sellerproductsellerlocationservice",
                "is_deleted": "api_sellerproductsellerlocationservice",
                "created_by": "api_sellerproductsellerlocationservice",
                "updated_by": "api_sellerproductsellerlocationservice"
            },
            "material": {
                "id": "api_sellerproductsellerlocationmaterial",
                "seller_product_seller_location": "api_sellerproductsellerlocationmaterial",
                "waste_types": [],  # M2M via api_sellerproductsellerlocationmaterialwastetype
                "created_on": "api_sellerproductsellerlocationmaterial",
                "updated_on": "api_sellerproductsellerlocationmaterial",
                "is_deleted": "api_sellerproductsellerlocationmaterial",
                "created_by": "api_sellerproductsellerlocationmaterial",
                "updated_by": "api_sellerproductsellerlocationmaterial"
            },
            "rental_one_step": {
                "id": "api_sellerproductsellerlocationrentalonestep",
                "seller_product_seller_location": "api_sellerproductsellerlocationrentalonestep",
                "rate": "api_sellerproductsellerlocationrentalonestep",
                "created_on": "api_sellerproductsellerlocationrentalonestep",
                "updated_on": "api_sellerproductsellerlocationrentalonestep",
                "is_deleted": "api_sellerproductsellerlocationrentalonestep",
                "created_by": "api_sellerproductsellerlocationrentalonestep",
                "updated_by": "api_sellerproductsellerlocationrentalonestep"
            },
            "rental": {
                "id": "api_sellerproductsellerlocationrental",
                "seller_product_seller_location": "api_sellerproductsellerlocationrental",
                "included_days": "api_sellerproductsellerlocationrental",
                "price_per_day_included": "api_sellerproductsellerlocationrental",
                "price_per_day_additional": "api_sellerproductsellerlocationrental",
                "created_on": "api_sellerproductsellerlocationrental",
                "updated_on": "api_sellerproductsellerlocationrental",
                "is_deleted": "api_sellerproductsellerlocationrental",
                "created_by": "api_sellerproductsellerlocationrental",
                "updated_by": "api_sellerproductsellerlocationrental"
            },
            "rental_multi_step": {
                "id": "api_sellerproductsellerlocationrentalmultistep",
                "seller_product_seller_location": "api_sellerproductsellerlocationrentalmultistep",
                "hour": "api_sellerproductsellerlocationrentalmultistep",
                "day": "api_sellerproductsellerlocationrentalmultistep",
                "week": "api_sellerproductsellerlocationrentalmultistep",
                "two_weeks": "api_sellerproductsellerlocationrentalmultistep",
                "month": "api_sellerproductsellerlocationrentalmultistep",
                "created_on": "api_sellerproductsellerlocationrentalmultistep",
                "updated_on": "api_sellerproductsellerlocationrentalmultistep",
                "is_deleted": "api_sellerproductsellerlocationrentalmultistep",
                "created_by": "api_sellerproductsellerlocationrentalmultistep",
                "updated_by": "api_sellerproductsellerlocationrentalmultistep",
            },
            "service_times_per_week": {
                "id": "api_sellerproductsellerlocationservicetimesperweek",
                "seller_product_seller_location": "api_sellerproductsellerlocationservicetimesperweek",
                "one_every_other_week": "api_sellerproductsellerlocationservicetimesperweek",
                "one_time_per_week": "api_sellerproductsellerlocationservicetimesperweek",
                "two_times_per_week": "api_sellerproductsellerlocationservicetimesperweek",
                "three_times_per_week": "api_sellerproductsellerlocationservicetimesperweek",
                "four_times_per_week": "api_sellerproductsellerlocationservicetimesperweek",
                "five_times_per_week": "api_sellerproductsellerlocationservicetimesperweek",
                "created_on": "api_sellerproductsellerlocationservicetimesperweek",
                "updated_on": "api_sellerproductsellerlocationservicetimesperweek",
                "is_deleted": "api_sellerproductsellerlocationservicetimesperweek",
                "created_by": "api_sellerproductsellerlocationservicetimesperweek",
                "updated_by": "api_sellerproductsellerlocationservicetimesperweek",
            }
        }
    ]
}
```

---

## api_v1_sellerinvoicepayable_list
`GET /api/v1/sellerinvoicepayable/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_sellerinvoicepayable",
            "created_on": "api_sellerinvoicepayable",
            "updated_on": "api_sellerinvoicepayable",
            "is_deleted": "api_sellerinvoicepayable",
            "created_by": "api_sellerinvoicepayable",
            "updated_by": "api_sellerinvoicepayable",
            "seller_location": "api_sellerinvoicepayable",       # FK ID by default
            "location_mail_item": "api_sellerinvoicepayable",    # FK ID by default
            "user_address": "api_sellerinvoicepayable",          # FK ID by default
            "resolved_by": "api_sellerinvoicepayable",           # FK ID by default
            "parent_invoice": "api_sellerinvoicepayable",        # FK ID by default
            "child_invoices": "computed",                        # reverse relation; [] by default
            "line_items": "computed",                            # reverse relation; [] by default
            "invoice_file": "api_sellerinvoicepayable",
            "supplier_invoice_id": "api_sellerinvoicepayable",
            "invoice_date": "api_sellerinvoicepayable",
            "due_date": "api_sellerinvoicepayable",
            "amount": "api_sellerinvoicepayable",
            "status": "api_sellerinvoicepayable",
            "account_number": "api_sellerinvoicepayable",
            "ocr_status": "api_sellerinvoicepayable",
            "parsed_data": "api_sellerinvoicepayable",
            "service_address_raw": "api_sellerinvoicepayable",
            "vendor_address_raw": "api_sellerinvoicepayable",
            "fuel_fee": "api_sellerinvoicepayable",
            "env_fee": "api_sellerinvoicepayable",
            "tax_amount": "api_sellerinvoicepayable",
            "matched_user_address_confidence": "api_sellerinvoicepayable",
            "variance_total": "api_sellerinvoicepayable",
            "resolution_notes": "api_sellerinvoicepayable",
            "resolved_at": "api_sellerinvoicepayable",
            "ingestion_source": "api_sellerinvoicepayable"
        }
    ]
}
```

---

## api_v1_main_product_categories_list
`GET /api/v1/main-product-categories/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_mainproductcategory",
            "created_on": "api_mainproductcategory",
            "updated_on": "api_mainproductcategory",
            "is_deleted": "api_mainproductcategory",
            "created_by": "api_mainproductcategory",
            "updated_by": "api_mainproductcategory",
            "name": "api_mainproductcategory",
            "description": "api_mainproductcategory",
            "image": "api_mainproductcategory",
            "icon": "api_mainproductcategory",
            "popularity": "api_mainproductcategory",
            "slug": "api_mainproductcategory",
            "sort": "api_mainproductcategory",
            "main_product_category_code": "api_mainproductcategory",
            "group": "api_mainproductcategory",   # FK ID
            "industry": "api_mainproductcategory",  # M2M IDs
            "main_product_category_infos": [
                {
                    "id": "api_mainproductcategoryinfo",
                    "name": "api_mainproductcategoryinfo",
                    "sort": "api_mainproductcategoryinfo",
                    "main_product_category": "api_mainproductcategoryinfo",
                    "created_on": "api_mainproductcategoryinfo",
                    "updated_on": "api_mainproductcategoryinfo",
                    "is_deleted": "api_mainproductcategoryinfo",
                    "created_by": "api_mainproductcategoryinfo",
                    "updated_by": "api_mainproductcategoryinfo"
                }
            ]
        }
    ]
}
```

---

## api_v1_main_product_category_groups_list
`GET /api/v1/main-product-category-groups/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_mainproductcategorygroup",
            "created_on": "api_mainproductcategorygroup",
            "updated_on": "api_mainproductcategorygroup",
            "is_deleted": "api_mainproductcategorygroup",
            "created_by": "api_mainproductcategorygroup",
            "updated_by": "api_mainproductcategorygroup",
            "name": "api_mainproductcategorygroup",
            "sort": "api_mainproductcategorygroup",
            "icon": "api_mainproductcategorygroup",
            "slug": "api_mainproductcategorygroup",
            "main_product_categories": [
                # full nested MainProductCategorySerializer objects (not just IDs)
                # same structure as api_v1_main_product_categories_list data items
            ]
        }
    ]
}
```

---

## api_v1_advertisements_list
`GET /api/v1/advertisements/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_advertisement",
            "text": "api_advertisement",
            "image": "api_advertisement",
            "background_color": "api_advertisement",
            "text_color": "api_advertisement",
            "object_type": "api_advertisement",
            "sort": "api_advertisement",
            "start_date": "api_advertisement",
            "end_date": "api_advertisement",
            "object_id": "computed",  # from linked_object.id
            "is_active": "computed"   # derived from is_active + dates
        }
    ]
}
```

---

## api_v1_day_of_weeks_list
`GET /api/v1/day-of-weeks/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_dayofweek",
            "created_on": "api_dayofweek",
            "updated_on": "api_dayofweek",
            "is_deleted": "api_dayofweek",
            "created_by": "api_dayofweek",
            "updated_by": "api_dayofweek",
            "name": "api_dayofweek",
            "number": "api_dayofweek"
        }
    ]
}
```

---

## api_v1_time_slots_list
`GET /api/v1/time-slots/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_timeslot",
            "created_on": "api_timeslot",
            "updated_on": "api_timeslot",
            "is_deleted": "api_timeslot",
            "created_by": "api_timeslot",
            "updated_by": "api_timeslot",
            "name": "api_timeslot",
            "start": "api_timeslot",
            "end": "api_timeslot"
        }
    ]
}
```

---

## api_v1_rbac_role_templates_list
`GET /api/v1/rbac/role-templates/`

All fields are computed from hardcoded constants (not DB):

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "key": "computed",
            "name": "computed",
            "description": "computed",
            "display_order": "computed",
            "scope_keys": "computed"
        }
    ]
}
```

Note: Requires non-staff user context — not accessible with staff API key.

---

## api_v1_rbac_roles_list
`GET /api/v1/rbac/roles/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "rbac_rbacrole",
            "key": "rbac_rbacrole",
            "name": "rbac_rbacrole",
            "scope_options": [
                {
                    "id": "rbac_rbacscope",
                    "key": "rbac_rbacscope",
                    "granted": "computed"  # derived from rbac_rbacrole_scopes join
                }
            ]
        }
    ]
}
```

Note: Requires non-staff user context.

---

## api_v1_rbac_scopes_list
`GET /api/v1/rbac/scopes/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "rbac_rbacscope",
            "key": "rbac_rbacscope"
        }
    ]
}
```

Note: Requires non-staff user context.

---

## api_v1_user_address_types_list
`GET /api/v1/user-address-types/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_useraddresstype",
            "created_on": "api_useraddresstype",
            "updated_on": "api_useraddresstype",
            "is_deleted": "api_useraddresstype",
            "created_by": "api_useraddresstype",
            "updated_by": "api_useraddresstype",
            "name": "api_useraddresstype",
            "sort": "api_useraddresstype"
        }
    ]
}
```

---

## api_v1_order_group_attachments_list
`GET /api/v1/order-group-attachments/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_ordergroupattachment",
            "order_group": "api_ordergroupattachment",
            "file_name": "computed",   # derived from file.name
            "file_type": "computed"    # derived from file extension
            # file field is write-only, not returned
        }
    ]
}
```

---

## api_v1_mobile_widget_list
`GET /api/v1/mobile-widget/`

All fields are computed aggregates — no direct DB columns in response.

```python
{
    "cart_count": "computed",       # count of orders where submitted_on IS NULL
    "active_bookings": "computed",  # count of order_groups with end_date > now
    "past_due_invoices": "computed",# count of invoices status=OPEN, due_date < now
    "last_order": {
        "id": "api_mainproduct",
        "name": "api_mainproduct"
    }
}
```

---

## api_v1_orders_for_seller_list
`GET /api/v1/orders-for-seller/`

Same serializer as `api_v1_orders_list` but scoped to seller context.

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "api_order",
            "created_on": "api_order",
            "updated_on": "api_order",
            "created_by": "api_order",
            "code": "api_order",
            "start_date": "api_order",
            "end_date": "api_order",
            "submitted_on": "api_order",
            "accepted_on": "api_order",
            "completed_on": "api_order",
            "status": "api_order",
            "schedule_window": "api_order",
            "sent_auto_renewal_message": "api_order",
            "disposal_location": {
                "id": "api_disposallocation",
                "name": "api_disposallocation",
                "street": "api_disposallocation",
                "city": "api_disposallocation",
                "state": "api_disposallocation",
                "postal_code": "api_disposallocation",
                "country": "api_disposallocation",
                "latitude": "api_disposallocation",
                "longitude": "api_disposallocation",
                "created_on": "api_disposallocation",
                "updated_on": "api_disposallocation",
                "is_deleted": "api_disposallocation",
                "created_by": "api_disposallocation",
                "updated_by": "api_disposallocation",
            },
            "order_group": "api_order",
            "main_product": "computed",  # via order_group → spsl → seller_product → product → main_product
            "seller": "computed",        # via order_group → spsl → seller_product → seller
            "account_owner": "api_order",
            "submitted_by": "api_order",
            "order_type": "computed",
            "price": "computed"
        }
    ]
}
```

---

## api_v1_payouts_metrics_list
`GET /api/v1/payouts/metrics/`

All fields are computed aggregates.

```python
{
    "total": {
        "count": "computed",
        "amount": "computed"
    },
    "pending": {
        "count": "computed",
        "amount": "computed"
    },
    "this_week": {
        "count": "computed",
        "amount": "computed"
    }
}
```

---

## api_v1_seller_dashboard_metrics_list
`GET /api/v1/seller-dashboard/metrics/`

Requires `start_date` and `end_date` params. All fields are computed aggregates.

```python
{
    "total_sales_amount": "computed",
    "order_count": "computed",
    "average_order_amount": "computed",
    "daily_average_sales": "computed",
    "sales_by_location": [
        {
            "id": "api_sellerlocation",
            "name": "api_sellerlocation",
            "total_sales": "computed",
            "percentage": "computed"
        }
    ],
    "sales_by_main_product": [
        {
            "id": "api_mainproduct",
            "name": "api_mainproduct",
            "total_sales": "computed",
            "percentage": "computed"
        }
    ]
}
```

---

## api_v1_invoices_metrics_list
`GET /api/v1/invoices/metrics/`

All fields are computed aggregates.

```python
{
    "past_due": "computed",    # sum of amount_remaining where status=OPEN, due_date < today
    "outstanding": "computed", # sum of amount_remaining where status=OPEN, due_date >= today
    "paid": "computed"         # sum of amount_paid where status=PAID
}
```

---

## api_v1_orders_internal_sales_data_list
`GET /api/v1/orders/internal/sales-data/`

Restricted to sales users/managers. All fields are computed aggregates.

```python
{
    "month": "computed",
    "user": {
        "month_to_date": {
            "in_cart": "computed",
            "scheduled": "computed",
            "commission_eligible": "computed"
        }
    },
    "company": {
        "month_to_date": {
            "in_cart": "computed",
            "scheduled": "computed",
            "invoiced": "computed",
            "commission_eligible": "computed"
        }
    }
}
```

---

## api_v1_financial_connection_list
`GET /api/v1/financial-connection/`

All fields from Stripe API — none stored locally.

```python
{
    # all Stripe financial_connections.session fields
    "ephemeral_key": "computed",
    "publishable_key": "computed"
}
```

---

## api_v1_identity_verification_list
`GET /api/v1/identity-verification/`

All fields from Stripe API — none stored locally.

```python
{
    # all Stripe identity.verification_session fields
    "metadata": {
        "user_id": "api_user"  # injected from request.user
    },
    "ephemeral_key": "computed",
    "publishable_key": "computed"
}
```

---

## api_v1_user_group_admin_approval_user_invite_list
`GET /api/v1/user-group-admin-approval-user-invite/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "admin_approvals_usergroupadminapprovaluserinvite",
            "created_on": "admin_approvals_usergroupadminapprovaluserinvite",
            "updated_on": "admin_approvals_usergroupadminapprovaluserinvite",
            "is_deleted": "admin_approvals_usergroupadminapprovaluserinvite",
            "created_by": "admin_approvals_usergroupadminapprovaluserinvite",
            "updated_by": "admin_approvals_usergroupadminapprovaluserinvite",
            "email": "admin_approvals_usergroupadminapprovaluserinvite",
            "phone": "admin_approvals_usergroupadminapprovaluserinvite",
            "type": "admin_approvals_usergroupadminapprovaluserinvite",
            "first_name": "admin_approvals_usergroupadminapprovaluserinvite",
            "last_name": "admin_approvals_usergroupadminapprovaluserinvite",
            "redirect_url": "admin_approvals_usergroupadminapprovaluserinvite",
            "status": "admin_approvals_usergroupadminapprovaluserinvite",
            "user_group": "admin_approvals_usergroupadminapprovaluserinvite",
            "role": "admin_approvals_usergroupadminapprovaluserinvite",
            "user": {
                "id": "api_user",
                "user_id": "computed",
                "phone": "api_user",
                "email": "api_user",
                "push_id": "api_user",
                "date_joined": "api_user",
                "first_name": "api_user",
                "last_name": "api_user",
                "username": "api_user",
                "photo_url": "api_user",
                "photo": "api_user",
                "identity_verified": "api_user",
                "is_onboarded": "api_user",
                "is_staff": "api_user",
                "is_superuser": "api_user",
                "is_admin": "api_user",
                "is_archived": "api_user",
                "is_active": "api_user",
                "source": "api_user",
                "terms_accepted": "api_user",
                "type": "api_user",
                "last_active": "api_user",
                "last_login": "api_user",
                "timezone": "api_user",
                "send_new_invoice_emails": "api_user",
                "redirect_url": "api_user",
                "user_group": "api_user",   # FK ID by default
                "role": "api_user",
            }
        }
    ]
}
```

---

## api_v1_public_location_pages_list
`GET /api/v1/public/location-pages/`

All fields are computed — built from a seed data JSON file + seller coverage queries.

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "location": "computed",        # from seed records JSON file
            "coverage": "computed",        # from seller_location + spsl counts
            "seo": "computed",             # hardcoded templates
            "content": "computed",         # hardcoded content
            "internalLinks": "computed",   # from nearby seed records
            "meta": "computed"
        }
    ]
}
```

---

## api_v1_knowledge_search_list
`POST /api/v1/knowledge/search/`

Note: Documented as GET in catalog but implemented as POST. All fields are computed — vector search over `knowledge_documentchunk`.

```python
{
    "object": "computed",
    "has_more": "computed",
    "data": [
        {
            "id": "computed",              # encoded as kdoc_*
            "object": "computed",          # "knowledge_document"
            "document_id": "knowledge_documentchunk",
            "slug": "knowledge_documentchunk",
            "heading": "computed",         # from metadata JSON
            "score": "computed",           # vector similarity score
            "excerpt": "computed",         # normalized content
            "metadata": "knowledge_documentchunk"
        }
    ],
    "meta": {
        "query": "computed",
        "visibility": "computed",
        "retrieval": "computed"
    }
}
```

---

## api_insight_hub_account_classification_list
`GET /api/insight-hub/account-classification/`

Note: Uses `InsightHubApiKeyAuthentication`. All fields are computed analytics aggregated at runtime.

```python
{
    "summary": {
        "net_new_gmv": "computed",
        "expansion_gmv": "computed",
        "backlog_gmv": "computed",
        "total_gmv": "computed",
        "net_new_accounts": "computed",
        "expansion_accounts": "computed",
        "backlog_orders": "computed",
    },
    "monthly_trend": [{"month": "computed", "gmv": "computed"}],
}
```

---

## api_insight_hub_account_growth_list
`GET /api/insight-hub/account-growth/`

```python
{
    "summary": {
        "net_new": "computed",
        "churned": "computed",
        "retained": "computed",
        "net_growth": "computed",
    },
    "net_new_accounts": [{"id": "api_usergroup", "name": "api_usergroup", "first_order_date": "computed"}],
    "churned_accounts": [{"id": "api_usergroup", "name": "api_usergroup", "last_order_date": "computed"}],
    "monthly_trend": [{"month": "computed", "net_new": "computed"}],
}
```

---

## api_insight_hub_commissions_list
`GET /api/insight-hub/commissions/`

```python
{
    "commission_rate_percent": "computed",
    "summary": {
        "total_commission_eligible": "computed",
        "total_commission": "computed",
        "total_in_cart": "computed",
        "total_scheduled": "computed",
    },
    "reps": [
        {
            "rep_id": "api_user",
            "rep_name": "computed",
            "commission_eligible": "computed",
            "commission": "computed",
            "in_cart": "computed",
            "scheduled": "computed",
        }
    ],
    "monthly_trend": [{"month": "computed", "total": "computed"}],
}
```

---

## api_insight_hub_customer_spend_mom_list
`GET /api/insight-hub/customer-spend-mom/`

```python
{
    "customers": [
        {
            "user_group_id": "api_usergroup",
            "user_group_name": "api_usergroup",
            "month": "computed",
            "spend": "computed",
        }
    ],
    "monthly_totals": [{"month": "computed", "total_spend": "computed"}],
}
```

---

## api_insight_hub_first_touch_to_order_list
`GET /api/insight-hub/first-touch-to-order/`

```python
{
    "average_days": "computed",
    "total_conversions": "computed",
    "details": [
        {
            "cart_id": "computed",
            "user_group_name": "api_usergroup",
            "days_to_order": "computed",
        }
    ],
}
```

---

## api_insight_hub_gmv_by_state_list
`GET /api/insight-hub/gmv-by-state/`

```python
{
    "states": [{"state": "api_useraddress", "gmv": "computed", "order_count": "computed"}],
}
```

---

## api_insight_hub_gmv_mom_list
`GET /api/insight-hub/gmv-mom/`

```python
{
    "months": [
        {
            "month": "computed",
            "gmv": "computed",
            "supplier_cost": "computed",
            "net_revenue": "computed",
            "take_rate_percent": "computed",
            "aov": "computed",
            "order_count": "computed",
        }
    ],
}
```

---

## api_insight_hub_product_mix_list
`GET /api/insight-hub/product-mix/`

```python
{
    "categories": [{"category": "api_mainproductcategory", "order_count": "computed", "percent": "computed"}],
    "total_orders": "computed",
}
```

---

## api_insight_hub_quota_vs_actual_list
`GET /api/insight-hub/quota-vs-actual/`

```python
{
    "rows": [
        {
            "rep_id": "api_user",
            "rep_name": "computed",
            "month": "computed",
            "gmv_target": "api_salesquota",
            "gmv_actual": "computed",
            "attainment_percent": "computed",
            "new_accounts_target": "api_salesquota",
            "new_accounts_actual": "computed",
            "orders_target": "api_salesquota",
            "orders_actual": "computed",
        }
    ],
}
```

---

## api_insight_hub_quotas_list
`GET /api/insight-hub/quotas/`

```python
{
    "data": [
        {
            "id": "api_salesquota",
            "rep_id": "api_salesquota",
            "month": "api_salesquota",
            "gmv_target": "api_salesquota",
            "new_accounts_target": "api_salesquota",
            "orders_target": "api_salesquota",
        }
    ],
}
```

---

## api_insight_hub_sales_funnel_list
`GET /api/insight-hub/sales-funnel/`

```python
{
    "stages": [{"stage": "computed", "count": "computed", "gmv": "computed"}],
    "conversion_rates": {
        "cart_to_quote": "computed",
        "quote_to_close": "computed",
        "overall": "computed",
    },
}
```

---

## api_insight_hub_spend_by_product_list
`GET /api/insight-hub/spend-by-product/`

```python
{
    "products": [
        {
            "main_product_name": "api_mainproduct",
            "gmv": "computed",
            "order_count": "computed",
            "aov": "computed",
        }
    ],
}
```

---

## api_insight_hub_spend_by_supplier_list
`GET /api/insight-hub/spend-by-supplier/`

```python
{
    "suppliers": [{"seller_id": "api_seller", "seller_name": "api_seller", "gmv": "computed"}],
}
```

---

## api_insight_hub_take_rate_mom_list
`GET /api/insight-hub/take-rate-mom/`

```python
{
    "rows": [
        {
            "rep_id": "api_user",
            "rep_name": "computed",
            "month": "computed",
            "customer_total": "computed",
            "seller_total": "computed",
            "net_revenue": "computed",
            "take_rate_percent": "computed",
        }
    ],
}
```

---

## api_v1_admin_communications_list
`GET /api/v1/admin/communications/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "communications_communication",
            "object": "computed",   # hardcoded "communication"
            "channel": "communications_communication",
            "direction": "communications_communication",
            "source": "communications_communication",
            "summary": "communications_communication",
            "occurred_at": "communications_communication",
            "from_user": "communications_communication",
            "to_user": "communications_communication",
            "from_value": "communications_communication",
            "to_value": "communications_communication",
            "content": "computed"   # branches by channel:
            # EMAIL: {subject, body_text, internet_message_id, in_reply_to} from communications_emailcommunication
            # SMS:   {message, provider} from communications_smscommunication
            # CALL:  {duration_seconds, recording_url, disposition, transcript_text} from communications_callcommunication
        }
    ]
}
```

---

## api_v1_admin_sales_target_vs_actuals_list
`GET /api/v1/admin/sales/target-vs-actuals/`

No pagination — single response object. All fields are computed aggregates.

```python
{
    "period": {
        "month": "computed", "as_of": "computed",
        "current_month_start": "computed", "current_month_end": "computed",
        "previous_month_start": "computed", "previous_month_end": "computed",
        "days_elapsed": "computed"
    },
    "gmv": {
        "target": "computed",                       # from pricing_engine tables
        "actual_mtd": "computed",                   # from api_order
        "booked_month_total": "computed",
        "future_booked_this_month": "computed",
        "previous_month_mtd_aligned": "computed",
        "delta_vs_previous_month_mtd": "computed",
        "delta_vs_previous_month_mtd_percent": "computed",
        "expected_to_date": "computed",
        "attainment_percent": "computed",
        "projected_month_end": "computed",
        "on_track": "computed"
    },
    "daily_progress": {
        "actual_complete_cumulative": [{"date": "computed", "day_of_month": "computed", "cumulative_gmv": "computed", "point_phase": "computed"}],
        "booked_total_cumulative": "computed",
        "expected_pace_cumulative": "computed",
        "previous_month_cumulative_aligned": "computed"
    },
    "definitions": "computed"
}
```

---

## api_v1_admin_transactional_emails_list
`GET /api/v1/admin/transactional-emails/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "notifications_emailnotification",
            "object": "computed",   # hardcoded "transactional_email"
            "subject": "notifications_emailnotification",
            "from_email": "notifications_emailnotification",
            "reply_to": "notifications_emailnotification",
            "sent_at": "notifications_emailnotification",
            "to_emails": "computed"  # array from notifications_emailnotificationto.email
        }
    ]
}
```

---

## api_v1_admin_user_groups_goal_progress_aggregate_list
`GET /api/v1/admin/user-groups/goal-progress/aggregate/`

No pagination — single response object. All fields computed.

```python
{
    "period": {"as_of": "computed", "current_month_start": "computed", "previous_month_start": "computed"},
    "gmv": {"goal": "computed", "current": "computed", "previous_month": "computed", "gap": "computed", "attainment_percent": "computed"},
    "users": {"goal": "computed", "current": "computed", "gap": "computed", "attainment_percent": "computed"},
    "job_site_starts": {"goal": "computed", "current": "computed", "gap": "computed", "attainment_percent": "computed"},
    "project_start_funnel": {
        "target_monthly_project_starts": "computed",
        "expected_to_date": "computed",
        "addresses_starting_this_month": "computed",
        "due_by_now": "computed",
        "later_this_month": "computed",
        "due_by_now_with_populated_cart": "computed",
        "due_by_now_with_checked_out_cart": "computed",
        "due_by_now_added_to_cart_pct": "computed",
        "due_by_now_cart_to_checkout_pct": "computed",
        "due_by_now_added_to_checkout_pct": "computed"
    }
}
```

---

## checkout_v1_list
`GET /checkout/v1/`

Raw array (no pagination wrapper — `JsonResponse(..., safe=False)`).

```python
[
    {
        "id": "cart_cart",
        "code": "cart_cart",
        "user_address": "cart_cart",    # FK ID
        "payment_method": "cart_cart",  # FK ID
        "pay_later": "cart_cart",
        "orders": [
            # full OrderSerializer — same structure as api_v1_orders_list data item
        ],
        "price": "computed",            # {customer_price, seller_price, estimated_taxes, total, take_rate, order_count}
    }
]
```

---

## checkout_v1_cart_list
`GET /checkout/v1/cart/`

All fields computed from Cart + Order aggregation.

```python
{
    "cart": [
        {
            "address": {
                # full UserAddressSerializer — same structure as api_v1_user_addresses_list data item
            },
            "items": [
                {
                    "main_product": {
                        "id": "api_mainproduct",
                        "name": "api_mainproduct",
                        "image": "computed",
                        "product_type": "api_mainproduct",
                        "can_bundle_freight": "api_mainproduct",
                    },
                    "order": {
                        # CartItemOrderSerializer: exclude = ("zoho_sales_order_id", "zoho_desk_ticket_id")
                        # BaseModel fields
                        "id": "api_order",
                        "created_on": "api_order",
                        "updated_on": "api_order",
                        "is_deleted": "api_order",
                        "updated_by": "api_order",
                        # Declared serializer fields (override model defaults)
                        "created_by": {
                            "id": "api_user",
                            "first_name": "api_user",
                            "last_name": "api_user",
                            "email": "api_user",
                        },
                        "service_date": "computed",         # SerializerMethodField → obj.end_date
                        "order_type": "computed",
                        "price": "computed",
                        "estimated_end_date": "api_ordergroup",
                        "seller_location": {
                            "id": "api_sellerlocation",
                            "name": "api_sellerlocation",
                            "street": "api_sellerlocation",
                            "city": "api_sellerlocation",
                            "state": "api_sellerlocation",
                            "postal_code": "api_sellerlocation",
                        },
                        "bundle": {
                            "id": "api_freightbundle",
                            "name": "api_freightbundle",
                            "delivery_fee": "api_freightbundle",
                            "removal_fee": "api_freightbundle",
                            "created_on": "api_freightbundle",
                            "updated_on": "api_freightbundle",
                            "is_deleted": "api_freightbundle",
                            "created_by": "api_freightbundle",
                            "updated_by": "api_freightbundle",
                        },
                        # Order model fields (from exclude approach)
                        "code": "api_order",
                        "order_group": "api_order",         # FK
                        "account_owner": "api_order",       # FK
                        "disposal_location": "api_order",   # FK
                        "start_date": "api_order",
                        "end_date": "api_order",
                        "submitted_on": "api_order",
                        "submitted_by": "api_order",        # FK
                        "accepted_on": "api_order",
                        "accepted_by": "api_order",         # FK
                        "completed_on": "api_order",
                        "completed_by": "api_order",        # FK
                        "schedule_details": "api_order",
                        "status": "api_order",
                        "intercom_id": "api_order",
                        "custmer_intercom_id": "api_order",
                        "billing_comments_internal_use": "api_order",
                        "schedule_window": "api_order",
                        "cart": "api_order",                # FK
                        "sent_auto_renewal_message": "api_order",
                    },
                    "subtotal": "computed",
                    "tax": "computed",
                    "total": "computed",
                }
            ],
            "customer_price": "computed",
            "total": "computed",
            "count": "computed",
            "show_quote": "computed"
        }
    ],
    "subtotal": "computed",
    "cart_count": "computed"
}
```

---

## checkout_v1_cart_count_list
`GET /checkout/v1/cart/count/`

```python
{
    "cart_count": "computed"   # count of orders where submitted_on IS NULL
}
```

---

## checkout_v1_carts_list
`GET /checkout/v1/carts/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "cart_cart",
            "code": "cart_cart",
            "created_on": "cart_cart",
            "updated_on": "cart_cart",
            "payment_method": "cart_cart",
            "pay_later": "cart_cart",
            "to_emails": "cart_cart",
            "quote_expiration": "cart_cart",
            "quote_accepted_at": "cart_cart",
            "submitted_on": "cart_cart",
            "lost_on": "cart_cart",
            "lost_reason": "cart_cart",
            "first_touch_email_id": "cart_cart",
            "first_touch_open_count": "cart_cart",
            "first_touch_click_count": "cart_cart",
            "orders": [
                # full OrderSerializer — same structure as api_v1_orders_list data item
            ],
            "user_address": {
                # full UserAddressSerializer — same structure as api_v1_user_addresses_list data item
            }
        }
    ]
}
```

---

## checkout_v1_quote_get
`GET /checkout/v1/quote/{cart_id}/`

All fields computed from Cart + Order + User + UserGroup data.

```python
{
    "quote_expiration": "computed",
    "quote_id": "computed",
    "user_address_id": "computed",
    "project_id": "computed",
    "full_name": "computed",
    "phone": "computed",
    "email": "computed",
    "company_name": "computed",
    "location_name": "computed",
    "delivery_address": "computed",
    "billing_address": "computed",
    "billing_email": "computed",
    "one_step": "computed",
    "two_step": "computed",
    "multi_step": "computed",
    "site_services_groups": "computed",
    "total": "computed",
    "seller_total": "computed",
    "estimated_total": "computed",
    "estimated_taxes": "computed",
    "payment_due_label": "computed",
    "payment_due_date": "computed",
    "contact": "computed",
    "signed_by": "computed",
    "signed_on": "computed"
}
```

---

## explore_v1_search_list
`GET /explore/v1/search/`

```python
{
    "main_products": [
        # same structure as api_v1_main_products_list data items
    ],
    "main_product_categories": [
        # same structure as api_v1_main_product_categories_list data items
    ],
    "main_product_category_groups": [
        {
            "id": "api_mainproductcategorygroup",
            "name": "api_mainproductcategorygroup",
            "icon": "api_mainproductcategorygroup",
            "sort": "api_mainproductcategorygroup"
        }
    ]
}
```

---

## explore_v1_main_product_match_list
`POST /explore/v1/main-product/match/`

Note: Implemented as POST (not GET).

```python
{
    "id": "api_product",
    "main_product": "api_product",
    "product_code": "api_product",
    "description": "api_product",
    "removal_price": "api_product",
    "popularity": "api_product",
    "created_on": "api_product",
    "updated_on": "api_product",
    "is_deleted": "api_product",
    "created_by": "api_product",
    "updated_by": "api_product",
    "product_add_on_choices": [
        {
            "id": "api_productaddonchoice",
            "product": "api_productaddonchoice",
            "name": "api_productaddonchoice",
            "created_on": "api_productaddonchoice",
            "updated_on": "api_productaddonchoice",
            "is_deleted": "api_productaddonchoice",
            "created_by": "api_productaddonchoice",
            "updated_by": "api_productaddonchoice",
            "add_on_choice": {
                "id": "api_addonchoice",
                "add_on": "api_addonchoice",
                "name": "api_addonchoice"
            }
        }
    ]
}
```

---

## financial_accounts_v1_financial_connection_account_list
`GET /financial-accounts/v1/financial-connection-account/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "financial_accounts_financialconnectionaccount",
            "created_on": "financial_accounts_financialconnectionaccount",
            "updated_on": "financial_accounts_financialconnectionaccount",
            "user": "financial_accounts_financialconnectionaccount",
            "user_group": "financial_accounts_financialconnectionaccount",
            # stripe_id is write_only — not returned in GET responses
            "display_name": "financial_accounts_financialconnectionaccount",
            "institution_name": "financial_accounts_financialconnectionaccount",
            "last4": "financial_accounts_financialconnectionaccount",
            "category": "financial_accounts_financialconnectionaccount",
            "subcategory": "financial_accounts_financialconnectionaccount",
            "status": "financial_accounts_financialconnectionaccount",
            "balance": "financial_accounts_financialconnectionaccount",
            "currency": "financial_accounts_financialconnectionaccount",
            "balance_last_updated": "financial_accounts_financialconnectionaccount",
            "transactions_last_updated": "financial_accounts_financialconnectionaccount"
        }
    ]
}
```

---

## financial_accounts_v1_financial_statement_list
`GET /financial-accounts/v1/financial-statement/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "financial_accounts_financialstatement",
            "created_on": "financial_accounts_financialstatement",
            "updated_on": "financial_accounts_financialstatement",
            "user": "financial_accounts_financialstatement",
            "user_group": "financial_accounts_financialstatement",
            "parsed_data": "financial_accounts_financialstatement"
        }
    ]
}
```

---

## matching_engine_v1_product_match_list
`GET /matching-engine/v1/product-match/`

```python
{
    "id": "api_product",
    "product_code": "api_product",
    "description": "api_product",
    "main_product": "api_product",
    "removal_price": "api_product",
    "popularity": "api_product",
    "created_on": "api_product",
    "updated_on": "api_product",
    "is_deleted": "api_product",
    "created_by": "api_product",
    "updated_by": "api_product",
    "product_add_on_choices": [
        {
            "id": "api_productaddonchoice",
            "name": "api_productaddonchoice",
            "product": "api_productaddonchoice",
            "add_on_choice": {
                "id": "api_addonchoice",
                "add_on": "api_addonchoice",
                "name": "api_addonchoice",
            },
            "created_on": "api_productaddonchoice",
            "updated_on": "api_productaddonchoice",
            "is_deleted": "api_productaddonchoice",
            "created_by": "api_productaddonchoice",
            "updated_by": "api_productaddonchoice",
        }
    ],
}
```

---

## matching_engine_v1_seller_product_seller_locations_by_lat_long_list
`GET /matching-engine/v1/seller-product-seller-locations-by-lat-long/`

Raw array (no pagination wrapper — view hand-builds response with `JsonResponse(..., safe=False)`).

```python
[
    {
        "id": "computed",           # str(spsl.id)
        "distance_miles": "computed",
        "ranking": {
            "tier": "computed",
            "score": "computed",
            "reasons": [
                {
                    "code": "computed",
                    "detail": "computed",
                }
            ],
        },
    }
]
```

---

## notifications_v1_push_notifications_list
`GET /notifications/v1/push-notifications/`

```python
{
    "object": "pagination",
    "url": "pagination",
    "count": "pagination",
    "has_more": "pagination",
    "data": [
        {
            "id": "notifications_pushnotification",
            "created_on": "notifications_pushnotification",
            "updated_on": "notifications_pushnotification",
            "template_id": "notifications_pushnotification",
            "title": "notifications_pushnotification",
            "message": "notifications_pushnotification",
            "image": "notifications_pushnotification",
            "link": "notifications_pushnotification",
            "custom_data": "notifications_pushnotification",
            "sent_at": "notifications_pushnotification",
            "is_deleted": "notifications_pushnotification",
            "created_by": "notifications_pushnotification",
            "updated_by": "notifications_pushnotification",
            "is_read": "computed",  # from notifications_pushnotificationto.is_read
        }
    ]
}
```

---

## pricing_engine_v1_seller_product_seller_location_pricing_list
`GET /pricing-engine/v1/seller-product-seller-location-pricing/`

## pricing_engine_v1_seller_product_seller_location_pricing_by_lat_long_list
`GET /pricing-engine/v1/seller-product-seller-location-pricing-by-lat-long/`

Both endpoints return identical structure — all computed pricing breakdown.

```python
{
    "service": "computed",
    "rental": "computed",
    "material": "computed",
    "delivery": "computed",
    "removal": "computed",
    "winterization": "computed",
    "fuel_and_environmental": "computed",
    "texas_surcharge": "computed",
    "rpp": "computed",
    "adjustments": "computed",
    "ai_macro_adjustment": "computed",
    "total": "computed",
    "tax": "computed",
    "breakdown": "computed"
}
```

---

## pricing_engine_v1_supplier_insights_list
`GET /pricing-engine/v1/supplier-insights/`

**Does not exist** — no ViewSet, serializer, or URL pattern found in TG-API-proxy. This endpoint is defined in mcp_catalog.py but not implemented.

---

## api_v1_industries_get
Single record — same structure as `api_v1_industries_list` data item.

---

## api_v1_waste_types_get
Single record — same structure as `api_v1_waste_types_list` data item.

---

## api_v1_main_products_get
Single record — same structure as `api_v1_main_products_list` data item.

---

## api_v1_main_product_categories_get
Single record — same structure as `api_v1_main_product_categories_list` data item.

---

## api_v1_main_product_category_groups_get
Single record — same structure as `api_v1_main_product_category_groups_list` data item.

---

## api_v1_advertisements_get
Single record — same structure as `api_v1_advertisements_list` data item.

---

## api_v1_day_of_weeks_get
Single record — same structure as `api_v1_day_of_weeks_list` data item.

---

## api_v1_time_slots_get
Single record — same structure as `api_v1_time_slots_list` data item.

---

## api_v1_user_address_types_get
Single record — same structure as `api_v1_user_address_types_list` data item.

---

## api_v1_sellers_get
Single record — same structure as `api_v1_sellers_list` data item.

---

## api_v1_seller_locations_get
Single record — same structure as `api_v1_seller_locations_list` data item.

---

## api_v1_seller_products_get
Single record — same structure as `api_v1_seller_products_list` data item.

---

## api_v1_seller_product_seller_locations_get
Single record — same structure as `api_v1_seller_product_seller_locations_list` data item.

---

## api_v1_sellerinvoicepayable_get
Single record — same structure as `api_v1_sellerinvoicepayable_list` data item.

---

## api_v1_invoices_get
Single record — same structure as `api_v1_invoices_list` data item.

---

## api_v1_orders_get
Single record — same structure as `api_v1_orders_list` data item.

---

## api_v1_orders_for_seller_get
Single record — same structure as `api_v1_orders_for_seller_list` data item.

---

## api_v1_order_groups_get
Single record — same structure as `api_v1_order_groups_list` data item.

---

## api_v1_payment_methods_get
Single record — same structure as `api_v1_payment_methods_list` data item.

---

## api_v1_payouts_get
Single record — same structure as `api_v1_payouts_list` data item.

---

## api_v1_insurance_policies_get
Single record — same structure as `api_v1_insurance_policies_list` data item.

---

## api_v1_user_addresses_get
Single record — same structure as `api_v1_user_addresses_list` data item.

---

## api_v1_user_groups_get
Single record — same structure as `api_v1_user_groups_list` data item.

---

## api_v1_users_get
Single record — same structure as `api_v1_users_list` data item.

---

## api_v1_user_group_admin_approval_user_invite_get
Single record — same structure as `api_v1_user_group_admin_approval_user_invite_list` data item.

---

## financial_accounts_v1_financial_connection_account_get
Single record — same structure as `financial_accounts_v1_financial_connection_account_list` data item.

---

## financial_accounts_v1_financial_statement_get
Single record — same structure as `financial_accounts_v1_financial_statement_list` data item.

---

## notifications_v1_push_notifications_get
Single record — same structure as `notifications_v1_push_notifications_list` data item.

---

## api_v1_public_location_pages_get
Single record — same structure as `api_v1_public_location_pages_list` data item.

---

## api_v1_order_groups_filter_options_list
`GET /api/v1/order-groups/filter-options/`

```python
{
    "supplier": [{"value": "computed", "label": "computed", "count": "computed"}],
    "product_category": [{"value": "computed", "label": "computed", "count": "computed"}]
}
```

---

## api_v1_user_addresses_filter_options_list
`GET /api/v1/user-addresses/filter_options/`

```python
{
    "state": [{"value": "computed", "label": "computed", "count": "computed"}],
    "city": [{"value": "computed", "label": "computed", "count": "computed"}],
    "brand": [{"value": "computed", "label": "computed", "count": "computed"}],
    "product_category": [{"value": "computed", "label": "computed", "count": "computed"}],
    "suppliers": [{"value": "computed", "label": "computed", "count": "computed"}]
}
```

---

## api_v1_user_addresses_recommendations_list
`GET /api/v1/user-addresses/{id}/recommendations/`

```python
{
    "count": "pagination",
    "next": "pagination",
    "previous": "pagination",
    "results": [
        # UserAddressRecommendationSerializer — structure TBD
    ]
}
```

---

## api_v1_order_groups_removal_checkout_list
`GET /api/v1/order-groups/{order_group_id}/removal-checkout/`

## api_v1_order_groups_swap_checkout_list
`GET /api/v1/order-groups/{order_group_id}/swap-checkout/`

Both return a checkout preview — all fields computed from Order + pricing engine.

```python
{
    "order": {
        # same structure as api_v1_orders_list data item
    },
    "pricing": "computed"   # pricing breakdown dict
}
```

---

## api_v1_industries_popular_products_list
`GET /api/v1/industries/{id}/popular-products/`

Returns array (no pagination wrapper) of MainProduct objects — same structure as `api_v1_main_products_list` data items.

```python
[
    # same structure as api_v1_main_products_list data item
]
```

---

## checkout_v1_get
`GET /checkout/v1/{id}/`

Single cart record — same structure as `checkout_v1_list` data item.

---

## checkout_v1_carts_get
Single record — same structure as `checkout_v1_carts_list` data item.

---

## checkout_v1_quote_accept_list
`POST /checkout/v1/quote/accept/`

Returns the updated Cart after quote acceptance — same structure as `checkout_v1_carts_list` data item.

---

## api_v1_admin_user_addresses_goal_progress_list
`GET /api/v1/admin/user-addresses/{user_address_id}/goal-progress/`

Fully computed from aggregated queries across Order, OrderGroup, Cart models. No pagination wrapper.

```python
{
    "carts": {
        "count": "computed",
        "open_count": "computed",
        "checked_out_count": "computed",
        "lost_count": "computed",
        "total_value": "computed",
        "open_value": "computed",
        "checked_out_value": "computed",
        "lost_value": "computed",
    },
    "order_groups": {
        "count": "computed",
        "active_count": "computed",
        "lost_count": "computed",
        "total_estimated_value": "computed",
        "active_estimated_value": "computed",
        "lost_estimated_value": "computed",
    },
    "orders": {
        "count": "computed",
        "in_cart_count": "computed",
        "checked_out_count": "computed",
        "completed_count": "computed",
        "lost_count": "computed",
        "total_value": "computed",
        "in_cart_value": "computed",
        "checked_out_value": "computed",
        "completed_value": "computed",
        "lost_value": "computed",
    },
}
```

---

## api_v1_admin_user_groups_goal_progress_list
`GET /api/v1/admin/user-groups/{user_group_id}/goal-progress/`

Fully computed from aggregated queries across UserGroup, UserGroupMonthlySpend, UserAddress models. No pagination wrapper.

```python
{
    "period": {
        "as_of": "computed",
        "current_month_start": "computed",
        "previous_month_start": "computed",
    },
    "gmv": {
        "goal": "api_usergroup",
        "current": "user_usergroupmonthlyspend",
        "previous_month": "user_usergroupmonthlyspend",
        "gap": "computed",
        "attainment_percent": "computed",
    },
    "users": {
        "goal": "api_usergroup",
        "current": "computed",
        "gap": "computed",
        "attainment_percent": "computed",
    },
    "job_site_starts": {
        "goal": "api_usergroup",
        "current": "computed",
        "gap": "computed",
        "attainment_percent": "computed",
    },
    "project_start_funnel": {
        "target_monthly_project_starts": "api_usergroup",
        "expected_to_date": "computed",
        "month_start": "computed",
        "month_end": "computed",
        "as_of": "computed",
        "addresses_starting_this_month": "api_useraddress",
        "due_by_now": "api_useraddress",
        "later_this_month": "api_useraddress",
        "due_by_now_with_populated_cart": "api_useraddress",
        "due_by_now_with_checked_out_cart": "api_useraddress",
        "due_by_now_added_to_cart_pct": "computed",
        "due_by_now_cart_to_checkout_pct": "computed",
        "due_by_now_added_to_checkout_pct": "computed",
    },
}
```

---

## api_v1_admin_user_groups_notes_list
`GET /api/v1/admin/user-groups/{user_group_id}/notes/`

Returns a list of UserGroupNote records.

```python
{
    "pagination": {
        "object": "pagination",
        "url": "pagination",
        "count": "pagination",
        "has_more": "pagination",
    },
    "data": [
        {
            "id": "api_usergroupnote",
            "text": "api_usergroupnote",
            "created_on": "api_usergroupnote",
            "updated_on": "api_usergroupnote",
            "created_by_id": "api_usergroupnote",
            "updated_by_id": "api_usergroupnote",
        }
    ]
}
```

---

## api_v1_seller_product_seller_locations_metrics_list
`GET /api/v1/seller-product-seller-locations/metrics/`

Computed counts from `SellerProductSellerLocation` queryset manager methods. No pagination wrapper.

```python
{
    "active": "computed",
    "needs_attention": "computed",
    "inactive": "computed",
}
```

---

## impersonation_start
Not a REST API endpoint. MCP-only tool — sets `X-On-Behalf-Of` header for subsequent calls. No response body.

---

## impersonation_end
Not a REST API endpoint. MCP-only tool — clears impersonation session. No response body.

---

## impersonation_status
Not a REST API endpoint. MCP-only tool — returns in-memory session state.

```python
{
    "is_active": "computed",
    "user_id": "computed",
}
```
