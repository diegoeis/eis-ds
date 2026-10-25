#!/usr/bin/env python3
"""Check that src/css/site.css stays isolated from elements and applications.

Every selector in site.css must start with `.eis-site-`. A site rule then cannot
restyle bare HTML, a core element (.eis-button, .eis-panel...) or an application
layout. Exit 1 on the first file with violations.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "src" / "css" / "site.css"


def selectors(css: str) -> list[str]:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    found = []
    for raw in re.findall(r"([^{}]+)\{", css):
        sel = raw.strip()
        if sel.startswith("@"):
            continue
        found += [s.strip() for s in sel.split(",")]
    return found


def main() -> int:
    bad = [s for s in selectors(SITE.read_text()) if not s.startswith(".eis-site-")]
    if bad:
        print(f"{SITE.relative_to(ROOT)}: {len(bad)} selector(s) outside .eis-site-:")
        for s in bad:
            print("  ", s)
        return 1
    print(f"{SITE.relative_to(ROOT)}: all selectors scoped to .eis-site-")
    return 0


if __name__ == "__main__":
    sys.exit(main())
