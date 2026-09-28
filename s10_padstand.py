#!/usr/bin/env python3
"""S-1 / S-2 — AOG elevated aluminum generator stand on a precast foam-core pad.

THIS COPY IS POPULATED FOR: AOG STANDARD DETAIL — NOT SITE SPECIFIC

This sheet is an IN-HOUSE MARKUP issued to an engineer for review and seal. It
is not a stamped document and nothing on it is an engineering conclusion: the
geometry is what AOG fabricates and installs, and every capacity question is
listed for the engineer of record in the OPEN ITEMS block on S-1.

Two things make it different from the rest of the stack, and both are switches
in aoglib.titleblock() rather than a second title block:

  * somebody else seals it, so the contractor licence numbers DO print
    (they come off only on a sheet Brandon seals himself), and
  * the reserved box at the top of the title block is labelled for the
    engineer of record, not for AOG.

Sources for the geometry, both in Permitting Files\\Electrical\\Concrete pad and
Elevated Stand details\\:
  * stand frame, gussets, base plates, mid-height brace, welds — AMG Structural
    Engineering master set "14-28Kw Air Cooled Master Set 03-16-2026 AMG.pdf"
    (Aaron M. Gillmor PE 67567), which covers the stand on a cast-in-place slab
    and stops at a 4'-0" stand. Heights above 4'-0" are deliberately not drawn.
  * pad size, make-up and the leg-to-pad anchor AOG installs — the precast
    foam-core pad AOG buys, 54" x 32" x 4".

The precast pad is a different host from the cast slab the stand set was sealed
against, which is the whole reason this goes to an engineer. Say that on the
sheet rather than implying the two sealed sets already cover it.

    mkdir -p out && python3 s10_padstand.py
"""
import os
import sys

from reportlab.lib.colors import Color, black, white
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aoglib as A
from aoglib import GREY, box, line, tx, wrap

# --------------------------------------------------------------- sheet content
# Non-site-specific standard detail: the title block's PROJECT lines name the
# assembly instead of an address, and JURISDICTION says out loud that applying
# it to a site is the engineer's call, not this sheet's.
A.JOB = dict(
    addr="ALUMINUM GENERATOR STAND",
    city="ON A PRECAST FOAM-CORE PAD",
    proj="AOG STANDARD DETAIL — NOT SITE SPECIFIC",
    ahj="SITE-SPECIFIC APPLICATION BY THE E.O.R.",
    gen="AIR-COOLED STANDBY GENERATOR, 14–28 kW — "
        "48\" L × 26\" W × 33\" H MAX ENVELOPE",
    ats="PRECAST FOAM-CORE CONCRETE PAD — 54\" × 32\" × 4\", 362 LB MIN",
    date=A.DATE_SHORT,
    scope=("IN-HOUSE MARKUP ISSUED FOR STRUCTURAL REVIEW AND SEAL. AOG STANDARD "
           "ALUMINUM GENERATOR STAND, 1'-0\" TO 4'-0\" CLEAR HEIGHT, ANCHORED TO A "
           "PRECAST FOAM-CORE CONCRETE PAD AT GRADE. GEOMETRY AND CONNECTIONS ARE "
           "AS AOG FABRICATES AND INSTALLS THEM. ALL CAPACITIES, ANCHOR VALUES AND "
           "WIND PRESSURES ARE FOR THE ENGINEER OF RECORD TO DETERMINE."),
)
# Structural sheet, so the NEC half of the standard CODES line is replaced with
# the structural standards — but the FBC and ASCE 7 editions still come from
# aoglib.CODE_CYCLES, never typed here.
A.CODES = ("%s · %s · ALUMINUM DESIGN MANUAL · ACI 318 · AWS D1.2"
           % (A.FBC_EDITION, A.ASCE7_EDITION))

LIC = "ECI3007388 · LI100055"

ORANGE = Color(.76, .38, .08)
HAIR = Color(.88, .88, .88)
BAND = Color(.975, .965, .945)

W, H = 17 * 72, 11 * 72                    # 17x11 landscape
MARGIN, TBW = 18, 250
XL = MARGIN + 12                           # left edge of the drawing area
XR = W - MARGIN - TBW - 12                 # right edge of the drawing area
NOTEX = 700                                # notes column starts here
NOTEW = XR - NOTEX

PPI = 3.0                                  # points per real-world inch


# ------------------------------------------------------------------- helpers
def sechead(c, x, y, head, sub=None, w=None):
    """7.6 pt bold orange over a 0.9 pt orange rule, grey subtitle after."""
    tx(c, x, y, head, 7.6, "Helvetica-Bold", ORANGE)
    line(c, x, y - 4.5, x + (w or 200), y - 4.5, .9, ORANGE)
    if sub:
        tx(c, x, y - 14, sub, 6.6, "Helvetica", GREY)
        return y - 24
    return y - 15


def bub(c, x, y, num, ref, r=8.5):
    c.saveState()
    c.setLineWidth(.9)
    c.setStrokeColor(black)
    c.circle(x, y, r, stroke=1, fill=0)
    c.restoreState()
    tx(c, x, y - 3.1, str(num), 9, "Helvetica-Bold", black, "c")
    if ref:
        line(c, x - r, y - r - 2.5, x + r, y - r - 2.5, .7)
        tx(c, x, y - r - 11, str(ref), 7.5, "Helvetica", black, "c")


def dtitle(c, x, y, num, title, view="DETAIL", ref="S-1", scale="NOT TO SCALE"):
    """Detail bubble + title, house style: bubble left, title right of it."""
    bub(c, x + 9, y + 9, num, ref)
    tx(c, x + 26, y + 11, title, 9.6, "Helvetica-Bold")
    tx(c, x + 26, y + 2, scale, 6.2, "Helvetica", GREY)
    tx(c, x + 26 + c.stringWidth(scale, "Helvetica", 6.2) + 10, y + 2, view,
       6.2, "Helvetica", GREY)


def tick(c, x, y, lw=.6):
    line(c, x - 2.4, y - 2.4, x + 2.4, y + 2.4, lw)


def dimh(c, x1, x2, y, label, size=5.4, ext=None, col=black):
    line(c, x1, y, x2, y, .5, col)
    tick(c, x1, y); tick(c, x2, y)
    if ext is not None:
        line(c, x1, y, x1, ext, .35, HAIR)
        line(c, x2, y, x2, ext, .35, HAIR)
    tx(c, (x1 + x2) / 2, y + 2.6, label, size, "Helvetica", col, "c")


