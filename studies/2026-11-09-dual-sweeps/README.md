# The second dual sweeps CO ∩ μ·RD and ID ∩ μ·RT on the DICTO Hopscotch, study 2026-11-09

Framework, names and the proposal to read every DICTO sweep as a polar line: DICTO (the Hopscotch, antipol, hop, step, jump, the
turn, emergence, dissolution; outline papers/polar-line-outline). Computation and proofs with Claude (Anthropic).

## Verdicts (one line per bird)

1. **Walls: SETTLED (exact).** CO–RD has walls at μ = 1, 4/3, 3/2, 2 and ID–RT at μ = 1 + 2√5/5, 7/6 + √5/2, 5/4 + √5/2, 3/2 + √5/2.
   In both cases these are exactly the **squared flag radii of P** (face centres of each kind, edge midpoint, corner). Every wall is
   the root of a 4×4 concurrency determinant that is linear in μ. The kinds come in the same order on both lines: emergence,
   emergence, jump, dissolution. The line as a whole is a step.
2. **Turn: NO TURN on either line (theorem plus exact check).** The antipol carries P ∩ μP* back onto its own line only if every
   face of P is at one distance and every corner at one radius, which means P is regular. So the C–O line has a turn and these two
   lines do not. **"The turn maximises t_min" therefore has nothing to test here.** What carries over is a local turn at the jump.
   The only interior maximum of t_min sits at √(ρ²·f), where ρ² is the jump wall and f is the antipol's own jump (a foot wall), and
   the t_min piece there is symmetric under μ ↦ ρ²f/μ. On the C–O line this local turn coincides with the turn (√3).
3. **#89's golden rhombic cuts: NOT ON THESE SWEEPS (exact; this corrects the ranked gap's premise).** #91's "every corner cut is on
   P ∩ μP*" holds for regular P, which has one corner orbit. RD and RT have two corner orbits, so their two-depth cuts form a plane
   of solids, and the second dual sweep is a single line in that plane. All four golden rhombic cuts lie off it. In metric terms:
   #89's cut needs TWO linear metric factors to vanish together (equal corner sides, and corner : original = φ^{±1}). On a
   one-parameter line that needs a common root, and the equal-corner factor has no root in the octagon hop on either line (CO–RD
   (10 + √2)/7 ≈ 1.6306; ID–RT ≈ 2.44004; both past the jump).
4. **Golden cuts as walls: NO, they are METRIC events (agrees with splash-determinants rule 4).** A golden cut is never a
   face-structure wall of S(μ); it sits inside a hop, at the root of a linear edge-ratio factor. On the C–O line this was checked
   exactly for all four (Icosaxes μ = φ, Unborn Axes 3 − φ, both Golden Cut Cubes in Q(√2, √5)), matching splash
   data/sweep-events.json to 10⁻¹². The factor can be dressed as a 4×4 determinant, but only by adding a plane through the centre on
   the golden ray, whose normal lies outside the field of the solid's normals. That is a metric factor written as an incidence, not
   an incidence.
5. **#49's stretches as stops: NO (symmetry), one exception.** Every member of these lines has full octahedral or icosahedral
   symmetry. A stretch along a segment keeps only the stabiliser of its axis, so it cannot be a member. The exception is #49's
   tetrahedron with four caps, the cuboctahedron, which is not a stretch along a segment. It is the end μ = 2 of CO–RD and the jump
   wall of the C–O line.

**Follow-up (splash-determinants study): three event types, and its 5/3 prediction.**
- **Incidence** (4×4 plane determinants, in the field of the normals):
  - CO–RD: walls 1, 4/3, 3/2, 2 of S, plus the foot wall 8/5, an incidence of the antipol S^∨ that shows as a kink of t_min.
  - ID–RT: walls h₅², h₃², ρ², R², plus the foot wall (38 + 14√5)/29.
