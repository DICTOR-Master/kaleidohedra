# Knitted HexOct Cushion: Plan (3 November 2026)

DICTO chose the object for the Knitted HexOct (#83, DICTO proposed): one square cushion that serves as seat cushion and pillow.
This is the PLAN for his approval (no full pattern yet). It replaces the rejected patterns booklet (studies/2026-11-03-knitted-hexoct-patterns).

**Plan:** 40 × 40 cm, about 6.5 cm deep, 3 garter sheets A-B-C (middle sheet c), a = 36.4 mm (8 st DK), d = 29.7 mm, 126/126/136 nodes,
721 links. Method: the three sheets knitted by hand in step on three needles; each link cord knitted into the node stitches of both sheets
(spacer-fabric principle), one V and one single link per node and gap (493 pieces, 1214 catches). Fill (carded wool) pushes, cords pull;
side walls picked up and closed by three-needle bind-off; boxed cover with zip. Trial pair T-c / T-h first (press and shear test).
Estimate: ~560 m DK cotton, ~56 m 1 mm polyester cord, 400–500 g wool, ~65 h for the cushion.
Part 2 block tests rerun for 3 and 4 sheets (data/out_*.json): free shear links-only rigid joints c 0.193 vs h 3.708 (19.2×); 4 sheets 7.5×.

**Status:** plan typeset `~/Documents/papers-to-read/hexoct-cushion-plan.pdf` (4 pp); DICTO: "cushion plan ok", then "sounds too much but maybe a
patch is enough to start with". So the next step is the **patch pattern** (below), not the full cushion pattern. Not published, nothing knitted.

## Patch pattern (3 November 2026)
Knitter-ready pattern for ONE patch, the plan's trial piece c (A-B-C), on the plan's lattice (a = 8 st, node rows every 7 ridges, same offsets
and rounding): 35 st x 33 ridges (15.9 x 15.0 cm), 16 + 16 + 16 nodes, 80 links (40 + 40) from 56 cord pieces (24 V of 14 cm, 32 singles of
9 cm), 136 catches; 32 link pairs straight on through B. Three needles in step (row 1 A, B, C; turn the stack; row 2 C, B, A); cords going up
caught on row 1, going down on row 2; far ends caught at the card length a, stopper knots. Card gauge printed at true size (measured 90.3 mm
card, 50.5 mm check bar at 300 dpi). The h patch (A-B-A) differs only in sheet 3's node positions (= sheet A's); 80 links, 56 pieces.
Typeset `~/Documents/papers-to-read/hexoct-patch-pattern.pdf` (7 pp), pattern, not published, awaiting DICTO's read.

## Files
- `scripts/pattern.py <out>` + `scripts/pattern.src.html` → `patch/paper.html`, `patch/figs/*.svg`, `patch/data/check.out` (52 asserted checks),
  `patch/data/patch.json`. Run on dicto-big-brother with ~/geom/bin/python (stdlib only) in ~/kres-tmp/hexoct-patch; printed in ~/kres-tmp/cw-print:
  `node print.mjs hexoct-patch-pattern hexoct-patch-pattern.pdf "Knitted HexOct Patch: Pattern" "none (pattern, not published)" 1`.
- `scripts/plan.py <out> [png dir]` → `figs/*.svg`, `data/numbers.json`, `data/check.out` (run on dicto-big-brother, ~/geom/bin/python;
  run in ~/kres-tmp/hexoct-cushion/study with data/out_*.json beside it). Optional png dir = check renders, scratch only.
- `data/out_<labels>_<links|full>.json`: mech.py of studies/2026-11-02-hexoct-knit-mechanics, task `blockL:<labels>:frame:<variant>`.
- Printed in ~/kres-tmp/cw-print: `node print.mjs hexoct-cushion-plan hexoct-cushion-plan.pdf "Knitted HexOct Cushion: Plan" "none (plan for approval, not published)" 1`.
