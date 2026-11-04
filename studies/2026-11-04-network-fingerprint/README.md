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

## The 18-corner candidate (4 Nov, follow-up)
Hull of the two-icosahedra node star (icosahedron edge 1): 8 equilateral triangles (icosahedron faces) + 4 quadrilaterals (sides √2/2, φ√2/2, 1, 1)
+ 4 hexagons with sides among √2/2, 1, √2, 1.144, 1.851, 2.288; symmetry order 4; hull volume 6.937 > star 6.263 (the star is not convex).
Verdict: an irregular convex hull of mixed edges and low symmetry, not a solid in the sense of the papers (no equal edges, no regular faces beyond the triangles).
The real find is the NODE: two icosahedra sharing a corner where the golden twins change (a twin boundary of the Admiral network).

## Best twin pattern (ground state), 4 Nov
scripts/twin_ground_state.py (exhaustive side 2; annealing sides 4, 6, 8), data/twin-ground-state.json.
- The local bound 2/3 of shared edges is reached exactly, already with period 2 (4 octahedra classes; 6 optimal patterns: two classes per twin).
- Ground states found: twin(c) = parity(c_a) XOR f(c_b) for two different cube axes a, b and ANY function f of the layer index c_b:
  the twins alternate layer by layer along one axis, and every layer across a second axis may be flipped freely. Checked: all 96 (side 4) and 384 (side 6) such patterns are optimal;
  all 42 distinct optima met by annealing on side 4 are of this form (completeness not proved).
- So the ground states are uncountably many, one free bit per layer: a layer law like the close-packed stackings (#92), here on the cube's layers.
LEADS: prove completeness; fingerprint the twin-boundary layers (where f flips); does a physical Admiral build prefer one layer word?
