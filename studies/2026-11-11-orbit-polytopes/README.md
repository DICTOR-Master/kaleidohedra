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
DICTO's solids that ARE orbits (8 of 67): Icosaxes and Unborn Axes (B3, two mirrors, labels exchanged: the partner pair from the seed side);
Delilah (B3, one mirror); Lotus Jewel Axes (outer corners = an Icosaxes-type orbit); Dogstar (outer corners, B3 by this test: TO CHECK, a
dodecahedral solid is expected to show H3 or pyritohedral symmetry); DICTO Hexa-Key (outer corners, B3); DICTO Dodeca-13 (outer corners, H3);
Cleo (D3). The other 59 are not orbits (e.g. Unborn, Samson, Dodecaxes, AXE, FUJI, Jewels, Hexa, Spheroid-13 RD pieces): their corners
fall into several kinds.
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
