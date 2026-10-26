# Layout

How to set up a page or piece built with the system.

## 1. Files to load

A piece is a standalone HTML file. It links one stylesheet:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="<src>/<scope>/<scope>.css">
<style>/* this piece's layout only */</style>
```

- `<src>` is the relative path to the `src/` folder at the repository root. From `site/examples/<kind>/` it is `../../../src`.
- `<scope>` is `web` (websites, landing pages, docs) or `app` (dashboards, tools). See §7.
- `<scope>.css` is the only stylesheet to link. It imports `../shared/shared.css` (fonts, shared tokens, base, elements), then the scope tokens and components. Keep `shared/` next to the scope folder. The preconnect lines are optional: they make the fonts load faster.
- `shared.css` imports the fonts, the shared tokens, the base and the elements. The base already sets box-sizing, margins, body type, canvas background and focus. Don't repeat it.
- The piece's `<style>` contains **layout only**: grids, regions, positions, page-specific arrangements. It MUST NOT redefine buttons, chips, fields, tables, panels or any shared element.
- No frameworks or libraries (React, Tailwind, Bootstrap, icon fonts).

## 2. Page skeleton

```html
<!doctype html>
<html lang="en">
<head>…files above…</head>
<body class="eis-app-shell">
  <aside class="eis-app-sidebar" aria-label="Sidebar">
    <nav class="eis-app-nav" aria-label="Main">…</nav>
  </aside>
  <main class="eis-app-main">
    <header>
      <nav class="eis-breadcrumb eis-label" aria-label="Breadcrumb">…</nav>
      <h1>Page title</h1>
    </header>
    <section class="eis-panel" aria-labelledby="…">…</section>
  </main>
</body>
</html>
```

A web page (website, landing, docs) uses the web scope instead:

```html
<body>
  <div class="eis-web-sheet">
    <header class="eis-web-wrap eis-web-grid eis-web-header">…</header>
    <main>
      <section class="eis-web-hero" aria-labelledby="hero-h">…</section>
      <section class="eis-web-section" aria-labelledby="…">…</section>
    </main>
    <footer class="eis-web-wrap eis-web-grid eis-web-footer">…</footer>
  </div>
</body>
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
- Grey ramp for normal values, `--accent` only for the exception (see `tokens-usage.md` §2).
- Every chart has `role="img"` and an `aria-label` that states the numbers.
- Legends are lists (`<ul>`), `aria-hidden` if the `aria-label` already carries the data.

## 7. Scopes: shared, web and app

eis-ds is several design systems in one. They share the same base and never conflict.

| Folder | Use for | Load | Class prefix | Variable prefix |
|---|---|---|---|---|
| `src/shared/` | Every scope | Imported by each scope entry | `eis-` | `--color-`, `--space-`, `--ink`… |
| `src/web/` | Websites, landing pages, marketing pages, documentation | `web/web.css`, optional `web/js/lines.js` | `eis-web-` | `--web-` |
| `src/app/` | Dashboards, tools, system screens | `app/app.css` | `eis-app-` | `--app-` |

To build a website, copy `src/shared/` and `src/web/`. To build a dashboard, copy `src/shared/` and `src/app/`. More scopes (slides, email, docs) follow the same pattern.

Rules:
- `shared` never depends on a scope. Shared elements (button, chip, fields, table, panel) and, later, icons live there.
- A scope's tokens live under its own group (`web.*`, `app.*`) and MAY reference shared tokens: `"{font.size.800}"`. A colour change in shared reaches every scope.
- A scope MUST NOT reference another scope's tokens, variables or classes.
- Every selector in `<scope>/css/components.css` starts with `.eis-<scope>-`. A scope never styles bare HTML or shared classes on their own. It MAY place a shared element in its own context (`.eis-app-tasks .eis-table`) for layout only.
- `scripts/build-tokens.py` validates the token rules. `scripts/check-css.py` validates the CSS rules. Both MUST pass.
- A pattern used on two or more pages goes into the scope CSS. A pattern used on one page only stays in that page's `<style>`.

### Web components

| Class | What it is |
|---|---|
| `eis-web-docnav` | Top bar of documentation pages |
| `eis-web-page`, `eis-web-intro`, `eis-web-toc` | Documentation page shell, intro with title and facts, table of contents |
| `eis-web-doc` | Documentation section: title column + content column |
| `eis-web-spec`, `eis-web-pair`, `eis-web-scroll` | Specification table, contrast pair sample, horizontal scroll wrapper |
| `eis-web-docfoot` | Footer of documentation pages |
| `eis-web-sheet`, `eis-web-wrap`, `eis-web-grid` | Landing sheet on the canvas (always 32px from the window edge, 24px up to 760px), side padding, 12-column grid |
| `eis-web-header`, `eis-web-brand` | Landing top bar and brand mark |
| `eis-web-hero` (`__index`, `__meta`, `__lead`, `__sub`, `__actions`) | Hero block |
| `eis-web-lines` + `data-eis-web-lines` | Line art drawn by `web/js/lines.js`. Options: `data-seed`, `data-step` |
| `eis-web-section` (`__head`, `__body`, `__aside`) | Landing section: numbered label, title, body column |
| `eis-web-numbered`, `eis-web-cards`/`eis-web-card`, `eis-web-principles`, `eis-web-steps` | Numbered list, cards with a figure, principles grid, step timeline |
| `eis-web-code`, `eis-web-cta`, `eis-web-footer`, `eis-web-arrow` | Code block, closing call to action, landing footer, arrow link |

### App components

| Class | What it is |
|---|---|
| `eis-app-shell` | On `<body>`: sidebar + main grid. Becomes a top bar below 1024px |
| `eis-app-sidebar`, `eis-app-brand`, `eis-app-nav` (`__section`, `__count`) | Sidebar, brand, navigation with counts |
| `eis-app-main`, `eis-app-page-head`, `eis-app-toolbar` | Main region, page title row, action toolbar |
| `eis-app-metrics` | Row of metric cells (`<dl>`) |
| `eis-app-grid` (`--halves`, `--main`), `eis-app-stack` | Panel grids and the side column stack |
| `eis-app-agenda`, `eis-app-cells`, `eis-app-legend`, `eis-app-bar`, `eis-app-pips` | Agenda list, cell matrix, legend, stacked bar, pips |
| `eis-app-tasks`, `eis-app-meta`, `eis-app-due` | Task groups with tables, task metadata, due dates |
| `eis-app-topics`, `eis-app-people`, `eis-app-done` | Side lists |

### Add a scope

1. Create `src/<scope>/tokens/<scope>.tokens.json`. Put every token under the group `<scope>`. Reference shared tokens where a value already exists.
2. Create `src/<scope>/tokens/<scope>.resolver.json`. Copy `src/web/tokens/web.resolver.json` and change the names.
3. Run `python3 scripts/build-tokens.py`. It finds the new scope and writes `src/<scope>/css/tokens.css`.
4. Create `src/<scope>/css/components.css`. Every selector starts with `.eis-<scope>-`. Then create the entry `src/<scope>/<scope>.css`: copy `src/web/web.css` and change the names.
5. Run `python3 scripts/check-css.py`.
6. Add the scope to the table at the top of this section, to `README.md` and to `AGENTS.md`. Add its tokens to `tokens-usage.md` §7.
7. Add an example in `site/examples/<kind>/` and a card on `examples.html`.
