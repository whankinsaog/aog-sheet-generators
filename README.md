# AOG Sheet Generators

Python + reportlab scripts that build the Always On Generators permit sheets.
These are the **source of truth for how an AOG permit sheet looks**. The
`permit-packet` skill describes the decisions behind them; this folder is what
actually draws them.

First built on **3085 Fort Charles Dr, Naples** (Sept 2026). Every layout choice
in here was reviewed by Brandon on that job.

## The sheets

| Script | Sheet | Size |
|---|---|---|
| `s1_siteplan.py` | SP-1 Site Plan | survey overlay |
| `s5_clearance.py` | SP-2 Generator Clearances | 36×24 |
| `s2_riser.py` | E-1 Riser Diagram | 36×24 |
| `s3_panel.py` | E-2 Panel Schedules | 36×24 |
| `s9_loadcalc.py` | E-3 Unmanaged + E-4 Managed Load Calc | letter portrait |
| `s6_sow.py` | Scope of Work | overlay on the company PDF |
| `s7_isometric.py` | G-1 Gas Piping Isometric | 17×11, SVG → cairosvg |
| `s8_sheetnum.py` | sheet number onto an externally-produced PDF | any |
| `s10_padstand.py` | S-1 / S-2 aluminum stand on a precast foam-core pad | 17×11 |

`aoglib.py` — shared: job data, the title block with reserved stamp space, the
company block, `tx` / `box` / `line` / `wrap` helpers.
`paneldata.py` — the engineer's panel schedules transcribed circuit by circuit.

**`s7_isometric.py` is the one exception to the stack.** A true 30° isometric is
written as SVG by hand and rasterised by `cairosvg` (`pip install cairosvg`),
not drawn in reportlab. It is 17×11 and monochrome — colour on gas linework
reads as a second pipe material. It still follows the house rules: title block
bottom-right, no licence numbers, no personal names. It reads `aoglib` for the
job date and address when they are left as `None` at the top of the file, so it
cannot disagree with the rest of the package. First built on **112 1st Ave N,
Naples** (Sept 2026) and reviewed line by line by Brandon on that job.

**`s10_padstand.py` is the first sheet in the stack somebody else seals.** It is
an in-house structural markup of the AOG aluminum generator stand sitting on a
precast foam-core pad, drawn so an engineer can review it and stamp it — AOG
stops buying a one-permit licence for somebody else's sealed pad-and-stand
document every time a job needs one. Two consequences, and both are arguments to
`aoglib.titleblock()` rather than a second title block:

- `licences="ECI3007388 · LI100055"` — the contractor licence numbers **print**
  here. They come off only on a sheet Brandon seals himself. Leave the argument
  out and the block behaves exactly as it always did.
- `seal_label="ENGINEER OF RECORD — SEAL"` — the reserved box at the top of the
  title block is the engineer's, not AOG's.

It also overrides `aoglib.JOB` and `aoglib.CODES` in its own file, because it is
a standard detail with no address and a structural code list. Nothing else in the
stack does that; do not copy the pattern onto a job sheet.

The honest part is the point of the sheet: the stand geometry comes from the AMG
Structural Engineering air-cooled master set, which is sealed for the stand on a
**cast-in-place slab** and stops at **4'-0"**. The precast pad is a different
host. S-1 carries an OPEN ITEMS block naming what the engineer still has to
decide — starting with the anchor, since the sealed slab detail uses 5/16" × 4¾"
anchors at full embed and a 4" precast pad cannot take them. Do not quietly
resolve an open item by copying a number off somebody else's sealed drawing.

**`s8_sheetnum.py` is a utility, not a sheet.** When a calc or a spec sheet comes
from outside the stack and only needs a sheet number, this stamps one into the
clear strip at the foot of the page without touching the content — so the
reviewed numbers stay byte-identical. It checks `/Rotate`, and it *measures* the
clear space by rasterising the page at 150 dpi and finding the last row with ink,
then refuses to stamp if the number would land on existing content.
`python3 s8_sheetnum.py in.pdf out.pdf E-3`

## Overlaying someone else's PDF

`s1_siteplan.py` and `s8_sheetnum.py` both composite onto a source PDF. Use
**pikepdf `page.add_overlay()`**, not pypdf's `merge_page`: on the 614 5th Ave
survey, `merge_page` concatenated the two content streams and emitted an invalid
`QQ` operator that silently killed the whole page — it rendered as the untouched
original, so it looked like nothing had happened rather than like an error.
Verify by `pdftotext`, not by the script exiting cleanly.

Mask a superseded region only with a deliberate `fill=white` rectangle, and only
where the old numbers must not survive beside the new ones. Sample the source's
own colours off a raster so the patch is indistinguishable, and measure the mask
rectangles off that raster rather than guessing coordinates.

## Running a new job

1. Copy this folder next to the new job.
2. Edit **`aoglib.py` → `JOB`**: address, city, project, AHJ, generator, ATS,
   scope. Nothing else in that file is per-job.
