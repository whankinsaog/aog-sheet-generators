"""Panel schedules transcribed from RCI Engineering Sheet E5, dated 02-27-2025.

Row = (first ckt, poles, description, wire, conduit, brkr type, trip, values, shed)
  values: dict keyed 'ND' (no demand), 'APP' (appliance), 'LTG' (lighting),
          or 'DEM' (demand) for panel MDP.
  shed:   "" | "SACM" | "SMM"   under the revised HVAC-first scheme.
"""
S = ""            # not shed
A = "SHED"        # load-managed
M = "SHED"        # load-managed

from aoglib import note as _note

_ = None


def P(ck, po, d, w, cd, bt, tr, v, sh=S):
    return (ck, po, d, w, cd, bt, tr, v, sh)


# ===================================================================== MDP
MDP = dict(
    name="MDP", cols=("ND", "DEM"), nckt=54,
    meta=[("TYPE", "PANELBOARD"), ("MAIN BUS", "800 A"),
          ("SERVICE", "1 PH, 3W — 120/240 V"), ("MAIN", "M.L.O."),
          ("MOUNTING", "SURFACE"), ("ENCLOSURE", "NEMA 1"), ("A.I.C.", "22,000"),
          ("FED FROM", "EXISTING 800A ATS")],
    odd=[
        P(1,  2, "PANEL 'PA'  (SEE RISER)", "—", "—", "—", "100-2", {"ND": "2.6", "DEM": "33.7"}),
        P(5,  2, "PANEL 'PB'  (SEE RISER)", "—", "—", "—", "100-2", {"ND": "1.8", "DEM": "24.5"}),
        P(9,  2, "PANEL 'PC'  (SEE RISER)", "—", "—", "—", "125-2", {"ND": "9.1", "DEM": "21.6"}),
        P(13, 2, "PANEL 'PP'  (SEE RISER)", "—", "—", "—", "100-2", {"ND": "7.0", "DEM": "9.0"}),
        P(17, 2, "PANEL 'PD'  (SEE RISER)", "—", "—", "—", "100-2", {"ND": "6.0", "DEM": "9.8"}),
        P(21, 2, "STEAMER",    "4",  "1¼\"",  "—",    "70-2", {"ND": "—", "DEM": "13.0"}),
        P(25, 2, "EV CHARGER", "6",  "1\"",   "—",    "60-2", {"ND": "9.6", "DEM": "—"}),
        P(29, 2, "ELEVATOR",   "10", "3/4\"", "—",    "30-2", {"ND": "—", "DEM": "5.0"}),
        P(33, 2, "DRYER",      "10", "3/4\"", "GFCI", "30-2", {"ND": "—", "DEM": "5.0"}),
        P(37, 2, "DRYER",      "10", "3/4\"", "GFCI", "30-2", {"ND": "—", "DEM": "5.0"}),
        P(41, 2, "AHU-3",      "8",  "1\"",   "—",    "40-2", {"ND": "10.0", "DEM": "—"}, M),
        P(45, 2, "CU-3",       "8",  "3/4\"", "—",    "40-2", {"ND": "(6.2)", "DEM": "—"}),
        P(49, 1, "SPACE",      "—",  "—",     "—",    "—",    {}),
        P(51, 2, "SPD",        "10", "3/4\"", "—",    "30-2", {}),
    ],
    even=[
        P(2,  2, "AHU-1", "6",  "1\"",   "—", "50-2", {"ND": "10.0"},  A),
        P(6,  2, "AHU-2", "6",  "1\"",   "—", "50-2", {"ND": "10.0"},  A),
        P(10, 2, "AHU-4", "6",  "1\"",   "—", "50-2", {"ND": "10.0"},  A),
        P(14, 2, "AHU-5", "6",  "1\"",   "—", "50-2", {"ND": "10.0"},  A),
        P(18, 2, "AHU-6", "6",  "1\"",   "—", "50-2", {"ND": "10.0"}),
        P(22, 2, "CU-1",  "6",  "1\"",   "—", "50-2", {"ND": "(7.6)"}),
        P(26, 2, "CU-2",  "6",  "1\"",   "—", "50-2", {"ND": "(7.6)"}),
        P(30, 2, "CU-4",  "8",  "3/4\"", "—", "40-2", {"ND": "(6.2)"}),
        P(34, 2, "CU-5",  "4",  "1¼\"",  "—", "60-2", {"ND": "(10.3)"}),
        P(38, 2, "CU-6",  "10", "3/4\"", "—", "30-2", {"ND": "(4.6)"}),
        P(42, 2, "SPACE", "—", "—", "—", "—", {}),
        P(46, 2, "SPACE", "—", "—", "—", "—", {}),
        P(50, 2, "SPACE", "—", "—", "—", "—", {}),
        P(54, 1, "SPACE", "—", "—", "—", "—", {}),
    ],
    totals={"L": {"ND": "46.1", "DEM": "126.6"}, "R": {"ND": "50.0"}},
    summary=[("TOTAL DEMAND LOAD", "126.6 kVA", 0),
             ("FIRST 10 kVA + 40% REMAINING", "56.6 kVA", 0),
             ("TOTAL NON-DEMAND LOAD  (46.1 + 50.0)", "96.1 kVA", 0),
             ("TOTAL CALCULATED LOAD", "152.7 kVA = 636 A", 1)],
    keynotes=["VALUES IN PARENTHESES ARE THE SMALLER OF THE HEATING / COOLING "
              "LOADS AND ARE OMITTED FROM THE COLUMN TOTALS PER NEC 220.60.",
              "M  CIRCUITS MARKED 'M' CARRY A LOAD-SHED MODULE AND ARE EXCLUDED FROM "
              "THE MANAGED LOAD CALCULATION PER %s. ONE MODULE PER " % _note("load_mgmt_cite") +
              "SYSTEM, ON THE AIR HANDLER CIRCUIT ONLY — THE CONDENSER HAS NO "
              "INDEPENDENT CONTROL POWER AND DROPS WITH ITS AIR HANDLER, SO NO "
              "MODULE IS REQUIRED ON A CONDENSER CIRCUIT. SIX SYSTEMS: AHU-1 THRU "
              "AHU-5 PLUS CU-7/FCU-7A-B (PANEL 'PC' CKT 31). AHU-6/CU-6 IS THE "
              "PRIORITY ZONE AND IS NOT MANAGED. SEE SHEET E-4.",
              "PANEL FEEDER CONDUCTORS — SEE THE RISER DIAGRAM, SHEET E-1."],
)

