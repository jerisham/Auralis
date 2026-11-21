# Tasks — 10 Vendor Dashboard

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-10-01 | Portal shell: auth (vendor roles), navigation, responsive layout | T-01-07, T-16-03 | M | Todo |
| T-10-02 | Customisable widget board (show/hide/reorder/resize, persist per user, reset) | T-10-01 | L | Todo |
| T-10-03 | Product management: form with dynamic attributes, variants, media upload, duplicate, statuses | T-04-01, T-16-06 | L | Todo |
| T-10-04 | Bulk upload (CSV/Excel + images) with validation report | T-10-03 | L | Todo |
| T-10-05 | Inventory & pricing grid with inline edit, price rules, history | T-10-03 | M | Todo |
| T-10-06 | Orders management: tabs, accept/reject, slips, mark dispatched, bulk actions, CSV export | T-12-02, T-14-01 | L | Todo |
| T-10-07 | Payouts page, statements, commission invoices | T-13-10 | M | Todo |
| T-10-08 | Settings: shipping, serviceability, holiday mode, notification prefs | T-10-01 | M | Todo |
| T-10-09 | Insights + performance score calculation | T-19-04 | M | Todo |
| T-10-10 | Staff users and role permissions | T-10-01 | M | Todo |
| T-10-11 | New-vendor quality review gate (first 30 days) | T-11-05 | S | Todo |

---

### T-10-01 — Shell
- **Done when:** Vendor login (same OTP identity, vendor role required); nav per §2; works at 360px.

### T-10-02 — Widget board
- **Steps:** Use a grid layout library; widgets as independent components fetching own data; layout JSON in `dashboard_layouts` (user_id, layout, version).
- **Done when:** Layout persists across devices; reset restores default; a broken widget doesn't break the board.

### T-10-03 — Products
- **Steps:** Direct-to-blob upload via signed URLs; server generates renditions (16).
- **Done when:** Product with 3 variants and 6 images created on a phone in ≤ 5 min.

### T-10-04 — Bulk upload
- **Done when:** 500-row file processed asynchronously; error report downloadable with row/column messages; valid rows imported.

### T-10-05 — Inventory grid
- **Done when:** Inline edits saved in batch; rules in §5 enforced; history visible.

### T-10-06 — Orders
- **Done when:** All actions in §6 work and call state machine (12); tracking ID mandatory for dispatch; SLA timers visible.

### T-10-07 — Payouts
- **Done when:** Figures match ledger (13) for every order; statement PDF downloadable.

### T-10-08 — Settings
- **Done when:** Shipping settings feed cart (06) and PDP estimator (05); holiday mode per 09.

### T-10-09 — Insights & score
- **Steps:** Score = weighted (on-time dispatch %, 1 − cancellation %, 1 − claim %, avg rating) over 30 days; recalculated nightly; exposed to ranking (04).
- **Done when:** Charts render; score documented in `score.md`.

### T-10-10 — Staff
- **Done when:** Owner invites staff by phone; permission matrix §10 enforced in API (not just UI).

### T-10-11 — Quality gate
- **Done when:** New-vendor products enter moderation queue; approved ones publish.
