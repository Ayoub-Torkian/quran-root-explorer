# DESIGN SYSTEM — single source of truth (v2.0, user-mandated)

One palette, one type scale, everywhere: app pages, charts, sidebar, banners, cards.
Any future UI work MUST use these tokens. No off-palette hex. No ad-hoc font sizes.

## 1. Color tokens — every color has ONE meaning

| Token | Hex | Allowed use (ONLY this) |
|---|---|---|
| NAVY | #1D3557 | Identity: hero bands, section headers, chart hub/emphasis |
| NAVY-TEXT | #16365C | Interactive text: links, secondary-button text, nav items |
| INK | #243447 | Body text (markdown, paragraphs) |
| INK-SOFT | #3D4757 | Captions, secondary text — the LIGHTEST text allowed |
| TEAL | #1D9E75 | GO actions (primary buttons) · positive/Qur'an data series · Meccan bars |
| TEAL-DARK | #0F6E56 | Hover state of TEAL · strong positive text |
| BLUE | #378ADD | Charts: the SEMANTIC/meaning channel |
| ORANGE | #EF9F27 | Charts: the TERRITORY/co-location channel |
| AMBER | #E9C46A | INTERNAL-ONLY verdict class · soft warnings |
| RED | #E63946 | Destructive actions · danger · Medinan bars · DIVERGENT relation. NEVER decoration |
| GREY-DATA | #B4B2A9 | Chart series for neutral comparators (ord/sajʿ) ONLY |
| BORDER | #E2E8F1 | Card/expander borders (light) |
| BORDER-2 | #C9D6E8 | Input/button borders (stronger) |
| BG-PAGE | #FAFBFD | App background |
| BG-CARD | #FFFFFF | Cards, expanders, metric tiles |
| BG-TINT | #EEF3FB | Info panels / banners (with NAVY left border) |

**Banned:** gradients (sole exception: the global progress ribbon) · text-shadow ·
gold/yellow backgrounds (#FCBF49, #FFF3B0, #FFF8E1) · gray TEXT (#6B7280, #888, #999,
#444…) — gray exists only in borders and the GREY-DATA chart series.

## 2. Type scale — one proportional ladder (px)

| Step | Size | Use |
|---|---|---|
| XXL | 30 | h1 — one per page max |
| XL | 23 | h2 |
| L | 19 | h3 / tile titles |
| M+ | 17 | hero band title |
| M | 15 | UI labels, layer labels |
| BASE | 14 | body UI: buttons, nav links, table text, expander headers (14.5) |
| S | 13.5 | captions, widget labels, chart captions |
| XS | 12 | chip metadata, fine print — NOTHING below 12 |

**Arabic text (content, not UI):** verse display 24–29 · chip roots 20–22 · inline 16–18.
Weights: 400 body · 600 interactive · 700 headers · 800 reserved for the hero band only.

## 3. Chart conventions (recap of APP_PLAN locked standard)
Series: Qur'an/positive = TEAL · semantic = BLUE · territory = ORANGE · comparators =
GREY-DATA · Medinan = RED, Meccan = TEAL (control-only label mandatory). Margins
l10/r10/t40/b10, heights 240–320. Every chart: computed "📍 What to take from this" line.
Geometry must encode meaning (rule 4b).

## 4. Where it's enforced
Global CSS: `state.py` (inject_css + render_grouped_nav). Inline HTML in pages must use
tokens above. Plotly colors per §3. The enforcement sweep (phase 10) normalized all
pre-existing off-palette hex and font sizes; run a grep for `#F77F00|#FCBF49|#FFF3B0`
and `font-size` outliers before any release.
