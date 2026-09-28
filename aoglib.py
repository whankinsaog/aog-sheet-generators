"""Shared drawing helpers for the Always On Generators permit sheets.

THIS COPY IS POPULATED FOR: 1912 Jung Blvd E, Naples FL 34120 (Collier County)
                            NEW PERMIT - electric only: portable generator power inlet +
                            Square D RCGK2 interlock in the existing 200 A meter-main
AOG stamps these sheets, so NO licence numbers print and a clear
stamp box is reserved on every sheet.
"""
import datetime as _dt
import os as _os

from reportlab.lib.colors import Color, black, white
from reportlab.pdfgen import canvas

# ------------------------------------------------------------------ job date
# The permit is dated the day the package is built. Every sheet reads these
# two constants and nothing hard-codes a date, so E-1 through E-4, SP-1, SP-2
# and the Scope of Work can never disagree. To re-issue an old package under
# its original date, set AOG_JOB_DATE=YYYY-MM-DD in the environment.
_ovr = _os.environ.get("AOG_JOB_DATE")
JOB_DATE = _dt.date.fromisoformat(_ovr) if _ovr else _dt.date.today()
DATE_SHORT = JOB_DATE.strftime("%m-%d-%Y")                      # 09-14-2026
DATE_LONG = "%s %d, %d" % (JOB_DATE.strftime("%B"), JOB_DATE.day,
                           JOB_DATE.year)                        # September 14, 2026

# --------------------------------------------------------- plan review date
# This package is a CORRECTION RESPONSE, not a revision to an issued permit:
# the application was kicked back, and the generator make was changed as part
# of answering the comments rather than left for a later revision. Those are
# different things to a reviewer, and the sheets must not say "revision".
# One constant owns the comment date so the title blocks, the riser subtitle
# and the scope of work can never cite two different ones.
# Left as None the sheets still read correctly, just without the date — never
# a placeholder, never a blank. Set it and every sheet picks the date up.
REVIEW_DATE = None            # "MM-DD-YYYY" off the correction letter
CORRECTION = ("CORRECTION RESPONSE TO THE PLAN REVIEW COMMENTS DATED %s."
              % REVIEW_DATE) if REVIEW_DATE else \
             "CORRECTION RESPONSE TO THE PLAN REVIEW COMMENTS."

# ---------------------------------------------------------------- job data
JOB = dict(
    addr="1912 JUNG BLVD E",
    city="NAPLES, FLORIDA 34120",
    proj="PORTABLE GENERATOR INLET & INTERLOCK",
    ahj="COLLIER COUNTY",
    trade="TRADE: ELECTRIC — GENERATOR INTERLOCK",
    gen="50 A POWER INLET - CONNECTICUT ELECTRIC EGSPI50, 125/250V, NEMA 3R, CS6375",
    ats="SQUARE D RCGK2 GENERATOR INTERLOCK KIT, 50 A 2-POLE HOM BACKFED BREAKER, IN THE EXISTING 200 A METER-MAIN",
    date=DATE_SHORT,
    scope=("INSTALL ONE 50 A PORTABLE GENERATOR POWER INLET AND ONE SQUARE D RCGK2 "
           "INTERLOCK KIT WITH A 50 A 2-POLE BACKFED BREAKER IN THE EXISTING 200 A "
           "METER-MAIN. INSTALL ONE 100 A SUB PANEL AND ONE PLUG-IN SURGE PROTECTIVE "
           "DEVICE, AND RE-TERMINATE THE EXISTING POOL PANEL FEEDER IN THE SUB PANEL. "
           "PORTABLE GENERATOR BY OWNER."),
)

CO = ["ALWAYS ON GENERATORS",
      "3120 6th St NW, Naples FL 34120",
      "(239) 839-3553",
      "Permitting@alwaysongenerators.com"]

