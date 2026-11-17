# Blender: what it can and cannot do for leather

**There is no Blender plugin for leather goods.**
(And to be fair to the field: leather *has* been simulated properly — by Fraunhofer
ITWM and by the Simucal group. See `durability.md` §1a. Just never as a Blender add-on,
because every one of those models needs per-hide calibration data.) No add-on knows about grain
direction, skiving, pricking irons, edge paint, or fold allowance. What exists is a
healthy cloth ecosystem with a preset that happens to be called "leather".

---

## 1. The preset is not a material model

Blender ships a **Cloth → Leather** preset. Its actual values:

| preset | vertex mass | tension stiffness | bending stiffness |
|---|---|---|---|
| Leather | 0.4 kg | 80 | 150 |
| Cotton | ~0.3 kg | 15 | 0.5 |
| Silk | low | ~5 | ~0.5 |

That is a **stiffness slider wearing a leather name.** It captures one true thing —
leather is stiff in bending relative to cloth — and nothing else. It has no
orthotropy (leather bends differently along vs across the backbone), no thickness
dependence, no viscoelastic creep, no finish layer, no damage.

Use it to make a render look plausible. Do not use it to answer a question.

### Why cloth solvers fight leather

Leather is **nearly inextensible** — 5–15 % across the hide, almost nothing along it.
Cloth solvers are tuned for fabrics that stretch freely, and they go unstable or
"rubbery" when you push tension stiffness high enough to be leather-like. Cloth Lab's
own docs have a troubleshooting section literally titled *"If the cloth looks like
rubber"*. That is the engine telling you it has left its calibrated range.

---

## 2. The add-ons that actually exist

| add-on | what it does | price / licence | honest use for leather |
|---|---|---|---|
| **Seams to Sewing Pattern** (Thomas Kole) | mesh + UV seams → sewing pattern → **SVG export**, plus cloth sim, tension view in the UV window | free | 3D form → flat pattern. UV-unwrap based, so it inherits unwrap distortion. Built for Blender 2.8/2.9; works unreliably on 4.x/5.x. A GPLv3 remaster exists (`artyredd/blender-seams-to-sewing-pattern`) |
| **Garment Tool** (bartoszstyperek) | build from **2D bezier curves**, stitch them, triangulate, simulate; reports **mismatched sewn segment lengths**; bind tool for pockets and bags | free / paid tiers | the closest to the real leather workflow: design flat, assemble, simulate |
| **Simply Cloth Studio 2.0** (Vjaceslav Tissen) | cut & sew, sewing system, wrinkle generator, presets incl. leather | ~$36–46, MIT | fastest route to a decent drape. Blender 4.0–5.2 |
| **Cloth Lab** (SLOHERO) | free cloth + garment tool, **dynamic tension-driven tearing**, fold analysis, A/B sewing boundaries | free, GPL-3.0 | the only near-miss on "stress test" — see the caveat below |

### The one interesting feature

**Cloth Lab's dynamic tearing** (experimental XPBD, Blender 5.2+) separates the mesh
under tension. It is the only thing in the ecosystem that responds to load by failing.

**The caveat:** the tear threshold is an arbitrary number you set, not a calibrated
material property. It has no relationship to an ISO 5402 flex cycle count. It tells
you *where* a load concentrates, which is genuinely useful. It does not tell you *how
long* the part lasts. Do not present it as fatigue analysis.

---

## 3. The honest division of labour

```
skill (build_piece.py)                     Blender
----------------------                     -------
exact 2D geometry            ----SVG--->   import as curves
cut files at 1:1 mm                        assemble, sew, simulate
stitch pitch / edge offset                 drape and silhouette check
fold allowance pi*t                        find the pinch points
gates on numbers                           render for the client
```

**Blender is the renderer and the intuition pump. The skill is the measuring
instrument.** Neither replaces the felt mock, and neither predicts durability.

### The concrete loop that works

1. Build the panels with `build_piece.py` → `pattern.svg`
2. Blender → **File > Import > SVG as Curves**
3. Garment Tool (or Simply Cloth) → stitch the boundaries, triangulate
4. Add cloth with high bending stiffness, pin the seams, simulate
5. Look for: pinching where a radius is too tight, gussets buckling, corners that
   cannot sit flat
6. Fix the **spec**, regenerate, re-import

Step 5 is the entire value. You are looking for geometric infeasibility that a
drawing hides — not for physics.

---

## 4. Two gotchas that waste days

**Scene scale.** Cloth stiffness values in Blender are only meaningful if the scene
is at real scale in metres. Model a 200 mm wallet as 200 units and every stiffness
number is wrong by six orders of magnitude. Set unit scale and scale the object
before touching physics.

**SVG curves import as n-gons.** You must triangulate before cloth will behave. Use
even, densely triangulated meshes — all the garment add-ons do this for you precisely
because a bad triangulation makes the sim buckle.

---

## 5. So what should you actually use?

| question | tool |
|---|---|
| "what do I cut?" | **the skill** — build_piece.py → SVG/DXF/1:1 PDF |
| "will it look right?" | Blender + a garment add-on |
| "where does it pinch?" | Blender, or just check the radius gates |
| "will the hinge crack, and when?" | **neither.** Compute `ε = t/(2R+t)`, then ISO 5402-1 flex test a real sample |
| "how thick does it get closed?" | the skill's stack gate |

If someone tells you a Blender plugin will validate a leather pattern, they are
describing a render.
