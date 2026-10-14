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

Civora is the quiet, dependable place where people and their town hall meet. The page behaves like a good clerk who respects you: calm in tone, exact in facts, never loud. An indigo arch with a lit terracotta doorway is the mark, and the page builds its whole illustration language from that shape plus the modrotlač pattern (town, hall, houses, people at a door) and leads with people and a story, not with features.

The ground is warm paper, never white. Indigo carries strictness (links, headings accents, the mark); terracotta carries warmth and is reserved for the single primary action and the lit door. Roughly 70 % paper and cream, 20 % indigo, 10 % terracotta. The earlier cold blue-on-white look is an anti-reference: no blue buttons, no navy band, no grey tints.

**Key Characteristics:**
- Warm paper ground, one strict deep-indigo band (the closing call to action).
- Story first: a clerk, a colleague, a citizen, in short concrete moments; a founder's letter instead of a pitch.
- Humanist type pairing: Alegreya Sans for voice, Source Sans 3 for reading.
- Terracotta only on fills (button, door); never on body text.
- Flat surfaces with hairlines; depth only on product screenshots.
- Slovak first: every face and subset covers ľ š č ť ž ý á í é ô ä ň ď.
- Product truth in copy: numbers and sources over adjectives, no prices, no pilot terms.

## Colors

A paper-and-ink palette with one cool anchor and one warm companion.

