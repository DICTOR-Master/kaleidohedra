# The octahedral constant 3 (#43 Conjecture 2) — study 2026-11-08

**Conclusion: #43 Conjecture 2 is true: every convex polytope with octahedral rotational symmetry satisfies S ⊂ 3·P(S), sharp for the cube and the octahedron.**
**Status: PROVED** (two independent exact proofs of the one missing step, the octahedral covering lemma; every step checked in exact arithmetic).

Extras proved on the way: the same constant 3 for pyritohedral symmetry (T_h), the constant 9 for tetrahedral symmetry (T, T_d), and
the invariance of t_min under #81's core turn μ ↦ 3/μ, with the closed form of t_min on the whole cube–octahedron sweep.

## 1. The statement and what was missing

Notation of #43 (DICTO Kyushindo Cores, Zenodo 23532013): S a convex polytope with O inside, faces n_i·x ≤ h_i; R(S) the largest
corner distance, r(S) the smallest face distance; P(S) the hull of the foot points h_i n_i of the face planes (DICTO's step of the
downward family); t_min(S) the least t with S ⊂ t·P(S).

- #43 Theorem 1 (general): t_min(S) ≤ R/r(P(S)) ≤ (R/r)², equality for the Platonic solids.
- #43 Conjecture 2: octahedral rotational symmetry ⇒ S ⊂ 3·P(S). By Theorem 1 it is enough that r(S) ≥ R(S)/√3; and since S contains
  the hull of the orbit of its farthest corner v, it is enough that every orbit O·v comes within arccos(1/√3) = 54.7356° of every
  direction (the covering lemma). #43's kite argument proves the icosahedral version but fails here: the kite's second diagonal is 60°.

Ledger: the Concordance ledger (44 entries) has no earlier attempt on #43; the only earlier work is the 2026-10-21-nesting-proof study
(covering_lemma.py: numerical support, kite fails). So the attempt here retried nothing.

## 2. Theorem A (#43 Conjecture 2)

**Covering lemma.** For all unit vectors u, w: max over the 24 rotations g of O of (g u)·w ≥ 1/√3.
Equality only when u lies on a 4-fold axis and w on a 3-fold axis, or the reverse.

