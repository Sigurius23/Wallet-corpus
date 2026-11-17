# Wallet Pattern Corpus

A research and prototyping corpus for measuring flat leather goods from photographs
and generating dimensioned wallet patterns. It brings together synthetic test data,
reconstruction scripts, parametric pattern tools, reference material, and example
exports.

> **Scope and accuracy:** The quantitative reconstruction examples are primarily
> synthetic. They are useful for reproducing the documented experiments, not evidence
> of validated performance on real leather goods. Always check dimensions and make a
> test cut before using a pattern.

## What is here

### Photo reconstruction and evaluation

| Path | Contents |
|---|---|
| `reconstruct.py` | Deterministic OpenCV pipeline: calibrates from ArUco markers, rectifies the photo, measures the panel and stitch holes, and exports a pattern and report. |
| `make_synthetic.py` | Creates a perspective-distorted synthetic capture and its exact metric ground truth. |
| `make_blind_test.py` | Generates a synthetic blind-test example. |
| `synthetic/` | Synthetic photo, exact `ground_truth.json`, and matching `ground_truth.dxf`. |
| `blind/`, `cardtest/` | Additional test photos with their annotation JSON files. `blind/cv_out.txt` is a preserved run log; its scorer invocation is incompatible with the annotation schema and is not a successful benchmark result. |
| `results_raw.json`, `results_comp.json` | Saved reconstruction measurements and comparisons for the synthetic case. |

### Pattern generation

| Path | Contents |
|---|---|
| `leatherkit/` | Lightweight Python wallet-pattern library for bifolds and card holders; exports SVG, layered DXF, tiled 1:1 PDF, and JSON. |
| `skill/leather-patterns/` | Agent skill and detailed references for making general leather patterns, building from sketches, and inspecting photos. See its [README](skill/leather-patterns/README.md) for installation and commands. |
| `leather-patterns-skill.zip` | Packaged copy of the leather-patterns skill; its unpacked contents are in `skill/leather-patterns/`. |
| `out_wallet/` | Example bifold pattern and parameter report. |
| `out_wallets/` | Example outputs for a card holder, 8-card bifold, Japanese 4-card bifold, and slim 6-card bifold. Each folder contains SVG, DXF, 1:1 PDF, and a JSON report. |
| `example_wallet.py` | Small `leatherkit` usage example. |

### Reference and visual assets

- `wallet-reconstruction-feasibility.md` records the architecture, experiment results,
  limitations, and research notes.
- `pattern-making-tools-report.html` is a report on pattern-making tools.
- `wallet-pattern-reference-sheet.pdf` and `page*.png`, `wallet_pdf_p*.png`,
  `check_metric.png`, `jp1.png`, and `sketch_test.jpg` are visual/reference materials
  and rendered pages.
- `build_wallet_ref.py` builds a printable wallet reference sheet.
- `workspace-*.zip` is the original source bundle from which this repository content
  was unpacked.

## Reproduce the synthetic reconstruction

The top-level reconstruction scripts require Python 3 and `numpy`, an OpenCV
contrib build (for ArUco support), and `ezdxf`. The headless OpenCV package is
sufficient for these command-line scripts:

```bash
python3 -m pip install numpy opencv-contrib-python-headless ezdxf
python3 make_synthetic.py
python3 reconstruct.py synthetic/photo.jpg \
  --truth synthetic/ground_truth.json \
  --edge-comp 0.6 \
  --out out
```

`make_synthetic.py` writes the synthetic photo and its exact JSON/DXF geometry to
`synthetic/`. `reconstruct.py` writes its measurement and pattern outputs to `out/`;
the optional `--truth` argument scores measurements against annotations, and
`--edge-comp` compensates for the simulated burnished-edge bias. Run
`python3 reconstruct.py --help` for all options.

The saved result in `results_raw.json` reports 96 holes recovered after deduplication
and a snapped 3.85 mm stitch pitch. The documented outline and dimension errors are
from synthetic input and should not be interpreted as real-world accuracy guarantees.

## Use the pattern tools

For general pattern building, photo intake, and sketch workflows, follow the
requirements and examples in [skill/leather-patterns/README.md](skill/leather-patterns/README.md).
The standalone wallet library and its output formats are described in
[leatherkit/README.md](leatherkit/README.md).

The already-generated patterns in `out_wallet/` and `out_wallets/` can be inspected
without installing Python dependencies. Print 1:1 PDFs at **actual size / 100%** (not
“fit to page”) and verify the included calibration square before cutting.

## Notes on data and reuse

- `synthetic/ground_truth.json` uses millimetres and describes the synthetic scene,
  marker layout, panel outline, and stitch-hole positions.
- The test folders contain different annotation layouts; do not assume the blind-test
  JSON uses the same schema as `synthetic/ground_truth.json`.
- No dataset split or real-world validation protocol is defined here. Treat these
  files as examples and experiments, not as a ready-to-train or production-certified
  dataset.
- No repository-level license is provided. Check the rights and license of each
  bundled document, asset, script, and dependency before redistributing or using it
  commercially. The research notes are informational, not legal advice.
