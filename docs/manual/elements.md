# Elements

Every basic element: when to use it, the HTML to copy, variants, and what is forbidden. Styles live in `src/shared/css/elements.css`. Elements are shared by every scope. The rendered versions are on `site/elements.html`.

**General rules for all elements**

- MUST use the native HTML element that carries the meaning. A `div` or `span` never pretends to be a button, checkbox, table, list or form.
- Every class starts with `eis-`. Naming: block `eis-panel`, part `eis-panel__head`, variant `eis-chip--accent`, state `eis-is-accent`.
- A **variant changes colour only** (through the local `--bg`, `--fg`, `--bd`, `--glow`). Never size, padding, radius, structure or behaviour.
- A **size** (`--sm`, `--lg`) changes size only: height, padding, gap and font size, all from the spacing and type tokens. Never colour. Combine one size with any variant. No size class = medium.
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
| Pick several of many options, and show the picks in the field | **Multi-select** `<div class="eis-multiselect">` |
| Turn a setting on/off that applies immediately | **Switch** |
| Switch the view of the current page (Today / Week / All) | **Tabs** |
| Show items one per row, with a short text and an action or status | **List** `<ul class="eis-list">` |
| Group each part of a panel body that has two or more titled parts | **Panel section** `<section class="eis-panel__section">` |
| Split two parts of the same panel body that have no title | **Divider** `<hr>` |
| Show rows × columns of data | **Table** |
| Group content in a container | **Panel** |
| Group the buttons that end a form or a step, at the right | **Actions** `<div class="eis-actions">` |
| Content that opens and closes | **Disclosure** (`<details>`) |
| Label–value pairs (metrics, metadata) | `<dl>`. A row of numbers: **Metrics** `<dl class="eis-metrics">` |

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

Naming: the orange is **accent** (`--accent`, `eis-button--accent`, `eis-chip--accent`), the market name for the brand highlight colour. The main action is **primary** (`eis-button--primary`, ink fill). `eis-button--black` is the same ink fill as a colour, for a dark button that is not the main action (a pressed choice). A remove or delete action is **danger** (`eis-button--danger`). Plain `eis-button` is the default (white).

---

## Button

```html
<button class="eis-button eis-button--primary" type="button">Save</button>
<button class="eis-button" type="button">Cancel</button>
<button class="eis-button eis-button--ghost" type="button">Skip</button>
<button class="eis-button eis-button--accent" type="button">Record</button>
<button class="eis-button" type="button" disabled>Disabled</button>
```

| Variant | Use for | Limit |
|---|---|---|
| `--primary` | The main action of a view, or of a panel that saves on its own (each Save on a settings page). | Use for a secondary action. |
| `--black` | Ink fill as a colour: a pressed choice, a dark button that is not the main action. | Use for the main action (use `--primary`). |
| `--danger` | Remove, delete: an action that loses data. A ghost with a red line and red text (`--danger-ink`); on hover it fills `--danger` with dark text. | Use for anything that does not remove or break. |
| *(default)* | Secondary actions. White background (`--surface-raised`), line border. | — |
| `--ghost` | Low-emphasis actions next to others (Skip, Clear). | No glow on hover. |
| `--accent` | Only when the action **is** the accent: record, go live, publish. In the app scope: the main action of the page head (`eis-app-page-head`), e.g. "New task" (layout.md §7, "Page head"). | Rare: one per page, and it counts toward the accent budget. Never "Save" or "Delete". |
| `--success` | Save, when the page asks for a positive action in green. | Not together with a `--primary` button for the same action. |

- `type="button"` unless it submits a form (`type="submit"`) or resets (`type="reset"`).
- Hover: background shifts and a glow in the variant's colour appears (built in). Don't add your own shadow.
- Disabled: the `disabled` attribute, never a class.
- Order in a group: secondary/ghost first, the `--primary` button last (rightmost).

### Button with an icon

```html
<button class="eis-button eis-button--primary" type="button"><i data-lucide="plus" class="eis-icon"></i>New topic</button>
<a class="eis-button" href="/report">Open report<i data-lucide="arrow-right" class="eis-icon"></i></a>
<button class="eis-button eis-button--icon eis-button--sm" type="button" aria-label="Edit topic" title="Edit topic"><i data-lucide="pencil" class="eis-icon"></i></button>
```

