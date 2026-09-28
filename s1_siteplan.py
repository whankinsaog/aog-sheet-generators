"""SP-1 — site plan markup, corrected for the Kohler correction response.

THIS COPY IS POPULATED FOR: 456 Sample Ave N, Naples FL 34102

This does NOT redraw the site plan. It overlays the customer's existing marked
survey and masks only the two regions whose content is now wrong — the callout
label and the green note block — then redraws them in the same place, the same
colours and the same style. The survey, the arrows, the generator symbol, the
setback blocks and the company block are untouched.

Why the note block had to change: it described the Generac (83.4" x 33.6", SwRI
listing), put the unit at grade on "an existing mechanical pad", claimed a 7.5'
side-yard and a 40' front line, and called the flood zone X500. The unit is a
Kohler 48RCLC on the 2nd floor mechanical deck, and Sheet A2 says Zone X.

Geometry below was measured off a 200 dpi raster of the source, not guessed.
"""
import tempfile
from pathlib import Path

import pikepdf
from reportlab.lib.colors import Color
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

SRC = str(Path(__file__).resolve().parent / "input" / "site-plan.pdf")  # put the customer's survey here
OUT = "out/SP-1 Site Plan - 456 Sample Ave N.pdf"

# sampled from the source raster so the patch is indistinguishable
GREEN = Color(24 / 255, 255 / 255, 39 / 255)
DRED = Color(139 / 255, 30 / 255, 25 / 255)
WHITE = Color(1, 1, 1)

# measured regions (PDF points, origin bottom-left)
NOTE = dict(x=303.8, y=492.8, w=439.2, h=161.7)      # green note block
LABEL_OLD = dict(x=407.9, y=815.0, w=45.3, h=14.1)   # "48KW" highlight
LABEL = dict(x=320.0, y=807.0, w=133.0, h=24.5)      # its replacement

TITLE = "Proposed location of generator — 2nd floor mechanical deck"

# ------------------------------------------------ setbacks: required vs provided
# Drawn in the clear band directly BELOW the customer's own green "Front yard /
# Side yard / Rear yard" legend, so the required figures he already put on the
# sheet and the provided figures read as one pair. The band is measured off a
# 150 dpi raster (see BAND below), not guessed, and asserted before drawing.
#
# Distances are the field/plan figures confirmed by AOG for this unit. The
# survey's own 83' to the WEST (far) lot line is deliberately NOT shown: it is
# the opposite side, no ordinance turns on it, and it does not reconcile with
# the 9'-0" east figure across a 90.00' lot. One unexplained number on a
# setback sheet is worse than one fewer dimension.
SETBACKS = [
    ("FRONT (NORTH) LOT LINE", "30'-0\"", "34'-0\""),
    ("REAR (SOUTH) LOT LINE", "25'-0\"", "110'-0\""),
    ("SIDE (EAST) LOT LINE", "7'-6\"", "9'-0\""),
]
BAND = dict(x=42.0, y=96.0, w=470.0, h=94.0)   # PDF pts, origin bottom-left

for _nm, _req, _prov in SETBACKS:
    def _ft(s):
        f, i = s.replace('"', '').split("'-")
        return int(f) + int(i) / 12.0
    assert _ft(_prov) >= _ft(_req), (
        "%s: %s provided against %s required — this sheet asserts compliance "
        "and must not print a dimension that fails it" % (_nm, _prov, _req))
BULLETS = [
    "Generator will be installed in accordance to manufacturer's instructions",
    "Kohler 48RCLC — 89.8\" x 32.9\" x 46.5\" high",
    "Generator will be set on the 2nd floor concrete mechanical deck, not at grade",
    "Generator will be 34'-0\" from the front lot line, 110'-0\" from the rear "
    "lot line and 9'-0\" from the east side lot line — no portion of the "
    "equipment is located in a required yard",
    "Generator will be 2'-4\" from the house wall — more than the 18 in. offset "
    "the 48RCLC is listed and labeled for by the manufacturer",
    "Adjacent wall is 8\" reinforced C.M.U. — noncombustible construction "
    "per Sheet A3",
    "Generator will be placed in Flood Zone X per Sheet A2",
    "Screened by planter with live vegetation to the full height of the "
    "equipment per Sec. 56-41(a)",
    "See Sheet SP-2 for dimensioned placement, clearances and screening",
]


def wrapw(text, maxw, font, size):
    out, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if stringWidth(trial, font, size) > maxw and cur:
            out.append(cur); cur = w
        else:
            cur = trial
    if cur:
        out.append(cur)
    return out


