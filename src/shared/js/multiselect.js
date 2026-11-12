/* eis-ds · shared/js/multiselect.js
   Drives the multi-select field (elements.md, "Multi-select"). The options are native checkboxes in a
   <details>, so the form sends the values with or without this script. The script:
   - shows each checked option as a chip with a remove button, in the order of the list;
   - unchecks the option when its remove button is clicked;
   - closes the list on Esc or on a click outside the field;
   - with an All option (a checkbox with data-eis-multiselect-all and no name, the first of the list):
     checks or unchecks every option that is not disabled, and shows checked when all are, mixed
     (indeterminate) when some are. All is never sent with the form and never shows as a chip.
   Load it at the end of <body>:
     <script src="<src>/shared/js/multiselect.js"></script>
   It starts every [data-eis-multiselect] that is in the page when it loads. A page that adds a field
   later (from a template) calls EisMultiselect.init(container) after it adds the field. The call starts
   each field in the container, or the container itself, and skips a field that already runs.
   The chips follow the checkboxes. A script that checks a box from code must dispatch a "change" event
   on it (bubbles: true) for the chips to follow. A form reset updates the chips. */
(function () {
  "use strict";
  function start(root) {
    if (root.eisMultiselect) return;
    var chips = root.querySelector(".eis-multiselect__chips");
    var menu = root.querySelector(".eis-multiselect__menu");
    var summary = menu && menu.querySelector("summary");
    if (!chips || !menu || !summary) return;
    root.eisMultiselect = true;
    var boxes = function () { return root.querySelectorAll(".eis-multiselect__options input[type=checkbox]:not([data-eis-multiselect-all])"); };
    var all = root.querySelector(".eis-multiselect__options input[data-eis-multiselect-all]");

    function name(box) {
      var label = box.closest("label");
      return (label ? label.textContent : box.value).trim();
    }
    function syncAll() {
      if (!all) return;
      var on = Array.prototype.filter.call(boxes(), function (b) { return !b.disabled; });
      var n = on.filter(function (b) { return b.checked; }).length;
      all.checked = on.length > 0 && n === on.length;
      all.indeterminate = n > 0 && n < on.length;
    }
    function render() {
      syncAll();
      chips.textContent = "";
      boxes().forEach(function (box, i) {
        if (!box.checked) return;
        var text = name(box);
        var chip = document.createElement("li");
        chip.className = "eis-chip";
        chip.append(text);
        var remove = document.createElement("button");
        remove.type = "button";
        remove.className = "eis-chip__remove";
        remove.setAttribute("aria-label", "Remove " + text);
        remove.title = "Remove " + text;
        remove.dataset.index = i;
        chip.append(remove);
        chips.append(chip);
      });
    }

    root.addEventListener("change", function (e) {
      if (e.target === all) {
        /* every option follows All; each changed box sends its own change event, as the page expects */
        var want = all.checked;
        boxes().forEach(function (box) {
          if (box.disabled || box.checked === want) return;
          box.checked = want;
          box.dispatchEvent(new Event("change", { bubbles: true }));
        });
        render();
        return;
      }
      if (e.target.matches("input[type=checkbox]")) render();
    });
    chips.addEventListener("click", function (e) {
      var remove = e.target.closest(".eis-chip__remove");
      if (!remove) return;
      var box = boxes()[remove.dataset.index];
      box.checked = false;
      box.dispatchEvent(new Event("change", { bubbles: true }));
      /* the button is gone: give the focus to the next chip's button, or to the summary */
      var rest = chips.querySelectorAll(".eis-chip__remove");
      var i = 0;
      while (i < rest.length && Number(rest[i].dataset.index) < Number(remove.dataset.index)) i++;
      (rest[i] || summary).focus();
    });
    root.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.open) { menu.open = false; summary.focus(); }
    });
    var form = root.closest("form");
    if (form) form.addEventListener("reset", function () { setTimeout(render); });
    render();
  }

  function init(container) {
    var scope = container || document;
    if (scope.matches && scope.matches("[data-eis-multiselect]")) start(scope);
    scope.querySelectorAll("[data-eis-multiselect]").forEach(start);
  }

  /* one listener for all fields: a click outside a field closes its list. The path is read from the
     event, because a remove button leaves the page before this listener runs */
  document.addEventListener("click", function (e) {
    var path = e.composedPath();
    document.querySelectorAll("[data-eis-multiselect] .eis-multiselect__menu[open]").forEach(function (menu) {
      if (path.indexOf(menu.closest("[data-eis-multiselect]")) < 0) menu.open = false;
    });
  });

  window.EisMultiselect = { init: init };
  init(document);
})();
