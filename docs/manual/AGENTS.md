# eis-ds manual

The usage manual of the design system. Written to be applied literally by people and by LLMs: every rule is a "use / don't use", every element has HTML to copy.

Read these files in this order before you build anything:

| File | Answers |
|---|---|
| [`tokens-usage.md`](tokens-usage.md) | Which variable do I use for this colour, size, space, radius or line? |
| [`elements.md`](elements.md) | What HTML and classes make a button, chip, field, table, panel…? Which variant? |
| [`layout.md`](layout.md) | How do I set up a page: files to load, page skeleton, grids, responsiveness, scopes (shared, web, app)? |
| [`checklist.md`](checklist.md) | What must be true before a piece is done? |

Related, not part of the manual:

- `docs/tokens.md` — how tokens are **written** (W3C DTCG format). Read it only when adding or changing a token.
- `docs/visual-guidance/visual-guidance.md` — where the visual direction came from, and the decision log. Read it to understand *why*. This manual says *what*.
- `site/` (at the repository root) — the visual manual for humans: this manual applied and rendered. Start at `site/foundations.html`. The tokens and the CSS live in `src/`: `shared/`, `web/` and `app/` (see `layout.md` §7). When the manual and the CSS disagree, the CSS in `src/css/` wins. Then fix the manual.

For LLMs outside this repository, the site publishes the manual as one file: https://diegoeis.github.io/eis-ds/llms-full.txt. `scripts/build-llms.py` generates it from this folder and `llms.txt`. A new file in this folder needs a link in `llms.txt`. The script also copies the section "Rules with no exceptions" below into `llms.txt`. Change the rules here, never in `llms.txt`.

## Rules with no exceptions

The other files of this manual give the details of each rule.

- Use only the shared classes and the classes of your scope (`eis-web-*` or `eis-app-*`). Never mix scopes.
- Your own CSS holds layout only. Do not restyle an eis-ds element. Do not write CSS that eis-ds already covers.
- Use no raw values for colour, type, space or radius. Use the tokens. The manual lists the few allowed exceptions.
- Use semantic HTML and native controls: `table`, `button`, `a`, `input`, `select`, `details`, `fieldset`. Never make a control or a table from `div` or `span`.
- A variant changes colour only. A size (`--sm`, `--lg`) changes size only.
- Use the accent once per piece, on 5% of the area or less.
- Every piece works from 360px to wide screens, with no horizontal scroll.
- Before you finish, check the piece against the checklist.

## Conventions used in this manual

- **MUST / MUST NOT** — no exceptions.
- **Prefer** — the default. Deviate only for a reason you can state.
- Code blocks are copy-ready. Replace only the text and the `id`/`for` values.
- This manual writes variable names without `var()`: `--ink` means `var(--ink)`.
