# The property matrix — treatment → what changes

**This is the reference the rest of the folder exists to support.** The user's question was
*"how does it change the qualities of the leather"*; this file answers it as a lookup.

## How to read it

**Every row is a treatment. Every column is a property. The cell is the direction and size of
the change.**

| Symbol | Meaning |
|---|---|
| **↑↑ / ↑** | increase, strongly / moderately |
| **↓↓ / ↓** | decrease, strongly / moderately |
| **—** | no material effect |
| **↕** | moves within a trade-off (see the note in the cell) |
| **?** | direction uncertain or source-dependent |

Columns, with what each really means:

| Column | Property | Test that would settle it |
|---|---|---|
| **SOFT** | softness / pliability | stiffer-vs-softer hand; flexural rigidity |
| **STR** | tensile and tear strength | ISO 3376 tensile, ISO 3377 tear |
| **ELONG** | elongation and stretch | elongation at break; lastometer |
| **FORM** | shape retention / firmness | — (sets the "will it hold a fold" question) |
| **H2O** | water resistance, water uptake, water spotting | ISO 5403; hydrostatic ISO 811 |
| **HEAT** | heat stability | **shrinkage temperature, ISO 3380** ✓ |
| **GRAIN** | grain tightness and break | visual break on lastometer dome |
| **PATINA** | tendency to change with use and age | — (qualitative) |
| **BREATH** | air and moisture vapour permeability | ISO 14268 |
| **ABRADE** | surface abrasion resistance | Taber (ASTM D7255 / DIN 53863), Martindale |
| **FLEX** | flex-fatigue resistance | **Bally flex, ISO 5402-1:2022** |
| **AREA** | area yield and dimensional stability | — |
| **COST** | process time, cost, labour | — |

---

# 1 · Beamhouse levers

| Treatment | SOFT | STR | ELONG | FORM | HEAT | GRAIN | COST | Notes |
|---|---|---|---|---|---|---|---|---|
| **Heavy liming** | ↑↑ | ↓ | ↑ | ↓ | — | ↓ loose | ↑ | swelling opens structure; the softness lever |
| **Light liming** | ↓ | — | ↓ | ↑↑ | — | ↑↑ tight | — | sole/belt route |
| **Long bating (enzymes)** | ↑↑ | ↓ | ↑ | ↓ | — | ↓↓ **empty grain risk** | ↑ | irreversible |
| **Minimal bating** | ↓ | — | ↓ | ↑ | — | ↑↑ | ↓ | |
| **Full degreasing** | ↑ (even) | — | — | — | — | ↑ (no grease spots) | ↑ | essential on sheep/pig |
| **Incomplete degreasing** | ? | ↓ | ? | ↓ | — | ↓↓ | ↓ | uneven dye, greasy spots — **unfixable** |
| **Splitting thick (grain split)** | ↓ | ↑ | ↓ | ↑ | — | ↑ | ↑ | keeps more corium |
| **Shaving thin** | ↑* | ↓↓ | ↑ | ↓ | — | ↓ | ↓ | *thinner = floppier, but **weaker**; see skiving paradox |
| **Unhairing — hair-saving** | — | **↑** (32.1 MPa) | **↑** (64.2 %) | — | — | **↑ cleaner grain** | ↑ | **strongest of the four routes** ✓~ |
| **Unhairing — conventional sulphide** | — | baseline (30.3 MPa) | baseline (60.5 %) | — | — | baseline | — | the reference route |
| **Unhairing — painting** | — | — (30.3 MPa) | **↓** (41.5 %) | — | — | — | ↑ | lower elongation than the others |
| **Unhairing — oxidative** | — | **↓↓** (21.8 MPa) | **↓↓** (39.6 %) — grain-crack test FAILED | — | — | ↓↓ | — | **~28 % weaker in tensile, ~15 % in tear** ✓~ |
| **Enzymatic unhairing** | — | ↑ | — | — | — | ↕ **more buffing effect, uneven dye** ✓ | ↑ | greener effluent, not a free upgrade |
| **Pickling (pelt state)** | — | — | — | — | ↓↓ | — | — | the raw material for transparent leather |

