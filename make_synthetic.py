#!/usr/bin/env python3
"""
make_synthetic.py — build synthetic "photo of a wallet on a mat" test cases with
exact ground truth in millimetres.

Scene convention (physical reality, mm):
  - cutting mat 300 x 250 mm
  - 4 ArUco markers (DICT_4X4_50, 40 mm) whose centres sit at known mm positions
  - the wallet panel placed at a known mm position, rotated by a known angle

Outputs
  synthetic/photo.jpg            simulated phone photo (perspective + lighting + noise)
  synthetic/ground_truth.json    exact mm geometry of outline + stitch holes
  synthetic/ground_truth.dxf     same, as CAD

Everything in the ground truth is in SCENE mm, so the reconstruction must recover
the same numbers from the photo alone.
"""
import json, math, os
import numpy as np
import cv2
import ezdxf

os.makedirs("synthetic", exist_ok=True)
rng = np.random.default_rng(11)

# ------------------------------------------------------------------ design parameters
PANEL_W, PANEL_H = 110.0, 95.0
CORNER_R = 8.0
PITCH = 3.85
EDGE_OFFSET = 3.5

MAT_W, MAT_H = 300.0, 250.0
MARKER_MM = 40.0
MARKER_CENTRES = {
    0: (35.0, 35.0),
    1: (MAT_W - 35.0, 35.0),
    2: (MAT_W - 35.0, MAT_H - 35.0),
    3: (35.0, MAT_H - 35.0),
}
PANEL_ORIGIN = (95.0, 78.0)     # where the panel's top-left corner sits, scene mm
PANEL_ROT_DEG = 7.0

PPM = 10.0                       # px per mm for the master render


# ------------------------------------------------------------------ geometry helpers
def rounded_rect(w, h, r, n_arc=24):
    pts = []
    for cx, cy, a0, a1 in [(r, r, 180, 270), (w - r, r, 270, 360),
                           (w - r, h - r, 0, 90), (r, h - r, 90, 180)]:
        for i in range(n_arc + 1):
            a = math.radians(a0 + (a1 - a0) * i / n_arc)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return np.array(pts, float)


def resample_closed(pts, spacing):
    closed = np.vstack([pts, pts[:1]])
    seg = np.linalg.norm(np.diff(closed, axis=0), axis=1)
    cum = np.concatenate([[0], np.cumsum(seg)])
    total = cum[-1]
    n = int(round(total / spacing))
    step = total / n
    out, j = [], 0
    for k in range(n):
        t = k * step
        while j < len(seg) - 1 and cum[j + 1] < t:
            j += 1
        f = 0.0 if seg[j] == 0 else (t - cum[j]) / seg[j]
        out.append(closed[j] + f * (closed[j + 1] - closed[j]))
    return np.array(out)


def transform(pts, origin, rot_deg):
    a = math.radians(rot_deg)
    R = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    return pts @ R.T + np.array(origin)


# ------------------------------------------------------------------ ground truth (scene mm)
outline_local = rounded_rect(PANEL_W, PANEL_H, CORNER_R)
inner_local = rounded_rect(PANEL_W - 2 * EDGE_OFFSET, PANEL_H - 2 * EDGE_OFFSET,
                           CORNER_R, n_arc=400) + np.array([EDGE_OFFSET, EDGE_OFFSET])
holes_local = resample_closed(inner_local, PITCH)

outline_mm = transform(outline_local, PANEL_ORIGIN, PANEL_ROT_DEG)
inner_mm = transform(inner_local[::20], PANEL_ORIGIN, PANEL_ROT_DEG)
holes_mm = transform(holes_local, PANEL_ORIGIN, PANEL_ROT_DEG)

print(f"ground truth: panel {PANEL_W}x{PANEL_H} mm, {len(holes_mm)} holes @ {PITCH} mm")

# ------------------------------------------------------------------ render the scene (mm -> px)
IW, IH = int(MAT_W * PPM), int(MAT_H * PPM)


def mm2px(p):
    return (int(round(p[0] * PPM)), int(round(p[1] * PPM)))


scene = np.full((IH, IW, 3), 238, np.uint8)          # mat, light grey, BGR

# mat grid every 10 mm, to look like a cutting mat
for gx in range(0, int(MAT_W) + 1, 10):
    c = (210, 210, 210) if gx % 50 else (185, 185, 185)
    cv2.line(scene, mm2px((gx, 0)), mm2px((gx, MAT_H)), c, 1)
