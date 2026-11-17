# leather-patterns — an agent skill

Generate cutting patterns for **any flat leather design**: wallets, card holders,
bags, pouches, cases, sleeves, straps, covers, tool rolls, or a one-off freeform
shape you describe. The agent writes a spec; a deterministic kernel writes the
geometry. No model estimates a millimetre.

## Install

Drop this folder into your skills directory:

```
<skills>/leather-patterns/
├── SKILL.md
├── scripts/
│   ├── build_piece.py    # general entry point: ANY design
│   ├── sketch_to_spec.py # drawing -> structured brief -> spec
│   ├── build_wallet.py   # shortcut for bifold / card holder
│   ├── inspect_photo.py  # measure a real item from a photo
│   └── leatherkit/
│       ├── shape.py      # general kernel: Shape, Panel, stitching
│       ├── wallet.py     # one opinionated recipe
│       ├── geom.py · stitch.py · export.py · pdf.py
├── reference/
│   ├── spec.md           # every spec node type, with examples
│   ├── construction.md   # how to build a non-wallet good
│   ├── api.md
│   ├── constraints.md
│   ├── pitches.md
│   ├── sketch-brief.md   # the sketch -> brief -> pattern pipeline
│   └── photo-intake.md
└── assets/mat.svg
```

Requires: `numpy`, `shapely`, `svgpathtools`, `ezdxf`, `reportlab`.
`opencv-contrib-python` additionally, for photo intake. No network at runtime.

```
pip install numpy shapely svgpathtools ezdxf reportlab opencv-contrib-python
```

## Use — any design

Describe the part as a JSON tree of primitives and booleans:

```json
{"name": "window_case", "leather_t": 1.2, "kerf": 0.1,
 "shape": {"type": "difference",
   "a": {"type": "rect", "w": 120, "h": 80, "r": 8},
   "b": {"type": "union", "a": {"type": "circle", "d": 30, "cx": 35, "cy": 40},
                         "b": {"type": "rect", "w": 60, "h": 12, "r": 6, "x": 50, "y": 34}}},
 "stitch": [{"edge": 4.0, "pitch": 3.85}]}
```

```bash
python3 scripts/build_piece.py spec.json --out ./out
```

Prints a PASS/FAIL gate table and **exits 2 if any gate fails**, so a calling agent
cannot mistake a bad pattern for a good one.

```
  [PASS] panel has real area             8149 mm2 (120.0 x 80.0 mm)
  [PASS] stitch run 1 inside the outline run 1: 62 holes at 4.0 mm inside the edge
  [PASS] stitches clear of cutouts       1 cutout(s), no conflicts
  [PASS] stitch run 1 spacing error      0.000 mm (limit 0.15)
  [PASS] stitch run 1 pitch honoured     3.820 mm is a standard iron
  [PASS] kerf compensation sane          kerf 0.10 mm vs smallest dimension 80.0 mm
  [PASS] leather thickness in range      1.20 mm (0.4-4.0)
  [PASS] pieces generated                1 piece(s)
```

Supported nodes: `rect`, `circle`, `stadium`, `polygon`, `svg_path` (any bezier or
arc), plus `union`, `difference`, `intersection`, `offset`, `translate`, `rotate`,
`mirror`, `scale`, `repeat`. See `reference/spec.md`.

## Use — from a sketch

Words cannot carry proportions, so the drawing is the input:

```bash
python3 scripts/sketch_to_spec.py sketch.jpg --out ./brief/   # paper sketch + ISO card
python3 scripts/sketch_to_spec.py sketch.svg --out ./brief/   # vector, exact
python3 scripts/build_piece.py brief/spec.json --out ./brief/cut
```

Emits `brief.json`: panels in millimetres, detected cutouts, an `assumed` list, and
a `questions` list. **The questions are the point** — a corner radius comes back as
a band (`9.5 mm, 5.7-13.0`) because a pencil wobbles about 1 mm, which is the same
order as the whole plausible range. The skill instructs the agent to ask, not assert.

Verified on a synthetic sketch (110 × 85 mm panel, r=12, thumb notch + window):

| quantity | truth | traced |
|---|---|---|
| panel size | 110 × 85 mm | 109.0 × 84.5 (−0.9 %) |
| cutouts | notch + window | 2 ✓ |
| corner radius | 12 mm | 9.5 mm, reported as a band, flagged to confirm |
| stitch pitch | — | snapped to a standard iron, confirmed with user |

End to end it produced a 1:1 PDF with the notch followed by 93 stitch holes, the
window cut, and the calibration square intact.

## Use — known products

```bash
python3 scripts/build_wallet.py --style bifold --cards 6 --leather-t 1.0 \
        --pitch 3.85 --out ./wallet_out
```

## From a photo

```bash
python3 scripts/inspect_photo.py photo.jpg --debug debug/
```

Requires an ISO bank card in frame as scale. Returns panel size, corner radius,
measured stitch pitch snapped to a standard iron, edge offset, hole count. **Refuses
to run without a valid card** rather than returning confidently wrong millimetres.

## Verified

| test | truth | result |
|---|---|---|
| generic silhouette (bezier) | — | builds, gates pass |
| window case, cutout + stitches | — | 2 CUT polylines, 62 stitches, no conflict |
| all 11 primitive/op nodes | — | build correctly |
| photo, panel | 123.4 × 84.4 mm | 125.4 × 86.2 (+1.6 %) |
| photo, pitch | 3.38 mm | 3.329 → snapped 3.38 |
| photo, holes | 112 | 112 |
| bad pitch, bad thickness, unknown node, malformed JSON | — | exit 2 / 2 / 1 / 1 |
| inset deeper than half-width | — | exit 1 with the real minimum |

## Honest limits

- **Flattening 3D → flat is out of scope.** Developable surfaces (cones, cylinders)
  flatten exactly; doubly-curved forms do not flatten without distortion, because
  leather does not stretch. Flatten once in Rhino/Blender, feed the outline in as
  `svg_path`. See `reference/construction.md` §2.
- Photo intake and sketch intake are tested on **synthetic** input only. Real
  pencil on real paper, with shadows and perspective, is untested. Expect the size
  error to be worse than the 1 % measured here.
- Corner radius from a sketch is an estimate. It cannot be measured from a pencil line.
- The tracer finds *enclosed* regions, so an open stroke is refused rather than guessed.
- Assembly, hardware placement, and thread are construction knowledge, not computed.
- Always build a felt mock before cutting leather.