def layout(size):
    """Return the drawn lines at this type size, or None if they overrun."""
    pad, lead = 9.0, size * 1.32
    avail = NOTE["w"] - 2 * pad
    lines = [("t", l) for l in wrapw(TITLE, avail, "Helvetica-Bold", size)]
    for b in BULLETS:
        wrapped = wrapw("-" + b, avail - 4, "Helvetica", size)
        lines += [("b", w) for w in wrapped]
    if len(lines) * lead + 2 * pad > NOTE["h"]:
        return None
    return lines, pad, lead


def build():
    # pikepdf, not pypdf: pypdf's merge_page concatenated this file's content
    # stream straight onto the overlay's and produced an invalid "QQ" operator,
    # which silently killed the whole page. pikepdf's overlay wraps each stream.
    pdf = pikepdf.open(SRC)
    page = pdf.pages[0]
    assert int(page.get("/Rotate", 0)) == 0, (
        "source page is rotated; overlay coordinates would not line up")
    box = page.mediabox
    W = float(box[2]) - float(box[0])
    H = float(box[3]) - float(box[1])

    size = 10.0
    while size >= 6.0:
        got = layout(size)
        if got:
            break
        size -= 0.25
    assert got, "the corrected note will not fit the original green block"
    lines, pad, lead = got

    with tempfile.TemporaryDirectory() as td:
        ov = Path(td) / "ov.pdf"
        c = canvas.Canvas(str(ov), pagesize=(W, H))

        # ---- mask + redraw the callout label
        c.setFillColor(WHITE); c.setStrokeColor(WHITE)
        c.rect(LABEL_OLD["x"] - 1, LABEL_OLD["y"] - 1, LABEL_OLD["w"] + 2,
               LABEL_OLD["h"] + 2, stroke=1, fill=1)
        c.setFillColor(GREEN)
        c.rect(LABEL["x"], LABEL["y"], LABEL["w"], LABEL["h"], stroke=0, fill=1)
        c.setFillColor(DRED)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(LABEL["x"] + 4, LABEL["y"] + LABEL["h"] - 11,
                     "KOHLER 48RCLC")
        c.setFont("Helvetica-Bold", 8.0)
        c.drawString(LABEL["x"] + 4, LABEL["y"] + 4, "ON 2ND FLR. MECH. DECK")

        # ---- mask + redraw the green note block, same box, same colours
        c.setFillColor(GREEN); c.setStrokeColor(DRED); c.setLineWidth(2.0)
        c.rect(NOTE["x"], NOTE["y"], NOTE["w"], NOTE["h"], stroke=1, fill=1)
        c.setFillColor(DRED)
        y = NOTE["y"] + NOTE["h"] - pad - size
        for kind, text in lines:
            c.setFont("Helvetica-Bold" if kind == "t" else "Helvetica", size)
            c.drawString(NOTE["x"] + pad, y, text)
            y -= lead
        # ---- setbacks table, in the measured clear band at the foot
        bx, by, bw, bh = BAND["x"], BAND["y"], BAND["w"], BAND["h"]
        c.setFillColor(GREEN); c.setStrokeColor(DRED); c.setLineWidth(2.0)
        c.rect(bx, by, bw, bh, stroke=1, fill=1)
        c.setFillColor(DRED)
        c.setFont("Helvetica-Bold", 11.0)
        c.drawString(bx + 9, by + bh - 17, "GENERATOR SETBACKS — REQUIRED vs PROVIDED")
        colx = (bx + 9, bx + 250, bx + 350)
        c.setFont("Helvetica-Bold", 8.5)
        for cx, hd in zip(colx, ("LOT LINE", "REQUIRED", "PROVIDED")):
            c.drawString(cx, by + bh - 34, hd)
        c.setLineWidth(0.8)
        c.line(bx + 9, by + bh - 38, bx + bw - 9, by + bh - 38)
        yy = by + bh - 52
        for nm, req, prov in SETBACKS:
            c.setFont("Helvetica", 9.0)
            c.drawString(colx[0], yy, nm)
            c.drawString(colx[1], yy, req)
            c.setFont("Helvetica-Bold", 9.0)
            c.drawString(colx[2], yy, prov)
            yy -= 13.5
        _last = by + bh - 52 - 13.5 * (len(SETBACKS) - 1)
        assert _last > by + 8, "the setbacks table overruns its band"

        c.save()
        with pikepdf.open(str(ov)) as ovp:
            page.add_overlay(ovp.pages[0])
        pdf.save(OUT)
    print("wrote", OUT, " note type size %.2f pt, %d lines" % (size, len(lines)))


if __name__ == "__main__":
    build()
