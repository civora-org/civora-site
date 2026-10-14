---
name: Civora (civora.sk), identity "Dvere"
description: Warm but strict, like a beloved teacher. Trust between people and their town.
colors:
  indigo: "#34408a"
  indigo-deep: "#232c63"
  terracotta: "#b5523a"
  terracotta-deep: "#9a4430"
  clay-tint: "#f4d9cc"
  paper: "#fbf6ee"
  cream: "#f3e9db"
  rule: "#e3d8c8"
  ink: "#2b2a40"
  muted: "#5b576c"
  white: "#ffffff"
typography:
  display:
    fontFamily: "Alegreya Sans, system-ui, sans-serif"
    fontSize: "clamp(2.5rem, 1.4rem + 4.4vw, 4.25rem)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.012em"
  headline:
    fontFamily: "Alegreya Sans, system-ui, sans-serif"
    fontSize: "clamp(1.9rem, 1.3rem + 2vw, 2.75rem)"
    fontWeight: 700
    lineHeight: 1.1
  title:
    fontFamily: "Alegreya Sans, system-ui, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 700
    lineHeight: 1.15
  body:
    fontFamily: "Source Sans 3, system-ui, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Source Sans 3, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 600
rounded:
  card: "10px"
  pill: "999px"
  arch: "999px 999px 20px 20px"
spacing:
  gutter: "clamp(20px, 5vw, 48px)"
  section: "clamp(56px, 8vw, 104px)"
components:
  button-primary:
    backgroundColor: "{colors.terracotta}"
    textColor: "{colors.white}"
    rounded: "{rounded.pill}"
    padding: "0 28px"
    height: "48px"
  button-primary-hover:
    backgroundColor: "{colors.terracotta-deep}"
  panel-quiet:
    backgroundColor: "{colors.cream}"
    textColor: "{colors.ink}"
  band-strict:
    backgroundColor: "{colors.indigo-deep}"
    textColor: "{colors.paper}"
---

# Design System: Civora (civora.sk)

Shipped state of the civora.sk landing page and 404 page. Token names and values match `brand/tokens.css`; the site inlines them in `index.html` (`:root`, prefix `--civora-`). Brand source: the "Dvere" identity (round 2, variant 1).

## Overview

**Creative North Star: "The Open Door"**

Civora is the quiet, dependable place where people and their town hall meet. The page behaves like a good clerk who respects you: calm in tone, exact in facts, never loud. An indigo arch with a lit terracotta doorway is the mark, and the page repeats that shape sparingly (the hero dome, the step doors, the closing row of doors) instead of decorating with anything else.

The ground is warm paper, never white. Indigo carries strictness (links, headings accents, the mark); terracotta carries warmth and is reserved for the single primary action and the lit door. Roughly 70 % paper and cream, 20 % indigo, 10 % terracotta. The earlier cold blue-on-white look is an anti-reference: no blue buttons, no navy band, no grey tints.

**Key Characteristics:**
- Warm paper ground, one strict deep-indigo band (the closing call to action).
- Humanist type pairing: Alegreya Sans for voice, Source Sans 3 for reading.
- Terracotta only on fills (button, door); never on body text.
- Flat surfaces with hairlines; depth only on product screenshots.
- Slovak first: every face and subset covers ľ š č ť ž ý á í é ô ä ň ď.
- Product truth in copy: numbers and sources over adjectives, no prices, no pilot terms.

## Colors

A paper-and-ink palette with one cool anchor and one warm companion.