- The icon goes before the text (left) or after it (right). The button gap spaces it. Left is the default. Use right only for a direction: next, open, external.
- `eis-button--icon`: a square button with only an icon. It MUST have `aria-label` and `title` with the action. Combine it with any variant and size. Use it for repeated actions in a row or a table (edit, remove, archive), where a text button does not fit.
- One icon per button. Never an icon only for decoration in a text button that is clear without it.
- Never type a character as an icon (`+`, `→`, `×`, `✓`). Use the Lucide icon.

| Size | Height | Padding | Font | Use for |
|---|---|---|---|---|
| `--sm` | `--space-300` (32px) | 1.5 × `--space-100` | `--font-size-100` | Actions inside a row, a table or a dense toolbar. |
| *(default)* | 40px | `--space-200` | `--font-size-200` | Forms and page toolbars. |
| `--lg` | 1.5 × `--space-300` (48px) | `--space-300` | `--font-size-300` | The single main action of an empty state or landing view. |

## Chip

```html
<span class="eis-chip">Accepted</span>
<span class="eis-chip eis-chip--outline">PLT-204</span>
<span class="eis-chip eis-chip--solid">Organizer</span>
<span class="eis-chip eis-chip--accent">Overdue</span>
<span class="eis-chip eis-chip--hatch">Cancelled</span>
<span class="eis-chip eis-chip--dot">On track</span>
<span class="eis-chip eis-chip--blue">Platform</span>
<span class="eis-chip eis-chip--blue eis-chip--pastel">Platform</span>
```

| Variant | Use for |
|---|---|
| *(default)* | Neutral status: accepted, waiting, on track. |
| `--outline` | Identifiers and categories: ticket codes, stream names. |
| `--solid` | Strong neutral status: new, organizer, problem. |
| `--accent` | The exception: overdue, conflict, urgent. Counts toward the accent budget. |
| `--success` | A positive state: done, sent, saved. |
| `--hatch` | What no longer counts: cancelled, blocked. |
| `--dot` | Adds a status dot. Combine it with any variant. |
| `--pink`, `--terracotta`, `--yellow`, `--green`, `--aqua`, `--blue`, `--lilac` | Categories: a team, a project, a topic, a calendar type. The colour tells groups apart. It does not mark a state. |
| `--pastel` | The light tone of the same hue. Put it after a category colour: `eis-chip eis-chip--blue eis-chip--pastel`. It has no effect on other variants. |

| Size | Height | Padding | Font | Use for |
|---|---|---|---|---|
| `--sm` | `--space-200` (16px) | 0.75 × `--space-100` | `--font-size-100` | Inline with a line of text: a task title, a table cell. |
| *(default)* | 24px | 10px | `--font-size-200` | Meta rows, lists, panel heads. |
| `--lg` | `--space-300` (32px) | 1.5 × `--space-100` | `--font-size-300` | A status that leads a section or a page head. |

- Text in sentence case (`Overdue`, not `OVERDUE`).
- Never wrap a chip in `<a>` or `<button>`.
- A chip that shows a value the user picked can hold one remove button, `<button class="eis-chip__remove">`, after its text. The CSS draws the Lucide `x`. Give the button `aria-label` and `title` ("Remove Billing"). Only the button reacts to the pointer. The chip stays without hover. The multi-select writes these chips for you.
- Give each category one colour, and keep it in all views. Use one tone per set: all mid tone or all pastel. Use the mid tone when the chips must stand out, and the pastel tone in dense lists.
- Never use a category colour for a state. Overdue is `--accent`, done is `--success`.
- With more than seven categories, use `--outline` for the rest. Do not repeat a colour in one view.

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
- A fieldset field (a group of options, a multi-select) uses `<legend>` as its label. The legend has the same style and the same gap to the control as a label.
- Use the right `type`: `email`, `date`, `number`, `search`, `url`…
- Error: `aria-invalid="true"` on the control + `aria-describedby` pointing to `.eis-field__error`. Never colour alone.
- Hint and error sit below the control. An empty hint or error takes no room, so a script can keep the `<p>` and fill it on demand.
- Fields always use body type, also inside a label-styled container (a panel title being edited).
- Put fields in a `<form>`. Put the actions at the end, the `--primary` button last.

### Multi-select

