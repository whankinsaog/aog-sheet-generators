"""Sheet SP-2 — Generator placement, clearances & mechanical screening.

THIS COPY IS POPULATED FOR: 456 Sample Ave N, Naples FL 34102

SCREEN_TYPE = "planter" is a fourth screening condition added on this job:
the generator sits on an ELEVATED concrete mechanical deck and is screened by
a planter of live vegetation on the deck itself, not by a fence, a wall or
grade-level landscaping. Keep it in the script — it is not a one-off.

Three things this sheet learned the hard way, all asserted below:
  * Sec. 56-41(a) screens ALL new mechanical equipment, not just the
    generator, so the planter run must cover the condensing units too.
  * The right-hand view is a SECTION, not an elevation. It was labelled an
    elevation while being drawn to plan coordinates, which put the planter
    beside the unit instead of in front of it and showed a meaningless 2"
    gap where the real dimension is the 3'-0" working space.
  * Equipment positions are DERIVED from clearances (GEN_X0 = CU_EAST +
    AC_CLR), never typed, so a moved condenser can't silently eat the
    NEC 110.26(A) working space.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, black, white
from reportlab.pdfbase.pdfmetrics import stringWidth
from aoglib import tx, box, line, wrap, titleblock, GREY, JOB

# =========================================================== CONFIG (per job)
SCREEN_TYPE = "planter"

GEN_NAME = "KOHLER 48RCLC"
GEN_L, GEN_W, GEN_H = 7.483, 2.742, 3.875      # 89.8" x 32.9" x 46.5"
GEN_WT = "1,690 LB OPERATING WEIGHT"

DECK_L, DECK_D = 25.167, 9.333                 # 25'-2" x 9'-4"  (Sheet A8)
WALL_OFF = 2.333                               # 2'-4" to the house wall
# Brandon asked for the generator off the wall for maintenance access. The
# lever is the planter DEPTH, not its width: width runs east-west, the wall
# offset runs north-south. A 12" planter frees 9" and all of it goes here,
# leaving the NEC 110.26(A) working space at exactly 3'-0". Asserted below.
RAIL_H = 3.00                                  # 36" guard railing
VEG_H = 4.00                                   # 48" installed planting height

# deck-local coordinates: x runs west->east, y = 0 at the outboard (railing)
# edge, y = DECK_D at the house wall.
GEN_Y0 = DECK_D - WALL_OFF - GEN_W             # 5.09
WS_D = 3.00                                    # NEC 110.26(A) depth
# WHICH FACE THE CONTROL PANEL AND LINE CIRCUIT BREAKER ARE ON. This is not a
# drafting preference — it decides where the 110.26(A) working space goes, and
# it must come from the manufacturer's own literature or the field, never from
# the last job's machine. The Kohler spec sheet G4-306 does NOT show it (its
# dimension drawing is two plain rectangles and it says in print that it is for
# reference only and not for planning installation), so this is set from AOG's
# field knowledge of the 48RCLC: controller and breaker on the FRONT face, at
# the left (west) end. It was previously "west", carried over from the Generac
# XG08045, whose panel really is on the narrow end face.
PANEL_FACE = "front"                           # "front" | "west"
CB_W = 2.50                                    # width of the panel/breaker strip
AC_CLR = 3.00                                  # NEC 445.10 / 430.14 to the CUs
# The planter must never crowd the front of the generator. Asserted below.
END_WALL = DECK_L                              # east end wall of the deck

# The WHOLE east-west layout is solved backwards from the exhaust clearance,
# because that is the dimension that matters: NFPA 37 4.1.4 wants 5 ft from
# openings and from combustible walls, and hitting it outright is cleaner than
# arguing the end wall has neither. Everything downstream falls out of it:
#     generator east face  = END_WALL - EXH_TARGET
#     generator west face  = that - GEN_L
#     last condenser       = generator west face - AC_CLR   (NEC 445.10/430.14)
#     first condenser      = 4'-0" west of it (1'-0" between units)
# Nothing in this block is a typed coordinate. Raising EXH_TARGET pushes the
# condensers west and eats the walk-through at the gate end, which is why
# WEST_CLR is asserted rather than left to chance.
EXH_TARGET = 5.00                              # NFPA 37 4.1.4
CU_W = CU_H = 3.00
CU_GAP = 1.00                                  # between the two condensers
CU_WALL_OFF = 1.50                             # condensers' own offset to the wall
WEST_MIN = 2.50                                # walk-through at the louver gate

GEN_X1 = END_WALL - EXH_TARGET
GEN_X0 = GEN_X1 - GEN_L
CU_EAST = GEN_X0 - AC_CLR
_cu2 = CU_EAST - CU_W
_cu1 = _cu2 - CU_W - CU_GAP
CU_LIST = [("A/C", _cu1, DECK_D - CU_WALL_OFF - CU_H, CU_W, CU_H),
           ("A/C", _cu2, DECK_D - CU_WALL_OFF - CU_H, CU_W, CU_H)]
WEST_CLR = _cu1
assert WEST_CLR >= WEST_MIN, (
    "only %.2f ft of deck west of the first condenser; %.2f ft is the minimum "
    "walk-through at the louver gate. Lower EXH_TARGET." % (WEST_CLR, WEST_MIN))
assert GEN_X0 > CU_EAST, "the generator has been pushed west of the condensers"

# The planter must still cover every piece of new mechanical equipment
# (Sec. 56-41(a)), so it is sized off the equipment run, not typed.
PLANT_X0 = _cu1 - 0.20
PLANT_X1 = GEN_X1 + 0.20
PLANT_Y0, PLANT_D = 0.25, 1.00
FRONT_CLR = 3.00   # NEC 110.26(A) working space at the front of the unit

_FRONT_GAP = GEN_Y0 - (PLANT_Y0 + PLANT_D)
assert _FRONT_GAP >= FRONT_CLR, (
    "only %.2f ft clear at the front of the generator; %.2f ft required — "
    "move the planter outboard" % (_FRONT_GAP, FRONT_CLR))


def _ftin(v):
    f = int(v); i = int(round((v - f) * 12))
    if i == 12:
        f, i = f + 1, 0
    return "%d'-%d\"" % (f, i)


FRONT_DIM = _ftin(_FRONT_GAP)
WALL_DIM = _ftin(WALL_OFF)
AC_DIM = _ftin(GEN_X0 - CU_EAST)
EXH_DIM = _ftin(END_WALL - (GEN_X0 + GEN_L))
assert GEN_X0 - CU_EAST >= AC_CLR, "generator is inside the CU clearance"
if PANEL_FACE == "west":
    assert GEN_X0 - WS_D >= CU_EAST, (
        "the NEC 110.26(A) working space overlaps a condensing unit")
assert GEN_X0 + GEN_L < END_WALL, "the generator runs past the end wall"
# Sec. 56-41(a) covers ALL new mechanical equipment, not only the generator.
_SCREENED = [("GENERATOR", GEN_X0, GEN_X0 + GEN_L)] + \
            [(nm, cx, cx + cw) for nm, cx, _, cw, _ in CU_LIST]
for _nm, _x0, _x1 in _SCREENED:
    assert PLANT_X0 <= _x0 and _x1 <= PLANT_X1, (
        "%s at %s-%s is not screened by the planter" %
        (_nm, _ftin(_x0), _ftin(_x1)))

KEYNOTES = [
    ("1", WALL_DIM + " FROM THE GENERATOR ENCLOSURE TO THE ADJACENT HOUSE WALL. THE "
          "ADJACENT WALL IS 8 IN. REINFORCED C.M.U. WITH #5 BAR IN GROUT-FILLED "
          "CELLS AND STUCCO EXTERIOR FINISH — NONCOMBUSTIBLE CONSTRUCTION, PER "
          "SHEET A3. THE 48RCLC IS LISTED AND LABELED BY THE MANUFACTURER FOR "
          "AN 18 IN. OFFSET; THE INSTALLED OFFSET EXCEEDS THAT MINIMUM."),
    ("2", "NEC 110.26(A) WORKING SPACE AT THE CONTROL PANEL AND LINE CIRCUIT "
          "BREAKER, WHICH ARE ON THE FRONT FACE OF THE ENCLOSURE AT THE WEST "
          "END — 3'-0\" DEEP BY THE FULL 7'-6\" WIDTH OF THE EQUIPMENT, MEASURED "
          "FROM THE FRONT FACE. THE WORKING SPACE LANDS WHOLLY ON THE CONCRETE "
          "DECK AND IS CLEAR OF THE PLANTER."),
    ("3", "PLANTER WITH LIVE VEGETATION, SCREENING THE GENERATOR AND BOTH "
          "CONDENSING UNITS TO THEIR FULL HEIGHT PER SEC. 56-41(a). THE PLANTER "
          "IS SET " + FRONT_DIM + " CLEAR OF THE FRONT OF THE GENERATOR "
          "ENCLOSURE. SEE THE SECTION."),
    ("4", "EXHAUST DISCHARGE AIR LEAVES THE EAST END OF THE ENCLOSURE INTO OPEN "
          "DECK. " + EXH_DIM + " CLEAR FROM THE DISCHARGE END OF THE ENCLOSURE "
          "TO THE END WALL. NO PLANTING OR EQUIPMENT IS PLACED IN THE "
          "DISCHARGE PATH."),
    ("5", AC_DIM + " CLEAR FROM THE NEAREST CONDENSING UNIT TO THE GENERATOR "
          "ENCLOSURE, MEETING THE 3'-0\" MINIMUM PER NEC 445.10 AND 430.14."),
    ("6", "36\" HIGH GUARD RAILING AT THE OUTBOARD DECK EDGE, BY OTHERS, PER THE "
          "ARCHITECTURAL SET."),
    ("7", "NEC 110.26(A)(1)(a): WORKING SPACE IS NOT REQUIRED IN THE BACK OR "
          "SIDES OF DEAD-FRONT ASSEMBLIES WHERE ALL CONNECTIONS AND ALL "
          "RENEWABLE OR ADJUSTABLE PARTS ARE ACCESSIBLE FROM LOCATIONS OTHER "
          "THAN THE BACK OR SIDES. ALL CONNECTIONS, THE 200 A LINE CIRCUIT "
          "BREAKER AND THE CONTROL PANEL ARE ACCESSIBLE AT THE FRONT FACE OF "
          "THE ENCLOSURE. NO WORKING SPACE IS REQUIRED AT THE BACK OF THE "
          "GENERATOR."),
    ("8", "LOUVER GATE AT THE WEST END OF THE DECK, BY OTHERS, PER THE "
          "ARCHITECTURAL SET. ACCESS TO THE MECHANICAL DECK IS THROUGH THIS "
          "GATE."),
]

# ---- table block geometry (declared early: the screening note asserts against it)
TY, TH = 40.0, 414.0

# ================================================================ sheet setup
W, H = 1224.0, 792.0
RED = Color(.78, .05, .09)
ORNG = Color(.76, .38, .08)
GRN = Color(.05, .42, .16)
LGRY = Color(.93, .93, .93)
HATCH = Color(.72, .72, .72)
VEGC = Color(.13, .38, .16)
TBW, M = 250, 18

OUT = "out/SP-2 Generator Placement Clearances and Screening - 456 Sample Ave N.pdf"
c = canvas.Canvas(OUT, pagesize=(W, H))
box(c, M, M, W - 2 * M, H - 2 * M, lw=1.6)


def wrapw(text, maxw, font="Helvetica", size=6.6):
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


def tx_fit(cv, x, y, s, maxsize, availw, font="Helvetica-Bold", col=black, anchor="l"):
    sz = maxsize
    while sz > 4.5 and stringWidth(s, font, sz) > availw:
        sz -= .2
    tx(cv, x, y, s, sz, font, col, anchor)


tx(c, 26, H - M - 26, "GENERATOR PLACEMENT, CLEARANCES & MECHANICAL SCREENING",
   17, "Helvetica-Bold")
tx(c, 26, H - M - 40, "CITY OF NAPLES CODE OF ORDINANCES SEC. 56-41 — MECHANICAL "
                      "EQUIPMENT  ·  SEC. 58-176 SETBACKS  ·  NFPA 37  ·  NEC 110.26  ·  "
                      "MANUFACTURER'S INSTALLATION MANUAL",
   8.0, "Helvetica-Oblique", GREY)
line(c, 26, H - M - 47, 956, H - M - 47, lw=.9, col=ORNG)

# ==================================================================== PLAN
SC = 15.0
PX, PY = 62.0, 536.0


def P(fx, fy):
    return PX + fx * SC, PY + fy * SC


tx(c, 26, 706, "PLAN — GENERATOR ON CONCRETE MECHANICAL DECK", 9.6, "Helvetica-Bold")
tx(c, 338, 706, "SCALE: 1\" = 4'-0\"", 6.8, "Helvetica-Oblique", GREY)

# house wall along the top of the deck
c.saveState(); c.setFillColor(HATCH); c.setStrokeColor(black); c.setLineWidth(.8)
a, b = P(-0.9, DECK_D); d, e = P(DECK_L + 0.9, DECK_D + 0.62)
c.rect(a, b, d - a, e - b, stroke=1, fill=1); c.restoreState()
tx(c, *P(0.4, DECK_D + 0.20), "RESIDENCE — EXTERIOR WALL, 8\" REINFORCED "
   "C.M.U. W/ STUCCO FINISH (NONCOMBUSTIBLE) — SHEET A3", 6.4, "Helvetica-Bold")

# deck slab
box(c, *P(0, 0), DECK_L * SC, DECK_D * SC, lw=1.4, fill=Color(.975, .972, .965))
tx(c, *P(4.2, 3.35), "CONCRETE MECHANICAL DECK", 6.0, "Helvetica-Bold", GREY)

# east end wall of the deck
c.saveState(); c.setFillColor(HATCH); c.setStrokeColor(black); c.setLineWidth(.9)
_e0 = P(END_WALL, 0); _e1 = P(END_WALL + 0.58, DECK_D + 0.62)
c.rect(_e0[0], _e0[1], _e1[0] - _e0[0], _e1[1] - _e0[1], stroke=1, fill=1)
c.restoreState()
tx(c, P(END_WALL + 0.29, 0)[0], P(0, 4.1)[1], "END WALL — 8\" C.M.U.", 6.0,
   "Helvetica-Bold", anchor="c", rot=90)

# louver gate at the west end of the deck (by others). Drawn as a symbol only —
# the architectural set governs its size and position, so nothing here is
# dimensioned to it.
GATE_Y0, GATE_Y1 = 6.03, DECK_D
c.saveState(); c.setStrokeColor(black); c.setLineWidth(2.0)
c.line(*P(0, GATE_Y1), *P(0, GATE_Y0))
c.setLineWidth(.8); c.setDash(3, 2)
_gr = (GATE_Y1 - GATE_Y0) * SC
c.arc(P(0, GATE_Y1)[0] - _gr, P(0, GATE_Y1)[1] - _gr,
      P(0, GATE_Y1)[0] + _gr, P(0, GATE_Y1)[1] + _gr, 270, 90)
c.restoreState()
# The gate label sits BELOW the condenser band, not beside it. It used to sit
# at y=5.45, level with the units; when the condensers moved west to buy the
# 5'-0" exhaust clearance they ran straight through it. Its clear zone is now
# derived from the first condenser, and asserted.
_GL_X, _GL_Y = 0.55, 3.95
_GL_W = max(stringWidth(t, "Helvetica-Bold", 6.0)
            for t in ("LOUVER GATE", "BY OTHERS")) / SC
assert (_GL_X + _GL_W <= CU_LIST[0][1]) or (_GL_Y + 0.30 <= CU_LIST[0][2]), (
    "the louver gate label runs into the first condensing unit")
assert _GL_Y - 0.35 > PLANT_Y0 + PLANT_D, "the gate label sits on the planter"
tx(c, *P(_GL_X, _GL_Y), "LOUVER GATE", 6.0, "Helvetica-Bold")
tx(c, *P(_GL_X, _GL_Y - 0.35), "BY OTHERS", 6.0, "Helvetica-Bold")

# guard railing at outboard edge
c.saveState(); c.setStrokeColor(black); c.setLineWidth(2.4)
c.line(*P(0, 0), *P(DECK_L, 0)); c.restoreState()

# condensing units
for nm, cx, cy, cw, ch in CU_LIST:
    box(c, *P(cx, cy), cw * SC, ch * SC, lw=1.0, fill=white)
    tx(c, P(cx + cw / 2, 0)[0], P(0, cy + ch / 2 - 0.10)[1], nm, 7.4,
       "Helvetica-Bold", anchor="c")

# planter
c.saveState(); c.setFillColor(Color(.88, .93, .87)); c.setStrokeColor(VEGC)
c.setLineWidth(1.2)
p0 = P(PLANT_X0, PLANT_Y0); p1 = P(PLANT_X1, PLANT_Y0 + PLANT_D)
c.rect(p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1], stroke=1, fill=1)
c.restoreState()
for i in range(7):
    fx = PLANT_X0 + 0.7 + i * ((PLANT_X1 - PLANT_X0 - 1.4) / 6.0)
    vx, vy = P(fx, PLANT_Y0 + PLANT_D / 2)
    c.saveState(); c.setFillColor(VEGC); c.setStrokeColor(VEGC)
    c.circle(vx, vy, 7.0, stroke=0, fill=1); c.restoreState()
# The planter label is centred on the run WEST of the working space, not on the
# whole planter: with the panel on the front face the 110.26 hatch covers the
# middle of the planter and swallowed this label.
_pl_c = (PLANT_X0 + (GEN_X0 if PANEL_FACE == "front" else PLANT_X1)) / 2
_pl_w = stringWidth("PLANTER — LIVE VEGETATION SCREEN", "Helvetica-Bold", 6.6) / SC
assert _pl_c + _pl_w / 2 <= GEN_X0 + 0.10 or PANEL_FACE != "front", \
    "the planter label runs under the working-space hatch"
tx(c, P(_pl_c, 0)[0], P(0, PLANT_Y0 + PLANT_D + 0.30)[1],
   "PLANTER — LIVE VEGETATION SCREEN", 6.6, "Helvetica-Bold", VEGC, "c")
assert PLANT_Y0 > 0, "the planter has been pushed off the outboard deck edge"

# NEC 110.26(A) working space — grey fill, red diagonal hatch, then label
if PANEL_FACE == "front":
    ws0 = P(GEN_X0, GEN_Y0 - WS_D)
    ws1 = P(GEN_X0 + GEN_L, GEN_Y0)
else:
    ws0 = P(GEN_X0 - WS_D, GEN_Y0)
    ws1 = P(GEN_X0, GEN_Y0 + GEN_W)
c.saveState(); c.setFillColor(LGRY); c.setStrokeColor(black); c.setLineWidth(.9)
c.rect(ws0[0], ws0[1], ws1[0] - ws0[0], ws1[1] - ws0[1], stroke=1, fill=1)
c.restoreState()
c.saveState()
pth = c.beginPath(); pth.rect(ws0[0], ws0[1], ws1[0] - ws0[0], ws1[1] - ws0[1])
c.clipPath(pth, stroke=0, fill=0)
c.setStrokeColor(RED); c.setLineWidth(.45)
t = -(ws1[1] - ws0[1])
while t < ws1[0] - ws0[0]:
    c.line(ws0[0] + t, ws0[1], ws0[0] + t + (ws1[1] - ws0[1]), ws1[1]); t += 4.5
c.restoreState()
wsmx = (ws0[0] + ws1[0]) / 2
wsmy = (ws0[1] + ws1[1]) / 2
for i, s in enumerate(("NEC 110.26", "WORKING", "SPACE")):
    tx(c, wsmx, wsmy + 9 - i * 8.6, s, 6.4, "Helvetica-Bold", black, "c")

# generator enclosure
g0 = P(GEN_X0, GEN_Y0); g1 = P(GEN_X0 + GEN_L, GEN_Y0 + GEN_W)
box(c, g0[0], g0[1], g1[0] - g0[0], g1[1] - g0[1], lw=2.2, fill=white, stroke=RED)
# control / breaker strip, on the face PANEL_FACE names
c.saveState(); c.setFillColor(Color(.97, .93, .90)); c.setStrokeColor(RED)
c.setLineWidth(.9)
if PANEL_FACE == "front":
    c.rect(g0[0], g0[1], CB_W * SC, 0.55 * SC, stroke=1, fill=1); c.restoreState()
    tx(c, g0[0] + CB_W * SC / 2, g0[1] + 0.20 * SC, "CB / CONTROL", 5.6,
       "Helvetica-Bold", RED, "c")
    _glx = (g0[0] + g1[0]) / 2
    _glw = GEN_L * SC - 10
    _gly = (g0[1] + g1[1]) / 2 + 0.28 * SC
else:
    c.rect(g0[0], g0[1], 0.55 * SC, g1[1] - g0[1], stroke=1, fill=1); c.restoreState()
    tx(c, g0[0] + 0.28 * SC, (g0[1] + g1[1]) / 2, "CB / CONTROL", 5.6,
       "Helvetica-Bold", RED, "c", rot=90)
    _glx = g0[0] + 0.55 * SC + (GEN_L - 0.55) * SC / 2
    _glw = (GEN_L - 0.55) * SC - 10
    _gly = (g0[1] + g1[1]) / 2
tx_fit(c, _glx, _gly + 2, GEN_NAME, 8.2, _glw, col=RED, anchor="c")
tx_fit(c, _glx, _gly - 8, "7'-6\" × 2'-9\" × 3'-10½\" H",
       6.4, _glw, font="Helvetica", col=RED, anchor="c")

# exhaust discharge air, east end
ax, ay = g1[0], (g0[1] + g1[1]) / 2
c.saveState(); c.setStrokeColor(GRN); c.setFillColor(GRN); c.setLineWidth(1.5)
c.line(ax + 3, ay, ax + 26, ay)
pth = c.beginPath(); pth.moveTo(ax + 24, ay - 4.5); pth.lineTo(ax + 24, ay + 4.5)
pth.lineTo(ax + 36, ay); pth.close(); c.drawPath(pth, stroke=0, fill=1)
c.restoreState()
tx(c, ax + 4, ay + 13, "EXHAUST", 5.8, "Helvetica-Bold", GRN)
tx(c, ax + 4, ay + 5, "DISCHARGE", 5.8, "Helvetica-Bold", GRN)


def dim(x1, y1, x2, y2, label, off=0, vert=False, col=RED, size=6.8, lshift=0):
    c.saveState(); c.setStrokeColor(col); c.setLineWidth(.9)
    if vert:
        c.line(x1 + off, y1, x1 + off, y2)
        for yy in (y1, y2):
            c.line(x1 + off - 4, yy, x1 + off + 4, yy)
        mx, my = x1 + off, (y1 + y2) / 2
    else:
        c.line(x1, y1 + off, x2, y1 + off)
        for xx in (x1, x2):
            c.line(xx, y1 + off - 4, xx, y1 + off + 4)
        mx, my = (x1 + x2) / 2, y1 + off
    c.restoreState()
    my += lshift
    wdt = stringWidth(label, "Helvetica-Bold", size) + 16
    box(c, mx - wdt / 2, my - 6.5, wdt, 13, lw=.7, fill=white, stroke=col)
    tx(c, mx, my - 3.2, label, size, "Helvetica-Bold", col, "c")


dim(P(GEN_X0 + GEN_L - 1.4, 0)[0], P(0, GEN_Y0 + GEN_W)[1], 0, P(0, DECK_D)[1],
    WALL_DIM, vert=True)
dim(P(GEN_X0, 0)[0], P(0, 0)[1], P(GEN_X0 + GEN_L, 0)[0], 0, "7'-6\"", off=-20)
dim(P(CU_EAST, 0)[0], P(0, 0)[1], P(GEN_X0, 0)[0], 0, AC_DIM, off=-20)
# the front clearance, called out on the plan as well as the section
dim(P(22.3, 0)[0], P(0, PLANT_Y0 + PLANT_D)[1], 0, P(0, GEN_Y0)[1],
    FRONT_DIM, vert=True)
dim(P(GEN_X0 + GEN_L, 0)[0], P(0, 0)[1], P(END_WALL, 0)[0], 0,
    EXH_DIM, off=-20)
dim(P(0, 0)[0], P(0, 0)[1], P(DECK_L, 0)[0], 0, "25'-2\"", off=-40)
dim(P(DECK_L, 0)[0], P(0, 0)[1], 0, P(0, DECK_D)[1], "9'-4\"", off=46,
    vert=True, col=black)

# keynote bubbles
def bub(n, fx, fy, tox, toy):
    bx, by = P(fx, fy)
    tx0, ty0 = P(tox, toy)
    line(c, bx, by, tx0, ty0, lw=.7, col=black)
    c.saveState(); c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(1.0)
    c.circle(bx, by, 7.5, stroke=1, fill=1); c.restoreState()
    tx(c, bx, by - 2.6, n, 7.0, "Helvetica-Bold", black, "c")


bub("1", 18.0, DECK_D - 0.62, 18.0, DECK_D - WALL_OFF)
if PANEL_FACE == "front":
    bub("2", 10.55, GEN_Y0 - WS_D + 0.95, GEN_X0 + 0.80, GEN_Y0 - WS_D + 0.95)
else:
    bub("2", 12.15, GEN_Y0 + GEN_W + 0.75, GEN_X0 - WS_D / 2, GEN_Y0 + GEN_W)
bub("3", 23.5, PLANT_Y0 + PLANT_D / 2, PLANT_X1, PLANT_Y0 + PLANT_D / 2)
bub("4", 24.3, GEN_Y0 - 0.85, GEN_X0 + GEN_L, GEN_Y0 + GEN_W / 2)
bub("5", 12.6, GEN_Y0 - 1.15, 11.00, GEN_Y0 + 1.37)
bub("6", 1.5, 1.35, 2.4, 0.05)
bub("7", 15.9, DECK_D - 0.62, 15.9, GEN_Y0 + GEN_W)
bub("8", 2.6, 7.4, 0.15, 7.9)

# ============================================ SECTION THROUGH THE MECH DECK
# This is a SECTION, not an elevation: the horizontal axis is the DEPTH of the
# deck (outboard rail on the left, house wall on the right), so it is drawn to
# the same spacing as the plan. Drawn as an "elevation" the planter landed
# beside the generator instead of in front of it and showed a gap that meant
# nothing. Every horizontal position below is a real plan coordinate.
EX, EY, ES = 648.0, 566.0, 24.0
tx(c, 604, 706, "SECTION THROUGH THE MECHANICAL DECK", 9.6, "Helvetica-Bold")
tx(c, 604, 695, "SCALE: 1\" = 3'-0\"   ·   LOOKING EAST   ·   SCREENING AND "
                "FRONT CLEARANCE", 6.8, "Helvetica-Oblique", GREY)


def E(fx, fy):
    """fx is the deck-depth coordinate used by the plan; fy is height."""
    return EX + fx * ES, EY + fy * ES


# deck slab
c.saveState(); c.setFillColor(LGRY); c.setStrokeColor(black); c.setLineWidth(1.3)
p0, p1 = E(-0.55, -0.7), E(DECK_D + 0.5, 0)
c.rect(p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1], stroke=1, fill=1); c.restoreState()
tx(c, *E(-0.55, -1.25), "CONCRETE MECHANICAL DECK", 6.4, "Helvetica-Bold", GREY)

# house wall on the right
c.saveState(); c.setFillColor(HATCH); c.setStrokeColor(black); c.setLineWidth(.9)
p0, p1 = E(DECK_D, 0), E(DECK_D + 0.5, 4.7)
c.rect(p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1], stroke=1, fill=1); c.restoreState()
tx(c, E(DECK_D + 0.25, 0)[0], E(0, 5.05)[1], "HOUSE WALL", 6.0,
   "Helvetica-Bold", anchor="c")
tx(c, E(DECK_D + 0.25, 0)[0], E(0, 4.82)[1], "8\" C.M.U.", 6.0,
   "Helvetica-Bold", anchor="c")

# guard railing at the outboard edge
c.saveState(); c.setStrokeColor(black); c.setLineWidth(1.4)
c.line(*E(0, 0), *E(0, RAIL_H))
c.line(*E(-0.22, RAIL_H), *E(0.22, RAIL_H))
c.line(*E(-0.18, RAIL_H - 0.35), *E(0.18, RAIL_H - 0.35))
c.restoreState()
tx(c, E(-0.15, 0)[0], E(0, RAIL_H + 0.42)[1], "36\" GUARD", 6.0,
   "Helvetica-Bold", anchor="r")
tx(c, E(-0.15, 0)[0], E(0, RAIL_H + 0.17)[1], "RAILING", 6.0,
   "Helvetica-Bold", anchor="r")

# planter, at its real plan position
c.saveState(); c.setFillColor(Color(.80, .74, .66)); c.setStrokeColor(black)
c.setLineWidth(1.0)
p0, p1 = E(PLANT_Y0, 0), E(PLANT_Y0 + PLANT_D, 1.30)
c.rect(p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1], stroke=1, fill=1); c.restoreState()
_pc = PLANT_Y0 + PLANT_D / 2
c.saveState(); c.setFillColor(VEGC); c.setStrokeColor(VEGC)
for (fx, fy, r) in ((_pc, 2.25, 17), (_pc - 0.42, 3.15, 14), (_pc + 0.42, 3.20, 14),
                    (_pc, 3.95, 15), (_pc - 0.30, 1.80, 13), (_pc + 0.32, 1.85, 13)):
    vx, vy = E(fx, fy)
    c.circle(vx, vy, r, stroke=0, fill=1)
c.restoreState()

# generator, at its real plan position
c.saveState(); c.setStrokeColor(RED); c.setLineWidth(1.8); c.setFillColor(white)
p0, p1 = E(GEN_Y0, 0), E(GEN_Y0 + GEN_W, GEN_H)
c.rect(p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1], stroke=1, fill=1); c.restoreState()
_gc = GEN_Y0 + GEN_W / 2
tx(c, E(_gc, 0)[0], E(0, GEN_H / 2 + 0.12)[1], GEN_NAME, 6.8, "Helvetica-Bold",
   RED, "c")
tx(c, E(_gc, 0)[0], E(0, GEN_H / 2 - 0.20)[1], "3'-10½\" H", 6.2, "Helvetica",
   RED, "c")
_fx = (PLANT_Y0 + PLANT_D + GEN_Y0) / 2
tx(c, E(_fx, 0)[0], E(0, 2.62)[1], "FRONT OF", 6.0, "Helvetica-Bold", RED, "c")
tx(c, E(_fx, 0)[0], E(0, 2.38)[1], "GENERATOR", 6.0, "Helvetica-Bold", RED, "c")
c.saveState(); c.setStrokeColor(RED); c.setFillColor(RED); c.setLineWidth(.9)
c.line(E(_fx + 0.55, 0)[0], E(0, 2.50)[1], E(GEN_Y0 - 0.12, 0)[0], E(0, 2.50)[1])
_pth = c.beginPath()
_pth.moveTo(E(GEN_Y0 - 0.18, 0)[0], E(0, 2.56)[1])
_pth.lineTo(E(GEN_Y0 - 0.18, 0)[0], E(0, 2.44)[1])
_pth.lineTo(E(GEN_Y0, 0)[0], E(0, 2.50)[1]); _pth.close()
c.drawPath(_pth, stroke=0, fill=1); c.restoreState()

# ---- the two horizontal clearances this section exists to show
dim(E(PLANT_Y0 + PLANT_D, 0)[0], E(0, 0.62)[1], E(GEN_Y0, 0)[0], 0, FRONT_DIM)
dim(E(GEN_Y0 + GEN_W, 0)[0], E(0, 0.62)[1], E(DECK_D, 0)[0], 0, WALL_DIM)
tx(c, (E(PLANT_Y0 + PLANT_D, 0)[0] + E(GEN_Y0, 0)[0]) / 2, E(0, 1.05)[1],
   "NEC 110.26(A) WORKING SPACE", 5.8, "Helvetica-Bold", RED, "c")

# ---- heights
# The two height dimensions get their OWN extension line at their OWN x. Stacked
# on one line they overlap and the shorter one disappears under the taller. The
# dashed leaders also break at the house wall instead of running through its
# hatch, which is what made this corner unreadable.
WALL_X0, WALL_X1 = DECK_D, DECK_D + 0.5
GEN_DIM_X, VEG_DIM_X = DECK_D + 1.60, DECK_D + 2.30


def height_leader(fy, x_from, dim_x, col):
    """dashed height line, broken either side of the wall"""
    c.saveState(); c.setStrokeColor(col); c.setLineWidth(1.0); c.setDash(5, 3)
    c.line(*E(x_from, fy), *E(WALL_X0, fy))
    c.line(*E(WALL_X1, fy), *E(dim_x + 0.12, fy))
    c.restoreState()


height_leader(VEG_H, PLANT_Y0 - 0.3, VEG_DIM_X, VEGC)
height_leader(GEN_H, GEN_Y0, GEN_DIM_X, RED)
dim(E(GEN_DIM_X, 0)[0], E(0, 0)[1], 0, E(0, GEN_H)[1], "3'-10½\"", vert=True)
# both dims run from the deck, so their labels land at almost the same height —
# stagger the taller one clear of the shorter one as well as offsetting its line
dim(E(VEG_DIM_X, 0)[0], E(0, 0)[1], 0, E(0, VEG_H)[1], "4'-0\"", vert=True,
    col=VEGC, lshift=26)
assert E(VEG_DIM_X, 0)[0] + 24 < W - M - TBW, \
    "the height dimensions run into the title block"
assert E(GEN_DIM_X, 0)[0] - 24 > E(WALL_X1, 0)[0], \
    "a height dimension label sits on the house wall"
tx(c, *E(2.95, VEG_H + 0.22), "TOP OF PLANTING AT INSTALLATION — 4'-0\"",
   6.4, "Helvetica-Bold", VEGC)

# Box height is computed from the wrapped line count, never a constant — a
# fixed height silently spills the last lines out below the border.
_NW = 320.0
_NLH = 9.8
_nl = wrapw("LIVE VEGETATION IS INSTALLED AT NOT LESS THAN 4'-0\" AND MAINTAINED AT "
            "NOT LESS THAN THE FULL HEIGHT OF THE GENERATOR ENCLOSURE (3'-10½\"), "
            "SCREENING THE EQUIPMENT TO ITS FULL HEIGHT PER SEC. 56-41(a).",
            _NW - 22, size=7.0)
_nh = len(_nl) * _NLH + 13
_NOTE_TOP = 506.0
_ny = _NOTE_TOP - _nh
box(c, 630.0, _ny, _NW, _nh, lw=.8, stroke=VEGC, fill=Color(.95, .97, .94))
for i, ln in enumerate(_nl):
    tx(c, 641.0, _ny + _nh - 13 - i * _NLH, ln, 7.0,
       "Helvetica-Bold", VEGC)
assert _ny > TY + TH + 6, "screening note overruns the tables below"

# ==================================================== keynotes + compliance
TX0, TW = 26.0, 930.0

# --- keynote column (left)
KW = 296.0
box(c, TX0, TY, KW, TH, lw=1.3)
tx(c, TX0 + 10, TY + TH - 17, "CLEARANCE KEY NOTES", 9.6, "Helvetica-Bold")
line(c, TX0 + 10, TY + TH - 23, TX0 + KW - 10, TY + TH - 23, lw=.9, col=ORNG)
ky = TY + TH - 38
for n, t in KEYNOTES:
    c.saveState(); c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(.9)
    c.circle(TX0 + 20, ky - 2, 7.2, stroke=1, fill=1); c.restoreState()
    tx(c, TX0 + 20, ky - 4.6, n, 6.8, "Helvetica-Bold", black, "c")
    for ln in wrapw(t, KW - 50, size=6.4):
        tx(c, TX0 + 34, ky, ln, 6.4); ky -= 8.0
    ky -= 7.0

tx(c, TX0 + 10, TY + 40, "SCREEN CONSTRUCTION", 8.0, "Helvetica-Bold")
for i, ln in enumerate(wrapw(
        "PLANTER IS CONSTRUCTED ON THE MECHANICAL DECK, SET CLEAR OF THE NEC "
        "110.26(A) WORKING SPACE AND CLEAR OF THE EXHAUST DISCHARGE PATH AT THE "
        "EAST END OF THE ENCLOSURE.", KW - 24, size=6.2)):
    tx(c, TX0 + 12, TY + 30 - i * 8.0, ln, 6.2, "Helvetica", GREY)

# --- compliance table (right)
CX = TX0 + KW + 12
CW = TW - KW - 12
box(c, CX, TY, CW, TH, lw=1.3)
tx(c, CX + 12, TY + TH - 17, "CLEARANCE AND ORDINANCE COMPLIANCE", 9.6, "Helvetica-Bold")
line(c, CX + 12, TY + TH - 23, CX + CW - 12, TY + TH - 23, lw=.9, col=ORNG)

COLS = [("SOURCE", 84), ("REQUIREMENT", 234), ("PROVIDED", 220), ("STATUS", 76)]
xs, x = [], CX
for _, w in COLS:
    xs.append(x); x += w
hy = TY + TH - 45
box(c, CX, hy, CW, 17, lw=.9, fill=Color(.90, .90, .90))
for (nm, w), xx in zip(COLS, xs):
    line(c, xx, hy, xx, hy + 17, lw=.6, col=GREY)
    tx(c, xx + 6, hy + 5.4, nm, 6.8, "Helvetica-Bold")

ROWS = [
    ("SEC. 56-41(a)", "MECHANICAL EQUIPMENT INSTALLED WITH NEW CONSTRUCTION MAY NOT "
     "BE LOCATED IN A REQUIRED YARD, REGARDLESS OF HEIGHT OR PROJECTION.",
     "THE GENERATOR IS SET ON THE CONCRETE MECHANICAL DECK OF THE RESIDENCE, "
     "INSIDE THE BUILDING ENVELOPE. NO PORTION OF THE EQUIPMENT IS LOCATED IN THE "
     "REQUIRED FRONT, REAR OR SIDE YARD."),
    ("SEC. 56-41(a)", "ALL NEW MECHANICAL EQUIPMENT MUST BE SCREENED FROM VIEW TO "
     "THE FULL HEIGHT OF THE EQUIPMENT, CONSISTENT WITH FENCING AND LANDSCAPING "
     "REQUIREMENTS AND THE MANUFACTURER'S SPECIFICATIONS.",
     "THE ENCLOSURE IS 3'-10½\" HIGH. LIVE VEGETATION IN THE DECK PLANTER IS "
     "INSTALLED AT NOT LESS THAN 4'-0\" AND MAINTAINED AT NOT LESS THAN THE "
     "FULL HEIGHT OF THE EQUIPMENT. THE PLANTER RUNS ALONG THE FRONT OF THE "
     "DECK PAST THE GENERATOR AND BOTH CONDENSING UNITS."),
    ("SEC. 58-176", "REQUIRED YARDS, R1-10: FRONT 30'-0\", REAR 25'-0\", "
     "SIDE 7'-6\".",
     "THE GENERATOR IS 34'-0\" FROM THE FRONT LOT LINE, 110'-0\" FROM THE REAR "
     "LOT LINE AND 9'-0\" FROM THE EAST SIDE LOT LINE. SEE SHEET SP-1."),
    ("SEC. 56-41(c)", "GENERATORS WITHIN 15 FT OF A PROPERTY LINE SHALL USE PROPANE, "
     "NATURAL GAS OR FUEL WITH SIMILAR EXHAUST IMPACTS. GASOLINE AND DIESEL ARE "
     "PROHIBITED WITHIN 15 FT.",
     "THE GENERATOR IS LP (PROPANE) FIRED, SERVED FROM THE 1,000 GALLON BURIED "
     "PROPANE TANK SHOWN ON SHEET A2."),
    ("SEC. 56-41(d)", "AUTOMATIC CYCLING OF GENERATORS SHALL TAKE PLACE BETWEEN "
     "9:00 A.M. AND 4:00 P.M., MONDAY THROUGH THURSDAY.",
     "THE RDC2 CONTROLLER EXERCISER IS SET FOR TUESDAY AT 11:00 A.M., WITHIN THE "
     "PERMITTED 9:00 A.M. TO 4:00 P.M. MONDAY THROUGH THURSDAY WINDOW."),
    ("NFPA 37 4.1.4", "ENGINES AND THEIR ENCLOSURES INSTALLED OUTDOORS SHALL BE "
     "AT LEAST 5 FT FROM OPENINGS IN WALLS AND AT LEAST 5 FT FROM STRUCTURES "
     "HAVING COMBUSTIBLE WALLS, UNLESS LISTED AND LABELED FOR A LESSER "
     "SEPARATION.",
     "THE ADJACENT WALL IS 8 IN. REINFORCED C.M.U. WITH STUCCO FINISH — "
     "NONCOMBUSTIBLE CONSTRUCTION PER SHEET A3. THE 48RCLC IS LISTED AND "
     "LABELED FOR AN 18 IN. OFFSET AND IS SET AT " + WALL_DIM + " FROM THAT "
     "WALL."),
    ("NEC 110.26(A)(1)(a)", "WORKING SPACE IS NOT REQUIRED IN THE BACK OR SIDES "
     "OF DEAD-FRONT ASSEMBLIES WHERE ALL CONNECTIONS AND ALL RENEWABLE OR "
     "ADJUSTABLE PARTS ARE ACCESSIBLE FROM LOCATIONS OTHER THAN THE BACK OR "
     "SIDES.",
     "ALL CONNECTIONS, THE 200 A LINE CIRCUIT BREAKER AND THE RDC2 CONTROL "
     "PANEL ARE ACCESSIBLE AT THE FRONT FACE OF THE ENCLOSURE. NO WORKING SPACE "
     "IS REQUIRED AT THE BACK OF THE GENERATOR, WHICH FACES THE HOUSE WALL."),
    ("NEC 110.26(A)", "WORKING SPACE AT THE CONTROL PANEL AND LINE CIRCUIT BREAKER: "
     "3'-0\" DEEP, NOT LESS THAN THE WIDTH OF THE EQUIPMENT, ON A LEVEL "
     "LOAD-BEARING SURFACE.",
     "3'-0\" DEEP BY 7'-6\" WIDE AT THE FRONT FACE. THE WORKING SPACE LANDS "
     "WHOLLY ON THE CONCRETE DECK AND IS KEPT CLEAR OF THE PLANTER."),
    ("NEC 445.10 / 430.14", "ALLOW SUFFICIENT ROOM ON ALL SIDES FOR MAINTENANCE AND "
     "SERVICING AND FOR FREE FLOW OF INTAKE AND DISCHARGE AIR WITHOUT "
     "RECIRCULATION.",
     "THE DECK IS 25'-2\" × 9'-4\". " + FRONT_DIM + " IS CLEAR AT THE FRONT OF "
     "THE ENCLOSURE TO THE PLANTER, " + AC_DIM + " TO THE NEAREST CONDENSING "
     "UNIT, AND " + EXH_DIM + " FROM THE EXHAUST DISCHARGE END TO THE END WALL, "
     "INTO OPEN DECK CLEAR OF PLANTING AND EQUIPMENT."),
    ("STRUCTURAL", "THE SUPPORTING DECK CARRIES THE OPERATING WEIGHT OF THE "
     "EQUIPMENT.",
     "THE 48RCLC OPERATING WEIGHT IS 1,690 LB ON A 7'-6\" × 2'-9\" SKID. THE "
     "MECHANICAL DECK IS ENGINEERED FOR THE LIQUID-COOLED UNIT BY THE ENGINEER OF "
     "RECORD."),
    ("FBC / FEMA", "EQUIPMENT ELEVATED ABOVE THE DESIGN FLOOD ELEVATION.",
     "THE SITE IS FLOOD ZONE X PER SHEET A2. THE EQUIPMENT IS SET ON AN ELEVATED "
     "MECHANICAL DECK ABOVE FIRST-FLOOR ELEVATION 12.00' N.A.V.D."),
]

AVAIL = hy - (TY + 26)
for SZ, LH, PAD in ((6.4, 7.6, 7), (6.2, 7.3, 6), (6.0, 7.0, 5.5),
                    (5.8, 6.7, 5), (5.6, 6.4, 4.5), (5.4, 6.1, 4),
                    (5.2, 5.9, 3.5), (5.0, 5.7, 3)):
    hts = [max(len(wrapw(r[1], COLS[1][1] - 13, size=SZ)),
               len(wrapw(r[2], COLS[2][1] - 13, size=SZ))) * LH + PAD for r in ROWS]
    if sum(hts) <= AVAIL:
        break

ry = hy
for (src, req, prov), rh in zip(ROWS, hts):
    rl = wrapw(req, COLS[1][1] - 13, size=SZ)
    pl = wrapw(prov, COLS[2][1] - 13, size=SZ)
    ry -= rh
    for (nm, w), xx in zip(COLS, xs):
        box(c, xx, ry, w, rh, lw=.5, fill=None, stroke=GREY)
    tx_fit(c, xs[0] + 6, ry + rh - 10, src, 6.4, COLS[0][1] - 12)
    yy = ry + rh - 10
    for ln in rl:
        tx(c, xs[1] + 6, yy, ln, SZ); yy -= LH
    yy = ry + rh - 10
    for ln in pl:
        tx(c, xs[2] + 6, yy, ln, SZ); yy -= LH
    tx(c, xs[3] + COLS[3][1] / 2, ry + rh / 2 - 3, "COMPLIES", 7.0,
       "Helvetica-Bold", GRN, "c")
box(c, CX, ry, CW, hy + 17 - ry, lw=1.1)

for i, ln in enumerate(wrapw(
        "SEC. 56-41 AND SEC. 58-176 TEXT PER THE CITY OF NAPLES CODE OF ORDINANCES "
        "(COMP. DEV. CODE 1990, § 9-1-9; CODE 1994, § 110-41; ORD. NO. "
        "06-11495, § 4, 12-20-2006). DECK AND BUILDING DIMENSIONS FROM R.G. "
        "DESIGNS SHEETS A2 AND A8, DATED 1-20-25. GENERATOR DIMENSIONS, WEIGHT AND "
        "THE 18 IN. OFFSET LISTING FROM KOHLER SPECIFICATION G4-306 (48RCLC).",
        CW - 20, size=6.0)):
    tx(c, CX + 8, TY + 20 - i * 7.6, ln, 6.0, "Helvetica-Oblique", GREY)

titleblock(c, W, H, "SP-2", "GENERATOR PLACEMENT, CLEARANCES & MECHANICAL SCREENING",
           margin=M, tbw=TBW, stamp=124)
c.save()
print("wrote", OUT)
print("compliance rows:", len(ROWS), "table bottom y =", round(ry, 1),
      "(must exceed", TY + 26, ")")
assert ry > TY + 26, "compliance table overflows its box"