# ------------------------------------------------------------- codes in force
# Florida runs a triennial cycle and each edition takes effect on December 31.
# The code in force on a permit is the one in force ON THE PERMIT DATE, and
# JOB_DATE already owns that date — so the edition is DERIVED here and nothing
# anywhere types "8th Edition" again. When Florida adopts, one row below changes
# and the whole stack follows: the title blocks, the riser general notes, the
# scope of work, the gas isometric notes and the load calc header and footer.
#
# A cycle whose referenced standards are not yet verified carries None. Asking
# for a sheet dated inside it raises instead of printing a guess — a wrong code
# line is a correction letter, and a silently wrong one is worse than a script
# that stops and tells you what to go read.
CODE_CYCLES = [
    dict(
        effective=_dt.date(2023, 12, 31),
        fbc="FLORIDA BUILDING CODE 8TH EDITION (2023)",
        fbc_title="Florida Building Code, 8th Edition (2023)",
        fbc_abbr="FBC 8TH ED. (2023)",
        nec="NEC 2020 (NFPA 70)",
        nec_short="NEC 2020",
        nfpa54="NFPA 54 / ANSI Z223.1 (2021)",
        asce7="ASCE 7-22",
        note="Confirmed by Brandon, Aug 2026.",
    ),
    dict(
        effective=_dt.date(2026, 12, 31),
        fbc="FLORIDA BUILDING CODE 9TH EDITION (2026)",
        fbc_title="Florida Building Code, 9th Edition (2026)",
        fbc_abbr="FBC 9TH ED. (2026)",
        # NFPA 70—23 "as published September 1, 2022", read off Chapter 35 of
        # the Building volume (FLBC2026V1.0) by Brandon, 09-17-2026.
        nec="NEC 2023 (NFPA 70)",
        nec_short="NEC 2023",
        # NFPA 54 is NOT adopted by reference by the Florida code — it is the
        # companion citation AOG puts beside the FL Fuel Gas sections, because
        # the two number the same requirements differently and a reviewer may
        # be working from either. So the edition here is AOG's choice, not the
        # code's, and no chapter of the 9th Edition names it. Paired to 2024 to
        # match the base: the 9th Edition Fuel Gas volume is the 2023 volume
        # updated to the 2024 IFGC (ICC Digital Codes title page, read
        # 09-17-2026). To stay on an older NFPA 54, change this one line.
        nfpa54="NFPA 54 / ANSI Z223.1 (2024)",
        # ASCE 7—22, same Chapter 35 read. Unchanged from the 8th Edition, so
        # the wind criteria on the structural sheets do not move this cycle.
        asce7="ASCE 7-22",
        note=(
            "The 9th Edition volumes are published on ICC Digital Codes and take "
            "effect 12-31-2026, amending the 2024 I-Codes — "
            "codes.iccsafe.org/codes/florida. Every edition in this row is "
            "filled in. When it goes live, update User Info!B18 in the load "
            "calculation workbook and the editions table in the permit-packet "
            "skill in the same pass — neither of those follows this file.\n\n"
            "SECTION NUMBERS ARE NOT EDITIONS, and this row does not move them. "
            "The 2023 NEC reorganized 230.85, 445.18/445.19 and 702.4 — what was "
            "read is recorded in CITATION_MOVES below, and `s11_citecheck.py` "
            "reports which sheets still carry a superseded citation. Work that "
            "list before the first 2027 package goes out."
        ),
    ),
]


