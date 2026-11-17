# Simulation, stress and durability — what actually exists for leather

Short answer: **nobody sells an off-the-shelf, hide-agnostic leather simulator.** That
distinction matters. The capability exists, validated and published, in research groups,
and one of the tools is commercially licensable. But every model needs per-hide
calibration data that no vendor can ship in a box. See §1a before §1.

---

## 1a. Who has actually simulated different leathers

These are real, published, validated. If you need to argue that it is possible, cite
these — not a vendor page.

### Fraunhofer ITWM — the most complete work

**Dietrich, Lykhachova, Cheng, Godehardt, Kronenberger, Meyer, Neusius, Orlik,
Schladitz, Schulz, Voigt, "Simulation of Leather Visco-Elastic Behavior Based on
Collagen Fiber-Bundle Properties and a Meso-Structure Network Model", *Materials*
2021, 14(8), 1894.** FILK Freiberg + Fraunhofer ITWM.

This is the answer to "has anyone modelled *different leathers*". The method:

1. **Micro-CT of leather snippets** at a **3.3 µm voxel edge** — fine enough to
   resolve individual collagen fibre bundles and part of their substructure.
2. Extract the **fibre-bundle network geometry**: how bundles wind, contact and branch.
3. Build a parameterisable 2D tessellation network model from that geometry, with
   **frictional sliding contact between bundles**.
4. Feed in bundle properties measured by tensile testing, solve in FEA.

Validated across **two animal species, several tanning procedures, and different
positions within the hide** — exactly the axes along which real leathers differ.

They went further than elastic behaviour: **damage and crack growth** were simulated
with birth/death elements (SOLID185 / SHELL281 in ANSYS), killing elements whose
stress exceeds local strength, to predict how a cutout propagates under tension.

### Polytechnic University of Valencia — Simucal

**Rupérez, Giner, Monserrat, Montiel, *Computer-Aided Design* 44(12):1205–1216, 2012**,
plus earlier papers from 2008 and the 2010 contact-model paper in CAD 42(5):425–431.

A named application — **Simucal** — with an actual leather constitutive model: linear
elastic **orthotropic**, large deformation, membrane **and** bending, calibrated from
tensile tests on calfskin and validated against two physical experiments (resistance to
damage on lasting, and last-forming). The authors note the hard part explicitly: there
are **no standardised test methods for leather's Poisson's ratios and shear moduli**.

### Leather property measurement, for virtual prototyping

**"Mechanical Parameters of Leather in Relation to Technological Processing of the
Footwear Uppers", *Materials* 2022, 15(15), 5107** — Young's modulus and Poisson's
ratio on a SATRA STM 466, with a factorial design over manufacturing operations, so
that a processed panel's stiffness and lateral contraction can be predicted rather than
assumed.

### Anisotropic hyperelastic models

Natural leather shows **two fibre families**; artificial leather one. Anisotropic
hyperelastic models with distributed fibre orientation reproduce this in FEA, including
viscosity for the rate-dependent case.

### Adjacent, and transferable

- **Tanning itself is simulated**: molecular dynamics of gallotannin diffusing into the
  collagen microfibril (USDA ARS), and discrete-event simulation of tannery production
  lines in FlexSim.
- **Commercial hide handling**: Zünd + Mind + Mindhive demonstrated end-to-end digital
  hide capture, grading, nesting and cutting at Simac 2026. No mechanics — but it is
  "different leathers" managed digitally.

---

## 1b. Is any of it released as code?

Short answer: **the leather-specific code is not open. The building blocks are.**

| source | code released? | what it is |
|---|---|---|
| **Fraunhofer ITWM — TexMath / FISFT** | **No.** In-house, GUI-based, **licensable on request** | FISFT is a *module inside* TexMath. The methods were developed "over the past 15 years through numerous PhD works" — per Orlik, Neusius, Krier & Steiner's own TexMath review, not a claim about FISFT alone |
| **Simucal** (Valencia) | **No.** Research application, never published as source | the named footwear simulator |
| **The MDPI paper (*Materials* 2021)** | **No code.** CC BY 4.0 covers the *article*. No data-availability statement pointing at a repo, no GitHub/GitLab link | — |
| **FILK follow-on (BMWK IGF 01IF23328N)** | Not yet — running **06/2024–09/2026** | whole-hide network model; the project page states FEM/CAD for leather *is not state of the art commercially* |

**How you get it:** Fraunhofer ITWM publishes a **"Request a License"** path for
TexMath. That is the concrete answer — the capability is commercial-in-practice and you
license it from the institute. It is not a download.

### What IS open, and directly reusable

| project | licence | why it matters |
|---|---|---|
| **PolyTex** (Yang, Feng, Béguin, Causse, Wang; *Composites Science and Technology* vol. 259, art. 110940, 2025 — per the PolyPublie record and the Zenodo deposit; re-verify volume/page before citing in anything published) | **GPL-3.0**, code + Zenodo DOI + full PhD thesis | micro-CT → meso-scale geometry → **voxel mesh with per-cell material properties**; APIs for OpenFOAM and Abaqus. Textile tows, but the same pipeline Fraunhofer runs on leather |
| **FElupe** | GPL-3.0 | pure-Python nonlinear FEM, hyperelastic models with automatic differentiation |
| **FibreNet** | open source, C++/OpenCL | particle dynamics for meso-scale fibre networks, GPU, bond failure |
| **ColECM** | MIT | collagen fibril network simulation (ECM, not leather) |
| **fedoo** (+ microgen, simcoon) | GPL-3.0 | FEM + meshing of heterogeneous materials — the homogenisation route |

### The pattern, honestly

The institutes keep the leather-specific code because the value is in the
**calibration pipeline**, not the equations. What they publish is the method and the
validation; what they license is the tool. Meanwhile the generic machinery —
image→mesh→FEM with homogenisation — is GPL and available today.

---

## 1. The tool landscape