3. Edit **`paneldata.py`**: transcribe the engineer's panel schedules, circuit by
   circuit. Row format is
   `P(first_ckt, poles, description, wire, conduit, brkr_type, trip, values, shed)`.
   Set the `shed` flag (`M`) on the **air handler circuits only** for managed
   systems — see below.
4. Edit **`s9_loadcalc.py`** content block: `STEP1`, `HVAC`, `STEP3`, `POOL`,
   `COOKING`, `DRYER`, then `PRIORITY` and `SHED_UNITS` once Brandon has picked
   the shed list.
5. `mkdir -p out && python3 s3_panel.py && python3 s9_loadcalc.py && ...`

## The date

Nothing hard-codes a date. `aoglib.py` computes it once:

```python
JOB_DATE   = today, unless AOG_JOB_DATE=YYYY-MM-DD is set
DATE_SHORT = "09-14-2026"        # title blocks
DATE_LONG  = "September 14, 2026" # load calc footer
```

Every sheet reads those, so the package can never carry two dates. To re-issue
an old package under its original date:
`AOG_JOB_DATE=2026-09-14 python3 s3_panel.py`

## The code edition

Nothing types "8th Edition" or "NEC 2020" any more. `aoglib.py` holds
`CODE_CYCLES`, one row per Florida triennial edition with its effective date,
and derives the edition in force **from `JOB_DATE`** — the code that applies is
the code in force on the permit date, and one constant already owns that date.

```python
FBC_EDITION      # "FLORIDA BUILDING CODE 8TH EDITION (2023)"  — drawing blocks
FBC_TITLE        # "Florida Building Code, 8th Edition (2023)"  — prose
FBC_ABBR         # "FBC 8TH ED. (2023)"                         — narrow columns
NEC_EDITION      # "NEC 2020 (NFPA 70)"
NEC_SHORT        # "NEC 2020"
NFPA54_EDITION   # "NFPA 54 / ANSI Z223.1 (2021)"
ASCE7_EDITION    # "ASCE 7-22"
CODES            # NEC_EDITION · FBC_EDITION — the title block line
```

Seven places read them, and that is the whole list: the title block (`aoglib`),
the riser general notes (`s2`), the scope of work (`s6`), the gas isometric
note 1 (`s7`), the load calc header and footer (`s9`), and both the code line
and the design-criteria table on the pad/stand sheet (`s10`).

**The 9th Edition (2026) row is already in the table, effective 12-31-2026** —
FBC 9th Edition, **NEC 2023 (NFPA 70)** and **ASCE 7-22**, all read off Chapter
35 of the Building volume (FLBC2026V1.0) on 09-17-2026. ASCE 7 does not move
this cycle, so the wind criteria on the structural sheets stay put.

**NFPA 54 is the one entry that is a choice, not a lookup.** Florida does not
adopt it by reference — it is the companion citation AOG puts beside the FL Fuel
Gas sections, because the two number the same requirements differently. It is
paired to **(2024)** to match the base, since the 9th Edition Fuel Gas volume is
the 2023 volume updated to the 2024 IFGC. One line changes it.

The row is complete, so every sheet builds past the flip. Preview with:

```
AOG_JOB_DATE=2027-01-05 python3 s9_loadcalc.py     # cites NEC 2023
AOG_JOB_DATE=2027-01-05 python3 s7_isometric.py    # cites NFPA 54 (2024)
```

An edition left as `None` is an `_Unread` sentinel rather than a crash at
import: it survives until a sheet tries to *print* it, so a future gap stops
only the sheets that cite that standard and leaves the rest building. Nothing
can reach a reviewer carrying a guessed edition.

**Section numbers are not editions, and this table does not touch them.** The
2023 NEC reorganized Article 220 and rewrote 230.85. After the flip the load
calc header will read "NEC 2023 ART. 220 PART IV, 220.82" and the riser will
still cite 230.85 — both have to be *read against the 2023 text* and rewritten,
not renumbered and not assumed to have survived. Do that before the first 2027
package goes out.

Two things live outside this file and do **not** follow automatically — change
them in the same pass: `User Info!B18` in the load calculation workbook, and the
editions table in the `permit-packet` skill.

## Citations — `s11_citecheck.py`

Editions and section numbers are different problems. `CODE_CYCLES` moves the
edition; **nothing moves a citation automatically, on purpose.** A citation is a
number *and* the sentence around it, and dropping a new number into an old
sentence gives you a note that reads correct and is wrong.

`aoglib.CITATION_MOVES` records what was actually read in the 2023 NEC — three
moves, seven new requirements, one confirmed-unchanged, and an explicit list of
what has **not** been read. `s11_citecheck.py` greps the sheets for the
superseded citations and prints the note to rewrite beside each hit.

```
python3 s11_citecheck.py                        # against today's job date
AOG_JOB_DATE=2027-01-05 python3 s11_citecheck.py
python3 s11_citecheck.py && python3 s9_loadcalc.py   # gate a build on it
```

Exit status is 1 while a stale citation is still on a sheet. Today it is quiet;
dated past the flip it flags five, across `s2_riser.py`, `s9_loadcalc.py` and
`paneldata.py`.

