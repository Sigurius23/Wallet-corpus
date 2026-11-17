# Shape spec reference

A spec is one JSON object. `build_piece.py` builds it, validates it, and writes
SVG + DXF + 1:1 tiled PDF + `report.json`. Exit codes: **0** pass, **1** bad input,
**2** a gate failed.

```json
{
  "name": "belt_pouch",
  "leather_t": 1.4,
  "kerf": 0.0,
  "shape":   { ... shape tree ... },
  "stitch":  [ { "edge": 4.0, "pitch": 4.0, "mode": "variable" } ],
  "folds":   [ { "a": [60, 0], "b": [60, 85] } ]
}
```

Units are always **millimetres**, origin top-left, **y increases downward** (SVG
convention, so an SVG path drops in unchanged).

---

## Shape nodes

Every node is an object with a `type`. Any node that takes `a` / `b` / `of` takes
another **node**, so shape trees nest to any depth.

### Primitives

| type | keys | example |
|---|---|---|
| `rect` | `w`, `h`, optional `r` (corner radius), `x`, `y` | `{"type":"rect","w":120,"h":80,"r":8}` |
| `circle` | `d` (diameter), optional `cx`, `cy` | `{"type":"circle","d":30,"cx":35,"cy":40}` |
| `stadium` | `w`, `h` (w ≥ h) — full-radius ends, the right primitive for slots and straps | `{"type":"stadium","w":80,"h":14}` |
| `polygon` | `points`: list of `[x,y]`, ≥3, implicit close | `{"type":"polygon","points":[[0,0],[60,0],[70,35],[30,55]]}` |
| `svg_path` | `d`: any SVG path (M L H V C S Q T A Z), optional `flat` (samples per curve, default 12) | `{"type":"svg_path","d":"M 20 60 C 20 20 60 5 100 20 S 160 70 140 105 Z"}` |

`rect` with `r = h/2` gives a true stadium, and `r` is clamped to `min(w,h)/2`.

### Boolean operations

| type | keys |
|---|---|
| `union` | `a`, `b` |
| `difference` | `a`, `b` — `b` is cut out of `a` |
| `intersection` | `a`, `b` |

Interior rings produced by `difference` are exported as **cut-outs**, not stitch
holes, in all three formats. A stitch hole that lands inside a cut-out is a gate
failure.

```json
{"type":"difference",
 "a":{"type":"rect","w":120,"h":80,"r":8},
 "b":{"type":"union","a":{"type":"circle","d":30,"cx":35,"cy":40},
                     "b":{"type":"rect","w":60,"h":12,"r":6,"x":50,"y":34}}}
```
A window case: rounded body, circular thumb hole, 60 × 12 slot merging into it.

### Transforms

| type | keys |
|---|---|
| `offset` | `of`, `d` — positive grows outward, negative shrinks inward |
| `translate` | `of`, `dx`, `dy` |
| `rotate` | `of`, `deg` (clockwise), optional `origin` (`"center"`, default) or `[x,y]` |
| `mirror` | `of`, optional `about` (x position of the mirror line, default 0) |
| `scale` | `of`, `s` |

### Repetition

| type | keys |
|---|---|
| `repeat` | `of`, `n`, `dx`, `dy` — arrays a child `n` times |

```json
{"type":"repeat","n":6,"dy":8,"of":{"type":"circle","d":4}}
```
Six buckle holes on a strap.

**Note:** `repeat` unions its copies, so keep copies disjoint. For a strap you want
the outline *and* the holes, build them as two nodes and subtract.

---

## Stitch runs

`stitch` is a list. Each entry:

| key | default | meaning |
|---|---|---|
| `edge` | 3.5 | mm inside the cut line where holes sit |
| `pitch` | 3.85 | requested spacing, snapped to a standard iron |
| `mode` | `"variable"` | `variable` closes the loop exactly at a slightly adjusted pitch; `fixed` holds the pitch and reports the remainder |
| `closed` | `true` | closed loop vs open run |
| `start` | `null` | `[x,y]` — rotate the hole phase so one hole lands near this point |

Use `mode="variable"` unless the user names an exact pitch. `fixed` almost always
trips the 0.15 mm spacing gate, which is the correct outcome when it does.

Getting a stitch line inside a narrow region needs a shallower `edge`:

```json
{"edge": 2.0, "pitch": 3.0}
```
on a 12 mm-wide strap keeps holes 2 mm from each edge.

---

## Folds

`folds` is a list of crease lines. The allowance defaults to `π × leather_t` — the
flat length a leather fold consumes — and the gate fails if a supplied allowance
deviates from that by more than 0.01 mm.

```json
{"a": [99.15, 0], "b": [99.15, 87]}
```

Folds are drawn on their own layer and never cut.

---

## Worked examples

Print any of these to start from:

```bash
python3 scripts/build_piece.py --example bifold     > spec.json
python3 scripts/build_piece.py --example cardholder > spec.json
python3 scripts/build_piece.py --example pouch      > spec.json
python3 scripts/build_piece.py --example freehand   > spec.json
```

`freehand` is a closed cubic-bezier outline with no straight lines at all — proof
that the kernel is not limited to rectangles.
