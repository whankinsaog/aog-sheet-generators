"""Sheet E-2 — panel schedules only, restated from RCI Engineering Sheet E5."""
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, black, white
from aoglib import tx, box, line, wrap, titleblock, GREY
import paneldata as D

W, H = 2592.0, 1728.0
RED = Color(.78, .05, .09)
HDRC = Color(.90, .90, .90)
METAC = Color(.955, .955, .955)
TBW, M = 400, 18

PW = 1040.0
HALF = PW / 2
RH = 18.0
LBL = {"ND": "NO DEM.\nkVA", "APP": "APP.\nkVA", "LTG": "LTG.\nkVA", "DEM": "DEM.\nkVA"}
OTHER = {"TRIP": "TRIP\nPOLE", "TYPE": "BRKR\nTYPE", "COND": "CON-\nDUIT",
         "WIRE": "WIRE", "DESC": "DESCRIPTION", "CKT": "CKT"}

c = canvas.Canvas("out/E-2 Panel Schedules - 789 Placeholder Dr.pdf", pagesize=(W, H))
box(c, M, M, W - 2 * M, H - 2 * M, lw=1.6)


def colspec(cols):
    if len(cols) == 2:
        w = {cols[0]: 56, cols[1]: 56, "TRIP": 46, "TYPE": 38, "COND": 38,
             "WIRE": 32, "DESC": 224, "CKT": 30}
        order = [cols[0], cols[1], "TRIP", "TYPE", "COND", "WIRE", "DESC", "CKT"]
    else:
        w = {cols[0]: 44, cols[1]: 42, cols[2]: 46, "TRIP": 42, "TYPE": 34,
             "COND": 34, "WIRE": 28, "DESC": 222, "CKT": 28}
        order = [cols[0], cols[1], cols[2], "TRIP", "TYPE", "COND", "WIRE",
                 "DESC", "CKT"]
    assert abs(sum(w[k] for k in order) - HALF) < .01, sum(w[k] for k in order)
    return order, w


def head_label(k):
    return LBL[k] if k in LBL else OTHER[k]


