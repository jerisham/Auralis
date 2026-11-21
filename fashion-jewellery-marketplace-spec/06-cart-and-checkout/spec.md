# 06 — Cart & Checkout (Multi-vendor)

**Phase:** P1 · **Depends on:** 03, 05, 12, 13 · **Status:** Draft

## 1. Purpose
Let a customer buy from several vendors in **one cart and one payment**, while making it obvious that each vendor ships separately (separate shipping fee, separate delivery date, separate tracking).

## 2. Cart
- Items **grouped by vendor**: vendor name + logo, items, vendor subtotal, vendor shipping fee (or "Free shipping — you saved ₹X"; "Add ₹Y more for free shipping from <Vendor>"), estimated delivery for that group.
- Item row: image, name, variant, qty stepper, price, remove, move to wishlist.
- Order summary: items total, total discount (MRP − price), shipping total (sum of vendors), platform convenience fee (if decided — default ₹0), **grand total**.
- Banner: "Your order ships in N packages from N sellers."
- Price/stock revalidated on every cart view and at checkout; changes highlighted.

## 3. Checkout steps (single page on desktop, 3-step on mobile)
1. **Login** (if guest) via OTP sheet (03).
2. **Address:** choose saved or add new; serviceability check per vendor (vendor may exclude PIN ranges, e.g., no NE). Unserviceable vendor group flagged with option to remove.
3. **Review & pay:** summary per vendor, delivery estimates, email for invoice, accept Terms; **Pay** → gateway (UPI, cards, netbanking, wallets). No COD in MVP (Q-06).

## 4. Functional requirements
| ID | Requirement |
|---|---|
| FR-06-01 | Cart persists for logged-in users (server) and guests (local, 30 days). |
| FR-06-02 | Max 10 distinct items, max 5 per SKU, max 6 vendors per order (configurable). |
| FR-06-03 | On "Pay": create `Order` (status `PENDING_PAYMENT`) + one `VendorOrder` per vendor + **stock reservation** for 15 minutes. |
| FR-06-04 | Gateway order created with **split instructions** per vendor (13). |
| FR-06-05 | Payment success is confirmed by **server-side webhook** (not the browser redirect) → order `PAID` → vendor orders `AWAITING_ACCEPTANCE` (12). |
| FR-06-06 | Payment failure/timeout → reservation released; "Retry payment" available for 15 minutes from Orders. |
| FR-06-07 | Idempotency key on order creation and payment confirmation; double-click never creates two orders. |
| FR-06-08 | Order confirmation page: order number, per-vendor packages, expected dates, "What happens next" explainer. |
| FR-06-09 | Coupons: platform-wide coupons (admin-created), cost borne by platform — **P2**; field hidden in MVP. |
| FR-06-10 | Tax: prices are tax-inclusive; invoice per vendor order shows vendor as seller with tax breakup (13/18). |

## 5. Money breakdown shown to customer (example)
| | Vendor A | Vendor B | Total |
|---|---|---|---|
| Items | ₹500 | ₹1,200 | ₹1,700 |
| Shipping | ₹60 | Free | ₹60 |
| **Pay** | | | **₹1,760** |
(Platform fee is deducted from vendor side, never added to customer bill unless Q-02 decides otherwise.)

## 6. Edge cases
- Item goes out of stock between cart and pay → block payment, show which item, offer remove.
- Price increased → require customer acknowledgement before paying.
- Webhook arrives late (> 15 min) but payment captured → still confirm order if stock available; else auto-refund + apology notification.
- Customer closes tab mid-payment → webhook still completes order; email/WhatsApp confirmation sent.
- Partial vendor rejection after payment → handled in 12 (refund that vendor order only).
