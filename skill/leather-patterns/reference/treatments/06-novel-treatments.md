# Treatments a maker applies — the design layer

Everything above happens at the tannery. **This file is the set of treatments a designer or
workshop applies to finished leather** — the ones that change the material after it is bought.

These are the treatments that interact most directly with a pattern, because most of them are
**cut-path or surface operations whose behaviour depends on the geometry of the part.**

---

## 1. Cutting and its alternatives

| Method | Edge character | Notes |
|---|---|---|
| **Hand knife / head knife** | clean, slightly bevelled, forgiving | the reference edge |
| **Rotary / die clicker** | clean, vertical | production; needs a clicker die per size |
| **CNC drag knife / tangential blade** | clean on straight and gentle curves | **fails on tight radii** — the blade cannot pivot fast enough |
| **Laser** | **seared, hard, dark edge**; smell | see below |
| **Waterjet** | clean, no heat | wet; not common on leather |
| **Ultrasonic** | sealed edge on thin leather | specialist |

### Laser, in detail

Laser is popular because it is fast and file-driven, and it changes the leather in ways a pattern
must account for ✓:

- **The cut edge is charred and brittle.** It is a different material from the leather behind it.
  It does not take edge paint the same way and it dusts.
- **Minimum practical feature size.** Below **~0.2 mm** the laser becomes unreliable; **0.5 mm**
  is the figure quoted for reliable results ✓. Any pattern with thin bridges, fine slots or
  small holes must be checked against this.
- **Heat-affected zone.** The leather immediately beside the cut is dried and stiffened. On a
  thin leather this can be most of the thickness.
- **The backside scorches.** Cutting leather needs **backing or pasting flat** to avoid marking
  the reverse ✓.
- **Engraving is not cutting.** Engraving 0.5–2 mm depth is a surface relief ✓.

**Pattern consequence:** a laser-cut part with a 0.4 mm slot is a part that will break. Treat the
laser's feature floor as a design constraint, exactly like a minimum radius.

---

## 2. Perforation and cut-work

Punched holes, from the classic **broguing** repp sizes through to engineered graphic perforation.

| | Effect |
|---|---|
| **Aesthetics** | pattern, light transmission, texture |
| **Mechanical** | **each hole is a stress concentration and a tear-initiation site.** A row of holes is a perforated tear line — the leather tears along it under load |
| **Direction** | holes also introduce **anisotropy**: a line of holes across the stretch direction tears far sooner than one along it |

**Pattern rule:** perforation belongs **away from load paths and hinge lines**, or as an
intentional line of weakness (e.g. a tear-off tab). Do not perforate a fold that will be flexed
thousands of times — you have pre-cut the crack.

The same applies to **stitch holes**: an unsewn row of holes is a tear line. This is why
perforated leather goods need backing or lining through the perforated area.

---

## 3. Emboss and deboss — as a design tool

Distinct from tannery embossing (which imitates grain). Here it is deliberate relief ✓:

| | Depth | Character |
|---|---|---|
| **Emboss / deboss** | **0.2–0.5 mm relief** ✓ | crisp shapes, logos, textures; works well on firm leather |
| **Engraving** | **0.5–2 mm** ✓ | deeper, more graphic; can cut through on thin leathers |

**Practical rules:**

- **Firm, dense leather takes relief; soft leather does not.** A soft leather will not hold a
  crisp emboss — the relief relaxes out.
- **Engraved leather darkens *or* lightens** depending on the finish and the laser/heat ✓ — you
  cannot predict which without testing. Test a scrap from the same hide.
- **Exotic and heavy-grained leather disrupts engraving** — the natural surface fights the
  pattern; **emboss instead** ✓.
- **Parchment-finished leather engraves white and slightly raised** ✓ — a genuinely useful
  contrast effect, and one of the few reliable light-on-dark operations.

---

## 4. Heat and water forming

- **Wet forming / moulding.** Vegetable-tanned leather soaked and pressed over a form holds the
  shape as it dries — this is the mechanism behind masks, cases and holsters. **Chrome-tanned
  leather does the same thing worse**; the tannin matrix is what sets.
