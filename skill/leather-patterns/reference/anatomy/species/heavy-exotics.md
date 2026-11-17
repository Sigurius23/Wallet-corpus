# Heavy exotics — elephant, hippo, yak, camel, and the fur-bearing skins

Large animals whose leather is defined by **thickness and surface rather than by region**. In
this group the region map mostly stops mattering, because the raw material is thicker than any
fold you will ask it to make.

---

## Elephant — *Loxodonta africana*

The most distinctive leather in the trade, and the one where **the surface texture is
structural**.

| Property | Value | Confidence |
|---|---|---|
| Grain | **thick, coarse; a crackled network of triangle and square grooves** | ✓~ |
| Skiveability | **cannot be skived thinner than ~1.2 mm** — the deep wrinkles make it too thick | ✓ (single source, but stated as a working limit) |
| Durability | **one of the most scuff- and scratch-resistant leathers**; puncture-resistant | ✓~ |
| Hand | fairly dry; **needs regular conditioning** | ✓~ |
| Colour | dull; earthy tones | ~ |
| Legality | **CITES-listed; legal trade exists from managed populations under permit** (e.g. Zimbabwe) | ✓ |

### Why the wrinkles matter to a pattern

Elephant skin's wrinkle network is not decoration — it is **the mechanism by which a very thick
skin flexes**. The grooves are where the bending happens. So:

- **You cannot thin your way out of the thickness.** The floor is ~1.2 mm ✓, which is thicker
  than most flat-goods constructions expect.
- **Skiving to even thickness would destroy the flex mechanism** and leave a stiff slab.
- **The groove network is directional in scale but isotropic in arrangement** — it will flex in
  any direction, which is unusual and is the reason it makes good boots.
- **Design at thickness.** Edge treatment, seam bulk and the closed-stack height all assume
  ~1.2 mm minimum, not the 0.8–1.0 mm of a typical small-goods leather.

**Pattern consequence:** elephant is a **thick-stock material**, like a heavy veg-tan. Do not
carry a calf pattern across; the seam allowances and the stack height both change.

---

## Hippo — *Hippopotamus amphibius*

| Property | Value | Confidence |
|---|---|---|
| Surface | **striated, suede-like, soft and velvety**, or polished smooth | ✓~ |
| Flex | **surprisingly flexible** for its thickness | ~ |
| Character | natural scars are common and add character | ~ |
| Use | boots, bags, accessories; often made-to-order | ~ |
| Legality | CITES-certified hides from controlled harvests; rare and expensive | ~ |

**Pattern note:** hippo is unusual in that the **finished surface is a suede** unless polished —
so the "grain" question is a finishing decision rather than an anatomical given. That makes it
a chameleon material: order it smooth and it patterns like calf; order it suede and it patterns
like a napped leather with a nap direction.

---

## Yak

- **Thick and heavy**, from large bovines of the Himalayan and Tibetan regions ~
- Used for goods needing **strong, tough, abrasion-resistant** leather — belts, boots, straps,
  bags, saddlery, harness ~
- **Region note:** treat as a bovine. The same L1/L2 map applies, at greater substance.

---

## Camel

Covered in `kangaroo-deer-other.md`: **stiff, hard finish, high fibre density ~, scarce supply
(often from animals that died naturally) ✓, loses colour under hard wear ✓.** Structural, not
supple.

---

## Fur-bearing skins — a different product category

Beaver, chinchilla, coyote, fox, lynx, mink, muskrat, opossum, rabbit, raccoon, sable, seal,
wolf ✓~. These are sold as **fur**, and the leather is the substrate rather than the product.

Two things a flat-goods pattern maker needs:

1. **"Double face"** — one face finished leather, the other left as fur ✓. This changes the
   construction: you cannot skive a double-face skin, you cannot line it conventionally, and the
   seam is usually a butted or lapped join rather than a turned seam.
2. **Direction of the pile.** Like any napped material, fur has a **nap direction** that shows in
   raking light. On a flat pattern this behaves like leather's grain direction but is far more
   visible — a part cut with the nap reversed reads as a different colour.

> **For a flat-goods spec:** fur-on and double-face materials sit outside this folder's
> mechanical framework. The regional anatomy still applies to the skin beneath, but the design
> problem is nap, seam type and volume, not fibre weave.

---

## What these have in common

| Property | Why it matters |
|---|---|
| **Thickness is the design constraint** | not area, not region. Elephant has a hard floor ✓; yak and hippo are thick by nature |
| **Region guidance is weak** | the L1 map exists but rarely decides a part, because no part is thin enough to care |
| **Legality is a first-class constraint** | elephant, hippo and seal are all CITES or nationally restricted. Check before specifying |
| **Surface finishing is often a choice** | hippo smooth or suede ~; elephant left crackled or (badly) levelled |
| **Scars are normal** | on animals that fight and wallow, natural scarring is expected and not a defect ~ |

## What to specify

```
MATERIAL  Elephant (L0) · hide (L2) · crackled grain retained (L3) ·
          >= 1.2 mm, cannot be skived thinner · CITES permit
MATERIAL  Hippo (L0) · hide (L2) · surface finished smooth or suede (finish decision) ·
          CITES-certified
MATERIAL  Yak (L0) · butt/bend (L2) · 2.0-3.0 mm · heavy-goods construction
```

## Honest limits

- **Elephant's 1.2 mm floor is a single source** ✓ but it is stated as a practical limit by
  someone selling the material, and it is consistent with the "deep wrinkles" mechanism. Treat
  it as a working floor, not a specification.
- **Hippo and elephant property claims are trade descriptions**, not measurements. There is no
  mechanical test literature for either in anything found.
- **Legality for all four is CITES and national law**, and it changes. Nothing in this file
  constitutes a legal determination.
