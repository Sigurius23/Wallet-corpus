# leatherkit — code-CAD for flat leather goods

The pattern equivalent of `build123d`. The LLM writes parametric Python; a
deterministic kernel emits cut files. No model ever guesses a millimetre.

```python
from leatherkit import Wallet, export_all
w = Wallet.bifold(cards=6, leather_t=1.0, pitch=3.85, reveal=8.0)
export_all(w, "out_wallet/")     # SVG + layered DXF + 1:1 tiled PDF + JSON
```

## What it emits

| Output | Use |
|---|---|
| `pattern.svg` | open in Affinity / Illustrator, or feed a laser |
| `pattern.dxf` | layered CUT / STITCH / FOLD — laser, CNC, Leathercraft CAD, Seamly2D |
| `pattern_1to1.pdf` | tiled A4 with a calibration square and registration marks |
| `report.json` | every parameter, piece size, hole count, leather area |

## The parameters are the design

```python
Wallet.bifold(
    cards=6,            # capacity split across two banks
    leather_t=1.0,      # outer shell, mm -> drives fold compensation (pi x t)
    slot_t=0.7,         # card slot leather, mm -> drives the closed stack
    pitch=3.85,         # pricking iron; snapped to a standard size
    reveal=8.0,         # visible strip of card above each slot
    clearance=2.0,      # side clearance around a card
    corner_r=8.0,
    interior_gap=8.0,   # interior shorter than outer, per end
)
```

## Stitch planning, done properly

`stitch_run()` models what a pricking iron actually does:

- **variable** (default) — n = round(perimeter / pitch), then the pitch snaps to
  perimeter/n so the run closes exactly. Reports the actual pitch used.
- **fixed** — hold nominal pitch, absorb the remainder in one gap, report it as
  `spacing_error`.

You cannot fit an exact 3.85 mm pitch around an arbitrary perimeter. Every real
pattern has this problem; most tools hide it. This one quantifies it.

## Install

`opencv`/`numpy`/`ezdxf`/`reportlab`. Pure Python, all permissive licences.
