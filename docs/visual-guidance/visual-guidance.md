# Visual guidance

The visual direction of eis-ds, the references it came from and what was taken from each. Use it for future lookup: when deciding a token or building a piece, come back here to see **where** each choice came from.

> Usage rules for tokens and elements live in `docs/manual/`. This file is direction, provenance and decision history.

> This document describes direction and observations. Final values exist only in `src/shared/tokens/` and `src/<scope>/tokens/`. While a value appears here as "measured" or "observed", it is a candidate, not a decision.

---

## 1. Direction

**Minimalist retrofuturism.** The future as imagined from the 60s to the 90s (lab equipment, radio, calculator, home computer, science fiction poster), drawn with today's discipline and cleanliness.

What it **is**: industrial product, screen-printed panel, visible grid, thin line, a single color signal, engineering typography.

What it **is not**: neon, synthwave, glitch, purple and pink gradient, chrome, "cyberpunk". These images appeared in the illustration references and were noted, but they do not define the system (see §5).

One sentence to guide any piece: **it looks like an equipment manual someone made too beautiful.**

---

## 2. Sources

> The image files left the repository on 2026-10-25 to keep it small. The Pinterest links are now the source of record. Images without a link (Teenage Engineering screenshots, images sent directly) are not stored. Their observations stay in the tables below, and the values taken from them are already in the tokens.

### 2.1 Anchor: Teenage Engineering

The starting point of the inspiration. The brand's product language and graphic communication are the base of the system.

- Site: https://teenage.engineering/
- Screenshots of the site and products, not stored:

| Reference | What it shows |
|---|---|
| `vinyl-sinus.png` | Record and sleeve: display typography, thin rules, brackets |
| `ko2-flat.png` | EP–133 K.O. II from above: key grid, orange as signal, outlined title |
| `tp7.png` | TP-7 in aluminum: small uppercase labels, red only on the record button |
| `po80-record-factory.png` | PO-80: orange as surface, an exception to the rule |
| `op-xy.png` | OP-XY: matte black, keys in a grid, orange LED |
| `riddim-ting.png` | EP–40 Riddim: dark product green, signals in red |
| `tx6.png` | TX-6 on black: large thin typography, small product in the center |
| `ep-series-lineup.png` | EP family: repeated modules, Japanese as texture, each product with its own color |
| `op1-field.png` | OP-1 field: aluminum, screen with information blue |
| `ep-series-update.png` | Graphic piece: ruled table, UPDATE label in an orange block, version number as title |

### 2.2 Moodboard: retrofuturism (Pinterest)

These widen the repertoire, mainly for **illustrations and images**. Links below.

