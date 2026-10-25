# Layout

How to set up a page or piece built with the system.

## 1. Files to load

A piece is a standalone HTML file. It loads, in this order:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600&family=Geist+Mono:ital,wght@0,300;0,400;0,500;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="<path>/css/tokens.css">
<link rel="stylesheet" href="<path>/css/elements.css">
<style>/* this piece's layout only */</style>
```

- `<path>` is the path to `site/`. From `site/examples/<kind>/` it is `../..` (so `../../css/tokens.css`).
- `elements.css` already sets the base (box-sizing, margins, body type, canvas background, focus). Don't repeat it.
- `site/css/docs.css` is for the system's own documentation pages only. Pieces MUST NOT load it.
- The piece's `<style>` contains **layout only**: grids, regions, positions, page-specific arrangements. It MUST NOT redefine buttons, chips, fields, tables, panels or any element of `elements.css`.
- No frameworks or libraries (React, Tailwind, Bootstrap, icon fonts).

## 2. Page skeleton

```html
<!doctype html>
<html lang="en">
<head>…files above…</head>
<body>
  <aside class="eis-sidebar" aria-label="Sidebar">
    <nav aria-label="Main">…</nav>
  </aside>
  <main>
    <header>
      <nav class="eis-breadcrumb eis-label" aria-label="Breadcrumb">…</nav>
      <h1>Page title</h1>
    </header>
    <section class="eis-panel" aria-labelledby="…">…</section>
  </main>
</body>
</html>
```

Element roles:

| Region | Element |
|---|---|
| Sidebar / side navigation | `<aside aria-label="…">` — also when it becomes a top bar on mobile |
| Navigation lists | `<nav aria-label="…">` + `<ul>` |
| Page or section heading area | `<header>` (never for the sidebar) |
| Main content | `<main>`, one per page |
| Content blocks | `<section aria-labelledby>` (has a heading) or `<article>` (stands alone) |
| Footer of page, panel or sidebar | `<footer>` |
| Dates and times | `<time datetime="…">` |

- Headings in order, one `<h1>` per page. Panel titles are `h2`/`h3` with the `eis-label` class — the visual size doesn't decide the level.
- Interface text and file names in **English**. Example content is **fictional**: invented first names, invented codes like `PLT-204`. Never use real people, clients or data.

## 3. Spacing the page

| Where | Space |
|---|---|
| Page padding | `--space-300` desktop, `--space-200` below 1024px |
| Gap between page regions (header, metric row, panel grid) | `--space-300` |
| Gap between panels in a grid | `--space-200` |
| Panel padding, row padding | `--space-200` |
| Inside components | `--space-100` |

Surfaces: page on `--surface-canvas`, content in `--surface-panel` panels. Nothing else. No background grid, no gradients, no shadows.

## 4. Grids and responsiveness

Every piece MUST work from 360px to wide screens with **no horizontal scroll**, no clipped text and no overlap.

- Fluid first: `grid`, `flex`, `minmax`, `clamp()`. Breakpoints only where the composition breaks.
- Auto grids MUST use `minmax(min(<px>, 100%), 1fr)`:
  ```css
  grid-template-columns: repeat(auto-fit, minmax(min(250px, 100%), 1fr));
  ```
  A bare `minmax(250px, 1fr)` overflows when the container is narrower than 250px.
- Grid and flex children that contain text: `min-width: 0` (or `minmax(0, 1fr)` columns) so long text wraps instead of pushing the layout.
- Display titles: `font-size: clamp(--font-size-600, 5vw, --font-size-800)`.
- Typical breakpoints so far:
  - 1280px: the side column drops below.
  - 1024px: the sidebar becomes a top bar.
  - 760px: tables reflow, metrics go 2 × 2.
  - 420px: toolbar buttons stretch.
- A horizontal nav that can't fit scrolls **inside itself** (`overflow-x: auto` on the nav), never the page.
- Tables: reflow to cards with CSS, or scroll inside a wrapper.

## 5. Slides and fixed-ratio pieces

- Each slide is a container. Set `container-type: inline-size` and `aspect-ratio: 16/9`.
- Size everything inside in container units (`cqw`), so the slide scales as one object.
- Use the same tokens for colour, line and type families. Sizes in `cqw` are the allowed exception to px tokens.

## 6. Data visualisation

- Data as a matrix of equal cells (like device keys) or thin bars. No pie charts, no 3D, no gradients.
- Grey ramp for normal values, `--signal` only for the exception (see `tokens-usage.md` §2).
- Every chart has `role="img"` and an `aria-label` that states the numbers.
- Legends are lists (`<ul>`), `aria-hidden` if the `aria-label` already carries the data.
