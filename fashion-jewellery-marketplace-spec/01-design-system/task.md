# Tasks — 01 Design System

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-01-01 | Brand identity: logo, wordmark, favicon, app icon | Q-01 | M | Todo |
| T-01-02 | Mood board + 2 visual directions; pick one | T-01-01 | S | Todo |
| T-01-03 | Define tokens (colour, type, space, radius, shadow, motion) in Figma | T-01-02 | M | Todo |
| T-01-04 | Design component library in Figma | T-01-03 | L | Todo |
| T-01-05 | Key screen templates: Home, PLP, PDP, Cart, Vendor dashboard, Admin list | T-01-04 | L | Todo |
| T-01-06 | Export tokens via Style Dictionary (CSS vars + JS/RN theme) | T-01-03 | S | Todo |
| T-01-07 | Build coded component library in React + Storybook | T-01-06, 16 repo | L | Todo |
| T-01-08 | Accessibility pass on tokens and components | T-01-07 | M | Todo |
| T-01-09 | Vendor photo guidelines page (shared with 08/10) | T-01-02 | S | Todo |

---

### T-01-01 — Brand identity
- **Done when:** Logo in SVG (light + dark), favicon set, 1024px app icon, usage rules page.

### T-01-02 — Visual direction
- **Steps:** Two mood boards ("Midnight Atelier" dark-gold vs. a light "Ivory Boutique"); test with 5 target customers; choose.
- **Done when:** Direction chosen and recorded in spec §2.

### T-01-03 — Tokens
- **Done when:** All tokens in §2 exist as Figma variables with light/dark modes.

### T-01-04 — Component library (Figma)
- **Done when:** All components in §3 exist with states (default, hover, focus, disabled, error, loading) and mobile/desktop variants.

### T-01-05 — Templates
- **Done when:** 6 templates designed at 360px and 1440px, reviewed by product owner.

### T-01-06 — Token pipeline
- **Steps:** `tokens/*.json` → Style Dictionary → `dist/css/tokens.css`, `dist/js/tokens.ts`, `dist/rn/theme.ts`. Run in CI.
- **Done when:** Changing a token in JSON updates all three outputs in one build.

### T-01-07 — Coded components
- **Steps:** Implement in `packages/ui`; each with Storybook story, props docs, unit test, dark/light.
- **Done when:** All §3 components in Storybook, published to internal package.

### T-01-08 — Accessibility
- **Steps:** Contrast check all pairs; keyboard focus rings; ARIA roles; screen-reader labels; reduced motion.
- **Done when:** axe reports 0 serious/critical issues in Storybook.

### T-01-09 — Photo guidelines
- **Done when:** One-page visual guide (good vs bad examples) available to vendors in onboarding.
