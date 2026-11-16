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
Redone 16 Nov 2026 after DICTO's critique of the first set ("they look all the same except color"): the slices were uniform clear crystals, the projection hid their differences, and in the plates figure every fin overlapped from one centre. The first set is in git history only.
- `RENDER-non-heart-vacuus-A-slices.png` and `-B-slices.png`: one slice per kind of plate. Every face is coloured by its kind, with a legend: triangle green, rectangle blue, rhombus pink, hexagon lavender (the Kaleidohedra app's face-kind colours), trapezoid yellow (the app's octahedron colour), pentagon red (the app's tetrahedron colour), heptagon the app's orange. Every slice is in one standard pose (the plate's own two-face flat at the bottom, gold rim, dashed where hidden; the same camera height and turn) and at one scale for all slices of both solids. Under each slice is a face-count strip: A1 2 triangles · 3 trapezoids; A2 3 triangles · 3 pentagons · 1 hexagon; B1 4 triangles · 3 rectangles · 7 hexagons; B2 1 triangle · 9 trapezoids · 1 hexagon · 3 heptagons; B3 6 triangles · 1 rectangle · 4 trapezoids · 2 pentagons; B4 2 triangles · 3 rectangles · 3 rhombi · 3 hexagons. White dots mark corners of the solid.
- `RENDER-non-heart-vacuus-A-plates.png` and `-B-plates.png`: one plate of each kind, alone: the cone from the centre over its two-face, drawn in the plate's own 3-space (true shape, same pose and scale as the slices, clear sides so the two-face's kind colour shows). Next to it a locator: the whole solid as a depth-shaded wire view (projection along the 5-cell axis through coordinate 5; per plate, the view of four that shows the two-face most open), with that two-face filled and its spokes to the centre dashed.
- Script: `scripts/render_vacuus.py` (pilot `--pilot` under 5 s, then the full run on the compute machine; log `data/render.log`, FINAL ok). It asserts the pose is a rigid motion with the ridge at z = 0, each strip adds up to the slice's face count, each model is inside its frame at the common scale, and each locator shows its two-face open. Edge-crop check: `data/edgecheck.log` (edgecheck.py, exit 0).

## The Vacuus as slotted sheets (16 Nov 2026, after DICTO: "better vacuus figures but they don't appear as vacuus in the figures")
DICTO's physical Vacuus solids are flat central plates slotted together through the centre (his cardboard octahedron: 3 squares with half-lap slots). These four figures draw the Vacuus that way. Camera and colours are those of the figures above (DICTO: "keep the view angles and colours"): the standard camera of `render_vacuus.py` for the key and the three kinds, the locator view along the 5-cell axis for A and B, and the app colours.

**Method (`scripts/render_sheets.py` with `scripts/sheets_lib.py`; log `data/render-sheets.log`, FINAL ok).** A 4D plate is the cone from the centre over one two-face R. A 3D hyperplane H through the centre cuts that cone in the cone over R ∩ H: one flat triangle (centre, p, q), where p and q are the two points at which H crosses the boundary of R. The triangles of one plate lie in one plane of H and together make that plate's sheet. Where two sheets of different plates cross, the common line through the centre gives the slot line. The corners p and q are exact in Q(√5). Floats are used for drawing only. The sheets are see-through (each pixel composites its sheets back to front by depth). The outline of the solid's own 3D section is drawn faint, and the slot lines are drawn bright. Edges are at least 1.5 px.

**Figures (`figures/`, copies in the reading folder)**
- `RENDER-vacuus-key.png`: heart = the octahedron: 12 edges on 3 planes, 4 on each, giving 3 full square sheets slotted along the axes. Non-heart = the regular tetrahedron: 6 fins (centre, edge). Checked exactly (integer coordinates): the plane through the centre and an edge holds that edge only, the 6 fin planes are distinct (no two fins coplanar), and each fin plane is a mirror (its normal is the opposite edge). The tetrahedron is turned (a rigid turn) so that every fin is seen open under the common camera.
- `RENDER-vacuus-A-sheets.png`, `RENDER-vacuus-B-sheets.png`: two cuts each, at one scale. Symmetric cut: H across the 5-cell axis through coordinate 5, normal (1, 1, 1, 1, −4). This is exactly the 3-space of the locator view. Generic cut: normal (3, −1, 7, −2, −7). Sheets are coloured by plate kind: A1 triangle green, A2 hexagon lavender; B1 green, B2 yellow-green, B3 rectangle blue, B4 sea green (B1, B2 and B4 all sit on triangles, so they are told apart by shades of green).
  - A, symmetric cut: 18 fins (12 A1, 6 A2). A, generic cut: 15 fins (7 A1, 8 A2).
  - B, symmetric cut: 36 fins (12 B1, 12 B2, 12 B3). B, generic cut: 39 fins (9 B1, 9 B2, 17 B3, 4 B4).
  - In every cut each plate gives one triangle and no fin passes through the centre. The fins meet only along spokes from the centre to the corners of the section (12, 10, 24 and 26 slot lines), so the cut reads as a fan of single fins.
- `RENDER-vacuus-three-kinds.png`: the 600-cell (heart), the 600-cell less an independent set of 8 corners on one side of the cut (inherited heart; 112 corners, 960 two-faces, 60 plates carrying 10 to 20 two-faces each, not centrally symmetric, Euler 0), and A (non-heart). The 600-cell pair is cut across a cell centre (a cross wall of the Queens, not a plate) at one scale. A is cut across its 5-cell axis. Each piece is coloured by what it shares: blue if its opposite piece lies on the same plate (a sheet through the centre); pink if its plate carries two or more two-faces but the opposite piece is missing; green for a single fin. The counts are: 600-cell 240 triangles on 48 sheets, all blue; diminished 174 triangles on 48 sheets, 108 blue and 66 pink; A 18 green. Three large sheets per panel are drawn solid. They are the largest triple that is at least 53° apart, with every pair slotting for the 600-cell pair. The rest are faint. The cut is turned inside H (a rotation, checked) so the three sheets stand like the key's squares under the same camera. A dashed line shows each solid sheet's whole plane across the section.

**Finding shown by the three-kinds figure.** In 4D a heart sheet is not a full polygon. A 600-cell plate holds 20 triangles of its icosidodecahedral slice but none of its 12 pentagons, so its sheet in a cut is a centrally symmetric fan with gaps over the pentagons (the dashed outline marks the whole cut). The octahedron's squares are full only because, in 3D, its four edges make up the whole boundary of the square slice.

**Checks.** 2664 exact corner checks: every sheet corner lies on its plate (n · p = 0, n from the two-face) and on H (u · p = 0). For A and B the check is repeated in the study's 5D coordinates, together with coordinate sum 0. For A and B: one two-face per plate (30 and 80 plates) and every piece a single fin. For the 600-cell: every piece has its opposite on its plate. For the diminished one: both kinds of shared piece occur and every plate carries at least two two-faces. Lengths are kept in the drawing, every model lies inside its frame margin, and every caption and legend fits. Edge-crop check: `data/edgecheck-sheets.log` (edgecheck.py, exit 0). Each image was looked at. The key, A, B and the 600-cell panel read as sheets slotted or fanned at the centre. The inherited-heart panel reads as blue sheets through the centre beside one-sided pink pieces.

## Leads
- The next version of #105 can state the plate counts with the kind table above.
- The B1 and B2 slices share their counts (21, 33, 14) but differ in face types (B1 has rectangles and hexagons, B2 has heptagons and trapezoids). This is worth one line in the paper.

DICTO · dictospheres.com