# ====================================================================== PA
PA = dict(
    name="PA", cols=("ND", "APP", "LTG"), nckt=54,
    meta=[("TYPE", "LOAD CENTER"), ("MAIN BUS", "125 A"),
          ("SERVICE", "1 PH, 3W — 120/240 V"), ("MAIN", "M.L.O."),
          ("MOUNTING", "SURFACE"), ("ENCLOSURE", "NEMA 1"), ("A.I.C.", "22,000")],
    odd=[P(n, 1, d, "12", "1/2\"", bt, "20-1", {"LTG": v}) for n, d, bt, v in [
        (1, "SM APP KITCHEN", "AFCI", "1.5"), (3, "SM APP KITCHEN", "AFCI", "1.5"),
        (5, "SM APP KITCHEN", "AFCI", "1.5"), (7, "SM APP KITCHEN", "AFCI", "1.5"),
        (9, "1ST LAUNDRY CKT", "AFCI", "1.5"), (11, "2ND LAUNDRY CKT", "AFCI", "1.5"),
        (13, "DINING RCPT", "AFCI", "1.5"), (15, "SM APP PREP KIT", "AFCI", "1.5"),
        (17, "SM APP PREP KIT", "AFCI", "1.5"), (19, "SM APP PREP KIT", "AFCI", "1.5"),
        (21, "SM APP ODK", "AFCI", "1.5"), (23, "SM APP LOUNGE", "AFCI", "1.5"),
        (25, "BATH #2 RCPT", "—", "GNRL"), (27, "SPA/BATH #2 RCPT", "—", "GNRL"),
        (29, "POOL BATH", "—", "GNRL"), (31, "BATH #5 RCPT", "—", "GNRL"),
        (33, "BATH #6 RCPT", "—", "GNRL"), (35, "GARAGE SOUTH RCPT", "—", "GNRL"),
        (37, "OUTDOOR DIN RCPT", "—", "GNRL"), (39, "MOTORIZED SHADES", "—", "GNRL"),
        (41, "GNRL LIGHTING", "AFCI", "GNRL"), (43, "GNRL LIGHTING", "AFCI", "GNRL"),
        (45, "GNRL LIGHTING", "AFCI", "GNRL")]] + [
        P(n, 1, "SPACE", "—", "—", "—", "—", {}) for n in (47, 49, 51, 53)],
    even=[P(n, 1, d, "12", "1/2\"", bt, tr, v) for n, d, bt, tr, v in [
        (2, "BEDRM 2 RCPT ¹", "AFCI", "20-1", {"LTG": "14.7"}),
        (4, "MUD RM/MECH RCPT ¹", "AFCI", "20-1", {"LTG": "GNRL"}),
        (6, "PANTRY/HW RCPT", "AFCI", "20-1", {"LTG": "GNRL"}),
        (8, "FAMILY ROOM RCPT", "AFCI", "20-1", {"LTG": "GNRL"}),
        (10, "NOOK RCPT", "AFCI", "20-1", {"LTG": "GNRL"}),
        (12, "HALLWAY RCPT", "AFCI", "20-1", {"LTG": "GNRL"}),
        (14, "BEDRM 2 RCPT", "AFCI", "20-1", {"LTG": "GNRL"}),
        (16, "EXERCISE RM RCPT", "AFCI", "20-1", {"LTG": "GNRL"}),
        (18, "HALLWAY RCPT", "AFCI", "20-1", {"LTG": "GNRL"}),
        (20, "BEDRM 5 RCPT", "AFCI", "20-1", {"LTG": "GNRL"}),
        (22, "BEDRM 5 RCPT", "AFCI", "20-1", {"LTG": "GNRL"}),
        (24, "BEDRM 6 RCPT", "AFCI", "20-1", {"LTG": "GNRL"}),
        (26, "BEDRM 6 RCPT", "AFCI", "20-1", {"LTG": "GNRL"}),
        (28, "FIREPLACE", "—", "20-1", {"APP": "0.9"}),
        (30, "DEH-A1", "—", "20-1", {"ND": "0.8"}),
        (32, "DEH-B2", "—", "20-1", {"ND": "0.8"}),
        (34, "DEH-B3", "—", "20-1", {"ND": "0.8"})]] + [
        P(36, 1, "SPACE", "—", "—", "—", "—", {}),
        P(38, 1, "ZONE DAMPER SYS#1", "12", "1/2\"", "—", "20-1", {"ND": "0.1"}),
        P(40, 1, "ZONE DAMPER SYS#4", "12", "1/2\"", "—", "20-1", {"ND": "0.1"}),
        P(42, 1, "MAKEUP AIR FAN", "12", "1/2\"", "—", "20-1", {"APP": "0.1"})] + [
        P(n, 1, "SPACE", "—", "—", "—", "—", {}) for n in (44, 46, 48, 50)] + [
        P(52, 2, "SPD", "10", "3/4\"", "—", "30-2", {})],
    totals={"L": {"LTG": "18.0"}, "R": {"LTG": "14.7", "APP": "1.0", "ND": "2.6"}},
    summary=[("TOTAL GENERAL LIGHTING LOAD", "32.7 kVA", 0),
             ("FIRST 3 kVA + 35% REMAINING", "13.4 kVA", 0),
             ("TOTAL APPLIANCES LOAD", "1.0 kVA", 0),
             ("APPLIANCES @ 75% IF 4 OR MORE", "1.0 kVA", 0),
             ("TOTAL NON-DEMAND LOAD", "2.6 kVA", 0),
             ("TOTAL CALCULATED LOAD", "17.0 kVA = 71 A", 1)],
    keynotes=["¹  4,892 SQ.FT. OF GENERAL POWER & LIGHTING @ 3 W/SQ.FT.",
              "DUAL FUNCTION (DF) BREAKERS SHALL HAVE AFCI AND GFCI PROTECTION."],
)

