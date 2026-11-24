# One fair die for every balanced set of face directions (24 November 2026)

DICTO · dictospheres.com · study 2026-11-24-aequi-uniqueness · with Claude (Anthropic).

**Result.** The observation behind the Aequi catalogue (about 9 500 orbit sets searched, continuous off-axis
families included, and every set with exactly one fair die) is now a theorem. It holds for every set of face
directions whose unit vectors add up to zero. In particular it holds for every union of orbits of a finite group
that fixes only the centre.

- **Uniqueness** (any number of fair dice ≤ 1, over all depth vectors, not only inside a search box) is Alexandrov's
  uniqueness theorem applied to the polar. This is #112 Theorem A (a). It is already proved in Lean:
  `fair_die_unique` in study 2026-11-22-lean-alexandrov, `Alexandrov/Dice.lean`.
- **Existence** is new here (Theorem B below). Alexandrov's condition for equal masses holds automatically when the
  directions are balanced. #112 had this only for directions in opposite pairs (Corollary 3), and so only for groups
  containing the central inversion. Theorem B covers every group fixing only the centre: T, O, Td, D_n, D_nd, D_nh,
  S_4, S_6, … as well.

So the contribution is the existence half. The uniqueness half is Alexandrov's theorem, credited as such.

## Setting

n_1, …, n_N are distinct unit vectors, not all in one closed hemisphere, and d_k > 0. The die is
P = {x : n_k·x ≤ d_k}. It is fair about 0 when every face subtends Ω_k = 4π/N. Since 4π/N > 0, **a fair die has every
face present**, and no face can be missing.

## What was already proved (checked first)

- #112 Lemma 1 (the polar identity): Ω_k equals the curvature of P° = conv{n_k/d_k} at the corner n_k/d_k.
  In Lean this is `solidAngle_eq_curvature`.
- #112 Theorem A:
  - (a) A fair die exists iff μ = (1/N)Σδ_{n_k} satisfies Alexandrov's condition. It is then unique up to scale.
  - (b) Its symmetry group is the group of the directions.
  - (c) If that group fixes no direction, the centroid is 0.
  - In Lean, (a) is `fair_die_iff` and `fair_die_unique` (built on `alexandrov_iff` and `alexandrov_unique`:
    M10, M11, 0 sorry). (b) and (c) are not yet in Lean.
- #112 Proposition 2: the condition fails iff some set A of a directions lying in an open hemisphere has
  g(A) = 2π(2a − N)/N − L(A) ≥ 0. Here L(A) is the perimeter of the spherical convex hull of A (Girard).
- **Answer to "is fair_die_iff exactly this?"**
  - Uniqueness: yes. `fair_die_unique` is the uniqueness theorem in full: in all of (0,∞)^N, every face present.
  - Existence: no. `fair_die_iff` reduces existence to Alexandrov's condition, but it does not decide the condition
    for any set. Theorem B decides it for balanced sets.

## Why one depth per orbit loses nothing

