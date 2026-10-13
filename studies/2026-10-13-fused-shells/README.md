# Fused shells, opened by large facets (DICTO 2026-10-13)

DICTO's question: treat the many pieces of each nested structure as solids, divide them by large facets (as when an
icosahedron or dodecahedron is opened into its face pyramids), and name them technically. A first, computed pass; a
possible paper by DICTO. Data: `pieces.json` (exported from `src/app/seeds-data.js`); scripts in `scripts/`
(`layers.py`: which partial builds are convex; `facets.py`: the facet wedges, written to `facets.json`).

## Method
1. **Classic solids.** Every union of piece types (split by distance from the centre) whose volume equals its convex
   hull's volume is a convex solid; these are the classic solids the structure passes through.
2. **Shells.** The solid between two consecutive convex builds.
3. **Large facets.** Each shell is cut by the planes through the centre and each edge of its outer solid. Under each outer
   face: (pyramid over the face, apex the centre) minus (the part of the inner solid in that pyramid). Checked: do whole
   pieces fill the wedge (no piece crosses a cutting plane)?

## Results
| Structure | Shell (inner → outer) | Facet wedges | Name (technical) | Whole pieces? |
|---|---|---|---|---|
| Chain of Karma (Lotus) | icosahedron → icosahedron φ³ | 20 | triangular frustum (inner part a triangular pyramid) | no |
| Bodhi Kit B | rhombic triacontahedron → RT (φ² × …) | 30 | rhombic frustum (inner part a rhombic pyramid) | no (the 24 hold B1, B5L, B5R whole; cut pieces too) |
| Spheres of Dharma | icosahedron → icosidodecahedron | 20 + 12 | triangular frustum; pentagonal pyramid minus a pentagonal dipyramid | no |
| | icosidodecahedron → dodecahedron | 12 | pentagonal pyramid minus an 11-faced cap (5 tri, 5 quad, 1 pent) | no |
| | dodecahedron → truncated icosahedron | 12 + 20 | pentagonal frustum; hexagonal pyramid minus a 9- or 12-faced part | no |
| | truncated icosahedron → icosahedron | 20 | triangular pyramid minus a 7-faced part | no |
| | truncated icosahedron → 80-corner solid | 12 + 60 + 30 | pentagonal frustum; triangular frustum; quadrilateral pyramid minus a triangular dipyramid-like part | **the 12 pentagonal frusta: yes** |
| | 80-corner solid → rhombic triacontahedron | 30 | rhombic pyramid minus an 11-faced part | no |
| | rhombic triacontahedron → icosahedron φ³ | 20 | triangular pyramid minus a triangular dipyramid (the RT's 3 rhombi round a corner) | no (nface whole, the rest cut) |

Findings: (1) where inner and outer solids are similar and aligned, every facet wedge is a **frustum** (named); (2) where
they differ (duals, truncations), the wedge is a **pyramid with a recess** shaped by the inner solid's faces in that cone:
not a named family, names to propose; (3) the pieces almost never respect the facet cuts: opening by facets makes **new**
solids, except the 12 pentagonal frusta of the truncated icosahedron → 80-corner shell in Spheres of Dharma.

Not yet done: exact (symbolic) dimensions; the dual-pair split (cones over the inner solid's faces instead); literature
search (library first: Kepler 1596, Jamnitzer 1568, Hogan 1976; to add: Mackay 1962 icosahedral shells).

DICTO · dictospheres.com
