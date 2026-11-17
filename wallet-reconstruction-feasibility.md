# Wallet pattern reconstruction from a photo — feasibility note

**Question:** which app / architecture should an AI agent use to reconstruct leather
wallet patterns from photographs?

**Short answer:** no app does this. The correct architecture is *deterministic computer
vision on a calibrated capture surface*, with an LLM doing construction reasoning — not
segmentation. I built and measured a working prototype; the numbers are below.

---

## 1. Why "which app" has no answer

The only serious prior art on photo → sewing pattern is academic and garment-shaped:

| Work | Venue | What it does | Status |
|---|---|---|---|
| **SewFormer** (Sea AI Lab) | SIGGRAPH Asia 2023 | Single photo → panels + stitch relations, ~1M rendered training pairs, reported 95.7% F1 | Repo dormant since Dec 2023, no dependency manifest, multi-day setup |
| **Panelformer** | WACV 2024 | Panels from a garment **image** (not a worn body) — much closer to your case | Official code released, research-grade |
| **NeuralTailor** | 2022 | Patterns from **3D point clouds** | Superseded |

These solve a harder problem than yours. Garments need **drape, ease, pose and body
inference** from a single view — that is why practitioners in 2026 still call photo→pattern
output "a reference, not a sewable pattern."

Flat leather goods are a different problem class:

- no drape, no ease, no pose ambiguity
- the object is a **planar polygon** — its true shape is directly visible
- the features you care about (outline, stitch holes, fold lines, slot edges) are all
  **high-contrast and measurable**
- the dimensional anchors are standardised (ISO/IEC 7810 ID-1 card = 85.6 × 53.98 mm)

So the hard part isn't perception. It's **capture and calibration**.

---

## 2. The architecture that works

```
phone photo ──▶ ArUco markers (physical scale)
             ──▶ homography ──▶ metric top-down render (1 px = 0.25 mm)
             ──▶ segmentation ──▶ outline + rounded-corner radius
             ──▶ blob detection ──▶ stitch holes ──▶ PITCH recovery
             ──▶ export SVG / DXF / 1:1 PDF
                    │
                    └── LLM layer: construction inference, missing-info questions
```

**Stack**

| Layer | Choice | Why |
|---|---|---|
| Host | Python + FastAPI, Tauri or PySide6 shell | needs OpenCV, Shapely, ezdxf in-process |
| Scale | `cv2.aruco` (DICT_4X4_50) | deterministic metric frame, sub-mm reprojection |
| Segmentation | HSV gating + morphology (SAM 2 as fallback) | fast, auditable, no training data |
| Hole detection | adaptive threshold + blob filtering | lighting-invariant; black-hat fails (see §5) |
| Vectorisation | contour approx / potrace | clean SVG, not pixel soup |
| Export | `ezdxf` + SVG + tiled PDF | DXF → laser / Seamly2D; SVG/PDF → Affinity |
| Agent | vision LLM with tool calls | reasoning, not geometry |

**The LLM should not do the geometry.** Its job is what CV genuinely cannot infer:
construction class (bifold / card holder / gusseted), how many card slots are banked behind
each other, which edges are meant to pair, whether the piece is skived, and asking for
leather thickness — which is *never* visible in a photo but is required for fold
compensation (π × t).

---

## 3. Measured results

Synthetic test: 110 × 95 mm panel, R8 corners, 96 holes at 3.85 mm pitch, 3.5 mm edge
offset, on a 300 × 250 mm mat with four 40 mm ArUco markers. Photo simulated with
perspective, 2.5° roll, lighting gradient, sensor noise and JPEG compression.

| Metric | Measured | Truth | Error |
|---|---|---|---|
| Markers detected | 4 | 4 | — |
| Marker reprojection error | 0.0 mm | — | — |
| Panel width | 111.29 mm | 110.00 mm | +1.29 |
| Panel width, edge-compensated | 110.30 mm | 110.00 mm | **+0.30** |
| Panel height, edge-compensated | 95.42 mm | 95.00 mm | **+0.42** |
| Corner radius | 8.72 mm | 8.00 mm | +0.72 |
| **Stitch pitch, measured** | **3.797 mm** | **3.85 mm** | **−0.053** |
| **Stitch pitch, snapped to standard iron** | **3.85 mm** | **3.85 mm** | **0.00** |
| Edge offset (hole → edge) | 4.00 mm | 3.50 mm | +0.50 |
| **Hole count** | **96** | **96** | **0** |
| Hole diameter | 1.62 mm | 1.10 mm | +0.51 |
| Outline error, mean | 0.417 mm | — | — |
| Outline error, p95 | 0.772 mm | — | — |
| Outline error, max | 0.811 mm | — | — |

