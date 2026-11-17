#!/usr/bin/env python3
"""
reconstruct.py — photo of a flat leather wallet panel  ->  measured, cuttable pattern.

  photo ──▶ ArUco scale ──▶ rectify to 1 px = 1/4 mm ──▶ segment panel
        ──▶ detect stitch holes ──▶ recover PITCH, edge offset, corner radius
        ──▶ export SVG + DXF + JSON + overlay, optionally scored against ground truth

Usage
  python3 reconstruct.py synthetic/photo.jpg --truth synthetic/ground_truth.json
  python3 reconstruct.py myphoto.jpg --marker-layout markers.json

Design notes
  * No machine learning. Every step is deterministic and auditable — which is the
    whole point: for flat goods you get millimetre accuracy without a training set.
  * Stitch pitch is recovered from the holes themselves, then snapped to the nearest
    standard pricking-iron pitch, because that is what a maker will actually own.
"""
import argparse, json, math, os
import numpy as np
import cv2
import ezdxf

# standard pricking iron pitches, mm
STANDARD_PITCHES = (2.7, 3.0, 3.38, 3.85, 4.0, 5.0)

ap = argparse.ArgumentParser()
ap.add_argument("image")
ap.add_argument("--truth", default=None)
ap.add_argument("--out", default="out")
ap.add_argument("--marker-layout", default=None,
                help="JSON: {\"0\":[x,y], ...} marker centres in mm (default: 300x250 mat)")
ap.add_argument("--edge-comp", type=float, default=0.0,
                help="mm to shrink the outline by, to undo a burnished edge that "
                     "straddles the true cut line")
ap.add_argument("--snap-pitch", action="store_true", default=True)
ap.add_argument("--no-snap-pitch", dest="snap_pitch", action="store_false")
args = ap.parse_args()

os.makedirs(args.out, exist_ok=True)
S = 4.0                                  # working resolution: px per mm
MAT_W, MAT_H = 300.0, 250.0
DEFAULT_LAYOUT = {0: (35.0, 35.0), 1: (265.0, 35.0), 2: (265.0, 215.0), 3: (35.0, 215.0)}
LAYOUT = DEFAULT_LAYOUT
if args.marker_layout:
    LAYOUT = {int(k): tuple(v) for k, v in json.load(open(args.marker_layout)).items()}

report = {}

# ============================================================ 1 · markers -> metric frame
img = cv2.imread(args.image)
if img is None:
    raise SystemExit(f"cannot read {args.image}")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
d = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
p = cv2.aruco.DetectorParameters()
p.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
p.adaptiveThreshWinSizeMin, p.adaptiveThreshWinSizeMax = 7, 41
corners, ids, _ = cv2.aruco.ArucoDetector(d, p).detectMarkers(gray)

if ids is None or len(ids) < 3:
    raise SystemExit(f"need >=3 markers, found {0 if ids is None else len(ids)}")

ip, mp = [], []
for c, i in zip(corners, ids.ravel()):
    if i in LAYOUT:
        ip.append(c.reshape(4, 2).mean(axis=0))
        mp.append(LAYOUT[i])
ip, mp = np.array(ip, np.float32), np.array(mp, np.float32)
Hm, _ = cv2.findHomography(ip, mp, 0)                 # image px -> mat mm

proj = cv2.perspectiveTransform(ip.reshape(-1, 1, 2), Hm).reshape(-1, 2)
report["markers_detected"] = int(len(ip))
report["marker_reproj_err_mm"] = round(float(np.mean(np.linalg.norm(proj - mp, axis=1))), 3)

Sx = np.array([[S, 0, 0], [0, S, 0], [0, 0, 1.0]])
metric = cv2.warpPerspective(img, Sx @ Hm, (int(MAT_W * S), int(MAT_H * S)),
                             flags=cv2.INTER_CUBIC, borderValue=(255, 255, 255))
cv2.imwrite(f"{args.out}/01_metric.png", metric)

# ============================================================ 2 · segment the panel
hsv = cv2.cvtColor(metric, cv2.COLOR_BGR2HSV)
sat, val = hsv[:, :, 1], hsv[:, :, 2]

