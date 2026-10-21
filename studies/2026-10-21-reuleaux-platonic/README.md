# The Platonic solids as Reuleaux bodies (DICTO, 2026-10-21)

DICTO's idea: a ball on every corner of a Platonic solid, radius = the solid's diameter; the body is what all balls share. Named by
look (DICTO): balls on the cube's corners = Reuleaux octahedron, on the octahedron's = Reuleaux cube, on the dodecahedron's = Reuleaux
icosahedron, on the icosahedron's = Reuleaux dodecahedron. `reuleaux_platonic.py` (mesh, colouring), `reuleaux_compose.py` (figure).

## Widths (`widths.py`, `widths.log`; no mesh)
Support function from the candidate extreme points (ball caps, sphere-sphere circles, triple points), width min/max over 3000
directions + Nelder-Mead refinement. At diameter 1:
- Reuleaux tetrahedron 1 .. 1.024944 (classical; not of constant width).
- Reuleaux octahedron and Reuleaux cube: 1 .. 1.248391589161, equal to 12 digits; Reuleaux icosahedron and Reuleaux dodecahedron:
  1 .. 1.110988655456, equal to 15 digits.
- Why (exact): along the axis through a face centre of the solid the extreme point lies on the axis, held by the corners of the
  opposite face: width = 2 sqrt(3/4 + r^2) - 2r, with circumradius 1/2 and r the inradius. Dual solids share r/R (1/sqrt3 for
  cube/octahedron; sqrt((5 + 2 sqrt5)/15) for dodecahedron/icosahedron), so the widths along those axes are equal exactly:
  (sqrt30 - sqrt3)/3 = 1.248392 and 1.110989. The minimum 1 is the diameter (two opposite corners). That these axis values are the
  global maxima is numerical (search above), not proved.
- Prior art: the Reuleaux tetrahedron (Reuleaux), Meissner bodies (1911), Reuleaux polytopes (Sallee 1970), ball-polyhedra
  (Bezdek, Lángi, Naszódi, Papez 2007), Meissner polyhedra (Montejano, Roldán-Pensado 2017). Ball-polyhedra, Meissner polyhedra and Hynd 2023 (Reuleaux polyhedra) are now in the library (arXiv, 2026-10-21), Sallee link-only;
  add legal copies before any paper. The library search (Fedorov, Grünbaum, papers/, history/, shapes/) found nothing on these bodies.

Checks for paper #45 (`reuleaux_checks.py`, `reuleaux-checks.log`, 45 PASS). Exact (Q(sqrt5)): diametric pairs (4, 3, 10, 6 against
2m - 2 = 14, 10, 38, 22; the tetrahedron 6 = 6), each corner on exactly one other sphere (so not a Reuleaux polyhedron in Sallee's
sense), corner heights >= -r along a face axis, (r/R)^2 shared by duals, the closed forms, and the tetrahedron's edge-midpoint width
sqrt3 - sqrt2/2. Numerical: face-axis widths = widths.log maxima, volumes at diameter 1 (0.42216, 0.64940, 0.68764, 0.57188, 0.59679;
the tetrahedron = Harbourne's formula quoted by Hynd 2023, to 1.1e-8), faces meet along arcs exactly along the solid's edges, fewest
colours 4/2/3/3/4.

DICTO · dictospheres.com
