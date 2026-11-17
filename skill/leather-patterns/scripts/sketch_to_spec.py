#!/usr/bin/env python3
"""
sketch_to_spec.py — turn a drawing into a structured brief for build_piece.py.

The premise: words cannot carry proportions, silhouettes or spatial relations.
So the drawing IS the prompt. You hand this a sketch (photo of paper, or an SVG),
it traces it, and emits a spec.json plus a BRIEF that states, in millimetres,
what was measured, what was assumed, and what it still needs to ask a human.

    python3 sketch_to_spec.py sketch.jpg --out brief/        # photo + ISO card
    python3 sketch_to_spec.py sketch.svg --out brief/        # vector, exact
    python3 sketch_to_spec.py sketch.jpg --name card_case --stitch 3.5 --out brief/

Exit codes: 0 spec written, 1 could not read the sketch.
"""
import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from leatherkit.shape import STANDARD_PITCHES, snap_pitch

ISO_CARD_LONG = 85.6
ISO_CARD_RATIO = 85.6 / 53.98          # 1.586


# ------------------------------------------------------------------ photo path
def _card_scale(img):
    """
    Find an ISO ID-1 card and return (px_per_mm, bbox).

    Edge/quads, not colour: a white card on white paper has no saturation but it
    does have a border. Colour-based detection silently fails on the most common
    case (a card lying on a sketchbook).
    """
    import cv2
    import numpy as np

    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g = cv2.GaussianBlur(g, (5, 5), 0)
    best = None
    for lo, hi in ((30, 90), (50, 150), (75, 200)):
        edges = cv2.Canny(g, lo, hi)
        edges = cv2.dilate(edges, np.ones((3, 3), np.uint8))
        cnts, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            if peri < 200:
                continue
            ap = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(ap) != 4 or not cv2.isContourConvex(ap):
                continue
            (_, _), (w, h), _ = cv2.minAreaRect(ap)
            lo_, hi_ = min(w, h), max(w, h)
            if lo_ < 30:
                continue
            ratio = hi_ / lo_
            if not (1.45 <= ratio <= 1.72):       # ISO ID-1 is 1.586; allow +-8%
                continue
            fill = cv2.contourArea(ap) / max(hi_ * lo_, 1e-6)
            if fill < 0.85:
                continue
            if best is None or hi_ > best[0]:
                best = (hi_, ap)
    if best is None:
        return None, None
    return best[0] / ISO_CARD_LONG, cv2.boundingRect(best[1])


