# The non-heart Vacuus of the golden solids A and B (16 Nov 2026, for "Silent Running: Twisted Silence")

**Conclusion (exact, Q(√5)):** solid A has 30 two-faces on 30 central plates in 2 kinds, solid B has 80 two-faces on 80 central plates in 4 kinds. Each plate carries exactly one two-face, so both are Vacuus of the non-heart kind. The control, the n = 5 permutohedron, gives 150 two-faces on 65 plates, with 5 heart slices that are DICTO 1:2 Truncated Octahedra.

Status: SETTLED (exact). This replaces the floating-point pilot in `studies/2026-11-15-golden-a4-candidate/vacuus/RESULT.md`.

## Question
The Vacuus (#105) is the set of central plates: each plate is the hyperplane through the centre spanned by one two-face (ridge). A slice is the solid cut by one plate. For A = hull of the permutations of (φ², φ², φ², φ, 0) and B = hull of the permutations of (φ², φ², 1, 1, 0), each centred at its mean, we count the plates exactly, sort them into kinds under the symmetry group, and describe one slice of each kind.

## Method
`scripts/vacuus_exact.py` does all arithmetic exactly in Q(√5) using Fractions:
- facets from the faces x_S = min (Rado), cross-checked against a floating-point hull;
- edges and two-faces from facet incidences, with a 4D Euler check;
- each plate's normal as an exact null vector, normalised so its first nonzero entry is 1;
- the full symmetry group, taken as every vertex permutation that keeps the centred Gram matrix (exact backtracking, so any symmetry beyond Sym5 would show up);
- the orbits of the plates;
- one exact slice per orbit: corners (corners of the solid on the plate, plus points where the plate crosses an edge), edges and faces, with a 3D Euler check, exact side lengths, exact angle tests and a shape name for each face.

`scripts/render_vacuus.py` draws the figures from `data/vacuus-exact.json`. Floats are used for drawing only.

## Results (`data/vacuus-exact.txt`)
| solid | corners, edges, two-faces, cells | symmetry group | centrally symmetric | plates | two-faces per plate |
|---|---|---|---|---|---|
| A | 20, 40, 30, 10 (5 tetrahedra, 5 golden truncated tetrahedra) | 120 | no | 30 | 1 on each |
| B | 30, 90, 80, 20 (5 octahedra, 10 golden prisms, 5 golden cuboctahedra) | 120 | no | 80 | 1 on each |
| control: permutohedron n = 5 | 120, 240, 150, 30 | 240 | yes | 65 | 2 on 60 plates, 6 on 5 plates |

Kinds of plate, with the slice each one cuts. A slice's corner count is written as corners of the solid + edge crossings.
- **A1**: 20 plates on the triangles (side √2, between a tetrahedron and a golden truncated tetrahedron). The slice is a frustum with 6 = 6 + 0 corners, 9 edges and 5 faces: the ridge triangle (√2), a triangle with side φ²√2, and 3 isosceles trapezoids with sides √2, 2φ, φ²√2, 2φ.
- **A2**: 10 plates on the hexagons (sides √2 and φ√2 in turn, between two golden truncated tetrahedra). The slice has 10 = 6 + 4 corners, 15 edges and 7 faces: the ridge hexagon, 3 isosceles triangles (√6/2, √6/2, √2) and 3 pentagons (√6/2, φ√2, √6/2, φ²√6/2, φ²√6/2).
- **B1**: 20 plates on the triangles (φ√2, between an octahedron and a golden prism). The slice has 21 = 3 + 18 corners, 33 edges and 14 faces: the ridge triangle, 3 rectangles, 3 isosceles triangles, 1 equiangular hexagon (φ√2/2 and √2) and 6 hexagons.
- **B2**: 20 plates on the triangles (φ√2, between a golden cuboctahedron and an octahedron). The slice has 21 = 3 + 18 corners, 33 edges and 14 faces: the ridge triangle, 9 isosceles trapezoids, 1 equiangular hexagon (√2/2 and φ√2) and 3 heptagons.
- **B3**: 30 plates on the rectangles (√2 × φ√2, between a golden cuboctahedron and a golden prism). The slice has 13 = 9 + 4 corners, 24 edges and 13 faces: the ridge rectangle, 4 scalene and 2 isosceles triangles, 4 isosceles trapezoids and 2 pentagons.
- **B4**: 10 plates on the triangles (√2, between two golden cuboctahedra). The slice has 15 = 6 + 9 corners, 24 edges and 11 faces: the ridge triangle, a triangle with side φ√2, 3 rectangles (√2 × φ√6/2), 3 rhombi (side φ√6/2) and 3 hexagons.
- **Control**: the 5 plates that carry 6 squares each cut the 1:2 Truncated Octahedron (6 squares √2 and 8 hexagons with sides √2 and 2√2 in turn): the heart. The other permutohedron plates fall into three kinds: 20 and 10 plates on hexagon pairs, and 30 plates on square pairs.

Exact face lists for every slice are in `data/vacuus-exact.txt`. Exact normals, coordinates and incidences are in `data/vacuus-exact.json`.

## Checks
- Controls: the permutohedron gives 120/240/150/30, 65 plates and group order 240.
- The asserted counts match the background: A gives 20/40/30/10 and 30 plates; B gives 30/90/80/20 and 80 plates.
- Neither A nor B is centrally symmetric (exact test); both have group order 120.
- Euler holds in 4D for each solid and in 3D for each slice. Each plate's ridge is a face of its own slice.
- Floating-point hull facet counts agree with the exact ones.
- Logs: `data/vacuus-exact.log` (FINAL ok), `data/render.log` (FINAL ok), `data/edgecheck.log` (edgecheck.py, the edge-crop check used by figcheck.mjs: exit 0).
- figcheck.mjs itself needs a paper.html; per the brief, paper.html was not edited, so the images were checked with edgecheck.py directly. In addition, every panel asserts that its model lies inside the frame margin and uses one scale for x and y.

## Figures (`figures/`, copies in the reading folder as RENDER-non-heart-vacuus-*.png)
- `RENDER-non-heart-vacuus-A-slices.png` and `-B-slices.png`: one slice per kind of plate, drawn as a see-through crystal. The plate's own two-face is filled in the kind's colour with a gold rim. White dots mark corners of the solid.
- `RENDER-non-heart-vacuus-A-plates.png` and `-B-plates.png`: every plate of each kind, drawn as the cone from the centre over its two-face, inside the wire cage of the solid. The 3D projection is taken along one coordinate axis of the 5-cell.
- Colours of the kinds (element colours): A1 T red, A2 I blue; B1 O yellow, B2 C green, B3 I blue, B4 D violet.
- The optional heart / non-heart side-by-side panel was not made.

## Leads
- The next version of #105 can state the plate counts with the kind table above.
- The B1 and B2 slices share their counts (21, 33, 14) but differ in face types (B1 has rectangles and hexagons, B2 has heptagons and trapezoids). This is worth one line in the paper.

DICTO · dictospheres.com
