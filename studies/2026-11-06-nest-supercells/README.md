# Supercells of nests (DICTO 11-06: "make them into supercells like our 13s we built"; "or parts of the 120 and 600 or mid structure"; "c")
Route (c): clusters of cells from the 120-cell / 600-cell, a five-solid nest in every cell. Connected to studies/2026-11-06-five-in-octet
(nests, catalogue, gap pieces) and studies/2026-10-09-dodeca-13 (DICTO's Dodeca-13).

**Conclusion so far:** the 120-cell's 1 + 12 = DICTO's Dodeca-13 (13 dodecahedra + 30 wedges + 20 needles) carries a full nest in every
dodecahedron: D 1 > I 1.1708 (face centres) > O 1.3396 (six edge midpoints of I) > C 0.6315 (face centres of O) > T 0.8930 (alternate
corners of C); all 13 nests regular and nested, the 13 dodecahedra disjoint. Status: step 1 of route (c).

- scripts/nest13.py -> nest13.json; scripts/render13.py -> nested-dodeca-13.png (wedges and needles left out so the nests show).
- Freedom per cell: I holds five octahedra (and C two tetrahedra), so each dodecahedron has 10 ways to carry its O, C, T: the nests can be
  turned cell by cell (DICTO's "combis"); the figure uses the first found in each cell, so they point different ways.
- Next: choose the turns so the 13 nests line up (shared axes through the face-sharing pairs); then the 600-cell side (20 tetrahedra round
  a corner, each T > O > I > D > C) and the middle slice (icosidodecahedron); gaps by wedges/needles and the named pieces.

## Turns aligned (DICTO "align the turns"; scripts/align13.py -> nest13-aligned.json, nested-dodeca-13-aligned.png)
Central nest: its octahedron on the axes. Each outer nest = the MIRROR of the central nest in the pentagon they share; checked to be one of
that dodecahedron's own 10 nest choices (mirrored icosahedron = the outer one's face centres exactly). Six outer octahedra come out parallel
to the central one, six turned by 26.57 deg.

## The 600-cell side (DICTO "then do the 600 side"; scripts/tets600.py -> nest600.json, render600.py -> nested-600-corner.png)
The 600-cell's 20 tetrahedra round one corner, built with regular tetrahedra (edge 1), corner at the centre, far faces square-on to an
icosahedron's faces: pairwise disjoint; thin gaps 0.388167 = 14.1% of their hull (the 3D trace of the 4D curvature, like the Dodeca-13's
wedges). Every tetrahedron holds the six-solid nest T > TT 1/3 > O 1/2 > I (Pacioli) > D > C; all checked. The nest has the tetrahedron's
three-fold symmetry about its axis, so no turn choice arises on this side.
Next: the middle slice (the 600-cell's equatorial icosidodecahedron); gap pieces of the 20-tetrahedra corner.