| engine | what it genuinely does for leather | what it does not | licence / cost |
|---|---|---|---|
| **CLO3D** | soft-body drape with measured fabric data; stress, strain, pressure maps; DXF/AAMA export | leather is not a fabric — different bending-stiffness regime, and it assumes near-zero membrane stretch where leather has 5–15 % | ~$50/mo, $450/yr |
| **Style3D** | same class, tensor/bending testers, multi-layer stress | same limits; individual tier **non-commercial** | ~$40/mo |
| **Abaqus / ANSYS** | the only route that can model leather's real constitutive behaviour — orthotropic hyperelastic, viscoelastic, damage, finish bond | needs tensile/biaxial/tear test data per hide lot | Abaqus expensive; ANSYS has a free student tier |
| **Footwear CAD** (Icad Universe, Shoemaster, Romans CAD) | 3D upper → flattened pattern, lasting allowances, grading, cutting output | *geometry*, not mechanics. No fatigue, no durability | enterprise |
| **Blender** | cloth sim + XPBD/mesh solvers; scriptable, free | no leather material model, no calibration workflow | free, GPL |

### Why none of this is a tool you can use

| method | what it needs | why it does not ship |
|---|---|---|
| Fraunhofer meso-structure | micro-CT scan of *your* hide, 3.3 µm | a scanner, not a checkbox |
| Simucal / orthotropic FE | tensile + biaxial tests, per lot | Poisson's ratio and shear modulus have no standard test |
| Hyperelastic fibre models | fibre-orientation data per species/tannage | imaging, not guesswork |

---

## 2. The physics: a screening heuristic, not a failure criterion

The governing relation for a bent sheet:

$$\varepsilon = \frac{t}{2R + t}$$

`t` = thickness, `R` = inside bend radius, `ε` = tensile strain at the outer fibre —
the grain side, the side that cracks.

**Read the caveats before using it.** This is a **thin-shell, pure-bending, small-strain**
approximation. Leather is viscoelastic, anisotropic, and deforms well past the small-
strain regime. It ignores creep, the finish layer, grain direction, and the fact that a
crease tightens progressively. **The 20 % threshold below is a screening heuristic for
rejecting obviously bad geometry — it is not a validated failure criterion.** Use it to
compare two designs; do not use it to certify one.

**Outer-fibre strain, %** (rows = thickness mm, columns = inside radius mm):

| t \ R | 0.5 | 1.0 | 1.5 | 2.0 | 3.0 | 5.0 |
|---|---|---|---|---|---|---|
| 0.8 | 44.4 | 28.6 | 21.1 | 16.7 | 11.8 | 7.4 |
| 1.0 | 50.0 | 33.3 | 25.0 | 20.0 | 14.3 | 9.1 |
| 1.4 | 58.3 | 41.2 | 31.8 | 25.9 | 18.9 | 12.3 |
| 2.0 | 66.7 | 50.0 | 40.0 | 33.3 | 25.0 | 16.7 |
| 2.5 | 71.4 | 55.6 | 45.5 | 38.5 | 29.4 | 20.0 |

What the table does legitimately tell you: **a fold with no radius is not a fold, it is a
fracture test.** Folding 1.4 mm leather flat puts ~100 % strain into the grain. That is
why folded edges are skived first — skiving to 0.5 mm takes the same fold from ~100 % to
~33 %, and a 1 mm radius takes it to 41 %.

### Screening rule

A leather fold wants an inside radius of roughly **2–3 × t**. Below **1 × t** you are
relying on the finish to hold the grain together, and it will not.

### The skiving paradox — a real trade-off

Skiving lowers strain by reducing `t`. **But a skive line is itself a thickness step, and
therefore a new stiffness discontinuity — exactly the kind of feature that initiates
cracking.** You have moved the risk from the fold to the skive boundary. Skive with a
long, feathered taper rather than a step, and never put a skive edge across a hinge.
"Skive it" is not automatically the safe answer.

---

## 2b. The better model: leather is a stiff film on a soft substrate

Everything in §2 treats leather as a **homogeneous sheet**. It is not. Leather is a
**thin stiff layer bonded to a thick compliant one**:

- **Film** — finish system (base coat, pigment, topcoat), plus the grain surface itself.
  Thickness `t_f` roughly 10-100 µm. Modulus much higher than the corium.
- **Substrate** — the corium. Thickness ~1 mm in a wallet leather. Far more compliant,
  and it is the layer that does the bending.

A stiff film on a compliant substrate under compression does not simply stretch. **It
buckles** — and which instability you get is decided by geometry and modulus ratio, not
by strain alone. This is the same physics that governs skin wrinkling, the same physics
that governs a wrinkled polymer coating, and it is a **better description of what
actually happens at a leather crease** than the `ε = t/(2R+t)` number in §2.

### The relations

Wrinkle wavelength (semi-infinite substrate, linear elastic, small strain):

$$\lambda = 2\pi t_f \left(\frac{E_f}{3E_s}\right)^{1/3}$$

Critical compressive strain to onset wrinkling:

$$\varepsilon_c = \left(\frac{3\bar E_s}{8\bar E_f}\right)^{2/3}$$

where `Ē = E/(1-ν²)` is the plane-strain modulus. This is algebraically identical to the
more commonly quoted `¼(3E_s/E_f)^(2/3)` — check it if you like: `(3/8)^(2/3) = ¾·3^(2/3)`,
so the two differ only by which modulus convention you fold in. **If you see the two forms
quoted as if they disagree, they don't.**

**Critical strain vs modulus ratio:**

| `E_f/E_s` | 2 | 5 | 10 | 20 | 50 | 100 | 1000 |
|---|---|---|---|---|---|---|---|
| **`ε_c`** | 32.8 % | 17.8 % | 11.2 % | 7.1 % | 3.8 % | 2.4 % | 0.5 % |

Read that table against §2. Section 2 says a fold is safe below ~20 % strain. **The
film-substrate model says a stiff grain layer buckles at 2-12 % compressive strain** —
depending entirely on how much stiffer the finish is than the corium. These are not in
conflict; they answer different questions. Section 2 tells you what the *bulk* outer
fibre sees. This tells you when the *surface* loses stability first. **The surface
usually loses.**

### The counter-intuitive consequence — finishes trade abrasion for creasing

From the two relations together:

- **A stiffer finish increases `E_f/E_s`**, which
  - **lowers** the critical strain (`∝ (E_f/E_s)^(-2/3)`) → surface buckles *sooner*, and
  - **raises** the wavelength (`∝ (E_f/E_s)^(1/3)`) → fewer, broader creases.

So a harder "tougher" topcoat is genuinely better against abrasion and **genuinely worse
against creasing**. It gives you fewer but deeper folds. This is a real, quantifiable
design trade-off, and it cuts against the intuition that a tougher finish is simply
better. A soft finish on a compliant substrate tends toward fine shallow crazing; a hard
finish tends toward a small number of deep creases that then crack at the valleys.

