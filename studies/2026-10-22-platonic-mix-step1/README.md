# Any mix of Platonic solids fills space: step 1 (cube, tetrahedron, octahedron)

DICTO's idea (2026-10-22): connect all the Platonic solids in any combination, combining the earlier work. Settled with DICTO: one edge length (1), new connector pieces allowed, filling without gaps is enough (no face-to-face condition), aim a theorem paper. Step 1: the 7 mixes of C (cube), T (tetrahedron), O (octahedron).

**Result (mixes.py, mixes.log):** all 7 mixes fill space at edge 1 with only two connector pieces, both cut from the solids themselves:
- P, the half octahedron (square pyramid, Johnson J1), and
- Q, the tetrahedron's face pyramid (a quarter tetrahedron; #44).

| mix | filling | connectors |
|---|---|---|
| C | cubic lattice | none |
| T, O | octet | none |
| T | octet, each octahedron split into 2 P | P |
| O | octet, each tetrahedron split into 4 Q | Q |
| C, T, O | octet above z = 0, cubes below | P (the octahedra cut by the seam) |
| C, T | as C, T, O with every octahedron split into 2 P | P |
| C, O | as C, T, O with every tetrahedron split into 4 Q | P, Q |

The seam: in the octet with vertices at the fcc points s(x, y, z), x + y + z even (s = 1/√2), the plane z = 0 is tiled exactly by the square equators (edge 1) of the octahedra centred in it, so edge-1 cubes below meet the half octahedra square to square. Check: 40 000 random points in a box of side 3.2 are each covered by exactly one piece, for every mix; each mix uses its own solids and no others.

Classical alternatives (prior art, uniform honeycombs): T + truncated tetrahedra (DICTO's suggestion), O + cuboctahedra. DICTO's adaptor/scutoid bridge idea is not needed for step 1; it may matter for the icosahedron and dodecahedron steps.
