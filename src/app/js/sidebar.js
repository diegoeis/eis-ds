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

   Below 1024px the sidebar is a drawer. A top bar, first in <body>, holds the menu button and the page name:
     <header class="eis-app-topbar">
       <button class="eis-button eis-button--ghost eis-button--icon" type="button" aria-controls="sidebar"
               aria-expanded="false" aria-label="Menu" title="Menu" data-eis-app-drawer-toggle>
         <i data-lucide="menu" class="eis-icon"></i></button>
       <p class="eis-app-topbar__title">Page name</p>
     </header>
   The button opens the sidebar over the content. Esc, a click outside the sidebar or a click on a nav item
   (a link, or a button that is not a sub-list toggle) closes it. While it is open, Tab stays inside it.
   On close the focus goes back to the button (Esc and outside click only, not after a nav item).

   Also opens and closes the nav items that hold a sub-list, and keeps each one's state for the
   next visit (key "eis-app-nav:" + the sub-list id):
     <li><button class="eis-app-nav__toggle" type="button" aria-expanded="true" aria-controls="nav-x"
                 data-eis-app-nav-toggle>Item</button>
       <ul class="eis-app-nav__sub" id="nav-x">…</ul></li> */
(function () {
  "use strict";
  /* the drawer below 1024px: the menu button in eis-app-topbar opens the sidebar */
  function drawer() {
    var toggle = document.querySelector("[data-eis-app-drawer-toggle]");
    if (!toggle) return;
    var panel = document.getElementById(toggle.getAttribute("aria-controls"));
    if (!panel) return;
    var narrow = window.matchMedia("(max-width:1024px)");
    var FOCUSABLE = "a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex='-1'])";
    function isOpen() { return toggle.getAttribute("aria-expanded") === "true"; }
    function items() {
      return Array.prototype.filter.call(panel.querySelectorAll(FOCUSABLE), function (el) { return el.getClientRects().length > 0; });
    }
    function open() {
      toggle.setAttribute("aria-expanded", "true");
      var first = panel.querySelector("[aria-current='page']") || items()[0];
      if (first) first.focus();
    }
    function close(refocus) {
      if (!isOpen()) return;
      toggle.setAttribute("aria-expanded", "false");
      if (refocus) toggle.focus();
    }
    toggle.setAttribute("aria-expanded", "false");
    toggle.addEventListener("click", function () { if (isOpen()) close(true); else open(); });
    document.addEventListener("keydown", function (e) {
      if (!isOpen()) return;
      if (e.key === "Escape") { e.preventDefault(); close(true); return; }
      if (e.key !== "Tab") return;
      var list = items();
      if (!list.length) return;
      var first = list[0], last = list[list.length - 1];
      if (!panel.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
      else if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    document.addEventListener("click", function (e) {
      if (!isOpen() || toggle.contains(e.target)) return;
      if (!panel.contains(e.target)) { close(true); return; }
      var item = e.target.closest("a[href],button");
      if (item && item.closest(".eis-app-nav") && !item.hasAttribute("data-eis-app-nav-toggle")) close(false);
    });
    /* back to a wide screen: the sidebar is in the page again, the drawer state goes */
    narrow.addEventListener("change", function () { if (!narrow.matches) close(false); });
  }
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

  drawer();

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
