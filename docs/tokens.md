# Tokens — format and conventions

eis-ds tokens follow the **Design Tokens Format Module 2025.10** from the W3C Design Tokens Community Group (DTCG). They also follow the sibling Color and Resolver modules of the same version.

- Format: https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/
- Color: https://www.w3.org/community/reports/design-tokens/CG-FINAL-color-20251028/
- Resolver: https://www.w3.org/community/reports/design-tokens/CG-FINAL-resolver-20251028/

> This is a final Community Group report, not a W3C Standard. The document itself declares it stable and ready for implementation. When the spec uses MUST/SHOULD, the same weight applies here.

This document says **how** to write tokens. **Which** tokens exist and why lives in `docs/` as the visual direction is defined.

---

## 1. Source of truth

- The `.tokens.json` files are the only source of truth. Everything else (CSS, prompts, visual documentation) is derived from them.
- Never edit a value directly in the derived CSS. Change the token and regenerate.
- Extension: `.tokens.json`. The spec recommends `.tokens` or `.tokens.json`. We use `.tokens.json` so editors open the files as JSON.
- Media type, if ever served: `application/design-tokens+json`.
- Plain JSON (RFC 8259). No comments, no trailing commas. Explanations go in `$description`.

## 2. Anatomy of a token

An object with `$value` is a token. An object without `$value` is a group.

```json
{
  "color": {
    "$type": "color",
    "$description": "Primitive colors. Do not use directly in pieces; use the semantic roles.",
    "neutral": {
      "900": {
        "$value": { "colorSpace": "srgb", "components": [0.067, 0.067, 0.067], "hex": "#111111" },
        "$description": "Primary ink."
      }
    }
  }
}
```

Reserved properties (`$` prefix):

| Property | Where | Use in eis-ds |
|---|---|---|
| `$value` | token | **Required.** |
| `$type` | token or group | **Required**, declared on the highest possible group and inherited by children. Tools cannot guess the type from the value. |
| `$description` | token or group | **Required on every token.** States the role and when to use it. Does not repeat the value. |
| `$deprecated` | token or group | `true` or a string pointing to the replacement. A token is never deleted without passing through here first. |
| `$extensions` | token or group | Custom data, always under the `com.diegoeis.eis-ds` key. E.g.: provenance of the decision. |
| `$extends` | group | Inherits another group (deep merge). Avoid, unless a mode really is a variation of another. |
| `$root` | inside a group | "Default" token of a group that also has variations (`color.accent.$root`, `color.accent.strong`). |

## 3. Names

**Spec rules (MUST):**
- Names do not start with `$`.
- Names do not contain `{`, `}` or `.`.
- Names are case-sensitive.

**eis-ds conventions:**
- All lowercase, `kebab-case`, no spaces or accents: `line-height`, not `Line Height`.
- Never two names that differ only in case.
- Path = category › property › variant, from general to specific: `color.neutral.900`, `space.200`, `font.size.300`.
- Numeric scales use steps of 100 (`100`, `200`, `300`…) to leave room for insertion without renaming.
- A primitive name describes **what it is** (`neutral.900`). A semantic name describes **what it is for** (`surface.base`, `ink.primary`). Never mix them.

**From path to CSS:** replace `.` with `-` and prefix with `--`.
`color.neutral.900` → `--color-neutral-900`. For `$root`, the segment is dropped: `color.accent.$root` → `--color-accent`.

## 4. Layers

| Layer | Folder | Content | Consumed by |
|---|---|---|---|
| Primitives | `src/tokens/primitive/` | Raw values: the palette, the space scale, the fonts. | Pieces, for everything without a semantic role. |
| Semantics | `src/tokens/semantic/` | Color roles that carry meaning (`surface`, `ink`, `line`, `signal`) and text styles. They point to primitives by reference. | Pieces, whenever the role exists. |

- **Semantic only when it adds meaning.** A role exists if it says *what a color is for* (background, text, line, signal) or if it will change between modes. An alias that only renames a primitive is complexity with no gain and is not added.
- **Using the primitive directly is normal** for space, radius, border, font size and weight, and for the chart gray scale (`--color-neutral-200 · 400 · 600 · 900`).
- **Surface, text, line and signal colors always through the role** (`--surface-panel`, `--ink-muted`, `--signal`), never through the primitive, because that is what changes when a new mode is added.
- When creating dark mode, reassess the chart scale: if it needs to invert, then it gets semantic roles.

## 5. References (aliases)

- Standard syntax: curly braces with the full path, `"$value": "{color.neutral.900}"`.
- A reference points to a **token**, never to a group. For a group's default, use `{color.accent.$root}`.
- Chained references are allowed (`a → b → c`). A circular reference is an error.
- The type does not need to be repeated in an alias. It inherits the type of the referenced token.
- JSON Pointer (`{ "$ref": "#/color/neutral/900/$value/components/0" }`) only when you need part of a composite value. In eis-ds this should be rare.

