# Tasks — 09 Vendor Storefront

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-09-01 | Store API + SSR store page (template §2) | T-04-04, T-08-02 | M | Todo |
| T-09-02 | Store editor in vendor portal (logo, banner, about, tags) with live preview | T-10-01 | M | Todo |
| T-09-03 | Featured products + collections manager (drag to order) | T-10-03 | M | Todo |
| T-09-04 | Automated content checks + moderation flagging | T-11-05 | S | Todo |
| T-09-05 | Holiday mode + suspended state handling | T-09-01 | S | Todo |
| T-09-06 | Share card + QR generator | T-09-01 | S | Todo |

---

### T-09-01 — Store page
- **Done when:** Template sections render from API; vendor-scoped filters work; SSR + OG tags.

### T-09-02 — Store editor
- **Done when:** Vendor edits content slots only; preview matches live page; no styling controls exist.

### T-09-03 — Collections
- **Done when:** Max 8 featured, 6 collections enforced; drag-and-drop order persists.

### T-09-04 — Content checks
- **Done when:** Phone numbers, URLs, emails and profanity in about text blocked or flagged; low-res images rejected.

### T-09-05 — Holiday/suspended
- **Done when:** FR-09-03 and FR-09-04 behaviours implemented.

### T-09-06 — Share kit
- **Done when:** Downloadable 1080×1920 story image and QR pointing to store URL with UTM tags.
