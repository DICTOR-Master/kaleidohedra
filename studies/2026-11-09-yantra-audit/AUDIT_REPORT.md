Verdict: Theorems 9 and 10 are now certified. Both polynomials are irreducible, each slope's root is isolated in a rational interval, and both are proved to be the exact yantra's slopes. Both piece counts are certified: 43 for the DICTO Yantra and 45 for Kulaichev's yantra. One request was replaced by an equivalent proof: writing Q, S and b1 as explicit rational functions of u was not feasible at the sizes involved.

# Proof audit of paper #103, *The DICTO Yantra: Two Exact Solutions* (Version 2)

Zenodo record 24061031 (Version 2); concept DOI 10.5281/zenodo.24052633. Audit date: 9 November 2026. The brief is the external
review's to-do list (DICTO_Yantra_Proof_Audit_Brief.md, tasks 1–6). Nothing was committed, pushed or published. The paper and the study folders are unchanged.

## Summary per task

| Task | Outcome |
|---|---|
| 1. Certify Theorems 9 and 10 | **Certified**, by a different route for the exact-residual step: interval Newton plus elimination identities (see §1.3). Irreducibility, rational isolating intervals, factor and root selection: all exact. |
| 2. Certified piece counts | **Certified** for both. DICTO Yantra: 43 = 14 + 10 + 10 + 8 + 1 (all triangles), 18 marmas, 24 sandhis; minimum certified margin 5.2·10⁻⁶. Kulaichev: 45 = 14 + 10 + 12 + 8 + 1 (41 triangles), 18 marmas, 28 sandhis; minimum certified margin 5.8·10⁻⁸. |
| 3. Relation H | **Done**: appendix_H.md (G, Q(t), the trivial factors, all 43 coefficients of H, machine-readable form). |
| 4–6. Wording | **Prepared, not applied**: v3-patches.md (Theorem 1's admissibility, Proposition 8's heading, the proof-status table). It also holds the certificate paragraphs for §10, the credits rewording (house rule of 9 Nov) and the Version 3 line. |
| Rerun of the repository | **Partly**: 31 study scripts (30 plus figure.py) and 6 companion scripts were rerun from a fresh copy; 31 of the 37 end FINAL ok. The heavy eliminations were replaced by a new, faster elimination that reproduces both polynomials. See §4. |
| Novelty against the Śrī Yantra literature | **Not independently re-checked** (outside this audit). See §5. |

## 1. Theorems 9 and 10 (certificates/thm9, certificates/thm10, scripts in certificates/common)

### 1.1 Irreducibility and the polynomials themselves (stage1_poly.py, stage1b_sqrt5_check.py)
- f160 (Theorem 9): even, degree 160, 81 terms; largest coefficient 226 digits, at u⁸⁰; 60 real roots. All of this matches the paper.
  - **Irreducible.** f160 mod 43 is irreducible (degree 160). Mod 3 it factors with degrees 20⁴ + 40² (needed only for the record).
  - **g(y) = f160(√y) irreducible.** Mod 3 its degrees are 20² + 40, mod 17 they are 4 + 6² + 24 + 40, and mod 43 it stays irreducible (degree 80).
  - **Confirmed by two more methods:** PARI polisirreducible, and FLINT/NTL factoring through Sage.
  - **Over ℚ(√5):** g = g₁·ḡ₁ with deg g₁ = 40 (PARI nffactor). sympy checks exactly that the product is g up to a constant and that the two factors are conjugate. With g irreducible over ℚ, each factor is irreducible over ℚ(√5). So u² has degree 40 over ℚ(√5), and √5 ∈ ℚ(u²).
- f348 (Theorem 10): even, degree 348, 175 terms; largest coefficient 33 digits, at u²¹⁰; 34 real roots; leading coefficient 2²⁰·5², constant −2⁸·3⁵. All of this matches the paper.
  - **Irreducible.** The degree patterns of f mod 7, 11, 13 and 19 leave only the trivial factorisations. Mod 11: 2 + 4 + 60 + 141²; mod 13: 1² + 6 + 10 + 165²; mod 19: 1² + 26 + 37² + 82³.
  - **g(y) irreducible**, by the same four primes. Mod 11: 1 + 2 + 30 + 141; mod 13: 1 + 3 + 5 + 165; mod 19: 1 + 13 + 37 + 41 + 82.
  - **Confirmed** by PARI and Sage as well.

