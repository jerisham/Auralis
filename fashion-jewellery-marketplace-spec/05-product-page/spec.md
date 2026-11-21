# 05 — Product Detail Page (PDP)

**Phase:** P1 · **Depends on:** 01, 04, 09 · **Status:** Draft

## 1. Purpose
Give the customer every detail they need to buy a piece of fashion jewellery with confidence — great images, honest materials and skin-safety info, seller trust signals, delivery estimate, and simple add-to-cart.

## 2. Layout (mobile order; desktop = gallery left, info right)
1. **Gallery:** swipeable images (up to 8) + optional 15 s video; pinch/zoom; full-screen viewer; scale-reference image highlighted.
2. **Title & seller:** product name (display serif), "by <Vendor>" link with Verified badge and rating.
3. **Price block:** selling price, MRP strike-through, % off; "Inclusive of all taxes".
4. **Variant selectors:** colour swatches, size (ring/bangle/length) — out-of-stock variants disabled.
5. **Quantity** (max = min(stock, 5)).
6. **CTAs:** "Add to cart" (gold) and "Buy now"; wishlist heart; share (WhatsApp, Instagram story link, copy link).
7. **Delivery check:** PIN input → "Delivered by <date range>" based on vendor dispatch time + transit estimate; vendor shipping fee and free-shipping threshold.
8. **Key highlights chips:** Nickel-free · Anti-tarnish · Lightweight 12 g · Ships in 24 h.
9. **Details accordion:** Description · Materials & finish · Dimensions & weight · Care instructions · Return policy (platform + vendor) · Seller information (legal name, address, GSTIN if any — required by e-commerce rules).
10. **Complete the look:** products from any vendor that match (admin looks first; else attribute-matched).
11. **More from this seller** carousel.
12. **Ratings & reviews:** average, distribution, photo reviews first, "verified purchase" tag.
13. **Similar items** carousel.
14. Sticky bottom bar on mobile: price + Add to cart.

## 3. Functional requirements
| ID | Requirement |
|---|---|
| FR-05-01 | URL `/p/<slug>-<id>`; variant selectable via query (`?v=<sku>`). |
| FR-05-02 | Price and stock fetched fresh (not cached > 30 s); "Only 2 left" when stock ≤ 3. |
| FR-05-03 | Delivery estimate = order date + vendor `dispatch_days` + zone transit days (metro/same-state/rest/NE & J&K) table. Shown as range. |
| FR-05-04 | Seller info block mandatory and sourced from vendor KYC record (not editable free text). |
| FR-05-05 | "Report this product" link (counterfeit, wrong info, offensive). |
| FR-05-06 | Recently viewed stored (local + account). |
| FR-05-07 | Share produces Open Graph image/title/price so WhatsApp/Instagram previews look premium. |
| FR-05-08 | If vendor is on holiday: show "Seller is away until <date>" and disable add-to-cart. |

## 4. Edge cases
- Product deleted/unpublished → 410 page with similar items.
- Price changes while item is in cart → cart shows updated price with notice (06).
- Variant without images → fall back to parent images.
