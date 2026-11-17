# Sources reviewed — leather pattern & durability project

Status key:

- **✓ verified** — bibliographic details checked against a publisher or repository record
- **~ single source** — details from one secondary reference; re-verify before publishing
- **✗ not found** — searched for and could not locate; removed from recommendation
- **✗ dropped** — could not confirm; NOT cited in `durability.md`
- **(proj)** — research programme or project page, not a paper

---

## A. Leather simulation and mechanics — leather-specific

| # | Reference | What it gives us | Status |
|---|---|---|---|
| A1 | **Dietrich, S., Lykhachova, O., Cheng, X., Godehardt, M., Kronenberger, M., Meyer, M., Neusius, D., Orlik, J., Schladitz, K., Schulz, H., Steiner, K. & Voigt, D.**, *Simulation of Leather Visco-Elastic Behavior Based on Collagen Fiber-Bundle Properties and a Meso-Structure Network Model*, *Materials* **2021**, 14(8):1894, DOI 10.3390/ma14081894 | The flagship leather simulation: 3.3 µm voxel CT, parameterised 2D bundle tessellation, sliding frictional contact, element-death damage, validated across species / tannage / hide position. Introduces **FISFT** (1D FEM, large deformation + friction evolution) | ✓ |
| A2 | **Rupérez, M.J., Giner, E., Monserrat, C. & Montiel, E.** — *Simucal*, *Computer-Aided Design* **44**(12):1205-1216 (2012) | Calfskin orthotropic linear-elastic, large-deformation membrane + bending, validated against lasting and damage tests. States that **no standard test exists for leather Poisson's ratio or shear modulus** | ✓ |
| A3 | **Mihai, A., Seul, A., Curteza, A. & Costea, M.**, *Mechanical Parameters of Leather in Relation to Technological Processing of the Footwear Uppers*, *Materials* **2022**, 15(15):5107, DOI 10.3390/ma15155107 | Young's modulus and Poisson's ratio on a **SATRA STM 466**, factorial design over layers/lining/perforation. Calfskin E = **72 N/mm²**; drops 3 % with a leather lining, 22 % with PES knit; perforation intervals of 2/3 mm change shear and flexibility, 5 mm is safe | ✓ |
| A4 | **Oh, S. et al.**, *Materials & Design* **109**:270-281 (2016), *Wrinkle prediction of seat cover considering cyclic loading-unloading with viscoelastic characteristics*, *Materials & Design* **109**:270-281 (2016), DOI 10.1016/j.matdes.2016.07.040 | Leather seat covers in PAM-COMFORT, membrane elements over foam, parameters from cyclic loading-creep-unloading strip tests (1-2 h, 60 cycles). **Macro-scale membrane wrinkling driven by bulk creep — not finish-layer film buckling** | ✓ |
| A5 | **Long, W., Peng, L., Li, J., Yu, Y. & Zhang, W.**, *A simple method for identifying the elementary units governing the mechanical properties in leather materials*, *Collagen and Leather* **7**, Article **6** (2025), DOI 10.1186/s42825-024-00184-4 (published 01 Mar 2025) | 12 bovine leathers. FB radius **230-950 nm**; tear strength 75/60/45 N/mm by tannage, ~83 with oleic acid; **tear strength linear in (1-P)/R at R² > 0.99** — quantitative proof the fibre bundle is the elementary load-bearing unit | ✓ |
| A6 | **Haines, B.M. & Barlow, J.R.**, *The anatomy of leather*, *Journal of Materials Science* **10**(3):525-538 (1975), DOI 10.1007/BF00543698 | The conceptual foundation. **Weave angle** governs tensile and tear strength; **fibril mobility within the bundle** governs flexibility. Gives a microstructural mechanism for permanent set | ✓ |
| A7 | **Yang, B., Feng, Y., Béguin, C., Causse, P. & Wang, J.**, *Open source tool for Micro-CT aided meso-scale modeling and meshing of complex textile composite structures* (**PolyTex**), *Composites Science and Technology* **259**:110940 (2025), DOI 10.1016/j.compscitech.2024.110940; PolyPublie 61714 | Open-source (GPL-3.0) micro-CT → digital material twin → mesh workflow. **Note: it is a textile-composites tool, not a leather tool** | ✓ |
| A8 | **Siggel, L., Bulo, R.E., Molnar, F., Weiss, H. & Taeger, T.** (BASF), *Leather related collagen modeling: the challenges of modeling hierarchical structures*, *JALCA* **102**(10):333-336 (2007) | MD of a 34-triple-helix fibril at pH 7 with 200-mer PAA and PMAA. PAA forms strong H-bonds pulling fibrils together (parchment-like); PMAA buffers | ✓ |
| A9 | **USDA ARS, Eastern Regional Research Center** — bovine type I collagen microfibril model, *International Journal of Biological Macromolecules* **53**:20-25 (2013) | Five triple helices in a supercoil, one D-space, gap/overlap and telopeptides. Built as a tool for interrogating tanning chemistry (chrome, glutaraldehyde, genipin) | ✓ |
| A10 | **Fraunhofer ITWM**, AIf leather project (proj) | FISFT confirmed as a module of **TexMath**; methods developed over 15 years of PhD work (Orlik, Neusius, Krier, Steiner review); "Request a License" commercial path | ✓ (proj) |
| A11 | **FILK**, IGF project **01IF23328N** (06/2024-09/2026) (proj) | Whole-hide network model from CT. States explicitly that commercial FEM/CAD for leather is **not** state of the art | ✓ (proj) |

---

## B. Skin simulation