Let G be a finite group whose maps permute the directions, and P the unique fair die. Each g in G carries P to a
fair die gP with the same directions, so gP = λP by uniqueness. The volumes are equal, so λ = 1 (#112 Theorem A (b)).
Hence d_{g(k)} = d_k: the depth is constant on every G-orbit. The symmetric search (one depth per orbit, the
Krawczyk-certified boxes of study 2026-11-24-aequi-certify-extend) therefore finds the one fair die of the whole
problem, and no fair die is missed outside the box.

## Theorem B (balanced directions carry a fair die)

**Theorem B.** Let n_1, …, n_N (N ≥ 4) be distinct unit vectors with Σ n_k = 0, not all on one great circle. Then
Alexandrov's condition holds for μ = (1/N)Σδ_{n_k}. Hence there is a die with these face normals that is fair about
0, every face present, and it is unique up to scale.

**Corollary B1 (the Aequi).** Let G be a finite orthogonal group fixing only 0, and take any union of G-orbits of
directions that does not lie in one plane. Then it carries exactly one fair die up to scale. That die has one depth
per orbit and its centroid at the centre. *Proof:* Σ n_k is fixed by G, so it is 0. Then apply Theorem B, the orbit
argument above, and #112 Theorem A (c). ∎

This explains both halves of what every search saw for groups fixing only the centre: "never two" (Alexandrov) and
"never none" (Theorem B). It covers both icosahedron placements, all 16 subgroup classes of Part 2, and the
continuous off-axis families of Part 2(c): every parameter value gives a balanced set, so every value has exactly one
fair die.

### Proof

By #112 Proposition 2 it is enough to show g(A) < 0 for every set A of the directions that lies in an open
hemisphere. Write a = |A| and b = N − a.

**Step 1 (the centre of A).** Choose a unit vector c that maximises t = min_{n∈A} n·c. Since A lies in an open
hemisphere, t > 0. Write t = cos R with 0 ≤ R < π/2. This is a convex program (maximise t subject to n·c ≥ t for n
in A and |c| ≤ 1), and Slater's condition holds. Its KKT conditions give c = Σ λ_n n, with λ_n ≥ 0 and the sum
taken over the active points (n·c = cos R). There are three cases:
- If only one point is active, then c is that point. So R = 0 and A is that single point, a = 1.
- Otherwise c lies in the spherical hull of two active points p, q, or of three active points p, q, r.

**Step 2 (balance gives b ≥ a cos R).** Σ_{n∉A} n = −Σ_{n∈A} n, so b ≥ |Σ_{n∈A} n| ≥ Σ_{n∈A} n·c ≥ a cos R.

Since (a − b)/(a + b) decreases in b,

  (2a − N)/N = (a − b)/(a + b) ≤ (1 − cos R)/(1 + cos R) = tan²(R/2).

**Step 3 (perimeter ≥ 4R).**
- *Two active points.* c lies on the minor arc pq, at distance R from each end, so the arc pq has length 2R. Each
  of the two boundary paths of the hull between p and q is at least 2R long, so L(A) ≥ 4R. (For an arc, L is twice
  its length, as in Proposition 2.)
- *Three active points.* p, q, r lie on the circle of radius R about c, at azimuths with gaps φ_1, φ_2, φ_3 around c.
  Each gap is at most π (c lies in their hull) and the gaps add up to 2π. The side opposite gap φ has length
  s(φ) = 2 arcsin(sin R · sin(φ/2)), from cos s = cos²R + sin²R cos φ.
  - s is concave on [0, π]. With h(x) = arcsin(α sin x), α = sin R < 1:
    h''(x) = α(α² − 1) sin x / (1 − α² sin² x)^{3/2} ≤ 0.
  - A concave function on the polytope {0 ≤ φ_i ≤ π, Σφ_i = 2π} takes its minimum at a vertex, a permutation of
    (π, π, 0). So per(pqr) ≥ s(π) + s(π) + s(0) = 4R.
  - The triangle pqr lies in the hull of A. Their polar polygons are therefore nested the other way, and Girard's
    formula (area of polar = 2π − perimeter, as in Proposition 2) gives L(A) ≥ per(pqr) ≥ 4R.

**Step 4 (conclusion).**
- For a = 1: g = 2π(2 − N)/N < 0, since N ≥ 3.
- For a ≥ 2, so that 0 < R < π/2: Steps 2 and 3 give g(A) ≤ f(R) with f(R) = 2π tan²(R/2) − 4R.
  - f(0) = 0.
  - f(π/2) = 2π − 2π = 0.
  - f'' = 2π (d²/dR²) tan²(R/2) > 0, since tan²(R/2) is strictly convex on [0, π/2).
  - So f < 0 on the open interval (0, π/2), and g(A) < 0.

So the condition holds, and Theorem A (a) gives existence and uniqueness. Balanced and not all on one great circle
means not in any closed hemisphere: if n·u ≥ 0 for all n and Σ n·u = 0, then every n·u = 0. ∎

*Remark.* The constant is sharp in the limit only: f → 0 as R → π/2. The inequality is strict for every finite set.

### Consistency check against the 87 failures (scripts/sums.py, data/sums-alexandrov-sets.csv)

Study 2026-11-20-aequi-alexandrov found 87 orbit sets (groups C_n, C_nv, C_s, which fix a line or a plane) that
fail Alexandrov's condition. Theorem B predicts that each of them has a nonzero vector sum. All 369 sets of that
study were checked (319 without a die in the box, plus 50 controls):
- Every set that could be failing (165 sets, matched conservatively by group, orbit families and N) has
  |Σ n| ≥ 0.3135. The error of the double-precision sum is below 4e-14, so these sums are certainly nonzero.
- The only 3 sets with Σ n = 0 are controls that hold.
- Output: FINAL ok.

## How a face disappears (the question asked)

- *At a fair die:* never. Every face has Ω = 4π/N > 0, so every given direction is a true face.
- *Along the search:* a depth vector at which some orbit's faces vanish is not fair for that orbit set. Its solid
  angles belong to the smaller set, which has its own N and its own unique fair die. So "every orbit's faces present"
  is not an extra hypothesis; it is forced.
- *Type changes inside the space of depths:* the walls of Part 1 and Part 2 of study 2026-11-24-aequi-certify-extend
  (where corners with four planes appear) change the combinatorial type, not the set of faces. Uniqueness does not
  depend on the type, because Alexandrov's theorem is global. The exact-equality questions there (CIRT-30, the
  rows on walls) are about where the unique point lies, and they stay open.

