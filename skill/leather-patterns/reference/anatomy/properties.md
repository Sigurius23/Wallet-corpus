# What actually varies across a hide — and by how much

This file is deliberately separated from the taxonomy, because **the vocabulary is
self-consistent and the numbers are not.** Every claim below is attached to a study so
you can see where it stops being true.

---

## 1. Tensile strength varies 4–7× within one hide

The cleanest measurement available: **10 chrome-tanned nappa sheepskins, sampled with a
press knife into 2,147 specimens**, every value mapped in MATLAB ✓.

| | mean | min | max |
|---|---|---|---|
| Tensile strength, perpendicular samples | 9.66 N/mm² | **2.98** | **21.71** |
| Tensile strength, parallel samples | 9.33 N/mm² | 4.52 | 18.22 |
| Elongation at break, perp. | 57.3 % | 30.3 % | 91.0 % |
| Elongation at break, parallel | 74.9 % | — | — |

**4 to 7× strength variation over the area of the same leather.** The UNIDO minimum for
chrome-tanned garment leather is 10 N/mm² — so **the same hide passes or fails depending
which square you cut the specimen from**. That is the single most important number in
this folder.

Note the direction result: elongation is **higher parallel** (74.9 vs 57.3 %), which is
the **opposite** of the classic "higher elongation perpendicular" rule. Direction
effects are real but not even consistent in sign between studies and species. Do not
build a precise model on them.

Also from that study: strength is **highest near the backbone and falls gradually
toward the edges**; **the kidney area is weaker than the neck area**.

## 2. But "the butt is strongest" does not survive a proper survey

The largest systematic attempt to map strength across whole hides ✓ sampled **two
animals each** of ovine, bovine and cervine by grid, measuring tear strength in two
orthogonal directions plus SAXS fibril orientation, 31–56 tear specimens per hide.

Findings:

- **"In none of the species could a part of the hide be identified that had
  consistently higher strength than another."**
- **"There were no obvious regions of generally stronger or weaker skin."**
- Overall strength ranking by species: **cervine > bovine > ovine**.
- Ovine had the **greatest within-skin variability**.
- Predominant fibril direction was **perpendicular to the backbone in all three species**
  (which is itself in tension with the "fibres run along the backbone" statement — see
  §5).

And a second, older survey of location effects on upper leather (8 locations: neck,
shoulder, front shank, belly, butt, official butt, back shank, tailend) reports **highest
tensile strength in the middle of the flank and adjacent positions, lowest in the tail
area** ~ — again, not the butt.

### So how do both things stay true?

Because **"best part of the hide" in the trade means four different things**, and only
one is tensile strength:

| What the butt actually is | Reliably true? |
|---|---|
| **thickest** | yes ✓ |
| **densest / finest weave** | yes ✓ |
| **lowest and most uniform stretch** | yes ✓ |
| **most uniform over area** | yes ✓ — and this is what a flat pattern needs |
| supports the **highest peak load before tearing** | **contested** — depends on animal |

**Use this framing in a spec.** "Butt is strongest" is a folklore compression of "butt is
the most *consistent*". Consistency is the property that makes a cutting layout safe.
Peak strength is a property you cannot rely on from a region name at all.

The honest, useful claim: **strength is not predictable from location alone; uniformity
is.** For a flat good — where the failure you care about is a hinge creasing or a panel
sagging, not a tensile rupture — uniformity is the relevant property. Say that, and you
are defensible.

## 3. Thickness — anatomy gives you a range, the tannery gives you the number

- Bovine dermis **4–8 mm** thick ✓ (vs 1–2 mm human dermis); epidermal layer 0.1–0.2 mm ✓
- Follicle density: **~80/cm² at the butt → ~200/cm² at the belly** ✓, with follicles
  implanted **3–6 mm** deep, and posterior guard hairs at greater depth in the butt
  and shoulder (5–6 mm)
- Fresh hide thickness ranges commonly quoted: backbone **4.5 mm+**, sides ~3.5→2.5 mm,
  belly **3 → 0.8 mm**, shoulder 3–4.5 mm ~ — **forum figure, unsplit hide, illustrative only**

> **Do not put a location-based thickness in a spec.** Splitting and shaving set the
> delivered thickness deliberately, because "hides have considerable variations in
> thickness between the butt, shoulders, neck and belly areas, and between individual
> hides" ✓. A split leather can be near-uniform in *mm* while wildly non-uniform in
> *behaviour*. Buy the thickness; respect the weave.

## 4. Collagen density and weave angle

