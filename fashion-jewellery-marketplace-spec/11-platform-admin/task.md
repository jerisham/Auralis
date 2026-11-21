# Tasks — 11 Platform Admin

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-11-01 | Admin portal shell, admin RBAC, mandatory 2FA | T-16-03 | M | Todo |
| T-11-02 | Vendor applications queue & review actions | T-08-02 | M | Todo |
| T-11-03 | Vendor management: profile, suspend, strikes, overrides | T-11-02 | M | Todo |
| T-11-04 | Commission rules engine UI (global, category, vendor override, effective dates) | T-13-04 | M | Todo |
| T-11-05 | Moderation queue (products, store content, reviews, reports) | T-11-01 | M | Todo |
| T-11-06 | Orders console + claims/disputes decision tool + support tickets | T-12-02, T-07-04 | L | Todo |
| T-11-07 | Homepage & media CMS (intro, hero, sections, banners, looks, schedule) | T-11-01, T-16-06 | L | Todo |
| T-11-08 | Payouts & finance console (holds, retries, balances, reports) | T-13-06, T-13-09 | L | Todo |
| T-11-09 | Business dashboard (KPIs) | T-19-04 | M | Todo |
| T-11-10 | Configuration screens (SLAs, return window, zones, limits, templates, ranking, flags) | T-16-08 | M | Todo |
| T-11-11 | Audit log viewer + admin user management | T-17-06 | S | Todo |
| T-11-12 | Category & attribute tree editor | T-04-01 | S | Todo |

---

### T-11-01 — Shell & RBAC
- **Done when:** Roles §4 enforced at API; TOTP 2FA required at login; session timeout 30 min idle.

### T-11-02 — Applications
- **Done when:** Queue sorted by age; KYC result badges; actions trigger 08 state changes and notifications.

### T-11-03 — Vendors
- **Done when:** Strike policy §3 auto-applied by events; suspension hides store/products within 60 s.

### T-11-04 — Commission rules
- **Done when:** Priority: vendor override > category > global; effective-from respected; preview "₹500 item → fee ₹X".

### T-11-05 — Moderation
- **Done when:** Single queue with type filters; bulk approve; rejection reasons sent to vendor.

### T-11-06 — Orders & disputes
- **Done when:** Evidence viewer shows media, tracking events, timeline; decision executes refunds via 13; ticketing with macros.

### T-11-07 — Homepage CMS
- **Done when:** Every homepage section in 02 §4 editable; scheduled banners; looks builder with product search across vendors.

### T-11-08 — Finance console
- **Done when:** Failed transfer retry; manual hold/release with reason; reports exportable CSV.

### T-11-09 — KPIs
- **Done when:** Dashboard shows metrics from 00 §8 with date filters.

### T-11-10 — Config
- **Done when:** Changing SLA hours affects new orders without deploy.

### T-11-11 — Audit
- **Done when:** All admin mutations listed with before/after diff; immutable (append-only).

### T-11-12 — Taxonomy editor
- **Done when:** Drag-drop tree; attribute editor; changes reflected in vendor product form.
