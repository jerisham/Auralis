# Validation — 01 Design System

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-01-01 | T-01-01 | Review | | | |
| V-01-02 | T-01-02 | User test | | | |
| V-01-03 | T-01-03 | Review | | | |
| V-01-04 | T-01-04 | Review | | | |
| V-01-05 | T-01-05 | Review + user test | | | |
| V-01-06 | T-01-06 | Automated | | | |
| V-01-07 | T-01-07 | Automated + review | | | |
| V-01-08 | T-01-08 | Automated + manual | | | |
| V-01-09 | T-01-09 | Review | | | |

### V-01-01 — Brand assets
- **Pass criteria:** Logo legible at 24px height on both dark and light; trademark search shows no conflicting mark in class 14/35.

### V-01-02 — Direction test
- **Steps:** Show both directions to 5 target customers; ask "Which feels more premium? Which would you trust to buy from?"
- **Pass criteria:** Chosen direction preferred by ≥ 4/5.

### V-01-03 — Tokens
- **Pass criteria:** Every colour pair used for text passes AA (checked with a contrast tool); dark & light modes switch with no hard-coded colours.

### V-01-04 — Components complete
- **Pass criteria:** Checklist of §3 components 100% present with all states.

### V-01-05 — Templates usability
- **Steps:** 5-second test + "find earrings under ₹500" task on PLP prototype with 5 users.
- **Pass criteria:** ≥ 4/5 describe the site as "premium/elegant"; ≥ 4/5 complete the task < 30 s.

### V-01-06 — Token pipeline
- **Steps:** Change `--gold-500` in JSON, run build.
- **Pass criteria:** CSS, TS and RN outputs all contain the new value; CI job green.

### V-01-07 — Component library
- **Pass criteria:** Storybook builds in CI; every component has a story and a passing test; visual regression baseline captured.

### V-01-08 — Accessibility
- **Pass criteria:** axe: 0 serious/critical; all interactive components reachable and operable by keyboard; reduced-motion disables animations.

### V-01-09 — Photo guidelines
- **Pass criteria:** 3 pilot vendors read it and produce compliant photos without extra help.

## Module sign-off
- [ ] All checks Pass
- [ ] Design lead + product owner approval
