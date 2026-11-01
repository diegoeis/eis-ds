#!/usr/bin/env python3
"""Keep llms.txt and llms-full.txt in sync with the manual.

llms.txt (repository root) follows the llms.txt format: H1, blockquote, context,
then H2 sections with link lists. You write it by hand, except one block: the list
after the line "Rules that have no exceptions:". The script copies that list from the
section "Rules with no exceptions" of docs/manual/AGENTS.md.

The script checks that every eis-ds URL in llms.txt points to a file in this
repository, and that every file in docs/manual/ has a link in llms.txt (CLAUDE.md only
points to AGENTS.md, so it needs no link).

Then it writes llms-full.txt with the same structure as llms.txt:

- It copies the H1, the blockquote and the context as they are.
- In every H2 section except "Optional", each link to a local Markdown file becomes
  an H3 with the link text, a source line and the full content of the file. The
  headings of the file go down three levels (# becomes ####), outside code blocks.
  Relative links in the file become absolute URLs.
- The "Optional" section stays a list of links.

Usage:
  python3 scripts/build-llms.py           write llms.txt (rules block) and llms-full.txt
  python3 scripts/build-llms.py --check   exit 1 if one of the two files is not up to date

Standard library only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "llms.txt"
TARGET = ROOT / "llms-full.txt"
MANUAL = ROOT / "docs" / "manual"
BASE = "https://diegoeis.github.io/eis-ds/"

LINK_ITEM = re.compile(r"^- \[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)(?::\s*(?P<desc>.*))?$")
HEADING = re.compile(r"^(#{1,6})(\s)")
FENCE = re.compile(r"^\s*(```|~~~)")
REL_LINK = re.compile(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)")
SITE_URL = re.compile(re.escape(BASE) + r"[^\s)`>\]]+")
RULES_LEAD = "Rules that have no exceptions:"
RULES_HEADING = "## Rules with no exceptions"


def local_path(url: str) -> Path | None:
    if not url.startswith(BASE):
        return None
    return ROOT / url[len(BASE):]


def demote(text: str, url: str, levels: int = 3) -> str:
    folder = url.rsplit("/", 1)[0] + "/"
    out, in_code = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            in_code = not in_code
        elif not in_code:
            line = HEADING.sub(lambda m: "#" * min(6, len(m.group(1)) + levels) + m.group(2), line)
            line = REL_LINK.sub(lambda m: f"]({folder}{m.group(1)})", line)
        out.append(line)
    return "\n".join(out).strip()


def manual_rules() -> list[str]:
    lines = (MANUAL / "AGENTS.md").read_text(encoding="utf-8").splitlines()
    if RULES_HEADING not in lines:
        raise SystemExit(f"docs/manual/AGENTS.md has no section '{RULES_HEADING}'")
    rules = []
    for line in lines[lines.index(RULES_HEADING) + 1:]:
        if line.startswith("## "):
            break
        if line.startswith("- "):
            rules.append(line)
    if not rules:
        raise SystemExit(f"the section '{RULES_HEADING}' in docs/manual/AGENTS.md has no list")
    return rules


def sync_rules(text: str) -> str:
    lines = text.splitlines()
    if RULES_LEAD not in lines:
        raise SystemExit(f"llms.txt has no line '{RULES_LEAD}'")
    start = lines.index(RULES_LEAD) + 1
    end = start
    while end < len(lines) and not lines[end].startswith("## "):
        end += 1
    return "\n".join(lines[:start] + [""] + manual_rules() + [""] + lines[end:]) + "\n"


def check_urls(text: str) -> list[str]:
    errors = []
    for url in sorted(set(SITE_URL.findall(text))):
        path = local_path(url.rstrip(".,:;"))
        if path is not None and "<" not in url and not path.exists():
            errors.append(f"llms.txt links a missing file: {url}")
    return errors


def build_full(source: str) -> str:
    lines = source.splitlines()
    first = next((i for i, l in enumerate(lines) if l.startswith("## ")), len(lines))
    out = ["\n".join(lines[:first]).rstrip()]
    linked: set[Path] = set()
    errors = check_urls(source)

    section = None
    for line in lines[first:]:
        if line.startswith("## "):
            section = line[3:].strip()
            out.append(f"\n{line}")
            continue
        m = LINK_ITEM.match(line.strip())
        if not m:
            if line.strip():
                out.append(line)
            continue
        path = local_path(m["url"])
        if path is not None and not path.exists():
            continue
        if section == "Optional" or path is None or path.suffix != ".md":
            if out[-1].lstrip().startswith("## "):
                out.append("")
            out.append(line)
            continue
        linked.add(path.resolve())
        body = demote(path.read_text(encoding="utf-8"), m["url"])
        out.append(f"\n### {m['title']}\n\nSource: {m['url']}\n\n{body}\n\n---")

    for md in sorted(MANUAL.glob("*.md")):
        if md.name != "CLAUDE.md" and md.resolve() not in linked:
            errors.append(f"llms.txt has no link to {md.relative_to(ROOT)}")
    if errors:
        raise SystemExit("\n".join(errors))
    return "\n".join(out).rstrip("-\n ") + "\n"


def main() -> int:
    source = sync_rules(SOURCE.read_text(encoding="utf-8"))
    outputs = {SOURCE: source, TARGET: build_full(source)}
    if "--check" in sys.argv[1:]:
        stale = [p.name for p, text in outputs.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != text]
        if stale:
            print(f"not up to date: {', '.join(stale)}. Run: python3 scripts/build-llms.py")
            return 1
        print("llms.txt and llms-full.txt are up to date.")
        return 0
    for path, text in outputs.items():
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)}")
    print("llms.txt and llms-full.txt are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
