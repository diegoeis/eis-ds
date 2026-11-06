#!/usr/bin/env python3
"""Check that the CSS scopes stay independent.

Scopes are the folders in src/ that have a tokens/<scope>.resolver.json, plus shared.

- shared/css/*.css: no selector or variable from any scope (.eis-<scope>-, --<scope>-).
- <scope>/css/components.css: every selector starts with .eis-<scope>-, and it uses no
  selector or variable from another scope. So a scope cannot restyle bare HTML, a shared
  element or another scope.
- index.html and site/**/*.html: every eis-* class in a class attribute or in a page
  <style> selector exists in src/**/*.css. A page frame class uses the doc- prefix.
  Script blocks are skipped, so class strings that JS builds are not checked.
- The same pages: every .eis-panel holds only its parts (head first, body, footer last)
  or a panel part (PANEL_CONTENT). No eis-panel__body inside another one. A panel that is
  a list (ul/ol, eis-list), an eis-form or a doc- frame holds rows or fields instead.

Generated tokens.css files are skipped. Exit 1 if anything fails.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"


def scopes() -> list[str]:
    return sorted(p.name for p in SRC.iterdir()
                  if p.name != "shared" and (p / "tokens" / f"{p.name}.resolver.json").exists())


def selectors(css: str) -> list[str]:
    found = []
    for raw in re.findall(r"([^{}]+)\{", css):
        sel = raw.strip()
        if not sel.startswith("@"):
            found += [s.strip() for s in sel.split(",")]
    return found


def check(path: Path, own: str | None, all_scopes: list[str]) -> list[str]:
    css = re.sub(r"/\*.*?\*/", "", path.read_text(), flags=re.S)
    bad = []
    for s in (x for x in all_scopes if x != own):
        if re.search(rf"\.eis-{s}-", css):
            bad.append(f"uses classes of scope '{s}' (.eis-{s}-)")
        if re.search(rf"var\(--{s}-", css):
            bad.append(f"uses variables of scope '{s}' (--{s}-)")
    if own:
        bad += [f"selector outside .eis-{own}-: {s}" for s in selectors(css)
                if not s.startswith(f".eis-{own}-")]
    return bad


def defined_classes() -> set[str]:
    found = set()
    for path in SRC.rglob("*.css"):
        css = re.sub(r"/\*.*?\*/", "", path.read_text(), flags=re.S)
        found |= set(re.findall(r"\.(eis-[\w-]+)", css))
    return found


def check_page(path: Path, defined: set[str]) -> list[str]:
    html = re.sub(r"<!--.*?-->|<script\b[^>]*>.*?</script>", "", path.read_text(), flags=re.S | re.I)
    used = set()
    for m in re.finditer(r"\bclass\s*=\s*(?:\"([^\"]*)\"|'([^']*)')", html):
        used |= {c for c in (m.group(1) or m.group(2) or "").split() if c.startswith("eis-")}
    for style in re.findall(r"<style\b[^>]*>(.*?)</style>", html, flags=re.S | re.I):
        style = re.sub(r"/\*.*?\*/", "", style, flags=re.S)
        used |= set(re.findall(r"\.(eis-[\w-]+)", style))
    return [f"class not in src/**/*.css: {c} (a page frame class uses doc-)"
            for c in sorted(used - defined)]


# Panel structure (docs/manual/elements.md, "Panel"). The direct children of an
# .eis-panel are its parts: head, body, footer. A full-width element with its own
# padding can take the place of a body: these shared elements and the scope
# components that layout.md §7 lists as panel parts.
PANEL_PARTS = {"eis-panel__head", "eis-panel__body", "eis-panel__footer"}
PANEL_CONTENT = {
    "eis-table", "eis-list", "eis-disclosure", "eis-metrics",
    "eis-web-scroll", "eis-web-spec",
    "eis-app-agenda", "eis-app-cells", "eis-app-legend", "eis-app-bar",
    "eis-app-topics", "eis-app-people", "eis-app-done", "eis-app-add-bar",
}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "source", "track", "wbr"}


class PanelCheck(HTMLParser):
    """Walk a page and collect panel structure errors."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, set[str]]] = []
        self.kids: list[list[set[str]]] = []  # classes of each direct child, per open element
        self.skip = 0
        self.bad: list[str] = []

    def err(self, msg: str) -> None:
        self.bad.append(f"line {self.getpos()[0]}: {msg}")

    def free(self, tag: str, cls: set[str]) -> bool:
        """A panel that is itself a list, a form or a doc frame: its children are not parts."""
        return tag in ("ul", "ol") or bool(cls & {"eis-form", "eis-list"}) or any(c.startswith("doc-") for c in cls)

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in ("script", "style", "template"):
            self.skip += 1
        if self.skip:
            return
        cls = set((dict(attrs).get("class") or "").split())
        if self.stack:
            ptag, pcls = self.stack[-1]
            self.kids[-1].append(cls)
            if "eis-panel" in pcls and not self.free(ptag, pcls):
                if not cls & (PANEL_PARTS | PANEL_CONTENT) and not any(c.startswith("doc-") for c in cls):
                    name = tag + "".join("." + c for c in sorted(cls))
                    self.err(f"<{name}> in .eis-panel: a panel holds only head, body, footer "
                             "or a panel part (table, list, disclosure, metrics, scope part)")
        parent = self.stack[-1][1] if self.stack else set()
        if "eis-panel__body" in cls and any("eis-panel__body" in c for _, c in self.stack):
            self.err("eis-panel__body inside another eis-panel__body")
        if cls & {"eis-panel__body", "eis-panel__footer"} and not ({"eis-panel", "eis-disclosure"} & parent):
            self.err(f"{' '.join(sorted(cls & PANEL_PARTS))} is not a direct child of .eis-panel or .eis-disclosure")
        if "eis-panel__head" in cls and "eis-panel" not in parent:
            self.err("eis-panel__head is not a direct child of .eis-panel")
        if tag not in VOID:
            self.stack.append((tag, cls))
            self.kids.append([])

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style", "template"):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                ptag, pcls = self.stack[i]
                kids = self.kids[i]
                if "eis-panel" in pcls and not self.free(ptag, pcls):
                    heads = [k for k, c in enumerate(kids) if "eis-panel__head" in c]
                    foots = [k for k, c in enumerate(kids) if "eis-panel__footer" in c]
                    if heads and heads != [0]:
                        self.err("eis-panel__head must be the one first child of the panel")
                    if foots and foots != [len(kids) - 1]:
                        self.err("eis-panel__footer must be the one last child of the panel")
                del self.stack[i:]
                del self.kids[i:]
                break


def check_panels(path: Path) -> list[str]:
    html = re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.S)
    p = PanelCheck()
    p.feed(html)
    return p.bad


def report(rel: Path, bad: list[str]) -> bool:
    if bad:
        print(f"FAIL {rel}")
        for b in bad:
            print("   ", b)
        return True
    print(f"ok   {rel}")
    return False


def main() -> int:
    names = scopes()
    failed = False
    files = [(p, None) for p in sorted((SRC / "shared" / "css").glob("*.css")) if p.name != "tokens.css"]
    files += [(SRC / s / "css" / "components.css", s) for s in names if (SRC / s / "css" / "components.css").exists()]
    for path, own in files:
        failed |= report(path.relative_to(ROOT), check(path, own, names))
    defined = defined_classes()
    for path in [ROOT / "index.html", *sorted((ROOT / "site").rglob("*.html"))]:
        failed |= report(path.relative_to(ROOT), check_page(path, defined) + check_panels(path))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
