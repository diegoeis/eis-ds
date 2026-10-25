#!/usr/bin/env python3
"""Check that the CSS scopes stay independent.

Scopes are the folders in src/ that have a tokens/<scope>.resolver.json, plus shared.

- shared/css/*.css: no selector or variable from any scope (.eis-<scope>-, --<scope>-).
- <scope>/css/components.css: every selector starts with .eis-<scope>-, and it uses no
  selector or variable from another scope. So a scope cannot restyle bare HTML, a shared
  element or another scope.

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


def main() -> int:
    names = scopes()
    failed = False
    files = [(p, None) for p in sorted((SRC / "shared" / "css").glob("*.css")) if p.name != "tokens.css"]
    files += [(SRC / s / "css" / "components.css", s) for s in names if (SRC / s / "css" / "components.css").exists()]
    for path, own in files:
        bad = check(path, own, names)
        rel = path.relative_to(ROOT)
        if bad:
            failed = True
            print(f"FAIL {rel}")
            for b in bad:
                print("   ", b)
        else:
            print(f"ok   {rel}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
