# Tasks — 05 Product Page

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-05-01 | Product detail API (product, variants, live price/stock, vendor summary) | T-17-02, T-10-03 | M | Todo |
| T-05-02 | Gallery: swipe, zoom, full-screen, video | T-01-07 | M | Todo |
| T-05-03 | Info section: price block, variants, qty, CTAs, highlights, accordions, seller block | T-05-01 | M | Todo |
| T-05-04 | Delivery estimator (PIN → zone → date range) | T-03-06, T-10-08 | M | Todo |
| T-05-05 | Carousels: complete the look, more from seller, similar | T-04-04, T-04-09 | M | Todo |
| T-05-06 | Reviews display block | T-07-05 | S | Todo |
| T-05-07 | Share + Open Graph images | T-05-01 | S | Todo |
| T-05-08 | Report product flow → admin queue | T-11-05 | S | Todo |
| T-05-09 | Edge pages: 410, vendor on holiday, out of stock | T-05-03 | S | Todo |

---

### T-05-01 — PDP API
- **Done when:** `GET /v1/products/{id}` returns everything for §2 in one call; stock/price uncached ≤ 30 s; p95 ≤ 250 ms.

### T-05-02 — Gallery
- **Done when:** Swipe on mobile, arrow keys on desktop, pinch-zoom, video plays muted inline.

### T-05-03 — Info section
- **Done when:** All elements in §2 items 2–9 and 14 render; disabled states for OOS variants.

### T-05-04 — Delivery estimator
- **Steps:** Zone table (admin-configurable) by origin state vs destination PIN region; combine with vendor dispatch days.
- **Done when:** Estimate shown and stored PIN remembered.

### T-05-05 — Carousels
- **Done when:** Each carousel has ≥ 4 items or hides itself.

### T-05-06 — Reviews block
- **Done when:** Shows avg, distribution, photo reviews first, paginated.

### T-05-07 — Share
- **Done when:** OG image generated (product image on brand background with price); WhatsApp preview renders.

### T-05-08 — Report
- **Done when:** Report creates admin moderation item with reason.

### T-05-09 — Edge pages
- **Done when:** FR-05-08 and §4 handled.
