# API reference

All units **millimetres**. Library works in mm with y pointing **down**; exports flip
to PDF convention internally.

## `Wallet.bifold(...)`

| param | default | meaning |
|---|---|---|
| `cards` | 6 | total capacity, split across two banks |
| `leather_t` | 1.0 | outer shell thickness → drives fold compensation |
| `slot_t` | 0.7 | card-slot leather thickness → drives closed stack |
| `pitch` | 3.85 | pricking iron; snapped to nearest standard |
| `reveal` | 8.0 | visible strip of card above a slot |
| `clearance` | 2.0 | side clearance around a card (85.6 → 87.6 slot) |
| `corner_r` | 8.0 | outer corner radius |
| `interior_gap` | 8.0 | interior shorter than outer, per open end |
| `height` / `width` | auto | override the derived panel size |

Derived values:

```
pocket_h    = ISO_CARD_H + 3.0 - reveal
step        = reveal + 2.0
interior_h  = pocket_h + step*(slots_per_bank-1) + 2.0
panel_w     = ISO_CARD_W + clearance + 2*5.0
panel_h     = interior_h + 2*interior_gap
fold_comp   = pi * leather_t
outer_w     = 2*panel_w + fold_comp
```

## `Wallet.card_holder(...)`

`cards`, `leather_t`, `pitch`, `reveal` (default 10), `corner_r` (default 3).
Body is one folded piece.

```
body_w = ISO_CARD_W + 6.0
body_h = (ISO_CARD_H + 4.0)*2 + pi*leather_t + reveal*(cards-1)
```

## `stitch_run(outline, pitch, mode)`

- `mode="variable"` (default) — `n = round(perimeter/pitch)`, pitch snaps to
  `perimeter/n`. Run closes exactly. `spacing_error = 0`.
- `mode="fixed"` — holds nominal pitch, absorbs the remainder in one gap, reports
  `spacing_error`.

Returns `StitchPattern(pitch, n_holes, perimeter, mode, spacing_error, points)`.

## `export_all(wallet, outdir)`

Writes `pattern.svg`, `pattern.dxf` (layers CUT/STITCH/FOLD/NOTES),
`pattern_1to1.pdf` (tiled A4 + calibration square + registration marks + cut sheet),
`report.json`. Returns a dict of paths.

## `Wallet.report()`

```json
{"wallet": "bifold",
 "params": {"style": "...", "cards": 6, "pitch": 3.85, "outer_w": 198.34,
            "outer_h": 86.98, "stack_closed_mm": 5.9,
            "stitch": {"pitch": 3.845, "n_holes": 140, "spacing_error": 0.0}},
 "pieces": [{"name": "01_outer_shell", "width_mm": 198.34, "height_mm": 86.98,
             "holes": 140, "folds": 1}],
 "leather_area_dm2": 2.87}
```
