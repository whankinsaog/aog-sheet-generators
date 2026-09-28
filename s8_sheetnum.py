"""Stamp a sheet number onto a PDF that was produced outside the generators.

Used for the AOG load-calculation sheets, which come out of the load-calc
workbook rather than reportlab. The calc itself is NOT touched — this only
composites a sheet number into the clear strip at the foot of the page, so the
calc keeps whatever numbers were submitted and reviewed.

Two things this script does rather than assume:
  * checks /Rotate on the source page and calls transfer_rotation_to_content()
    when it is non-zero, so the overlay lands where a viewer shows the page
    rather than where the raw content stream puts it;
  * measures the actual clear space at the foot of the page by rasterising it
    and finding the last row with ink, and refuses to stamp if the number
    would land on top of existing content.

Usage:  python3 s8_sheetnum.py <in.pdf> <out.pdf> <sheet>
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import Color, black
from reportlab.pdfgen import canvas

ORNG = Color(.76, .38, .08)
DPI = 150
SIZE = 14.0          # sheet-number type size
PAD_R = 28.0         # right margin for the number
BASE = 7.0           # baseline above the page foot


def clear_points_at_foot(pdf_path):
    """Rasterise page 1 and return the height, in points, of the clear strip
    at the bottom of the page."""
    with tempfile.TemporaryDirectory() as td:
        stem = str(Path(td) / "pg")
        subprocess.run(["pdftoppm", "-r", str(DPI), "-png", "-f", "1", "-l", "1",
                        str(pdf_path), stem], check=True)
        png = next(Path(td).glob("pg*.png"))
        a = np.array(Image.open(png).convert("L"))
    rows = np.where((a < 240).any(axis=1))[0]
    if len(rows) == 0:
        return a.shape[0] / DPI * 72.0
    return (a.shape[0] - 1 - rows.max()) / DPI * 72.0


def stamp(src, dst, sheet):
    reader = PdfReader(str(src))
    page = reader.pages[0]
    if page.get("/Rotate"):
        page.transfer_rotation_to_content()
    w = float(page.mediabox.width)
    h = float(page.mediabox.height)

    clear = clear_points_at_foot(src)
    needed = BASE + SIZE + 3
    assert clear >= needed, (
        "only %.1f pt clear at the foot of %s; the sheet number needs %.1f pt "
        "and would land on existing content" % (clear, Path(src).name, needed))

    with tempfile.TemporaryDirectory() as td:
        ov = Path(td) / "ov.pdf"
        c = canvas.Canvas(str(ov), pagesize=(w, h))
        c.setStrokeColor(ORNG)
        c.setLineWidth(1.0)
        c.line(w - PAD_R - 58, BASE + SIZE + 1.5, w - PAD_R, BASE + SIZE + 1.5)
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", SIZE)
        c.drawRightString(w - PAD_R, BASE, sheet)
        c.save()
        page.merge_page(PdfReader(str(ov)).pages[0])

    out = PdfWriter()
    out.add_page(page)
    with open(dst, "wb") as fh:
        out.write(fh)
    print("%-6s -> %s  (%.1f pt clear at foot)" % (sheet, Path(dst).name, clear))


if __name__ == "__main__":
    stamp(sys.argv[1], sys.argv[2], sys.argv[3])
