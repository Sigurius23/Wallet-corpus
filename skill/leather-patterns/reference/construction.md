# How to build a leather good that isn't a wallet

`build_piece.py` gives you geometry. This file gives you the **construction
knowledge** to know what geometry to ask for. Two things, in order: how leather
behaves, and how a 3D object becomes flat panels.

---

## 1. Where leather differs from sheet metal

Sheet-metal unfolders assume this and leather violates every one:

| sheet metal | leather |
|---|---|
| bends are **straight** lines with a constant bend allowance | bends are **any** curve; allowance varies along the bend |
| material **yields** and stretches to fit | material **does not stretch** — it gathers, compresses, or wrinkles instead |
| thickness is uniform and machined | thickness varies 5–10 % across one hide, more between hides |
| a flat pattern is a mathematical certainty | a flat pattern is a **first attempt**; the finish changes the size |
| you compensate for **springback** | you compensate for **stretch, skiving, and burnishing** |

**The practical consequence:** never trust a computed flat pattern for a curved 3D
form the way you would trust a sheet-metal flat. Build the flat, cut it in cheap
material (2 mm felt, card stock, scrap veg-tan), assemble, and correct. The kernel
makes that iteration cheap — one spec edit, one re-cut — which is the actual value.

### Thickness effects that must be modelled

- **Fold allowance** — a fold consumes about `π × t` of flat length. The kernel adds
  it; the gate checks `π × t` exactly.
- **Stack-up at a seam** — two 1.2 mm panels sewn edge-to-edge need the seam to
  accommodate 2.4 mm of butt-joined material, or 4.8 mm if the seam is a lap.
- **Corner radius must exceed thickness.** Below about `3 × t` a burned or folded
  corner cracks, and the edge paint will not hold.
- **Skiving** — anywhere a panel tucks behind another, skive the edge to ~0.4 mm or
  the finished piece has a visible step. This is the single most common reason a
  correct pattern makes a bad object.

### Shrinkage and stretch, by type

| leather | behaviour | how to compensate |
|---|---|---|
| veg-tan | takes water, sets hard, shrinks 2–5 % when drying wet-formed | cut wet-formed pieces 3 % oversize, trim after drying |
| chrome-tan garment leather | 5–15 % stretch across the hide, almost none along | orient long panels along the spine direction |
| oil-tan / pull-up | compresses and creases permanently at a fold | do not fold tight; allow a full-radius turn |
| bridle / harness | stiff, minimal stretch | patterns hold to ±1 mm |
| suede | stretches both ways, edges fray | line it, or use a turned edge everywhere |

---

## 2. Turning a 3D object into flat panels

This is the step the skill does **not** automate, and the step that decides whether
the result is right. Three routes, in order of how well they fit leather.

### Route A — design flat, reason about the 3D (best for most goods)

For bags, pouches, cases, sleeves: start from **flat panels that you know assemble
into the form**, rather than from a 3D model you have to flatten.

**The two-panel rule.** A pouch, sleeve, or simple bag is almost always two identical
panels sewn around their perimeter, with an optional gusset between them:

```
finished width  W  →  panel width  = W + seam allowance × 2
finished height H  →  panel height = H + seam allowance × 2
```

**Gussets.** A gusset is a strip whose width equals the depth you want. Its length
equals the perimeter of the opening it joins — measure it along the stitch line, not
the cut line:

```
gusset_length = perimeter of the mating panel's stitch line
gusset_width  = finished depth + 2 × seam allowance
```

For a rounded-corner body, the gusset must be **shorter at the cut line than at the
seam line** — the kernel gives you both; offset the body inward by the seam allowance
to get the curve you need. Get this backwards and the gusset ruckles.

**Box corners.** To give a flat-bottomed bag corners, cut a square or a wedge from each
bottom corner of the panel. The depth of the removed square is the finished depth.
`difference` with a rect or an SVG path does this in one node.

### Route B — flatten a 3D surface (needed for curved, non-developable forms)

A surface that is **developable** (curved in one direction only — cylinders, cones)
flattens exactly. Anything curved in two directions (a dome, an organic bag body)
**cannot** be flattened without distortion, because leather will not stretch.

Tools that do the flattening properly, and their real costs:

| tool | flatten quality | headless / scriptable | licence |
|---|---|---|---|
| **Rhino + `UnrollSrf`** | exact for developable surfaces | via `Rhino.Compute` (REST), not plain Python | Rhino licence; **$0.10/core-hour** on servers, core-hour only on Linux |
| **Blender + Papercraft/PolyZamboni** | triangulated unfold, seams respected | yes, `bpy` is scriptable headless | GPL-3.0 add-ons |
| **libigl / ARAP flattening in Python** | good, with measurable distortion | yes, pure Python bindings | MPL-2.0 |
| **Poisson / BFF** | near-conformal, excellent for organic | C++ CLI | MIT-ish academic |

**Honest assessment:** for a leather good, Route B is worth it only for genuinely
curved forms (a moulded holster, a seat, a curved bag side). For a wallet, a bag, a
case, or a sleeve it is a slower, more fragile path to the same panels Route A gives
you directly. If the design *is* curved, flatten it once in Rhino or Blender, export
the flat outline to SVG or DXF, and feed that outline into `svg_path`.
That is the intended boundary: **flattening happens outside, cutting happens here.**

### Route C — trace a photo (route already built in)

`scripts/inspect_photo.py` measures an existing item from a photo with an ISO card
in frame. Use it when the user has a physical object to reproduce the *proportions*
of. It will not recover a 3D form.

---

## 3. Assembly patterns worth knowing

| construction | flat pattern looks like | watch for |
|---|---|---|
| **Bifold wallet** | outer panel = 2 × pocket width + fold allowance; interior = stacked pockets | stack-up; the fold is the wear point |
| **Card holder** | one panel, two T-slots folded up | slot leather must be thin (≤0.8 mm) |
| **Two-panel pouch** | two identical panels | corners ruckle if radius < 3t |
| **Gusseted bag** | two panels + one gusset strip | gusset must be cut to the stitch-line perimeter |
| **T-slot / card pocket** | panel with two vertical slots and a folded tab | slot ends need rounding or they tear |
| **Box corner bag** | panel with corner squares removed | removed square = finished depth |
| **Turned-edge sleeve** | panel + lining, sewn outside in, turned through a gap | add 0 of seam allowance but subtract the turn radius |
| **Tool roll** | long panel + flap + tie or elastic loops | slot pitch must match tool diameters |
| **Round-bottom circle** | circle + strip gusset | strip length = π × d at the seam line |
| **Belt / strap** | long stadium + buckle holes | holes at a repeat; end in a point or round |

---

## 4. Order of operations that avoids rework

1. **Fix the contents.** Measure the objects going in, plus 2 mm clearance each side.
2. **Fix the leather thickness.** Everything downstream depends on it.
3. **Choose the construction** from §3, which fixes the panel count.
4. **Compute the panels** at the *stitch line*, then offset outward by seam allowance.
5. **Add the hardware** last — rivets, snaps, D-rings all want their own holes.
6. **Generate, then build a felt mock.** Cheap. Always.
7. **Correct the spec, regenerate.** One edit, one re-cut.

The mock step is not optional and the kernel is built to make it fast.
