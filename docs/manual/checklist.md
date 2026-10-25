# Checklist

Run this before calling a piece, element or token done. Every box must be true.

## Files and CSS

- [ ] Links one scope entry (`web/web.css` or `app/app.css`), then only its own layout CSS. No separate font link.
- [ ] Uses only shared classes and the classes of its own scope.
- [ ] Scope CSS changed? `python3 scripts/check-css.py` passes.
- [ ] No raw colours, font sizes, spacing or radii (only the exceptions in `tokens-usage.md` §8).
- [ ] Backgrounds, text, lines and signal use roles (`--surface-*`, `--ink*`, `--line`, `--signal*`), not primitives.
- [ ] Does not restyle any element from `elements.css`.
- [ ] Every class starts with `eis-`.
- [ ] Variants change colour only.
- [ ] No shadows (except the built-in button hover glow), no gradients, no glow, no background grid.

## HTML

- [ ] Semantic regions: `aside` for the sidebar, `main`, `header`, `nav`, `section`, `footer`.
- [ ] One `h1`. Headings in order.
- [ ] Tabular data in `<table>` with `thead`, `tbody`, `th scope`, `caption`.
- [ ] Controls are native: `button`, `a`, `input` (checkbox / radio / switch), `select`, `textarea`, `details`, `form`, `fieldset` + `legend`. No `div`/`span` pretending.
- [ ] Every control has a label. Invalid fields have `aria-invalid` + `aria-describedby`.
- [ ] Visual-only elements are `aria-hidden`. Charts have `role="img"` + a data `aria-label`.
- [ ] Dates and times in `<time datetime>`.
- [ ] Interface text is in English. Example data is fictional.

## Visual rules

- [ ] Signal used once per piece, ≤ 5% of the area (or one declared accent block).
- [ ] Statuses are chips. Actions are buttons. One primary button per view.
- [ ] Every border and divider is `--line`, 1px.
- [ ] Numbers are mono and tabular. Labels use the label style. Running text is in sentence case.
- [ ] Two surface levels only: canvas and panel. No panel inside a panel.

## Contrast

- [ ] You measured every text/background pair that is not in the pairing table (`tokens-usage.md` §1): ≥ 4.5:1 text, ≥ 3:1 large text and UI graphics.
- [ ] No white or `--ink-inverse` on `--signal`. No `--signal` as text.

## Responsive

- [ ] Rendered and looked at in **375px, 768px and 1440px**.
- [ ] You dragged the window between them. `scrollWidth ≤ clientWidth` at every width from ~280px up.
- [ ] Auto grids use `minmax(min(<px>, 100%), 1fr)`.
- [ ] Nothing is clipped or overlaps. Tables reflow or scroll inside a wrapper.

## Keyboard

- [ ] Every interactive element reachable with Tab, in a sensible order.
- [ ] Focus visible on all of them.

## When adding to the system

- [ ] New token: in `src/shared/tokens/` (shared) or `src/<scope>/tokens/` (one scope), `python3 scripts/build-tokens.py` passes, shown on `foundations.html`, usage added to `tokens-usage.md`.
- [ ] New or changed element: in `src/shared/css/elements.css`, shown on `elements.html`, documented in `elements.md`.
- [ ] New or changed scope component: in `src/<scope>/css/components.css`, listed in `layout.md` §7, `check-css.py` passes.
- [ ] New scope: steps in `layout.md` §7, "Add a scope".
- [ ] New page in this repository: Google Tag Manager snippet first in `<head>` and first in `<body>` (copy from `index.html`).
- [ ] New example: in `site/examples/<kind>/`, card on `examples.html`.
- [ ] Decision recorded in `docs/visual-guidance/visual-guidance.md` §7.
