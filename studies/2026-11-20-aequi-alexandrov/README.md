# Alexandrov's condition for the 319 polar orbit sets without a die (20 November 2026)

**Verdict: of the 319 polar orbit sets for which study 2026-11-19-aequi-complete found no die fair about the frame centre, 87 fail Alexandrov's condition (no such die exists; 12 of them with equality) and 232 satisfy it: for each of these 232 the die exists and was found here and confirmed to 80 digits. All 232 lie outside the study's search box (largest depth ratio 4.53 to 116.4, box e^1.5 = 4.48), and none has its centroid at the centre (offset / volume^(1/3) from 0.21 to 1.02), so none is an Aequus and the study's counts (149 frame-group Aequi, 4553 in all) are unchanged. The study's sentence "319 polar sets have no frame-centre solution in the box" stays true; read as "no die" it is true only for 87. Control: all 50 solved polar sets pass the test, and the die-finder returns the study's die in each (largest relative depth difference 1.2e-12).**

## The test

A fair die with unit face normals n_1..n_N (each face subtends 4π/N from the origin) is, through the polar body, Alexandrov's problem of prescribing the integral Gauss curvature μ = (1/N) Σ δ_{n_k} (σ the uniform probability measure on the sphere). Alexandrov's condition (A. D. Aleksandrov, C. R. (Dokl.) Acad. Sci. URSS 35 (1942) 131–134; as stated in J. Bertrand, Geom. Dedicata 183 (2016) 81–99, arXiv:1505.04821, Theorem 1.2, and in V. Oliker, Adv. Math. 213 (2007) 600–620, arXiv:math/0701398, Theorem 1, with the polytope case in Theorems 4 and 6): for every nonempty spherical convex ω ≠ S², μ(ω) < σ(ω_{π/2}). It is necessary and sufficient, and the body is unique up to dilation about the origin.

For a discrete μ the test reduces to finite sets A of normals:

- Only ω = the spherical convex hull of a set A of normals matters (shrinking ω to that hull keeps μ(ω) and lowers σ(ω_{π/2})).
- If A is not in an open hemisphere, its hull holds two antipodal points, so σ(ω_{π/2}) = 1 > μ(ω) (the normals bound a solid). So A lies in an open hemisphere.
- Then σ(ω_{π/2}) = 1 − σ(A*), with A* = {y : y·a ≤ 0 for all a in A} the polar polygon of the hull (Bertrand's (18)). Its area is 2π − L(A), L the perimeter of the hull: Girard's formula with the polar's angles π − (side lengths). For one point L = 0 and A* is a hemisphere; for an arc L is twice its length and A* is a lune.

So **the condition fails if and only if some A in an open hemisphere has g(A) = 2π(2|A| − N)/N − L(A) ≥ 0**. Only sets of more than N/2 normals can fail.

## Method

1. **Sets** (scripts/extract.py, data/sets.jsonl): the 319 polar records of the study with no solution (classes C5v, C4v, C3v, C5, C2v, C4, C3, C2, Cs; N = 4 to 13), and 50 controls spread evenly over the 4619 solved polar records.
2. **Witness search** (scripts/alex.py, data/alex.jsonl): every subset of more than N/2 normals (all sets have N ≤ 13, so the search is exhaustive), plus caps around many directions and local moves (kept for larger N). Open hemisphere by a linear program. Hull by the gnomonic chart, perimeter from the hull's corners. The best A is re-checked in 50-digit arithmetic from the exact frame coordinates (0, ±1, ±φ, ±1/φ), with an exact check that the float hull is the hull.
3. **Die-finder, no box** (scripts/alex.py): ψ_k = log d_k, one per orbit. The face met by the ray u maximises (n_k·u)e^{−ψ_k}, so Φ(ψ) = ∫ log max_k (n_k·u)e^{−ψ_k} dσ(u) + Σ μ_k ψ_k is convex with gradient μ_k − Ω_k/4π. This is the variational form of the problem (Oliker's functional Q_K, Theorem 4; Bertrand's Kantorovich dual, Theorem 1.5). Φ is minimised on a 200 000-point Fibonacci grid (|ψ| ≤ 25), then polished with the study's exact solid angles (Van Oosterom and Strackee's triangle formula, IEEE Trans. Biomed. Eng. BME-30 (1983) 125–126; study solve.py) by hybrid Powell. Accepted when every face is within 1e-10 of 4π/N.
4. **80 digits** (scripts/confirm.py, data/confirm.jsonl): every die found is re-solved with the study's refinement (exact.py: mpmath findroot, corners by Cramer's rule). Checks: every face |Ω − 4π/N| < 1e-50, every corner on its planes and inside all others to 1e-50. Also its centroid.
5. **Summary** (scripts/summarise.py, data/verdicts.csv with one row per set, logs/summary.log).

