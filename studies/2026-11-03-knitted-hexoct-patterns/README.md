# Knitted HexOct: Patterns (3 November 2026)

Knitter-ready patterns for DICTO's Knitted HexOct test pieces T-c (A-B-C) and T-h (A-B-A′), and the five stacking sequences of #83
(3C, 2H, 4H, 6H, Fibonacci) as three-dimensional stacks of knitted sheets and cords, from the spec of studies/2026-11-02-knitted-hexoct
(garter sheets with marked node stitches, 3-stitch i-cord links, self-centring by tension).

**Conclusion:** one sheet instruction (row by row, node table, chart with nodes 1–9) serves every sheet; shared techniques (node stitch,
lacing, cord, sewing, finishing, measuring, card template, cells) appear once, each illustrated; T-c and T-h each have their own stacking
plan, step-by-step assembly (all 42 cords, 3D view after each stage) and check; c against h once; stacking sequences with the rule for any
word, Fibonacci growth (a → ab, b → a), and per sequence offsets, cord rule per gap, side and 3D views, size, materials and checks.
Every number generated and checked by script: 27 nodes, 42 links, node stitches 9 + 16i + 8j on rows 13/41/69, link length a at 54.7356°,
#75 tile closed around B5 (c-tile in T-c, h-tile in T-h); sequence words agree with #83 v3 (swatch table) and #83 v4 part 2 (c/h of the
12-sheet words and their mean Hägg symbols); 21 cords and 4 · 4 · 4 cells in every gap.
**Status:** booklet typeset `~/Documents/papers-to-read/knitted-hexoct-patterns.pdf` (29 pp, restructured 3 Nov after DICTO's read of the
18-page version), awaiting DICTO's read; pattern, not published, no DOI; not yet test-knitted. Stack yarn amounts are estimates
(55 m per sheet, 1 m per cord).

## Files
- `scripts/patterns.py` → `paper.html`, `figs/*.svg`, `data/check.out`. Run on dicto-big-brother with ~/geom/bin/python:
  `python patterns.py <out dir> <dir with tiles.py, engine.py, stackings.py>` (the #75 scripts; used: ~/kres-tmp/knitted-hexoct);
  out dir ~/kres-tmp/knitted-hexoct-patterns/print/papers/knitted-hexoct-patterns.
- Printed there with `node print.mjs knitted-hexoct-patterns knitted-hexoct-patterns.pdf "Knitted HexOct: Patterns" "pattern, not published"`
  (in ~/kres-tmp/knitted-hexoct-patterns/print/papers).
- Figures: `chart.svg` the sheet; `nk`, `mark`, `icord`, `attach`, `lace`, `hang`, `measure`, `card` technique drawings; per piece
  `piece-*`, `side-*`, `layout-*`, `stage1-3-*`, `cells-*`; `ch.svg` c against h; `seq-<name>-side/3d.svg` the sequences.
