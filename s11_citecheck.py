#!/usr/bin/env python3
"""Citation check — which sheets still cite a section the code has moved.

Not a sheet. A pre-flight, in the same spirit as the overflow asserts: a wrong
code section on a submitted drawing is a correction letter, and the cheapest
place to catch one is before the package is built.

It reads `aoglib.CITATION_MOVES` and greps the sheet scripts for the superseded
citations belonging to every cycle that is in force on the job date. It does
NOT edit anything. A citation is a number and the sentence around it, and
swapping the number into an old sentence produces a note that reads correct and
is wrong — so this prints what to go rewrite and stops there.

    python3 s11_citecheck.py                    # against today's job date
    AOG_JOB_DATE=2027-01-05 python3 s11_citecheck.py

Exit status is 1 when a superseded citation is still on a sheet, so it can gate
a build:

    python3 s11_citecheck.py && python3 s9_loadcalc.py
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aoglib as A

HERE = os.path.dirname(os.path.abspath(__file__))
SKIP = {"s11_citecheck.py", "aoglib.py"}

BOLD, DIM, RED, ORANGE, GREEN, OFF = (
    "\033[1m", "\033[2m", "\033[31m", "\033[33m", "\033[32m", "\033[0m")
if not sys.stdout.isatty():
    BOLD = DIM = RED = ORANGE = GREEN = OFF = ""


def wrap(s, n=76, indent=""):
    out, cur = [], ""
    for w in s.split():
        if len(cur) + len(w) + 1 > n and cur:
            out.append(indent + cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(indent + cur)
    return "\n".join(out)


def sheets():
    for p in sorted(glob.glob(os.path.join(HERE, "*.py"))):
        if os.path.basename(p) not in SKIP:
            yield p


# 750.30(B) — loads an energy management system shall not disconnect. From
# 12-31-2026 this stops being only AOG's air-handlers-only convention and
# becomes a code requirement, because 702.4(A)(2)(b) pulls 750.30 in by
# reference. Patterns are deliberately loose; a false flag costs a glance.
PROTECTED = [
    ("elevator", "750.30(B)(1) elevators"),
    ("escalator", "750.30(B)(1) escalators"),
    ("moving walk", "750.30(B)(1) moving walks"),
    ("stair lift", "750.30(B)(1) stairway lift chairs"),
    ("stairway lift", "750.30(B)(1) stairway lift chairs"),
    ("chair lift", "750.30(B)(1) stairway lift chairs"),
    ("emergency light", "750.30(B)(4) circuits supplying emergency lighting"),
]


def shed_rows():
    """Every load carrying a shed flag, as (source, description)."""
    rows = []
    try:
        import paneldata as P
    except Exception as exc:
        return rows, "paneldata.py did not import (%s)" % exc
    for name in dir(P):
        pan = getattr(P, name)
        if not isinstance(pan, dict) or "odd" not in pan:
            continue
        for side in ("odd", "even"):
            for r in pan.get(side) or []:
                if isinstance(r, tuple) and len(r) >= 9 and r[8]:
                    rows.append(("paneldata.py %s" % pan.get("name", name), r[2]))
    try:
        import s9_loadcalc  # noqa: F401 — only for SHED_UNITS
    except Exception:
        pass
    else:
        for u in getattr(s9_loadcalc, "SHED_UNITS", []) or []:
            rows.append(("s9_loadcalc.py SHED_UNITS", u))
    return rows, None


def check_shed(enforced):
    rows, err = shed_rows()
    print("\n%sSHED LIST vs 750.30(B)%s" % (BOLD, OFF))
    if err:
        print("   %s%s — not checked%s" % (ORANGE, err, OFF))
        return 0
    if not rows:
        print("   %sno shed-flagged loads found%s" % (DIM, OFF))
        return 0
    bad = []
    for src, desc in rows:
        low = (desc or "").lower()
        for pat, why in PROTECTED:
            if pat in low:
                bad.append((src, desc, why))
    print("   %d shed-flagged load(s) checked" % len(rows))
    if not bad:
        print("   %s✓ none of them is a load 750.30(B) protects%s" % (GREEN, OFF))
        return 0
    for src, desc, why in bad:
        print("   %s✗ %s — %s%s" % (RED, desc, src, OFF))
        print(wrap("An energy management system shall not disconnect this: %s. "
                   "Take it off the shed list." % why, indent="      "))
    return len(bad) if enforced else 0


def main():
    cycles = [(d, c) for d, c in sorted(A.CITATION_MOVES.items())
              if d <= A.JOB_DATE]
    print("%sCITATION CHECK%s  job date %s  ·  %s"
          % (BOLD, OFF, A.JOB_DATE, A.FBC_EDITION))

    if not cycles:
        pending = [d for d in sorted(A.CITATION_MOVES) if d > A.JOB_DATE]
        print("\n%sNo citation moves in force yet.%s" % (GREEN, OFF))
        for d in pending:
            print("  Next cycle %s — preview it with "
                  "AOG_JOB_DATE=%s python3 s11_citecheck.py" % (d, d))
        check_shed(enforced=False)
        return 0

    files = {p: open(p, encoding="utf-8").read() for p in sheets()}
    stale = 0

    for eff, cyc in cycles:
        print("\n%s── cycle effective %s %s" % (BOLD, eff, OFF))
        print(DIM + wrap(cyc["source"], indent="   ") + OFF)

        for m in cyc["moves"]:
            hits = sorted(os.path.basename(p) for p, t in files.items()
                          if m["old"] in t)
            tag = ("%sREWRITE%s" % (RED, OFF) if m["rewrite"]
                   else "%sRENUMBER%s" % (ORANGE, OFF))
            mark = "%s✗%s" % (RED, OFF) if hits else "%s✓%s" % (GREEN, OFF)
            print("\n %s %s  %s → %s   [%s]"
                  % (mark, BOLD + m["old"] + OFF, "", m["new"], tag))
            print(wrap(m["note"], indent="     "))
            if hits:
                stale += len(hits)
                print("     %sstill on:%s %s" % (RED, OFF, ", ".join(hits)))
            else:
                print("     %snot found on any sheet%s" % (DIM, OFF))

        if cyc.get("additions"):
            print("\n %sNEW REQUIREMENTS — no old citation to grep for%s"
                  % (BOLD, OFF))
            for a in cyc["additions"]:
                print(wrap("· " + a, indent="   "))

        if cyc.get("unchanged"):
            print("\n %sCONFIRMED UNCHANGED%s" % (BOLD, OFF))
            for u in cyc["unchanged"]:
                print(wrap("· " + u, indent="   "))

        if cyc.get("unchecked"):
            print("\n %sNOT READ YET — absence of a flag is not a clean bill%s"
                  % (ORANGE, OFF))
            for u in cyc["unchecked"]:
                print(wrap("· " + u, indent="   "))

    stale += check_shed(enforced=True)

    print()
    if stale:
        print("%s%d item(s) to fix before this package goes out.%s "
              "Rewrite the notes, then re-run." % (RED, stale, OFF))
        return 1
    print("%sClean — no superseded citations, no protected load on the shed "
          "list.%s" % (GREEN, OFF))
    return 0


if __name__ == "__main__":
    sys.exit(main())
