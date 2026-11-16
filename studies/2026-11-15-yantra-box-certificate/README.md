**Verdict: FEASIBLE, and the certificate is built and checked.** Kulaichev's yantra is unique by a branch-and-bound interval certificate that uses no elimination identity. It has 64,613 rational boxes in 10 charts and 68,041 polynomial evaluations (18.4 million term evaluations). Every box endpoint has at most 9 digits. Each box is closed by one sign test. One box of half-width 2⁻²² is left over, and the Krawczyk test in exact rational arithmetic proves that it holds exactly one solution, Theorem 10's. Every box was re-proved in exact integer arithmetic. Every box was then re-proved independently in FLINT/Arb ball arithmetic, with a different enclosure, on the second compute machine. Both negative controls fail as they must.

**Lean status (16 Nov 2026): the whole theorem is proved in Lean.** `YantraCert.Y.kulaichev_unique : ∃! y : Yantra, y.Huet ∧ y.Kulaichev ∧ y.Admissible` and `YantraCert.Y.kulaichev_slope` (w7/b7 lies in an interval of width 2⁻²¹ around 0.75043851602221…) are proved over Lean 4 + Mathlib v4.35.0-rc2, the Palomar toolchain, with no `sorry` and no `native_decide`. `#print axioms` lists only `propext`, `Classical.choice` and `Quot.sound` for both. All four steps of the plan are done (§7):
- **Step 1, the certificate.** The 64,613 boxes in 10 charts pass `decide +kernel`, through a checker that is proved sound.
- **Step 2, the derivation.** A verified sparse-polynomial normaliser checks every identity between the geometry and the stored polynomials. It covers 24 construction steps (the divisor lemma, made mechanical), the three equations, the pull-backs, the 36 tests, the chart identities and the rescalings.
- **Step 3, the coverings and box bounds.** The box bounds and the chart coverings are proved, and the case split over the charts is assembled.
- **Step 4, the Krawczyk box.** It is proved: contraction for uniqueness, Banach's theorem for existence.
- **Existence.** The figure rebuilt from the zero of F~ is proved to meet every condition.

The Palomar entry passes the local preflight (§7, milestone 11): Palomar's source check, a clean build and clean axioms, and the comparator, where Lean's kernel, NanoDa and con-ron all accept the solution.

A Lean pilot on the same toolchain measured the cost. The soundness of the box evaluator is proved in Lean. 1000 boxes of the certificate pass `decide +kernel` in 18 s of kernel time (no `native_decide`). The slope-form checker costs about 1 s per box of the largest polynomial. So the whole certificate is roughly 10 to 12 core-hours of kernel time, split into files that check in parallel (about 1.5 h on the 24-core compute machine): it fits a kernel check. What remains for a Palomar entry is listed under **Next steps**.

# A box certificate for the uniqueness of Kulaichev's Śrī Yantra (study 2026-11-15)

DICTO, 15 Nov 2026: "make it so". This replaces the one step of the uniqueness proof (studies/2026-11-15-yantra-uniqueness, ledger [240]) that is too large for a Lean kernel. That step is the eliminant identity: degree 1744, with cofactors from a 40 × 40 Sylvester matrix. The certificate here is a branch-and-bound interval proof. Each step is a sign check on a rational box, so a kernel can repeat it with integers.

## The theorem certified

The statement is the theorem of studies/2026-11-15-yantra-uniqueness: Huet's conditions (Chiodo's form), Kulaichev's (a)–(d), and #103 Theorem 1 admissibility. Then there is exactly one figure, Theorem 10's yantra, with u = 0.7504385160222140244…

## 1. The system and the box

- **Unknowns.** These are the census's u = w7/b7, t = b1/w1 and S = b9. The equations are its system after the divisor lemma (s1_system.py): G = 0 for (c), H1 = 0 for marma (1,4,6), and D = 0 for (d) squared. They are copied in inputs/system-K.txt.
- **Box coordinates** (scripts/b1_polys.py):
  - t = u·τ;
  - S = R + ρ(1 − u)(1 − R), with R = b7 = 1/(1 + u²).
- **Why the box holds every admissible yantra.** The box is 0 ≤ u ≤ 1, 0 ≤ τ ≤ 1, 0 ≤ ρ ≤ 6, and every admissible yantra lies inside it:
  - 0 < u because w7 > 0.
  - u < 1 because b3 < b7: P = u²/(1+u²) < R = 1/(1+u²).
  - 0 < τ because w1 > 0.
  - τ < 1 because b1 < b3: t²/(1+t²) < u²/(1+u²).
  - 0 < ρ because b7 < b9.
  - ρ < 5. First, b9 < 1 gives ρ(1 − u) < 1, so ρ < 5 when u ≤ 4/5. Second, t9's corner lies in the closed disc, so w9 ≤ 1/2. The construction gives w9 = u⁵ρ / ((1+u²)(1+u)), so ρ ≤ (1+u²)(1+u)/(2u⁵). This bound decreases in u and equals 4.504 at u = 4/5.
- **The equations in box coordinates.** Each equation is pulled back and multiplied by (1+u²)^deg_S. Its factors u, 1 − u and 1 + u² are dropped; they are nonzero inside the box. This leaves F~ = (G~, H~, D~), with integer coefficients. The terms are 13, 522 and 359, and the degrees (u, τ, ρ) are (8,0,2), (26,10,3) and (26,10,2).
- **Admissibility tests.** There are 36. They are #103 Theorem 1's list as in s3_backsolve.py:
  - b_i < b_{i+1};
  - w_i > 0;
  - each apex on its side;
  - the corners of t2, t4, t5, t6, t8 and t9 in the closed disc;
  - b5 < 1/2 < Q, which undoes the squaring in (d).
  
  Two tests are added: b9 < 1, and b3 < b6. The second is the same as c138 > 0, because (Q − P)·c138 = xZ(P − b1)².