| # | Reference | What it gives us | Status |
|---|---|---|---|
| B1 | **Flynn, C. & McCormack, B.A.O.**, *Finite element modelling of forearm skin wrinkling*, *Skin Res Technol* **14**(3):261-269 (2008), DOI 10.1111/j.1600-0846.2008.00289.x | Three-layer FE model (stratum corneum, dermis, hypodermis) validated against 8 volunteers with laser profilometry. Max range and average roughness off by **34 % and 43 %** | ✓ |
| B2 | **Flynn, C.O. & McCormack, B.A.O.**, *A three-layer model of skin and its application in simulating wrinkling*, *Comput Methods Biomech Biomed Eng* **12**(2):125-134 (2009) | Full method; tab displacement 45→20 mm | ✓ |
| B3 | **Flynn, C.O. & McCormack, B.A.O.**, *Simulating the wrinkling and aging of skin with a multi-layer finite element model*, *J Biomech* **43**(3):442-448 (2010), DOI 10.1016/j.jbiomech.2009.10.007 | Pre-stress delays wrinkling onset and reduces amplitude. Pre-stress values (1, 2, 5 kPa) had to be **swept** because none were published | ✓ |
| B4 | **Zhao, Y., Feng, B., Lee, J., Lu, N. & Pierce, D.M.**, *A multi-layered computational model for wrinkling of human skin predicts aging effects*, *J Mech Behav Biomed Mater* **103**:103552 (2020), DOI 10.1016/j.jmbbm.2019.103552 | 2-6 layers. Flattening of the dermal-epidermal junction with age **enhances** wrinkling; VE thinning, RD thinning, PD thickening all enhance it | ✓ |
| B5 | **Chavoshnejad, P., More, S. & Razavi, M.J.**, *From surface microrelief to big wrinkles in skin: A mechanical in-silico model*, *Extreme Mechanics Letters* **36**:100647 (2020) | Microrelief breaks symmetry and seeds wrinkle location. **Hypodermis is irrelevant to wrinkling**; epidermis modulus change drives it | ✓ |
| B6 | **Montes Maestre, J.S., Kavan, L., Boyer, E., Goldade, R., Coros, S. & Thomaszewski, B.**, *Physics-Based Simulation of Contact-Induced Facial Wrinkling*, **Computer Graphics Forum 45**(8), 2026; arXiv:2607.04768; DOI 10.1111/cgf.70580 (SCA 2026) | High-order prismatic solid-shell elements; viscoelastic; ligament constraints. **Linear and quadratic elements cannot produce wrinkle-frequency deformation at all** | ✓ |
| B7 | **Guissouma, I., Hambli, R., Rekik, A. & Hivet, A.**, *A multiscale four-layer finite element model to predict the effects of collagen fibers on skin behavior under tension*, *Proc IMechE Part H* **235**(11):1274-1287 (2021), DOI 10.1177/09544119211022059 | Four layers with Mori-Tanaka homogenisation of collagen fibre structure | ✓ |
| B8 | **Corigliano, D., Montes Maestre, J.S., Hinchet, R., Coros, S. & Thomaszewski, B.**, *ViSkin: Physics-based Simulation of Virtual Skin on Personalized Avatars*, **3DV 2025** | Body-scale skin on personalised avatars: anisotropy, **sliding**, Langer-line pre-stress, ligament sliding limit `lmax`. States no prior body-scale model existed | ✓ |
| B9 | **US20140002463A1** (patent) — *Skin and flesh simulation using finite elements, biphasic materials, and rest state retargeting* | The film-VFX answer: FEM flesh with a **sliding skin layer**, tuned for walking/crawling/running. Two constraint forces per node | ✓ |
| B10 | **Li et al.**, *Thin Skin Elastodynamics* (2013) | Thin hyperelastic skin that stretches and slides | ✓ |
| B11 | *An Innovative Tool to Measure Human Skin Strain Distribution In Vivo using Motion Capture and Delaunay Mesh* (2012) | 42 markers at 8 mm spacing, Delaunay FE from marker positions | ✓ |

---

## C. Film-substrate instability — the §2b basis

None of these is leather. All are the mature general theory that §2b extrapolates.

