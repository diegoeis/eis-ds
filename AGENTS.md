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
src/                     the design system assets. Apps and the site load these
  tokens/                source of truth (.tokens.json)
  css/tokens.css         GENERATED. Never edit by hand
  css/elements.css       base and basic elements
  css/site.css           site layer: landing, marketing and docs pages. Apps never load it
index.html               landing page: what the system is, for whom, how to start
site/                    the visual manual for humans. Loads ../src/css/
  foundations.html       home of the manual
  elements.html, examples.html
  examples/<kind>/       pages built with the tokens and elements
docs/
  manual/                written usage rules for tokens, elements and layout
  tokens.md              token format
  visual-guidance/       reference only: direction, images, decisions
scripts/build-tokens.py  validates src/tokens and generates src/css/tokens.css
scripts/check-css.py     checks that site.css only has .eis-site- selectors
```

`src/` is the only thing an application needs. `site/` and `docs/` document it and never hold tokens or element CSS.

## Workflow

1. Token: edit the `.tokens.json` file. Run `python3 scripts/build-tokens.py`. If it fails, do not use the result.
2. Element: change it in `elements.css`. Site component (landing, docs): change it in `site.css`, then run `python3 scripts/check-css.py`. Show it on `elements.html`. Document it in `docs/manual/elements.md`.
3. New example: put it in `site/examples/<kind>/`. Add a card on `examples.html`.
4. New reference image: add it to the source table in `visual-guidance.md`.

## Rules

- Interface text, file names and documentation are in English.
- Write documentation in STE-flavored English (ASD-STE100): short sentences, active voice, no semicolons, no phrasal verbs.
- Every piece is responsive from 360px to wide screens, with no horizontal scroll.
- Use semantic HTML and native controls that work. Never fake a table or a control with `div` or `span`.
- Every class starts with `eis-`. Site-layer classes start with `eis-site-` and live only in `site.css`.
- No raw values in CSS. All values come from the tokens.
- A piece does not restyle a basic element. If it needs a change, change the element in the system.
- A variant changes colour only.
- Examples use fictional data only.
- No frameworks (React, Tailwind and similar).
- Show a visual decision in HTML before it becomes a token.
- Measure contrast. Never estimate it.
- Temporary files start with `_`. Delete them after use.