- **Metric** (lengths affine in μ, linear factors):
  - CO–RD Dehn invariant (s4, exact; one irrational angle class θ = arccos(1/√3), PSLQ-checked):
    - identically 0 on [1, 4/3], where every dihedral angle is a rational multiple of π;
    - 24√2(3μ − 4)·θ on (4/3, 3/2), zero only at the wall 4/3;
    - **24√2(3μ − 5)·θ on (3/2, 2): the prediction is CONFIRMED, root exactly 5/3.** The factor is (total oct–rhomb edge length) −
      (total cube–oct edge length) = 24√2[(2 − μ) − (2μ − 3)].
  - ID–RT Dehn: two irrational angle classes give two components per hop, and their roots never coincide inside a hop. Roots:
    h₅² on the first hop; h₅² and h₃² on the second; 4/3 + √5/2 and φ² on the third. **So no Dehn zero on the open ID–RT line.**
  - Golden one-factor stations in the octagon hops (side ratio φ^{±1} or 1 between two of the three octagon sides):
    - CO–RD: 1.36851, 1.38923, 1.40825, 1.42820, 1.47037, all exact in Q(√2, √3, √5) (see the log).
    - ID–RT: 2.31189, 2.32131, 2.33129, from the triangle side against the remnant side only.
    - None is a #89 cut.
- **Stationary** (derivative zero):
  - the interior maximum of t_min at the local turn √(ρ²f): √(12/5) on CO–RD, √((165 + 73√5)/58) on ID–RT;
  - the CO–RD Q4 zero of 2026-11-04 is a harmonic event, the splash study's fourth kind; not re-derived here.
- Agreement with splash: CO ∩ μ·RD has no turn (its §5) and ID ∩ μ·RT has none either. φ enters the ID–RT incidence walls only
  because the normals lie in Q(√5), which fits its rule 4.
- s4_metric_events.py reuses splash's corrd_events.py, with the plane list and exact corner enumeration exec'd from a copy in
  data/input-splash, and cross-checked against sweeplib at 3 points. It also reuses splash's data/sweep-events.json (golden cuts).

Bonus, closing LEAD 3 of 2026-11-04-co-rd-sweep: Q4 is constant on (3/2, 2) because every corner there is an image of
(1, μ − 1, 2 − μ). For that corner x = y + z, and the identity (y + z)⁴ + y⁴ + z⁴ = 2(y² + yz + z²)² gives Σx⁴/|x|⁴ = 1/2 for
every corner. The CO's corners (1, 1, 0) satisfy the same relation, so Q4 equals the CO's value, 0.1909.

Ledger: entries 15 and 41 (CO–RD Q6 and Dehn) and 58 (sphere row) touch these lines; none attempted walls, turn or golden placement.
Nothing here retries an earlier attempt.

Scripts: scripts/, all run on compute-host with python3 and sympy 1.14. Each takes under 3 min and ends FINAL ok; the
logs are in data/. sweeplib.py is an exact Q(√d) field plus a polar-line walker: corners are found in floating point, then re-solved
and certified exactly. On a hop every corner is p + μq, and the next wall is the smallest root of a·(p + μq) = b(μ). drive.py
finds walls, kinds, foot walls and the exact t_min envelope. s0_cube_oct_known.py is the known case. s1_co_rd.py and s2_id_rt.py are
the two lines. s3_golden.py covers birds 3 and 4. s2_geometry.py holds the ID/RT planes and is shared with s3. s4_metric_events.py covers the Dehn invariant, golden metric factors
and the three event types.

## Known case first (s0, FINAL ok)

C–O line P_μ = [−1, 1]³ ∩ {|x| + |y| + |z| ≤ μ}. The face-structure walls are **1, 2, 3**:
- 1: emergence of the 6 squares, det 4μ − 4.
- 2: jump, 12 oct–oct bonds dissolve as 12 cube–cube bonds emerge, det 4 − 2μ.
- 3: dissolution of the 8 triangles, det 3 − μ.

