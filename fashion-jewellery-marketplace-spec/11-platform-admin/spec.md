# 11 — Platform Admin (Super Admin Portal)

**Phase:** P1 · **Depends on:** 08, 10, 12, 13 · **Status:** Draft

## 1. Purpose
The platform team's control room: approve vendors, keep catalog quality high, curate the homepage, resolve disputes, control fees and payouts, and see the health of the business. This is the role your original brief didn't name but the marketplace cannot run without.

## 2. Sections
| Section | Capabilities |
|---|---|
| **Dashboard** | GMV, orders, take rate, new vendors, SLA breaches, open disputes, payouts due, top categories |
| **Vendor applications** | Queue with KYC results, first-5 products preview; Approve / Request changes / Reject (reason templates) |
| **Vendors** | Profile, KYC, bank status, score, orders, payouts, notes; actions: suspend, unsuspend, change commission override, warning/strike, force holiday, change slug |
| **Catalog moderation** | New-vendor products, reported products, flagged store content, flagged reviews; approve/reject/edit attributes; bulk |
| **Categories & attributes** | Tree editor, attribute definitions, required flags, HSN defaults |
| **Orders** | Search by order/phone/vendor; full timeline; admin overrides (with mandatory reason, audited) |
| **Claims & disputes** | Escalated claims; evidence viewer (photos/video, tracking, courier POD); decide refund/replacement/reject; templated messages |
| **Payouts & finance** | Tranches due, holds, failed transfers (retry), vendor balances incl. negative balances, reconciliation report, commission invoices, TCS/TDS reports |
| **Homepage & media** | Intro video & hero (02), homepage sections, banners with schedule, Looks curation, featured sellers |
| **Configuration** | Commission rules, SLA timers, return window, zone transit table, cart limits, notification templates, ranking weights, feature flags |
| **Support** | Tickets from customers/vendors, linked to orders; SLA, assignment, macros |
| **Users & roles** | Admin users, roles (Ops, Catalog, Finance, Support, Super Admin), 2FA mandatory |
| **Audit log** | Every admin action: who, what, before/after, when, IP |

## 3. Vendor strike policy (default, configurable)
| Event | Strike |
|---|---|
| Missed dispatch SLA (auto-cancel) | 1 |
| Claim resolved against vendor | 1 |
| False material/skin-safety claim | 2 |
| Off-platform solicitation (asking customer to pay outside) | 3 |
3 strikes in 90 days → 7-day suspension; 6 → permanent review.

## 4. Admin RBAC
| Area | Ops | Catalog | Finance | Support | Super |
|---|---|---|---|---|---|
| Vendor approval/suspend | ✓ | — | — | — | ✓ |
| Moderation, categories | — | ✓ | — | — | ✓ |
| Orders view / override | view / ✓ | — | view | view | ✓ |
| Disputes decide | ✓ | — | — | ✓ (≤ ₹2,000) | ✓ |
| Payout release/hold, commission rules | — | — | ✓ | — | ✓ |
| Homepage & media | — | ✓ | — | — | ✓ |
| Admin users, feature flags | — | — | — | — | ✓ |

## 5. Rules
- All money-affecting actions require reason + are double-logged (audit + ledger).
- Commission rule changes apply only to **new** orders (effective-from date).
- Admin can never see full bank account numbers or card data.