- **How a test is stored.** Each quantity q is written as c·E·N/D. Here E collects the factors that are positive inside the box. For a strict test, E also collects factors of even power.
  - For the closed-disc tests, even powers are kept in N and D. There q = 0 is allowed, so a vanishing square must not be dropped. This was found and fixed before the final run (job yboxcert2).
  - A box on which N and D have opposite fixed signs has q < 0 everywhere on it, so it holds no admissible yantra.

## 2. Where F~ vanishes on the boundary, and the corner charts

- **The face analysis.** It is in scripts/explore/, x4–x6.
  - On the closed box, F~ = 0 has exactly two boundary points: (u, τ, ρ) = (0, 0, 1) and (1, 1, 2).
  - On u = 1, G~ = ρ² − 4 and gcd(H~, D~) = ρ(1 − τ²)⁴. On u = 0, G~ = ρ − 1 and gcd(H~, D~) = τ².
  - The other faces carry no common zero.
- **Why charts are needed.** At these two points every equation and every test vanishes, so no box touching them can be closed. They are resolved by blow-up charts (scripts/b1_charts.py). Each chart is a polynomial map from a parameter box with parameters ≥ 0. The pulled-back functions are divided by the largest power of each parameter, which is positive inside the chart.
- **Corner (1, 1, 2).** Homogeneous blow-up. Chart A is u = 1 − x, τ = 1 − xθ. Chart B is u = 1 − yη, τ = 1 − y. Each has x, y ≤ 1/8 and θ, η ∈ [0, 1], and together they cover [7/8, 1]² × [0, 6]. Chart A closes with one box: Q < 1/2 on the whole chart.
- **Corner (0, 0, 1).** Here the yantra collapses and the corner is very degenerate.
  - On G = 0, D~ behaves like (τ − u⁴)² and H~ like −2τ³ − u¹².
  - The thin wedge τ ≈ u⁴ is where the marma (1,3,8) coefficient c138 ≈ u(τ − u⁴) changes sign.
  - It is resolved by a weighted tower of seven charts:
    - **C1:** u = s, τ = s⁴θ, with s ≤ 1/4 and θ ≤ 2.
    - **C2:** u = sη, τ = s⁴, with s ≤ 1/2 and η ≤ 27/32. C1 and C2 together cover [0, 1/4] × [0, 1/16] × [0, 6].
    - Inside C1, the neighbourhood N1 = [0, 1/16] × [1/2, 3/2] × [1/2, 3/2] of the point (s, θ, ρ) = (0, 1, 1) is covered by the weighted blow-up along the curve θ = 1, ρ = 1 + s. The weights are (s, θ − 1, ρ − 1 − s) = (1, 4, 2), with the weighted size ν = max(s, (|θ − 1|/4)^{1/4}, (|ρ − 1 − s|/4)^{1/2}).
    - **W** (ν = s): θ = 1 + s⁴ζ and ρ = 1 + s + s²x, with ζ, x ∈ [−4, 4].
    - **Wt±** (ν from θ): θ − 1 = ±4σ⁴, s = σa, ρ − 1 − s = 4σ²x, with a ≤ 1 and |x| ≤ 1.
    - **Wr±** (ν from ρ): ρ − 1 − s = ±4σ², s = σa, θ − 1 = 4σ⁴ζ, with a ≤ 1 and |ζ| ≤ 1.
    - The bounds σ ≤ 3/5 for Wt± and σ ≤ 3/8 for Wr± follow from N1's extent.
  - In W at s = 0 the leading terms are G ∝ x − 1, D ∝ (ζ + x − 2)² and H ∝ −x(ζ + 1). The tower ends there because H stays away from 0 on D's zero curve. Points with s = 0 have u = 0, so they are not admissible.
- **Choosing the coordinates.** Every covering claim above is a case split on which of the weighted sizes is largest, with real 4th and square roots. That is the hand-written part of the proof (§ Next steps). The order of the tower was read off the Newton polygons (scripts/explore/x8, x10–x13). The windows come from the tests c138 > 0, Q > 1/2 and Q < R.

## 3. The certificate

- **Generator** (scripts/b2_bnb.py). Bisection runs on the coordinate of least depth, lowest index first. A box is closed by the first test that holds on it: G~, then H~, then D~, then the admissibility tests from smallest to largest. Holes are covered elsewhere: the Krawczyk box, the corner holes and N1. Floating point only chooses the boxes; it proves nothing.
- **Enclosure.** All coordinates are ≥ 0. Two enclosures are used:
  - the monotone split p⁺(lo) − p⁻(hi) ≤ p ≤ p⁺(hi) − p⁻(lo), which is Moore's natural extension in this form;
  - the slope form of Krawczyk and Neumaier (1985), p = p(m) + Σ_j (y_j − m_j)·A_j, with x^a − m^a = (x − m)·Σ_k x^k m^{a−1−k}, where the A_j are bounded by the monotone split. On the half-grid of the cell centre this is pure integer arithmetic, because H − M = M − L = 1.
- **Krawczyk box** (scripts/b3_krawczyk.py). It is the dyadic box of half-width 2⁻²² around Theorem 10's (u, τ, ρ) = (0.75043851602221402440608, 0.45221118447869732890388, 3.11791257983550903598). The method is R. Krawczyk (1969), in the uniqueness form of Moore (1977) and Neumaier (1990, Thm 5.1.7). J(X) is enclosed by the monotone split, Y is a 2⁻⁶⁰-dyadic rounding of J(y)⁻¹, and all arithmetic is exact rational.
  - K(X) lies inside int X, with width ratios 0.051, 0.125 and 0.125.
  - The census point (the 60-digit census value, itself certified there in a box of radius 1e-300) lies in X.