### First: wrinkles and creases are two different instabilities

Do not conflate them, because **the wavelength formula inverts to different variables**
for the two modes and they do not carry the same information.

| | **Wrinkle** | **Crease** |
|---|---|---|
| shape | smooth, sinusoidal undulation | sharp, localised fold; the surface self-contacts at a cusp |
| onset mechanism | linear bifurcation — perturbation of *infinitesimal strain, finite space* | nucleation — perturbation of *finite strain, infinitesimal length of self-contact* |
| critical strain `ε_c` | `(1/4)(3E_s/E_f)^(2/3)` — **modulus-dependent** | **≈ 0.35, universal** for neo-Hookean elastomers, gels, tissues. Independent of modulus, size, shape and loading mode |
| spacing | `λ = 2π t_f (E_f/3E_s)^(1/3)` | `W/H ≈ 3.5`, i.e. **proportional to film thickness only** |
| after onset | saturates in amplitude | deepens progressively; opens a crack at the valley |

Two consequences that matter for leather:

1. **The two are not alternatives chosen by strain level.** Biot predicted wrinkling at
   `ε = 0.46`; Gent and Cho measured creasing at `≈ 0.35`. Creases can set in **before**
   wrinkles. Which mode appears is set by modulus ratio, thickness contrast, curvature and
   adhesion — not simply by "how hard you folded it".
2. **A crease opens a crack at its valley.** That is precisely the classic leather
   failure: the grain layer crazes at the bottom of a sharp fold. So on a *worn item*,
   a sharp crease is the expected finding, not the exception.

### Diagnostic A — fine pattern, sharp but not self-contacting: back out `E_f/E_s`

**Use this only if the pattern is visibly sinusoidal or undulating.** Then invert the
wrinkle wavelength relation:

$$\frac{E_f}{E_s} = 3\left(\frac{\lambda}{2\pi t_f}\right)^{3}$$

Cubes are brutal, which is what makes this diagnostic. Patterns that look similar differ
by more than an order of magnitude in modulus ratio:

| observed **wrinkle** wavelength | assumed finish `t_f` | implied `E_f/E_s` |
|---|---|---|
| 0.3 mm (fine, close-spaced) | 20 µm | ~41 |
| 0.5 mm | 20 µm | ~190 |
| 1.0 mm | 50 µm | ~97 |
| 2.0 mm (broad, lazy) | 50 µm | ~770 |

**Do not apply this to a sharp crease.** It will return a confident number that means
nothing.

### Diagnostic B — sharp, deep folds: back out `t_f`, not `E_f/E_s`

For a crease array, the spacing scales with **thickness** only. The commonly adopted
minimum-energy spacing is `W/H ≈ 3.5` in the **undeformed** state — the standard unit-cell
assumption in the crease literature (used by Chen, Cai, Suo & Hayward, *PRL* **109**, 038001,
2012, who cite it as established). Observed spacing in the *deformed* state is
`w = (1 - ε)W`, so:

$$t_f \approx \frac{w}{3.5(1-\varepsilon)}$$

| observed **crease** spacing | ε = 0.35 | ε = 0.5 | ε = 0.6 |
|---|---|---|---|
| 0.10 mm | 44 µm | 57 µm | 71 µm |
| 0.15 mm | 66 µm | 86 µm | 107 µm |
| 0.30 mm | 132 µm | 171 µm | 214 µm |
| 0.50 mm | 220 µm | 286 µm | 357 µm |
| 1.00 mm | 440 µm | 571 µm | 714 µm |

This is a **different and arguably more useful measurement** for leather, because it is
linear in `w` rather than cubic, and **less circular** — Diagnostic A assumes you already
know `t_f` to find `E_f/E_s`, whereas Diagnostic B estimates `t_f` independently.

**Do not over-read the precision.** The measurement is linear, but the *prefactor* is the
weak link. Published crease spacings span roughly `W/H` 2 to 3.5 depending on whether the
figure is deformed or undeformed and on the strain — Hohlfeld & Mahadevan give a deformed
`L_C/H ≈ 2` near `ε = 0.353`, against the 3.5 unit-cell convention. That is a factor-of-1.5
spread in `t_f` before anything is measured. **Treat the table as order-of-magnitude.**

Read the table like this: crease spacings of **0.1-0.3 mm** are what you expect from a
**normal 40-130 µm finish** — unremarkable, and the geometry, not the finish, is to blame.
Spacings of **0.5-1 mm or more** imply an unusually thick finish (>200 µm, i.e. a
heavy corrected-grain or coated-split finish) or an unstable estimate. A crease spacing
larger than the designed fold scale points at **thickness**, not at finish stiffness.

### The qualitative rule, which holds in both modes

Whatever the mode, the comparison that actually drives a decision is **observed damage
scale versus designed fold scale**:

- **Damage far finer than the folds you designed** → the surface is failing on its own
  length scale. The fault is the **finish system**, and re-drawing the pattern will never
  fix it. The fix is a different, softer finish, or accepting the crazing.
- **Damage at the designed fold scale** → it is a **geometry** problem and §2 applies.

Use the numbers above to *corroborate* that reading — not to replace it.

### Limits — and they matter

- **`t_f` and `E_f` for leather finishes are not standardised anywhere.** There is no
  published table of finish moduli by type. Both numbers above are *illustrative*. You
  cannot compute a real `ε_c` without measuring your own finish. **This is the same
  calibration gap that blocks leather FEA generally (§1a, §5).** The *form* of the model
  transfers cleanly; the *numbers* do not come with it.
- **Finite substrate.** The wavelength formula assumes a semi-infinite substrate. Corium
  at ~1 mm against a 20-100 µm film gives film/substrate thickness ratios of 10-50, so
  the assumption is roughly respectable — but not exact, and it degrades for thick,
  heavily-finished leathers.
- **The 0.35 crease threshold is for ideal elastic materials.** It holds for
  neo-Hookean elastomers, gels and tissue. Leather is not neo-Hookean: its fibre network
  yields and damages. Work on *plasticity retards the formation of creases* shows that
  dissipative materials resist creasing well past 0.35 — metals with `E_t/E ≈ 0.001` show
  no crease even at `ε = 0.8`. So treat 0.35 as an **upper indicator that creasing is
  plausible**, not a value leather must obey. Leather creases because it takes **set**,
  which is a different (and less well-posed) problem than an elastic crease bifurcation.