## The routes checked

- **Polar and Alexandrov (used).** A fair die is Alexandrov's prescribed-curvature problem for the polar, with equal
  masses at the given directions. This is #112 Lemma 1 and Theorem A, after Alexandrov (1942), Oliker (2007,
  Theorems 4 and 6) and Bertrand (2016, Theorem 1.2). The uniqueness is theirs.
- **Variational route.** Oliker's functional Φ(ψ) = ∫ log max_k (n_k·u)e^{−ψ_k} dσ + (1/N)Σψ_k is convex in the log
  depths, with gradient 1/N − Ω_k/4π. Existence comes from coercivity, which is exactly Alexandrov's condition.
  This is the proof formalised in Lean, M9 and M10. Theorem B supplies the condition.
- **Monotonicity (M-matrix).** ∂Ω_k/∂d_j ≥ 0 for j ≠ k (pushing a neighbour out gives face k more sky), and
  Σ_j d_j ∂Ω_k/∂d_j = 0 (scaling). So −J is a singular M-matrix with kernel spanned by d, which gives local
  uniqueness. Global injectivity is the maximum-principle argument of the Lean `alexandrov_unique`. Nothing beyond
  Alexandrov is needed.
- **Degree theory.** It is not needed once the variational existence is available.

## Sources checked

- #112 (papers/2026-11-20-aequi, paper.html): Lemma 1, Theorem A, Proposition 2, Corollaries 3, 3′, 4.
- Lean study 2026-11-22-lean-alexandrov: Main.lean (`AlexandrovCondition`, `alexandrov_iff`, `alexandrov_unique`),
  Dice.lean (`fair_die_iff`, `fair_die_unique`), Margin.lean (`nbhd`).
- A. D. Aleksandrov, Doklady 35 (1942): not opened (cited via the next two, as in #112).
- V. Oliker, Adv. Math. 213 (2007), arXiv:math/0701398.
- J. Bertrand, Geom. Dedicata 183 (2016), arXiv:1505.04821.
- V. Semenov, The discrete Gauss image problem, arXiv:2210.16974v2 (2024), **full text read** (24 Nov). Its problem has the
  *target* measure λ discrete (finitely many prescribed normals u_j), not spherical Lebesgue measure. Main result (Theorem 1.1):
  for µ discrete, not concentrated on a closed hemisphere, and λ discrete equal-weight, edge-normal loop free, a solution exists
  iff µ and λ are *weak* Aleksandrov related (Definition 3.2, µ(ω) ≤ λ(ω^{π/2}) for compact spherically convex ω), proved through
  an assignment functional and Hall's marriage theorem (Lemma 4.3); uniqueness is of the assignment function (Theorem 1.2), and a
  solution is never unique as a body (Proposition 5.12). No criterion in terms of Σ n_k, a barycentre or a centroid, and no
  sufficient condition that makes the Aleksandrov relation automatic, appears anywhere in the text (searched also for "balanc",
  "barycent", "centroid", "sum").
- V. Semenov, The Gauss image problem with weak Aleksandrov condition, arXiv:2210.16778v3 (2024), **full text read**.
  Theorem 1.4: µ discrete, not concentrated on a closed hemisphere, λ absolutely continuous, µ weakly Aleksandrov related to λ ⇒
  a polytope P with vertices in the directions of µ solves µ = λ(P, ·). With λ = spherical Lebesgue measure this is our setting
  (the polar of the die), but the hypothesis is the (weak) Aleksandrov relation itself; it is not decided for any class of µ.
- K. J. Böröczky, E. Lutwak, D. Yang, G. Zhang, Y. Zhao, The Gauss image problem, Comm. Pure Appl. Math. 73 (2020),
  doi:10.1002/cpa.21898 (free preprint on the NSF public-access repository, **full text read**). Theorem 1.1 (existence for λ
  absolutely continuous under the Aleksandrov relation), Theorem 1.2 (necessity and uniqueness up to dilation when λ is positive
  on open sets). The one class of µ for which the relation is shown to hold automatically is **even** measures: Lemma 5.6
  ("even Borel measure … not concentrated on any great hypersphere … with |µ| = |λ| … are Aleksandrov related"), giving
  Theorems 1.3 and 8.5 (origin-symmetric solutions). For equal point masses this is exactly #112 Corollary 3 (directions in
  opposite pairs).
