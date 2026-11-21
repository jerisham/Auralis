# Tasks — 03 Customer Accounts

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-03-01 | Identity service: users, roles, OTP issue/verify, JWT + refresh rotation | T-16-03, T-17-02 | L | Todo |
| T-03-02 | SMS + WhatsApp OTP provider integration with rate limits | T-03-01, T-15-02 | M | Todo |
| T-03-03 | Google sign-in | T-03-01 | S | Todo |
| T-03-04 | Login sheet UI (phone, OTP, name) incl. WebOTP autofill | T-01-07, T-03-01 | M | Todo |
| T-03-05 | Profile + email verification | T-03-01 | S | Todo |
| T-03-06 | Address book with PIN validation and autofill | T-03-01 | M | Todo |
| T-03-07 | Wishlist + guest merge | T-03-01, 04 | M | Todo |
| T-03-08 | Guest cart merge on login | T-06-01 | S | Todo |
| T-03-09 | Account deletion + data export jobs | T-03-01, 18 | M | Todo |
| T-03-10 | Follow store | T-09-01 | S | Todo |

---

### T-03-01 — Identity service
- **Steps:** Tables `users`, `user_roles`, `otp_requests`, `refresh_tokens`; endpoints `POST /v1/auth/otp/request`, `POST /v1/auth/otp/verify`, `POST /v1/auth/refresh`, `POST /v1/auth/logout`, `POST /v1/auth/logout-all`. OTP hashed at rest.
- **Done when:** Endpoints in OpenAPI, unit + integration tests pass, tokens carry `sub`, `roles`, `vendor_id` (if any).

### T-03-02 — OTP delivery
- **Done when:** OTP arrives via SMS in staging test numbers; WhatsApp fallback works; limits in FR-03-01 enforced.

### T-03-03 — Google sign-in
- **Done when:** Google account creates/links user; existing phone user can link Google from profile.

### T-03-04 — Login UI
- **Done when:** Full flow in < 20 s on a phone; errors (wrong OTP, expired, too many) shown inline.

### T-03-05 — Profile
- **Done when:** Edit name/email/birthday/preferences; email verification link expires in 24 h.

### T-03-06 — Addresses
- **Steps:** Load India PIN directory into a lookup table; API `GET /v1/pincodes/{pin}`.
- **Done when:** Invalid PIN rejected; valid PIN autofills city/state; max 10 enforced; default address logic works.

### T-03-07 — Wishlist
- **Done when:** Add/remove from card and PDP; guest wishlist merges with no duplicates.

### T-03-08 — Cart merge
- **Done when:** Rules of FR-03-06 implemented with tests.

### T-03-09 — Delete/export
- **Done when:** Deletion and export jobs run via queue; email sent; audit log entries written.

### T-03-10 — Follow store
- **Done when:** Follow/unfollow button on storefront; list in account.
