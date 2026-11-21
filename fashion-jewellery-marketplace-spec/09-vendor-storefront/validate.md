# Validation — 09 Vendor Storefront

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-09-01 | T-09-01 | Playwright + Lighthouse | | | |
| V-09-02 | T-09-02 | Manual | | | |
| V-09-03 | T-09-03 | Playwright | | | |
| V-09-04 | T-09-04 | Automated | | | |
| V-09-05 | T-09-05 | Playwright | | | |
| V-09-06 | T-09-06 | Manual | | | |

### V-09-01 — Store page
- **Pass criteria:** Two different vendors' stores have identical layout/styles (visual diff only in content regions); LCP ≤ 2.5 s mobile.

### V-09-02 — Editor limits
- **Steps:** Inspect editor and API for any style/layout field; try to POST `custom_css` to API.
- **Pass criteria:** No such controls; API rejects unknown fields (400).

### V-09-03 — Collections
- **Pass criteria:** Reorder persists after reload; 9th featured product blocked.

### V-09-04 — Content checks
- **Cases:** About text containing "WhatsApp 98xxxxxx", "www.mystore.com", profanity; 400×400 banner.
- **Pass criteria:** All blocked or sent to moderation with reason.

### V-09-05 — Holiday/suspend
- **Pass criteria:** Holiday → products absent from search, PDP add-to-cart disabled, pending orders still visible to vendor; suspend → store unavailable page.

### V-09-06 — Share kit
- **Pass criteria:** QR scans to store with UTM; story image looks correct on Instagram story preview.

## Module sign-off
- [ ] All checks Pass
- [ ] Product owner approval