# ------------------------------------------------------- citation moves
# These are NOT editions. They are section numbers inside the code, and this
# table deliberately does not rewrite anything — a citation is a number AND the
# sentence around it, and swapping the number into an old sentence produces a
# note that is confidently wrong. What this records is the reading, so that it
# is done once, and so `s11_citecheck.py` can refuse to let a stale citation
# reach a reviewer.
#
# rewrite=True: the number moved AND the requirement changed. Rewrite the note.
# rewrite=False: same requirement, deeper subsection. Renumber and move on.
CITATION_MOVES = {
    _dt.date(2026, 12, 31): dict(
        source="NFPA 70 (2023) read on link.nfpa.org — Articles 230, 445, 702 "
               "and 220 on 09-17-2026; Articles 110, 250, 430, 705 and 750 on "
               "09-18-2026. Every citation printed on an AOG sheet has now been "
               "read against the 2023 text except Article 680.",
        moves=[
            dict(old="445.18(D)", new="445.19(C)", rewrite=True,
                 note="445.18 is now only (A) Disconnecting Means and (B) "
                      "Generators Installed in Parallel — there is no (D). "
                      "Prime-mover shutdown moved to 445.19, and 445.19(C) is "
                      "the one- and two-family dwelling case: a shutdown device "
                      "outside the dwelling at a readily accessible location, "
                      "permitted on the exterior of the generator enclosure, "
                      "marked Generator Emergency Shutdown per 110.21(B). That "
                      "is a DIFFERENT requirement from the old 'accessible, "
                      "lockable in the open position' disconnect note, which "
                      "now lives in 445.18(A). The riser needs both, and the "
                      "sentence rewritten. 702.7(A) carries the same swap "
                      "inline in its own text."),
            dict(old="230.85(1)", new="230.85(B)(1)", rewrite=False,
                 note="230.85 gained subsections: (A) General [(1) Location, "
                      "(2) Rating, (3) Grouping], (B) Disconnects, (C) "
                      "Replacement, (D) Identification of Other Isolation "
                      "Disconnects, (E) Marking. The service-disconnect option "
                      "is the same requirement, one level deeper."),
            dict(old="702.4(B)(2)(b)", new="702.4(A)(2)(b)", rewrite=True,
                 note="Load management is now under (A) System Capacity, not "
                      "(B) — and it no longer just says load management. It "
                      "requires an Energy Management System employed IN "
                      "ACCORDANCE WITH 750.30. Read 750.30 against the shed "
                      "scheme before the first 2027 managed calc; it bears on "
                      "the ATS-integrated vs. standalone-relay distinction."),
            dict(old="705.70", new="705.170", rewrite=False,
                 note="Microgrid Interconnect Devices. Part II of Article 705 "
                      "renumbers into the 705.1xx block in 2023, so the MID "
                      "section is 705.70 under the 2020 NEC and 705.170 under "
                      "2023. Same three bullets either way: an MID is required "
                      "for any connection between a microgrid system and a "
                      "primary power source, it is listed or field-labeled for "
                      "the application, and it has enough overcurrent devices "
                      "to protect from all sources. FOUND ON A SHEET THE WRONG "
                      "WAY ROUND — the 112 1st Ave N generator riser printed "
                      "705.170 three times on a sheet whose title block says "
                      "NEC 2020. A 2023 number on a 2020 sheet is the same "
                      "defect as a 2020 number on a 2023 sheet, and "
                      "s11_citecheck.py only looks for the second kind. Until "
                      "it looks both ways, check MID citations by hand."),
        ],
        additions=[
            "230.85(E)(2) — the marking goes on the outside front of the "
            "disconnect enclosure, RED background, WHITE text, letters at "
            "least 1/2 in. high, and complies with 110.21(B). The riser's "
            "marking callout should state the colour and letter height.",
            "230.85(D) — where isolation means for OTHER energy sources are "
            "not adjacent to the emergency disconnect, a plaque or directory "
            "giving their location goes adjacent to it. Its informational note "
            "names 445.18 and 705.20, so on an AOG job the generator disconnect "
            "is exactly what it means.",
            "702.7(A) — for one- and two-family dwellings, a sign at the "
            "230.85 disconnect giving the location of each permanently "
            "installed optional standby source disconnect or shutdown means. "
            "Same placard as 230.85(D), required from both directions. This is "
            "a deliverable on every job, not a drafting note.",
            "702.2 — reconditioned transfer switches are not permitted.",
            "702.5(B) — a transfer switch between the meter and the meter "
            "enclosure shall be a listed meter-mounted transfer switch and "
            "shall be approved (UL 1008M).",
            "445.6 — stationary generators shall be listed.",
            "445.11 — marking shall indicate whether the generator neutral is "
            "bonded to its frame, and additional marking is required where the "
            "bonding is modified in the field. Useful support for the riser's "
            "not-separately-derived note.",
            "750.30(B) — THE ONE THAT CHANGES A DECISION, NOT A NOTE. Because "
            "702.4(A)(2)(b) now requires the EMS to comply with 750.30, the "
            "shed list is no longer only house style: an energy management "
            "system SHALL NOT disconnect power to elevators, escalators, "
            "moving walks, stairway lift chairs, or circuits supplying "
            "emergency lighting. AOG already sheds air handlers only, so this "
            "codifies the existing rule — but it makes 'shed the elevator to "
            "drop a genset size' a violation rather than a judgement call. "
            "s11_citecheck.py checks the shed flags against this list.",
            "750.30(C)(4) — where an EMS is used to LIMIT CURRENT on a "
            "conductor, the supplying equipment is field marked with the "
            "maximum current setting, the date of the calculation and setting, "
            "the loads and sources involved, and wording that the limiting "
            "feature is not to be bypassed. Judgement call whether AOG's "
            "generator-capacity management is current limiting on a conductor "
            "at all — read 750.30(C) against the actual scheme before "
            "deciding. (A) and (B) apply regardless.",
            "110.21(B) — field-applied hazard markings now must also be of "
            "sufficient durability for the environment, and the section cites "
            "ANSI Z535.2-2011 (R2017). Same number, slightly more to meet.",
            "230.67(A) — the SPD requirement is no longer dwelling units only; "
            "it now lists dwelling units, dormitory units, hotel/motel guest "
            "rooms and suites, and nursing-home patient sleeping rooms. No "
            "practical change for AOG's work, but the note should not say the "
            "requirement is limited to dwellings.",
            "250.24(A) — the range is now 250.24(A)(1) through (A)(4), where "
            "it ran to (A)(5). 250.24(A)(1) itself is unchanged.",
            "250.94 — retitled 'Bonding for Communications Systems' and worded "
            "around bonding CONDUCTOR terminations per (A) or (B). Same "
            "number; the intersystem bonding termination is now (A).",
        ],
        unchanged=[
            "220.82 is intact, label AND arithmetic. Part IV is still "
            "'Optional Feeder and Service Load Calculations'; (A) is the same "
            "100 A / 3-wire qualifier; (B) is still 100 percent of the first "
            "10 kVA plus 40 percent of the remainder, 3 VA/sq ft, 1500 VA per "
            "small-appliance and laundry circuit; (C) is still the largest of "
            "six selections at 100/100/100+65/65/40/100 percent. The E-3/E-4 "
            "header, footer and math all stand as written.",
            "ARTICLE 705 DOES NOT APPLY to AOG's standard install. 705.1 "
            "scopes the article to sources operating IN PARALLEL with the "
            "primary source; a standby set behind an ATS never does. 705.20 "
            "matters only as the reference 230.85(D) names for other energy "
            "sources such as PV. READ THAT NARROWLY: it is about the "
            "STANDARD install. Where the set lands behind a microgrid "
            "interconnect device into an energy storage system instead of an "
            "ATS, Article 705 is live — 705.1's own Insight says the primary "
            "source need not be the utility, so the generator parallels with "
            "the ESS inside the microgrid. See the 2023-12-31 entry below.",
            "Same numbers, editorial changes only: 250.20(D), 250.24(A)(1), "
            "250.24(B), 250.28, 250.50, 250.122; 110.25, 110.26(A), "
            "110.26(A)(1), 110.26(A)(3); 430.14(A) and (B).",
        ],
        unchecked=[
            "Article 680. AOG cites it bare, as a heading over the pool panel "
            "rather than a specific requirement, so it cannot go stale the way "
            "a subsection can — but nobody has read it.",
        ],
    ),

    # The cycle IN FORCE. Everything here is a reading of the 2020 text against
    # sheets AOG is printing today — not a move. It exists because the 2026
    # entry above records what CHANGES in 2023, and that turned out to be a
    # different question from what the 2020 text actually says. Three of the
    # findings below were errors on a delivered sheet.
    _dt.date(2023, 12, 31): dict(
        source="NFPA 70 (2020) read on link.nfpa.org — Articles 445, 705 and "
               "706 in full on 09-23-2026, against the 112 1st Ave N job: a "
               "48 kW set feeding three EG4 GridBOSS generator ports behind a "
               "microgrid interconnect device, no ATS anywhere in the job.",
        moves=[],
        additions=[
            "445.6 IS IN THE 2020 TEXT. 'Stationary generators 600 volts and "
            "less shall be listed.' It was not added in 2023. Cite it for the "
            "UL 2200 listing on every set; a sheet that omits it leaves a free "
            "compliance line on the table.",

            "445.18 IN 2020 RUNS (A) THROUGH (E) AND CARRIES NO MARKING "
            "LANGUAGE AT ALL. (A) disconnecting means, lockable open per "
            "110.25. (B) emergency shutdown of the prime mover, which must "
            "(1) disable ALL prime mover start control circuits so the engine "
            "cannot start and (2) initiate a shutdown requiring a MECHANICAL "
            "RESET. (C) remote emergency stop for sets over 15 kW, outside the "
            "equipment room or generator enclosure, and it must also meet "
            "(B)(1) and (B)(2). (D) one- and two-family dwellings — shutdown "
            "device outside the dwelling unit at a readily accessible "
            "location. (E) generators in parallel. ON A RESIDENTIAL JOB THE "
            "GOVERNING PAIR IS (C) AND (D). A sheet citing only (B) and (C) is "
            "missing the dwelling subsection, which is the one a Florida "
            "reviewer looks for. The 'GENERATOR EMERGENCY SHUTDOWN' label is "
            "NOT required by 445.18 in 2020 — cite 110.21(B) for the marking. "
            "The wording requirement arrives with 445.19(C) in 2023, which is "
            "why the 2026 entry above calls that a rewrite, not a renumber.",

            "445.18(B)(1) AND (2) ARE PERFORMANCE REQUIREMENTS, NOT A DEVICE "
            "TYPE. The E-stop note has to say that opening the loop disables "
            "all prime mover start control circuits and latches until "
            "mechanically reset. 'N.C. loop; opening the circuit shuts down "
            "the prime mover' describes half the requirement.",

            "445.13(A) EXCEPTION — THE EVIDENCE IS THE NAMEPLATE, NOT THE "
            "BREAKER. The Exception permits 100 percent of nameplate 'where "
            "the design and operation of the generator prevent overloading', "
            "and the Insight narrows that to inherently designed OR an "
            "overcurrent protective RELAY. 445.11(4) requires the nameplate to "
            "state which of inherent design / relay / circuit breaker / fuse "
            "protects the set. A set whose nameplate says CIRCUIT BREAKER is "
            "not obviously inside the Exception, and the general rule is 115 "
            "percent — on a 200 A set that is 230 A, which moves the feeder "
            "from 3/0 Cu to 4/0 Cu. READ THE NAMEPLATE BEFORE SIZING A "
            "GENERATOR FEEDER. Do not assume an integral main breaker buys the "
            "Exception; AOG sheets have been written as though it does.",

            "445.11 LAST PARAGRAPH — where the factory neutral-to-frame "
            "bonding is MODIFIED IN THE FIELD, additional marking is required "
            "to indicate whether the neutral is bonded. Every "
            "non-separately-derived install that lifts the factory bond owes "
            "this marking. It is an installation step, not a drafting note, "
            "and it belongs in the scope of work.",

            "706.20(C)(1) IS THE HOOK THAT DRAGS 110.26 ONTO AN ESS — 'Working "
            "spaces for ESS shall comply with 110.26 and 110.34.' On a battery "
            "job cite that rather than 110.26 bare. At 0–150 V to ground the "
            "numbers are 3'-0\" deep, 30 in. or the equipment width, 6'-6\" high "
            "measured from the floor or platform — and 110.26(A)(3) makes the "
            "space taller, not shorter, when equipment is mounted high.",

            "706.20(B) — an ESS for a one- or two-family dwelling shall not "
            "exceed 100 volts dc between conductors or to ground, unless live "
            "parts are inaccessible during routine maintenance, which opens it "
            "to 600 V. A 51.2 V nominal stack is clear; a high-voltage stack "
            "is not. Check it before quoting one.",

            "706.15(A)(1) REQUIRES THE ESS DISCONNECTING MEANS TO BE READILY "
            "ACCESSIBLE, and (A) permits it to be integral to listed ESS "
            "equipment. That is what stops a wall-mounted battery from going "
            "up where you need a ladder — Article 100 names portable ladders "
            "in the definition. 240.24(A)(4) does NOT rescue it: 706.15 is the "
            "more specific rule and Chapter 7 modifies Chapter 2. The last "
            "sentence of (A) lets a dwelling satisfy the OUTSIDE-THE-BUILDING "
            "requirement with the disconnect OR ITS REMOTE CONTROL; it does "
            "not waive (A)(1). A remote control buys location, not height.",

            "706.33(A) AND 705.13(E) — the adjustable means controlling ESS "
            "charging, and the settings of a listed power control system, "
            "shall be accessible ONLY TO QUALIFIED PERSONS. Where a job leans "
            "on a programmed generator-input current limit for its capacity "
            "argument, the scope of work has to say the setting is locked to "
            "installer level. An unlocked setting is not a control.",

            "706.5 PLUS THE 706.1 SCOPE INSIGHT — UL 9540 is a SYSTEM listing. "
            "A group of batteries, racks, charge controllers and inverters "
            "with no overall ESS listing is a storage battery system under "
            "ARTICLE 480, not 706, and a different rulebook applies. Get the "
            "9540 certificate naming the exact inverter/battery combination "
            "before writing 'UL 9540 listed system' on a riser.",

            "705.6 — interactive equipment intended to operate in parallel, "
            "'including but not limited to interactive inverters, ENGINE "
            "GENERATORS, energy storage equipment and wind turbines', shall be "
            "listed for interactive function or field-labeled for it. If the "
            "MID parallels the set rather than transferring to it, a stock "
            "standby genset does not meet this. Ask the ESS manufacturer how "
            "the generator port behaves before drawing the job — it decides "
            "whether Article 705 applies to the generator at all.",
        ],
        unchanged=[
            "702.4(B)(2) sizing against a 220.82 calculated dwelling load does "
            "not describe a generator that never serves the dwelling. Where "
            "the set feeds only the ESS generator ports through a distribution "
            "panel, and the dwelling loads are carried by the inverters off "
            "the MID's load side, the governing number is the programmed "
            "generator-input current limit, not a load calculation. Say that "
            "in the scope of work in one bullet and cite the limit; do not "
            "submit a 220.82 calc that describes a system that does not exist.",

            "Generac ESP ratings carry a note that the 24-hour AVERAGE output "
            "shall not exceed 70 percent of the rating. Charging a battery "
            "bank is flat continuous duty, which is exactly what an ESP rating "
            "is not written for, so 70 percent is the ceiling to size the "
            "generator-input limit against — not the nameplate amps. This is a "
            "manufacturer limit reaching the sheet through 110.3(B), not an "
            "NEC number.",
        ],
        unchecked=[
            "NFPA 855 and the Florida Fire Prevention Code. A residential ESS "
            "has per-unit and aggregate stored-energy caps and location "
            "restrictions that live there, not in the NEC, and fire review is "
            "a different desk from electrical. Nobody has read the edition the "
            "FFPC adopts. Do it before the next battery job.",

            "Article 480. Only matters if a 9540 system certificate turns out "
            "not to cover the installed combination — but if that happens the "
            "whole job moves out of 706 and nothing in this entry applies.",
        ],
    ),
}


