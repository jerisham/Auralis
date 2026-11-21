# 03 — Customer Accounts

**Phase:** P1 · **Depends on:** 01, 16, 17, 18 · **Status:** Draft

## 1. Purpose
Let customers sign in with almost no friction (phone OTP), save addresses and wishlist, and see their orders. Browsing never requires login; login is asked at checkout or when saving something.

## 2. User stories
- As a guest, I browse everything without signing in.
- As a customer, I log in with my mobile number + OTP (or Google) in under 20 seconds.
- As a customer, I save multiple delivery addresses and pick one at checkout.
- As a customer, I keep a wishlist that syncs across devices; my guest cart/wishlist merges when I log in.
- As a customer, I can download my data or delete my account.

## 3. Functional requirements
| ID | Requirement |
|---|---|
| FR-03-01 | Login/sign-up via Indian mobile number + 6-digit OTP (SMS; WhatsApp OTP as fallback). OTP valid 5 min, 3 attempts, resend after 30 s, max 5 sends/hour/number. |
| FR-03-02 | Optional Google sign-in; email optional on profile but required for invoices (ask at first checkout). |
| FR-03-03 | Profile: name, phone (verified), email (verified by link), optional birthday (for offers), notification preferences. |
| FR-03-04 | Address book: name, phone, line 1/2, landmark, city, state, PIN (6-digit, validated against PIN directory), type (Home/Work/Other), default flag. Max 10. |
| FR-03-05 | Wishlist (heart on product cards); guest wishlist stored locally, merged on login. |
| FR-03-06 | Guest cart merged into account cart on login (quantities summed, capped at stock). |
| FR-03-07 | Sessions: access token 15 min, refresh token 30 days rotating; "Log out of all devices". |
| FR-03-08 | Account deletion: soft-delete immediately, hard-delete personal data after open orders/returns close and legal retention period ends (invoices retained per tax law). |
| FR-03-09 | Data export: JSON/CSV of profile, addresses, orders, reviews, emailed within 72 h. |
| FR-03-10 | Followed stores: customer can "follow" vendors → feed of new arrivals (P1 basic list, P2 notifications). |

## 4. Screens
- **Login sheet** (bottom sheet on mobile, modal on desktop): phone input with +91 → OTP input (auto-read on Android via WebOTP API) → name (first time only).
- **Account home:** Orders, Wishlist, Addresses, Followed stores, Profile, Notifications, Help, Logout.
- **Address form** with PIN-code autofill of city/state.

## 5. Rules
- Same phone cannot be both a customer and a vendor owner login? → **Allowed**; one identity, multiple roles. Vendor portal requires separate role activation (08).
- Blocked customers (fraud) cannot check out; can still browse.

## 6. Edge cases
- Phone number change: requires OTP on both old (if accessible) and new; otherwise support flow.
- OTP SMS delayed: offer WhatsApp OTP after 30 s.
- PIN not serviceable by any vendor in cart → flag at checkout (06), not here.
