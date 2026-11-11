# 2026-11-02 Halo fillers (DICTO: positive search for space-fillers and space-filling pairs among the new halos)

Conclusion: none fills. No new halo of the Stars and Halos census tiles space alone, no two new halos fill together, and no new halo
fills together with any of 12 known filler sets (cube, RD, TO, hexagonal prism, triangular prism, tetrahedron + octahedron, and DICTO's
six published fills in DICTO Solids v7), at any relative scale, face to face or not. Status: study note (halo-fillers.pdf in DICTO's
reading folder); not in a paper.

Counts: 84 new halos (42 centre, 42 polar) from 2026-11-02-halo-census. Test 1 (edges): 0 / 84 alone, 0 / 3486 halo + halo,
14 / 1008 halo + known set pass. Test 2 (corners): 14 / 14 pass. Tests 3 (balance) and 4 (keyed bond): 0 / 14 pass.

Run on compute-host (~/work/halo-fillers, python3), one foreground process per step; nothing left running.
Inputs: ~/work/halo-census/data (census.json + shapes/<slug>.json, corners and faces of each halo), ~/work/dataset-v7.
- scripts/screen.py data/screen.json: test 1. At a point inside an edge of dihedral angle a, the other pieces add their dihedral
  angles or pi, total 2 pi; so 2 pi - a or pi - a must be a non-negative integer sum of the set's dihedral angles. Floats, 1e-7 rad.
  Also checks each known filler set passes on its own angles (dihedrals of the non-convex keyed pieces from oriented faces, reflex
  angles included). Writes per-halo angle classes, witnesses, counts. data/screen.log.
- scripts/margins.py data/margins.json: for each halo alone, the widest gap of a failing edge to the nearest sum; smallest is
  0.0019 rad (float error of the angles < 1e-12), so every single-halo failure is a proof.
- scripts/screen2.py data/screen.json data/screen2.json: test 2. If no edge of a halo face can be crossed (pi - a not a sum),
  coplanar neighbour faces cover it exactly; each corner angle must be a sum of face corner angles of the set.
- scripts/screen3.py data/screen2.json data/screen3.json: test 3, the balance argument (classical): in a tiling of a convex polygon
  by convex polygons, edge length facing u minus facing -u is additive; centrally symmetric tiles add 0. With zonohedral partners
  (skewed ED F16, F18, skewed RD) a non-symmetric halo face whose edges cannot be crossed, and inside which only congruent halo faces
  fit, must meet a halo copy face to face; every placement of the copy fails test 1 at some edge. Rules out 12 of the 14.
- scripts/keyed_check.py -> data/keyed_check.txt: test 4 for DBT / OTT Polar Halo + keyed bond (Lotus Jewel Axes + Dodecaxes):
  the halo triangle (all edges 142.62) needs the Dodecaxes' 217.38 reflex edge on every edge; a 60 corner needs 22.24 + 37.76 from
  two Dodecaxes triangles whose inner edges carry 109.47 + 125.26, plus pi from the halo face: 414.73 > 360. Rules out the last 2.
- scripts/sanity.py data/sanity.json: test 1 passes cube, RD, TO; fails RT, dodecahedron, icosahedron, octahedron, tetrahedron;
  fails all 26 known/repeated census halos; face counts of the hulls used match the census for all 110 halos.
- scripts/describe.py: faces (sides, lengths, corner angles, distance) of the survivors and partners (construction step input).
- scripts/typeset.py: the PDF (printed on compute-host with papers/print.mjs). figs/: the four halos that passed test 1
  (census thumbnails).
- Prior art: no filler found, so no construction and no prior-art check. The balance argument is classical, not claimed as new.
- Limits: partners are the 12 sets above only; tests are necessary conditions (that is why survivors would have gone to construction);
  floats with tolerance 1e-7 rad in test 1 (failures have margin >= 0.0019 rad).
