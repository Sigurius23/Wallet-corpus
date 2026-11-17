---
name: leather-patterns
description: >
  Generate production-ready cutting patterns for FLAT LEATHER GOODS — any design:
  wallets, card holders, bags, pouches, cases, sleeves, straps, covers, belts, key
  fobs, phone and notebook cases, tool rolls, and one-off freeform shapes. Use when
  the user wants a sewing/stitching pattern, a cut file (SVG/DXF), a printable 1:1
  tiled PDF, or asks to "design a wallet", "make me a card holder pattern", "pattern
  for this bag", "turn my sketch into a pattern", "convert this photo into a
  pattern", or asks about stitch pitch,
  fold allowance, seam allowance, edge offset, or leather thickness. Also use when
  asked which leather a design needs, how tanning/dyeing/finishing changes a leather's
  qualities, or about transparent, chromic, conductive or other avant-garde leather
  treatments. Do NOT use for garments (shirts, trousers, dresses) — those need drafting
  blocks and drape.
version: 2.3.0
license: MIT
---

# Leather patterns — general flat-goods kernel

Any flat leather design described as a **2D outline plus stitching**. There is no
fixed menu of allowed products: you compose primitives, boolean ops, and SVG paths
into the shape you need, and the kernel emits cut files.

**You write the spec; the kernel writes the geometry.** Never hand-place a coordinate,
never estimate a millimetre by eye.

## The one rule

If a number ends up on a cutting template, it must come out of `scripts/`. When you are
tempted to write "about 90 mm", build it instead. The kernel is the measuring
instrument; you are not.

## Workflow

1. **Decompose the design into panels, then into a shape spec.** Ask for what you
   cannot infer: overall size, what goes in it, leather thickness, pitch, whether
   edges are burnished or turned. Use the defaults table for the rest and *state each
   assumption* in your reply.
2. **Build** with the general entry point:

   ```bash
   python3 scripts/build_piece.py spec.json --out ./out
   python3 scripts/build_piece.py --example pouch     # template to copy from
   ```

   The spec is a JSON tree of primitives and operations — see
   `reference/spec.md` for every node type. Anything expressible as a polygon,
   rounded rect, circle, stadium, stroked path, SVG bezier/arc path, or a boolean
   combination of those is supported.
### If the user gives you a drawing, a photo, or a sketch

**Words cannot carry proportions. The sketch is the prompt** — so do not translate
it into adjectives and do not eyeball millimetres. Trace it:

```bash
python3 scripts/sketch_to_spec.py sketch.jpg --out ./brief/     # photo of paper + ISO card
python3 scripts/sketch_to_spec.py sketch.svg --out ./brief/     # vector, exact
```

This writes `brief.json` (a structured brief, in millimetres) and `spec.json`
(ready for `build_piece.py`). Read the brief before building:

- `panels[].size_mm` — measured from the card scale, accurate to about 1 %.
- `cutouts` — enclosed loops become holes; a bite out of an edge is caught too.
- **`questions`** — what the drawing could not carry. **Ask these before cutting.**
  A corner radius reads as a band, not a number, because a pencil wobbles about
  1 mm and that swamps a 6 vs 12 mm radius. Never present the estimate as measured.
- **`assumed`** — every default you are relying on. State them in your reply.

Then build the spec and run the gates as usual. If the sketch has no ISO card in
frame the tracer refuses — ask for one; do not estimate scale from the image.

3. **Read the gates.** The script prints PASS/FAIL and **exits 2 if anything fails**.
   Never report success on a failing pattern — report the failure and the fix.
4. **Deliver files**: `pattern.svg`, `pattern.dxf`, `pattern_1to1.pdf`, `report.json`.

`scripts/build_wallet.py` remains as a shortcut for the two most common products
(bifold, card holder) when the user wants one and does not care about the details.

## Defaults

| Parameter | Default | Why |
|---|---|---|
| pitch | 3.85 mm | European standard. 3.38 mm is the Japanese/"diamond" alternative |
| stitch edge offset | 3.5 mm | 3–4 mm hand-sewn; 5–6 mm on a machine |
| outer leather | 1.0 mm | stiff enough to hold shape when empty |
| slot / lining leather | 0.7 mm | thick linings bulge the closed stack |
| seam allowance | 3.0 mm | on panels that get sewn to another panel |
| corner radius | 5 mm slots / 8 mm outer | tighter radii crack the edge finish |
| kerf | 0 mm | set 0.1–0.2 mm only for laser or CNC cutting |