- **Exact checker** (scripts/b4_check.py). It rebuilds the bisection tree from the root box, using the same split rule, so the leaves are shown to cover the box. It then re-proves each leaf's test in integer arithmetic, trying the monotone split first and the slope form second. Holes are checked by exact rational comparison.

| chart | leaves | evaluations | term evaluations | max endpoint digits | max coefficient digits | closed by |
|---|---|---|---|---|---|---|
| main | 46,037 | 48,891 | 12,391,498 | 9 | 4 | G~ 17624, H~ 16986, D~ 8481, tests 2900, holes 38 + 8 |
| A | 1 | 2 | 63 | 1 | 10 | Q > 1/2 |
| B | 85 | 136 | 12,991 | 1 | 25 | G~ 34, tests 51 |
| C1 | 18,194 | 18,668 | 5,633,402 | 5 | 32 | H~ 9049, G~ 6400, D~ 2263, tests, N1 |
| C2 | 1 | 2 | 16 | 1 | 15 | Q > 1/2 |
| W | 90 | 93 | 91,152 | 2 | 108 | G~, H~, b6 < b7, D~ |
| Wt+ | 187 | 215 | 227,734 | 2 | 68 | D~, H~, G~, tests |
| Wt− | 16 | 32 | 5,023 | 1 | 43 | w4 > 0, b3 < b6 |
| Wr+ | 1 | 1 | 20 | 1 | 9 | G~ |
| Wr− | 1 | 1 | 20 | 1 | 9 | G~ |
| **total** | **64,613** | **68,041** | **18,361,919** | **9** | **108** | |

These counts are from the final job yboxcert2, which ended FINAL ok (data/certificate-size.json; data/poly-sizes.json for the coefficients). The polynomials have up to 2551 terms and total degree 151 (chart Wt+). The first run, yboxcert, came before the closed-disc fix and had 64,485 leaves. It was also checked in full, and only the main chart and chart B changed.

## 4. Controls

- **Semantic control of the derivation** (scripts/b4b_semantic.py). This is pure Python with no Sage. At up to 400 leaf centres per test per chart, the yantra is rebuilt from the geometry in exact rationals.
  - Each claimed failing admissibility quantity must be < 0 at those centres.
  - The original G, H1, D must be nonzero there, and the sign of F_orig / F_chart must be the same throughout a chart.
  - Result: no contradiction. This covered 2724 centres in the main chart and 1678 in C1, and every leaf of the other charts.
- **Negative control (a): a perturbed system.** The main certificate was checked against G~ + 2⁻²⁰ and is rejected: 354 of its 46,037 leaves fail. The Krawczyk test on G + 2⁻²⁰ also fails.
- **Negative control (b): equations only.** The generator was run with every admissibility test removed. The cover then stays open at 20 boxes, and all of them lie within 10⁻³ of the census's non-admissible solution (u, τ, ρ) = (0.668656, 0.188438, 2.78081), the u = 0.66866 root of f348 where t4 turns over. So the admissibility tests carry real weight, and the equations alone have no other zero in the box.
- **Independent re-check** (scripts/b5_arb.py, FLINT/Arb by F. Johansson through python-flint, 320 bits, on the second compute machine). This uses a different enclosure: Moore's centred (mean-value) form, with the gradient over the box in ball arithmetic. A leaf that is inconclusive is split into 8, at most twice. Every leaf of every chart is confirmed. Job yboxarb2 on the final certificate ended FINAL ok: 46,037/46,037 in the main chart (13,746 needed a split), 18,194/18,194 in C1 (6638 split), and 85 + 187 + 90 + 16 + 1 + 1 + 1 + 1 in B, Wt+, W, Wt−, A, C2, Wr+ and Wr−. Job yboxarb had confirmed the first certificate in the same way.

## 5. Lean pilot

The pilot used Lean 4 v4.35.0-rc2 with Mathlib, the toolchain of the local Palomar project. The source is lean/BoxCheck.lean, with the generator scripts/b6_lean_export.py and the runner scripts/lean_pilot.sh.

