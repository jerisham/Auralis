# Tasks — 06 Cart & Checkout

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-06-01 | Cart model & API (server + guest), grouping by vendor, limits | T-17-03 | M | Todo |
| T-06-02 | Shipping fee & free-shipping threshold calculation per vendor | T-10-08 | S | Todo |
| T-06-03 | Cart UI (grouped, summary, nudges, revalidation messages) | T-01-07, T-06-01 | M | Todo |
| T-06-04 | Address step with per-vendor serviceability | T-03-06, T-10-08 | M | Todo |
| T-06-05 | Order creation: Order + VendorOrders + stock reservation (15 min) + idempotency | T-12-01 | L | Todo |
| T-06-06 | Gateway checkout with split instructions | T-13-02 | L | Todo |
| T-06-07 | Webhook-driven confirmation, failure/timeout handling, retry payment | T-13-03 | M | Todo |
| T-06-08 | Confirmation page + "what happens next" | T-06-07 | S | Todo |
| T-06-09 | Reservation expiry job + late-webhook handling | T-06-05 | M | Todo |

---

### T-06-01 — Cart model
- **Done when:** `GET/POST/PATCH/DELETE /v1/cart/items`; response grouped by vendor with totals; limits FR-06-02 enforced.

### T-06-02 — Shipping calc
- **Done when:** Per-vendor fee/threshold applied; nudge text computed by API.

### T-06-03 — Cart UI
- **Done when:** §2 implemented; price/stock change banners shown.

### T-06-04 — Address & serviceability
- **Done when:** Unserviceable vendor group flagged with remove option; cannot pay until resolved.

### T-06-05 — Order creation
- **Steps:** Single DB transaction: validate stock/price → create Order, VendorOrders, OrderItems → reserve stock (`reserved_qty`) with expiry → return payment payload. Require `Idempotency-Key` header.
- **Done when:** Concurrent test (two customers, last unit) → exactly one reservation succeeds.

### T-06-06 — Gateway checkout
- **Done when:** Gateway order contains transfers per vendor linked account with `on_hold` per 13; customer pays via UPI/card in sandbox.

### T-06-07 — Confirmation via webhook
- **Done when:** Signature-verified webhook marks order PAID exactly once (idempotent); failure path releases stock.

### T-06-08 — Confirmation page
- **Done when:** FR-06-08 content shown; also emailed/WhatsApp'd (15).

### T-06-09 — Expiry & late webhook
- **Done when:** Reservations auto-released after 15 min; late successful payment either confirmed or auto-refunded per §6.
