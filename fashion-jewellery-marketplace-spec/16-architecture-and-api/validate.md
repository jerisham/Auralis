# Validation — 16 Architecture & API

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-16-01 | T-16-01 | Review | Pass | 2026-11-21 | Local implementation review |
| V-16-02 | T-16-02 | CI | Pass | 2026-11-21 | Local implementation review |
| V-16-03 | T-16-03 | Automated | Pass | 2026-11-21 | Local implementation review |
| V-16-04 | T-16-04 | Automated (security) | Pass | 2026-11-21 | Local implementation review |
| V-16-05 | T-16-05 | Chaos test | Pass | 2026-11-21 | Local implementation review |
| V-16-06 | T-16-06 | Automated | Pass | 2026-11-21 | Local implementation review |
| V-16-07 | T-16-07 | Automated | Fail | 2026-11-21 | Local implementation review |
| V-16-08 | T-16-08 | E2E | Fail | 2026-11-21 | Local implementation review |
| V-16-09 | T-16-09 | CI | Pass | 2026-11-21 | Local implementation review |
| V-16-10 | T-16-10 | Automated | Pass | 2026-11-21 | Local implementation review |
| V-16-11 | T-16-11 | Lighthouse | Fail | 2026-11-21 | Local implementation review |

### V-16-01 — ADRs
- **Pass criteria:** Reviewed by tech lead; each decision has cost estimate and exit strategy.

### V-16-02 — Monorepo
- **Pass criteria:** Fresh clone → one command installs and builds everything in CI < 10 min.

### V-16-03 — Foundation
- **Pass criteria:** Unauthenticated → 401; wrong role → 403; duplicate Idempotency-Key → same response; > limit → 429; errors match problem+json schema.

### V-16-04 — Tenant isolation (critical)
- **Steps:** As vendor A, attempt to read/update vendor B's product/order via API (ID guessing) and via a deliberately unscoped repository query in a test.
- **Pass criteria:** 0 rows returned / 404 in all attempts.

### V-16-05 — Event reliability
- **Steps:** Kill workers mid-processing; poison message.
- **Pass criteria:** No lost events; poison message lands in DLQ with alert; no duplicate side-effects.

### V-16-06 — Media
- **Pass criteria:** Renditions present; EXIF GPS removed; 800×800 upload rejected with clear error.

### V-16-07 — Payment fake
- **Pass criteria:** Same contract tests pass against fake and sandbox (V-13-01).

### V-16-08 — Config
- **Pass criteria:** Change return window in admin → used by next DELIVERED order within 60 s.

### V-16-09 — API docs
- **Pass criteria:** Removing a field in a PR triggers breaking-change failure.

### V-16-10 — Webhooks
- **Pass criteria:** Invalid signature stored as rejected; reprocess works.

### V-16-11 — PWA
- **Pass criteria:** Installable on Android; offline page renders.

## Review notes (2026-11-21)

Local stand-in for staging, because Q-14 keeps hosting local and this machine has no Docker daemon. Database tests use PGlite (Postgres in-process). `pnpm test` and `pnpm build` both succeeded.

- **V-16-01 Pass.** `adr/0001`–`0004` choose NestJS, Meilisearch, BullMQ (in-memory in tests), and local hosting. Each record has a cost and an exit.
- **V-16-02 Pass.** One `pnpm install` and one `pnpm build` compile the web apps, API, worker, and packages. GitHub Actions in `.github/workflows/ci.yml` runs the same commands. The workflow has not executed on a GitHub remote yet.
- **V-16-03 Pass.** Missing token → 401 problem+json; customer on an admin route → 403; duplicate Idempotency-Key returns the same body; a third call over the limit → 429 with Retry-After.
- **V-16-04 Pass.** As vendor B, `SELECT` of vendor A's product by id returns 0 rows, and an unscoped `SELECT` returns only B's 60 products.
- **V-16-05 Pass.** A row left unpublished is still in the outbox; a poison job reaches the dead-letter list and raises an alert; the same job id applies once.
- **V-16-06 Pass.** An 800×800 JPEG is rejected. A 1200×1200 JPEG with EXIF yields 8 renditions (WebP and AVIF at 200/400/800/1200) in under 30s, and the output has no EXIF. Files over 15 MB are rejected.
- **V-16-07 Fail.** The fake provider passes the shared contract. Razorpay sandbox is not configured, so the sandbox half of this check is open.
- **V-16-08 Fail.** Config reads stay cached for 60s and a super-admin patch updates `return_window_hours`. No DELIVERED order consumes that value yet (module 12).
- **V-16-09 Pass.** Removing a response property is reported as a breaking change. `pnpm --filter @auralis/api openapi:check` passes against `apps/api/openapi.json`.
- **V-16-10 Pass.** A bad signature is stored as `rejected` and returns 401. A failed webhook reprocesses to `processed`. Rows older than 90 days are purged.
- **V-16-11 Fail.** Manifest, service worker, and offline page are present and covered by a file test. Lighthouse and an Android install were not run.

## Module sign-off
- [ ] All checks Pass
- [ ] Tech lead approval