def dimv(c, y1, y2, x, label, size=5.4, ext=None, col=black):
    line(c, x, y1, x, y2, .5, col)
    tick(c, x, y1); tick(c, x, y2)
    if ext is not None:
        line(c, x, y1, ext, y1, .35, HAIR)
        line(c, x, y2, ext, y2, .35, HAIR)
    tx(c, x - 2.6, (y1 + y2) / 2, label, size, "Helvetica", col, "c", rot=90)


def lead(c, tipx, tipy, tox, toy, lines, size=5.6, anchor="l", lw=.5):
    """Leader from an arrow tip to a stack of text."""
    line(c, tipx, tipy, tox, toy, lw)
    c.saveState()
    c.setFillColor(black)
    c.setStrokeColor(black)
    dx, dy = tipx - tox, tipy - toy
    m = max((dx * dx + dy * dy) ** .5, .001)
    ux, uy = dx / m, dy / m
    px, py = -uy, ux
    pth = c.beginPath()
    pth.moveTo(tipx, tipy)
    pth.lineTo(tipx - 5 * ux + 1.7 * px, tipy - 5 * uy + 1.7 * py)
    pth.lineTo(tipx - 5 * ux - 1.7 * px, tipy - 5 * uy - 1.7 * py)
    pth.close()
    c.drawPath(pth, stroke=0, fill=1)
    c.restoreState()
    ty = toy + 1.5 + 6.6 * (len(lines) - 1)
    sx = tox + (3 if anchor == "l" else -3)
    for ln in lines:
        tx(c, sx, ty, ln, size, "Helvetica", black, anchor)
        ty -= 6.6


def concrete(c, x, y, w, h, seed=7, dens=.0016):
    """Cast concrete poche — stipple plus a few aggregate flecks."""
    box(c, x, y, w, h, lw=.7, fill=white)
    st = seed
    n = int(w * h * dens) + 6
    for i in range(n):
        st = (st * 1103515245 + 12345) & 0x7FFFFFFF
        px = x + 2 + (st % 10000) / 10000.0 * max(w - 4, 1)
        st = (st * 1103515245 + 12345) & 0x7FFFFFFF
        py = y + 2 + (st % 10000) / 10000.0 * max(h - 4, 1)
        st = (st * 1103515245 + 12345) & 0x7FFFFFFF
        if st % 3 == 0:
            p = c.beginPath()
            p.moveTo(px, py); p.lineTo(px + 2.1, py)
            p.lineTo(px + 1.05, py + 1.9); p.close()
            c.saveState(); c.setFillColor(Color(.45, .45, .45))
            c.drawPath(p, stroke=0, fill=1); c.restoreState()
        else:
            c.saveState(); c.setFillColor(Color(.5, .5, .5))
            c.circle(px, py, .45, stroke=0, fill=1); c.restoreState()


def foam(c, x, y, w, h):
    """EPS core — light fill with a fine diagonal rule."""
    box(c, x, y, w, h, lw=.6, fill=Color(.955, .955, .93))
    i = 0.0
    while i < w + h:
        x1, y1 = x + i, y
        x2, y2 = x, y + i
        if x1 > x + w:
            y1 += x1 - (x + w); x1 = x + w
        if y2 > y + h:
            x2 += y2 - (y + h); y2 = y + h
        if x1 >= x2 and y1 <= y2:
            line(c, x1, y1, x2, y2, .3, Color(.78, .78, .74))
        i += 4.5


def alum(c, x, y, w, h, lw=.8):
    """Aluminum member in section — solid-ish grey fill."""
    box(c, x, y, w, h, lw=lw, fill=Color(.80, .80, .82))


def grade(c, x1, x2, y, label=True):
    line(c, x1, y, x2, y, .9)
    x = x1
    while x < x2:
        line(c, x, y, x - 4, y - 4.5, .45, Color(.45, .45, .45))
        x += 5.5
    if label:
        tx(c, x2 + 3, y + 2, "GRADE", 5.6, "Helvetica", GREY)


def notes(c, x, y, w, head, sub, items, size=5.9, lead_=7.3, num=True,
          gap=4.5, bullet=None):
    """Numbered / bulleted note block. Returns the y below the last line."""
    y = sechead(c, x, y, head, sub, w)
    for i, it in enumerate(items):
        pre = ("%d." % (i + 1)) if num else (bullet or "·")
        tx(c, x, y, pre, size, "Helvetica-Bold")
        ind = 13 if num else 8
        for j, ln in enumerate(wrap(it, int((w - ind) / (size * .49)))):
            tx(c, x + ind, y, ln, size, "Helvetica")
            y -= lead_
        y -= gap * .45
    return y - gap


