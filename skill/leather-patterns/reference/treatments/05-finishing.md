# Window 4 — finishing

Finishing builds a **surface** on the leather. It is the window that decides how the object
looks and how it survives the world — and it is the window that most often quietly destroys the
material properties the other three windows paid for.

**The governing trade-off of this entire file:** *a finish that resists stains and wear is a
finish that seals the surface, and a sealed surface does not breathe.*

---

## The finish spectrum: aniline → patent

The industry classifies leather by **how much coating is on it**. This is a ladder, and every
rung trades natural character for protection.

| Level | What is on the surface | Stain resistance | Breathability | Patina | Scuff behaviour |
|---|---|---|---|---|---|
| **Full aniline** | dye only, no pigment, no film | **lowest** ✓ | highest | **strongest** — it darkens and burnishes with use | scuffs buff out; absorbs everything |
| **Semi-aniline** | dye + a **thin** pigment coat, often with a print | medium | medium | some | a fingernail scratch shows ✓ |
| **Pigmented (protected)** | dye + **opaque pigment + resin topcoat** | **highest**; "least porous, most stain-resistant, most fade-resistant" ✓ | **lowest** | almost none | scuffs sit on the film; can look plasticky |
| **Pull-up** | **wax/oil film over a lighter pigment base** | medium | low–medium | **the point of it** — see below | scratches reveal the lighter core, then blend ✓ |
| **Patent** | heavy lacquer — a mirror film | very high for liquid | **none** | none | the film itself can crack and lift |
| **Nubuck / suede** | **no coating** — sanded surface | **low** — nap absorbs ✓ | high | yes, and it stains | nap scuffs; not cleanable |

**Semi-vegetable and "washed"/"vintage" finishes** sit at the natural end: extra finishing steps
to create **uneven colour, a broken-in look and a supple hand** ✓. They are a *style* claim, not
a durability claim.

---

## The pull-up mechanism

Worth its own section because it is the clearest example of a treatment whose visible behaviour
*is* its construction:

**A pull-up leather is a lighter-coloured pigmented base covered with a wax/oil film.** When the
leather flexes or is stretched, the **wax film micro-cracks and the lighter core shows
through** ✓. That is the "pull-up" — you are seeing the base coat through a cracked film.

Consequences a pattern maker should know:

- **The effect is stress-drawn.** It shows up at fold lines, at the mouth of a pocket, wherever
  the pattern puts strain. On a tightly patterned piece it reads as wear; on a loose piece as
  character.
- **It is not repairable, only blendable** — warmth and rubbing redistribute the wax.
- **It photographs beautifully and cleans badly** — the wax holds dirt.

---

## The finish stack, from the leather outwards

Industrial finishing is a sequence of layers, each with a job ✓:

| Layer | Job | Typical chemistry |
|---|---|---|
| **Impregnation / base coat** | seal the grain, stop the topcoat sinking in | acrylic or polyurethane dispersion — this is also where **softening fillers** can be added |
| **Ground coat** | colour and opacity | pigment + binder |
| **Print / emboss** | texture — often applied to the coated surface with a release paper or plate | — |
| **Top coat** | wear and stain resistance, the hand you feel | nitrocellulose lacquer (traditional), polyurethane, acrylic, silicone |
| **Fixative / feel modifiers** | slip, waxy hand, matt/gloss control | — |

**Two places this matters for a design:**

1. **Where the finish is and is not.** The finish covers the grain side and, on better goods,
   the edges and flesh side get some treatment too. **A cut edge always shows the substrate.**
   Any design that relies on the leather looking the same at a cut needs to say so.
2. **The finish has a thickness.** A pigmented finish with a heavy topcoat measurably changes
   the **bend behaviour** of a thin leather — the film is stiffer than the leather. On a 0.8 mm
   leather, a patent finish is a structurally significant layer, and it is the layer that fails
   first in flexing (film cracking, not leather cracking).

---

## How to identify what you are looking at — the water-bead test

