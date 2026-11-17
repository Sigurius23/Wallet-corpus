# When the user supplies a photo instead of a spec

Run the deterministic measurement first. **Never estimate dimensions by eye** —
it is 20 %+ wrong without a scale reference, and still 5–8 % wrong with one, which
breaks a cutting template.

## Procedure

1. Check for scale. If there is no ISO card (85.6 x 53.98 mm) or ArUco marker in
   frame, stop and ask for one:

   > "Please place a bank card flat beside the wallet and shoot straight down from
   > about 30 cm, so the whole wallet and all four card corners are visible."

2. Measure:

   ```bash
   python3 scripts/inspect_photo.py photo.jpg --scale card --debug debug/
   ```

3. Read the JSON. Turn measurements into a **spec**, not a polygon:

   | measured | becomes |
   |---|---|
   | `panel_w_mm`, `panel_h_mm` | target `panel_w`, `panel_h` |
   | `pitch_snapped_mm` | `pitch` |
   | `corner_radius_mm` | `corner_r` |
   | `edge_offset_mm` | stitch run offset |
   | `holes_detected` | sanity check on capacity |

4. Re-generate with `build_wallet.py` using those parameters, and tell the user what
   you inferred versus what you assumed.

## Known limits — say these out loud

- a single photo cannot see **leather thickness**, so fold compensation is an
  assumption; ask, or state the default.
- burnished edges straddle the true cut line, biasing dimensions outward by roughly
  0.5–1.3 mm. Expect to trim.
- dark leather and specular highlights degrade hole detection; if
  `holes_detected` looks implausible, say so rather than trusting the pitch.

## Reading the result

`holes_detected` is the reliability signal. If it is 0 or implausibly low on an item
that clearly has stitching, hole detection failed — say so and fall back to asking the
user for the pitch, rather than reporting a number you do not believe.