# ============================================================== S-1 details
def stand_elev(c, ox, oy, height_in, front=False, brace=False, gen=True):
    """One stand elevation. oy is the GRADE line; the pad sits on it.

    front=True draws the 2'-2" face, otherwise the 4'-0" face.
    """
    P = PPI
    span = (26.0 if front else 48.0)
    padw = (32.0 if front else 54.0)
    cx = ox + padw * P / 2.0

    # ---- pad (4" thick, sitting at grade)
    px, pt = ox, oy + 4 * P
    concrete(c, px, oy, padw * P, 4 * P, seed=11 if front else 5)
    grade(c, px - 30, px, oy, label=False)
    grade(c, px + padw * P, px + padw * P + 30, oy, label=False)

    # ---- legs: 3x3 tube, base plate 6x6x1/4
    lx0 = cx - span * P / 2.0
    lx1 = cx + span * P / 2.0
    top = pt + height_in * P
    for lx in (lx0, lx1):
        s = -1 if lx == lx0 else 1
        # base plate
        alum(c, lx - (0 if s < 0 else 6 * P), pt, 6 * P, .25 * P)
        # anchors through the plate
        for a in (1.5, 4.5):
            axp = (lx + a * P) if s < 0 else (lx - 6 * P + a * P)
            line(c, axp, pt + .25 * P, axp, pt - 2 * P, 1.0)
            line(c, axp - 1.6, pt + .25 * P + 1.2, axp + 1.6, pt + .25 * P + 1.2, 1.4)
        # leg tube
        legx = lx if s < 0 else lx - 3 * P
        alum(c, legx, pt + .25 * P, 3 * P, top - pt - .25 * P - 3 * P)

    # ---- top rail: 3x6 LLH angle, 3" deep
    alum(c, lx0, top - 3 * P, span * P, 3 * P)

    # ---- corner gussets 8x8x1/4
    def gus(c_, x_, y_, s_):
        p = c_.beginPath()
        p.moveTo(x_, y_); p.lineTo(x_ + s_ * 8 * P, y_)
        p.lineTo(x_, y_ - 8 * P); p.close()
        c_.saveState(); c_.setFillColor(Color(.72, .72, .75))
        c_.setStrokeColor(black); c_.setLineWidth(.7)
        c_.drawPath(p, stroke=1, fill=1); c_.restoreState()

    gus(c, lx0 + 3 * P, top - 3 * P, 1)
    gus(c, lx1 - 3 * P, top - 3 * P, -1)

    # ---- mid-height brace: 3x3 angle + gussets, only over 3'-0"
    if brace:
        by = pt + height_in * P / 2.0
        alum(c, lx0 + 3 * P, by, span * P - 6 * P, 3 * P)
        gus(c, lx0 + 3 * P, by + 3 * P, 1)
        gus(c, lx1 - 3 * P, by + 3 * P, -1)
        dimv(c, pt, by, lx0 - 13, "EQ")
        dimv(c, by, top - 3 * P, lx0 - 13, "EQ")

    # ---- generator envelope
    if gen:
        gh = 16 * P
        c.saveState(); c.setDash(3, 2); c.setLineWidth(.7)
        c.setStrokeColor(Color(.45, .45, .45))
        c.rect(cx - (48 if not front else 26) * P / 2.0, top,
               (48 if not front else 26) * P, gh, stroke=1, fill=0)
        c.restoreState()
        tx(c, cx, top + gh - 9, "GENERATOR UNIT", 5.6, "Helvetica-Bold", GREY, "c")
        tx(c, cx, top + gh - 16, "BY OTHERS", 5.6, "Helvetica", GREY, "c")
        line(c, cx - 14, top + gh + 3, cx + 14, top + gh + 3, .5, Color(.6, .6, .6))
        tx(c, cx, top + gh + 6, "(BREAK)", 4.8, "Helvetica-Oblique", GREY, "c")

    # ---- dimensions
    dimv(c, pt, top, lx1 + 16, height_in >= 36 and "3'-0\" TO 4'-0\"" or "1'-0\" TO 3'-0\"")
    dimh(c, lx0, lx1, top + (gen and 16 * P + 26 or 14),
         "%s (OUT TO OUT)" % ("2'-2\"" if front else "4'-0\""))
    dimh(c, px, px + padw * P, oy - 16, "%s PAD" % ("2'-8\"" if front else "4'-6\""))
    return top


def pad_section(c, ox, oy):
    """Section through the precast foam-core pad, long direction."""
    P = PPI * 2.4                       # blown up — 4" of pad needs the scale
    L, T = 54.0, 4.0
    end = 14.0                          # solid concrete band at each end
    core = L - 2 * end

    concrete(c, ox, oy, L * P, T * P, seed=23, dens=.0020)
    foam(c, ox + end * P, oy, core * P, 2 * P)
    # concrete plugs through the core
    for i in range(4):
        cxp = ox + (end + 3.0 + i * (core - 6.0) / 3.0) * P
        concrete(c, cxp - 1 * P, oy, 2 * P, 2 * P, seed=31 + i, dens=.004)
    box(c, ox, oy, L * P, T * P, lw=1.0)
    line(c, ox, oy + 2 * P, ox + L * P, oy + 2 * P, .4, Color(.55, .55, .55))

    grade(c, ox - 46, ox, oy, label=False)
    grade(c, ox + L * P, ox + L * P + 46, oy, label=False)

    # perimeter bar + mesh
    for i in range(11):
        xx = ox + (3 + i * 4.8) * P
        c.saveState(); c.setFillColor(black)
        c.circle(xx, oy + 3 * P, 1.1, stroke=0, fill=1); c.restoreState()
    c.saveState(); c.setFillColor(black)
    c.circle(ox + 1.6 * P, oy + 2.6 * P, 1.5, stroke=0, fill=1)
    c.circle(ox + L * P - 1.6 * P, oy + 2.6 * P, 1.5, stroke=0, fill=1)
    c.restoreState()

    top_ = oy + T * P
    lead(c, ox + 1.6 * P, oy + 2.6 * P, ox + 2 * P, top_ + 22,
         ["#2 PERIMETER BAR, ALL SIDES"])
    lead(c, ox + 20 * P, oy + 1 * P, ox + 14 * P, top_ + 46,
         ["2\"Ø CONCRETE SUPPORTS THROUGH", "THE CORE — (8) TOTAL"])
    lead(c, ox + 30 * P, oy + 1 * P, ox + 31 * P, top_ + 22,
         ["2\" EPS FOAM CORE"])
    lead(c, ox + 40 * P, oy + 3.3 * P, ox + 36 * P, top_ + 46,
         ["#2 REBAR @ 12\" O.C. EACH WAY,", "OR W6 × W6 / W1.4 × W1.4 W.W.M."])
    lead(c, ox + 48 * P, oy + 3 * P, ox + 45 * P, top_ + 22,
         ["2\" CONCRETE TOP SLAB,", "3,000 PSI MIN"])

    dimh(c, ox, ox + end * P, oy - 18, "1'-2\" SOLID")
    dimh(c, ox + end * P, ox + (end + core) * P, oy - 18, "2'-2\" FOAM CORE")
    dimh(c, ox + (end + core) * P, ox + L * P, oy - 18, "1'-2\" SOLID")
    dimh(c, ox, ox + L * P, oy - 34, "4'-6\" PAD LENGTH")
    dimv(c, oy, oy + T * P, ox + L * P + 16, "4\"")

    # the legs land on the solid bands — the point of the whole detail
    for lx in (ox + 3 * P, ox + (L - 3) * P):
        c.saveState(); c.setDash(2, 2); c.setStrokeColor(ORANGE); c.setLineWidth(1.0)
        c.rect(lx - 3 * P, top_, 6 * P, 4, stroke=1, fill=0)
        c.restoreState()
    lead(c, ox + 3 * P, top_ + 4, ox + 4 * P, top_ + 70,
         ["STAND LEG BASE PLATES BEAR ON THE SOLID CONCRETE",
          "END BANDS — NOT OVER THE FOAM CORE"])