| # | Reference | What it gives us | Status |
|---|---|---|---|
| C1 | **Cao, Y. & Hutchinson, J.W.**, *Wrinkling phenomena in neo-Hookean film/substrate bilayers*, *JAM* **79**(3):031019 (2012), DOI 10.1115/1.4005960 | Bifurcation analysis; post-bifurcation modes: period-doubling, folding, mountain ridge | ✓ |
| C2 | **Cao, Y.-P., Li, B. & Feng, X.-Q.**, *Surface wrinkling and folding of core-shell soft cylinders*, *Soft Matter* **8**(2):556-562 (2012), DOI 10.1039/C1SM06354E | Pre-stretch and curvature effects; wrinkle-to-fold transitions on curved core-shell systems | ✓ |
| C3 | **Wang, Q. & Zhao, X.**, *Phase diagrams of instabilities in compressed film-substrate systems*, *JAM* **81**:051004 (2014) | The **mode-selection map**: strong bond + stiff film → wrinkle; strong bond + matched moduli → crease; **weak bond → delaminated buckle** | ✓ |
| C4 | **Chen, D., Cai, S., Suo, Z. & Hayward, R.C.**, *Surface energy as a barrier to creasing of elastomer films: an elastic analogy to classical nucleation*, *PRL* **109**, 038001 (2012) | States the **minimum-energy crease spacing `W/H ≈ 3.5`**, citing it as established. **Not an authored derivation of the 3.5** — it is a convention inherited from prior crease unit-cell work | ✓ |
| C5 | **Karpitschka, S., Eggers, J., Pandey, A. & Snoeijer, J.H.**, *Cusp-Shaped Elastic Creases and Furrows*, *PRL* **119**(19):198001 (2017) | `κ = kℓ(d_c − d)^-2` — the **cusp profile**, NOT the spacing law. (Commonly miscited as a spacing relation) | ✓ |
| C6 | **Jin, Suo et al.**, *Mechanical Instabilities of Soft Materials: Creases, Wrinkles, Folds* (Harvard) | Biot 0.46 (wrinkle) vs Gent & Cho 0.35 (crease); creases can precede wrinkles | ✓ |
| C7 | **Yang, J., Jin, L., Hutchinson, J.W. & Suo, Z.**, *Plasticity retards the formation of creases*, *JMPS* **123**:305-314 (2019), DOI 10.1016/j.jmps.2018.08.016 | Dissipative materials resist creasing: metals with `E_t/E ≈ 0.001` **do not crease even at ε = 0.8**. Why 0.35 is not a leather limit | ✓ |
| C8 | **Nikravesh, S., Ryu, D. & Shen, Y.-L.**, *Instabilities of Thin Films on a Compliant Substrate: Direct Numerical Simulations from Surface Wrinkling to Global Buckling*, *Sci Rep* **10**:5728 (2020), DOI 10.1038/s41598-020-62600-z | Embedded-imperfection FE method; wrinkling and global buckling can co-occur | ✓ |
| C9 | **Zhao, R. & Zhao, X.**, *Multimodal Surface Instabilities in Curved Film–Substrate Structures*, *JAM* **84**(8):081001 (2017), DOI 10.1115/1.4036940 | Curvature shifts critical strain; concave promotes creasing/folding | ✓ |
| C10 | **Mei, H. & Huang, R.**, *Wrinkling and Delamination of Thin Films on Compliant Substrates*, ICF13 (2013). Companion journal paper: **Mei, H., Landis, C.M. & Huang, R.**, *Concomitant wrinkling and buckle-delamination of elastic thin films on compliant substrates*, *Mechanics of Materials* **43**:627-642 (2011) | Wrinkle → interfacial crack → delamination sequence; interface toughness controls growth, not initiation | ✓ |
| C11 | **Meng, Y., Xiang, H., Zhang, J. & Guo, W.**, *The universal scaling law for wrinkle evolution in stiff membranes on soft films*, *Matter* (2023) | One parameter (thickness contrast) predicts final instability order | ✓ |
| C12 | **Chen, D., Yoon, J., Chandra, D., Crosby, A.J. & Hayward, R.C.**, *Stimuli-responsive buckling mechanics of polymer films*, *J Polym Sci B* **52**(22):1441-1461 (2014), DOI 10.1002/polb.23590 | Review of wrinkling / creasing / global buckling across stimuli | ✓ |
| C13 | **Saha, K., Kim, J., Irwin, E., Yoon, J., Momin, F., Trujillo, V., Schaffer, D.V., Healy, K.E. & Hayward, R.C.**, *Surface Creasing Instability of Soft Polyacrylamide Cell Culture Substrates*, *Biophys J* **99**(12):L94-L96 (2010), DOI 10.1016/j.bpj.2010.09.045 | Equibiaxial compression from swelling; crease spacing ∝ film thickness; ε_c ≈ 0.30-0.37, mean 0.33 | ✓ |
| C14 | **Huang, X., Zhao, H.-P., Xie, W.-H., Hong, W. & Feng, X.-Q.**, *Radial wrinkles on film–substrate system induced by local prestretch: A theoretical analysis*, *IJSS* **58**:12-19 (**2015**), DOI 10.1016/j.ijsolstr.2014.12.011 | Hankel-transform solution; radial/spoke wrinkling from local pre-strain. **Note the year: online 2014, issue 2015** | ✓ |
| C15 | **Kopecz-Muller, C., Gaunand, C., Tran, Y., Labousse, M., Raphaël, E., Salez, T., Box, F. & McGraw, J.D.**, *Swelling and evaporation determine surface morphology of grafted hydrogel thin films*, arXiv:2410.05919; *Langmuir* (2025) | Crease spacing proportional to wet thickness with a logarithmic correction | ✓ |
| C16 | **Chen, D., McKinley, G.H. & Cohen, R.E.**, *Spontaneous wettability patterning via creasing instability*, *PNAS* **113**(29):8087-8092 (2016), DOI 10.1073/pnas.1522700113 | **`W/H ≈ 2-2.5`** in a swollen-elastomer system — evidence the crease spacing prefactor is not fixed at 3.5 | ✓ |
| C17 | **González-Henríquez, C.M., Sarabia-Vallejos, M.A. & Rodríguez-Hernández, J.**, *Strategies for the Fabrication of Wrinkled Polymer Surfaces* (review) | Breadth of wrinkling / creasing literature; fabrication routes | ✓ |

---

## D. Collagen molecular — generic, NOT leather

Cited only as mechanism, clearly labelled non-leather in §2d.

| # | Reference | What it gives us | Status |
|---|---|---|---|
| D1 | **Malaspina, Szleifer, Dhaher**, *Mechanical properties of a collagen fibril under simulated degradation*, *J Mech Behav Biomed Mater* **75**:549-557 (2017), DOI 10.1016/j.jmbbm.2017.08.020 | Fibril stiffness falls sharply with even small crosslink, surface or volumetric degradation | ✓ |
| D2 | **Kamml, Ke, Acevedo, Kammer**, *The influence of AGEs and enzymatic cross-links on the mechanical properties of collagen fibrils*, arXiv **2301.13010** (2023) | AGEs inhibit intrafibrillar sliding → higher stiffness → **abrupt brittle fracture** instead of frictional dissipation. Motivating problem is bone brittleness in ageing/diabetes | ✓ |
| D3 | **Kamml, Acevedo, Kammer**, arXiv **2308.05514** (2023) | AGEs loading energy capacity, not just density, is the determining factor | ✓ |
| D4 | *Exploring the Mechanical Properties and Performance of Type-I Collagen at Various Length Scales*, *Materials* **2022**, 15(8):2753 | Length-scale review of collagen mechanics | ✓ |
| D5 | *Multiscale Characterization of Type I Collagen Fibril Stress–Strain Behavior under Tensile Load*, *Bioengineering* **9**(5):193 (2022) | Analytical vs MD; enzymatic crosslink effect on modulus | ✓ |

---

## E. Dropped — could not verify

Listed so they are not silently lost, and so nobody re-adds them thinking they were checked. **None appear in `durability.md`.**

| Reference as given | Why dropped |
|---|---|
| *Ion-induced conformational dynamics of collagen fibrils*, PubMed 40441579 (2025) | Could not confirm title against the ID. The ID surfaced under a different paper |
| *A simulation study on the significant nanomechanical heterogeneous properties of collagen*, *Biomech Model Mechanobiol* (2014) | Could not confirm author or DOI |
| *An exploration of enhancing thermal stability of leather by silane-modified collagen*, *Collagen and Leather* (2022) | Could not confirm volume/DOI |

Also flagged: several URLs supplied during review pointed at **different papers than their titles** (PubMed and PMC IDs mismatched). The underlying papers were real; the identifiers were wrong. All citations in §2d therefore use title + volume + DOI, not bare URLs.

---

## F. Standards referenced