### Verdict

- **Pitch recovery is the standout result.** 3.797 mm measured from holes alone, then
  correctly snapped to the 3.85 mm European standard. No CAD tool can tell you this from
  a photo; it is a genuinely new capability.
- **Outline is accurate to sub-millimetre** (0.42 mm mean) but **biased outward by ~1.3 mm**
  because the burnished rim straddles the true cut line. A fixed 0.6 mm inset brings both
  dimensions within 0.42 mm. In production this should be a *learned* per-material offset,
  not a constant.
- **Hole count is exact** after de-duplication. Diameter over-reads by 0.5 mm because the
  burnished hole rim merges with the hole at this resolution.
- **Corner radius is the weakest number** (+0.72 mm). It is derived geometrically from the
  distance from the bbox corner to the arc (r · (√2 − 1)), which is exact for a true
  rounded corner but biased outward by the same rim effect.

---

## 3b. Objection: "can't an LLM just do this?" — tested

Fair challenge, so it was tested rather than argued. Two blind tests: geometry randomised,
photo rendered, truth written to a sealed file, model committed to an estimate from the
image alone, *then* the file opened.

### Test A — no scale reference (markers present but unread)

Truth: 122.5 x 106.5 mm, R8.4, pitch 3.85, edge offset 2.95, 109 holes.

| Metric | LLM eyeball | Error | CV pipeline | Error |
|---|---|---|---|---|
| Width | ~95 mm | **-27 mm (-22%)** | 123.77 mm | +1.27 mm |
| Height | ~83 mm | **-23.5 mm (-22%)** | 107.85 mm | +1.35 mm |
| Corner radius | ~8 mm | -0.4 mm | 9.27 mm | +0.87 mm |
| Pitch | 3.85 (guess) | right by luck | 3.819 measured | -0.03 mm |
| Hole count | ~85 | **-24 (-22%)** | 109 | **0** |

Without a metric anchor the task is not "hard", it is **undefined** — the model has no way
to know what a pixel is worth. Relative quantities (corner radius) survive; absolute ones
do not.

### Test B — ISO card in frame as the ruler

Truth: 123.4 x 84.4 mm, R7.5, pitch 3.38, 112 holes.

| Metric | LLM eyeball | Error | CV with auto-detected card | Error |
|---|---|---|---|---|
| Width | 120.0 mm | -3.4 mm (-2.8%) | 125.4 mm | +2.0 mm |
| Height | 78.0 mm | **-6.4 mm (-7.6%)** | 86.2 mm | +1.8 mm |
| Pitch | guessed 3.85 | **WRONG (3.38)** | not recovered | — |
| Hole count | ~105 | -7 | — | — |

### Conclusion

An in-frame card **is a legitimate scale anchor** and it improved eyeball accuracy from
~22% to 3-8%. That is a real result and it should be used. But:

- a cutting template needs **~0.5 mm on an 84 mm part = 0.6%**; eyeballing delivered 7.6%
- pitch and hole count were not recoverable by eye at all, and those are the numbers that
  differentiate the product
- the accurate result came from *detecting the card's contour and 1.586 aspect ratio
  programmatically* — CV using the card as an anchor, not vision reading the card

**Revised capture strategy:** offer "place a bank card beside the part" as the zero-friction
default (no printed mat, no hardware), and detect the card programmatically rather than
trusting the model to read it. Keep the ArUco mat as the high-precision option. Banknotes are
a worse anchor than cards: euro notes range 120-153 mm long, and a card is always
85.6 x 53.98 mm under ISO/IEC 7810 ID-1.

**Revised architecture:** the strongest option is an LLM **with a Python sandbox** — not
reading pixels, but writing and executing per-photo CV (CLAHE for dark leather, a different
threshold for specular highlights, fallback to markers when the card is occluded). That
adapts to real-world variation in a way this fixed pipeline cannot, and it keeps every
measured number in deterministic code.


---

## 4. What this means for the product

**The capability is real, and the wedge is narrow and defensible.** A flat-goods-only
reconstructor that outputs *measured* patterns — including the pitch and edge offset that
competitors can't produce at all — is a viable product. Garments are a different company.

**Scope the MVP brutally:**

1. One SKU class: flat bifold. One capture rig: printed mat with 4 markers.
2. 20–50 real photos with hand-measured ground truth. Everything above is synthetic.
3. Targets to hold yourself to: outline ≤ 0.5 mm, pitch exact, ≤ 3 user corrections.
4. Only then add SAM for cluttered backgrounds and the LLM construction layer.

**Do not build a CAD editor.** Export into Leathercraft CAD, Affinity (SVG/PDF only — no
native DXF import), Seamly2D, or straight to a laser service.