def assembly_elev(c, ox, oy):
    """Whole system at 4'-0": generator, stand, pad, ground anchors."""
    P = PPI * .62
    padw, H_ = 54.0, 48.0
    concrete(c, ox, oy, padw * P, 4 * P, seed=9)
    grade(c, ox - 40, ox, oy, label=False)
    grade(c, ox + padw * P, ox + padw * P + 40, oy, label=False)
    pt = oy + 4 * P
    cx = ox + padw * P / 2.0
    lx0, lx1 = cx - 24 * P, cx + 24 * P
    top = pt + H_ * P
    for lx, s in ((lx0, -1), (lx1, 1)):
        alum(c, lx - (0 if s < 0 else 6 * P), pt, 6 * P, .3 * P)
        alum(c, lx if s < 0 else lx - 3 * P, pt + .3 * P, 3 * P,
             top - pt - .3 * P - 3 * P)
    alum(c, lx0, top - 3 * P, 48 * P, 3 * P)
    by = pt + H_ * P / 2.0
    alum(c, lx0 + 3 * P, by, 48 * P - 6 * P, 3 * P)
    # generator
    box(c, cx - 24 * P, top, 48 * P, 33 * P, lw=.9, fill=Color(.97, .97, .97))
    tx(c, cx, top + 20 * P, "AIR-COOLED STANDBY", 5.8, "Helvetica-Bold", GREY, "c")
    tx(c, cx, top + 20 * P - 8, "GENERATOR — BY OTHERS", 5.8, "Helvetica", GREY, "c")
    tx(c, cx, top + 20 * P - 18, "48\" × 26\" × 33\" MAX", 5.8, "Helvetica", GREY, "c")

    # ground anchors at the pad midpoint, each side
    for gx in (ox + 2, ox + padw * P - 2):
        line(c, gx, oy, gx, oy - 24, 1.2)
        for i in range(3):
            c.saveState(); c.setLineWidth(.9); c.setStrokeColor(black)
            p = c.beginPath()
            p.moveTo(gx - 4.5, oy - 10 - i * 5); p.lineTo(gx + 4.5, oy - 14 - i * 5)
            c.drawPath(p, stroke=1, fill=0); c.restoreState()
    lead(c, ox + 2, oy - 20, ox + 6, oy - 38,
         ["GROUND ANCHOR AT THE PAD MIDPOINT, EACH",
          "SIDE — TYPE AND RATING BY THE E.O.R."])

    dimv(c, pt, top, lx1 + 22, "4'-0\" MAX")
    dimh(c, cx - 24 * P, cx + 24 * P, top + 33 * P + 8, "4'-0\"")


# ============================================================== S-2 details
def frame_plan(c, ox, oy):
    P = PPI * 1.35
    L, Wd = 48.0, 26.0
    box(c, ox, oy, L * P, Wd * P, lw=.9, fill=white)
    # top rails
    alum(c, ox, oy + Wd * P - 6 * P, L * P, 6 * P, lw=.7)
    alum(c, ox, oy, L * P, 6 * P, lw=.7)
    alum(c, ox, oy + 6 * P, 6 * P, Wd * P - 12 * P, lw=.7)
    alum(c, ox + L * P - 6 * P, oy + 6 * P, 6 * P, Wd * P - 12 * P, lw=.7)
    # legs below, dashed
    c.saveState(); c.setDash(3, 2); c.setLineWidth(.8)
    for lx in (ox, ox + L * P - 3 * P):
        for ly in (oy, oy + Wd * P - 3 * P):
            c.rect(lx, ly, 3 * P, 3 * P, stroke=1, fill=0)
    c.restoreState()
    # anchor pattern in the base plates
    for lx in (ox + 1.5 * P, ox + L * P - 1.5 * P):
        for ly in (oy + 1.5 * P, oy + Wd * P - 1.5 * P):
            for k in (-1.6, 0, 1.6):
                c.saveState(); c.setFillColor(black)
                c.circle(lx, ly + k * P, 1.3, stroke=0, fill=1); c.restoreState()
    dimh(c, ox, ox + L * P, oy + Wd * P + 26, "4'-0\" OUT TO OUT", ext=oy + Wd * P)
    dimh(c, ox + 1.5 * P, ox + L * P - 1.5 * P, oy + Wd * P + 13,
         "3'-9\" LEG C/L SPACING")
    dimv(c, oy, oy + Wd * P, ox - 26, "2'-2\" OUT TO OUT", ext=ox)
    dimv(c, oy + 1.5 * P, oy + Wd * P - 1.5 * P, ox - 13, "1'-11\" C/L")
    lead(c, ox + 24 * P, oy + Wd * P - 3 * P, ox + 16 * P, oy + Wd * P + 44,
         ["3\" × 6\" × ¼\" LLH ALUMINUM ANGLE TOP RAIL",
          "(6\" LEG HORIZONTAL — UNIT BEARS ON IT)"])
    lead(c, ox + 1.5 * P, oy + 1.5 * P, ox + 14 * P, oy - 34,
         ["3\" × 3\" × ¼\" ALUMINUM TUBE LEG BELOW,",
          "ON 6\" × 6\" × ¼\" BASE PLATE, 4 LOCATIONS"])


