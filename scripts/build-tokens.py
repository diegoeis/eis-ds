#!/usr/bin/env python3
"""Validate the DTCG tokens and generate site/css/tokens.css.

Stdlib only. Run from anywhere:

    python3 scripts/build-tokens.py           # validate + write css/tokens.css
    python3 scripts/build-tokens.py --check   # validate only, exit 1 on errors

Reads tokens/eis-ds.resolver.json, merges the sets in resolutionOrder, checks every
rule in docs/tokens.md section 10 that a machine can check, then writes one CSS custom
property per token (aliases stay live as var()) plus an .eis-type-<name> class per
typography token.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKENS = ROOT / "site" / "tokens"
OUT = ROOT / "site" / "css" / "tokens.css"

TYPES = {"color", "dimension", "fontFamily", "fontWeight", "number", "duration",
         "cubicBezier", "typography", "border", "shadow", "strokeStyle", "gradient", "transition"}
WEIGHT_ALIASES = {"thin": 100, "hairline": 100, "extra-light": 200, "ultra-light": 200, "light": 300,
                  "normal": 400, "regular": 400, "book": 400, "medium": 500, "semi-bold": 600,
                  "demi-bold": 600, "bold": 700, "extra-bold": 800, "ultra-bold": 800, "black": 900,
                  "heavy": 900, "extra-black": 950, "ultra-black": 950}
GENERIC_FAMILIES = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui",
                    "ui-monospace", "ui-sans-serif", "ui-serif"}
NAME_OK = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REF = re.compile(r"^\{([^{}]+)\}$")

errors: list[str] = []


def deep_merge(a: dict, b: dict) -> dict:
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(a.get(k), dict) and "$value" not in v:
            deep_merge(a[k], v)
        else:
            a[k] = v
    return a


def load_tree() -> dict:
    resolver = json.loads((TOKENS / "eis-ds.resolver.json").read_text())
    tree: dict = {}
    for entry in resolver["resolutionOrder"]:
        ref = entry["$ref"]
        if not ref.startswith("#/sets/"):
            errors.append(f"resolver: unsupported reference {ref}")
            continue
        for src in resolver["sets"][ref.split("/")[-1]]["sources"]:
            deep_merge(tree, json.loads((TOKENS / src["$ref"]).read_text()))
    return tree


def walk(node: dict, path: list[str], inherited: str | None, out: dict) -> None:
    gtype = node.get("$type", inherited)
    for key, child in node.items():
        if key.startswith("$") and key != "$root":
            continue
        where = ".".join(path + [key])
        if key != "$root" and not NAME_OK.match(key):
            errors.append(f"{where}: name must be lowercase kebab-case without {{ }} . $")
        if not isinstance(child, dict):
            errors.append(f"{where}: expected an object")
            continue
        if "$value" in child:
            t = child.get("$type", gtype)
            out[".".join(path + [key])] = {"type": t, "value": child["$value"],
                                           "desc": child.get("$description")}
        else:
            walk(child, path + [key], gtype, out)


def resolve_type(name: str, tokens: dict, seen=()) -> str | None:
    tok = tokens[name]
    if tok["type"]:
        return tok["type"]
    m = REF.match(tok["value"]) if isinstance(tok["value"], str) else None
    if m and m.group(1) in tokens and m.group(1) not in seen:
        return resolve_type(m.group(1), tokens, seen + (name,))
    return None


def check_ref(where: str, ref: str, tokens: dict) -> None:
    target = ref[1:-1]
    if target not in tokens:
        errors.append(f"{where}: reference {ref} does not resolve to a token")
        return
    chain, cur = [where], target
    while True:
        v = tokens[cur]["value"]
        m = REF.match(v) if isinstance(v, str) else None
        if not m:
            return
        if cur in chain:
            errors.append(f"{where}: circular reference {' -> '.join(chain + [cur])}")
            return
        chain.append(cur)
        cur = m.group(1)
        if cur not in tokens:
            return


def validate(tokens: dict) -> None:
    for name, tok in tokens.items():
        t = resolve_type(name, tokens)
        tok["type"] = t
        if t not in TYPES:
            errors.append(f"{name}: missing or unknown $type ({t})")
            continue
        if not tok["desc"]:
            errors.append(f"{name}: $description is required")
        v = tok["value"]
        if isinstance(v, str) and REF.match(v):
            check_ref(name, v, tokens)
            continue
        if t == "color":
            if v.get("colorSpace") != "srgb":
                errors.append(f"{name}: colorSpace must be srgb")
            h = v.get("hex", "")
            if not re.match(r"^#[0-9a-f]{6}$", h):
                errors.append(f"{name}: hex must be 6-digit lowercase")
            else:
                want = [round(int(h[i:i + 2], 16) / 255, 3) for i in (1, 3, 5)]
                if any(abs(a - b) > 0.002 for a, b in zip(want, v.get("components", []))):
                    errors.append(f"{name}: components {v.get('components')} disagree with hex {h}")
        elif t == "dimension":
            if v.get("unit") not in ("px", "rem"):
                errors.append(f"{name}: dimension unit must be px or rem")
        elif t == "fontWeight":
            if not (isinstance(v, (int, float)) and 1 <= v <= 1000) and v not in WEIGHT_ALIASES:
                errors.append(f"{name}: invalid fontWeight {v}")
        elif t == "typography":
            for k in ("fontFamily", "fontSize", "fontWeight", "letterSpacing", "lineHeight"):
                if k not in v:
                    errors.append(f"{name}: typography missing {k}")
                elif isinstance(v[k], str) and REF.match(v[k]):
                    check_ref(f"{name}.{k}", v[k], tokens)


def var_name(path: str) -> str:
    return "--" + "-".join(p for p in path.split(".") if p != "$root")


def css_value(v, t: str) -> str:
    if isinstance(v, str) and REF.match(v):
        return f"var({var_name(v[1:-1])})"
    if t == "color":
        a = v.get("alpha", 1)
        if a < 1:
            r, g, b = (round(c * 255) for c in v["components"])
            return f"rgb({r} {g} {b} / {a})"
        return v["hex"]
    if t == "dimension":
        n = v["value"]
        return f"{n:g}{v['unit']}" if n else "0"
    if t == "fontFamily":
        names = v if isinstance(v, list) else [v]
        return ", ".join(n if n in GENERIC_FAMILIES else f'"{n}"' for n in names)
    if t == "fontWeight":
        return str(WEIGHT_ALIASES.get(v, v))
    if t == "number":
        return f"{v:g}"
    raise ValueError(f"no CSS conversion for {t}")


TYPO_PROPS = [("fontFamily", "font-family", "fontFamily"), ("fontSize", "font-size", "dimension"),
              ("fontWeight", "font-weight", "fontWeight"), ("letterSpacing", "letter-spacing", "dimension"),
              ("lineHeight", "line-height", "number")]


def build_css(tokens: dict) -> str:
    lines = ["/* GENERATED by scripts/build-tokens.py from site/tokens/*.tokens.json. Do not edit. */", "",
             ":root {"]
    classes = []
    group = None
    for name, tok in tokens.items():
        top = name.split(".")[0]
        if top != group:
            lines.append(f"\n  /* {top} */")
            group = top
        if tok["type"] == "typography" and isinstance(tok["value"], dict):
            base = var_name(name)
            decl = []
            for key, prop, sub in TYPO_PROPS:
                lines.append(f"  {base}-{prop}: {css_value(tok['value'][key], sub)};")
                decl.append(f"  {prop}: var({base}-{prop});")
            classes.append(f".eis-{base[2:]} {{\n" + "\n".join(decl) +
                           ("\n  text-transform: uppercase;" if name.endswith("label") else "") + "\n}")
            continue
        lines.append(f"  {var_name(name)}: {css_value(tok['value'], tok['type'])};")
    lines.append("}\n")
    return "\n".join(lines) + "\n/* text styles */\n" + "\n\n".join(classes) + "\n"


def main() -> int:
    tree = load_tree()
    tokens: dict = {}
    walk(tree, [], None, tokens)
    validate(tokens)
    if errors:
        print("\n".join(f"ERROR {e}" for e in errors))
        return 1
    print(f"{len(tokens)} tokens valid")
    if "--check" in sys.argv:
        return 0
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(build_css(tokens))
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