```html
<fieldset class="eis-field">
  <legend>Teams</legend>
  <div class="eis-multiselect" data-eis-multiselect>
    <ul class="eis-multiselect__chips" aria-label="Selected teams"></ul>
    <details class="eis-multiselect__menu">
      <summary><span class="eis-multiselect__placeholder">Select teams</span></summary>
      <div class="eis-multiselect__options">
        <label class="eis-choice"><input class="eis-checkbox" type="checkbox" name="teams" value="billing" checked> Billing</label>
        <label class="eis-choice"><input class="eis-checkbox" type="checkbox" name="teams" value="platform"> Platform</label>
        <label class="eis-choice"><input class="eis-checkbox" type="checkbox" name="teams" value="data"> Data</label>
      </div>
    </details>
  </div>
</fieldset>
```

Load the script at the end of `<body>`:

```html
<script src="<src>/shared/js/multiselect.js"></script>
```

- Use it to pick several values from a list of about 5 to 30 options: teams, tags, people. The picks stay visible in the field. For 2 to 4 options, show the checkboxes in a `fieldset` (see "Checkbox, radio, switch"). To pick one value, use the select.
- The options are native checkboxes in a `<details>`. The form sends the checked values with or without the script. Give every checkbox the same `name`.
- The field is a `fieldset` with a `legend`, because it holds a group of controls.
- `shared/js/multiselect.js` shows each checked option as a chip with a remove button (`eis-chip__remove`), in the order of the list. The remove button unchecks the option. Esc and a click outside the field close the list. After a remove, the focus goes to the next remove button, or to the summary.
- The placeholder in `__placeholder` shows while the user has no option checked. With a value, it leaves the view, but screen readers still read it as the name of the summary.
- The list stays open while the user checks options. It is as wide as the field, and scrolls when it is taller than 256px (2 × `--space-500`).
- The field grows in height when the chips wrap to more rows. With no value, or with chips on one row, it is 40px tall, as the other fields.
- A script that checks an option from code must dispatch a `change` event (`bubbles: true`) on the checkbox, so the chips follow. A form reset updates the chips.
- Error: put `aria-invalid="true"` and `aria-describedby` on the `fieldset`, and the `.eis-field__error` after the `.eis-multiselect`.

### Form

```html
<form class="eis-panel eis-form" action="/tasks" method="post">
  <div class="eis-field">
    <label for="title">Title</label>
    <input class="eis-input" id="title" name="title" type="text">
  </div>
  <div class="eis-field">
    <label for="due">Due</label>
    <input class="eis-input" id="due" name="due" type="date">
  </div>
  <div class="eis-field eis-field--wide">
    <label for="notes">Notes</label>
    <textarea class="eis-textarea" id="notes" name="notes"></textarea>
  </div>
  <div class="eis-actions">
    <button class="eis-button eis-button--ghost" type="reset">Clear</button>
    <button class="eis-button eis-button--primary" type="submit">Create task</button>
  </div>
</form>
```

- `.eis-form` goes on the `<form>`. It sets the fields in two equal columns, with its own padding. Put it on the same element as `eis-panel`: the form is the panel.
- `.eis-field--wide` makes a field take the whole row: a textarea, a long text. It works only inside `.eis-form`.
- Close the form with an `.eis-actions` as the last child (see "Actions"). In `.eis-form` it takes the whole row.
- At ≤640px the form has one column.
- Use it for a form that is the whole content of a panel (create, edit). Don't use it for fields in an `eis-panel__body` next to other content.
- In the app scope, a settings panel lays out its fields with `eis-app-form-row` inside `eis-panel__body`, and its buttons in `eis-panel__footer` (layout.md §7). Don't mix `eis-form` with `eis-app-form-row`.

### Actions

```html
<div class="eis-actions">
  <button class="eis-button eis-button--ghost" type="button">Cancel</button>
  <button class="eis-button eis-button--primary" type="submit">Create task</button>
</div>
```

- `.eis-actions` groups the buttons of one task: Cancel and Create, Clear and Save. It puts them at the right, in one row that wraps, with a `--line` above it.
- The `--primary` button goes last. Use one `--primary` button in a group, or none.
- Use it in an `eis-form` (as the last child), at the end of an `eis-panel__body`, or in a page section with no panel. It is not a panel part: never put it as a direct child of an `eis-panel`.
- Use `<button>` elements, or `<a class="eis-button">` for a link. A group holds only buttons.
- `eis-actions` vs `eis-panel__footer`: the footer is the bottom part of a panel. It has no line above it and acts on the whole panel. The Save of a settings panel stays in `eis-panel__footer` (see "Panel structure"). Use `eis-actions` for a group of buttons inside content: the end of a form, or a step in a body.