# ====================================================================== PB
PB = dict(
    name="PB", cols=("ND", "APP", "LTG"), nckt=54,
    meta=[("TYPE", "LOAD CENTER"), ("MAIN BUS", "125 A"),
          ("SERVICE", "1 PH, 3W — 120/240 V"), ("MAIN", "M.L.O."),
          ("MOUNTING", "RECESSED"), ("ENCLOSURE", "NEMA 1"), ("A.I.C.", "10,000")],
    odd=[P(n, 1, d, "12", "1/2\"", "AFCI", "20-1", v) for n, d, v in [
        (1, "SM APP BAR", {"LTG": "1.5"}), (3, "SM APP BAR", {"LTG": "1.5"}),
        (5, "SM APP MASTER BR", {"LTG": "1.5"}), (7, "FOYER RCPT ¹", {"LTG": "14.8"}),
        (9, "CLUB ROOM RCPT ¹", {"LTG": "GNRL"}), (11, "CLUB ROOM RCPT", {"LTG": "GNRL"}),
        (13, "OFFICE RCPT", {"LTG": "GNRL"}), (15, "LIVING ROOM RCPT", {"LTG": "GNRL"}),
        (17, "MASTER BEDRM RCPT", {"LTG": "GNRL"}), (19, "MASTER BEDRM RCPT", {"LTG": "GNRL"}),
        (21, "HIS/HER WIC RCPT", {"LTG": "GNRL"}), (23, "BED ROOM 4 RCPT", {"LTG": "GNRL"}),
        (25, "BED ROOM 3 RCPT", {"LTG": "GNRL"}), (27, "LOUNGE RCPT", {"LTG": "GNRL"}),
        (29, "HALLWAY RCPT", {"LTG": "GNRL"}), (31, "HALLWAY RCPT", {"LTG": "GNRL"}),
        (33, "AV EQUIPMENT", {"APP": "1.5"}), (35, "AV EQUIPMENT", {"APP": "1.5"}),
        (37, "MOTORIZED SHADES", {"LTG": "GNRL"}), (39, "GNRL LIGHTING", {"LTG": "GNRL"}),
        (41, "GNRL LIGHTING", {"LTG": "GNRL"}), (43, "GNRL LIGHTING", {"LTG": "GNRL"}),
        (45, "MASTER WIC RCPT", {"LTG": "GNRL"})]] + [
        P(n, 1, "SPACE", "—", "—", "—", "—", {}) for n in (47, 49, 51, 53)],
    even=[P(n, 1, d, "12", "1/2\"", bt, tr, v) for n, d, bt, tr, v in [
        (2, "POWDER RCPT", "—", "20-1", {"LTG": "GNRL"}),
        (4, "HIS BATH RCPT", "—", "20-1", {"LTG": "GNRL"}),
        (6, "HER BATH RCPT", "—", "20-1", {"LTG": "GNRL"}),
        (8, "HER BATH RCPT", "—", "20-1", {"LTG": "GNRL"}),
        (10, "OUTDOOR RCPT", "—", "20-1", {"LTG": "GNRL"}),
        (12, "BATH 4 RCPT", "—", "20-1", {"LTG": "GNRL"}),
        (14, "BATH 3 RCPT", "—", "20-1", {"LTG": "GNRL"}),
        (16, "ICE MAKER", "DF", "20-1", {"APP": "0.4"}),
        (18, "UC REF", "DF", "20-1", {"APP": "0.4"}),
        (20, "UC REF", "DF", "20-1", {"APP": "0.4"}),
        (22, "ELEV PIT RCPT", "—", "20-1", {"LTG": "GNRL"}),
        (24, "ELV CAB LTG", "—", "20", {"LTG": "GNRL"}),
        (26, "FIREPLACE", "—", "20-1", {"APP": "1.0"}),
        (28, "DEH-2A", "—", "20-1", {"ND": "0.8"}),
        (30, "DEH-A3", "—", "20-1", {"ND": "0.8"}),
        (32, "ZONE DAMPER SYS#6", "—", "20-1", {"ND": "0.1"}),
        (34, "ZONE DAMPER SYS#3", "—", "20-1", {"ND": "0.1"})]] + [
        P(n, 1, "SPACE", "—", "—", "—", "—", {}) for n in range(36, 51, 2)] + [
        P(52, 2, "SPD", "10", "3/4\"", "—", "30-2", {})],
    totals={"L": {"APP": "3.0", "LTG": "19.3"}, "R": {"APP": "2.2", "ND": "1.8"}},
    summary=[("TOTAL GENERAL LIGHTING LOAD", "19.3 kVA", 0),
             ("FIRST 3 kVA + 35% REMAINING", "8.7 kVA", 0),
             ("TOTAL APPLIANCES LOAD", "5.4 kVA", 0),
             ("APPLIANCES @ 75% IF 4 OR MORE", "4.1 kVA", 0),
             ("TOTAL NON-DEMAND LOAD", "1.8 kVA", 0),
             ("TOTAL CALCULATED LOAD", "14.6 kVA = 61 A", 1)],
    keynotes=["¹  4,947 SQ.FT. OF GENERAL POWER & LIGHTING @ 3 W/SQ.FT.",
              "DUAL FUNCTION (DF) BREAKERS SHALL HAVE AFCI AND GFCI PROTECTION."],
)

