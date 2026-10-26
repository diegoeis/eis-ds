# eis-ds

A visual design system in plain HTML and CSS. Minimal retrofuturism: cool neutrals, thin lines, a mono voice for data and one orange accent.

It is several design systems in one. They share the same base and never conflict:

| Folder | For | Link |
|---|---|---|
| `src/shared/` | Every project: fonts, tokens, base, elements | Imported by each scope |
| `src/web/` | Websites, landing pages, documentation | `web/web.css`, optional `web/js/lines.js` |
| `src/app/` | Dashboards, tools, system screens | `app/app.css` |

More scopes (slides, email) will follow the same pattern.

Version 0.1, draft. Light mode only.

Site: https://diegoeis.github.io/eis-ds/

[![Example dashboard built with eis-ds (app scope): sidebar, four metrics, agenda, task age matrix and task tables](site/examples/dashboard/tasks-work.png)](https://diegoeis.github.io/eis-ds/site/examples/dashboard/tasks-work.html)

*Example dashboard (app scope), with fictional data. [Open it live](https://diegoeis.github.io/eis-ds/site/examples/dashboard/tasks-work.html).*

## Use it

No package and no build step.

1. Copy `src/shared/` and one scope (`src/web/` or `src/app/`) into your project.
2. Link one file. It imports the fonts, shared and the scope:

```html
<link rel="stylesheet" href="eis-ds/app/app.css">
```

Keep `shared/` next to the scope folder: the scope file imports `../shared/shared.css`.

Or link it from the published site, with no copy:

```html
<link rel="stylesheet" href="https://diegoeis.github.io/eis-ds/src/app/app.css">
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
