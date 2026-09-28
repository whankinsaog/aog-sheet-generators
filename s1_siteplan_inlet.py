"""SP-1 — site plan markup, portable generator inlet variant.

THIS COPY IS POPULATED FOR: 1912 Jung Blvd E, Naples FL 34120 (Collier County)

Overlays the customer's own marked boundary survey (Geometric Surveying, survey
19-00801, field date 11/18/2021). Nothing on the survey is masked: the existing
"Metermain/Panel" callout is correct and stays. Two things are ADDED, both in
clear space measured off a 72 dpi raster of the source (zero ink pixels):
  * keynote bubble 1 beside the meter-main marker in the detail;
  * a notes block in the clear field over Tract 64, keyed to bubble 1.
The red is sampled from the source's own "Metermain/Panel" label (220,38,38).
"""
import tempfile
from pathlib import Path

import numpy as np
import pikepdf
from PIL import Image
import subprocess
from reportlab.lib.colors import Color, white, black
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

SRC = ("/root/.claude/uploads/ca17b5f7-fa55-551e-9666-eae0d5b96921/"
       "c384756a-Site-Plan_1912_Jung_Blvd_E.pdf")
OUT = "out/SP-1 Site Plan - 1912 Jung Blvd E.pdf"
PW, PH = 612.0, 1008.0
LRED = Color(220 / 255, 38 / 255, 38 / 255)
DGREY = Color(.15, .15, .15)

# measured clear regions, raster px at 72 dpi (== pt), origin TOP-left
NOTE_PX = (444, 668, 576, 752)          # x0, y0, x1, y1
BUB_PX = (318, 352, 332, 366)
METER_PX = (328, 340)                   # the survey's own meter-main marker

TITLE = "PROPOSED GENERATOR INLET"
NOTES = [
    ("1", "New 50 A power inlet and 100 A sub panel on the west wall beside the "
          "existing meter-main; RCGK2 interlock inside the meter-main."),
    ("", "45.43' from the west lot line per survey. No change to the footprint."),
    ("", "Portable generator (by owner) runs outdoors, 10'-0\" min. from any "
         "door, window or opening."),
    ("", "Riser: Sheet E-1."),
]


def check_clear(pdf):
    """Re-measure: the two regions we draw into must carry no survey ink."""
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdftoppm", "-r", "72", "-gray", "-singlefile", pdf,
                        td + "/p"], check=True)
        ink = np.array(Image.open(td + "/p.pgm")) < 235
    for nm, (x0, y0, x1, y1) in (("notes", NOTE_PX), ("bubble", BUB_PX)):
        n = int(ink[y0:y1, x0:x1].sum())
        assert n == 0, "%s region is not clear on the survey (%d ink px)" % (nm, n)


def wrapw(text, maxw, font, size):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if stringWidth(t, font, size) > maxw and cur:
            out.append(cur); cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out


def build():
    src = pikepdf.open(SRC)
    rot = int(src.pages[0].get("/Rotate", 0))
    assert rot == 0, "survey page is rotated %d — transfer rotation first" % rot
    check_clear(SRC)

    x0, y1, x1, y0 = (NOTE_PX[0], PH - NOTE_PX[1], NOTE_PX[2], PH - NOTE_PX[3])
    bw, bh = x1 - x0, y1 - y0
    pad = 4.0
    for size in (6.2, 6.0, 5.8, 5.6, 5.4, 5.2, 5.0, 4.8):
        lead = size * 1.18
        blocks = [wrapw(t, bw - 2 * pad - 9, "Helvetica", size) for _, t in NOTES]
        need = (size + 3.5) + sum(len(b) * lead + 1.6 for b in blocks)
        if need <= bh - 2 * pad:
            break
    assert need <= bh - 2 * pad, "notes do not fit the clear region"

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name
    c = canvas.Canvas(tmp, pagesize=(PW, PH))
    # notes block
    c.setFillColor(white); c.setStrokeColor(LRED); c.setLineWidth(.9)
    c.rect(x0, y0, bw, bh, stroke=1, fill=1)
    yy = y1 - pad - size
    c.setFillColor(LRED); c.setFont("Helvetica-Bold", size + 0.6)
    c.drawString(x0 + pad, yy, TITLE)
    yy -= size + 3.5
    for (key, _), blk in zip(NOTES, blocks):
        bx = x0 + pad + 3
        if key:
            c.setStrokeColor(LRED); c.setFillColor(white); c.setLineWidth(.7)
            c.circle(bx, yy + size * .33, 3.1, stroke=1, fill=1)
            c.setFillColor(LRED); c.setFont("Helvetica-Bold", 4.6)
            c.drawCentredString(bx, yy + size * .33 - 1.6, key)
        else:
            c.setFillColor(DGREY); c.circle(bx, yy + size * .33, .9, stroke=0, fill=1)
        c.setFillColor(DGREY); c.setFont("Helvetica", size)
        for ln in blk:
            c.drawString(x0 + pad + 9, yy, ln); yy -= lead
        yy -= 1.6
    assert yy > y0, "notes overran the block"

    # keynote bubble at the meter-main
    bx = (BUB_PX[0] + BUB_PX[2]) / 2.0
    by = PH - (BUB_PX[1] + BUB_PX[3]) / 2.0
    c.setStrokeColor(LRED); c.setFillColor(white); c.setLineWidth(1.0)
    c.circle(bx, by, 6.0, stroke=1, fill=1)
    c.setFillColor(LRED); c.setFont("Helvetica-Bold", 7.4)
    c.drawCentredString(bx, by - 2.6, "1")
    c.save()

    ov = pikepdf.open(tmp)
    src.pages[0].add_overlay(ov.pages[0])
    Path(OUT).parent.mkdir(exist_ok=True)
    src.save(OUT)
    txt = subprocess.run(["pdftotext", OUT, "-"], capture_output=True, text=True).stdout
    for must in ("PROPOSED GENERATOR INLET", "45.43' from the west lot line",
                 "Metermain/Panel", "1912 JUNG BLVD E"):
        assert must in txt, "missing on the built sheet: %r" % must
    print("wrote", OUT, "| notes at %.1f pt" % size)


if __name__ == "__main__":
    build()
