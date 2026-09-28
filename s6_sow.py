"""Fill Always On Generators' Scope of Work template.

THIS COPY IS POPULATED FOR: 1912 Jung Blvd E, Naples FL 34120 (Collier County)
                            NEW PERMIT — electric only: portable generator inlet +
                            Square D RCGK2 interlock. No fuel gas, no load calc
                            (manual transfer, NEC 702.4(B)(1)).

Overlays text onto the company template so the seal and the FBC 105.6 /
105.7 / 107.2.1 boilerplate are preserved exactly as they are in the
original file. pikepdf, not pypdf: pypdf's merge_page has emitted an
invalid "QQ" operator on this kind of composite and silently killed the
page, which renders as the untouched original rather than as an error.

The body auto-fits: it steps the type down until the block clears the
usable band, then asserts it fits. It must stay on one page — the FBC
block already runs to the bottom margin.
"""
import tempfile
from pathlib import Path

import pikepdf
from reportlab.lib.colors import black
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from aoglib import DATE_SHORT, FBC_TITLE, NEC_EDITION

SRC = "Scope of Work.pdf"
OUT = "out/Scope of Work - 1912 Jung Blvd E.pdf"

W, H = 612.0, 792.0
VX = 320.0                      # x for the three header values
LX, RX = 56.0, 572.0            # description text column
TOP, BOT = 506.0, 236.0         # usable vertical band for the description

DATE = DATE_SHORT
LOCATION = "1912 Jung Blvd E, Naples, Florida 34120"
PROJECT = "Portable Generator Inlet & Interlock — Electrical"

BODY = [
    ("p", "Install a 50 A portable generator power inlet and a listed generator "
          "interlock kit in the existing 200 A Square D Homeline RC-series meter-main at an "
          "existing single-family dwelling, Parcel 37393720002, West 1/2 of Tract "
          "49, Golden Gate Estates Unit 16. Transfer is manual."),
    ("h", "WORK INCLUDED IN THIS PERMIT:"),
    ("n", "Install one (1) Square D RCGK2 generator interlock kit in the existing "
          "meter-main, with a 50 A 2-pole HOM backfed generator breaker in positions "
          "2 and 4 nearest the service disconnect, secured per NEC 408.36(D). Only "
          "one of the 200 A main and the generator breaker can be on at any time "
          "— NEC 702.5."),
    ("n", "Install one (1) Connecticut Electric EGSPI50 50 A, 125/250 V NEMA 3R "
          "power inlet outdoors beside the meter-main: (3) #8 AWG CU or #6 AWG AL "
          "and (1) #10 AWG CU or #8 AWG AL equipment grounding conductor in 3/4\" "
          "PVC. Warning sign at the inlet per NEC 702.7(C)."),
    ("n", "Install one (1) 100 A NEMA 3R sub panel fed from a 100 A 2-pole HOM "
          "breaker in the meter-main — (3) #3 AWG CU or #1 AWG AL, EGC #8 AWG CU or "
          "#6 AWG AL, in 1-1/4\" PVC — and re-terminate the existing pool panel "
          "feeder ((3) #6 AWG CU, EGC #8 AWG CU, 1\" PVC, as installed) on a new "
          "60 A 2-pole breaker in it."),
    ("n", "Install one (1) Square D Homeline SurgeBreaker plug-in surge protective "
          "device in the meter-main — NEC 230.67."),
    ("n", "Mark the 200 A main EMERGENCY DISCONNECT, SERVICE DISCONNECT per NEC "
          "230.85(1) and 110.21(B), and post the optional standby source sign at "
          "the service per NEC 702.7(A)."),
    ("h", "NOT IN THIS PERMIT:"),
    ("b", "The portable generator and its cord set — furnished by the owner."),
    ("b", "The existing meter-main enclosure, Panel 'A' (200 A) and its feeder, the "
          "pool panel and its feeder conductors, and the grounding electrode system — existing, not altered."),
    ("h", "CODES IN FORCE:"),
    ("p", "%s; %s." % (NEC_EDITION, FBC_TITLE)),
]

for _k, _t in BODY:
    for _bad in ("field verify", "verify", "confirm", "to be determined", "T.B.D."):
        assert _bad.lower() not in _t.lower(), (
            "%r appears in the scope of work; a permit document states the "
            "installed condition, it does not flag its own homework" % _bad)

for _k, _t in BODY:
    for _ch in _t:
        try:
            _ch.encode("cp1252")
        except UnicodeEncodeError:
            raise AssertionError("%r is outside WinAnsi and prints as a black box" % _ch)


def wrapw(text, maxw, font, size):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if stringWidth(t, font, size) > maxw and cur:
            out.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out


def layout(size, lead):
    """Return drawing instructions and the total height at this font size."""
    ops, y, num = [], 0.0, 0
    for i, (kind, text) in enumerate(BODY):
        if i:
            y -= lead * (0.75 if kind == "h" else 0.28)
        if kind == "h":
            ops.append((LX, y, text, "Helvetica-Bold", size))
            y -= lead
            continue
        if kind == "n":
            num += 1
            mark, ind = "%d." % num, 20.0
        elif kind == "b":
            mark, ind = "•", 14.0
        else:
            mark, ind = None, 0.0
        lines = wrapw(text, RX - LX - ind, "Helvetica", size)
        for j, ln in enumerate(lines):
            if j == 0 and mark:
                ops.append((LX, y, mark, "Helvetica", size))
            ops.append((LX + ind, y, ln, "Helvetica", size))
            y -= lead
    return ops, -y


ops = None
for SZ in (10.0, 9.6, 9.2, 8.8, 8.4, 8.0, 7.6, 7.2):
    LEAD = SZ * 1.30
    ops, total = layout(SZ, LEAD)
    if total <= TOP - BOT:
        break
assert ops is not None and total <= TOP - BOT, (
    "the scope of work runs %.0f pt against %.0f pt of band and will spill onto "
    "a second page — cut a line, do not shrink past 7.2 pt" % (total, TOP - BOT))

with tempfile.TemporaryDirectory() as td:
    ov = Path(td) / "ov.pdf"
    c = canvas.Canvas(str(ov), pagesize=(W, H))
    c.setFillColor(black)

    for val, vy in ((DATE, 716.0), (LOCATION, 692.0), (PROJECT, 668.0)):
        fs = 11.0
        while stringWidth(val, "Helvetica-Bold", fs) > 582.0 - VX and fs > 8.0:
            fs -= 0.25
        c.setFont("Helvetica-Bold", fs)
        c.drawString(VX, vy, val)

    for x, dy, text, font, size in ops:
        c.setFont(font, size)
        c.drawString(x, TOP + dy, text)
    c.save()

    pdf = pikepdf.open(SRC)
    page = pdf.pages[0]
    assert int(page.get("/Rotate", 0)) == 0, (
        "the template page is rotated; overlay coordinates would not line up")
    assert len(pdf.pages) == 1, "the scope of work template is no longer one page"
    with pikepdf.open(str(ov)) as ovp:
        page.add_overlay(ovp.pages[0])
    pdf.save(OUT)

print("ok  font %.1f  height %.0f of %.0f" % (SZ, total, TOP - BOT))
