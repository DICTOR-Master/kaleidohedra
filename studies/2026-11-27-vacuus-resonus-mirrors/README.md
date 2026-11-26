# Vacuus + Resonus and mirror planes (27 Nov 2026)
DICTO's conjecture (from his cube and octahedron models): when the Vacuus and Resonus planes are aligned, the gaps between the two
shapes become linear trigonometry for space filling. With Claude (Anthropic). Script scripts/mirrors.py (exact, Q(sqrt2)/Q(sqrt5),
the K class of the Vacuus-Solids study); log logs/mirrors.log; table mirrors.json. Snub cube and snub dodecahedron left out (chiral:
no mirror planes; coordinates need cubic irrationals).

## Step 1 (exact): which planes are mirror planes
Control: mirror counts dodecahedron 15, icosahedron 15, cube 9, tetrahedron 6, octahedron 9: correct.
- Vacuus + Resonus = ALL mirror planes, exactly: **cube** (6 Vacuus + 3 Resonus = 9) and **rhombic triacontahedron** (15 + 15, the
  same 15 planes twice). No other solid of the 27.
- Vacuus planes are all mirrors for every Platonic solid and every Catalan solid; Resonus planes are all mirrors only for cube,
  rhombic dodecahedron, rhombic triacontahedron, and (9 or 15 of their 13 or 31) the rhombicuboctahedron, truncated cuboctahedron,
  rhombicosidodecahedron, truncated icosidodecahedron.
- **Correction to the chat of 27 Nov ~04:15**: the octahedron does NOT give the same 9 planes as the cube. Its Vacuus is the 3
  coordinate planes (mirrors) but its Resonus is the 4 planes x +- y +- z = 0, which are not mirrors. Cube + octahedron together:
  9 mirrors + 4 further planes.
- What still holds for every solid here: its Vacuus + Resonus planes form a set invariant under the solid's full symmetry group,
  so the pieces they cut from any gap repeat by symmetry; one mirror chamber's pieces, reflected, give all of them. For cube +
  octahedron: each of the 48 chambers (0 < z < y < x) is cut once more, by x = y + z, so the gap's pieces come in 2 shapes, 96 pieces
  (by hand from the plane list; to be checked exactly in step 2).

## Step 2 (exact): piece shapes per mirror chamber, solid + its dual (scripts/pieces.py, logs/pieces.log, pieces.json)
All Vacuus and Resonus planes of both solids, plus the mirror planes; on the sphere a chamber is a triangle, each other plane a
chord; shapes per chamber = 1 + chords + sum over inner crossings (m - 1); pieces = shapes x chambers (24, 48, 120). Control: cube +
octahedron 2 shapes, 96 pieces (by hand): passed; one solid alone never exceeds the pair: passed.

| pair | planes | shapes per chamber | pieces | first solid alone (shapes per chamber) |
|---|---|---|---|---|
| cube + octahedron | 13 | 2 | 96 | 1 |
| dodecahedron + icosahedron | 43 | 12 | 1440 | 2 |
| tetrahedron + tetrahedron (dual) | 10 | 3 | 72 | 3 |
| truncated tetrahedron + triakis tetrahedron | 34 | 33 | 792 | 14 |
| cuboctahedron + rhombic dodecahedron | 13 | 2 | 96 | 2 |
| truncated cube + triakis octahedron | 37 | 18 | 864 | 8 |
| truncated octahedron + tetrakis hexahedron | 37 | 16 | 768 | 8 |
| rhombicuboctahedron + deltoidal icositetrahedron | 49 | 31 | 1488 | 17 |
| truncated cuboctahedron + disdyakis dodecahedron | 73 | 90 | 4320 | 36 |
| icosidodecahedron + rhombic triacontahedron | 31 | 4 | 480 | 4 |
| truncated dodecahedron + triakis icosahedron | 91 | 50 | 6000 | 21 |
| truncated icosahedron + pentakis dodecahedron | 91 | 51 | 6120 | 21 |
| rhombicosidodecahedron + deltoidal hexecontahedron | 121 | 88 | 10560 | 48 |
| truncated icosidodecahedron + disdyakis triacontahedron | 181 | 233 | 27960 | 96 |

So DICTO's 'solve one, reflect' holds for every pair; the work per pair is the number of shapes in one chamber: 2 for cube +
octahedron and for cuboctahedron + rhombic dodecahedron, 3 for the two tetrahedra, 4 for icosidodecahedron + rhombic
triacontahedron, up to 233 for the truncated icosidodecahedron pair. (These are cones from the centre; any gap between two such
shapes is cut along them.)

