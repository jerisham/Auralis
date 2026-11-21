# Validation — 12 Order Lifecycle

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-12-01 | T-12-01 | Automated (property tests) | | | |
| V-12-02 | T-12-02 | Automated (API) | | | |
| V-12-03 | T-12-03 | Automated (time-travel) | | | |
| V-12-04 | T-12-04 | Automated (chaos) | | | |
| V-12-05 | T-12-05 | Automated | | | |
| V-12-06 | T-12-06 | Automated | | | |
| V-12-07 | T-12-07 | CI check | | | |

### V-12-01 — Legal transitions only
- **Steps:** Generate every (state, trigger) pair.
- **Pass criteria:** Pairs in §4 succeed; all others return IllegalTransition; 100% transition coverage.

### V-12-02 — Actor permissions
- **Pass criteria:** Vendor B cannot accept Vendor A's order (403); customer cannot dispatch; cancel after dispatch returns 409.

### V-12-03 — Timers
- **Scenarios (simulated clock):** no accept in 24 h → CANCELLED_SLA; dispatched with no tracking updates → prompt at +7 d, DELIVERED at +10 d; delivered + 48 h → COMPLETED; restart service mid-timer → still fires once.

### V-12-04 — Exactly-once effects
- **Steps:** Kill relay process during publish; send duplicate dispatch requests.
- **Pass criteria:** T1 released once; customer notified once; no lost events (outbox drained).

### V-12-05 — History & derived status
- **Pass criteria:** 3-vendor order where one rejected, two completed → Order = PARTIALLY_FULFILLED; timeline complete.

### V-12-06 — Override
- **Pass criteria:** Override requires reason; audit row present with before/after.

### V-12-07 — Docs in sync
- **Pass criteria:** CI fails if transitions table changes without regenerating the diagram.

## Module sign-off
- [ ] All checks Pass
- [ ] Tech lead approval
