# Scutoid bonds (DICTO 27 Nov 2026: "is there a possibility of including scutoid-frusta bonds in the web of bonds"; plan 1,2,3 yes)
Status: PILOT, numerical, not a result.
- Reasoning (to be checked): any cut of each double cone gives pieces that fill space; convexity forces neighbouring cuts to cross their
  shared spoke triangle along one line, so cuts are fixed by points on the spokes. #51's cut planes are power bisectors, so splitting the
  weights of the two tetrahedron orientations (w_up, w_dn; octahedra 0) keeps every piece convex and space-filling (power diagram).
- pilot2 (scripts/power_octet.py): the diagonal w_up = w_dn reproduces #51 exactly (tetrahedron + RD with 8 corners cut, 30 corners;
  then cut cube 16 corners + octahedron), volume control up + dn + oct = 2 per two unit cubes holds there. Off the diagonal 14 cell
  types appear (e.g. an up cell that is a cube while the octahedron cell is a tetrahedron), BUT the volume control fails at 85 of 625
  grid points: off-diagonal numbers are NOT trusted yet. Likely cause: the neighbour radius (2.6) or the representative cell vanishing.
Next method (decided): widen the neighbour set, report empty cells as such, rerun; then follow one path through the type changes and test
whether a face changes its number of sides (a swap -> Scutoid-Frusta straws). Pass: an exact convex, space-filling example with a swap,
or a proof that two-kind splits cannot swap.

NAME (DICTO, 28 Nov 2026): **Scutoid-Frusta bond** (replaces the placeholder "Scutoid bond").
PILOT 3 (28 Nov, scripts/power_octet.py, FINAL ok): fault found and fixed: with unequal weights a centre can lie OUTSIDE its own
power cell, and the cell was built from a point next to the centre; now an interior point is found by LP (largest inscribed ball),
and a vanished cell is reported as empty. Volume control up + dn + oct = 2 per two unit cubes holds at all 625 grid points (0
failures). 16 combinatorial types (data_pilot3_types.txt; numerical). Notable: in two regimes one tetrahedron class VANISHES and space
is filled by only two kinds of convex cell: dn cells with 22 corners (4 triangles, 12 pentagons) + octahedron-centre cells that are
tetrahedra (e.g. w_up = -0.6, w_dn = 0.4), and the mirror case: two-kind convex fillings, i.e. candidate bonds off #51's line.
Next: follow a path in (w_up, w_dn) across type changes and test whether a face changes its number of sides (a swap), which is the
Scutoid-Frusta bond's defining event; then exact coordinates for any pass.
