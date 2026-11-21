# Validation — 02 Intro Experience

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-02-01 | T-02-01 | Review | | | |
| V-02-02 | T-02-02 | Automated | | | |
| V-02-03 | T-02-03 | Manual + automated | | | |
| V-02-04 | T-02-04 | Automated (Playwright) | | | |
| V-02-05 | T-02-05 | Manual + Lighthouse | | | |
| V-02-06 | T-02-06 | Manual | | | |
| V-02-07 | T-02-07 | Manual | | | |

### V-02-01 — Media quality
- **Pass criteria:** 5 target users watch the intro; ≥ 4/5 rate it "premium/attractive" (4–5 of 5). Rights document on file.

### V-02-02 — Encoding
- **Pass criteria:** Each rendition within §5 size budget; plays in Chrome, Safari (iOS), Firefox, Samsung Internet.

### V-02-03 — Overlay controls
- **Steps:** Load `/` in fresh browser; press Tab once; press Enter.
- **Pass criteria:** Skip is first focus target and skips; CTA appears at 3 s ± 0.3 s; fade ≤ 400ms; sound off by default.

### V-02-04 — Display rules
- **Scenarios (all must pass):**
  1. Fresh browser `/` → intro plays.
  2. Reload `/` → no intro, hero loop shown.
  3. Fresh browser `/p/<product>` → no intro.
  4. Emulate reduced motion → poster, no autoplay.
  5. Emulate Slow 3G + Save-Data → poster.
  6. Block video URL → poster + CTA within 2.5 s.

### V-02-05 — Homepage performance
- **Pass criteria (mobile, Moto G Power profile, 4G):** LCP ≤ 2.5 s, CLS ≤ 0.1, INP ≤ 200 ms; intro video does **not** count against LCP (poster is the LCP element). All 10 sections render; view-source shows product names (SSR).

### V-02-06 — Admin scheduling
- **Steps:** Schedule "Diwali" intro for tomorrow 00:00–23:59 (use time-travel in staging).
- **Pass criteria:** Correct video served during window, default before/after.

### V-02-07 — Analytics
- **Pass criteria:** 4 events recorded with correct properties for a test session.

## Module sign-off
- [ ] All checks Pass
- [ ] Product owner approval
