# Validation — 13 Payments, Commission & Settlement

All tests in gateway sandbox. Amount checks are to the **paise**.

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-13-01 | T-13-01 | Contract tests | | | |
| V-13-02 | T-13-02 | Sandbox E2E | | | |
| V-13-03 | T-13-03 | Automated | | | |
| V-13-04 | T-13-04 | Property tests | | | |
| V-13-05 | T-13-05 | Sandbox E2E | | | |
| V-13-06 | T-13-06 | Sandbox E2E | | | |
| V-13-07 | T-13-07 | Manual + CA | | | |
| V-13-08 | T-13-08 | Sandbox | | | |
| V-13-09 | T-13-09 | Automated | | | |
| V-13-10 | T-13-10 | Manual | | | |
| V-13-11 | T-13-11 | Document | | | |

### V-13-01 — Interface contract
- **Pass criteria:** Same contract test suite passes against sandbox and against an in-memory fake provider.

### V-13-02 — Split accuracy (golden cases)
| Case | Expected |
|---|---|
| ₹500 item, 20%, no tax, no shipping | fee ₹100, T1 ₹300, T2 ₹100 |
| §3 tax example | values exactly as calculator spec |
| 3 vendors, mixed rules, one free shipping | Σ transfers + platform = captured |
- **Pass criteria:** All golden cases match; gateway dashboard shows held transfers.

### V-13-03 — Webhook safety
- **Pass criteria:** Forged signature rejected; replaying same event 5× produces one effect.

### V-13-04 — Ledger invariants
- **Steps:** 10,000 random event sequences.
- **Pass criteria:** Every txn balanced; vendor_payable per vendor = Σ held + released − reversed.

### V-13-05 — Refund scenarios
- **Pass criteria:** Each §5 row executed end-to-end; customer refund reflects in sandbox; vendor receivable created and netted on the vendor's next release.

### V-13-06 — Release timing
- **Pass criteria:** T1 released only after DISPATCHED; T2 only after COMPLETED; claim keeps T2 held; paused vendor's releases queue and execute after unpause.

### V-13-07 — Invoices
- **Pass criteria:** Numbering gap-free per series; CA approves sample invoices.

### V-13-08 — Linked accounts
- **Pass criteria:** Approved vendor → linked account ACTIVE; orders blocked until ACTIVE.

### V-13-09 — Reconciliation
- **Steps:** Inject a gateway transfer with no ledger entry.
- **Pass criteria:** Next run flags it; Finance alerted.

### V-13-10 — Statements
- **Pass criteria:** Statement totals = ledger totals for the vendor and month.

### V-13-11 — CA sign-off
- **Pass criteria:** Signed note present; config values updated to confirmed rates.

## Module sign-off
- [ ] All checks Pass
- [ ] Finance lead + CA approval
