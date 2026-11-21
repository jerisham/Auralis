# 08 — Vendor Onboarding & KYC

**Phase:** P1 · **Depends on:** 03, 13, 15, 18 · **Status:** Draft

## 1. Purpose
Turn a small jewellery seller into a verified, payable vendor in **under 15 minutes of their time**, on a phone, while collecting what the law and the payment gateway require. Onboarding is "plug-in": once approved, the vendor's store and products go live automatically with zero work from the platform team.

## 2. Flow
```
Landing "Sell with us" → Sign up (phone OTP) → Business details → KYC documents
→ Bank account → Store setup → Accept Seller Agreement → Add first 5 products
→ Submitted → Admin review (≤ 48 h) → Approved → Gateway linked account active → Store LIVE
                                     └→ Changes requested → vendor fixes → resubmit
                                     └→ Rejected (with reason)
```
Progress bar with save-and-resume at every step.

## 3. Steps & fields
| Step | Fields | Validation |
|---|---|---|
| 1. Account | Owner name, mobile (OTP), email (verify) | Unique per vendor |
| 2. Business | Business type (Individual/Proprietor, Partnership, Pvt Ltd, LLP), legal name, display/store name, pickup address (+PIN), city, years in business, Instagram handle (optional), monthly order volume (range) | Store name unique, profanity check |
| 3. KYC | PAN (individual or business), GSTIN (if registered / required by Q-07), Aadhaar-based e-KYC or ID upload for proprietors, address proof | PAN & GSTIN verified via a KYC API; name match with bank |
| 4. Bank | Account holder name, account no., IFSC; penny-drop verification | Name match ≥ threshold; stored tokenised/masked; full details only at gateway |
| 5. Store setup | Logo (square), banner (16:5), about (≤ 500 chars), speciality tags, dispatch time (1–3 days), shipping fee + free threshold, serviceable regions, return policy add-ons | Image checks per 01 guidelines |
| 6. Agreement | Seller Agreement, commission schedule, SLA rules, prohibited items policy — e-sign checkbox with timestamp + IP | Version stored |
| 7. First products | Minimum 5 products (via 10 product form or CSV) | Quality checked by admin |

## 4. Functional requirements
| ID | Requirement |
|---|---|
| FR-08-01 | Mobile-first wizard; each step autosaves; resume from any device. |
| FR-08-02 | KYC & bank verification via third-party API; results stored with reference IDs, not raw images beyond legal need. |
| FR-08-03 | On approval, create the vendor's **linked account** at the payment gateway (13) automatically; vendor cannot receive orders until it is `ACTIVE`. |
| FR-08-04 | Application states: `DRAFT → SUBMITTED → IN_REVIEW → CHANGES_REQUESTED → APPROVED / REJECTED`. |
| FR-08-05 | Notifications at each state change (15). |
| FR-08-06 | Approved vendor gets: store URL `/<store-slug>`, vendor portal access, welcome kit (photo guide, how to ship, SLA cheat sheet). |
| FR-08-07 | Changing bank account or legal details later requires re-verification and admin approval; payouts paused meanwhile. |
| FR-08-08 | "Sell with us" landing page: benefits, fee calculator (price → you receive ₹X), FAQs, testimonials (real only). |
| FR-08-09 | Referral code field (vendor referred by another vendor) for later incentives. |

## 5. Prohibited items (policy, enforced in 10/11)
Real gold/silver/diamond claims, counterfeit branded designs (e.g., logos of luxury houses), items made with banned wildlife material, anything misrepresenting material.

## 6. Edge cases
- PAN name ≠ bank name → manual review.
- Vendor abandons at step 4 → reminders at 24 h and 72 h.
- Same PAN applies twice → block, link to existing application.
