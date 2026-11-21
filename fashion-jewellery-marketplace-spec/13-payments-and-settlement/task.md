# Tasks — 13 Payments, Commission & Settlement

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-13-01 | Gateway account + marketplace/split product activation; `PaymentProvider` interface (T-16-07) implementation | Q-05, T-16-07 | M | Todo |
| T-13-02 | Checkout order creation with amounts calc (§3) and held T1/T2 transfers | T-13-01, T-13-04 | L | Todo |
| T-13-03 | Webhook handler (signature, idempotency, event routing) | T-13-01 | M | Todo |
| T-13-04 | Ledger: schema, posting service, invariants, amount calculator with rule snapshots | T-17-04 | L | Todo |
| T-13-05 | Refunds, transfer reversals, vendor receivables & netting | T-13-04 | L | Todo |
| T-13-06 | Tranche release engine (listens to 12 events; pause/hold logic) | T-12-04, T-13-02 | M | Todo |
| T-13-07 | Invoices: customer invoice (on vendor's behalf), commission invoice, numbering series | T-13-04 | M | Todo |
| T-13-08 | Vendor linked-account creation & status sync (used by 08) | T-13-01 | M | Todo |
| T-13-09 | Daily reconciliation job + mismatch alerts | T-13-04 | M | Todo |
| T-13-10 | Vendor statements + statutory TCS/TDS reports | T-13-04 | M | Todo |
| T-13-11 | CA review of formulas, invoices and reports | T-13-07, T-13-10 | S | Todo |

---

### T-13-01 — Gateway foundation
- **Done when:** Sandbox keys in Key Vault; interface methods implemented and contract-tested.

### T-13-02 — Checkout amounts & transfers
- **Done when:** For any cart, transfers sum + platform share = captured amount exactly (paise).

### T-13-03 — Webhooks
- **Done when:** Invalid signature → 401; duplicate event → 200 no-op; unknown event logged.

### T-13-04 — Ledger
- **Steps:** Posting templates per event (capture, release T1, release T2, refund, reversal, receivable, netting); DB constraint/trigger ensures balance per txn.
- **Done when:** Property tests: random event sequences never break invariants.

### T-13-05 — Refunds & recoveries
- **Done when:** Every row in §5 table implemented with tests.

### T-13-06 — Release engine
- **Done when:** DISPATCHED → T1 released; COMPLETED → T2 released; claim freezes T2; pause queues releases.

### T-13-07 — Invoices
- **Done when:** Sequential invoice numbers per vendor per financial year; PDFs generated; stored immutably.

### T-13-08 — Linked accounts
- **Done when:** Created from verified KYC/bank data; status webhook updates vendor payout status.

### T-13-09 — Reconciliation
- **Done when:** Daily report; any mismatch alerts Finance (15) and appears in console (11).

### T-13-10 — Statements & reports
- **Done when:** Monthly statement per vendor; TCS/TDS report exportable per period.

### T-13-11 — CA sign-off
- **Done when:** Written CA confirmation of rates, invoice format, and report format attached in this folder.