- Fibre thickness: **higher in back and neck (up to 194.2 µm) than abdomen (~150.3 µm)** ✓
- Goat skin grain layer is **24–54 % of total thickness**, varying by region (table in
  `taxonomy.md` L3) ~
- **Angle of weave** — the inclination of fibre bundles to the surface — is what sets
  hardness and stretch, and it varies by region ✓. In goat it is a **low angle even in
  the butt** ~, which is why goat reads as "tight" everywhere.

Angle of weave is the mechanism behind everything in §2. Dense + low angle = firm, flat,
non-stretch. Loose + high angle = supple, directional, sagging.

## 5. Direction: the rule, and its three asterisks

The rule: fibres run predominantly **parallel to the backbone**, giving **higher tensile
parallel, higher elongation perpendicular** ✓.

The asterisks, in order of how much they should change your behaviour:

1. **Asterisk 1 — it is measured at one point.** Max/min stretch direction is defined at
   the **OSP (ISO 2418)**; elsewhere on the hide **the direction rotates** ✓. A single
   "cut parallel to the backbone" instruction is only exact at the OSP.
2. **Asterisk 2 — the sign flips.** The 2,147-specimen sheepskin study found elongation
   **higher parallel**, not perpendicular ✓. Either species or tannage matters more than
   the textbook says, or the "rule" is grain-relative and gets inverted by processing.
3. **Asterisk 3 — fibril orientation ≠ fibre bundle orientation.** SAXS measures
   *fibril* orientation, which came out **perpendicular to the backbone in all three
   species tested** ✓. Histology measures *bundle* weave. These are different scales and
   they do not have to agree. When someone says "the fibres run along the backbone",
   ask which fibres.

Practical translation: **treat direction as a strong first-order effect for long parts
(straps, belts, hinges) and as unreliable for fine layout decisions.** Measure the
piece you are about to cut if the part is structural.

## 6. Anisotropy magnitude, if you want a number

- Glutaraldehyde-tanned leather: tensile **8.9 MPa perpendicular vs 14 MPa parallel**;
  extension **106 % perpendicular vs 47 % parallel** ✓ — i.e. **~1.6× in strength,
  ~2.3× in extension**, purely from cut direction
- Coefficients of variation for tensile strength in those tests: **0.31 (aldehyde), 0.44
  (chrome)** ✓ — a CV of 30–44 % *within a single leather* tells you the scatter is not
  noise you can average away with 3 specimens
- Tear strength, by contrast, **varies little with sampling angle** ✓ — so tear and
  tensile anisotropy are not the same phenomenon

That last point is the one to carry into `../durability.md`: a **tear** failure and a
**tensile** failure in the same leather will have different directional dependence, so a
single "grain direction" arrow on a pattern is an oversimplification of both.

## 7. Surface, not bulk: where the defects live

Region quality is also a *surface* claim, and the surface is graded separately:

- **Neck/shoulder:** natural growth marks, fat wrinkles, and neck creasing ~. Wanted for
  rustic goods, disqualifying for a clean flat panel.
- **Belly:** thinnest, most stretchy, and the most defect-prone area — holes, creases,
  irregular thickness ~.
- **Shanks / legs:** dense but small and strongly curved; also where butcher cuts from
  hide removal land.
- **Peripheral edges generally:** more scratches and nicks because they were nearest the
  environment ~.

Natural markings (fine scars, healed scratches, veins, grain variation, insect bites)
are **expected** on full-grain aniline and veg-tan, and only reduce grade when deep or
central ~. **Defects reduce value where they intersect the cutting area that matters** —
which is a statement about your layout, not about the hide.

---

## The three sentences to use

1. **Strength varies 4–7× within one hide** (2,147 specimens, sheepskin), so a region
   name cannot guarantee a strength number.
2. **No region is consistently strongest across animals** (two-animal-per-species survey,
   three species) — what the butt reliably gives is **uniformity, thickness and low
   stretch**, and that is what a flat pattern needs.
3. **Direction matters more than region for long parts**, but its maximum/minimum are
   defined only at the OSP and the direction rotates across the hide.

## What to do differently in the pattern

| Situation | Action |
|---|---|
| Long strap or belt | one piece, butt/back, along the backbone. Never spliced from belly |
| Hinge that must not stretch | butt; verify against the strain screen in `../durability.md` |
| Large flat panel | bend or butt, one continuous piece; check the actual hide for the kidney-area weakness |
| Thin flexible slots | shoulder or a split; not belly for anything that will be pulled |
| Lining, stiffener | belly. This is what belly is for |
| Nesting to save area | you may rotate **non-structural** parts only. Rotating a structural part trades away a measured property |