- **The crease spacing is only unfrozen until the material yields.** Once a leather crease
  becomes permanent set, its spacing stops reflecting the current strain and starts
  reflecting the strain history. Crease spacing on a *used* item is therefore a record of
  the worst cycle, not of the current state.
- **Rate-independent.** Film-substrate theory has no time in it. Leather creeps. The
  theory predicts **where** a crease forms and at what strain, not **when** it deepens.
  Time-dependence is what turns a crease into permanent set (§3), and for that you need
  viscoelastic test data, not bifurcation analysis.
- **This is extrapolation, not a published result.** To be clear about provenance: the
  film-substrate instability literature is extensive and mature (Cao & Hutchinson;
  Zhao's group's phase diagrams of wrinkling / creasing / folding / ridging; cohesive
  interface models of wrinkle-induced delamination). **Its application to leather
  finishes specifically is an inference I am drawing, not a result I found.** No
  paper I could locate does this for a leather finish over corium. Treat it as a
  hypothesis with good theoretical grounding and no leather-specific validation.

### One adjacent precedent that does exist — but it is a different mechanism

Oh et al., *Wrinkle prediction of seat cover considering cyclic loading-unloading with
viscoelastic characteristics*, **Materials & Design 109:270-281 (2016)**,
DOI 10.1016/j.matdes.2016.07.040. Leather automotive seat covers in PAM-COMFORT, leather
as **membrane elements** over solid foam pads, parameters from cyclic loading-creep-
unloading strip tests (1-2 h creep, 60 cycles), predicting permanent wrinkle deformation
and validated against physical tests.

**Be precise about what this validates.** It is a **macro-scale membrane-wrinkling**
model of the whole leather sheet, driven by **bulk viscoelastic creep** of the corium.
It is **not** a micro-scale film-on-substrate instability model of the finish layer. The
Fraunhofer ITWM work cites it in exactly this macro, creep-driven sense.

So it is the right precedent for *"leather wrinkles under cyclic load"* — and it is
**not** precedent for the §2b film-buckling model, which remains an extrapolation. Do not
let the existence of one leather-wrinkling paper imply the other has been validated.

What it does demonstrate is the *method*: they needed **their own cyclic test campaign**
to get the parameters. They did not take them from the literature.

---

## 2c. Where the film model sits in leather simulation as a whole

Leather simulation is not one thing. It is a **hierarchy of fidelity**, and knowing which
rung a question needs stops you paying for a rung you do not need.

| level | models | data needed | cost |
|---|---|---|---|
| **0. Analytical / hand-calc** | idealised geometry — this doc's `ε = t/(2R+t)` | thickness, radius | nil |
| **1. Continuum FEM** | leather as a homogeneous anisotropic hyperelastic / viscoelastic solid | tensile + biaxial per lot; `ν` and `G` have **no standard test** | moderate |
| **2. Homogenised RVE** | representative volume of the fibre network, homogenised upward; predicts hole/notch stress | micro-CT or SEM + bundle tests | high |
| **3. Meso fibre-network FEM** | discrete fibre bundles with sliding contact — Fraunhofer's TexMath/FISFT | micro-CT at ~3.3 µm voxel + per-bundle tests | very high |
| **4. Molecular / atomistic** | triple helix, cross-links, tannin diffusion | MD force fields | extreme, tiny domains |

These levels are **nested, not competing**: molecules set bundle stiffness and relaxation
time (4→3); the network homogenises to a material card (3→2→1); and the continuum result
degenerates to the closed form in the simple-geometry limit (1→0). Fraunhofer validated
at least one link in that chain explicitly — macroscopic relaxation as a single-bundle
relaxation multiplied by a **geometric factor from CT**, checked against tensile tests.

### Which rung a question actually needs

| question | rung | why |
|---|---|---|
| *Will this hinge crack?* | **0 + a physical flex test** | the strain screen plus ISO 5402-1. FEM adds nothing for a simple fold |
| *Will this hole tear?* | 1 or 2 | stress concentration needs at least continuum FEM |
| *Why do two hides of the same species differ?* | 2 or 3 | only fibre resolution explains orientation, bundle thickness, branching |
| *How does tanning change stiffness?* | 4 → 3 | only molecular work links chemistry to mechanics |
| *Will the finish craze before the grain cracks?* | **§2b** | see below |

**Practical conclusion: a wallet hinge does not require climbing this hierarchy.** Rung 0
plus a real flex test answers it. The higher rungs matter only if you want to predict
before cutting, or explain hide-to-hide variation.

### The axis this hierarchy is missing — and why §2b is not just "a different question"

Describing §2b as a separate branch on a separate axis is right but understates it. The
hierarchy above is a **through-thickness refinement scale**. Adhesion is **orthogonal to
it** — and there is no rung in the table where interface strength lives.

That is not a presentational point, it is a physics point. In the film-substrate phase
diagrams, **bond strength is a first-class parameter that selects which instability you
get**:

- **strong bond**, film much stiffer than substrate → **wrinkling**
- **strong bond**, film modulus comparable to substrate → **creasing**
- **weak bond** → **delaminated buckling** — the film lifts instead of folding

So §2b depends on a material property (`Γ`, interfacial adhesion) that the bulk hierarchy
has no slot for at any level, however finely you mesh. And for leather the weak-bond case
is the *known first failure mode* (§3): finish and topcoat delaminate **before** the fibres
fail.

**This gives a diagnostic that costs nothing to apply.** Look at how the finish has failed:

- **Crazing / fine cracking, no lifting** → well-bonded, wrinkling or creasing regime.
  §2b's spacing diagnostics apply, and the fix is geometry or finish modulus.
- **Flaking, lifting, or a visible edge where the film peels** → **weak bond**,
  delamination regime. The spacing formulae do **not** apply. The fix is **adhesion**
  — a different primer or tie coat — and no change to modulus or geometry will help.

Telling those two apart is worth more than any number in §2b, and it needs a fingernail,
not a solver.

### The honest gaps in the whole hierarchy

Two things are missing at **every** level, not just the cheap ones:

- **Fatigue / cyclic degradation.** No rung models accumulated damage over thousands of
  cycles. It remains empirical — the flexometer — exactly as §4 and §5 say.
