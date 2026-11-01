/* eis-ds · shared/js/icons.js
   Draws the content icons. Each icon is an <i data-lucide="name" class="eis-icon"></i>.
   Lucide (https://lucide.dev, ISC licence) replaces it with an inline <svg> and keeps the class.
   Load Lucide first, then this file, at the end of <body>:
     <script src="https://unpkg.com/lucide@1.66.0/dist/umd/lucide.min.js"></script>
     <script src="<src>/shared/js/icons.js"></script>
   Lucide draws only the <i> that are on the page when it runs. The script draws the icons on
   load and again every time the page adds new ones (HTML written with JavaScript from a data
   file), so such a page needs no extra call. Lucide sets aria-hidden and keeps the class.
   Without Lucide (offline) the <i> stays empty and the button keeps its text or its aria-label.
   Icons that belong to an element (disclosure marker, done check, sidebar arrow) are not here:
   the CSS draws them from shared/css/icons.css. */
(function () {
  "use strict";
  if (!window.lucide || !window.lucide.createIcons) return;
  var queued = false;
  function draw() {
    queued = false;
    window.lucide.createIcons();
  }
  function queue() { if (!queued) { queued = true; requestAnimationFrame(draw); } }
  draw();
  new MutationObserver(function (list) {
    for (var i = 0; i < list.length; i++) {
      var added = list[i].addedNodes;
      for (var j = 0; j < added.length; j++) {
        var n = added[j];
        if (n.nodeType === 1 && (n.matches("i[data-lucide]") || n.querySelector("i[data-lucide]"))) { queue(); return; }
      }
    }
  }).observe(document.body, { childList: true, subtree: true });
})();