### 1.2 Root isolation (stage1_poly.py)
- **Rational intervals of width 10⁻⁴⁰** (numerators over 10⁴⁰):
  - DICTO Yantra: [6793185887067746573886503103907545526887, …888]
  - Kulaichev: [7504385160222140244060846570512345103408, …409]
- **Exactly one real root in each.** PARI polsturm counts it exactly, and an independent Descartes count (pure Python integers, Möbius-transformed polynomial) gives 1 sign variation.
- **Refinement.** Exact sign changes of f at rational points narrow each interval to width 3·10⁻¹⁰⁰⁰. The root's first 1000 digits are stored in work-outputs/stage1-*.json.
- **u² isolated too.** g has exactly one real root in [a², b²].
- **Agreement with stored values.** The roots agree with the stored u to all their digits: 30 for GF1, 60 for Kulaichev.
- **Next real root of f itself:** 2.6·10⁻³ away (f160) and 1.3·10⁻² away (f348).

### 1.3 That the yantra's slope is this root (stage4_elim.py, stage5_certify.py)
The brief calls for Q, S and b1 as explicit rational functions of u modulo f, substituted into every equation. That was tried first.
- **Modular solution.** The system was solved modulo a 62-bit prime p in the residue field F_q of ℚ(u²), with q = p¹⁷⁴. There are 3 solutions there; 2 of them are degenerate, since a divisor of the construction vanishes. The non-degenerate one was lifted p-adically to 32 000 digits, and every condition, including the bindu condition, holds there to that precision.
- **Reconstruction failed.** Rational reconstruction of its coordinates in the power basis still did not stabilise. The coefficients exceed 16 000 digits each, in a field of degree 174, so the exact substitution would handle numbers of order 10⁸ digits (attempt log: thm10/stage3-K-hensel-attempt-log.txt).

The certificate used instead proves the same statement rigorously:
1. **Interval Newton.** The Krawczyk test runs at 520 digits on the square system G = 0 (condition (c)), H₁ = 0 (closing equation) and D = 0 (bindu centred, squared), in the unknowns (u, t, S). This is Theorem 6's natural coordinates, with uv = 2/φ³, or with v = u. It proves **exactly one exact solution** in a box of radius 10⁻⁴⁸⁰, and encloses it in a box of width 5.9·10⁻⁴⁹⁸ (DICTO) and 1.2·10⁻⁵³⁴ (Kulaichev).
2. **Elimination identities.**
   - Every resultant is a polynomial combination of its arguments, so Res_S(G, H₁) and Res_S(G, D), and for the DICTO case their norms over ℚ(√5), vanish exactly at that solution.
   - Every factor that the elimination drops is certified **nonzero** on the box. The kept factors are of degrees (40, 40) and (40, 56) in (t, u) for the DICTO case, and (20, 50) and (20, 44) for Kulaichev.
   - Hence the last resultant Res_t vanishes at u*. Each of its factors other than f has **no real root** in the isolating interval (exact Sturm counts), and the box lies inside that interval. So **f(u*) = 0 and u* = u0** (exact selection of root and factor).
3. **The solution is the yantra.**
   - The whole yantra is rebuilt in interval arithmetic by model.solve (27 divisions for the DICTO case, 26 for Kulaichev). Every divisor is certified nonzero.
   - The closing equation holds exactly: H₁ does, and its cleared denominator and dropped factors (u, v, tu ± 1, t ± v) are nonzero. (b) holds by the circle parametrisation, (c) by G, and (d) by D, with the four sign conditions that undo the squaring certified.
   - Every Huet condition then holds by an exact lemma (stage2_symbolic.py): each condition of model.all_conditions is identically zero, or, for the marma (1,4,6) only, a multiple of the closing polynomial. The lemma was checked in Singular via Sage and in sympy, for both cases and for general u, v.
   - Admissibility holds with strict inequalities. The rebuilt b1, Q and S agree with the stored values to 10⁻⁴⁰ (DICTO) and 4·10⁻⁶¹ (Kulaichev).
   - The slope conditions are built in: v = (2√5 − 4)/u = (2/φ³)/u, or v = u.