---

# 2 · Tannages — the biggest single lever

| Tannage | SOFT | STR | ELONG | FORM | **HEAT (Ts)** | **H2O** | PATINA | GRAIN | COST | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| **Chrome (Cr III)** | ↑↑ | ↑↑ | — | ↓ | **↑↑ >100 °C** (110 °C onset, 52 J/g ✓~) | **↑↑ >1500 mm hydrostatic** ✓~ | **↓↓ none** | ↑ uniform | ↓ fast, 24–48 h | 80–90 % of world ✓ |
| **Vegetable** | ↓↓ | ↑ (dense) | ↓ | **↑↑** | **↑ 70–85 °C** ✓ | **↓ ~600 mm** ✓~ | **↑↑ strong** | ↑ | ↑↑ 30–60 d | toolable; water-spots |
| **Aldehyde / wet-white** | **↑↑ softest** (flexural rigidity <2–2.5 N·m ✓~) | — | — | ↓ | ↑ >85 °C | **↓↓ <300 mm** ✓~ | ↓ none | ↑ | ↑ | **UV yellowing**; needs more dye+fatliquor |
| **Synthetic (syntan alone)** | ? | ? | ? | ? | — | — | — | — | — | supplementary, not standalone ✓ |
| **Combination (veg + chrome)** | ↑ | ↑ | — | ↑ | ↑ ~100–112 °C ✓~ | ↑ | ↑ some | ↑ | ↑ | sequence matters; uneven-tan risk |
| **Alum / tawing** | ↑ | ↓ | — | ↓ | ↓↓ **reverts in water** | **↓↓ poor** | — | — | — | **not a true tannage** |
| **Brain / smoke** | ↑↑ | ↓↓ | ↑↑ | ↓↓ | ↓ | ↓ | ↑ | ↓ | ↑ | very soft, not structural |
| **Oil / chamois** | ↑↑ | ↓ | ↑ | ↓↓ | ↓ | ↕ **absorbent** | — | ↓ | ↑ | washable, polishing |
| **Zeolite-based** | — | — | — | — | **69 °C / 15 J/g** ✓~ | — | — | — | — | |
| **Aluminium triformate** | — | — | — | — | **68 °C / 22 J/g** ✓~ | — | — | — | — | |
| **Tara + zeolite blend** | — | tear **15.9 N**, stretch **42.3 %** ✓~ | ↑ | — | **98.6 °C** ✓~ — **beats Cr–Al 89.1 °C** | — | — | — | ↑ | best metal-free result found |
| **THPS + LA** | — | — | — | — | 82.6 °C ✓~ | — | — | — | — | |
| **THPS + veg + Al** | — | — | — | — | **110 °C** ✓~ | — | — | — | ↑ | the metal-free route to chrome-level Ts |

**The single most useful line in this table:** Tanning is the only window that **raises heat
stability**, and nothing else in the process raises it much. A leather's Ts is essentially its
tannage. Everything in windows 3 and 4 can lower it and nothing can raise it substantially.

---

# 3 · Post-tanning levers