## Checkbox, radio, switch

```html
<fieldset class="eis-field">
  <legend>Show</legend>
  <label class="eis-choice"><input class="eis-checkbox" type="checkbox" checked> Overdue</label>
  <label class="eis-choice"><input class="eis-checkbox" type="checkbox"> New today</label>
</fieldset>

<fieldset class="eis-field">
  <legend>Sort by</legend>
  <label class="eis-choice"><input class="eis-radio" type="radio" name="sort" checked> Due date</label>
  <label class="eis-choice"><input class="eis-radio" type="radio" name="sort"> Age</label>
</fieldset>

<label class="eis-choice"><input class="eis-switch" type="checkbox" role="switch"> Compact rows</label>
```

- Always use a real `<input>`. Restyle it with `appearance:none`. Never replace it with a `span`.
- Groups of related options go in `<fieldset class="eis-field">` + `<legend>`. On a `fieldset`, `eis-field` removes the border and stacks the options. No other class is necessary.
- Radios in one group share `name`.
- Switch = checkbox + `role="switch"`, only for settings that apply immediately (no Save button).
- Wrapping the input in `<label class="eis-choice">` makes the whole text clickable and gives the hover.
- In a table, a checkbox without visible text needs `aria-label` or a `<label for>`.

## Tabs

```html
<fieldset class="eis-tabs">
  <legend>Range</legend>
  <label><input type="radio" name="range" value="today" checked><span>Today</span></label>
  <label><input type="radio" name="range" value="week"><span>Week</span></label>
  <label><input type="radio" name="range" value="all"><span>All</span></label>
</fieldset>
```

- It is a radio group (not ARIA tabs). Use it to switch the **view** of the current page, 2–4 options.
- The checked option has the `--surface-inverse` fill and `--ink-inverse` text, as the current item of a nav. An option under the pointer has the `--surface-canvas` fill.
- Height 40px, like the default button, input and select: in a toolbar, put tabs next to a default-size button (not `--sm`), and they line up.
- When the options do not fit the width (narrow screens), they wrap to more rows and each row fills the width. There is never a horizontal scroll.
- Radius `--radius-100`, like buttons, inputs and selects. The selected item uses the inner radius (`--radius-100` minus the padding).
- Not for navigation between pages (use links) and not for form answers (use radio).
- Count: when an option filters a list, put the number of items after its text, in `<span class="eis-tabs__count">` inside the option's `<span>`: `<span>Team <span class="eis-tabs__count">04</span></span>`. Two digits at least, as in metrics. The count of the whole list goes on `All`.

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
        <td><span class="eis-chip eis-chip--accent">Overdue</span></td>
        <td class="eis-num">13</td>
      </tr>
    </tbody>
  </table>
</div>
```

- Tabular data MUST be `<table>` with `<thead>`, `<tbody>`, `<th scope>`. Never a grid of `div`s.
- Every table has a `<caption>` (visually hidden if the panel already has a title).
- Cells are vertically centred (`th`, `td`: `vertical-align: middle`). Don't override. A row that holds an `eis-disclosure` (a list that opens) aligns its cells to the top instead, so the row's title stays at the top when the list is open, and a disclosure after other content in the cell (a date, a text) keeps `--space-200` above it. The table sets both: write no class.
- Numbers: `.eis-num` (mono, tabular, right-aligned), including the header cell.
- Header row (`thead th`): `--surface-inverse` background, `--ink-inverse` text, label type, inner padding. A scope may change the inline padding of the header to align it with its cells. It never changes the colours.
- Rows separated by `--line`. No zebra stripes, no vertical lines.
- A selected row gets the `--surface-selected` background. A row is selected when it has `aria-selected="true"`; a checked checkbox in the row does not select it (a done task is not a selection). Write no class. Every text role passes on it, `--ink-muted` included.
- On narrow screens a table MAY reflow into cards with CSS (`display:block/grid` on `tr`), keeping the HTML a table. If it can't reflow, wrap it in a horizontally scrollable container — the page itself MUST NOT scroll sideways.

## Panel

```html
<section class="eis-panel" aria-labelledby="agenda-h">
  <header class="eis-panel__head">
    <h2 class="eis-panel__title" id="agenda-h">Today's agenda</h2>
    <span class="eis-mono">10:30 — 17:15</span>
  </header>
  <!-- content -->