# ====================================================================== PC
PC = dict(
    name="PC", cols=("ND", "APP", "LTG"), nckt=42,
    meta=[("TYPE", "LOAD CENTER"), ("MAIN BUS", "225 A"),
          ("SERVICE", "1 PH, 3W — 120/240 V"), ("MAIN", "M.L.O."),
          ("MOUNTING", "RECESSED"), ("ENCLOSURE", "NEMA 1"), ("A.I.C.", "18,000")],
    odd=[P(n, 1, "SPACE", "—", "—", "—", "—", {}) for n in (1, 3, 5, 7)] + [
        P(9,  2, "OVEN",  "10", "3/4\"", "—", "30-2", {"APP": "4.5"}),
        P(13, 2, "SAUNA", "10", "3/4\"", "—", "30-2", {"APP": "4.0"}),
        P(17, 2, "CU-8",  "12", "1/2\"", "—", "20-2", {"ND": "1.0"}),
        P(21, 2, "WINE EVAPORATOR", "12", "1/2\"", "—", "20-2", {"ND": "0.1"})] + [
        P(n, 1, "SPACE", "—", "—", "—", "—", {}) for n in (25, 27, 29)] + [
        P(31, 2, "CU-7 & FCU-7A-B", "4", "1¼\"", "—", "70-2", {"ND": "8.0"}, M)] + [
        P(n, 1, "SPACE", "—", "—", "—", "—", {}) for n in (35, 37, 39, 41)],
    even=[P(n, 1, d, "12", "1/2\"", bt, "20-1", v) for n, d, bt, v in [
        (2, "GARAGE DOOR MTR", "—", {"APP": "0.8"}),
        (4, "GARAGE DOOR MTR", "—", {"APP": "0.8"}),
        (6, "GARAGE DOOR MTR", "—", {"APP": "0.8"}),
        (8, "SPARE", "DF", {"APP": "1.0"}),
        (10, "DISHWASHER PREP K.", "DF", {"APP": "1.2"}),
        (12, "DISHWASHER KITCHEN", "DF", {"APP": "1.2"}),
        (14, "DISPOSAL KITCHEN", "DF", {"APP": "1.0"}),
        (16, "UC REF ODK", "DF", {"APP": "0.4"}),
        (18, "UC REF LOUNGE", "DF", {"APP": "0.4"}),
        (20, "REFRIGERATOR", "AFCI", {"APP": "0.6"}),
        (22, "FREEZER", "AFCI", {"APP": "0.6"}),
        (24, "RANGE", "AFCI", {"APP": "0.2"}),
        (26, "GRILL", "AFCI", {"APP": "0.1"}),
        (28, "HOOD", "AFCI", {"APP": "0.6"}),
        (30, "HOOD", "AFCI", {"APP": "0.6"}),
        (32, "WASHER", "—", {"APP": "1.0"}),
        (34, "WASHER", "—", {"APP": "1.0"}),
        (36, "GAS WATER HEATER", "—", {"APP": "0.2"}),
        (38, "GAS WATER HEATER", "—", {"APP": "0.4"})]] + [
        P(40, 2, "SPD", "10", "3/4\"", "—", "30-2", {})],
    totals={"L": {"ND": "9.1", "APP": "8.5"}, "R": {"APP": "13.1"}},
    summary=[("TOTAL GENERAL LIGHTING LOAD", "0.0 kVA", 0),
             ("FIRST 3 kVA + 35% REMAINING", "0.0 kVA", 0),
             ("TOTAL APPLIANCES LOAD", "21.6 kVA", 0),
             ("APPLIANCES @ 75% IF 4 OR MORE", "16.2 kVA", 0),
             ("TOTAL NON-DEMAND LOAD", "9.1 kVA", 0),
             ("TOTAL CALCULATED LOAD", "25.3 kVA = 105 A", 1)],
    keynotes=["DUAL FUNCTION (DF) BREAKERS SHALL HAVE AFCI AND GFCI PROTECTION.",
              "M  CIRCUIT MARKED 'M' IS LOAD-MANAGED BY THE GENERATOR LOAD-SHED "
              "SYSTEM PER %s. SEE THE MDP KEY NOTES AND SHEET E-4."
              % _note("load_mgmt_cite")],
)