**Capture beats model size.** A €2 printed mat and a phone clamped overhead will beat any
model trained on hand-held snapshots. Sell the mat.

---

## 5. Findings worth keeping

- **Black-hat morphology fails here.** It merges the continuous stitch groove into one
  component, yielding a single 9118 mm² blob. Adaptive thresholding on the value channel
  separates individual holes. This is the single most important implementation detail.
- **Rectified resolution matters.** The pipeline works at 4 px/mm and breaks at 8–12 px/mm
  with the same kernel sizes. Keep S = 4 and scale kernels with S.
- **`warpPerspective` inverts intuitively.** The matrix that rectifies is the same one
  `findHomography(img → mat)` returns, composed with the px/mm scale — not its inverse.
  Verify empirically, don't reason about it.
- **Axis-aligned bounding boxes are wrong for rotated parts.** Use `minAreaRect` and rotate
  into the panel frame before measuring anything. That one change cut the width error from
  +10 mm to +1.3 mm.
- **Snapping to standard pitches is a feature, not a hack.** Makers own 3.38 or 3.85 mm
  irons. Report both the measured value and the snapped one.

---

## 6. Risks

| Risk | Mitigation |
|---|---|
| Design copying — cloning a competitor's commercial wallet from product photos | explicit UX gate + construction-class-only mode; EU design-rights exposure is real |
| Lighting / dark leather / low contrast | standardise on a neutral grey mat, add a diffuse ring light; reject low-confidence captures rather than guessing |
| Real leather ≠ synthetic | 20–50 real photos with measured ground truth before believing any number here |
| Burnished edges bias every dimension outward | per-material edge compensation, calibrated once per leather type |
| Hole detection under oblique light | adaptive threshold is lighting-invariant for gradient, not for specular highlights; detect and flag glare regions |

---

## 7. Files

| File | What it is |
|---|---|
| `make_synthetic.py` | generates the test photo + exact ground truth |
| `reconstruct.py` | the full pipeline; `--truth` scores it, `--edge-comp` compensates the rim |
| `synthetic/photo.jpg` | simulated phone photo |
| `synthetic/ground_truth.json` / `.dxf` | exact mm geometry |
| `out/pattern.svg` / `pattern.dxf` | reconstructed pattern, ready for Affinity or laser |
| `out/02_overlay.png` | visual overlay: detection vs truth |
| `out/report.json` | every measured value |
| `make_blind_test.py` | blind-test generator (sealed truth) |
| `blind/` | Test A photo + truth |
| `cardtest/` | Test B photo + truth (card as scale) |

Reproduce:

```bash
python3 make_synthetic.py
python3 reconstruct.py synthetic/photo.jpg --truth synthetic/ground_truth.json --edge-comp 0.6
```

*Measured 8 November 2026 on a synthetic scene. All figures are synthetic-input results;
real-world accuracy is unverified pending physical samples.*

---

## 8. Licensing — verified 8 Nov 2026

### Your own stack: already clear to ship

`reconstruct.py` depends only on **OpenCV (Apache-2.0, ArUco included), NumPy (BSD-3),
ezdxf (MIT)**. All permissive, no copyleft, no attribution burden in a closed product.

### Research code

| Project | Licence | Ship it? |
|---|---|---|
| SewFormer (SIGGRAPH Asia 2023) | **none — no LICENSE file** | **No.** Default copyright, all rights reserved |
| Panelformer (WACV 2024) | MIT (verified) | Yes |
| GarmentCode | MIT (verified) | Yes |
| NeuralTailor | MIT (verified) | Yes |
| SewFactory dataset / SewFormer weights | separate HF repo, no model card | Unclear — treat as unlicensed |

**SewFormer is the trap.** Most-cited, code public, looks open source, and is the one you
cannot legally build on. Re-implement from the paper if you want the ideas; do not copy code.

### Pattern CAD applications

| Tool | Licence | Note |
|---|---|---|
| Seamly2D | **GPL-3.0** (verified) | Copyleft: linking/deriving + distributing obliges you to GPL your code |
| Valentina | GPL-3.0 | Same |
| FreeSewing | **MIT** (verified) | Repo archived on GitHub in Apr 2025, migrated to Codeberg; still MIT |
| Leathercraft CAD | Freeware, closed source | Free incl. commercial use; cannot fork or embed |
| EasyPatt | Free SaaS | Proprietary |
| Affinity | Proprietary freeware | Free != open source |

### Practical rule

Permissive core (own CV + MIT/Apache deps) -> DXF/SVG output -> user opens it in whatever
CAD they like. Keep GPL tools like Seamly2D behind an **file-format boundary**
(import/export), never a linked library. `free` and `open source` are different things, and
`code on GitHub` is not a licence.
