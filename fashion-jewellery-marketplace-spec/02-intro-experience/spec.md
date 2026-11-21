# 02 — Intro Experience ("A new world")

**Phase:** P1 · **Depends on:** 01, Q-15 (video) · **Status:** Draft

## 1. Purpose
The first time someone opens the site, it should feel like stepping into a jewellery boutique, not a shopping list. A short cinematic video sets the mood, then hands off to the homepage within seconds. It must never slow down returning shoppers.

## 2. User stories
- As a first-time visitor, I see a short, beautiful jewellery film so I immediately understand what this place is.
- As a returning visitor, I go straight to the homepage (with a subtle looping hero), not the full intro again.
- As anyone, I can skip the intro instantly.
- As a user on slow data or with reduced-motion settings, I get a still image instead of a heavy video.

## 3. Functional requirements
| ID | Requirement |
|---|---|
| FR-02-01 | First visit (no `intro_seen` flag): full-screen, muted, autoplaying video, 8–12 s. |
| FR-02-02 | "Skip" (top-right) visible from 0 s; "Enter the collection" CTA appears at 3 s and at end. |
| FR-02-03 | On end/skip/CTA: fade (400ms) into homepage; set `intro_seen` (localStorage + cookie, 90 days; and on the user profile if logged in). |
| FR-02-04 | Returning visit: homepage with a 6–8 s silent looping hero video (or image carousel) behind the headline. |
| FR-02-05 | `prefers-reduced-motion`, Save-Data header, or effective connection type `2g/slow-2g` → show poster image with the same CTA; no autoplay. |
| FR-02-06 | Sound toggle (off by default). |
| FR-02-07 | Deep links (product, store, look URLs) **never** show the intro — users from Instagram/WhatsApp links land directly on content. |
| FR-02-08 | Admin can replace intro video, poster and hero loop from admin portal (11) without a deploy; can schedule festive versions (Diwali, wedding season). |
| FR-02-09 | Crawlers/SEO: homepage HTML content is fully server-rendered under the video layer. |

## 4. Homepage (after intro) — sections in order
1. Hero (loop video/image) + headline + "Shop now" / "Explore looks".
2. Shop by category (circular icons: Earrings, Necklaces, Sets, Bangles, Rings, Anklets, Nose pins, Maang tikka, Hair).
3. Shop by occasion (Wedding, Festive, Office, Party, Everyday, Gifting).
4. Trending now (product carousel).
5. Complete the look (cross-vendor look cards).
6. Featured sellers (vendor cards with logo, city, rating).
7. Under ₹499 / Under ₹999.
8. Skin-safe picks (nickel-free, hypoallergenic).
9. New arrivals.
10. Trust strip: "Verified sellers · Secure payments · Money held until dispatch · Easy damage claims".
All sections curated or auto-filled via admin (11).

## 5. Video specifications
| Asset | Spec |
|---|---|
| Intro desktop | 1920×1080, H.264 MP4 + VP9/AV1 WebM, ≤ 6 MB, 24/30fps |
| Intro mobile | 1080×1920 vertical, ≤ 3 MB |
| Hero loop | 6–8 s seamless loop, ≤ 2.5 MB mobile |
| Poster | AVIF/WebP, ≤ 150 KB |
| Delivery | CDN, `preload="metadata"`, adaptive by viewport |
Content: macro shots of earrings catching light, model wearing layered necklaces, quick cuts across styles (ethnic, western, minimal), ending on logo + tagline. No text that needs translating, except logo/tagline.

## 6. Edge cases
- Autoplay blocked by browser → show poster with play button and CTA.
- Video fails to load within 2.5 s → show poster + CTA.
- Private/incognito mode (no storage) → intro shows each session; acceptable.