panel = ((sat > 45) & (val > 25)).astype(np.uint8) * 255
panel = cv2.morphologyEx(panel, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
panel = cv2.morphologyEx(panel, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))

cnts, _ = cv2.findContours(panel, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
if not cnts:
    raise SystemExit("no panel found — is the leather more saturated than the background?")
cnt = max(cnts, key=cv2.contourArea)
report["panel_area_mm2"] = round(float(cv2.contourArea(cnt) / S / S), 1)

approx = cv2.approxPolyDP(cnt, 0.004 * cv2.arcLength(cnt, True), True)
outline = approx[:, 0, :].astype(np.float64) / S          # mm, mat frame

# ============================================================ 3 · panel frame (upright)
(rcx, rcy), (rw, rh), rang = cv2.minAreaRect(approx)
if rw < rh:                                                # make rw the long side
    rw, rh = rh, rw
if rang > 45:
    rang -= 90
elif rang < -45:
    rang += 90
report["bbox_mm"] = [round(rw / S, 2), round(rh / S, 2)]
report["panel_rotation_deg"] = round(float(rang), 2)

th = math.radians(rang)
Rinv = np.array([[math.cos(-th), -math.sin(-th)], [math.sin(-th), math.cos(-th)]])
origin = np.array([rcx / S, rcy / S])


def panel_raw(pts):
    """rigid only: mat mm -> panel-aligned mm (no re-origin)"""
    return (np.asarray(pts, float) - origin) @ Rinv.T


outline_raw = panel_raw(outline)
dense_raw = panel_raw(cnt[:, 0, :].astype(np.float64) / S)

OFF = outline_raw.min(axis=0)          # one shared origin so all sets stay registered


def to_panel(pts):
    return panel_raw(pts) - OFF


outline_p = outline_raw - OFF
dense_p = dense_raw - OFF

if args.edge_comp:
    # shrink the polygon toward its centroid, exactly by --edge-comp mm
    c0 = outline_p.mean(axis=0)
    if len(outline_p) >= 3:
        area = 0.5 * abs(np.dot(outline_p[:, 0], np.roll(outline_p[:, 1], -1)) -
                         np.dot(outline_p[:, 1], np.roll(outline_p[:, 0], -1)))
        perim = float(np.sum(np.linalg.norm(np.diff(np.vstack([outline_p, outline_p[:1]]),
                                                   axis=0), axis=1)))
        inset = args.edge_comp
        v = c0 - outline_p
        n = np.linalg.norm(v, axis=1, keepdims=True)
        outline_p = outline_p + (v / np.maximum(n, 1e-9)) * inset
        dense_p = dense_p + 0  # dense set keeps measuring the true edge
        report["edge_comp_mm"] = inset
        Wc, Hc = (outline_p.max(axis=0) - outline_p.min(axis=0))
        report["bbox_mm_compensated"] = [round(float(Wc), 2), round(float(Hc), 2)]

# ============================================================ 4 · corner radius (panel frame)
def fit_circle(P):
    x, y = P[:, 0], P[:, 1]
    A = np.c_[2 * x, 2 * y, np.ones(len(P))]
    sol, *_ = np.linalg.lstsq(A, x ** 2 + y ** 2, rcond=None)
    cx, cy, c = sol
    return cx, cy, math.sqrt(max(c + cx ** 2 + cy ** 2, 1e-9))


def corner_radius(dense_pts, w, h, band=0.25):
    """
    For a rounded rectangle with radius r, the arc point closest to the bbox
    corner sits at distance r*(sqrt(2)-1) from that corner. So measure the
    minimum distance from each bbox corner to the dense outline and invert it.
    This is exact for true rounded corners and far more stable than circle
    fitting, which is at the mercy of how many arc points survive sampling.
    """
    k = math.sqrt(2.0) - 1.0
    out = []
    for cx, cy in [(0, 0), (w, 0), (w, h), (0, h)]:
        dmin = np.linalg.norm(dense_pts - np.array([cx, cy]), axis=1).min()
        r = dmin / k
        if 0.5 < r < band * min(w, h):      # sanity: radius must be plausible
            out.append(r)
    return round(float(np.median(out)), 2) if out else None


report["corner_radius_mm"] = corner_radius(dense_p, report["bbox_mm"][0], report["bbox_mm"][1])

# ============================================================ 5 · stitch holes
roi = cv2.erode(panel, np.ones((int(2.5 * S),) * 2, np.uint8))
vg = cv2.GaussianBlur(val, (3, 3), 0)
# adaptive threshold isolates local dark blobs and ignores the lighting gradient
ath = cv2.adaptiveThreshold(vg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
                            int(3.0 * S) | 1, 12)
ath = cv2.bitwise_and(ath, roi)
ath = cv2.morphologyEx(ath, cv2.MORPH_OPEN,
                       cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))

