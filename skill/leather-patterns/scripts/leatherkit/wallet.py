"""
Wallet generators. Every number here is a design decision with a reason, and
every one is a parameter — that is the whole point of code-CAD for patterns.
"""
import math
import numpy as np
from .geom import (Piece, rounded_rect, resample_even, inset, polygon_area)
from .stitch import stitch_run, STANDARD_PITCHES

ISO_CARD_W, ISO_CARD_H = 85.6, 53.98          # ISO/IEC 7810 ID-1
EURO_NOTE_W, EURO_NOTE_H = 156.0, 66.3        # longest euro note


class Wallet:
    """A parametric wallet. Build with .bifold() / .card_holder()."""

    def __init__(self, name, pieces, params):
        self.name = name
        self.pieces = pieces
        self.params = params

    # ------------------------------------------------------------------ factories
    @classmethod
    def bifold(cls, cards=6, leather_t=1.0, slot_t=0.7, pitch=3.85,
               reveal=8.0, clearance=2.0, corner_r=8.0, interior_gap=8.0,
               height=None, width=None):
        """
        Bifold wallet.

        cards          total card capacity across both banks
        leather_t      outer shell thickness, mm
        slot_t         card-slot leather thickness, mm
        pitch          pricking-iron pitch, mm
        reveal         visible strip of card above each slot, mm
        clearance      side clearance either side of a card, mm
        interior_gap   how much shorter the interior is than the outer, per end
        """
        pitch_requested = pitch
        if pitch not in STANDARD_PITCHES:
            pitch = min(STANDARD_PITCHES, key=lambda s: abs(s - pitch))

        slots_per_bank = max(1, cards // 2)
        slot_w = ISO_CARD_W + clearance
        # pocket height: a card must sit in the pocket with `reveal` showing
        pocket_h = ISO_CARD_H + 3.0 - reveal
        # each successive slot steps down by the reveal + a small stitch margin
        step = reveal + 2.0
        interior_h = pocket_h + step * (slots_per_bank - 1) + 2.0

        # outer panel: the interior plus the gap at each open end
        panel_w = width if width else slot_w + 2 * 5.0
        panel_h = height if height else interior_h + 2 * interior_gap

        # fold compensation: the outer layer must travel further around the fold
        fold_comp = math.pi * leather_t

        pieces = []

        # ---- outer shell: one piece, 2 panels + fold compensation, stitched round
        outer = Piece("01_outer_shell",
                      rounded_rect(2 * panel_w + fold_comp, panel_h, corner_r))
        sp = stitch_run(inset(outer.outline, 3.5), pitch=pitch, mode="variable")
        outer.holes = sp.points
        outer.folds = [[(panel_w + fold_comp / 2, 2.0),
                        (panel_w + fold_comp / 2, panel_h - 2.0)]]
        outer.notes = [(4, panel_h - 4, f"OUTER  {2*panel_w+fold_comp:.1f} x {panel_h:.1f} mm"),
                       (4, panel_h - 8.5, f"fold comp = pi x {leather_t} = {fold_comp:.2f} mm"),
                       (4, 10, f"stitch: {sp}")]
        pieces.append(outer)

        # ---- card slot bank (one bank, mirrored for the other side)
        bank_w = slot_w
        bank_outline = rounded_rect(bank_w, interior_h, min(corner_r, 5.0))
        bank = Piece("02_slot_bank", bank_outline)
        # one slot piece per card, each stepped down by `step`
        pieces.append(bank)
        for i in range(slots_per_bank):
            slot = Piece(f"03_slot_{i+1}",
                         rounded_rect(bank_w, interior_h - i * step, min(corner_r, 5.0)))
            slot.notes = [(3, 6, f"slot {i+1}: {bank_w:.1f} x {interior_h - i*step:.1f} mm"
                                f"{'  (fold top edge)' if True else ''}")]
            pieces.append(slot)

        # ---- bill divider
        div = Piece("04_bill_divider",
                    rounded_rect(bank_w, interior_h - step, min(corner_r, 5.0)))
        pieces.append(div)

        params = dict(
            style="bifold", cards=cards, slots_per_bank=slots_per_bank,
            leather_t=leather_t, slot_t=slot_t, pitch=pitch,
            pitch_requested=pitch_requested,
            pitch_substituted=bool(pitch != pitch_requested),
            reveal=reveal, clearance=clearance, pocket_h=round(pocket_h, 2),
            step=step, interior_h=round(interior_h, 2), interior_gap=interior_gap,
            panel_w=round(panel_w, 2), panel_h=round(panel_h, 2),
            outer_w=round(2 * panel_w + fold_comp, 2), outer_h=round(panel_h, 2),
            fold_comp=round(fold_comp, 2), corner_r=corner_r,
            closed_size=(round(2 * panel_w * 0.5, 1), round(panel_h, 1)),
            stack_closed_mm=round(leather_t + slots_per_bank * slot_t * 2 + slot_t, 2),
            stitch=dict(sp.__dict__ | {"points": f"<{sp.n_holes} points>"}),
        )
        return cls("bifold", pieces, params)

    @classmethod
    def card_holder(cls, cards=4, leather_t=1.0, pitch=3.85, reveal=10.0,
                    corner_r=3.0):
        """Simple front-pocket card holder: one folded body, N slot steps."""
        pitch_requested = pitch
        if pitch not in STANDARD_PITCHES:
            pitch = min(STANDARD_PITCHES, key=lambda s: abs(s - pitch))
        body_w = ISO_CARD_W + 6.0
        body_h = (ISO_CARD_H + 4.0) * 2 + math.pi * leather_t + reveal * (cards - 1)
        body = Piece("01_body", rounded_rect(body_w, body_h, corner_r))
        sp = stitch_run(inset(body.outline, 3.0), pitch=pitch, mode="variable")
        body.holes = sp.points
        body.notes = [(3, body_h - 4, f"BODY {body_w:.1f} x {body_h:.1f} mm"),
                      (3, 8, f"stitch: {sp}")]
        params = dict(style="card_holder", cards=cards, leather_t=leather_t,
                      pitch=pitch, pitch_requested=pitch_requested,
                      pitch_substituted=bool(pitch != pitch_requested),
                      reveal=reveal, panel_w=round(body_w, 2),
                      body_w=round(body_w, 2), body_h=round(body_h, 2),
                      corner_r=corner_r,
                      stitch=dict(sp.__dict__ | {"points": f"<{sp.n_holes} points>"}))
        return cls("card_holder", [body], params)

    # ------------------------------------------------------------------ reporting
    def report(self):
        leather = sum(polygon_area(p.outline) for p in self.pieces) / 100.0  # dm^2
        return {
            "wallet": self.name,
            "params": self.params,
            "pieces": [
                {"name": p.name, "width_mm": round(p.width, 2),
                 "height_mm": round(p.height, 2),
                 "holes": len(p.holes),
                 "folds": len(p.folds)}
                for p in self.pieces
            ],
            "leather_area_dm2": round(leather, 4),
            "leather_area_cm2": round(leather * 100, 1),
        }
