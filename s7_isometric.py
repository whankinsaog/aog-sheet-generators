#!/usr/bin/env python3
# =============================================================================
# G-1 GAS PIPING ISOMETRIC - reusable sheet generator
# First built on 112 1st Ave N, Naples FL (Sept 2026).  Reviewed line by line
# by Brandon on that job; this layout is the approved one.
#
# THIS COPY IS POPULATED FOR:  1264 WHITEHEART AVE, MARCO ISLAND  (Sept 2026)
#   1,000 gal U.G. LP tank -> 26 kW air-cooled generator, tankless W.H.,
#   pool heater, and an interior attic CSST run to cooktop + dryer.
#
#   mkdir -p out && python3 s7_isometric.py
#       -> out/gas_iso.svg, out/gas_iso.pdf, out/gas_iso.png
#
# ------------------------------------------------------------- HOW THIS DIFFERS
# This is the one sheet in the folder that is NOT reportlab.  A true 30 deg
# isometric is written as SVG by hand and rasterised by cairosvg:
#
#       pip install cairosvg
#
# It is 17x11 (half of the 36x24 sheets, prints legibly on 11x17) and
# monochrome - no AOG orange.
#
# ---------------------------------------------------------------- PER-JOB EDITS
#   JOB IDENTITY   ADDR / LEGAL / SHEET_DATE at the top of this file.
#   TITLE BLOCK    subtitle line -> tank size + kW
#   LOAD SCHEDULE  one row per appliance + the generator, then the total
#   PIPE SCHEDULE  one row per segment; letters match the seg_bub() tags
#   SIZING NOTE    recompute with the NFPA 54 equations, do not reuse a number
#   GENERAL NOTES  renumbering the list means renumbering every note_bub()
#   GEOMETRY       ST stations along the buried main, BH house-branch offset,
#                  ZP / ZR / ZA buried depth / riser top / attic run level
#
# ------------------------------------------------------------------ CONVENTIONS
#   * Equipment boxes are drawn BEFORE their piping.
#   * Grade patches are drawn first so piping crosses over them.
#   * Riser stack bottom-up: anodeless transition (below grade), shutoff,
#     2nd stage regulator, appliance shutoff, sediment trap, connector.
#   * No text over linework; keyed bubbles with short leaders instead.
# =============================================================================
import math
import os
import re

# ------------------------------------------------------------- job identity
ADDR = "1264 WHITEHEART AVENUE, MARCO ISLAND, FL 34145"
LEGAL = "LOT 41, BLOCK 206, MARCO BEACH UNIT 7"
COUNTY = "COLLIER COUNTY, FLORIDA"
SHEET_DATE = None                                  # None -> aoglib DATE_SHORT
SHEET_NO = "G-1"

if ADDR is None or SHEET_DATE is None:
    try:                                           # share the package date
        from aoglib import DATE_SHORT as _DS, JOB as _J
        ADDR = ADDR or "%s  %s" % (_J["addr"], _J["city"])
        SHEET_DATE = SHEET_DATE or _DS.replace("-", "/")
    except Exception:                              # runs standalone too
        import datetime as _dt
        _o = os.environ.get("AOG_JOB_DATE")
        _d = _dt.date.fromisoformat(_o) if _o else _dt.date.today()
        SHEET_DATE = SHEET_DATE or _d.strftime("%m/%d/%Y")
        ADDR = ADDR or "SET ADDR AT TOP OF s7_isometric.py"

W, H = 1700, 1100
S = 8.2
COS30 = math.cos(math.radians(30))
K = COS30 * S          # horizontal px per unit
L = 0.5 * S            # vertical px per unit (horizontal axes)
Z = S                  # vertical px per unit (z axis)
OX, OY = 250, 500

out = []
def add(s): out.append(s)

def P(u, v, z=0.0):
    return (OX + (u + v) * K, OY + (u - v) * L - z * Z)

def path(pts, w=1.0, dash=None, col="#000", cap="round"):
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" '
        f'stroke-linecap="{cap}" stroke-linejoin="round"{ds}/>')

def line(a, b, w=1.0, dash=None, col="#000"):
    path([a, b], w, dash, col)

FAM = "DejaVu Sans Condensed, Arial Narrow, Helvetica, sans-serif"
def txt(x, y, s, size=10, anchor="start", w="normal", col="#000", ls=0.4):
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FAM}" font-size="{size}" '
        f'font-weight="{w}" fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')

def rect(x, y, w_, h_, sw=1.0, fill="none", col="#000"):
    add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w_:.1f}" height="{h_:.1f}" '
        f'fill="{fill}" stroke="{col}" stroke-width="{sw}"/>')

def circ(x, y, r, sw=1.0, fill="none", col="#000"):
    add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{col}" stroke-width="{sw}"/>')

def poly(pts, sw=1.0, fill="none", col="#000"):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    add(f'<polygon points="{p}" fill="{fill}" stroke="{col}" stroke-width="{sw}"/>')

LW_NEW, LW_CSST, LW_EX, LW_OBJ, LW_LEAD = 3.1, 2.7, 1.7, 1.4, 0.8
GRAY, LT = "#5a5a5a", "#909090"
VALVE = "#c70d17"      # shutoff valves in red, 2nd stage regulators in blue -
REG2  = "#0d52a8"      # both at Brandon's direction.  The 1st stage stays black.

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add(f'<rect width="{W}" height="{H}" fill="#fff"/>')

# -------------------------------------------------------------- sheet + titles
rect(14, 14, W - 28, H - 28, 2.2)
rect(20, 20, W - 40, H - 40, 0.9)
RX = 1268
line((RX, 20), (RX, H - 20), 1.6)

