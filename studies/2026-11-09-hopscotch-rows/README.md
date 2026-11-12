# The DICTO Hopscotch: two rows verified (hyperboloid/projective row #103, sphere row #43/#81), study 2026-11-09

**Row 1 (projective, #103 viewpoint principle): PROVED-FROM-FRAMEWORK.** The viewpoints are exactly the automorphisms of the circle
fixing O and T; u·v is the cross-ratio (P, Q; T, O) on the circle; Kulaichev's (d) is one wall, linear in β, with exactly one root
for every yantra: β\* = −(height of the bindu's hyperbolic incentre). The turn is β ↦ −β (fixed point β = 0); it comes from the
half-turn, not from the polarity (the polarity commutes with every viewpoint).

**Row 2 (sphere, #43 constants and #81 core turn): PROVED-FROM-FRAMEWORK for Theorem 1, Theorem 4, Corollary 7 (9, 3, 3) and the
core turn. FITS-BUT-NOT-DERIVED for Theorem 2 (15 − 6√5) by the orbit-moment route:** the bilinear form takes it to a covering
bound, but icosahedral orbit moments (5-designs) give only 5/3. The constant needs the bilinear vertex lemma on the Möbius triangle
(already proved exactly in 2026-11-08-octahedral-constant), which works on cones of the same bilinear form, not on moments.

Framework, names and the prediction of a common denominator: DICTO (the Hopscotch, antipol, hop, step, jump, the turn, emergence,
dissolution; outline papers/polar-line-outline). Classical tools used: Klein's model of the hyperbolic plane, the projective geometry
of conics (cross-ratio on a conic, pole and polar), polar bodies and the bipolar theorem, spherical designs (Delsarte–Goethals–Seidel).

Ledger: the 57 entries have no attempt on either row (entries 44 and 52/55 touch #43, on Conjectures 2 and 1, not on these
derivations). Nothing here retries an earlier attempt.

Scripts (all on compute-host, python3, sympy 1.14; each under 2 min; logs in data/; every one ends FINAL ok):
scripts/row1_group.py (data/row1_group.log), scripts/row1_wall.py (data/row1_wall.log), scripts/row2_sphere.py (data/row2_sphere.log).
Input copies: data/kites.json, viewpoint.json, golden_family.json (from studies/2026-11-08-sri-yantra/figures, 40 digits).

## Row 1: the projective row (#103, Theorem 5)

Quadric: the yantra's circle, homogeneous X = (x, y, w), J = diag(1, 1, −1). O = (0, 1, 1), T = (0, −1, 1) are null; the axis x = 0
is the polar of E1 = (1, 0, 0), the point at infinity across the axis.

**(a) The viewpoints are exactly the circle's automorphisms fixing O and T.** Let M keep the circle (MᵀJM = J after scaling; the
scale is positive since J has signature (2, 1)) and fix O and T: MO = aO, MT = bT. The J-orthogonal complement of {O, T} is the line
of E1 (exact), so ME1 = cE1 with c² = 1, and ⟨MO, MT⟩ = ab⟨O, T⟩ = −2ab forces ab = 1. In the basis (E1, O, T), M = diag(c, a, 1/a).
Back in x, y (exact): x′ = c·2ax/(a² + 1 + (a² − 1)y), y′ = ((a² + 1)y + a² − 1)/(a² + 1 + (a² − 1)y), which is T_β with
β = (a² − 1)/(a² + 1), times the mirror x ↦ cx. So the group is {T_β} × {x ↦ ±x}; adding the half-turn y ↦ −y (O ↔ T) gives the
whole stabiliser of the axis. The multiplier of T_β at O is a = λ = √((1 + β)/(1 − β)) = e^θ (θ = artanh β, the hyperbolic length of
the step), at T it is 1/λ. Checked: MᵀJM = J for both signs c; the circle is kept; T_β commutes with the polarity X ↦ JX.

**(b) u·v is the cross-ratio (P, Q; T, O).** Give the circle its own coordinate z = x/(1 − y) = (1 + y)/x (the slope of the line
from O; z(O) = ∞, z(T) = 0). On the circle the slope from T is 1/z. An upper great leg of slope u (through O) meets the circle at
P with z_P = u; a lower leg of slope v (through T) meets it at Q with z_Q = 1/v. Then
  (P, Q; T, O) = (z_P − 0)(z_Q − ∞)/((z_P − ∞)(z_Q − 0)) = z_P/z_Q = u·v.
T_β acts on the circle as z ↦ λz (exact), which fixes 0 and ∞; so u ↦ λu, v ↦ v/λ, and the cross-ratio is kept. That is why u·v
is the invariant: it is the only invariant of a pair of points on a conic under the automorphisms fixing two further points.
Corollary: u·v = 1 exactly when the two legs meet on the circle (P = Q), checked exactly.

**Direction.** u ↦ λu (upper slope), v ↦ v/λ (lower), λ = √((1 + β)/(1 − β)), as in #103 Theorem 5. Checked against the computed
V1: K1 at β = −0.0405464286 (λ = 0.9602432222) gives λ·(2/φ²) = 0.733560546821 and (1/√2)/λ = 0.736382996355, the published V1
slopes. **The sri-yantra study README (line 175, "u -> u/lambda, v -> v*lambda") and the docstring of its viewpoint.py still have
the direction backwards;** the paper is right. Not changed here (not this study's file).

**(c) Kulaichev's (d) is ONE wall on the β-line, linear in β.** T_β sends p_β = (0, −β) to the centre. In Klein's model a Euclidean
circle about the centre is a hyperbolic circle about the centre, so the image of the bindu has its incircle centred exactly when
the bindu's hyperbolic incircle (in the yantra's own circle) is centred at p_β. With unit lines l̂ = l/√(lᵀJl), oriented positive
inside, the hyperbolic incentre lies on the bisector m = l̂_base − l̂_leg, and the wall is the single equation
  W(β) = m · (0, −β, 1) = m_w − β m_y = 0,   β\* = m_w/m_y,
linear in β (one root, exact). For a bindu with apex (0, a), base y = b, base half-width c, leg L = √((a − b)² + c²):
  y_H = (c a √(1 − b²) + b √(L² − c²a²)) / (c √(1 − b²) + √(L² − c²a²)),   β\* = −y_H,
the Euclidean incentre height y_E = (ca + Lb)/(c + L) with c ↦ c√(1 − b²) and L ↦ √(L² − c²a²) (identical to the bisector root,
checked symbolically). Since a hyperbolic triangle has exactly one incentre and it lies on the axis inside the disc, **every
symmetric yantra has exactly one viewpoint that centres its bindu** (#103 says only that the incircle moves, "which is how (d) can
be won"). Checks (40-digit data):
- K1: β\* = −0.0405464286398567528042933305097, equal to viewpoint.py's root to 30 digits; T_β\* centres the Euclidean incircle (< 10⁻³⁵).
- V1 and GF1 (the DICTO Yantra, bindu already centred): β\* = 0 (4.6·10⁻⁴¹, 4.2·10⁻⁴¹).
- GF1 undone by T_{−β} with β = (λ² − 1)/(λ² + 1), λ = u/(2/φ²): the preimage has great slopes 2/φ² and 1/φ to 30 digits (the Cleo-Icos
  and the Antonius side) and its wall is β\* = −0.11685233666123018165 = β_GF (#103 §9.1 gives −0.11685).
- 200 random symmetric bindus: T_β\* centres the incircle (< 10⁻⁴⁰); on a 399-point grid of (−1, 1) the Euclidean incentre height
  changes sign exactly once.

**The turn of this line.** The β-line is the one-parameter group T_β (additive in θ = artanh β), running from wall to wall between
β = −1 and β = 1, where the view degenerates onto O or T. Conjugation by the half-turn R (y ↦ −y) gives R T_β R = T_{−β} (exact):
the turn is β ↦ −β, λ ↦ 1/λ, with fixed point β = 0, the frontal view; the return visits the mirrored yantra (O and T exchanged,
u and v exchanged). On the slope hyperbola u·v = p (one orbit) the turn point is u = v = √p: **equal great triangles, Kulaichev's
fourth condition, is the turn of its orbit.** The DICTO Yantra sits off the turn (u = 0.6793, v = 0.6950, √(v/u) = 1.0115); its
fourth condition, the Cleo-Antonius product 2/φ³, chooses the orbit, and the wall (d) chooses the point on it.
What does not fit the sphere-row pattern: the circle's polarity commutes with every T_β, so it does not move along the line; its
fixed points on the axis (y ↦ 1/y) are O and T, the two ends of the line, not its middle. The turn here is a group symmetry.

## Row 2: the sphere row (#43, #81)

Antipol: S = {nᵢ·x ≤ hᵢ} (unit normals), S^∨ = {nᵢ·x ≤ 1/hᵢ} (same normals, inverted distances). P(S) = conv(hᵢnᵢ) has polar S^∨
(each foot point hᵢnᵢ gives the inequality nᵢ·y ≤ 1/hᵢ). The gauge of a body is the support function of its polar, so
  (B)  t_min(S) = max_{x ∈ S} gauge_{P(S)}(x) = max_{x ∈ S, y ∈ S^∨} x·y,
the bilinear form of the sphere's polarity on the antipol (S, S^∨), attained at a corner pair (Proposition C of
2026-11-08-octahedral-constant). Checked on 300 random polytopes against the direct gauge computation (largest gap 5.5·10⁻¹²).

**#43 Theorem 1 from (B).** Lower bound: for a corner v put y = v/h_P(v); then nᵢ·y ≤ 1/hᵢ ⇔ hᵢnᵢ·v ≤ h_P(v), so y ∈ S^∨ and
x·y = |v|²/h_P(v) ≤ t_min (the test pair with y parallel to x). Upper bounds: Cauchy–Schwarz, x·y ≤ R(S)·R(S^∨), and
R(S^∨) = 1/r(P(S)) (polar radii), giving t_min ≤ R(S)/r(P(S)). Last step: for y = s w ∈ S^∨ (|w| = 1) let tw be the boundary point
of S on that ray, on face i; then nᵢ·w = hᵢ/t and s nᵢ·w ≤ 1/hᵢ give s ≤ t/hᵢ² ≤ R/r², so R(S^∨) ≤ R/r² and t_min ≤ (R/r)².
Equality for the Platonic solids: one face distance h, so S^∨ = S/h² and max x·y = R²/h² at x = y. Exact: tetrahedron 9, cube 3,
octahedron 3, dodecahedron and icosahedron 15 − 6√5. #43's Lemma A (og-margin) is (B) maximised over x first:
t_min = max_{y ∈ S^∨} h_S(y) = max_u h_S(u)/h_P(u), since the boundary point of S^∨ on the ray u is u/h_P(u). Lemma G (og-gnomon)
is the pairing of a foot point of P(S) with the foot point of the matching face of S^∨: (hᵢnᵢ)·(nᵢ/hᵢ) = 1, so h_P(nᵢ) ≥ hᵢ.

**Theorem 4 and Corollary 7 from (B) plus the orbit moments.** For G-symmetric S (G a rotation group), S contains the orbit of a
farthest corner v, so every face distance is h ≥ R·min_{u,w} max_g (gu)·w =: R·c, and (B) with Cauchy–Schwarz gives t_min ≤ 1/c².
The moments of t_g = (gu)·w over a generic orbit (exact, symbolic u, w): T and T_d orbits are 2-designs, T_h and O are 3-designs,
I is a 5-design (degree 6 fails). Certificates (exact means):
- 2-design: mean of (m − t)(1 + t) = m − 1/3, so m ≥ 1/3: constant 9 (tetrahedral; sharp, tetrahedron).
- 3-design: mean of (t − m)(t + 1/(3m))² = (1 − 3m²)/(9m), so m ≥ 1/√3: constant 3 (octahedral, pyritohedral; sharp, cube, octahedron).
- 5-design: mean of (t − m)(t + m)²t² = m/5 − m³/3, so m ≥ √(3/5): constant 5/3 only.
**Theorem 2 does not follow from moments:** 5/3 > 15 − 6√5 ≈ 1.5836 (exact). The icosahedral constant c² = (5 + 2√5)/15 comes from
the bilinear vertex lemma on the (2, 3, 5) Möbius triangle (the three-mirror average, nine generator pairs, exact in
2026-11-08-octahedral-constant/sanity_icosahedral.py) or #43's kite. Both are statements about the same bilinear form on cones, so
the row fits; the moment half of the claimed derivation does not reach it.

**#81 core turn μ ↦ 3/μ as the turn of the cube–octahedron line.** P_μ = [−1, 1]³ ∩ {|x| + |y| + |z| ≤ μ}: normals eᵢ (|N|² = 1,
d = 1) and (±1, ±1, ±1) (|N|² = 3, d = μ); inversion d ↦ |N|²/d gives exactly P_μ^∨ = P_{3/μ}. So the antipol of a square of the
line is another square of the line, and the turn is μ ↦ 3/μ. Its fixed point: S^∨ = S ⇔ every face at unit distance ⇔ every face
tangent to the reference sphere, μ = √3 (exact). At a self-antipol (B) gives t_min = max_{x,y ∈ S} x·y = R² = (R/r)² (r = 1); for
P_√3, 5 − 2√3 (exact): Theorem 1's upper bound is attained exactly at the turn. The walls are concurrency determinants, linear in μ:
x = 1, y = 1, x + y + z = μ, x + y − z = μ gives det = −2(μ − 2) (the square faces vanish, cuboctahedron); x = 1 with three octahedron
planes gives 4(μ − 1) (octahedron end). The turn sends the walls 1, 2 to 3, 3/2 (the same events on S^∨). Closed form, symmetric
under the turn by sight:
  t_min(P_μ) = min(μ, 3/μ, 5 − s),  s = μ + 3/μ the turn-invariant coordinate  (1 < μ < 3),
checked exactly at 43 rational μ by full corner enumeration; 5 − s ≤ 5 − 2√3 with equality only at √3, since
s − 2√3 = (μ − √3)²/μ (AM–GM in s). The turn's fixed point maximises t_min on this line. (#43 Theorem 3, reciprocation sending
Universal PiTet beat k to beat 5 − k, is the same kind of turn on the beat line, fixed point k = 5/2 between GTI and FPD; not
re-derived here.)

## The two paragraphs for the foundations paper

**Projective row.** DICTO proposed the viewpoint, and the Hopscotch places it. Take the yantra's circle as the quadric. The
viewpoints of #103 are exactly the projective maps that keep the circle and fix its two axis points O and T, the translations of
Klein's model along the axis, T_β with multiplier λ = √((1 + β)/(1 − β)) at O and 1/λ at T. On the circle's own coordinate z (the
slope seen from O) T_β is z ↦ λz, so the upper slope goes to λu and the lower slope to v/λ, and u·v, the cross-ratio of the two
corners P and Q with T and O, cannot change. The one condition a viewpoint can alter, the bindu's incircle being centred, is a
single wall on the β-line and is linear in β: since T_β carries (0, −β) to the centre, and a circle about the centre is the same for
Euclid and for Klein, the wall is β = −y_H, where y_H is the height of the bindu's hyperbolic incentre. Every symmetric yantra
therefore has exactly one centring viewpoint. The turn of the line is β ↦ −β, the yantra turned over, with the frontal view as its
fixed point; on each orbit u·v = p it falls at u = v, Kulaichev's equal great triangles.

**Sphere row.** For a solid S with faces nᵢ·x ≤ hᵢ, DICTO's antipol pairs S with S^∨, the solid with the same normals and inverted
distances 1/hᵢ, the polar of the foot-point hull P(S). The containment constant is then the bilinear form of the sphere's polarity
on the antipol, t_min(S) = max x·y over x ∈ S and y ∈ S^∨. #43's Theorem 1 is this form under Cauchy–Schwarz (upper bounds) and on a
pair with y parallel to x (lower bound), with equality 9, 3, 3, 15 − 6√5, 15 − 6√5 for the Platonic solids, where S^∨ is S scaled.
With the moments of a symmetry orbit it gives the octahedral and pyritohedral constant 3 (3-designs) and the tetrahedral constant 9
(2-designs); the icosahedral constant 15 − 6√5 needs the same bilinear form on the cones of the Möbius triangle, since moments alone
give 5/3. On the cube–octahedron line P_μ the antipol of P_μ is P_{3/μ}: #81's core turn μ ↦ 3/μ is the turn of the line, its fixed
point √3 the solid whose faces all touch the sphere, where t_min = R² = 5 − 2√3 is largest, and t_min = min(μ, 3/μ, 5 − μ − 3/μ)
reads the same from either end.

## LEADS 4 and 5 worked (12 Nov 2026; scripts/lead4_cert.py, scripts/lead5_exact.py, logs data/lead4_cert.log, data/lead5_exact.log, both FINAL ok)

**LEAD 4 CONCLUSION (12 Nov 2026): CLOSED EXACTLY; the degree-6 harmonic is a cubic in (x², y², z²) whose critical points are found over Q(√5), so 15 − 6√5 follows from moments plus one harmonic with no numerical step (scripts/lead4_range.py, FINAL ok).**

**LEAD 4: the icosahedral constant from moments plus one invariant harmonic. CLOSED (exact, every step).**
Certificate p(t) = (t − c)(t + c)²(t² − c′²)², degree 7, where ±c, ±c′ (c² = (5 + 2√5)/15, c′² = (5 − 2√5)/15) are the only inner
products between the orbit of a five-fold axis (the 12 icosahedron vertices) and a three-fold axis. p ≤ 0 on [−1, c]. Its mean over
an I-orbit, for unit u, w, uses the 5-design property, the vanishing degree-7 harmonic part (exact) and the degree-6 invariant
harmonic h(u, w) = mean_g ((gu)·w)⁶ − 1/7:  mean p = A + p₆ h(u, w), A = 4(√30 + 5√6)√(5 + √5)/14175, p₆ > 0.
Exact: h has rank one (28 × 28 coefficient matrix, rank 1), h = Φ(u)Φ(w)/Φ(x₀); mean p = 0 at the extremal pair, where
h = −16/945; Φ at the five-fold axis 16/21 + 32√5/105, at the three-fold axis −80/189 − 32√5/189.
These two axis values are the maximum and minimum of Φ on the sphere (first checked numerically, 400 000 points; now PROVED, below),
so h ≥ −16/945 everywhere and mean p ≥ 0 for all unit u, w. Hence max_g (gu)·w ≥ c for every pair, c is attained, and the
constant is 1/c² = 15 − 6√5 (#43 Theorem 2) by the moment route.
**The range step, exact (scripts/lead4_range.py, 42 checks, FINAL ok, 21 s).** (i) Exact polynomial identities over Q(√5):
H(x₀, x₀)·H(u, w) = Φ(u)Φ(w) with H(x₀, x₀) = 240/7 + 320√5/21 (rank one as an identity), and Φ = √5·f6 − (5 + 2√5)/21·|u|⁶ with
f6 = (y² − φ²z²)(z² − φ²x²)(x² − φ²y²), the product of the six planes normal to the five-fold axes. (ii) f6 = F(x², y², z²) with F
the cubic (Y − φ²Z)(Z − φ²X)(X − φ²Y), so the range of Φ on the sphere is the range of F on the triangle X + Y + Z = 1, X, Y, Z ≥ 0.
(iii) Extremes of F there sit at a vertex, an edge critical point or an interior critical point. Vertices: F = 0. Each edge: F′ is a
quadratic that splits over Q(√5), roots (5 ± √5)/10-type and (3 ± √5)/6-type, values F₅ = (2 + √5)/5 and F₃ = −(2 + √5)/27. Interior:
the resultant of ∂F/∂X, ∂F/∂Y (after Z = 1 − X − Y) is a nonzero quartic that splits into the four linear factors X = 1/3, 1/4,
(3 ± √5)/8; a gcd gives one Y each: the centre (F₃) and the three two-fold points (F = 0). Every candidate value lies in [F₃, F₅],
compared exactly in Q(√5); so Φ ranges exactly over [−80/189 − 32√5/189, 16/21 + 32√5/105] and min h = Φ_min·Φ_max/H(x₀, x₀) =
−16/945. (iv) The last link also made exact: if max_g (gu)·w < c, every t_g is a zero of p below c, in {−c, c′, −c′}, and no
weights on these three values match the orbit moments of degree 0 to 5 (exact solve: none).
Controls: POSITIVE, the octahedral x⁴ + y⁴ + z⁴ (F = X² + Y² + Z²) gives the known range [1/3, 1]; with c allowed the moment solve
returns the extremal orbit (weights 1/4 on ±c, ±c′); COUNT, the candidates lift to 12 + 20 + 30 = 62 sphere points, the five-fold
value on exactly 12, the three-fold value on exactly 20; NEGATIVE, a two-fold maximum is refuted (F₅ > 0), dropping the edges loses
the maximum (interior only gives F₃ and 0), and f6 built with 8/5 in place of φ cannot represent Φ.
Controls: POSITIVE, the tetrahedral group with its degree-3 invariant (xyz) gives by the same construction c = 1/3, constant 9,
with the range of xyz exact (AM–GM); NEGATIVE, treating the I-orbit as a 6-design (h = 0) contradicts the exact orbit mean at the
extremal pair (A ≠ 0), so the harmonic term is essential; moments up to degree 5 give only √(3/5) < c. Sanity: 20 000 random unit
pairs never go below c.

**LEAD 5: the icosahedral two-family line. YES, the turn's fixed point maximises t_min, with the same closed form shape.**
S_λ = {a·x ≤ 1 (12 unit five-fold normals, dodecahedron faces), b·x ≤ λ (20 unit three-fold normals, icosahedron faces)}; inverting
the distances gives S_λ^∨ = S_{1/λ}, so the turn is λ ↦ 1/λ with fixed point λ = 1 (every face tangent to the unit sphere). The line
runs from the icosahedron (λ = 1/ρ) to the dodecahedron (λ = ρ), ρ² = 15 − 6√5. Wall (four-plane determinant, linear in λ): the
icosidodecahedron at λ_w = √(30 + 6√5)/6 ≈ 1.0982, its turn image 1/λ_w the same event on S^∨. Exact closed form
  t_min(S_λ) = min(ρλ, ρ/λ, 10 − √5 − 3λ_w·s),  s = λ + 1/λ,
checked exactly at 22 rational λ across the line, each against the maximum of all 3600 corner pairs (the 60 corners are one
I-orbit in each chamber). The middle piece is linear in s, so t(1) − t(λ) = 3λ_w(s − 2) ≥ 0 (AM–GM) for every λ: the maximum is
exactly at the fixed point, t_min = 10 − √5 − √(30 + 6√5) = R² of the self-antipol S_1, as on the cube–octahedron line
(min(μ, 3/μ, 5 − s)). Controls: the corner types checked on both sides of the wall; the ends meet the middle piece exactly at the walls.

## LEADS

1. Correct the direction in studies/2026-11-08-sri-yantra/README.md (line 175) and viewpoint.py's docstring: u → λu, v → v/λ
   (one-word fix each; the paper is right).
2. #103: the uniqueness statement "every symmetric yantra has exactly one centring viewpoint, β\* = −y_H" can go into Theorem 5 or a
   remark; destination: a #103 version line (DICTO's choice where).
3. Kulaichev's equal great triangles = the turn of its viewpoint orbit: is there a yantra meeting (b), (c), (d) AND sitting at the
   turn (u = v) besides Kulaichev's own? (Kulaichev = equal slopes + (b) + (c), (d) then holds to 10⁻²⁵⁵ per #103.)
4. [CLOSED EXACTLY 12 Nov, see above; range step proved in scripts/lead4_range.py] Icosahedral constant from the framework: find the degree-6 certificate (I's first invariant harmonic) that closes 5/3 → 15 − 6√5,
   so the moment route covers all three constants (same as octahedral-constant LEAD 4).
5. [WORKED 12 Nov, see above: yes, exact] The outline's prediction "the fixed point of a polar turn maximises t_min": on the C–O line it follows from s = μ + 3/μ ≥ 2√3; test
   the icosahedral two-family line (dodecahedron ∩ μ·icosahedron, turn μ ↦ c/μ) for the same closed form min(·, ·, a − b·s).
6. #43 Theorem 3 (beat k ↔ 5 − k) as the turn of the Universal PiTet line, fixed point k = 5/2: write it as a row of the table.
7. Projective row and the outline's yantra prediction ("the yantra's conditions are walls of one determinant family"): (d) is now a
   linear wall in β; (b) and (c) are walls in the slope plane; the next step is to write (b), (c) as determinants in (u, v) on one orbit.

## Ready Concordance ledger lines

```json
{"question": "Hopscotch projective row: #103 viewpoint principle and invariant u·v derived from the framework", "method": "exact sympy: automorphisms of the circle fixing O,T; cross-ratio on the conic; bindu wall as hyperbolic incentre (40-digit K1, V1, GF1, 200 random bindus) (studies/2026-11-09-hopscotch-rows)", "status": "SETTLED", "result": "PROVED-FROM-FRAMEWORK: viewpoints = circle automorphisms fixing O,T (times x->-x); u v = cross-ratio (P,Q;T,O); u -> lambda u, v -> v/lambda (sri-yantra README has it backwards); (d) is one wall linear in beta, beta* = -y_H (hyperbolic incentre), exactly one centring viewpoint for every yantra; turn beta -> -beta from the half-turn, not the polarity; equal great triangles = the turn of an orbit", "retry": "never; only lead 3 (yantra at the turn) or lead 7 ((b),(c) as determinants)", "study": "studies/2026-11-09-hopscotch-rows", "date": "2026-11-09"}
{"question": "Hopscotch sphere row: #43 containment constants and #81 core turn from the bilinear form t_min = max x.y over S x S^v", "method": "exact sympy (Platonic, orbit moments of T,T_h,O,I, P_mu corners at 43 rational mu, wall determinants) + float (300 random polytopes) (studies/2026-11-09-hopscotch-rows)", "status": "SETTLED", "result": "PROVED-FROM-FRAMEWORK: Theorem 1 (Cauchy-Schwarz + parallel pair), Theorem 4 and Corollary 7 (3-designs -> 3, 2-designs -> 9), Lemma A and Lemma G as readings of the form, core turn (P_mu^v = P_3/mu, fixed point sqrt3 = all faces tangent, t_min = R^2 = 5-2sqrt3, t_min = min(mu, 3/mu, 5-mu-3/mu), walls linear det at 1, 3/2, 2, 3). FITS-BUT-NOT-DERIVED by moments: Theorem 2 (I orbits are 5-designs, moments give only 5/3 > 15-6sqrt5; needs the bilinear vertex lemma on the Mobius triangle)", "retry": "only a degree-6 moment certificate for 15-6sqrt5, or the icosahedral two-family line", "study": "studies/2026-11-09-hopscotch-rows", "date": "2026-11-09"}
```

## Sources checked

papers/polar-line-outline/paper.html (§0–5); papers/dicto-concordance/ledger-digest.txt (57 entries); papers/2026-11-08-dicto-yantra
/paper.html (§5 Theorem 5, §9.1–9.2, Table 3); studies/2026-11-08-sri-yantra (README viewpoint, Cleo-Antonius and E1 notes; scripts
/viewpoint.py; figures/kites.json, viewpoint.json, golden_family.json); papers/2026-10-21-kyushindo-cores/paper.html v2 (Theorems 1–4,
Corollaries 1, 7, Lemma 3); studies/2026-11-08-octahedral-constant (README, logs: all FINAL ok); studies/2026-11-09-og-margin (Lemma A);
studies/2026-11-09-og-gnomon (Lemma G). Reference library not searched for this study: the classical tools named above are textbook
(Klein model; cross-ratio on a conic; bipolar theorem; Delsarte–Goethals–Seidel 1977 for designs, cited from memory as in the
octahedral-constant study, to check before paper text).

DICTO · dictospheres.com
