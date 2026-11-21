# 17 — Data Model

**Phase:** P0 · **Depends on:** 16 · **Status:** Draft

## 1. Purpose
Core entities and relationships. Column lists are the minimum; types follow conventions in §4.

## 2. Entities by domain

### Identity
| Entity | Key fields |
|---|---|
| `users` | id, phone (unique), email, name, status, created_at |
| `user_roles` | user_id, role (customer, vendor_owner, vendor_staff, admin, super_admin), vendor_id?, admin_role? |
| `addresses` | id, user_id, name, phone, line1, line2, landmark, city, state, pin, type, is_default |
| `refresh_tokens`, `otp_requests` | per 03 |

### Vendor
| Entity | Key fields |
|---|---|
| `vendor_applications` | id, owner_user_id, state, step_data (JSONB), submitted_at, reviewed_by, decision_reason |
| `vendors` | id, legal_name, display_name, slug, business_type, pan_masked, gstin, pickup_address, status (active, holiday, suspended), holiday_until, score, strikes, payout_status, gateway_linked_account_id |
| `vendor_kyc` | vendor_id, provider_refs, verified_at, documents (encrypted refs) |
| `vendor_bank` | vendor_id, holder_name, account_last4, ifsc, verified_at, gateway_ref |
| `vendor_settings` | vendor_id, dispatch_days, shipping_fee, free_threshold, excluded_pin_prefixes[], return_addons |
| `store_profiles` | vendor_id, logo_media_id, banner_media_id, about, tags[] |
| `collections` | id, vendor_id, name, position; `collection_products`(collection_id, product_id, position) |
| `dashboard_layouts` | user_id, vendor_id, layout (JSONB), version |
| `seller_agreement_acceptances` | vendor_id, version, accepted_at, ip, user_agent |

### Catalog
| Entity | Key fields |
|---|---|
| `categories` | id, parent_id, name, slug, hsn_default, position |
| `attributes` | id, code, name, type (enum, multi, number, bool), values[] |
| `category_attributes` | category_id, attribute_id, required |
| `products` | id, vendor_id, category_id, title, slug, description, care, status, attributes (JSONB), skin_safety[], created_at, published_at |
| `product_variants` | id (SKU), product_id, vendor_id, options (JSONB), price, mrp, stock, reserved, weight_g, status |
| `price_history` | variant_id, price, mrp, changed_by, changed_at |
| `media` | id, owner_type, owner_id, vendor_id?, kind, original_url, renditions (JSONB), position |
| `looks` | id, title, occasion, hero_media_id, status; `look_items`(look_id, variant_id, position) |
| `reviews` | id, product_id, vendor_order_item_id, user_id, rating, text, media[], status |
| `vendor_ratings` | vendor_order_id, user_id, rating |
| `wishlists`, `follows` | user ↔ product / vendor |

### Commerce
| Entity | Key fields |
|---|---|
| `carts`, `cart_items` | per 06 |
| `orders` | id, number, user_id, address_snapshot (JSONB), totals, status, payment_status, created_at |
| `vendor_orders` | id, order_id, vendor_id, number, state, items_total, shipping, commission, taxes (JSONB), vendor_net, t1, t2, sla_accept_at, sla_dispatch_at, return_window_ends_at |
| `order_items` | id, vendor_order_id, variant_id, title_snapshot, qty, unit_price, mrp, commission_rate_snapshot, hsn |
| `order_events` | id, vendor_order_id, from_state, to_state, actor_type, actor_id, reason, meta, at |
| `stock_reservations` | variant_id, order_id, qty, expires_at |
| `shipments` | id, vendor_order_id, courier, tracking_id, method, dispatched_at, delivered_at, proof, events (JSONB) |
| `claims` | id, vendor_order_id, type, state, items, media[], vendor_response, admin_decision, amounts |

### Finance
| Entity | Key fields |
|---|---|
| `payments` | id, order_id, gateway, gateway_order_id, gateway_payment_id, amount, status, method |
| `transfers` | id, vendor_order_id, tranche (T1/T2), gateway_transfer_id, amount, status (held, released, reversed, settled), released_at |
| `refunds` | id, order_id, vendor_order_id, amount, reason, gateway_refund_id, status |
| `ledger_entries` | id, txn_id, account, debit, credit, vendor_id?, vendor_order_id?, at |
| `commission_rules` | id, scope (global/category/vendor), scope_id, rate_bps, fixed_fee, effective_from, effective_to |
| `invoices` | id, type (customer, commission), series, number, vendor_id, vendor_order_id?, pdf_url, issued_at |
| `payout_holds` | vendor_id, reason, created_by, released_at |
| `reconciliation_runs`, `reconciliation_items` | per 13 |

### Platform
`notifications`, `notification_templates`, `notification_preferences`, `support_tickets`, `moderation_items`, `config`, `feature_flags`, `cms_sections`, `banners`, `audit_log` (append-only), `outbox`, `webhook_events`, `pincodes`.

## 3. Key relationships
- User 1—N Address; User 1—N Order; Order 1—N VendorOrder; VendorOrder 1—N OrderItem; VendorOrder 1—1 Shipment; VendorOrder 1—2 Transfers.
- Vendor 1—N Product 1—N Variant; Variant N—N Look.
- Every money movement ⇒ ≥ 2 LedgerEntries sharing `txn_id`.

## 4. Conventions
- IDs: UUIDv7 (time-ordered); human-readable numbers for orders (`ORD-2611-000123`) and vendor orders (`ORD-2611-000123-A`).
- Money: `bigint` paise; never floats. Rates: basis points (`rate_bps`, 2000 = 20%).
- Timestamps: `timestamptz` UTC.
- Snapshots: order items/addresses store copies (titles, prices, rates) so history never changes when products change.
- Soft delete (`deleted_at`) for user-facing entities; **no deletes** on ledger, audit, order_events.
- PII columns tagged in schema comments for 18 (encryption, export, deletion).