txt(46, 60, "GAS PIPING ISOMETRIC", 27, w="bold", ls=1.2)
txt(46, 80, "PROPOSED 1,000 GAL. UNDERGROUND LP TANK &amp; 26 kW STANDBY GENERATOR", 12.5, ls=0.7)
line((46, 89), (880, 89), 1.2)
txt(46, 106, "%s   &#183;   %s   &#183;   %s" % (ADDR, LEGAL, COUNTY), 10.6, col=GRAY)
txt(1252, 60, "NOT TO SCALE", 12, anchor="end", w="bold")
txt(1252, 77, "DIAGRAMMATIC &#8212; SEE SITE PLAN FOR ACTUAL ROUTING", 9.2, anchor="end", col=GRAY)

# -------------------------------------------------------------------- symbols
def dirv(u, v, z=0.0):
    dx = (u + v) * K
    dy = (u - v) * L - z * Z
    m = math.hypot(dx, dy) or 1
    return (dx / m, dy / m)

DU, DV, DZ = dirv(1, 0), dirv(0, 1), (0.0, -1.0)
def perp(d): return (-d[1], d[0])

def ball_valve(pt, d, size=7.0, col=None):
    col = col or VALVE
    px, py = perp(d)
    a = (pt[0] - d[0] * size, pt[1] - d[1] * size)
    b = (pt[0] + d[0] * size, pt[1] + d[1] * size)
    h = size * 0.70
    poly([a, (a[0] + px * h, a[1] + py * h), (a[0] - px * h, a[1] - py * h)], 1.1, fill=col, col=col)
    poly([b, (b[0] + px * h, b[1] + py * h), (b[0] - px * h, b[1] - py * h)], 1.1, fill=col, col=col)
    st = (pt[0] + px * size * 1.55, pt[1] + py * size * 1.55)
    line(pt, st, 1.3, col=col)
    line((st[0] - d[0] * 4.6, st[1] - d[1] * 4.6), (st[0] + d[0] * 4.6, st[1] + d[1] * 4.6), 1.7, col=col)

def regulator(pt, d, size=7.4, col="#000"):
    px, py = perp(d)
    bw, bh = size, size * 0.60
    c = [(pt[0] - d[0]*bw - px*bh, pt[1] - d[1]*bw - py*bh),
         (pt[0] + d[0]*bw - px*bh, pt[1] + d[1]*bw - py*bh),
         (pt[0] + d[0]*bw + px*bh, pt[1] + d[1]*bw + py*bh),
         (pt[0] - d[0]*bw + px*bh, pt[1] - d[1]*bw + py*bh)]
    poly(c, 1.25, fill="#fff", col=col)
    dm = (pt[0] + px * (bh + 4.8), pt[1] + py * (bh + 4.8))
    circ(dm[0], dm[1], 5.9, 1.25, fill="#fff", col=col)
    line((dm[0] - d[0]*3.2, dm[1] - d[1]*3.2), (dm[0] + d[0]*3.2, dm[1] + d[1]*3.2), 0.9, col=col)
    vt = (dm[0] + px * 5.9, dm[1] + py * 5.9)
    line(vt, (vt[0] + px * 4.6 + d[0] * 3.6, vt[1] + py * 4.6 + d[1] * 3.6), 1.0, col=col)

def sed_trap(pt, size=12):
    b = (pt[0], pt[1] + size)
    line(pt, b, 2.1)
    line((b[0] - 4.3, b[1]), (b[0] + 4.3, b[1]), 2.3)

def flexline(a, b, n=5, amp=3.2):
    dx, dy = b[0] - a[0], b[1] - a[1]
    Ln = math.hypot(dx, dy) or 1
    px, py = -dy / Ln, dx / Ln
    pts = [a]
    for i in range(1, n * 2):
        t = i / (n * 2)
        s = amp if i % 2 else -amp
        pts.append((a[0] + dx * t + px * s, a[1] + dy * t + py * s))
    pts.append(b)
    path(pts, 1.7)

def tee(pt, r=3.3):
    circ(pt[0], pt[1], r, 0, fill="#000")

def iso_box(u, v, z, du, dv, dz, sw=LW_OBJ):
    p000, p100 = P(u, v, z), P(u + du, v, z)
    p010 = P(u, v + dv, z)
    q000, q100 = P(u, v, z + dz), P(u + du, v, z + dz)
    q110, q010 = P(u + du, v + dv, z + dz), P(u, v + dv, z + dz)
    poly([q000, q100, q110, q010], sw, fill="#f4f4f4")
    poly([p000, p100, q100, q000], sw, fill="#e6e6e6")
    poly([p000, p010, q010, q000], sw, fill="#efefef")
    return dict(q=[q000, q100, q110, q010], p=[p000, p100, p010])

def grade_patch(u, v, r=3.4, ticks=7):
    a, b = P(u - r, v - r), P(u + r, v - r)
    c, d = P(u + r, v + r), P(u - r, v + r)
    poly([a, b, c, d], 0.85, fill="#f2f2f2", col=LT)
    for i in range(ticks + 1):
        t = i / ticks
        x = a[0] + (d[0] - a[0]) * t; y = a[1] + (d[1] - a[1]) * t
        line((x, y), (x - 4.2, y + 6.4), 0.6, col=LT)

def leader(frm, to, dot=True, col="#000"):
    path([frm, to], LW_LEAD, col=col)
    if dot: circ(frm[0], frm[1], 1.9, 0, fill=col)

def block(x, y, lines, size=9.4, lead=11.4, anchor="start"):
    for i, (s, sty) in enumerate(lines):
        w = "bold" if sty == "b" else "normal"
        c = "#000" if sty in ("b", "n") else GRAY
        txt(x, y + i * lead, s, size if sty != "s" else size - 0.7, anchor=anchor, w=w, col=c)

# ------------------------------------------------------------------- geometry
ZP, ZR, ZA = -4.0, 13.0, 25.0
ST = dict(start=0.0, teeH=22.0, gen=30.0, wh=58.0, ph=78.0)
BH = 20.0                                  # house branch leaves main, far side
CT_U, DR_U = 62.0, 78.0                    # cooktop / dryer stations, attic run