# --------------------------------------------------- cycle-dependent sheet text
# A citation is a number AND the sentence around it, so the notes that carry one
# live here per cycle rather than being typed into the sheets. A package dated
# today prints the 2020 NEC wording; one dated past the flip prints the 2023
# wording. Neither can print the other's.
#
# Only notes whose CITATION or REQUIREMENT moved are here. Everything else stays
# in the sheet script where it belongs.
#
# Is the load-management scheme an Energy Management System? From the 2026 cycle
# on, 702.4(A)(2)(b) requires the EMS to comply with Article 750.30, so the
# answer decides which note prints AND how the set is sized: an EMS gets
# 702.4(A)(2)(b) and its managed capacity; anything else falls to
# 702.4(A)(2)(a) and the standby source must carry the FULL automatically
# connected load. AOG's standalone under-frequency latching relays are not
# obviously an Art. 100 energy management system — that is a real question for
# the job, not a drafting choice, so it is left None and raises rather than
# defaulting. Set it per job once it has been decided.
EMS_COMPLIANT = None          # True | False, from the 2026 cycle onward

SHEET_NOTES = {
    _dt.date(2023, 12, 31): {
        "shutdown_note":
            "THE EMERGENCY SHUTDOWN IS INSTALLED AT THE METER, OUTSIDE THE "
            "DWELLING AND READILY ACCESSIBLE, CAPABLE OF BEING LOCKED IN THE "
            "OPEN POSITION AND CLEARLY LABELED, PER NEC 445.18(D).",
        "shutdown_tag": "NEC 445.18(D)",
        "shutdown_recap":
            "EMERGENCY SHUTDOWN AT THE METER — OUTSIDE, READILY ACCESSIBLE, "
            "LOCKABLE IN THE OPEN POSITION, NEC 445.18(D)",
        "emerg_disc_note":
            "THE EXISTING 600 A SERVICE DISCONNECT IS IN A READILY ACCESSIBLE "
            "OUTDOOR LOCATION AND IS MARKED “EMERGENCY DISCONNECT, SERVICE "
            "DISCONNECT” PER NEC 230.85(1). MARKING COMPLIES WITH NEC "
            "110.21(B).",
        "emerg_disc_tag": "NEC 230.85",
        "load_mgmt_cite": "NEC 702.4(B)(2)(b)",
        "load_mgmt_note":
            "THE OPTIONAL STANDBY SYSTEM CARRIES THE ENTIRE SERVICE WITH "
            "AUTOMATIC LOAD MANAGEMENT PER NEC 702.4(B)(2)(b). MANAGED LOADS "
            "ARE DROPPED BY STANDALONE UNDER-FREQUENCY LATCHING RELAYS WIRED "
            "INLINE AT EACH MANAGED CIRCUIT. THE MANAGED SCHEME AND THE "
            "CALCULATED DEMAND ARE ON SHEETS E-3 AND E-4.",
    },
    _dt.date(2026, 12, 31): {
        # 445.18 has no (D). The device AOG installs satisfies two sections at
        # once, which 445.19(A) expressly permits where it is lockable open per
        # 110.25 — so the note names both rather than renumbering one.
        "shutdown_note":
            "ONE DEVICE AT THE METER IS BOTH THE GENERATOR DISCONNECT AND THE "
            "EMERGENCY SHUTDOWN, AS NEC 445.19(A) PERMITS: OUTSIDE, READILY "
            "ACCESSIBLE, OPENING ALL UNGROUNDED CONDUCTORS AND LOCKABLE OPEN "
            "PER NEC 110.25 (445.18(A)); DISABLING ALL START CIRCUITS WITH A "
            "MECHANICAL RESET AND MARKED GENERATOR EMERGENCY SHUTDOWN PER NEC "
            "110.21(B) (445.19(C)).",
        "shutdown_tag": "NEC 445.18(A) / 445.19(C)",
        "shutdown_recap":
            "GENERATOR DISCONNECT AND EMERGENCY SHUTDOWN AT THE METER — "
            "OUTSIDE, READILY ACCESSIBLE, LOCKABLE OPEN, MARKED GENERATOR "
            "EMERGENCY SHUTDOWN, NEC 445.18(A) / 445.19(C)",
        # The placard 230.85(D) and 702.7(A) each require lives AT the service
        # disconnect, which is what this note is already about — so it folds in
        # here rather than becoming a twelfth bullet the box cannot hold.
        "emerg_disc_note":
            "THE EXISTING 600 A SERVICE DISCONNECT IS IN A READILY ACCESSIBLE "
            "OUTDOOR LOCATION, MARKED “EMERGENCY DISCONNECT, SERVICE "
            "DISCONNECT” IN WHITE ON RED, ½ IN. LETTERS MIN., PER NEC "
            "230.85(B)(1), (E)(1), (E)(2) AND 110.21(B). A PLACARD THERE GIVES "
            "THE LOCATION OF THE GENERATOR DISCONNECT AND SHUTDOWN, PER NEC "
            "230.85(D) AND 702.7(A).",
        "emerg_disc_tag": "NEC 230.85(E)",
    },
}


