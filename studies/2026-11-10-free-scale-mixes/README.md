# #47 at free scale: the core (DICTO 22 Oct plan; started 10 Nov: "yes start the free scale core")
**Result (mixes_free.py, data-free.log, FINAL ok):** every one of the 31 mixes of the five Platonic solids fills space with the solids at
their own sizes, in TWO worlds (#47 needed four) joined by ONE seam that meets FACE TO FACE, with a kit of SIX connectors
(P, Q, A, S, X, Y; #47's Q′ is gone).
- Sizes: dodecahedron edge 1; cube edge φ (Euclid's cube: the SAME circumsphere as the dodecahedron, radius 1.401); octahedron and
  tetrahedron edge φ (circumradius 1.144 and 0.991); icosahedron edge √2/φ ≈ 0.874 in Pacioli's position inside the octet's
  octahedra (circumradius 0.831), the rest of each such octahedron DICTO's six Admiral Caps.
- World 1, golden cubic (grid φ): dodecahedra and Dogstars S with the boundary X/Y layer (as #47), and cubes C in the same grid.
- World 2, ONE octet of edge φ turned 45° about the vertical, so its square layers are exactly the cube faces of world 1: every
  octahedron is O, or I + 6 A (O and I alternate when both are in the mix; DICTO 10 Nov: "octahedra could go in that mix too"), or
  2 P; every tetrahedron T or 4 Q.
- Checks (as #47's mixes3.py): 40 000 random points per mix through the whole stack, pieces as signed sums of convex parts: every point
  covered exactly once; no two dodecahedra overlap; every solid of the mix used; seam: every cube face in a 4 × 4 window equals an
  octahedron's equator square (face to face).
Next (DICTO's 22 Oct list): cubes as cubes in the X/Y edging (fewer helpers); the D–I bridge (a true meeting, Chain of Karma lead);
sphere-unit sizes (octet scale options); coloured-glass views in the #47 world; random packings joined by adaptors.

## Step 2: cubes as cubes (10 Nov, mixes_cubes.py, data-cubes.log, FINAL ok)
In every mix with both D and C, each edging cell next to a Dogstar is a PLAIN CUBE (edge φ, a solid of the mix) and that Dogstar keeps
the roof-space on the edging side; Y disappears. All 31 mixes still fill space (points covered once, no dodecahedra overlap, every solid
used, seam face to face). Window count: edging cells 26 whole cubes C, 24 X (next to a dodecahedron, its roof pokes in).
Exact shapes of the kept-roof Dogstars: in the thinnest slab (one layer of dodecahedra, the check above) each Dogstar has edging above
and below, so it keeps two roof-spaces: a cube of edge φ minus its four side roofs (S4). In a thicker slab a Dogstar next to one edging
keeps one: a cube minus five roofs (S5); inner Dogstars stay S. (The script labels both 'S5'.) Kit for mixes with D and C, thinnest
slab: P, Q, A, S4, X (five; Y and S not needed). Names of S4/S5 are DICTO's.
Next: the D–I bridge (a true meeting of dodecahedra and icosahedra; lead: a flat Chain of Karma); sphere-unit sizes.

## Step 3: RD and CO (10 Nov, mixes_rdco.py, data-rdco-127.log, FINAL ok)
All 127 mixes of D, I, C, T, O, RD, CO fill space in the two worlds (points covered once, no dodecahedra overlap, every solid used, seam
face to face). RD (cube + 6 square pyramids) on the alternating cubes of world 1, with or beside the dodecahedra; one new edging helper
XR (cube minus an RD pyramid); with RD alone the cells between RDs are filled completely by the pyramids. CO in the octet, each = its 8
tetrahedra + 6 half octahedra (centres spaced 4 apart); touched octahedra keep their other half as P. TO left out (DICTO).
## Step 4A: the D–I bridge by Karma cells (10 Nov, mixes_karma.py, data-karma-127.log, FINAL ok)
Every icosahedron in world 1 as a Karma cell (#22: dodecahedron of edge 1 = icosahedron of edge 1/φ + 12 pentagonal pyramids + 30 AXE +
20 CLEO): all 127 mixes again fill space; D and I now share ONE world (the mix D+I has no octet and no seam); the octet carries T, O, CO.
