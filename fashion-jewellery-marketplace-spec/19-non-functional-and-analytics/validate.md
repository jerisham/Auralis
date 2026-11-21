# Validation — 19 Non-functional & Analytics

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-19-01 | T-19-01 | CI | | | |
| V-19-02 | T-19-02 | Drill | | | |
| V-19-03 | T-19-03 | Automated | | | |
| V-19-04 | T-19-04 | Manual + data check | | | |
| V-19-05 | T-19-05 | Automated + manual | | | |
| V-19-06 | T-19-06 | Load test | | | |
| V-19-07 | T-19-07 | Manual/BrowserStack | | | |

### V-19-01 — Budgets enforced
- **Pass criteria:** PR adding a 300 KB library to PDP fails CI.

### V-19-02 — Observability drill
- **Steps:** Inject payment-gateway errors in staging.
- **Pass criteria:** Alert fires ≤ 15 min; trace identifies failing span.

### V-19-03 — i18n
- **Pass criteria:** Pseudo-locale shows no untranslated strings on 10 key screens.

### V-19-04 — Analytics accuracy
- **Pass criteria:** Test session's events match expected list; analytics `payment_success` count = DB paid orders (±1%) for a day of test traffic; consent decline → no non-essential events.

### V-19-05 — Accessibility
- **Pass criteria:** 0 serious/critical axe issues; checkout completed with screen reader.

### V-19-06 — Load
- **Pass criteria:** Targets in §1 met at 600 RPS; error rate < 0.5%; autoscaling observed; no DB connection exhaustion.

### V-19-07 — Devices
- **Pass criteria:** Smoke suite green across matrix.

## Module sign-off
- [ ] All checks Pass
- [ ] Tech lead approval