def note(key, on=None):
    """Sheet text that moves with the code cycle. Raises rather than guessing."""
    on = on or JOB_DATE
    val = None
    for eff in sorted(SHEET_NOTES):
        if eff <= on and key in SHEET_NOTES[eff]:
            val = SHEET_NOTES[eff][key]
    if val is None:
        raise KeyError(
            "aoglib.note(%r): no wording is defined for the code cycle in "
            "force on %s. Add it to SHEET_NOTES." % (key, on))
    if callable(val):
        return val()
    return val


def note_opt(key, on=None):
    """Like note(), but returns None where the cycle defines no such note."""
    try:
        return note(key, on)
    except KeyError:
        return None


def _load_mgmt_2026():
    if EMS_COMPLIANT is None:
        raise RuntimeError(
            "aoglib.EMS_COMPLIANT is not set.\n\n"
            "From 12-31-2026 the load-management note depends on whether the "
            "shed scheme is an Energy Management System: 702.4(A)(2)(b) "
            "requires one that complies with Article 750.30, and anything that "
            "is not an EMS falls to 702.4(A)(2)(a), where the standby source "
            "must carry the FULL automatically connected load — which changes "
            "the generator size, not just the note.\n\n"
            "AOG's standalone under-frequency latching relays are not "
            "obviously an Article 100 energy management system. Decide it for "
            "this job, then set aoglib.EMS_COMPLIANT = True or False.\n\n"
            "Whichever way it goes, 750.30(B) forbids shedding elevators, "
            "escalators, moving walks, stairway lift chairs and emergency "
            "lighting circuits; s11_citecheck.py checks the shed list.")
    if EMS_COMPLIANT:
        return ("THE OPTIONAL STANDBY SYSTEM CARRIES THE ENTIRE SERVICE WITH "
                "AUTOMATIC LOAD MANAGEMENT BY AN ENERGY MANAGEMENT SYSTEM PER "
                "NEC 702.4(A)(2)(b) AND 750.30. NO LOAD LISTED IN NEC "
                "750.30(B) IS MANAGED. THE SCHEME AND CALCULATED DEMAND ARE "
                "ON E-3 AND E-4.")
    return ("THE OPTIONAL STANDBY SYSTEM CARRIES THE ENTIRE SERVICE AND THE "
            "STANDBY SOURCE SUPPLIES THE FULL LOAD THAT IS AUTOMATICALLY "
            "CONNECTED, PER NEC 702.4(A)(2)(a). THE CALCULATED DEMAND IS ON "
            "SHEET E-3.")