## Next
3. Line lattices on face planes; 4. repeated planes in space (affine arrangements); 5. cells of the periodic arrangements
(classical ones credited: Sommerville, Goldberg; icosahedral families -> de Bruijn multigrid / Ammann planes, quasiperiodic).

## Step 6-7: solid angles and fair-sized dice from the cube + octahedron pieces (27 Nov 2026; DICTO: fair dice search)
scripts/angles.py, relations.py, fairsearch.py; logs/angles.log, relations.log, fairsearch.log; angles.json, relations.json, fairdice.json.
- Every piece of the cube + octahedron planes is one of two kinds (identified at 58 digits, integer relations; not yet proved):
  A = 1/16 - theta/8, B = -1/24 + theta/8 of the sphere, theta = arccos(1/3)/pi (irrational). So a union of pieces has a
  rational share iff #A = #B = a, share a/48, and a die with such faces has N = 48/a faces. (Same pieces for cuboctahedron +
  rhombic dodecahedron. Icosidodecahedron + rhombic triacontahedron: four kinds, three irrationals; equal counts of all four.)
- Complete search (CP-SAT, all solutions; faces = convex unions with #A = #B; no T-junctions; each tiling kept only if it is the
  pattern seen from O of a convex polyhedron, LP), up to the 48 symmetries:
  N 48: 1 (disdyakis dodecahedron); N 24: 4353 tilings, 158 up to symmetry, 136 realised as convex polyhedra (3 with full
  symmetry = tetrakis hexahedron, deltoidal icositetrahedron, triakis octahedron; then symmetry 16: 2, 12: 4, 8: 4, 6: 3, 4: 20,
  2: 55, 1: 45; faces all triangles in 125, triangles + quadrilaterals in 10, quadrilaterals in 1); N 16: 99 tilings, 7 up to
  symmetry, 3 realised (symmetry 16: 1, 8: 2; all triangles).
- These faces subtend equal solid angles from O. Fair dice need that from the centre of mass: step 8 (fair_centroid.py).

## Step 8: fair from the centre of mass (scripts/fair_centroid.py, logs/fair_centroid.log, fair_centroid_retry.log)
For each realised pattern the planes were moved (face cones kept) until the centre of mass is O; then each face's solid angle
from the centre of mass was measured. Numerical (least squares, 1e-15 level), not yet certified exactly.
- Fair: N 48: 1 of 1; N 24: 136 of 136 (die 9 needed a second start); N 16: 2 of 3. Die 137 (N 16, symmetry 8) keeps an
  angle error 3.3e-9 from every start: not shown fair (likely the centre of mass cannot be put at O with that pattern).
- Control: the four Catalans (full symmetry) fair.
- Against the catalogue (10 725 Aequi; groups down to order 4: C2h, D2, S4): the 45 fair dice with no symmetry and the 55 with
  symmetry of order 2 lie in classes the catalogue does not contain. Matching the others (orders 4 to 16) against catalogue
  entries of the same group and face count is the next step; then exact certification.
- Each pattern realises as a family (the edge sizes left free by the cones); the numbers count patterns, not single solids.

## Step 9: against the Aequi catalogue (scripts/catalogue_match.py, logs/catalogue_match.log, catalogue_match.json)
Each fair die's symmetry group (named from the cube symmetries that keep its pattern) and combinatorial type (face-adjacency
graph with side counts) against every catalogue die of the same group and face count (catalogue 2, built from its planes; the
first 1232 have no die of these groups and face counts except T, Th, Td, O, Oh, which ours do not hit below full symmetry).
- 137 of the 138 fair dice checked are NEW AS COMBINATORIAL TYPES (no catalogue die of the same group, face count and graph):
  N 24: C1 45, Cs 39, C2 16, C2v 15, C2h 4, C3v 3, C4v 2, D2h 2, D3d 3, D4h 2, Oh 3 (the Catalans, which the catalogue keeps
  among its first numbers outside these batches); N 16: D2d 1, D4h 1; N 48: Oh 1 (the disdyakis dodecahedron).
- One N 24 D3d die has the same type as a catalogue die (see the log): it may be a member of that die's family.
- Groups C1, Cs, C2, C2v, C3v, C4v are not in the catalogue at all.
- Caveats: same combinatorial type does not mean the same die, and a new type is new only up to this check; the solid angles
  rest on the two piece kinds identified at 58 digits (to prove), and fairness from the centre of mass is numerical.
