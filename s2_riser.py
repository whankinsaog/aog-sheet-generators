"""Sheet E-1 — generator riser diagram.

THIS COPY IS POPULATED FOR: 614 5th Ave. N, Naples FL 34102

Correction response: the GENERATOR changes from a Generac 48 kW to a KOHLER
48RCLC. This is NOT a revision to an issued permit — the application was kicked
back and the make was changed as part of answering the comments.
Everything else on the service is EXISTING and is not altered — the 600 A
meter, the 600 A service disconnect, the Generac 600 A automatic transfer
switch, the MDP and all branch panels.

Two drafting rules this sheet enforces, both from Brandon:
 1. Each branch panel gets its OWN raceway from its OWN overcurrent device.
    A single horizontal line touching every panel reads as one shared
    raceway, which is wrong when the panels come off 200/150/150/100 A
    breakers. Feeders drop out of the MDP at four separate points, run at
    four separate levels and rise into their own panel.
 2. The grounding electrode conductor leaves the METER enclosure, and the
    emergency shutdown is AT the meter.
 3. The OCPD label sits at the PANEL end of its own run, not in the drop
    cluster at the MDP — four labels stacked at the MDP read as one bank.
 4. Load-shed modules do NOT belong on the riser when the job uses standalone
    PSP SAK-60 under-frequency relays: they are wired inline at each managed
    load, not in the generator's own one-line.

Three equipment states, and the legend carries all three: solid red = new
under this permit; DASHED RED = new, but furnished and set by others (the
Kohler KUS-600 transfer switch here); dashed black = existing to remain.
"Existing" and "new by others" are not the same thing, and Brandon will catch
a sheet that draws a contractor-furnished new switch as existing.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, black, white
from reportlab.pdfbase.pdfmetrics import stringWidth
from aoglib import (tx, box, line, wrap, titleblock, GREY, JOB, CORRECTION,
                    FBC_EDITION, NEC_EDITION, note)

W, H = 1224.0, 792.0
RED = Color(.78, .05, .09)
ORNG = Color(.76, .38, .08)
TBW, M = 250, 18

OUT = "out/E-1 Riser Diagram - 614 5th Ave N.pdf"
c = canvas.Canvas(OUT, pagesize=(W, H))
box(c, M, M, W - 2 * M, H - 2 * M, lw=1.6)


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


def equip(x, y, w, h, lines, new=False, byothers=False):
    """new=solid red (this permit); byothers=dashed red (new, set by others);
    neither=dashed black (existing to remain)."""
    c.saveState()
    c.setFillColor(white)
    c.setStrokeColor(RED if (new or byothers) else black)
    c.setLineWidth(2.0 if new else (1.6 if byothers else 1.0))
    if byothers:
        c.setDash(6, 3)
    elif not new:
        c.setDash(3, 2)
    c.rect(x, y, w, h, stroke=1, fill=1)
    c.restoreState()
    yy = y + h - 12
    for i, (s, sz, bold) in enumerate(lines):
        tx(c, x + w / 2, yy, s, sz, "Helvetica-Bold" if bold else "Helvetica",
           RED if ((new or byothers) and bold and i == 0) else black, "c")
        yy -= sz + 2.0


def conn(x1, y1, x2, y2, lw=2.0, new=False, dash=None, col=None):
    c.saveState()
    c.setStrokeColor(col or (RED if new else black))
    c.setLineWidth(lw)
    if dash:
        c.setDash(dash)
    c.line(x1, y1, x2, y2)
    c.restoreState()


def tag(x, y, s, new=False, size=6.4):
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
    return ww, hh


# ================================================================== header
tx(c, M + 12, H - M - 24, "ELECTRICAL RISER DIAGRAM", 16, "Helvetica-Bold")
tx(c, M + 12, H - M - 38, "N.T.S.   ·   " + CORRECTION + " GENERATOR CHANGED FROM "
                          "GENERAC TO KOHLER. THE TRANSFER SWITCH IS NEW, BY OTHERS. "
                          "THE SERVICE, MDP AND ALL PANELS ARE EXISTING.",
   8, "Helvetica-Oblique", GREY)
line(c, M + 12, H - M - 45, 956, H - M - 45, lw=.9, col=ORNG)

lx = 726
c.saveState(); c.setStrokeColor(RED); c.setLineWidth(2.0)
c.rect(lx, H - M - 30, 20, 11, stroke=1, fill=0); c.restoreState()
tx(c, lx + 26, H - M - 27, "NEW — THIS PERMIT", 7.5, "Helvetica-Bold", RED)
c.saveState(); c.setStrokeColor(RED); c.setLineWidth(1.6); c.setDash(6, 3)
c.rect(lx, H - M - 44, 20, 11, stroke=1, fill=0); c.restoreState()
tx(c, lx + 26, H - M - 41, "NEW — INSTALLED BY OTHERS", 7.5, "Helvetica-Bold", RED)
c.saveState(); c.setStrokeColor(black); c.setLineWidth(1.0); c.setDash(3, 2)
c.rect(lx, H - M - 58, 20, 11, stroke=1, fill=0); c.restoreState()
tx(c, lx + 26, H - M - 55, "EXISTING TO REMAIN", 7.5, "Helvetica")

# ============================================================ service row
SY = 560.0

equip(40, SY, 104, 86, [("EXISTING", 6.4, False), ("600 A", 12, True),
                        ("METER", 9, True), ("120/240V 1Ø 3W", 6.4, False),
                        ("FLORIDA POWER", 6.0, False), ("& LIGHT", 6.0, False)])

DSCX, DSCW = 186.0, 108.0
equip(DSCX, SY - 6, DSCW, 98, [("EXISTING", 6.4, False), ("600 A", 11, True),
                               ("SERVICE", 8.6, True), ("DISCONNECT", 8.6, True),
                               ("SERVICE DISCONNECTING", 5.8, False),
                               ("MEANS", 5.8, False)])
# NEC 230.85 marking — the service disconnect is the emergency disconnect
_mk = ["EMERGENCY DISCONNECT,", "SERVICE DISCONNECT"]
_mw = max(stringWidth(t, "Helvetica-Bold", 6.0) for t in _mk) + 14
conn(DSCX + DSCW / 2, SY - 6, DSCX + DSCW / 2, SY - 23, lw=.8, col=RED)
box(c, DSCX + DSCW / 2 - _mw / 2, SY - 48, _mw, 25, lw=1.1, fill=white, stroke=RED)
for _i, _t in enumerate(_mk):
    tx(c, DSCX + DSCW / 2, SY - 32 - _i * 8.4, _t, 6.0, "Helvetica-Bold", RED, "c")
tx(c, DSCX + DSCW / 2, SY - 57, note("emerg_disc_tag"), 6.0,
   "Helvetica-Bold", RED, "c")

ATSX, ATSW = 334.0, 132.0
equip(ATSX, SY - 14, ATSW, 114, [
    ("NEW — BY OTHERS", 6.2, True), ("KOHLER KUS-600", 9.8, True),
    ("600 A AUTOMATIC", 7.8, True), ("TRANSFER SWITCH", 7.8, True),
    ("120/240V 1Ø · SOLID NEUTRAL", 6.0, False),
    ("UL 1008 LISTED", 6.0, False),
    ("ON THE LOAD SIDE OF THE", 5.8, False),
    ("SERVICE DISCONNECT", 5.8, False)], byothers=True)

MDPX, MDPW = 506.0, 122.0
equip(MDPX, SY - 44, MDPW, 144, [
    ("EXISTING", 6.4, False), ("NEMA 3R MDP", 9.6, True), ("600 A", 9, True),
    ("120/240V 1Ø · 22 kAIC", 6.0, False), ("", 4, False),
    ("150 A  ·  100 A", 6.4, False), ("150 A  ·  200 A", 6.4, False)])

# ---- service run, all existing
conn(144, SY + 43, DSCX, SY + 43, lw=2.2)
conn(DSCX + DSCW, SY + 43, ATSX, SY + 43, lw=2.2)
conn(ATSX + ATSW, SY + 43, MDPX, SY + 43, lw=2.2)
_w1, _h1 = tag(46, 676, "EXISTING SERVICE CONDUCTORS, NOT ALTERED — (2) SETS: "
                        "(3) 350 MCM CU,\nEGC: #1 AWG CU  ·  3\" PVC EACH SET")
conn(46 + _w1 / 2, 676, 165, SY + 43, lw=.8, col=GREY)

# ================================================= branch panels and feeders
# One raceway per panel, off its own overcurrent device. Four drop points on
# the MDP, four run levels, four risers — nothing is shared.
# (name, ocpd, panel x, run level, drop x off the MDP, feeder spec)
# Levels descend with distance so no two raceways ever cross: the nearest
# panel takes the highest level. Drop points all sit inside the MDP footprint.
PANELS = [
    ("PANEL A", "200 A", 668.0, 500.0, 560.0, "(3) 3/0 AWG CU · EGC #6 AWG CU · 2\" PVC"),
    ("PANEL B", "150 A", 740.0, 484.0, 578.0, "(3) 1/0 AWG CU · EGC #6 AWG CU · 2\" PVC"),
    ("PANEL C", "150 A", 812.0, 468.0, 596.0, "(3) 1/0 AWG CU · EGC #6 AWG CU · 2\" PVC"),
    ("PANEL P", "100 A", 884.0, 452.0, 614.0, "(3) #3 AWG CU · EGC #8 AWG CU · 1¼\" PVC"),
]
PW = 62.0
assert all(MDPX < d < MDPX + MDPW for _, _, _, _, d, _ in PANELS), \
    "a feeder drop is not on the MDP"
assert len({l for _, _, _, l, _, _ in PANELS}) == len(PANELS), \
    "two feeders share a run level — they would read as one raceway"
OCPD_LABELS = []
for nm, amp, px, lvl, dropx, _spec in PANELS:
    equip(px, SY + 8, PW, 66, [("EXISTING", 5.6, False), (nm, 8.2, True),
                               (amp, 8.2, True), ("120/240V 1Ø", 5.6, False)])
    cx = px + PW / 2
    # drop out of the MDP, run at this feeder's own level, rise into the panel
    conn(dropx, SY - 44, dropx, lvl, lw=1.3, dash=(3, 2))
    conn(dropx, lvl, cx, lvl, lw=1.3, dash=(3, 2))
    conn(cx, lvl, cx, SY + 8, lw=1.3, dash=(3, 2))
    # OCPD rating sits near the PANEL END of its own horizontal run, not back
    # at the drop. Bunched at the drops the four labels stack on top of one
    # another and stop reading against the raceway they belong to; parked just
    # short of each panel riser they stagger into a clean diagonal, one label
    # per raceway, and every one of them clears the drop cluster.
    mid = cx - 34
    box(c, mid - 15, lvl + 2, 30, 11, lw=.7, fill=white, stroke=GREY)
    tx(c, mid, lvl + 5, amp, 5.8, "Helvetica-Bold", anchor="c")
    OCPD_LABELS.append((mid - 15, mid + 15, lvl))

_DROPS = [d for _, _, _, _, d, _ in PANELS]
_RISERS = [p + PW / 2 for _, _, p, _, _, _ in PANELS]
for _x0, _x1, _lv in OCPD_LABELS:
    assert _x0 > max(_DROPS) + 2, "an OCPD label is back in the drop cluster"
    assert not any(_x0 - 3 < r < _x1 + 3 for r in _RISERS), \
        "an OCPD label sits on a panel riser"

# ---- feeder schedule
FSX, FSY, FSW, FSH = 636.0, 318.0, 320.0, 120.0
box(c, FSX, FSY, FSW, FSH, lw=1.2)
tx(c, FSX + 10, FSY + FSH - 16, "EXISTING BRANCH PANEL FEEDERS", 8.6, "Helvetica-Bold")
line(c, FSX + 10, FSY + FSH - 22, FSX + FSW - 10, FSY + FSH - 22, lw=.9, col=ORNG)
tx(c, FSX + 10, FSY + FSH - 32, "PANEL", 6.0, "Helvetica-Bold", GREY)
tx(c, FSX + 52, FSY + FSH - 32, "OCPD", 6.0, "Helvetica-Bold", GREY)
tx(c, FSX + 92, FSY + FSH - 32, "CONDUCTORS AND RACEWAY", 6.0, "Helvetica-Bold", GREY)
assert FSY + FSH < min(l for _, _, _, l, _, _ in PANELS), \
    'a feeder run crosses the feeder schedule box'
fy = FSY + FSH - 44
for nm, amp, px, lvl, dropx, spec in PANELS:
    tx(c, FSX + 10, fy, nm, 6.2, "Helvetica-Bold")
    tx(c, FSX + 52, fy, amp, 6.2, "Helvetica-Bold")
    tx(c, FSX + 92, fy, spec, 6.0)
    fy -= 11.5
for i, ln in enumerate(wrapw("EACH PANEL IS FED BY ITS OWN RACEWAY FROM ITS OWN "
                             "OVERCURRENT DEVICE IN THE MDP. THESE FEEDERS ARE "
                             "EXISTING, ARE SHOWN AS INSTALLED IN COPPER, AND ARE "
                             "NOT ALTERED UNDER THIS PERMIT.", FSW - 22, size=5.8)):
    tx(c, FSX + 10, fy - 2 - i * 7.2, ln, 5.8, "Helvetica-Oblique", GREY)

# ============================================================ generator row
GY = 300.0
GENX, GENW = 260.0, 186.0
equip(GENX, GY, GENW, 118, [
    ("NEW", 7.0, True), ("KOHLER 48RCLC", 11.5, True),
    ("48 kW LP STANDBY", 7.6, False), ("120/240V 1Ø 3W · 200 A", 7.2, False),
    ("4Q7BX ALTERNATOR", 6.8, False),
    ("200 A LINE CIRCUIT BREAKER", 6.6, False),
    ("RDC2 CONTROLLER", 6.4, False)], new=True)

GRISER = ATSX + ATSW / 2
conn(GRISER, GY + 118, GRISER, SY - 14, lw=2.2, new=True)
_wg, _hg = tag(GRISER + 14, 446,
               "GENERATOR FEEDER — 200 A OCPD\n"
               "(3) 3/0 AWG CU or (3) 250 MCM AL\n"
               "EGC: #6 AWG CU or #4 AWG AL\n"
               "2½\" PVC", new=True)

# Load management is NOT shown on this sheet. The managed loads are dropped by
# standalone PSP SAK-60 under-frequency latching relays wired inline at each
# managed circuit — there is no central load-management device and no control
# wiring to the generator, so there is nothing on the riser to draw. The
# scheme itself lives on E-3 / E-4. See note 7.
assert GRISER + 14 + _wg < PANELS[0][4], "generator feeder tag hits the first feeder drop"

# ---- emergency shutdown AT THE METER
ESTX, ESTY, ESTW, ESTH = 112.0, 424.0, 148.0, 58.0
equip(ESTX, ESTY, ESTW, ESTH, [
    ("NEW", 6.6, True), ("EMERGENCY SHUTDOWN", 8.0, True),
    ("AT THE METER — OUTSIDE,", 6.2, False),
    ("READILY ACCESSIBLE, LOCKABLE", 6.2, False),
    (note("shutdown_tag"), 6.2, False)], new=True)
conn(ESTX + 18, ESTY + ESTH, ESTX + 18, SY, lw=.9, new=True, dash=(3, 2))
conn(ESTX + ESTW, ESTY + 26, GENX + 18, ESTY + 26, lw=1.2, new=True, dash=(4, 3))
conn(GENX + 18, ESTY + 26, GENX + 18, GY + 118, lw=1.2, new=True, dash=(4, 3))
tx(c, GENX + 24, GY + 126, "SHUTDOWN CONTROL", 6.0, "Helvetica-Bold", RED)
assert GENX < GENX + 18 < GENX + GENW, "shutdown control riser misses the generator"

# ============================================================== grounding
# GEC leaves the EXISTING METER enclosure. NEC 250.24(A)(1) permits the
# connection at any accessible point from the load end of the service
# conductors to and including the service disconnecting means. The MAIN
# BONDING JUMPER stays in the existing 600 A service disconnect per 250.24(B).
GECX, GRY = 92.0, 236.0
conn(GECX, SY, GECX, GRY, lw=1.6)
conn(GECX, GRY, GECX + 48, GRY, lw=1.6)
_wge, _hge = tag(112, 252, "GEC: #6 AWG CU FROM THE METER\nENCLOSURE TO THE GROUND RODS")
assert 252 + _hge < GY, "GEC tag hits the generator enclosure"
for gx in (GECX, GECX + 48):
    c.saveState(); c.setStrokeColor(black); c.setLineWidth(1.6)
    c.line(gx, GRY, gx, GRY - 12)
    for j, ww in enumerate((17, 11, 5)):
        c.line(gx - ww, GRY - 12 - j * 5, gx + ww, GRY - 12 - j * 5)
    c.restoreState()
tx(c, GECX + 78, GRY - 10, "TWO 10'-0\" × 5/8\" GROUND RODS, 6'-0\" APART MIN.",
   6.4, "Helvetica-Bold")
tx(c, GECX + 78, GRY - 20, "GROUNDING ELECTRODE CONDUCTOR LANDS AT THE METER", 6.2)
tx(c, GECX + 78, GRY - 29, "ENCLOSURE. THE MAIN BONDING JUMPER IS IN THE EXISTING", 6.2)
tx(c, GECX + 78, GRY - 38, "600 A SERVICE DISCONNECT.", 6.2)

# ================================================================== notes
NX, NY, NW, NH = 636.0, 40.0, 320.0, 266.0
box(c, NX, NY, NW, NH, lw=1.2)
tx(c, NX + 10, NY + NH - 17, "GENERAL NOTES", 9.6, "Helvetica-Bold")
line(c, NX + 10, NY + NH - 23, NX + NW - 10, NY + NH - 23, lw=.9, col=ORNG)

NOTES = [
    "ALL WORK IS IN ACCORDANCE WITH %s AND THE %s."
    % (NEC_EDITION, FBC_EDITION),
    "THE SCOPE OF THIS PERMIT IS THE GENERATOR. THE 600 A AUTOMATIC TRANSFER "
    "SWITCH IS NEW AND IS INSTALLED BY OTHERS, ON THE LOAD SIDE OF THE "
    "EXISTING SERVICE DISCONNECT. THE SERVICE, THE 600 A SERVICE DISCONNECT, "
    "THE MDP AND ALL BRANCH PANELS ARE EXISTING AND ARE NOT ALTERED.",
    note("emerg_disc_note"),
    "THE GROUNDING ELECTRODE CONDUCTOR LANDS AT THE EXISTING METER ENCLOSURE. "
    "NEC 250.24(A)(1) PERMITS THE CONNECTION AT ANY ACCESSIBLE POINT FROM THE "
    "LOAD END OF THE SERVICE CONDUCTORS TO AND INCLUDING THE SERVICE "
    "DISCONNECTING MEANS. THE MAIN BONDING JUMPER IS IN THE EXISTING 600 A "
    "SERVICE DISCONNECT PER NEC 250.24(B) AND 250.28.",
    "THE TRANSFER SWITCH HAS A SOLID (UNSWITCHED) NEUTRAL. THE GENERATOR IS "
    "NOT A SEPARATELY DERIVED SYSTEM PER NEC 250.20(D). THE GENERATOR NEUTRAL "
    "IS NOT BONDED AT THE MACHINE AND NO SEPARATE GROUNDING ELECTRODE IS "
    "INSTALLED AT THE GENERATOR.",
    "AN EQUIPMENT GROUNDING CONDUCTOR IS RUN WITH THE GENERATOR FEEDER PER "
    "NEC 250.122, SIZED TO THE 200 A GENERATOR LINE CIRCUIT BREAKER.",
    note("shutdown_note"),
    note("load_mgmt_note"),
    "EACH BRANCH PANEL IS FED BY A SEPARATE RACEWAY FROM ITS OWN OVERCURRENT "
    "DEVICE IN THE MDP. NO RACEWAY IS SHARED BETWEEN PANELS.",
    "THE GENERATOR FEEDER CALLOUT GIVES A COPPER SIZE AND AN ALUMINUM SIZE, "
    "AND ITS CONDUIT IS SIZED FOR THE ALUMINUM CONDUCTOR. EXISTING CONDUCTORS "
    "ARE SHOWN AS INSTALLED. THE GROUNDING ELECTRODE CONDUCTOR IS COPPER: NEC "
    "250.64(A) DOES NOT PERMIT ALUMINUM IN DIRECT CONTACT WITH EARTH OR "
    "WITHIN 18 IN. OF EARTH.",
]


for SZ, LH in ((6.4, 7.6), (6.2, 7.3), (6.0, 7.0), (5.8, 6.7), (5.6, 6.4),
               (5.4, 6.1), (5.2, 5.9), (5.0, 5.7)):
    blocks = [wrapw(n, NW - 36, size=SZ) for n in NOTES]
    _r = max(4.6, SZ * 0.92)
    if sum(max(len(b) * LH + 5.5, 2 * _r + 4) for b in blocks) \
            <= (NY + NH - 36) - (NY + 10):
        break
_R = max(4.6, SZ * 0.92)                     # bullet radius tracks the type size
yy = NY + NH - 36
for i, blk in enumerate(blocks):
    c.saveState(); c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(.9)
    c.circle(NX + 18, yy - 2, _R, stroke=1, fill=1); c.restoreState()
    tx(c, NX + 18, yy - 2 - SZ * 0.34, str(i + 1), SZ * 0.98, "Helvetica-Bold",
       black, "c")
    _top = yy
    for ln in blk:
        tx(c, NX + 31, yy, ln, SZ); yy -= LH
    # a one-line note is shorter than its own bullet, so never let the next
    # bullet ride up into this one
    yy = min(yy - 5.5, _top - (2 * _R + 4))
if yy <= NY + 6:
    raise AssertionError(
        "general notes overrun their box by %.0f pt at the smallest type in "
        "the ladder (%.1f pt).\n\n"
        "The GENERAL NOTES box is 320 x 266 with the EXISTING BRANCH PANEL "
        "FEEDERS box immediately above it, so there is nowhere to grow. The "
        "2023 NEC wording is longer than the 2020 wording it replaces — "
        "445.18(A) and 445.19(C) are two requirements where the 2020 edition "
        "had one, and 230.85 now carries the marking spec and the "
        "230.85(D)/702.7(A) placard.\n\n"
        "Levers, in the order worth trying: shorten one of the notes that is "
        "NOT carrying a citation; move the feeders box up and grow this one; "
        "or split the notes into two columns. Do not shave the code notes "
        "further — they are already at the point where trimming costs meaning."
        % ((NY + 6) - yy, SZ))

# ========================================================= equipment recap
RX, RW, RH = 40.0, 572.0, 108.0
box(c, RX, NY, RW, RH, lw=1.2)
tx(c, RX + 10, NY + RH - 17, "NEW EQUIPMENT — THIS PERMIT", 9.6, "Helvetica-Bold")
line(c, RX + 10, NY + RH - 23, RX + RW - 10, NY + RH - 23, lw=.9, col=ORNG)
RECAP = [
    ("GENERATOR", "KOHLER 48RCLC — 48 kW LP STANDBY, 120/240V 1Ø 3W, 200 A, "
                  "4Q7BX ALTERNATOR, 200 A LINE CIRCUIT BREAKER"),
    ("GENERATOR FEEDER", "(3) 3/0 AWG CU or (3) 250 MCM AL, EGC #6 AWG CU or "
                         "#4 AWG AL, IN 2½\" PVC"),
    ("SHUTDOWN", note("shutdown_recap")),
]
ry = NY + RH - 37
for lbl, val in RECAP:
    tx(c, RX + 10, ry, lbl, 6.6, "Helvetica-Bold")
    for ln in wrapw(val, RW - 130, size=6.2):
        tx(c, RX + 108, ry, ln, 6.2); ry -= 7.4
    ry -= 2.6
assert ry > NY + 4, "equipment recap overruns its box"

titleblock(c, W, H, "E-1", "ELECTRICAL RISER DIAGRAM", margin=M, tbw=TBW, stamp=124)
c.save()
print("wrote", OUT)
print("notes bottom y =", round(yy, 1), " recap bottom y =", round(ry, 1))
