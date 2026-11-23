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

# The larger table: all subgroups (DICTO, 24 November 2026)

"The Non-Periodic Table of the Aequi — all subgroups" (draft title). **All 4553 Aequi of study 2026-11-19-aequi-complete: 22 rows
(Ih 120 … Ci 2) × m = 2..7; counts equal that study's data/counts.md and data/table.csv cell by cell, total 4553.** Same design as above,
three dice per cell side by side. Too tall for one A4-wide page, so two panels, one page each: (a) groups of order 12 or more (13 rows),
(b) order less than 12 (9 rows, with the column totals and the key).

Vacuus kind, computed here for every die from its face planes (the 4553 were not classified before): **3159 heart, 1370 inherited heart,
24 non-heart.** Heart exactly when the full group contains −I (all 4553); the 149 dice also in the 1232 classification get the same kind
(149 of 149). Non-heart dice lie in T (2), D3 (10), D2 (11) and S4 (1). Depths compared at 60 digits (equal within 1e-40); no die has every
face paired with a parallel face at a different depth.

Colours: the app's face colours; an orbit mixing two families (for example C6+RT24/10) takes the colour of its icosahedral family, an
O8/4 orbit is the tetrahedron's red, and a second orbit of one colour in a die is drawn paler.

- scripts/make_table_all.py (python3 make_table_all.py <this study> <study 2026-11-19-aequi-complete>; reads its data/dice/*.json,
  counts.md, table.csv and scripts/groups.py for the 74 directions).
- data/all-cells.csv (every filled cell: counts by Vacuus kind, drawn dice), data/all-dice-kinds.csv (Vacuus kind of each of the 4553),
  data/all-checks.log.
- figures/aequi-table-all-a.svg, figures/aequi-table-all-b.svg, figures/aequi-table-all.pdf (two pages); figures/all/paper.html for
  figcheck: FIGCHECK OK.
