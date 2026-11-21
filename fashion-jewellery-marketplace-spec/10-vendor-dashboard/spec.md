# 10 — Vendor Dashboard (Vendor Portal)

**Phase:** P1 · **Depends on:** 01, 08, 12, 13, 15 · **Status:** Draft

## 1. Purpose
The vendor's private workspace ("tenant admin"). Everything a seller needs — add/edit products, change prices and stock, handle orders, see money — in a calm, simple interface that works on a phone. Each vendor can **arrange their own dashboard home** (which widgets, in what order) but cannot change the portal's design.

## 2. Navigation
Home · Orders · Products · Inventory & Pricing · Store (09) · Payouts · Reviews & Claims · Insights · Settings (shipping, holiday, staff, bank, notifications) · Help

## 3. Home — customisable widget board
Vendor can **show/hide, reorder and resize (S/M/L)** widgets; layout saved per user. "Reset to default" available.
| Widget | Content |
|---|---|
| Action needed | Orders to accept, to dispatch (with SLA countdown), open claims, low-stock items |
| Today | Orders, revenue, store visits |
| Sales trend | 7/30/90-day line chart |
| Payouts | Pending (on hold), next release, last settlement |
| Top products | By revenue / views |
| Low stock | SKUs ≤ threshold |
| Ratings | Avg rating, latest reviews |
| Performance score | Dispatch-on-time %, cancellation %, claim % (affects ranking, 04) |
| Tips | Contextual tips (e.g., "Add a model photo to boost conversion") |

## 4. Products
- **Product form** (single page, sections): Category → required attributes appear dynamically (04 §3) · Title · Description · Images (drag reorder, crop to 1:1, auto background-clean optional P2) · Video (≤ 15 s) · Variants (colour/size) each with SKU, price, MRP, stock, weight · Skin-safety declarations · Care instructions · HSN code (default per category) · Status (Draft / Published / Archived).
- **Duplicate product** (fast way to add similar items).
- **Bulk upload:** CSV/Excel template per category + image ZIP or image URLs; validation report with row errors; up to 500 rows.
- **Bulk actions:** publish/unpublish, change price by % or fixed, change stock, add to collection, archive.
- New products from vendors in their first 30 days go to admin quality review; later ones publish instantly (post-moderation).

## 5. Inventory & pricing
- Spreadsheet-like grid: SKU, name, variant, price, MRP, stock, status — inline edit, save all.
- Price rules: price ≤ MRP; price change > 50% in one edit asks for confirmation; price history kept (prevents fake "% off" — MRP changes logged and visible to admin).
- Low-stock threshold per vendor (default 3); alerts via 15.

## 6. Orders
- Tabs: To accept · To dispatch · Shipped · Delivered · Completed · Cancelled · Claims.
- Order card: order no., items with images, **customer name, phone, full delivery address** (needed for self-delivery), amount, payout breakdown, SLA timer.
- Actions: **Accept** / **Reject** (reason; counts against score) → **Print packing slip & invoice** → **Mark dispatched** (courier name + tracking ID mandatory, optional parcel photo) → (delivery confirmed by 14).
- Bulk accept, bulk print slips, export CSV for courier upload.
- Optional (P2): book courier via shipping aggregator from dashboard.

## 7. Payouts
- Balance cards: On hold (T1 waiting dispatch), Releasing soon (T2 in return window), Paid this month, Deductions (refunds/recoveries).
- Per-order breakdown: item total, shipping, platform fee, tax deductions (TCS/TDS if applicable), T1, T2, status, UTR.
- Monthly statement PDF + commission tax invoice download (13).

## 8. Insights
Views, add-to-carts, conversion, revenue by product/category, traffic sources (incl. their own shared links via UTM), rating trend. Export CSV.

## 9. Settings
Shipping (fee, free threshold, dispatch days, serviceable regions/PIN exclusions) · Holiday mode · Staff users (Owner + up to 3 Staff; roles: Catalog, Orders) · Bank (re-verification flow, 08) · Notification preferences (which events on WhatsApp/email/push) · Business details (view; changes via request).

## 10. Permissions
| Area | Owner | Staff-Catalog | Staff-Orders |
|---|---|---|---|
| Products, inventory, store | ✓ | ✓ | view |
| Orders, claims | ✓ | view | ✓ |
| Payouts, bank, staff, business | ✓ | ✗ | ✗ |
| Insights | ✓ | ✓ | ✓ |
