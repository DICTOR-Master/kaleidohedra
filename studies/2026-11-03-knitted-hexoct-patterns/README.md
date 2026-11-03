# Knitted HexOct: Patterns (3 November 2026)

Knitter-ready patterns for DICTO's Knitted HexOct test pieces T-c (A-B-C) and T-h (A-B-A′), from the spec of
studies/2026-11-02-knitted-hexoct (garter sheets with marked node stitches, 3-stitch i-cord links, self-centring by tension).

**Conclusion:** both pieces written out in full (3 sheets with row-by-row instructions and charts, all 42 links, joining,
finishing, check-your-work with 3D figures and a true-size 54.7° card template); every number generated and checked by script:
27 nodes, 42 links, node stitches 9 + 16i + 8j on rows 13/41/69, link length a at 54.7356°, and around node B5 the four pieces of
the #75 tile (λ = −1/8) are closed cells of the piece (c-tile in T-c, h-tile in T-h).
**Status:** booklet typeset `~/Documents/papers-to-read/knitted-hexoct-patterns.pdf` (18 pp), awaiting DICTO's read; pattern,
not published, no DOI; not yet test-knitted.

## Files
- `scripts/patterns.py` → `paper.html`, `figs/*.svg`, `data/check.out`. Run on dicto-big-brother with ~/geom/bin/python:
  `python patterns.py <out dir> <dir with tiles.py, engine.py, stackings.py>` (the #75 scripts; used: ~/kres-tmp/knitted-hexoct).
- Printed with papers/print.mjs (copy in ~/kres-tmp/knitted-hexoct-patterns/print/papers, footer
  "Knitted HexOct: Patterns · DICTO · dictospheres.com · pattern, not published").
- Figures: `chart-<piece>-<sheet>.svg` stitch charts; `piece-*.svg` the tensioned piece; `cells-*.svg` sheet B's tile pieces
  (gold tetrahedral, violet octahedral halves, teal cords); `ch-*.svg` c against h (section + plan); `card.svg` true-size template.
