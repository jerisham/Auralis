# 12 — Order Lifecycle (State Machine)

**Phase:** P1 · **Depends on:** 16, 17 · **Status:** Draft

## 1. Purpose
One authoritative definition of every state an order can be in, who can move it, what triggers each move, and what side-effects (money, stock, notifications) happen. Payments (13), delivery (14), notifications (15), and all UIs follow this file.

## 2. Two levels
- **Order** (customer checkout): `PENDING_PAYMENT → PAID → (derived) PARTIALLY_FULFILLED / FULFILLED / CANCELLED / CLOSED`
  Order status is **derived** from its vendor orders after payment.
- **VendorOrder** (one per vendor): the real workflow below.

## 3. VendorOrder states
| State | Meaning | Entered by |
|---|---|---|
| `AWAITING_ACCEPTANCE` | Paid; vendor must accept | System on payment webhook |
| `ACCEPTED` | Vendor committed to ship | Vendor |
| `DISPATCHED` | Handed to courier; tracking ID recorded | Vendor (tracking mandatory) |
| `DELIVERED` | Delivery confirmed (14) | Tracking API / Customer / Auto-timer / Admin |
| `COMPLETED` | Return window ended with no open claim | System timer |
| `SETTLED` | All payouts released | System (13) |
| `REJECTED_BY_VENDOR` | Vendor declined | Vendor |
| `CANCELLED_BY_CUSTOMER` | Customer cancelled pre-dispatch | Customer |
| `CANCELLED_SLA` | Vendor missed accept/dispatch SLA | System timer |
| `CLAIM_OPEN` | Customer reported a problem | Customer |
| `CLAIM_RESOLVED` | Claim decided (refund/replacement/rejected) | Vendor / Admin |
| `REFUNDED` | Money returned to customer (full) | System (13) |

## 4. Transitions & side-effects
| From | To | Trigger | Guard | Side-effects |
|---|---|---|---|---|
| — | AWAITING_ACCEPTANCE | payment.captured | — | Convert stock reservation → committed; notify vendor (WhatsApp+email+push) & customer; start accept SLA (24 h) |
| AWAITING_ACCEPTANCE | ACCEPTED | vendor.accept | — | Start dispatch SLA (72 h from payment) |
| AWAITING_ACCEPTANCE | REJECTED_BY_VENDOR | vendor.reject(reason) | — | Restore stock; refund vendor order; strike/score impact; notify customer |
| AWAITING_ACCEPTANCE / ACCEPTED | CANCELLED_BY_CUSTOMER | customer.cancel | before dispatch | Restore stock; refund; notify vendor |
| AWAITING_ACCEPTANCE / ACCEPTED | CANCELLED_SLA | timer | SLA exceeded | Restore stock; refund; strike; notify both |
| ACCEPTED | DISPATCHED | vendor.dispatch(courier, tracking) | tracking format valid | **Release tranche T1** (13); notify customer with tracking; start auto-delivery timer |
| DISPATCHED | DELIVERED | tracking.delivered / customer.received / timer / admin | — | Start return window (48 h); notify both; ask for review |
| DELIVERED | CLAIM_OPEN | customer.claim | within window | **Freeze T2**; notify vendor; start vendor response SLA 48 h |
| DELIVERED | COMPLETED | timer | window ended, no claim | Schedule **T2 release** |
| CLAIM_OPEN | CLAIM_RESOLVED | vendor/admin decision | — | Refund/replacement/none; recover from vendor if needed (13) |
| CLAIM_RESOLVED | COMPLETED / REFUNDED | system | — | Release T2 or close with recovery |
| COMPLETED | SETTLED | payout.released | all tranches paid | — |

Any transition not in this table is **illegal** and must be rejected (409).

## 5. Timers (configurable in 11)
| Timer | Default |
|---|---|
| Vendor accept SLA | 24 h after payment |
| Dispatch SLA | 72 h after payment |
| Auto-deliver if no tracking update | dispatch + 10 days (customer gets "Did you receive?" prompt at +7 days) |
| Return/claim window | 48 h after delivered |
| Vendor claim response | 48 h |
| Reminder to vendor before SLA breach | at 50% and 90% of SLA |

## 6. Rules
- Every transition writes an `order_events` row (actor, from, to, reason, metadata, timestamp).
- Transitions are executed in a DB transaction with row lock on the vendor order; side-effects emitted as events via the **outbox pattern** (16) — no lost or duplicated notifications/payouts.
- Admin override allowed for any transition **with reason**, audited.
