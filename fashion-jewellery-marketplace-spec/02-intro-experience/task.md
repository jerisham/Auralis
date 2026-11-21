# Tasks — 02 Intro Experience

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-02-01 | Produce/license intro film, hero loop and posters | Q-15, T-01-01 | L | Todo |
| T-02-02 | Video encoding pipeline (MP4/WebM, mobile/desktop, posters) | 20 CDN | S | Todo |
| T-02-03 | Intro overlay component with skip, CTA, sound toggle, fade | T-01-07 | M | Todo |
| T-02-04 | First-visit logic (`intro_seen`), deep-link bypass, reduced-motion/slow-network fallback | T-02-03 | M | Todo |
| T-02-05 | Homepage sections 1–10 with SSR | T-01-07, 04 APIs | L | Todo |
| T-02-06 | Admin-managed media + scheduling (hook into 11) | T-11-07 | M | Todo |
| T-02-07 | Analytics events: intro_start, intro_skip, intro_complete, intro_cta | 19 | S | Todo |

---

### T-02-01 — Media production
- **Done when:** Final assets meeting §5, with written usage rights for web, app and social.

### T-02-02 — Encoding pipeline
- **Steps:** ffmpeg script / CI job producing all renditions + posters; upload to blob storage under `/media/intro/<version>/`.
- **Done when:** One command produces all renditions within size budgets.

### T-02-03 — Overlay component
- **Done when:** Component in Storybook; Skip focusable first; Esc key skips; CTA timing per FR-02-02.

### T-02-04 — Display logic
- **Steps:** Check storage flag + profile flag; skip on any route other than `/`; check `matchMedia('(prefers-reduced-motion)')`, `navigator.connection.saveData`, `effectiveType`.
- **Done when:** All rules in FR-02-01..07 implemented with unit tests.

### T-02-05 — Homepage
- **Done when:** All 10 sections render server-side from API data, with skeletons and empty states.

### T-02-06 — Admin media
- **Done when:** Admin uploads new intro and schedules it for a date range; site switches automatically.

### T-02-07 — Analytics
- **Done when:** Events visible in analytics with `variant` and `device` properties.
