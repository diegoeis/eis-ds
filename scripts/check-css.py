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

Generated tokens.css files are skipped. Exit 1 if anything fails.
"""
from __future__ import annotations

import re
import sys
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
        failed |= report(path.relative_to(ROOT), check_page(path, defined))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