def pad_plan(c, ox, oy):
    P = PPI * 1.35
    L, Wd = 54.0, 32.0
    end = 14.0
    concrete(c, ox, oy, L * P, Wd * P, seed=41, dens=.0010)
    c.saveState(); c.setDash(2, 3); c.setLineWidth(.6)
    c.setStrokeColor(Color(.55, .55, .55))
    c.rect(ox + end * P, oy + 3 * P, (L - 2 * end) * P, Wd * P - 6 * P,
           stroke=1, fill=0)
    c.restoreState()
    tx(c, ox + L * P / 2, oy + Wd * P / 2, "EPS FOAM CORE BELOW TOP SLAB",
       5.4, "Helvetica-Oblique", GREY, "c")
    # stand footprint
    fx, fy = ox + 3 * P, oy + 3 * P
    c.saveState(); c.setDash(4, 2); c.setLineWidth(.9); c.setStrokeColor(ORANGE)
    c.rect(fx, fy, 48 * P, 26 * P, stroke=1, fill=0)
    c.restoreState()
    for bx in (fx, fx + 48 * P - 6 * P):
        for by in (fy, fy + 26 * P - 6 * P):
            box(c, bx, by, 6 * P, 6 * P, lw=.9, fill=Color(.82, .82, .84))
            for k in (-1.6, 0, 1.6):
                c.saveState(); c.setFillColor(black)
                c.circle(bx + 3 * P, by + 3 * P + k * P, 1.4, stroke=0, fill=1)
                c.restoreState()
    dimh(c, ox, ox + L * P, oy + Wd * P + 30, "4'-6\" PAD LENGTH", ext=oy + Wd * P)
    dimh(c, ox, fx, oy + Wd * P + 16, "3\"")
    dimh(c, fx + 48 * P, ox + L * P, oy + Wd * P + 16, "3\"")
    dimv(c, oy, oy + Wd * P, ox - 28, "2'-8\" PAD WIDTH", ext=ox)
    dimv(c, oy, fy, ox - 14, "3\"")
    lead(c, fx + 3 * P, fy + 3 * P, ox + 13 * P, oy - 30,
         ["6\" × 6\" × ¼\" ALUMINUM BASE PLATE, 4 LOCATIONS,",
          "EACH WITH (3) 3/8\"Ø × 2\" MIN EMBED S.S. SCREW",
          "ANCHORS AND 1¼\" O.D. WASHERS"])
    lead(c, ox + end * P, oy + Wd * P - 3 * P, ox + 30 * P, oy + Wd * P + 44,
         ["LIMIT OF SOLID CONCRETE END BAND — ALL FOUR",
          "BASE PLATES FALL INSIDE IT"])


def leg_conn(c, ox, oy):
    """Enlarged leg base plate to pad connection. Text stacks to the right in
    short lines — the connection details share one band and long callouts
    walked into the neighbouring detail the first time round."""
    P = PPI * 2.9
    S = 5.0
    concrete(c, ox, oy, 12 * P, 2 * P, seed=57, dens=.006)
    foam(c, ox, oy - 2 * P, 12 * P, 2 * P)
    box(c, ox, oy - 2 * P, 12 * P, 4 * P, lw=1.0)
    grade(c, ox - 22, ox, oy - 2 * P, label=False)
    alum(c, ox + 3 * P, oy + 2 * P, 6 * P, .3 * P)
    alum(c, ox + 4.5 * P, oy + 2.3 * P, 3 * P, 3.4 * P)
    for a in (4.5, 7.5):
        axp = ox + a * P
        line(c, axp, oy + 2.3 * P, axp, oy + .0 * P, 1.5)
        line(c, axp - .6 * P, oy + 2.4 * P, axp + .6 * P, oy + 2.4 * P, 2.0)
    tR = ox + 13.6 * P
    lead(c, ox + 6 * P, oy + 4.6 * P, tR, oy + 62,
         ["3\" × 3\" × ¼\" ALUM.", "TUBE LEG"], size=S)
    lead(c, ox + 3.6 * P, oy + 2.15 * P, tR, oy + 38,
         ["6\" × 6\" × ¼\" ALUM.", "BASE PLATE"], size=S)
    lead(c, ox + 7.5 * P, oy + 2.5 * P, tR, oy + 22,
         ["1¼\" O.D. WASHER"], size=S)
    lead(c, ox + 7.5 * P, oy + 1 * P, tR, oy + 2,
         ["3/8\"Ø × 2\" MIN EMBED S.S.", "SCREW ANCHOR, (3) PER LEG"], size=S)
    lead(c, ox + 2.0 * P, oy + 1 * P, ox + 2.6 * P, oy - 44,
         ["2\" CONCRETE TOP SLAB"], size=S)
    lead(c, ox + 6.0 * P, oy - 1 * P, ox + 6.6 * P, oy - 58,
         ["2\" EPS FOAM CORE — NO ANCHOR VALUE"], size=S)
    dimh(c, ox + 3 * P, ox + 9 * P, oy + 6.3 * P, "6\"")
    dimv(c, oy, oy + 2 * P, ox + 12 * P + 11, "2\"")
    dimh(c, ox, ox + 3 * P, oy - 30, "2½\" MIN EDGE", col=ORANGE)


def gen_conn(c, ox, oy):
    """Generator foot to top rail thru-bolt."""
    P = PPI * 2.9
    S = 5.0
    alum(c, ox, oy, 11 * P, 1.6 * P)                 # top rail, 6" leg
    box(c, ox + 1.5 * P, oy + 1.6 * P, 8 * P, 1.1 * P, lw=.9,
        fill=Color(.93, .93, .93))
    axp = ox + 5.5 * P
    line(c, axp, oy + 3.1 * P, axp, oy - 1.0 * P, 1.8)
    line(c, axp - .7 * P, oy + 2.75 * P, axp + .7 * P, oy + 2.75 * P, 2.4)
    line(c, axp - .7 * P, oy - .55 * P, axp + .7 * P, oy - .55 * P, 2.4)
    line(c, axp - .5 * P, oy - .95 * P, axp + .5 * P, oy - .95 * P, 3.0)
    tR = ox + 11.6 * P
    lead(c, axp, oy + 3.0 * P, tR, oy + 40,
         ["3/8\"Ø S.S. THRU-BOLT,", "NUT AND WASHER TOP", "AND BOTTOM — (4) TOTAL"],
         size=S)
    lead(c, ox + 3 * P, oy + 2.1 * P, tR, oy + 8,
         ["INTEGRATED MOUNTING", "FOOT OR CLIP PER THE", "UNIT MANUFACTURER"], size=S)
    lead(c, ox + 1 * P, oy + .8 * P, ox + 1.6 * P, oy - 34,
         ["3\" × 6\" × ¼\" LLH ALUMINUM TOP RAIL"], size=S)


