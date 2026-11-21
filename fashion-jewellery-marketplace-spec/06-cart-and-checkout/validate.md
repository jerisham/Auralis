# Validation — 06 Cart & Checkout

All payment tests use gateway **sandbox/test mode**.

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-06-01 | T-06-01 | Automated | | | |
| V-06-02 | T-06-02 | Automated | | | |
| V-06-03 | T-06-03 | Playwright | | | |
| V-06-04 | T-06-04 | Playwright | | | |
| V-06-05 | T-06-05 | Automated (concurrency) | | | |
| V-06-06 | T-06-06 | Sandbox E2E | | | |
| V-06-07 | T-06-07 | Sandbox E2E | | | |
| V-06-08 | T-06-08 | Manual | | | |
| V-06-09 | T-06-09 | Automated | | | |

### V-06-01 — Cart API
- **Pass criteria:** 11th distinct item rejected; 6th unit of SKU rejected; grouping and totals correct for 3-vendor cart.

### V-06-02 — Shipping
- **Case:** Vendor A fee ₹60, free above ₹999; cart A = ₹500.
- **Pass criteria:** Shipping ₹60; nudge "Add ₹499 more for free shipping"; at ₹999 → free.

### V-06-03 — Cart UI
- **Pass criteria:** Change price in admin → cart shows "Price updated" banner; banner "ships in 2 packages from 2 sellers" correct.

### V-06-04 — Serviceability
- **Case:** Vendor B excludes PIN 79xxxx; address PIN 791001.
- **Pass criteria:** Vendor B group flagged; Pay disabled until removed.

### V-06-05 — Reservation race
- **Steps:** Stock = 1; 20 parallel order-create requests from different users.
- **Pass criteria:** Exactly 1 succeeds; others get "out of stock"; repeated request with same Idempotency-Key returns same order.

### V-06-06 — Split payment
- **Steps:** Pay ₹1,760 for 2-vendor cart via UPI test.
- **Pass criteria:** Gateway dashboard shows transfers to both linked accounts with correct amounts (per 13 formula) and on-hold flags.

### V-06-07 — Webhook confirmation
- **Scenarios:** success; failure; close browser before redirect; webhook delivered twice.
- **Pass criteria:** Success → PAID once; failure → stock released; closed browser → still PAID + notification; duplicate webhook → no duplicate effects.

### V-06-08 — Confirmation
- **Pass criteria:** Page and messages list each vendor package and dates.

### V-06-09 — Expiry
- **Pass criteria:** Unpaid reservation released at 15 min (± 1 min); late success with stock available → PAID; without stock → auto-refund initiated and customer notified.

## Module sign-off
- [ ] All checks Pass
- [ ] Finance reviewer confirms amounts