## Results

| | sets | condition fails | of which equality | condition holds | die found, 80 digits |
|---|---|---|---|---|---|
| no die in the study box | 319 | 87 | 12 | 232 | 232 |
| controls (study die known) | 50 | 0 | 0 | 50 | 50 |

By class (fails / holds): C5v 5/5, C4v 2/2, C3v (9 orbits) 3/2, C3v (17 orbits) 10/8, C5 5/5, C2v (11 orbits) 2/4, C2v (27 orbits) 10/60, C2v (11 orbits, second class) 1/7, C4 2/2, C3 12/30, C2 (38 orbits) 8/52, C2 (14 orbits) 0/2, Cs (45 orbits) 26/51, Cs (17 orbits) 1/2.

- **Fails (87).** In every one the witness is all the normals but one (|A| = N − 1). The smallest positive margin is g = 0.0329 (C2: C6 + RD12/2 + RT24/2, N = 5). Example: C3v, O8/1 + O8/1 + RT24/3, N = 5: A = four normals with hull perimeter 3π/5, so μ(ω) = 0.8 ≥ σ(ω_{π/2}) = 0.65. On 78 of the 87 the convex minimiser runs to the bound |ψ| = 25 (a face goes off to infinity), as expected when no die exists.
- **Equality (12 of the 87).** μ(ω) = σ(ω_{π/2}) exactly; the hull's sides are exact angles: 60° and 36° (perimeter 8π/5, N = 10, three C3v sets), 90° three times (3π/2, N = 8), 60° four times (4π/3, N = 6; C2v, C4v, C4), 60° three times (π, N = 4; C3v, C3, Cs), and 70.53° + 2 × 54.74° = 180° (π, N = 4; two Cs sets; arccos(1/3) + 2 arccos(1/√3) = π). Alexandrov's inequality is strict, so these fail. For one of them (C3v: C6/3 + O8/1 + O8/1 + RD12/3) the die-finder gives a near-solution with one face at depth 6.5e10; it is the limit with that face at infinity, and it does not confirm at 80 digits.
- **Holds (232).** The exhaustive search finds no failing A; the largest g is −0.0369. The die exists, and was found and confirmed to 80 digits (largest |Ω − 4π/N| ≤ 1e-99). The study missed these because its starts lay on depth ratios 0.65–1.7 inside e^±1.5. Here the largest depth ratio ranges from 4.528 (C3: O8/1 + RD12/3 + RT24/3, depths 1, 4.528, 1.215) to 116.4 (C2v: C6/1 + O8/4 + RT24/4, depths 1, 0.01132, 0.00859). Every one has its centroid off the frame centre, so none is an Aequus.
- **Controls (50).** All satisfy the condition (largest g −0.539), and the die-finder returns the study's die in all 50. That is uniqueness seen directly: the same die from the convex minimiser and from the study's grid of starts.