for gy in range(0, int(MAT_H) + 1, 10):
    c = (210, 210, 210) if gy % 50 else (185, 185, 185)
    cv2.line(scene, mm2px((0, gy)), mm2px((MAT_W, gy)), c, 1)

# ArUco markers
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
marker_px = int(MARKER_MM * PPM)
for mid, (cx, cy) in MARKER_CENTRES.items():
    m = cv2.aruco.generateImageMarker(aruco_dict, mid, marker_px)
    m = cv2.copyMakeBorder(m, marker_px // 4, marker_px // 4, marker_px // 4,
                           marker_px // 4, cv2.BORDER_CONSTANT, value=255)
    m3 = cv2.cvtColor(m, cv2.COLOR_GRAY2BGR)
    side = int(MARKER_MM * 1.5 * PPM)
    m3 = cv2.resize(m3, (side, side), interpolation=cv2.INTER_AREA)
    x0 = int(cx * PPM - side / 2)
    y0 = int(cy * PPM - side / 2)
    scene[y0:y0 + side, x0:x0 + side] = m3

# the wallet panel
poly = np.array([mm2px(p) for p in outline_mm], np.int32)
cv2.fillPoly(scene, [poly], (86, 108, 158))
cv2.polylines(scene, [poly], True, (52, 66, 104), thickness=int(1.1 * PPM), lineType=cv2.LINE_AA)
cv2.polylines(scene, [np.array([mm2px(p) for p in inner_mm], np.int32)], True,
              (58, 74, 112), thickness=max(1, int(0.3 * PPM)), lineType=cv2.LINE_AA)
for h in holes_mm:
    cv2.circle(scene, mm2px(h), max(2, int(0.55 * PPM)), (30, 36, 54), -1, lineType=cv2.LINE_AA)

# subtle grain inside the panel only
grain = rng.normal(0, 3.5, (IH, IW, 1)).repeat(3, axis=2)
scene = np.clip(scene.astype(np.float32) + grain, 0, 255).astype(np.uint8)

# ------------------------------------------------------------------ simulate a photo
h, w = scene.shape[:2]
src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
dst = np.float32([[28, 44], [w - 60, 18], [w - 24, h - 30], [50, h - 8]])
M = cv2.getPerspectiveTransform(src, dst)
photo = cv2.warpPerspective(scene, M, (w, h), borderValue=(232, 232, 232))

R2 = cv2.getRotationMatrix2D((w / 2, h / 2), 2.5, 1.0)
photo = cv2.warpAffine(photo, R2, (w, h), borderValue=(232, 232, 232))

yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
shade = (1.0 - 0.22 * (xx / w) - 0.12 * (yy / h))[..., None]
photo = np.clip(photo.astype(np.float32) * shade, 0, 255)
photo = np.clip(photo + rng.normal(0, 2.5, photo.shape), 0, 255).astype(np.uint8)
photo = cv2.GaussianBlur(photo, (3, 3), 0.6)
cv2.imwrite("synthetic/photo.jpg", photo, [cv2.IMWRITE_JPEG_QUALITY, 93])

# ------------------------------------------------------------------ write ground truth
gt = {
    "units": "mm",
    "scene": {"mat_width": MAT_W, "mat_height": MAT_H},
    "marker_centres": {str(k): list(v) for k, v in MARKER_CENTRES.items()},
    "marker_size": MARKER_MM,
    "panel": {
        "width": PANEL_W, "height": PANEL_H, "corner_radius": CORNER_R,
        "origin": list(PANEL_ORIGIN), "rotation_deg": PANEL_ROT_DEG,
        "stitch_pitch": PITCH, "edge_offset": EDGE_OFFSET,
        "hole_count": int(len(holes_mm)),
        "outline_mm": outline_mm.round(4).tolist(),
        "holes_mm": holes_mm.round(4).tolist(),
    },
}
json.dump(gt, open("synthetic/ground_truth.json", "w"), indent=1)

doc = ezdxf.new("R2010", setup=True)
doc.units = ezdxf.units.MM
msp = doc.modelspace()
doc.layers.add("CUT", color=7)
doc.layers.add("STITCH", color=1)
msp.add_lwpolyline([tuple(p) for p in outline_mm], close=True, dxfattribs={"layer": "CUT"})
for hx, hy in holes_mm:
    msp.add_circle((hx, hy), 0.55, dxfattribs={"layer": "STITCH"})
doc.saveas("synthetic/ground_truth.dxf")

print("wrote synthetic/photo.jpg + ground_truth.{json,dxf}")
