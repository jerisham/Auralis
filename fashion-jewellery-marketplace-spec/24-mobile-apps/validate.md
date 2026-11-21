# Validation — 24 Mobile Apps

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-24-01 | T-24-01 | CI | | | |
| V-24-02 | T-24-02 | Device testing | | | |
| V-24-03 | T-24-03 | Sandbox E2E (Detox/Maestro) | | | |
| V-24-04 | T-24-04 | Device testing | | | |
| V-24-05 | T-24-05 | Device testing | | | |
| V-24-06 | T-24-06 | Device testing | | | |
| V-24-07 | T-24-07 | Store review | | | |
| V-24-08 | T-24-08 | Metrics | | | |
| V-24-09 | T-24-09 | Release | | | |

### V-24-01 — Builds
- **Pass criteria:** CI produces installable builds for both platforms; changing a token updates app theme.

### V-24-02 — Browsing
- **Pass criteria:** Screens match web behaviour (same API responses); cold start ≤ 2.5 s on mid-range Android.

### V-24-03 — Purchase
- **Pass criteria:** Multi-vendor order paid via UPI intent (Android) and card (iOS) in sandbox; appears identically on web.

### V-24-04 — Push
- **Pass criteria:** Delivered with app killed, backgrounded, foregrounded; tapping opens correct screen.

### V-24-05 — Links
- **Pass criteria:** Links open app when installed, web when not, on both platforms.

### V-24-06 — Vendor app
- **Pass criteria:** Accept + dispatch with scanned tracking in ≤ 30 s; T1 released per 13.

### V-24-07 — Store review
- **Pass criteria:** Both stores approve without rejection for privacy/data reasons.

### V-24-08 — Beta quality
- **Pass criteria:** Crash-free sessions ≥ 99.5%; beta NPS ≥ 40.

### V-24-09 — Release
- **Pass criteria:** Public listings live; an OTA fix reaches ≥ 80% of users within 48 h.

## Module sign-off
- [ ] All checks Pass
- [ ] Product owner approval
