"""Demo: parametric variants, the way an agent would drive it."""
import sys; sys.path.insert(0, "/home/user")
from leatherkit import Wallet, export_all

VARIANTS = {
    "slim_6card":  dict(cards=6, leather_t=1.0, pitch=3.85, reveal=8.0),
    "fat_8card":   dict(cards=8, leather_t=1.4, pitch=3.85, reveal=7.0),
    "japanese_4":  dict(cards=4, leather_t=0.8, pitch=3.38, reveal=9.0),
    "cardholder":  dict(cards=4, leather_t=1.0, pitch=3.85, reveal=10.0),
}

for name, kw in VARIANTS.items():
    if name == "cardholder":
        w = Wallet.card_holder(**kw)
    else:
        w = Wallet.bifold(**kw)
    files = export_all(w, f"/home/user/out_wallets/{name}")
    p = w.report()["params"]
    print(f"{name:12} outer {p.get('outer_w', p.get('body_w')):7.2f} x "
          f"{p.get('outer_h', p.get('body_h')):6.2f} mm   "
          f"{p['stitch']['n_holes']:3d} holes @ {p['stitch']['pitch']:.4f}   "
          f"stack {p.get('stack_closed_mm', 0):.2f} mm")
    print(f"             -> {files['pdf']}")