The two that are rewrites, not renumbers:

- **445.18(D) → 445.19(C).** 445.18 no longer has a (D). Prime-mover shutdown
  moved to 445.19, and (C) is the dwelling case — a shutdown device outside the
  dwelling, marked *Generator Emergency Shutdown*. That is a different
  requirement from the old lockable-disconnect note, which is now 445.18(A). The
  riser needs both notes, not one renumbered one.
- **702.4(B)(2)(b) → 702.4(A)(2)(b).** Load management now has to be an Energy
  Management System *per Article 750.30*. Read 750.30 against the shed scheme
  before the first 2027 managed calc.

And two new placards that are job deliverables rather than drafting notes:
230.85(D) and 702.7(A) both want a sign at the service emergency disconnect
giving the location of the generator disconnect / shutdown means, and
230.85(E)(2) now specifies red background, white text, ½ in. letters.

It also checks the **shed list against 750.30(B)**. From 12-31-2026 that stops
being house style and becomes code: because 702.4(A)(2)(b) pulls 750.30 in, an
energy management system may not disconnect elevators, escalators, moving walks,
stairway lift chairs or emergency lighting circuits. AOG already sheds air
handlers only, so nothing breaks — but "shed the elevator to drop a genset size"
is now a violation rather than a judgement call, and the check will say so.

**The unchecked list is part of the record.** Every citation printed on an AOG
sheet has now been read against the 2023 text except Article 680, and that one
is named in the report rather than left silent. Nothing flagged is not the same
as nothing wrong.

Worth knowing from the second pass: **220.82 is intact, arithmetic included** —
the 10 kVA / 40 percent split, the 3 VA/sq ft, and the six heating-and-cooling
selections are all unchanged, so the load calc math does not move. And **Article
705 does not apply** to a standby set behind an ATS; 705.1 scopes it to sources
operating in parallel.

## House style — do not drift

- **Letter portrait** for load calcs, **36×24** for the large sheets.
- **AOG orange** `Color(.76, .38, .08)` — section rules, sheet accents, the
  generator callout.
- **Managed red** `Color(.78, .05, .09)` — the **M** markers on E-2 and the
  managed rows on the E-4 ladder. Red means load-managed everywhere in the
  package, nothing else.
- Title block on the right edge, **stamp space reserved at the top**, and **no
  licence numbers** on any sheet Brandon seals himself.
- Body text Helvetica 7.2 pt, section heads 7.6 pt bold in orange over a 0.9 pt
  orange rule, notes 6.2 pt grey.

## Two rules that are easy to get wrong

**Load-shed modules land on the air handler circuit only.** The condenser has no
independent control power, so it drops with its air handler. One module per
system; the count of red **M** markers equals the module count.

**Panel schedules never restate the engineer's load-summary block** (TOTAL
CALCULATED LOAD etc.). That is NEC 220 Part III standard-method math; the
submitted calc is 220.82 optional method on E-3/E-4. Two calculated loads in one
package is a denial. Column totals stay; the summary box goes.

## Glyphs

reportlab base-14 fonts are WinAnsi. Anything outside it prints as a solid black
box with no warning — `²`, `φ`, `◀`, `◂` have all bitten. Test with
`ch.encode('cp1252')` before putting a character on a sheet. Safe: `—` `·` `×`
`Ø` `¼` `¾`.

## Portable generator inlet + interlock jobs — `s2_riser_inlet.py`, `s1_siteplan_inlet.py`

First built on **1912 Jung Blvd E, Naples (Collier County)**, Sept 2026. A
different riser, not a variant of `s2_riser.py`: no ATS, no generator feeder,
no load shed. The listed CSED interlock kit (Square D RCGK2 on a Homeline RC-series meter-main here — the QCGK3 is QO/QOA only; match the kit to the CSED series on the label) is the
transfer equipment, NEC 702.5, and the backfed breaker is secured per 408.36(D).

- **Three states in the legend:** solid red new · dashed black existing ·
  **dotted grey = by owner, not part of this permit** (the portable generator
  and its cord set).
- **No load calc** — manual transfer, the user selects the load, NEC
  702.4(B)(1). Say so on the sheet rather than leaving the reviewer to wonder.
- **No emergency shutdown** — NEC 2020 445.18(D) excludes cord-and-plug-connected
  portable generators. One-line note, because it is a deliberate omission.
- **Neutral is not switched**, so the generator must be floating-neutral, and
  the inlet carries the NEC 702.7(C) warning sign — drawn on the sheet.
- The generator breaker goes in the positions the kit's own bulletin names
  (QCGK3: 2 and 4 nearest the service disconnect). Read the bulletin per kit.
- `s1_siteplan_inlet.py` masks nothing: it measures clear space off a 72 dpi
  raster, asserts zero ink there, and adds a keynote bubble + notes block.

`aoglib.titleblock()` changes made on this job: the TRADE line reads
`JOB["trade"]` (defaults to the old standby wording), and the EQUIPMENT box
height is computed from its wrapped line count — the constant 74 pt overflowed
into SCOPE OF WORK on a long `JOB["ats"]` line.
