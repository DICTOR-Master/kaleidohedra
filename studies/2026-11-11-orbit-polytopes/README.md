# Orbit polytopes from one corner (DICTO 11 Nov 2026)
DICTO: "identify / chase down the remainder of reflection-group orbit polytopes by seeing one corner and discerning the hyper-cube";
confirmed restatement: from one corner read the reflection group and the seed, regenerate the rest; sort DICTO's solids into orbits and not.
Method (scripts/orbit_id.py, float, tol 1e-7): full symmetry group of the outer corners; its reflections; the group W they generate; the
solid is an orbit polytope iff one corner's W-orbit is all corners; seed labels = the corner's inner products with W's simple roots
(zero = that mirror unused; order of labels not yet Dynkin-ordered).
Controls (11, all PASS): 7 Platonic/Archimedean orbits of B3 and H3; snub cube (no mirrors) and rhombic dodecahedron (two corner kinds) rejected.
## Census of the app's registry (389 solids; data/orbit_results_hull.json, log data/orbits2.log, FINAL ok)
332 convex. 42 orbit polytopes (37 convex): B3 16, H3 11, A3 7, dihedral/prism groups 8. First pass (registry vertex lists incl. inner
points) kept for the record in data/orbit_results.json; superseded by the outer-corner pass.
CORRECTION (11 Nov, Dogstar check): for a non-convex solid the outer-corner test identifies its convex HULL, not the solid. Dogstar's
outer corners are a cube's 8 corners (its spikes end at a cube's corners), Hexa-Key's hull is a cube, Dodeca-13's hull has 60 corners and
32 faces (truncated-icosahedron type), Lotus Jewel Axes' hull is an Icosaxes-type truncated octahedron.
DICTO's solids that ARE orbit polytopes (convex): Icosaxes and Unborn Axes (B3, labels exchanged: the partner pair from the seed side),
Delilah (B3, one mirror), Cleo (D3). Non-convex ones are described by their kinds of corner (exact_seeds.py). The other DICTO solids are
not orbits: their corners fall into several kinds.
NEXT: Dynkin-ordered labels and exact recognition; check Dogstar; 4D (A4, B4, F4, H4: the permutohedra, the Queens, the bitruncated
600-cell); then the uniform family chased seed by seed for each group, with DICTO's solids placed in it.
## 4D (scripts/orbit4d.py; data/orbit4d_results_queens.json, log data/orbits4d.log, FINAL ok)
Controls PASS: tesseract and 16-cell (B4, chain 3-3-4), 24-cell (F4, 1152, chain 3-4-3), 4D permutohedron (A4, chain 3-3-3, ALL FOUR seed
labels equal and nonzero: the orders of 1..5), and two non-orbits (24-cell + 16-cell; a 600-cell with one corner moved).
The Queens and the stages between them, built by truncation (not as orbits), are all orbits of H4 (60 mirrors, 14400 symmetries; Coxeter
chain 5-3-3), read from one corner. Seed = which mirrors are used (chain ends: W at the 3-end, R at the 5-end):
| solid | corners | mirrors used (chain 5-3-3, nodes R . . W) |
| 600-cell (White Queen) | 120 | one, at the W end |
| truncated 600-cell | 1440 | the W end and its neighbour, equal labels |
| bitruncated 600-cell (the midpoint) | 3600 | the two MIDDLE nodes, equal labels |
| truncated 120-cell | 2400 | the R end and its neighbour (joined by the 5), equal labels |
| 120-cell (Red Queen) | 600 | one, at the R end |
So the path between the Queens (#76, #104) is the seed sliding along the chain from one end to the other, and the bitruncated 600-cell,
the scutoid tissue with the balance law 601/601 (#104), is the exact middle of the chain. The 4D permutohedron (#105) is the A4 analogue
with every mirror used. #104 and #105 sit in one frame: orbit polytopes of reflection groups, read from one corner.
## Exact seeds, each PROVED by rebuilding every corner from the exact seed (scripts/exact_seeds.py, registry_seeds.py; data/seeds.log)
Seeds in Coxeter-chain order, scaled so the smallest nonzero label is 1 (B3 chain 4-3 read from the 4-end; H4 chain 5-3-3 read from the 5-end):
| solid | group | seed |
| Kelvin's truncated octahedron T(1) | B3 | (0, 1, 1) |
| DICTO 1:2 Truncated Octahedron T(1/2) | B3 | (0, 1, 2) = (0, 1/2, 1) |
| DICTO 2:1 Truncated Octahedron T(2) | B3 | (0, 2, 1) |
| Icosaxes T(tau) | B3 | (0, phi, 1) (registry precision, mismatch < 1e-9) |
| Unborn Axes T(1/tau) | B3 | (0, 1, phi) |
| Delilah (regular octahedron, edge 2^(-1/3)) | B3 | (0, 0, 1) |
| 4D permutohedron | A4 | (1, 1, 1, 1) |
| 120-cell (Red Queen) | H4 | (1, 0, 0, 0) |
| truncated 120-cell | H4 | (1, 1, 0, 0) |
| bitruncated 600-cell | H4 | (0, 1, 1, 0) |
| truncated 600-cell | H4 | (0, 0, 1, 1) |
| 600-cell (White Queen) | H4 | (0, 0, 0, 1) |
So T(x) has the seed (0, x, 1): the golden loop is one B3 seed whose middle label is the gap ratio x (Paradigm Chs 2-3; Koca's
(1, x, 0) read from the other end). The Queens' path is the seed sliding along the H4 chain; the bitruncated 600-cell is (0, 1, 1, 0),
the exact middle. Corner kinds of non-convex solids (orbits of their full symmetry group): Dogstar 4 kinds (12, 12, 24, 8; group 24,
pyritohedral; the 8 outermost = a cube); Hexa-Key 7 kinds (group 24); Lotus Jewel Axes 2 kinds (8 + 24 on an Icosaxes; group 48);
Dodeca-13 3 kinds of 60 (group 120).
## Dogstar's Vacuus (DICTO 11 Nov: "maybe dogstar has a vacuus form")
Its 138 edges lie on 27 central planes: 12 planes carry 8 edges each and 3 planes carry 6 each (114 of 138 edges on 15 central discs),
12 planes carry 2. Only 1 of its 84 faces is central. A concentrated Vacuus, near the octahedron's few-disc pattern (control:
cuboctahedron, 4 planes x 6 edges). Hexa-Key: 70 planes, one carrying 36 edges.
## Vacuus census of the registry (scripts/vacuus_census.py; data/vacuus_census.json; controls: octahedron D8 3 x 4, cuboctahedron 4 x 6,
icosidodecahedron 6 x 10, matching #87)
A disc = a central plane carrying at least 3 edges. 389 solids: 21 have a COMPLETE disc Vacuus (every edge on a disc), 281 have no disc.
Complete: octahedron, cuboctahedron, icosidodecahedron, the rhombic dodecahedron and triacontahedron, several Catalan solids (triakis
octahedron, tetrakis hexahedron, deltoidal icositetrahedron, disdyakis dodecahedron, triakis icosahedron, pentakis dodecahedron,
deltoidal hexecontahedron, disdyakis triacontahedron), two Johnson solids, and among DICTO's: Delilah (3 x 4, a regular octahedron), the
dodecahedron seamed for Dogstars (51 discs, every edge), a Spheroid-13 RD centre piece, the Reuleaux octahedron.
DICTO's solids ranked by share of edges on discs: Sunstar tetrahedral cluster 94%, Dogstar 83% (15 discs: the 15 mirror planes of the
icosahedral group, 3 coordinate + 12 golden), Hexa-Key 80%, Sunstar octahedral cluster 79%, Hexa 76%, Lotus Jewel Axes 71%, Jewel
clusters 48-70%, Icosaxes and Unborn Axes 33% (3 discs of 4 edges + 12 planes of 2: the same pattern as the DICTO 1:2's 3D Vacuus in
#105, the whole T(x) family); 37 of 66 DICTO solids have no disc.
Figure: figures/dogstar-vacuus.png (scripts/dogstar_vacuus.html): Dogstar's 15 discs as fins, the 3 coordinate discs gold, the 12
golden discs violet, Dogstar a cut-away glass shell.
## The Vacuus of the Queens (scripts/vacuus_queens.py, mirror_check.py; data/vqueens.log; FINAL ok, every 2-face carried once)
| stage | 2-faces | on the 60 H4 mirrors | scattered (2 per slice, 1200 slices) |
| 600-cell | 1200 triangles | 20 triangles each (all) | none |
| truncated 600-cell | 2400 triangles, 1200 hexagons | 20 hexagons each | the 2400 triangles |
| bitruncated 600-cell | 1200 triangles, 720 pentagons, 2400 hexagons | 20 triangles + 12 pentagons each | the 2400 hexagons |
| truncated 120-cell | 2400 triangles, 720 decagons | 12 decagons each | the 2400 triangles |
| 120-cell | 720 pentagons | 12 pentagons each (all) | none |
The 60 central slices of both Queens are exactly the 60 mirror hyperplanes of H4 (mirror_check.py, both ways). At the bitruncated
600-cell each mirror carries the White Queen's 20 (triangles, between truncated tetrahedra) AND the Red Queen's 12 (pentagons, between
truncated icosahedra) together: the faces between like cells lie on the mirrors; the 2400 hexagons between unlike cells (where #104's
exchanges happen) scatter, two per slice. Slice shapes per class in the log.
## The Vacuus of every chain's ends and middle (scripts/vacuus_middles.py; data/vacuus_middles.log; FINAL ok; H4 control repeats
vacuus_queens.py: 3600 corners, 720 cells, 60 mirrors x (20 triangles + 12 pentagons), 2400 hexagons off the mirrors)
Every 2-face of the ends (regular polytopes) lies on a mirror. At the middle (0,1,1,0):
| chain | middle | on the mirrors | off the mirrors |
| A4 3-3-3 | bitruncated 5-cell (10 truncated tetrahedra) | 20 triangles (2 per mirror) | 20 hexagons |
| B4 4-3-3 | bitruncated tesseract (8 TO + 16 TT) | 32 triangles TT-TT, 24 squares TO-TO | 64 hexagons TO-TT |
| F4 3-4-3 | bitruncated 24-cell (48 truncated cubes) | 192 triangles (8 per mirror) | 144 octagons |
| H4 5-3-3 | bitruncated 600-cell (600 TT + 120 TI) | 1200 triangles, 720 pentagons | 2400 hexagons TT-TI |
LAW (observed in all four chains): at the middle, the faces of the MIDDLE BOND (the 2m-gons where both ringed nodes meet: hexagons
for bond 3, octagons for bond 4) are exactly the faces off the mirrors; every other face lies on a mirror. Where the chain is not
self-dual (B4, H4) the middle-bond faces are exactly those between unlike cells, so "like on the mirrors, unlike off" holds there; in the
self-dual chains (A4, F4) all cells are alike and the middle-bond faces still leave the mirrors. Off-mirror faces sit 1-2 per central
plane (plane grouping at 6 digits splits a few; vacuus_queens.py gives exactly 2 per plane for H4). To prove: the stabiliser of a
middle-bond face fixes no root orthogonal to it (lead).
