# Validation — 07 Customer Orders, Returns & Reviews

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-07-01 | T-07-01 | Playwright | | | |
| V-07-02 | T-07-02 | Playwright | | | |
| V-07-03 | T-07-03 | Sandbox E2E | | | |
| V-07-04 | T-07-04 | Sandbox E2E | | | |
| V-07-05 | T-07-05 | Automated | | | |
| V-07-06 | T-07-06 | Manual (CA review) | | | |
| V-07-07 | T-07-07 | Manual | | | |

### V-07-01 — Orders view
- **Pass criteria:** 2-vendor order shows two packages with independent statuses; Cancel hidden after dispatch.

### V-07-02 — Receipt confirmation
- **Pass criteria:** Clicking "I received it" sets DELIVERED, starts return window timer, notifies vendor.

### V-07-03 — Cancel & refund
- **Pass criteria:** Refund for exactly that vendor order (items + shipping) shows in gateway sandbox; stock restored; vendor's held transfer reversed.

### V-07-04 — Claim scenarios
1. Vendor accepts → refund issued, tranche 2 cancelled, T1 recovered from vendor balance (13).
2. Vendor rejects → customer escalates → admin refunds → same financial result as 1.
3. Vendor silent 48 h → auto-escalated.
4. Claim after window → blocked with message.
- **Pass criteria:** All four pass; ledger balanced after each (13 V-13-04).

### V-07-05 — Reviews
- **Pass criteria:** Cannot review undelivered item; second review on same item blocked; profanity masked; average updates ≤ 5 min.

### V-07-06 — Invoice
- **Pass criteria:** CA confirms invoice fields are compliant for B2C sale by a vendor through a marketplace.

### V-07-07 — Help
- **Pass criteria:** Ticket visible in admin with order link within 1 min.

## Module sign-off
- [ ] All checks Pass
- [ ] Ops lead approval of claim process
