# Roadmap

Estimates assume a small team: 1 product/design lead, 2–3 full-stack developers, 1 DevOps (part-time), 1 QA (part-time). Treat durations as rough planning numbers, not commitments.

## Milestones

| Milestone | Contents (modules) | Exit criteria | Rough duration |
|---|---|---|---|
| **M0 – Decisions** | `OPEN-QUESTIONS.md` | All "Blocker" questions answered | 1 week |
| **M1 – Foundations** | 00, 01, 16, 17, 20, 21 (setup) | Design tokens in code; repo, CI/CD, dev/staging environments live; schema v1 migrated; auth skeleton | 3–4 weeks |
| **M2 – Vendor side** | 08, 09, 10 (products & orders tabs), 11 (vendor approval) | A vendor can register, be approved, list 50 products with images | 4–5 weeks |
| **M3 – Customer side** | 02, 03, 04, 05, 06 | A customer can browse, search, add items from 3 vendors to one cart and reach payment | 4–5 weeks |
| **M4 – Money & fulfilment** | 12, 13, 14, 15, 07 | End-to-end paid order → vendor notified → dispatched → delivered → payouts settled, in sandbox | 4–5 weeks |
| **M5 – Hardening** | 18, 19, 21 (full), 11 (rest) | Security review, load test, accessibility audit, legal pages all pass | 2–3 weeks |
| **M6 – Pilot launch** | 22 | 15–25 pilot vendors, ≥ 500 live products, invite-only customers | 4 weeks |
| **M7 – Public launch** | 22 | Pilot KPIs met (see 22) | — |
| **M8 – Growth** | 23 | Feature-by-feature | ongoing |
| **M9 – Mobile apps** | 24 | Apps live on Play Store / App Store | 8–10 weeks |

## Build order (dependency view)

```
00 vision ─┬─> 01 design system ──> 02,03,04,05,06,07,09,10,11 (all UI)
           └─> 16 architecture ─> 17 data model ─> 12 order lifecycle ─> 13 payments ─> 14 delivery
20 devops (parallel from day 1)        08 onboarding ─> 09 storefront ─> 10 dashboard
21 testing (parallel from day 1)       15 notifications (needed by 08, 12, 13, 14)
18 security / 19 NFR (rules apply from day 1, audit in M5)
```

## What is explicitly NOT in MVP
- Platform-run logistics / warehouses
- Customer-to-vendor chat (use order notes + support tickets instead)
- Coupons per vendor (platform-wide coupons only, P2)
- Multi-currency / international shipping
- AR try-on, reels, Instagram import (P2)
- Native apps (P3; the web is a PWA in the meantime)