SHEET_NOTES[_dt.date(2026, 12, 31)]["load_mgmt_note"] = _load_mgmt_2026
SHEET_NOTES[_dt.date(2026, 12, 31)]["load_mgmt_cite"] = (
    lambda: "NEC 702.4(A)(2)(b)" if EMS_COMPLIANT
    else ("NEC 702.4(A)(2)(a)" if EMS_COMPLIANT is False else _load_mgmt_2026()))


def cycle_for(on=None):
    """The code cycle in force on a date — the last one already effective."""
    on = on or JOB_DATE
    live = [c for c in CODE_CYCLES if c["effective"] <= on]
    if not live:
        raise RuntimeError("No Florida code cycle is in force on %s." % on)
    return live[-1]


CYCLE = cycle_for()


class _Unread(object):
    """A standard whose edition for this cycle has not been read yet.

    It survives import, so a cycle with one gap does not stop the sheets that
    do not cite that standard — an unread NFPA 54 blocks the gas isometric and
    leaves the riser, the load calcs and the structural sheets building. It
    raises the moment a sheet tries to put it on paper, which is the only moment
    that matters: nothing reaches a reviewer with a guessed edition on it.
    """

    def __init__(self, key):
        self.key = key

    def _die(self, *_a):
        raise RuntimeError(
            "AOG sheet stack — this sheet cites %s, and the edition referenced "
            "by the code cycle effective %s has not been read yet (job date "
            "%s).\n\n%s\n\nEdit aoglib.CODE_CYCLES, or re-issue an older package "
            "under its own date with AOG_JOB_DATE=YYYY-MM-DD."
            % (self.key, CYCLE["effective"], JOB_DATE, CYCLE["note"]))

    __str__ = _die
    __format__ = _die

    def __repr__(self):
        return "<unread edition: %s>" % self.key


