# 24 — Mobile Apps

**Phase:** P3 · **Depends on:** 16 (API), 01 (tokens), P1 live · **Status:** Draft

## 1. Purpose
Native iOS and Android apps for customers (and a light vendor app) built on the **same API** and design tokens, so no backend rewrite is needed. Until then, the web is an installable PWA.

## 2. Approach
- **React Native with Expo** (TypeScript), sharing `packages/api-client`, validation schemas, and design tokens (`dist/rn/theme.ts`) from the monorepo.
- **Customer app** first (full shopping). **Vendor app** second: a focused companion for orders (accept, dispatch, scan tracking barcode with camera), push alerts, quick price/stock edits, payouts view. Full catalog management stays on web.
- Payments via the gateway's React Native SDK (physical goods — app-store in-app purchase rules don't apply).

## 3. App-specific features
| Feature | Customer | Vendor |
|---|---|---|
| Push notifications (FCM/APNs) | Order updates, back-in-stock, price drop on wishlist | New order (high priority), SLA reminders, payouts |
| Deep links / universal links | Product, store, look, order links open in app | Order links |
| Camera | Try-on (23), review photos | Barcode scan of tracking ID, dispatch photo |
| Biometric login | Optional | Optional (Face ID / fingerprint) |
| Offline | Cached wishlist & recent views | Cached order list |
| Intro experience | Native splash → short intro on first launch (02 rules) | — |
| Share | Native share sheet | Store share card |

## 4. Release requirements
- Developer accounts (Apple, Google), app privacy labels / data safety forms matching 18 data map.
- App icons/splash from 01.
- OTA updates (Expo EAS Update) for JS fixes; store releases for native changes.
- Minimum OS: iOS 16, Android 8 (API 26).
- Crash reporting (Sentry) and analytics events identical to web (19).
- Account deletion available in-app (store requirement).