| Treatment | SOFT | STR | ELONG | FORM | H2O | GRAIN | AREA | COST | Notes |
|---|---|---|---|---|---|---|---|---|---|
| **Deeper neutralisation** | — | — | — | — | — | — | — | — | **controls depth** of everything below ✓ |
| **Vegetable retan** | ↓ | ↑ | ↓ | **↑↑ firm** | ↓ | ↑ | — | ↑ | the "make it firmer" lever ✓ |
| **Resin / syntan retan** | ↑ | — | ↑ | ↓ | ↑ some | ↑ fuller | — | ↑ | can feel plastic |
| **Heavy filling agents** | ↑ | ↑ (apparent) | — | ↑ | — | ↓ covered | — | ↑ | artificial hand |
| **More fatliquor, deeper** | **↑↑** | ↓ | ↑ | ↓ | ↑ some | **↓↓ coarser break** ✓ | — | ↑ | **the central trade-off** |
| **Less fatliquor** | ↓↓ | ↑ | ↓ | ↑ | ↓ | ↑↑ tight | — | ↓ | stiff; cracks if worked |
| **Fatliquor 60–66 °C, 30–40 min** | ↑ | — | — | — | — | — | — | — | the standard condition ✓ |
| **Toggle / paste drying** | ↓ | ↑ | **↓↓** | ↑↑ | — | ↑ | **↑↑** | ↑ | flat and stable |
| **Hang drying** | ↑ | — | ↑↑ | ↓ | — | ↓ | ↓ | ↓ | softer, less area |
| **Vacuum drying** | ↓ | — | ↓ | ↑↑ | — | ↑ | ↑ | ↑ | fast, firm, flat |
| **Conditioning to 18–28 %** | — | — | — | — | — | — | — | — | prerequisite for staking ✓ |
| **Staking** | **↑↑** | ↓ slight | ↑ | ↓ | — | ↕ opens | — | ↑ | breaks drying bonds ✓ |
| **Milling / dry drumming** | **↑↑** | ↓ | ↑ | ↓↓ | — | **↕ raises and rounds** ✓ | ↓ slight | ↑ | the "milled grain" look |
| **Buffing — grain side (nubuck)** | ↑ | ↓ (thin) | — | — | **↓↓ absorbs** | **↓↓ removed** | — | ↑ | nap |
| **Buffing — flesh side (suede)** | ↑ | ↓ | — | — | **↓↓** | ↓↓ | — | ↑ | flesh split as face |
| **Shaving to final thickness** | ↑ | **↓↓ below a floor** | ↑ | ↓ | ↓ | ↓ risk | ↑ yield | — | **skiving paradox** |

---

# 4 · Finishing levers

| Treatment | SOFT | BREATH | ABRADE | H2O | FLEX | PATINA | GRAIN | COST | Notes |
|---|---|---|---|---|---|---|---|---|---|
| **Full aniline** | ↑ | **↑↑** | ↓ | ↓↓ | ↑ | **↑↑** | ↑ natural | — | stains |
| **Semi-aniline** | — | ↑ | ↑ | ↑ | — | ↑ | ↕ | ↑ | scratchable ✓ |
| **Pigmented / protected** | ↓ (film) | **↓↓** | **↑↑** | **↑↑** | ↕ film cracks | **↓↓** | ↓↓ covered | ↑ | least porous ✓ |
| **Heavy topcoat (patent)** | **↓↓** | **↓↓↓ none** | ↑↑ (until it cracks) | ↑↑ | **↓ film fails first** | ↓↓ | ↓↓ | ↑ | a structural layer on thin leather |
| **Pull-up wax film** | — | ↓ | — | ↑ | — | **↑↑ via wear** | — | ↑ | **micro-cracks reveal lighter base** ✓ |
| **Oiling / waxing** | ↑ | ↓ | — | **↑↑** | ↑ | ↑ darkening | ↑ | ↓ labour | re-apply; attracts dirt |
| **Plating / hot press** | ↓ | ↓ | ↑ | ↑ | — | ↓ | **↑↑ set** | ↑ | flattens character |
| **Glazing / ironing** | — | ↓ | ↑ | ↑ | — | — | ↑ gloss | ↑ | |
| **Embossing** | ↓ | — | ↑ | ↑ | — | ↓ | **↑↑ imposed** | ↑ | **hides defects** ✓ |
| **Hand burnishing (edges)** | — | — | **↑↑** | ↑↑ | ↑ | ↑ | — | ↑ labour | **veg-tan only; far more durable** |
| **Edge paint** | — | — | ↓ | ↑ | **↓ chips at flex** | — | — | ↓ | a consumable, not a finish |
| **Backing / interlining** | ↓ | ↓ | ↑ | ↑ | ↑ | ↓ | ↑ | ↑ | **non-recoverable panel** |

---

# 5 · Maker-applied treatments