def _ed(key, label):
    v = CYCLE.get(key)
    return v if v is not None else _Unread(label)


FBC_EDITION = _ed("fbc", "the Florida Building Code")        # blocks — caps
FBC_TITLE = _ed("fbc_title", "the Florida Building Code")    # prose — title case
FBC_ABBR = _ed("fbc_abbr", "the Florida Building Code")      # narrow columns
NEC_EDITION = _ed("nec", "the NEC")                          # "NEC 2020 (NFPA 70)"
NEC_SHORT = _ed("nec_short", "the NEC")                      # "NEC 2020"
NFPA54_EDITION = _ed("nfpa54", "NFPA 54 / ANSI Z223.1")
ASCE7_EDITION = _ed("asce7", "ASCE 7")

# Built eagerly where it can be; an unread half defers the failure to the first
# title block drawn, which is why titleblock() calls str() on it.
CODES = (_Unread("the CODES IN FORCE line")
         if (CYCLE.get("nec") is None or CYCLE.get("fbc") is None)
         else "%s · %s" % (NEC_EDITION, FBC_EDITION))

GREY = Color(.42, .42, .42)
LGREY = Color(.86, .86, .86)


# ------------------------------------------------------------------ basics
def tx(c, x, y, s, size=7, font="Helvetica", col=black, anchor="l", rot=0):
    c.saveState()
    c.setFillColor(col)
    c.setFont(font, size)
    if rot:
        c.translate(x, y)
        c.rotate(rot)
        x = y = 0
    if anchor == "c":
        c.drawCentredString(x, y, s)
    elif anchor == "r":
        c.drawRightString(x, y, s)
    else:
        c.drawString(x, y, s)
    c.restoreState()


def box(c, x, y, w, h, lw=.8, fill=None, stroke=black):
    c.saveState()
    c.setLineWidth(lw)
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
    c.rect(x, y, w, h, stroke=1 if (stroke is not None and lw) else 0,
           fill=1 if fill is not None else 0)
    c.restoreState()


def line(c, x1, y1, x2, y2, lw=.8, col=black, dash=None):
    c.saveState()
    c.setLineWidth(lw)
    c.setStrokeColor(col)
    if dash:
        c.setDash(dash)
    c.line(x1, y1, x2, y2)
    c.restoreState()


def wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out