def gusset_detail(c, ox, oy):
    P = PPI * 2.1
    S = 5.0
    alum(c, ox, oy, 3 * P, 11 * P)                   # leg
    alum(c, ox, oy + 8 * P, 13 * P, 3 * P)           # rail
    p = c.beginPath()
    p.moveTo(ox + 3 * P, oy + 8 * P)
    p.lineTo(ox + 11 * P, oy + 8 * P)
    p.lineTo(ox + 3 * P, oy + 0 * P)
    p.close()
    c.saveState(); c.setFillColor(Color(.72, .72, .75))
    c.setStrokeColor(black); c.setLineWidth(.8)
    c.drawPath(p, stroke=1, fill=1); c.restoreState()
    # weld symbol, arrow into the gusset, tail up and to the right
    ax_, ay_ = ox + 6.0 * P, oy + 3.2 * P
    hx, hy = ox + 12.6 * P, oy + 4.6 * P
    line(c, ax_, ay_, hx, hy, .6)
    line(c, hx, hy, hx + 3.4 * P, hy, .6)
    p = c.beginPath()
    p.moveTo(hx + .3 * P, hy); p.lineTo(hx + 1.3 * P, hy)
    p.lineTo(hx + .3 * P, hy + 1.0 * P); p.close()
    c.saveState(); c.setFillColor(black)
    c.drawPath(p, stroke=0, fill=1); c.restoreState()
    tx(c, hx - .4 * P, hy + .4 * P, "¼\"", 5.8, "Helvetica", black, "r")
    tx(c, hx + .3 * P, hy + 1.5 * P, "TYP. ALL AROUND", S, "Helvetica", GREY)
    dimh(c, ox + 3 * P, ox + 11 * P, oy + 11 * P + 11, "8\"")
    dimv(c, oy, oy + 8 * P, ox - 12, "8\"")
    tx(c, ox - 12, oy - 16, "8\" × 8\" × ¼\" ALUMINUM PLATE TRIANGLE, (2) AT EACH",
       S, "Helvetica")
    tx(c, ox - 12, oy - 22.6, "CORNER — ONE EACH FACE, FULL ¼\" WELD ALL AROUND",
       S, "Helvetica")


SCHED = [
    ("1", "AGS-1", "3\" × 3\" × ¼\" ALUMINUM TUBE — LEG", "4"),
    ("2", "AGS-2", "3\" × 6\" × ¼\" LLH ALUMINUM ANGLE — TOP RAIL, LONG SIDE", "2"),
    ("3", "AGS-3", "3\" × 6\" × ¼\" LLH ALUMINUM ANGLE — TOP RAIL, SHORT SIDE", "2"),
    ("4", "AGS-4", "6\" × 6\" × ¼\" ALUMINUM BASE PLATE", "4"),
    ("5", "AGS-5", "8\" × 8\" × ¼\" ALUMINUM PLATE TRIANGLE — CORNER GUSSET", "8"),
    ("6", "AGS-6", "3\" × 3\" × ¼\" ALUMINUM ANGLE — MID-HEIGHT BRACE", "4"),
    ("7", "AGS-7", "8\" × 8\" × ¼\" ALUMINUM PLATE TRIANGLE — BRACE GUSSET", "8"),
    ("8", "AGS-8", "3/8\"Ø × 2\" MIN EMBED S.S. SCREW ANCHOR, 1¼\" WASHER", "12"),
    ("9", "AGS-9", "3/8\"Ø S.S. THRU-BOLT, NUT AND WASHERS — UNIT TO STAND", "4"),
    ("10", "AGS-10", "GROUND ANCHOR AT PAD MIDPOINT — TYPE AND RATING BY E.O.R.", "2"),
]


def schedule(c, ox, oy, w):
    cols = [22, 44, w - 22 - 44 - 30, 30]
    rh = 11.5
    y = oy
    # header
    box(c, ox, y - rh, w, rh, lw=.7, fill=BAND)
    xx = ox
    for t, cw in zip(("ITEM", "MARK", "DESCRIPTION", "QTY"), cols):
        tx(c, xx + 4, y - rh + 3.6, t, 6.4, "Helvetica-Bold", GREY)
        xx += cw
    y -= rh
    for r in SCHED:
        line(c, ox, y, ox + w, y, .4, HAIR)
        xx = ox
        for v, cw in zip(r, cols):
            tx(c, xx + 4, y - rh + 3.6, v, 6.4, "Helvetica")
            xx += cw
        y -= rh
    box(c, ox, y, w, oy - y, lw=.7)
    xx = ox
    for cw in cols[:-1]:
        xx += cw
        line(c, xx, y, xx, oy, .4, HAIR)
    tx(c, ox, y - 9, "ALL ALUMINUM 6061-T6 U.N.O. QUANTITIES ARE PER STAND; "
                     "ITEMS 6 AND 7 APPLY TO STANDS OVER 3'-0\" ONLY.",
       5.7, "Helvetica-Oblique", GREY)
    return y - 20


# ============================================================== sheet frames
def sheetframe(c, sheet, title, banner=False):
    box(c, MARGIN, MARGIN, W - 2 * MARGIN, H - 2 * MARGIN, lw=2.6, stroke=ORANGE)
    A.titleblock(c, W, H, sheet, title, margin=MARGIN, tbw=TBW, stamp=170,
                 licences=LIC, seal_label="ENGINEER OF RECORD — SEAL")
    try:
        c.drawImage("aoglogo.jpeg", XL, H - MARGIN - 40, width=96, height=26,
                    preserveAspectRatio=True, anchor="sw", mask="auto")
    except Exception:
        tx(c, XL, H - MARGIN - 32, "ALWAYS ON GENERATORS", 13, "Helvetica-Bold")
    tx(c, XL + 108, H - MARGIN - 22, title, 12.5, "Helvetica-Bold")
    tx(c, XL + 108, H - MARGIN - 33,
       "AOG STANDARD DETAIL — ISSUED FOR ENGINEERING REVIEW", 7.0, "Helvetica", GREY)
    line(c, XL, H - MARGIN - 46, XR, H - MARGIN - 46, 1.0, ORANGE)
    A.footer_note(c, XL, MARGIN + 8, XR - XL)
    tx(c, XR, MARGIN + 8, "AOG SHEET GENERATOR s10_padstand.py · %s" % A.DATE_SHORT,
       6.2, "Helvetica-Oblique", GREY, "r")


def review_box(c, x, y, w):
    h = 50
    box(c, x, y - h, w, h, lw=1.2, stroke=ORANGE, fill=Color(.995, .965, .94))
    tx(c, x + 8, y - 14, "ISSUED FOR ENGINEERING REVIEW", 7.6,
       "Helvetica-Bold", ORANGE)
    yy = y - 24
    for ln in wrap("This sheet is unsealed. It is not valid for permit or for "
                   "construction until it is signed and sealed by the engineer "
                   "of record, who determines every capacity shown or implied.",
                   int((w - 16) / 3.05)):
        tx(c, x + 8, yy, ln, 6.0, "Helvetica")
        yy -= 7.2
    return y - h - 10


