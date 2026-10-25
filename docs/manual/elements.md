# Elements

Every basic element: when to use it, the HTML to copy, variants, and what is forbidden. Styles live in `site/css/elements.css`. The rendered versions are on `site/elements.html`.

**General rules for all elements**

- MUST use the native HTML element that carries the meaning. A `div` or `span` never pretends to be a button, checkbox, table, list or form.
- Every class starts with `eis-`. Naming: block `eis-panel`, part `eis-panel__head`, variant `eis-chip--signal`, state `eis-is-signal`.
- A **variant changes colour only** (through the local `--bg`, `--fg`, `--bd`, `--glow`). Never size, padding, radius, structure or behaviour.
- A piece MUST NOT restyle an element from `elements.css`. If it needs something different, change the element in the system (and on `elements.html`).
- Every control is keyboard-reachable and has a visible focus (`:focus-visible`, 2px `--ink` outline — already global).

---

## Decision table: which element?

| You need to… | Use |
|---|---|
| Trigger an action (save, filter, export, create) | **Button** `<button class="eis-button">` |
| Go to another page | **Link** `<a>` — styled as button (`<a class="eis-button">`) only if it's a call to action |
| Show a status, category, tag, code, count | **Chip** `<span class="eis-chip">` |
| Pick several independent options | **Checkbox** |
| Pick one of a few options in a form | **Radio** group |
| Pick one of many options | **Select** |
| Turn a setting on/off that applies immediately | **Switch** |
| Switch the view of the current page (Today / Week / All) | **Segmented** control |
| Show rows × columns of data | **Table** |
| Group content in a container | **Panel** |
| Content that opens and closes | **Disclosure** (`<details>`) |
| Label–value pairs (metrics, metadata) | `<dl>` |

**Button vs chip** — the most common mistake:

| | Button | Chip |
|---|---|---|
| Meaning | Acts | Describes |
| Shape | Rectangle, `--radius-100` | Pill, `--radius-full` |
| Text | MONO UPPERCASE, tracked | Mono sentence case |
| Height | 40px | 24px |
| Cursor | pointer | default |
| Hover | Background change + glow | None |
| Element | `<button>` / `<a>` | `<span>` |

A status MUST be a chip. A chip MUST NOT be clickable.

---

## Button

```html
<button class="eis-button eis-button--primary" type="button">Save</button>
<button class="eis-button" type="button">Cancel</button>
<button class="eis-button eis-button--ghost" type="button">Skip</button>
<button class="eis-button eis-button--signal" type="button">Record</button>
<button class="eis-button" type="button" disabled>Disabled</button>
<a class="eis-button" href="/report">Open report →</a>
```

| Variant | Use for | Limit |
|---|---|---|
| `--primary` | The main action of the view. | **One** per view. |
| *(default)* | Secondary actions. | — |
| `--ghost` | Low-emphasis actions next to others (Skip, Clear). | No glow on hover. |
| `--signal` | Only when the action **is** the signal: record, go live, publish. | Rare. Never "Save" or "Delete". |

- `type="button"` unless it submits a form (`type="submit"`) or resets (`type="reset"`).
- Hover: background shifts and a glow in the variant's colour appears (built in). Don't add your own shadow.
- Disabled: the `disabled` attribute, never a class.
- Order in a group: secondary/ghost first, primary last (rightmost).

## Chip

```html
<span class="eis-chip">Accepted</span>
<span class="eis-chip eis-chip--outline">PLT-204</span>
<span class="eis-chip eis-chip--solid">Organizer</span>
<span class="eis-chip eis-chip--signal">Overdue</span>
<span class="eis-chip eis-chip--hatch">Cancelled</span>
<span class="eis-chip eis-chip--dot">On track</span>
```

