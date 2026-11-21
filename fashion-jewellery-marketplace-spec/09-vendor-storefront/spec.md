# 09 — Vendor Storefront

**Phase:** P1 · **Depends on:** 01, 04, 08 · **Status:** Draft

## 1. Purpose
Every vendor gets a store page inside the platform. **All stores share one fixed template** (same look for everyone — the "common view"); vendors fill in content slots only. This keeps the brand consistent while giving sellers a page they can proudly share on Instagram.

## 2. Template (fixed)
1. Banner (vendor image, 16:5) with gradient overlay.
2. Logo (circle), store name, city, "Verified seller" badge, rating (★ 4.6 · 230 reviews), "Ships in 24 h" badge if applicable, Follow button, Share button.
3. About (≤ 500 chars), speciality tags (e.g., Oxidised, Kundan, Handmade).
4. **Featured collection** (vendor picks up to 8 products).
5. **Vendor collections** as tabs (e.g., "Bridal", "Office wear") — up to 6, vendor-named and ordered.
6. All products grid with the standard PLP filters (04), scoped to this vendor.
7. Store policies: dispatch time, shipping fee/threshold, return policy additions.
8. Seller legal info (from KYC).

## 3. What a vendor CAN and CANNOT change
| Vendor CAN | Vendor CANNOT |
|---|---|
| Logo, banner, about text, speciality tags | Colours, fonts, layout, CSS, section order |
| Featured products & order | Add custom HTML/scripts/links to external stores |
| Collections: create, name, order, assign products | Change header/footer/navigation |
| Store holiday mode with return date | Hide platform badges, ratings or reviews |
| Shipping fee, threshold, dispatch days, serviceable regions | Change the URL slug after approval (admin only) |

## 4. Functional requirements
| ID | Requirement |
|---|---|
| FR-09-01 | URL `/s/<store-slug>`; SSR; Open Graph for sharing. |
| FR-09-02 | Content edits (banner, about) go live immediately but pass automated checks (image size, profanity, no phone numbers/URLs in text to prevent off-platform selling); flagged items to admin moderation. |
| FR-09-03 | Holiday mode: store shows banner "Away until <date>", products hidden from search, add-to-cart disabled; pending orders still must be fulfilled. |
| FR-09-04 | Suspended store → 404-like "Store unavailable" page; products removed from search. |
| FR-09-05 | Store QR code + share card (story-size image) downloadable from vendor dashboard for Instagram promotion. |

## 5. Edge cases
- Vendor with < 4 products → hide featured section, show grid only.
- Banner missing → platform default gradient.
