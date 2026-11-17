"""
General 2D geometry kernel — arbitrary leather goods, not just wallets.

`wallet.py` is one opinionated recipe. This module is the layer underneath it:
any closed outline you can describe becomes a cut piece with stitch holes,
offsets, folds and 1:1 output. Signed-distance reasoning (offset in / offset out)
is done by shapely, which is robust on concave shapes where naive vertex
offsetting self-intersects.

Coordinate convention: millimetres, origin top-left, y DOWN (matches SVG).
Any function that flips y says so.
"""
import math
import numpy as np

try:
    from shapely.geometry import Polygon, MultiPolygon, Point, LineString, box
    from shapely.ops import unary_union
    from shapely import affinity
    _SHAPELY = True
except ImportError:                                   # pragma: no cover
    _SHAPELY = False

# Pricking-iron pitches sold in Europe. Substitution must be flagged, never silent.
STANDARD_PITCHES = (2.7, 3.0, 3.38, 3.85, 4.0, 5.0)

_JOIN = {"round": 1, "miter": 2, "bevel": 3}


def snap_pitch(p, tol=0.12):
    """Return (pitch_to_use, substituted: bool)."""
    best = min(STANDARD_PITCHES, key=lambda s: abs(s - p))
    if abs(best - p) <= tol:
        return best, False
    return p, True


def _rings(geom):
    """Yield every exterior+interior ring of a Polygon or MultiPolygon."""
    polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    for pg in polys:
        yield np.asarray(pg.exterior.coords, float)[:-1]
        for hole in pg.interiors:
            yield np.asarray(hole.coords, float)[:-1]


def resample_closed(pts, n):
    """Place `n` points evenly by arc length around a closed polyline."""
    pts = np.asarray(pts, float)
    if len(pts) < 2:
        return pts.copy()
    seg = np.linalg.norm(np.diff(np.vstack([pts, pts[:1]]), axis=0), axis=1)
    total = seg.sum()
    if total <= 0:
        return pts[:n].copy()
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    target = np.arange(n) * total / n
    out = np.empty((n, 2))
    j = 0
    for i, t in enumerate(target):
        while j < len(seg) - 1 and cum[j + 1] < t:
            j += 1
        u = 0.0 if seg[j] == 0 else (t - cum[j]) / seg[j]
        out[i] = pts[j] + u * (pts[(j + 1) % len(pts)] - pts[j])
    return out


def resample_open(pts, n):
    """Place `n` points along an open polyline, endpoints included."""
    pts = np.asarray(pts, float)
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    total = seg.sum()
    if total <= 0 or n < 2:
        return pts[:n].copy()
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    target = np.linspace(0, total, n)
    out = np.empty((n, 2))
    j = 0
    for i, t in enumerate(target):
        while j < len(seg) - 1 and cum[j + 1] < t:
            j += 1
        u = 0.0 if seg[j] == 0 else (t - cum[j]) / seg[j]
        out[i] = pts[j] + u * (pts[j + 1] - pts[j])
    return out


def _ring_inside(inner, outer):
    """True if an interior ring is geometrically inside an exterior ring."""
    try:
        return Polygon(outer).contains(Polygon(inner).representative_point())
    except Exception:
        return False


