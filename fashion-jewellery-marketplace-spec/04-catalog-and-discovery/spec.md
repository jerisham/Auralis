# 04 — Catalog & Discovery

**Phase:** P1 · **Depends on:** 01, 16, 17 · **Status:** Draft

## 1. Purpose
Help customers find the right piece fast across all vendors: categories, search, filters built for fashion jewellery, occasions, "complete the look", and vendor stores. All vendors' products appear in one unified catalog with one consistent layout.

## 2. Category tree (admin-managed, 2 levels)
| Category | Sub-categories |
|---|---|
| Earrings | Studs, Jhumkas, Hoops, Drops & Danglers, Chandbalis, Ear cuffs, Ear chains |
| Necklaces | Chokers, Pendants, Layered, Long / Rani haar, Chains |
| Jewellery sets | Necklace sets, Bridal sets, Choker sets |
| Bangles & Bracelets | Bangles, Kada, Bracelets, Cuffs |
| Rings | Statement, Adjustable, Stackable, Toe rings |
| Anklets | — |
| Nose pins & rings | Nose pins, Nath, Septum (clip-on) |
| Head & Hair | Maang tikka, Matha patti, Hair clips, Passa |
| Others | Brooches, Waist chains (kamarbandh), Men's |

## 3. Product attributes (filterable)
| Attribute | Values (examples) | Required |
|---|---|---|
| Style | Ethnic, Western, Indo-western, Minimal, Statement, Boho | Yes |
| Base material | Brass, Copper, Alloy, Stainless steel, 925 silver-plated, German silver / Oxidised, Beads, Fabric, Resin | Yes |
| Plating / finish | Gold-plated, Rose-gold, Rhodium, Antique, Oxidised, Matte, Meenakari | Yes |
| Stones / work | Kundan, Polki-style, American diamond (CZ), Pearl, Crystal, Temple, Beads, None | No |
| Colour | Multi-select palette | Yes |
| Occasion | Wedding, Festive, Party, Office, Everyday, Gifting | Yes (multi) |
| Skin safety | Nickel-free, Lead-free, Hypoallergenic, Anti-tarnish | No (vendor declares; see rules) |
| Size / fit | Length (cm), Adjustable, Ring size, Bangle size (2.4/2.6/2.8) | Category-specific |
| Weight (g) | Number | Yes |
| Price | Range | — |
| Rating | 4★ & up | — |
| Delivery | "Ships within 24 h", seller city | — |
| Seller | Vendor multi-select | — |

## 4. Functional requirements
| ID | Requirement |
|---|---|
| FR-04-01 | Product listing page (PLP) per category, sub-category, occasion, collection, look, vendor and search query. |
| FR-04-02 | Filters per §3 in a sheet (mobile) / sidebar (desktop); applied filters as removable chips; counts per filter value. |
| FR-04-03 | Sort: Relevance (default), New, Price ↑, Price ↓, Popular, Rating. |
| FR-04-04 | Search with autocomplete (products, categories, vendors), typo tolerance, and synonyms incl. Hinglish ("jhumki"→jhumka, "jhumka"→jhumkas, "AD"→american diamond, "oxidized"→oxidised, "tikka"→maang tikka). |
| FR-04-05 | Recent and trending searches; "no results" page suggests closest categories and popular items. |
| FR-04-06 | Product card: image (second image on hover), name, vendor name, price, MRP + % off, rating, wishlist heart, badges (New, Bestseller, Nickel-free, Ships in 24h). |
| FR-04-07 | Infinite scroll on mobile (with "back" restoring scroll position), pagination on desktop; URLs reflect filters for sharing/SEO. |
| FR-04-08 | **Looks:** curated sets of 2–5 products (any vendors) with a hero image, title and occasion; "Add all to cart". Admin-curated in P1; auto-suggested in P2 (23). |
| FR-04-09 | **Fair ranking:** relevance blends text match, conversion rate, rating, freshness, vendor reliability score (dispatch SLA, disputes); cap of 3 products per vendor in the top 12 of category pages to give small sellers visibility. |
| FR-04-10 | Out-of-stock items hidden from PLP by default (toggle "show out of stock"). |
| FR-04-11 | Products from suspended/on-holiday vendors hidden from PLP and search. |
| FR-04-12 | "Sellers" directory page: browse all vendors with filters (city, speciality, rating). |

## 5. Rules
- Skin-safety claims: vendor must tick a declaration; claims shown with "Seller declared" note; admin may require a lab report for "Hypoallergenic" badge (P2). False claims → strike policy (11).
- Search index updated ≤ 60 s after product create/update/stock change.

## 6. Edge cases
- Very large result sets → facet counts approximate beyond 10k (acceptable).
- Filter combination with 0 results → show "Remove a filter" suggestions.