def draw_panel(x0, ytop, p):
    order, wd = colspec(p["cols"])
    nrows = p["nckt"] // 2

    # ---- name + meta strip
    MH = 44
    y = ytop - MH
    box(c, x0, y, PW, MH, lw=1.1, fill=METAC)
    tx(c, x0 + 14, y + 15, "PANEL  '%s'" % p["name"], 15, "Helvetica-Bold")
    mx = x0 + 176
    cw = (PW - 176) / len(p["meta"])
    for i, (k, v) in enumerate(p["meta"]):
        xx = mx + i * cw
        line(c, xx, y, xx, y + MH, lw=.6, col=GREY)
        tx(c, xx + 7, y + MH - 15, k, 6.4, "Helvetica-Bold", GREY)
        tx(c, xx + 7, y + MH - 29, v, 8, "Helvetica-Bold")

    # ---- column header
    HH = 24
    y -= HH
    box(c, x0, y, PW, HH, lw=1.0, fill=HDRC)
    for side in (0, 1):
        cols = order if side == 0 else list(reversed(order))
        xx = x0 + side * HALF
        for k in cols:
            line(c, xx, y, xx, y + HH, lw=.55, col=GREY)
            ls = head_label(k).split("\n")
            yy = y + HH - 10 if len(ls) == 1 else y + HH - 8
            for l in ls:
                tx(c, xx + wd[k] / 2, yy - 3, l, 6.2, "Helvetica-Bold", anchor="c")
                yy -= 7.6
            xx += wd[k]

    top = y
    bot = top - nrows * RH

    def draw_side(rows, side):
        cols = order if side == 0 else list(reversed(order))
        base = x0 + side * HALF
        xs, xx = {}, base
        for k in cols:
            xs[k] = xx
            xx += wd[k]
        for (ck, poles, desc, wire, cond, brk, trip, vals, _shed) in rows:
            i = (ck - (2 if side else 1)) // 2
            y1 = top - i * RH
            y0 = y1 - poles * RH
            for k in cols:
                if k == "CKT":
                    for q in range(poles):
                        yy = y1 - q * RH
                        box(c, xs[k], yy - RH, wd[k], RH, lw=.45, fill=None, stroke=GREY)
                        tx(c, xs[k] + wd[k] / 2, yy - RH + 6.2, str(ck + 2 * q), 6.6,
                           "Helvetica-Bold", anchor="c")
                    continue
                box(c, xs[k], y0, wd[k], poles * RH, lw=.45, fill=None, stroke=GREY)
                v = ({"DESC": desc, "TRIP": trip, "TYPE": brk, "COND": cond,
                      "WIRE": wire}.get(k) or vals.get(k, "—"))
                if not v:
                    continue
                yc = y0 + poles * RH / 2 - 2.6
                if k == "DESC":
                    ind = 7
                    if _shed:
                        by_ = y0 + poles * RH / 2
                        box(c, xs[k] + 5, by_ - 5.6, 11.5, 11.2, lw=.7,
                            fill=None, stroke=RED)
                        tx(c, xs[k] + 10.75, by_ - 2.7, "M", 7.0,
                           "Helvetica-Bold", RED, anchor="c")
                        ind = 21
                    ls = v.split("\n")
                    yy = yc + (len(ls) - 1) * 3.8
                    for l in ls:
                        tx(c, xs[k] + ind, yy, l, 7.4,
                           "Helvetica" if desc == "SPACE" else "Helvetica-Bold",
                           GREY if desc == "SPACE" else black)
                        yy -= 7.6
                else:
                    tx(c, xs[k] + wd[k] / 2, yc, v, 7.0,
                       col=GREY if desc == "SPACE" else black, anchor="c")

    draw_side(p["odd"], 0)
    draw_side(p["even"], 1)
    box(c, x0, bot, PW, top - bot, lw=1.2)
    line(c, x0 + HALF, bot, x0 + HALF, top, lw=1.2)

    # ---- column totals
    TH = 20
    ty = bot - TH
    box(c, x0, ty, PW, TH, lw=1.0, fill=Color(.93, .93, .93))
    for side in (0, 1):
        cols = order if side == 0 else list(reversed(order))
        xx = x0 + side * HALF
        tot = p["totals"]["L" if side == 0 else "R"]
        for k in cols:
            line(c, xx, ty, xx, ty + TH, lw=.55, col=GREY)
            if k == "DESC":
                tx(c, xx + (7 if side == 0 else wd[k] - 7), ty + 6.6, "COLUMN TOTALS",
                   6.8, "Helvetica-Bold", anchor="l" if side == 0 else "r")
            elif k in tot:
                tx(c, xx + wd[k] / 2, ty + 6.4, tot[k], 7.4, "Helvetica-Bold", anchor="c")
            xx += wd[k]

    # ---- key notes, full width
    #
    # The engineer's load-summary block (TOTAL GENERAL LIGHTING LOAD / FIRST
    # 3 kVA + 35% / APPLIANCES @ 75% / TOTAL CALCULATED LOAD) is deliberately
    # NOT restated here. Those are NEC 220 Part III standard-method figures;
    # the submitted calc is the 220.82 optional method on sheets E-3 / E-4.
    # Carrying both into one package puts two different calculated loads in
    # front of the reviewer and reads as a contradiction. The panel schedules
    # are the circuit reference; the load calc lives on its own sheets.
    # p["summary"] is retained in paneldata.py as provenance only.
    WRAPC = 170
    nlines = sum(len(wrap(n, WRAPC)) for n in p["keynotes"])
    BH = max(46, 27 + nlines * 7.4 + len(p["keynotes"]) * 1.4 + 6)
    by = ty - BH
    box(c, x0, by, PW, BH, lw=1.0)
    tx(c, x0 + 10, by + BH - 14, "KEY NOTES", 8, "Helvetica-Bold")
    yy = by + BH - 27
    for n in p["keynotes"]:
        for ln in wrap(n, WRAPC):
            tx(c, x0 + 10, yy, ln, 6.2)
            yy -= 7.4
        yy -= 1.4
    return ytop - by


# ======================================================================= sheet
tx(c, 26, H - M - 26, "PANEL SCHEDULES", 20, "Helvetica-Bold")
tx(c, 26, H - M - 42, "ALL PANELS, ALL BREAKERS  ·  PER RCI ENGINEERING SHEET E5, "
                      "DATED 02-27-2025  ·  ALL PANELS ARE EXISTING AND ARE "
                      "NOT ALTERED UNDER THIS PERMIT", 9, "Helvetica-Oblique", GREY)

LX, RXC = 26.0, 1096.0
y = H - M - 58
for pn in (D.PA, D.PB, D.PD):
    y -= draw_panel(LX, y, pn) + 26
y2 = H - M - 58
for pn in (D.MDP, D.PC, D.PP):
    y2 -= draw_panel(RXC, y2, pn) + 26

titleblock(c, W, H, "E-2", "PANEL SCHEDULES", margin=M, tbw=TBW, stamp=250)
c.save()
print("ok")
