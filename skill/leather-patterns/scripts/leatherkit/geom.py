"""Geometry primitives. All units millimetres, origin top-left, y down."""
import math
import numpy as np


class Piece:
    """A single cut piece: outline + stitch holes + fold lines + annotations."""

    def __init__(self, name, outline, holes=None, folds=None, notes=None,
                 cutouts=None):
        self.name = name
        self.outline = np.asarray(outline, float)
        # interior closed rings that are CUT THROUGH, not merely stitched.
        # Without this, a window or a thumb slot silently vanishes from the file.
        self.cutouts = [np.asarray(c, float) for c in (cutouts or [])]
        self.holes = np.asarray(holes, float) if holes is not None else np.zeros((0, 2))
        self.folds = folds or []          # list of ((x1,y1),(x2,y2))
        self.notes = notes or []          # list of (x, y, text)

    @property
    def bbox(self):
        mn, mx = self.outline.min(axis=0), self.outline.max(axis=0)
        return (0.0, 0.0, float(mx[0] - mn[0]), float(mx[1] - mn[1]))

    @property
    def width(self):
        return self.bbox[2]

    @property
    def height(self):
        return self.bbox[3]

    def translated(self, dx, dy):
        return Piece(self.name, self.outline + [dx, dy],
                     self.holes + [dx, dy] if len(self.holes) else self.holes,
                     [[(a[0] + dx, a[1] + dy), (b[0] + dx, b[1] + dy)] for a, b in self.folds],
                     [(x + dx, y + dy, t) for x, y, t in self.notes],
                     [c + [dx, dy] for c in self.cutouts])

    def mirrored_x(self, about=0.0):
        o = self.outline.copy()
        o[:, 0] = 2 * about - o[:, 0]
        h = self.holes.copy()
        if len(h):
            h[:, 0] = 2 * about - h[:, 0]
        return Piece(self.name + "_mirror", o, h, self.folds, self.notes)

    def __repr__(self):
        return (f"<Piece {self.name} {self.width:.1f}x{self.height:.1f}mm "
                f"{len(self.holes)} holes {len(self.cutouts)} cutouts>")


def rounded_rect(w, h, r, n_arc=24, x0=0.0, y0=0.0):
    """Closed rounded-rectangle outline, clockwise in screen coords."""
    r = min(r, w / 2, h / 2)
    pts = []
    for cx, cy, a0, a1 in [(x0 + r, y0 + r, 180, 270),
                           (x0 + w - r, y0 + r, 270, 360),
                           (x0 + w - r, y0 + h - r, 0, 90),
                           (x0 + r, y0 + h - r, 90, 180)]:
        for i in range(n_arc + 1):
            a = math.radians(a0 + (a1 - a0) * i / n_arc)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return np.array(pts, float)


def polygon_area(pts):
    x, y = pts[:, 0], pts[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def perimeter(pts, closed=True):
    p = np.vstack([pts, pts[:1]]) if closed else pts
    return float(np.sum(np.linalg.norm(np.diff(p, axis=0), axis=1)))


def resample_even(pts, n=None, spacing=None, closed=True):
    """Place n points evenly along a polyline (or at ~spacing)."""
    p = np.vstack([pts, pts[:1]]) if closed else np.asarray(pts, float)
    seg = np.linalg.norm(np.diff(p, axis=0), axis=1)
    cum = np.concatenate([[0], np.cumsum(seg)])
    total = cum[-1]
    if n is None:
        n = max(2, int(round(total / spacing)))
    step = total / n
    out, j = [], 0
    for k in range(n):
        t = k * step
        while j < len(seg) - 1 and cum[j + 1] < t:
            j += 1
        f = 0.0 if seg[j] == 0 else (t - cum[j]) / seg[j]
        out.append(p[j] + f * (p[j + 1] - p[j]))
    return np.array(out)


def inset(pts, d):
    """Shrink a closed polygon toward its centroid by d mm (approximate)."""
    c = pts.mean(axis=0)
    v = c - pts
    n = np.linalg.norm(v, axis=1, keepdims=True)
    return pts + (v / np.maximum(n, 1e-9)) * d
