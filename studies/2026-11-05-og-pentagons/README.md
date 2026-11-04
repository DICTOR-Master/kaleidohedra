# OG with pentagons (DICTO's proposals, 5 Nov 2026)
- Cut the 12 five-fold tips: regular pentagons; = rectified truncated icosahedron (90 corners = edge midpoints of a regular truncated icosahedron = C60 bond centres). Volume 98.35%.
- Equal-edge version: equilateral triangles, regular pentagons, hexagons with angles 124.72/115.28 (equilateral.py, float).
- Truncated-triangle hexagons: chiral left/right family (trunc_tri.py), with 120° angles, convex to sides 0.114/0.343.
- Dehn nonzero (float screen) for the OG and the cut OG. Densest lattice packing of the cut OG 0.776244 (299 starts; OG 0.789260).
- Octet kit (scripts/octet_kit2.py, manifold3d): cut OG in each octahedron, plus a connector (hull of 2 facing pentagons) across every octahedron edge, 6 per octahedron, volume 0.018887, 63% inside octahedra.
  No overlaps. Rest of the octahedron: 6 pieces of volume 0.07826 (one per octahedron corner; 4 touch, so manifold merges them into one 0.31304 piece).
  Rest of each tetrahedron: one piece 0.397254. Per octahedron + 2 tetrahedra: 1.132872 + 6(0.018887) + 6(0.07826) + 2(0.397254) = 2.510264 = cell. Congruence of the corner pieces not yet checked.
- Kit shapes (octet_kit3.py, probe2.py): all 6 corner pieces are congruent (3-fold turns), and the corner piece is achiral; the dented tetrahedra are a left/right pair (T+ and T- mirror images, no rotation maps them).
- Bull-horns adaptor for the cut OG (hole_piece_cut.py; calibration reproduces the OG adaptor 0.111898): bcc double network, hole Voronoi cell minus 6 cut OGs.
  Volume 0.118230 = gap/3 exactly; one solid, genus 0; centrosymmetric with a mirror (no left/right); sphericity 0.514 (OG adaptor 0.502).
  Two shapes fill space: cut OG 76.16%, adaptors 23.84%.
- GYRATED OCTET (gyro_kit2.py, gyro_twin.py): a single twin layer x+y+z = R, with the mirror image below.
  Octet connectors on all 230 edge-sharing pairs, no overlaps. Face-sharing mirror pairs across the twin layer have no octet connector on the 3 twin-face edges.
  The freed space is 3 bits of 0.005923 per octahedron (the halves of the absent connectors), wedged between corner pieces.
  TWIN CONNECTOR = hull of the two mirror pentagons facing a twin-face edge (axes dot -0.263): volume 0.015495, 51 in the patch, no overlaps.
  With it, a twin-layer octahedron holds 3 octet corner pieces (0.07826) + 3 TWIN CORNER PIECES (0.07707), all separate; a twin-layer tetrahedron holds one TWIN DENTED TETRAHEDRON (0.4059).
  So the gyrated kit = octet kit + 3 new shapes. TODO: a fully gyrated test (every layer twinned); chirality and congruence of the new pieces; exact volumes.
- FULLY GYRATED (gyro_full.py; 4 layers, 3 twin planes): 168 octet connectors + 171 twin connectors, every edge pair served, no overlaps.
  Middle-layer octahedra: leftover = 6 twin corner pieces (0.07707 each; touching ones merge in the boolean: 0.3083 = 4x, 0.23122 = 3x).
  Tetrahedra: all 12 are twin dented tetrahedra (0.4059). So any stacking uses at most 7 shapes: cut OG, octet connector, twin connector,
  corner piece, twin corner piece, dented tetrahedron (L/R), twin dented tetrahedron. TODO: chirality/congruence of the twin pieces; exact volumes; a sample mixed stacking (e.g. hcp-like ABAC).

## 11-05 Left/right test of the twin pieces (gyro_chiral.py, fully gyrated patch, float)
Corners = true corners only (boolean mesh artefacts on flat faces/straight edges dropped); match tolerance 1e-4.
- Twin connector: 40 of 40 congruent by rotation; 9 corners; its mirror image is a rotation of itself -> ONE achiral shape.
- Twin corner piece: 5 sampled; 3 one hand, 2 the other; not equal to its mirror -> chiral LEFT/RIGHT pair.
- Twin dented tetrahedron: 12; 6 + 6; chiral LEFT/RIGHT pair.
Kit for any stacking: 7 shapes, 10 counting mirror images (cut OG, octet connector, twin connector, corner piece achiral; twin corner L/R, dented tetrahedron L/R, twin dented tetrahedron L/R).

## 11-05 Exact Dehn of the cut OG (dehn_exact_cut.py, exact Q(√5) coordinates)
Two edge classes: 60 triangle–pentagon edges, length² = 4/81, interior dihedral 159.923249°, cos²(normal angle) = 89/109 + 16√5/545;
120 triangle–hexagon edges, length² = 2/9 − 2√5/27, dihedral 156.199817°, cos² = 51/109 + 18√5/109.
Length ratio² = 9/2 − 3√5/2, not a square in Q(√5) → the two lengths are Q-independent, so Dehn = 0 iff both dihedrals are rational multiples of π.
cos² of degree 2 → cos of degree ≤ 4 → a rational angle kπ/n needs φ(n) ≤ 8 (n ∈ {1..10,12,14,15,16,18,20,24,30}); neither angle is any such kπ/n.
PROOF: Dehn(cut OG) ≠ 0 exactly.

## 11-05 DICTO idea: regular-triangle cut OG on a pyrochlore network (pyro_eq.py, float, edge = 1)
Copies at the nodes of a diamond net, joined through 4 hexagons pointing to the corners of a regular tetrahedron; joints at the bond midpoints = the pyrochlore sites.
Patch of 49 copies: no overlap (residual 2e-5 at volume 89 = float noise). The equal-edge hexagon (angles 124.72/115.28) is not centrally symmetric:
against its point reflection the corners miss by 0.0475 edge, so touching copies meet on full planes but corners do not match.
A thin twisted hexagonal connector at each joint (hull of the two hexagons; gaps 0.05–0.2 tried, no overlap) makes every join face to face; the connectors sit exactly on the pyrochlore sites.
Open: what fills the space between (compare Golden Bodhi Pyrochlore and the 10-16 OCD-pyrochlore study).

## 11-05 Where the pyrochlore network goes (pyro_fill.py, pyro_jacket.py; float; equal-edge cut OG, edge 1)
Diamond nodes (cut OGs) + the empty second diamond together form a bcc lattice; its truncated octahedra (TO) split space.
- Each cut OG lies wholly inside its own TO and touches it on 8 hexagons: the 4 joints (pyrochlore sites) and the 4 facing empty cells.
- The empty cells are WHOLE TOs (nothing enters them) → fill with truncated octahedra.
- Cut OG fills 75.43% of its TO (gap 0); with connectors gap 0.1: 71.78%, 0.3: 65.18%.
- Jacket (TO − cut OG, 29.067) split by the 14 face pyramids: 8 hexagon pieces 2.2898 (rings round the touching hexagon, genus 1)
  + 6 square pieces 1.7914 (solid, genus 0). Symmetry of the arrangement = Th (24): squares one rotation orbit, achiral;
  hexagon pieces one Th orbit with only C3 on each → left/right pair, 4 + 4 (by symmetry; float matcher noisy on this data).
KIT: cut OG (equal-edge) + truncated octahedron + hexagon ring L/R + square piece = 4 shapes (5 with mirrors) fill space; pyrochlore sites = the joint hexagons.
