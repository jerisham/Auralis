# KPI sheet — module 00 §8

**Date:** 21 Nov 2026 · **Task:** T-00-05

Pilot window: first 90 days after invite-only launch. Money events are counted only when `payment_success` has been confirmed by the payment webhook, then joined to the database on `order_id`. Client events never carry phone, address, or a raw user id.

| KPI | Target | Formula | Source |
|---|---|---|---|
| Active vendors (≥ 1 order) | 20 | Count of distinct `vendor_id` on vendor orders whose parent order has a `payment_success` event in the window | `payment_success` joined to `vendor_orders` |
| Live products | ≥ 1,000 | Count of products whose latest catalogue event is `product_published` (no later `product_unpublished`), checked against `products.status = published` | `product_published` / `product_unpublished` |
| Monthly orders | 500 | Count of `payment_success` events in the calendar month | `payment_success` |
| Conversion (session → order) | ≥ 1.5% | Distinct `session_id` with a `payment_success` ÷ distinct `session_id` with a `page_view` | `page_view`, `payment_success` |
| Average vendor dispatch time | ≤ 48 h | Mean of `minutes_since_paid` on `vendor_order_dispatched` ÷ 60 | `vendor_order_dispatched` |
| Orders with a dispute | ≤ 3% | Count of orders with at least one `claim_opened` ÷ count of `payment_success` | `claim_opened`, `payment_success` |
| Repeat customers within 60 days | ≥ 20% | Customers with two or more `payment_success` events ≤ 60 days apart (user resolved from `orders.user_id` via `order_id`) ÷ customers with at least one `payment_success` | `payment_success` |
| Vendor NPS | ≥ 40 | NPS from `vendor_nps_submitted.score` in the window: (% promoters 9–10) − (% detractors 0–6) | `vendor_nps_submitted` |

Funnel used beside these KPIs (module 19): visit (`page_view`) → PDP (`product_view`) → add to cart (`add_to_cart`) → checkout (`checkout_start`) → paid (`payment_success`). Vendor funnel: `vendor_onboarding_step` → approval in the database → first `payment_success` that includes that vendor.

Every event name in this table is defined in `19-non-functional-and-analytics/spec.md` §7.
