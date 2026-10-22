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

## Step 2: adding the icosahedron (mixes2.py, mixes2.log, caps.py)

All 8 mixes containing the icosahedron I fill space, every solid at edge 1. The icosahedron (edge 1) sits in Pacioli's position in a regular octahedron of edge L = φ²/√2 ≈ 1.851 (its 12 corners on the octahedron's edges at the golden section; checked); the rest of that octahedron is DICTO's six Admiral Caps (F21, connector A: six congruent non-convex pieces, one round each octahedron corner, each of volume (√2L³/3 − 5φ²/12)/6 ≈ 0.31664). These large octahedra form an octet of edge L whose tetrahedra are split into 4 face pyramids (connector Q′, the tetrahedron's face pyramid at size L). The large octet is turned so a (111) layer plane is horizontal and fills the half-space above it with whole pieces; below, the step-1 filling of the rest of the mix (edge 1), its top plane cutting octahedra into half octahedra P. Faces need not match across that plane (the lattices differ by the irrational factor L), which the settled rules allow.

| mix | connectors |
|---|---|
| I | A, Q′ |
| I, C | A, Q′ |
| I, T | A, Q′, P |
| I, O | A, Q′, P, Q |
| I, T, O | A, Q′, P |
| I, C, T | A, Q′, P |
| I, C, O | A, Q′, P, Q |
| I, C, T, O | A, Q′, P |

Check: 30 000 random points in a box of side 3 (both seams inside), each covered by exactly one piece, for every mix. With step 1: 15 of the 31 mixes done, connector kit so far P, Q, Q′, A. Step 3 (the dodecahedron, with Dogstars on the cubic lattice) remains.
