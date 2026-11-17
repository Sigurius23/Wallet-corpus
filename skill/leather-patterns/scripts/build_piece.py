#!/usr/bin/env python3
"""
build_piece.py — generate a cut pattern for ANY flat leather design.

No fixed list of allowed shapes. You describe a part as a JSON spec; this script
builds it, validates it, and writes SVG + DXF + 1:1 tiled PDF + report.

    python3 build_piece.py spec.json --out ./out
    python3 build_piece.py --example bifold > spec.json

Exit codes: 0 all gates pass, 1 bad input, 2 a gate failed.
"""
import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from leatherkit.shape import Shape, Panel, STANDARD_PITCHES


# ---------------------------------------------------------------- spec helpers
def _num(d, key, default=None, lo=None, hi=None):
    if key not in d:
        if default is None:
            raise ValueError(f"missing required key '{key}'")
        return default
    v = float(d[key])
    if lo is not None and v < lo:
        raise ValueError(f"'{key}' = {v} is below the minimum {lo}")
    if hi is not None and v > hi:
        raise ValueError(f"'{key}' = {v} is above the maximum {hi}")
    return v


def shape_from_spec(node):
    """Recursive: any node may be a primitive or a boolean of two nodes."""
    if isinstance(node, list):
        raise ValueError("spec node must be an object, not a list — "
                         "wrap booleans as {'op': ..., 'a': ..., 'b': ...}")
    t = node.get("type", "rect")

    if t == "rect":
        w = _num(node, "w", lo=1)
        h = _num(node, "h", lo=1)
        r = _num(node, "r", 0.0, lo=0)
        return Shape.rect(w, h, r, _num(node, "x", 0.0), _num(node, "y", 0.0))
    if t == "circle":
        return Shape.circle(_num(node, "d", lo=1), _num(node, "cx", 0.0), _num(node, "cy", 0.0))
    if t == "stadium":
        w, h = _num(node, "w", lo=1), _num(node, "h", lo=1)
        if h > w:
            raise ValueError("stadium needs w >= h")
        return Shape.stadium(w, h)
    if t == "polygon":
        pts = node.get("points")
        if not pts or len(pts) < 3:
            raise ValueError("polygon needs at least 3 points")
        return Shape.from_points(pts)
    if t == "svg_path":
        d = node.get("d")
        if not d:
            raise ValueError("svg_path needs a 'd' string")
        return Shape.from_svg_path(d, int(node.get("flat", 12)))

    if t in ("union", "difference", "intersection"):
        a = shape_from_spec(node["a"])
        b = shape_from_spec(node["b"])
        return getattr(a, t)(b)

    if t == "offset":
        return shape_from_spec(node["of"]).offset(_num(node, "d"))
    if t == "rotate":
        return shape_from_spec(node["of"]).rotate(_num(node, "deg"),
                                                  node.get("origin", "center"))
    if t == "translate":
        return shape_from_spec(node["of"]).translate(_num(node, "dx", 0.0),
                                                      _num(node, "dy", 0.0))
    if t == "mirror":
        return shape_from_spec(node["of"]).mirror_x(_num(node, "about", 0.0))
    if t == "scale":
        return shape_from_spec(node["of"]).scale(_num(node, "s", lo=0.01))
    if t == "repeat":
        """Array a child n times along a vector — strap holes, rivet runs, slots."""
        child = node["of"]
        n = int(_num(node, "n", lo=1))
        dx, dy = _num(node, "dx", 0.0), _num(node, "dy", 0.0)
        acc = None
        for i in range(n):
            g = shape_from_spec(child).translate(dx * i, dy * i)
            acc = g if acc is None else acc.union(g)
        return acc

    raise ValueError(f"unknown shape type '{t}'")