**3/2 is not a wall of S.** It is a foot wall: a wall of the foot-point hull P(S), and so of the antipol S^∨. It is the turn's image
of the jump at 2. The README of 2026-11-09-hopscotch-rows lists "1, 3/2, 2, 3"; read correctly, that is three walls of S plus one
foot wall. Also reproduced: S^∨(μ) = S(3/μ) at 6 points; t_min = min(μ, 3/μ, 5 − μ − 3/μ) at 43 rationals; t_min(√3) = 5 − 2√3.

## Bird 1: the walls

Coordinates: P* is the polar of P in the unit sphere, and S(μ) = P ∩ μP*.
- CO–RD: CO = {|xᵢ| ≤ 1, |x| + |y| + |z| ≤ 2}, RD = {|xᵢ| + |xⱼ| ≤ 1}. These are the units of 2026-11-04-co-rd-sweep.
- ID–RT: the ID is the set of edge midpoints of the icosahedron with corners the cyclic permutations of (0, ±1, ±φ).
  RT = {m·x ≤ 1 : m a corner of the ID}.

| wall | CO–RD μ | ID–RT μ | flag point of P | 4 concurrent planes | det (linear) | kind |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 + 2√5/5 ≈ 1.8944 | square / pentagon centre h² | 1 P-face + 3 P*-faces | 2μ − 2; (5/4 + 3√5/4)μ − 11/4 − 5√5/4 | emergence of 6 squares / 12 pentagons |
| 2 | 4/3 | 7/6 + √5/2 ≈ 2.2847 | triangle centre h² | 1 P-face + 3 P*-faces | 3μ − 4; 9/2 + 2√5 − (9/4 + 3√5/4)μ | emergence of 8 / 20 triangles |
| 3 | 3/2 | 5/4 + √5/2 ≈ 2.3680 | edge midpoint ρ² | 2 P-faces + 2 P*-faces | 2μ − 3; 25/4 + 11√5/4 − (3 + √5)μ | **jump**: 24 / 60 rhomb–rhomb bonds dissolve and as many square–triangle (pentagon–triangle) bonds emerge |
| 4 | 2 | 3/2 + √5/2 = φ² | corner R² | 3 P-faces + 1 P*-face | 2 − μ; (3 + √5)μ − 7 − 3√5 | dissolution of 12 / 30 rhombi |

Censuses along the CO–RD line:
- (1, 4/3): 6 squares and 12 hexagons, 32 corners.
- (4/3, 3/2): 6 squares, 8 triangles and 12 octagons, 48 corners.
- (3/2, 2): 6 octagons, 8 hexagons and 12 quadrilaterals, 48 corners.

Censuses along the ID–RT line:
- (h₅², h₃²): 12 pentagons and 30 hexagons, 80 corners.
- (h₃², ρ²): 12 pentagons, 20 triangles and 30 octagons, 120 corners.
- (ρ², R²): 12 decagons, 20 hexagons and 30 quadrilaterals, 120 corners.

Every quadruple concurrent at a wall was checked, not just one per orbit: 6, 8, 24, 48 quadruples for CO–RD and 12, 20, 60, 120
for ID–RT. Each determinant is linear, with its root at the wall. Euler's formula gives 2 on both sides of every wall.

**Why the walls are linear (Hopscotch Theorem, sphere case).** The 4×4 determinant det[nᵢ | −bᵢ(μ)] is linear in its last column,
and each bᵢ is either constant or proportional to μ. So every concurrency wall of every polar line is linear in μ.

**Why the walls are the flag radii.** P has a midsphere, so a P*-edge crosses its P-edge at the tangent point m. Then:
- the corner μnᵢ/hᵢ of μP* reaches face i at its centre when μ = hᵢ²;
- the crossing edges meet when μ = |m|² = ρ²;
- the plane v·x = μ reaches the corner v when μ = R².

On all three lines checked these are the only walls; the C–O line, with the cube's 1, 2, 3, fits the same rule.

**Hop, step, jump.** On each line the hand-over from P* to P is a step: P's faces emerge (h²) before P*'s faces dissolve (R²), and
for the stretch in between both are present. The single jump in the middle, at the edge midpoints, is where P*'s edges are exchanged
for P's edges.

## Bird 2: the turn

