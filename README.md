# eis-ds

A visual design system in plain HTML and CSS. Minimal retrofuturism: cool neutrals, thin lines, a mono voice for data and one orange signal.

It is several design systems in one. They share the same base and never conflict:

| Folder | For | Load |
|---|---|---|
| `src/shared/` | Every project | `shared/shared.css` (tokens, base, elements) |
| `src/web/` | Websites, landing pages, documentation | `web/css/tokens.css`, `web/css/web.css`, optional `web/js/lines.js` |
| `src/app/` | Dashboards, tools, system screens | `app/css/tokens.css`, `app/css/app.css` |

More scopes (slides, email) will follow the same pattern.

Version 0.1, draft. Light mode only.

## Use it

No package and no build step.

1. Copy `src/shared/` and one scope (`src/web/` or `src/app/`) into your project.
2. Load the fonts, then the CSS:

```html
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600&family=Geist+Mono:ital,wght@0,300;0,400;0,500;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="eis-ds/shared/shared.css">
<link rel="stylesheet" href="eis-ds/app/css/tokens.css">
<link rel="stylesheet" href="eis-ds/app/css/app.css">
```

3. Build with native HTML: shared classes (`eis-button`, `eis-chip`, `eis-panel`…) and the classes of your scope (`eis-app-*` or `eis-web-*`). Your own CSS holds layout only.
4. Check the piece against `docs/manual/checklist.md`.

## Documentation

- `index.html` — landing page.
- `site/foundations.html`, `site/elements.html`, `site/examples.html` — the visual manual: tokens, elements and examples, running live.
- `docs/manual/` — the written rules: which token, which element, page layout, scopes, checklist. Written to be applied literally by people and LLMs.
- `docs/tokens.md` — the token format (W3C Design Tokens Format Module 2025.10).
- `docs/visual-guidance/visual-guidance.md` — visual direction, Pinterest references and the decision log.

## Change it

Tokens are the source of truth, in `src/<scope>/tokens/*.tokens.json`. Never edit a generated `tokens.css`.

```sh
python3 scripts/build-tokens.py   # validate the tokens of every scope and write each tokens.css
python3 scripts/check-css.py      # check that scopes never use each other's classes or variables
```

Both scripts use the Python standard library only. Contributor and agent rules are in `AGENTS.md`.
