# eis-ds

A visual design system in plain HTML and CSS. It contains primitives (colour, type, space, shape) and basic elements. Uses: slides, websites, email, illustrations and images.

Version 0.1, draft. Only the light mode exists.

## Read before you change anything
1. `README.md` — what the system is and how a project uses it.
2. `docs/manual/` — how to use tokens and elements. MUST read before you build a piece.
3. `docs/tokens.md` — the token format (W3C DTCG 2025.10). MUST read before you change a token.
4. `docs/visual-guidance/visual-guidance.md` — visual direction, references and the decision log. Read it before you propose a new value.
5. `site/` — the visual manual. Start at `site/foundations.html`.

## Structure

```
src/                     the design system. Copy shared/ + one scope into a project
  shared/                used by every scope
    shared.css           entry: imports the fonts and the three files below
    tokens/              shared tokens (.tokens.json): source of truth
    css/tokens.css       GENERATED. Never edit by hand
    css/base.css         reset, body type, focus, text helpers
    css/elements.css     basic elements: button, chip, fields, table, panel…
  web/                   scope: websites, landing pages, docs
    web.css              entry a page links: imports shared, tokens, components
    tokens/  css/tokens.css (GENERATED)  css/components.css  js/lines.js
  app/                   scope: dashboards, tools
    app.css              entry a page links: imports shared, tokens, components
    tokens/  css/tokens.css (GENERATED)  css/components.css
index.html               landing page: what the system is, for whom, how to start
site/                    the visual manual for humans (web scope). foundations.html is the home
  foundations.html, elements.html, examples.html
  examples/<kind>/       pages built with the system
docs/
  manual/                written usage rules: tokens, elements, layout and scopes
  tokens.md              token format
  visual-guidance/       reference only: direction, Pinterest links, decisions
scripts/build-tokens.py  validates the tokens of every scope and generates each tokens.css
scripts/check-css.py     checks that scopes never use each other's classes or variables
```

A project needs `src/shared/` and one scope. `site/` and `docs/` document the system and never hold tokens or CSS. Scope rules: `docs/manual/layout.md` §7.

## Workflow

1. Token: edit the `.tokens.json` file of `shared` or of one scope. Run `python3 scripts/build-tokens.py`. If it fails, do not use the result.
2. Element: change it in `src/shared/css/elements.css`, show it on `elements.html` and document it in `docs/manual/elements.md`. Scope component: change it in `src/<scope>/css/components.css` and list it in `docs/manual/layout.md` §7. Then run `python3 scripts/check-css.py`.
3. New example: put it in `site/examples/<kind>/`. Add a card on `examples.html` with a 1440×900 PNG screenshot next to the page (`<name>.png`), never a live iframe.
4. New scope (slides, email…): follow `docs/manual/layout.md` §7, "Add a scope".
5. New reference: pin it on Pinterest and add the link to the source table in `visual-guidance.md`. Do not commit image files.

## Rules

- Interface text, file names and documentation are in English.
- Write documentation in STE-flavored English (ASD-STE100): short sentences, active voice, no semicolons, no phrasal verbs.
- Every piece is responsive from 360px to wide screens, with no horizontal scroll.
- Use semantic HTML and native controls that work. Never fake a table or a control with `div` or `span`.
- Every class starts with `eis-`. Scope classes start with `eis-<scope>-` and live only in that scope. Scopes never use each other.
- No raw values in CSS. All values come from the tokens.
- A piece does not restyle a basic element. If it needs a change, change the element in the system.
- A variant changes colour only.
- Examples use fictional data only.
- No frameworks (React, Tailwind and similar).
- Show a visual decision in HTML before it becomes a token.
- Measure contrast. Never estimate it.
- Every HTML page published on GitHub Pages has the Google Tag Manager snippet (`GTM-KWLTJ7HD`): the script first in `<head>`, the `noscript` first in `<body>`. Copy it from `index.html`.
- Temporary files start with `_`. Delete them after use.