</section>
```

- The only container. `--surface-panel`, 1px `--line`, `--radius-100`, no shadow.
- Head: `--surface-head` background, text in `--ink`. The title is `eis-panel__title` (label type, ink: it names the panel, it is not a muted label) on the left, mono meta (count, range) on the right. `eis-mono` and an outline chip in the head take `--ink`: `--ink-muted` fails on `--surface-head` (3.8:1). `eis-label` is in `--ink` on every surface.
- MUST NOT nest a panel inside a panel. Separate inside with hairlines.
- Content padding: `--space-200`.

### Panel structure

A panel holds only its parts, as direct children, in this order:

```html
<section class="eis-panel" aria-labelledby="run-h">
  <header class="eis-panel__head"><h2 class="eis-panel__title" id="run-h">Run</h2></header>
  <div class="eis-panel__body" id="run"><!-- fields, text. The id of a script goes here --></div>
  <footer class="eis-panel__footer"><button class="eis-button eis-button--primary" type="button">Save</button></footer>
</section>
```

- The head is first. Use it when the panel has a title. The footer is last and optional. A panel has one head and one footer at most.
- MUST NOT put a wrapper (`div`, `form`, `section`) between the panel and its parts. Loose content (a heading, a paragraph, a field, a button) goes in the body, never directly in the panel.
- In place of a body, a panel can hold a full-width element that has its own padding: `eis-table` (or the horizontal scroll wrapper of a table that can't reflow), `eis-list`, `eis-disclosure`, `eis-metrics`, or a scope component that `layout.md` §7 lists as a panel part. Put it directly in the panel, after the head.
- The panel can be the content itself: a list (`<ul class="eis-panel eis-list">`) or a form with no title (`<form class="eis-panel eis-form">`, see Form). Its children are then the rows or the fields. It has no head, body or footer.
- MUST NOT put an `eis-panel__body` inside another `eis-panel__body` or inside an `eis-panel__section`. A `<form>` inside a body gets no `eis-panel__body` class.
- A panel with a head and a footer that submits a form: make the `<form>` the panel (`<form class="eis-panel">`, with the head, the body and the footer in it). The `<form>` never sits between the panel and its parts.
- The Save button of a settings panel (it saves the whole panel) goes in `eis-panel__footer`, never in the body or the head. A button that acts on one row or one field (Save of one key, Remove) stays in that row.
- In an `eis-disclosure`, the same parts come after the `<summary>`: a body, then an optional footer.
- `scripts/check-css.py` fails when a page in `site/` or `index.html` breaks these rules.

- `eis-panel__body`: the padded content area under the head. Its children stack with a `--space-200` gap. Use it for any panel that holds fields or text, not for a panel that holds a table or a metric row.
- When a script fills the body of a panel, put the `id` on the body itself: `<div class="eis-panel__body" id="doctor">`. The script writes the content into it. Never put an empty `<div id="…">` in the panel, or around or inside the body, for the script: the body loses its padding and gap, or the content gets them twice. The same rule applies to an `eis-panel__section` that a script fills.
- `eis-bleed` (helper): a direct child of `eis-panel__body` that touches the panel edges: no side padding, none above it when it is first, none below it when it is last. Use it for a quoted block or a strip, never to remove the body padding of fields.
- `eis-panel__footer`: the bottom area for actions. Same padding, buttons in one row that wraps. No line above it. After a body it drops its top padding, so body and footer share one gap.

### Panel section

```html
<section class="eis-panel" aria-labelledby="ws-h">
  <header class="eis-panel__head"><h2 class="eis-panel__title" id="ws-h">Workspace</h2></header>
  <div class="eis-panel__body">
    <section class="eis-panel__section" aria-labelledby="ws-daily-h">
      <h3 class="eis-label" id="ws-daily-h">Daily notes folder</h3>
      <div class="eis-field">
        <label for="ws-daily">Folder</label>
        <input class="eis-input" id="ws-daily" type="text" value="notes/daily">
      </div>
    </section>
    <section class="eis-panel__section" aria-labelledby="ws-topics-h">
      <h3 class="eis-label" id="ws-topics-h">Your topics</h3>
      <p>Topics that only this workspace uses.</p>
      <p><button class="eis-button eis-button--sm" type="button"><i data-lucide="plus" class="eis-icon"></i>Topic</button></p>
      <ul class="eis-list eis-bleed">…</ul>
    </section>
  </div>
  <footer class="eis-panel__footer"><button class="eis-button eis-button--primary" type="button">Save</button></footer>