**Theorem (no turn off the regular solids).** S(μ) has faces nᵢ·x ≤ hᵢ (P) and v̂ⱼ·x ≤ μ/|vⱼ| (μP*). Its antipol has the distances
1/hᵢ and |vⱼ|/μ. For a scaled copy λS^∨ to lie on the line we need λ/hᵢ = hᵢ for every i and λ|vⱼ|/μ = ν/|vⱼ| for every j. That
means one face distance h and one corner radius R, and then ν = h²R²/μ.
- Cube: h = 1, R² = 3, so the turn is μ ↦ 3/μ.
- CO has two face distances (1 and 2/√3) and ID two (h₅ and h₃). RD and RT, read as P, have two corner radii.

So neither line has a turn. Exact checks:
- CO–RD: S^∨(μ) ≠ S(2/μ) at all 6 samples. S^∨(μ) = TO ∩ (2/μ)·RD for μ > 4/3, with TO = cube ∩ (3/2)·oct, the C–O line's turn image
  of the CO. S^∨(μ) = cube ∩ (2/μ)·RD for μ < 4/3.
- ID–RT: h₃²/h₅² = 5/6 + √5/6 ≠ 1, and the antipol inverts this ratio, so S^∨ lies on another line.

**The CO–RD walls are symmetric under μ ↦ 2/μ: a coincidence, not a turn.** R²h_sq² = 2·1 and ρ²h_tri² = (3/2)(4/3) are both 2.
Evidence that it is a coincidence:
- The mirrored hops are not related: (1, 4/3) has 32 corners and 18 faces, while (3/2, 2) has 48 corners and 26 faces.
- The foot wall 8/5 maps to 5/4, which is not an event.
- The midsphere value c = (ρ_CO/ρ_RD)² = 9/4 gives no symmetry.
- On the general line cube ∩ t·oct ∩ μ·RD the walls are 1, 2t/3, (t + 1)/2, t, symmetric only at t = 2.
- ID–RT has no such symmetry: 1.8944 × 2.6180 ≠ 2.2847 × 2.3680.

