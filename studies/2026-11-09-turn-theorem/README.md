# The turn theorem: on the polar line of every regular polytope, t_min is largest at the turn, study 2026-11-09

**Verdict: PROVED for every regular convex polytope in every dimension.** The antipol maps S(μ) to S(c/μ) up to scale (c = h²R²).
t_min has an exact closed form along the whole line. It is largest at the fixed point μ = hR, and only there; at that point every
face of S touches one sphere and t_min = (R/r)² of that solid. **Status: DONE.** Exact checks: 171 sample solids on 13 lines
(the five Platonic solids, the six regular 4-polytopes, the 5-cube and the 5-orthoplex). Every script ends FINAL ok.

DICTO proposed the turn ("when you reach the end of your hopscotch you jump around and go back") and predicted that its fixed point
maximises t_min (outline papers/polar-line-outline). The framework and its names are DICTO's: the Hopscotch, antipol, hop, step,
jump, the turn, emergence, dissolution. Computation and proofs with Claude (Anthropic). Classical tools used: Coxeter's flag
(characteristic) simplex of a regular polytope, the dominance lemma for finite reflection groups (Bourbaki, Lie groups ch. V §3;
Humphreys, Reflection Groups and Coxeter Groups §1.12), and convex order (Jensen's inequality on a mean-preserving spread).

Ledger: entry 58 (sphere row) proved the C–O turn, entry 68 the D–I turn, entry 60 (dual sweeps) the no-turn theorem off the regular
solids. Splash-determinants found the turned events in 3 of 3 families. None of these attempted a general proof. This study proves
the general case and recovers each of those lines as a special case. Nothing here retries an earlier attempt.

## 1. Setting

P is a regular convex polytope in R^d, centred at 0, with inradius h and circumradius R. For a k-face F_k, its **flag radius**
ρ_k is the distance from 0 to the centre of F_k, so

  h² = ρ_{d−1}² < ρ_{d−2}² < … < ρ_1² < ρ_0² = R².

These d numbers are the **nodes**, and the intervals between consecutive nodes are the **hops**. With unit face normals n_i and
unit corner directions v̂_j, the polar line is

  S(μ) = {n_i·x ≤ h} ∩ {v̂_j·x ≤ μ/R},   h² ≤ μ ≤ R².

The corner plane v̂·x = μ/R passes through the centre of a k-face exactly when μ = ρ_k². So S(h²) = P* (the dual, with its corners
at the face centres of P) and S(R²) = P. The antipol S^∨ keeps the normals and inverts the distances, d ↦ 1/d. On the antipol pair,
t_min(S) = max x·y over x ∈ S and y ∈ S^∨ (form (B) of studies/2026-11-09-hopscotch-rows). On the open line every plane is a facet.

## 2. The theorem

**Turn Theorem.** Let c = h²R². For h² < μ < R²:

1. **(The turn.)** S(μ)^∨ = h⁻²·S(c/μ). Hence t_min(S(μ)) = t_min(S(c/μ)). The turn μ ↦ c/μ maps the line onto itself, and its
   fixed point is μ = hR.
2. **(Closed form.)** Let U_a be the random variable that takes the two nodes bracketing a, with mean a. Then
     h²·t_min(S(μ)) = E min(U_μ, U'_{c/μ})   (two independent variables).
   Written out:
   - if μ and c/μ lie in one hop [r, A], then h²·t_min = r + (μ − r)(c/μ − r)/(A − r);
   - otherwise h²·t_min = min(μ, c/μ).
3. **(The maximum.)** log t_min is a concave function of log μ that the turn leaves unchanged. t_min is largest at μ = hR, and only
   there. At that point every face of S lies at distance h, so it touches the sphere of radius h, and S^∨ = h⁻²S. The value is
     t_min(S(hR)) = R(S)²/h² = (R/r)² of the tangent solid = (r + (hR − r)²/(A − r))/h²,
   where [r, A] is the hop that contains hR. This is the equality case of #43's Theorem 1, t_min ≤ (R/r)².
4. **(Walls in turned pairs.)** S changes its face lattice exactly at the nodes μ = ρ_k² (this proves dual-sweeps LEAD 1 for
   regular P). S^∨ changes exactly at the turned nodes c/ρ_k². So each wall of S is paired with the antipol's wall at c/μ, and the
   ends h² and R² are paired with each other. t_min itself breaks at only one turned pair, μ₁ = max(r, c/A) and μ₂ = min(A, c/r),
   with μ₁μ₂ = c:
   - when rA ≠ c, these are a wall of S and the turn of a wall (a foot wall, a wall of S^∨). On the C–O line they are 2 and 3/2;
   - when hR is itself a node, the only break is the turn (tetrahedron, tesseract, 16-cell);
   - when rA = c, the hop of hR is turned onto itself and t_min is C¹. Only its curvature jumps, at r and A (5-cell, 24-cell).

## 3. Proof

Let G be the symmetry group of P. It is a finite reflection group. Fix a flag F_0 ⊂ F_1 ⊂ … ⊂ F_{d−1} and let q_k be the centre of
F_k, so |q_k| = ρ_k. The closed cone C̄ spanned by q_0, …, q_{d−1} is a closed chamber of G (Coxeter's characteristic simplex).

**Lemma 1 (dominance).** If x, y ∈ C̄, then x·y ≥ x·(gy) for every g ∈ G. This is standard: y − gy is a non-negative combination of
the simple roots, and x pairs non-negatively with each of them.

**Lemma 2 (flag Gram identity).** q_j·q_k = ρ²_{max(j,k)}. Proof: for j ≤ k, q_j lies in F_k. Also q_k is the foot of the
perpendicular from 0 to the affine span of F_k, so (q_j − q_k)·q_k = 0.

**Lemma 3 (the chamber slice).** n_0 = q_{d−1}/h and v̂_0 = q_0/R lie in C̄. By Lemma 1, on C̄ the largest n_i·x is n_0·x and the
largest v̂_j·x is v̂_0·x. So, writing x = Σ α_k q_k,

  S(μ) ∩ C̄ = {α_k ≥ 0, Σ α_k ≤ 1, Σ α_k ρ_k² ≤ μ}

(Lemma 2 gives q_{d−1}·x = h² Σ α_k and q_0·x = Σ α_k ρ_k²). This is the characteristic simplex conv(0, q_0, …, q_{d−1}) cut by one
plane. The cut passes a vertex exactly when μ = ρ_k², which proves part 4 for S. Its image under the turn proves part 4 for S^∨.

**Lemma 4 (the probability form).** Send x = Σ α_k q_k to the random variable U with P(U = ρ_k²) = α_k and P(U = 0) = 1 − Σ α_k. Then
q_0·x = E U, and by Lemma 2 x·y = Σ α_j β_k min(ρ_j², ρ_k²) = E min(U, V) for independent U, V.

**Part 1.** S(μ)^∨ = {n_i·y ≤ 1/h} ∩ {v̂_j·y ≤ R/μ}. Multiplying by h² gives {n_i·x ≤ h} ∩ {v̂_j·x ≤ h²R/μ} = S(c/μ). Form (B) is
symmetric in S and S^∨ and does not change under scaling, so t_min(S(μ)) = t_min(S(c/μ)).

**Part 2.** S and S^∨ are G-invariant, so by Lemma 1 the maximum in (B) can be taken over x, y ∈ C̄. By Lemmas 3 and 4,

  h²·t_min(S(μ)) = max {E min(U, V) : E U ≤ μ, E V ≤ c/μ, both taking values in the nodes and 0}.

For fixed V, φ(u) = E min(u, V) is concave and non-decreasing in u. Among all laws on the nodes with mean a, the bracketing two-point
law U_a is the least in convex order: every other law is a mean-preserving spread of it. So by Jensen, E φ(U) ≤ E φ(U_a), for every
V at once. Applying this to both variables gives h²·t_min = E min(U_μ, U'_{c/μ}). If the two bracketing hops differ, the smaller
variable lies below the larger one everywhere, so E min = min(μ, c/μ). If both lie in one hop [r, A], the 2 × 2 table gives
r + (μ − r)(c/μ − r)/(A − r).

**Part 3.** Put s = log μ. The turn is s ↦ log c − s.
- On the outer pieces h²·t_min = μ or c/μ, which is linear in s.
- On the middle piece h²·t_min = const − r(e^s + c e^{−s})/(A − r), a negative cosh, which is strictly concave and symmetric about
  s = log √c.
- At the breaks the slope of log t_min drops. At μ₁ = c/A ≥ r the right slope is r(A² − c)/(A(A − r)) against the left slope
  c/A = g(μ₁), and r(A² − c) ≤ c(A − r) ⟺ rA ≤ c. At μ₁ = r ≥ c/A the right slope is (c − r²)/(A − r) against r, and that inequality
  is again rA ≤ c. Both cases hold, since μ₁ = max(r, c/A).

So log t_min is concave in s and symmetric about log √c. Its maximum is at s = log √c, and it is unique, because the function is
strictly monotone on the outer pieces and strictly concave on the middle one. The comparison can also be written directly, by AM–GM.
For μc/μ = c in one hop,
  F(√c, √c) − F(μ, c/μ) = r(√μ − √(c/μ))²/(A − r) ≥ 0.
Across two hops, F = μ ≤ R(S(√c))² because
  r + (√c − r)²/(A − r) − c/A = r(A − √c)²/(A(A − r)) ≥ 0.
Both identities are checked in sympy. At μ = hR both distances equal h, so S^∨ = h⁻²S and t_min = max_{x,y∈S} x·y/h² = R(S)²/h².
∎

**Corollary (cube family).** For the d-cube the nodes are 1, 2, …, d (h = 1) and c = d. With m = ⌊√d⌋, the peak of the
cube–orthoplex line is t_min = m + (√d − m)². This gives 5 − 2√3 for d = 3, 2 for d = 4 (the fixed point is the 24-cell) and
11 − 4√5 for d = 5 (checked exactly).

## 4. Checks (all exact unless marked)

Scripts are in scripts/ and ran on dicto-big-brother (~/geom/bin/python, sympy 1.14, scipy 1.18), in the foreground, each under
4 minutes. Logs are in data/. Q(√5) arithmetic comes from q5.py, copied from studies/2026-11-09-icosahedral-line. Corners are found
by a float half-space intersection, then solved exactly. Each corner is checked exactly against every plane within 10⁻⁶ of it; every
other plane clears it by more than 10⁻⁶ in floats.

- **t1_lines.py** (logs t1_platonic.log, t1_4d_small.log, t1_cell600.log, t1_cell120.log, t1_5d.log). For each line it computes
  the facets and the flag of P, checks the Gram identity, and runs the samples: every node, every turned node, and the
  midpoints and quarter points between them. At each sample it checks:
  - (a) corners of S^∨(μ) = h⁻²·corners of S(c/μ), exactly;
  - (b) t_min = max x·y over all corner pairs, exactly. On the 720-plane lines it is exact on the float-selected near-maximal pairs;
  - (c) t_min equals the closed form and t_min(c/μ).
  It also runs a 4001-point float scan for the argmax and the symmetry. **171 of 171 samples agree; every run FINAL ok.**
- **t2_symbolic.py** (t2_symbolic.log, t2_table.json). It checks:
  - the three identities;
  - the published closed forms, recovered exactly: C–O min(μ, 3/μ, 5 − μ − 3/μ) and D–I (bird 3 Theorem 3, unit form μ_u = μ/√c),
    plus the tetrahedron 3·min(μ, 1/μ);
  - the exact peaks of all 11 regular polytopes in dimensions 3 and 4;
  - the breaks of t_min (one turned pair; none when rA = c);
  - when the min-of-three form is valid;
  - the tangent solid S(hR) by brute force for D, I, C, T, O: every face at distance h, S^∨ = S/h², t_min = R(S)²/h².
  42 checks, FINAL ok. The simplified 600-cell peak was checked by minimal polynomial (FINAL ok).

| P | squared flag radii h² … R² | c = h²R² | hR lies in | peak t_min = (R/r)² of the tangent solid | breaks of t_min |
|---|---|---|---|---|---|
| dodecahedron | 1 + 2√5/5, φ², 3 | 3 + 6√5/5 | first hop | 10 − √5 − √(30 + 6√5) ≈ 1.174819 | 2.170820, φ² |
| icosahedron | 7/6 + √5/2, φ², φ + 2 | 25/6 + 11√5/6 | last hop | the same | φ², 3.157379 |
| cube | 1, 2, 3 | 3 | first hop | 5 − 2√3 ≈ 1.535898 | 3/2, 2 |
| tetrahedron | 1/3, 1, 3 | 1 | node (edge wall) | 3 (octahedron) | 1 only |
| octahedron | 1/3, 1/2, 1 | 1/3 | last hop | 5 − 2√3 | 1/2, 2/3 |
| 5-cell | 1/5, 8/15, 6/5, 16/5 | 16/25 | middle hop, rA = c | 16/5 | none (C¹) |
| tesseract | 1, 2, 3, 4 | 4 | node (square centres) | 2 (24-cell) | 2 only |
| 16-cell | 1/4, 1/3, 1/2, 1 | 1/4 | node | 2 (24-cell) | 1/2 only |
| 24-cell | 1, 4/3, 3/2, 2 | 2 | middle hop, rA = c | 24 − 16√2 = 8(√2 − 1)² ≈ 1.372583 | none (C¹) |
| 600-cell | 7/16 + 3√5/16, 1/2 + √5/6, 5/8 + √5/8, 1 | = h² | last hop | 26 − 2√5 − 10√2 − 2√10 ≈ 1.061173 | 0.904508, 0.947214 |
| 120-cell | 7/2 + 3√5/2, 4 + 8√5/5, 9/2 + 3√5/2, 8 | 28 + 12√5 | first hop | the same | 7.236068, 7.577709 |
| 5-cube | 1, 2, 3, 4, 5 | 5 | middle hop, rA = 6 | 11 − 4√5 ≈ 2.055728 | 2, 5/2 |
| 5-orthoplex | 1/5, 1/4, 1/3, 1/2, 1 | 1/5 | middle hop | 11 − 4√5 | 2/5, 1/2 |

Dual pairs give the same family of solids read in the opposite direction (up to scale), so they have the same peak. The breaks listed for the 5-cube and the 5-orthoplex come from the closed form, which t1 checked at 40 exact samples; t2 covers dimensions 3 and 4. The self-dual polytopes
(tetrahedron, 5-cell, 24-cell) have nodes closed under the turn: their walls and the antipol's walls coincide.

## 5. What does not generalise

- **Non-regular P.** The turn exists only for regular P (dual-sweeps theorem: one face distance and one corner radius). The proof
  needs it twice: one face orbit and one corner orbit make Lemma 3 a single simplex cut by one plane, and the flag makes the Gram
  matrix the min-kernel of Lemma 2. On CO ∩ μ·RD and ID ∩ μ·RT only the local turn at the jump survives.
- **Theorem 1's Cauchy–Schwarz route fails.** t_min ≤ R(S)·R(S^∨) = R(S(μ))·R(S(c/μ))/h² is too weak to locate the peak. R(S(μ))² is
  piecewise quadratic, convex inside each hop and equal to μ at the nodes, so log R is not concave. On the cube line at μ = 2 the
  bound gives 2·1.25 = 2.5 > (5 − 2√3)² ≈ 2.359. The proof has to use the bilinear form itself, through the probability form.
- **min(μ, c/μ, g(μ)) is not always the closed form.** It holds on the whole line only when hR lies in the first or the last hop, or
  is a node. That covers all of 3D, the tesseract, the 16-cell, the 600-cell and the 120-cell. It fails for the 5-cell, the 24-cell,
  the 5-cube and the 5-orthoplex: there g < μ below min(r, c/A), and the piecewise form of part 2 is needed.
- **The ends.** On the line t_min → 1 at both ends, because S^∨ keeps the planes that just touch there. The end solids taken alone
  have t_min = (R/h)², for example 3 and 3 on the C–O line. The antipol is discontinuous at the ends.
- **Tangent solid vs. the extreme of #43.** The peak value is (R/r)² of the tangent solid S(hR). This is not the universal
  constant of #43 Theorems 2–4 (9, 3, 15 − 6√5), which bounds all polytopes with a given symmetry.

## 6. Paragraph for the Hopscotch foundations paper

DICTO proposed the turn: at the end of the hopscotch one jumps around and comes back. On the polar line S(μ) = P ∩ μP* of a regular
polytope P with inradius h and circumradius R, the turn is exact. The antipol of S(μ) is S(h²R²/μ), scaled by 1/h². Its fixed point
μ = hR is the solid whose faces all touch one sphere. The containment constant t_min = max x·y over S × S^∨ is largest there, and only
there, with value (R/r)² of that tangent solid. This is the equality case of the bound t_min ≤ (R/r)². The proof reduces everything
to the characteristic simplex of the flag, where the squared flag radii ρ_k² form a min-kernel, q_j·q_k = ρ²_{max(j,k)}. Each point
of S becomes a random variable on the squared flag radii, and t_min becomes the largest E min(U, V) for two independent variables
with means μ and h²R²/μ. Convex order makes the maximiser the two-point law between neighbouring radii. An AM–GM inequality then puts
the maximum at the turn, and log t_min is concave in log μ. The walls of S are the squared flag radii, and the walls of its antipol
are their turns. t_min breaks at a single turned pair, one wall of S and one wall of S^∨, and is smooth (C¹) on the self-dual lines
of the 5-cell and the 24-cell. The theorem holds in every dimension. On the tesseract line the turn is the 24-cell (t_min = 2). On
the 600-cell line the peak is 26 − 2√5 − 10√2 − 2√10.

## 7. LEADS

1. **The two-depth plane of RD and RT** (dual-sweeps LEAD 3). With two corner orbits, Lemma 4 becomes a two-variable law. Does the
   local turn √(ρ²f) come out as a convex-order optimum in the same way? (closed form of dual-sweeps LEAD 2)
2. **Quasi-regular P with a midsphere** (cuboctahedron, icosidodecahedron). The chamber slice is still
   one simplex but has two face orbits. Test whether t_min peaks at the solid with all faces tangent. Dual-sweeps says not on CO–RD
   (peak √(12/5)); find the rule.
3. **All dimensions, three infinite families.** The d-cube corollary m + (√d − m)² is proved. Write the d-simplex and the
   d-orthoplex lines the same way, from their flag radii. The simplex nodes are closed under the turn.
4. **The beat line (#43 Theorem 3)** has a turn too, fixed point 5/2 (icosahedral-line bird 4). Test whether a convex-order form
   exists there.
5. **Kepler–Poinsot and star polytopes.** The flag still exists, but the solid is not convex. Find out what replaces form (B).

## 8. Concordance ledger line

{"question": "Hopscotch Turn Theorem: on the polar line S(mu) = P cap mu P* of a regular polytope, does the antipol turn mu -> c/mu hold and is t_min largest at its fixed point, in general", "method": "proof: chamber slice by the dominance lemma, flag Gram identity q_j.q_k = rho^2_max(j,k), points as random variables on the squared flag radii, convex order (bracketing two-point law), AM-GM / log-concavity in log mu; exact checks Q(sqrt5) at 171 samples on 13 lines (5 Platonic, 6 regular 4-polytopes, 5-cube, 5-orthoplex) + sympy identities and published closed forms (studies/2026-11-09-turn-theorem)", "status": "SETTLED", "result": "PROVED for every regular convex polytope, any dimension: S(mu)^v = h^-2 S(c/mu), c = h^2R^2; h^2 t_min = E min(U_mu, U_c/mu) (two-point laws on bracketing flag radii) = r + (mu-r)(c/mu-r)/(A-r) in a common hop, min(mu, c/mu) otherwise; log t_min concave in log mu, unique max at mu = hR (all faces tangent), value (R/r)^2 of the tangent solid; walls of S = squared flag radii (dual-sweeps LEAD 1 for regular P), walls of S^v = their turns; t_min breaks at one turned pair (none if rA = c: 5-cell, 24-cell; only hR if a node: T, tesseract, 16-cell). Peaks: D,I 10-sqrt5-sqrt(30+6sqrt5); C,O 5-2sqrt3; T 3; 5-cell 16/5; tesseract/16-cell 2 (24-cell); 24-cell 24-16sqrt2; 600/120-cell 26-2sqrt5-10sqrt2-2sqrt10; d-cube m+(sqrt d-m)^2. Cauchy-Schwarz route fails (cube mu=2); min-of-three form fails when hR is in a middle hop (5-cell, 24-cell, 5-cube)", "retry": "never; only LEAD 1-2 (two-depth / quasi-regular lines) or LEAD 5 (star polytopes)", "study": "studies/2026-11-09-turn-theorem", "date": "2026-11-09"}