</section>
```

- Use `eis-panel__section` when a panel body has two or more parts, and each part has a title. Put one section around each whole part: its title and all its content (text, fields, buttons, a list).
- When the body has only one part, do not use a section. Put the content directly in `eis-panel__body`. The panel title names it.
- A section is a direct child of `eis-panel__body`. Do not mix sections and loose content in one body. Do not put a section in a section.
- The title is the first child: `<h3 class="eis-label">` with an `id` (one level below the panel title). The `<section>` has `aria-labelledby` with that `id`. The section shows its title one step up (`--font-size-200`), as the heading of a disclosure, so it reads above the field labels of the part.
- The content of a section stacks with a `--space-200` gap, as in the body. `eis-bleed` works in a section as it does in the body.
- From the second section on, a `--line` above the section touches the panel edges. Do not write an `<hr>` between sections.

## Disclosure

```html
<details class="eis-disclosure" open>
  <summary><h3>Payments</h3><span class="eis-mono">13</span></summary>
  <!-- content -->
</details>
```

- Native `<details>`/`<summary>`. It opens and closes without JS. It is the only element that opens and closes: groups of tasks, topics or any list use it too.
- The CSS draws the marker on the right: Lucide `plus` when closed, `minus` when open. Write no icon in the summary. When open, the summary gets `--surface-canvas` background and a `--line` under it. A closed summary under the pointer gets `--surface-hover`; `eis-mono` in it takes `--ink` (`--ink-muted` fails on `--surface-hover`).
- The heading in the summary (`h2`, `h3` or `h4`, no class needed) uses the label type one step up (`--font-size-200`), in `--ink`: it names the group. A count or a path goes after it in `eis-mono`.
- A `--line` separates stacked disclosures. To list several, put them as direct children of one `eis-panel`.
- Content goes right after the summary: an `eis-panel__body` for text and fields, or an `eis-table` (its first row drops its top line, the summary line already separates them), then an optional `eis-panel__footer`.
- The styles reach only the disclosure's own summary (`> summary`). A `<details>` inside the content keeps its own style.

## Metrics (label–value)

```html
<dl class="eis-metrics">
  <div><dt class="eis-label">Open</dt><dd>84</dd><dd>11 streams</dd></div>
  <div class="eis-metrics__cell--accent"><dt class="eis-label">Overdue</dt><dd>06</dd><dd>3 in Platform</dd></div>
</dl>
```

- Always `<dl>`. Each cell is a `<div>` with a `<dt>` (the label, `eis-label`), a `<dd>` (the value) and an optional second `<dd>` (the context line). The CSS sets the context line in mono and `--ink-muted`. Write no class on it.
- The first `<dd>` takes the `metric` type. Write numbers with two digits at least (`06`, not `6`).
- One column per cell: two cells make two columns, four make four. A `--line` separates the cells. Prefer two to four cells. The min height of a cell is `--space-400` × 2.
- Small screens: at ≤760px, two cells stay side by side and four cells go 2 × 2. Other counts stack in one column at ≤640px, with a `--line` between the cells. On a small screen the value drops to `--font-size-600`.
- `eis-metrics__cell--accent` on a cell puts an accent dot before its label. Use it only on the metric that is the exception (overdue, conflict), once per row.
- Put the `<dl>` as a direct child of an `eis-panel`, under its `eis-panel__head`. The cells have their own padding.
- It is the one row of numbers for every scope. The app scope has no metrics component of its own.
- Don't use it for metadata in running text (owner, date, source): use a plain `<dl>`.

## Breadcrumb and link

```html
<nav class="eis-breadcrumb eis-label" aria-label="Breadcrumb">
  <ol><li><a href="/tasks">Tasks</a></li><li aria-current="page">Work</li></ol>
</nav>

