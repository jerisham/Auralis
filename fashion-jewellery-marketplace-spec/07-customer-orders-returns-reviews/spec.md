# 07 — Customer Orders, Returns & Reviews

**Phase:** P1 · **Depends on:** 06, 12, 13, 14 · **Status:** Draft

## 1. Purpose
After purchase, the customer must always know where each package is, how to confirm receipt, how to report a problem, and how to review. This is where trust is earned or lost.

## 2. Screens
- **My orders:** list of orders; each shows vendor packages with status pill (Confirmed, Packed, Shipped, Delivered, Cancelled, Return requested…).
- **Order detail:** per vendor package: items, status timeline, courier name + tracking link, expected date, seller contact (masked relay email/phone via platform in P2; P1 shows "Contact via Help"), buttons by state:
  - Before dispatch: **Cancel package**.
  - Shipped: **Track**, **I received it** (confirms delivery, 14).
  - Delivered (within return window): **Report a problem**.
  - Completed: **Write a review**, **Download invoice**.
- **Report a problem (damage/wrong/missing claim):** reason, photos (≥ 2) and/or unboxing video (≤ 60 s), description; select items.
- **Help:** FAQs + raise ticket linked to order (handled in admin 11).

## 3. Functional requirements
| ID | Requirement |
|---|---|
| FR-07-01 | Customer can cancel a vendor order until it reaches `DISPATCHED`; full refund of that vendor order (items + its shipping). |
| FR-07-02 | Claims allowed within return window (default 48 h after delivery, Q-09). Reasons: Damaged, Wrong item, Missing item, Not as described, Quality issue. |
| FR-07-03 | Vendor has 48 h to respond to a claim: Accept refund / Offer replacement / Reject with reason. No response → auto-escalate to admin. |
| FR-07-04 | Customer can escalate a vendor rejection to admin within 7 days; admin decision final (11). |
| FR-07-05 | Return shipping (if item must be returned): vendor provides reverse pickup or customer ships and uploads tracking; refund on vendor confirming receipt or after 7 days of reverse-delivery tracking. |
| FR-07-06 | Refunds go to original payment method via gateway; customer sees refund status and reference (UTR/ARN). |
| FR-07-07 | Reviews: only for delivered items, once per item per order; 1–5 stars, text (optional, 10–1000 chars), up to 5 photos; editable for 30 days. Reviews moderated by profanity filter + reports. |
| FR-07-08 | Vendor rating = average of product reviews + a delivery-experience rating (1–5) asked separately per vendor order. |
| FR-07-09 | Invoice PDF per vendor order (vendor as seller; platform commission invoice is separate, vendor-facing — 13). |

## 4. Rules
- A claim freezes the remaining payout tranche for that vendor order (13) until resolved.
- Fraud guard: customers with > 3 claims in 60 days are flagged for admin review.

## 5. Edge cases
- Customer claims "not received" while tracking says delivered → dispute flow; admin checks courier proof of delivery.
- Partial claim (1 of 3 items) → partial refund of that item only; shipping refunded only if whole package affected.
