# 01 — Design System

**Phase:** P0 · **Depends on:** 00, Q-01 (brand) · **Status:** Draft
> **Decision (17 Nov 2026, Q-01):** Brand name is **Auralis**. Domain, Instagram handle, and trademark (classes 14/35) are still to verify. Visual direction remains Midnight Atelier.

## 1. Purpose
One visual language for every screen (customer, vendor, admin, later mobile apps). The look must feel **premium, glossy and cinematic** — "a new world" — while staying fast and easy. The platform owns the design; vendors never change it.

## 2. Design direction — "Midnight Atelier"
Dark, rich backgrounds that make metallic and stone jewellery glow, with warm champagne-gold accents and generous white space. Light mode for vendor/admin portals (long working sessions) and as a customer option.

### Colour tokens
| Token | Value (starting point) | Use |
|---|---|---|
| `--bg-base` | `#0E0D10` | Customer app background (dark) |
| `--bg-elevated` | `#17151B` | Cards, sheets |
| `--glass` | `rgba(255,255,255,0.06)` + 16px backdrop blur | Floating nav, filter sheet |
| `--gold-500` | `#D4AF6A` | Primary accent, CTAs, prices |
| `--gold-gradient` | `linear-gradient(135deg,#F3E2B3,#D4AF6A 45%,#A8823E)` | Primary button, highlights |
| `--rose-400` | `#E8B4A0` | Secondary accent (rose gold) |
| `--ivory-50` | `#F7F3EC` | Text on dark; light-mode background |
| `--ink-900` | `#1A1A1E` | Text on light |
| `--muted` | `#9A94A3` | Secondary text |
| `--success` / `--warning` / `--danger` | `#4CAF7D` / `#E2A93B` / `#E0605E` | Status |

All text/background pairs must meet WCAG 2.2 AA contrast (4.5:1 body, 3:1 large text). Gold on dark is used for large text/buttons only, never small body text.

### Typography
- **Display:** an elegant serif (e.g., *Cormorant Garamond* or *Playfair Display*) — headings, hero text, product names on PDP.
- **UI/Body:** a clean sans (e.g., *Manrope* or *Inter*) — everything else, prices, forms.
- Scale (px): 12 · 14 · 16 (base) · 20 · 24 · 32 · 44 · 60. Line height 1.5 body, 1.15 display.
- Indian rupee: always `₹1,299` (Indian digit grouping via `Intl.NumberFormat('en-IN')`).

### Space, shape, depth
- 4px base spacing grid; container max 1280px; product grid gutters 16 (mobile) / 24 (desktop).
- Radius: 12 cards, 999 pills/buttons, 20 sheets.
- Shadows: soft, warm (`0 8px 32px rgba(0,0,0,.35)` on dark).
- "Gloss": subtle animated sheen on hero product cards and primary CTA hover (CSS gradient sweep, 1.2s, once).

### Motion
- Durations: 150ms (micro), 250ms (UI), 400ms (page/sheet), easing `cubic-bezier(.2,.8,.2,1)`.
- Product images: fade-and-scale-in on load; hover swaps to second image.
- `prefers-reduced-motion` → disable sheen, parallax and autoplay video.

### Imagery rules (shared with vendors in 08/10)
- Square 1:1 primary image, min 1200×1200, plain or soft background, product centred.
- Additional: on-model shot, scale reference (coin/hand), close-up detail.
- Platform auto-generates sizes and WebP/AVIF (see 16).

## 3. Components (minimum library)
Buttons (primary gold, secondary outline, ghost, icon) · Inputs (text, OTP, phone with +91, select, textarea, price) · Chips/filters · Product card · Vendor card · Look card · Price block (MRP strike-through, selling price, % off) · Rating stars · Badge (Nickel-free, New, Bestseller, Verified seller) · Bottom sheet · Modal · Toast · Tabs · Stepper · Empty state · Skeleton loaders · Pagination/infinite scroll · Data table (vendor/admin) · Stat tile & chart wrapper (dashboard) · Image uploader with crop · Navigation: top bar (desktop), bottom tab bar (mobile: Home, Explore, Looks, Cart, Account).

## 4. Fixed layout rules (the "common view")
- Logo always top-left; search centre (desktop) / top (mobile); cart + account top-right.
- Footer identical everywhere: About, Sell with us, Help, Policies, social links.
- Vendor content appears only in defined slots (see 09). No vendor-controlled CSS, fonts, or colours.

## 5. Deliverables
1. Figma library (tokens, components, 3 key templates per portal).
2. Tokens exported as JSON (Style Dictionary) → CSS variables + React Native theme (for 24).
3. Coded component library (React + Storybook).
