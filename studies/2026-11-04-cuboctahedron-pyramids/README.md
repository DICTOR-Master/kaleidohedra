# Cuboctahedron centre pyramids (2026-11-04)
DICTO Concordance Part 5, gap 1 (ranked first). Started on DICTO's "yes start the cuboctahedron pyramids", 4 Nov 2026.

Pieces (edge 1): the CO's circumradius equals its edge, so its 8 triangle pyramids are regular tetrahedra T and its 6 square pyramids S are half-octahedra.

## Result (face to face)
1. Only S has a square, so every square is shared by two S, and S + S is the regular octahedron. So a face-to-face tiling by T and S is a face-to-face tiling by regular tetrahedra and octahedra, i.e. (#92) a close-packed stacking, with each octahedron cut along one of its three squares, freely. Uncountably many even on the octet alone (3 choices per octahedron).
2. A whole CO forms round a vertex v exactly when its 6 octahedra are all cut across v's axes, and v is a straight (c) vertex. Round a twisted (h) vertex the same 8 T + 6 S make the anticuboctahedron (J27): the CO's pyramids also rebuild its twisted twin, as the RD's rebuild in #93 only by choice.
3. Each tetrahedron lies in at most one CO, so at most 1/4 of the vertices are CO centres. The bound is reached in the octet by the centres 2Z^3: every tetrahedron in a CO, the rest whole octahedra: the rectified cubic honeycomb, i.e. #90's sweep at its midpoint (μ = 2), which by #93 Theorem A is the only tiling by CO + O.
Checks: scripts/co_pyramid_checks.py, 12 PASS (data/co-pyramid-checks.log, .json).

## Not face to face
Open: half-octahedron layers can slide on square slabs (as #92 Theorem D's cubes); expect no finite list.

## LEADS
- J27 + octahedra: is there a tiling where every tetrahedron lies in an anticuboctahedron (hcp analogue of the rectified cubic)? On mixed stackings, max density of whole COs / J27s.
- Same method for the other quasi-regular solid: icosidodecahedron pyramids (circumradius = edge·φ, not regular pieces) — and the rhombic duals (RD done in #93; RT open).
- The octahedron's three cut choices are a 3-colouring problem on the octet: counting the choices that give a given set of CO centres.
- Physical: DICTO's node work (CO = fcc coordination shell, J27 = hcp) — the c vertex builds the CO, the h vertex its twin.

## The twin of the rectified cubic honeycomb on every stacking (4 Nov) — scripts/j27_tiling.py (+ whole-octahedra condition, run inline)
Integer program on periodic boxes (≥ 4 layers; 2–3-layer boxes fold neighbours and are invalid): choose centres so every tetrahedron has exactly one centre
corner and every octahedron serves both ends of one axis or none. FEASIBLE on ABCABC (fcc, control), ABAB and ABABAB (hcp), ABCB, ABCACB (mixed),
boxes 4×4 and 6×6: centres = 1/4 of the balls, no half-octahedron left over. So on every stacking tested, space is tiled by whole cuboctahedra
(at straight centres), anticuboctahedra J27 (at twisted centres) and whole octahedra; on hcp by J27 and octahedra alone — the twisted twin of the
rectified cubic honeycomb. PRIOR ART to check (Johnson-solid space-fillers; tilings with triangular orthobicupolae).
