# Per-species anatomy

One file per animal group, all using the framework from `../taxonomy.md`
(**L0** animal · **L1** region · **L2** cut · **L3** layer · **L3.5** hard parts ·
**L4** direction).

Read `../README.md` for the framework, `../appendages.md` for the hard-part axis that exotic
leather requires, `../properties.md` for the numbers, and `../reference-matrix.md` for the
**all-species tables in one place**.

## The files

| File | Covers | The one thing it adds |
|---|---|---|
| `bovine.md` | cow, steer, bull, calf, kip, buffalo, bison, zebu | the reference case; how the bovines differ |
| `equine.md` | horse, colt, pony | index into `../horse.md` — front / strip / shell / culatta |
| `ovine-caprine.md` | sheep, lamb, goat, kid | **shoulder is the strongest region in both — not the rump** |
| `porcine.md` | pig, hog, peccary | the grain runs **through** the thickness, uncorrectable |
| `ostrich.md` | ostrich body + leg | four materials from one bird; the crown is ⅓ of the skin |
| `poultry.md` | emu, rhea, chicken, turkey, duck, goose | follicle **distribution**: crown vs uniform pin |
| `crocodilian.md` | crocodile, alligator, caiman | graded on the belly only; **calcium is the quality variable** |
| `reptile-snake.md` | snakes, lizards | scales are folds of skin; failure is **lift**, not crack |
| `fish-stingray.md` | stingray, shark, salmon, cod, wolffish, perch, tilapia, pirarucu, sturgeon, eel… | denticles; stingray is armour, shark is leather; the full fish roster |
| `kangaroo-deer-other.md` | kangaroo, deer, elk, camel, buffalo, seal | uniform-fibre species where the region map stops mattering |
| `heavy-exotics.md` | elephant, hippo, yak, camel, fur-bearing | **thickness is the constraint, not region**; double-face and nap |
| `amphibian-shell.md` | cane toad, turtle, "is it a hide?" | the smallest real trade; and where the word "leather" stops applying |
| `heavy-exotics.md` | elephant, hippo, yak, camel, fur-bearing | **thickness is the constraint**; double-face and nap direction |

## Coverage at a glance

**Mammals** cow steer bull ox calf kip buffalo bison zebu yak goat kid sheep lamb pig hog
peccary horse colt pony donkey mule kangaroo deer elk moose camel llama alpaca rabbit cane toad
elephant hippo seal walrus + fur-bearing (beaver chinchilla coyote fox lynx mink muskrat opossum
raccoon sable wolf)

**Birds** ostrich emu rhea chicken turkey duck goose

**Reptiles and amphibians** crocodile alligator caiman snake lizard teju turtle tortoise

**Fish** stingray shark salmon cod haddock perch wolffish eel sturgeon tilapia pirarucu pacu
catfish carp plaice parrotfish dolphinfish moray boxfish puffer

Animals the sources name but for which **no reliable anatomy exists** are named in
`../reference-matrix.md` §1 with a `~` and no invented detail.

## Reading order by question

- *"Which part of this hide should I cut from?"* → the species file, L1/L2 tables.
- *"Will this fold?"* → `../appendages.md` first if there are scales, quills or osteoderms;
  otherwise `../../durability.md`.
- *"Is this real or embossed?"* → `../appendages.md`, last section.
- *"How big a skin do I need?"* → the species file, or `../reference-matrix.md` §5. Crocodilian
  is measured by **belly width**; ostrich crown is a **third** of the hide; shell cordovan is an
  **oval**. Area in square feet tells you far less than shape does.
- *"Is this even leather?"* → `amphibian-shell.md`, last section.
