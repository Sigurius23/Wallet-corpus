# Sketch → brief → pattern

## Why this exists

Prompting is a poor interface for anything spatial. Words cannot carry proportions,
silhouettes, or where a hole sits relative to a corner — and for a leather pattern
those *are* the design. So the drawing is the input, and the job of this pipeline is
to convert it into a **structured brief**: explicit millimetres, explicit
assumptions, explicit open questions.

The rule that makes it work: **the brief is not the answer, it is the agenda.** A
sketch cannot carry every number, and pretending otherwise is how you cut a wrong
panel. The brief says what it knows, what it guessed, and what to ask.

```bash
python3 scripts/sketch_to_spec.py sketch.jpg --out ./brief/ --debug ./brief/dbg
#   -> brief/brief.json   structured brief: panels, sizes, cutouts, assumptions, questions
#   -> brief/spec.json    ready for build_piece.py
python3 scripts/build_piece.py brief/spec.json --out ./brief/cut
```

---

## What it measures, and how well

| quantity | method | accuracy |
|---|---|---|
| scale | ISO/IEC 7810 ID-1 card in frame, edge-detected as a 1.586:1 quad | exact to the card's own tolerance |
| panel size | enclosed-region tracing + **half stroke width** added back | about **1 %** |
| cutouts / holes | enclosed regions inside the panel bounding box | reliable if the loop is closed |
| stitch pitch | not measured — snapped to a standard pricking iron | you confirm |
| **corner radius** | Menger curvature, returned as a **band** | **a guess. Always ask.** |

### Why the stroke-width correction matters

The tracer finds regions *enclosed by ink*, so every measurement is bounded by the
**inside** of the pencil line. A 0.7 mm pencil therefore reads about 0.7 mm
undersize. The script estimates stroke width from a distance transform and adds half
of it back out, which takes the error from −2.5 % to about −1 %.

### Why the corner radius is a band and not a number

Three estimators were tested against known radii of 6, 12, 18 and 25 mm:

| estimator | 6 mm | 12 mm | 18 mm | 25 mm | verdict |
|---|---|---|---|---|---|
| algebraic circle fit | — | — | — | — | returns None; unstable on a wobbly arc |
| corner-offset geometry | None | None | None | None | no straight run survives 1 mm of jitter |
| Menger curvature | 5.5 | 8.9 | 12.3 | 14.0 | **monotonic but compressed** |

A pencil wobbles roughly 1 mm, and that is the same order as the entire range of
plausible radii. So the honest output is `9.5 mm (band 5.7–13.0) — confirm`. The
script puts it in `questions`, and the skill instructs the agent to ask rather than
assert. If you need the real radius, it comes from a spec, not a sketch.

---

## What the tracer will not do

- **Trace an open stroke.** If a line does not close, there is no panel — by
  construction, because the method finds enclosed paper. The script says so instead
  of emitting a plausible rectangle. Close the loop.
- **Estimate scale without a card.** No card, no millimetres. It refuses.
- **Separate overlapping items.** If the scale card overlaps the drawing, the panel
  is fragmented and the largest region is wrong. Move the card.
- **Read a photo of a finished product.** That is `inspect_photo.py`, and it recovers
  proportions, not construction.
- **Know proportions of things it cannot see.** It traces what is drawn, including
  your mistakes.

---

## How to sketch for this

1. **Dark pen or pencil on plain light paper.** Blue-lined paper and shadows confuse
   the threshold.
2. **Close every outline.** A gap of more than ~0.5 mm breaks the region.
3. **Put a bank card flat in frame**, fully visible, not touching the drawing.
4. **Shoot straight down**, fill the frame, avoid a hard shadow across the paper.
   Perspective is the main remaining error source — a tilted photo stretches the
   drawing.
5. **Draw true size.** Do not scale. The card sets the scale and a scaled sketch
   comes back the wrong size.
6. **Sketch the outline and the holes, not the stitching detail.** Pitch comes from
   the pricking iron you own, not from the drawing.

Vector is better than a photo whenever you have it: an `.svg` at 1:1 is exact, needs
no card, and skips tracing entirely.

---

## The intended loop

```
sketch  ->  brief  ->  ASK THE QUESTIONS  ->  spec  ->  gates  ->  felt mock  ->  correct
```

The mock step is not optional. The pattern is a hypothesis about how leather
behaves; the mock is the experiment. Because the spec is a small JSON file, one
correction costs one edit and one re-cut.