- **Proved.** The monotone-split evaluator is sound: `BoxCheck.bounds`, then `no_zero` and `no_zero_all`. If a leaf passes `signFixed`, the polynomial has no real zero in that leaf. The proof is by induction over terms; each term is bracketed by its corner values. It compiles in 4 s.
- **Proved and kernel-checked** (lean/ProvedG1000.lean, generated from the first certificate's main chart). 1000 leaves of the main certificate pass `theorem LM_ok : LM.all (signFixed Dx Dy Dz P) = true := by decide +kernel`, with no `native_decide`, and the corollary `LM_no_zero` follows. The polynomial is G~ on these leaves. This took 21.9 s, of which 18 s is kernel, with a peak of 8 GB.
- **Timed.** The Nat-only slope checker is not yet proved sound. Job yboxlean (FINAL ok, data/lean-pilot.json) ran it on 500 leaves closed by H~ (522 terms, the largest polynomial in the main chart), in 10 files of 50 leaves, two at a time. The files took 34–83 s each, 539 s in total, which is about 1.0 s per leaf. Each file peaked at 8.8–9.2 GB, of which 6.6 GB is the Mathlib import itself.
- **Practical lessons.** Data must be packed into Nat literals; tuple literals of Int took minutes to elaborate. Powers must be Nat powers (GMP-accelerated); `Int.pow` unfolds step by step in the kernel. The slope sums need no recursion, since H − M = 1.
- **Estimate for the whole certificate.** 18.4 M term evaluations at about 1.9 ms, plus about 70 ms per leaf, comes to about 10–12 core-hours. Memory is about 9 GB per file, which allows about 9 files at once, so the check takes about 1.5 h on the compute machine. Importing only the modules the evaluator needs, instead of all of Mathlib, would cut both. **It fits a kernel check.**

## 6. Next steps toward a Palomar entry (nothing submitted)

Status 16 Nov (§7): steps 1–4 are **DONE**, and so are the top-level theorem, its existence half and the assembly.

1. **Lean: soundness of the slope form.** This is the identity x^a − m^a = (x − m)Σ x^k m^{a−1−k} (Mathlib `geom_sum₂_mul`) plus the monotone split already proved, about 150 lines. Then chunk the 64,485 leaves into files.
2. **Lean: the statement and the derivation.**
   - State the construction (27 coordinates, the incidences, (a)–(d)) and the admissibility as in #103 Theorem 1.
   - Prove the divisor lemma (field_simp / positivity steps, as assessed in the census README).
   - Prove that the stored F~ and the stored (N, D) of each test are the construction quantities up to the dropped positive factors. These are polynomial identities of at most about 5000 terms per chart. This is the new identity checking, but at the size of `ring` or a verified sparse normaliser, not the degree-1744 eliminant.
3. **Lean: the coverings.** These are the main box bounds of §1 and the chart lemmas of §2 (case splits on the weighted sizes, with real roots).
4. **Lean: the Krawczyk box.** Existence and uniqueness come from the contraction x ↦ x − Y F(x) on X (Banach, in Mathlib). It is a contraction because ‖I − Y J(X)‖ < 1 and K(X) ⊂ X, both already checked in exact rationals. Then identify the zero with Theorem 10's (its f348 interval lies in X).
5. **The DICTO Yantra** (studies/2026-11-15-dicto-yantra-uniqueness, Theorem 15). The same tool serves, with two changes.
   - The coefficients lie in ℚ(√5). Use c = 2√5 − 4 as a fourth coordinate of fixed width ([0.4721359549, 0.4721359550]), or interval coefficients; the monotone split and slope form carry over, since c > 0.
   - u is not confined to (0, 1) there, because P < R holds for every u. So the box bounds and the boundary face analysis (§2) must be redone.

## 7. Lean formalisation (15 Nov 2026)

**Setting.** The library `YantraCert` lives in the Lake project of the Palomar preparation (studies/2026-11-14-lean-loop-equality). The toolchain is Lean 4 v4.35.0-rc2 with Mathlib v4.35.0-rc2. Nothing was submitted, and no repository was created.

### Source files (in git)

- **`lean/YantraCert/Check.lean`.** Lean core only, with no Mathlib. It holds:
  - polynomials with natural coefficients, as signed pairs P⁺ − P⁻;
  - the sign codes of the monotone split and the slope form;
  - hole boxes;
  - the tree walk `go`, which uses the generator's split rule (the coordinate of least depth, lowest index first);
  - `checkTree`.

  Every function uses the recursors directly, so the kernel never unfolds `brecOn`. Every number is a natural number, so the kernel computes with GMP.
- **`Sound.lean`.** It proves the two enclosures sound.
  - `SP.signMono_sound`: the monotone split, Moore's natural extension in the form P⁺(lo) − P⁻(hi) ≤ p ≤ P⁺(hi) − P⁻(lo).
  - `SP.signSlope_sound`, through `SP.slope_enclosure`: the slope form of Krawczyk and Neumaier (1985). It rests on the identity (Σ_{i<n} x^i m^{n−1−i})(x − m) = x^n − m^n, which is Mathlib's `geom_sum₂_mul`.
- **`Cover.lean`.** It proves `checkTree_sound`: if the kernel accepts a tree, the tree covers its cell. At every point of the cell, one of three things holds:
  - a stored equation is nonzero;
  - a stored test has N·D < 0;
  - the point lies in a hole.
- **`Krawczyk.lean`.** It holds two kinds of result.
  - `krawczyk_unique` and `krawczyk_exists`, for any finite dimension. The test is Krawczyk's (1969), in the uniqueness form of Moore (1977) and Neumaier (1990, Thm 5.1.7), with slopes in place of derivatives. Existence uses Banach's fixed-point theorem through Mathlib's `ContractingWith.fixedPoint`.
  - The slopes of polynomials, and their corner enclosures on a box with a common denominator Q.
- **`KBox.lean`.** It proves the Krawczyk box, using the generated `KBoxData.lean`.
- **`Charts.lean`.** It proves the chart coverings.
- **`lean/Challenge/KulaichevYantra.lean`.** The top-level statement.

### Generated files (in git since 16 Nov 2026)

- **What they are.** `lean/YantraCert/Data/<chart>/{Polys, P<k>, All}.lean`: 1,216 files, 7.6 MB. Also `lean/YantraCert/KBoxData.lean` and the 153 derivation files `lean/YantraCert/Deriv/*.lean` (generators c5, c8, c11). All are committed, in module form (see Version (Palomar-ready)).
- **Generators.** `scripts/c1_lean_cert.py` (budget 1.2e5) and `scripts/c2_kbox_lean.py`. The bench is `scripts/c0_bench.py`.
- **Hashes.** The sha256 of every generated file is in `data/lean-generated.sha256` (certificate and Krawczyk box) and `data/lean-deriv-generated.sha256` (derivation). The manifest, with the cell, leaf count, cost and sha256 of each subtree module, is `data/lean-cert-files.json`.
- **Jobs.** `scripts/run_lean_cert.sh` (all modules, assemblies, axioms) and `scripts/run_lean_node.sh` (the independent re-check).

### Milestones

1. **Step 1a, the faster checker is proved sound: DONE.**
   - Bench (job-free pilot, 50 slope leaves of H~, 522 terms): 5.8 s and 1.2 GB. The yboxlean pilot took about 50 s and 9 GB for the same 50 leaves, so the recursor-based checker in natural numbers is about 10 times faster.
   - Negative control: the whole cube, offered as one leaf, is rejected ("`decide` proved that the proposition … is false").
2. **Step 1b, the whole certificate is kernel-checked: DONE.** Job ylean-cert ended FINAL ok.
   - **What was built.** The core, 10 polynomial modules (each `C_deg` by `decide +kernel`), 1,194 subtree modules, and 10 assemblies.
   - **Module size.** Each subtree module was cut at an estimated 1.2·10⁵ slope-term units. That is 10–30 s each, at most 2.36 GB, run 5 at a time.
   - **Time.** 6,387 s of module time, 22 min of wall time.
   - **The theorems.** The assemblies prove `YantraCert.Data.<chart>.covered : C.Covered ⟨0, 0, 0, 0, 0, 0⟩` for main, A, B, C1, C2, W, Wt+, Wt−, Wr+ and Wr−.
   - **Axioms.** All 11 lines (the 10 charts and `checkTree_sound`) list only `propext`, `Classical.choice` and `Quot.sound` (logs/lean/axioms-cert.log). No source contains `sorry` or `native_decide`.
   - **What `covered` says.** Take any point y of the unit cube, the chart's box rescaled by y = x/W. Then one of the chart's stored equations is nonzero at y, or one stored test has N(y)·D(y) < 0, or y lies in a hole. The holes are the Krawczyk box, corner0 and corner1 for the main chart, and N1 for C1.
   - **Independent re-check.** Job ylean-node2 ran on the second compute machine, with the aarch64 build of the same kernel (commit 11acb17). It checks every module of the 8 small charts and every 4th subtree module of main and C1, and it ended FINAL ok: 314 of 314 modules accepted, 1,939 s of module time, at most 1.91 GB (data/lean-node-times.tsv). An earlier full run, ylean-node, was stopped by the agent after about 100 modules, because the full set needed 4 to 5 h, more than its cap. Its built modules count as checked. Together, 408 of the 1,194 subtree modules were accepted by the second kernel, and none was rejected.
3. **Step 4, the Krawczyk box: DONE.** The theorem is `KBox.kbox_exists_unique : ∃! x, InBox cX rX x ∧ ∀ k, F k x = 0`, for F = (G~, H~, D~) in (u, τ, ρ). X is the certificate's hole, of half-width 2⁻²².
   - **Uniqueness** comes from `krawczyk_unique`, with the polynomial slopes enclosed at the corners of X. The ratios Σ_j M_ij r_j / r_i are 0.0506, 0.1250 and 0.1253, matching §3's 0.051, 0.125 and 0.125.
   - **Existence** comes from `krawczyk_exists` on a box Xs of half-width 2⁻¹⁰⁰.
     - Xs is centred on a 120-digit Newton zero, with u = 0.7504385160222140244060846570…, which is Theorem 10's.
     - The contraction constant is at most 2⁻²⁰. The inclusion ratios are below 5·10⁻¹³.
     - Z = Y⁻¹ is exact, and Xs ⊂ X is proved.
   - **How the numbers are checked.** The 78 corner and centre sums are evaluated by the kernel, and the 3 × 3 inequalities by `norm_num`.
   - **Axioms** are clean (logs/lean/axioms-kbox-charts.log).
4. **Step 3, the chart coverings: DONE.** This is part of step 3.
   - `cover_corner1`: A and B cover [7/8, 1]².
   - `cover_corner0`: C1 and C2 cover [0, 1/4] × [0, 1/16]. The bound η ≤ 27/32 holds because (27/32)⁴ > 1/2.
   - `cover_N1`: W, Wt± and Wr± cover N1 for s > 0, with σ ≤ 3/5 and σ ≤ 3/8. Points with s = 0 have u = 0, so they are not admissible.

   Each is a case split on the largest weighted size. Axioms are clean.
5. **Statement: DONE.** It compiles, with `sorry`, in 110 lines.
   - **The theorems.** `kulaichev_unique : ∃! y : Yantra, y.Huet ∧ y.Kulaichev ∧ y.Admissible`, and `kulaichev_slope`, which says that w7/b7 lies in X's u-interval.
   - **Huet's conditions.** The concurrencies are the coefficient determinants of the leg, base and leg lines, as in #103's model.py.
   - **(a)** is congruence: equal heights and equal half-widths. For inscribed triangles this is u = v.
   - **(d)** is the incentre: b5 < 1/2 < a1, and the centre is equally far from t5's base and from t1's leg.
   - **Admissibility** is #103 Theorem 1's list.

### Milestones of 16 Nov 2026: steps 2 and 3b, the assembly and existence (all DONE)

6. **Step 2, a verified polynomial normaliser: DONE.**
   - **The library.** `ZPoly` is in Lean core. It holds sparse integer polynomials in three variables, kept sorted by merging, with `add`, `mul`, `pow`, `subst`, `substH` and `eqv`. `ZPolySound` proves that every operation commutes with evaluation, and `ZP.eq_of_eqv` turns a kernel-checked `eqv` into an identity of real functions.
   - **Fractions.** `Frac` handles expressions in named quantities and their fractions (`frac_sound`). `step_inv` is the divisor lemma made mechanical: a new quantity is its stored reduced fraction as soon as two kernel identities hold, and the cancelled factor is shown nonzero automatically. `num_zero` and `zero_of_num` link an expression to its numerator.
7. **Step 2, the derivation from the geometry: DONE.**
   - **The construction is forced.** `Geom` and the generated `GeomSteps` show that Huet + Kulaichev + admissibility force the 26 named quantities of s1_system.py, one relation at a time. Each relation is proved by a `linear_combination` certificate that Singular found (`scripts/c6_geom_lean.py`); `dne*` proves each divisor nonzero.
   - **The equations and tests.** `Unique1` (generated by c9) gives `invs` (every quantity is its stored fraction), `fs_*` (G, H1 and D vanish, via nonvanishing witnesses) and `fm_*` (the stored G~, H~ and D~ vanish at the main-chart point).
   - **Kernel checks.** 78 + 10 kernel modules ran in jobs ylean-deriv4 and ylean-deriv5 and in ylean-rescale. They check 24 steps, 3 equations, 3 pull-backs, the tests at the main chart, every chart identity and every rescaling. KTest_28 (corner t5) needs over 46 GB and is not used; existence handles it otherwise.
   - **Times.** The largest module took 7.9 GB (data/lean-deriv-times-*.tsv). The first runs were stopped by the out-of-memory killer, so equal denominators are now kept once and the (1,4,6) fraction goes through two helper steps.
   - **Second machine.** It accepted 69 of the 78 derivation modules (ylean-deriv-node4 FINAL ok).
8. **Step 3b, the box bounds: DONE.** `BoxBounds` proves 0 < u < 1, 0 < τ < 1 and 0 < ρ ≤ 6. For ρ ≤ 6 there are two cases: b9 < 1 when u ≤ 5/6, and ρ u⁵ R = w9 (1 + u) with w9 ≤ 1/2 when u > 5/6.
9. **The assembly and uniqueness: DONE.**
   - **The charts.** `Unique2` (generated by c10) proves that at chart parameters which map to the figure's point, each chart's `Good` can only hold in a hole. It uses `GlueLemmas.sign_transfer` for the test pairs.
   - **The case split.** `Unique3` proves `pt_in_X` by the case split over A/B, C1/C2 and N1 → W/Wt±/Wr±, and the main chart.
   - **The theorems.** `Unique4` proves `unique` and `slope`. `KKBox` identifies the Krawczyk box's polynomials with the stored ones.
10. **Existence: DONE.** The proof works at `xs`, the zero of F~ in the small Krawczyk box.
    - **The figure.** The named quantities are their stored fractions there. Their denominators are nonzero by kernel sign checks on the box: 24 modules `KExD*`, plus 35 + 3 test modules `KExT*`, job ylean-exist4.
    - **Steps, tests, equations.** The construction steps hold by `step_of_inv`. Every admissibility test is positive, from the signs of its pulled-back numerator and denominator; corner t5 uses the bounds 2/5 < b5 < 3/5 and w5 < 1/5. The three equations hold.
    - **The triple points.** Each of the 12 holds by a Singular certificate (`Exist`, generated by c12).
    - **The conditions.** `ExistFinal` (generated by c13) proves `ystar_ok`. `Main` proves `kulaichev_unique` and `kulaichev_slope`, and `#print axioms` is clean.
11. **The Palomar entry, local preflight.** Nothing is submitted, and no repository is created.
    - **Assembly.** `scripts/c14_palomar_entry.py` assembles the entry in Palomar's module layout, using the template files of the loop-equality entry. The entry holds Challenge.lean (116 lines, Mathlib only), Solution.lean (the Challenge word for word, with its proofs in namespace `KulaichevYantra`) and 1,372 library modules: exactly what `YantraCert.Main` imports, directly or indirectly.
    - **Source check and build.** Palomar's source check passes (job ylean-palomar4). The clean `lake build` completes with 10,307 jobs.
    - **Axioms.** `#print axioms` of `KulaichevYantra.kulaichev_unique` and `KulaichevYantra.kulaichev_slope`, as seen from Solution, lists only propext, Classical.choice and Quot.sound. No `sorry` and no `native_decide` appear anywhere.
    - **Comparator (job ylean-comparator).** It exports 26,164 declarations, a 379 MB stream.
      - **con-ron accepts the solution.** It runs with 4 workers and takes 39 min. With its default 16 workers it needs more than 46 GB on the heavy kernel-decide records, and con-ron's verdict does not depend on the worker count; `scripts/run_comparator_lowmem.sh` sets the count.
      - **NanoDa accepts the solution.**
      - **Lean's default kernel (leanchecker) accepts the solution**, and the comparator reports "Your solution is okay!".
      - **Totals.** The whole comparator run took 2 h 31 min wall time; con-ron checked 26,723 declarations in `--verified` mode.
    - **Negative controls: all three REJECTED** (job ylean-negctl, `scripts/run_negative_controls.sh`). Each ran in its own scratch copy of the entry, through the same 4-worker comparator, and each was rejected within minutes:
      - (a) One constant in the Challenge changed (the lower bound of `kulaichev_slope`, last digit +1). The comparator says: "Challenge and solution theorem statement do not match: 'KulaichevYantra.kulaichev_slope'".
      - (b) The Challenge conclusion weakened (∃! to ∃ in `kulaichev_unique`). The comparator says: "Challenge and solution theorem statement do not match: 'KulaichevYantra.kulaichev_unique'".
      - (c) One Solution proof (`kulaichev_slope`) replaced by `sorry`. `#print axioms` lists `sorryAx`, and the comparator says: "Illegal axiom detected: 'sorryAx'".
      - The comparator therefore both passes (the real entry) and fails (all three altered copies).
    - **Rerun after the metadata update (16 Nov 2026, job ylean-palomar5).** The Challenge comment header (sources with pages, a scope line) and formalization.yaml were updated, with the theorem statements unchanged. Source check, build, axioms and the 4-worker comparator all pass again (FINAL ok); see study 2026-11-16-palomar-yantra.

## Version (Palomar-ready) (16 November 2026)

Palomar now requires every committed Lean file of a submitted repository, generated certificates included, to use the module system (`module` first, module doc comments after it), with at most 10,000 physical lines per file and the Challenge within 1,000 lines and 100 KiB. DICTO approved making the work ready in this repository (16 Nov: "count them and do whichever fits"). The Challenge and the theorem statements are unchanged word for word; only headers and visibility changed.

- **One layout, one function.** `scripts/lean_module.py` puts `module` first, makes the leading imports `public import` and opens `@[expose] public section`; the rest of each file is unchanged. It is the transformation that `scripts/c14_palomar_entry.py` already applied to the entry, and it does nothing to a file already in module form.
- **Generators.** Every Lean generator writes through it: c1 (`Data/*`), c2 (`KBoxData`), c5, c8 and c11 (`Deriv/*`), c6 (`GeomSteps`), c9 (`Unique1`), c10 (`Unique2`), c12 (`Exist`), c13 (`ExistFinal`), and the bench c0. The hand-written files (the library, `Challenge/KulaichevYantra.lean`, `BoxCheck.lean`, `ProvedG1000.lean`, and `Deriv/KKBox.lean`, which has no generator) were converted by the same function.
- **Regeneration (job ymod-regen2, FINAL ok).** `scripts/run_module_regen.sh` reran the ten generators on their unchanged inputs. All 1,399 library and statement files equal `modulize(the file before)` byte for byte, with none missing and none new. `data/lean-cert-files.json` changed only in each file's sha256 and size; `data/lean-generated.sha256` and `data/lean-deriv-generated.sha256` hold the new hashes.
- **In git.** The generated files (`lean/YantraCert/Data/`, `lean/YantraCert/Deriv/`, `lean/YantraCert/KBoxData.lean`; 1,369 Lean files, 2.9 MB of text) are now committed, because Palomar builds from the repository. Only `lean/bench/` stays out of git.
- **The entry.** `c14_palomar_entry.py` assembles it from the committed files. At the check below (ymod-palomar2) the assembled entry was byte-identical to the one checked in ylean-palomar5. After it, only two metadata files changed, with no Lean file touched: `lean/palomar/formalization.yaml` gained the related work below, and `lean/palomar/README.md` was rewritten for the standalone repository.
- **Related work: the Rao constraint engine** (S.-E. Gherbi, sri-yantra-constraint-engine, doi:10.5281/zenodo.20617730; study 2026-11-16-palomar-yantra). It is now cited in formalization.yaml. Of its four errata to Rao's printed equations (2.22, 3.3, 3.4, 3.14b), only E1 (eq. 2.22, the base arc x16) touches a constraint the entry cites: F8 = r − r16. The corrigendum ties the other three to F3, F4 and F14/F15 and names no effect on F1, F2, F9 or F20. The entry cites Rao's tabulated figure only as a comparison, and the statement uses Huet's and Kulaichev's conditions, so the theorem is unaffected.
- **Full check from a clean build (job ymod-palomar2).** Palomar's source check passes. A clean `lake build`, with no build folder at the start, completes with 10,307 jobs. `#print axioms` lists only propext, Classical.choice and Quot.sound for `kulaichev_unique` and `kulaichev_slope`, and no `sorry` or `native_decide` appears. The comparator accepts the solution with all three kernels: con-ron (4 workers, `--verified`, 26,723 declarations in 49 min), NanoDa and Lean's default kernel. It reports "Your solution is okay!" after 2 h 39 min of wall time, and the job ends FINAL ok.
- **Negative controls (job ymod-negctl).** All three are rejected by the same 4-worker comparator, each in its own scratch copy, within minutes (FINAL ok): (a) one Challenge constant changed gives "theorem statement do not match: 'KulaichevYantra.kulaichev_slope'"; (b) ∃! weakened to ∃ gives the same for `kulaichev_unique`; (c) one Solution proof replaced by `sorry` lists `sorryAx` and gives "Illegal axiom detected: 'sorryAx'".
- **A fault fixed on the way.** In the first clean build (ymod-palomar, stopped), two parallel `lake build`s raced on a shared dependency (`Data.Wtp.Polys`), and one module failed. `scripts/run_palomar.sh` now builds the 14 shared dependencies first, in one lake process, and retries a failed module alone; only a second failure counts.
- **Whole repository.** `scripts/palomar_source_check.py` (repository root) checks every committed `.lean` file: `module` header, at most 10,000 lines, no symbolic links, Challenge limits. It ends FINAL ok; the longest file is `Data/Main/All.lean` (2,383 lines), and the Challenge has 124 lines and 7,210 bytes.
- Nothing was submitted. No GitHub workflow or runner was added; those steps wait for DICTO.

## Version (Palomar-ready, memory) (17 November 2026)

Palomar's preflight of the standalone repository (DICTOR-Master/kulaichev-yantra-lean, run on 16 Nov) stopped in the Solution build: the standard runner has 4 cores and 16 GB, `lake build` compiles up to 4 modules at once, and the build was killed for lack of memory (peak 15.4 GB, exit 137). The theorem statements, the Challenge and the axioms are unchanged.

- **Measurement.** `scripts/measure_lean_mem.sh` recompiles every module of a built entry alone, as lake compiles it, and records each module's memory peak and RSS (`data/lean-mem-before.tsv`). Nine modules needed more than about 3 GB: `Deriv/KRWtp` 11.8 GB, `Deriv/KRW` 9.9, `Deriv/KFin_D` 6.4, `Deriv/KCW_FH1` 6.1, `Exist` 5.3, `Deriv/KFin_H1` 4.7, `Deriv/KSteps` 3.7, `Deriv/KCWtp_FH1` 3.3 and `Deriv/KExT27` 3.2. The 1,216 certificate modules need at most 1.9 GB each.
- **The one bad proof term.** Inside `KRWtp`, the single theorem `res_F1` took 11.7 GB. Almost all of it went on `ZP.ofSP` of the stored chart polynomial (11.5 GB alone), which sorted the concatenation P⁺ ++ P⁻ by insertion while the stored terms were roughly in descending order. Two generator-level changes fix it:
  - `ZP.ofSP` now sorts P⁺ and P⁻ separately and merges them (`ZPoly2.lean`; its soundness lemma `eval_ofSP` re-proved in `ZPoly2Sound.lean`);
  - `c1_lean_cert.py` writes each part of every stored polynomial in ascending order of (a, b, e), so each sort is linear. Only the 10 `Polys.lean` files change; the subtree modules `P<k>` and the assemblies are byte-identical.
  - `KRWtp` now needs 0.5 GB in 3.8 s (was 11.8 GB in 111 s), and `KRW` 0.45 GB (was 9.9 GB). Measurements after the change: `data/lean-mem-ofsp.tsv`.
- **Build order.** The 8 modules still above 2.5 GB (6.4 GB at most) are put in one chain by `scripts/c15_build_order.py` (list: `data/lean-build-order.json`). Each imports the previous one with a plain `import` marked "build order (memory)", so lake never builds two of them at once. The chain follows the real import graph, and the script checks that it adds no cycle. With every other module at 2.1 GB or less, 4 modules at once stay below about 13 GB.
- **Regeneration.** `run_module_regen.sh` (now ending with c15) reproduces every committed file byte for byte (COMPARE ok).
- **Fit check under Palomar's limits (job kyl-fit, `scripts/run_fit_check.sh`).** The check ran a clean `lake build Solution`, Palomar's own build command. It ran on 4 CPUs (`taskset`, `LEAN_NUM_THREADS=4`; at most 4 lean processes were seen at once) inside a cgroup capped at 14 GB with no swap. The build succeeds in 26 min (1 h 20 min of CPU) with a **memory peak of 8.2 GB**, and the axioms are propext, Classical.choice and Quot.sound only. @@FITCOMP@@
- **Negative controls (job kyl-negctl).** All three are rejected again on the new entry (FINAL ok): (a) and (b) by "theorem statement do not match", (c) by `sorryAx`, "Illegal axiom detected".
- **Preflight.** @@PREFLIGHT@@

## Credits (at point of use)

- **Interval arithmetic and the natural extension:** R. E. Moore, *Interval Analysis* (1966), and *Methods and Applications of Interval Analysis* (1979).
- **Krawczyk operator:** R. Krawczyk, *Computing* 4 (1969) 187–201.
- **Uniqueness form:** R. E. Moore, *SIAM J. Numer. Anal.* 14 (1977); A. Neumaier, *Interval Methods for Systems of Equations* (Cambridge 1990), Thm 5.1.7.
- **Slopes:** R. Krawczyk and A. Neumaier, *SIAM J. Numer. Anal.* 22 (1985).
- **Branch and bound with interval tests:** E. Hansen, *Global Optimization Using Interval Analysis* (1992); Neumaier (1990).
- **Software:**
  - Singular, through passagemath/Sage: pull-backs and factorisation.
  - FLINT/Arb by F. Johansson, through python-flint: the independent ball check.
  - mpmath: the centre refinement.
  - NumPy: the floating-point generator.
  - Lean 4 and Mathlib: the pilot and the formalisation of §7. From Mathlib: `geom_sum₂_mul` (the slope identity), `ContractingWith.fixedPoint` (Banach's fixed-point theorem), `abs_sum_le_sum_abs`, `pi_norm_le_iff_of_nonneg`, `dist_pi_le_iff` and `Real.sqrt`.
  - The Banach fixed-point theorem: S. Banach, *Fund. Math.* 3 (1922) 133–181.
- **Problem and conditions:** as in studies/2026-11-15-yantra-uniqueness (Kulaichev 1984, Pustynski 2014, Chiodo 2021, Huet 2002).

## Files

- `scripts/b1_polys.py`: the system and the 36 tests in the box coordinates (data/polys-utr.json and .txt).
- `scripts/b1_charts.py`: the 9 corner charts (data/polys-utr-<chart>.json).
- `scripts/b2_bnb.py`: the generator (data/bnb-<chart>.json).
- `scripts/b3_krawczyk.py`: the Krawczyk box (data/kbox-K.json).
- `scripts/b4_check.py`: the exact checker (data/bnb-<chart>.check.json).
- `scripts/b4b_semantic.py`: the semantic control.
- `scripts/b5_arb.py`: the Arb re-check (data/bnb-<chart>.arb.json).
- `scripts/b6_lean_export.py`, `lean/BoxCheck.lean`, `scripts/lean_pilot.sh`: the Lean pilot (data/lean-pilot.json).
- `scripts/run_cert.sh`, `scripts/run_arb.sh`: the jobs.
- `scripts/explore/`: the face and Newton-polygon explorations that chose the charts (x0–x13).
- `inputs/system-K.txt`: G, H1, D from the census.
- `data/certificate-size.json`, `data/poly-sizes.json`: the sizes.
- `data/control-notests-open.json`: the 20 open boxes of negative control (b). Its 272,209 leaves are not kept.
- `lean/ProvedG1000.lean`: the kernel-checked pilot file.
- `lean/YantraCert/`: the Lean library of §7 (Check, Sound, Cover, Krawczyk, KBox, Charts); `lean/Challenge/KulaichevYantra.lean`: the statement.
- `scripts/c0_bench.py`, `scripts/c1_lean_cert.py`, `scripts/c2_kbox_lean.py`: the bench and the two Lean generators; `scripts/run_lean_cert.sh`, `scripts/run_lean_node.sh`: the jobs.
- `data/lean-cert-files.json` (the subtree modules: cell, leaves, cost, sha256), `data/lean-generated.sha256` (every generated Lean file), `data/lean-cert-times.tsv` (seconds and peak memory per module), `data/lean-kbox.json` (the Krawczyk ratios).
- `logs/lean/`: the axioms checks and the job tails.
- `logs/`: all step logs.