# ====================================================================== PD
PD = dict(
    name="PD", cols=("ND", "APP", "LTG"), nckt=8,
    meta=[("TYPE", "LOAD CENTER"), ("MAIN BUS", "125 A"),
          ("SERVICE", "1 PH, 3W — 120/240 V"), ("MAIN", "2P-100 A"),
          ("MOUNTING", "SURFACE"), ("ENCLOSURE", "NEMA 4X"), ("A.I.C.", "10,000")],
    odd=[P(1, 2, "BOAT LIFT MOTORS", "6", "1\"", "GFCI", "40-2", {"ND": "6.0"}),
         P(5, 2, "SHORE POWER ¹", "6", "1\"", "GFCI", "50-2", {"LTG": "9.6"})],
    even=[P(2, 1, "SHORE POWER ¹", "10", "1/2\"", "GFCI", "30-1", {"ND": "(2.3)"}),
          P(4, 1, "GFCI RECEPTACLE", "12", "1/2\"", "GFCI", "20-1", {"LTG": "0.2"}),
          P(6, 1, "SPACE", "—", "—", "—", "—", {}),
          P(8, 1, "SPACE", "—", "—", "—", "—", {})],
    totals={"L": {"ND": "6.0", "LTG": "9.6"}, "R": {"LTG": "0.2"}},
    summary=[("TOTAL GENERAL LIGHTING LOAD", "9.8 kVA", 0),
             ("FIRST 3 kVA + 35% REMAINING", "5.4 kVA", 0),
             ("TOTAL APPLIANCES LOAD", "0.0 kVA", 0),
             ("APPLIANCES @ 75% IF 4 OR MORE", "0.0 kVA", 0),
             ("TOTAL NON-DEMAND LOAD", "6.0 kVA", 0),
             ("TOTAL CALCULATED LOAD", "11.4 kVA = 48 A", 1)],
    keynotes=["¹  RECEPTACLE WITH LARGER LOAD CONSIDERED, PER TABLE 555.12 NOTE 1."],
)

