"""E-3 / E-4 Load Calculation — 3085 Fort Charles Dr.

Inventory (what exists, quantities, circuits) : RCI Engineering Sheet E5.
VA per item                                   : AOG Load Calculation library.
Condenser VA                                  : E5 as scheduled (sealed source).
Blower VA                                     : AOG PSC table, top of table.

MANAGED (6): AHU-1/CU-1, AHU-2/CU-2, AHU-3/CU-3, AHU-4/CU-4, AHU-5/CU-5,
             CU-7 & FCU-7A-B
LIVE:        AHU-6/CU-6 (priority zone), CU-8, and everything else.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, black
from reportlab.pdfbase.pdfmetrics import stringWidth

W, H = 612.0, 792.0
ORANGE = Color(.76, .38, .08)
GREY = Color(.42, .42, .42)
LGREY = Color(.72, .72, .72)
RULE = Color(.88, .88, .88)
RED = Color(.78, .05, .09)      # load-managed — same red as the M on E-2
BAND = Color(.975, .965, .945)

LX, LW = 46.0, 254.0
RX, RW = 314.0, 255.0
TOP = 692.0
RH = 11.5
FS = 7.2

ADDR = ["3085 Fort Charles Dr", "Naples, FL 34102"]
from aoglib import DATE_LONG, NEC_SHORT, note
DATESTR = DATE_LONG
V = 240.0
GEN_VA = 75000.0

# ------------------------------------------------------------------ content
STEP1 = [("General Lighting (9,839 sq ft × 3 VA/sq ft)", 29517),
         ("Small Appliance Circuits ×13 (1,500 VA ea.)", 19500),
         ("Laundry Circuits ×2 (1,500 VA ea.)", 3000)]
STEP1_TOT = sum(v for _, v in STEP1)

# PSC blower running VA, AOG standard table. Taken at the top of the table
# (5 ton, 1,050 VA) for every air handler so that no unverified tonnage is
# relied on; the figure can only overstate the blower, never understate it.
BLOWER = 1050

# (name, condenser VA per E5, strip-heat VA per E5, blower VA, ckts)
HVAC = [("AHU-1 / CU-1", 7600, 10000, BLOWER, "MDP 2   (CU 22)"),
        ("AHU-2 / CU-2", 7600, 10000, BLOWER, "MDP 6   (CU 26)"),
        ("AHU-3 / CU-3", 6200, 10000, BLOWER, "MDP 41   (CU 45)"),
        ("AHU-4 / CU-4", 6200, 10000, BLOWER, "MDP 10   (CU 30)"),
        ("AHU-5 / CU-5", 10300, 10000, BLOWER, "MDP 14   (CU 34)"),
        ("AHU-6 / CU-6", 4600, 10000, BLOWER, "MDP 18   (CU 38)"),
        ("CU-7 & FCU-7A-B", 8000, 0, 0, "PC 31"),
        ("CU-8", 1000, 0, 0, "PC 17")]

# Step 3 — E5 inventory, AOG library VA. Items the library has no row for
# keep the E5 scheduled value.
STEP3 = [("Fireplaces ×2", 1900), ("Dehumidifiers ×5 (960 ea.)", 4800),
         ("Zone Dampers ×4", 400), ("Makeup Air Fan", 100),
         ("AV Equipment ×2", 3000), ("Ice Maker", 600),
         ("U/C Refrigerators ×4 (340 ea.)", 1360), ("Refrigerator", 780),
         ("Freezer", 600), ("Dishwashers ×2 (1,030 ea.)", 2060),
         ("Disposal (1/3 HP)", 828), ("Range Hoods ×2 (540 ea.)", 1080),
         ("Grill", 100), ("Gas Water Heaters ×2 (controls)", 200),
         ("Wine Evaporator", 230), ("Sauna", 4000),
         ("Garage Door Motors ×3 (720 ea.)", 2160),
         ("Spare (DF, scheduled)", 1000),
         ("Boat Lift Motors ×2 (1 HP ea.)", 3680),
         ("Shore Power (T555.12 Note 1)", 9600),
         ("Dock GFCI Receptacle", 200), ("Pool Equip. Panel 'PP'", 15307),
         ("Steamer", 13000), ("EV Charger — 48 A", 11520),
         ("Elevator (5 HP)", 6440)]
STEP3_TOT = sum(v for _, v in STEP3)
COOKING, DRYER = 4700, 10000

POOL = [("Pool Heater — heat pump", 9600), ("Blower Motor (1/2 HP)", 1127),
        ("Spa Jets Pump (1 HP)", 1840),
        ("Recirculation / Pool Pump (1 HP)", 1840),
        ("Pool Lighting", 300), ("Salt Chlorinator", 300),
        ("Gas Heater (controls)", 300)]

BASE = STEP1_TOT + STEP3_TOT + COOKING + DRYER
DEMAND = 10000 + 0.40 * (BASE - 10000)

# ---- the scheme -----------------------------------------------------------
PRIORITY = "AHU-6 / CU-6"          # held live, never managed
SHED_UNITS = ["AHU-5 / CU-5", "CU-7 & FCU-7A-B", "AHU-1 / CU-1",
              "AHU-2 / CU-2", "AHU-3 / CU-3", "AHU-4 / CU-4"]
NSHED = len(SHED_UNITS)
LIVE_UNITS = [u for u in HVAC if u[0] not in SHED_UNITS]
CKTS = {u[0]: u[4] for u in HVAC}
SHED_ROWS = [(n, CKTS[n]) for n in SHED_UNITS]

NOTES = [
    "Inventory, quantities and circuit numbers are taken line by line from RCI "
    "Engineering Sheet E5 panel schedules dated 02-27-2025 — panels MDP, PA, PB, "
    "PC, PD and PP. Areas per the E5 keynotes: 4,892 + 4,947 sq ft.",
    "Step 3 VA figures are the AOG standard appliance library; items it has no "
    "entry for keep the E5 value. Net difference against E5: 145 VA on the base.",
    "Condensers are as scheduled on E5. Each air handler also carries a 1,050 VA "
    "PSC blower E5 does not schedule — its AHU line is exactly 10.0 kVA, the heater "
    "kit alone. A blower runs in both modes, so it counts at 100% in both "
    "candidates. 1,050 VA is the top of the AOG table, so no tonnage is assumed.",
    "One module per system, on the air handler circuit only. The condenser has no "
    "independent control power — its contactor is driven from the air handler — so "
    "it drops with the air handler and needs no module of its own.",
    "E5 uses the standard method of NEC 220 Part III and its MDP summary reads "
    "152.7 kVA = 636 A; this sheet uses the 220.82 optional method. Different "
    "methods, not a discrepancy.",
    "The two washers on panel PC run on the laundry branch circuits already allowed "
    "at 1,500 VA each in Step 1 per 220.82(B)(2), so they are not counted again in "
    "Step 3. Dryers are counted in Step 5 per 220.82(B)(3)(c).",
]

GENS = [('AC 10KW', 10), ('AC 12KW', 12), ('AC 14KW', 14), ('AC 16KW', 16),
        ('AC 18KW', 18), ('AC 22KW', 22), ('AC 24KW', 24), ('AC 26KW', 26),
        ('LC 25KW', 25), ('LC 30KW', 30), ('AC 28KW', 28), ('LQ 32KW', 32),
        ('LQ 40KW', 40), ('LQ 48KW', 48), ('LQ 60KW', 60), ('LQ 80KW', 75),
        ('LQ 100KW', 96), ('LQ 130KW', 130), ('LQ 150KW', 134)]
SVC_SIZES = [100, 110, 125, 150, 175, 200, 225, 250, 300, 350, 400, 450, 500,
             600, 700, 800, 1000, 1200, 1600, 2000]


def pick_gen(va):
    kw, best = va / 1000.0, None
    for n, lp in GENS:
        if lp >= kw and (best is None or lp < best):
            best = lp
    return [n for n, lp in GENS if lp == best][0], best


def hvac_step2(live):
    """220.82(C): larger of cooling or strip heat at its demand factor.
    The blower belongs to the air handler and counts at 100% in both."""
    blw = sum(u[3] for u in live)
    cool = sum(u[1] for u in live) + blw
    el = sum(u[2] for u in live)
    n = sum(1 for u in live if u[2] > 0)
    hf = 0.40 if n >= 4 else 0.65
    heat = el * hf + blw
    return max(cool, heat), cool, heat, hf, blw


def ladder():
    order = [u[0] for u in sorted(HVAC, key=lambda u: -u[1])
             if u[0] != PRIORITY]
    out, shed = [], []
    for i in range(len(order) + 1):
        live = [u for u in HVAC if u[0] not in shed]
        s2, cool, heat, hf, _b = hvac_step2(live)
        svc = DEMAND + s2
        out.append(dict(n=i, last=("—" if i == 0 else order[i - 1]),
                        s2=s2, svc=svc, amps=svc / V,
                        mgn=100.0 * (GEN_VA - svc) / GEN_VA,
                        live=len(live),
                        gov="cooling" if cool >= heat else "heat"))
        if i < len(order):
            shed.append(order[i])
    return out


LADDER = ladder()
assert LADDER[NSHED]["mgn"] >= 0 and LADDER[NSHED - 1]["mgn"] < 0, \
    "scheme is not the minimum that fits"


def fmt(n):
    return "{:,}".format(int(round(n)))


# ------------------------------------------------------------------ drawing
def tx(c, x, y, s, size=FS, font="Helvetica", col=black, anchor="l"):
    c.setFont(font, size)
    c.setFillColor(col)
    if anchor == "r":
        c.drawRightString(x, y, s)
    elif anchor == "c":
        c.drawCentredString(x, y, s)
    else:
        c.drawString(x, y, s)


def rule(c, x, y, w, col=RULE, lw=.5):
    c.setStrokeColor(col)
    c.setLineWidth(lw)
    c.line(x, y, x + w, y)


def wrapw(text, maxw, font="Helvetica", size=6.3):
    out, cur = [], ""
    for wd in text.split():
        t = (cur + " " + wd).strip()
        if stringWidth(t, font, size) > maxw and cur:
            out.append(cur)
            cur = wd
        else:
            cur = t
    if cur:
        out.append(cur)
    return out


class Col:
    def __init__(self, c, x, w, y):
        self.c, self.x, self.w, self.y = c, x, w, y

    def head(self, title, sub=None):
        self.y -= 13
        tx(self.c, self.x, self.y, title, 7.6, "Helvetica-Bold", ORANGE)
        if sub:
            tx(self.c, self.x + stringWidth(title, "Helvetica-Bold", 7.6) + 6,
               self.y, sub, 6.6, "Helvetica", GREY)
        self.y -= 4
        rule(self.c, self.x, self.y, self.w, ORANGE, .9)
        self.y -= 2

    def row(self, label, value, bold=False, sub=False, band=False, big=False):
        self.y -= RH
        if band:
            self.c.setFillColor(BAND)
            self.c.rect(self.x, self.y - 1.5, self.w, RH, stroke=0, fill=1)
        f = "Helvetica-Bold" if bold else "Helvetica"
        lc = GREY if sub else black
        tx(self.c, self.x + (10 if sub else 3), self.y + 2.2, label,
           FS - (0.5 if sub else 0), f, lc)
        if value is not None:
            tx(self.c, self.x + self.w - 3, self.y + 2.2, value,
               (FS + 2.2) if big else FS,
               "Helvetica-Bold" if (bold or not sub) else "Helvetica",
               ORANGE if big else lc, "r")
        rule(self.c, self.x, self.y - 1.5, self.w)

    def caption(self, text):
        self.y -= 9.5
        tx(self.c, self.x + self.w - 3, self.y + 2, text, 6.2, "Helvetica",
           GREY, "r")

    def note(self, text):
        for ln in wrapw(text, self.w - 6, size=6.2):
            self.y -= 7.6
            tx(self.c, self.x + 3, self.y, ln, 6.2, "Helvetica", GREY)
        self.y -= 3

    def gap(self, n=9):
        self.y -= n


def build(managed):
    units = LIVE_UNITS if managed else HVAC
    s2, cool, heat, hf, blw = hvac_step2(units)
    svc = DEMAND + s2
    amps = svc / V
    gen, lp = pick_gen(svc)
    svc_size = next((s for s in SVC_SIZES if amps <= s), 2000)
    margin = lp - svc / 1000.0

    tag = "Managed" if managed else "Unmanaged"
    sheet = "E-4" if managed else "E-3"
    out = "out/%s Load Calculation - %s - 3085 Fort Charles Dr.pdf" % (sheet, tag)
    c = canvas.Canvas(out, pagesize=(W, H))

    c.setStrokeColor(ORANGE)
    c.setLineWidth(2.6)
    c.rect(18, 18, W - 36, H - 36, stroke=1, fill=0)

    # header
    tx(c, LX, H - 68, "Always On Generators", 21, "Helvetica-Bold", ORANGE)
    tx(c, LX, H - 82, "RESIDENTIAL LOAD CALCULATION — %s ART. 220 "
       "PART IV, 220.82 OPTIONAL METHOD" % NEC_SHORT.upper(),
       7.4, "Helvetica", GREY)
    tx(c, LX, H - 92, "INVENTORY: RCI ENGINEERING SHEET E5, 02-27-2025  ·  "
       "VA: AOG STANDARD LIBRARY  ·  %s LOAD" % tag.upper(),
       6.6, "Helvetica-Bold", GREY)
    tx(c, W - 46, H - 56, "SITE ADDRESS", 7.2, "Helvetica-Bold", GREY, "r")
    tx(c, W - 46, H - 68, ADDR[0], 8.4, "Helvetica", black, "r")
    tx(c, W - 46, H - 79, ADDR[1], 8.4, "Helvetica", black, "r")
    rule(c, LX, H - 99, W - 2 * LX, ORANGE, 1.6)

    # ---------------- left column
    L = Col(c, LX, LW, TOP)
    L.head("STEP 1", "— LIGHTING & CIRCUITS  220.82(B)(1),(2)")
    for d, v in STEP1:
        L.row(d, fmt(v) + " VA")
    L.row("Step 1 Total", fmt(STEP1_TOT) + " VA", bold=True, band=True)

    L.gap()
    L.head("STEP 2", "— HVAC  220.82(C)  ·  added @ 100%")
    L.y -= 10
    tx(c, LX + 3, L.y + 2, "UNIT", 6.2, "Helvetica-Bold", GREY)
    tx(c, LX + 128, L.y + 2, "CU/HP", 6.2, "Helvetica-Bold", GREY, "c")
    tx(c, LX + 180, L.y + 2, "BLOWER", 6.2, "Helvetica-Bold", GREY, "c")
    tx(c, LX + LW - 3, L.y + 2, "HEAT", 6.2, "Helvetica-Bold", GREY, "r")
    L.y -= 2
    rule(c, LX, L.y, LW)
    for name, cu, ht, bw, _ck in units:
        L.y -= RH
        lab = name + ("   (priority zone)" if managed and name == PRIORITY else "")
        tx(c, LX + 3, L.y + 2.2, lab, FS)
        tx(c, LX + 128, L.y + 2.2, fmt(cu), FS, "Helvetica-Bold", anchor="c")
        tx(c, LX + 180, L.y + 2.2, fmt(bw) if bw else "—", FS,
           "Helvetica-Bold" if bw else "Helvetica",
           black if bw else LGREY, "c")
        tx(c, LX + LW - 3, L.y + 2.2, fmt(ht) if ht else "—", FS,
           "Helvetica-Bold" if ht else "Helvetica",
           black if ht else LGREY, "r")
        rule(c, LX, L.y - 1.5, LW)
    if managed:
        L.row("%d systems load-managed — see MANAGED LOADS" % NSHED,
              None, sub=True)
    L.row("Cooling candidate — CU + blower", fmt(cool) + " VA", sub=True)
    L.row("Heating candidate — heat × %d%% + blower" % int(hf * 100),
          fmt(heat) + " VA", sub=True)
    L.row("Step 2 Applied — larger of the two", fmt(s2) + " VA",
          bold=True, band=True)
    L.caption("%s governs" % ("Cooling" if cool >= heat else "Heating"))

    L.gap()
    L.head("STEP 3", "— FIXED APPLIANCES  220.82(B)(3),(4)")
    for d, v in STEP3:
        L.row(d, fmt(v) + " VA")
    L.row("Step 3 Total (raw VA)", fmt(STEP3_TOT) + " VA", bold=True, band=True)

    def steps45(col):
        col.gap()
        col.head("STEPS 4 & 5", "— COOKING & DRYER")
        col.row("Cooking Load  220.82(B)(3)b", fmt(COOKING) + " VA")
        col.row("Oven — electric", "4,500 VA", sub=True)
        col.row("Range — gas (controls)", "200 VA", sub=True)
        col.row("Dryer Load  220.82(B)(3)c ×2", fmt(DRYER) + " VA")


    # ---------------- right column
    R = Col(c, RX, RW, TOP)
    R.head("SERVICE DEMAND", "— NEC 220.82")
    R.row("Base loads (Steps 1+3+4+5)", fmt(BASE) + " VA")
    R.row("Demand (first 10k@100%, rest@40%)", fmt(DEMAND) + " VA")
    R.row("+ HVAC @ 100% (220.82(C))", "+ " + fmt(s2) + " VA")
    R.row("Service Demand", fmt(svc) + " VA", bold=True, band=True)
    R.row("Demand @ 240 V, 1Ø", "%.1f A" % amps, bold=True)
    R.row("Minimum Service Size", "%d A" % svc_size)

    R.gap()
    R.head("GENERATOR", "— PROPANE")
    R.row("Minimum Generator Required", gen, big=True, bold=True)
    if managed:
        R.row("Managed loads required", "%d" % NSHED, bold=True)
    R.row("Rated output on LP", "%d kW" % lp, sub=True)
    R.row("Margin over calculated demand", "%.2f kW  (%.1f%%)"
          % (margin, 100 * margin / lp), sub=True)
    if not managed:
        R.caption("Exceeds the XG08045 — load management required")
    else:
        R.caption("XG08045 = LQ 80KW, 75 kW on LP = 312.5 A")

    if not managed:
        R.gap()
        R.head("POOL PANEL", "— PANEL 'PP', NEC 680")
        for d, v in POOL:
            R.row(d, fmt(v) + " VA")
        R.row("Pool Panel Loads Total", fmt(sum(v for _, v in POOL)) + " VA",
              bold=True, band=True)
        R.caption("Carried as one 15,307 VA line in Step 3")

    if managed:
        R.gap()
        R.head("MANAGED LOADS",
               "— red = load-managed  ·  %s" % note("load_mgmt_cite"))
        for name, ckts in SHED_ROWS:
            R.y -= RH
            tx(c, RX + 3, R.y + 2.2, name, FS, "Helvetica-Bold", RED)
            tx(c, RX + RW - 3, R.y + 2.2, ckts, FS, "Helvetica-Bold", RED, "r")
            rule(c, RX, R.y - 1.5, RW)
        R.caption("%d of %d systems managed · %d remain live"
                  % (NSHED, len(HVAC), len(HVAC) - NSHED))

    steps45(R)

    R.gap()
    R.head("NOTES")
    for n in NOTES:
        R.note(n)

    # ---------------- shed ladder (managed sheet, full width, bottom)
    if managed:
        ly = 148.0
        tx(c, LX, ly + 6, "LOAD MANAGEMENT", 7.6, "Helvetica-Bold", ORANGE)
        tx(c, LX + 82, ly + 6, "— why six modules, and not five or seven",
           6.6, "Helvetica", GREY)
        rule(c, LX, ly, W - 2 * LX, ORANGE, .9)
        AVAIL = GEN_VA / V                       # 312.5 A
        X_N, X_SYS, X_LIVE = LX + 3, LX + 46, LX + 178
        X_HV, X_SVC, X_AMP, X_VS = LX + 250, LX + 330, LX + 384, LX + 400
        y = ly - 11
        tx(c, X_N, y + 2, "MODULES", 6.2, "Helvetica-Bold", GREY)
        tx(c, X_SYS, y + 2, "SYSTEM ADDED AT THIS STEP", 6.2,
           "Helvetica-Bold", GREY)
        tx(c, X_LIVE, y + 2, "A/C STILL LIVE", 6.2, "Helvetica-Bold", GREY, "c")
        tx(c, X_HV, y + 2, "HVAC LOAD", 6.2, "Helvetica-Bold", GREY, "r")
        tx(c, X_SVC, y + 2, "SERVICE DEMAND", 6.2, "Helvetica-Bold", GREY, "r")
        tx(c, X_AMP, y + 2, "AMPS", 6.2, "Helvetica-Bold", GREY, "r")
        tx(c, X_VS, y + 2, "AGAINST THE 312.5 A AVAILABLE", 6.2,
           "Helvetica-Bold", GREY)
        y -= 2
        rule(c, LX, y, W - 2 * LX)
        for r in LADDER:
            y -= 9.2
            pick = r["n"] == NSHED
            inscheme = 1 <= r["n"] <= NSHED
            if inscheme:
                c.setFillColor(BAND)
                c.rect(LX, y - 1.5, W - 2 * LX, 9.2, stroke=0, fill=1)
            col = RED if inscheme else black
            f = "Helvetica-Bold" if pick else "Helvetica"
            over = r["amps"] - AVAIL
            tx(c, X_N, y + 2.2, str(r["n"]), 6.5, f, col)
            tx(c, X_SYS, y + 2.2,
               "— nothing managed —" if r["n"] == 0 else "+  " + r["last"], 6.5,
               f, GREY if r["n"] == 0 else col)
            tx(c, X_LIVE, y + 2.2, str(r["live"]), 6.5, f, col, "c")
            tx(c, X_HV, y + 2.2, fmt(r["s2"]) + " VA", 6.5, f, col, "r")
            tx(c, X_SVC, y + 2.2, fmt(r["svc"]) + " VA", 6.5, f, col, "r")
            tx(c, X_AMP, y + 2.2, "%.1f A" % r["amps"], 6.5, f, col, "r")
            if pick:
                vs = "UNDER by %.1f A  —  AS DESIGNED" % -over
            elif over > 0:
                vs = "over by %.1f A" % over
            elif abs(r["svc"] - LADDER[NSHED]["svc"]) < 1:
                vs = "under by %.1f A  —  no gain over 6" % -over
            else:
                vs = "under by %.1f A" % -over
            tx(c, X_VS, y + 2.2, vs, 6.5,
               "Helvetica-Bold" if pick else "Helvetica",
               RED if inscheme else GREY)
            rule(c, LX, y - 1.5, W - 2 * LX)
        for ln in ["THE SIX IN RED ARE THE MANAGED SYSTEMS — rows 1 through %d "
                   "together. The name on each row is the system added at that "
                   "step, not the only one managed." % NSHED,
                   "%s is the priority zone and is never managed. A 7th module "
                   "on CU-8 buys nothing — with one air handler live the strip "
                   "heat governs, and CU-8 is on the cooling side." % PRIORITY]:
            y -= 8.0
            tx(c, LX + 3, y, ln, 6.2, "Helvetica-Oblique", GREY)

    rule(c, LX, 44, W - 2 * LX, RULE, .8)
    tx(c, LX, 34, "Inventory per RCI Engineering Sheet E5 · VA per AOG standard "
       "library · %s Art. 220.82 Optional Method" % NEC_SHORT,
       6.3, "Helvetica", GREY)
    tx(c, W - LX, 34, DATESTR, 6.3, "Helvetica", GREY, "r")

    c.save()
    print("%-10s %10s VA  %7.1f A  -> %-9s (LP %3d kW, margin %5.2f%%)"
          "   low_y L=%.0f R=%.0f" %
          (tag, fmt(svc), amps, gen, lp, 100 * margin / lp, L.y, R.y))
    return out


if __name__ == "__main__":
    print("BASE %s   DEMAND %s" % (fmt(BASE), fmt(DEMAND)))
    for r in LADDER:
        print("  n=%d  %-18s s2=%8s  svc=%9s  %6.1f A  %6.2f%%  (%s)"
              % (r["n"], r["last"], fmt(r["s2"]), fmt(r["svc"]),
                 r["amps"], r["mgn"], r["gov"]))
    build(False)
    build(True)
