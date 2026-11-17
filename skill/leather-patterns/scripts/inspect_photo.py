#!/usr/bin/env python3
"""
inspect_photo.py — for when the user supplies a photo instead of a spec.

Measures a flat leather panel from a photo containing an ISO bank card or ArUco
markers as the scale reference. Deterministic CV; no model reads pixels.

  python3 scripts/inspect_photo.py photo.jpg --scale card
  python3 scripts/inspect_photo.py photo.jpg --scale aruco --debug out/

Outputs JSON the agent can turn into a spec: measured outline, corner radius,
stitch pitch (snapped to a standard iron), edge offset, hole count.
"""
import argparse, json, math, os, sys
import numpy as np
import cv2

ISO_CARD_LONG = 85.6
STANDARD_PITCHES = (2.7, 3.0, 3.38, 3.85, 4.0, 5.0)


def card_scale(bgr):
    """px-per-mm from an ISO ID-1 card's long side (85.6 mm)."""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    sat, val = hsv[:, :, 1], hsv[:, :, 2]
    m = ((sat < 40) & (val > 140) & (val < 230)).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cs:
        return None
    # A card is an ISO ID-1 rectangle: long/short = 85.6/53.98 = 1.586.
    # Reject anything else, or we silently scale off a marker, a book, or the
    # wallet itself and return confidently wrong millimetres.
    best = None
    for c in cs:
        if cv2.contourArea(c) < 500:
            continue
        (_, _), (w, h), _ = cv2.minAreaRect(c)
        lo, hi = min(w, h), max(w, h)
        if lo < 20:
            continue
        ratio = hi / lo
        if not (1.45 <= ratio <= 1.72):        # +-8% around 1.586
            continue
        ar = cv2.contourArea(c) / max(hi * lo, 1e-6)
        if ar < 0.85:                          # must be a well-filled rectangle
            continue
        if best is None or hi > best[0]:
            best = (hi, c)
    if best is None:
        return None
    long_side, c = best
    return long_side / ISO_CARD_LONG, c


def measure(bgr, ppm, debug=None):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    sat, val = hsv[:, :, 1], hsv[:, :, 2]
    panel = ((sat > 50) & (val > 25)).astype(np.uint8) * 255
    panel = cv2.morphologyEx(panel, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    ps, _ = cv2.findContours(panel, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not ps:
        return None
    pc = max(ps, key=cv2.contourArea)
    (_, _), (w, h), ang = cv2.minAreaRect(pc)
    if w < h:
        w, h = h, w

    roi = cv2.erode(panel, np.ones((int(1.5 * ppm),) * 2, np.uint8))
    vg = cv2.GaussianBlur(val, (3, 3), 0)
    # blockSize must scale with resolution; C=8 is the stable threshold here
    bs = max(15, int(3.0 * ppm) | 1)
    ath = cv2.adaptiveThreshold(vg, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                cv2.THRESH_BINARY_INV, bs, 8)
    ath = cv2.bitwise_and(ath, roi)
    # THE critical step: a stitch line is a continuous GROOVE that merges every
    # hole into one blob. Open with a disk wider than the groove (~0.3 mm) but
    # narrower than a hole (~1.1 mm) and the individual holes separate cleanly.
    k = max(5, int(round(0.9 * ppm)) | 1)
    ath = cv2.morphologyEx(ath, cv2.MORPH_OPEN,
                           cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    n, lab, st, ct = cv2.connectedComponentsWithStats(ath, 8)
    holes = []
    for i in range(1, n):
        a_mm2 = st[i, cv2.CC_STAT_AREA] / (ppm * ppm)
        if not (0.2 <= a_mm2 <= 4.0):
            continue
        ww, hh = st[i, cv2.CC_STAT_WIDTH], st[i, cv2.CC_STAT_HEIGHT]
        if max(ww, hh) > 2.2 * min(ww, hh):
            continue
        holes.append(ct[i])
    holes = np.array(holes, np.float32) if holes else np.zeros((0, 2), np.float32)

    out = {"panel_w_mm": round(float(w / ppm), 2),
           "panel_h_mm": round(float(h / ppm), 2),
           "rotation_deg": round(float(ang), 2),
           "holes_detected": int(len(holes))}

    if len(holes) > 8:
        d = np.linalg.norm(holes[:, None] - holes[None], axis=2)
        np.fill_diagonal(d, 1e9)
        nn = d.min(axis=1) / ppm
        nn = nn[nn < 2 * np.median(nn)]
        raw = float(np.median(nn))
        out["pitch_raw_mm"] = round(raw, 3)
        out["pitch_snapped_mm"] = min(STANDARD_PITCHES, key=lambda s: abs(s - raw))
        cnt = pc[:, 0, :].astype(np.float32)
        offs = np.abs([cv2.pointPolygonTest(cnt.reshape(-1, 1, 2),
                                            (float(x), float(y)), True) / ppm
                       for x, y in holes])
        out["edge_offset_mm"] = round(float(np.median(offs)), 2)

    # corner radius. Must be measured in the panel's own frame: an axis-aligned
    # bounding box around a rotated part gives wildly wrong numbers. For a rounded
    # rectangle the arc point nearest the bbox corner sits r*(sqrt2 - 1) away.
    (rcx, rcy), (rw, rh), rang = cv2.minAreaRect(pc)
    th = math.radians(rang)
    R = np.array([[math.cos(-th), -math.sin(-th)], [math.sin(-th), math.cos(-th)]])
    loc = (pc[:, 0, :].astype(np.float64) - np.array([rcx, rcy])) @ R.T
    x0, y0 = loc.min(axis=0)
    loc -= [x0, y0]
    bw, bh = loc.max(axis=0)
    k = math.sqrt(2.0) - 1.0
    rs = []
    for cx, cy in [(0, 0), (bw, 0), (bw, bh), (0, bh)]:
        dmin = np.linalg.norm(loc - np.array([cx, cy]), axis=1).min()
        r = dmin / k / ppm
        if 0.5 < r < 0.3 * min(bw, bh) / ppm:
            rs.append(r)
    if rs:
        out["corner_radius_mm"] = round(float(np.median(rs)), 2)

    if debug:
        os.makedirs(debug, exist_ok=True)
        dbg = bgr.copy()
        cv2.drawContours(dbg, [pc], -1, (0, 200, 0), 2)
        for x, y in holes:
            cv2.circle(dbg, (int(x), int(y)), int(2 * ppm), (255, 0, 255), 1)
        cv2.imwrite(os.path.join(debug, "photo_overlay.png"), dbg)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--scale", default="card", choices=["card"])
    ap.add_argument("--debug", default=None)
    a = ap.parse_args()
    img = cv2.imread(a.image)
    if img is None:
        print(json.dumps({"error": f"cannot read {a.image}"}))
        sys.exit(1)
    sc = card_scale(img)
    if sc is None:
        print(json.dumps({"error": "no ISO/IEC 7810 ID-1 card detected (need a rectangle "
                                   "with 1.586:1 proportions, at least 85% filled). Ask the "
                                   "user to place a bank card flat beside the item, straight "
                                   "on, with all four corners visible - do NOT estimate "
                                   "dimensions without a scale reference."}))
        sys.exit(1)
    ppm, _ = sc
    m = measure(img, ppm, a.debug)
    m["px_per_mm"] = round(ppm, 3)
    m["measured_by"] = "ISO/IEC 7810 ID-1 card long side = 85.6 mm"
    print(json.dumps(m, indent=1))


if __name__ == "__main__":
    main()