def _trace_photo(img, px_per_mm, card_bbox):
    """
    Trace closed ink loops.

    A drawn loop must ENCLOSE paper. So: threshold the ink, bridge pencil gaps,
    flood-fill the paper from the outside, and any paper the flood cannot reach is
    an enclosed region — a panel, or a hole in one. That is the only reliable way
    to tell a closed panel from a loose stroke, and it costs no guessing.
    """
    import cv2
    import numpy as np

    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g = cv2.GaussianBlur(g, (3, 3), 0)
    bs = max(31, int(9 * px_per_mm) | 1)
    ink = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                cv2.THRESH_BINARY_INV, bs, 12)

    if card_bbox is not None:                      # the scale card is not a panel
        x, y, w, h = card_bbox
        pad = int(1.5 * px_per_mm)
        ink[max(0, y - pad):y + h + pad, max(0, x - pad):x + w + pad] = 0

    k = max(3, int(round(0.6 * px_per_mm)) | 1)    # bridge pencil gaps
    ink = cv2.morphologyEx(ink, cv2.MORPH_CLOSE,
                           cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))

    # paper reachable from outside = background; everything else is enclosed
    ff = ink.copy()
    hh, ww = ff.shape
    mask = np.zeros((hh + 2, ww + 2), np.uint8)
    cv2.floodFill(ff, mask, (0, 0), 255)
    enclosed = cv2.bitwise_not(ff)

    n, lab, st, ct = cv2.connectedComponentsWithStats(enclosed, 8)
    regions = []
    for i in range(1, n):
        area_mm2 = st[i, cv2.CC_STAT_AREA] / (px_per_mm ** 2)
        if area_mm2 < 100:
            continue
        regions.append((area_mm2, i))

    if not regions:
        return [], "no enclosed region found"

    # How wide is the pencil line? The enclosed regions are bounded by the INSIDE
    # of the stroke, so the true cut line is half a stroke further out. Without
    # this correction every sketch reads consistently undersize.
    dist = cv2.distanceTransform(ink, cv2.DIST_L2, 5)
    vals = dist[dist > 0]
    stroke_mm = float(2.0 * np.median(vals) / px_per_mm) if len(vals) else 0.0
    grow = stroke_mm / 2.0

    regions.sort(key=lambda r: -r[0])
    main_area, main_i = regions[0]
    pb = st[main_i, :4]                       # panel bbox (x, y, w, h)

    def contour_of(idx):
        m = np.zeros_like(enclosed)
        m[lab == idx] = 255
        cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return max(cs, key=cv2.contourArea) if cs else None

    main_c = contour_of(main_i)
    if main_c is None:
        return [], "panel region had no contour"

    # a hole is an enclosed region that sits inside the panel's bounding box and
    # is far smaller than the panel. bbox test, not point-in-solid: a bite out of
    # the edge is concave, so the panel's filled contour does not cover it.
    hole_cs = []
    for area_mm2, i in regions[1:]:
        x, y, w, h = st[i, :4]
        inside_bbox = (x >= pb[0] - 2 and y >= pb[1] - 2
                       and x + w <= pb[0] + pb[2] + 2 and y + h <= pb[1] + pb[3] + 2)
        if not inside_bbox or area_mm2 > 0.35 * main_area:
            continue
        c = contour_of(i)
        if c is not None:
            hole_cs.append(c)

    eps = max(1.0, 0.30 * px_per_mm)

    def to_mm(c, expand=grow):
        pts = [(float(q[0][0]) / px_per_mm, float(q[0][1]) / px_per_mm)
               for q in cv2.approxPolyDP(c, eps, True)]
        if expand > 0 and len(pts) >= 3:
            from shapely.geometry import Polygon as _P
            g = _P(pts).buffer(expand, quad_segs=6)
            if not g.is_empty:
                gg = g.geoms[0] if hasattr(g, "geoms") else g
                pts = [(round(a, 2), round(b, 2)) for a, b in gg.exterior.coords]
        return [(round(a, 2), round(b, 2)) for a, b in pts]

    outline = to_mm(main_c)
    if len(outline) < 3:
        return [], "panel outline simplified to fewer than 3 points"
    cuts = [c for c in (to_mm(h) for h in hole_cs) if len(c) >= 3]

    return [{"points": outline, "area_mm2": main_area, "cutouts": cuts,
             "stroke_mm": stroke_mm}], None


# ------------------------------------------------------------------ svg path
def _trace_svg(path):
    from svgpathtools import svg2paths2
    paths, _, _ = svg2paths2(path)
    out = []
    for p in paths:
        if len(p) == 0 or not p.isclosed():
            continue
        pts = []
        for seg in p:
            for i in range(8):
                z = seg.point(i / 8)
                pts.append((z.real, z.imag))
        out.append({"points": pts, "area_mm2": abs(p.area()) if hasattr(p, "area")
                    else 0.0, "cutouts": []})
    return out


