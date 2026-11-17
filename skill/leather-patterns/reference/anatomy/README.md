# Hide and skin anatomy — a taxonomy for pattern makers

A hide is not a sheet. It is a **map of a body**: thickness, fibre weave, follicle
density, stretch direction and surface quality all change with position, and they
change on different axes. Every "use the good part" rule in leathercraft is a
compressed version of that map.

This folder exists because a pattern is only as good as the assumption it makes about
the material. `constraints.md` tells you what a fold can survive. `durability.md` tells
you how it fails. **This folder tells you which part of the animal you are asking to
do the work.**

## The five levels — and why conflating them is the main source of confusion

Trade vocabulary mixes five different axes under one flat list of nouns. "Culatta",
"bend" and "shell" look like the same kind of word. They are not: one is a **commercial
cut**, one is a **body region**, one is a **layer through the thickness**.

| Level | Axis | Examples | Answers |
|---|---|---|---|
| **L0** | Animal | species, breed, age, sex, husbandry | how big and how dense |
| **L1** | Body region | neck, shoulder, fore shank, belly, flank, back, butt, hind shank, cheek, head, tail | where on the body |
| **L2** | Commercial cut | whole hide, side, back, crop, double shoulder, bend, double bend, butt, culatta, belly, strip, front, shell | what a supplier will sell you |
| **L3** | Layer | grain (papillary), grain–corium junction, reticular corium, **hyaline layer** (equine only), flesh split | which depth |
| **L3.5** | **Hard parts** | osteoderms, scales, scutes, denticles, quill bumps, nails and hooves | what is *hard* inside the skin — **exotic leather needs this level; bovine does not** |
| **L4** | Direction | parallel / perpendicular to the backbone; the "line of least stretch" | which way the fibres run |

**The rule: a term belongs to exactly one level, and a specification must name all
applicable levels.** "Vegetable-tanned shoulder" leaves L2 and L4 unspecified.
"Double shoulder, 1.2 mm, cut parallel to the backbone, 3–4 oz" does not.

Two consequences worth internalising:

- **An L2 cut is not a homogeneous material.** A *side* is a bag containing nearly every
  L1 region, including the offal. Buying a side buys the map, not a sample of it.
- **The same L2 name has different outlines at different suppliers** (see
  `taxonomy.md`, "Term conflicts"). Culatta is the worst offender; it is a genuine
  different region in the bovine trade and the equine trade.

## Files

| File | What is in it |
|---|---|
| **`reference-matrix.md`** | **Everything as text, in five matrices:** all ~45 species · property→species lookup · every term with its level · failure-mode index · shape-constraint matrix. Start here if you want one file. |
| `taxonomy.md` | The full bovine term list, sorted by level. Including the conflicts. |
| `properties.md` | What actually varies within a hide, and by how much — with numbers and the counter-evidence. |
| `horse.md` | The equine case in full: front, strip, butt, culatta, shell. The most structured hide in the trade. |
| **`appendages.md`** | **L3.5 — hard parts.** Osteoderms, scales, denticles, quills, nails. Why a plated hide fails differently. |
| **`species/`** | **One file per animal group.** All the animals, with their own vocabulary: `bovine`, `equine`, `ovine-caprine`, `porcine`, `ostrich`, `crocodilian`, `reptile-snake`, `fish-stingray`, `kangaroo-deer-other`. |
| `sources.md` | Where each claim comes from, and how much to trust it. |
| `plate-01.svg` | Labelled diagram: bovine L1 regions and L2 cuts; equine front / butt / strip / shell; two through-thickness stacks. |
| **`plate-01.md`** | **The same plate, written out.** Every label, band, cut line and caption as text. |
| `plate-02.svg` | Six hard-part surface types; ostrich "one bird, four materials" with the foot detail; four failure-mode diagrams; the replacement rule. |
| **`plate-02.md`** | **The same plate, written out.** |

**Nothing in this folder is picture-only.** Each plate has an `.md` twin, and
`reference-matrix.md` carries the same content as tables.

## The short version, for a pattern spec

| Part of the product | Region to ask for | Why |
|---|---|---|
| Large flat outer panel | **bend / butt**, one continuous piece | densest, most uniform weave; least stretch |
| Fold or hinge (spine, gusset) | **butt**, cut **parallel to the backbone** | the line of least stretch; folds roll instead of warping |
| Long narrow strap, handle, belt | **back**, parallel to backbone | tension along the fibre direction |
| Card slots, thin flexing tongues | **shoulder** or a **bend split** | thin, but not the loose belly weave |
| Hidden lining, stiffener, non-structural | **belly** | cheap, thin, stretchy, and nobody sees it |
| Never for a visible flat panel | **neck**, **shank**, **belly** | neck wrinkle and growth marks, shank is dense but small and curved, belly sags |

## Coverage

**Species with their own treatment:** cow steer bull ox calf kip buffalo bison zebu yak · horse
colt pony donkey mule · goat kid sheep lamb · pig hog peccary · kangaroo deer elk moose camel
llama alpaca rabbit · cane toad elephant hippo seal walrus + fur-bearing · ostrich emu rhea
chicken turkey duck goose · crocodile alligator caiman snake lizard teju turtle tortoise ·
stingray shark salmon cod haddock perch wolffish eel sturgeon tilapia pirarucu pacu catfish carp
plaice parrotfish dolphinfish moray boxfish puffer.

Where a source names a species but **no reliable anatomy exists**, it is listed with a `~` and
no invented detail — see `reference-matrix.md` §1 and each file's "Honest limits".

## The exotic caveat

Everything above is a **bovine** answer. It assumes a hide that is a continuous soft sheet.
Three other kinds of animal break that assumption, and each breaks it differently:

| Kind | Examples | What breaks |
|---|---|---|
| **Plate-armoured** | crocodilian, stingray, ostrich leg | the surface is hard islands in a soft matrix; failure is at the **interface**, and the fold-strain screen is meaningless |
| **Fold-scaled** | snakes and lizards | scales are folds of the skin with **free edges**, so the failure mode is **lift**, not crack |
| **Narrow strips or tubes** | snake, salmon, ostrich leg, shell cordovan oval | **shape** dominates the layout, not region |

And the one that inverts the folk rule: on **goat and sheep the shoulder is the strongest
region, not the rump** — a properly significant result that the bovine heuristic hides.
See `species/ovine-caprine.md`.

## Hard parts are the real difference

If you remember one thing about exotic leather: **a quill is soft, a scute is hard, and an
osteoderm is brittle.** They are three different materials and they get three different
failure modes. `appendages.md` separates them.

**And the caveat that keeps this honest:** "butt is strongest" is repeated everywhere
and is only partly true. See the counter-evidence in `properties.md` — the largest
within-hide strength survey found no region that was consistently strongest across
animals, and peak tensile strength has been measured in the **flank**, not the butt.
What the butt reliably gives you is **uniformity, thickness and low stretch**, which
is what a flat pattern actually needs. Prefer the claim you can defend.