- **Boiling / hardening.** Historically, boiled leather (cuir bouilli) hardened into a rigid
  armour material. Modern equivalents are resin-impregnated. This is leather deliberately taken
  out of its material class.
- **Thermo-forming.** Some finished leathers can be heat-vacuum formed; the finish cracks unless
  it is formulated for it.

**Pattern consequence:** a wet-formed part is a **3D form**, not a flat pattern. It cannot be
flattened back without distortion — see the doubly-curved-surface rule in the main skill.

---

## 5. Pleating, folding and smocking

- **Hand pleating** requires a **shape-retaining (firm or veg-retanned) leather** and heat setting.
  Soft leather will not hold a pleat.
- **Knife pleats / accordion pleats** are set with heat and pressure; the crease is permanent
  because the leather is being **plastically deformed at the fold** — the same mechanism as a
  permanent crease anywhere else.
- **Smocking and shirring** gather leather on elastic or thread. The leather must be **thin and
  soft**, and the gathers are a permanent area reduction: **a smocked panel uses much more
  leather per finished area than its flat measurement suggests.** Budget 1.8–3× depending on
  gather ratio.
- **Mille-feuille / mille** (layered, sliced-and-spread constructions) and **splicing**
  (piecing leather into a larger sheet) are both **area multipliers** — they let small skins
  become large panels. They also create **many seams**, each one a place the leather can fail.

---

## 6. Metallics, foil and coatings applied after manufacture

- **Foil stamping / hot foil.** Heat + pressure transfers a metallic or pigment film. Bonds to
  the finish, not the leather — **on an aniline leather it will not hold**.
- **Screen printing / hand painting.** Sits on top, wears at flex points.
- **Airbrushing and patination.** Cosmetic; a matched-but-not-identical technique.
- **Edge paint vs burnishing.** **Edge paint** is a film — it chips and peels at flex; it is the
  only option on chrome-tanned and on multi-layer edges. **Burnishing** (sanding + gum/wax +
  friction) fuses the leather's own fibres and is **far more durable**, but only works on
  **vegetable-tanned or firmly veg-retanned leather** with a solid fibre structure.

> **This is one of the most consequential choices in the whole folder for small goods.** An edge
> that will be handled daily should be burnished if the leather allows it. Edge paint is a
> consumable maintenance item, not a permanent finish.

---

## 7. Stitching and reinforcement

Not a leather treatment, but it changes the material's behaviour and belongs here as a warning:

- **Every stitch line is a row of stress concentrations.** A seam does not just join; it
  **perforates**.
- **A stitched fold is stiffer than an unstitched fold**, because the thread resists opening.
  This changes the drape of the whole panel.
- **Backing / interlining** (leather board, salpa, bonded reinforcement) is the standard way to
  make thin leather behave like thick leather, or to stabilise an area that will be perforated
  or stressed. It also makes the panel **non-recoverable** — a lined panel cannot be re-shaped.

---

## Summary — maker-applied treatments and their pattern consequences

| Treatment | Improves | Costs | Pattern consequence |
|---|---|---|---|
| Laser cut | speed, file-driven accuracy | charred brittle edge, heat zone | respect a **0.5 mm feature floor** |
| Perforation | look, breathability | tear initiation, anisotropy | keep off load paths and live folds |
| Emboss | texture, branding | needs firm leather | relief 0.2–0.5 mm |
| Engrave | graphic depth | cuts structure; colour unpredictable | 0.5–2 mm; test colour |
| Wet forming | 3D shape | non-flattenable, chrome does it poorly | 3D form, not a flat pattern |
| Pleating | structure, surface | needs firm leather | area multiplier |
| Smocking | elasticity, fullness | area cost, soft leather only | **budget 1.8–3× area** |
| Foil / print | decoration | bonds to finish, wears at flex | not on aniline |
| Edge paint | works on any leather | chips, is maintenance | not for high-wear edges |
| Burnish | fused, durable, repairable | veg-tan only | **preferred for handled edges** |