# ================================================================== S-1 page
def page1(c):
    sheetframe(c, "S-1", "STAND ELEVATIONS, PAD SECTION & DESIGN CRITERIA")

    # ---------- elevations, top row
    gy = 470
    stand_elev(c, XL + 40, gy, 30, front=False, brace=False)
    dtitle(c, XL + 30, 392, 1, "STAND ELEVATION — LONG SIDE",
           "ELEV", "S-1", "1'-0\" TO 3'-0\" STAND HEIGHT")
    stand_elev(c, XL + 260, gy, 48, front=False, brace=True)
    dtitle(c, XL + 250, 392, 2, "STAND ELEVATION — LONG SIDE",
           "ELEV", "S-1", "3'-0\" TO 4'-0\" STAND HEIGHT")
    stand_elev(c, XL + 490, gy, 48, front=True, brace=True)
    dtitle(c, XL + 470, 392, 3, "STAND ELEVATION — SHORT SIDE",
           "ELEV", "S-1", "3'-0\" TO 4'-0\" STAND HEIGHT")

    # ---------- pad section, bottom left
    pad_section(c, XL + 50, 200)
    dtitle(c, XL + 20, 120, 4, "PRECAST FOAM-CORE PAD — SECTION",
           "SECTION", "S-1", "NOT TO SCALE")

    # ---------- whole assembly, bottom right
    assembly_elev(c, XL + 550, 200)
    dtitle(c, XL + 520, 120, 5, "SYSTEM ASSEMBLY AT MAXIMUM HEIGHT",
           "ELEV", "S-1", "NOT TO SCALE")

    # ---------- notes column
    y = review_box(c, NOTEX, H - MARGIN - 56, NOTEW)

    y = sechead(c, NOTEX, y, "DESIGN CRITERIA",
                "AOG's intent — to be confirmed or reset by the E.O.R.", NOTEW)
    crit = [
        ("GOVERNING CODE", "%s, %s" % (A.FBC_ABBR, A.ASCE7_EDITION)),
        ("RISK CATEGORY", "II"),
        ("ULT. WIND SPEED", "170–175 MPH (BY SITE)"),
        ("EXPOSURE", "C OR D (BY SITE)"),
        ("STAND HEIGHT", "1'-0\" MIN TO 4'-0\" MAX"),
        ("MID-HEIGHT BRACE", "REQUIRED OVER 3'-0\""),
        ("ALUMINUM", "6061-T6, ¼\" MIN THICKNESS"),
        ("CONCRETE (PAD)", "3,000 PSI MIN AT 28 DAYS"),
        ("PAD WEIGHT", "362 LB MIN"),
        ("UNIT ENVELOPE", "48\" × 26\" × 33\" MAX"),
        ("SUBGRADE", "COMPACTED — VALUE BY E.O.R."),
    ]
    for i, (k, v) in enumerate(crit):
        if i % 2 == 0:
            box(c, NOTEX, y - 2.6, NOTEW, 10.2, lw=0, fill=BAND, stroke=None)
        tx(c, NOTEX + 2, y, k, 6.0, "Helvetica-Bold")
        tx(c, NOTEX + NOTEW - 2, y, v, 6.0, "Helvetica", black, "r")
        y -= 10.2
    y -= 10

    y = notes(c, NOTEX, y, NOTEW,
              "OPEN ITEMS FOR THE ENGINEER OF RECORD",
              "What this markup does not answer.",
              [
                  "Design wind pressure at the site, and the resulting uplift, "
                  "shear and overturning at the four leg base plates.",
                  "Capacity of a 3/8\"Ø × 2\" embed anchor into the pad's 2\" "
                  "concrete top slab. AOG's sealed slab-on-grade stand detail "
                  "uses 5/16\" × 4¾\" anchors at full embed, which a 4\" precast "
                  "pad cannot accept — confirm the short anchor or direct "
                  "another connection.",
                  "Whether all four base plates must land on the solid concrete "
                  "end bands, as drawn in 4/S-1 and 2/S-2, and the edge distance "
                  "that governs.",
                  "Sliding and overturning of the pad itself at 4'-0\", and the "
                  "uplift rating, type and count of ground anchor needed.",
                  "The maximum stand height permitted on this pad, and the height "
                  "at which the mid-height brace becomes mandatory.",
                  "Maximum and minimum generator weight for the system, and "
                  "whether the unit's four factory mounting holes develop the "
                  "uplift.",
              ])

    y = notes(c, NOTEX, y, NOTEW, "BASIS OF THIS MARKUP", None,
              [
                  "Stand geometry, gussets, base plates and welds follow the AOG "
                  "aluminum stand as fabricated and as detailed in the AMG "
                  "Structural Engineering air-cooled master set, which is sealed "
                  "for the stand on a cast-in-place slab and stops at 4'-0\".",
                  "The pad is the precast foam-core pad AOG buys and sets, 54\" × "
                  "32\" × 4\".",
                  "A precast pad is a different host from the cast slab the stand "
                  "was sealed against. That combination is what is being "
                  "submitted here for review; no sealed set in AOG's files "
                  "already covers it.",
              ], num=False, bullet="—")

    y = sechead(c, NOTEX, y - 2, "STAND HEIGHT & CONFIGURATION",
                "Clear height from the top of the pad to the top of the frame.",
                NOTEW)
    rows = [("1'-0\" TO 3'-0\"", "NOT REQUIRED", "1/S-1"),
            ("3'-0\" TO 4'-0\"", "REQUIRED AT MID-HEIGHT", "2, 3/S-1"),
            ("OVER 4'-0\"", "NOT COVERED BY THIS SHEET", "—")]
    cw = (78, NOTEW - 78 - 52, 52)
    rh = 11.5
    box(c, NOTEX, y - rh, NOTEW, rh, lw=.7, fill=BAND)
    xx = NOTEX
    for t, w_ in zip(("STAND HEIGHT", "MID-HEIGHT BRACE", "DETAIL"), cw):
        tx(c, xx + 3, y - rh + 3.6, t, 6.0, "Helvetica-Bold", GREY)
        xx += w_
    yy = y - rh
    for r in rows:
        line(c, NOTEX, yy, NOTEX + NOTEW, yy, .4, HAIR)
        xx = NOTEX
        for v, w_ in zip(r, cw):
            tx(c, xx + 3, yy - rh + 3.6, v, 6.0, "Helvetica")
            xx += w_
        yy -= rh
    box(c, NOTEX, yy, NOTEW, y - yy, lw=.7)
    xx = NOTEX
    for w_ in cw[:-1]:
        xx += w_
        line(c, xx, yy, xx, y, .4, HAIR)

    c.showPage()


