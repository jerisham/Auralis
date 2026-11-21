# Validation — 11 Platform Admin

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-11-01 | T-11-01 | Automated (API) | | | |
| V-11-02 | T-11-02 | E2E | | | |
| V-11-03 | T-11-03 | E2E | | | |
| V-11-04 | T-11-04 | Automated | | | |
| V-11-05 | T-11-05 | E2E | | | |
| V-11-06 | T-11-06 | Sandbox E2E | | | |
| V-11-07 | T-11-07 | Manual | | | |
| V-11-08 | T-11-08 | Sandbox | | | |
| V-11-09 | T-11-09 | Automated (data check) | | | |
| V-11-10 | T-11-10 | E2E | | | |
| V-11-11 | T-11-11 | Automated | | | |
| V-11-12 | T-11-12 | E2E | | | |

### V-11-01 — RBAC & 2FA
- **Pass criteria:** Each role matrix cell tested via API (allowed → 2xx, denied → 403); login without TOTP impossible.

### V-11-02 — Applications
- **Pass criteria:** Approve triggers full 08 activation (V-08-09) with no extra steps.

### V-11-03 — Strikes & suspension
- **Steps:** Simulate 3 auto-cancels in 30 days.
- **Pass criteria:** 3 strikes → auto 7-day suspension; products gone from search ≤ 60 s; vendor notified.

### V-11-04 — Commission precedence
- **Cases:** Global 20%, Earrings 15%, Vendor X override 12%.
- **Pass criteria:** X earrings → 12%; Y earrings → 15%; Y necklace → 20%; rule change tomorrow doesn't affect today's orders.

### V-11-05 — Moderation
- **Pass criteria:** Reported product appears in queue; rejection reason delivered to vendor; bulk approve of 20 items works.

### V-11-06 — Dispute decision
- **Pass criteria:** Admin refund decision → gateway refund created, ledger balanced, both parties notified, audit entry present.

### V-11-07 — CMS
- **Pass criteria:** Non-technical team member updates hero, creates a look and schedules a banner without help.

### V-11-08 — Finance console
- **Pass criteria:** Simulated failed transfer shows in console; retry succeeds; manual hold blocks automatic release.

### V-11-09 — KPIs
- **Pass criteria:** GMV and order counts match SQL query on seeded data exactly.

### V-11-10 — Config live
- **Pass criteria:** Change dispatch SLA 72 h → 48 h; next new order uses 48 h; existing orders unchanged.

### V-11-11 — Audit immutability
- **Pass criteria:** DB role used by app cannot UPDATE/DELETE audit rows (permission test).

### V-11-12 — Taxonomy
- **Pass criteria:** New attribute appears in vendor form and PLP filters.

## Module sign-off
- [ ] All checks Pass
- [ ] Ops + Finance leads approval