# grade patches first so piping draws over them
for (gu_, gv_, rr_) in [(-14.0, 12.0, 3.4), (ST["teeH"], BH, 2.8),
                        (ST["gen"], 0, 2.8), (ST["wh"], 0, 2.8),
                        (ST["ph"], 0, 2.8), (14.0, 0, 2.6)]:
    grade_patch(gu_, gv_, rr_, 6)

# buried main
A0, A1 = P(ST["start"], 0, ZP), P(ST["ph"], 0, ZP)
line(A0, A1, LW_NEW)

# ============================================================== 1000 GAL TANK
tv, tz = 12.0, -9.6
tu0, tu1 = -21.0, -6.5
RT = 14.0
c0, c1 = P(tu0, tv, tz), P(tu1, tv, tz)
pxp, pyp = perp(DU)
ox_, oy_ = pxp * RT * 1.9, pyp * RT * 1.9
poly([(c0[0] + ox_, c0[1] + oy_), (c1[0] + ox_, c1[1] + oy_),
      (c1[0] - ox_, c1[1] - oy_), (c0[0] - ox_, c0[1] - oy_)], LW_OBJ, fill="#f7f7f7")
ang = math.degrees(math.atan2(pyp, pxp)) - 90
for c, fl in ((c1, "#fdfdfd"), (c0, "#f0f0f0")):
    add(f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="{RT*0.56:.1f}" ry="{RT*1.9:.1f}" '
        f'transform="rotate({ang:.1f} {c[0]:.1f} {c[1]:.1f})" fill="{fl}" stroke="#000" '
        f'stroke-width="{LW_OBJ}"/>')

def crown(u):
    p = P(u, tv, tz)
    return (p[0] - ox_, p[1] - oy_)
def belly(u):
    p = P(u, tv, tz)
    return (p[0] + ox_, p[1] + oy_)

# tie-down straps + anchor plates
for su in (tu0 + 3.0, tu0 + 8.0):
    cr, bl = crown(su), belly(su)
    path([cr, bl], 1.2, dash="6,3", col=GRAY)
    ap_ = (bl[0], bl[1] + 30)
    path([bl, ap_], 1.2, dash="6,3", col=GRAY)
    line((ap_[0] - 7, ap_[1]), (ap_[0] + 7, ap_[1]), 2.4)

# dome + 1st stage regulator
dcx = -14.0
dbot, dtop = crown(dcx), P(dcx, tv, 0.4)
line((dbot[0] - 13, dbot[1] + 2), (dtop[0] - 13, dtop[1]), LW_OBJ)
line((dbot[0] + 13, dbot[1] + 2), (dtop[0] + 13, dtop[1]), LW_OBJ)
add(f'<ellipse cx="{dtop[0]:.1f}" cy="{dtop[1]:.1f}" rx="13.5" ry="6.4" fill="#fff" '
    f'stroke="#000" stroke-width="{LW_OBJ}"/>')
regulator((dtop[0] + 1, dtop[1] - 13), DU, 7.4)

# anode on tank end
an = (c0[0] - 27, c0[1] + 10)
circ(an[0], an[1], 5.0, 1.2, fill="#fff")
txt(an[0], an[1] + 3.4, "A", 8.2, anchor="middle", w="bold")
line((an[0] + 5, an[1] - 2), (c0[0] - 9, c0[1] + 4), 1.1)

# tank outlet -> buried main
o1, o2 = crown(tu1), P(tu1, tv, ZP)
line((o1[0], o1[1]), o2, LW_NEW)
line(o2, A0, LW_NEW)
bvp = ((o2[0] + A0[0]) / 2, (o2[1] + A0[1]) / 2)
ball_valve(bvp, DU, 7.0)

cr_ = crown(tu1)
leader((cr_[0], cr_[1]), (296, 381))
block(300, 371, [
    ("1,000 GAL. ASME LP TANK (NEW)", "b"),
    ("BURIED, AG/UG STYLE", "s"),
    ("1st STAGE REGULATOR AT DOME, 10 PSI OUTLET", "s"),
    ("Mg ANODE &#183; TIE-DOWN AUGERS &#183; SEE NOTES 3 &amp; 4", "s"),
])

# ====================================================== APPLIANCE RISERS (MAIN)
def appl(u, name, lab, sub, lx, ly, du=7, dv=6, dz=13, bv=-12):
    bot, top = P(u, 0, ZP), P(u, 0, ZR)
    b = iso_box(u - du / 2, bv, ZR - 1.0, du, dv, dz)     # box first
    line(bot, top, LW_NEW)
    tee(bot)
    regulator((top[0], top[1] + 34), DZ, 7.4, REG2)
    ball_valve((top[0], top[1] + 58), DZ, 7.0)
    end = P(u, bv + dv, ZR)
    line(top, end, LW_NEW)
    # no second shutoff here: the valve upstream of the 2nd stage regulator on this
    # riser is itself within 6'-0" of the appliance and serves as its shutoff.
    sed_trap((end[0] + 6, end[1] + 1))
    cx = (b["q"][0][0] + b["q"][2][0]) / 2
    cy = (b["q"][0][1] + b["q"][2][1]) / 2
    txt(cx, cy + 3.4, name, 9.0, anchor="middle", w="bold")
    leader((cx - 4, cy + dz * Z * 0.30), (lx + 8, ly - 9))
    block(lx, ly, [(lab, "b"), (sub, "s")])
    return b

whb = appl(ST["wh"], "W.H.", "TANKLESS WATER HEATER", "200,000 BTU/HR", 530, 872)
phb = appl(ST["ph"], "POOL HTR", "POOL HEATER", "400,000 BTU/HR", 790, 960)