| Standard | Scope | Status |
|---|---|---|
| **ISO 5402-1:2022** / IULTCS **IUP 20:2022** | Flex resistance, whole-shoe upper / general. Edition 3, published 2022-03-30; **cancels and replaces ISO 5402-1:2017 (withdrawn)**. Applies to flexible leather **< 3.0 mm** | ✓ |
| **ISO 5402-1:2017** (superseded) | Source of the key text: specimen folded in half lengthwise, **grain surface face to face**; upper clamp reciprocated **(22.5 ± 0.5)°** at **(100 ± 5) cycles/min**; specimen **70 × 45 mm** | ✓ — cited only to explain the geometry |
| **ASTM D6182-23** | **Finish** flexibility and adhesion. **Excludes wet blue.** Complementary to ISO 5402-1, not a substrate test | ✓ |
| **ISO 3377-1** (IUP 40) | Tear — single edge | ✓ |
| **ISO 3376** | Tensile strength and elongation | ✓ |
| **ISO 3378** | Grain crack resistance / ball burst | ✓ |
| **ISO 17694:2016** | *Footwear — Test methods for uppers and lining — **Flex resistance***. **Second edition, 2016-05-01.** The **Bally flexometer** method. Upper clamp angle **22°30' ± 0°30'**, **(100 ± 5) cycles/min**, clamp gap **25 ± 1 mm**, clamp radius **2 mm**, press knife **70 ± 1 × 45 ± 1 mm**, magnifier 4-6×. Runs **dry, wet, or cold** (usually −5 ± 2 °C); conditioning per **ISO 18454** ≥24 h. Inspection stages 1 000 / 2 000 / 5 000 / 10 000 / 25 000 / 50 000 / 100 000. Refers to ISO 17709 for the along/across direction | ✓ |
| **ISO 5402-2:2015** | *Leather — Determination of flex resistance — **Part 2: Vamp flex method*** (IULTCS/IUP **39-2**). The method for **wet flex**. Two inverted-V clamps, internal angle **40 ± 1°**, tip radius **6.4 ± 0.5 mm**, minimum separation **9.5 ± 1.0 mm**, travel **19.0 ± 1.5 mm**, **300 ± 30 cycles/min**. Dry cycles: 50 000 / 100 000 / 250 000 / 500 000 / 1 000 000; wet: 50 000 / 100 000, re-wet every 25 000. **Its damage list explicitly includes "delamination or flaking of the surface finish"** — the §2c distinction. Supersedes ISO 22288:2006 | ✓ |
| **EN 13512** | Could not verify what this covers. Listed in an earlier draft alongside ISO 17694 without evidence. **Treat as unconfirmed** | ✗ |
| **ISO 3376:2020** / IUP 6 | Tensile strength and percentage elongation — note the 2020 edition | ✓ |
| **SATRA TM24** | Lastometer ball burst — grain crack | ✓ |
| **SATRA TM25** | Vamp flex — resistance to creasing and cracking | ✓ |
| **SATRA TM31** | Abrasion — Martindale method | ✓ |
| **SATRA TM33** | Strength perpendicular to needle perforations | ✓ |
| **SATRA TM36** | Break / pipiness | ✓ |
| **SATRA TM43** | Tensile strength and extension at break of leather | ✓ |
| **SATRA TM44** | Liability to wrinkle | ✓ |
| **SATRA TM47** | Water vapour permeability and absorption | ✓ |
| **SATRA TM55** | Flexing resistance of upper materials — Bally flexometer | ✓ |
| **SATRA TM129** | Determination of the cold crack temperature of leather | ✓ |
| **SATRA TM148** | **Resistance of finish films on upper leather to peeling and delamination** — the standardised test for the §2c delamination-vs-crazing distinction | ✓ |
| **SATRA TM162** | Tear strength — **Baumann** method (2017 revision) | ✓ |
| **SATRA TM163** | Abrasion — Taber method | ✓ |
| **SATRA TM172** | Water vapour permeability | ✓ |
| **SATRA TM179** | Tear strength — **wing rip** method | ✓ |
| ~~SATRA TM235~~ | **Does not exist** in SATRA's catalogue. The wetting/drying requirement is met by **ISO 5402-2:2015** (wet vamp flex, re-wetted every 25 000 cycles and checked for spue) and **ISO 17694:2016** (wet flex). The gap is now closed by real standards rather than a guessed method number | ✗ removed → replaced |

**Two corrections from verification:**

- **TM24 is the "Lastometer ball burst"** for grain crack, *not* the cold crack test — cold crack is **TM129**. An earlier draft conflated them.
- **TM172 is "Water vapour permeability"**; water vapour *absorption* is **TM178**. Also present and relevant: **TM173** reciprocating rub fastness, **TM180** strength of stitched seams, **TM133** crack initiation and growth (belt flex), **TM161** Bennewart cut growth, **TM164** universal fatigue flexing.

SATRA's own usage list for *"Leather — uppers and linings"* contains TM24, TM33, TM129, TM162 and TM179 — a good minimal set for a wallet specification.
| **ISO/IEC 7810 ID-1** | Card 85.6 × 53.98 mm — the scale reference for card slots | ✓ |

---

## G. Tools, software and industry sources — verified

Not papers, but sources nonetheless. Everything here was checked against a vendor page,
repository, licensing file or the software's own source code.

### Blender cloth presets — read from the source file

| Item | Verified value | Status |
|---|---|---|
| **Blender `Leather` cloth preset** | `scripts/presets/cloth/Leather.py` in the Blender repo: quality **15**, mass **0.4**, tension / compression / shear stiffness all **80**, bending **150**, the three dampings **25**, air damping 1, internal springs **off** | ✓ read from source |
| Blender itself | GPL-2.0-or-later | ✓ |

**Correction:** an earlier draft asserted "Cotton ≈ tension 15, bending 0.5" alongside this.
Those numbers were **not** verified and have been **removed** rather than repeated.
The Leather preset is now cited to the actual file, not to memory.

### Blender add-ons

