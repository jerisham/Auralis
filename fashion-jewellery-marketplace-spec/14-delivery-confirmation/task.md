# Tasks — 14 Delivery Confirmation

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-14-01 | Shipment model + dispatch form validation (courier list, regex, photo, hand-delivery rules) | T-17-03 | M | Todo |
| T-14-02 | Customer "I received it" + "Not received" actions | T-12-02 | S | Todo |
| T-14-03 | Tracking aggregator integration (webhook + polling) and status normalisation | T-14-01 | L | Todo |
| T-14-04 | Tracking verification within 24/48 h + vendor warnings/admin flags | T-14-03 | M | Todo |
| T-14-05 | Auto-confirm timer + customer prompt at +7 days | T-12-03 | S | Todo |
| T-14-06 | RTO handling flow | T-14-03, T-11-06 | M | Todo |
| T-14-07 | (P2) Delivery OTP | T-14-01 | M | Todo |

---

### T-14-01 — Shipment & dispatch
- **Done when:** Invalid tracking format rejected; hand delivery requires OTP/confirmation path.

### T-14-02 — Customer actions
- **Done when:** Received → DELIVERED; Not received → claim NOT_RECEIVED.

### T-14-03 — Tracking integration
- **Done when:** Events stored and normalised for ≥ 5 major couriers; webhook verified; polling fallback works.

### T-14-04 — Verification
- **Done when:** Unknown tracking after 24 h warns vendor; 48 h flags admin.

### T-14-05 — Auto-confirm
- **Done when:** Prompt at +7 days; auto-deliver at +10 days unless claim; not applied to hand delivery.

### T-14-06 — RTO
- **Done when:** RTO status creates admin task; refund/penalty decisions flow through 13.

### T-14-07 — Delivery OTP (P2)
- **Done when:** 4-digit OTP shown to customer after OUT_FOR_DELIVERY; vendor enters OTP → DELIVERED.
