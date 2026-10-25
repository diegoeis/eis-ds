# Tokens: usage

Which variable to use for what. All variables come from `docs/manual/site/css/tokens.css` (generated — never edit it).

**Two layers.**
- **Semantic roles** (`--surface-*`, `--ink*`, `--line`, `--signal*`) carry meaning and will change between modes (dark, paper). For backgrounds, text, lines and the signal colour you **MUST** use the role, never the primitive behind it.
- **Primitives** (`--color-*`, `--space-*`, `--radius-*`, `--border-*`, `--font-*`): use them directly for everything that has no role: spacing, radii, type sizes and weights, and the grey ramp for data.

**No raw values.** You MUST NOT write a hex, rgb, px font size, px spacing or radius in piece CSS. If a value is missing, the token is missing: add it (see `docs/tokens.md`), don't hard-code it. [§7](#7-allowed-raw-values) lists the allowed exceptions.

---

## 1. Colour roles

| Variable | Value | Use for | MUST NOT |
|---|---|---|---|
| `--surface-canvas` | `#eaeaea` | Page background. Hover background of secondary/ghost controls. Background of an open disclosure summary. | Use as a card or panel background. |
| `--surface-panel` | `#f7f7f7` | Panels, sidebar, inputs, table backgrounds. The second and **last** surface level. | Stack a panel inside a panel to get a third level. Use a line instead. |
| `--surface-inverse` | `#111111` | Primary button, active nav item, solid chip. | Use for large areas. |
| `--line` | `#cfcfcf` | **Every** border, divider and hairline: panels, table rows, separators, chip outlines. | Use `--ink` or any darker grey for borders of shapes, panels or cards. |
| `--ink` | `#111111` | Primary text, headings, numbers, checked controls, focus outline. | — |
| `--ink-muted` | `#666666` | Secondary text, labels, metadata, placeholders, **outlines of interactive controls** (input, checkbox, radio, switch). 4.8:1 on canvas. | Use for decorative borders (that is `--line`). |
| `--ink-inverse` | `#f7f7f7` | Text on `--surface-inverse`. | Put on `--signal` (use `--signal-on`). |
| `--signal` | `#f35919` | **Fills and marks** for the one thing that matters: overdue, conflict, urgent, record. | Use as text on light surfaces (3.1:1, fails). Decorate. Exceed ~5% of the visible area. |
| `--signal-ink` | `#b5400c` | The signal **as text**: overdue dates, error messages, current breadcrumb item. 4.7:1 on canvas. | Use as a fill. |
| `--signal-on` | `#111111` | Text and icons placed **on** a `--signal` fill. 5.6:1. | Use white on `--signal` (3.1:1, fails). |

### Signal budget

- One signal per piece. If two things compete for it, one of them is not important.
- Signal covers ≤ 5% of the area. Exception: one "accent block" (a whole section in `--signal`) per page, declared on purpose.
- Normal data is grey. Signal marks only the exception.

### Pairing quick-reference

| Background | Text | Secondary text | Accent text |
|---|---|---|---|
| `--surface-canvas` | `--ink` | `--ink-muted` | `--signal-ink` |
| `--surface-panel` | `--ink` | `--ink-muted` | `--signal-ink` |
| `--surface-inverse` | `--ink-inverse` | — | — |
| `--signal` | `--signal-on` | — | — |

Any other pair MUST be measured (WCAG 2.1: 4.5:1 text, 3:1 large text and UI graphics) before use.

## 2. Neutral primitives

Use the role above whenever one exists. Use these primitives directly **only** for data visualisation and the cases listed.

| Variable | Value | Direct use allowed for |
|---|---|---|
| `--color-neutral-0` | `#f7f7f7` | — (use `--surface-panel` / `--ink-inverse`) |
| `--color-neutral-100` | `#eaeaea` | — (use `--surface-canvas`) |
| `--color-neutral-200` | `#dddddd` | Data ramp, lowest step. |
| `--color-neutral-300` | `#cfcfcf` | Data ramp. (As a border, use `--line`.) |
| `--color-neutral-400` | `#a3a3a3` | Data ramp. |
| `--color-neutral-500` | `#858585` | Data ramp. Icons and non-text graphics (3.4:1 on panel). Never body text. |
| `--color-neutral-600` | `#666666` | Data ramp. (As text, use `--ink-muted`.) |
| `--color-neutral-900` | `#111111` | Data ramp, highest step. (As text, use `--ink`.) |

