# 00 — Product Vision

**Phase:** P0 · **Depends on:** — · **Status:** Approved v1.0 — 21 Nov 2026, while validating V-00-04. Personas, roles, and MVP scope in §5–§7 are unchanged. Interview notes in research.md stay labeled as generated, not field interviews.

## 1. Purpose
Agree on the problem, who we serve, what makes us different, and how we measure success. Every other module traces back to this file.

## 2. Problem
- Fashion jewellery is one of the highest-volume categories in Indian e-commerce, but it is buried inside general marketplaces (Meesho, Amazon, Flipkart, Myntra) next to kitchenware and electronics, with a cheap look and inconsistent quality.
- Thousands of small jewellery sellers run on Instagram/WhatsApp: one shop per page, manual DMs, UPI screenshots, no cart across sellers, no buyer protection.
- The closest vertical player (Eternz, launched 2024) mixes fine jewellery (gold, silver, diamonds) with fashion jewellery and curates established brands, so small independent sellers mostly cannot join.

## 3. Vision
**"One beautiful place to discover and buy fashion jewellery from India's best independent sellers — with the trust of a big marketplace and the feel of a luxury boutique."**

## 4. Positioning & differentiators
| # | Differentiator | Module |
|---|---|---|
| D1 | **Fashion jewellery only** — every filter, attribute and visual built for it | 04, 05 |
| D2 | **Premium, glossy, cinematic design** at fashion-jewellery prices | 01, 02 |
| D3 | **Open to small sellers** — Instagram sellers onboard in minutes | 08, 23 |
| D4 | **Multi-vendor cart** — earrings from A, necklace from B, one checkout | 06 |
| D5 | **"Complete the look"** across vendors, by occasion | 04, 23 |
| D6 | **Skin-safety tags** (nickel-free, hypoallergenic, anti-tarnish) as first-class filters | 04, 05 |
| D7 | **Buyer protection** — money held until dispatch/delivery, clear dispute flow | 13, 14 |
| D8 | **WhatsApp-first vendor alerts** — sellers act on orders in minutes | 15 |
| D9 | Later: AR try-on, shoppable reels | 23 |

## 5. Personas
- **Priya, 24, customer** — college/early career, shops on Instagram, ₹300–₹2,000 per piece, wants trendy pieces for events and office, worries about quality and skin irritation.
- **Meena, 38, customer** — buys for weddings/festivals, wants complete sets, values trust and returns for damaged items.
- **Ravi, vendor** — runs a 3-person jewellery business in Jaipur from Instagram (8k followers), ships via a courier aggregator, wants more reach without Amazon's complexity.
- **Asha, vendor** — home-based designer, handmade beaded jewellery, low volume, not tech-savvy; uses phone only.
- **Platform admin** — approves vendors, resolves disputes, curates homepage.

## 6. Roles (system)
| Role | Can |
|---|---|
| Guest | Browse, search, view products and stores |
| Customer | + cart, checkout, orders, returns, reviews, wishlist, addresses |
| Vendor Owner | Manage own store profile, products, prices, inventory, orders, payouts, bank/KYC, staff, own dashboard layout |
| Vendor Staff | Products, inventory, orders (no bank, payouts, staff) |
| Admin | Vendor approval, catalog moderation, orders/disputes, homepage curation, reports |
| Super Admin | + commission rules, payout overrides, admin users, feature flags |

## 7. Scope
**MVP (P1) in:** customer web (PWA), vendor portal, admin portal, multi-vendor cart, payments with split + held tranches, vendor self-delivery with tracking, notifications (email + WhatsApp + in-app), returns for damaged items, reviews.
**Out of MVP:** platform logistics, COD, chat, vendor coupons, international, AR try-on, reels, native apps.

## 8. Success metrics
| Metric | Pilot target (first 90 days) |
|---|---|
| Active vendors (≥1 order) | 20 |
| Live products | ≥ 1,000 |
| Monthly orders | 500 |
| Conversion rate (session → order) | ≥ 1.5% |
| Avg. vendor dispatch time | ≤ 48 h |
| Orders with dispute | ≤ 3% |
| Repeat customers within 60 days | ≥ 20% |
| Vendor NPS | ≥ 40 |

## 9. Risks
| Risk | Mitigation |
|---|---|
| Vendor delivery quality varies | SLAs, tracking mandatory, payouts tied to delivery, vendor rating, suspension rules |
| Chicken-and-egg (no vendors ↔ no customers) | Onboard vendors first; launch only with ≥ 500 products; vendors bring their Instagram audience |
| Payment/regulatory compliance | Use gateway split-payment products; CA + lawyer review before launch (18) |
| Fake / low-quality listings | Approval + first-5-listings review, reporting, ratings |
