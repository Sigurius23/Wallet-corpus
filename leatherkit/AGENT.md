# Agent skill: leather pattern generation

Instructions for a coding agent asked to produce a leather pattern.

## Do not measure pixels. Write code.

1. **Extract intent into parameters**, not geometry. Ask for: style, card
   capacity, cash/coin, leather thickness, pricking-iron pitch, corner radius.
2. **Default anything unspecified** (see table) and state the assumption.
3. **Call `leatherkit`**, never hand-write coordinates.
4. **Read `report.json` back** and sanity-check it before declaring done.
5. **Deliver files**, not descriptions.

## Defaults

| Parameter | Default | Why |
|---|---|---|
| pitch | 3.85 mm | European standard; 3.38 is the Japanese alternative |
| outer leather | 1.0 mm | stiff enough to hold shape |
| slot leather | 0.7 mm | thinner, or the stack bulges |
| reveal | 8 mm | below 6 mm cards cannot be gripped |
| clearance | 2 mm | card is 85.6 mm wide, slot 87.6 |
| interior_gap | 8 mm/end | below ~6 mm the wallet waves when folded |
| corner_r | 5 mm slots / 8 mm outer | tighter cracks edge finish |

## Validation before answering

```
outer_w > 2 x (ISO_CARD_W + 2)     # both panels must fit a card
closed_stack < 8 mm                # else it will not sit flat
stitch spacing_error < 0.15 mm     # or warn the user
fold_comp == pi x leather_t        # never omit
```

## Things to refuse / flag

- Cloning a named commercial design from photos (design-rights exposure in the EU)
- Pitch not in the standard set, without explicit confirmation
- A requested closed stack above ~8 mm without warning the user