### Data ramp

Ordinal data (age, volume, intensity) goes from light to dark, low to high:

`--color-neutral-200` → `300` → `400` → `500` → `600` → `900`, and `--signal` for the exception (overdue, anomaly).

- Use as many steps as there are buckets, keeping the order. With fewer than 6 buckets, prefer skipping steps so neighbours differ more (e.g. 4 buckets: `200 · 400 · 600 · 900`).
- `200` and `300` are close (1.15:1). Don't put them next to each other when the difference matters.
- No hues for data. Status colours (green/red) do not exist in the system yet.

## 3. Space

Four steps, each double the previous. Each has a job. Pick by job, not by eye.

| Variable | Value | Job |
|---|---|---|
| `--space-100` | 8px | **Inside a component**: icon ↔ label, gap between chips, label ↔ field, field ↔ hint. |
| `--space-200` | 16px | **Between siblings**: panel padding, table cell padding, list rows, gap between panels in a grid. |
| `--space-300` | 32px | **Between blocks**: page padding (desktop), gap between page regions, title ↔ content of a section. |
| `--space-400` | 64px | **Between sections**: large section gaps on documentation and marketing pages. |

- Use the half step `calc(--space-100 / 2)` (4px) only in dense data: cell grids, segmented control padding, list item gaps.
- Mobile page padding drops one step (`--space-300` → `--space-200`).

## 4. Radius and line

| Variable | Value | Use for |
|---|---|---|
| `--radius-100` | 4px | Buttons, inputs, selects, nav items, small boxes. |
| `--radius-200` | 10px | Panels. |
| `--radius-full` | 999px | Chips, segmented control, switch, avatar, pills. |
| `--border-width-100` | 1px | **The only line weight.** Every border and divider. |

- Only the focus outline uses 2px.
- No shadows. The only exception is the button hover glow (defined in `elements.css`), never at rest.

## 5. Type

Two voices. **Sans** (`--font-family-sans`, Geist) speaks text. **Mono** (`--font-family-mono`, Geist Mono) speaks for the instrument: labels, numbers, dates, codes, sources, navigation, buttons.

### Text styles — prefer these

Apply with the class (`.eis-type-*`) or the per-property variables (`--type-<style>-font-size`, `-font-family`, `-font-weight`, `-letter-spacing`, `-line-height`).

| Style | Spec | Use for |
|---|---|---|
| `display` | sans 56 / 300 / −1.5 / 1 | Page title (`h1`). One per page. Use `clamp(--font-size-600, 5vw, --font-size-800)` for responsiveness. |
| `heading` | sans 24 / 400 / 1.25 | Section titles in documents and pages. |
| `lead` | sans 18 / 400 / 1.45 | Intro paragraph under a title. |
| `body` | sans 14 / 400 / 1.45 | Body text, UI text, task text, table text. The default on `<body>`. |
| `metric` | mono 48 / 300 / −1.5 / 1 | Big numbers in panels and summaries. `--font-size-600` on mobile. |
| `mono` | mono 12 / 400 | Dates, times, sources, metadata, counts, codes. Also `.eis-mono`. |
| `label` | mono 11 / 500 / +0.88 / UPPERCASE | Panel titles, table headers, field labels, nav section titles. Also `.eis-label`. |

Rules:
- Numbers that line up (tables, metrics, counts) MUST be mono with `font-variant-numeric: tabular-nums` (`.eis-mono` and `.eis-num` already do it).
- UPPERCASE is only for `label` style and buttons. Running text MUST be sentence case.
- Weights: 300 for display/metric, 400 for text, 500 for labels and emphasis, 600 only for the brand mark. No bold (700).
- Don't invent sizes. Use `--font-size-100…800`.

## 6. Mode

Only the light mode exists. Pieces MUST still use roles for surfaces/ink/line/signal so a dark mode can be added by redefining roles only.

## 7. Allowed raw values

The only places a literal number is acceptable in piece CSS:
- Component dimensions: control heights (40px, 24px chips), icon and avatar sizes, checkbox 16px, fixed sidebar width, column widths in a table.
- `calc(--space-100 / 2)` in dense data.
- `0`, `100%`, `1fr`, `auto`, percentages and viewport/container units in layout.
- Breakpoints in `@media`.
- Opacity `.4` for disabled.