So Theorem A (the paper's reading of Alexandrov) and the search agree on all 369 sets. Each of the 319 has no fair die exactly when the condition fails; the other 232 have exactly one, outside the old box.

## Task 2: what the sources state (full text read 20 November 2026)

- **Bertrand**, "Prescription of Gauss curvature using optimal mass transport", Geometriae Dedicata 183 (2016) 81–99, doi:10.1007/s10711-016-0147-3 (arXiv:1505.04821, 2015).
  - Theorem 1.2 (Alexandrov): "Let σ be the uniform probability measure on S^m and µ be a Borel probability measure on S^m satisfying for any non-empty convex set ω ⊊ S^m, µ(ω) < σ(ω_{π/2}). Then, there exists a unique convex body in R^{m+1} containing 0 in its interior (up to homotheties) whose µ is the Gauss curvature measure."
  - ω_{π/2} = {x : d(x, ω) < π/2}. Necessity is (3) in §1.1. A convex ω ⊂ S^m is one whose cone is convex (§3), and ω* = {y : ⟨y, x⟩ ≤ 0 ∀x ∈ ω} is (18).
  - It covers any Borel probability measure, so finitely supported μ (the polytope case) is included, existence and uniqueness both. The paper's proof avoids polyhedra on purpose (§1.3); it approximates by finitely supported measures only inside the proof of Theorem 4.1.
- **Oliker**, "Embedding S^n into R^{n+1} with given integral Gauss curvature and optimal mass transport on S^n", Advances in Mathematics 213 (2007) 600–620, doi:10.1016/j.aim.2007.01.005 (arXiv:math/0701398).
  - Theorem 1 (Aleksandrov): necessary and sufficient conditions (i) µ nonnegative and countably additive, (ii) µ(S^n) = σ(S^n), (iii) µ(S^n \ ω) > σ(ω*) for every spherically convex ω ≠ S^n. Here σ is unnormalised; (iii) is the same condition.
  - The polytope case is stated explicitly. **Theorem 4**: for µ_i > 0 with Σ µ_i = σ(S^n), and Σ_{x_i ∉ V} µ_i > σ((S^n ∩ V)*) for every polyhedral convex cone V ≠ R^{n+1} with vertex O, possibly degenerate, there is a polytope P̃ in F^n_K (vertices only on the rays through x_1..x_K) minimising Q_K, unique up to rescaling.
  - **Theorem 6**: that minimiser has σ(α_P̃(x_i)) = µ_i for every i. Theorems 4 and 6 together give existence for the polytope case. Uniqueness of the minimiser is in Theorem 4. Uniqueness of the polytope solving the curvature problem is credited there to Aleksandrov [2] (1942), and in general to Bertrand's Theorem 1.2.
  - The abstract: "Our solution includes the case of a convex polytope."
- Semenov (arXiv:2210.16974) was not re-read here.

## LEADS

- The study's README should change one sentence: of the 319 polar sets with no frame-centre solution in the box, 87 have none at all (Alexandrov's condition fails) and 232 have one outside the box (found here). The Aequi counts do not change.
- The failing sets have a simple pattern: N − 1 normals inside a hull of perimeter at most 2π(N − 2)/N, so the last face cannot reach 4π/N. That could be stated as a corollary of Theorem A. Whether every failure among frame orbit sets has |A| = N − 1 is not proved; it holds for all 87 here.
- The convex die-finder needs no box and no grid of starts, so it can replace the grid search in later runs (one minimisation per orbit set). It decides existence by itself only together with the exhaustive witness test.
- The 232 extra dice (fair about the frame centre, centroid elsewhere) are not Aequi. If the dataset record lists the off-centre solids, they belong with the 3554 already listed there.

## Files

scripts/: extract.py, alex.py, confirm.py, summarise.py. They import groups.py, solve.py and exact.py from ../2026-11-19-aequi-complete/scripts. data/: sets.jsonl, alex.jsonl (per set: witness, 50-digit g, hull sides, die-finder result), confirm.jsonl (80-digit dice), verdicts.csv. logs/: alex.log, confirm.log, summary.log.

FINAL ok