# ================================================================= GENERATOR
gu = ST["gen"]
iso_box(gu - 6.0, -26, 0.0, 12, 12, 1.6)              # pad drawn first
gb = iso_box(gu - 5.0, -24.5, 1.6, 10, 9, 7)          # generator drawn first
gcx = (gb["q"][0][0] + gb["q"][2][0]) / 2
gcy = (gb["q"][0][1] + gb["q"][2][1]) / 2
g0, gt = P(gu, 0, ZP), P(gu, 0, 3.4)
line(g0, gt, LW_NEW); tee(g0)
regulator((gt[0], gt[1] + 26), DZ, 7.6, REG2)
ball_valve((gt[0], gt[1] + 46), DZ, 7.2)
gl = P(gu, -12.5, 3.4)
line(gt, gl, LW_NEW)
ball_valve(P(gu, -5.0, 3.4), DV, 6.6)                 # appliance shutoff, <6'
sed_trap((gl[0] - 5, gl[1] + 2))
flexline(gl, P(gu, -15.5, 3.4), 4, 2.8)
txt(gcx - 6, gcy + 2, "26 kW", 11, anchor="middle", w="bold")
txt(gcx - 6, gcy + 14, "GENERATOR", 8.2, anchor="middle")
leader((gcx - 40, gcy + 26), (140, 852))
block(52, 862, [
    ("NEW GENERAC 26 kW AIR-COOLED", "b"),
    ("STANDBY GENERATOR &#8212; LP VAPOR", "b"),
    ("361,000 BTU/HR INPUT", "b"),
    ("ON ENGINEERED PRE-CAST PAD, 48&quot; &#215; 26&quot;", "s"),
    ("PAD SET NOT LESS THAN EL. 9.0 (N.A.V.D. 88)", "s"),
    ("18&quot; MIN. FROM STRUCTURE (SwRI-LISTED) &#183; 5'-0&quot;", "s"),
    ("MIN. FROM ANY OPENING &#183; 4'-0&quot; FROM LOT LINE", "s"),
])

# ============================================== HOUSE BRANCH / INTERIOR CSST
hu = ST["teeH"]
h0, h1 = P(hu, 0, ZP), P(hu, BH, ZP)
line(h0, h1, LW_NEW); tee(h0)
ht = P(hu, BH, ZR)                                    # anodeless riser top
line(h1, ht, LW_NEW)
ball_valve((ht[0], ht[1] + 58), DZ, 7.0)              # shutoff below regulator
regulator((ht[0], ht[1] + 34), DZ, 7.4, REG2)
ha = P(hu, BH, ZA)                                    # up into the attic
line(ht, ha, LW_NEW)

ct_top = P(CT_U, BH, ZA)
dr_top = P(DR_U, BH, ZA)
path([ha, ct_top, dr_top], LW_CSST, dash="11,3.5,2.5,3.5")

# cooktop: box first, then the drop and the horizontal into its face
ctb = iso_box(CT_U - 3.5, BH - 9.0, ZA - 11.0, 7, 6, 7)
ct_dn = P(CT_U, BH, ZA - 7.0)
line(ct_top, ct_dn, LW_NEW)
ct_end = P(CT_U, BH - 3.0, ZA - 7.0)
line(ct_dn, ct_end, LW_NEW)
ball_valve(P(CT_U, BH - 1.1, ZA - 7.0), DV, 6.4)      # appliance shutoff, <6'
sed_trap((ct_end[0] + 6, ct_end[1] + 1))
ccx = (ctb["q"][0][0] + ctb["q"][2][0]) / 2
ccy = (ctb["q"][0][1] + ctb["q"][2][1]) / 2
txt(ccx, ccy + 3.4, "RANGE", 8.6, anchor="middle", w="bold")
leader((ccx - 26, ccy + 6), (772, 478))
block(678, 462, [("RANGE", "b"), ("35,000 BTU/HR", "s")])

# dryer: box first, then the drop and the horizontal into its face
drb = iso_box(DR_U - 3.5, BH - 9.0, ZA - 15.0, 7, 6, 7)
dr_dn = P(DR_U, BH, ZA - 11.0)
line(dr_top, dr_dn, LW_NEW)
dr_end = P(DR_U, BH - 3.0, ZA - 11.0)
line(dr_dn, dr_end, LW_NEW)
ball_valve(P(DR_U, BH - 1.1, ZA - 11.0), DV, 6.4)     # appliance shutoff, <6'
sed_trap((dr_end[0] + 6, dr_end[1] + 1))
dcx_ = (drb["q"][0][0] + drb["q"][2][0]) / 2
dcy_ = (drb["q"][0][1] + drb["q"][2][1]) / 2
txt(dcx_, dcy_ + 3.4, "DRYER", 8.6, anchor="middle", w="bold")
leader((dcx_ + 20, dcy_ + 26), (1012, 646))
block(1017, 642, [("DRYER", "b"), ("30,000 BTU/HR", "s")])

txt(624, 250, "INTERIOR / ATTIC RUN &#8212; CSST", 9.4, w="bold")
txt(624, 263, "ABOVE CEILING, WITHIN THE RESIDENCE", 8.2, col=GRAY)

# ================================================ SEGMENT + NOTE BUBBLES
def seg_bub(anchor, bx, by, letter, r=10.5):
    path([anchor, (bx, by)], LW_LEAD)
    circ(anchor[0], anchor[1], 1.9, 0, fill="#000")
    circ(bx, by, r, 1.5, fill="#fff")
    txt(bx, by + 3.6, letter, 11, anchor="middle", w="bold")

def hexa(cx, cy, r=11.0):
    pts = [(cx + r * math.cos(math.radians(60 * i - 30)),
            cy + r * math.sin(math.radians(60 * i - 30))) for i in range(6)]
    poly(pts, 1.4, fill="#fff")

def note_bub(anchor, bx, by, num, r=11.0):
    path([anchor, (bx, by)], LW_LEAD)
    circ(anchor[0], anchor[1], 1.9, 0, fill="#000")
    hexa(bx, by, r)
    txt(bx, by + 3.4, num, 10, anchor="middle", w="bold")