A field method, and a good one ✓:

**Put a drop of water on the surface.**

| Result | Finish |
|---|---|
| **Absorbs immediately, darkens the spot** | aniline, nubuck or suede — no film |
| **Beads, sits on the surface** | semi-aniline, pigmented, or patent — there is a film |

It is a screening test, not a measurement, but it correctly separates the two families that
matter. (And it also tells you something about the object: water-beading leather is leather that
will not patina.)

---

## Mechanical and surface finishes

These are treatments applied by machine or hand to the surface, and they do not add a coating.

| Treatment | Method | Effect | Cost |
|---|---|---|---|
| **Plating** | hot press plate, ~80–100 °C, pressed flat | smooths, sets the grain, glazes | flattens natural grain character |
| **Ironing / glazing** | hot iron or glass roller | **gloss and a crisp surface** | — |
| **Embossing** | heated plate or roller with a pattern | **permanent surface texture**, 0.2–0.5 mm relief ✓ | hides defects — and **is used to**; embossed "grain" is not the animal's grain |
| **Roller printing** | engraved roller | continuous pattern | — |
| **Buffing** | abrasive, grain or flesh side | nubuck or suede nap ✓ | removes the protective layer (see `03-post-tanning.md`) |
| **Milling** | dry drum tumbling | softness + **raised, rounded grain** ✓ | dimensional stability |
| **Hand-burnishing** | friction + gum/tokonole/wax on edges | sealed, glossy edge | labour |
| **Waxing / oiling** | surface application | water resistance, pull-up, darkening | re-application needed; attracts dirt |
| **Glazing / "museum calf"** | hand-applied glaze over a mottled base | depth and variation | cosmetic only |

### Embossing and the honesty problem

**A huge fraction of "grained" leather is embossed, not natural.** Standard embossed patterns —
including the classic names for pebbled and printed grains — are plates and rollers, applied to
corrected-grain leather. This is not fraud; it is a legitimate way to make a lower-grade hide
usable and consistent.

But it means: **"full grain" and "embossed grain" are different claims**, and a pattern that
assumes the grain will behave a particular way at a fold is assuming something about a printed
film. See `06-novel-treatments.md` for emboss as a design tool rather than a correction.

---

## What the finish changes, and what it cannot

| Finish buys | Finish pays |
|---|---|
| Stain resistance | breathability |
| Colour consistency across panels | natural variation and character |
| Wear resistance on the *surface* | the ability to repair by burnishing |
| Water repellency | the ability to patina |
| Defect hiding | honesty about the hide |
| A crisp, uniform look at scale | a plastic hand at the extreme |

**What the finish cannot do:** make weak leather strong. A finish is a film tens of microns
thick on a 1 mm substrate; it does not carry load. A heavily finished leather feels protected and
fails at the same force as the same leather unfinished.

---

## Specifying a finish

```
FINISH  full aniline, dye only — will patina, will stain, will darken
FINISH  semi-aniline, light pigment — consistent colour, some patina, wipes clean
FINISH  pigmented, PU topcoat — maximum stain resistance, no patina, lowest breathability
FINISH  pull-up wax over pigmented base — expect stress-drawn lightening at folds
FINISH  nubuck (grain buffed) — nap, absorbs liquid, do not specify for wet use
FINISH  embossed [pattern] over corrected grain — consistent texture, not natural grain
```

## Honest limits

- The **finish ladder and its property directions are consistent** across tanning and furniture
  sources ✓ (Leather Magic, Leather Circle, Homestratosphere, Leather Naturally).
- **The water-bead test is a screening classification**, taught in the trade, not a standard.
- **"Patina" is not a measurable property** and is used inconsistently. Here it means: *visible,
  desirable change with use, arising from the leather itself rather than the finish.*
- Finish **thickness and chemistry are trade-specific**; no numbers are given because they are
  not published comparably.

---

# Part 2 — Effect finishes

Finishes that exist to produce a *look*, not to protect. They are the ones most often specified
by name and least often understood.