**t_min (#43's containment constant) along the lines, exact envelope.**

| line | jump wall ρ² | foot jump f | local turn μ ↦ ρ²f/μ | interior max of t_min | sup on the open line | ends t_min(P*), t_min(P) |
|---|---|---|---|---|---|---|
| C–O | 2 | 3/2 | 3/μ (= the turn) | 5 − 2√3 at √3 | 5 − 2√3 (interior) | 3, 3 |
| CO–RD | 3/2 | 8/5 | 12/(5μ) | **9 − 2√15 ≈ 1.25403 at μ = √(12/5) ≈ 1.54919** | 3/2 as μ → 1⁺ | 2, 3/2 |
| ID–RT | 5/4 + √5/2 | (38 + 14√5)/29 ≈ 2.38983 | (165 + 73√5)/(58μ) | **13 + 4√5 − 2√(55 + 24√5) ≈ 1.09571 at μ = √((165 + 73√5)/58) ≈ 2.37891** | (9 − 3√5)/2 as μ → h₅²⁺ | (5 − √5)/2, (9 − 3√5)/2 |

What the table shows:
- On every line t_min jumps down at each emergence wall, because a newborn face adds a far foot point to P(S).
- On every line its only interior maximum lies between the jump of S and the jump of S^∨. There the piece α + βμ + γ/μ takes equal
  values at both ends (5/4 and 5/4 for CO–RD; 11/8 − √5/8 twice for ID–RT), so its peak falls at the geometric mean √(ρ²f).
- At √2 (CO–RD) t_min is only 1/2 + √2/2 ≈ 1.2071.
- **Reformulated prediction:** the maximum of t_min sits at the local turn of the jump; it is the global maximum only when the line
  has a turn (regular P).

## Birds 3 and 4: golden cuts

**#89's golden rhombic cuts (s3, exact from #89 Theorem 3; y values reproduce Table 2 to 6 decimals).**
- A two-depth cut of the RD is RD ∩ c·cube ∩ t·oct. CO ∩ μ·RD is the ray t/c = 2.
  - Greater Golden Cut Rhombic Dodecahedron: t/c = 1.70640188.
  - Lesser Golden Cut Rhombic Dodecahedron: t/c = 1.62890680.
  - Both are roots of 64271z⁸ − 877416z⁷ + 4995324z⁶ − 15466824z⁵ + 28371474z⁴ − 31350456z³ + 20143404z² − 6741144z + 861111, in
    Q(√2, √3, √5).
  - So each golden RD is P_k ∩ ν·RD, with P_k = cube ∩ k·oct a truncated-octahedron-type member of the C–O line (3/2 < k < 2), not
    the CO.
- RT, with the same reading: the pentagon:triangle plane ratio over the ID's ratio is 1.09710 (Greater) and 1.13244 (Lesser), not 1.
- On the CO–RD line the octagon hop (4/3, 3/2) has corner sides 2(μ − 1) at the squares and √2(3μ − 4) at the triangles. These are
  equal only at μ = (10 + √2)/7 ≈ 1.6306, past the jump, where the rhombi are no longer octagons. **So no member of the line is
  alternating at all, golden or not.**

**Golden cuts are metric events (C–O line, exact).** Each is the root of a linear edge-ratio factor, edge ratio − φ^{±1}. The
golden division points of a moving edge scale with μ, so they lie on a fixed ray. That makes it possible to write the same factor as
the 4×4 determinant of: the fixed plane, the edge's two planes, and an auxiliary plane through the centre on the golden ray. The
auxiliary plane's normal lies outside the field of the solid's normals, so this is a metric factor in disguise (splash rule 4).
- Unborn Axes: det (1 + √5/5)μ − 2, so μ = 5/2 − √5/2 = 3 − φ, and the hexagon's remnant/corner = φ.
- Icosaxes: det (√5 − 1)μ − 2, so μ = φ, and remnant/corner = 1/φ.
- Greater Golden Cut Cube: μ = (8 + 3√2 − 2√5 − √10)/2 ≈ 2.30411.
- Lesser Golden Cut Cube: μ = (8 − 3√2 + 2√5 − √10)/2 ≈ 2.53361.
- All four determinants are linear.

The Paradigm row "#88–#91: the cuts at roots of the face-plane determinants" is wrong as stated, as the splash study also found.
The cuts are metric events, roots of linear edge-ratio factors. None of the four is a wall of S; they sit inside the hops (1, 2) and
(2, 3).

## Paragraph for the Hopscotch foundations paper

DICTO proposed that every sweep is a line of antipols, and the two second dual sweeps CO ∩ μ·RD and ID ∩ μ·RT show what this gives
when P is not regular. With P* the polar of P in the unit sphere, the face structure of S(μ) = P ∩ μP* changes exactly at the
squared flag radii of P. The faces of P emerge at μ = h², when the corners of μP* reach the face centres. At μ = ρ², the edges of μP*
cross the edges of P at their tangent points and the old bonds are exchanged for new ones in a single jump. The faces of μP*
dissolve at μ = R², on the corners of P: 1, 4/3, 3/2, 2 for the cuboctahedron and 1 + 2√5/5, 7/6 + √5/2, 5/4 + √5/2, φ² for the
icosidodecahedron, each the root of a 4×4 concurrency determinant that is linear in μ because only its last column moves. The whole
line is a step: P's faces emerge before P*'s dissolve. A turn exists only when the antipol maps the line to itself, which needs
every face at one distance and every corner at one radius. The cube–octahedron line has one, μ ↦ 3/μ; these two lines do not. What
survives is a local turn at the jump: the containment constant t_min has its only interior maximum at the geometric mean of the
jump wall and the antipol's own jump (√(12/5) for the cuboctahedron, where t_min = 9 − 2√15), and on the cube–octahedron line this
local turn is the turn itself, √3. The events are of three types. Incidence events are the walls and the antipol's walls, in the field of the normals. Metric events
are roots of linear length factors: the Dehn invariant of CO ∩ μ·RD is 24√2(3μ − 5)·arccos(1/√3) on its last hop, and so vanishes
at exactly μ = 5/3, and the golden cuts are roots of edge-ratio factors inside a hop. Stationary events are the maxima of t_min. The
golden cuts of the rhombic dodecahedron and triacontahedron need two metric factors to vanish at once, and on these lines the two
factors never share a root.

## LEADS

1. Prove that the flag radii are the only walls for every P with a midsphere. The proof needs the order h² ≤ ρ² ≤ R² and the absence
   of cross-incidences. Then predict the D·I and T·T lines of #91 (D·I: h_D², ρ_D², R_D²) and check them with s1/s2's walker.
2. Find a closed form for the foot jump f and the local turn ρ²f (12/5 and (165 + 73√5)/58). Is t_min's equal-ends property at
   [ρ², f] a consequence of (B) being symmetric under S ↔ S^∨?
3. Two-parameter plane RD ∩ c·cube ∩ t·oct: the golden rhombic cuts lie on the alternating line through the RD. Map the walls of this
   plane, which are lines in (c, t), and place #89's cuts as golden stations of a polar line in it (the two-depth analogue of bird 4).
4. The golden one-factor stations of both octagon hops are now listed (s4). Still open: is any of them a named solid?
5. The antipol pairs CO ∩ μ·RD with TO ∩ (2/μ)·RD: study the TO–RD line as the second square of the same antipol.
6. #49 Archimedean stretches stay open as #49's own question (listing plus prior art). They are not stations of symmetric lines.

## Ready Concordance ledger lines

```json
{"question": "Hopscotch: walls and turn of the second dual sweeps CO ∩ mu RD and ID ∩ mu RT", "method": "exact Q(sqrt2)/Q(sqrt5) polar-line walker (corners affine in mu, next wall = least root), all concurrent quadruples' 4x4 determinants, foot walls of the antipol, exact t_min envelope; known case C-O reproduced (studies/2026-11-09-dual-sweeps)", "status": "SETTLED", "result": "walls = squared flag radii of P: CO-RD 1, 4/3, 3/2, 2; ID-RT 1+2sqrt5/5, 7/6+sqrt5/2, 5/4+sqrt5/2, phi^2; every det linear; kinds emergence, emergence, jump (edge midpoints), dissolution; line = step. NO turn: antipol keeps P cap mu P* on its line iff P has one face distance and one corner radius (regular); CO-RD 2/mu wall symmetry is a coincidence (R^2 h_sq^2 = rho^2 h_tri^2 = 2). t_min interior max at the local turn sqrt(rho^2 f) (f = antipol's jump): CO-RD 9-2sqrt15 at sqrt(12/5), ID-RT at sqrt((165+73sqrt5)/58); on C-O this is the turn sqrt3. C-O line: 3/2 is a foot wall, not a wall of S", "retry": "never; only LEAD 1 (proof that flag radii are the only walls) or LEAD 2 (closed form of the local turn)", "study": "studies/2026-11-09-dual-sweeps", "date": "2026-11-09"}
{"question": "#89 golden rhombic cuts on the second dual sweeps (ranked gap: 'must sit on these sweeps')", "method": "exact sympy from #89 Theorem 3 closed forms (Table 2 reproduced); plane-ratio test against CO cap mu RD and ID cap mu RT (studies/2026-11-09-dual-sweeps s3_golden.py)", "status": "SETTLED", "result": "NOT on the sweeps: RD/RT have two corner orbits, cuts form a plane, the sweep is one ray in it. GCRD at t/c = 1.70640 (Greater), 1.62891 (Lesser) vs 2 (degree-8 roots); GCRT ratio factor 1.09710, 1.13244 vs 1. CO-RD octagon hop never alternating (equal corner sides only at (10+sqrt2)/7, past the jump). Gap premise corrected: #91's theorem covers regular P only", "retry": "never; only LEAD 3 (walls of the two-depth plane)", "study": "studies/2026-11-09-dual-sweeps", "date": "2026-11-09"}
{"question": "Hopscotch golden-cuts row (#88-#91): golden cuts as walls of S(mu) = P cap mu P*", "method": "exact sympy on the cube-octahedron line: 4x4 determinants with the golden ray of the moving edge (studies/2026-11-09-dual-sweeps s3_golden.py)", "status": "SETTLED", "result": "METRIC, not incidence (agrees with splash-determinants rule 4): golden cuts sit inside hops as roots of linear edge-ratio factors (Unborn Axes 3-phi, Icosaxes phi, Golden Cut Cubes (8 ± (3sqrt2 - 2sqrt5) - sqrt10)/2, matching splash sweep-events.json); a 4x4 form exists only with an auxiliary golden-ray plane outside the normal field. #89 rhombic cuts need two metric factors at once; the equal-corner factor has no root in the octagon hop of CO-RD or ID-RT", "retry": "never; only the D-I and T-T lines (LEAD 1) for completeness", "study": "studies/2026-11-09-dual-sweeps", "date": "2026-11-09"}
{"question": "#49 Archimedean stretches as stations of the second dual sweeps", "method": "symmetry argument (members have full O_h / I_h; a segment stretch keeps only its axis stabiliser)", "status": "SETTLED", "result": "NO; only the cuboctahedron (#49's tetrahedron with four caps, not a segment stretch) appears: end mu = 2 of CO-RD and jump wall of C-O", "retry": "never (the stretch listing stays #49's own open question)", "study": "studies/2026-11-09-dual-sweeps", "date": "2026-11-09"}
{"question": "2026-11-04 co-rd-sweep LEAD 3: why Q4 is constant on (3/2, 2)", "method": "algebra: corners are images of (1, mu-1, 2-mu) with x = y+z; identity (y+z)^4 + y^4 + z^4 = 2(y^2+yz+z^2)^2", "status": "SETTLED", "result": "sum x^4/|x|^4 = 1/2 for every corner, as for the CO's (1,1,0); so Q4 = CO's value 0.1909 on the whole hop", "retry": "never", "study": "studies/2026-11-09-dual-sweeps", "date": "2026-11-09"}
{"question": "splash-determinants prediction: CO ∩ mu RD has a Dehn factor linear in mu with root exactly 5/3; Dehn of ID ∩ mu RT", "method": "exact edge lengths per hop (sweeplib, reusing splash corrd_events.py planes), dihedral angles reduced mod pi Q by PSLQ (60 digits, checked 1e-50) (studies/2026-11-09-dual-sweeps s4_metric_events.py)", "status": "SETTLED", "result": "CONFIRMED: Dehn = 24sqrt2(3mu-5) theta on (3/2,2), theta = arccos(1/sqrt3), root 5/3 (oct-rhomb minus cube-oct total edge length); 0 identically on [1,4/3]; 24sqrt2(3mu-4) theta on (4/3,3/2). ID-RT: two angle classes, component roots never coincide inside a hop: no Dehn zero on the open line", "retry": "never", "study": "studies/2026-11-09-dual-sweeps", "date": "2026-11-09"}
```

## Sources checked

- papers/polar-line-outline/paper.html (§0–5).
- papers/dicto-concordance/ledger-digest.txt (59 lines); ledger.entries[15] and [41] opened.
- studies/2026-11-04-co-rd-sweep (README, log, script).
- studies/2026-11-09-hopscotch-rows/README.md.
- papers/golden-cuts-beyond-plato (#89: abstract, §4, §5 Theorem 3, Table 2).
- papers/dual-pairs-dimensions (#91: abstract, introduction).
- papers/six-dimensions-golden-cubes (#90: abstract, §2).
- papers/2026-10-22-swept-dodecahedra (#49: lead, §§ on the Platonic stretches, open questions).

Reference library not searched. The tools used here (polar bodies, flags, the midsphere of quasi-regular solids) are textbook. The
flag-radius statement for P ∩ μP* was not looked up in the literature; check prior art before paper text (Zefiro's cuts of the
cubic Archimedean solids by the RD, cited in #89, are the nearest known source).

DICTO · dictospheres.com
