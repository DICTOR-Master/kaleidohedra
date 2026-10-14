# Truncated rhombi (study, DICTO, 2026-10-14)

DICTO's question: is there a family of "truncated rhombi", related to or separate from the FUJI family's flat-ended triangles?
Two rhombi: the rhombic dodecahedron's (diagonals 1 : √2, angles 70.53° and 109.47°) and the golden rhombus of the rhombic
triacontahedron (diagonals 1 : φ, angles 63.43° and 116.57°). Corners cut: the sharp ones, the blunt ones, or all four.
`scripts/rhombi.py`, `rhombi.json`.

## 1. One natural cut each (cyclic truncation)

A pyramid with all side edges equal stands only on a base whose corners lie on one circle (as FUJI's flat-ended triangle does).

- **Cutting the sharp corners** makes the rhombus cyclic at exactly one depth: when the circle through the two blunt corners (radius
  half the short diagonal) also passes through the four cut points.
  - RD rhombus: cut **one third** of each side; a hexagon with sides 1/3 and 1/√3 (short diagonal 1).
  - Golden rhombus: cut **1/√5** of each side; a hexagon with sides 1/√5 and √((5 − √5)/10) = 0.5257.
- **Cutting the blunt corners** never makes it cyclic, and cutting all four only does in the limit where the rhombus is cut away.
- On each cyclic hexagon a pyramid with **equilateral faces on its long sides** stands (as FUJI's do): height 1/(2√3) = 0.2887
  (RD) and √((5 − 2√5)/20) = 0.1625 (golden), both low.

So unlike the triangle, a rhombus gives one natural member, not a family running from sharp to flat.

## 2. Even spacing: solids with truncated-rhombus faces

As with the dictosphere (cube and octahedron planes at the same depth), each rhombic solid with a second set of planes at the
same depth:

| Solid | Faces | Truncated rhombi |
|---|---|---|
| rhombic dodecahedron + cube planes | 6 squares + 12 hexagons | sharp corners cut; sides 0.507 and 0.828, angles 109.47°, 125.26° |
| rhombic dodecahedron + octahedron planes | 8 triangles + 12 hexagons | blunt corners cut; sides 0.551 and 1.101, angles 70.53°, 144.74° |
| rhombic triacontahedron + dodecahedron planes | 12 pentagons + 30 hexagons | sharp corners cut; sides 0.334 and 0.413, angles 116.57°, 121.72°, nearly regular hexagons |
| rhombic triacontahedron + icosahedron planes | 20 triangles + 30 hexagons | blunt corners cut; sides 0.351 and 0.639, angles 63.43°, 148.28° |

(Inradius 1 throughout.) These are the "port spheres" of the rhombic solids: the patterns a sphere takes when ports at the face
centres of both sets are spaced evenly, as the dictosphere's 14 ports gave flat-ended triangles. The third, 42 ports in the
pattern of 12 pentagons and 30 near-regular hexagons, is close to a football and is the icosahedral counterpart of DICTO's
dictosphere. The even-spacing cuts are not the cyclic ones of §1.

## Open

- Which truncated rhombi turn up in DICTO's builds (DICTO mentioned one of his own; which?).
- Do the cyclic members of §1 close any cluster, as FUJI closes the Lotus seed?

DICTO · dictospheres.com