4. **A second derivation of f.** stage4_elim.py is a new elimination in natural coordinates (Singular resultants and norm, PARI resultant and factorisation).
   - DICTO case: in 1 minute (against 66 minutes for the original route) it gives the same factor degrees as the paper, 1^1600, 160, 160, 320, and f160 is one of the factors.
   - Kulaichev's case: in 18 seconds it gives a resultant of degree 1744 with factors 1^178, 1^274, 1^178, 2^185, **348** and 396. f348 is the 348 factor. This is a different route from kulaichev_exact.py (variables t, S instead of b1, Q, S), so it confirms Theorem 10 independently.

**What remains, precisely.** The field of definition of the other coordinates is not established: whether Q, S and b1 lie in ℚ(u²). It is supported by the unique non-degenerate solution in F_q, but not proved. Neither paper theorem claims it. Theorems 9 and 10 claim only the minimal polynomial of u, and that is now proved.

## 2. Piece counts (certificates/piece_counts/certified_counts.py)
- **Input:** the stage-5 enclosures of all 27 coordinates (widest 5.7·10⁻⁴⁹⁶ for the DICTO Yantra, 2.0·10⁻⁵²⁵ for Kulaichev), written with outward rounding.
- **One basic predicate.** Every decision of the arrangement of the 27 sides comes down to "do three of the lines pass through one point?" (a 3×3 determinant), plus orientation and order signs.
- **How each predicate is decided.** A sign is certified when its interval excludes 0. Otherwise the predicate is proved exactly zero by the symbolic model: it is identically zero, or a multiple of the closing polynomial.
- **What is computed from it:** vertices, edges, the rotation system, the faces (Euler characteristic 2 checked), and each face's containing triangles. The containing triangles are found by crossing edges from the outer face, and every face must come out the same way from each neighbour.