### Primary
- **Modrotlač Indigo** (#34408a): links, feature titles, the active gallery title, the arch in the mark, step doors 1, 2 and 4. 8.7:1 on paper.
- **Terakota** (#b5523a): the primary button fill, the lit doorway, step door 3. White on it is 4.96:1; never use it as text colour.
- **Terakota Deep** (#9a4430): hover state of the primary button only. Derived for this site; not a brand colour.

### Neutral
- **Teplý Papier** (#fbf6ee): page ground and the reversed text on indigo.
- **Krém** (#f3e9db): the hero dome and quiet full-width sections (workflow, gallery).
- **Hlina** (#f4d9cc): soft fill, selection highlight, the middle door in the closing row.
- **Tuš** (#2b2a40): body and headings. Warm, not black. 12.9:1 on paper.
- **Prach** (#5b576c): secondary text. 6.45:1 on paper, 5.8:1 on cream.
- **Rule** (#e3d8c8): hairlines and dividers.
- **Deep Indigo** (#232c63): the one strict band. Text on it is paper or #e3dcee (9.8:1).

### Named Rules
**The One Warm Thing Rule.** Terracotta appears once per viewport as an action (the button) plus at most the doors. If two things glow, neither is the door.
**The No Pure White Rule.** Brand surfaces use paper or cream. White is only for product screenshots.

## Typography

**Display Font:** Alegreya Sans 700 (self-hosted, fallback system-ui)
**Body Font:** Source Sans 3 400 / 600 (self-hosted, fallback system-ui)

**Character:** A humanist, slightly old-fashioned friendly display face over a clear, neutral reading face. The headline sounds like a person; the paragraph reads like a form you can trust.

### Hierarchy
- **Display** (700, clamp 2.5 to 4.25rem, 1.1, -0.012em): the single H1 on the page.
- **Headline** (700, clamp 1.9 to 2.75rem, 1.1): section headings (H2).
- **Title** (700, 1.5rem, 1.15): step names and gallery items (H3); feature terms at 1.375rem in indigo.
- **Body** (400, 1.125rem, 1.55): copy, measure capped at 66ch. Lead paragraph 1.3125rem in muted.
- **Label** (600, 1rem): navigation, buttons, facts.

### Named Rules
**The Slovak Subset Rule.** Alegreya ships as `latin` + `latin-ext` 700 woff2, Source Sans 3 as `latin` + `sk-ext` 400/600. Preload the ones above the fold; never load fonts from third-party hosts.
**The Weight Is Emphasis Rule.** Headings are 700, nothing is gradient, spaced out, or all-caps. The 500 weight belongs to the wordmark outlines only.

## Layout

A single-column static page. `.wrap` is a 1180px container with a fluid gutter (20 to 48px). Sections alternate paper and cream with generous vertical rhythm (56 to 104px). Two-column splits (4fr / 7fr) collapse to one column at 900px; the four workflow steps go 4, 2, 1 columns at 900px and 640px. Phone first in behaviour: no horizontal scroll at 375px, the header keeps only the wordmark and the primary button below 640px, and the hero button goes full width. Gallery: a tablist with a sticky stage at 960px and wider, stacked frames elsewhere and without JavaScript.

## Elevation & Depth

Flat by default; hairlines (`--civora-rule`) separate. The only lifted element is a product screenshot frame (`0 1px 2px rgba(43,42,64,.08), 0 24px 40px -24px rgba(43,42,64,.3)`), because it is a window onto another surface. No glass, no glow, no hard offset shadows.

## Shapes

The arch is the one signature shape: a half-circle top on a rectangular body. It appears as the hero dome (`border-radius: 999px 999px 20px 20px`), as the numbered step doors (56 x 68px, 28px top radius), and in the closing row of three doors (SVG, `viewBox="0 -12 268 162"`). Everything else is calm: buttons are pills, cards and screenshots use 10px radius, hairlines are 1px.

## Components

### Buttons
- **Primary:** terracotta fill, white 600 text, pill, 48px high (44px in the header), 28px side padding. Hover darkens to Terakota Deep. One per viewport. Focus ring: 3px indigo outline offset 3px (paper outline on the indigo band).
- **Text link:** indigo, underlined with 0.18em offset; hover thickens to 2px and deepens.

### Navigation
Wordmark SVG left, three plain labels and the primary button right. Labels get a 2px indigo underline on hover. Below 640px only the wordmark and the button remain.

### Steps (doors)
An ordered list of four items, each opened by an indigo arch holding its number (terracotta for the publication step). Title in Alegreya, description in muted.

### Feature list
A two-column definition list with a hairline above each pair. Term: Alegreya 1.375rem indigo. Description: muted, 44ch.

### Product frame and gallery
Screenshots sit in a 1px rule frame with 10px radius. They show the fictional "Obec Ukážková" only and still carry the product's current look. Every gallery screenshot has five files (PNG plus WebP at four widths) and a `?v=YYYYMMDD` cache-bust.

### Closing band
The only deep-indigo surface: paper heading, #e3dcee text, white underlined contact links, the primary button, and the three doors on the right.

### Brand files
Published at stable URLs under `/brand/` (wordmarks, marks at 16 to 512 px, icons, tokens), plus `/favicon.svg`, `/favicon.ico`, `/apple-touch-icon.png`, `/manifest.webmanifest` and the 1200 x 630 Open Graph image at `/img/og-image.png`. The e-mail signature uses `https://civora.sk/brand/mark-96.png`.

## Do's and Don'ts

### Do:
- **Do** keep paper as the ground and use terracotta once per viewport, for the action.
- **Do** write calm, exact copy: "Verejné ešte neznamená čitateľné", "Poďte dnu, pozrite sa sami".
- **Do** lead with trust between people and their town; present Civora Zmluvy as the first product.
- **Do** keep the CRZ attribution wherever CRZ data is shown (footer and the CRZ detail screenshot).
- **Do** show only the fictional "Obec Ukážková" in screenshots, and use "Cena podľa veľkosti obce — pošlem ponuku" for pricing.
- **Do** check 375px (no horizontal scroll) and Slovak diacritics in every face after a copy change.

### Don't:
- **Don't** publish prices, pilot terms or the names of prospect towns anywhere on the site.
- **Don't** recolour, rotate, stretch, shadow or crop the mark; below 24px use `mark-tight`.
- **Don't** put terracotta on text, or paper text on terracotta below 4.5:1 (white on #b5523a is 4.96:1).
- **Don't** reintroduce the old cold blue, navy bands, grey tints or white page grounds.
- **Don't** use hype ("revolučný", "AI"), superlatives, urgency, emoji, or accuse towns of hiding contracts.
- **Don't** add third-party fonts, scripts or stylesheets; the page stays self-contained.