mid = lambda a_, b_: ((a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2)

# pipe segment tags (see PIPE SIZING SCHEDULE)
seg_bub(P(12, 0, ZP), 300, 540, "A")
seg_bub(mid(h0, h1), 470, 668, "B")
seg_bub(mid(ht, ha), 598, 364, "C")
seg_bub(mid(ha, ct_top), 688, 340, "D")
seg_bub(mid(ct_dn, ct_end), 905, 547, "E")
seg_bub(mid(ct_top, dr_top), 920, 436, "F")
seg_bub(mid(dr_dn, dr_end), 1062, 498, "G")
seg_bub(mid(gt, gl), 356, 474, "H")
seg_bub(P(46, 0, ZP), 618, 790, "J")
seg_bub((P(ST["wh"], 0, ZR)[0], P(ST["wh"], 0, ZR)[1] + 16), 700, 618, "K")
seg_bub(P(70, 0, ZP), 880, 890, "L")
seg_bub((P(ST["ph"], 0, ZR)[0], P(ST["ph"], 0, ZR)[1] + 16), 972, 716, "M")

# general-note reference bubbles
note_bub(P(4, 0, ZP), 258, 584, "5")                     # PE pipe / cover / tracer
note_bub((P(ST["teeH"], BH, ZP)[0] + 4, P(ST["teeH"], BH, ZP)[1] - 6), 612, 528, "6")
sa, sb = P(15.0, 0, ZP), P(21.0, 0, ZP)                  # sleeve under the paver drive
pxs, pys = perp(DU)
o = 7.0
poly([(sa[0] + pxs * o, sa[1] + pys * o), (sb[0] + pxs * o, sb[1] + pys * o),
      (sb[0] - pxs * o, sb[1] - pys * o), (sa[0] - pxs * o, sa[1] - pys * o)], 1.0, col=GRAY)
note_bub(mid(sa, sb), 428, 560, "7")
rr = P(ST["wh"], 0, ZR)
note_bub((rr[0], rr[1] + 58), 566, 724, "8")             # shutoff / trap / connector
note_bub((ht[0] + 4, ht[1] + 34), 462, 452, "9")         # 2nd stage regulator / vents
note_bub(mid(ct_top, dr_top), 826, 352, "10")            # CSST protection / bonding
note_bub(P(ST["gen"] + 5.0, -22.0, 8.6), 456, 744, "11") # generator setbacks

# 12" cover dimension
cu = 64.0
gpt, ppt = P(cu, 0, 0), P(cu, 0, ZP)
dx0 = gpt[0] + 22
line((gpt[0] + 2, gpt[1]), (gpt[0] + 30, gpt[1]), 0.8, col=GRAY)
line((dx0, gpt[1]), (dx0, ppt[1]), 0.9)
for yy_, sg in ((gpt[1], 1), (ppt[1], -1)):
    poly([(dx0, yy_), (dx0 - 3, yy_ + 7 * sg), (dx0 + 3, yy_ + 7 * sg)], 0.8, fill="#000")
path([(dx0, ppt[1] + 2), (dx0 + 16, ppt[1] + 20), (860, ppt[1] + 8)], LW_LEAD)
txt(866, 800, "12&quot; MIN.", 8.6, w="bold")
txt(866, 810, "COVER", 8.6, w="bold")
txt(168, 620, "FINISH GRADE (TYP.)", 8.6, col=GRAY)
leader((P(14, 0, 0)[0] - 18, P(14, 0, 0)[1] + 6), (288, 616), dot=False)

# ==================================================== PRESSURE ZONE KEY
kx, ky, kw, kh = 974, 140, 276, 122
rect(kx, ky, kw, kh, 1.2, fill="#fff")
txt(kx + 14, ky + 21, "SYSTEM PRESSURE ZONES", 10.4, w="bold", ls=0.9)
line((kx + 14, ky + 28), (kx + kw - 14, ky + 28), 1.0)

zy = ky + 66                                  # flow-row centreline
def zbox(x0, w_, h_, lines):
    rect(x0, zy - h_ / 2, w_, h_, 1.0, fill="#f5f5f5")
    n = len(lines)
    for i, t in enumerate(lines):
        txt(x0 + w_ / 2, zy + 3.2 - (n - 1) * 4.6 + i * 9.2, t, 8.2, anchor="middle", w="bold")

def zarrow(x0, x1, label):
    line((x0 + 3, zy), (x1 - 8, zy), 1.3)
    poly([(x1, zy), (x1 - 8, zy - 3.6), (x1 - 8, zy + 3.6)], 0.8, fill="#000")
    txt((x0 + x1) / 2, zy - 20, label, 8.4, anchor="middle", w="bold")

zbox(kx + 14, 50, 24, ["TANK"])
zarrow(kx + 64, kx + 99, "10 PSI")
zbox(kx + 99, 70, 28, ["2nd STAGE", "REGULATOR"])
zarrow(kx + 169, kx + 204, '11&quot; W.C.')
zbox(kx + 204, 58, 24, ["APPLIANCE"])

txt(kx + 14, ky + 106, "1st STAGE REG. AT TANK DOME &#183; 2nd STAGE AT EACH RISER", 7.8, col=GRAY)

# ==================================================================== LEGEND
LX, LY, LW_, LH_ = 46, 140, 466, 208
rect(LX, LY, LW_, LH_, 1.2, fill="#fff")
txt(LX + 14, LY + 21, "LEGEND", 11.5, w="bold", ls=0.9)
line((LX + 14, LY + 28), (LX + LW_ - 14, LY + 28), 1.0)

LEG = [
    ("new",   "NEW GAS PIPING &#8212; PE U.G. / RIGID"),
    ("csst",  "NEW CSST &#8212; INTERIOR / ATTIC"),
    ("valve", "MANUAL SHUTOFF (BALL) VALVE"),
    ("reg1",  "1st STAGE REGULATOR (AT TANK)"),
    ("reg2",  "2nd STAGE REGULATOR"),
    ("trap",  "SEDIMENT TRAP"),
    ("tee",   "TEE / BRANCH CONNECTION"),
    ("flex",  "FLEXIBLE APPLIANCE CONNECTOR"),
    ("grade", "FINISH GRADE"),
    ("seg",   "PIPE SEGMENT TAG &#8212; SEE SCHEDULE"),
    ("note",  "REFERS TO GENERAL NOTE No."),
]
ROW = 26.0
COLX = [LX + 12, LX + 234]
SW = 46.0

def leg_symbol(kind, x0, cy):
    x1 = x0 + SW
    xm = (x0 + x1) / 2
    if kind == "new":
        line((x0, cy), (x1, cy), LW_NEW)
    elif kind == "csst":
        line((x0, cy), (x1, cy), LW_CSST, dash="11,3.5,2.5,3.5")
    elif kind == "ex":
        line((x0, cy), (x1, cy), LW_EX, dash="8,4")
    elif kind == "valve":
        line((x0, cy), (x1, cy), 1.4)
        ball_valve((xm, cy + 2), (1, 0), 6.6)
    elif kind == "reg1":
        line((x0, cy + 3), (x1, cy + 3), 1.4)
        regulator((xm, cy + 4), (-1, 0), 5.4)
    elif kind == "reg2":
        line((x0, cy + 3), (x1, cy + 3), 1.4)
        regulator((xm, cy + 4), (-1, 0), 5.4, REG2)
    elif kind == "trap":
        line((x0, cy - 4), (x1, cy - 4), 1.4)
        sed_trap((xm, cy - 4), 9)
    elif kind == "tee":
        line((x0, cy + 3), (x1, cy + 3), 1.4)
        line((xm, cy + 3), (xm, cy - 5), 1.4)
        tee((xm, cy + 3), 2.9)
    elif kind == "flex":
        flexline((x0, cy), (x1, cy), 4, 2.6)
    elif kind == "grade":
        line((x0, cy - 2), (x1, cy - 2), 0.9, col=LT)
        for i in range(7):
            xg = x0 + (x1 - x0) * i / 6
            line((xg, cy - 2), (xg - 4, cy + 4), 0.65, col=LT)
    elif kind == "seg":
        circ(xm, cy, 8.4, 1.4, fill="#fff")
        txt(xm, cy + 3.2, "A", 9, anchor="middle", w="bold")
    elif kind == "note":
        hexa(xm, cy, 8.8)
        txt(xm, cy + 3.2, "5", 8.8, anchor="middle", w="bold")

for i, (kind, label) in enumerate(LEG):
    col, row = (0, i) if i < 6 else (1, i - 6)
    x0 = COLX[col]
    cy = LY + 52 + row * ROW
    leg_symbol(kind, x0, cy)
    txt(x0 + SW + 10, cy + 3.2, label, 8.4)

# ============================================================== RIGHT COLUMN
CX0, CX1 = 1286, 1682
def col_head(y, s):
    txt(CX0, y, s, 11.5, w="bold", ls=0.9)
    line((CX0, y + 5), (CX1 - 4, y + 5), 1.3)

def table(y, cols, rows, widths, rh=15.0, bold_last=False):
    xs = [CX0]
    x = CX0
    for w_ in widths:
        x += w_; xs.append(x)
    add(f'<rect x="{CX0}" y="{y}" width="{sum(widths)}" height="{rh}" fill="#ececec" stroke="#000" stroke-width="0.8"/>')
    for i, c in enumerate(cols):
        a = "start" if i == 0 else "end"
        tx = xs[i] + 4 if i == 0 else xs[i + 1] - 4
        txt(tx, y + rh - 4.6, c, 8.4, anchor=a, w="bold")
    yy = y + rh
    for j, rw in enumerate(rows):
        rect(CX0, yy, sum(widths), rh, 0.7)
        bold = "bold" if (bold_last and j == len(rows) - 1) else "normal"
        for i, c in enumerate(rw):
            a = "start" if i == 0 else "end"
            tx = xs[i] + 4 if i == 0 else xs[i + 1] - 4
            txt(tx, yy + rh - 4.6, c, 8.6, anchor=a, w=bold)
        yy += rh
    for xv in xs:
        line((xv, y), (xv, yy), 0.7)
    return yy

y = 62
col_head(y, "CONNECTED LOAD SCHEDULE")
yend = table(y + 12, ("APPLIANCE", "QTY", "BTU/HR EA", "TOTAL"), [
    ("GENERATOR &#8212; 26 kW A.C. (NEW)", "1", "361,000", "361,000"),
    ("POOL HEATER", "1", "400,000", "400,000"),
    ("TANKLESS WATER HEATER", "1", "200,000", "200,000"),
    ("RANGE", "1", "35,000", "35,000"),
    ("DRYER", "1", "30,000", "30,000"),
    ("TOTAL CONNECTED LOAD", "", "", "1,026,000"),
], (196, 30, 78, 88), rh=14.0, bold_last=True)
txt(CX0, yend + 11, "GENERATOR INPUT PER THE MANUFACTURER'S RATING.  REMAINING APPLIANCE", 8.0, col=GRAY)
txt(CX0, yend + 20, "INPUTS PER STANDARD BTU SCHEDULE &#8212; VERIFY AGAINST APPLIANCE DATA PLATES.", 8.0, col=GRAY)

y = yend + 38
col_head(y, "PIPE SIZING SCHEDULE")
yend = table(y + 12, ("SEG", "LOAD BTU/HR", "LENGTH", "SIZE / MATERIAL"), [
    ("A", "1,026,000", "75'-0&quot;", "3/4&quot; IPS SDR-11 PE"),
    ("B", "65,000", "10'-0&quot;", "3/4&quot; IPS SDR-11 PE"),
    ("C", "65,000", "10'-0&quot;", "3/4&quot; RIGID (SCH 40)"),
    ("D", "65,000", "75'-0&quot;", "3/4&quot; CSST (EHD 23)"),
    ("E", "35,000", "10'-0&quot; MAX", "1/2&quot; RIGID (SCH 40)"),
    ("F", "30,000", "40'-0&quot;", "3/4&quot; CSST (EHD 23)"),
    ("G", "30,000", "10'-0&quot; MAX", "1/2&quot; RIGID (SCH 40)"),
    ("H", "361,000", "10'-0&quot; MAX", "3/4&quot; RIGID (SCH 40)"),
    ("J", "600,000", "9'-0&quot;", "3/4&quot; IPS SDR-11 PE"),
    ("K", "200,000", "10'-0&quot; MAX", "3/4&quot; RIGID (SCH 40)"),
    ("L", "400,000", "25'-0&quot;", "3/4&quot; IPS SDR-11 PE"),
    ("M", "400,000", "10'-0&quot; MAX", "3/4&quot; RIGID (SCH 40)"),
], (40, 108, 74, 170), rh=12.6)
yy = yend + 11
for n in ["SEG. A CARRIES THE WHOLE CONNECTED LOAD; SEG. B TEES OFF IT AND",
          "SERVES THE RANGE AND DRYER ONLY.  SEG. C IS THE ANODELESS RISER,",
          "RIGID FROM THE BELOW-GRADE TRANSITION UP THE WALL TO THE ATTIC,",
          "WHERE THE CSST BEGINS.  BURIED PE SEGMENTS (A, B, J, L) SIZED AT",
          "10 PSI INLET / 1.0 PSI ALLOWABLE DROP, LEAVING 9 PSIG MIN. AT EACH 2nd",
          "STAGE REGULATOR INLET &#8212; WITHIN THE NGR02-SERIES LISTED RANGE.",
          "SEG. A CAPACITY = 858 CFH &#8776; 2,134,000 BTU/HR OVER THE 109'-0&quot;",
          "DEVELOPED RUN FROM TANK TO POOL HEATER, 0.860&quot; I.D., PER THE NFPA 54",
          "HIGH-PRESSURE EQUATION (Cr = 1.2462, Y = 0.9910, 2,488 BTU/FT&#179;)",
          "= 2.1 &#215; THE CONNECTED LOAD.",
          "ALL OTHER SEGMENTS AT 11&quot; W.C. / 0.5&quot; W.C. DROP, SIZED ON THE 135'-0&quot;",
          "DEVELOPED RUN FROM THE 2nd STAGE REGULATOR TO THE DRYER (150 FT",
          "COLUMN): CSST EHD 23 = 83,000 BTU/HR PER THE MANUFACTURER'S LP TABLE;",
          "RIGID PER NFPA 54 TABLE 6.2(1) (LP), 3/4&quot; = 140,000 AND 1/2&quot; = 67,000 BTU/HR.",
          "LENGTHS ARE DEVELOPED LENGTHS; ADD FITTING EQUIVALENTS PER TABLE 6.4."]:
    txt(CX0, yy, n, 7.9, col=GRAY); yy += 8.6

y = yy + 8
col_head(y, "GENERAL NOTES")
# Note 1 carries the codes in force, so it is DERIVED from aoglib.CODE_CYCLES
# rather than typed — see the block in aoglib.py. This import is deliberately
# unconditional, unlike the date import above: a gas sheet must not print a code
# citation that has not come from the one place that owns it. Re-wrapped rather
# than hand-split so a longer edition string still breaks at this block's column
# instead of running off the sheet.
from aoglib import FBC_EDITION as _FBC, NFPA54_EDITION as _N54


def _wrapnote(num, body, width=70):
    out, cur = [], ""
    for _w in body.split():
        if len(cur) + len(_w) + 1 > width and cur:
            out.append(cur)
            cur = _w
        else:
            cur = (cur + " " + _w).strip()
    if cur:
        out.append(cur)
    return ["%-4s%s" % ("%d." % num, out[0])] + ["     " + l for l in out[1:]]


notes = _wrapnote(1, "ALL WORK PER NFPA 58 (LP GAS CODE), %s AND %s &#8212; "
                     "FUEL GAS, WITH ALL CITY OF MARCO ISLAND AMENDMENTS."
                     % (_N54, _FBC)) + [
 "2.  TWO-STAGE LP VAPOR SYSTEM: 1st STAGE REGULATOR AT TANK DOME",
 "     (10 PSI OUTLET); 2nd STAGE REGULATOR AT EACH RISER (11&quot; W.C.).",
 "3.  1,000 GAL. ASME TANK BURIED, AG/UG STYLE, W/ Mg ANTI-CORROSION ANODE,",
 "     STRAPPED TO TIE-DOWN AUGERS WITH NYLON-COATED 5/16&quot; STEEL CABLING PER",
 "     THE SEALED ANCHORAGE DETAIL.  SERVICE VALVE W/ EXCESS FLOW AT OUTLET.",
 "4.  TANK SETBACKS: 10'-0&quot; MIN. FROM ANY BUILDING OR BUILDABLE LINE (6.4.2.3);",
 "     10'-0&quot; MIN. FROM ANY SOURCE OF IGNITION (6.4.4.4); 10'-0&quot; MIN. FROM THE",
 "     DRIVEWAY OR VEHICLE BARRIER PROTECTION PROVIDED (6.8.6.1(B)).",
 "5.  UNDERGROUND PE PIPE: YELLOW, ASTM D2513 SDR-11, 12&quot; MIN. COVER",
 "     (18&quot; MIN. WHERE SUBJECT TO VEHICULAR TRAFFIC), W/ No. 14 AWG",
 "     INSULATED TRACER WIRE AND WARNING TAPE CONTINUOUS ABOVE PIPE.",
 "6.  NO PE PIPE ABOVE GRADE OR INSIDE ANY STRUCTURE; TRANSITION TO",
 "     RIGID (SCH 40 STEEL) BY ANODELESS RISER BELOW GRADE.",
 "7.  PE PIPE UNDER THE PAVER DRIVE SLEEVED IN SCH 40 PVC, SLEEVE",
 "     EXTENDED 12&quot; BEYOND EDGE OF PAVEMENT.",
 "8.  ACCESSIBLE MANUAL SHUTOFF VALVE UPSTREAM OF EACH 2nd STAGE REGULATOR;",
 "     THAT VALVE ALSO SERVES AS THE APPLIANCE SHUTOFF WHERE IT IS WITHIN 6'-0&quot;",
 "     OF THE APPLIANCE.  ELSEWHERE A SEPARATE SHUTOFF IS PROVIDED WITHIN 6'-0&quot;,",
 "     AHEAD OF THE TRAP AND LISTED CONNECTOR.  GENERATOR ON A LISTED WHIP.",
 "9.  REGULATOR AND RELIEF VENTS 3'-0&quot; MIN. FROM ANY BUILDING OPENING",
 "     AND 5'-0&quot; MIN. FROM ANY SOURCE OF IGNITION.",
 "10. ALL CSST IS 3/4&quot; (EHD 23), INTERIOR / ATTIC ONLY, NOT UNDERGROUND OR IN",
 "     CONTACT WITH EARTH.  PROTECTED FROM PHYSICAL DAMAGE, STRIKER PLATES",
 "     WITHIN 3&quot; OF FRAMING MEMBER EDGES, SUPPORTED PER MANUFACTURER.",
 "     BONDED PER NFPA 54 7.13.2 WITH A BONDING JUMPER NOT SMALLER THAN No. 6",
 "     AWG COPPER AND NOT LONGER THAN 75 FT, TERMINATING ON THE BUILDING",
 "     GROUNDING ELECTRODE SYSTEM.  THE JUMPER ATTACHES AT ANY APPROPRIATE",
 "     LOCATION IN THE CSST SYSTEM &#8212; A RIGID PIPE SEGMENT, PIPE FITTING OR CSST",
 "     FITTING.  A BONDING CLAMP IS NOT ATTACHED DIRECTLY TO THE TUBING.",
 "11. GENERATOR 18&quot; MIN. FROM THE STRUCTURE (SwRI-LISTED SEPARATION FOR",
 "     THIS MODEL), 5'-0&quot; MIN. FROM ANY OPENING (NFPA 37 4.1.4), 4'-0&quot;",
 "     FROM THE LOT LINE, ON AN ENGINEERED PRE-CAST PAD.",
 "12. FLOOD ZONE AE, B.F.E. 8.0 (FIRM 12021C0837H, 05/16/2012).  TOP OF",
 "     GENERATOR PAD SET NOT LESS THAN EL. 9.0 (N.A.V.D. 88), B.F.E. +1'-0&quot;.",
 "13. PRESSURE TEST ALL NEW PIPING PER NFPA 54 8.1 AT 1.5 &#215; MAX. WORKING",
 "     PRESSURE (3 PSIG MIN.), DURATION PER A.H.J.  SUBMIT THE GAS MANOMETER",
 "     TEST FORM AT INSPECTION, INCLUDING GENERATOR INLET PRESSURE UNDER LOAD.",
 "14. TANK VAPORIZATION CAPACITY AND FILL SCHEDULE PER TANK",
 "     MANUFACTURER'S DATA FOR THE TOTAL CONNECTED LOAD SHOWN.",
]
KEYED = {5, 6, 7, 8, 9, 10, 11}
hexa(CX0 + 9, y + 17, 6.4)
txt(CX0 + 22, y + 20, "HEXAGON BESIDE A NOTE = THAT NOTE IS KEYED ON THE ISOMETRIC", 7.8, col=GRAY)
yy = y + 34
for n in notes:
    m = re.match(r"^(\d+)\.", n)
    if m and int(m.group(1)) in KEYED:
        hexa(CX0 + 9, yy - 3, 6.4)
    txt(CX0 + 22, yy, n, 8.1); yy += 9.0

# ============================================================== TITLE BLOCK
TBY = 946
print("right column ends at y = %.1f  (title block top = %d)" % (yy, TBY))
assert yy < TBY, "right column overflows the title block"
rect(CX0 - 6, TBY, CX1 - CX0 + 6, H - 24 - TBY, 1.4, fill="#fff")
txt(CX0 + 4, TBY + 21, "ALWAYS ON GENERATORS", 15.5, w="bold", ls=0.8)
txt(CX0 + 4, TBY + 34, "3120 6th ST NW, NAPLES, FL 34120   &#183;   (239) 839-3553", 8.6)
txt(CX0 + 4, TBY + 45, "PERMITTING@ALWAYSONGENERATORS.COM", 8.6)
line((CX0 + 4, TBY + 52), (CX1 - 10, TBY + 52), 0.9)
txt(CX0 + 4, TBY + 95, "DESIGNED BY:  ALWAYS ON GENERATORS", 8.4, col=GRAY)
txt(CX0 + 4, TBY + 108, ADDR, 9.0, w="bold")
txt(CX0 + 4, TBY + 121, "DATE: " + SHEET_DATE, 8.8)
txt(CX1 - 10, TBY + 121, "SHEET", 8.8, anchor="end")
txt(CX1 - 10, TBY + 108, SHEET_NO, 21, anchor="end", w="bold")

add("</svg>")

# ================================================================== RENDER
OUT = "out" if os.path.isdir("out") else "."
svg = os.path.join(OUT, "gas_iso.svg")
open(svg, "w").write("\n".join(out))
print("wrote", svg)
try:
    import cairosvg
    cairosvg.svg2pdf(url=svg, write_to=os.path.join(OUT, "gas_iso.pdf"),
                     output_width=1632, output_height=1056)
    cairosvg.svg2png(url=svg, write_to=os.path.join(OUT, "gas_iso.png"),
                     output_width=1632, output_height=1056)
    print("wrote", os.path.join(OUT, "gas_iso.pdf"), "and .png")
except ImportError:
    print("cairosvg not installed - SVG only.  pip install cairosvg")
