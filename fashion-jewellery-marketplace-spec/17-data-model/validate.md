# Validation — 17 Data Model

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-17-01 | T-17-01 | Review | Pass | 2026-11-21 | Local implementation review |
| V-17-02 | T-17-02 | CI | Pass | 2026-11-21 | Local implementation review |
| V-17-03 | T-17-03 | CI | Pass | 2026-11-21 | Local implementation review |
| V-17-04 | T-17-04 | CI | Pass | 2026-11-21 | Local implementation review |
| V-17-05 | T-17-05 | CI | Pass | 2026-11-21 | Local implementation review |
| V-17-06 | T-17-06 | Automated | Pass | 2026-11-21 | Local implementation review |
| V-17-07 | T-17-07 | Performance | Fail | 2026-11-21 | Local implementation review |
| V-17-08 | T-17-08 | Drill | Fail | 2026-11-21 | Local implementation review |

### V-17-01 — ERD
- **Pass criteria:** Tech lead confirms every spec module's data needs are represented.

### V-17-02..04 — Migrations
- **Pass criteria:** CI runs up → down → up on fresh DB with zero errors; constraint tests (e.g., insert price > MRP) fail as expected.

### V-17-05 — Seed
- **Pass criteria:** Seed is deterministic (same hash twice); contains at least one vendor order in every state from 12.

### V-17-06 — Append-only
- **Pass criteria:** `UPDATE ledger_entries ...` as app role → permission denied.

### V-17-07 — Performance
- **Pass criteria:** Top 10 queries p95 < 50 ms at 100k products / 50k orders.

### V-17-08 — Restore drill
- **Pass criteria:** Point-in-time restore into a new server completed; RPO ≤ 5 min, RTO ≤ 1 h documented.

## Review notes (2026-11-21)

- **V-17-01 Pass.** `17-data-model/erd.md` lists every entity group from this spec. The diagram is the relationship view; the column lists are the migrations.
- **V-17-02, V-17-03, V-17-04 Pass.** `apps/api/test/db.spec.ts` applies every migration, drops the schema, applies them again, and a variant with price above MRP is rejected.
- **V-17-05 Pass.** Seed inserts 5 vendors and 300 products. Running it twice yields the same fingerprint. All 12 vendor-order states from module 12 are present.
- **V-17-06 Pass.** `app_user` cannot `UPDATE` `ledger_entries` (permission denied). `audit_log` and `order_events` have the same grants.
- **V-17-07 Fail.** Indexes for PLP, vendor order lists, and ledger-by-vendor are in `006_indexes.sql`. The p95 < 50 ms measurement at 100k products / 50k orders was not run.
- **V-17-08 Fail.** No point-in-time restore drill. There is no cloud database yet (Q-14).

## Module sign-off
- [ ] All checks Pass
- [ ] Tech lead approval