## Hard constraints (warn, or refuse)

Read `reference/constraints.md` for thresholds and reasoning. In short:

- a stitch line offset deeper than the local half-width self-destructs → build fails
  with the real minimum; redesign or reduce the offset.
- `spacing_error` > 0.15 mm → the pricking iron will not follow the line.
- pitch outside `{2.7, 3.0, 3.38, 3.85, 4.0, 5.0}` → confirm with the user; the script
  flags the substitution and fails rather than snapping silently.
- closed stack above ~8 mm → warn: the piece will not sit flat.
- stitch holes landing inside a cutout → gate failure, the seam would have a gap.
- a hinge or fold with less than 2x leather thickness inside radius → warn loudly and
  report the outer-fibre strain `eps = t/(2R+t)`. Treat ~20 % as a SCREENING threshold,
  not a validated failure criterion - leather is viscoelastic and anisotropic.
  Never reassure a user about durability without reading `reference/durability.md`.

## Things to refuse

- **Garments.** Sleeves, trousers, dresses need drafting blocks and drape. Flat goods
  only. Say so and stop.

## Never do this when discussing durability

- Do not quote a flex-test cycle count as a **service life**. No S-N curve or crack-growth
  law exists for leather; there is no validated acceleration factor.
- Do not cite ISO 5402-1:2017 — it is **withdrawn**; the current edition is **2022**.
- Do not describe the Bally test as a gentle motion. The specimen is folded in half and
  the crease is severe; only the 22.5° stroke is small.
- Do not present "50k-100k cycles" as a standard threshold. ISO 5402-1 leaves the cycle
  count to the buyer's specification.
- Do not apply bovine rules to other species. On goat and sheep the strongest region is
  the SHOULDER, not the rump. On kangaroo the whole skin is effectively one region. On
  ostrich one bird gives four materials. See `reference/anatomy/species/`.
- Do not run the fold strain screen, or any continuous-sheet reasoning, on a plated or
  scaled hide. Crocodilian, stingray, ostrich leg and snakeskin are composites of hard
  parts in a soft matrix; failure is an interface problem at the plate boundary, and how
  the hard part is made decides everything. See `reference/anatomy/appendages.md`.
- Do not describe an exotic material's strength with a vendor multiple ("stingray 25x
  cowhide", "kangaroo 10x cowhide", "elephant strongest leather"). No cross-species test
  set exists; cite the mechanism instead. `reference/anatomy/sources.md` records which
  claims are quarantined.
- Do not treat a hide as uniform across its area. Tensile strength varies 4-7x WITHIN one
  hide, so a region name cannot guarantee a strength number. And do not repeat "the butt
  is the strongest part" as fact - what the butt reliably gives is uniformity, thickness
  and low stretch. See `reference/anatomy/properties.md`.
- Do not treat leather as a homogeneous sheet when the surface is failing. The finish is a
  stiff film on a compliant corium and can wrinkle at 2-12 % strain - well below the bulk
  number. See the film-substrate section in `reference/durability.md` (2b) before blaming
  the pattern for a creasing problem.
- Do not mix up wrinkles and creases. They are separate instabilities with different
  scalings: wrinkle wavelength depends on E_f/E_s, crease spacing depends only on film
  thickness. Inverting the wrong one returns a confident, meaningless number.
- Before applying any finish-spacing number, check HOW the finish failed. Crazing with no
  lifting means a well-bonded film; flaking or lifting means delamination, where the
  spacing formulae do not apply at all and the fix is adhesion. See 2c in
  `reference/durability.md`.
- Do not climb the simulation hierarchy for a wallet hinge. Rung 0 (the strain screen)
  plus a physical flex test is the answer; higher rungs are for predicting before cutting
  or explaining hide-to-hide variation.

- **Do not call transparent leather a coating, a film, or a laminated clear layer.** It
  is refractive-index matching in the BULK: the air in the fibre structure is replaced
  with a medium of RI ~1.31-1.59 to match collagen, so light stops scattering. A clear
  coating on opaque leather is not transparent leather. See
  `reference/treatments/07-avant-garde.md`.
- **Do not quote a vendor's or a patent's performance figures as a specification.** The
  transparent-leather patents claim 50-85 % transmittance, 0.5-1.5 mm and Ts 50-70 C;
  those are claims, not measurements, and **no independent mechanical testing of any
  transparent leather exists** in the sources gathered. The one figure worth carrying is
  that a claimed Ts of 50-70 C sits BELOW veg (70-85) and far below chrome (>100) -- so
  a transparent leather is a materially less heat-stable leather. Say that, not the
  transmittance.
