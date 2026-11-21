# Tasks — 07 Customer Orders, Returns & Reviews

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-07-01 | My orders list + order detail with per-vendor timeline | T-12-02 | M | Todo |
| T-07-02 | Tracking view + "I received it" button | T-14-02 | S | Todo |
| T-07-03 | Cancel vendor order (pre-dispatch) + refund trigger | T-12-02, T-13-05 | M | Todo |
| T-07-04 | Claims: create (media upload), vendor response, escalation, resolution, refunds | T-13-05, T-11-06 | L | Todo |
| T-07-05 | Reviews & ratings (product + vendor delivery rating), moderation hooks | T-07-01 | M | Todo |
| T-07-06 | Invoice PDF generation per vendor order | T-13-07 | M | Todo |
| T-07-07 | Help centre FAQ + order-linked support tickets | T-11-06 | M | Todo |

---

### T-07-01 — Orders UI
- **Done when:** All statuses from 12 map to customer-friendly labels; buttons appear only in valid states.

### T-07-02 — Tracking & receipt
- **Done when:** Tracking link opens courier page; "I received it" moves vendor order to DELIVERED (14).

### T-07-03 — Cancel
- **Done when:** Cancel allowed only before DISPATCHED; refund created; vendor notified; stock restored.

### T-07-04 — Claims
- **Steps:** Claim entity + state machine (OPEN → VENDOR_ACCEPTED / VENDOR_REJECTED / ESCALATED → RESOLVED_REFUND / RESOLVED_REPLACEMENT / RESOLVED_REJECTED); media to blob storage (≤ 50 MB video); timers for 48 h vendor SLA.
- **Done when:** All transitions implemented with tests; tranche freeze hook calls 13.

### T-07-05 — Reviews
- **Done when:** FR-07-07, 08 implemented; aggregate ratings updated asynchronously ≤ 5 min.

### T-07-06 — Invoices
- **Done when:** PDF with vendor legal details, GSTIN if any, HSN code, tax breakup, order IDs.

### T-07-07 — Help
- **Done when:** FAQ pages editable by admin; ticket created with order reference appears in admin.
