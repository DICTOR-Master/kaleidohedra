# The reversed neighbour (2026-11-04) — Concordance gap 3; #92 open point 1, #93 open point 1
Started on DICTO's "yes start the reversed neighbour".
Method: by #92 Prop. 7 (T) and #93 Thm D (C6), round every lateral edge of a pyramid lie exactly three such pyramids sharing that whole edge,
so each of the two other sectors holds the NORMAL piece (same solid) or the REVERSED piece (apex at the other end). Depth-first search over
these forced choices with an exact-geometry overlap test (separating axes); a branch dies when a sector admits neither piece.
scripts/reversed_search.py (T), scripts/reversed_general.py (T and C6).
RESULTS
- T (tetrahedron's centre pyramid): every branch starting with a reversed neighbour dies within 20 pieces: 89 search nodes, 90 rejections,
  smallest overlap depth 0.2016 (edge 1) — far above rounding; same tree at tolerances 1e-7, 1e-9, 1e-11. Normal pieces close the tetrahedron (4, no overlap).
- C6 (cube's centre pyramid): dies within 7 nodes, smallest overlap 0.444.
THEOREM (computer-assisted, exact up to a 0.2 margin): no reversed neighbour occurs in any tiling, face to face or not.
Hence (i) in every tiling by the tetrahedron's and octahedron's centre pyramids, the T pyramids fall into whole regular tetrahedra (#92 §6 open point 1 closed);
(ii) in every tiling by the cube's centre pyramids, they fall into whole cubes, so the tilings are exactly the cube tilings cut from the centres (#93 open point 1 closed; the freedom of #93 Thm D is that of cube tilings).
Placement (publish rule 11-04): sections of #92 v3 and #93 v2 in the weekly batch; chapter of the Centre Pyramids volume.
LEADS: the R12 pieces (two kinds of lateral edge, #93 Thm C) by the same search; O pyramids: do they always fall into octahedra or the cube's four corners?

## RD pyramids (R12), 4 Nov
- Reversed neighbours DO occur for R12: they are #93 Theorem C's free diagonal choices (pieces with apex at the far corner). The open question is #93 open point 2 (not face to face).
- All R12 angles are rational multiples of π (π/3, π/2, 2π/3), so edge-angle counting forces nothing.
- Plane of faces: in the Theorem C tiling where every square perpendicular to z is cut along its diagonal on x + y = integer (other squares either way),
  the plane x + y = 1 cuts no piece (384 pieces checked): it is made of faces. Every plane x + y = k is, so each half-space can slide along it by any amount.
  Hence uncountably many R12 tilings that are not face to face, with continuous parameters: no finite list describes them (as for C6, #93 Thm D, and #92 Cor. 9).
