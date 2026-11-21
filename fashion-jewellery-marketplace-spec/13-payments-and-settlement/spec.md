# 13 — Payments, Commission & Settlement

**Phase:** P1 · **Depends on:** 12, 17, Q-02..Q-07 · **Status:** Draft
> ⚠️ Tax figures and rules here are a planning baseline. **A chartered accountant must confirm** commission GST, TCS (GST s.52) and TDS (Income-tax s.194-O) treatment and rates before go-live. All rates are configuration, not code.
>
> **Locked decisions (17 Nov 2026):** Global commission **15%** of item price, no listing fee (Q-02). Tranches **75% on DISPATCHED / 25% after COMPLETED** (Q-03). Platform absorbs gateway fees out of commission (Q-04). Gateway is **Razorpay Route**, behind `PaymentProvider` (Q-05). No COD (Q-06). GSTIN only when legally required (Q-07). The 20% figures below are the original tranche illustration, not the launch rate.

## 1. Purpose
Collect one payment from the customer, split it between vendors and the platform, **hold vendor money** until they perform (dispatch, then delivery + return window), and keep a perfect, auditable record of every rupee.

## 2. Approach
- Use Razorpay Route (Q-05). Cashfree Easy Split stays a possible swap through `PaymentProvider`. Each approved vendor has a **linked account** at the gateway (created in 08).
- The platform never manually moves vendor money from its own bank account. The gateway holds and transfers funds; we instruct it.
- Code talks to a `PaymentProvider` interface (create order, create held transfers, release transfer, reverse transfer, refund, fetch settlements) so the gateway can be swapped or a second one added.

## 3. Amounts (all integers in **paise**)
For each VendorOrder:
```
items_total        = Σ (unit_price × qty)                 # tax-inclusive selling prices
shipping           = vendor shipping fee (0 if free)
gross              = items_total + shipping                # what customer paid for this vendor
commission         = round(items_total × commission_rate) + fixed_fee_per_order
gst_on_commission  = round(commission × 18%)               # platform's service to vendor (confirm)
tcs                = round(net_taxable_value × tcs_rate)   # only if vendor GST-registered (confirm)
tds                = round(gross × tds_rate)               # s.194-O, subject to exemptions (confirm)
vendor_net         = gross − commission − gst_on_commission − tcs − tds
T1                 = floor(vendor_net × t1_percent)        # default 75%, on DISPATCHED
T2                 = vendor_net − T1                       # on COMPLETED (after return window)
platform_keeps     = commission + gst_on_commission (+ tcs, tds held for remittance to government)
gateway_fee        = charged by gateway on the whole payment; borne by platform (Q-04)
```
Commission rate resolved per item by rule precedence (11): vendor override > category > global, using the rule **effective at order time** (snapshotted on the order item).

### Launch example (Q-02 / Q-03, no taxes, no shipping)
Item ₹500, commission 15% → fee ₹75 → vendor_net ₹425 → **T1 ₹318.75 on dispatch, T2 ₹106.25 after delivery + return window.** In paise: items 50000, commission 7500, vendor_net 42500, T1 31875, T2 10625.

### Original brief illustration (not the launch rate)
Item ₹500, commission 20% → fee ₹100 → vendor_net ₹400 → T1 ₹300, T2 ₹100. Kept so the 75/25 split is easy to see.

### Example (with tax placeholders)
Item ₹500, shipping ₹60, commission 20% = ₹100, GST on commission ₹18, TCS 0.5% of ₹500 ≈ ₹2.50, TDS 0.1% of ₹560 ≈ ₹0.56
→ vendor_net ≈ ₹438.94 → T1 ≈ ₹329.20, T2 ≈ ₹109.74.

## 4. Money flow
1. **Checkout (06):** gateway order for full amount; on capture, create **two held transfers per vendor order** (T1, T2) to the vendor's linked account. Platform share stays in platform account.
2. **DISPATCHED (12):** release T1 hold → gateway settles to vendor bank on its schedule.
3. **COMPLETED:** release T2 hold.
4. **CLAIM_OPEN:** T2 stays held (frozen) until resolution.
5. **Payouts paused** (bank change, suspension, fraud review): releases queued, not executed.

## 5. Refunds & recoveries
| Situation | Action |
|---|---|
| Cancelled/rejected/SLA before dispatch | Reverse T1 + T2 (both still held) → refund customer full `gross` → commission reversed |
| Claim → full refund after T1 released | Reverse T2 (held); attempt reversal of T1 from linked account; if insufficient, create **vendor receivable** netted against future releases → refund customer |
| Partial refund (one item) | Reverse proportionally from T2 first, then T1/receivable |
| Replacement instead of refund | No money movement; T2 released after replacement delivered |
| Vendor at fault (SLA miss, false claim) | Optional penalty fee (config, default ₹0 in pilot) |
Customer refund always proceeds on time even if vendor recovery is pending — platform carries the receivable risk.

## 6. Ledger (source of truth)
Double-entry, append-only `ledger_entries` (entry_id, txn_id, account, debit, credit, currency, vendor_order_id, created_at). Every money event posts balanced entries.
Accounts: `customer_clearing`, `vendor_payable:<vendor>`, `vendor_receivable:<vendor>`, `platform_commission_revenue`, `gst_output_commission`, `tcs_payable`, `tds_payable`, `gateway_fee_expense`, `refunds_clearing`.
Invariant: Σ debits = Σ credits per txn and globally.

## 7. Documents
- **Customer invoice** per vendor order — vendor is the seller (generated by platform on vendor's behalf) (07).
- **Commission tax invoice** — platform → vendor, monthly consolidated.
- **Vendor statement** — monthly, every order with breakdown, tranches, UTRs, deductions.
- **Statutory reports** — TCS/TDS summaries by vendor and period for filing.

## 8. Reconciliation
Daily job: fetch gateway payments, transfers, reversals, refunds, settlements → match to ledger by IDs → mismatches into finance console (11) with alert.

## 9. Security
No card/UPI data touches our servers (gateway hosted checkout/SDK). Webhooks verified by signature; all handlers idempotent by gateway event ID.
