# Regulation and certification — what is actually restricted

The regulatory layer exists because several of the chemicals in this folder are restricted, and
because "eco", "non-toxic" and "chrome-free" are marketing terms that map only loosely onto law.

**This file is a map, not legal advice. Regulations differ by market and change. Verify before
relying on any number.**

---

## The restricted substances, and why

| Substance | Concern | Where it comes from in this folder | File |
|---|---|---|---|
| **Cr(VI) — hexavalent chromium** | carcinogen, sensitiser | **not used in tanning** — leather is tanned with Cr(III). Cr(VI) can form as a **degradation product** under heat, humidity and time ✓ | `02-tanning.md` |
| **Azo dyes** | some cleave to carcinogenic aromatic amines | certain dye classes | `04-dyes.md` |
| **Formaldehyde** | carcinogen, sensitiser | some tannages, some finishes, some resins ✓ | `02`, `05` |
| **Pentachlorophenol (PCP) / chlorinated phenols** | toxic, persistent | historic preservatives and biocides | `01-beamhouse.md` |
| **PFAS / fluorochemicals** | persistent ("forever chemicals") | **fluorochemical DWR** ✓ | `05-finishing.md` |
| **APEO / alkylphenol ethoxylates** | endocrine disruptor, aquatic toxicity | surfactants and degreasers | `01` |
| **Heavy metals — Cd, Pb, Hg, As** | toxic | contamination and some pigments | `04`, `05` |
| **Chlorinated solvents** | occupational and environmental | solvent degreasing ✓ | `01` |
| **Dimethyl fumarate** | severe sensitiser | anti-mould sachets in transit | `01` (storage) |
| **Nickel** | sensitiser | hardware, not leather | `06-novel-treatments.md` |

**Where the regulation lives:** the EU **REACH** restrictions annex and the **REACH SVHC**
candidate list; the EU **Biocidal Products Regulation** for antimicrobial and preservative
treatments; **CPSIA** in the US for children's articles. The leather trade bodies publish
**restricted substance lists** that consolidate these for the industry.

---

## The certification landscape — what each one actually certifies

| Scheme | What it certifies | What it does **not** |
|---|---|---|
| **Leather Working Group (LWG)** | **tannery environmental management and process** — audits the facility, not the material | not a product-safety or a "chemical-free" claim; **it is a tannery audit** ✓ |
| **OEKO-TEX LEATHER STANDARD** | **the finished article is tested for harmful substances** | not an environmental or a process claim |
| **bluesign** | process inputs and resource use across the supply chain | not a property claim about the leather |
| **ISO 14001 / 9001** | management systems | nothing about the material |
| **Gold-rated LWG** | the highest tier of the same tannery audit | still not a chemical-free claim |
| **"Chrome-free"** (self-declared) | **no chromium in the tan** | **not metal-free** — may be Al, Zr, Ti; **not aldehyde-free**; not a retan claim ✓ |
| **"Vegetable tanned"** (self-declared) | usually a veg tan; sometimes a chrome tan with a heavy veg retan | no threshold is universal |
| **"Eco-friendly leather"** | **nothing specified** — no legal definition | anything |
| **"Non-toxic"** | **nothing specified** | anything |
| **"Biodegradable"** | varies wildly; finished leather with a heavy coating is not | verify the test and the conditions |

**The pattern in that right-hand column is the point: most certifications certify a *process* or
a *facility*, and most marketing claims certify *nothing*.** If a claim matters to a design, ask
for the test report, not the badge.

---

## What a designer should actually put in a spec

```
COMPLIANCE  LWG Gold-rated tannery
COMPLIANCE  OEKO-TEX LEATHER STANDARD class II (articles in contact with skin)
N/A         chrome-free (not required — chrome-tanned is acceptable)
RESTRICTED  no PFAS DWR; use a wax-based water repellent and design for re-treatment
RESTRICTED  azo-free dyes
```

**Three practical rules:**

1. **Chrome-tanned leather is not a hazard claim.** Cr(III) is the tanning agent; Cr(VI) is a
   degradation product and is what regulations target. Do not mix them up in either direction —
   neither "chrome leather contains Cr(VI)" nor "chrome leather is proven safe forever".
2. **"Chrome-free" is a chemistry claim, not a safety claim.** The alternatives include
   glutaraldehyde, a regulated sensitiser, and aluminium/zirconium salts.
3. **PFAS is the live issue in water repellency.** Choosing a wax-based DWR is a design decision
   with a performance cost (see `05-finishing.md`), not a free upgrade.

## Honest limits

- **Regulation changes.** Thresholds, lists and scope shift; this file states the structure and
  the concerns, not current limit values, because a limit value quoted here could be stale.
- **Certification scope is the thing most often misread.** LWG in particular is routinely cited
  as if it certified the leather; it audits the tannery.
- **No certification covers "will this leather last"** in the way `../durability.md` means it.
  There is no badge for fatigue life.
