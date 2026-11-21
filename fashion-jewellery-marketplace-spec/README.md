# Fashion Jewellery Marketplace — Product & Technical Specification

**Version:** 0.1 (draft) · **Date:** 14 Nov 2026 · **Status:** For review
**Working name:** _TBD_ (see `OPEN-QUESTIONS.md` → Q-01)

A multi-vendor marketplace (like Amazon/Flipkart, but much simpler and more premium) **only for fashion / imitation jewellery**. Many independent vendors (tenants) list products; customers buy from several vendors in one cart; **each vendor ships their own orders**; the platform takes a fee and settles vendor payouts in tranches tied to dispatch and delivery.

Web first (responsive, mobile-first), mobile apps later on the same API.

---

## How this folder works

Every module is a folder. Every folder contains three files:

| File | Purpose |
|---|---|
| `spec.md` | **What** to build and **why** — scope, user stories, rules, UI, data, edge cases |
| `task.md` | **How** it gets built — numbered tasks (`T-<module>-<n>`), dependencies, size, definition of done |
| `validate.md` | **Proof** it works — one check per task (`V-<module>-<n>`), steps, expected result, pass criteria, module sign-off |

Task `T-06-03` is always validated by `V-06-03`. A task is **Done** only when its validation passes.

### Root files

| File | Purpose |
|---|---|
| `ROADMAP.md` | Phases, milestones, build order |
| `OPEN-QUESTIONS.md` | Business decisions you must make before/while building (with recommendations) |
| `GLOSSARY.md` | Shared vocabulary (tenant, vendor order, tranche, etc.) |
| `TRACKER.md` | Every task across all modules in one table — update status here |
| `_templates/` | Copy these to add a new module |

---

## Module index

| # | Module | Audience | Phase |
|---|---|---|---|
| 00 | [Product vision](00-product-vision/spec.md) | All | P0 |
| 01 | [Design system](01-design-system/spec.md) | All | P0 |
| 02 | [Intro experience (video welcome)](02-intro-experience/spec.md) | Customer | P1 |
| 03 | [Customer accounts](03-customer-accounts/spec.md) | Customer | P1 |
| 04 | [Catalog & discovery](04-catalog-and-discovery/spec.md) | Customer | P1 |
| 05 | [Product page](05-product-page/spec.md) | Customer | P1 |
| 06 | [Cart & checkout (multi-vendor)](06-cart-and-checkout/spec.md) | Customer | P1 |
| 07 | [Customer orders, returns, reviews](07-customer-orders-returns-reviews/spec.md) | Customer | P1 |
| 08 | [Vendor onboarding & KYC](08-vendor-onboarding/spec.md) | Vendor | P1 |
| 09 | [Vendor storefront](09-vendor-storefront/spec.md) | Vendor / Customer | P1 |
| 10 | [Vendor dashboard](10-vendor-dashboard/spec.md) | Vendor | P1 |
| 11 | [Platform admin](11-platform-admin/spec.md) | Platform team | P1 |
| 12 | [Order lifecycle (state machine)](12-order-lifecycle/spec.md) | System | P1 |
| 13 | [Payments, commission & settlement](13-payments-and-settlement/spec.md) | System | P1 |
| 14 | [Delivery confirmation](14-delivery-confirmation/spec.md) | System | P1 |
| 15 | [Notifications](15-notifications/spec.md) | System | P1 |
| 16 | [Architecture & API](16-architecture-and-api/spec.md) | Engineering | P0 |
| 17 | [Data model](17-data-model/spec.md) | Engineering | P0 |
| 18 | [Security, privacy & compliance](18-security-privacy-compliance/spec.md) | Engineering / Legal | P0–P1 |
| 19 | [Non-functional requirements & analytics](19-non-functional-and-analytics/spec.md) | Engineering | P0–P1 |
| 20 | [DevOps & infrastructure](20-devops-and-infrastructure/spec.md) | Engineering | P0 |
| 21 | [Testing strategy](21-testing-strategy/spec.md) | Engineering | P0–P1 |
| 22 | [Launch & vendor acquisition](22-launch-and-vendor-acquisition/spec.md) | Business | P1 |
| 23 | [Growth features (try-on, reels, Instagram import)](23-growth-features/spec.md) | Customer / Vendor | P2 |
| 24 | [Mobile apps](24-mobile-apps/spec.md) | Customer / Vendor | P3 |

### Phases
- **P0 – Foundations:** design system, architecture, data model, infra, CI/CD.
- **P1 – MVP web launch:** everything needed for real vendors to sell and real customers to buy.
- **P2 – Growth:** differentiators (AR try-on, shoppable reels, Instagram import, AI "complete the look").
- **P3 – Mobile:** iOS/Android apps on the same API.

---

## Global Definition of Done (applies to every task)
1. Code merged to `main` via reviewed PR; CI green.
2. The matching `V-xx-yy` validation passes in **staging**.
3. Unit/integration tests added where logic exists; no drop in coverage.
4. Works on mobile (360 px), tablet, and desktop (1440 px).
5. Meets accessibility baseline (WCAG 2.2 AA) for any UI.
6. API changes reflected in OpenAPI spec; data changes in migrations.
7. `TRACKER.md` status updated.

## Local implementation

The runnable monorepo sits next to these spec folders: `apps/` (customer web, vendor, admin, API, worker) and `packages/` (events, payments, media, tokens, ui, api-client). Decisions are in `adr/`. Local services are in `infra/docker-compose.yml` (Postgres, Redis, Meilisearch, MinIO). Tests use in-process Postgres when Docker is not running.

```
pnpm install
pnpm test
pnpm build
pnpm dev:api
pnpm dev:web
```

Copy `.env.example` to `.env` before pointing the API at Compose. Do not use live payment keys.

## Core principles
- **One look for everyone.** The platform owns the design. Vendors own their *content* (products, prices, photos, store bio) — never page layout or theme.
- **Simple over complete.** If Amazon has a feature and our customer doesn't miss it, we don't build it.
- **Trust is the product.** Verified vendors, clear delivery proof, money held safely until delivery.
- **API-first.** Every screen is backed by a documented API so the mobile apps reuse it unchanged.