- **Coupled moisture–structure–mechanics.** Leather's stiffness, relaxation and crease
  propensity all move with humidity, and no published model carries water content →
  bundle properties → macroscopic response in one framework. Fraunhofer treats relaxation
  as a fixed material property, not a moisture-dependent one. This is why §6 insists on
  conditioning.

### If you do want open code for §2b

**`calugo/wrinkles`** (GitHub, CC BY 4.0) is the closest reusable implementation of the
bilayer-compression FEM problem. Three scripts: `slab.py` (monolayer stretch, self-
contained), **`Nbbz.py`** plus **`N3mesh.py`** (bilayer compression, Neo-Hookean, *near*
incompressible), `bbz.py` (morphoelastic growth of a bilayer). It is structurally the same
problem as finish-on-corium — you would swap geometry and material parameters.

Caveats before you rely on it:

- **Licence: CC BY 4.0 is not a software licence.** Creative Commons themselves recommend
  against it for software; the FSF says *"like all CC licenses, it should not be used on
  software."* It carries **no patent grant** and is **not compatible with the major
  software licences**, so you cannot safely combine it into a larger project. **Read the
  equations and re-implement them; do not vendor the code.** The relations in §2b are
  closed-form and reproduce in a dozen lines.
- **Research-grade.** ~9 stars, 4 forks, single author, last commit Jan 2025. Support repo
  for papers, not a maintained library.
- **Legacy FEniCS.** The scripts are `python3` but target `dolfin` / FEniCS Mechanics, not
  DOLFINx. Getting it running in 2026 means a legacy conda-forge FEniCS environment.
- Related: `materialsguy/Buckling_Analysis_Laminated_Samples` is an Abaqus eigenvalue /
  Riks workflow for layered samples — a template, needs an Abaqus licence, and is
  **CC BY-NC-ND** (no derivatives, non-commercial), which is even more restrictive.

**And you almost certainly do not need any of it.** The §2b diagnostics are closed-form
inverses that run in a spreadsheet. FEM only becomes necessary if you want to predict
*where* a crease nucleates on a specific geometry — a different and much harder question
than wavelength or modulus ratio, and one that needs the calibration nobody has anyway.

---

## 2d. The same hierarchy, with verified citations

§2c gave the ladder. This section attaches a real paper to each rung, so nothing in it is
argued from memory. Every citation below was checked against a publisher or repository
record. Where I could not confirm one, it is **omitted** rather than guessed — see the
note at the end.

### Level 0 — analytical

**No citation exists, and that is the honest answer.** `ε = t/(2R+t)` is standard
thin-shell bending theory. Using it as a **hinge-screening gate with a threshold** is a
pattern-making practice, not a published research result. Do not dress it up as one, and
do not claim it is novel either: I have not run a prior-art search across the
pattern-cutting literature, so *"appears to be original"* and *"is original"* are different
claims and only the first is defensible.

### Level 1 — continuum FEM

**Rupérez, Giner, Monserrat, Montiel**, Simucal — *Computer-Aided Design* **44**(12):
1205-1216 (2012). Orthotropic linear-elastic, large-deformation membrane + bending model
of calfskin, validated against lasting and damage tests. Confirms explicitly that **no
standard test exists for leather's Poisson's ratio or shear modulus** — the calibration
hole that blocks this level.

**Mechanical parameters of leather in relation to technological processing of footwear
uppers** — *Materials* **2022**, 15(15):5107. Young's modulus and Poisson's ratio measured
on a **SATRA STM 466**, factorial design over processing steps. This is the data source a
Level 1 model needs, and it is one of very few.

### Level 2 — homogenised RVE

**Haines & Barlow**, *The anatomy of leather*, *Journal of Materials Science*
**10**(3):525-538 (1975), DOI 10.1007/BF00543698. The conceptual foundation, and still the
best single description of why microstructure governs behaviour:

- **Weave angle** controls tensile and tear strength — a low angle lets load transfer
  along the fibre axis and permits more frequent interweaving per unit thickness.
- **Fibril mobility within the bundle** controls flexibility. Fine spaces between fibrils,
  visible as longitudinal striations, let them slide; if fibrils adhere, the leather is
  firm.

**Long, Peng, Li, Yu, Zhang**, *A simple method for identifying the elementary units
governing the mechanical properties in leather materials*, *Collagen and Leather* (2025),
DOI 10.1186/s42825-024-00184-4. Twelve bovine leathers, Cr(III) / Zr(IV) / aldehyde
crosslinking plus fillers, mercury intrusion porosimetry to measure fibril-bundle radius.
Results worth having as numbers:

- FB radius spans **230-950 nm** — Cr(III) 424 nm, aldehyde 951 nm
- Tear strength **75 N/mm** (Cr), 60 (Zr), 45 (aldehyde); ~83 N/mm with oleic acid added
- **Tear strength is linear in `(1-P)/R` with R² > 0.99**

That last number is the important one: it is a *quantitative* demonstration that the fibre
bundle is the elementary load-bearing unit, not a modelling convenience.

### Level 3 — meso fibre-network FEM

**Dietrich et al.**, *Materials* **2021**, 14(8):1894. The flagship, already covered in
§1a: micro-CT at 3.3 µm, parameterised 2D bundle tessellation with sliding frictional
contact, element-death damage, validated across species, tannage and hide position.

### Level 4 — molecular — and a split that matters

**Leather-specific:**

- **USDA ARS, Eastern Regional Research Center — collagen microfibril model.** Bovine
  type I, five triple helices in a supercoil, one D-space (~1.4 collagen monomers),
  including gap/overlap regions and telopeptides. Built explicitly as a tool for
  interrogating tanning chemistry — chrome, glutaraldehyde, genipin — against collagen
  binding sites. Published in *International Journal of Biological Macromolecules*
  **53**:20-25 (2013).
- **Siggel, Bulo, Molnar, Weiss, Taeger** (BASF), *Leather related collagen modeling: the
  challenges of modeling hierarchical structures*, *JALCA* **102**(10):333-336 (2007).
  MD of a 34-triple-helix fibril model at pH 7 with 200-mer polyacrylic and
  polymethacrylic acid. Finding relevant to retanning: PMAA sits as a better buffer
  between microfibrils, while PAA forms many strong hydrogen bonds that pull fibrils into
  close proximity — a parchment-like structure. Validated against experimental density.

**Collagen-generic, NOT leather — do not pass these off as leather work:**