### Primary
- **Modrotlač Indigo** (#34408a): links, checklist titles, the active gallery title, the arch in the mark, the town hall and the checklist arches. 8.7:1 on paper.
- **Terakota** (#b5523a): the primary button fill, the lit doorway, the CRZ checklist arch. White on it is 4.96:1; never use it as text colour.
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
- **Title** (700, 1.5rem, 1.15): vignette and gallery titles (H3); checklist titles at 1.375rem in indigo.
- **Body** (400, 1.125rem, 1.55): copy, measure capped at 66ch. Lead paragraph 1.3125rem in muted.
- **Label** (600, 1rem): navigation, buttons, facts.

### Named Rules
**The Slovak Subset Rule.** Alegreya ships as `latin` + `latin-ext` 700 woff2, Source Sans 3 as `latin` + `sk-ext` 400/600. Preload the ones above the fold; never load fonts from third-party hosts.
**The Weight Is Emphasis Rule.** Headings are 700, nothing is gradient, spaced out, or all-caps. The 500 weight belongs to the wordmark outlines only.

## Layout

A story, not a template. `.wrap` is a 1180px container with a fluid gutter (20 to 48px). Order: hero (text left, illustrated town right, standing on a cream ground and a modrotlač strip), the story (a narrow 900px column, three vignettes zig-zagging at 230px art), "Čo si môžete overiť" (a 4fr/7fr split with a hairline checklist, on cream), the screenshots (small and secondary), the founder's letter (photo placeholder plus a letter sheet, on cream), and the one indigo band. No card grid, no numbered steps, no feature grid. Splits collapse at 900px; below 640px the header keeps only the wordmark and the button, vignettes stack, and the hero button goes full width. No horizontal scroll at 375px.

## Elevation & Depth

Flat by default; hairlines (`--civora-rule`) separate. Lifted: screenshots (they are windows onto another surface, always inside a cream mat with a demo-data caption) and the letter sheet (very soft). No glass, no glow on UI, no hard offset shadows.

## Shapes

The arch is the one signature shape (`999px 999px 20px 20px`, or an SVG `a` arc). It is the town hall, every house, every doorway, every window, every figure's body, the vignette frames, the photo placeholder and the closing doors. Everything else is calm: pills for buttons, 10px radius for screenshots, 1px hairlines.

## Illustration Language

Own SVG, inline, built from three things only: arches, the palette, and the modrotlač pattern.
- **Town:** the town hall is the mark scaled up (indigo arch, terracotta doorway, a clock showing the visitor's local time). Houses are smaller arches in clay, deep indigo and cream with arched windows. Flat fills, no outlines except thin deep-indigo details on the clock and flag.
- **People:** abstract paper dolls, an arch body plus a round head, no faces, no skin tones, in paper, clay and cream. Never generated, never stock. Names in copy are invented and the page says so.
- **Modrotlač:** a 22px tile of paper-coloured dots (a five-dot flower plus corner dots) printed on indigo, like resist-dyed cloth. Used only as the strip under the hero, as the top edge of the letter, and on the hall's frieze. It lives in `--mr` (CSS data URI) and `#mr` (SVG pattern); keep both in sync.
- **Vignettes:** one 200 x 240 arch per person (clay, indigo, cream grounds); the one warm element in each (lamp, magnifier, window) is terracotta.
- **Rules:** one terracotta thing per scene; terracotta-deep only for the silhouette in the lit door. Illustrations are `aria-hidden` except the hero, which is `role="img"` with a Slovak label.

## Motion

Quiet and respectful. Defaults are always visible; motion enhances them.
- **Door light:** `--lit` on the hero scene warms from 0.2 to 1 as you scroll the first 90% of a viewport. It drives the opacity of the peach door layer, the halo, the floor glow and the silhouette in the doorway.
- **Rising in:** houses, hall, people, doors and each vignette rise 18 to 26px and fade in once, staggered by `--d`, with `cubic-bezier(.16,1,.3,1)`. One observer, no libraries.
- **Delight:** the town hall clock shows the visitor's own time.
- `prefers-reduced-motion: reduce` turns all of it off (content visible, door lit at 0.85, no transitions). Without JavaScript everything is visible (`.js` is only set by script).

## Components

### Buttons
- **Primary:** terracotta fill, white 600 text, pill, 48px high (44px in the header), 28px side padding. Hover darkens to Terakota Deep (and lifts 1px with a pointer). One per viewport. Focus ring: 3px indigo outline offset 3px (paper outline on the indigo band).
- **Text link:** indigo, underlined with 0.18em offset; hover thickens to 2px and deepens.

### Navigation
Wordmark SVG left, three plain labels (Príbeh, List, Ukážky) and the primary button right. Below 640px only the wordmark and the button remain.

### Checklist ("Čo si môžete overiť")
A `ul` of six hairline-separated items. Each opens with a small indigo arch (terracotta for the CRZ item), a 1.375rem Alegreya title in indigo, a muted sentence.

### Founder's letter
A paper sheet with a modrotlač top edge, first-person copy signed "Denys Kozlov", next to a dashed arch holding the literal text `[FOTO]` until a real photograph exists. Never a stock or generated face.

### Product frame and gallery
Screenshots sit in a cream mat, then a 1px rule frame with 10px radius, at most 560px wide, below the story. They show the fictional "Obec Ukážková" only and still carry the product's current look; the note says so. Every screenshot has five files (PNG plus WebP at four widths) and a `?v=YYYYMMDD` cache-bust. Tablist with a sticky stage at 960px and wider, stacked frames elsewhere and without JavaScript.

### Closing band
The only deep-indigo surface: paper heading, #e3dcee text, white underlined contact links, the primary button, the offer line ("Cena podľa veľkosti obce — pošlem ponuku", no prices) and the three doors on the right, which rise in.

### Brand files
Published at stable URLs under `/brand/` (wordmarks, marks at 16 to 512 px, icons, tokens), plus `/favicon.svg`, `/favicon.ico`, `/apple-touch-icon.png`, `/manifest.webmanifest` and the 1200 x 630 Open Graph image at `/img/og-image.png`. The e-mail signature uses `https://civora.sk/brand/mark-96.png`.

## Do's and Don'ts

### Do:
- **Do** keep paper as the ground and use terracotta once per viewport, for the action.
- **Do** write like a person: short sentences, concrete moments, invented names that the page admits are invented. "Verejné ešte neznamená čitateľné", "Poďte dnu, pozrite sa sami".
- **Do** keep motion optional: visible by default, off for reduced motion, no libraries.
- **Do** lead with trust between people and their town; present Civora Zmluvy as the first product.
- **Do** keep the CRZ attribution wherever CRZ data is shown (footer and the CRZ detail screenshot).
- **Do** show only the fictional "Obec Ukážková" in screenshots, and use "Cena podľa veľkosti obce — pošlem ponuku" for pricing.
- **Do** check 375px (no horizontal scroll) and Slovak diacritics in every face after a copy change.

### Don't:
- **Don't** go back to a card grid, a numbered "Postup 1-2-3-4", a feature list or a trust strip.
- **Don't** use stock photos or AI-generated people; the only photo allowed is a real one of the founder, replacing `[FOTO]`.
- **Don't** publish prices, pilot terms or the names of prospect towns anywhere on the site.
- **Don't** recolour, rotate, stretch, shadow or crop the mark; below 24px use `mark-tight`.
- **Don't** put terracotta on text, or paper text on terracotta below 4.5:1 (white on #b5523a is 4.96:1).
- **Don't** reintroduce the old cold blue, navy bands, grey tints or white page grounds.
- **Don't** use hype ("revolučný", "AI"), superlatives, urgency, emoji, or accuse towns of hiding contracts.
- **Don't** add third-party fonts, scripts or stylesheets; the page stays self-contained.