n, lab, stats, cent = cv2.connectedComponentsWithStats(ath, 8)
cand = []
for i in range(1, n):
    a = stats[i, cv2.CC_STAT_AREA] / (S * S)               # mm^2
    if not (0.3 <= a <= 3.0):
        continue
    ww, hh = stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]
    if max(ww, hh) > 2.0 * min(ww, hh):                   # discard creases / slots
        continue
    cand.append((cent[i][0] / S, cent[i][1] / S, (ww + hh) / 2 / S))
cand = np.array(cand, float) if cand else np.zeros((0, 3))

# keep only holes that sit in a band around the outline (a stitch run)
cnt_mm = cnt[:, 0, :].astype(np.float32) / S
def dist_to_outline(points):
    return np.abs([cv2.pointPolygonTest(cnt_mm.reshape(-1, 1, 2), (float(x), float(y)), True)
                   for x, y in points])

if len(cand):
    dd = dist_to_outline(cand[:, :2])
    band = np.median(dd) + 1.2
    cand = cand[dd <= band]
report["holes_detected"] = int(len(cand))

pitch_raw = None
if len(cand) >= 8:
    report["hole_diameter_mm"] = round(float(np.median(cand[:, 2])), 2)
    report["edge_offset_mm"] = round(float(np.median(dist_to_outline(cand[:, :2]))), 2)

    # order the holes along the stitch run, then take median consecutive spacing
    ang = np.arctan2(cand[:, 1] - cand[:, 1].mean(), cand[:, 0] - cand[:, 0].mean())
    order = np.argsort(ang)
    seq = cand[order, :2]
    steps = np.linalg.norm(np.diff(seq, axis=0), axis=1)
    steps = steps[(steps > 1.0) & (steps < 8.0)]
    if len(steps):
        pitch_raw = float(np.median(steps))
        report["stitch_pitch_raw_mm"] = round(pitch_raw, 3)

    # snap to the nearest standard iron
    if args.snap_pitch and pitch_raw:
        snapped = min(STANDARD_PITCHES, key=lambda s: abs(s - pitch_raw))
        report["stitch_pitch_mm"] = snapped
        report["stitch_pitch_snap_err_mm"] = round(snapped - pitch_raw, 3)
    elif pitch_raw:
        report["stitch_pitch_mm"] = round(pitch_raw, 3)

    # de-duplicate: greedy suppression of detections closer than 0.6 * pitch
    keep_idx = []
    taken = np.zeros(len(cand), bool)
    order_by_conf = np.argsort(np.abs(cand[:, 2] - np.median(cand[:, 2])))
    for i in order_by_conf:
        if taken[i]:
            continue
        keep_idx.append(i)
        close = np.linalg.norm(cand[:, :2] - cand[i, :2], axis=1) < 0.6 * (pitch_raw or 3.0)
        taken |= close
    cand = cand[np.sort(np.array(keep_idx))]
    report["holes_after_dedupe"] = int(len(cand))

    # second pass: drop outliers, re-estimate edge offset from the inliers
    keep = np.abs(dist_to_outline(cand[:, :2]) - (report.get("edge_offset_mm") or 0)) < 1.0
    if keep.sum() >= 8:
        cand = cand[keep]
        report["holes_inliers"] = int(len(cand))

holes_p = to_panel(cand[:, :2]) if len(cand) else np.zeros((0, 2))

# ============================================================ 6 · export
W, Hh = report["bbox_mm"]

svg = ['<?xml version="1.0" encoding="UTF-8"?>',
       f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{Hh}mm" '
       f'viewBox="-3 -3 {W + 6} {Hh + 6}">',
       '<g fill="none" stroke="#111" stroke-width="0.25">',
       '  <polygon points="' + " ".join(f"{x:.3f},{y:.3f}" for x, y in outline_p) + '" />',
       '</g>',
       '<g fill="none" stroke="#cc2222" stroke-width="0.15">']