- **Malaspina, Szleifer, Dhaher**, *Mechanical properties of a collagen fibril under
  simulated degradation*, *J Mech Behav Biomed Mater* **75**:549-557 (2017),
  DOI 10.1016/j.jmbbm.2017.08.020. Fibril stiffness falls sharply with even small
  crosslink, surface or volumetric degradation.
- **Kamml, Ke, Acevedo, Kammer**, *The influence of AGEs and enzymatic cross-links on the
  mechanical properties of collagen fibrils*, arXiv:2301.13010 (2023). Coarse-grained
  steered MD. Mechanism: AGEs inhibit intrafibrillar sliding, raising stiffness and
  causing **abrupt brittle fracture** rather than frictional dissipation. (Companion:
  arXiv:2308.05514.) Their motivating problem is **bone brittleness in ageing and
  diabetes** — not leather.

The distinction is not pedantic. Tanning is itself a controlled crosslinking process, so
the AGEs result is *mechanistically suggestive* for over-tanned or aged leather — but it
is a hypothesis by analogy, and this document has already been burned once for that.

### The two cross-level bridges — the strongest evidence the ladder is real

1. **Fraunhofer, 3→1.** Macroscopic relaxation = single-bundle relaxation × a purely
   **geometric factor from CT**, checked against tensile tests. Homogenisation is
   demonstrated to work for leather, at least for relaxation.
2. **FB radius, 2/3→0/1.** Tear strength linear in `(1-P)/R` at **R² > 0.99** across
   twelve leathers. A microstructural observable predicts a macro measurable.

### What Haines & Barlow adds to this document specifically

Their 1975 finding that **creasing depends on fibril mobility within the bundle** is a
microstructural mechanism for the **permanent set** described in §3. Set is not only
viscoelastic creep of the sheet — it is the loss of the fine spaces that let fibrils slide
past one another. Leather that has taken a set has, at least locally, become the "firm"
leather Haines describes. That also suggests why conditioning matters so much (§6):
moisture is what keeps those sliding interfaces lubricated.

### Gaps — consistent at every rung

- **Fatigue / cyclic degradation: absent at all five levels.** Dietrich 2021 is quasi-static
  tension plus relaxation, not repeated cycling. This is §5's gap, structural rather than
  incidental.
- **Coupled moisture–structure–mechanics: absent at all five levels.** Fraunhofer treats
  relaxation as a fixed material property. Nothing carries water content → bundle
  properties → macroscopic response in one framework.

Both gaps are why §4's physical testing is the right answer regardless of which rung you
are working on — not a limitation of the cheap levels, but of all of them.

### Provenance note

Verified against publisher or repository records for this section: Haines & Barlow 1975;
Long et al. 2025 (DOI above, with the R² > 0.99, 230-950 nm and tear-strength figures read
from the article); Siggel et al. 2007 (**JALCA 102**(10):333-336); Malaspina et al. 2017
(DOI above); Kamml et al. 2023 (arXiv:2301.13010). Also verified earlier: Rupérez 2012 and
Dietrich 2021.

**Omitted because I could not confirm them:** a "ion-induced conformational dynamics of
collagen fibrils" paper, a "nanomechanical heterogeneous properties of collagen"
*Biomech Model Mechanobiol* 2014 paper, and a *Collagen and Leather* 2022 paper on silane
thermal stability. Treat any of those as leads to check, not as citations.

---

## 3. Where stress concentrates — the mechanics, not folklore

Each is a stiffness discontinuity or a geometric singularity.

| location | why | what to do |
|---|---|---|
| **The hinge** | highest curvature, and the only line that sees the full cycle *every time the item opens* | radius it, skive it with a taper, or move it. Do not decorate it |
| **Under a stitch hole** | the hole removes ~90 % of the cross-section over its diameter. FEA on stitched leather shows stress mid-stitch can be **4–5×** the stress at the ends of a run | never put a hole within one stitch run of the hinge; end runs away from high curvature; quantify with SATRA TM33 (§4) |
| **A sharp internal corner** | stress singularity, roughly `σ ∝ 1/√r` | radius every internal corner. This is why the library gates on it |
| **Where thick meets thick** | doubled seam, unskived fold-back, layered card stack — and the **skive line** (§2) | feather the taper. 0.4 mm over 5 mm, not a step |
| **Hole patterns / perforation lines** | a row of holes is a tear-initiation line if it runs across the bend | perforate parallel to the fold, never across it |
| **Finish-to-leather bond** | topcoat and PU film delaminate before the fibres fail — the **first** failure mode. This is a stiff film on a compliant substrate and buckles at 2-12 % strain, well below the bulk figure in §2 (§2b) | buy flex-rated finish and test it (§4). If creases on a worn item are far finer than the designed folds, the fault is the finish, not the pattern |
| **Fold + salt + wet** | wet flex is a separate, harsher regime; salt accelerates it | keep the hinge out of the wetted zone; test wet flex, not just dry |
| **Cold** | flex life drops sharply with temperature — roughly 4× between 23 °C and −10 °C in one automotive comparison | if the item will see winter, test cold; a hinge marginal at 20 °C is failing |
| **Over-drying** | low hydration raises strength but kills elongation — the hinge stops bending before it stops pulling | condition for suppleness deliberately, and say which property you are choosing |

### A failure mode this list used to miss: permanent set

Repeated flexing produces **permanent deformation — "set" — not only crack initiation.**
Haines & Barlow (1975, §2d) give the microstructural reason: flexibility comes from the
fine spaces that let fibrils **slide within the bundle**. Take a set and those interfaces
are, at least locally, no longer sliding — the leather has become what they call "firm".
Which is also why moisture matters (§6): water keeps those sliding interfaces working.
In a wallet hinge the first visible sign of degradation is usually not a crack but a
**soft, floppy crease that no longer returns flat**, plus surface grain coarsening. By the
time you see a crack, the hinge has been failing for a long while. Assess set explicitly.

---

## 4. Testing: multi-mode, not just flex

Real wallet durability is **flex + tear + abrasion + stitch + aging + moisture cycling.**
A hinge can pass flex and still fail by abrasion on the inside face, or by tear once a
crack starts.

> **Caveat on this table.** The ISO numbers below are current as cited. The SATRA TM
> numbers are given as they appear in SATRA's test catalogue — **confirm the current
> revision with SATRA before writing them into a purchase specification.** Standards
> get revised; this file is a map, not the standard.

### Flex — the crease

Flex testing has **three different methods**, and they are not interchangeable:

