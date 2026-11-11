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