| Treatment | SOFT | STR | GRAIN | ABRADE | BREATH | FLEX | Notes |
|---|---|---|---|---|---|---|---|
| **Laser cut** | ↓ at edge | **↓↓ at edge** | — | — | — | ↓ edge | charred brittle edge; **0.5 mm feature floor** ✓ |
| **Perforation** | ↑ slight | **↓↓ along the hole line** | — | — | **↑↑** | ↓↓ at line | a **tear line**; anisotropic |
| **Emboss / deboss (design)** | ↓ | — | ↑ imposed | — | — | — | 0.2–0.5 mm relief ✓; needs firm leather |
| **Engrave** | ↓ | ↓ | — | — | — | ↓ | 0.5–2 mm ✓; darkens **or** lightens ✓ |
| **Wet forming** | ↓↓ | ↓ | ↑ set | — | ↓ | ↓↓ | veg-tan only; **3D, non-flattenable** |
| **Pleating / heat set** | ↓↓ | ↓ at crease | ↑ | — | — | ↓↓ | firm leather only |
| **Smocking / shirring** | ↑↑ | — | — | — | — | ↑ | **1.8–3× area cost** |
| **Hot foil stamping** | — | — | — | ↓ wears | — | — | **not on aniline** |
| **Natural dye + alum mordant** | — | — | — | — | — | — | pulls tannins out; alters receptivity ✓ |
| **Natural dye + iron mordant** | ↓ **brittle** | **↓↓ over decades** | — | — | — | ↓ | **the 5–10 year caveat** ✓ |
| **Direct acid dye (transparent work)** | — | ↑ **as filler** ✓ | — | — | — | — | dye acted as a filler in the shadow-puppet study |

---

# 6 · Avant-garde

| Treatment | SOFT | STR | HEAT | H2O | Notes |
|---|---|---|---|---|---|
| **Transparent — polyol fill** | ↕ | **↓** | **↓↓ Ts 50–70 °C** ✓~ | **↓ leaches in water** | 50–85 % transmittance claimed ~ |
| **Transparent — in-situ IPN** | ↕ | ↓ (routes criticise swelling route for low strength) | ↓↓ | ↑ **fixes the leaching** ✓ | the current answer |
| **Transparent — ionic liquid + calendering** | ↕ | ? | ? | ? | least documented route |
| **Glycerin impregnation (shadow puppet)** | **↓↓ rigid** | ↑ (dye as filler) | ↓ | ↕ | deliberately **semi**-transparent + stiff ✓ |
| **Photochromic coat** | — | — | — | — | passive, reversible, ageing coating ✓ |
| **Thermochromic microcapsules** | — | — | — | — | **25–50 °C**, finite cycles ~ |
| **Cholesteric LC (Bragg)** | ↑ smoother surface ✓ | — | — | ↑ good water-drop ✓ | **37–40 °C**, 0.75–1.25 g/m² ✓ |
| **Electrochromic stack** | ↓ | — | — | — | **needs conductive layer + power** ✓ |
| **Conductive (polypyrrole)** | — | — | — | — | **turns black**; wears ✓ |
| **Biofabricated (not leather)** | — | — | — | — | **no material meets animal-free + plastic-free + durable + biodegradable** ✓ |

---

# 6b · Hair-on, wool-on, shearling

Against the same skin dehaired. Detail in `09-hair-on-shearling.md`.

| Treatment | SOFT | STR | ELONG | H2O | ABRADE | FLEX | Cut | Notes |
|---|---|---|---|---|---|---|---|---|
| **Hair-on (any species)** | skin ↑ | **↓↓ skin is thin** | ↑ | **↓↓ wicks** | **↓↓ pile matts** | ↓ | **special** | nap direction is a spec; edges shed |
| **Wool-on / unsheared sheepskin** | skin ↑ | ↓↓ | ↑ | ↓↓ | ↓↓ | ↓ | **special** | insulation is the point |
| **Shearling (sheared)** | skin ↑ | ↓↓ | ↑ | ↓↓ | ↓↓ | ↓ | **special** | **pile length is the spec number**; no edge paint |
| **Double face** | ↑ | ↓↓ | ↑ | ↓↓ | ↓ | ↓ | **special** | both sides functional |