| method | standard | what it does |
|---|---|---|
| **Flexometer / Bally** | **ISO 5402-1:2022** (IUP 20); identical method in **ISO 17694:2016** | specimen **folded in half, grain face to face**, clamped; upper clamp oscillates **22°30'** at **100 cycles/min**. The classic wallet-hinge analogue |
| **Vamp flex** | **ISO 5402-2:2015** (IUP 39-2) | specimen folded over an **inverted-V clamp** (40° internal angle, 6.4 mm tip radius), clamps driven apart **19 mm** at **300 cycles/min**. Produces **four creases at once**, and is the method for **wet** flex |
| **Whole-shoe flex** | **ISO 24266** (SATRA TM92) | the assembled shoe, for completeness |

**ISO 5602-2's damage list is worth knowing** because it names the failure modes this document
cares about verbatim: creasing in the central inward fold, cracking in the inward fold,
cracking in the outward folds, **delamination or flaking of the surface finish**, cracking
extending to the piece edge, and spue.



- **ISO 5402-1:2022 / IULTCS IUP 20:2022** (edition 3, published 2022-03-30;
  **cancels and replaces ISO 5402-1:2017**, which is withdrawn). Applies to flexible
  leather **below 3.0 mm**. Part 2 is the Vamp Flex method.
- **ISO 17694:2016** — footwear uppers and linings, flex resistance. (EN 13512 could not be
  verified and is no longer cited.)
- **SATRA TM55**, **BS 3144**, **JIS K6545**, **ISO 32100** (coated fabrics).

**ASTM D6182-23** — "Flexibility and Adhesion of Finish on Leather". Read the scope
carefully: this is a **finish-coating** test, not a leather-substrate test, and it
excludes wet blue. It is *complementary* to ISO 5402-1, which covers the leather itself.
Use D6182 when you care whether the topcoat survives; use ISO 5402-1 when you care
whether the hide does.

#### What the Bally flexometer actually does — correcting a common misreading

This file previously said the 22.5° stroke made the test "gentler than a wallet hinge."
**That was wrong, and it inverted the risk.**

Per ISO 5402-1 clause 7.3, the specimen is **folded in half lengthwise, grain surface to
grain surface**, clamped folded-edge-first in the movable upper clamp, then the free end
is drawn around and clamped in the fixed lower clamp. The tested surface sits on the
**outside of a tight folded loop**. The **22.5° ± 0.5°** is only the oscillation *stroke*,
which makes the crease **run along** the specimen at 100 ± 5 cycles/min.

So: the *stroke* is small, the *crease* is severe. Per cycle, the local fold curvature is
often **harsher** than a wallet's open-to-flat motion. This is a fatigue test at a tight
radius, not a gentle wiggle.

#### Cycle counts are specification-level, not standard-level

ISO 5402-1 is a **qualitative, visual-rating method**. Its own introduction says:

> "The number of flexing cycles chosen depends on the end use of the leather and the
> expected performance. **The leather specification normally defines the number of flex
> cycles that the leather is required to achieve without damage.**"

The frequently quoted "50,000–100,000 cycles for quality top-grain", and the
"20,000–50,000 cycles at −10 to −15 °C" for notebook/luggage covers, are **commonly
specified targets from industry practice, not values mandated by ISO 5402-1 or ASTM
D6182.** Present them as targets a buyer can choose, never as a standard's pass threshold.

**Reported failure grades**, in the order they appear:

1. colour change / greying of finish, no structural damage
2. crazing or cracking of finish
3. loss of adhesion (finish→leather, or between coats)
4. powdering / flaking
5. coarse grain lines ("pipey" grain), loss of grain pattern
6. cracking of the grain layer
7. fibre breakdown to powder, then complete failure

Plus, not in the visual grade list but real: **permanent set** (§3).

**Orientation matters**: leather bends differently along vs across the backbone. Label
cut direction before conditioning, or the result is noise.

### Tear — a cracked hinge propagates as a tear

- **ISO 3377-1** single-edge tear (IUP 40)
- **SATRA TM162** (Baumann tear), **TM179** (wing rip)

A hinge that cracks does not usually "wear through"; it **tears** from the crack tip.
Tear strength is the property that decides whether a small crack stays cosmetic.

### Tensile strength and elongation

- **ISO 3376**, **SATRA TM43**

Two jobs: material qualification, **and** the input data for any FEA calibration (§1a).

### Grain crack resistance

- **ISO 3378** (ball burst / lastometer type), **SATRA TM24** — note TM24 is the *lastometer
  ball burst*, not the cold crack test

Distinct from finish cracking and directly relevant at folds: this is whether the
**grain layer itself** splits. A finish can pass while the grain underneath fails.

### Needle and stitch tear

- **SATRA TM33** — strength perpendicular to needle perforations

This is the test that **quantifies the stitch-hole stress concentrator** in §3 rather
than asserting it. If you specify one non-flex test for a stitched leather good, this is
the one.

### Abrasion

- **SATRA TM31** (Martindale), **SATRA TM163** (Taber)

Wallet interiors see constant rubbing against cards, cash and pocket lining. A hinge can
survive flex indefinitely and still fail by surface abrasion on the liner.

### Moisture — how it behaves when damp

- **SATRA TM47 / TM172** for water vapour permeability and absorption (absorption is TM178)
- **ISO 5402-2:2015 — wet vamp flex**, re-wetted every 25 000 cycles and inspected for spue. This is
  the standard for the "fold + salt + wet"
  concern in §3, which previously had no test attached)

### Cold — a bigger derating factor than most people expect

Cold matters twice over: as a **cold crack** test (SATRA TM129) and as a **cold flex** test
(ISO 17694 run at about −5 ± 2 °C; automotive specs go to **−30 °C**, e.g. GMW 3013 requires
100 000 flex cycles at −30 °C without cracking).

The size of the effect is the point. In one automotive comparison, 1.1 mm genuine leather
ran **45 000 Ross flex cycles at 23 °C but only 12 000 at −10 °C** — roughly a **factor of
four**. A wallet that passes comfortably in a temperate workshop can fail its first winter.
That figure is from a vendor comparison rather than peer review, so treat the *direction*
as the finding and the digits as indicative.

**Design consequence:** if a hinge is marginal at 20 °C, it is not marginal, it is failing.

### Cold crack

