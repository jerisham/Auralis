# Validation — 15 Notifications

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-15-01 | T-15-01 | Automated | | | |
| V-15-02 | T-15-02 | Manual | | | |
| V-15-03 | T-15-03 | Manual + tool | | | |
| V-15-04 | T-15-04 | Manual | | | |
| V-15-05 | T-15-05 | Automated + E2E | | | |
| V-15-06 | T-15-06 | Automated | | | |
| V-15-07 | T-15-07 | Chaos test | | | |

### V-15-01 — Service correctness
- **Pass criteria:** Replaying an event 3× sends one message; rendering with missing variable fails safely (alert, no broken message sent).

### V-15-02 — Templates approved
- **Pass criteria:** Approval screenshots/IDs recorded for every DLT and WhatsApp template.

### V-15-03 — Email deliverability
- **Pass criteria:** SPF/DKIM/DMARC pass; lands in Gmail inbox (not spam) for 5 test accounts.

### V-15-04 — Push & inbox
- **Pass criteria:** Push received on Android Chrome and desktop; inbox counts correct.

### V-15-05 — **Vendor new-order alert (critical)**
- **Steps:** Place paid order for 2 vendors.
- **Pass criteria:** Each vendor receives WhatsApp + email + push within **60 s** (p95), with correct items, customer name, city and a working deep link; customer receives confirmation listing both packages.

### V-15-06 — Preferences
- **Pass criteria:** Disabling email for marketing stops marketing emails only; quiet hours delay digests but not order alerts.

### V-15-07 — Fallback
- **Steps:** Force WhatsApp provider failure.
- **Pass criteria:** SMS fallback within 2 min; ops alert after 5 consecutive failures.

## Module sign-off
- [ ] All checks Pass
- [ ] 3 pilot vendors confirm alerts are timely and clear