# ================================================================== S-2 page
def page2(c):
    sheetframe(c, "S-2", "PLANS, CONNECTIONS & PART SCHEDULE")

    frame_plan(c, XL + 70, 545)
    dtitle(c, XL + 20, 486, 1, "STAND FRAME PLAN", "PLAN", "S-2", "NOT TO SCALE")

    pad_plan(c, XL + 390, 537)
    dtitle(c, XL + 350, 486, 2, "PAD PLAN WITH STAND FOOTPRINT",
           "PLAN", "S-2", "NOT TO SCALE")

    leg_conn(c, XL + 40, 392)
    dtitle(c, XL + 20, 300, 3, "LEG BASE PLATE TO PAD", "DETAIL", "S-2",
           "NOT TO SCALE")

    gen_conn(c, XL + 270, 382)
    dtitle(c, XL + 250, 300, 4, "GENERATOR UNIT TO STAND", "DETAIL", "S-2",
           "NOT TO SCALE")

    gusset_detail(c, XL + 510, 366)
    dtitle(c, XL + 480, 300, 5, "CORNER GUSSET & WELD", "DETAIL", "S-2",
           "NOT TO SCALE")

    y = sechead(c, XL + 20, 262, "PART SCHEDULE", None, 430)
    schedule(c, XL + 20, y, 430)

    notes(c, XL + 480, 262, 200, "INSTALLATION", "What the crew does on site.", [
        "Set the pad on compacted, level bearing. Shim with concrete or "
        "compacted fill, never with wood or plastic.",
        "Locate the stand on the pad per 2/S-2 and check that all four base "
        "plates land on the solid concrete end bands before drilling.",
        "Drill and set the anchors per the anchor manufacturer's instructions. "
        "An anchor that spins or will not seat gets relocated inside the same "
        "band, not re-used.",
        "Coat any aluminum that will bear on concrete before the leg is set.",
        "Bolt the unit down through all four factory mounting holes. Do not "
        "substitute the count.",
        "A condition in the field that does not match this sheet stops work and "
        "goes back to the engineer of record.",
    ], size=5.6, lead_=6.9)

    # ---------- notes column
    y = H - MARGIN - 60
    y = notes(c, NOTEX, y, NOTEW, "STRUCTURAL ALUMINUM", None, [
        "All structural aluminum is 6061-T6 or better, ¼\" minimum thickness "
        "unless noted otherwise.",
        "Fabricate and erect in accordance with the Aluminum Design Manual, "
        "Specifications and Guidelines for Aluminum Structures.",
        "Aluminum in contact with concrete, masonry, steel or pressure-treated "
        "lumber is coated first — one coat of zinc molybdate primer or an alkali "
        "resistant bituminous paint — and the coating carries to 12\" above any "
        "concrete surface.",
        "Isolate aluminum from dissimilar metals. Non-reactive washers may "
        "separate stainless fasteners from aluminum where the E.O.R. accepts them.",
    ])

    y = notes(c, NOTEX, y, NOTEW, "WELDING", None, [
        "Weld to AWS D1.2, Structural Welding Code — Aluminum. Minimum weld "
        "size ¼\" unless noted otherwise.",
        "Corner gussets take a full ¼\" groove or fillet weld all around, both "
        "plates at every corner.",
        "Filler alloy per the Aluminum Design Manual for 6061-T6 base metal.",
    ])

    y = notes(c, NOTEX, y, NOTEW, "FASTENERS & ANCHORS", None, [
        "All fasteners, nuts and washers are 304 stainless steel.",
        "Anchors are installed per the anchor manufacturer's published "
        "instructions, into sound concrete only — not through stucco, foam or "
        "any other finish, and not into the pad's EPS core.",
        "Anchor edge distance and spacing are as drawn, or as the anchor "
        "manufacturer requires where that is greater.",
        "Drill bolt holes no more than 1/16\" over the nominal bolt diameter.",
    ])

    y = notes(c, NOTEX, y, NOTEW, "GENERAL", None, [
        "Do not scale these drawings. Dimensions govern.",
        "The generator unit, its mounting feet and its factory mounting holes "
        "are the unit manufacturer's, and the unit is set per their "
        "installation instructions.",
        "Electrical and gas work is by separate submittal and is not part of "
        "this sheet.",
        "Any change to the members, the connections or the stand height shown "
        "here goes back to the engineer of record before it is built.",
    ])

    y = sechead(c, NOTEX, y - 4, "REVISIONS", None, NOTEW)
    rh = 12.0
    hdrs = (("No.", 24), ("DATE", 58), ("DESCRIPTION", NOTEW - 24 - 58))
    box(c, NOTEX, y - rh, NOTEW, rh, lw=.7, fill=BAND)
    xx = NOTEX
    for t, cw in hdrs:
        tx(c, xx + 3, y - rh + 3.8, t, 6.0, "Helvetica-Bold", GREY)
        xx += cw
    yy = y - rh
    for i in range(4):
        line(c, NOTEX, yy, NOTEX + NOTEW, yy, .4, HAIR)
        if i == 0:
            tx(c, NOTEX + 3, yy - rh + 3.8, "0", 6.0, "Helvetica")
            tx(c, NOTEX + 27, yy - rh + 3.8, A.DATE_SHORT, 6.0, "Helvetica")
            tx(c, NOTEX + 85, yy - rh + 3.8, "ISSUED FOR ENGINEERING REVIEW",
               6.0, "Helvetica")
        yy -= rh
    box(c, NOTEX, yy, NOTEW, y - yy, lw=.7)
    xx = NOTEX
    for _, cw in hdrs[:-1]:
        xx += cw
        line(c, xx, yy, xx, y, .4, HAIR)

    review_box(c, NOTEX, yy - 12, NOTEW)

    c.showPage()


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "AOG Stand on Precast Pad - IN HOUSE MARKUP.pdf")
    c = canvas.Canvas(path, pagesize=(W, H))
    c.setTitle("AOG Elevated Aluminum Generator Stand on Precast Pad — "
               "In-House Markup")
    page1(c)
    page2(c)
    c.save()
    print("wrote", path)


if __name__ == "__main__":
    main()
