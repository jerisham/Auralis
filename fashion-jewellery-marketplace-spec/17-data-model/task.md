# Tasks — 17 Data Model

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-17-01 | ERD diagram (dbdiagram/Mermaid) committed as `erd.md` | — | S | Done |
| T-17-02 | Migrations v1: identity, vendor, catalog, media | T-16-02 | M | Done |
| T-17-03 | Migrations v1: commerce (cart, orders, vendor orders, items, events, reservations, shipments, claims) | T-17-02 | M | Done |
| T-17-04 | Migrations v1: finance (payments, transfers, refunds, ledger, rules, invoices, holds, reconciliation) | T-17-03 | M | Done |
| T-17-05 | Seed & fixture data (5 vendors, 300 products, customers, orders in every state) | T-17-04 | M | Done |
| T-17-06 | Audit log + outbox + webhook tables; append-only permissions | T-17-02 | S | Done |
| T-17-07 | Indexes & query plans for hot paths (PLP, order lists, ledger by vendor) | T-17-04 | S | Todo |
| T-17-08 | Backup/restore + migration rollback procedure | T-20-03 | S | Todo |

---

### T-17-01 — ERD
- **Done when:** All §2 entities and relations drawn; reviewed.

### T-17-02 .. T-17-04 — Migrations
- **Done when:** Up/down migrations run cleanly on empty DB and on seeded DB; constraints (FKs, checks like `price <= mrp`, `debit >= 0`) present.

### T-17-05 — Seed data
- **Done when:** `make seed` produces deterministic dataset used by validations across modules.

### T-17-06 — Append-only tables
- **Done when:** App DB role lacks UPDATE/DELETE on `audit_log`, `ledger_entries`, `order_events`.

### T-17-07 — Indexes
- **Done when:** EXPLAIN for top 10 queries shows index usage; p95 < 50 ms on seeded 100k products.

### T-17-08 — Backup/restore
- **Done when:** Documented and rehearsed restore to a point in time.