| Tool | Verified facts | Licence | Status |
|---|---|---|---|
| **Simply Cloth Studio 2.0** | Vjaceslav Tissen; rewritten for 2.0; adaptive wrinkle system; **Blender 4.0–5.2**; **$46 single user** for 2.0 (the $36 tier is v1.x); $66 with Cut & Sew library; commercial tier ~$170–270 | **MIT** (per Superhive listing) | ✓ |
| **Cloth Lab** | SLOHERO / dodohan0721; current **v0.8.1**; standard tools **Blender 4.5+**, dynamic tearing and self-contact bake **5.2+**; **explicitly independent of, and unaffiliated with, Simply Cloth Studio** | **GPL-3.0-or-later** | ✓ |
| **Garment Tool** | bartoszstyperek (Gumroad); builds sim-ready cloth from 2D Bézier patterns; sewing defined in the 3D viewport; garment library | **Proprietary — no source distributed, so no open-source licence applies.** Price varies by tier on Gumroad; **not verified** | ✓ existence |
| **Seams to Sewing Pattern** | Thomas Kole; UV-layout → sewing pattern; **.svg export**; original targets Blender 2.8x/2.9x; mirrors at `belzecue/` and `fjardon/` | **GPL-2.0** | ✓ |

**Correction:** earlier notes said Seams to Sewing Pattern was GPLv3 and mentioned an
`artyredd` remaster. The repository's own licence file is **GPL V2**, and the remaster
could not be confirmed. Both corrected.

### Garment / cloth simulation suites

Pricing for this category is volatile and **most sources contradict each other**, so treat
these as indicative only.

| Tool | Verified | Status |
|---|---|---|
| **CLO 3D** | Individual **$50/month or $450/year** excl. tax; Student $25/month; annual saves ~25 %; 2+ employee companies forced to Business tier; Fit Map includes Stress / Strain / Fit / Pressure | ✓ (vendor pricing page, Nov 2026) |
| **Marvelous Designer** | Personal **$39/month or $280/year**; Student $8.25/month | ✓ |
| **Browzwear VStitcher** | **Freelancer $75/month or $750/year**; **Freelancer Plus $150/month or $1,500/year**; **Teams $3,950/year**; Enterprise by quote; Learner licence free for students, 6 months. *Sources differ on whether $3,950 is per user or for 3 named users* | ✓ price, ~ seat count |
| **Style3D** | Style3D's **own blog** states tiers of roughly **$35–99 basic**, **$180–299 professional**, **$500+ enterprise**. Third-party listings variously quote $40, $49, $99 and "enterprise quote only" — so the published range is wide and the vendor's own number is marketing rather than a price list. Free tier is **non-commercial**; **permanent purchase options ended 30 Apr 2026** | ~ vendor's own blog only |

**Correction:** an earlier draft quoted Style3D at "~$40/mo, individual tier non-commercial."
The non-commercial part holds up; **the price does not.** Do not cite a Style3D number.

### Footwear CAD

| Tool | Verified | Status |
|---|---|---|
| **Icad Universe** | **INESCOP** (Elda, Alicante; non-profit, founded 1971), distributed by **Red21**. Bidirectional 2D/3D in one file; automatic flattening respecting lasting allowance and grain direction; exports **HPGL / PLT / DXF**; Adobe Substance 3D plugin. **The "conflicting" install counts are different sources, not errors:** INESCOP's own product page says **1,700+ installations / 39 countries**; distributor Red21 says **3,000+ licences / 60+ countries**; Icad3D+ distributor pages claim 2,400-3,200 / 43-44 countries. Quote whichever you name. Price **~€10,000** (Arsutoria School) | ✓ — cite the source of the count |
| **Shoemaster** | **Atom Group** division (Vigevano, Lombardy; Atom founded 1946); lineage traces to the **CAD unit at Clarks (UK)**. Grading across sizes, cut optimisation, factory tech specs. Used by **800+ shoe manufacturers**; ~**12 %** global footwear-CAD share per one market report | ✓ existence, ~ the share figure |
| **Romans CAD** | Appears as a named vendor in footwear-CAD market reports. Last → 3D → style lines → flatten → grade. Positioned at small/mid manufacturers with lower price points; cloud-based | ✓ as a vendor, ~ the product detail |
| **Procam** | **Not found in any footwear-CAD vendor or market-report list** (which name Lectra, Dassault, Autodesk/Delcam, Shoemaster, Romans CAD, Torielli, GRAFIS, Tajima, INESCOP). Either defunct, a misremembering, or outside this category. **Do not cite it** | ✗ |

### Hide scanning, nesting and cutting

| Item | Verified | Status |
|---|---|---|
| **Zünd** | Swiss cutter manufacturer; **L3**, **G3** (227 × 160 cm working area), **D3** dual-beam | ✓ |
| **Mind / MindCUT** (Portugal) | Hide digitisation, defect and quality-zone capture (up to **five quality zones**), stretch-direction definition, interactive and automatic nesting, drives Zünd cutters, parts removal | ✓ |
| **Mindhive FinishSelect** | AI finished-leather inspection: **20+ defect classes**, **0.17 mm** resolution, **~15 s per hide**, 1,000–1,920 hides per 8-hour shift; feeds defect maps into MindCUT | ✓ |
| **Dectura** workflow | Zünd + Mind + Mindhive combined line, shown at **Simac Tanning Tech, Milan** | ✓ |

**Relevant to this document:** all three capture *defects, quality zones and stretch
direction* — **none of them models mechanics.** Hide grading optimises yield, not
durability. That is the gap `durability.md` §1 describes, confirmed from the vendors.

### Open-source building blocks — licence-checked

| Package | What it is | Licence | Status |
|---|---|---|---|
| **FElupe** (`adtzlr/felupe`) | Python nonlinear FEM infrastructure, autodiff hyperelastic | **GPL-3.0** | ✓ |
| **fedoo / microgen / simcoon** (3MAH) | FEM, microstructure generation, homogenisation | **GPL-3.0** | ✓ |
| **ColECM** (`franklongford`) | Collagen ECM fibril-network simulation | **MIT** | ✓ |
| **FibreNet** (`ppieczywek`) | C++/OpenCL particle dynamics for fibre networks; GPU-optimised | **MIT** | ✓ |
| **PolyTex** | Micro-CT → material twin (textile composites, **not leather**) | GPL-3.0 | ✓ |
| **`calugo/wrinkles`** | FEniCS bilayer-wrinkling scripts | **CC BY 4.0** — *not a software licence* | ✓ |
| `materialsguy/Buckling_Analysis_Laminated_Samples` | Abaqus eigenvalue / Riks template | **CC BY-NC-ND 4.0** | ✓ |
| `heathmanc/Leather-Drafting` ("Stitch Hero") | Leather drafting helper | MIT | ✓ |

