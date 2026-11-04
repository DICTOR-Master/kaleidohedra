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