| Reference | Pin | What it shows |
|---|---|---|
| `palette-modern-retro-industrial.jpg` | [1132233162604331330](https://br.pinterest.com/pin/1132233162604331330/) | "Modern Retro Industrial" palette, with published hex values (see §3.2) |
| `retrofuturism-helmet-goggles.jpg` | [521925044333070995](https://br.pinterest.com/pin/521925044333070995/) | Portrait with helmet, pink and blue neon |
| `poster-luna.jpg` | [442478732134038569](https://br.pinterest.com/pin/442478732134038569/) | LUNA poster: Ball Chair, spherical TV, flat blue, rounded grotesque |
| `illus-sega-saturn-desk.jpg` | [354588170671333402](https://br.pinterest.com/pin/354588170671333402/) | Desk illustration with console, black line and flat color |
| `diagram-wormhole-blue.jpg` | [669840144618923623](https://br.pinterest.com/pin/669840144618923623/) | Wormhole diagram in white line on blue, red sphere |
| `logo-new-era-rainbow-stripes.jpg` | [850898923392490209](https://br.pinterest.com/pin/850898923392490209/) | "RETRO" logo with rainbow stripes on black |
| `diagram-wormhole-black.jpg` | [1136384918466043677](https://br.pinterest.com/pin/1136384918466043677/) | The same diagram in thin line on black, red dot |
| `illus-cyberpunk-monitor.jpg` | [324751823145896643](https://br.pinterest.com/pin/324751823145896643/) | Illustration: operator at the monitor, yellow mecha, neon |
| `poster-astral-plane.jpg` | [77616793573995629](https://br.pinterest.com/pin/77616793573995629/) | "Meeting on the Astral Plane" cover: stacked grid planes on black |
| `illus-amiga-desk-1994.jpg` | [461407924340903455](https://br.pinterest.com/pin/461407924340903455/) | "Lazy Saturday, 1994": desk with Amiga, black line and flat color |
| `scenography-prism-stars.jpg` | [634444666298973787](https://br.pinterest.com/pin/634444666298973787/) | Glass boxes, starry sky, spectral beam |
| `illus-retro-computer-library.jpg` | [1074812267312275160](https://br.pinterest.com/pin/1074812267312275160/) | Illustration of a desk with an old computer and bookshelf |
| `illus-space-eye.jpg` | [935904366328784289](https://br.pinterest.com/pin/935904366328784289/) | Mechanical eye in a detailed illustration |
| `illus-city-pink-moon.png` | no link (sent directly) | Machine city, pink moon, yellow sky, technical line |
| `illus-workbench-mess.png` | no link (sent directly) | Boy at an electronics workbench, anime style |

### 2.4 Palette

| Reference | Origin | What it shows |
|---|---|---|
| `orange-circles-grid` | sent directly, no link, not stored | Cards in orange, cream, olive black and yellow with thin-line circle diagrams. **Source of the system orange** (`#f35919`). Also has cream `#f0f2e7`, olive black `#2c2e20` and yellow `#f3cd4e`, noted and not adopted |

### 2.3 Interface (Pinterest)

UI references: sites, dashboards and apps. They define how the system behaves **on screen**. They come from the board [Interface Eis Design System References](https://br.pinterest.com/diegoeis/interface-eis-design-system-references/), with 66 pins as of 2026-10-25.

**Main**, chosen by the author and weighted more than the rest of the board:

| Reference | Pin | What it shows |
|---|---|---|
| `main-1-layout-poster-pipeline.jpg` | [203647214397329946](https://br.pinterest.com/pin/203647214397329946/) | "How we manage your network" site: light gray with visible background grid, white cards, wireframe illustration, large thin title |
| `main-2-dashboard-charts.jpg` | [203647214397329956](https://br.pinterest.com/pin/203647214397329956/) | Monochrome dashboard: labels and numbers in uppercase mono, bar chart made of cells, ruled table |
| `main-3-analytics-dashboard.jpg` | [203647214397329953](https://br.pinterest.com/pin/203647214397329953/) | Analytics dashboard: grid heatmap, red only on anomalies, 1px separators |
| `main-4-engineering-site.jpg` | [203647214397329912](https://br.pinterest.com/pin/203647214397329912/) | Engineering site: cream and orange, mono body text, orange section block with ruled table and isometric wireframe drawing |

**Rest of the board**, numbered in board order as of 2026-10-25 (01 is the first pin). Grouped by what it shows:

| Group | Numbers | What they add |
|---|---|---|
| Dashboards and apps | 01, 26, 29, 30, 32, 35, 37, 41, 50 | Versions or relatives of the main ones. 50 is dark mode with the same vocabulary |
| Sites and editorial layouts | 02, 09, 10, 17, 18, 22, 25, 42, 45, 47, 51, 53, 54, 61, 63, 65, 66 | Column grid, rules, large numbers (61), orange section block (45, 66), same page in blue (17) |
| Styleguides | 06, 15, 55, 60 | Component panel in cream and orange (06), "The Grid Is Lying" (15), technical sheet in blue line (55), mono as identity (60) |
| Mobile | 21, 31, 38, 56, 59 | List with large uppercase typography (21, 31), recorder as a physical device (38), number next to a color ball (56) |
| Login | 03, 24, 40 | Minimal form next to an image |
| Technical and isometric illustration | 04, 07, 14, 16, 19, 43 | Line isometric (07), technical section (43), line topography (16) |
| Retro object | 11, 28, 33, 36, 48, 49, 57, 62, 64 | Beige and gray devices with colored keys: the same universe as TE |
| Scene and illustration | 05, 08, 12, 13, 20, 23, 27, 34, 39, 44, 46, 52, 58 | Mood and color. See §5 |


---

## 3. What the references say

### 3.1 Teenage Engineering: the system's language

1. **Material before color.** The piece is almost entirely neutral: aluminum, gray and raw plastic, matte black.
2. **A single accent, orange-red, used as a signal.** It marks a state or calls attention (record, LED, "INPUT", version number), never decorates. It takes up to ~5% of the area. The exception is the PO-80, where it becomes surface: that is a **highlight mode**, not the rule.
3. **Engineering typography.**
   - Geometric grotesque, thin or regular, often uppercase.
   - Numbers as protagonists (`2.0`, `50`, `1.9.3`, `EP–133`), with a dash instead of a hyphen.
   - Large outlined titles, and numbers in segmented or LCD display.
   - Small, spaced uppercase labels (OUTPUT, INPUT, SYNC, MIDI), like panel screen printing.
   - Japanese (サンプラー) used as graphic texture.
4. **Visible grid.** The piece is a matrix of equal modules, with rigid alignment and lots of empty space around it.
5. **Thin line as structure.** 1px rules separate information, brackets group controls and diagonal hatching makes bands.
6. **Block labels.** Solid rectangle with knocked-out text ("UPDATE", "MIDI", "USB"). It is practically the only recurring graphic element.
7. **Simple shapes.** Rectangle with small radius, perfect circle, dot pattern (speaker grille).
8. **No shadow in the graphic piece.** The shadows in the references come from product photography.
9. **Three backgrounds:** uniform light gray, raw paper, near-total black.

### 3.2 Moodboard: what it adds

- **The "Modern Retro Industrial" palette converges with TE.** The published "Rust Signal" (`#EC4624`) falls within the range measured in TE's orange (`#DD451D`–`#FC6A34`, median `#F15033`). Two independent sources pointing at the same accent reinforce the choice.
  - Values published on the pin: Iron Core `#222A2A`, Industrial Aqua `#4FBBBC`, Rust Signal `#EC4624`, Heat Marker `#F39120`, Architectural Cream `#E2DAC2`.
  - **Iron Core** (greenish black) and **Architectural Cream** (warm raw) are natural candidates for the dark background and paper mode.
  - **Industrial Aqua** and **Heat Marker** remain candidates for illustration color, not system color (see §5).
- **Thin-line scientific diagram** (the two wormholes and "Astral Plane"): 1px white line, perspective grid, a single red dot. It is the same TE rule (thin line as structure, one color signal) applied to illustration. **It is the most direct model for article images.**
- **LUNA poster:** flat color background, iconic 60s object (Ball Chair, spherical TV), lots of empty space, rounded display typography and simple grotesque for information. Model for covers and opening slides.
- **Black-line illustration with flat color** (Saturn, Amiga, library, city): uniform outline, flat color without gradient, many technical objects. It is a possible language for scene illustration, denser than the system and only for when the piece calls for it.

### 3.3 Color observations

Measured by pixel sampling (Pillow, reduced images, median across images), except where marked "published".

| Candidate role | Value | Origin |
|---|---|---|
| Accent | `#F15033` (range `#DD451D`–`#FC6A34`) | Median across 8 TE images |
| Accent (published) | `#EC4624` | Palette pin |
| Cool light background | `#D0D0D0`–`#E0E0E0` | `tp7`, `op1-field`, `ko2-flat` |
| Paper background | `#E0E0D8` measured, `#E2DAC2` published | `po80-record-factory`, palette pin |
| Dark background | `#101010`–`#181818` measured, `#222A2A` published | `vinyl-sinus`, `tx6`, palette pin |
| Product green | `#0F3A2E`–`#174E3A` | `riddim-ting`, `ep-series-lineup` |
| Interface orange | `#E85818` (range `#E05818`–`#F87040`) | `main-4`, board 06, 25, 45, 66 |
| Interface canvas | `#E8E8E8`–`#F0F0F0`, panel `#F8F8F8` | `main-1`, `main-2`, `main-3` |
| Interface cream | `#F0E0C8`–`#F8E8D0` | `main-4`, board 06 |
| Variant blue | `#1850A8` | board 17 (the same page as `main-4`, in blue) |

The interface orange leans more toward yellow (`#E85818`) than TE's (`#F15033`). Only one can be chosen.

### 3.4 Interface: how the system behaves on screen

Drawn mainly from the 4 main references and confirmed by the rest of the board.

1. **Light gray canvas, near-white panel.** The screen is a uniform light gray and content sits on slightly lighter panels. Two surface levels, no more (`main-1`, `main-2`).
2. **Visible construction grid.** Thin grid lines in the background cross the whole page and the cards snap to them (`main-1`, board 15, 25). It is the technical drawing ruler turned into structural decoration.
3. **Panel without shadow.** The card is separated by surface tone, or by a 1px rule, never by shadow. The radius is small to medium, around 8–12px.
4. **Mono as the voice of the interface.**
   - Section labels and table headers in small **uppercase mono** (TOTAL REVENUE, SALES TREND, ID, STATUS).
   - **Numbers in mono** ($20,320, 10,320, 3.9%), which aligns columns and gives an instrument feel.
   - Breadcrumb and navigation in uppercase mono, with the current item in the accent (`main-4`).
   - On more editorial sites, the entire body text in mono (`main-4`, board 60).
5. **Grotesque at two extremes.** Large thin title in sentence case (`main-1`) or bold uppercase title (`main-4`). The middle ground barely appears.
6. **Data as a grid of cells.** Bars made of stacked squares (`main-2`), day heatmap (`main-3`), thin vertical bars. It is the same TE key matrix applied to charts.
7. **Monochrome chart, accent only on the exception.** Black and grays show normal data. Red and orange mark the anomaly (the violations in `main-3`). It is TE's signal rule applied to data.
8. **Ruled tables and lists.** 1px line between items, no zebra striping, numbered columns (`01`, `02`, `03`) and mono italic for secondary text (`main-4`).
9. **Accent block as a section.** A single section per page can be entirely orange, with dark-line drawing and a ruled table on top (`main-4`, board 45, 66). It is TE's highlight mode (PO-80) applied to the web: **one block per page**, never two.
10. **The variant swaps only the color.** Board 17 is the same page as `main-4` with blue instead of orange and white instead of cream. The structure does not change at all, which confirms the variant rule.
11. **Wireframe line illustration.** Technical isometric, dot field, spiral and technical section, always in thin single-color line, no fill (`main-1`, `main-4`, board 07, 43, 55).
12. **Discreet controls.** Pill segmented control (Weekly / Monthly / Yearly), status as a pill with a dot, thin-line icons and one dark solid primary button (Export CSV). Nothing is colored without reason.
13. **Dark mode with the same vocabulary** (board 50): same grids, same lines, inverted colors.

---

## 4. Principles (with budget)

Draft of the rules that become norms when the tokens are approved:

- **Accent ≤ 5% of the area** and only to signal: state, single highlight, key number. Never to decorate. Highlight mode (accent as background) is a declared exception per piece.
- **One signal color per piece.** If two things compete for the accent, one of them is not important.
- **Line before fill.** Separate with a 1px rule before thinking of a box or background.
- **Grid visible or implicit, never broken.** Alignment is mandatory. Asymmetry comes from composition, not misalignment.
- **Empty space is material.** A piece with little content and lots of space is right. A full one is wrong.
- **Small, spaced uppercase text** is a label. Running text is always in sentence case.
- **No shadow, no gradient and no glow** in the system's language. Illustration may have texture, but not effects. Only exception: the button glow on hover, as a response to interaction, never at rest.
- **Two surface levels on screen**: canvas and panel. A third level is a sign the composition needs a rule, not another box.
- **Every border and every rule uses `--line`.** Ink (`--ink`) never outlines a shape, panel or card. The only exception is the outline of interactive controls (checkbox, field), which uses `--ink-muted` for sufficient contrast (WCAG requires 3:1 for components).
- **Numbers and labels in mono, text in grotesque.** Mono is the voice of the instrument. Grotesque is the voice of the text.
- **Data in black and gray. The accent marks only the exception.**
- **One accent block per page, at most.**

---

## 5. Outside the core (noted, not adopted)

| What | Where it appears | Why it stays out |
|---|---|---|
| Pink, cyan and purple neon | `retrofuturism-helmet-goggles`, `illus-cyberpunk-monitor`, `illus-city-pink-moon` | Cyberpunk and synthwave: contradict "minimalist" |
| Rainbow stripes | `logo-new-era-rainbow-stripes`, `scenography-prism-stars` | Decorative 70s retro. May become an occasional motif, never a palette |
| Product green | `riddim-ting` | Color of a specific product. Candidate for an optional variant |
| Screen blue | `op1-field`, `vinyl-sinus` | Information color on a display. Reassess if the system needs a data color |
| Aqua and Heat Marker | palette pin | Good for illustration. Evaluate as a separate illustration palette |
| Gradients, reflections and shadows | TE product photos | They come from photography, not the graphic language |
| Dense anime-style illustration | `illus-workbench-mess`, `illus-space-eye` | Too much detail for the system. Mood reference, not form |
| Lime yellow and cyan in the treemap | `main-3` | Neon in the interface. The structure of `main-3` is in. The colors are not |
| Green and red for change (+0,94, ▲▼) | `main-2`, `main-3` | Semantic data color. Decide later whether the system will have status colors |
| Photography and colorful 3D scenes | board 05, 08, 12, 20, 23, 44, 46 | Mood. They do not define UI |

---

## 6. Typography

Teenage Engineering uses proprietary typography that cannot be replicated. The system declares **slots** and fills them with open fonts:

| Slot | Role | Desired trait |
|---|---|---|
| Text | Body, titles, information | Geometric grotesque, good at thin weight, tabular figures |
| Label / mono | Panel labels, numbers, code | Monospaced or narrow grotesque, legible in small uppercase |
| Display (optional) | Covers, giant numbers | Rounded (LUNA) or segmented (LCD). Titles only |

The interfaces confirm that **mono is a first-class slot**, not a detail: it carries numbers, labels, tables, navigation and, on editorial sites, even body text. The grotesque must work well thin and large (`main-1`) and in bold uppercase (`main-4`).

Candidates will be compared side by side in HTML before the decision.

**Decided (2026-10-25): Geist (text) and Geist Mono (instrument).** Approved by the author in the first version of the dashboard. Open, on Google Fonts.

---

## 7. Decisions

### Made

| Date | Decision | Origin |
|---|---|---|
| 2026-10-25 | Typography: Geist + Geist Mono | Approved in dashboard v0.1 |
| 2026-10-25 | Solid color canvas. **The construction grid is not used as an interface background**. It remains a resource for illustration and graphic pieces | Author's request in dashboard v0.1 |
| 2026-10-25 | v0.1 primitives created as tokens (provisional in values, final in structure): cool neutrals, orange `#f15033` + `#b8321a` for text, spacing 8/16/32/64, radius 4/10/full, 1px line | `src/tokens/`, `site/foundations.html` |
| 2026-10-25 | `neutral.400` (`#bdbdbd`) exists only for the data scale, never surface or text | Task age scale |
| 2026-10-25 | Canvas `neutral.100` changes from `#e6e6e6` to **`#eaeaea`** | Author's choice |
| 2026-10-25 | Signal becomes **`#f35919`** (previously `#f15033`). The text version becomes `#b5400c`, same hue | `orange-circles-grid` palette image, exact sampled flat color |
| 2026-10-25 | No `data-*` roles: charts use the neutral primitives directly. Semantic only when it adds meaning | Author's request: less complexity |
| 2026-10-25 | `neutral.500` (`#858585`) joins the scale: mid gray for icons, placeholders and non-text graphics (3.5:1 on the panel) | Author's request |
| 2026-10-25 | Button gets a glow on hover, in the variant color. An exception to the no-shadow rule, only as a response to interaction | Author's request |
| 2026-10-25 | Data scale becomes `neutral.200` (`#dddddd`) · `400` (`#a3a3a3`, previously `#bdbdbd`) · `600` · `900`: the two light tones were nearly identical (1.2:1). Now each step differs ≥1.8:1 from its neighbor | Author's request in the dashboard |
| 2026-10-25 | Labels become **chips** (pill, sentence case, no hover), so they are not confused with buttons. The rectangular "block label" stays only for graphic pieces | Author's request in the dashboard |
| 2026-10-25 | Table cells always vertically centered | Author's request |
| 2026-10-25 | Basic elements in `src/css/elements.css`, demonstrated in `site/elements.html` | First version |
| 2026-10-25 | Reference images removed from the repository. Pinterest links are the source of record | Keep the repository small (82 MB of images) |
| 2026-10-25 | Scopes: `src/shared/` (tokens, base, elements, one `shared.css` entry), `src/web/` (sites and docs) and `src/app/` (dashboards). Scope tokens reference shared ones. Prefixes `eis-web-`/`--web-` and `eis-app-`/`--app-`, checked by `scripts/check-css.py` | Several systems in one: same colours and spacing, no conflicts. Copy shared + one scope to start a project |

### Open

1. **Neutral temperature:** cool is in use (provisional). Warm raw (PO-80, Architectural Cream) remains an alternative. The system cannot mix the two. In the interfaces, 3 of the 4 main references are neutral gray and only `main-4` is cream.
2. **Accent:** decided `#f35919` (see Made).
3. **Dark background:** neutral black (`#111`) or greenish Iron Core (`#222A2A`)? Depends on decision 1.
4. **Illustration palette:** have a secondary palette only for illustration (aqua, amber) or illustrate only with the system palette?
5. **Display:** is a third typographic slot (rounded or LCD) needed for covers?
6. **Status color:** will the system have green and red for data change, or only the accent marking the exception?
7. **Color variant:** blue (`#1850A8`) as the only alternative variant to orange, swapping only the color?

## 8. History

- **2026-10-25:** first batch of 10 Teenage Engineering references and 15 from the retrofuturism moodboard.
- **2026-10-25:** interface board with 66 pins, 4 of them marked as main.