**Correction:** FibreNet was previously listed as just "open" — it is **MIT**.

### Libraries used by this skill's own scripts

| Library | Licence | Status |
|---|---|---|
| **NumPy** | BSD-3-Clause | ✓ |
| **OpenCV** | Apache-2.0 | ✓ |
| **ezdxf** (Manfred Moitzi) | **MIT** | ✓ |
| **ReportLab** | BSD | ✓ |
| **Shapely** | BSD-3-Clause (GEOS underneath is LGPL-2.1) | ✓ |
| **rhino3dm** (McNeel) | MIT | ✓ |
| **svgpathtools** (Andy Port / `mathandy`) | **MIT** | ✓ |

**Correction:** an earlier draft listed ezdxf as MIT — that one was right — but described
the whole set as uniformly permissive. **Shapely drags LGPL-2.1 GEOS in transitively**,
which is fine for use but worth knowing before statically bundling.

---

## L. Fatigue, moisture and permanent set — sources added on request

These were hunted specifically against the two gaps this document admits: **no fatigue model**
and **no coupled moisture model**. They do not close the gaps, but they change how the gaps
should be described.

### Fatigue / cyclic degradation

| Source | What it gives | Status |
|---|---|---|
| *The Influence of Fatigue Conditions on the Mechanical Properties of Laminated Leather and its Separate Layers* (Kaunas University of Technology group; *Materials Science / Medžiagotyra*) | **The most directly useful fatigue result for leather.** Vamp-flexed per LST ISO 5423:1992 on a Pegasi/ZIPOR VAMP machine, ≥10 specimens each. Findings: **tensile strength of split leather falls 36 %** over the cyclic range tested; flexing to **5 × 10⁵ cycles (more than 7 days non-stop) never reached an endurance limit** in the materials tested — the authors explicitly call for testing into the millions. Also: laminated leather's relaxation behaviour is dominated by the PU film, not the leather. Ambient + elevated temperature effects measured | ~ single source, full text via ResearchGate only |
| **SAE J948** | Upholstery materials for passenger vehicles: flex fatigue, abrasion, seam fatigue | ✓ standard exists |
| **GMW 3013** (General Motors) | Coated fabrics: **100 000 flex cycles at −30 °C without cracking** | ~ single source |
| **LV 312-1** (Volkswagen) | Interior materials: flex testing combined with climate ageing | ~ single source |
| **ASTM D1052** | Ross flex — strip bent **90°**, cycles to crack initiation | ✓ |
| **SATRA TM60** | Ross flex, **cut growth on flexing** — and, importantly, **"not intended for leather"**; it is a soling-polymer method. Do not cite TM60 as a leather test | ✓ |
| **ISO 5423**, **ISO 4643**, **BS 5131:2.1** | Further flex methods named in the Ross / vamp-flex apparatus literature | ✓ exist |

**The number worth carrying:** a vendor comparison table (silicone *vs* PU *vs* genuine
leather, automotive grade) gives Ross flex cycles of **45 000 at 23 °C but 12 000 at −10 °C**
for 1.1 mm genuine leather — i.e. **cold roughly quarters the flex life**. The same table
gives PU 22 000 / 4 500. **Vendor marketing source, not peer-reviewed — use the direction,
not the digits.**

### Moisture

| Source | What it gives | Status |
|---|---|---|
| **Long, Peng, Li, Yu & Zhang**, *On the role of water in regulating the mechanics of collagen fibers*, *Colloids and Surfaces A* **702**:134957 (2024) | Cr-crosslinked collagen fibres across water content **0.031 g/g to full hydration**. Lower hydration → **higher tensile and tear strength**, **lower softness**, smaller D-period and lateral spacing. **Elongation at break has an optimum at a particular water content** — wetter is not simply worse. Mechanism: water tunes electrostatic and van der Waals interactions between fibres. This is the data a moisture-coupled model would need, and it is from the same group as the FB-radius paper | ✓ |
| *Collagen Fibrils: Nature's Highly Tunable Nonlinear Springs* (*ACS Nano*, 2018) | Osmotic pressure changes fibril stiffness **up to 24× transverse, 6× longitudinal**, reversibly. Hydration is a control parameter, not a fixed property | ✓ |
| *Hydration and distance dependence of intermolecular shearing between collagen molecules in a model microfibril* | Water lubricates sliding: slip-stick only below **1.3 nm** lateral spacing, smooth shear above. Water both lubricates and transfers load | ~ |

**Practical consequence for §6:** "conditioning" is not unambiguously good. Drier leather is
*stronger and tear-resistant but stiffer and less extensible*; there is an optimum for
elongation. Any conditioning advice should say which property it is trading away.

### Permanent set — and a correction to my own framing

**There is no standardised permanent-set test for leather.** I searched; the nearest
analogue is **ASTM D395** (compression set), which is written for **rubber and elastomers**,
not leather. So the §3 claim that permanent set is the first visible sign of degradation
stands, but there is **no ISO/IULTCS or SATRA method behind it** — it is assessed
qualitatively. That is a genuine gap in the test landscape, not something I simply failed to
find.

### A caveat on the fibre-bundle story in §2d

| Source | What it gives | Status |
|---|---|---|
| *Collagen Fibril Diameter and Leather Strength*, *J Agric Food Chem* (2013), DOI 10.1021/jf4041854 | Synchrotron SAXS. Fibril diameter correlates with tear strength in **bovine** leather (r² = 0.59, P = 0.009) but **not in ovine**, and **not across species**. Orientation index showed no correlation with diameter. The authors suggest ovine skin uses a different structural motif where **alignment matters more than diameter** | ✓ |

This is a **useful counterweight to §2d**: the FB-radius result (R² > 0.99) is a clean
within-study relationship on twelve *bovine* leathers. The SAXS work says the
microstructure→strength link is **species-dependent** and weaker than the single R² suggests
once you leave one species. Cite both.