# ------------------------------------------------------------------ gates
def gates(panel, spec):
    """
    Each gate is (ok, label, detail). A gate that cannot be evaluated must FAIL
    loudly — never default to passing.
    """
    out = []
    t = panel.leather_t
    sh = panel.shape

    # 1. the panel must exist and be big enough to hold its own stitches
    try:
        out.append((sh.area > 100, "panel has real area",
                    f"{sh.area:.0f} mm2 ({sh.width:.1f} x {sh.height:.1f} mm)"))
    except Exception as e:
        out.append((False, "panel has real area", f"could not measure: {e}"))

    # 2. every stitch run must fit inside the outline
    for i, s in enumerate(panel.stitches):
        need = s["edge"]
        try:
            ok = all(sh.contains(pt) for pt in s["points"])
            detail = (f"run {i+1}: {s['count']} holes at {need} mm inside the edge"
                      if ok else f"run {i+1}: holes fall OUTSIDE the cut line")
        except Exception as e:
            ok, detail = False, f"run {i+1}: containment check failed: {e}"
        out.append((ok, f"stitch run {i+1} inside the outline", detail))

    # 2b. no stitch hole may land inside an interior cutout — it would be
    #     cut away and the seam would have a gap exactly where you need it.
    try:
        from shapely.geometry import Polygon as _Poly, Point as _Pt
        cutouts = panel.pieces()[0].cutouts if panel.pieces() else []
        if cutouts:
            bad = 0
            for ring in cutouts:
                poly = _Poly(ring)
                for s in panel.stitches:
                    for pt in s["points"]:
                        if poly.contains(_Pt(pt[0], pt[1])):
                            bad += 1
            out.append((bad == 0, "stitches clear of cutouts",
                        f"{bad} hole(s) fall inside a cutout" if bad
                        else f"{len(cutouts)} cutout(s), no conflicts"))
    except Exception as e:
        out.append((False, "stitches clear of cutouts", f"check failed: {e}"))

    # 3. spacing error
    for i, s in enumerate(panel.stitches):
        ok = s["spacing_error_mm"] <= 0.15
        out.append((ok, f"stitch run {i+1} spacing error", 
                    f"{s['spacing_error_mm']:.3f} mm (limit 0.15)"))

    # 4. pitch honoured — substitution must be confirmed, never silent
    for i, s in enumerate(panel.stitches):
        if s["substituted"]:
            out.append((False, f"stitch run {i+1} pitch honoured",
                        f"requested {s['pitch_requested']} is not a standard iron; "
                        f"kept {s['pitch_used']:.3f} - CONFIRM WITH USER "
                        f"(standard: {STANDARD_PITCHES})"))
        else:
            out.append((True, f"stitch run {i+1} pitch honoured",
                        f"{s['pitch_used']:.3f} mm is a standard iron"))

    # 5. kerf sanity
    k = panel.cut_kerf
    min_feature = min(sh.width, sh.height)
    ok = k >= 0 and k * 2 < min_feature
    out.append((ok, "kerf compensation sane",
                f"kerf {k:.2f} mm vs smallest dimension {min_feature:.1f} mm"))

    # 6. thickness sanity — leather, not cardboard
    out.append((0.4 <= t <= 4.0, "leather thickness in range",
                f"{t:.2f} mm (0.4-4.0)"))

    # 7. folds carry compensation
    for i, f in enumerate(panel.folds):
        exp = math.pi * t
        ok = abs(f["allowance_mm"] - exp) < 0.01
        out.append((ok, f"fold {i+1} allowance",
                    f"{f['allowance_mm']:.2f} mm (pi x t = {exp:.2f})"))

    # 8. pieces actually generated
    try:
        ps = panel.pieces()
        out.append((len(ps) > 0, "pieces generated",
                    f"{len(ps)} piece(s)" if ps else "no geometry produced"))
    except Exception as e:
        out.append((False, "pieces generated", f"failed: {e}"))

    return out


