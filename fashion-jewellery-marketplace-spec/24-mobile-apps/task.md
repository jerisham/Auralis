# Tasks — 24 Mobile Apps

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-24-01 | Expo app scaffold in monorepo, shared api-client & tokens, CI with EAS Build | T-16-09, T-01-06 | M | Todo |
| T-24-02 | Customer app: auth, home, intro, PLP, search, PDP | T-24-01 | L | Todo |
| T-24-03 | Customer app: cart, checkout with gateway RN SDK, orders, claims, reviews | T-24-02 | L | Todo |
| T-24-04 | Push notifications (FCM/APNs) wired to 15 | T-15-01 | M | Todo |
| T-24-05 | Deep links / universal links (assetlinks.json, apple-app-site-association) | T-24-02 | S | Todo |
| T-24-06 | Vendor companion app: orders, accept, dispatch with barcode scan, quick edits, payouts | T-24-01 | L | Todo |
| T-24-07 | Store listings, privacy labels, data safety, screenshots | T-18-06 | S | Todo |
| T-24-08 | Beta (TestFlight, Play internal testing) with pilot users | T-24-03, T-24-06 | M | Todo |
| T-24-09 | Public release + OTA update process | T-24-08 | S | Todo |

---

### T-24-01 — Scaffold
- **Done when:** iOS and Android dev builds produced in CI; theme from tokens.

### T-24-02/03 — Customer app
- **Done when:** Critical journeys 1, 4 (21 §3) pass on both platforms.

### T-24-04 — Push
- **Done when:** Vendor new-order push arrives ≤ 60 s with high priority.

### T-24-05 — Deep links
- **Done when:** Product link from WhatsApp opens app if installed, web otherwise.

### T-24-06 — Vendor app
- **Done when:** Journey 2 (21 §3) passes in app; barcode scan fills tracking ID.

### T-24-07 — Store compliance
- **Done when:** Listings submitted with accurate privacy disclosures.

### T-24-08 — Beta
- **Done when:** ≥ 50 customers and ≥ 10 vendors used beta for 2 weeks; crash-free sessions ≥ 99.5%.

### T-24-09 — Release
- **Done when:** Apps live; OTA channel configured per environment.
