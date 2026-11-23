# The Non-Periodic Table of the Aequi: draft figure (24 November 2026)

Draft paper figure (later an app view; the app is unchanged). Title "The Non-Periodic Table of the Aequi" is DICTO's (draft, his to confirm).

**Verdict: all 1232 Aequi fall in 6 rows × 10 columns, 37 filled cells; the counts match every source table cell by cell.**

- Rows: full symmetry group, by group order: Ih 120, Oh 48, O 24, Td 24, Th 24, T 12 (ties at 24 in the picker's order).
- Columns: m = number of face orbits under the full group, 2 to 11.
- Each cell: the count; up to three thumbnails (all when three or fewer; otherwise fewest, median and most faces), face count beside each.
  Empty cells are left blank. Row totals at right, column totals below.
- Vacuus kind (DICTO's names): the kind follows the row (Ih, Oh, Th heart; O, Td, T inherited heart), except the 5 non-heart dice,
  marked "○ k" in their cells: Td m=2 (2), T m=2 (2), T m=3 (1).
- Render: orthographic from a general direction, solid flat-shaded faces in the app's face colours (paler tone = the app's second-place
  colour), crisp dark edges, no haze; each die scaled to its own circumradius. Vector SVG and PDF, 180 mm wide.

## Notes against the brief

- The brief expected rows down to Ci 2 and columns m = 2..7. Those ranges belong to the 4553 Aequi over all subgroups (study
  2026-11-19-aequi-complete). The 1232 (the picker set) have only the six groups that contain the frame rotation group T, and m runs to 11
  (the two-placements dice under T). The figure shows the 1232 as they are.

## Checks (data/checks.log)

- Picker table (group, m) = classification CSV table; CSV row n = picker die n for group, m and N (all 1232).
- Picker part A (149) = the frame-group rows (Ih, Oh, Td, Th, T) of 2026-11-19-aequi-complete/data/counts.md; part B (1083) =
  2026-11-20-aequi-two-placements/data/counts.md; cell by cell, no discrepancy. Total 1232.
- Each rendered die has exactly its N faces (assert). figcheck.mjs: FIGCHECK OK (figure inside the A4 text column).

## Files

- scripts/make_table.py: checks, cells, figure (python3 make_table.py <study folder>; numpy, scipy, matplotlib).
- data/inputs/: the picker data (k-mix aequi/dice.json), the Vacuus classification CSV (2026-11-24-aequi-vacuus-scutoids), the two
  source count tables. data/cells.csv: every filled cell with counts by Vacuus kind and the drawn dice (picker number: faces).
- figures/aequi-table.svg, figures/aequi-table.pdf; figures/paper.html (wrapper for figcheck).

Credit: the dice and their data are from the studies named above; the face colours are the Aequi picker's.