<p>Read the <a class="eis-link" href="/foundations">foundations</a> first.</p>
```

- Breadcrumb is `<nav>` + `<ol>`. The current item has `aria-current="page"` and shows in `--accent-ink`.
- Every `<a>` is underlined and turns `--accent-ink` on hover. This is the base style: you get it with no class. Never remove the underline from a link in text.
- `.eis-link` makes a link in running text quieter: `--ink` text with a `--line` underline. On hover the text and the underline turn `--accent-ink`.
- Use `--accent-ink`, not `--accent`, for link text: `--accent` fails contrast as text (3.1:1 on `--surface-panel`).
- Exceptions, set by the component: `.eis-button` links look like buttons, and navigation menus (`.eis-app-nav`, the web header and doc nav) have no underline because the whole item is the target.

## Lists and avatar

A list in its own box:

```html
<ul class="eis-panel eis-list">
  <li><span class="eis-avatar" aria-hidden="true">AN</span><p>Ana<small class="eis-mono">Release plan</small></p><span class="eis-chip">Waiting</span></li>
</ul>
```

A list inside a panel body, rows to the panel edges:

```html
<div class="eis-panel__body">
  <h3 class="eis-label">Topics</h3>
  <ul class="eis-list eis-bleed">
    <li>
      <p>Checkout<small class="eis-mono">project — New payment flow</small></p>
      <label class="eis-choice"><input class="eis-switch" type="checkbox" role="switch" checked> Use</label>
    </li>
  </ul>
</div>
```

- Lists are `<ul>`/`<ol class="eis-list">`. A `--line` separates the rows. The first row has no line.
- A row is one line: an optional leading `eis-avatar`, then one `<p>` that takes the free width, then optional trailing items (chips, buttons, a switch). The trailing items stay at the right end and never shrink.
- The `<p>` holds the title. An optional `<small class="eis-mono">` under it holds the description, in muted ink. Long text wraps.
- When the main part of a row is not a `<p>` (for example a `<form>` that edits the row in place), give it `eis-grow`. It then takes the free width like the `<p>`.

A row with a title, a description and a group of options (a topic and the workspaces it applies to):

```html
<ul class="eis-list eis-bleed">
  <li>
    <div class="eis-grow">
      <h6>Atlas</h6>
      <p>project — New billing engine</p>
      <fieldset>
        <legend>Workspaces for Atlas</legend>
        <label class="eis-choice"><input class="eis-checkbox" type="checkbox" checked> Payments</label>
        <label class="eis-choice"><input class="eis-checkbox" type="checkbox"> Growth</label>
      </fieldset>
    </div>
    <button class="eis-button eis-button--sm eis-button--danger" type="button">Remove</button>
  </li>
</ul>
```

- Use this form when a row holds more than a title and a description. The main part is a `<div class="eis-grow">` with a heading, then a `<p>`, then a `<fieldset>`. The `<p>` and the `<fieldset>` are optional.
- The heading (`h4`, `h5` or `h6`, no class) looks like the title of the short form. The `<p>` right after it looks like the `<small>` description: mono, muted.
- The `<fieldset>` needs no class. It puts its options (`eis-choice` + `eis-checkbox`) in a row that wraps on narrow screens. Its `<legend>` is hidden on screen, but it MUST name the group for screen readers: write the row title in it (`Workspaces for Atlas`).
- The short form (`<p>` + `<small>`) still works. Use it when the row has only a title and a description.
- Put the box on the list itself (`eis-panel eis-list`) or put the list in an `eis-panel__body`. In a body, add `eis-bleed` so the rows touch the panel edges and do not get the body padding twice.
- Avatar: initials in a circle, `aria-hidden` (the name is in the text). No photos, no colour fills.

## Divider

```html
<div class="eis-panel__body">
  <ul class="eis-list eis-bleed">…</ul>
  <hr>
  <label class="eis-choice"><input class="eis-switch" type="checkbox" role="switch" checked> Use the shared teams</label>
