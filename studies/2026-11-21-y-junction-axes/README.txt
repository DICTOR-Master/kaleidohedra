Y-junction vertices and the 2-fold axes of the core (21 Nov 2026)
Question: in every valid scutoid division of the amber-cell sweep, do the Y vertices (30 per cell) lie exactly on the 2-fold axes of the core?

Method: scripts/y_axes.py re-runs amber.py of the sweep unchanged except for one inserted dump line (_amber_patched.py, generated) for the 20 valid
cases with Y vertices (C1, C2 in sc/bcc/fcc at s0 and 6/5 s0; truncated dodecahedron, icosidodecahedron at 6/5 s0 in all three; compound bcc, fcc at 6/5 s0).
Every Y is exact in Q(sqrt5). Tests are exact (cross product with the axis = 0): axes = the core's own 2-fold axes (half-turn preserves vertex and
face sets exactly; candidates the 15 icosahedral axes). Also the line through the midpoint of a same-kind edge. Skeleton Y points of branch D tested too.
Files: log.txt (all results, ends FINAL ok = consistency: every run valid, Y count equals the sweep's, Y distinct), data/ydump_*.json (exact Y and cluster vertices),
data/run_*.log, data/amber_*.json (re-run outputs).

Result
- bcc mould, icosahedral core (C2 s0 and 6/5, truncated dodecahedron, icosidodecahedron, compound): all 30 Y on a 2-fold axis, 15 axes used (2 Y per axis).
  Through a same-kind edge midpoint: C2 and truncated dodecahedron yes (30); icosidodecahedron and compound have no same-kind edges to speak of; their Y sit on the
  axes through the core's 4-valent vertices / valley points (30).
- sc and fcc moulds (any core): only 6 Y (the cube axes) are on a 2-fold axis; 24 of 30 are off every 2-fold axis, by 0.5 to 2.7 degrees from the nearest
  axis/edge-midpoint line for the icosahedral cores (not exact). The claim is false there.
- C1 (Fullerene Star): core symmetry T_h only, 3 two-fold axes. 6 Y on them (bcc s0: all 6 Y, exact); the other 24 are 35 degrees or more from any 2-fold axis
  (0.2 to 2.7 degrees from a hexagon-hexagon or triangle-triangle edge-midpoint line, not on it). C1 sc s0: all 24 off.
- Skeleton (branch D): C1 exact: bcc 6/5, fcc s0: all Y points on cube axes; sc 6/5 and the 3/2 cases have Y points off the axes. C2 (50 digits): all 11 listed Y on icosahedral axes.
So Proposition 17 / Table 3 holds as stated only for the bcc mould with an icosahedral core; as a general statement it should be restricted or dropped.

OEIS: no natural infinite family arises. Per-cell counts are fixed constants (30 Y; 72, 80, 32, 120 pieces; 4,5,3,6 kinds) and do not depend on the scale once above the
threshold; the cores are finitely many solids. A sequence would need a new family (e.g. Goldberg/geodesic cores) that has not been computed; not forced.