| Variant | Use for |
|---|---|
| *(default)* | Neutral status: accepted, waiting, on track. |
| `--outline` | Identifiers and categories: ticket codes, stream names. |
| `--solid` | Strong neutral status: new, organizer, problem. |
| `--signal` | The exception: overdue, conflict, urgent. Counts toward the signal budget. |
| `--hatch` | What no longer counts: cancelled, blocked. |
| `--dot` | Adds a status dot. Combine it with any variant. |

- Text in sentence case (`Overdue`, not `OVERDUE`).
- Never wrap a chip in `<a>` or `<button>`.

## Fields

```html
<div class="eis-field">
  <label for="title">Title</label>
  <input class="eis-input" id="title" name="title" type="text" placeholder="What needs to be done" aria-describedby="title-hint">
  <p class="eis-field__hint" id="title-hint">Start with a verb.</p>
</div>

<div class="eis-field">
  <label for="stream">Stream</label>
  <select class="eis-select" id="stream" name="stream">
    <option>Priority</option><option>Billing</option>
  </select>
</div>

<div class="eis-field">
  <label for="owner">Owner</label>
  <input class="eis-input" id="owner" name="owner" type="email" aria-invalid="true" aria-describedby="owner-err">
  <p class="eis-field__error" id="owner-err">Enter a valid email.</p>
</div>

<div class="eis-field">
  <label for="notes">Notes</label>
  <textarea class="eis-textarea" id="notes" name="notes"></textarea>
</div>
```

- Label always above the control, always present, linked with `for`/`id`. A placeholder is not a label.
- Use the right `type`: `email`, `date`, `number`, `search`, `url`…
- Error: `aria-invalid="true"` on the control + `aria-describedby` pointing to `.eis-field__error`. Never colour alone.
- Hint and error sit below the control.
- Put fields in a `<form>`. Put the actions at the end, primary last.

## Checkbox, radio, switch

```html
<fieldset class="eis-field eis-choices">
  <legend>Show</legend>
  <label class="eis-choice"><input class="eis-checkbox" type="checkbox" checked> Overdue</label>
  <label class="eis-choice"><input class="eis-checkbox" type="checkbox"> New today</label>
</fieldset>

<fieldset class="eis-field eis-choices">
  <legend>Sort by</legend>
  <label class="eis-choice"><input class="eis-radio" type="radio" name="sort" checked> Due date</label>
  <label class="eis-choice"><input class="eis-radio" type="radio" name="sort"> Age</label>
</fieldset>

<label class="eis-choice"><input class="eis-switch" type="checkbox" role="switch"> Compact rows</label>
```

- Always use a real `<input>`. Restyle it with `appearance:none`. Never replace it with a `span`.
- Groups of related options go in `<fieldset>` + `<legend>`.
- Radios in one group share `name`.
- Switch = checkbox + `role="switch"`, only for settings that apply immediately (no Save button).
- Wrapping the input in `<label class="eis-choice">` makes the whole text clickable and gives the hover.
- In a table, a checkbox without visible text needs `aria-label` or a `<label for>`.

## Segmented control

```html
<fieldset class="eis-segmented">
  <legend>Range</legend>
  <label><input type="radio" name="range" value="today" checked><span>Today</span></label>
  <label><input type="radio" name="range" value="week"><span>Week</span></label>
  <label><input type="radio" name="range" value="all"><span>All</span></label>
</fieldset>
```

- It is a radio group. Use it to switch the **view** of the current page, 2–4 options.
- Not for navigation between pages (use links) and not for form answers (use radio).

## Table

```html
<div class="eis-panel">
  <table class="eis-table">
    <caption class="eis-visually-hidden">Open tasks by stream</caption>
    <thead>
      <tr>
        <th scope="col"><span class="eis-visually-hidden">Select</span></th>
        <th scope="col">Stream</th>
        <th scope="col">Status</th>
        <th scope="col" class="eis-num">Open</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><input class="eis-checkbox" type="checkbox" aria-label="Select Billing"></td>
        <th scope="row">Billing</th>
        <td><span class="eis-chip eis-chip--signal">Overdue</span></td>
        <td class="eis-num">13</td>
      </tr>
    </tbody>
  </table>
</div>
```

