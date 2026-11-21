# Validation — 10 Vendor Dashboard

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-10-01 | T-10-01 | Playwright | | | |
| V-10-02 | T-10-02 | Playwright + manual | | | |
| V-10-03 | T-10-03 | User test | | | |
| V-10-04 | T-10-04 | Automated | | | |
| V-10-05 | T-10-05 | Automated | | | |
| V-10-06 | T-10-06 | E2E | | | |
| V-10-07 | T-10-07 | Automated reconciliation | | | |
| V-10-08 | T-10-08 | E2E | | | |
| V-10-09 | T-10-09 | Automated | | | |
| V-10-10 | T-10-10 | Automated (API) | | | |
| V-10-11 | T-10-11 | Playwright | | | |

### V-10-01 — Access
- **Pass criteria:** Customer-only account gets 403 on vendor portal; vendor sees only own data.

### V-10-02 — Own dashboard
- **Steps:** Hide 2 widgets, move "Payouts" to top, resize "Sales trend" to L; log in on another device.
- **Pass criteria:** Same layout appears; reset restores default; forcing a widget API error shows that widget's error state only.

### V-10-03 — Product creation
- **Steps:** 3 pilot vendors add a product with variants on their phone.
- **Pass criteria:** Median ≤ 5 min; required attributes enforced per category.

### V-10-04 — Bulk upload
- **Case:** 500 rows with 20 deliberate errors.
- **Pass criteria:** 480 imported, 20 reported with correct row/field messages; processing ≤ 5 min.

### V-10-05 — Pricing rules
- **Pass criteria:** Price > MRP rejected; 60% change asks confirmation; MRP change logged.

### V-10-06 — Orders flow
- **Pass criteria:** Accept → To dispatch; dispatch without tracking ID blocked; with ID → Shipped, customer notified; reject → refund of that vendor order (13), score impacted.

### V-10-07 — Payout accuracy
- **Pass criteria:** For 20 seeded orders, payout page values = ledger values = gateway transfers (0 paise difference).

### V-10-08 — Settings propagation
- **Pass criteria:** Change free-shipping threshold → cart (06) reflects it immediately.

### V-10-09 — Score
- **Pass criteria:** Seeded history produces expected score (hand-calculated); ranking input updated nightly.

### V-10-10 — Permissions
- **Pass criteria:** Staff-Catalog calling payouts API → 403; Staff-Orders editing price → 403.

### V-10-11 — Quality gate
- **Pass criteria:** Day-5 vendor product → moderation; day-40 vendor product → published instantly.

## Module sign-off
- [ ] All checks Pass
- [ ] 3 pilot vendors rate portal ≥ 4/5 for ease of use
