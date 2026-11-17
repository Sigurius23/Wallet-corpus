"""Exports: SVG (mm), DXF (layered, for laser/CAD), 1:1 tiled A4 PDF, JSON report."""
import json, math, os
import numpy as np
from .pdf import tiled_pdf


def _ensure(d):
    os.makedirs(d, exist_ok=True)


def to_svg(pieces, path, gap=8.0, title="pattern"):
    # simple row layout with labels
    x = gap
    placed = []
    for p in pieces:
        placed.append((p, x, gap))
        x += p.width + gap
    W = max(x, 40)
    H = max((p.height for p in pieces), default=40) + 2 * gap + 14

    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}mm" height="{H:.2f}mm" '
           f'viewBox="0 0 {W:.2f} {H:.2f}">',
           '<rect width="100%" height="100%" fill="#fff"/>',
           f'<text x="{gap}" y="{gap+4}" font-family="Helvetica" font-size="4" '
           f'fill="#111">{title}</text>']
    for p, ox, oy in placed:
        pts = " ".join(f"{x+ox:.3f},{y+oy:.3f}" for x, y in p.outline)
        out.append(f'<polygon points="{pts}" fill="none" stroke="#111" stroke-width="0.25"/>')
        for c in getattr(p, "cutouts", []):
            pts = " ".join(f"{x+ox:.3f},{y+oy:.3f}" for x, y in c)
            out.append(f'<polygon points="{pts}" fill="none" stroke="#111" stroke-width="0.25"/>')
        out.append('<g fill="none" stroke="#c22" stroke-width="0.15">')
        for hx, hy in p.holes:
            out.append(f'<circle cx="{hx+ox:.3f}" cy="{hy+oy:.3f}" r="0.5"/>')
        out.append('</g>')
        out.append('<g stroke="#06c" stroke-width="0.2" stroke-dasharray="2 1">')
        for (a, b) in p.folds:
            out.append(f'<line x1="{a[0]+ox:.3f}" y1="{a[1]+oy:.3f}" '
                       f'x2="{b[0]+ox:.3f}" y2="{b[1]+oy:.3f}"/>')
        out.append('</g>')
        out.append(f'<text x="{ox}" y="{oy+p.height+5}" font-family="Helvetica" '
                   f'font-size="3.2" fill="#111">{p.name}  {p.width:.1f}x{p.height:.1f}</text>')
    out.append('</svg>')
    open(path, "w").write("\n".join(out))
    return path


def to_dxf(pieces, path):
    import ezdxf
    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()
    for nm, col in (("CUT", 7), ("STITCH", 1), ("FOLD", 5), ("NOTES", 3)):
        if nm not in doc.layers:
            doc.layers.add(nm, color=col)
    x = 0.0
    for p in pieces:
        off = (x, 0.0)
        msp.add_lwpolyline([(px + off[0], py + off[1]) for px, py in p.outline],
                           close=True, dxfattribs={"layer": "CUT"})
        for c in getattr(p, "cutouts", []):
            msp.add_lwpolyline([(cx + off[0], cy + off[1]) for cx, cy in c],
                               close=True, dxfattribs={"layer": "CUT"})
        for hx, hy in p.holes:
            msp.add_circle((hx + off[0], hy + off[1]), 0.5,
                           dxfattribs={"layer": "STITCH"})
        for (a, b) in p.folds:
            msp.add_line((a[0] + off[0], a[1] + off[1]),
                         (b[0] + off[0], b[1] + off[1]), dxfattribs={"layer": "FOLD"})
        msp.add_text(p.name, height=3.0,
                     dxfattribs={"layer": "NOTES"}).set_placement(
                         (off[0], -6.0))
        x += p.width + 10.0
    doc.saveas(path)
    return path


def export_all(wallet, outdir):
    _ensure(outdir)
    svg = to_svg(wallet.pieces, os.path.join(outdir, "pattern.svg"),
                 title=f"{wallet.name} — 1 unit = 1 mm")
    dxf = to_dxf(wallet.pieces, os.path.join(outdir, "pattern.dxf"))
    pdf = tiled_pdf(wallet.pieces, os.path.join(outdir, "pattern_1to1.pdf"),
                    title=f"{wallet.name} — print at 100%")
    rep = wallet.report()
    json.dump(rep, open(os.path.join(outdir, "report.json"), "w"), indent=1)
    return {"svg": svg, "dxf": dxf, "pdf": pdf,
            "report": os.path.join(outdir, "report.json")}