## 6. Allowed types

Every token uses a spec type. These are the ones eis-ds uses:

| Type | Value | Use in eis-ds |
|---|---|---|
| `color` | object `{ colorSpace, components, alpha?, hex? }` | Palette. |
| `dimension` | `{ "value": 16, "unit": "px" }`, unit only `px` or `rem` | Space, radius, line thickness, font size. `unit` required even for 0. |
| `fontFamily` | string or array, from most preferred to fallback | Typefaces. |
| `fontWeight` | number 1–1000 or alias (`regular`, `bold`…) | Weights. We prefer **number**. |
| `number` | JSON number | Line height (multiplier of the size), ratios. |
| `typography` | composite: `fontFamily`, `fontSize`, `fontWeight`, `letterSpacing`, `lineHeight` | Text styles, built by reference to primitives. |
| `border` | composite: `color`, `width`, `style` | If the system has borders. |
| `shadow` | composite: `color`, `offsetX`, `offsetY`, `blur`, `spread`, `inset?` | Only if the system decides to have shadows. |

Out of scope for now: `duration`, `cubicBezier`, `transition`, `gradient`, `strokeStyle`. They are added if and when decided.

### 6.1 Color

- `colorSpace`: **`srgb`**. Emails, generated images and most tools only understand sRGB. Another color space (`oklch`, `display-p3`) only with a recorded decision.
- `components`: `[r, g, b]` from 0 to 1, up to 3 decimal places.
- `hex`: **always filled in** in eis-ds (optional in the spec). Six digits, lowercase: `#f05627`. It is the value used in email, image prompts and human review.
- `components` and `hex` must represent the same color. When in doubt, `hex` wins and `components` are recalculated from it.
- `alpha`: only when different from 1. Transparency goes in `alpha`. `hex` stays at six digits.

### 6.2 Dimension

- Canonical unit: **`px`**. Slides, images and email work in pixels, and conversion to `rem` (÷16) can be done at web output.
- Integer values whenever possible.

## 7. Modes

Modes (light, dark, paper…) follow the **Resolver Module 2025.10**:

- A `src/tokens/eis-ds.resolver.json` file declares the fixed `sets`, i.e. the primitives, and a `mode` modifier with one context per mode, each pointing to its semantic file.
- Primitives are shared by all modes. Only the semantic layer changes.
- Every mode defines **the same set of names**. A role that exists in one mode exists in all.
- The default mode is declared in `default`.
- **Today only light mode exists.** Since a modifier with a single context is an error per the spec, the resolver has only two `sets` (`primitive`, `semantic`). The `mode` modifier is added together with the second mode.
- Note: the Resolver spec contradicts itself on the required `version` (`2025-10-01` in the table, `2025-11-01` in the text). We use `2025-10-01` until there is an erratum.

## 8. From token to CSS

Each token becomes a native CSS custom property. Conversion rules:

| Type | CSS output |
|---|---|
| `color` | the `hex`. With `alpha` < 1: `rgb(r g b / a)` |
| `dimension` | `16px` |
| `fontFamily` | comma-separated list, names with spaces in quotes, generic (`sans-serif`, `serif`, `monospace`) always last |
| `fontWeight` | number |
| `number` | number |
| alias | `var(--path-of-referenced)`, so the chain stays live in the CSS |
| `typography` | CSS has no composite variable: it becomes one variable per property (`--type-body-font-size`, `--type-body-line-height`…) **and** a `.eis-type-<name>` class that applies them all (`text-transform: uppercase` on `label`) |
| `border`, `shadow` | the CSS shorthand (`1px solid var(--…)`, `0 2px 8px 0 rgb(…)`) |

Modes in CSS: the default mode goes in `:root`, the others in `[data-mode="<name>"]`, redefining **only** semantic variables.

Conversion is done by `scripts/build-tokens.py` (Python, stdlib only), which also runs the §10 checklist before writing `src/css/tokens.css`. `letterSpacing` stays in `px` because the spec does not accept `em`. The value is calculated for the size at which the style is used (e.g.: `0.88px` = 0.08em at 11px).

## 9. Outside CSS

Prompts for image generators and tools that do not read CSS receive the resolved values as plain text: hex, px, font name. Each token's `$description` is written with this use in mind, explaining the role in plain language.

## 10. Checklist before marking a token as done

- [ ] `$type` present (on the token or inherited from the group)
- [ ] `$description` explains the role
- [ ] name lowercase and kebab-case, without `{`, `}`, `.` or `$`
- [ ] color with `colorSpace: srgb`, `components` and `hex` consistent with each other
- [ ] dimension with `unit`
- [ ] references resolve and do not form a cycle
- [ ] if semantic, exists in all modes
- [ ] contrast measured, if it is a text/background pair
- [ ] provenance recorded in `$extensions["com.diegoeis.eis-ds"].source`, when it comes from a reference