- **Do not repeat the "full grain > top grain > genuine > bonded" ladder as if it were a
  standard.** It is an internet convention; **no trade body or regulator uses it**, and
  "genuine leather" has no regulated definition -- it generally means the material contains
  real hide, grade unstated, usually coated split. What IS regulated: bonded leather must
  not be represented as leather, and EN 15987 sets a 50 % dry-leather minimum for the word.
  Specify **full grain, corrected grain, or split + coating name** -- never "genuine
  leather". See `reference/treatments/10-not-leather.md`.
- **Do not call an alternative process "cleaner" and stop there.** Oxidative unhairing cuts
  BOD/COD ~40 % and produces a measurably weaker leather: **21.8 MPa tensile vs 30.3 for
  the sulphide route, and it failed the grain-crack test** in the study that compared them.
  Enzymatic unhairing is gentler on effluent but gives a grain more prone to the buffing
  effect and less even dye uptake. Environmentally better and mechanically worse are a
  trade-off, not an opposite. See `reference/treatments/01-beamhouse.md`.
- **Do not recommend an iron-mordanted black without the lifespan caveat.** Iron-tannin
  black is the traditional route to true black and it accelerates degradation of the
  leather over decades; craft guidance accepts it only for a 5-10 year expected life.
  Vegetable retan gives firmness but water-spots; chrome gives water resistance but no
  patina; a heavy pigment coat gives stain resistance but kills breathability. When a
  material is claimed to be soft AND tight-grained, or stain-proof AND breathable, ask
  for the measurement rather than repeating the claim. See
  `reference/treatments/08-property-matrix.md` section 7.

## Reference

- `reference/spec.md` — every spec node type, with a worked example each
- `reference/api.md` — the Python API when you need geometry beyond a spec file
- `reference/constraints.md` — design rules and why they exist
- `reference/pitches.md` — standard pricking-iron pitches and thread pairing
- `reference/sketch-brief.md` — the sketch → brief → pattern pipeline, and its limits
- `reference/durability.md` — stress, fatigue and flex testing. Read this before
  answering ANY question about whether a design will last, crack, or fail at a fold
- `reference/anatomy/` — which part of the animal you are cutting. Region, cut, layer,
  hard parts and direction are five different axes with five different vocabularies; a
  hide is a map, not a sheet. Read `anatomy/properties.md` before making ANY claim that
  one part of a hide is stronger than another, and `anatomy/species/` before assuming a
  cow's anatomy generalises — it does not for goat, ostrich, crocodilian, snake or
  stingray. `anatomy/reference-matrix.md` holds every species, term and failure mode as
  tables, and `anatomy/plate-01.md` / `plate-02.md` are text versions of the diagrams —
  use them instead of describing a picture you cannot see
- `reference/treatments/` — how leather gets its properties. Every process step, every
  tanning chemistry, every dye class, every finish, and **what each one changes**. Read
  `treatments/08-property-matrix.md` FIRST — it is treatment -> property-effect as a
  lookup table, and it is the fastest way to answer "will this leather do X?". The rest
  of the folder explains the rows: `01-beamhouse.md` (where the softness/stretch ceiling
  is set and cannot be recovered), `02-tanning.md` (the Ts ladder: zeolite 69 / veg 70-85
  / aldehyde >85 / chrome >100 C), `03-post-tanning.md` (the fatliquor trade-off),
  `04-dyes.md` (natural + synthetic, mordants, the iron warning), `05-finishing.md`
  (aniline -> patent and the breathability cost), `06-novel-treatments.md` (laser,
  perforation, emboss as design tools), `07-avant-garde.md` (transparent, chromic,
  conductive, biofabricated), `09-hair-on-shearling.md` (the family that skips unhairing),
  `10-not-leather.md` (bonded, PU, microfibre, vegan, and why "genuine leather" is not a
  grade), `11-end-use-index.md` (**the reverse index — object -> treatment stack**),
  `12-regulation.md` (what is restricted, and what certifications actually certify).
  `treatments/sources.md` continues the source record as Part 3
- `reference/blender.md` — what 3D tools (Blender, CLO, FEA) can and cannot validate
- `reference/photo-intake.md` — measuring an existing item from a photo
