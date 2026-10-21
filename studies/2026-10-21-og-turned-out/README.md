# OG turned out: a new tower sequence (DICTO, 2026-10-21)

DICTO: "start by turning the inside towers out and starting a new sequence" -> flip the 80 Aktis outward (each mirrored in its own
face). Rule per beat: tip = mirror image of the centre in each face plane (2 x the face's foot point); next solid = hull.

Float result (`flip_float.py`, `flip-float.json`):
- Beats 1-4 are the OG's DOWNWARD family (#39: TPH 80 corners, TQH 132, TQP 140, TQHD 162), each doubled per beat (float: corner
  counts and corner-radius ratios match data/exact_downward.json of 2026-10-19-five-fold-octet). Reason: the downward step's corners
  are exactly the foot points; flipping puts tips at 2 x those.
- Turned out, every solid holds the one before it (the break TQP/TQH in #39 does not occur here). Float; exact check to do.
- Growth about x1.9-2.0 in radius per beat; stays round within 1-7%. Beats 5-8 are new solids (200, 192, 260, 312 corners; float).
- Fibonacci shells 1,1,2,3,5 = 12 beats: outer shell roughly 3000 x the core radius (beat 8 is already 200 x).

DICTO · dictospheres.com

## Golden step (DICTO "yes try the golden step"), `golden_step.py <t>`
Spires shortened before flipping: tip = t x foot point. t = phi (spire height = Aktis height / phi) and t = phi^2 tested (float).
- The solids do not change, only their size: beat k = t^k x the k-th downward solid (same corner/face counts; no old corner survives
  on the new hull, so each solid holds the one before).
- t = phi: growth per beat 1.520, 1.534, 1.608, 1.512, 1.591, 1.592 -> tends to phi (the downward family itself shrinks a little each
  step and levels off, so the ratio -> t). t = phi^2: 2.46 ... 2.58 -> phi^2.
- With Fibonacci shells 1,1,2,3,5 the shell boundaries sit at phi^0, phi^1, phi^2, phi^4, phi^7, phi^12 (times the downward family's
  own shrink): golden scale and Fibonacci rhythm together. Outer radius at 12 beats: very roughly 200-250 x the core (estimate).

## Exact (`golden_exact.py`, `golden-exact.json`, `golden-exact.log`) and figure (`golden_figs.py`, `golden_compose.py`)
Exact in Q(sqrt5): all five solids fully symmetric; each holds the one before; corners = flipped tips exactly. Shells 1,1,2 beats:
80 towers (60 on kites + 20 on hexagons), 132 (120 on triangles in TWO shapes, 60+60, + 12 on pentagons), 140 (60 tri + 60 quad +
20 hex); every shell sums to its gap exactly. The one FAIL line in the log is only the "one shape per kind" test for shell 2 (TPH
has two triangle kinds), not a geometry failure. Figure figures/og-turned-out.jpg.

## Flat-ended triangles (DICTO's theme, checked 2026-10-21)
DICTO: flat-ended triangles (hexagons, all angles 120°, sides alternating long/short) keep turning up (FUJI, latest Cleo builds,
OG up/down families). Checked on the boundary solids (float on exact corners): the GTI's 20 hexagons ARE flat-ended triangles,
all angles 120°, short/long = 0.4271 = (3 sqrt5 - 5)/4 (FUJI's base: 1/phi = 0.618). In the OG families none: OG, PHE (20),
DPHP, TQH, TQHD hexagons are regular; PHE's other 60 hexagons are irregular (sides 0.22, 0.22, 0.32, 0.78, 0.78, 1 by ratio).
Tower and piece faces not yet checked.
