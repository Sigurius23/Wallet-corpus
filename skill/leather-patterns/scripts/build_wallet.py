#!/usr/bin/env python3
"""
build_wallet.py — the skill's single entry point.

Emits SVG + layered DXF + 1:1 tiled PDF + report.json, then runs the validation
gates and prints a PASS/FAIL table. Exit code is non-zero if any gate fails, so a
calling agent cannot mistake a bad pattern for a good one.

  python3 scripts/build_wallet.py --style bifold --cards 6 --leather-t 1.0 --out ./o
  python3 scripts/build_wallet.py --style card_holder --cards 4 --out ./o --json
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from leatherkit import Wallet, export_all
from leatherkit.stitch import STANDARD_PITCHES

ISO_CARD_W = 85.6
MAX_FLAT_STACK = 8.0
MAX_SPACING_ERR = 0.15


def gate(label, ok, value, detail=""):
    return {"gate": label, "pass": bool(ok), "value": value, "detail": detail}


def validate(rep):
    p = rep["params"]
    st = p["stitch"]
    gates = []

    panel = p.get("panel_w")
    if panel is not None:
        min_w = ISO_CARD_W + 4.0
        gates.append(gate("panel fits a card", panel >= min_w, round(panel, 2),
                          f"panel_w {panel:.2f} mm, need >= {min_w:.1f} mm"))

    stack = p.get("stack_closed_mm")
    if stack is not None:
        gates.append(gate("closed stack under 8 mm", stack <= MAX_FLAT_STACK,
                          round(stack, 2),
                          f"{stack:.2f} mm; above ~{MAX_FLAT_STACK} mm it will not sit flat"))

    err = st.get("spacing_error", 0.0)
    gates.append(gate("stitch spacing error", err <= MAX_SPACING_ERR, round(err, 4),
                      "variable-pitch runs close exactly; fixed runs absorb one gap"))

    req = p.get("pitch_requested", p["pitch"])
    gates.append(gate("pitch honoured (not substituted)", not p.get("pitch_substituted", False),
                      p["pitch"],
                      (f"requested {req} mm, standard set is {STANDARD_PITCHES}; "
                       f"substituted {p['pitch']} - CONFIRM WITH USER")
                      if p.get("pitch_substituted") else "requested pitch is standard"))

    fc = p.get("fold_comp")
    if fc is not None:
        import math
        exp = round(math.pi * p["leather_t"], 2)
        gates.append(gate("fold compensation present", abs(fc - exp) < 0.01, fc,
                          f"pi x t = {exp} mm"))

    gates.append(gate("pieces generated", len(rep["pieces"]) > 0,
                      len(rep["pieces"]), ""))

    return gates


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--style", default="bifold", choices=["bifold", "card_holder"])
    ap.add_argument("--cards", type=int, default=6)
    ap.add_argument("--leather-t", type=float, default=1.0)
    ap.add_argument("--slot-t", type=float, default=0.7)
    ap.add_argument("--pitch", type=float, default=3.85)
    ap.add_argument("--reveal", type=float, default=8.0)
    ap.add_argument("--clearance", type=float, default=2.0)
    ap.add_argument("--corner-r", type=float, default=8.0)
    ap.add_argument("--interior-gap", type=float, default=8.0)
    ap.add_argument("--out", default="./wallet_out")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args()

    if a.style == "bifold":
        w = Wallet.bifold(cards=a.cards, leather_t=a.leather_t, slot_t=a.slot_t,
                          pitch=a.pitch, reveal=a.reveal, clearance=a.clearance,
                          corner_r=a.corner_r, interior_gap=a.interior_gap)
    else:
        w = Wallet.card_holder(cards=a.cards, leather_t=a.leather_t, pitch=a.pitch,
                               reveal=max(a.reveal, 9.0), corner_r=min(a.corner_r, 5.0))

    files = export_all(w, a.out)
    rep = w.report()
    gates = validate(rep)
    ok = all(g["pass"] for g in gates)

    result = {"ok": ok, "files": files, "report": rep, "gates": gates}

    if a.json:
        print(json.dumps(result, indent=1))
    else:
        print(f"\n{w.name}  ->  {a.out}")
        for name, path in files.items():
            print(f"  {name:7} {path}")
        print("\nvalidation:")
        for g in gates:
            print(f"  [{'PASS' if g['pass'] else 'FAIL'}] {g['gate']:26} "
                  f"{str(g['value']):>9}   {g['detail']}")
        print(f"\n{'ALL GATES PASS' if ok else 'GATE FAILURE - do not ship this pattern'}")
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
