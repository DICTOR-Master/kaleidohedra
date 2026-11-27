# The joint Vacuus + Resonus arrangement (study, 27 Nov 2026)

DICTO's conjecture, his words: "create intersecting planes of vacuus and resonus to define their intersectionality and resolve
desired outcomes via those planes through trigonometry ... including but not limited to calculating new combinations of or
alternative spacefilling solutions." Fairness of dice is one use, not the aim. DICTO "yes to all" (27 Nov) to:
1. state it as an arrangement theorem (finite explicit angle basis; space-filling, combinations and fair faces become exact linear
   conditions on cell counts), fairness a corollary; 2. n = 4 exactly; 3. Dehn-invariant filter on cells and unions, then tiling
   tests; 4. its own paper. With Claude (Anthropic).

## Step 1: n = 4, the truncated octahedron (scripts/joint4.py, logs/joint4.log, data/joint4.json)
P4 centred in the 3-space sum y = 0. All exact (fractions).
- 36 edges give **15 Vacuus planes**; 14 facets give **7 Resonus planes**; 3 Resonus planes are also Vacuus planes, so the joint
  arrangement has **19 distinct planes** (agrees with #120 and the Lean entry: A402191(4) = 15, 2^3 - 1 = 7, 2^2 = 4 not ridge planes).
- **93 lines** through the centre: 75 where 2 planes meet, 12 where 3 meet, 6 where 5 meet (which symmetry axes these
  are: to identify in step 2).
- **248 cones** (cells from the centre): 2 + 2 x sum (m - 1).
- Plane-pair angles, exact cos^2: 0 (15 pairs), 1/81 (12), 1/27 (24), 1/9 (18), 16/81 (24), 1/3 (24), 4/9 (24), 49/81 (6),
  64/81 (12), 25/27 (12).
- Angle basis (identified by PSLQ at 60 digits, NOT yet proved): every plane-pair angle is a rational combination of pi and
  five basic angles arccos sqrt(25/27), arccos sqrt(64/81), arccos sqrt(4/9), arccos sqrt(16/81), arccos sqrt(1/27); e.g.
  arccos(1/9) = pi - 2 arccos(2/3) (exact by the double-angle formula), arccos sqrt(1/3) = pi/3 - (1/3) arccos sqrt(25/27).
  Whether the five are independent over Q (with pi) is open (step 2).

## Next
2. Exact proofs of the relations (double/triple-angle identities, checked symbolically) and of independence where possible.
3. The pieces of P4 cut by the 19 planes (bounded cells); their Dehn invariants in the angle basis; unions with Dehn invariant 0
   = space-filling candidates; then tiling tests.

## DICTO's question (27 Nov): a shape from joining the cube and octahedron that fills space by itself
Overlap family: cube |x_i| <= 1, octahedron |x|+|y|+|z| <= s, 1 < s < 3 (octahedron -> truncated octahedra (1 < s < 2) ->
cuboctahedron (s = 2) -> truncated cubes (2 < s < 3) -> cube). **Exactly one member fills space: the Archimedean truncated
octahedron, s = 3/2.** Proof (exact, by the pair's plane angles; theta = arccos(1/3), theta/pi irrational):
- 1 < s < 2: square edges a = sqrt2 (s - 1), 24 of them, dihedral pi - arccos(1/sqrt3) = pi/2 + theta/2 (since 2 arccos(1/sqrt3) =
  pi - theta); hexagon-hexagon edges b = sqrt2 (2 - s), 12, dihedral pi - theta. Dehn invariant (mod Q pi) = 24a (x) theta/2 -
  12b (x) theta = 12 sqrt2 (2s - 3) (x) theta: zero iff s = 3/2 (x (x) theta = 0 iff x = 0, as theta is not in Q pi).
- s = 2 and 2 < s < 3: the triangle edges carry pi/2 + theta/2 with positive total length, the octagon-octagon (cube) edges pi/2:
  Dehn invariant nonzero, never a space-filler.
- Dehn invariant zero is necessary for space-filling (Debrunner 1980); s = 3/2 tiles (Fedorov 1885; Kelvin 1887). Facts classical;
  the one-line proof inside the family is ours.
Hull family (convex hull of the two): at s = 2 the rhombic dodecahedron (space-filler, classical). Other s: 1 < s < 2 tetrakis
type, 2 < s < 3 triakis type; whether any fills space is OPEN here (Dehn: needs both the base-edge and the lateral-edge angles
rational multiples of pi unless the edge lengths are commensurate; to check exactly).