- J. Bertrand, On the Gauss image problem, arXiv:2308.15810 (2023), **full text read**: Theorem 1.5, existence for λ
  absolutely continuous and µ not concentrated on a closed hemisphere under the weak Aleksandrov condition (optimal transport);
  no balanced or barycentre criterion.
- Followed from Semenov's references: Y. Zhao, The L_p Aleksandrov problem for origin-symmetric polytopes, arXiv:1803.10839 /
  Proc. AMS 147 (2019) (abstract: origin-symmetric, i.e. even, case only); Oliker (2007) and Bertrand (2016) above.
- Web searches: "Alexandrov condition … discrete measure barycenter zero equal masses sufficient"; "Aleksandrov integral
  curvature problem discrete measure equal masses centroid/barycenter at origin sufficient condition existence polytope"
  (no such statement found).

**Finding (24 Nov).** Theorem B is not stated, nor any equivalent, in the five full texts read or in the works they cite that
were checked. The nearest result is Böröczky–Lutwak–Yang–Zhang–Zhao, Lemma 5.6: **even** measures (with λ even, positive on
open sets) are Aleksandrov related. **How ours differs:** Theorem B assumes only that the N equal point masses are *balanced*,
Σ n_k = 0 (and not all on one great circle). An even set of directions is balanced, but a balanced set need not be even: for example the four face
normals of a regular tetrahedron, the three side normals of a triangular prism (D3h), and many orbit sets of T, Td, D_n, D_nh
(n odd) and S_4 among the Aequi are balanced and not symmetric under −1.
So Theorem B extends the even case (BLYZZ Lemma 5.6 for equal masses; #112 Corollary 3) to all balanced equal-mass sets; its
proof (Steps 1–4 above) uses the equal masses and the perimeter bound, and does not extend to arbitrary balanced weights as
stated (LEAD 2). Semenov's papers and Bertrand's note treat the relation as a hypothesis and give no class of measures that
satisfies it. Priority is still **not claimed** beyond this: the result was not found in the sources checked.

## LEADS

1. Done 24 Nov: Semenov arXiv:2210.16974 and 2210.16778, BLYZZ (2020) and Bertrand (2023) read in full; Theorem B not found (Sources checked). Cite BLYZZ Lemma 5.6 as the even case at the point of use in #112.
2. Weighted version: Σ κ_k n_k = 0, Σκ_k = 4π and every κ_k < 2π should give the condition by the same Steps 1–4.
   For non-discrete measures, check the perimeter facts for general convex ω. This is not claimed.
3. Formalise Theorem B in Lean on top of `fair_die_iff`. It needs:
   - Girard's formula for the polar polygon, in the volume form of `nbhd`;
   - the KKT centre;
   - the concavity bound.
   With it, Corollary B1 becomes a Lean theorem, `balanced → ∃! fair die`.
4. Into #112 at its next version (rule: closed gaps into the home paper):
   - Theorem B replaces Corollary 3 (opposite pairs) as the general case.
   - Corollary 4 (a) becomes "exactly one" in place of "at most one".
   - The searches' "never none" becomes a theorem.
