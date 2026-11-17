"""
1:1 tiled A4 PDF.

Library coordinates are mm with y DOWN; PDF is y UP. Each page gets a reserved
header band (calibration square + labels), and the drawing area is clipped to the
remaining cell so nothing ever bleeds into the header or across pages.
"""
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor

INK = HexColor("#111111"); RED = HexColor("#cc2222")
BLUE = HexColor("#0066cc"); GREY = HexColor("#999999")

PW_MM, PH_MM = A4[0] / mm, A4[1] / mm
MARGIN = 12.0
HEADER = 44.0          # reserved band at the top of every page


def _layout(pieces, gap=10.0):
    placed, x, y, row_h = [], 0.0, 0.0, 0.0
    limit = PW_MM - 2 * MARGIN
    for p in pieces:
        if x > 0 and x + p.width > limit:
            x, y, row_h = 0.0, y + row_h + gap + 9.0, 0.0
        placed.append((p, x, y))
        x += p.width + gap
        row_h = max(row_h, p.height)
    tw = max((px + p.width for p, px, _ in placed), default=10.0)
    th = max((py + p.height for p, _, py in placed), default=10.0)
    return placed, tw, th


def tiled_pdf(pieces, path, title="pattern", gap=10.0):
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle(title)
    placed, total_w, total_h = _layout(pieces, gap)

    cell_w = PW_MM - 2 * MARGIN
    cell_h = PH_MM - 2 * MARGIN - HEADER
    n_cols = max(1, math.ceil(total_w / cell_w))
    n_rows = max(1, math.ceil(total_h / cell_h))
    n_pages = n_rows * n_cols

    for row in range(n_rows):
        for col in range(n_cols):
            page_no = row * n_cols + col + 1

            # ---------- header band (never clipped)
            c.setFillColor(INK); c.setFont("Helvetica-Bold", 8)
            c.drawString(MARGIN * mm, (PH_MM - MARGIN - 4) * mm, title)
            c.setFont("Helvetica", 6); c.setFillColor(GREY)
            c.drawString(MARGIN * mm, (PH_MM - MARGIN - 8) * mm,
                         f"page {page_no} of {n_pages}   row {row+1}/{n_rows}   "
                         f"col {col+1}/{n_cols}")
            c.setStrokeColor(INK); c.setLineWidth(0.6)
            sqy = PH_MM - MARGIN - 18 - 26
            c.rect(MARGIN * mm, sqy * mm, 26 * mm, 26 * mm, stroke=1, fill=0)
            c.setFillColor(GREY); c.setFont("Helvetica", 5.2)
            hx0 = MARGIN + 34
            for i, line in enumerate([
                "26 x 26 mm calibration square (left) - measure it before cutting.",
                "Print at 100% / Actual size. Overlap between pages is intentional:",
                "trim to the corner registration marks, then tape and verify scale.",
            ]):
                c.drawString(hx0 * mm, (sqy + 22 - i * 4.2) * mm, line)

            # ---------- clipped drawing cell
            c.saveState()
            cx0, cy0 = MARGIN, MARGIN
            clip = c.beginPath()
            clip.rect(cx0 * mm, cy0 * mm, cell_w * mm, cell_h * mm)
            c.clipPath(clip, stroke=0, fill=0)

            c.setStrokeColor(GREY); c.setLineWidth(0.3)
            for (mx, my) in [(cx0, cy0), (cx0 + cell_w, cy0),
                             (cx0, cy0 + cell_h), (cx0 + cell_w, cy0 + cell_h)]:
                c.line((mx - 2) * mm, my * mm, (mx + 2) * mm, my * mm)
                c.line(mx * mm, (my - 2) * mm, mx * mm, (my + 2) * mm)

            def T(x, y):
                """pattern mm (y down) -> page mm (y up), offset for this tile"""
                X = MARGIN + x - col * cell_w
                Y = PH_MM - MARGIN - HEADER - (y - row * cell_h)
                return X * mm, Y * mm

            for p, ox, oy in placed:
                pts = [T(px + ox, py + oy) for px, py in p.outline]
                c.setStrokeColor(INK); c.setLineWidth(0.45)
                pth = c.beginPath(); pth.moveTo(*pts[0])
                for q in pts[1:]:
                    pth.lineTo(*q)
                pth.close(); c.drawPath(pth)

                c.setStrokeColor(RED); c.setLineWidth(0.25)
                for hx, hy in p.holes:
                    c.circle(*T(hx + ox, hy + oy), 0.5 * mm, stroke=1, fill=0)

                c.setStrokeColor(BLUE); c.setLineWidth(0.35); c.setDash(1.6, 1.0)
                for (a, b) in p.folds:
                    c.line(*T(a[0] + ox, a[1] + oy), *T(b[0] + ox, b[1] + oy))
                c.setDash()

                c.setFillColor(INK); c.setFont("Helvetica", 5.5)
                c.drawString(*T(ox + 1.0, oy + p.height + 4.0),
                             f"{p.name}   {p.width:.1f} x {p.height:.1f} mm")
            c.restoreState()
            c.showPage()

    # ---------- final summary / cut sheet page
    c.setFont("Helvetica-Bold", 13); c.setFillColor(INK)
    c.drawString(MARGIN * mm, (PH_MM - MARGIN - 6) * mm, title)
    c.setFont("Helvetica", 7); c.setFillColor(GREY)
    c.drawString(MARGIN * mm, (PH_MM - MARGIN - 11) * mm,
                 "cut sheet + parameters. Everything on this page is a variable in the source.")

    y = PH_MM - MARGIN - 22
    c.setFont("Helvetica-Bold", 7.5); c.setFillColor(INK)
    for col, head in ((MARGIN, "PIECE"), (MARGIN + 62, "SIZE (mm)"),
                      (MARGIN + 112, "HOLES"), (MARGIN + 134, "FOLDS")):
        c.drawString(col * mm, y * mm, head)
    y -= 3.5
    c.setStrokeColor(GREY); c.setLineWidth(0.3)
    c.line(MARGIN * mm, y * mm, (PW_MM - MARGIN) * mm, y * mm)
    y -= 5.0
    c.setFont("Helvetica", 6.8)
    for p, _, _ in placed:
        c.setFillColor(INK); c.drawString(MARGIN * mm, y * mm, p.name)
        c.drawString((MARGIN + 62) * mm, y * mm, f"{p.width:.1f} x {p.height:.1f}")
        c.drawString((MARGIN + 112) * mm, y * mm, str(len(p.holes)))
        c.drawString((MARGIN + 134) * mm, y * mm, str(len(p.folds)))
        y -= 4.4
    c.showPage()
    c.save()
    return path