| | DICTO Yantra | Kulaichev |
|---|---|---|
| exact zeros | 31 concurrencies, 36 parallel pairs (bases) | 31 concurrencies, 38 parallel pairs (bases, plus the rhombus's 2 pairs of opposite sides, u = v) |
| certified signs | 5 909 | 5 965 |
| vertices, edges, faces | 69, 142, 75 | 73, 150, 79 |
| odd faces by depth 1, 3, 5, 7, 9 | 14, 10, 10, 8, 1 = **43**, all triangles | 14, 10, 12, 8, 1 = **45**, of which 41 triangles |
| marmas, sandhis | 18, 24 | 18, 28 |
| minimum certified margin | 5.2·10⁻⁶ (near-concurrency of t6's and t8's left legs with t5's right leg) | 5.8·10⁻⁸ (doubled area of a tiny piece) |

Both margins exceed the coordinate error by more than 480 orders of magnitude. figure.py's float count agrees on both (74 and 78 bounded faces).

## 3. Appendix H, and the generic identity behind Theorem 1
- appendix_H.md gives Theorem 6's G and Q(t), the factorisation v²u⁵(tu − 1)(tu + 1)(t − v)²(t + v)²·H, and H in full. H has degree 10 in t, 3 in S and 24 in (u, v); it has 43 coefficients and 721 terms, and it is irreducible over ℚ. Extraction log: appendix_H/extract-H-log.txt.
- stage2_symbolic.py G is the generic identity behind Theorem 1, with u, v, Q, S and b1 all symbolic. All 23 condition expressions vanish identically except the marma (1,4,6), which is a multiple of the closing polynomial (Singular and sympy; log thm9/stage2-G-log.txt). Patch 1 in v3-patches.md uses this.

## 4. Rerun of the repository (rerun-of-study.txt, rerun-logs/)
The published study folder was copied fresh, and every script was run with a 10-minute limit.
- **Study folder.** 30 scripts were run.
  - **FINAL ok (25):** backwards, check_r1_independent, cleo_yantra, collinear, counts, discriminant, even_on_circle(_fig), even_yantra, gnomon_yantra, golden_family, hidden_triangles, kites, kulaichev_numeric, natural, natural_k1, one_slope, overlay, perfect_yantra, quadratic_family, render_gnomon, rhombus, rhombus345_exact, stella_yantra, verify_exact, viewpoint.
  - **figure.py** on GF1 and on both backwards rebuilds also gave FINAL ok.
  - **FINAL FAIL by design (3):** grid_yantra (as the paper says), and also **lattice_yantra and lattice_clash**. The paper names only grid_yantra.py as failing by design.
  - **selfsimilar.py** produced no output within 10 minutes. It is not cited in the paper.
- **Companion folder 2026-11-08-tetra-yantra.** frame, spherical, render3d, cleo_sphere and sphere81 end FINAL ok. **cleo_cap.py crashes** (brentq: no sign change) and prints no FINAL line. That is consistent with §11's statement that the tip angle never comes down to 72°, but it contradicts "each script ends with a checked FINAL line". Fix: catch the case and print FINAL ok with the finding.
- **Not rerun.**
  - dicto_exact.py, dicto_exact2.py, dicto_exact3.py and kulaichev_exact.py: 66 and 38 minutes. They are replaced by stage4_elim.py, which reproduces both polynomials.
  - rational_search.py and rational_search2.py: 9.7 million and 627 million cases.
  - kulaichev_algdep.py and stella_algdep.py: long runs.
  - 2026-11-08-yantra-4d/search.py (Proposition 8 (1)): it reads a dataset that exists only on the local machine (2026-10-27-white-queen-600), not on the compute machine.

## 5. Flags
- **Novelty.** The paper's claims of novelty against the Śrī Yantra literature (Kulaichev 1984, Huet 2002, Rao 1998, Pustynski 2014, Chiodo 2021, and others) were **not re-checked** in this audit. The paper itself says that Huet's and Kulaichev's full texts were not read, and that six works in Chiodo's bibliography were not read. A specialist will ask about this first.
- **Paper statement to correct:** "Each script ends with a checked FINAL line (grid_yantra.py prints FINAL FAIL by design)". It should name lattice_yantra.py and lattice_clash.py as well, and cleo_cap.py needs the fix above.
- **Kulaichev's 45 pieces.** "Not all of them triangles" can be made exact: 41 of the 45 are triangles.
- **Near-coincidence in the DICTO Yantra.** Its smallest certified margin is a near-concurrency, 5.2·10⁻⁶, of the left legs of t6 and t8 with the right leg of t5. It is not a marma, but it is close to one; this may be worth a sentence.
- **A bug in this audit, caught by its own checks.** The first version of stage 5 wrote its enclosures without outward rounding. The counter then refused to certify Kulaichev's arrangement and stopped. After the fix (outward rounding by 10⁻⁵²⁵) both counts certify. This shows the counter fails safely.

## 6. How to rerun
Requirements: Python with sympy 1.14, mpmath 1.3, cypari2 (PARI 2.17) and passagemath-singular (Singular via Sage).
```
bash certificates/run_all.sh <path to studies/2026-11-08-sri-yantra> <python>
```
This copies the inputs (model.py, natural.py, golden_family.json and the two polynomial files) into certificates/work/. It runs stage1 → stage1b → stage2 → stage4 → stage5 → certified_counts for both cases, then the generic lemma, and writes the logs into thm9/, thm10/ and piece_counts/. Each step ends with a FINAL line, and the whole run takes about 6 minutes. The outputs (isolating intervals, factor lists, enclosures, counts) are copied to certificates/work-outputs/.

| Stage | Script | What it proves |
|---|---|---|
| 1 | common/stage1_poly.py D\|K | descriptive claims; irreducibility (mod-p patterns, PARI, Sage); ℚ(√5) splitting; rational isolating interval |
| 1b | common/stage1b_sqrt5_check.py | ℚ(√5) splitting rechecked exactly in sympy |
| 2 | common/stage2_symbolic.py D\|K\|G | lemma: every Huet condition follows from the closing equation (Singular and sympy); polynomials and divisors of the system |
| 4 | common/stage4_elim.py D\|K | new elimination; f160 and f348 are factors of the final resultant; full factor lists |
| 5 | common/stage5_certify.py D\|K 520 | Krawczyk; nonvanishing of the dropped factors; f(u*) = 0 with u* = u0; the exact yantra rebuilt and admissible |
| counts | piece_counts/certified_counts.py D\|K | certified 43 and 45, marmas and sandhis, margins |
| (attempt) | common/stage3_hensel.py | p-adic solution; the reconstruction that did not stabilise (kept for the record) |

## 7. Proof-status table (after this audit)
See v3-patches.md, Patch 3, for the full table. In brief:
- **Certified algebraic:** Theorems 9 and 10.
- **Certified computation:** Proposition 11, and Proposition 3 for the DICTO Yantra.
- **Exact symbolic:** Theorems 1, 5, 6 and 7, and Proposition 4.
- **Exact rational:** Theorem 2.
- **Computational search:** Proposition 8 (1). Proposition 8 (2) is conditional on u² being irrational for PF2.
- **High-precision numerical:** the other yantras of Table 3.