# --------------------------------------------------------------- title block
def titleblock(c, W, H, sheet, title, margin=18, tbw=250, stamp=170,
               licences=None, seal_label="SEAL"):
    """Right-edge vertical title block with a reserved stamp box.

    Font sizes scale with the block width so the same block reads correctly
    on a 36x24 sheet and on letter.

    ``licences`` — leave None on any sheet AOG seals itself, which is the
    default and what every sheet in this stack did before s10 joined it. Pass
    the contractor licence line only on a sheet somebody else seals; the
    SEAL box at the top is then theirs, and ``seal_label`` names whose it is.
    """
    k = max(1.0, tbw / 250.0) ** 0.72          # font scale
    p = 10 * k                                  # inner pad
    x0 = W - margin - tbw
    y0 = margin
    th = H - 2 * margin
    box(c, x0, y0, tbw, th, lw=1.4, fill=white)

    def hdr(yy, s):
        tx(c, x0 + p, yy, s, 7.0 * k, "Helvetica-Bold", GREY)
        return yy - 13 * k

    y = y0 + th
    # ---- stamp space (top)
    y -= stamp
    box(c, x0, y, tbw, stamp, lw=.8)
    tx(c, x0 + tbw / 2, y + stamp - 15 * k, seal_label, 8 * k,
       "Helvetica-Bold", GREY, "c")
    tx(c, x0 + tbw / 2, y + 11 * k, "space reserved — do not obscure",
       6.5 * k, "Helvetica-Oblique", GREY, "c")

    # ---- project
    ph = 112 * k
    y -= ph
    box(c, x0, y, tbw, ph, lw=.8)
    yy = hdr(y + ph - 15 * k, "PROJECT")
    tx(c, x0 + p, yy, JOB["addr"], 11.5 * k, "Helvetica-Bold"); yy -= 13 * k
    tx(c, x0 + p, yy, JOB["city"], 9 * k); yy -= 13 * k
    tx(c, x0 + p, yy, JOB["proj"], 8.5 * k); yy -= 16 * k
    yy = hdr(yy, "JURISDICTION")
    tx(c, x0 + p, yy, JOB["ahj"], 9.5 * k, "Helvetica-Bold"); yy -= 13 * k
    tx(c, x0 + p, yy, JOB.get("trade", "TRADE: ELECTRIC — STANDBY GENERATOR"), 7.5 * k)

    # ---- equipment
    # Height from the wrapped line count, like SCOPE below — a long second
    # equipment line overflowed into SCOPE OF WORK at the old constant 74 pt.
    _gen, _ats = wrap(JOB["gen"], 40), wrap(JOB["ats"], 44)
    eh = max(74.0, 26 + 11 * len(_gen) + 3 + 10 * len(_ats) + 4) * k
    y -= eh
    box(c, x0, y, tbw, eh, lw=.8)
    yy = hdr(y + eh - 15 * k, "EQUIPMENT")
    for ln in wrap(JOB["gen"], 40):
        tx(c, x0 + p, yy, ln, 8 * k, "Helvetica-Bold"); yy -= 11 * k
    yy -= 3 * k
    for ln in wrap(JOB["ats"], 44):
        tx(c, x0 + p, yy, ln, 7.5 * k); yy -= 10 * k

    # ---- scope
    # Height is computed from the wrapped line count, never a constant: a scope
    # longer than two lines used to overflow into CODES IN FORCE on every sheet
    # that calls titleblock(), and it is invisible unless you render and look.
    _scope = wrap(JOB["scope"], 46)
    shh = (26 + 10.5 * len(_scope)) * k
    y -= shh
    box(c, x0, y, tbw, shh, lw=.8)
    yy = hdr(y + shh - 15 * k, "SCOPE OF WORK")
    for ln in _scope:
        tx(c, x0 + p, yy, ln, 7.5 * k); yy -= 10.5 * k

    # ---- codes
    ch = 40 * k
    y -= ch
    box(c, x0, y, tbw, ch, lw=.8)
    yy = hdr(y + ch - 15 * k, "CODES IN FORCE")
    for ln in wrap(str(CODES), 50):
        tx(c, x0 + p, yy, ln, 7 * k); yy -= 9.5 * k

    # ---- company
    # Height computed from the line count for the same reason the scope box is
    # — a licence line added below a four-line company block overflowed into
    # the sheet-id box the first time s10 called this with licences set.
    _co = list(CO) + ([licences] if licences else [])
    coh = max(74.0, 24 + 13 + 10 * (len(_co) - 1)) * k
    y -= coh
    box(c, x0, y, tbw, coh, lw=.8)
    yy = hdr(y + coh - 16 * k, "DESIGNED BY")
    tx(c, x0 + p, yy, _co[0], 12 * k, "Helvetica-Bold"); yy -= 13 * k
    for s in _co[1:]:
        tx(c, x0 + p, yy, s, 7.5 * k); yy -= 10 * k

    # ---- sheet id (bottom)
    box(c, x0, y0, tbw, y - y0, lw=.8)
    tx(c, x0 + p, y - 18 * k, "DATE", 7 * k, "Helvetica-Bold", GREY)
    tx(c, x0 + p + 62 * k, y - 18 * k, JOB["date"], 8.5 * k)
    tx(c, x0 + p, y - 33 * k, "SCALE", 7 * k, "Helvetica-Bold", GREY)
    tx(c, x0 + p + 62 * k, y - 33 * k, "AS NOTED", 8.5 * k)
    for i, ln in enumerate(wrap(title, 26)):
        tx(c, x0 + p, y0 + (44 + 13 * (len(wrap(title, 26)) - 1 - i)) * k,
           ln, 11 * k, "Helvetica-Bold")
    tx(c, x0 + tbw - p, y0 + 10 * k, sheet, 36 * k, "Helvetica-Bold", anchor="r")
    return x0


def footer_note(c, x, y, w):
    tx(c, x, y, "Prepared by Always On Generators for permit submittal. "
                "Installation is in accordance with the codes in force and the "
                "manufacturer's installation instructions.",
       6.2, "Helvetica-Oblique", GREY)
