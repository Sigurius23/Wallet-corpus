#!/usr/bin/env python3
"""
Blind test: randomise the panel geometry, render a photo, and write the truth ONLY
to a JSON file (never printed). The vision model then eyeballs the photo and commits
to an estimate before the file is opened.

Purpose: measure how accurately a multimodal LLM can recover millimetre dimensions
from a photo, versus the deterministic CV pipeline.
"""
import json, math, os
import numpy as np
import cv2

os.makedirs("blind", exist_ok=True)
rng = np.random.default_rng()          # genuinely unpredictable seed

# ---------------- randomised design (NOT printed) ----------------
PANEL_W = float(rng.uniform(88, 128))
PANEL_H = float(rng.uniform(76, 108))
CORNER_R = float(rng.uniform(4, 12))
PITCH = float(rng.choice([3.0, 3.38, 3.85, 4.0]))
EDGE_OFFSET = float(rng.uniform(2.8, 4.5))
PANEL_ROT = float(rng.uniform(-12, 12))
PANEL_ORIGIN = (float(rng.uniform(85, 110)), float(rng.uniform(65, 95)))


def rounded_rect(w, h, r, n=24):
    pts = []
    for cx, cy, a0, a1 in [(r, r, 180, 270), (w - r, r, 270, 360),
                           (w - r, h - r, 0, 90), (r, h - r, 90, 180)]:
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return np.array(pts, float)


def resample(pts, spacing):
    c = np.vstack([pts, pts[:1]])
    seg = np.linalg.norm(np.diff(c, axis=0), axis=1)
    cum = np.concatenate([[0], np.cumsum(seg)])
    n = int(round(cum[-1] / spacing))
    step = cum[-1] / n
    out, j = [], 0
    for k in range(n):
        t = k * step
        while j < len(seg) - 1 and cum[j + 1] < t:
            j += 1
        f = 0 if seg[j] == 0 else (t - cum[j]) / seg[j]
        out.append(c[j] + f * (c[j + 1] - c[j]))
    return np.array(out)


def xf(p, o, deg):
    a = math.radians(deg)
    R = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    return p @ R.T + np.array(o)


outline_l = rounded_rect(PANEL_W, PANEL_H, CORNER_R)
inner_l = rounded_rect(PANEL_W - 2 * EDGE_OFFSET, PANEL_H - 2 * EDGE_OFFSET,
                       CORNER_R, 400) + np.array([EDGE_OFFSET, EDGE_OFFSET])
holes_l = resample(inner_l, PITCH)

outline = xf(outline_l, PANEL_ORIGIN, PANEL_ROT)
inner = xf(inner_l[::20], PANEL_ORIGIN, PANEL_ROT)
holes = xf(holes_l, PANEL_ORIGIN, PANEL_ROT)

# ---------------- render ----------------
PPM = 10.0
MAT_W, MAT_H = 300.0, 250.0
IW, IH = int(MAT_W * PPM), int(MAT_H * PPM)


def mm2px(p):
    return (int(round(p[0] * PPM)), int(round(p[1] * PPM)))


scene = np.full((IH, IW, 3), 238, np.uint8)
for gx in range(0, int(MAT_W) + 1, 10):
    c = (208, 208, 208) if gx % 50 else (183, 183, 183)
    cv2.line(scene, mm2px((gx, 0)), mm2px((gx, MAT_H)), c, 1)
for gy in range(0, int(MAT_H) + 1, 10):
    c = (208, 208, 208) if gy % 50 else (183, 183, 183)
    cv2.line(scene, mm2px((0, gy)), mm2px((MAT_W, gy)), c, 1)

adict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
MC = {0: (35., 35.), 1: (265., 35.), 2: (265., 215.), 3: (35., 215.)}
for mid, (cx, cy) in MC.items():
    m = cv2.aruco.generateImageMarker(adict, mid, int(40 * PPM))
    m = cv2.copyMakeBorder(m, int(10 * PPM), int(10 * PPM), int(10 * PPM), int(10 * PPM),
                           cv2.BORDER_CONSTANT, value=255)
    m3 = cv2.cvtColor(m, cv2.COLOR_GRAY2BGR)
    side = int(60 * PPM)
    m3 = cv2.resize(m3, (side, side), interpolation=cv2.INTER_AREA)
    x0, y0 = int(cx * PPM - side / 2), int(cy * PPM - side / 2)
    scene[y0:y0 + side, x0:x0 + side] = m3

poly = np.array([mm2px(p) for p in outline], np.int32)
cv2.fillPoly(scene, [poly], (86, 108, 158))
cv2.polylines(scene, [poly], True, (52, 66, 104), thickness=int(1.1 * PPM), lineType=cv2.LINE_AA)
cv2.polylines(scene, [np.array([mm2px(p) for p in inner], np.int32)], True,
              (58, 74, 112), thickness=max(1, int(0.3 * PPM)), lineType=cv2.LINE_AA)
for h in holes:
    cv2.circle(scene, mm2px(h), max(2, int(0.55 * PPM)), (30, 36, 54), -1, lineType=cv2.LINE_AA)

g = rng.normal(0, 3.5, (IH, IW, 1)).repeat(3, axis=2)
scene = np.clip(scene.astype(np.float32) + g, 0, 255).astype(np.uint8)

h, w = scene.shape[:2]
src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
dst = np.float32([[30, 40], [w - 55, 22], [w - 28, h - 34], [46, h - 12]])
photo = cv2.warpPerspective(scene, cv2.getPerspectiveTransform(src, dst),
                            (w, h), borderValue=(232, 232, 232))
R2 = cv2.getRotationMatrix2D((w / 2, h / 2), 2.0, 1.0)
photo = cv2.warpAffine(photo, R2, (w, h), borderValue=(232, 232, 232))
yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
photo = np.clip(photo.astype(np.float32) * (1 - 0.2 * xx / w - 0.1 * yy / h)[..., None], 0, 255)
photo = np.clip(photo + rng.normal(0, 2.5, photo.shape), 0, 255).astype(np.uint8)
cv2.imwrite("blind/photo.jpg", cv2.GaussianBlur(photo, (3, 3), 0.6),
            [cv2.IMWRITE_JPEG_QUALITY, 93])

truth = {"panel_width_mm": round(PANEL_W, 1), "panel_height_mm": round(PANEL_H, 1),
         "corner_radius_mm": round(CORNER_R, 1), "stitch_pitch_mm": PITCH,
         "edge_offset_mm": round(EDGE_OFFSET, 2), "hole_count": int(len(holes)),
         "rotation_deg": round(PANEL_ROT, 1)}
json.dump(truth, open("blind/truth.json", "w"), indent=1)
print("blind/photo.jpg written. truth.json written but NOT printed.")
