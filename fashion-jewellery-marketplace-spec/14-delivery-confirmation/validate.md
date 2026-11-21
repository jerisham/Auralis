# Validation — 14 Delivery Confirmation

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-14-01 | T-14-01 | Automated | | | |
| V-14-02 | T-14-02 | Playwright | | | |
| V-14-03 | T-14-03 | Sandbox | | | |
| V-14-04 | T-14-04 | Time-travel | | | |
| V-14-05 | T-14-05 | Time-travel | | | |
| V-14-06 | T-14-06 | E2E | | | |
| V-14-07 | T-14-07 | E2E (P2) | | | |

### V-14-01 — Dispatch validation
- **Pass criteria:** Bad format for selected courier rejected; hand delivery without OTP/confirmation cannot become DELIVERED automatically.

### V-14-02 — Customer confirmation
- **Pass criteria:** "I received it" → DELIVERED + return window starts; "Not received" opens claim.

### V-14-03 — Tracking
- **Steps:** Use aggregator test tracking numbers or recorded webhook payloads for 5 couriers.
- **Pass criteria:** Correct normalised statuses; DELIVERED triggers 12 transition exactly once.

### V-14-04 — Verification
- **Pass criteria:** Fake tracking ID → vendor warning at 24 h, admin flag at 48 h.

### V-14-05 — Auto-confirm
- **Pass criteria:** Prompt sent at +7 d; DELIVERED at +10 d; open claim prevents auto-confirm.

### V-14-06 — RTO
- **Pass criteria:** RTO event → admin task + customer notification; decision posts correct ledger entries.

### V-14-07 — OTP (P2)
- **Pass criteria:** Wrong OTP rejected (3 attempts); correct OTP → DELIVERED.

## Module sign-off
- [ ] All checks Pass
- [ ] Ops lead approval