| Finish | Mechanism | What it does to the material | Care |
|---|---|---|---|
| **Rub-off / two-tone** | a coloured surface coat over a **contrasting base**; the top layer is designed to wear away at high points ✓ | **the colour change is the point** — it is engineered wear | cannot be restored; the wear is the design |
| **Pull-up** | wax film over a lighter pigment base; cracks under stress ✓ | see `05-finishing.md` part 1 | blendable with warmth, not repairable |
| **Shrunken / shrunk** | the leather is shrunk during processing so the grain **contracts into a raised, pebbled pattern** | thicker, more textured surface; less area | the texture is permanent |
| **Crushed / crash** | the leather is **tumbled and crushed** wet or dry to break the grain | a broken, irregular surface; usually softer | permanent; a "vintage" signal |
| **Antiqued / burnished** | contrasting wax or glaze rubbed into the grain, then buffed back | the recesses darken, the high points lighten | **the finish reveals the grain topography** — it is a legibility treatment for texture |
| **Washed / stonewashed** | tumbled with abrasive media or washed | softened and faded | permanent |
| **Pearlised / metallic** | mica or metal pigment in the coat | gloss and colour shift | a film; fails at flex like any film |
| **Patent** | heavy lacquer | mirror; **no breathability** | the film cracks before the leather does |
| **Nubuck / suede** | buffing ✓ | nap, absorbs | see `03-post-tanning.md` |
| **Hair-on / shearling** | no finish — the hair is the face | see `09-hair-on-shearling.md` | not repairable |
| **Waxed / oiled** | surface-applied wax or oil | water resistance, darkening, pull-up | re-apply; attracts dirt |

> **Three of these are "engineered wear" — rub-off, pull-up and antiqued.** They are designed to
> change. A designer who specifies one and then complains that the item looks worn in the fold
> lines has specified the wear. Put the change where the design wants it.

# Part 3 — Functional finishes

These are the finishes people buy for performance. They are real, and each has a specific limit.

| Finish | What it genuinely does | What it does not do |
|---|---|---|
| **Water repellent (DWR)** | raises the surface energy so water beads and runs ✓ | **it is not waterproof** — seams, cut edges and flex points are not covered; it wears off with abrasion and cleaning |
| **Fluorochemical DWR (C6/C8)** | the strongest water and oil repellency | **the PFAS problem** — persistent, regulated and being restricted in the EU and elsewhere ✓; a designer specifying "stain-proof" is often specifying PFAS |
| **PFAS-free / wax-based DWR** | good water repellency, lower durability | **poor oil and stain resistance** — it repels water, not grease |
| **Stain / soil release** | reduces adhesion, aids cleaning | does not prevent staining |
| **Antimicrobial / antifungal** | silver, zinc or quaternary compounds, or the cholesteric-LC effect noted in `07` ✓ | **does not sterilise**; performance fades; regulated as a biocide in the EU |
| **Flame retardant** | chemistry in the finish or the fibre | changes the hand and, sometimes, the flex behaviour |
| **Phase-change material (PCM)** | microcapsules absorb/release heat | **thermal buffering, not cooling**; adds a film |
| **Scented / aromatic** | microencapsulated fragrance | fades; not a functional claim |
| **Abrasion-resistant topcoat** | PU or silicone film | a film — breathability cost, and it is the thing that fails |
| **Anti-static** | conductive additives | same family as `07`'s conductive leather |

**Three honest rules:**

1. **DWR is a surface treatment on a surface that flexes.** The places it fails first are the
   places your pattern puts a fold.
2. **Waterproof is a construction claim, not a leather claim.** A waterproof leather in a sewn
   object with unsealed seams is not a waterproof object. Only a **construction** — seam sealing,
   taped or welded seams, no stitch perforations — makes an object waterproof.
3. **If a functional finish is load-bearing to the design, it is a maintenance item.** Ask what
   the re-treatment interval is, and design so the object is still acceptable when it has lapsed.
