/* eis-ds · app/js/sidebar.js
   Collapses and expands the app sidebar on wide screens (above 1024px).
   Collapsed, the sidebar shows only its toggle. The choice stays for the next visit (localStorage).

   Use: put the toggle last in the sidebar footer and load this script at the end of <body>:
     <aside class="eis-app-sidebar" id="sidebar" aria-label="Sidebar">
       …nav…
       <footer class="eis-app-sidebar__foot">
         <button class="eis-app-sidebar__toggle" type="button" aria-controls="sidebar"
                 aria-expanded="true" aria-label="Sidebar" data-eis-app-sidebar-toggle></button>
       </footer>
     </aside>
     <script src="src/app/js/sidebar.js"></script>

   Option: data-key on the button sets the storage key (default "eis-app-sidebar").

   Also opens and closes the nav items that hold a sub-list, and keeps each one's state for the
   next visit (key "eis-app-nav:" + the sub-list id):
     <li><button class="eis-app-nav__toggle" type="button" aria-expanded="true" aria-controls="nav-x"
                 data-eis-app-nav-toggle>Item</button>
       <ul class="eis-app-nav__sub" id="nav-x">…</ul></li> */
(function () {
  "use strict";
  function store(k, v) {
    try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; }
  }
  /* nav items with a sub-list: delegated, so a page may draw the list after this script runs */
  document.querySelectorAll("[data-eis-app-nav-toggle]").forEach(function (b) {
    var saved = store("eis-app-nav:" + b.getAttribute("aria-controls"));
    if (saved) b.setAttribute("aria-expanded", saved === "open" ? "true" : "false");
  });
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-eis-app-nav-toggle]");
    if (!b) return;
    var open = b.getAttribute("aria-expanded") !== "true";
    b.setAttribute("aria-expanded", open ? "true" : "false");
    store("eis-app-nav:" + b.getAttribute("aria-controls"), open ? "open" : "closed");
  });

  var button = document.querySelector("[data-eis-app-sidebar-toggle]");
  if (!button) return;
  var shell = document.querySelector(".eis-app-shell");
  var key = button.dataset.key || "eis-app-sidebar";

  function read() {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function save(value) {
    try { localStorage.setItem(key, value); } catch (e) { /* storage off: the choice lasts for this page only */ }
  }
  function set(open) {
    button.setAttribute("aria-expanded", open ? "true" : "false");
  }

  set(read() !== "collapsed");
  button.addEventListener("click", function () {
    var open = button.getAttribute("aria-expanded") !== "true";
    set(open);
    save(open ? "open" : "collapsed");
  });
  /* animate only after the first paint, so a collapsed page does not animate on load */
  if (shell) requestAnimationFrame(function () {
    requestAnimationFrame(function () { shell.setAttribute("data-eis-app-animate", ""); });
  });
})();