# ------------------------------------------------------------------ brief
def _corner_radius(pts):
    """
    Estimate corner radius by Menger curvature, returned as a band.

    A pencil line wobbles ~1 mm; that swamps the difference between a 6 mm and a
    12 mm radius. Three estimators were tried (algebraic circle fit, corner
    offset, Menger curvature); only Menger is monotonic across 6/12/18/25 mm, and
    even it compresses the range. So this returns (est, lo, hi) and the caller is
    REQUIRED to ask the human to confirm. Reporting a single confident radius here
    would be fabrication.
    """
    import numpy as np
    a = np.asarray(pts, float)
    if len(a) < 12:
        return None, None, None

    step, arm, k = 0.4, 3.0, 5
    seg = np.linalg.norm(np.diff(np.vstack([a, a[:1]]), axis=0), axis=1)
    L = seg.sum()
    if L <= 0:
        return None, None, None
    n = max(12, int(round(L / step)))
    cum = np.concatenate([[0], np.cumsum(seg)])
    out, j = [], 0
    for t in np.arange(n) * L / n:
        while j < len(seg) - 1 and cum[j + 1] < t:
            j += 1
        u = 0 if seg[j] == 0 else (t - cum[j]) / seg[j]
        out.append(a[j] + u * (a[(j + 1) % len(a)] - a[j]))
    q = np.array(out)

    ker = np.ones(k) / k
    q = np.c_[np.convolve(np.r_[q[-k:, 0], q[:, 0], q[:k, 0]], ker, "same")[k:-k],
              np.convolve(np.r_[q[-k:, 1], q[:, 1], q[:k, 1]], ker, "same")[k:-k]]

    m = max(1, int(round(arm / step)))
    N = len(q)
    R = []
    for i in range(N):
        p1, p2, p3 = q[(i - m) % N], q[i], q[(i + m) % N]
        ab = np.linalg.norm(p2 - p1)
        bc = np.linalg.norm(p3 - p2)
        ca = np.linalg.norm(p1 - p3)
        if ab * bc * ca < 1e-9:
            continue
        sp = (ab + bc + ca) / 2
        area = math.sqrt(max(0.0, sp * (sp - ab) * (sp - bc) * (sp - ca)))
        if area < 1e-9:
            continue
        R.append((ab * bc * ca) / (4 * area))
    if not R:
        return None, None, None
    R = np.array(R)
    R = R[R < max(np.ptp(a[:, 0]), np.ptp(a[:, 1]))]
    if len(R) < 4:
        return None, None, None
    est = float(np.median(np.sort(R)[:max(3, len(R) // 4)]))
    lo, hi = float(np.percentile(R, 5)), float(np.percentile(R, 40))
    return round(est, 1), round(lo, 1), round(hi, 1)


def build_brief(traces, args):
    """The structured brief: what we measured, what we assumed, what to ask."""
    from shapely.geometry import Polygon
    assumed, questions = [], []
    panels = []

    for i, t in enumerate(traces[:6]):
        poly = Polygon(t["points"])
        if not poly.is_valid:
            poly = poly.buffer(0)
        x0, y0, x1, y1 = poly.bounds
        w, h = x1 - x0, y1 - y0
        loc = [(x - x0, y - y0) for x, y in t["points"]]

        w_s, h_s = round(w * 2) / 2, round(h * 2) / 2
        if abs(w_s - w) > 0.05 or abs(h_s - h) > 0.05:
            assumed.append(f"panel {i+1}: snapped {w:.1f} x {h:.1f} to "
                           f"{w_s} x {h_s} mm (hand sketches are not precise to 0.1 mm)")

        r_est, r_lo, r_hi = _corner_radius(loc)
        if r_est is None:
            r = 6.0
            assumed.append(f"panel {i+1}: no corner tighter than the pencil round "
                           f"resolves; using r={r} mm (sharp leather corners crack "
                           f"below about 3x thickness)")
            questions.append(f"panel {i+1}: are the corners square or rounded?")
        else:
            r = round(r_est * 2) / 2
            questions.append(
                f"panel {i+1}: corner radius measures {r_est} mm but a sketch only "
                f"carries it to roughly {r_lo}-{r_hi} mm — confirm the real radius "
                f"before cutting (using {r} mm)")
            assumed.append(f"panel {i+1}: corner radius {r} mm is an estimate, "
                           f"not a measurement")

        edge = args.stitch
        if r is not None and min(w_s, h_s) / 2 < edge + 1:
            questions.append(f"panel {i+1}: {min(w_s,h_s):.0f} mm across is too narrow "
                             f"for a {edge} mm stitch offset — reduce it or skip stitching")

        panels.append({
            "name": f"panel_{i+1}",
            "size_mm": [w_s, h_s],
            "corner_radius_mm": r,
            "area_mm2": round(float(poly.area), 1),
            "cutouts": len(t["cutouts"]),
            "outline_points": [[round(x, 2), round(y, 2)] for x, y in loc],
            "cutouts_points": [[[round(x - x0, 2), round(y - y0, 2)] for x, y in c]
                               for c in t["cutouts"]],
        })

    pitch, sub = snap_pitch(args.pitch)
    if sub:
        assumed.append(f"pitch {args.pitch} is not a standard pricking iron; "
                       f"nearest standard is {pitch} mm — confirm before cutting")
    assumed.append(f"stitch offset {args.stitch} mm inside the cut line "
                   f"(3-4 mm hand-sewn, 5-6 mm machine)")
    assumed.append(f"leather thickness {args.leather_t} mm drives fold and stack maths")
    assumed.append("no seam allowance added — add it for panels that join another panel")

    return {"units": "mm", "source": args.source,
            "scale_reference": args.scale,
            "panels": panels, "assumed": assumed, "questions": questions,
            "pitch_mm": pitch, "leather_t_mm": args.leather_t,
            "stitch_offset_mm": args.stitch}


def to_spec(brief):
    """Emit a spec.json that build_piece.py accepts directly."""
    p = brief["panels"][0]
    node = {"type": "polygon", "points": p["outline_points"]}
    for c in p["cutouts_points"]:
        node = {"type": "difference",
                "a": node, "b": {"type": "polygon", "points": c}}
    return {"name": p["name"], "leather_t": brief["leather_t_mm"],
            "kerf": 0.0, "shape": node,
            "stitch": [{"edge": brief["stitch_offset_mm"],
                        "pitch": brief["pitch_mm"], "mode": "variable"}]}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sketch", help="photo of a sketch, or an .svg")
    ap.add_argument("--out", default="brief", help="output directory")
    ap.add_argument("--name", default=None, help="name for the first panel")
    ap.add_argument("--stitch", type=float, default=3.5, help="stitch edge offset, mm")
    ap.add_argument("--pitch", type=float, default=3.85, help="pricking-iron pitch, mm")
    ap.add_argument("--leather-t", type=float, default=1.0, help="leather thickness, mm")
    ap.add_argument("--debug", default=None, help="write an overlay here")
    args = ap.parse_args()
    args.source = os.path.basename(args.sketch)

    ext = args.sketch.lower().rsplit(".", 1)[-1]
    try:
        if ext == "svg":
            args.scale = "none needed - vector, already 1:1"
            traces = _trace_svg(args.sketch)
        else:
            import cv2
            img = cv2.imread(args.sketch)
            if img is None:
                raise ValueError(f"cannot read image {args.sketch}")
            ppm, bbox = _card_scale(img)
            if ppm is None:
                print(json.dumps({"error":
                      "no ISO/IEC 7810 ID-1 card found in the sketch. Put a bank card "
                      "flat beside the drawing so the tracer has a scale reference — "
                      "do NOT estimate dimensions from a sketch without one."}))
                return 1
            args.scale = f"ISO/IEC 7810 ID-1 card, {ISO_CARD_LONG} mm long side"
            traces, trace_err = _trace_photo(img, ppm, bbox)
            if trace_err:
                print(json.dumps({"error": f"traced the card but not the drawing: {trace_err}"}))
                return 1
            if args.debug:
                os.makedirs(args.debug, exist_ok=True)
                import numpy as np
                vis = img.copy()
                for t in traces:
                    pts = np.array([[int(x * ppm), int(y * ppm)] for x, y in t["points"]],
                                   np.int32)
                    cv2.polylines(vis, [pts], True, (0, 0, 255), 2)
                cv2.imwrite(os.path.join(args.debug, "trace_overlay.png"), vis)
    except Exception as e:
        print(json.dumps({"error": f"{type(e).__name__}: {e}"}))
        return 1

    if not traces:
        print(json.dumps({"error": "no closed drawn shape found. The sketch needs a "
                                   "clearly closed outline — open strokes are not a panel. "
                                   "Close the loop and photograph it again, or trace it "
                                   "in a vector tool and pass an .svg."}))
        return 1

    brief = build_brief(traces, args)
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "brief.json"), "w") as f:
        json.dump(brief, f, indent=1)
    spec = to_spec(brief)
    if args.name:
        spec["name"] = args.name
    with open(os.path.join(args.out, "spec.json"), "w") as f:
        json.dump(spec, f, indent=1)

    print(json.dumps(brief, indent=1))
    print(f"\nwrote {args.out}/brief.json and {args.out}/spec.json")
    print(f"next: python3 scripts/build_piece.py {args.out}/spec.json --out {args.out}/cut")
    return 0


if __name__ == "__main__":
    sys.exit(main())
