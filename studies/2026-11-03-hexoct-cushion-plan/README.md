# Knitted HexOct Cushion: Plan (3 November 2026)

DICTO chose the object for the Knitted HexOct (#83, DICTO proposed): one square cushion that serves as seat cushion and pillow.
This is the PLAN for his approval (no full pattern yet). It replaces the rejected patterns booklet (studies/2026-11-03-knitted-hexoct-patterns).

**Plan:** 40 × 40 cm, about 6.5 cm deep, 3 garter sheets A-B-C (middle sheet c), a = 36.4 mm (8 st DK), d = 29.7 mm, 126/126/136 nodes,
721 links. Method: the three sheets knitted by hand in step on three needles; each link cord knitted into the node stitches of both sheets
(spacer-fabric principle), one V and one single link per node and gap (493 pieces, 1214 catches). Fill (carded wool) pushes, cords pull;
side walls picked up and closed by three-needle bind-off; boxed cover with zip. Trial pair T-c / T-h first (press and shear test).
Estimate: ~560 m DK cotton, ~56 m 1 mm polyester cord, 400–500 g wool, ~65 h for the cushion.
Part 2 block tests rerun for 3 and 4 sheets (data/out_*.json): free shear links-only rigid joints c 0.193 vs h 3.708 (19.2×); 4 sheets 7.5×.

**Status:** plan typeset `~/Documents/papers-to-read/hexoct-cushion-plan.pdf` (4 pp), awaiting DICTO's read and approval; not published, nothing knitted.

## Files
- `scripts/plan.py <out> [png dir]` → `figs/*.svg`, `data/numbers.json`, `data/check.out` (run on dicto-big-brother, ~/geom/bin/python;
  run in ~/kres-tmp/hexoct-cushion/study with data/out_*.json beside it). Optional png dir = check renders, scratch only.
- `data/out_<labels>_<links|full>.json`: mech.py of studies/2026-11-02-hexoct-knit-mechanics, task `blockL:<labels>:frame:<variant>`.
- Printed in ~/kres-tmp/cw-print: `node print.mjs hexoct-cushion-plan hexoct-cushion-plan.pdf "Knitted HexOct Cushion: Plan" "none (plan for approval, not published)" 1`.
