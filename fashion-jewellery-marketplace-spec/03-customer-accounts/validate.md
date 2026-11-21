# Validation — 03 Customer Accounts

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-03-01 | T-03-01 | Automated | | | |
| V-03-02 | T-03-02 | Manual + automated | | | |
| V-03-03 | T-03-03 | Manual | | | |
| V-03-04 | T-03-04 | Manual + Playwright | | | |
| V-03-05 | T-03-05 | Automated | | | |
| V-03-06 | T-03-06 | Automated | | | |
| V-03-07 | T-03-07 | Playwright | | | |
| V-03-08 | T-03-08 | Automated | | | |
| V-03-09 | T-03-09 | Manual | | | |
| V-03-10 | T-03-10 | Playwright | | | |

### V-03-01 — Auth security
- **Checks:** OTP stored hashed; expired OTP rejected; 4th wrong attempt locked; refresh token reuse revokes the token family; access token expires at 15 min.
- **Pass criteria:** All automated tests green; OWASP ZAP baseline shows no high findings on auth endpoints.

### V-03-02 — OTP delivery & limits
- **Pass criteria:** OTP received < 15 s (p90) on Jio, Airtel, Vi test SIMs; 6th request in an hour returns 429.

### V-03-03 — Google
- **Pass criteria:** New user via Google can complete checkout after adding phone.

### V-03-04 — Login UX
- **Steps:** 5 users log in on their own phones.
- **Pass criteria:** Median time ≤ 20 s; 0 users stuck; Android autofills OTP.

### V-03-05 — Profile
- **Pass criteria:** Email unverified until link clicked; expired link shows resend.

### V-03-06 — Addresses
- **Pass criteria:** PIN `600008` autofills Chennai / Tamil Nadu; `000000` rejected; 11th address blocked.

### V-03-07 — Wishlist merge
- **Steps:** As guest add A, B; log in to account having B, C.
- **Pass criteria:** Wishlist = A, B, C.

### V-03-08 — Cart merge
- **Steps:** Guest cart: X×2; account cart: X×1, stock = 2.
- **Pass criteria:** Merged X×2 with message "Quantity adjusted to available stock".

### V-03-09 — Delete/export
- **Pass criteria:** Export email with complete data within 72 h (immediately in staging); deleted user cannot log in; orders remain for vendor with customer name anonymised after retention.

### V-03-10 — Follow
- **Pass criteria:** Followed store appears in account list; unfollow removes it.

## Module sign-off
- [ ] All checks Pass
- [ ] Security review of auth (18) done
