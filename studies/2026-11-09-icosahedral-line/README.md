# The DICTO Hopscotch: the icosahedral line (boulder 2), study 2026-11-09

**Bird 1 (degree-6 certificate for 15 − 6√5): PROVED-FROM-FRAMEWORK.** The icosahedral constant now follows from orbit moments,
like 9 and 3. The certificate has degree 7, p(t) = (t − c)(t + c)²(t² − a²)², and it reads the degree-6 icosahedral harmonic H.
No polynomial of degree ≤ 6 can reach c (proved; the best degree-6 bound is 1.6290). Status: exact, all checks FINAL ok.

**Bird 2 (New-Face Lemma, #43 Conjecture 1): BASE EXACT, LEMMA OPEN.** (r(D_12) = 1.179354549 vs need 1.084154, exact.) r(D_12) and the recovery r(D_9) < r(D_10) < r(D_11) < r(D_12)
on the five-fold faces are now exact, and so is r(D_12) ≥ (φ²/3)·R(D_11). So Theorem N rests only on the new faces of D_j, j ≥ 13.
The invariant-polynomial certificates cannot prove the lemma: one orbit of normals covers only to the factor c = 0.7947, and the
lemma needs 0.92. Status: REDUCED, as before, with the base now exact.

**Bird 3 (turn on the dodecahedron–icosahedron line): PROVED.** The antipol of S_μ is S_{1/μ}, and the turn μ ↦ 1/μ has its fixed
point at μ = 1, where every face touches the sphere. The closed form is t_min = min(μ/c, 1/(cμ), 10 − √5 − √κ₀·(μ + 1/μ)) with
κ₀ = (15 + 3√5)/2. Its maximum 10 − √5 − √(30 + 6√5) ≈ 1.174819 lies exactly at the turn, so the prediction "the turn maximises
t_min" holds on this line too. Status: exact, FINAL ok.

**Bird 4 (#43 Theorem 3, beat k ↔ 5 − k): PROVED-FROM-FRAMEWORK.** Lemma 3 together with P = T⁻¹ on the line gives π T π = T⁻¹, so the
polarity π reflects the beat line. Its fixed point is fixed by one fact, the GTI's corners lying on the reference sphere: then
π(GTI) = T(GTI) = FPD, which forces 5 − k. The fixed point 5/2 is the antipol GTI|FPD, and 1/2 is the antipol ID|RT one hop below.
The shell ratios agree with the prediction: the two fixed shells have the largest ratios. Status: exact, FINAL ok.

Framework, names and the idea of one common denominator: DICTO (the Hopscotch, antipol, hop, step, jump, the turn; outline
papers/polar-line-outline). This study answers boulder 2 of DICTO's "several birds with one boulder". Classical tools used: spherical
designs and the linear-programming method of Delsarte, Goethals and Seidel; invariant theory of the icosahedral group (Klein; the
Jacobian of the basic invariants of a reflection group is the product of the mirror forms, Steinberg); polar reciprocity.

Ledger: entry 58 (hopscotch-rows) has the retry "only a degree-6 moment certificate for 15 − 6√5, or the icosahedral two-family
line": birds 1 and 3 are exactly that retry. Entries 52 and 55 (#43 Conjecture 1) have the retry "only a proof of the New-Face Lemma":
bird 2 attempts it through certificates (structural failure, §2) and makes its base exact. No other entry touches these questions.

All computation ran on the large machine (python3, sympy 1.14, scipy 1.18), in the foreground, and every script ends with a
conditional FINAL line. The four scripts and their logs: scripts/bird1_certificate.py (data/bird1_certificate.log, 45 s),
scripts/bird2_base.py (data/bird2_base.log, data/bird2_base.json; pilot data/bird2_pilot.log), scripts/bird3_line.py
(data/bird3_line.log, 6 s), scripts/bird4_beats.py (data/bird4_beats.log, 2 s). Shared exact Q(√5) arithmetic and exact corners from
half-spaces: scripts/q5.py. All printed FINAL ok.

## 1. Bird 1: the icosahedral constant from moments

Setting (hopscotch-rows, sphere row): for unit u, w let t_g = (gu)·w, g in the 60 rotations I. If max_g t_g ≥ c for all u, w, then
every icosahedral polytope has r ≥ cR and t_min ≤ 1/c². #43 Theorem 2 is c² = (5 + 2√5)/15, 1/c² = 15 − 6√5.

**Orbit moments (exact, symbolic u, w; sympy over Q(√5)).**
E[t] = E[t³] = E[t⁵] = E[t⁷] = 0, E[t²] = |u|²|w|²/3, E[t⁴] = |u|⁴|w|⁴/5, and
  E[t⁶] = |u|⁶|w|⁶/7 + (175/192)·H(u)H(w),
where H(x) = Σ (a·x)⁶ − (6/7)|x|⁶ is the degree-6 icosahedral harmonic (the sum runs over the six unit five-fold axes a). This is why
the orbits are 5-designs and not 6-designs. H is harmonic and invariant under all 60 rotations (both checked exactly). No odd
moment below degree 15 survives, because I has no odd invariant harmonic below degree 15.

**The range of H (exact).** The Jacobian of (|x|², H, Q₁₀), where Q₁₀ = Σ (a·x)¹⁰, equals a nonzero constant times the product of the
15 mirror forms of I_h. So H restricted to the sphere has no critical point off the mirrors: there ∇H is not parallel to x. On a
mirror circle the critical polynomial factors exactly into the six lines of the 5-, 3- and 2-fold axes. Hence
  H(5-fold) = 32/175 = max,  H(2-fold) = −2/35,  H(3-fold) = −32/315 = min,
and z = H(u)H(w) ranges over [−1024/55125, 1024/30625]; the lowest value occurs only with u on a 5-fold axis and w on a 3-fold axis.

**Theorem 1 (degree-7 certificate).** Let c² = (5 + 2√5)/15 and a² = (5 − 2√5)/15. Then c² + a² = 2/3 and c²a² = 1/45, so
(t² − c²)(t² − a²) = t⁴ − (2/3)t² + 1/45. Put
  p(t) = (t − c)(t + c)²(t² − a²)²,
which is ≤ 0 for t ≤ c. The odd part of p has mean 0, so
  E[p] = c·E[(t² − c²)(t² − a²)²] = c·(16/945 + (175/192)·H(u)H(w)) ≥ c·(16/945 − (175/192)·(1024/55125)) = 0.
So the mean of p over the 60 values is ≥ 0, while each value is ≤ 0. Suppose every t_g < c. Then each t_g is a root of p, so it lies
in {−c, −a, a}. But E[t²] = 1/3 forces the share of −c to be (1/3 − a²)/(c² − a²) = 1/2, and then E[t] ≤ −c/2 + a/2 < 0 ≠ 0, a
contradiction. Hence max_g (gu)·w ≥ c for all unit u, w. This is #43's covering lemma, and with the sphere row's bilinear form it gives
Theorem 2 (t_min ≤ 15 − 6√5). Equality needs z at its minimum and every t_g in {±c, ±a}: u on a 5-fold axis and w on a 3-fold axis,
whose 60 values are ±c and ±a, 15 each (checked exactly). Geometrically these are the 12 icosahedron corners seen from a face centre.

**Theorem 2 (degree ≤ 6 cannot).** A certificate that proves the sharp c must have mean 0 on the extremal orbit. Each of its values
must then be a root, and −c, −a, a lie inside [−1, c], so they need roots of even order. That takes degree ≥ 1 + 2·3 = 7. Allowing
the certificate to depend on z = H(u)H(w) does not help, since the extremal orbit already sits at one z. LP with z at both ends of its
range gives the best bounds m ≥ 0.774347 at degree 5 (√(3/5) = 0.774597, up to the grid), 0.783500 at degree 6 (constant 1.629003)
and 0.794219 at degree 7 (c = 0.794654; the shortfall is the grid). So the three constants of the sphere row are moment bounds of
degrees 2, 3 and 7: tetrahedral 9 (a 2-design, linear times linear), octahedral 3 (a 3-design, cubic with roots ±1/√3) and
icosahedral 15 − 6√5 (degree 7, reading the first invariant harmonic, roots ±c and ±a).

Known cases reproduced first: the octahedral cubic certificate's mean (1 − 3m²)/(9m), 1/c² = 15 − 6√5, the 60 rotations.

## 2. Bird 2: the New-Face Lemma

Setting: og-margin and og-gnomon (#43 Conjecture 1, t_min(D_k) ≤ 3/φ²; exact for k ≤ 11). Theorem N: Conjecture 1 holds for every k ≥ 11
if r(D_12) ≥ 1.084154 = (φ²/3)·R(D_11) and every new face of D_j, j ≥ 13, lies at distance ≥ 1.084154.

**Exact results (bird2_base.py: the og-margin exact builds D_0..D_12 rerun with exact face distances; 413 s; t_min checks of
og-margin reproduced; FINAL ok).** All comparisons below are exact signs in Q(√5) (r(D_12)² has 18 425 digits).

| j | R(D_j) | r(D_j) | five-fold face distance | new-face minimum ν(D_j) | new / all face orbits |
|---|---|---|---|---|---|
| 9 | 1.290556855 | 1.155919434 | 1.155919434 (carries r) | 1.155919434 | 13 / 13 |
| 10 | 1.243721073 | 1.156886368 | 1.156886368 (carries r) | 1.165919629 | 12 / 13 |
| 11 | 1.242329981 | 1.165269366 | 1.165269366 (carries r) | 1.165593860 | 11 / 12 |
| 12 | 1.237154195 | 1.179354549 | 1.179354549 (carries r) | 1.181871231 | 16 / 17 |

**Theorem 5 (exact base of Theorem N).** (i) r(D_9) < r(D_10) < r(D_11) < r(D_12). For j = 9..12 the inradius sits on the 12 five-fold
faces, and the only surviving face orbit at j = 10, 11, 12 is that one. This makes og-gnomon's recovery mechanism (G1) exact.
(ii) R(D_k) is non-increasing for k = 0..12. (iii) r(D_12)² > (φ⁴/9)·R(D_11)², so r(D_12) = 1.179354549 > 1.084154039, with margin
+8.78 %. (iv) Every new face of D_1..D_12 lies above 1.084154 (exact; the smallest is ν(D_9) = 1.155919).
Hence, exactly: **#43 Conjecture 1 holds for k ≤ 11, and for every k ≥ 11 it follows from the New-Face Lemma alone, for
j ≥ 13** (every new face of D_j, j ≥ 13, at distance ≥ 1.084154). The base value of Theorem N is no longer a float.

**Certificates on the new faces: they do not reach the lemma.** A new face of D_{j+1} with normal w lies at distance
h_{D_{j+1}}(w) = max_i h_i (n_i·w) (Lemma A). If only orbits of normals are known, the best any polynomial certificate can give is the
covering factor of one orbit, min_w max_g (gn)·w ≤ c = 0.7947 (equality for n on a 5-fold axis, Theorem 1 above). The lemma needs
1.084154/r(D_j) ≈ 1.084154/1.1767 = 0.921, and the shortfall compounds over steps. The control has to come from the actual positions
of the normals and from the recovery mechanism (og-gnomon G1), not from the group. So this route is closed for the lemma; it does
reproduce the factor that drives Theorem 2.

## 3. Bird 3: the turn on the dodecahedron–icosahedron line

S_λ = {a·x ≤ φ + 2 for the 12 five-fold normals a (|a|² = φ + 2)} ∩ {b·x ≤ λ for the 20 three-fold normals b (|b|² = 3)}. The antipol
(same normals, inverted distances d ↦ |N|²/d) is S_λ^∨ = S_{κ₀/λ}/(φ + 2) with κ₀ = 3(φ + 2) = (15 + 3√5)/2, so the turn is λ ↦ κ₀/λ.
In the unit coordinate μ = λ/√κ₀ (the ratio of the two face distances) the turn is μ ↦ 1/μ, fixed point μ = 1. Both families are facets
for φ² < λ < κ₀/φ², i.e. c < μ < 1/c; the ends are the icosahedron and the dodecahedron (checked exactly).

**Walls.** S_λ changes its combinatorics at exactly one interior value, λ = φ + 2 (exact; four-plane concurrency, linear in λ), the
icosidodecahedron with 30 corners. The antipol pair also has the turned wall λ = κ₀/(φ + 2) = 3. Hence three regions.

**Theorem 3 (closed form; exact).** For φ² < λ < κ₀/φ²,
  t_min(S_λ) = min(λ/φ², κ₀/(φ²λ), 10 − √5 − (λ + κ₀/λ)),
and in unit form, t_min = min(μ/c, 1/(cμ), 10 − √5 − √κ₀·(μ + 1/μ)), since κ₀/φ⁴ = 15 − 6√5 = 1/c². In each region the maximising corner
pair is proved exactly: λ times the difference is a quadratic, checked ≥ 0 on the closed region. The form agrees with full corner
enumeration at two interior points per region. The middle form minus λ/φ² is concave and vanishes at λ = φ² and λ = 3, which gives
the minimum structure. The form is symmetric under the turn, and in s = μ + 1/μ the middle piece is 10 − √5 − √κ₀·s, decreasing in s.

**The turn maximises t_min.** The maximum over the open line is at μ = 1 (s = 2), with value 10 − √5 − √(30 + 6√5) = 1.174819194130. It
equals (R/r)² of the fixed solid, the solid with every face tangent to one sphere, where Theorem 1 of #43 is an equality. This is the
cube–octahedron pattern again (min(μ, 3/μ, 5 − s), maximum 5 − 2√3 at √3), now proved on the icosahedral line. At the two walls
t_min = 3/φ² exactly, #43 Conjecture 1's constant (the icosidodecahedron has t_min = 3/φ²). At the ends the limit is 1, while the
end solids themselves have 15 − 6√5: t_min jumps where a family stops being facets, as on the cube–octahedron line.

## 4. Bird 4: #43 Theorem 3 as the turn of the beat line

Beat line: S_0 = ID (circumradius φ, edge 1), S_{k+1} = T(S_k), S_{k+4} = c·S_k with c = 10/φ⁴ = 35 − 15√5 (the hop). Exact checks: every
plane of every T step is a facet, P(T(S)) = S at S_0..S_3 (so P = T⁻¹ on the line), and Lemma 3 (polar(P(S)) = T(polar S)) holds at
the radii² φ², 15 − 5√5 and 1.

**Theorem 4 (the beat turn from the framework).** Let π be reciprocation about any sphere centred at O. If S and π(S) lie on the
beat line, then π(T(S)) = T⁻¹(π(S)). Proof: Lemma 3 applied to T(S) gives π(S) = π(P(T(S))) = T(π(T(S))), and P = T⁻¹ on the line. So
π reverses the line: π(S_k) = S_{a−k} for one constant a. The constant comes from one fact. If every corner of S lies on the sphere
of radius ρ, then π_ρ(S) = {x : v·x ≤ ρ² = v·v} = T(S): the polar of an inscribed station is the next beat. The GTI (k = 2) has all
its corners at radius² 15 − 5√5 = cφ² (exact), so π(S_2) = S_3 and a = 5: beat k ↔ 5 − k, fixed point 5/2, the antipol GTI|FPD
(the GTI inscribed in the reference sphere, the FPD circumscribed about it). The ID (k = 0) is inscribed in the sphere of radius² φ²,
which gives the same turn one hop down: π_{φ²}(S_k) = S_{1−k}, fixed point 1/2, the antipol ID|RT (checked exactly). The RT and FPD
have corners on two spheres each, so they cannot fix a turn. #43 Theorem 3 (polar(S_k) = S_{5−k}, k = 0..5) is reproduced exactly.

**The turn and the shell ratios.** For t_k = min{t : S_k ⊂ t·S_{k−1}} polarity gives t_k = t_{6−k} (S ⊂ tS′ ⟺ polar S′ ⊂ t·polar S),
and t_{k+4} = t_k. So the shells ID→RT (k = 1) and GTI→FPD (k = 3) are the fixed shells, and RT→GTI ↔ FPD→c·ID are exchanged. Exact:
  t_1 = (5 − √5)/2 = 1.381966,  t_2 = t_4 = (9 − 3√5)/2 = 3/φ² = 1.145898,  t_3 = 5 − 5√5/3 = 1.273220.
The fixed shells carry the two largest ratios, the same reading of the prediction as on the solid lines. The moving pair carries 3/φ²
again.

## 5. Paragraph for the Hopscotch foundations paper

The icosahedral line closes the sphere row. The three containment constants of #43 are moment certificates of one bilinear form: for a
G-symmetric solid, t_min ≤ 1/c² with c = min max_g (gu)·w, and c is forced by a polynomial that is ≤ 0 below c and has nonnegative mean
over every orbit. Tetrahedral orbits are 2-designs (degree 2, constant 9), octahedral and pyritohedral orbits are 3-designs (degree 3,
constant 3), and icosahedral orbits are 5-designs whose sixth moment carries the first invariant harmonic H:
E[t⁶] = 1/7 + (175/192)·H(u)H(w). The certificate (t − c)(t + c)²(t² − a²)², with c² and a² the two conjugates (5 ± 2√5)/15, has mean
c·(16/945 + (175/192)·H(u)H(w)). That mean is ≥ 0 exactly because H runs from −32/315 at the 3-fold axes to 32/175 at the 5-fold
axes, so 15 − 6√5 is a moment bound of degree 7, and no degree below 7 can give it. On the dodecahedron–icosahedron line, with the face
distances in ratio μ, the antipol of S_μ is S_{1/μ}, and t_min = min(μ/c, 1/(cμ), 10 − √5 − √κ₀·(μ + 1/μ)) peaks at the turn μ = 1,
the solid with every face tangent to one sphere, as on the cube–octahedron line. On the beat line of Universal PiTet, reciprocation
conjugates the step to its inverse, so it reflects the line, and the station inscribed in the reference sphere fixes the mirror:
the GTI gives beat k ↔ 5 − k (#43 Theorem 3), with fixed point 5/2 between the GTI and the FPD.

## 6. LEADS

1. Bird 1 for other groups: the octahedral certificate is degree 3, but O also has a degree-4 invariant harmonic. Does a degree-5
   certificate reading it give the octahedral covering constant in other settings (e.g. the T_h or T constants for solids with
   one face family fixed)? The same machinery gives sharp constants for any orbit-pair problem whose extremal orbit has few values.
2. Bird 1 destination: the degree-7 certificate proves #43 Theorem 2 without the kite or the three-mirror lemma. It suits a #43
   version line or the foundations paper (DICTO's choice where).
3. Bird 2: the New-Face Lemma needs the actual normal positions. The next concrete step is a certified interval build of D_13..D_20
   (float hulls with rigorous error bounds and no exact coordinates). It would prove the lemma level by level up to 20, after
   which og-margin's mesh route has room (∏_{j≥20} cos θ_j ≥ 0.8836 suffices).
4. Bird 3: the three walls of the icosahedral line carry 3/φ² (λ = 3, λ = φ + 2) and the ends jump to 15 − 6√5. Is the OG's
   constant 3/φ² = t_min(ID) behind #43 Conjecture 1's equality at D_3? A one-line comparison of D_3 with the ID.
5. Bird 4: the shell ratios 3/φ² (moving shells), (5 − √5)/2 and 5 − 5√5/3 (fixed shells). Read the Cleo Towers' tower heights
   by the turn: are towers on the two fixed shells self-polar as sets?
6. The outline's prediction "the fixed point of a polar turn maximises the containment constant" now holds on three lines
   (cube–octahedron, dodecahedron–icosahedron, beat shells). A general proof would use the sphere row: at a self-antipol,
   t_min = R² = (R/r)² is Theorem 1's equality. What is left to show is that moving off the turn lowers max x·y.

## 7. Ready Concordance ledger lines

```json
{"question": "Hopscotch sphere row: degree-6 moment certificate for #43 Theorem 2 (15 - 6 sqrt5)", "method": "exact sympy over Q(sqrt5): orbit moments of the 60 rotations to degree 7 with symbolic u, w; degree-6 harmonic H; Jacobian of (|x|^2, H, Q10) = product of 15 mirror forms; mirror-circle critical points; LP for degrees 5-7 (studies/2026-11-09-icosahedral-line, bird1_certificate.py)", "status": "SETTLED", "result": "PROVED-FROM-FRAMEWORK: E[t^6] = 1/7 + (175/192) H(u)H(w), H in [-32/315 (3-fold), 32/175 (5-fold)]; certificate p = (t-c)(t+c)^2(t^2-a^2)^2, c^2,a^2 = (5 +- 2sqrt5)/15, E[p] = c(16/945 + (175/192)H(u)H(w)) >= 0 gives max_g (gu).w >= c, so 15 - 6sqrt5 from moments; degree <= 6 cannot (extremal orbit values +-c, +-a need even roots at -c, +-a); LP degree-6 best 1.629003", "retry": "never", "study": "studies/2026-11-09-icosahedral-line", "date": "2026-11-09"}
{"question": "#43 Conjecture 1: New-Face Lemma by invariant-polynomial certificates; exact base r(D_12)", "method": "exact Q(sqrt5) builds D_0..D_12 (og-margin exact_family.py extended with exact face distances, orbit sizes, new-face test) (studies/2026-11-09-icosahedral-line, bird2_base.py)", "status": "UNDECIDED", "result": "BASE EXACT, LEMMA OPEN: r(D_9) < r(D_10) < r(D_11) < r(D_12) exact, all on the five-fold faces (the only surviving orbit at 10-12); r(D_12) = 1.179354549 > (phi^2/3) R(D_11) = 1.084154039 exact (+8.78%); R(D_k) non-increasing k <= 12; new faces of D_1..D_12 all above 1.084154 (min 1.155919 at D_9); Conjecture 1 for k >= 11 now rests only on the New-Face Lemma for j >= 13; certificates on orbits cannot prove it (one orbit covers only to c = 0.7947, need 0.921)", "retry": "only a certified (interval) build of D_13..D_20 or a direct proof of the New-Face Lemma; never certificates on orbits alone", "study": "studies/2026-11-09-icosahedral-line", "date": "2026-11-09", "target": "#43 Conjecture 1 (the OG's margin)"}
{"question": "Hopscotch: the turn on the dodecahedron-icosahedron line; does the fixed point maximise t_min", "method": "exact Q(sqrt5): S_lam = {a.x <= phi+2} n {b.x <= lam}, antipol S_{k0/lam}, walls by exact concurrency, per-region maximising pair proved by exact quadratic signs, full enumeration spot checks (studies/2026-11-09-icosahedral-line, bird3_line.py)", "status": "SETTLED", "result": "PROVED: turn mu -> 1/mu (lam -> k0/lam, k0 = (15+3sqrt5)/2), one wall (icosidodecahedron, lam = phi+2) and its image 3; t_min = min(mu/c, 1/(c mu), 10 - sqrt5 - sqrt(k0)(mu + 1/mu)); maximum 10 - sqrt5 - sqrt(30+6sqrt5) = 1.174819 exactly at the turn mu = 1 (= (R/r)^2, all faces tangent); t_min = 3/phi^2 at both walls; ends jump (limit 1, end solids 15 - 6sqrt5)", "retry": "never", "study": "studies/2026-11-09-icosahedral-line", "date": "2026-11-09"}
{"question": "Hopscotch: #43 Theorem 3 (beat k <-> 5 - k) as the turn of the beat line", "method": "exact Q(sqrt5): ID, RT, GTI, FPD, c ID, c RT by the T step; Lemma 3 at three radii; inscribed-station lemma; polar(S_k) = S_{5-k}; shell ratios (studies/2026-11-09-icosahedral-line, bird4_beats.py)", "status": "SETTLED", "result": "PROVED-FROM-FRAMEWORK: Lemma 3 + P = T^-1 give pi T pi = T^-1, so polarity reflects the beat line; a station inscribed in the reference sphere has polar = its next beat, so the GTI (corners at radius^2 15 - 5sqrt5) fixes k <-> 5 - k, fixed point 5/2 = antipol GTI|FPD; the ID (radius^2 phi^2) gives the same turn one hop down (1/2, ID|RT); shell ratios t_k = t_{6-k}: fixed shells (5-sqrt5)/2 and 5 - 5sqrt5/3 are the largest, moving shells 3/phi^2", "retry": "never", "study": "studies/2026-11-09-icosahedral-line", "date": "2026-11-09"}
```

## 8. Sources checked

papers/polar-line-outline/paper.html (§0–5); papers/dicto-concordance/ledger-digest.txt (59 entries; entries 52, 55, 58 opened in the
digest only); studies/2026-11-09-hopscotch-rows/README.md; studies/2026-11-08-octahedral-constant (README; scripts
sanity_icosahedral.py: its group generator C5 belongs to a different frame from its axes, which is harmless there because only the
group order is used, but it is noted here because bird 1 builds the 60 rotations from the icosahedron's own corners instead);
studies/2026-11-09-og-margin (README; scripts/exact_family.py, copied and extended); studies/2026-11-09-og-gnomon/README.md;
papers/2026-10-21-kyushindo-cores/paper.html v2 (abstract, §1 beat definition, Theorem 3, Lemma 3, §4 Polar Cleo Towers).
Reference library not searched for this study. The tools named above are textbook and cited from memory, to check before any paper
text: Delsarte, Goethals, Seidel, Geom. Dedicata 6 (1977); Goethals, Seidel (1981) on orbits as designs; Steinberg (1960) on the
Jacobian of basic invariants; Klein's Lectures on the Icosahedron (1884) for the degree-6 invariant.

DICTO · dictospheres.com
