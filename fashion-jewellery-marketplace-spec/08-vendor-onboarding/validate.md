# Validation — 08 Vendor Onboarding & KYC

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-08-01 | T-08-01 | Manual | | | |
| V-08-02 | T-08-02 | Automated | | | |
| V-08-03 | T-08-03 | User test | | | |
| V-08-04 | T-08-04 | Sandbox | | | |
| V-08-05 | T-08-05 | Sandbox | | | |
| V-08-06 | T-08-06 | Automated | | | |
| V-08-07 | T-08-07 | Playwright | | | |
| V-08-08 | T-08-08 | Playwright | | | |
| V-08-09 | T-08-09 | Sandbox E2E | | | |
| V-08-10 | T-08-10 | Automated | | | |

### V-08-01 — Fee calculator
- **Pass criteria:** Price ₹500 with 20% commission shows "You receive ₹400"; matches 13 formula.

### V-08-02 — States
- **Pass criteria:** Invalid transitions (e.g., DRAFT → APPROVED) rejected with 409.

### V-08-03 — Onboarding time
- **Steps:** 3 real sellers (incl. one non-tech-savvy) complete onboarding on their own phones.
- **Pass criteria:** Median active time ≤ 15 min (excluding product photos); 0 sellers need developer help.

### V-08-04 — KYC
- **Pass criteria:** Valid PAN passes; invalid PAN fails; name mismatch → manual review queue.

### V-08-05 — Bank
- **Pass criteria:** Penny drop succeeds in sandbox; UI shows `XXXXXX1234` only; DB has no plain account number (checked by query).

### V-08-06 — Agreement record
- **Pass criteria:** Record contains version, timestamp, IP, UA.

### V-08-07 — Gate
- **Pass criteria:** Submit disabled with 4 products, enabled with 5.

### V-08-08 — Admin review
- **Pass criteria:** "Request changes" message reaches vendor via WhatsApp + email; vendor can edit and resubmit.

### V-08-09 — Plug-in activation
- **Pass criteria:** Approve → within 5 min: linked account ACTIVE in gateway sandbox, store URL live, products searchable, welcome sent — **no manual step by platform team**.

### V-08-10 — Reminders & re-verification
- **Pass criteria:** Reminder jobs fire at 24/72 h (time-travel); bank change sets payouts PAUSED.

## Module sign-off
- [ ] All checks Pass
- [ ] Legal/CA confirms KYC field set