- Tabular data MUST be `<table>` with `<thead>`, `<tbody>`, `<th scope>`. Never a grid of `div`s.
- Every table has a `<caption>` (visually hidden if the panel already has a title).
- Cells are vertically centred (`th`, `td`: `vertical-align: middle`). Don't override.
- Numbers: `.eis-num` (mono, tabular, right-aligned), including the header cell.
- Rows separated by `--line`. No zebra stripes, no vertical lines.
- On narrow screens a table MAY reflow into cards with CSS (`display:block/grid` on `tr`), keeping the HTML a table. If it can't reflow, wrap it in a horizontally scrollable container — the page itself MUST NOT scroll sideways.

## Panel

```html
<section class="eis-panel" aria-labelledby="agenda-h">
  <header class="eis-panel__head">
    <h2 class="eis-label" id="agenda-h">Today's agenda</h2>
    <span class="eis-mono">10:30 — 17:15</span>
  </header>
  <!-- content -->
</section>
```

- The only container. `--surface-panel`, 1px `--line`, `--radius-200`, no shadow.
- Head: label-style title on the left, mono meta (count, range) on the right.
- MUST NOT nest a panel inside a panel. Separate inside with hairlines.
- Content padding: `--space-200`.

## Disclosure

```html
<details class="eis-disclosure" open>
  <summary><h3 class="eis-label">Payments</h3><span class="eis-mono">13</span></summary>
  <!-- content -->
</details>
```

- Native `<details>`/`<summary>`. No JS needed.
- `+` closed, `−` open (built in). When open, the summary gets `--surface-canvas` background.
- A `--line` separates stacked disclosures.

## Metrics (label–value)

```html
<dl class="eis-metrics">
  <div><dt class="eis-label">Open</dt><dd>84</dd><dd class="eis-mono">11 streams</dd></div>
  <div><dt class="eis-label">Overdue</dt><dd>06</dd><dd class="eis-mono">3 in Platform</dd></div>
</dl>
```

- Always `<dl>`. Value in `metric` style, context line in `mono`.
- Only the metric that is the exception gets a signal mark.
- The layout of `.eis-metrics` is page CSS today. See `site/elements.html` for the reference.

## Breadcrumb and link

```html
<nav class="eis-breadcrumb eis-label" aria-label="Breadcrumb">
  <ol><li><a href="/tasks">Tasks</a></li><li aria-current="page">Work</li></ol>
</nav>

<p>Read the <a class="eis-link" href="/foundations">foundations</a> first.</p>
```

- Breadcrumb is `<nav>` + `<ol>`. The current item has `aria-current="page"` and shows in `--signal-ink`.
- Links inside text use `.eis-link` (hairline underline).

## Lists and avatar

```html
<ul class="eis-panel">
  <li><span class="eis-avatar" aria-hidden="true">AN</span><p>Ana<small class="eis-mono">Release plan</small></p><span class="eis-chip">Waiting</span></li>
</ul>
```

- Lists are `<ul>`/`<ol>`. A `--line` separates the rows.
- Avatar: initials in a circle, `aria-hidden` (the name is in the text). No photos, no colour fills.

## Labels and helpers

- `.eis-label` — label text style (mono, 11, uppercase, `--ink-muted`). For panel titles, table heads, nav section titles.
- `.eis-mono` — mono metadata (12, `--ink-muted`, tabular numbers).
- `.eis-visually-hidden` — hidden on screen, read by screen readers. For captions, legends and labels the design doesn't show.

## Not yet in the system

Dialog, popover/menu, tooltip, tabs, toast, pagination, icons. Until they exist, use the native element (`<dialog>`, `popover` attribute, `title`) and style it only with tokens. Propose the element for the system. Do not design it inside a piece.
