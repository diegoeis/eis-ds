/* eis-ds · web/lines.js
   Decorative line art for web pages: horizontal bars in the signal colour that rise
   like terrain. Seeded, so a page shows the same art on every load.

   Use:
     <svg class="eis-web-lines" data-eis-web-lines data-seed="7"
          viewBox="0 0 1440 360" preserveAspectRatio="none"
          aria-hidden="true" focusable="false"></svg>
     <script src="src/web/js/lines.js" defer></script>

   Options (data attributes): data-seed (any integer, default 7),
   data-step (row height in viewBox units, default 7). */
(function () {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";

  function draw(svg) {
    var box = (svg.getAttribute("viewBox") || "0 0 1440 360").split(/\s+/).map(Number);
    var W = box[2], H = box[3];
    var seed = parseInt(svg.dataset.seed || "7", 10) || 7;
    var step = parseFloat(svg.dataset.step || "7");
    var gap = 3;
    var rnd = function () { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
    var ridge = function (x) {
      var t = x / W;
      return H * (0.95 - 0.8 * Math.pow(t, 1.4)) + 24 * Math.sin(t * 9) + 12 * Math.sin(t * 23 + 1);
    };
    var g = document.createElementNS(NS, "g");
    g.setAttribute("fill", "var(--signal)");
    for (var y = 0; y < H; y += step) {
      var x = 0;
      while (x < W) {
        var len = 20 + rnd() * 160;
        if (y > ridge(x + len / 2) && rnd() > 0.06) {
          var r = document.createElementNS(NS, "rect");
          r.setAttribute("x", x.toFixed(1));
          r.setAttribute("y", y);
          r.setAttribute("width", Math.max(4, len - gap - rnd() * 10).toFixed(1));
          r.setAttribute("height", step - gap);
          g.appendChild(r);
        }
        x += len;
      }
    }
    svg.replaceChildren(g);
  }

  function run() { document.querySelectorAll("svg[data-eis-web-lines]").forEach(draw); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
})();