for x, y in holes_p:
    svg.append(f'  <circle cx="{x:.3f}" cy="{y:.3f}" r="0.5" />')
svg += ['</g>', '</svg>']
open(f"{args.out}/pattern.svg", "w").write("\n".join(svg))

doc = ezdxf.new("R2010", setup=True)
doc.units = ezdxf.units.MM
msp = doc.modelspace()
doc.layers.add("CUT", color=7)
doc.layers.add("STITCH", color=1)
msp.add_lwpolyline([tuple(q) for q in outline_p], close=True, dxfattribs={"layer": "CUT"})
for x, y in holes_p:
    msp.add_circle((x, y), 0.5, dxfattribs={"layer": "STITCH"})
doc.saveas(f"{args.out}/pattern.dxf")

ov = metric.copy()
cv2.drawContours(ov, [cnt], -1, (0, 150, 255), 2)
cv2.drawContours(ov, [approx], -1, (0, 200, 0), 2)
for hx, hy, _ in cand:
    cv2.circle(ov, (int(hx * S), int(hy * S)), int(2.5 * S), (255, 0, 255), 1)
cv2.putText(ov, f"{report.get('stitch_pitch_raw_mm','?')} mm raw -> "
                f"{report.get('stitch_pitch_mm','?')} mm snapped | {len(cand)} holes",
            (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 220), 2)
cv2.imwrite(f"{args.out}/02_overlay.png", ov)

# ============================================================ 7 · score
if args.truth:
    _gt = json.load(open(args.truth))
    gt = _gt["panel"] if "panel" in _gt else _gt      # accept both truth formats
    truth = np.array(gt["outline_mm"], float) if "outline_mm" in gt else None
    truth_p = to_panel(truth)          # same rigid alignment, for a fair comparison

    def pt_seg(P, A):                                            # P -> closed polyline A
        B = np.roll(A, -1, axis=0)
        best = np.full(len(P), np.inf)
        for a, b in zip(A, B):
            ab = b - a
            L2 = float(ab @ ab)
            if L2 == 0:
                dd = np.linalg.norm(P - a, axis=1)
            else:
                t = np.clip(((P - a) @ ab) / L2, 0, 1)
                dd = np.linalg.norm(P - (a + t[:, None] * ab), axis=1)
            best = np.minimum(best, dd)
        return best

    e = (np.concatenate([pt_seg(outline_p, truth_p), pt_seg(truth_p, outline_p)])
         if truth is not None else np.array([np.nan]))
    report["outline_err_mm"] = {"mean": round(float(e.mean()), 3),
                                "p95": round(float(np.percentile(e, 95)), 3),
                                "max": round(float(e.max()), 3)}
    tW = gt.get("width", gt.get("panel_width_mm"))
    tH = gt.get("height", gt.get("panel_height_mm"))
    tR = gt.get("corner_radius", gt.get("corner_radius_mm"))
    tP = gt.get("stitch_pitch", gt.get("stitch_pitch_mm"))
    tE = gt.get("edge_offset", gt.get("edge_offset_mm"))
    tN = gt.get("hole_count")
    report["truth"] = {"width": tW, "height": tH, "corner_radius": tR,
                       "stitch_pitch": tP, "edge_offset": tE, "hole_count": tN}
    def _d(a, b):
        return None if (a is None or b is None) else round(a - b, 2)

    report["err"] = {
        "width_mm": _d(report["bbox_mm"][0], tW),
        "height_mm": _d(report["bbox_mm"][1], tH),
        "corner_radius_mm": _d(report.get("corner_radius_mm"), tR),
        "pitch_mm": _d(report.get("stitch_pitch_raw_mm"), tP),
        "edge_offset_mm": _d(report.get("edge_offset_mm"), tE),
        "hole_count": (None if tN is None else
                       report.get("holes_after_dedupe", report["holes_detected"]) - tN),
    }

json.dump(report, open(f"{args.out}/report.json", "w"), indent=1)
print(json.dumps(report, indent=1))
