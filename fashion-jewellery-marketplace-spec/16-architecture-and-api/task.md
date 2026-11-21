# Tasks — 16 Architecture & API

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-16-01 | Architecture Decision Records (ADRs): backend framework, search, queue, hosting | — | S | Done |
| T-16-02 | Monorepo scaffold (web apps, api, workers, packages/ui, packages/api-client, tokens) | T-16-01, T-20-01 | M | Done |
| T-16-03 | API foundation: modules, auth middleware, RBAC guards, problem+json errors, idempotency, rate limiting | T-16-02 | L | Done |
| T-16-04 | Multi-tenancy with PostgreSQL RLS + tenant context per request | T-17-02 | M | Done |
| T-16-05 | Event backbone: outbox table, relay, queue, scheduler, consumer framework; search infra | T-16-03 | L | Done |
| T-16-06 | Media pipeline (signed upload, processing worker, CDN) | T-16-05, T-20-03 | M | Done |
| T-16-07 | `PaymentProvider` interface + fake provider for tests | T-16-03 | S | Todo |
| T-16-08 | Runtime config + feature flags | T-16-03 | S | Todo |
| T-16-09 | OpenAPI generation + typed client package + published docs | T-16-03 | S | Done |
| T-16-10 | Webhook ingestion framework (verify, store raw, async process) | T-16-05 | S | Done |
| T-16-11 | PWA shell (manifest, service worker, offline page, install prompt) | T-16-02 | S | Todo |

---

### T-16-01 — ADRs
- **Done when:** `adr/0001..000N.md` each with context, options, decision, consequences.

### T-16-02 — Monorepo
- **Done when:** `pnpm`/Turborepo (or Nx) workspace builds all apps; lint, typecheck, test commands at root.

### T-16-03 — API foundation
- **Done when:** Health endpoint, auth guard, role guard, error format, Idempotency-Key middleware, rate limiter — all tested.

### T-16-04 — RLS
- **Done when:** Policies on all vendor-owned tables; tenant context set per transaction; cross-tenant test suite passes.

### T-16-05 — Events
- **Done when:** Outbox → queue → consumer with retry, DLQ, idempotency store; scheduled messages for timers.

### T-16-06 — Media
- **Done when:** Upload 5 MB JPEG → 8 renditions on CDN in ≤ 30 s.

### T-16-07 — Payment interface
- **Done when:** Interface + in-memory fake used by all non-sandbox tests.

### T-16-08 — Config & flags
- **Done when:** Values changeable in admin (11) and effective within 60 s.

### T-16-09 — OpenAPI
- **Done when:** CI publishes spec; breaking-change check against `main` blocks PRs.

### T-16-10 — Webhooks
- **Done when:** Raw payloads retained 90 days; reprocess button for admins.

### T-16-11 — PWA
- **Done when:** Lighthouse PWA installable; offline page shown without network.