</div>
```

- `<hr>` is a hairline: one `--border-width-100` line in `--line`, no margin. The gap of the container spaces it.
- Use it to split two parts of the same panel body that have no title. In an `eis-panel__body` it touches the panel edges, like the rows of a list.
- When each part has a title, use `eis-panel__section` (see Panel). The section draws the line. Do not add an `<hr>`.
- Do not use it between panels or between list rows. Panels have their own border and lists draw their own lines.

## Icons

```html
<i data-lucide="pencil" class="eis-icon"></i>
```

Load at the end of `<body>`, Lucide first:

```html
<script src="https://unpkg.com/lucide@1.66.0/dist/umd/lucide.min.js"></script>
<script src="<src>/shared/js/icons.js"></script>
```

- Load a fixed Lucide version, never `@latest`. A new version can remove or rename an icon. Change the version on purpose and check the pages after the change.
- The set is [Lucide](https://lucide.dev/icons) (ISC licence): line icons with a 2px stroke, the same weight as the system lines. Use the Lucide name in `data-lucide`.
- `eis-icon` is 16px (`--space-200`) and takes the text colour (`currentColor`). Never colour an icon on its own. It follows the button or text it sits in.
- `shared/js/icons.js` calls Lucide on load. Lucide draws only the `<i>` that are on the page at that moment. A page that writes HTML with JavaScript after the load (`innerHTML` from a data file) adds new `<i>`, so the script watches the page and draws them too. A page that writes no HTML with JavaScript does not need that part, and it does no harm.
- Lucide hides the icon from screen readers (`aria-hidden="true"`) and keeps the `class`. Do not write `aria-hidden` on the `<i>`. The text or the `aria-label` of the control carries the meaning.
- Without the network the icon is empty. So an icon never is the only way to know what a control does: the control has text, or `aria-label` plus `title`.
- Inside a button, see "Button with an icon".
- An icon that belongs to an element, not to the content (the marker of a disclosure, the check of a done list, the arrow of the sidebar toggle), is drawn by the CSS. `shared/css/icons.css` holds these Lucide icons as `--icon-<name>` (generated by `scripts/build-icons.py`). A rule uses one as a mask on a pseudo-element, so it takes the text colour and needs no markup and no JavaScript.
- A native `<select>` cannot hold a pseudo-element, so its chevron is a background image. A background image cannot take the text colour. For these icons the script writes a copy with the stroke in a token colour, named `--icon-<name>-<token>` (`--icon-chevron-down-ink`). Add the icon to `INKED` in the script.
- The check of `eis-checkbox` and the chevron of `eis-select` and `eis-multiselect` are Lucide icons (`check`, `chevron-down`). If Lucide has no icon for a need, tell the owner of the system. Do not draw one.
- Never type a character as an icon (`+`, `−`, `→`, `×`, `✓`), in HTML or in CSS `content`.

## Labels and helpers

- `.eis-label` — label text style (mono, 11, uppercase, `--ink`). For panel titles, table heads, nav section titles, the title of a part of a panel body. It is in `--ink` on every surface: it names what follows, it is not metadata. Measured: 18.9:1 on `--surface-panel`, 17.6:1 on `--surface-canvas`, 13.9:1 on `--surface-head`. Use `eis-mono` for muted metadata.
- `.eis-mono` — mono metadata (12, `--ink-muted`, tabular numbers).
- `.eis-visually-hidden` — hidden on screen, read by screen readers. For captions, legends and labels the design doesn't show.
- `.eis-width-fit`, `.eis-width-100` … `.eis-width-500` — the width of a field, a button or a block: as wide as its content, or the `--width-*` step (128, 192, 256, 360, 480px). Never wider than the container. In a flex row (`eis-app-inline`) the item keeps its width and the others take the rest. In a row of fields (`eis-app-add-bar`, `eis-app-form-row`, `eis-app-filters__fields`) the step is the base and the minimum width of the field: it grows into the free room and wraps when it no longer fits (layout.md §7, "Rows of fields"). `eis-width-fit` in a row of fields keeps the content's width and does not grow. A short select before the field it controls is `<div class="eis-field eis-width-fit">`. Don't write a width in page CSS for this.
- `.eis-grow` — the item takes the free room of its flex row first (it grows three times as fast as the others). In a row of fields it marks the main field: it has no `--width-400` limit, while the other fields stop growing at `--width-400`. Put it on one item per row. With a width helper, the helper sets its base.

## Not yet in the system

Dialog, popover/menu, tooltip, tabs, toast, pagination. Until they exist, use the native element (`<dialog>`, `popover` attribute, `title`) and style it only with tokens. Propose the element for the system. Do not design it inside a piece.
