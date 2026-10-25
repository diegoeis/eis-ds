# eis-ds

A visual design system in plain HTML and CSS. It contains primitives (colour, type, space, shape) and basic elements. Uses: slides, websites, email, illustrations and images.

Version 0.1, draft. Only the light mode exists.

## Read before you change anything

1. `docs/manual/` — how to use tokens and elements. MUST read before you build a piece.
2. `docs/tokens.md` — the token format (W3C DTCG 2025.10). MUST read before you change a token.
3. `docs/visual-guidance/visual-guidance.md` — visual direction, references and the decision log. Read it before you propose a new value.
4. `docs/manual/site/foundations.html`, `elements.html`, `examples.html` — the manual rendered as pages.

## Structure

```
scripts/build-tokens.py  validates the tokens and generates tokens.css
docs/
  manual/                usage rules for tokens, elements and layout
    site/                the manual applied: pages, tokens, CSS and examples
      tokens/            source of truth (.tokens.json)
      css/tokens.css     GENERATED. Never edit by hand
      css/elements.css   base and basic elements
      css/docs.css       layout of the manual pages only
      examples/<kind>/   pages built with the tokens and elements
  tokens.md              token format
  visual-guidance/       reference only: direction, images, decisions
```

There is no production design system yet. Everything here is documentation: the rules (`docs/manual/*.md`) and their applied, rendered form (`docs/manual/site/`).

## Workflow

1. Token: edit the `.tokens.json` file. Run `python3 scripts/build-tokens.py`. If it fails, do not use the result.
2. Element: change it in `elements.css`. Show it on `elements.html`. Document it in `docs/manual/elements.md`.
3. New example: put it in `docs/manual/site/examples/<kind>/`. Add a card on `examples.html`.
4. New reference image: add it to the source table in `visual-guidance.md`.

## Rules

- Interface text, file names and documentation are in English.
- Write documentation in STE-flavored English (ASD-STE100): short sentences, active voice, no semicolons, no phrasal verbs.
- Every piece is responsive from 360px to wide screens, with no horizontal scroll.
- Use semantic HTML and native controls that work. Never fake a table or a control with `div` or `span`.
- Every class starts with `eis-`.
- No raw values in CSS. All values come from the tokens.
- A piece does not restyle a basic element. If it needs a change, change the element in the system.
- A variant changes colour only.
- Examples use fictional data only.
- No frameworks (React, Tailwind and similar).
- Show a visual decision in HTML before it becomes a token.
- Measure contrast. Never estimate it.
- Temporary files start with `_`. Delete them after use.