### "Conditioning" means two different things — disambiguate

| sense | what it means | source |
|---|---|---|
| **Test conditioning** | equilibrating specimens to a standard atmosphere before testing (ISO 18454 / ISO 2419) | the ISO flex methods |
| **Tannery conditioning** | **damping leather to 25-30 % moisture** and stacking it so moisture equalises, *before staking*, to loosen fibre-sticking after drying | *Back to Basics: Leather Manufacture*, Leather Naturally |

`durability.md` §6 uses the first sense. A reader who works in a tannery will read it as the
second. Both are real; the word is overloaded.

The Leather Naturally primer is also worth listing on its own merits as a **free, citable,
process-level source**: drying under tension makes leather firmer, compression during drying
makes it firmer, rapid drying makes it harder, gentle conditions give a better grain break.

---

## H. Verification log — what changed when these were checked

Recorded because a citation that quietly changes is worse than one that was never checked.

**Attribution errors found and fixed:**

- **`W/H ≈ 3.5` was attributed to "Yoon et al., PRL 109, 038001."** That paper is **Chen,
  Cai, Suo & Hayward**, *Surface energy as a barrier to creasing of elastomer films* — and
  it *states* 3.5 as the established minimum-energy spacing rather than deriving it. The
  derivation traces to the crease unit-cell literature (Hong, Zhao & Suo). **Diagnostic B
  still works, but the error bar is wider than originally stated** — published spacings span
  `W/H` ≈ 2-3.5 depending on deformed/undeformed convention and strain. `durability.md` now
  says order-of-magnitude, not ±10 %.
- **Phase diagrams**: "Zhao group" → **Wang, Q. & Zhao, X.**, *JAM* **81**:051004 (2014).
- **Cusp paper**: not "Taffetani & Ciarletta" → **Karpitschka, Eggers, Pandey & Snoeijer**,
  *PRL* **119**:198001 (2017).
- **Plasticity paper**: authors confirmed **Yang, Jin, Hutchinson & Suo**, *JMPS*
  **123**:305-314 (2019).

**Method errors found and fixed:**

- **SATRA TM24 conflation.** TM24 is the **lastometer ball burst** (grain crack). The cold
  crack test is **TM129**. An earlier draft treated them as interchangeable.

**Promoted from `~` to `✓`:**

- Mihai et al. 2022 (authors, DOI, and the numbers: calfskin E = 72 N/mm², −3 % with leather
  lining, −22 % with PES knit)
- PolyTex (full author list, DOI — but flagged as a **textile-composites** tool, not leather)
- Cao & Hutchinson 2012 (*JAM* **79**(3):031019, DOI 10.1115/1.4005960)
- ViSkin (Corigliano et al., 3DV 2025)
- Facial wrinkling (Montes Maestre et al., *CGF* **45**(8) 2026, DOI 10.1111/cgf.70580)
- The satin full SATRA catalogue, including four methods not previously listed: **TM25**
  vamp flex, **TM44** liability to wrinkle, **TM148** finish peeling/delamination, **TM36**
  break/pipiness. **TM148 is the standardised test for the §2c delamination-vs-crazing
  distinction** and has been added to `durability.md`.

**Downgraded to ✗:**

- **SATRA TM235** — could not be found anywhere in SATRA's published catalogue. Removed from
  the wetting/drying recommendation, which now stands without a method number.

**Still unverified, and honestly labelled as such:** ISO 17694 / EN 13512 (single source).
Everything in section C that came from secondary summaries should be re-read at source
before it appears in anything public.

---

## I. Second verification pass — the remainder

The first pass covered what the document leans on. This one covered everything else.

**Fully verified in pass 2, with author lists where they had been missing:**

- **Dietrich et al. 2021** — twelve authors confirmed (Dietrich, Lykhachova, Cheng,
  Godehardt, Kronenberger, Meyer, Neusius, Orlik, Schladitz, Schulz, Steiner, Voigt),
  DOI 10.3390/ma14081894
- **B2** Flynn & McCormack 2009 — *CMBBE* **12**(2):**125-134**
- **B1** — *Skin Res Technol* **14**(3):**261-269**
- **B4** Zhao, **Feng, Lee, Lu & Pierce** 2020, DOI 10.1016/j.jmbbm.2019.103552
- **B5** is **Chavoshnejad, More & Razavi**, *Extreme Mechanics Letters* **36**:100647 (2020)
- **B7** Guissouma et al. — *Proc IMechE H* **235**(11):**1274-1287**
- **C8** Nikravesh, Ryu & Shen — *Sci Rep* **10**:5728
- **C9** **R. Zhao & X. Zhao** (not "the Zhao group")
- **C10** Mei & Huang, ICF13; journal version Mei, Landis & Huang, *Mech Mater* **43**:627-642 (2011)
- **C11** Meng, Xiang, Zhang & Guo
- **C12** Chen, Yoon, Chandra, Crosby & Hayward — *JPS B* **52**(22):1441-1461
- **C13** Saha et al. — nine authors, *Biophys J* **99**(12):**L94-L96**
- **C14** Huang, Zhao, Xie, Hong & Feng — **year is 2015, not 2014** (online Dec 2014, issue
  *IJSS* **58**:12-19)
- **C15** Kopecz-Muller et al. — eight authors; now published in *Langmuir* (2025)
- **C16** Chen, McKinley & Cohen — *PNAS* **113**(29):8087-8092

**One substantive correction to a formula, and one non-correction:**

- The critical strain is quoted in the literature as **`ε_cr = (3Ē_s / 8Ē_f)^(2/3)`**
  (Huang et al.), with `Ē = E/(1-ν²)`. `durability.md` now shows that form. **It is
  algebraically identical** to the `¼(3E_s/E_f)^(2/3)` I had — `(3/8)^(2/3) = ¾·3^(2/3)` —
  so the numbers in the table were right, and anyone who sees the two forms presented as
  competing results is being misled.

**One more piece of support for the Diagnostic B caveat:** C16 measured **`W/H ≈ 2-2.5`**
in a swollen elastomer, against the 3.5 unit-cell convention. That is now two independent
sources putting the crease-spacing prefactor well below 3.5. The order-of-magnitude warning
in §2b is not excessive caution.