---

# 6c · Not leather (for comparison)

Not treatments — materials that get patterned as if they were leather. Detail in
`10-not-leather.md`.

| Material | STR | ELONG | ABRADE | FLEX | Repairable | Notes |
|---|---|---|---|---|---|---|
| **Full grain leather** | ↑↑ | ↕ | ↑↑ | ↑↑ | ↑ | the reference |
| **Split / "genuine leather" + coating** | ↓ | ↕ | ↕ coating-dependent | ↓ | ↓ | **the film is the failure mode** |
| **Bonded leather** | **↓↓** | ↓ | ↓ | **↓↓ delaminates** | **↓↓** | **frays at cut edges** — the field test |
| **PU on fabric** | ↓ | ↕ | ↕ | ↓ | ↓ | coating delamination |
| **Microfibre** | ↑ | ↓ | ↑↑ | ↑↑ | ↓ | **uniform and stable — easier to pattern than leather**, but no grain, no patina, no burnish |
| **Plant-based / mycelium (PU-coated)** | ? | ? | ↕ | ? | ↓ | **re-validate the pattern; do not assume leather mechanics** |

---

# 7 · The five trade-off families

Almost everything above belongs to one of five zero-sum levers. **If you remember nothing else,
remember these:**

| # | Lever | Gives | Takes |
|---|---|---|---|
| **1** | **Softness ↔ grain tightness** | more fatliquor, deeper → softer | **coarser break**, looser grain ✓ |
| **2** | **Firmness ↔ flexibility** | veg retan, tight drying, less fat | stiffness, water sensitivity, cracking |
| **3** | **Protection ↔ breathability** | pigment + topcoat | **breathability, patina, repairability** ✓ |
| **4** | **Heat stability ↔ everything else** | chrome | patina, environmental cost, slower routes |
| **5** | **Optical/functional novelty ↔ mechanical performance** | transparency, conductivity, colour change | **strength, Ts, colour, cycle life** |
| **6** | **Structural integrity ↔ area yield** | splitting thin, shaving, toggling | **strength, flex life** — the skiving paradox |
| **7** | **Reversibility ↔ performance** | retanning, coating, embossing, iron mordant | **you cannot undo it** — see `03-post-tanning.md` part 2 |
| **8** | **Hair as a face ↔ skin as a structure** | leaving the hair on | the skin is thin, weak, and a carrier |

**A spec that claims to win two sides of a lever is claiming a material that does not exist.**
When a supplier claims soft *and* tight-grained, or stain-proof *and* breathable, or transparent
*and* strong — the right response is not disbelief, it is a request for the measurement.

---

# 8 · Using this to write a spec

Turn a desired property set into a treatment plan by reading the matrix **backwards**:

**"I need a firm, dense, edge-burnishable leather that will patina."**
→ veg or veg-retan, low fatliquor, toggle-dried, restrained bate, full- or semi-aniline finish.
Cost: water-spots, stiffness, and it will darken.

**"I need a soft, drapey, waterproof lining."**
→ chrome, no veg retan, generous fatliquor, milled, no coating (it is a lining).
Cost: **coarse break** — do not expect a crisp edge.

**"I need a thin, light, foldable panel that survives flexing."**
→ chrome, aldehyde, or combination; **not veg**; fatliquor for flex; **no perforation on the fold
line**; expect edge paint, not burnishing.

**"I need a surface that resists stains and wipes clean."**
→ pigmented finish with PU topcoat, chrome substrate.
Cost: no patina, lowest breathability, the film is the thing that will fail.

**"I need something nobody has."**
→ read section 6, then read its cost column. There is always a cost column.

**If you know the end use rather than the properties**, start at `11-end-use-index.md`
instead — it goes the other way, from object to treatment stack, and then tells you what the
stack costs.