- **SATRA TM129** — establishes the low-temperature limit you are specifying when you
  write "−15 °C". Without this, a cold-flex number is unfalsifiable.

---

## 5. Life prediction: honestly, there isn't one

**The nearest thing to a leather fatigue result.** One study (Kaunas University of
Technology group, *Materials Science / Medžiagotyra*) flex-tested laminated leather and its
layers by the vamp method (LST ISO 5423:1992), ≥10 specimens per condition. Two findings
that matter:

- **Tensile strength of split leather fell 36 %** across the cyclic range tested.
- **5 × 10⁵ cycles — more than seven days of non-stop flexing — never reached an endurance
  limit.** The authors' own conclusion is that testing must go into the **millions**.

That second point is the honest one for this document: **there is no endurance limit
anywhere near the cycle counts a product sees.** So a "pass at 50 000 cycles" tells you the
hinge is not yet at failure, not that it is safe. It also confirms, from a real leather
fatigue experiment, that the S-N curve absent from §5 is not absent because nobody looked —
it is absent because nobody has run enough cycles to find the asymptote.

**No standardised permanent-set test exists for leather.** Permanent set (§3) is real and
observable, but the nearest standard method, **ASTM D395 compression set**, is written for
rubber and elastomers. There is no ISO/IULTCS or SATRA equivalent for leather. Set is
assessed by eye and by whether the item lies flat. That is a genuine hole in the test
landscape — it is not that this document failed to find the method.


**There is no published S-N curve (stress vs. cycles) or Paris-law-type crack-growth
model for leather** comparable to those for metals and polymers. This is a genuine
research gap, and it is the reason nobody can convert a cycle count into "years of life"
with any validity.

So the table below is **not a life prediction**. It is a linear index that assumes every
open is one identical cycle — which is false. Real use mixes small openings, full
openings, sitting on the wallet, and being stuffed in a pocket.

| opens per day | cycles/year | 50,000 cycles | 100,000 cycles |
|---|---|---|---|
| 10 | 3,650 | 13.7 yr | 27.4 yr |
| 20 | 7,300 | 6.8 yr | 13.7 yr |
| 40 | 14,600 | 3.4 yr | 6.8 yr |

Use it to rank materials and to sanity-check a target. Do not quote it as expected
service life, and do not present it without the caveats above.

---

## 6. A workflow that isn't wrong

Getting a meaningful number needs more than clamping a strip.

```
condition the specimens        (see below - this is mandatory, not optional)
        |
choose a material with a flex rating      (ISO 5402-1:2022, target set in YOUR spec)
        |
geometry: radius hinges and corners   (eps = t/(2R+t) as a SCREEN, < ~20%)
        |
cut >= 3-5 specimens, from different positions in the hide
        |
test flex + stitch tear (TM33) at minimum; add abrasion/tear as the design demands
        |
inspect at 25x for finish crazing AND measure permanent set - not just "is it broken"
        |
only then cut the pattern
```

### Conditioning is mandatory — but it is a trade, not a free win

Two different things are called conditioning, and this document means the **test** sense:
equilibrating specimens to a standard atmosphere before testing, required by ISO 18454 /
ISO 2419. (In a tannery, "conditioning" means damping leather to 25-30 % moisture before
staking — a different operation.)

Before treating moisture as simply good, know the trade-off. Long et al. (*Colloids Surf A*
**702**:134957, 2024) measured Cr-crosslinked collagen fibres from **0.031 g/g to full
hydration**:

- **Lower hydration → higher tensile and tear strength**, and *less* softness
- **Lower hydration → smaller D-period and lateral spacing** between molecules
- **Elongation at break has an optimum at an intermediate water content** — not at either extreme
- Mechanism: water tunes the electrostatic and van der Waals interactions between fibres

So drier leather is **stronger and more tear-resistant but stiffer and less extensible**.
"Keep it conditioned" is good advice for a hinge that must stay supple, and *bad* advice if
your failure mode is tear. Say which property you are trading away.

### Conditioning the specimen before the test

Neither ISO 5402-1 nor ASTM D6182 gives meaningful results on unconditioned specimens —
**ASTM D6182-23 explicitly requires conditioned specimens.** Record temperature, relative
humidity and duration with the result, or the number cannot be compared to anyone else's.
A result without its conditioning is not a result.

### Sample count and hide variability

Leather varies **significantly within a single hide**, let alone between hides and lots —
back, flank and belly differ in structure and therefore in flex life. **A single strip is
not representative.** Take a minimum of 3–5 specimens from different positions, and state
which positions. Treat any single-strip result as anecdote.

### Define acceptance before you test

A cycle count with no endpoint is unfalsifiable. Write the pass criterion first, choose
one:

- **no crack visible at 25x** (strictest, for a visible hinge)
- **no finish damage of grade ≥ 2** (finish survives; grain may shift)
- **no permanent set** beyond a stated angle
- **no tear propagation** from a pre-crack (the realistic long-term criterion)

"Survived 50k cycles" means nothing until you say survived *what*.

### The half-hour version

Clamp a strip of the **actual** leather in a vice, fold it through 180° both ways until
the grain crazes, and count. This is not spec-compliant and produces no certifiable
number. It ranks your material and finds a bad hinge before you cut the good hide. Note
that this crude test has **no conditioning and no valid acceleration factor** — it is
intuition, not data.

### No acceleration factor exists

There is no validated relationship between flexometer cycles and real wallet openings.
Do not compute one. Derate by judgement: the real hinge folds harder than the test
stroke, under dirt and compression, so require **more** than you think you need.

---

## 7. What this means for the skill

`build_piece.py` gates on geometry, not mechanics, and is honest about that. The
durability layer is arithmetic plus a test plan you run yourself:

- `ε = t/(2R+t)` as a **screening heuristic** — reject obvious geometry, do not certify
- keep stitch runs and hole patterns away from the hinge; quantify with SATRA TM33
- radius every internal corner; feather every skive
- specify a flex rating **and** a pass criterion in your own spec
- always build a felt mock, and always condition before testing

A future gate could compute strain at every declared fold and refuse above a threshold.
That is a small, well-defined addition — and it would still be a screen, not a
prediction.

---

## 8. Adjacent compliance concerns (out of scope here, but real)

If this becomes a product specification rather than a design note: **chrome VI
(ISO 17075)**, formaldehyde, azo dyes, and PFAS restrictions apply to leather goods in
the EU. None of it is a mechanical question, and none of it is covered above.
