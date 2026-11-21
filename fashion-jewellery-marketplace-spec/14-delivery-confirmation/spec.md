# 14 — Delivery Confirmation

**Phase:** P1 (OTP in P2) · **Depends on:** 12, 13, Q-10 · **Status:** Draft

## 1. Purpose
Because vendors deliver themselves, the platform needs a reliable, fair signal that a package was actually delivered — it triggers the return window and the final payout (T2). This is the trust core of the "vendor delivers" model.

## 2. Signals (in priority order)
| # | Signal | Strength | Phase |
|---|---|---|---|
| 1 | **Courier tracking status = Delivered** via shipping-tracking aggregator API/webhook | Strong | P1 |
| 2 | **Customer taps "I received it"** | Strong | P1 |
| 3 | **Delivery OTP** — customer shares OTP with delivery person; vendor/courier enters it | Strongest | P2 |
| 4 | **Auto-confirm** at dispatch + 10 days if no complaint (customer prompted at +7) | Weak (fallback) | P1 |
| 5 | **Admin decision** in dispute, using courier proof of delivery | Final | P1 |

## 3. Dispatch requirements (vendor side)
- Courier: select from list (India Post, Delhivery, Blue Dart, DTDC, Ekart, Xpressbees, Shadowfax, Ecom Express, Other) + tracking ID.
- Tracking ID validated per courier format (regex) and, where possible, verified live via tracking API within 24 h ("Tracking not found" → vendor warned; after 48 h → admin flag, T1 clawback possible).
- "Hand delivery" (same-city, vendor's own person) allowed only with **customer OTP or customer confirmation**; no auto-confirm for hand delivery.
- Optional parcel photo at dispatch (recommended; used in disputes).

## 4. Functional requirements
| ID | Requirement |
|---|---|
| FR-14-01 | Shipment record: courier, tracking ID, dispatched_at, events[], delivered_at, proof (photo/OTP/POD link). |
| FR-14-02 | Subscribe to tracking updates via aggregator webhook; poll fallback every 6 h. |
| FR-14-03 | Normalise courier statuses → `IN_TRANSIT`, `OUT_FOR_DELIVERY`, `DELIVERED`, `RTO` (returned to origin), `EXCEPTION`. |
| FR-14-04 | `DELIVERED` from tracking → transition vendor order (12). |
| FR-14-05 | `RTO` → vendor order flagged; customer notified; admin decides refund (and who pays). |
| FR-14-06 | Customer "Not received" while tracking says delivered → opens claim (07) with type `NOT_RECEIVED`. |
| FR-14-07 | Customer sees tracking timeline in order detail (07). |

## 5. Edge cases
- Wrong tracking ID entered → vendor can edit once within 12 h; changes audited.
- Courier not supported by aggregator → signal 2/4 only.
