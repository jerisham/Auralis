# Tasks — 04 Catalog & Discovery

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-04-01 | Category tree + attribute schema (admin-editable, per-category required attributes) | T-17-02 | M | Todo |
| T-04-02 | Search engine setup + indexing pipeline (events from product changes) | T-16-05 | L | Todo |
| T-04-03 | Synonyms & typo config (incl. Hinglish list) | T-04-02 | S | Todo |
| T-04-04 | Catalog API: list/filter/sort/facets, autocomplete | T-04-02 | M | Todo |
| T-04-05 | PLP UI: grid, filters sheet/sidebar, chips, sort, infinite scroll/pagination, URL state | T-01-07, T-04-04 | L | Todo |
| T-04-06 | Product card component with badges and wishlist | T-01-07 | S | Todo |
| T-04-07 | Search UI: autocomplete, recent/trending, no-results page | T-04-04 | M | Todo |
| T-04-08 | Ranking formula + vendor diversity cap | T-04-04, T-10-09 | M | Todo |
| T-04-09 | Looks: data model, admin curation, look page, "add all to cart" | T-11-07, T-06-01 | M | Todo |
| T-04-10 | Sellers directory page | T-09-01 | S | Todo |
| T-04-11 | SEO: SSR, canonical URLs, Product schema.org, sitemaps | T-04-05 | M | Todo |

---

### T-04-01 — Taxonomy
- **Done when:** Tree in §2 and attributes in §3 seeded; admin can add a sub-category and mark attributes required for it without code changes.

### T-04-02 — Search
- **Steps:** Choose engine (Meilisearch / OpenSearch / Azure AI Search — see 16); index document = product + vendor status + stock + rating + reliability score; consume `product.*` and `inventory.*` events.
- **Done when:** Index updates ≤ 60 s after change; full reindex job exists.

### T-04-03 — Synonyms
- **Done when:** Synonym file under version control with ≥ 40 entries; deployable without downtime.

### T-04-04 — Catalog API
- **Done when:** `GET /v1/products?category=&q=&filters=&sort=&cursor=` returns items + facets; `GET /v1/search/suggest?q=`; p95 ≤ 300 ms at 50 RPS.

### T-04-05 — PLP UI
- **Done when:** All FR-04-01..03, 07, 10 implemented; works at 360px and 1440px.

### T-04-06 — Product card
- **Done when:** Matches FR-04-06; image lazy-loaded; second image on hover (desktop only).

### T-04-07 — Search UI
- **Done when:** FR-04-04, 05 implemented; keyboard navigable suggestions.

### T-04-08 — Ranking
- **Done when:** Formula documented in this folder (`ranking.md`), weights configurable by admin, diversity cap enforced.

### T-04-09 — Looks
- **Done when:** Admin creates a look from 3 vendors' products; customer adds all to cart in one tap; out-of-stock members flagged.

### T-04-10 — Sellers directory
- **Done when:** Lists approved, active vendors with filters.

### T-04-11 — SEO
- **Done when:** Category/product/vendor pages SSR; `sitemap.xml` auto-generated; Google Rich Results test passes for product pages.
