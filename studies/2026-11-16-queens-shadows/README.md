# The Queens' shadows carry the wall lattice (16 Nov 2026)

**Conclusion: DICTO's picture holds, exactly in Q(√5).** Every shadow keeps exactly the walls that are parallel to its side-on cells: 45, 16, 16 and 33 walls in the four standard views. Each view shows layer outlines whose every edge fin lies in a kept wall: icosahedra, dodecahedra, tetrahedra, octahedra and a truncated icosahedron. Shadows of each type reach all 360 walls, and they form one connected lattice.

**DICTO's idea (16 Nov 2026, his words):** "all of the shadows seem to carry interconnected lattices of possible vacuus". DICTO confirmed this restatement. When a Queen is projected to 3D along d, every wall that contains d stays flat in the shadow as a central plane. A shape in the shadow whose central plates all lie in those planes is a possible Vacuus. Shadows share walls, so the plane sets join into one system.

## Method

- **Walls** (as in studies/2026-11-16-600cell-walls): 60 H4 mirrors and 300 cross walls (central sections parallel to opposite cells of the 600-cell). DICTO ruled that cross walls also count.
- **Test:** a wall with normal n contains d iff n·d = 0. A projected point P(x) lies on that wall's trace iff n·x = 0. Every test is therefore one exact dot product.
- **Plates (#87):** one fin per edge, through the shadow's centre O, or through the shape's own centre.
- **Coordinates:** the 600-cell comes from echo-shapes/shadow_echoes.py. The 120-cell is built here as its exact dual (centroids of the 600 tetrahedra), so the two Queens share one wall system and their four directions coincide:
  - 600-cell corner-first = 120-cell cell-first (V);
  - 600-cell edge-first = 120-cell pentagon-first (E);
  - 600-cell face-first = 120-cell edge-first (F);
  - 600-cell cell-first = 120-cell corner-first (C).
- **Symmetry:** W(H4) is generated exactly as 14400 permutations of the corners.
- **Files:** scripts/shadows.py, data/shadows.json, data/shadows.log (FINAL ok, 79 checks, 0 failed, 37 s on the compute machine) and data/tables.txt (all tables, from scripts/tables.py).

**Checks against the published atlases:**
- #63 hull f-vectors, front/side-on counts, the kinds of front piece (7/22/33/20), and the six turning angles;
- the Red Queen paper's hull f-vectors and front/side-on counts.

## 1. Kept planes per shadow (same for both Queens)

| view (600 / 120) | mirrors | cross | total | 3D arrangement |
|---|---|---|---|---|
| V corner-first / cell-first | 15 | 30 | 45 | the 15 icosahedral mirror planes, plus 30 planes whose normals point at the corners of the 120-cell's central rhombicosidodecahedron (one orbit, 2 per mirror plane) |
| E edge-first / pentagon-first | 6 | 10 | 16 | 1 plane ⊥ the 5-fold axis, 5 planes through it, 10 cross planes (one orbit); group of order 40 |
| F face-first / edge-first | 4 | 12 | 16 | 1 plane ⊥ the 3-fold axis, 3 through it, 6 + 6 cross planes; group of order 24 |
| C cell-first / corner-first | 6 | 27 | 33 | the 9 mirror planes of the cube's symmetry (6 diagonal mirror walls, plus 3 coordinate planes that are cross walls), plus 24 cross planes in general position; group O_h, order 48 |

**Law (checked in all 8 shadows):** the kept walls are exactly the central planes parallel to the side-on cells of the two Queens.
- The White Queen's side-on tetrahedra give the cross walls. They are its flat hull faces: 60, 20, 24 and 54 faces.
- The Red Queen's side-on dodecahedra give the mirrors. They are its non-pentagon hull faces: 30, 12, 8 and 12 faces.

So each Queen shows one family of walls on its own surface, and the other family on its partner's surface.

## 2. Possible-Vacuus shapes (fins from the shadow's centre O)

| shadow | possible Vacuus | partly / not |
|---|---|---|
| 600 V | icosahedron (two sizes, 30/30 mirror); dodecahedron (30/30 mirror); 380 of the 600 projected cells, among them the 40 Cleo-Icos (DICTO's name, #19; the core of #63) | icosidodecahedron: not (its fins lie in the 6 decagon planes, which are not walls); hull (42/120/80): 60 of 120 |
| 600 E | flat pentagons only; 10 cells | 10-corner pentagonal layers, central icosahedron (10/30), hull: partly |
| 600 F | flat triangles and hexagons; 4 cells | prisms and others: partly |
| 600 C | regular tetrahedra (6/6 mirror); octahedron (12/12 cross: the 3 coordinate planes); 34 cells | cuboctahedra: not; truncated tetrahedra 6/18; hull 48/120 |
| 120 V | dodecahedra (three sizes, 30/30 mirror); **truncated icosahedron at h = ±(1/8 + φ/4): 30 mirror + 60 cross**; 66 cells | icosidodecahedron and the two rhombicosidodecahedra: not; the second truncated icosahedron 30/90; hull GP(2,0): 60/120 |
| 120 E (pentagon-first) | flat pentagons only | the rest: partly or not |
| 120 F (edge-first) | flat triangles and hexagons | the rest: partly or not |
| 120 C (corner-first) | regular tetrahedra; 8 dodecahedral cells (15 cross + 12 mirror + 3 through O) | truncated octahedra and the rest: partly or not |

**At their own centres,** almost no off-centre cell passes. The exceptions are the flat side-on cells, which pass trivially (every fin is the cell's own plane), and the polar cells, whose centres sit at O. The per-class tables are in data/tables.txt.

**Names and credits:**
- The Platonic solids, after Euclid, Elements XIII.
- The Archimedean solids, named by Kepler in Harmonices Mundi (1619).
- The 600-cell and 120-cell (Schläfli, 1852).
- GP(2,0), after Goldberg (1937).
- Cleo-Icos and Vacuus are DICTO's.

## 3. The lattice

- **Walls per line:** each mirror contains 15 V, 36 E, 40 F and 30 C shadow lines. Each cross wall contains 6, 12, 24 and 27.
- **Reach:** the shadows of any one type reach all 360 walls.
- **Connectivity:** the shadow graph (two shadows joined when they share a wall) is connected for each type and for all types together. So is the wall graph.
- **Shared walls:** two corner-first shadows always share 4, 5 or 9 walls. Edge- and face-first pairs can share none. Full counts are in data/tables.txt (SHARED).
- **Turnings:** a view strictly inside one of #63's six turnings keeps only the walls common to both ends:

| turning | kept walls |
|---|---|
| V–E | 5 mirrors |
| V–F | 2 mirrors + 2 cross walls |
| V–C | 3 mirrors + 6 cross walls |
| E–F | 2 mirrors + 2 cross walls |
| E–C | 2 mirrors + 2 cross walls |
| F–C | 3 mirrors + 6 cross walls |

So the view moves through one wall system, seen through many windows.

## 4. Controls (all as required)

**Directions:**
- A generic rational direction keeps 0 walls, and so does a generic Q(√5) direction.
- A direction inside one mirror keeps exactly 1 wall.

**Shapes** (the icosahedra and the dodecahedron of 600 V):
- Turned by a symmetry of the shadow, each stays a possible Vacuus: 30/30.
- Turned by an exact generic rotation about d, each drops to 0/30.
- With one corner moved, each loses exactly the 5 (or 3) edges at that corner.
- Translated, each fails at O but keeps its parallel fins at its own centre.

## Faults

The first full run reported FAIL: the Red Queen hulls showed too many edges. The float hull ordered points lying inside a face (side-on cells seen flat) into the face cycle. Each face is now re-made as a 2D convex hull, and every face is certified exactly. A rerun under the 5-minute cap gave FINAL ok.

## Figures

figures/RENDER-queens-shadows-white.png (600 V) and -red.png (120 V), made by scripts/render_shadows.py (data/render.log FINAL ok). papers/edgecheck.py passes and both sheets were inspected. In each:
- discs show the kept planes, mirrors in blue (I) and cross walls in red (T);
- the possible-Vacuus layer outlines are drawn inside out, with the innermost a solid gold core;
- the shadow's hull is a faint cage.

## LEADS

1. Explain why the 120 V truncated icosahedron at h = ±(1/8 + φ/4) is all-wall while its twin at ±(1/8 + φ/8) is not. Test the other Archimedean layers of the 120-cell's slices the same way.
2. Off-centre cells fail at their own centres. Test whether some union of cells (a shell or a front layer) is a possible Vacuus as a whole.
3. Test the shadows of the 24-cell (F4) for the octahedral shapes that fail here.
4. Run generic views along the turnings and on great circles inside one wall. Map which views keep 2, 3 and so on walls; this is the full window structure of the lattice, beyond the four standard views.
5. Look at the 24 general cross planes of the cell-first view and the 30 of the corner-first view as plane arrangements in their own right: their chambers, and whether the possible-Vacuus layers are unions of chambers (cf. studies/2026-11-16-queens-chambers).

## Sources checked

- studies/2026-11-16-600cell-walls (README and scripts);
- papers/white-queen-600 (#63: shadows, turnings, Cleo shells);
- papers/red-queen-120 (shadows table);
- studies/2026-11-15-echo-shapes (echo_lib, shadow_echoes);
- studies/2026-11-16-non-heart-vacuus/scripts/render_vacuus.py (render canvas).

The sibling studies queens-vicinity-vacuus, queens-chambers and queens-construct were not edited.