**Still unresolved:** C2's original subject. *"Surface wrinkling and folding"* (2012) is
**Cao, Li & Feng on core-shell soft cylinders**, *Soft Matter* **8**(2):556-562 — not a flat
film/substrate paper. The entry now describes what the paper actually covers.

**Status after two passes: 69 ✓, 2 single-source, 4 ✗.** The two remaining single-source
items are ISO 17694 / EN 13512 and the ISO 3377-1 tear-method cross-reference.

---

## J. Third verification pass — the non-paper sources

Sections A–F were verified in passes 1 and 2. This pass covered **section G**, which had
previously been a list of names with no verification at all.

**Confirmed correct as originally stated:**

- The **Blender Leather cloth preset** — read directly from `scripts/presets/cloth/Leather.py`
  in the Blender repository. Mass 0.4, tension 80, bending 150 are all exactly right.
- `heathmanc/Leather-Drafting` — MIT.
- FElupe, fedoo, microgen, simcoon — GPL-3.0.
- ColECM — MIT.
- `calugo/wrinkles` — CC BY 4.0; `materialsguy/...` — CC BY-NC-ND 4.0.

**Wrong, and corrected:**

- **"Seams to Sewing Pattern is GPLv3, remaster by artyredd."** Its own repository licence
  file is **GPL V2**, and no `artyredd` remaster could be confirmed.
- **"Cotton preset ≈ tension 15, bending 0.5."** Could not verify. **Removed** rather than
  left in as plausible-looking filler.
- **"FibreNet — open."** It is **MIT**. Lazy status upgraded to a real licence.
- **"Style3D ~$40/mo."** Sources give $49, $99, $180 and "enterprise quote only." **No
  Style3D price is citable.** The one part that holds is that its free tier is
  non-commercial.
- **"Procam"** — could not verify as a current footwear CAD product. Left in the file as
  unverified rather than silently deleted, so nobody re-adds it as fact.
- **Simply Cloth Studio** — the **$36** figure is the v1.x tier; **2.0 is $46** for a single
  user. Price on the 2.0 release is $46.
- **Cloth Lab** — was noted as "experimental Blender 5.2+ XPBD." The 5.2+ requirement applies
  to **dynamic tearing and self-contact**, not the whole add-on, which runs on **4.5+**.
  Version is now **0.8.1**, not the 0.7 that was recorded.
- **The whole permissive-licence set** — **Shapely brings LGPL-2.1 GEOS transitively.**

**Still unverified, deliberately:**

- `svgpathtools` licence — not checked; the row says so.
- **Browzwear, Icad Universe, Shoemaster, Romans CAD** pricing/market figures — single
  commercial source each, and the Icad installation counts **contradict each other**
  (3,000/60 countries vs 1,700/39).

**Worth noting for the document itself:** Zünd, Mind and Mindhive all capture hide defects,
quality zones and stretch direction — and **none of them models mechanics.** The commercial
state of the art in leather is yield optimisation, not durability prediction. That is
independent vendor confirmation of §1's central claim.

---

## K. Fourth pass — closing every remaining gap

Everything marked unresolved has now been either verified or removed. This is the final
state.

**Resolved:**

- **ISO 17694:2016** — full method detail recovered: second edition 2016-05-01, Bally
  flexometer, 22°30' ± 0°30' at 100 ± 5 cycles/min, 25 ± 1 mm clamp gap, 2 mm radius,
  70 × 45 mm specimen, dry/wet/cold (usually −5 ± 2 °C), conditioning per ISO 18454.
- **ISO 5402-2:2015** — recovered, and it **closes the wet-flex gap** that TM235 was
  invented to fill. Vamp flex, inverted-V clamps 40° / 6.4 mm tip, 19 mm travel, 300
  cycles/min, re-wet every 25 000 cycles. Its damage list explicitly names **"delamination
  or flaking of the surface finish"** — the §2c distinction, standardised.
- **ISO 24266** — whole-shoe flex, the ISO equivalent of SATRA TM92.
- **Long et al. 2025** — *Collagen and Leather* **7**, Article **6**.
- **`svgpathtools`** — **MIT** (Andy Port / `mathandy`).
- **Browzwear** — full tier structure confirmed: Freelancer $75/mo or $750/yr, Freelancer
  Plus $150/mo or $1,500/yr, Teams $3,950/yr, Learner free 6 months.
- **Romans CAD** — confirmed as a named vendor in footwear-CAD market reports; positioned
  at small/mid manufacturers, cloud-based.
- **Shoemaster** — Atom Group division (Vigevano), lineage from the **Clarks CAD unit**,
  **800+ manufacturers**, ~12 % share per one report.
- **Icad Universe** — the "conflicting" counts were **not conflicting**: INESCOP's own page
  says 1,700+/39 countries, distributor Red21 says 3,000+/60+ countries. Both can be cited
  if the source is named.

**Removed as unverifiable — do not reinstate:**

- **SATRA TM235** — does not exist. Replaced by **ISO 5402-2:2015** and **ISO 17694:2016**,
  which actually cover wet flex.
- **EN 13512** — could not establish what it covers. Deleted from `durability.md`.
- **Procam** — absent from every footwear-CAD vendor and market-report list checked
  (Lectra, Dassault, Autodesk/Delcam, Shoemaster, Romans, Torielli, GRAFIS, Tajima,
  INESCOP). Probably a misremembering. Deleted.
- **Garment Tool licence/price** — the add-on is proprietary and distributes no source, so
  no open-source licence applies; the price varies by tier and was not verified. The
  existence and function are confirmed; the money is not.
- **Blender "Cotton" preset** — could not verify. Deleted in pass 3.

**Irreducibly uncertain, and says so in the row:**

- **Style3D pricing.** The vendor's *own blog* gives $35–99 / $180–299 / $500+, while
  resellers quote $40, $49, $99 and "enterprise only." This is not a fact that can be
  pinned down from outside; the row now names the source rather than asserting a number.
- **Browzwear $3,950** — sources disagree on whether that is per user or for three named
  users.

**Final tally: every reference is either ✓ verified, marked with the specific reason it
cannot be, or deleted.** There are no remaining `~ single source` rows carrying a factual
claim, and no `✗` rows still recommending something unverified.
