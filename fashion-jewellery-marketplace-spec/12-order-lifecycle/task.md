# Tasks — 12 Order Lifecycle

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-12-01 | State machine engine (states, transitions table, guards, illegal-transition errors) | T-17-03 | M | Todo |
| T-12-02 | Transition API endpoints for vendor/customer/admin actors with permission checks | T-12-01, T-16-03 | M | Todo |
| T-12-03 | Timer/scheduler service for SLAs, reminders, auto-deliver, return window | T-16-05 | M | Todo |
| T-12-04 | Outbox events for every transition (consumed by 13, 14, 15, 19) | T-16-05 | M | Todo |
| T-12-05 | Order events history + derived Order status | T-12-01 | S | Todo |
| T-12-06 | Admin override with reason + audit | T-11-11 | S | Todo |
| T-12-07 | State diagram doc (`state-diagram.md`, Mermaid) kept in sync with code | T-12-01 | S | Todo |

---

### T-12-01 — Engine
- **Steps:** Transitions defined as data (single source); generate docs/tests from it.
- **Done when:** All rows of §4 implemented; any other transition throws `IllegalTransition`.

### T-12-02 — API
- **Done when:** `POST /v1/vendor-orders/{id}/accept|reject|dispatch`, `/v1/orders/{id}/vendor-orders/{vid}/cancel|received|claim`, `/v1/admin/vendor-orders/{id}/transition`.

### T-12-03 — Timers
- **Steps:** Durable scheduled jobs (DB-backed or queue with delayed jobs); idempotent handlers; survive restarts.
- **Done when:** Each §5 timer fires once, even if service restarts between scheduling and firing.

### T-12-04 — Outbox
- **Done when:** Event written in same transaction as state change; relay publishes at-least-once; consumers idempotent.

### T-12-05 — History
- **Done when:** Timeline API returns ordered events; Order status derivation rules unit-tested.

### T-12-06 — Override
- **Done when:** Override without reason rejected; audit entry created.

### T-12-07 — Diagram
- **Done when:** Mermaid diagram generated from transitions table in CI.
