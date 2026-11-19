/* eis-ds · shared/js/modal.js
   Opens and closes the modal (elements.md, "Modal"). The modal is a native <dialog class="eis-modal">.
   showModal() gives the top layer, the focus trap, Esc and the return of the focus. The script adds:
   - a click on an element with data-eis-modal-open="<dialog id>" opens that dialog;
   - a click on an element with data-eis-modal-close (the x of the head, Cancel) closes the dialog it is in;
   - a click on the backdrop (outside the modal box) closes the dialog. A drag that starts in the box
     and ends outside it does not close it.
   The script listens on the document, so a dialog or a button that a page adds later works with no extra call.
   From code: EisModal.open(idOrElement) and EisModal.close(idOrElement). Listen to the native "close"
   event of the dialog to act after it closes (Esc, x, backdrop or code).
   Load it at the end of <body>:
     <script src="<src>/shared/js/modal.js"></script> */
(function () {
  "use strict";
  function find(target) {
    var el = typeof target === "string" ? document.getElementById(target) : target;
    return el && el.tagName === "DIALOG" ? el : null;
  }
  function open(target) {
    var dialog = find(target);
    if (dialog && !dialog.open) dialog.showModal();
    return dialog;
  }
  function close(target) {
    var dialog = find(target);
    if (dialog && dialog.open) dialog.close();
    return dialog;
  }
  var down = null;
  document.addEventListener("pointerdown", function (e) { down = e.target; });
  document.addEventListener("click", function (e) {
    var t = e.target;
    var opener = t.closest && t.closest("[data-eis-modal-open]");
    if (opener) { e.preventDefault(); open(opener.getAttribute("data-eis-modal-open")); return; }
    var closer = t.closest && t.closest("[data-eis-modal-close]");
    if (closer) { close(closer.closest("dialog")); return; }
    // the dialog box has no padding: a click whose target is the dialog itself lands on the backdrop
    if (t.tagName === "DIALOG" && t.open && t.classList.contains("eis-modal") && down === t) close(t);
  });
  window.EisModal = { open: open, close: close };
})();
