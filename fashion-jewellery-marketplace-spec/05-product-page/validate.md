# Validation — 05 Product Page

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-05-01 | T-05-01 | Automated | | | |
| V-05-02 | T-05-02 | Manual (devices) | | | |
| V-05-03 | T-05-03 | Playwright | | | |
| V-05-04 | T-05-04 | Automated | | | |
| V-05-05 | T-05-05 | Manual | | | |
| V-05-06 | T-05-06 | Manual | | | |
| V-05-07 | T-05-07 | Manual | | | |
| V-05-08 | T-05-08 | Playwright | | | |
| V-05-09 | T-05-09 | Playwright | | | |

### V-05-01 — API
- **Pass criteria:** Vendor changes price → PDP shows new price within 30 s; p95 ≤ 250 ms under 50 RPS.

### V-05-02 — Gallery
- **Pass criteria:** Works on iPhone Safari, Android Chrome, desktop Chrome/Edge; zoom shows detail without pixelation (source ≥ 1200px).

### V-05-03 — Info & CTAs
- **Pass criteria:** OOS variant disabled; qty cannot exceed stock; "Only 2 left" when stock = 2; seller legal name/address shown and matches KYC.

### V-05-04 — Delivery estimate
- **Cases:** Vendor in Jaipur (dispatch 1 day) → PIN Jaipur, Chennai, Guwahati.
- **Pass criteria:** Ranges match zone table exactly for all three.

### V-05-05 — Carousels
- **Pass criteria:** "Complete the look" shows items from ≥ 2 vendors when data exists; hides when < 4 items.

### V-05-06 — Reviews
- **Pass criteria:** Photo reviews appear first; only verified-purchase reviews displayed.

### V-05-07 — Share
- **Pass criteria:** Sharing link in WhatsApp shows image, name, price.

### V-05-08 — Report
- **Pass criteria:** Report visible in admin moderation queue with product link and reason.

### V-05-09 — Edge pages
- **Pass criteria:** Unpublished product → 410 with similar items; vendor on holiday → add-to-cart disabled with message.

## Module sign-off
- [ ] All checks Pass
- [ ] Product owner approval