**Theorem A.** Every convex polytope S with octahedral rotational symmetry about O has r(S) ≥ R(S)/√3, hence (#43 Theorem 1)
S ⊂ (R/r)²·P(S) ⊂ 3·P(S). Sharp: the cube and the octahedron have t_min = (R/r)² = 3 exactly.

Proof of Theorem A from the lemma: let v be a farthest corner, |v| = R. S is convex and O-symmetric, so it contains every g v; a face
plane with unit normal w has h ≥ max_g (g v)·w ≥ R/√3 by the lemma. So r ≥ R/√3 and (R/r)² ≤ 3. ∎

### Proof 1 of the lemma (moments; every O-orbit is a spherical 3-design)

For unit u, w put t_g = (g u)·w, g in O. Exact identities (design_proof.py, sympy, symbolic u and w):
Σ_g t_g = 0, Σ_g t_g² = 8|u|²|w|² (so the mean square is 1/3), Σ_g t_g³ = 0.
Suppose every t_g ≤ m with m > 0. The cubic p(t) = (t − m)(t + 1/(3m))² = (t − m)(3mt + 1)²/(9m²) is ≤ 0 for t ≤ m, so its mean
over the 24 values is ≤ 0; with the three moments that mean is exactly (1 − 3m²)/(9m). Hence 3m² ≥ 1, m ≥ 1/√3. ∎
Equality forces every t_g to be a root of p, i.e. ±1/√3: this happens for u = e1, w = (1,1,1)/√3 (checked exactly: the 24 values are
±1/√3).

### Proof 2 of the lemma (three mirrors; the repair of #43's kite)

The 48 Möbius triangles of O_h; take T = cone(e1, e1+e2, e1+e2+e3) = {x1 ≥ x2 ≥ x3 ≥ 0}, with corners on the 4-, 2- and 3-fold axes
(sides 45°, 35.26°, 54.74°; exact cos² 1/2, 2/3, 1/3). Write F(u,w) = max_g (g u)·w; F(hu, hw) = F(u, w) for every h in O_h (O is
normal in O_h) and F(ku, w) = F(u, kw) = F(u, w) for k in O. So we may take u = a in T, and then either w = b in T (case A) or
w = s0 b with b in T and s0 = diag(1, 1, −1), the mirror in the side e1–(e1+e2) (case B).

- Case A: g = identity gives a·b, and a·b ≥ |a||b|/√3 on T × T.
- Case B: three rotations, g1 = identity, g2 = s0·P12 (half-turn about (1,1,0)) and g3 = s0·P23 (quarter-turn about the x1 axis),
  give (g a)·(s0 b) = a1b1 + a2b2 − a3b3, a1b2 + a2b1 + a3b3, a1b1 + a2b3 + a3b2: a against the mirror images of b in the three sides
  of T. Their average L = (2a1b1 + a1b2 + a2b1 + a2b2 + a2b3 + a3b2)/3 is ≤ the max, and L ≥ |a||b|/√3 on T × T.

Both inequalities follow from the **vertex lemma**: if a bilinear L has L(v_i, w_j) ≥ 0 and 3 L(v_i, w_j)² ≥ |v_i|²|w_j|² for the
generators v_i of one cone and w_j of another, then L(a, b) ≥ |a||b|/√3 on the whole product (write a = Σ α_i v_i, α_i ≥ 0:
L(a, w_j) = Σ α_i L(v_i, w_j) ≥ |w_j|/√3 · Σ α_i |v_i| ≥ |w_j||a|/√3 by the triangle inequality; then the same in b).
The 9 generator pairs, exact (proof_check.py; generators (1,0,0), (1,1,0), (1,1,1)):

| v, w | \|v\|²\|w\|² | case A: 3(a·b)² | case B: 3L² |
|---|---|---|---|
| e1, e1 | 1 | 3 | 4/3 |
| e1, (1,1,0) | 2 | 3 | 3 |
| e1, (1,1,1) | 3 | 3 (equality) | 3 (equality) |
| (1,1,0), (1,1,0) | 4 | 12 | 25/3 |
| (1,1,0), (1,1,1) | 6 | 12 | 12 |
| (1,1,1), (1,1,1) | 9 | 27 | 49/3 |

(the three remaining pairs are the transposes, with the same numbers). Equality only at (e1, e1+e2+e3) and its transpose. ∎

Geometric reading: for a and b in one Möbius triangle, at least one of the three mirror images of b in the sides of the triangle lies
within 54.74° of a. #43 used one mirror (the longest side) and needed the kite; with all three the mean of the cosines suffices.
The LP search (certificate.py) found a single weight vector for all of T × T at the first try (weights 0.439, 0.268, 0.293 on the three terms
a1b1 + a2b2 − a3b3, a1b1 + a2b3 + a3b2, a1b2 + a2b1 + a3b3, exact rationals in data/certificate.json); the equal weights 1/3 of the table also pass.

## 3. Wider results (proved)

**Theorem A′ (any group whose orbits are 3-designs).** Proof 1 uses only the moments. Exact orbit sums (design_proof.py) show:
orbits of T_h (pyritohedral), O and I are spherical 3-designs (so also O_h, I_h, which contain them); orbits of T and T_d are only
2-designs (the invariant xyz). Hence every convex polytope with **pyritohedral** symmetry also satisfies S ⊂ 3·P(S) (sharp: cube,
octahedron, both pyritohedral). For icosahedral symmetry this gives only 3, weaker than #43 Theorem 2's 15 − 6√5.

**Theorem B (tetrahedral constant 9).** For a 2-design, t_g ∈ [−1, m] gives mean of (m − t)(t + 1) = m − 1/3 ≥ 0, so r ≥ R/3 and
every convex polytope with tetrahedral rotational symmetry (T, hence T_d) satisfies S ⊂ 9·P(S); sharp for the tetrahedron.
(The nesting-proof README of 2026-10-21 listed "tetrahedral analogue would be 9" as unproved.) Groups with an invariant axis have no
constant (#43's thin bipyramids), consistent with their orbits not being 2-designs.

**Proposition C (distance inversion; #81's core turn keeps t_min).** Let S = {N_k·x ≤ d_k} with every plane a facet and let
S^∨ = {N_k·x ≤ |N_k|²/d_k} (same normals, inverted distances). Then P(S) = conv(d_k N_k/|N_k|²) has polar S^∨, and since the gauge of
a body is the support function of its polar,
t_min(S) = max_{x ∈ S} gauge_{P(S)}(x) = max_{x ∈ S, y ∈ S^∨} x·y.
The right side is symmetric, so t_min(S) = t_min(S^∨) whenever every plane of S^∨ is a facet too. For a solid with two families of
planes on dual axes, S^∨ is (up to scale) the core of #81's turn, (a, b) ↦ (tcb, tca). On the cube–octahedron sweep
P_μ = [−1,1]³ ∩ {|x|+|y|+|z| ≤ μ} (1 < μ < 3), P_μ^∨ = P_{3/μ} exactly, so **t_min(P_μ) = t_min(P_{3/μ})**: the core turn μ ↦ 3/μ
keeps t_min (not (R/r)²).

**Proposition D (closed form on the sweep).** For 1 < μ < 3, with s = μ + 3/μ,
t_min(P_μ) = μ (1 < μ ≤ 3/2), 5 − s (3/2 ≤ μ ≤ 2), 3/μ (2 ≤ μ < 3).
Proof: by Proposition C, t_min is the largest x·y (a bilinear maximum, attained at corners) over corner pairs of P_μ and P_{3/μ}; the corners are the signed permutations of
(1, μ−1, 0) for μ ≤ 2 and of (1, 1, μ−2) for μ ≥ 2, and the rearrangement inequality picks the sorted pairing:
(1, μ−1, 0)·(1, 1, 3/μ − 2) = μ, and (1, μ−1, 0)·(1, 3/μ − 1, 0) = 5 − s (sorted wins since (2 − μ)(2 − 3/μ) ≥ 0). ∎
The maximum over the sweep is 5 − 2√3 ≈ 1.5359, at μ = √3, the fixed point of the core turn (among the tested μ also the only one with t_min = (R/r)²).
At the ends the formula jumps (t_min = 3 at μ = 1 and μ = 3): there one family of planes stops being facets.

## 4. Every number and how it was checked

All runs on dicto-big-brother (~/geom/bin/python, sympy 1.14, scipy 1.18), each under 1 minute, logs in data/.

| number / claim | value | how checked | script, log |
|---|---|---|---|
| sanity: t_min of tetrahedron, cube, octahedron, dodecahedron, icosahedron | 9, 3, 3, 15 − 6√5, 15 − 6√5 (= (R/r)²) | exact sympy, Q(√5) | tmin_tests.py, data/tmin_tests.log |
| sanity: icosahedral covering constant by the vertex lemma | c² = (5 + 2√5)/15, 1/c² = 15 − 6√5; kite (mirror in the 37.377° side) passes, other single mirrors fail, three-mirror average passes | exact Q(√5), group of 60 generated exactly | sanity_icosahedral.py, data/sanity_icosahedral.log |
| O-orbit moments | Σt = 0, Σt² = 8\|u\|²\|w\|², Σt³ = 0, Σt⁴ ≠ uniform | exact symbolic | design_proof.py, data/design_proof.log |
| mean of p | (1 − 3m²)/(9m) | exact symbolic | design_proof.py |
| design strengths | T 2, T_d 2, T_h 3, I 3 | exact symbolic orbit sums | design_proof.py |
| three rotations of case B in O, formulas E0, E12, E23 | as in §2 | exact (sympy matrices) | proof_check.py, data/proof_check.log |
| 9 vertex pairs, cases A and B | table in §2 | exact rationals | proof_check.py |
| reduction set up correctly | bound never above F in 20000 random pairs; min F = 0.6307 > 0.5774 | float | proof_check.py |
| LP certificate | 1 cell, weights exact rationals summing to 1, 9 pairs exact, tiling area sum exactly 1 | float LP to find, exact to check | certificate.py, data/certificate.json, data/certificate.log |
| pilot | min F over 400000 random pairs 0.6132; chamber case-B min 0.5883 near (e1, c3) | float | explore.py, data/explore.log |
| octahedral solids, exact t_min ≤ (R/r)² ≤ 3 | cuboctahedron 3/2 (2); truncated octahedron 3/2 (5/3); rhombic dodecahedron 2 (2); truncated cube 3√2 − 3 (5 − 2√2); rhombicuboctahedron (23 − 10√2)/7 (7 − 4√2); truncated cuboctahedron 1 + √2/7 ((69 + 2√2)/49); tetrakis hexahedron 5/3 (5/3); triakis octahedron 5 − 2√2 (5 − 2√2) | exact Q(√2) | tmin_tests.py |
| sweep P_μ, 15 rational μ plus φ, √3 | all ≤ 3; P_φ: t_min = 6 − 2√5, (R/r)² = 15 − 6√5 | exact | tmin_tests.py |
| random orbit hulls | O: 3000, max t_min 1.5279; O_h: 2000, max 1.2726; T_h: 2000, max 1.5339 (≤ 3); T: 2000, max 2.7990 (≤ 9) | float | tmin_tests.py |
| core turn keeps t_min | 34 values of μ (31 rational, √3, φ, 1 + √2/2): t_min(P_μ) = t_min(P_{3/μ}) every time; (R/r)² equal only at √3 | exact | tmin_core_turn.py, data/tmin_core_turn.log |
| closed form of Proposition D | matches all 34 exact values | exact | tmin_core_turn.py |
| Proposition C beyond two families | 1104 random three-family octahedral solids (planes on 4-, 2-, 3-fold axes, all facets in S and S^∨): max \|t_min(S) − t_min(S^∨)\| = 6.7e−16 | float | tmin_core_turn.py |
| 5-design moment bound (lead) | m ≥ 0.774597 = √(3/5) (gives 5/3 for icosahedral, weaker than 15 − 6√5 and above φ) | float LP | design_proof.py |

Every script ends with a conditional FINAL line; all six printed FINAL ok.

## 5. On the Concordance link (#80, #81)

The gap row says #80's gain 3 and #81's involution μ ↦ 3/μ "give the same constant". Checked: all three are 1/c² with
c = cos(angle from a 4-fold to the nearest 3-fold axis) = 1/√3, the hypotenuse of the (2,3,4) Möbius triangle: #80's gain is
(R/r)² of the cube and octahedron, #81's two-turn factor is t²c² with c² = 1/3, and the covering radius of Theorem A is arccos c. The
proof of Theorem A uses neither #80 nor #81. A real link beyond the shared number is Proposition C: #81's core turn is the distance
inversion S ↦ S^∨ on two-family solids, and it keeps t_min.

Nothing inconsistent was found in #43, #80 or #81 for the statements used here: #43 Theorem 1's equality cases, the value 15 − 6√5 and
its comparison with φ (29 < 13√5), the 60° kite diagonal, #80's gains 9, 3, 15 − 6√5 and #81's c² = 1/3 and (5 + 2√5)/15 all
reproduce exactly. Two remarks for later versions: (i) Conjecture 2's evidence sentence can become a theorem with either proof
above; (ii) P_μ's t_min is discontinuous at μ = 1 and 3 (a plane family stops being facets), so any table over the closed sweep should
mark the ends.

## 6. Sources checked

- #43 paper source ~/k-research/papers/2026-10-21-kyushindo-cores/paper.html (Theorems 1, 2, Corollary 1, Conjectures 1, 2).
- #80 ~/k-research/papers/star-cores-c/paper.html (abstract, Section 8 "The series"); #81 ~/k-research/papers/star-cores-b/paper.html
  (abstract); the P_μ sweep definition in ~/k-research/papers/2026-11-04-harmonic-fingerprint/paper.html.
- ~/k-research/studies/2026-10-21-nesting-proof (README.md, covering-lemma.log).
- Concordance concordance.json: gaps.ranked[4], gaps.weak[1], gaps.loose (#43), strands 6 and 9, ledger (44 entries, none on #43).
- Reference library (dicto-big-brother ~/library-index/passages.json, 7730 passages), queries "spherical design(s)", "Levenshtein",
  "Goethals", "Delsarte", "covering radius", "orbit polytope": 4 hits, none on spherical designs (Dutour Sikirić–Schürmann–Vallentin
  2008, Erdahl–Rybnikov 2001, Etzion 2011, a manifest; all about lattice covering radii or codes). Not in the library and cited from
  memory, to be checked before any paper text: Delsarte, Goethals, Seidel, "Spherical codes and designs", Geom. Dedicata 6 (1977);
  Goethals, Seidel, "Cubature formulae, polytopes, and spherical designs" (1981), where group orbits as designs are treated. The
  moment argument of Proof 1 is of their linear-programming kind; whether the inradius bound for orbit polytopes is stated there
  was not checked.

## 7. LEADS

1. Destination: Theorem A (and A′, B) closes #43 Conjecture 2: a "Version 2 adds Theorem 4" line for #43, or a section elsewhere.
   Propositions C and D belong with #81's core turn or the sweep paper. Where to place: DICTO's choice (one-line question).
2. Concordance: ledger entry and gap update (ranked[4] and weak[1] "#43 Conjecture 2 ↔ #80" can move from suggestive to proved).
3. A uniform proof of #43 Theorem 2: the three-mirror average also passes exactly for the icosahedral triangle
   (sanity_icosahedral.py), so the kite is not needed there either.
4. Moments alone do not reach 15 − 6√5: the 5-design bound gives only 5/3 > φ. Which degree-6 invariant of I closes the gap?
5. Proposition C turns t_min into a bilinear maximum, t_min(S) = max x·y over S × S^∨. For #43's downward family
   (P(D_k) = D_{k+1}) this gives t_min(D_k) = max over D_k × polar(D_{k+1}), a possible route to #43 Conjecture 1 (t_min(D_k) ≤ 3/φ²).
6. Equality cases of Theorem A: which octahedral polytopes have t_min exactly 3 besides the cube and octahedron (the lemma's equality
   needs the farthest corner on a 4- or 3-fold axis and a face on the other)?
7. The maximum of t_min on the C·O sweep sits at the core turn's fixed point √3, beside the isoperimetric maximum there
   (gaps.waiting[12]); an icosahedral two-family sweep (Icosaxes side) should show the same at its own fixed point.

DICTO · dictospheres.com
