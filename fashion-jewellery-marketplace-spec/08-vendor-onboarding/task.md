# Tasks — 08 Vendor Onboarding & KYC

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-08-01 | "Sell with us" landing page + fee calculator | T-01-07, Q-02 | M | Todo |
| T-08-02 | Vendor application model + state machine + autosave API | T-17-02 | M | Todo |
| T-08-03 | Wizard UI steps 1–6 (mobile-first) | T-08-02 | L | Todo |
| T-08-04 | KYC verification integration (PAN, GSTIN, ID) | T-08-02, T-18-03 | M | Todo |
| T-08-05 | Bank penny-drop verification + name match | T-08-04 | M | Todo |
| T-08-06 | Seller Agreement versioning + e-acceptance record | Q-17 | S | Todo |
| T-08-07 | First-5-products gate (uses vendor product form) | T-10-03 | S | Todo |
| T-08-08 | Admin review hook (approve / request changes / reject) | T-11-02 | S | Todo |
| T-08-09 | On approval: create gateway linked account, activate store, send welcome kit | T-13-08, T-15-05 | M | Todo |
| T-08-10 | Abandonment reminders + re-verification flow for detail changes | T-15-05 | S | Todo |

---

### T-08-01 — Landing
- **Done when:** Page live with calculator using live commission rules; mobile Lighthouse ≥ 90.

### T-08-02 — Application model
- **Done when:** States FR-08-04 enforced; `PATCH /v1/vendor-applications/{id}/steps/{n}` autosaves.

### T-08-03 — Wizard UI
- **Done when:** Can complete all steps on a 360px phone; resume works across devices.

### T-08-04 — KYC
- **Done when:** PAN/GSTIN verified with provider; mismatch routes to manual review; documents encrypted at rest.

### T-08-05 — Bank
- **Done when:** Penny-drop result and name-match score stored; only last 4 digits shown in UI.

### T-08-06 — Agreement
- **Done when:** Acceptance stores agreement version, timestamp, IP, user-agent.

### T-08-07 — Product gate
- **Done when:** Submit disabled until 5 valid products exist.

### T-08-08 — Review hook
- **Done when:** Admin actions update state and notify vendor with reason text.

### T-08-09 — Activation
- **Done when:** Approval → linked account created → status ACTIVE → store visible → welcome message sent; failure in gateway step retried and alerted.

### T-08-10 — Reminders & re-verification
- **Done when:** Reminders at 24/72 h; bank change pauses payouts until re-approved.
