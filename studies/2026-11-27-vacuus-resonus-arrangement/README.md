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
Hull family (convex hull of the two): at s = 2 the rhombic dodecahedron (space-filler, classical). Lattices (DICTO 27 Nov: "an
alternative or related construction of the fcc lattice"): hull at s = 2 = Voronoi cell of fcc; overlap at s = 3/2 = Voronoi cell
of bcc; so the pair gives both cubic lattices.
- 1 < s < 2 (cube + 6 square pyramids, height h = s - 1 < 1): 12 cube edges, length 2, dihedral pi/2 + 2 beta (tan beta = h);
  24 lateral edges, length l = sqrt(2 + h^2), dihedral pi - gamma (cos gamma = 1/(1 + h^2) = cos^2 beta). Dehn invariant (mod Q pi)
  = 48 (x) beta - 24 l (x) gamma.
  * If l is irrational, 1 and l are independent over Q, so zero needs beta and gamma both in Q pi with 2 cos gamma - cos 2 beta = 1.
    By Conway and Jones (1976, Acta Arith. 30) a rational value of such a two-cosine sum with rational angles forces both cosines
    rational (the only irrational two-term case is cos pi/5 - cos 2pi/5 = 1/2, coefficients 1, -1), i.e. cos gamma in {0, 1/2, 1}:
    impossible for 0 < h < 1 (cos gamma in (1/2, 1)). So NO space-filler with l irrational (this covers every transcendental h).
    [Proof sketch; to write out against the Conway-Jones list exactly.]
  * If l is rational (h = sqrt(r^2 - 2), r rational in (sqrt2, sqrt3)): one condition 48 beta - 24 r gamma in Q pi. Scan: all 6,388
    such r = p/q with q <= 200, PSLQ at 50 digits (coefficients up to 10^6): no zero. Not a proof (Baker-type argument needed).
- 2 < s < 3 (octahedron + 8 triangular pyramids, apexes at the cube corners; u = s - 2 in (0,1)): outward normals (1,1,u),
  (1,1,-u) across the 12 octahedron edges (length a = (u+2) sqrt2), (u,1,1) across the 24 lateral edges (length
  l = sqrt(u^2 + 2u + 3)); cos phi_b = (2 - u^2)/(2 + u^2), cos phi_l = (2u + 1)/(2 + u^2); Dehn invariant = -12 a (x) phi_b -
  24 l (x) phi_l (mod Q pi).
  * a, l independent over Q: zero needs phi_b, phi_l both in Q pi. Exact for cos phi_b rational: the only rational-angle value in
    (1/3, 1) is 1/2, giving u = sqrt(2/3) and cos phi_l = (3 + 2 sqrt6)/8, a quadratic irrational that is not the cosine of a rational
    angle (those are (+-1 +- sqrt5)/4, +-sqrt2/2, +-sqrt3/2): no. Irrational cos phi_b: scan of all 31,224 rational base angles
    p pi/q (q <= 400) in range, PSLQ for phi_l: no hit (not a proof).
  * a = t l, t rational (u from a quadratic): scan of 1,991 cases (t = P/Q, Q <= 200): 12 t phi_b + 24 phi_l never in Q pi
    (numerical, 50 digits).
  So, so far: on both sides the only hull that fills space is the rhombic dodecahedron (s = 2); exact for the generic sizes on the
  tetrakis side (Conway-Jones sketch), numerical for the rest.
- s <= 1 the hull is the cube (a space-filler, trivially); s >= 3 the octahedron (not).
