#!/usr/bin/env python3
"""Validate the DTCG tokens of every scope and generate src/<scope>/css/tokens.css.

Stdlib only. Run from anywhere:

    python3 scripts/build-tokens.py           # validate + write every tokens.css
    python3 scripts/build-tokens.py --check   # validate only, exit 1 on errors

Scopes: shared, then each folder in src/ that has tokens/<scope>.resolver.json.
For each scope: merge the sets in resolutionOrder, check every rule in docs/tokens.md
section 10 that a machine can check, then write one CSS custom property per token
(aliases stay live as var()) plus an .eis-<name> class per typography token.

Scope rules:
- shared tokens never reference another scope, and no shared group is named after a scope.
- every token of scope X lives under the group X (so its variables start with --X-).
- scope X may reference shared and X only. Its tokens.css holds only X tokens, so it
  must be loaded after shared/css/tokens.css.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

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


def load_tree(scope: str) -> dict:
    tokens_dir = SRC / scope / "tokens"
    resolver = json.loads((tokens_dir / f"{scope}.resolver.json").read_text())
    tree: dict = {}
    for entry in resolver["resolutionOrder"]:
        ref = entry["$ref"]
        if not ref.startswith("#/sets/"):
            errors.append(f"resolver: unsupported reference {ref}")
            continue
        for src in resolver["sets"][ref.split("/")[-1]]["sources"]:
            deep_merge(tree, json.loads((tokens_dir / src["$ref"]).read_text()))
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


def validate(tokens: dict, only: set | None = None) -> None:
    for name, tok in tokens.items():
        if only is not None and name not in only:
            continue
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


def build_css(tokens: dict, scope: str) -> str:
    lines = [f"/* GENERATED by scripts/build-tokens.py from src/{scope}/tokens/*.tokens.json. Do not edit. */",
             *([] if scope == "shared" else [f"/* Load after src/shared/css/tokens.css. */"]), "", ":root {"]
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
    return "\n".join(lines) + ("\n/* text styles */\n" + "\n\n".join(classes) + "\n" if classes else "")


def scopes() -> list[str]:
    others = sorted(p.name for p in SRC.iterdir()
                    if p.name != "shared" and (p / "tokens" / f"{p.name}.resolver.json").exists())
    return ["shared"] + others


def main() -> int:
    names = scopes()
    shared: dict = {}
    walk(load_tree("shared"), [], None, shared)
    for n in shared:
        if n.split(".")[0] in names[1:]:
            errors.append(f"shared/{n}: shared groups must not be named after a scope")
    validate(shared)
    built = {"shared": shared}
    for scope in names[1:]:
        own: dict = {}
        walk(load_tree(scope), [], None, own)
        for n, tok in own.items():
            if n.split(".")[0] != scope:
                errors.append(f"{scope}/{n}: every {scope} token must live under the group '{scope}'")
            refs = re.findall(r"\{([^{}]+)\}", json.dumps(tok["value"]))
            for r in refs:
                if r.split(".")[0] in names[1:] and r.split(".")[0] != scope:
                    errors.append(f"{scope}/{n}: references {{{r}}} from another scope")
        merged = {**shared, **own}
        validate(merged, set(own))
        built[scope] = own
    if errors:
        print("\n".join(f"ERROR {e}" for e in errors))
        return 1
    for scope, toks in built.items():
        print(f"{scope}: {len(toks)} tokens valid")
    if "--check" in sys.argv:
        return 0
    for scope, toks in built.items():
        out = SRC / scope / "css" / "tokens.css"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build_css(toks, scope))
        print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