class Shape:
    """A closed 2D region in mm. Immutable-ish: every op returns a new Shape."""

    def __init__(self, geom):
        if not _SHAPELY:
            raise ImportError("leatherkit.shape needs shapely: pip install shapely")
        if geom.is_empty:
            raise ValueError("empty shape")
        if not geom.is_valid:
            geom = geom.buffer(0)
        self.geom = geom
        self.pitch_requested = None
        self.pitch_substituted = False
        self.pitch_used = None

    # ---------- constructors ----------
    @classmethod
    def rect(cls, w, h, r=0.0, x0=0.0, y0=0.0):
        # Build the arcs explicitly. The buffer(-r).buffer(r) trick silently
        # collapses to nothing when r reaches min(w,h)/2, which is exactly the
        # stadium case people actually want for slots.
        from .geom import rounded_rect
        if r <= 0:
            return cls(box(x0, y0, x0 + w, y0 + h))
        pts = rounded_rect(w, h, r, x0=x0, y0=y0)
        return cls(Polygon(pts))

    @classmethod
    def circle(cls, d, cx=0.0, cy=0.0):
        return cls(Point(cx, cy).buffer(d / 2.0, quad_segs=32))

    @classmethod
    def stadium(cls, w, h):
        """Rounded slot: full-radius ends. w must be >= h."""
        r = h / 2.0
        return cls(box(0, 0, w, h).buffer(r, quad_segs=24, join_style=1)
                   .buffer(-r, quad_segs=24, join_style=1)
                   .union(Point(r, r).buffer(r, quad_segs=24))
                   .union(Point(w - r, r).buffer(r, quad_segs=24))
                   .union(box(r, 0, w - r, h)))

    @classmethod
    def from_points(cls, pts):
        return cls(Polygon(np.asarray(pts, float)))

    @classmethod
    def from_svg_path(cls, d, flat=12):
        """
        Arbitrary curves from an SVG path string — lines, quadratics, cubics, arcs.
        `flat` = samples per curve segment; 12 is plenty for cutting at 0.1 mm.
        SVG is already y-down, so no flip is needed.
        """
        from svgpathtools import parse_path
        p = parse_path(d)
        if len(p) == 0:
            raise ValueError("SVG path parsed to zero segments")
        pts = []
        for seg in p:
            for i in range(flat):
                z = seg.point(i / flat)
                pts.append((z.real, z.imag))
        if p.isclosed():
            return cls(Polygon(pts))
        return cls(Polygon(pts).buffer(0))

    @classmethod
    def from_lines(cls, polys, width):
        """A stroked path (e.g. a strap centreline) as a solid of given width."""
        return cls(unary_union([LineString(p).buffer(width / 2.0, cap_style=2)
                                for p in polys]))

    # ---------- ops ----------
    def offset(self, d, join="round"):
        """Positive grows outward, negative shrinks inward. Kerf = negative d."""
        return Shape(self.geom.buffer(d, join_style=_JOIN[join], quad_segs=12))

    def union(self, other):
        return Shape(self.geom.union(other.geom))

    def difference(self, other):
        return Shape(self.geom.difference(other.geom))

    def intersection(self, other):
        return Shape(self.geom.intersection(other.geom))

    def translate(self, dx, dy):
        return Shape(affinity.translate(self.geom, dx, dy))

    def rotate(self, deg, origin="center"):
        if origin == "center":
            c = self.geom.centroid
            origin = (c.x, c.y)
        return Shape(affinity.rotate(self.geom, deg, origin=origin, use_radians=False))

    def mirror_x(self, about=0.0):
        return Shape(affinity.scale(self.geom, xfact=-1, yfact=1, origin=(about, 0)))

    def scale(self, s):
        return Shape(affinity.scale(self.geom, xfact=s, yfact=s, origin=(0, 0)))

    # ---------- properties ----------
    @property
    def area(self):
        return self.geom.area

    @property
    def bbox(self):
        x0, y0, x1, y1 = self.geom.bounds
        return (0.0, 0.0, x1 - x0, y1 - y0)

    @property
    def width(self):
        return self.bbox[2]

    @property
    def height(self):
        return self.bbox[3]

    def perimeter(self):
        return self.geom.length

    def outline(self):
        """Largest ring as an Nx2 array — the part you actually cut."""
        rings = list(_rings(self.geom))
        return max(rings, key=lambda r: math.hypot(*(r.max(0) - r.min(0))))

    def contains(self, pt):
        return self.geom.contains(Point(pt))

    # ---------- stitching ----------
    def inset_ring(self, d, quad_segs=24):
        """
        Ring `d` mm inside the outline. Uses a negative buffer, not a naive
        offset, so concave shapes cannot fold back on themselves.
        """
        inner = self.geom.buffer(-d, join_style=1, quad_segs=quad_segs)
        if inner.is_empty:
            raise ValueError(f"inset of {d} mm self-destructs this shape "
                             f"(min half-width is about {self._min_halfwidth():.2f} mm)")
        # A shape with a cutout insets to TWO rings. The stitch line belongs on the
        # OUTER boundary, so pick by enclosed area — picking by point count silently
        # stitches around the window instead of around the part.
        rings = list(_rings(inner))
        return max(rings, key=lambda r: Polygon(r).area)

    def _min_halfwidth(self):
        return math.sqrt(max(self.geom.area, 1e-9) / math.pi)

    def stitch_holes(self, edge=3.5, pitch=3.85, mode="variable",
                     closed=True, start=None, path=None):
        """
        Evenly spaced stitch holes along a line `edge` mm inside the cut line.

        mode="variable"  -> hold the count from the requested pitch, then close the
                            loop exactly by adjusting pitch. spacing error = 0.
        mode="fixed"     -> hold the pitch, absorb the remainder in one gap and
                            report the error.

        Returns dict: points, pitch_requested, pitch_used, substituted,
                      spacing_error_mm, perimeter_mm
        """
        p_req = float(pitch)
        p, substituted = snap_pitch(p_req)
        if path is not None:
            line = np.asarray(path, float)
        else:
            line = self.inset_ring(edge)
        L = (np.linalg.norm(np.diff(np.vstack([line, line[:1]]), axis=0), axis=1).sum()
             if closed else np.linalg.norm(np.diff(line, axis=0), axis=1).sum())
        if L < p * 2:
            raise ValueError(f"stitch line is {L:.1f} mm, too short for pitch {p}")

        if mode == "variable":
            n = max(4, int(round(L / p)))
            used = L / n
            err = 0.0
        else:
            n = int(L // p)
            used = p
            err = abs(L - n * p)

        pts = (resample_closed(line, n) if closed else resample_open(line, n))
        if start is not None:                        # rotate phase to a feature
            i = int(np.argmin(np.linalg.norm(pts - np.asarray(start, float), axis=1)))
            pts = np.roll(pts, -i, axis=0)

        self.pitch_requested, self.pitch_used = p_req, used
        self.pitch_substituted = substituted
        return {"points": pts, "pitch_requested": p_req, "pitch_used": used,
                "substituted": substituted, "spacing_error_mm": err,
                "perimeter_mm": L, "count": n}


class Panel:
    """
    A Shape plus its leather construction: thickness, stitching, fold lines.
    This is the object a design description produces.
    """

    def __init__(self, shape, name="panel", leather_t=1.0, cut_kerf=0.0):
        self.shape = shape
        self.name = name
        self.leather_t = leather_t
        self.cut_kerf = cut_kerf
        self.stitches = []
        self.folds = []
        self.notes = []

    def add_stitch(self, edge=3.5, pitch=3.85, mode="variable", closed=True,
                   holes=True, start=None, path=None):
        res = self.shape.stitch_holes(edge=edge, pitch=pitch, mode=mode,
                                      closed=closed, start=start, path=path)
        self.stitches.append({"edge": edge, **res})
        return res

    def add_fold(self, a, b, allowance=None):
        """
        Fold line with compensation. A leather fold consumes about pi*t of flat
        length, but you never remove it from the pattern — the allowance is where
        the material goes. Recorded so the maker knows what to expect.
        """
        if allowance is None:
            allowance = math.pi * self.leather_t
        self.folds.append({"a": tuple(a), "b": tuple(b), "allowance_mm": allowance})
        return allowance

    def note(self, x, y, text):
        self.notes.append((x, y, text))

    def pieces(self):
        """
        One Piece per exterior ring. Interior rings become CUTOUTS — a window, a
        thumb slot, a hole you cut out — not stitch holes. Getting this wrong
        means the piece looks right in the report and is wrong on the bench.
        """
        from .geom import Piece
        kerf = self.cut_kerf

        def rings_of(g):
            if isinstance(g, MultiPolygon):
                ext, intr = [], []
                for pg in g.geoms:
                    ext.append(np.asarray(pg.exterior.coords, float)[:-1])
                    intr += [np.asarray(h.coords, float)[:-1] for h in pg.interiors]
                return ext, intr
            return ([np.asarray(g.exterior.coords, float)[:-1]],
                    [np.asarray(h.coords, float)[:-1] for h in g.interiors])

        ext, intr = rings_of(self.shape.geom)
        if kerf:
            allr = rings_of(self.shape.offset(-kerf).geom)
            ext = allr[0] if allr[0] else ext
            intr = allr[1] if allr[0] else intr

        holes = np.vstack([s["points"] for s in self.stitches]) \
            if self.stitches else np.zeros((0, 2))
        out = []
        for i, outline in enumerate(sorted(ext, key=len, reverse=True)):
            nm = self.name if len(ext) == 1 else f"{self.name}_{i+1}"
            own = [c for c in intr if _ring_inside(c, outline)]
            out.append(Piece(nm, outline, holes,
                             [(f["a"], f["b"]) for f in self.folds],
                             list(self.notes), cutouts=own))
        return out

    def report(self):
        r = {"name": self.name,
             "width_mm": round(self.shape.width, 2),
             "height_mm": round(self.shape.height, 2),
             "area_mm2": round(self.shape.area, 2),
             "leather_t_mm": self.leather_t,
             "cut_kerf_mm": self.cut_kerf,
             "stitch_runs": []}
        for s in self.stitches:
            r["stitch_runs"].append({
                "edge_mm": s["edge"], "count": s["count"],
                "pitch_requested": s["pitch_requested"],
                "pitch_used": round(s["pitch_used"], 4),
                "substituted": s["substituted"],
                "spacing_error_mm": round(s["spacing_error_mm"], 4),
                "perimeter_mm": round(s["perimeter_mm"], 2)})
        r["folds"] = [{"allowance_mm": round(f["allowance_mm"], 3)}
                      for f in self.folds]
        return r
