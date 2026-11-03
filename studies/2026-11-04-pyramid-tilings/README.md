# Tilings by the tetrahedron's and octahedron's centre pyramids (DICTO, 2026-11-04; paper #92)

DICTO's idea: the tilings left open in #44 (Aristotle's Pyramid) are decided by the pyramids' own parameters
(edge lengths, face shapes, dihedral angles). T = tetrahedron's centre pyramid, O = octahedron's, base edge 1.

## Results (proofs in ../../papers/2026-11-04-pyramid-tilings/paper.src.html)
- Face to face: T pyramids always form whole tetrahedra, O whole octahedra (faces of three non-congruent shapes;
  mirror argument). The face-to-face tet/oct tilings are exactly the Barlow stackings of octet layers (edges 2T+2O,
  TOTO or TTOO; two vertex stars, cuboctahedron or triangular orthobicupola; a layer plane exists and propagates).
  Equal numbers of T and O pyramids (8 + 8 per corner).
- Not face to face: nine edge configurations only (exact enumeration); every T lateral edge is shared end to end by
  three T pyramids; a cube of edge 1/sqrt2 = 4 T + 4 O in two ways, so every cube tiling (cut either way per cube)
  is a T/O tiling; half-space gluings along face planes. No finite parametrisation.
- OPEN: can a "reversed" T neighbour (apex at the other end of the shared lateral edge) occur? (if never, T always
  forms whole tetrahedra); configurations (1,1,0,3), (3,3,0,1), (1,1,0,1) undecided; structure theorem for
  non-face-to-face tilings; mixed sizes.

## Files
- tiling_checks.py -> data/tiling-checks.log (46 PASS, 0 FAIL), data/barlow-patches.json. Exact: sympy (Part A),
  integer coordinates (a/2, b*sqrt3/6, c*sqrt6/3) for stacking patches ABCABC, ABAB, ABCB, random 14 layers
  (Part B), Fractions for the cube (Part C).
- vertex_stars.py -> data/vertex-stars.log/.json: float search of all closed vertex stars; finds exactly two.
- figs.py -> figures/ (matplotlib; float copies of the same constructions).
Run on dicto-big-brother: ~/geom/bin/python3 <script> (sympy, numpy, matplotlib).

## Prior art
Barlow (1883); Gabbrielli, Jiao, Torquato, PRE 86 (2012) 041141 (state f2f = Barlow without proof; sliding;
CJT family); Conway, Jiao, Torquato, PNAS 108 (2011) 11009; Grunbaum, Geombinatorics 4 (1994) 49-56 (gyrated);
Wikipedia tet-oct honeycomb (library copy). Library: 246 PDFs full-text searched 2026-11-04.

DICTO · dictospheres.com
