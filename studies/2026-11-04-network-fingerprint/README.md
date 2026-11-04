# Network fingerprint: the Admiral Cap network (2026-11-04)
DICTO: "start the network fingerprint with admiral caps … and identify new potential solids". Method of #94 (Q4, Q6, Q8, W6 of each node's edge neighbours).
Network: the octet (edge √2 here), every octahedron = Pacioli icosahedron + 6 Admiral Caps (#47; edgeRoof.js), tetrahedra whole.
Engine slab (slabPieces('I')) is one layer thick, so the full 3D network is built here: scripts/build_admiral_octet.py (modes same / alt).
NOTE: the Admiral Cap is not convex (two tetrahedra over an icosahedron edge, a dent between) — handled as its two tetrahedra; I + 12 halves = octahedron 4/3 checked.

## Results
1. Frustration (exact, exhaustive): round one octet corner the 6 octahedra share 12 edges; whichever golden twin each icosahedron takes (64 choices),
   at most 8 of the 12 shared edges carry a common icosahedron corner. So the Admiral Cap network is never face to face: corners of one octahedron's
   icosahedron always land inside edges of a neighbour's pieces (T-junctions). A periodic box (8^3) gives 592 contradictions among 1536 edge constraints.
2. Node types (fingerprint, edge neighbours):
   - octet corner, 12 half-caps + 8 tetrahedra: same twins Q4 .1909 Q6 .5745 (= cuboctahedron, the fcc shell); alternating twins Q4 .2016 Q6 .5821 — the fingerprint hears the twin pattern.
   - icosahedron corner meeting a neighbour's edge (T-junction): 4 half-caps, 1 icosahedron, 2 tetrahedra; Q4 .3332 Q6 .4166.
   - NEW with alternating twins: two icosahedra share a corner (6 half-caps, 2 I, 2 T), Q4 .233 Q6 .239 Ŵ6 −.087 (most icosahedral-leaning node).
3. Vertex stars (union of pieces at a node): none convex. Hulls as candidate solids: octet corner star hull = cuboctahedron (8 tri + 6 sq);
   T-junction star hull 13 corners (6 tri, 2 quad, 4 pent); two-icosahedra star hull 18 corners (8 tri, 4 quad, 4 hex) — to check for regular faces/names.
## LEADS
- Best global twin pattern: does a pattern reach the local bound 8/12 at every corner? (spin-glass-like frustration; ANNNI link, Concordance 5.5)
- The two-icosahedra node and its 18-corner hull: exact shape, prior art, name for DICTO.
- Same fingerprint on the golden nests and OG networks; physical: frustration explains why the I world in #47 is a single slab.
