#!/usr/bin/env python3
"""
Build a 3-page A4 1:1 reference + geometry sheet for leather wallet pattern making.
Everything drawn in millimetres using reportlab.lib.units.mm.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import black, HexColor

PW, PH = A4
INK = HexColor("#1c1b19")
MUTED = HexColor("#6b6660")
ACC = HexColor("#7a4b2a")
SOFT = HexColor("#f3e9df")
LINE = HexColor("#c9bfb2")
GRID = HexColor("#e2ddd5")

M = 18 * mm          # page margin
RIGHT = PW - M

out = "wallet-pattern-reference-sheet.pdf"
c = canvas.Canvas(out, pagesize=A4)
c.setTitle("Leather Wallet Pattern Reference Sheet - 1:1")
c.setAuthor("Arena.ai")


def T(x, y, s, size=8, color=INK, font="Helvetica", align="l"):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "c":
        c.drawCentredString(x, y, s)
    elif align == "r":
        c.drawRightString(x, y, s)
    else:
        c.drawString(x, y, s)
    c.setFillColor(black)


def HL(x1, y, x2, color=LINE, w=0.4, dash=None):
    c.setStrokeColor(color)
    c.setLineWidth(w)
    if dash:
        c.setDash(dash, 0)
    c.line(x1, y, x2, y)
    if dash:
        c.setDash()


def BOX(x, y, w, h, color=LINE, lw=0.5, fill=None, dash=None):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    if dash:
        c.setDash(dash, 0)
    if fill is not None:
        c.setFillColor(fill)
        c.rect(x, y, w, h, stroke=1, fill=1)
        c.setFillColor(black)
    else:
        c.rect(x, y, w, h, stroke=1, fill=0)
    if dash:
        c.setDash()


def HDIM(x1, y, x2, label=None, color=ACC, size=6.5):
    c.setStrokeColor(color)
    c.setLineWidth(0.5)
    c.line(x1, y, x2, y)
    for x in (x1, x2):
        c.line(x, y - 1.1 * mm, x, y + 1.1 * mm)
    if label:
        T((x1 + x2) / 2, y + 1.5 * mm, label, size, color, align="c")


def SECTION(y, num, title):
    T(M, y, num, 8, ACC, "Helvetica-Bold")
    T(M + 7 * mm, y, title, 10.5, INK, "Helvetica-Bold")
    HL(M, y - 2.4 * mm, RIGHT, LINE, 0.6)


def PAGE_HEAD(title, sub):
    c.showPage()
    T(M, PH - 15 * mm, title, 14, INK, "Helvetica-Bold")
    T(M, PH - 20.5 * mm, sub, 7.8, MUTED)


def FOOT(page, total, note):
    HL(M, M + 11 * mm, RIGHT, LINE, 0.6)
    T(M, M + 7 * mm, note, 6.8, MUTED)
    T(RIGHT, M + 7 * mm, f"Page {page} of {total}", 6.8, MUTED, align="r")


TOTAL = 3

# =====================================================================  PAGE 1
T(M, PH - 15 * mm, "LEATHER WALLET PATTERN — 1:1 REFERENCE SHEET", 14, INK, "Helvetica-Bold")
T(M, PH - 20.5 * mm, "Print at 100% / “Actual size”. Turn OFF “fit to page”. Check the calibration square before trusting anything else on this sheet.", 7.8, MUTED)

# -------- 01 calibration + card
SECTION(PH - 32 * mm, "01", "Calibration and the two objects that set every dimension")
top = PH - 41 * mm

sq = 50 * mm
BOX(M, top - sq, sq, sq, INK, 0.8, SOFT)
BOX(M + 10 * mm, top - sq + 10 * mm, 30 * mm, 30 * mm, LINE, 0.4)
T(M + sq / 2, top - sq / 2 + 3 * mm, "exactly 50 mm?", 7, MUTED, align="c")
T(M + sq / 2, top - sq / 2 - 1.5 * mm, "50 × 50 mm", 8.5, ACC, "Helvetica-Bold", "c")
T(M + sq / 2, top - sq / 2 - 6 * mm, "measure it with a ruler", 7, MUTED, align="c")

cx = M + 62 * mm
cw, ch = 85.6 * mm, 53.98 * mm
BOX(cx, top - ch, cw, ch, INK, 0.8)
T(cx + cw / 2, top - ch / 2 + 3 * mm, "CREDIT CARD", 7.5, MUTED, "Helvetica-Bold", "c")
T(cx + cw / 2, top - ch / 2 - 2 * mm, "85.6 × 53.98 mm", 9.5, ACC, "Helvetica-Bold", "c")
T(cx + cw / 2, top - ch / 2 - 6.5 * mm, "ISO/IEC 7810 ID-1", 7, MUTED, align="c")
T(cx, top - ch - 4.5 * mm, "Slot width = card width + 2 mm. Pocket height = card height − reveal.", 7.2, MUTED)

# -------- banknote
by_top = top - sq - 13 * mm
bw, bh = 156 * mm, 66.3 * mm
BOX(M, by_top - bh, bw, bh, INK, 0.8, None, dash=[2, 2])
T(M + bw / 2, by_top - bh / 2 + 3 * mm, "EURO BANKNOTE", 7.5, MUTED, "Helvetica-Bold", "c")
T(M + bw / 2, by_top - bh / 2 - 2 * mm, "156 × 66.3 mm", 9.5, ACC, "Helvetica-Bold", "c")
T(M + bw / 2, by_top - bh / 2 - 6.5 * mm, "a US bill is the same length, 6.6 mm shorter in height", 7, MUTED, align="c")
T(M, by_top - bh - 5 * mm, "A bifold folds the note, so the bill compartment only needs to clear the folded height. That is why long wallets exist.", 7.2, MUTED)

# -------- 02 pitch
sy = by_top - bh - 17 * mm
SECTION(sy, "02", "Stitch pitch gauges — lay your pricking iron on the holes")
gy = sy - 9 * mm
T(M, gy, "pitch", 6.5, MUTED, "Helvetica-Bold")
T(M + 24 * mm, gy, "20 mm of actual holes — your iron should match one of these", 6.5, MUTED)
gy -= 5 * mm
for p in (3.0, 3.38, 3.85, 4.0):
    T(M, gy - 1.2 * mm, f"{p:.2f} mm", 8, ACC, "Helvetica-Bold")
    n = int(20 / p)
    c.setFillColor(INK)
    for i in range(n + 1):
        c.circle(M + 24 * mm + i * p * mm, gy - 1 * mm, 0.55 * mm, stroke=0, fill=1)
    c.setFillColor(black)
    nxt = 3.38 if p == 3.0 else (3.85 if p == 3.38 else 4.0)
    T(M + 24 * mm + n * p * mm + 4 * mm, gy - 1.5 * mm, f"{n} gaps = {n*p:.2f} mm", 6.8, MUTED)
    gy -= 8 * mm

T(M, gy + 2 * mm, "3.38 mm is the Japanese / “diamond” pitch; 3.85 mm is the European standard. Choose one and never mix — the pitch is baked into every pattern you draw.", 7.2, MUTED)
T(M, gy - 2 * mm, "Also relevant: thread. 0.45–0.55 mm waxed for wallets; a thick thread needs a longer stitch or the edge puckers.", 7.2, MUTED)

FOOT(1, TOTAL, "All dimensions in millimetres, drawn 1:1 at A4. Verify the calibration square first.")

# =====================================================================  PAGE 2
PAGE_HEAD("BIFOLD GEOMETRY — the four numbers that decide whether it works",
          "Most first wallets fail on one of these. Draw them before you cut anything.")

# -------- 01 radii
SECTION(PH - 32 * mm, "01", "Corner radius templates — trace these wallet corners")
rbase = PH - 62 * mm
for i, r in enumerate((3, 5, 8, 12)):
    x0 = M + i * 30 * mm
    # draw a square corner with a true radius fillet
    c.setStrokeColor(LINE); c.setLineWidth(0.35); c.setDash(1, 2)
    c.line(x0, rbase + 26 * mm, x0, rbase + r * mm)
    c.line(x0, rbase, x0 + 26 * mm, rbase)
    c.setDash()
    c.setStrokeColor(ACC)
    c.setLineWidth(0.8)
    p = c.beginPath()
    p.moveTo(x0, rbase + r * mm)
    p.arcTo(x0, rbase, x0 + 2 * r * mm, rbase + 2 * r * mm, startAng=180, extent=-90)
    c.drawPath(p)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.3)
    c.setDash(1, 2)
    c.line(x0, rbase, x0, rbase + r * mm)
    c.line(x0, rbase, x0 + r * mm, rbase)
    c.setDash()
    T(x0 + r * mm * 0.66, rbase - 4.5 * mm, f"R{r}", 7.5, ACC, "Helvetica-Bold", "c")
T(M, rbase - 8 * mm, "R5–R8 for card-wallet corners, R8–R12 for bifold outer corners. A tight radius cracks edge finish; too big a radius eats card retention.", 7.2, MUTED)

# -------- 02 plan view
sy = rbase - 19 * mm
SECTION(sy, "02", "Plan view — outer piece vs interior assembly")
pw, ph = 60 * mm, 40 * mm
gap = 7 * mm
ox, oy = M + 12 * mm, sy - 13 * mm - ph

BOX(ox, oy, pw * 2, ph, INK, 0.9, SOFT)
T(ox + 5 * mm, oy + ph - 5.5 * mm, "OUTER — one piece, folded", 7.8, ACC, "Helvetica-Bold")
T(ox + 5 * mm, oy + ph - 9.5 * mm, f"{2*pw:.0f} mm + fold compensation", 7, MUTED)
c.setStrokeColor(MUTED)
c.setLineWidth(0.5)
c.setDash(3, 2)
c.line(ox + pw, oy - 2 * mm, ox + pw, oy + ph + 2 * mm)
c.setDash()
T(ox + pw - 8 * mm, oy + ph + 1.5 * mm, "fold line", 6.8, MUTED)

iw = pw * 2 - gap * 2
ih = ph - 8 * mm
BOX(ox + gap, oy + 4 * mm, iw, ih, ACC, 0.8)
T(ox + 5 * mm, oy + 12.5 * mm, "INTERIOR assembly", 7.8, ACC, "Helvetica-Bold")
T(ox + 5 * mm, oy + 8 * mm, "shorter on every open edge", 6.8, MUTED)

HDIM(ox + gap, oy - 4 * mm, ox + gap + iw, f"interior = outer minus {2*gap:.0f} mm")
HDIM(ox, oy - 12 * mm, ox + pw * 2, "outer length = 2 x panel + fold compensation")

T(M, oy - 24 * mm, 'Pull the interior in 6-10 mm per end (about 1/4" to 3/8" total). More if the leather is thick or there are many pockets.', 7.2, MUTED)
T(M, oy - 27.6 * mm, "Get this wrong and the wallet waves when folded - the single most common first-wallet failure.", 7.2, MUTED)

sy = oy - 34 * mm
SECTION(sy, "03", "The formulas")
ty = sy - 7.5 * mm
c1, c2, c3 = M, M + 50 * mm, M + 106 * mm
T(c1, ty, "WHAT", 6.3, MUTED, "Helvetica-Bold")
T(c2, ty, "RULE", 6.3, MUTED, "Helvetica-Bold")
T(c3, ty, "TYPICAL VALUE", 6.3, MUTED, "Helvetica-Bold")
ty -= 3.5 * mm
HL(M, ty, RIGHT, LINE, 0.5)
ty -= 4.5 * mm
rows = [
    ("Pocket height", "card height 54 mm + 3 mm clearance − reveal", "≈ 47–50 mm"),
    ("Reveal (visible strip)", "6–10 mm; 8 mm is the common choice", "8 mm"),
    ("Slot width", "card width 85.6 + 2 mm clearance", "87–88 mm"),
    ("Slot stagger", "each slot sits 15–20 mm below the one above", "drives interior height"),
    ("Stitch line from edge", "3–4 mm hand stitched / 5–6 mm machine", "3.5 mm + your pitch"),
    ("Fold compensation", "π × leather thickness, per fold", "1.0 mm → 3.14 mm"),
    ("Interior vs outer", "6–10 mm shorter at each open end", "7–8 mm start"),
]
for a, b, d in rows:
    T(c1, ty, a, 7.6, INK, "Helvetica-Bold")
    T(c2, ty, b, 7.6, MUTED)
    T(c3, ty, d, 7.6, ACC)
    ty -= 4.4 * mm
    HL(M, ty + 1.3 * mm, RIGHT, GRID, 0.35)

# -------- 04 thickness
sy = ty - 6 * mm
SECTION(sy, "04", "Thickness stack — the closing-force budget")
ty = sy - 7.5 * mm
stack = [
    ("Outer shell", "1.0–1.2 mm (2.5–3 oz), stiff temper", "keeps the shape when empty"),
    ("Card slots", "0.6–0.8 mm (1.5–2 oz)", "skive the top edges or the stack bulges"),
    ("Bill divider", "0.6–0.8 mm, or a cloth lining", "cloth is thinner; it wears out first"),
    ("Closed total", "≈ 5–7 mm on a 6-slot bifold", "beyond ~8 mm it will not sit flat"),
]
for a, b, d in stack:
    T(c1, ty, a, 7.6, INK, "Helvetica-Bold")
    T(c2, ty, b, 7.6, ACC)
    T(c3, ty, d, 7.2, MUTED)
    ty -= 4.4 * mm
    HL(M, ty + 1.3 * mm, RIGHT, GRID, 0.35)

FOOT(2, TOTAL, "Fold compensation formula: π × t × number of folds. Two folds (trifold) at 1.0 mm = 6.28 mm.")

# =====================================================================  PAGE 3
PAGE_HEAD("FAILURE MODES, WORKFLOW, AND WHAT TO BUY",
          "Everything here maps a symptom back to the specific pattern piece or tool that caused it.")

sy = PH - 32 * mm
SECTION(sy, "01", "Symptom → cause")
ty = sy - 8 * mm
fails = [
    ("Waves or bows when folded", "Interior assembly is too long, or the gap between card banks is too small."),
    ("Gapes at the fold, will not close flat", "Fold compensation missing, or the total stack exceeds ~8 mm."),
    ("Cards sink in too deep", "Pocket too tall — reduce height or add a card-stop stitch line."),
    ("Cards too tight to remove", "Reveal under 6 mm, or slot width under card width + 2 mm."),
    ("Corners bulge or crack", "Radius too tight for the temper, or the edge was not skived."),
    ("Stitch line wanders off the edge", "Pitch mismatch, not a pattern error. One iron, one pitch, always."),
    ("Edge finish fails at the fold", "Burnish and seal before folding; fold stress is the enemy of edge paint."),
]
for a, b in fails:
    T(M, ty, "•", 9, ACC, "Helvetica-Bold")
    T(M + 4.5 * mm, ty, a, 7.8, INK, "Helvetica-Bold")
    T(M + 60 * mm, ty, b, 7.6, MUTED)
    ty -= 5.0 * mm

# -------- workflow
sy = ty - 5 * mm
SECTION(sy, "02", "The draw-it-once workflow")
ty = sy - 8 * mm
steps = [
    ("Mock up in foam", "1/8\" craft foam, stapled not sewn. Cheap, fast, and it tells you the fold behaves before leather does."),
    ("Flatten and photograph", "Cut the foam open, lay it flat, include a ruler in frame, shoot straight down."),
    ("Import and scale", "Leathercraft CAD or EasyPatt: import the photo, set DPI against the ruler, trace over it."),
    ("Add the engineering", "Stitch lines at your pitch, card-stop stitches, fold lines, hardware centres, edge bevel marks."),
    ("Print 1:1 tiled", "Verify the calibration square on every print run. Tape, then transfer to pattern plastic."),
    ("Make a template", "Third time you make a design, order an acrylic template from your own DXF/SVG or PDF."),
]
for i, (a, b) in enumerate(steps, 1):
    T(M, ty, f"{i}", 8, ACC, "Helvetica-Bold")
    T(M + 6 * mm, ty, a, 7.8, INK, "Helvetica-Bold")
    T(M + 6 * mm, ty - 3.8 * mm, b, 7.3, MUTED)
    ty -= 8.8 * mm

# -------- buy list
sy = ty - 3 * mm
SECTION(sy, "03", "Wallet-specific shortlist")
ty = sy - 8 * mm
items = [
    ("Leathercraft CAD", "Free / donation · Win + macOS + web beta", "Stitch holes as real objects, hardware library, 1:1 tiled print. The default."),
    ("EasyPatt", "Free · browser, no install", "Auto stitch-hole generation, 50 mm calibration square on every page."),
    ("Affinity (by Canva)", "Free — needs a Canva account", "Merged Designer/Photo/Publisher, free since Oct 2025. Best curves for laser-ready SVG/DXF artwork."),
    ("Fusion 360 (hobby)", "Free", "Parametric patterns plus CNC/3D-printed hardware. Overkill for wallets alone."),
    ("Pricking irons", "€25–70 per iron", "One pitch, good quality: 3.38 or 3.85 mm. Cheap sets drift."),
    ("Acrylic template", "€10–13 each, or cut your own", "€2–5 in 3 mm acrylic from a German laser service once you have the DXF."),
    ("Pattern plastic", "€5–15", "Makes a paper pattern survive more than three cuts."),
    ("Craft foam", "€1–2 / sheet", "The most valuable €2 in leather pattern making."),
]
for a, b, d in items:
    T(M, ty, a, 7.8, INK, "Helvetica-Bold")
    T(M + 50 * mm, ty, b, 7.2, ACC)
    T(M + 50 * mm, ty - 3.6 * mm, d, 7.2, MUTED)
    ty -= 8.4 * mm

# -------- minimum viable kit
ty -= 2 * mm
SECTION(ty, "04", "Minimum viable wallet kit — spend in this order")
ty -= 8 * mm
kit = [
    ("1st", "Craft foam + a scalpel", "€5", "Make three foam mock-ups before you touch leather. This is the whole skill."),
    ("2nd", "One good pricking iron", "€40-70", "Pick 3.38 or 3.85 mm. A cheap set will teach you bad habits at the edge."),
    ("3rd", "Leathercraft CAD or EasyPatt", "free", "Draw it properly once, then never redraw it by hand."),
    ("4th", "Pattern plastic + 1:1 prints", "€10", "Turns a fragile paper pattern into a tool you will still be using in a year."),
    ("5th", "Acrylic template, custom cut", "€5-13", "Only once the design is settled. Order 3 mm clear acrylic from your own DXF/SVG."),
]
for stage, what, cost, why in kit:
    T(M, ty, stage, 7.4, ACC, "Helvetica-Bold")
    T(M + 11 * mm, ty, what, 7.8, INK, "Helvetica-Bold")
    T(M + 62 * mm, ty, cost, 7.4, ACC)
    T(M + 76 * mm, ty, why, 7.2, MUTED)
    ty -= 4.7 * mm

BOX(M, ty - 13 * mm, RIGHT - M, 12.5 * mm, LINE, 0.6, SOFT)
T(M + 4 * mm, ty - 5.5 * mm, "The one rule", 8, ACC, "Helvetica-Bold")
T(M + 4 * mm, ty - 9.5 * mm, "Never change two variables between mock-ups. Change the interior length OR the slot stagger, make a foam model, check it, then move on.", 7.4, INK)

FOOT(3, TOTAL, "Prices as of November 2026. Verify leather thickness and pitch against your own stock before cutting.")

c.showPage()
c.save()
print("written", out)
