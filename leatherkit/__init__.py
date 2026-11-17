"""
leatherkit — a code-CAD library for flat leather goods.

The idea is the same one that makes text-to-CAD work for 3D printing:
the LLM writes *parametric source code*, and a deterministic kernel emits
cut files. Geometry is never guessed by a model.

    from leatherkit import Wallet
    w = Wallet.bifold(cards=6, leather_t=1.0, pitch=3.85)
    w.export("out/")        # SVG + DXF + 1:1 tiled PDF + report
"""
from .geom import Piece, rounded_rect, resample_even
from .stitch import stitch_run, StitchPattern
from .wallet import Wallet
from .export import export_all

__all__ = ["Piece", "rounded_rect", "resample_even", "stitch_run",
           "StitchPattern", "Wallet", "export_all"]
__version__ = "0.1.0"