# ------------------------------------------------------------------ examples
EXAMPLES = {
    "bifold": {
        "name": "bifold_wallet",
        "leather_t": 1.0,
        "kerf": 0.0,
        "shape": {"type": "rect", "w": 198.3, "h": 87.0, "r": 6.0},
        "stitch": [{"edge": 3.5, "pitch": 3.85, "mode": "variable"}],
        "folds": [{"a": [99.15, 0], "b": [99.15, 87]}],
    },
    "cardholder": {
        "name": "card_holder",
        "leather_t": 0.8,
        "shape": {"type": "rect", "w": 91.6, "h": 149.1, "r": 7.5},
        "stitch": [{"edge": 3.0, "pitch": 3.38, "mode": "variable"}],
    },
    "pouch": {
        "name": "belt_pouch",
        "leather_t": 1.4,
        "shape": {"type": "union",
                  "a": {"type": "rect", "w": 120, "h": 85, "r": 10},
                  "b": {"type": "rect", "w": 120, "h": 40, "r": 18, "y": 45}},
        "stitch": [{"edge": 4.0, "pitch": 4.0, "mode": "variable"}],
    },
    "freehand": {
        "name": "freehand_panel",
        "leather_t": 1.2,
        "kerf": 0.1,
        "shape": {"type": "svg_path",
                  "d": "M 20 60 C 20 20 60 5 100 20 S 160 70 140 105 "
                       "A 25 25 0 0 1 95 120 C 60 130 20 100 20 60 Z"},
        "stitch": [{"edge": 4.0, "pitch": 3.85, "mode": "variable"}],
    },
}


def build(spec):
    """spec dict -> (panel, gates). Raises ValueError on unusable input."""
    shape = shape_from_spec(spec["shape"])
    panel = Panel(shape,
                  name=spec.get("name", "panel"),
                  leather_t=_num(spec, "leather_t", 1.0, lo=0.01),
                  cut_kerf=_num(spec, "kerf", 0.0, lo=0.0))

    for st in spec.get("stitch", []):
        panel.add_stitch(edge=_num(st, "edge", 3.5, lo=0.5),
                         pitch=_num(st, "pitch", 3.85, lo=1.0),
                         mode=st.get("mode", "variable"),
                         closed=bool(st.get("closed", True)),
                         start=st.get("start"))
    for fd in spec.get("folds", []):
        panel.add_fold(fd["a"], fd["b"], fd.get("allowance_mm"))

    return panel, gates(panel, spec)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", nargs="?", help="JSON spec file, or - for stdin")
    ap.add_argument("--out", default="out", help="output directory")
    ap.add_argument("--example", choices=sorted(EXAMPLES),
                    help="print a template spec and exit")
    ap.add_argument("--json", action="store_true", help="emit report as JSON")
    args = ap.parse_args()

    if args.example:
        print(json.dumps(EXAMPLES[args.example], indent=1))
        return 0
    if not args.spec:
        ap.error("give a spec file, or use --example to print one")

    try:
        raw = sys.stdin.read() if args.spec == "-" else open(args.spec).read()
        spec = json.loads(raw)
        panel, gs = build(spec)
    except Exception as e:
        print(json.dumps({"error": f"{type(e).__name__}: {e}"}))
        return 1

    failed = [g for g in gs if not g[0]]

    if args.json:
        print(json.dumps({"report": panel.report(),
                          "gates": [{"ok": bool(o), "label": l, "detail": d}
                                    for o, l, d in gs],
                          "passed": not failed}, indent=1))
    else:
        print(f"\n  {panel.name}  —  {panel.shape.width:.2f} x "
              f"{panel.shape.height:.2f} mm, t={panel.leather_t} mm\n")
        for ok, label, detail in gs:
            print(f"  [{'PASS' if ok else 'FAIL'}] {label:<32}{detail}")
        print()
        if failed:
            print(f"  {len(failed)} GATE(S) FAILED — do not cut this file")
        else:
            print("  ALL GATES PASS")

    if failed:
        return 2

    from leatherkit.geom import Piece
    from leatherkit.export import to_svg, to_dxf
    from leatherkit.pdf import tiled_pdf

    pieces = panel.pieces()
    os.makedirs(args.out, exist_ok=True)
    to_svg(pieces, os.path.join(args.out, "pattern.svg"),
           title=f"{panel.name} — 1 unit = 1 mm")
    to_dxf(pieces, os.path.join(args.out, "pattern.dxf"))
    tiled_pdf(pieces, os.path.join(args.out, "pattern_1to1.pdf"),
              title=f"{panel.name} — print at 100%")
    with open(os.path.join(args.out, "report.json"), "w") as f:
        json.dump(panel.report(), f, indent=1)
    if not args.json:
        print(f"  wrote SVG + DXF + 1:1 PDF + report to {args.out}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
