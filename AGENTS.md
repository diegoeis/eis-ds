# eis-ds

A visual design system in plain HTML and CSS. It contains primitives (colour, type, space, shape) and basic elements. Uses: slides, websites, email, illustrations and images.

Version 0.1, draft. Only the light mode exists.

## Read before you change anything

1. `docs/manual/` — how to use tokens and elements. MUST read before you build a piece.
2. `docs/tokens.md` — the token format (W3C DTCG 2025.10). MUST read before you change a token.
3. `docs/visual-guidance/visual-guidance.md` — visual direction, references and the decision log. Read it before you propose a new value.
4. `site/` — the visual manual. Start at `site/foundations.html`.

## Structure

```
src/                     the design system. Copy shared/ + one scope into a project
  shared/                used by every scope
    shared.css           one entry point: imports the three files below
    tokens/              shared tokens (.tokens.json): source of truth
    css/tokens.css       GENERATED. Never edit by hand
    css/base.css         reset, body type, focus, text helpers
    css/elements.css     basic elements: button, chip, fields, table, panel…
  web/                   scope: websites, landing pages, docs
    tokens/  css/tokens.css (GENERATED)  css/web.css  js/lines.js
  app/                   scope: dashboards, tools
    tokens/  css/tokens.css (GENERATED)  css/app.css
index.html               landing page: what the system is, for whom, how to start
site/                    the visual manual for humans (web scope). foundations.html is the home
  foundations.html, elements.html, examples.html
  examples/<kind>/       pages built with the system
docs/
  manual/                written usage rules: tokens, elements, layout and scopes
  tokens.md              token format
  visual-guidance/       reference only: direction, images, decisions
scripts/build-tokens.py  validates the tokens of every scope and generates each tokens.css
scripts/check-css.py     checks that scopes never use each other's classes or variables
```

A project needs `src/shared/` and one scope. `site/` and `docs/` document the system and never hold tokens or CSS. Scope rules: `docs/manual/layout.md` §7.

## Workflow

1. Token: edit the `.tokens.json` file of `shared` or of one scope. Run `python3 scripts/build-tokens.py`. If it fails, do not use the result.
2. Element: change it in `src/shared/css/elements.css`. Scope component: change it in `src/<scope>/css/<scope>.css`. Then run `python3 scripts/check-css.py`. Show it on `elements.html`. Document it in `docs/manual/elements.md`.
3. New example: put it in `site/examples/<kind>/`. Add a card on `examples.html`.
4. New reference image: add it to the source table in `visual-guidance.md`.

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
- Temporary files start with `_`. Delete them after use.
