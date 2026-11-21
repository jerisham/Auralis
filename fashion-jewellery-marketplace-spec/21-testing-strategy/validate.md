# Validation — 21 Testing Strategy

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-21-01 | T-21-01 | CI | | | |
| V-21-02 | T-21-02 | CI | | | |
| V-21-03 | T-21-03 | CI | | | |
| V-21-04 | T-21-04 | Automated | | | |
| V-21-05 | T-21-05 | Run | | | |
| V-21-06 | T-21-06 | CI | | | |
| V-21-07 | T-21-07 | Review | | | |
| V-21-08 | T-21-08 | Drill | | | |

### V-21-01 — Frameworks
- **Pass criteria:** Integration test spins up Postgres container in CI and passes.

### V-21-02 — Playwright
- **Pass criteria:** Deliberately failing test produces trace + video artefacts.

### V-21-03 — Journeys
- **Pass criteria:** 10 consecutive green runs in staging (flakiness < 2%).

### V-21-04 — Clock safety
- **Pass criteria:** Starting prod config with test clock enabled fails fast.

### V-21-05 — Load scripts
- **Pass criteria:** Scripts reproduce V-19-06 results.

### V-21-06 — Visual & a11y
- **Pass criteria:** CSS change on product card triggers visual diff requiring approval.

### V-21-07 — UAT
- **Pass criteria:** ≥ 5 vendors and ≥ 20 customers complete UAT; Sev1/Sev2 found = fixed.

### V-21-08 — Defect flow
- **Pass criteria:** Test Sev1 issue pages on-call.

## Module sign-off
- [ ] All checks Pass
- [ ] QA lead approval
