# eis-ds manual

The usage manual of the design system. Written to be applied literally by people and by LLMs: every rule is a "use / don't use", every element has HTML to copy.

Read these files in this order before you build anything:

| File | Answers |
|---|---|
| [`tokens-usage.md`](tokens-usage.md) | Which variable do I use for this colour, size, space, radius or line? |
| [`elements.md`](elements.md) | What HTML and classes make a button, chip, field, table, panel…? Which variant? |
| [`layout.md`](layout.md) | How do I set up a page: files to load, page skeleton, grids, responsiveness? |
| [`checklist.md`](checklist.md) | What must be true before a piece is done? |

Related, not part of the manual:

- `docs/tokens.md` — how tokens are **written** (W3C DTCG format). Read it only when adding or changing a token.
- `docs/visual-guidance/visual-guidance.md` — where the visual direction came from, and the decision log. Read it to understand *why*. This manual says *what*.
- `site/foundations.html`, `site/elements.html`, `site/examples.html` — this manual applied and rendered. `site/` also holds the tokens and the CSS. When the manual and the CSS disagree, the CSS in `docs/manual/site/css/` wins. Then fix the manual.

## Conventions used in this manual

- **MUST / MUST NOT** — no exceptions.
- **Prefer** — the default. Deviate only for a reason you can state.
- Code blocks are copy-ready. Replace only the text and the `id`/`for` values.
- This manual writes variable names without `var()`: `--ink` means `var(--ink)`.
