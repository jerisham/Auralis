# Validation — 04 Catalog & Discovery

Seed data: 5 vendors × 60 products across all categories, with varied attributes.

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-04-01 | T-04-01 | Manual | | | |
| V-04-02 | T-04-02 | Automated | | | |
| V-04-03 | T-04-03 | Automated | | | |
| V-04-04 | T-04-04 | Automated + load | | | |
| V-04-05 | T-04-05 | Playwright + manual | | | |
| V-04-06 | T-04-06 | Storybook visual | | | |
| V-04-07 | T-04-07 | Playwright | | | |
| V-04-08 | T-04-08 | Automated | | | |
| V-04-09 | T-04-09 | Playwright | | | |
| V-04-10 | T-04-10 | Manual | | | |
| V-04-11 | T-04-11 | Tooling | | | |

### V-04-01 — Taxonomy editable
- **Steps:** Admin adds "Ear chains" sub-category and marks "Length" required.
- **Pass criteria:** Appears in navigation; vendor product form for it requires Length.

### V-04-02 — Index freshness
- **Steps:** Change a product price; set another product stock to 0.
- **Pass criteria:** Both reflected in search results ≤ 60 s.

### V-04-03 — Synonyms
- **Pass criteria:** Queries `jhumki`, `jumka` (typo), `AD earrings`, `oxidized` each return relevant products in the top 5.

### V-04-04 — API performance
- **Pass criteria:** k6 at 50 RPS: p95 ≤ 300 ms, 0% errors; facet counts match DB counts for 5 sample filter combinations.

### V-04-05 — PLP behaviour
- **Scenarios:** Apply 3 filters → URL updates → copy URL to new tab → same results; open product → back → scroll position restored; remove chip → results update; out-of-stock hidden by default.
- **Pass criteria:** All scenarios pass on mobile and desktop.

### V-04-06 — Card
- **Pass criteria:** Visual snapshot approved; badges render per data; heart toggles wishlist.

### V-04-07 — Search UX
- **Pass criteria:** Suggestions appear ≤ 200 ms after typing pause; no-results page shows suggestions.

### V-04-08 — Fair ranking
- **Steps:** Vendor A has 40 strong products in Earrings.
- **Pass criteria:** Top 12 of Earrings contains ≤ 3 from Vendor A; suspended vendor's products absent.

### V-04-09 — Looks
- **Pass criteria:** "Add all" adds every in-stock member; cart groups by vendor correctly.

### V-04-10 — Directory
- **Pass criteria:** Suspended vendor not listed; city filter works.

### V-04-11 — SEO
- **Pass criteria:** Google Rich Results test: valid Product with price + availability; Lighthouse SEO ≥ 95.

## Module sign-off
- [ ] All checks Pass
- [ ] Product owner approval
