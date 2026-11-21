# 23 — Growth Features (P2 Differentiators)

**Phase:** P2 · **Depends on:** P1 complete · **Status:** Draft — prioritise after pilot data

## 1. Purpose
Features that make the platform clearly better than general marketplaces and Instagram shopping. Each is independent and behind a feature flag. Prioritise by pilot learnings.

## 2. Feature list
| # | Feature | Description | Value | Effort |
|---|---|---|---|---|
| G1 | **Virtual try-on (earrings, necklaces, nose pins)** | In-browser camera with face landmark tracking (e.g., MediaPipe Face Landmarker); overlays a vendor-supplied transparent front-view PNG scaled using product dimensions. Photo mode fallback (upload a selfie). No images stored unless user saves. | Conversion, wow factor | L |
| G2 | **Shoppable reels feed** | Vertical video feed (vendor-uploaded 15–30 s clips) with tagged products; tap to add to cart; moderation queue. | Discovery, matches Instagram habits | L |
| G3 | **Instagram import for vendors** | Vendor connects an Instagram professional (Business/Creator) account through Meta's official API; recent posts appear as draft products (images + caption → title/description suggestions) for vendor to complete. | Faster onboarding | M |
| G4 | **AI "Complete the look"** | Suggest cross-vendor matches by attributes (plating, colour, occasion, style) + image embeddings; admin can pin/ban pairs. | AOV, D5 differentiator | M |
| G5 | **Outfit match** | Customer uploads an outfit photo → dominant colours & style detected → suggested jewellery. | Unique, shareable | M |
| G6 | **Gifting assistant** | Q&A (recipient, occasion, budget, style) → curated list; gift wrap + gift message option per vendor. | Gifting seasons | M |
| G7 | **Wishlist sharing & "help me choose"** | Share a wishlist link; friends vote. | Virality | S |
| G8 | **Platform coupons & vendor coupons** | Coupon engine (who funds: platform or vendor), limits, stacking rules; ledger-aware. | Promotions | M |
| G9 | **Delivery OTP** | See 14 T-14-07. | Trust | M |
| G10 | **Courier booking from dashboard** | Shipping aggregator integration for vendors to book pickups and print labels. | Vendor convenience, reliable tracking | M |
| G11 | **Loyalty ("Sparkle points")** | Points on delivered orders; redeem on future orders; platform-funded. | Retention | M |
| G12 | **Vendor ads / sponsored listings** | Vendors pay to boost products in search (clearly labelled "Sponsored"). | New revenue | L |
| G13 | **COD (limited)** | Only for trusted customers/vendors, with platform-collected COD via aggregator. | Reach tier-2/3 | L |
| G14 | **Hindi & Tamil UI** | Using i18n from 19. | Reach | M |

## 3. Rules
- Try-on and outfit match process images on-device where possible; any server processing requires explicit consent and deletion within 24 h.
- Sponsored listings never exceed 2 per 12 results and are always labelled.
- Instagram import uses only official, approved APIs and permissions requested by the vendor themselves.
