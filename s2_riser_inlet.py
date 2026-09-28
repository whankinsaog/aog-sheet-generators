"""Sheet E-1 — riser diagram, PORTABLE GENERATOR INLET + CSED INTERLOCK variant.

THIS COPY IS POPULATED FOR: 123 Example St, Naples FL 34120 (Collier County)

The configuration this script draws (new to the stack, first built on this job):
  * EXISTING 200 A Square D Homeline RC-series meter-main (CSED). Its 200 A main is the
    service disconnect and the 230.85 emergency disconnect.
  * NEW inside that meter-main: RCGK2 generator interlock kit, a 50 A 2-pole HOM
    backfed generator breaker in positions 2 & 4 (nearest the service
    disconnect, per Square D bulletin 40273-480-02), a 100 A 2-pole HOM feeding
    a new sub panel, and a Homeline SurgeBreaker plug-in SPD (230.67).
  * NEW 50 A power inlet (Connecticut Electric EGSPI50) beside the meter-main.
  * NEW 100 A NEMA 3R sub panel; the EXISTING pool panel feeder (conductors
    and raceway) is re-terminated on its 60 A 2-pole, so 2 & 4 are free.
  * EXISTING Panel A (200 A ML, indoors) and its 2/0 CU feeder — not altered.
  * Portable generator — BY OWNER, drawn dotted grey, not part of the permit.

What is deliberately NOT on this sheet, and why:
  * No load calc — manual transfer, the user selects the load, NEC 702.4(B)(1).
  * No emergency shutdown — 445.18(D) (2020) exempts cord-and-plug-connected
    portable generators.
  * No ATS, no generator feeder schedule, no load shed.

Three states, legended: solid red = new this permit; dashed black = existing
to remain; dotted grey = by owner, not part of this permit.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, black, white
from reportlab.pdfbase.pdfmetrics import stringWidth
from aoglib import (tx, box, line, titleblock, GREY, JOB, FBC_EDITION,
                    NEC_EDITION)

W, H = 1224.0, 792.0
RED = Color(.78, .05, .09)
ORNG = Color(.76, .38, .08)
OWN = Color(.55, .55, .55)
TBW, M = 250, 18

OUT = "out/E-1 Riser Diagram - 123 Example St.pdf"
c = canvas.Canvas(OUT, pagesize=(W, H))
box(c, M, M, W - 2 * M, H - 2 * M, lw=1.6)
PLACED = []          # (x0, y0, x1, y1, name) of every tag, for collision asserts


def wrapw(text, maxw, font="Helvetica", size=6.4):
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


def equip(x, y, w, h, lines, state="existing", top_pad=12):
    """state: 'new' solid red · 'existing' dashed black · 'owner' dotted grey"""
    c.saveState()
    c.setFillColor(white)
    col = {"new": RED, "existing": black, "owner": OWN}[state]
    c.setStrokeColor(col)
    c.setLineWidth({"new": 2.0, "existing": 1.0, "owner": 1.2}[state])
    if state == "existing":
        c.setDash(3, 2)
    elif state == "owner":
        c.setDash(1.2, 2.4)
    c.rect(x, y, w, h, stroke=1, fill=1)
    c.restoreState()
    yy = y + h - top_pad
    for i, (s, sz, bold) in enumerate(lines):
        if i:
            yy -= sz + 2.4          # step by THIS line's size so a big line
        fc = RED if (state == "new" and bold and i == 0) else (   # never rides
            OWN if state == "owner" else black)                  # up into a small one
        tx(c, x + w / 2, yy, s, sz, "Helvetica-Bold" if bold else "Helvetica", fc, "c")
    assert yy > y + 2, "equipment text overruns its box: %r" % (lines[:2],)
    return x, y, x + w, y + h


def conn(x1, y1, x2, y2, lw=2.0, state="existing", dash=None):
    c.saveState()
    c.setStrokeColor({"new": RED, "existing": black, "owner": OWN}[state])
    c.setLineWidth(lw)
    if dash:
        c.setDash(dash)
    elif state == "existing":
        c.setDash(3, 2)
    elif state == "owner":
        c.setDash(1.2, 2.4)
    c.line(x1, y1, x2, y2)
    c.restoreState()


def tag(x, y, s, new=False, size=6.4, name=""):
    ls = s.split("\n")
    ww = max(stringWidth(l, "Helvetica-Bold" if new else "Helvetica", size)
             for l in ls) + 13
    hh = len(ls) * (size + 2.6) + 7
    box(c, x, y, ww, hh, lw=.9, fill=white, stroke=RED if new else GREY)
    yy = y + hh - size - 3.5
    for l in ls:
        tx(c, x + 6.5, yy, l, size, "Helvetica-Bold" if new else "Helvetica",
           RED if new else black)
        yy -= size + 2.6
    PLACED.append((x, y, x + ww, y + hh, name))
    return ww, hh


def overlaps(a, b, pad=2):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or
                a[3] + pad <= b[1] or b[3] + pad <= a[1])


# ================================================================== header
tx(c, M + 12, H - M - 24, "ELECTRICAL RISER DIAGRAM", 16, "Helvetica-Bold")
tx(c, M + 12, H - M - 38, "N.T.S.   ·   PORTABLE GENERATOR POWER INLET WITH A LISTED "
                          "INTERLOCK IN THE EXISTING 200 A METER-MAIN. MANUAL "
                          "TRANSFER — NO AUTOMATIC TRANSFER SWITCH.",
   8, "Helvetica-Oblique", GREY)
line(c, M + 12, H - M - 45, 956, H - M - 45, lw=.9, col=ORNG)

lx = 716
for i, (st, lbl) in enumerate([("new", "NEW — THIS PERMIT"),
                               ("existing", "EXISTING TO REMAIN"),
                               ("owner", "BY OWNER — NOT PART OF THIS PERMIT")]):
    yy = H - M - 30 - 14 * i
    c.saveState()
    c.setStrokeColor({"new": RED, "existing": black, "owner": OWN}[st])
    c.setLineWidth({"new": 2.0, "existing": 1.0, "owner": 1.2}[st])
    if st == "existing":
        c.setDash(3, 2)
    elif st == "owner":
        c.setDash(1.2, 2.4)
    c.rect(lx, yy, 20, 11, stroke=1, fill=0)
    c.restoreState()
    tx(c, lx + 26, yy + 3, lbl, 7.5, "Helvetica-Bold" if st != "existing" else "Helvetica",
       {"new": RED, "existing": black, "owner": OWN}[st])

# ============================================================ meter-main
MMX, MMY, MMW, MMH = 140.0, 300.0, 196.0, 330.0
equip(MMX, MMY, MMW, MMH, [("EXISTING", 6.4, False),
                           ("200 A METER-MAIN", 11, True),
                           ("SQUARE D HOMELINE CSED", 6.6, False),
                           ("120/240V 1Ø 3W  ·  NEMA 3R", 6.2, False)])
# meter socket glyph
c.saveState(); c.setStrokeColor(black); c.setLineWidth(1.0)
c.circle(MMX + MMW / 2, MMY + MMH - 88, 28, stroke=1, fill=0)
c.rect(MMX + MMW / 2 - 16, MMY + MMH - 80, 32, 10, stroke=1, fill=0)
c.restoreState()
tx(c, MMX + MMW / 2, MMY + MMH - 128, "FPL METER", 6.2, "Helvetica", GREY, "c")
line(c, MMX + 8, MMY + MMH - 138, MMX + MMW - 8, MMY + MMH - 138, lw=.6, col=GREY,
     dash=(2, 2))

# main breaker (existing) + the new devices inside the meter-main
MBX, MBY, MBW, MBH = MMX + 12, MMY + 128, 70, 50
equip(MBX, MBY, MBW, MBH, [("EXISTING", 5.4, False), ("200 A", 9.4, True),
                           ("MAIN BREAKER", 5.8, True),
                           ("SERVICE DISC.", 5.4, False)], top_pad=10)
QKX, QKY, QKW, QKH = MMX + 94, MMY + 128, 90, 50
equip(QKX, QKY, QKW, QKH, [("NEW", 5.8, True), ("RCGK2 INTERLOCK", 6.8, True),
                           ("UTILITY MAIN OR GEN", 5.4, False),
                           ("BREAKER — ONE ON", 5.4, False)], state="new", top_pad=10)
# interlock bar across main breaker and generator breaker
c.saveState(); c.setStrokeColor(RED); c.setLineWidth(1.4); c.setDash(4, 2)
c.line(MBX + MBW, MBY + MBH / 2, QKX, QKY + QKH / 2); c.restoreState()

DEV = [  # (label lines, x) — plug-in devices in the meter-main branch section
    ([("NEW", 5.4, True), ("50 A 2P", 7.4, True), ("HOM BACKFED", 5.2, False),
      ("GEN · SP 2 & 4", 5.2, False)], MMX + 12),
    ([("NEW", 5.4, True), ("100 A 2P", 7.4, True), ("HOM", 5.2, False),
      ("SUB PANEL", 5.2, False)], MMX + 72),
    ([("NEW", 5.4, True), ("SPD", 7.4, True), ("HOM SURGE-", 5.2, False),
      ("BREAKER", 5.2, False)], MMX + 132),
]
DVY, DVW, DVH = MMY + 62, 52, 52
DEVBOX = []
for lines, dx in DEV:
    DEVBOX.append(equip(dx, DVY, DVW, DVH, lines, state="new", top_pad=10))
tx(c, MMX + 52, MMY + 50, "230.67 — SPD ON THE DWELLING SERVICE", 5.6,
   "Helvetica-Bold", RED, "l")
tx(c, MMX + 52, MMY + 40, "408.36(D) — BACKFED BREAKER SECURED", 5.6,
   "Helvetica-Bold", RED, "l")
tx(c, MMX + 52, MMY + 30, "702.5 — LISTED INTERLOCK TRANSFER", 5.6,
   "Helvetica-Bold", RED, "l")
tx(c, MMX + MMW / 2, MMY + 14, "ALL NEW DEVICES ARE INSIDE THE", 5.4,
   "Helvetica-Oblique", GREY, "c")
tx(c, MMX + MMW / 2, MMY + 6, "EXISTING METER-MAIN ENCLOSURE", 5.4,
   "Helvetica-Oblique", GREY, "c")

# 230.85 emergency disconnect marking, on the main breaker
_mk = ["EMERGENCY DISCONNECT,", "SERVICE DISCONNECT"]
_mw = max(stringWidth(t, "Helvetica-Bold", 6.0) for t in _mk) + 14
EDX, EDY = 30.0, MBY + 12
box(c, EDX, EDY, _mw, 25, lw=1.1, fill=white, stroke=RED)
for _i, _t in enumerate(_mk):
    tx(c, EDX + _mw / 2, EDY + 16 - _i * 8.4, _t, 6.0, "Helvetica-Bold", RED, "c")
tx(c, EDX + _mw / 2, EDY - 9, "NEC 230.85(1) · 110.21(B)", 5.8, "Helvetica-Bold", RED, "c")
conn(EDX + _mw, EDY + 12, MBX, EDY + 12, lw=.8, state="new")
assert EDX + _mw < MMX, "emergency disconnect marking overlaps the meter-main"

# utility service
conn(M + 8, MMY + MMH - 88, MMX, MMY + MMH - 88, lw=2.4, state="existing", dash=None)
tx(c, M + 12, MMY + MMH - 80, "FPL SERVICE", 6.6, "Helvetica-Bold")
tx(c, M + 12, MMY + MMH - 100, "EXISTING, NOT", 6.0, "Helvetica", GREY)
tx(c, M + 12, MMY + MMH - 108, "ALTERED", 6.0, "Helvetica", GREY)

# ============================================================ sub panel + pool
SPX, SPY, SPW, SPH = 392.0, 470.0, 120.0, 110.0
equip(SPX, SPY, SPW, SPH, [("NEW", 7.0, True), ("100 A SUB PANEL", 9.2, True),
                           ("NEMA 3R  ·  120/240V 1Ø", 6.2, False),
                           ("NEUTRAL ISOLATED,", 6.0, False),
                           ("EGC BAR BONDED", 6.0, False), ("", 4, False),
                           ("60 A 2P — POOL PANEL", 6.6, True)], state="new")
PPX, PPY, PPW, PPH = 568.0, 470.0, 104.0, 110.0
equip(PPX, PPY, PPW, PPH, [("EXISTING", 6.4, False), ("POOL PANEL", 9.2, True),
                           ("100 A", 9, True), ("120/240V 1Ø", 6.2, False),
                           ("NOT ALTERED", 6.0, False)])

# 100 A feeder: meter-main 100 A device -> sub panel (new)
F1Y = 450.0
d100 = DEVBOX[1]
f1x = (d100[0] + d100[2]) / 2
# route: up out of the 100 A device is blocked by the main/RCGK2 row, so leave
# the meter-main's right wall at F1Y and drop into the sub panel's left side
conn(MMX + MMW, F1Y, SPX + 30, F1Y, lw=2.0, state="new")
conn(SPX + 30, F1Y, SPX + 30, SPY, lw=2.0, state="new")
conn(f1x, DVY + DVH, f1x, DVY + DVH + 8, lw=1.4, state="new")
tx(c, f1x + 4, DVY + DVH + 2, "", 5)
_w, _h = tag(346, 590, "SUB PANEL FEEDER — 100 A\n(3) #3 AWG CU or (3) #1 AWG AL\n"
                       "EGC: #8 AWG CU or #6 AWG AL\n1¼\" PVC", new=True, name="f100")
conn(360, 590, 360, F1Y, lw=.8, state="new", dash=(2, 2))

# 60 A pool feeder: EXISTING conductors and raceway, re-terminated on the new
# sub panel's 60 A 2-pole. Drawn existing (dashed black), shown as installed.
F2Y = 440.0
conn(SPX + SPW - 30, SPY, SPX + SPW - 30, F2Y, lw=2.0, state="existing")
conn(SPX + SPW - 30, F2Y, PPX + PPW / 2, F2Y, lw=2.0, state="existing")
conn(PPX + PPW / 2, F2Y, PPX + PPW / 2, PPY, lw=2.0, state="existing")
_w2, _h2 = tag(520, 382, "EXISTING POOL PANEL FEEDER — 60 A\n"
                         "(3) #6 AWG CU · EGC #8 AWG CU · 1\" PVC\n"
                         "(AS INSTALLED) — RE-TERMINATED ON THE\n"
                         "NEW SUB PANEL 60 A 2P", name="f60")
conn(590, 382 + _h2, 590, F2Y, lw=.8, state="existing", dash=(2, 2))

# ============================================================ indoor / Panel A
WALLX = 704.0
c.saveState(); c.setStrokeColor(black); c.setLineWidth(1.2); c.setDash([10, 3, 2, 3])
c.line(WALLX, 180, WALLX, 690); c.restoreState()
tx(c, WALLX - 8, 682, "OUTDOOR", 8, "Helvetica-Bold", anchor="r")
tx(c, WALLX + 8, 682, "INDOOR", 8, "Helvetica-Bold")
PAX, PAY, PAW, PAH = 790.0, 420.0, 130.0, 200.0
equip(PAX, PAY, PAW, PAH, [("EXISTING", 6.4, False), ("PANEL A", 10, True),
                           ("200 A MAIN LUG", 8.6, True), ("120/240V 1Ø", 6.2, False),
                           ("NOT ALTERED", 6.0, False)])
F3Y = 330.0
conn(MMX + MMW, F3Y, PAX + PAW / 2, F3Y, lw=2.2, state="existing")
conn(PAX + PAW / 2, F3Y, PAX + PAW / 2, PAY, lw=2.2, state="existing")
_w3, _h3 = tag(740, 262, "EXISTING PANEL A FEEDER — NOT ALTERED\n"
                         "(3) 2/0 AWG CU · EGC #6 AWG CU\n2\" PVC (AS INSTALLED)",
               name="fA")
conn(760, 262 + _h3, 760, F3Y, lw=.8, state="existing", dash=(2, 2))

# ============================================================ inlet + portable gen
INX, INY, INW, INH = 392.0, 236.0, 126.0, 84.0
equip(INX, INY, INW, INH, [("NEW", 7.0, True), ("50 A POWER INLET", 8.6, True),
                           ("CONNECTICUT ELECTRIC", 6.0, False),
                           ("EGSPI50 · CS6375", 6.2, False),
                           ("125/250V · NEMA 3R", 6.2, False),
                           ("OUTDOOR, BESIDE METER", 6.0, False)], state="new")
d50 = DEVBOX[0]
g50x = (d50[0] + d50[2]) / 2
F4Y = 278.0
conn(g50x, DVY, g50x, MMY, lw=2.0, state="new")
conn(g50x, MMY, g50x, F4Y, lw=2.0, state="new")
conn(g50x, F4Y, INX, F4Y, lw=2.0, state="new")
_w4, _h4 = tag(196, 240, "INLET CIRCUIT — 50 A\n(3) #8 AWG CU or (3) #6 AWG AL\n"
                         "EGC: #10 AWG CU or #8 AWG AL\n¾\" PVC", new=True, name="f50")

# 702.7(C) sign at the inlet
SGX, SGY = INX + 4, INY - 44
_sg = ["WARNING: FOR CONNECTION OF A NONSEPARATELY", "DERIVED (FLOATING NEUTRAL) SYSTEM ONLY"]
_sgw = max(stringWidth(t, "Helvetica-Bold", 5.6) for t in _sg) + 12
box(c, SGX, SGY, _sgw, 22, lw=1.1, fill=white, stroke=RED)
for _i, _t in enumerate(_sg):
    tx(c, SGX + _sgw / 2, SGY + 14 - _i * 7.6, _t, 5.6, "Helvetica-Bold", RED, "c")
tx(c, SGX + _sgw / 2, SGY - 9, "SIGN AT THE INLET — NEC 702.7(C)", 5.8,
   "Helvetica-Bold", RED, "c")
conn(SGX + 20, SGY + 22, SGX + 20, INY, lw=.8, state="new")

PGX, PGY, PGW, PGH = 572.0, 236.0, 118.0, 84.0
equip(PGX, PGY, PGW, PGH, [("BY OWNER", 6.6, True), ("PORTABLE", 8.6, True),
                           ("GENERATOR", 8.6, True),
                           ("120/240V · 50 A MAX", 6.2, False),
                           ("FLOATING NEUTRAL", 6.2, False),
                           ("NOT PART OF THIS PERMIT", 5.6, False)], state="owner")
conn(INX + INW, F4Y, PGX, F4Y, lw=1.6, state="owner")
tx(c, (INX + INW + PGX) / 2, F4Y + 5, "50 A CORD SET", 5.8, "Helvetica-Bold", OWN, "c")
tx(c, (INX + INW + PGX) / 2, F4Y - 10, "BY OWNER", 5.6, "Helvetica", OWN, "c")

# ============================================================== grounding
GECX, GRY = 150.0, 214.0
conn(GECX, MMY, GECX, GRY, lw=1.6, state="existing")
for gx in (GECX,):
    c.saveState(); c.setStrokeColor(black); c.setLineWidth(1.6)
    c.line(gx, GRY, gx, GRY - 10)
    for j, ww in enumerate((17, 11, 5)):
        c.line(gx - ww, GRY - 10 - j * 5, gx + ww, GRY - 10 - j * 5)
    c.restoreState()
tx(c, GECX - 20, GRY - 36, "EXISTING GROUNDING ELECTRODE", 6.2, "Helvetica-Bold")
tx(c, GECX - 20, GRY - 45, "SYSTEM PER NEC 250.50 — NOT ALTERED", 6.2)
IBX, IBY = 44.0, 260.0
equip(IBX, IBY, 78, 26, [("EXISTING IBT", 6.2, True), ("NEC 250.94", 5.8, False)],
      top_pad=10)
conn(IBX + 78, IBY + 13, GECX, IBY + 13, lw=.9, state="existing")

# ------------------------------------------------ collision asserts
EQUIP = [(MMX, MMY, MMX + MMW, MMY + MMH, "meter-main"),
         (SPX, SPY, SPX + SPW, SPY + SPH, "sub panel"),
         (PPX, PPY, PPX + PPW, PPY + PPH, "pool panel"),
         (PAX, PAY, PAX + PAW, PAY + PAH, "panel A"),
         (INX, INY, INX + INW, INY + INH, "inlet"),
         (PGX, PGY, PGX + PGW, PGY + PGH, "portable gen"),
         (SGX, SGY - 12, SGX + _sgw, SGY + 22, "702.7C sign")]
for t in PLACED:
    for e in EQUIP:
        assert not overlaps(t, e), "tag %s hits %s" % (t[4], e[4])
    for u in PLACED:
        if u is not t:
            assert not overlaps(t, u), "tag %s hits tag %s" % (t[4], u[4])
    assert t[2] < 956 and t[1] > 180, "tag %s off the drawing field" % t[4]
    assert not (t[0] < WALLX < t[2]), "tag %s crosses the outdoor/indoor line" % t[4]
for i, e in enumerate(EQUIP):
    for f in EQUIP[i + 1:]:
        assert not overlaps(e, f), "%s overlaps %s" % (e[4], f[4])

# ================================================================== notes
NX, NY, NW, NH = 636.0, 40.0, 320.0, 136.0
RX, RW = 40.0, 584.0

NOTES = [
    "ALL WORK IS IN ACCORDANCE WITH %s, THE %s AND THE MANUFACTURERS' "
    "INSTALLATION INSTRUCTIONS." % (NEC_EDITION, FBC_EDITION),
    "TRANSFER IS BY A SQUARE D RCGK2 GENERATOR INTERLOCK KIT, UL LISTED FOR THE "
    "EXISTING HOMELINE RC-SERIES METER-MAIN, WHICH PERMITS ONLY ONE OF THE 200 A MAIN "
    "BREAKER AND THE 50 A GENERATOR BREAKER TO BE ON AT ANY TIME, PREVENTING "
    "INTERCONNECTION OF THE SOURCES PER NEC 702.5. INSTALLED PER SQUARE D "
    "BULLETIN 40273-480-02: THE 2-POLE HOM GENERATOR BREAKER OCCUPIES POSITIONS "
    "2 AND 4 NEAREST THE SERVICE DISCONNECT.",
    "THE BACKFED 50 A GENERATOR BREAKER IS SECURED IN PLACE BY AN ADDITIONAL "
    "FASTENER THAT REQUIRES OTHER THAN A PULL TO RELEASE IT, PER NEC 408.36(D).",
    "TRANSFER IS MANUAL. THE USER SELECTS THE LOAD CONNECTED TO THE OPTIONAL "
    "STANDBY SYSTEM PER NEC 702.4(B)(1).",
    "THE INTERLOCK DOES NOT SWITCH THE NEUTRAL. THE PORTABLE GENERATOR IS A "
    "NONSEPARATELY DERIVED (FLOATING NEUTRAL) SOURCE WITH ITS NEUTRAL BONDED "
    "ONLY AT THE SERVICE. THE INLET CARRIES THE NEC 702.7(C) WARNING SIGN.",
    "A SIGN AT THE SERVICE EQUIPMENT GIVES THE TYPE AND LOCATION OF THE OPTIONAL "
    "STANDBY POWER SOURCE (THE POWER INLET), PER NEC 702.7(A).",
    "THE EXISTING 200 A MAIN BREAKER IN THE METER-MAIN IS OUTDOORS, READILY "
    "ACCESSIBLE AND MARKED “EMERGENCY DISCONNECT, SERVICE DISCONNECT” PER "
    "NEC 230.85(1). MARKING COMPLIES WITH NEC 110.21(B).",
    "A SQUARE D HOMELINE SURGEBREAKER PLUG-IN SURGE PROTECTIVE DEVICE IS INSTALLED IN "
    "THE METER-MAIN PER NEC 230.67.",
    "THE NEW SUB PANEL HAS ITS NEUTRAL ISOLATED FROM THE ENCLOSURE AND ITS "
    "EQUIPMENT GROUNDING BAR BONDED, PER NEC 250.24(A)(5) AND 250.142(B). AN "
    "EQUIPMENT GROUNDING CONDUCTOR IS RUN WITH EVERY NEW CIRCUIT PER NEC 250.122.",
    "EVERY NEW CONDUCTOR CALLOUT GIVES A COPPER AND AN ALUMINUM SIZE; CONDUIT IS "
    "SIZED FOR THE ALUMINUM CONDUCTOR. EXISTING CONDUCTORS ARE SHOWN AS INSTALLED.",
    "NO EMERGENCY SHUTDOWN DEVICE IS INSTALLED: NEC 445.18(D) EXCLUDES "
    "CORD-AND-PLUG-CONNECTED PORTABLE GENERATORS.",
]
for _n in NOTES:
    for _bad in ("field verify", "verify", "confirm", "t.b.d", "to be determined"):
        assert _bad not in _n.lower(), "hedge %r in a note" % _bad
    for _ch in _n:
        _ch.encode("cp1252")

# notes run in three boxes across the foot of the sheet
def draw_notes(bx, by, bw, bh, title, items, start):
    box(c, bx, by, bw, bh, lw=1.2)
    tx(c, bx + 10, by + bh - 17, title, 9.6, "Helvetica-Bold")
    line(c, bx + 10, by + bh - 23, bx + bw - 10, by + bh - 23, lw=.9, col=ORNG)
    for SZ, LH in ((6.6, 7.9), (6.4, 7.6), (6.2, 7.3), (6.0, 7.0), (5.8, 6.7),
                   (5.6, 6.4), (5.4, 6.1)):
        blocks = [wrapw(n, bw - 44, size=SZ) for n in items]
        R = max(4.6, SZ * 0.92)
        if sum(max(len(b) * LH + 5.5, 2 * R + 4) for b in blocks) \
                <= (by + bh - 36) - (by + 8):
            break
    R = max(4.6, SZ * 0.92)
    yy = by + bh - 36
    for i, blk in enumerate(blocks):
        c.saveState(); c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(.9)
        c.circle(bx + 18, yy - 2, R, stroke=1, fill=1); c.restoreState()
        tx(c, bx + 18, yy - 2 - SZ * 0.34, str(start + i), SZ * 0.98,
           "Helvetica-Bold", black, "c")
        top = yy
        for ln in blk:
            tx(c, bx + 31, yy, ln, SZ); yy -= LH
        yy = min(yy - 5.5, top - (2 * R + 4))
    assert yy > by + 4, "%s overrun their box (y=%.1f)" % (title, yy)
    return yy


BH = 124.0
ya = draw_notes(40.0, NY, 290.0, BH, "GENERAL NOTES", NOTES[0:3], 1)
yb = draw_notes(338.0, NY, 290.0, BH, "GENERAL NOTES (CONT.)", NOTES[3:7], 4)
yc = draw_notes(NX, NY, NW, NH, "GENERAL NOTES (CONT.)", NOTES[7:], 8)
assert NY + BH < 180 and NY + NH < 236, "a notes box rises into the drawing field"
ly, ry = min(ya, yb), yc

titleblock(c, W, H, "E-1", "ELECTRICAL RISER DIAGRAM", margin=M, tbw=TBW, stamp=124)
c.save()
print("wrote", OUT, "| left notes y", round(ly, 1), "| right notes y", round(ry, 1))
