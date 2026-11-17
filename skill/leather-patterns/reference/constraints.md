# Design constraints, and why they exist

These are the rules that separate a pattern that sews from one that does not.

## 1. Closed stack must stay under ~8 mm

Every layer adds up: outer shell + 2 banks of slots + bill divider. Past roughly
8 mm the wallet cannot fold flat, the spine bulges, and the corner radii stop
matching. Fix by thinning slot leather (0.7 → 0.6) or reducing slot count, not by
making the wallet bigger.

## 2. Interior must be shorter than the outer, 6–10 mm per end

The outer layer travels around a longer path when folded. If interior and outer are
the same length the wallet *waves* along the fold — the single most common
first-wallet failure. 8 mm per end is a safe start; go higher with thick leather or
many pockets.

## 3. Fold compensation = pi x t per fold

The material at the fold forms a half-cylinder of radius t. Its arc length is pi x t,
so the outer piece must be that much longer than the sum of the two panels.
1.0 mm leather → 3.14 mm. Trifold → two folds → 6.28 mm.

## 4. You cannot fit an exact pitch around an arbitrary perimeter

A pricking iron has fixed teeth at a fixed pitch. For a perimeter P and pitch p,
`P / p` is almost never an integer. Real makers either stagger the last gap or run
variable pitch. `stitch_run` solves it explicitly and reports the actual pitch.

## 5. Reveal must stay above ~6 mm

The reveal is how much card sticks out. Below 6 mm a card cannot be gripped, and
worse, it slides down behind the slot. 8 mm is the usual compromise.

## 6. Slot width = card width + 2 mm

A card is 85.6 mm (ISO/IEC 7810 ID-1). Too tight and cards bind; too loose and they
fall out sideways. 87.6 mm is the standard answer.

## 7. Corner radius vs leather temper

Below ~4 mm radius, stiff veg-tan cracks along the edge finish. R5 for slots,
R8 for outer is safe. Softer leather tolerates tighter.

## 8. Stitch line offset 3–4 mm by hand, 5–6 mm by machine

The stitch line must be far enough in that the needle does not tear out the edge,
close enough that the edge stays flat. The hole radius is subtracted from that.

## 9. Banknotes drive the long dimension

A euro note is 156 x 66.3 mm (the longest common note; US bills are the same length).
A bifold folds the note, so the bill compartment only needs to clear the *folded*
height — which is why a wallet can be shorter than a note is long. A wallet that
must hold notes *unfolded* is a long wallet, a different design.
