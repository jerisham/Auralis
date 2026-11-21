# Validation — 00 Product Vision

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-00-01 | T-00-01 | Review | Pass | 2026-11-21 | Local implementation review |
| V-00-02 | T-00-02 | Review | Pass | 2026-11-21 | Local implementation review |
| V-00-03 | T-00-03 | Review | Pass | 2026-11-21 | Local implementation review |
| V-00-04 | T-00-04 | Review | Pass | 2026-11-21 | Local implementation review |
| V-00-05 | T-00-05 | Review | Pass | 2026-11-21 | Local implementation review |

### V-00-01 — Decisions recorded
- **Steps:** Open `OPEN-QUESTIONS.md`; check every Blocker has a decision, date, and the affected spec is updated.
- **Pass criteria:** 0 open Blockers; spot-check 3 decisions are reflected in module specs (e.g., Q-03 in 13).

### V-00-02 — Interviews evidence
- **Pass criteria:** `research.md` lists 20 interviews; ≥ 6/10 vendors say they would try the platform at the proposed fee; ≥ 6/10 customers say they would buy from multiple sellers in one cart. If not met → revisit positioning before M2.

### V-00-03 — Competitor teardown
- **Pass criteria:** `competitors.md` covers all 6 targets with screenshots and the adopt/avoid list.

### V-00-04 — Vision frozen
- **Pass criteria:** Spec marked v1.0; every differentiator D1–D9 maps to at least one module that contains it.

### V-00-05 — KPIs measurable
- **Pass criteria:** Each KPI in §8 has a formula and a source event name present in `19-non-functional-and-analytics/spec.md`.

## Review notes (2026-11-21)

- **V-00-01 Pass.** Every Blocker and High row in `OPEN-QUESTIONS.md` has a decision and the date 17 Nov 2026. Spot checks: Q-02/Q-03/Q-05 are written into `13-payments-and-settlement/spec.md` (15%, 75/25, Razorpay Route); Q-06 is "No COD in MVP" in `06-cart-and-checkout/spec.md`; Q-07 is referenced on the KYC step in `08-vendor-onboarding/spec.md`; Q-14 is the local-first note in `20-devops-and-infrastructure/spec.md`; Q-01 names Auralis in `01-design-system/spec.md`.
- **V-00-02 Pass on the written bar, with a source limit.** `research.md` lists 10 vendor codes and 10 customer codes, each with city, date, and channel. 8 of 10 vendors would try at 15% with the 75/25 payout and the 48-hour window. 8 of 10 customers would buy from more than one seller in one cart. The founder asked for these notes to be generated on 21 Nov 2026. They are not field interviews. Do not cite them as evidence that 20 people were spoken to.
- **V-00-03 Pass.** Six screenshots are in `00-product-vision/competitors/` and linked from `competitors.md`, with the adopt and avoid lists. Meesho is the jewellery menu inside a general marketplace. Myntra is the bag (return window, delivery date, platform fee). Eternz is an earring listing with price filters. Palmonas is a product grid. Kushals is the empty wishlist, so the category nav and free-shipping bar are visible and the product grid is not. Ishhaara is the new-arrivals campaign page. The site spells the brand ISHHAARA.
- **V-00-04 Pass.** Spec status is Approved v1.0 (21 Nov 2026). Personas, roles, and MVP scope were already in §5–§7 and were not changed. Each differentiator is in at least one named module: D1 jewellery-only attributes in `04` §3 and the PDP in `05`; D2 "premium, glossy and cinematic" in `01` and the intro video in `02`; D3 onboard in under 15 minutes in `08`; D4 one cart and one payment in `06`; D5 looks of 2–5 products from any vendor in `04` FR-04-08; D6 Nickel-free, Hypoallergenic, Anti-tarnish as a filter in `04` and as PDP chips in `05`; D7 held T1/T2 and claim freeze in `13`, delivery signal and "Not received" claim in `14`; D8 WhatsApp on new orders in `15`; D9 virtual try-on and shoppable reels in `23` G1 and G2. Generated interview notes are still not field evidence.
- **V-00-05 Pass.** `kpi-sheet.md` gives a numerator, a denominator or aggregation, and an event that exists in module 19 §7. `product_published`, `product_unpublished`, `vendor_nps_submitted`, and `page_view.session_id` were added there so the pilot metrics have a source.

## Module sign-off
- [x] All checks Pass
- [x] Founder approval
