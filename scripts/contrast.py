#!/usr/bin/env python3
"""WCAG 2.x contrast checker for foreground/background pairs.

Measures; does not guess. Accepts sRGB hex (#rgb, #rgba, #rrggbb, #rrggbbaa),
rgb()/rgba(), and oklch(L C H [/ A]). Translucent foregrounds are composited
over the background before measuring. Background colors must be opaque
(composite them over their own underlying surface first, with --over).

Usage:
  contrast.py FG BG                        one pair
  contrast.py --link LINK TEXT BG          inline-link three-way check
  contrast.py --file pairs.txt             one pair per line: name, fg, bg
  contrast.py --over BASE COLOR            print COLOR composited over BASE
  add --json for machine-readable output

Ratios are printed truncated (never rounded up) to two decimals; pass/fail
uses the unrounded value.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys

# --- parsing ---------------------------------------------------------------

def _hex(s: str):
    h = s.lstrip("#")
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h)
    if len(h) not in (6, 8) or not re.fullmatch(r"[0-9a-fA-F]+", h):
        raise ValueError(f"bad hex color: {s}")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
    return (r, g, b), a, False


def _num(tok: str, scale: float) -> float:
    tok = tok.strip()
    if tok.endswith("%"):
        return float(tok[:-1]) / 100 * scale
    return float(tok)


def _split_fn(s: str):
    inner = s[s.index("(") + 1:s.rindex(")")]
    alpha = None
    if "/" in inner:
        inner, alpha = inner.split("/", 1)
    parts = [p for p in re.split(r"[\s,]+", inner.strip()) if p]
    return parts, alpha


def _rgb(s: str):
    parts, alpha = _split_fn(s)
    if len(parts) == 4 and alpha is None:  # legacy rgba(r, g, b, a)
        alpha = parts.pop()
    if len(parts) != 3:
        raise ValueError(f"bad rgb color: {s}")
    r, g, b = (_num(p, 255) / 255 for p in parts)
    a = _num(alpha, 1) if alpha is not None else 1.0
    return (r, g, b), a, False


def _oklch(s: str):
    parts, alpha = _split_fn(s)
    if len(parts) != 3:
        raise ValueError(f"bad oklch color: {s}")
    L = _num(parts[0], 1)
    C = _num(parts[1], 0.4)
    H = float(parts[2].replace("deg", ""))
    a_ = C * math.cos(math.radians(H))
    b_ = C * math.sin(math.radians(H))
    l_ = (L + 0.3963377774 * a_ + 0.2158037573 * b_) ** 3
    m_ = (L - 0.1055613458 * a_ - 0.0638541728 * b_) ** 3
    s_ = (L - 0.0894841775 * a_ - 1.2914855480 * b_) ** 3
    lin = (
        4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
        -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
        -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_,
    )
    eps = 1e-3  # tolerate rounding in published oklch values
    out_of_gamut = any(c < -eps or c > 1 + eps for c in lin)
    enc = tuple(_encode(min(1.0, max(0.0, c))) for c in lin)
    a = _num(alpha, 1) if alpha is not None else 1.0
    return enc, a, out_of_gamut


def parse(s: str):
    s = s.strip()
    low = s.lower()
    if low.startswith("#") or re.fullmatch(r"[0-9a-f]{3,8}", low):
        return _hex(s)
    if low.startswith("rgb"):
        return _rgb(low)
    if low.startswith("oklch"):
        return _oklch(low)
    raise ValueError(f"unsupported color (use hex, rgb(), or oklch()): {s}")

# --- color math ------------------------------------------------------------

def _linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _encode(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def luminance(rgb) -> float:
    r, g, b = (_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def composite(fg, alpha, bg):
    # Browsers composite in gamma-encoded sRGB by default.
    return tuple(f * alpha + b * (1 - alpha) for f, b in zip(fg, bg))


def ratio(a, b) -> float:
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def to_hex(rgb) -> str:
    return "#" + "".join(f"{round(c * 255):02x}" for c in rgb)


def trunc2(x: float) -> str:
    return f"{math.floor(x * 100) / 100:.2f}"

# --- checks ----------------------------------------------------------------

THRESHOLDS = {
    "AA_text": 4.5,
    "AA_large": 3.0,
    "AAA_text": 7.0,
    "AAA_large": 4.5,
    "non_text": 3.0,
}


def resolve(fg_s: str, bg_s: str):
    fg, fa, fg_oog = parse(fg_s)
    bg, ba, bg_oog = parse(bg_s)
    if ba < 1:
        raise ValueError(
            f"background {bg_s} is translucent; composite it over its "
            "underlying surface first (--over BASE COLOR)")
    warnings = []
    if fg_oog:
        warnings.append(f"{fg_s} is outside sRGB; clipped (browsers may gamut-map differently)")
    if bg_oog:
        warnings.append(f"{bg_s} is outside sRGB; clipped (browsers may gamut-map differently)")
    if fa < 1:
        fg = composite(fg, fa, bg)
    return fg, bg, warnings


def check_pair(name: str, fg_s: str, bg_s: str) -> dict:
    fg, bg, warnings = resolve(fg_s, bg_s)
    r = ratio(fg, bg)
    return {
        "name": name,
        "fg": fg_s,
        "bg": bg_s,
        "fg_resolved": to_hex(fg),
        "bg_resolved": to_hex(bg),
        "ratio": r,
        "ratio_display": trunc2(r),
        "pass": {k: r >= v for k, v in THRESHOLDS.items()},
        "warnings": warnings,
    }


def check_link(link_s: str, text_s: str, bg_s: str) -> dict:
    link_bg = check_pair("link vs background", link_s, bg_s)
    text_bg = check_pair("body text vs background", text_s, bg_s)
    link_fg, _, _ = resolve(link_s, bg_s)
    text_fg, _, _ = resolve(text_s, bg_s)
    lt = ratio(link_fg, text_fg)
    ok = link_bg["pass"]["AA_text"] and text_bg["pass"]["AA_text"] and lt >= 3.0
    return {
        "link_vs_bg": link_bg,
        "text_vs_bg": text_bg,
        "link_vs_text": {"ratio": lt, "ratio_display": trunc2(lt), "pass": lt >= 3.0},
        "color_only_links_allowed": ok,
        "note": ("Even when this passes, links distinguished by color alone also need "
                 "a non-color cue (e.g. underline) on hover and keyboard focus. "
                 "A persistent underline avoids the three-way constraint."),
    }

# --- output ----------------------------------------------------------------

def fmt_pass(p: dict) -> str:
    mark = lambda b: "pass" if b else "FAIL"
    return (f"AA text {mark(p['AA_text'])} | AA large/non-text {mark(p['AA_large'])} | "
            f"AAA text {mark(p['AAA_text'])} | AAA large {mark(p['AAA_large'])}")


def print_pair(res: dict) -> None:
    label = f"{res['name']}: " if res["name"] else ""
    print(f"{label}{res['fg']} on {res['bg']}  ->  {res['ratio_display']}:1")
    if not (res["fg"].startswith("#") and len(res["fg"]) in (4, 7)):
        print(f"    resolved fg {res['fg_resolved']} on {res['bg_resolved']}")
    print(f"    {fmt_pass(res['pass'])}")
    for w in res["warnings"]:
        print(f"    warning: {w}")


def read_pairs(path: str):
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("//"):  # '//' comments ('#' is hex)
                continue
            sep = ";" if ";" in line else "\t" if "\t" in line else ","
            parts = [p.strip() for p in line.split(sep)]
            if len(parts) == 2:
                parts = [f"line {n}"] + parts
            if len(parts) != 3:
                raise ValueError(f"{path}:{n}: expected 'name, fg, bg' (use ';' or tabs "
                                 f"as separators when colors contain commas)")
            yield parts


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("colors", nargs="*", help="FG BG")
    ap.add_argument("--link", nargs=3, metavar=("LINK", "TEXT", "BG"))
    ap.add_argument("--file", help="pairs file: name, fg, bg per line")
    ap.add_argument("--over", nargs=2, metavar=("BASE", "COLOR"),
                    help="composite COLOR over opaque BASE and print hex")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    try:
        if a.over:
            base, ba, _ = parse(a.over[0])
            col, ca, _ = parse(a.over[1])
            if ba < 1:
                raise ValueError("BASE must be opaque")
            out = to_hex(composite(col, ca, base))
            print(json.dumps({"resolved": out}) if a.json else out)
            return 0
        if a.link:
            res = check_link(*a.link)
            if a.json:
                print(json.dumps(res, indent=2))
            else:
                print_pair(res["link_vs_bg"])
                print_pair(res["text_vs_bg"])
                lt = res["link_vs_text"]
                print(f"link vs body text  ->  {lt['ratio_display']}:1  "
                      f"({'pass' if lt['pass'] else 'FAIL'} >= 3:1)")
                print(f"color-only links allowed: {res['color_only_links_allowed']}")
                print(f"    {res['note']}")
            return 0 if res["color_only_links_allowed"] else 1
        if a.file:
            results = [check_pair(*p) for p in read_pairs(a.file)]
        elif len(a.colors) == 2:
            results = [check_pair("", *a.colors)]
        else:
            ap.print_usage(sys.stderr)
            return 2
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if a.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print_pair(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