# ====================================================================== PP
PP = dict(
    name="PP", cols=("ND", "APP", "LTG"), nckt=16,
    meta=[("TYPE", "LOAD CENTER"), ("MAIN BUS", "200 A"),
          ("SERVICE", "1 PH, 3W — 120/240 V"), ("MAIN", "M.L.O."),
          ("MOUNTING", "SURFACE"), ("ENCLOSURE", "NEMA 4X"), ("A.I.C.", "10,000")],
    odd=[P(1, 2, "POOL HEATER ¹", "6", "1\"", "—", "20-2", {"APP": "8.1"}),
         P(5, 2, "BLOWER MOTOR ¹", "12", "1/2\"", "—", "20-2", {"ND": "2.0"}),
         P(9, 2, "SPA JETS PUMP ¹", "12", "1/2\"", "—", "20-2", {"ND": "2.0"}),
         P(13, 1, "SPACE", "—", "—", "—", "—", {}),
         P(15, 1, "SPACE", "—", "—", "—", "—", {})],
    even=[P(2, 2, "RECIRCULATION /\nPOOL PUMP MOTOR ¹", "12", "1/2\"", "—", "20-2",
            {"ND": "3.0"}),
          P(6, 1, "POOL LIGHTING ¹", "12", "1/2\"", "—", "20-1", {"LTG": "0.3"}),
          P(8, 1, "POOL RECEPTACLE ¹", "12", "1/2\"", "—", "20-1", {"LTG": "GNRL"}),
          P(10, 1, "POOL SALT CHLOR ¹", "12", "1/2\"", "—", "20-1", {"APP": "0.3"}),
          P(12, 1, "GAS HEATER ¹", "12", "1/2\"", "—", "20-1", {"APP": "0.3"}),
          P(14, 2, "SPD", "10", "3/4\"", "—", "30-2", {})],
    totals={"L": {"ND": "4.0", "APP": "8.1"}, "R": {"LTG": "0.3", "APP": "0.6", "ND": "3.0"}},
    summary=[("TOTAL GENERAL LIGHTING LOAD", "0.3 kVA", 0),
             ("FIRST 3 kVA + 35% REMAINING", "0.3 kVA", 0),
             ("TOTAL APPLIANCES LOAD", "8.7 kVA", 0),
             ("APPLIANCES @ 75% IF 4 OR MORE", "8.7 kVA", 0),
             ("TOTAL NON-DEMAND LOAD", "7.0 kVA", 0),
             ("TOTAL CALCULATED LOAD", "16.0 kVA = 67 A", 1)],
    keynotes=["¹  REFER TO POOL SHOP DRAWINGS FOR MORE INFORMATION. POOL EQUIPMENT "
              "IS NOT SHOWN ON PLANS.",
              "G.C. SHALL PROVIDE FINAL EQUIPMENT SPECIFICATIONS BEFORE PURCHASING "
              "ANY MAJOR ELECTRICAL DISTRIBUTION PANELS, CONDUITS OR CONDUCTORS."],
)
