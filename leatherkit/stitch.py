"""
Stitch planning — the part generic CAD gets wrong.

A pricking iron has a fixed pitch and a fixed number of teeth. You cannot put an
even number of holes at an exact pitch around an arbitrary perimeter, so a real
maker either (a) accepts one longer/shorter gap at a chosen spot, or (b) runs
"variable pitch". We model both, and we report exactly the error introduced.
"""
import math
from dataclasses import dataclass
import numpy as np
from .geom import resample_even, perimeter

STANDARD_PITCHES = (2.7, 3.0, 3.38, 3.85, 4.0, 5.0)


@dataclass
class StitchPattern:
    pitch: float
    n_holes: int
    perimeter: float
    mode: str                 # "fixed" | "variable" | "snapped"
    spacing_error: float      # mm deviation of the worst gap from nominal
    points: np.ndarray

    def __str__(self):
        return (f"{self.n_holes} holes @ {self.pitch} mm ({self.mode}), "
                f"worst gap error {self.spacing_error:+.3f} mm")


def stitch_run(outline, pitch=3.85, mode="variable", start_index=0):
    """
    Plan a stitch run around a closed outline.

    mode="variable" : snap the pitch slightly so the run closes perfectly.
                      Returns the ACTUAL pitch used.
    mode="fixed"    : hold the nominal pitch; absorb the remainder in one gap
                      and report it as spacing_error.
    """
    per = perimeter(outline, closed=True)
    if mode == "variable":
        n = max(2, int(round(per / pitch)))
        actual = per / n
        pts = resample_even(outline, n=n)
        return StitchPattern(round(actual, 4), n, per, "variable", 0.0, pts)

    n = max(2, int(math.floor(per / pitch)))
    pts = resample_even(outline, n=n)
    # remainder is absorbed in the final gap by construction of resample_even;
    # report how far that last gap is from nominal
    gaps = np.linalg.norm(np.diff(np.vstack([pts, pts[:1]]), axis=0), axis=1)
    err = float(np.max(np.abs(gaps - pitch)))
    return StitchPattern(pitch, n, per, "fixed", round(err, 4), pts)
