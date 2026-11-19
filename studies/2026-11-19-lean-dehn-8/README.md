# Lean study 8 of the shape-language canon: the two families of nonzero words apart (19 November 2026)

**Question (DICTO's canon, continued from study 7):** study 7 left open every pair with one solid over θ = arccos(1/3) (octahedron, tetrahedron, the cube ∩ octahedron line with t ≠ 3/2, Lucky 7 among them) and one over α, β (dodecahedron, icosahedron, CLEO, AXE, FUJI). Prove in Lean that θ, α, β are independent modulo π, then the fifteen cross-family non-congruences, and update the canon table.

**Result:** proved, all of it. Two new Lean files (447 lines) compile with Lean v4.35.0-rc2 and the pinned Mathlib, with the twenty-seven files of studies 1 to 7 unchanged (same SHA-256 as their study folders): no errors, no warnings, no `sorry`, only the three standard axioms (`compile.log`; the whole chain of 29 files was recompiled).

## Proved in Lean (theorem names, statements)

### 1. Independence (`lean/Dehn8Indep.lean`, part AA)
```lean
theorem tet_word_angles_indep (p q r : ℚ)
    (h : (p : ℝ) * tetDihedral + q * wordAlpha + r * wordBeta ∈ ratPi) : p = 0 ∧ q = 0 ∧ r = 0
```
θ = `tetDihedral` = arccos(1/3), α = `wordAlpha` = arccos(1/√5), β = `wordBeta` (cos² β = 1/3 − 2√5/15). If p θ + q α + r β is a rational multiple of π, then p = q = r = 0. Steps:
- `tet_nat_mul`, `tet_int_mul_sin`: cos(nθ) is rational and sin(nθ) is a rational multiple of √2, for every integer n (cos θ = 1/3, sin θ = 2√2/3, addition formulas).
- `InQ5` (x = a + b√5 with a, b rational), closed under +, −, ×; `cos_two_wordAlpha_inQ5`, `sin_two_wordAlpha_inQ5` (−3/5, 4/5), `cos_two_wordBeta_inQ5`, `sin_two_wordBeta` (sin 2β = (10 − 2√5)/15); `sin_word_comb_inQ5`: sin(Q·2α + R·2β) lies in ℚ(√5) for all integers Q, R.
- `irrational_sqrt10`, `eq_zero_of_mul_sqrt2_inQ5`: **a rational multiple of √2 that lies in ℚ(√5) is zero.**
- `tet_word_relation`: a relation P θ + Q·2α + R·2β = m·2π with integers has P = 0.
- `tet_word_angles_int_indep`: the integer form; `tet_word_angles_indep`: the rational form.
- `tet_not_mem_span`: in the angle classes ℝ/ℚπ, θ is not a rational combination of α and β (the form the Dehn invariant needs).

### 2. The cross-family pairs and the table (`lean/Dehn8Cross.lean`, part AB)
- `not_scissorsCongruent_tet_ab`: if the invariant of P is L ⊗ θ with L ≠ 0 and the invariant of Q is a ⊗ α + b ⊗ β, then no similar copy of P is scissors congruent to a similar copy of Q (any sizes, any positions).
- The fifteen pairs, each by name, **not scissors congruent in any sizes and positions**:

| | dodecahedron | icosahedron | CLEO | AXE | FUJI |
|---|---|---|---|---|---|
| octahedron | `oct_dod_…` | `oct_ico_…` | `oct_cleo_…` | `oct_axe_…` | `oct_fuji_…` |
| tetrahedron | `tetra_dod_…` | `tetra_ico_…` | `tetra_cleo_…` | `tetra_axe_…` | `tetra_fuji_…` |
| cube ∩ octahedron, 1 < t < 2, t ≠ 3/2 (Lucky 7) | `co_dod_…` | `co_ico_…` | `co_cleo_…` | `co_axe_…` | `co_fuji_…` |

  (each name ends in `_not_scissorsCongruent`). The invariants used: octahedron −12√2 ⊗ θ, tetrahedron 12√2 ⊗ θ, cube ∩ octahedron 12√2(2t − 3) ⊗ θ (study 7); the five over α, β as in study 7's table.
- `TetFamily`, `ABFamily`, `abWord` (the five over α, β, indexed by `Fin 5`): `canon_cross_not_scissorsCongruent` (the fifteen pairs in one statement) and `canon_ab_not_scissorsCongruent` (any two different words over α, β; studies 6 and 7, now in one statement).
- `canon_table`: **the canon table**: (1) no nonzero word is scissors congruent to a zero word (study 7); (2) no two different words over α, β are; (3) no word over θ is scissors congruent to a word over α, β. With study 7's opposite-sign pairs over θ, every pair of nonzero words in the canon is decided except the same-sign pairs over θ.

## Method

### The argument on paper (checked first: `checks/cross_check.py`, output `checks/cross_check.out`, exact fractions)
Let P θ + Q·2α + R·2β = m·2π with integers. Then sin(Pθ) = −sin(Q·2α + R·2β). The left side is a rational multiple of √2: the pair (cos nθ, sin nθ / √2) stays rational under the step (a, b) ↦ (a/3 − 4b/3, b/3 + 2a/3). The right side lies in ℚ(√5), because cos and sin of 2α and 2β do: (−3/5, 4/5) and (−(10 + 8√5)/30, (10 − 2√5)/15), and ℚ(√5) is closed under the addition formulas. But √2 is not in ℚ(√5): from b√2 = c + d√5, squaring b√2 − d√5 = c gives 2bd√10 = 2b² + 5d² − c², so bd = 0 as √10 is irrational, and then b = 0 as √2 is irrational. So sin(Pθ) = 0, Pθ is an integer multiple of π, and P = 0 because θ is not a rational multiple of π (study 1, Niven's theorem). The relation is then one between α and β alone, and study 6 gives Q = R = 0. A rational relation is multiplied by its denominators to reach this form.

In field terms: e^{iθ} = (1 + 2√−2)/3 lies in ℚ(√−2), and e^{2iα}, e^{2iβ} in ℚ(√5, i); the two fields meet only in ℚ (the quadratic subfields of ℚ(√5, i) are ℚ(√5), ℚ(i), ℚ(√−5)). This is a special case of the Splitting Theorem of Conway, Radin and Sadun (§1 of their paper): mixed geodetic angles split by the square-free part d of tan² (θ: d = 2; α: d = 1; γ = α + 2β − π: d = 5).

### Why this route (the cheapest of those weighed)
- **Chosen: the two quadratic fields.** Only real numbers, two induction proofs with explicit rational coordinates, and the irrationality of √2 and √10 (both in Mathlib). No prime, no valuation, no integer sequence, no complex number. It needs no new number theory for θ at all: the 3-adic work stays where study 6 already did it, between α and β.
- **Considered: valuations at primes (the route in the brief).** e^{2iθ} = (1 − √−2)²/(1 + √−2)² has valuations −2 and +2 at the two primes above 3 in ℚ(√−2); e^{2iα} = (1 + 2i)/(1 − 2i) lives above 5 only; 15 e^{2iβ} has norm 225 and lives above 3 and 5 (`cross_check.out`, block 5). With a prime above 3 for θ and another for β this works, but in the compositum ℚ(√2, √5, i) the four primes above 3 see both θ and β, so the separation needs the 2 × 2 sign pattern of both numbers on those primes. That is a number field of degree 8 and its prime ideals, or concrete rings and reductions modulo primes: far more to write.
- **Considered: study 6's real-part recurrences, extended.** With three angles the real part alone is not enough: cos(Pθ + Qα′) mixes in sines, and the 3-adic count gives only R = 2P between θ and β; it needs the prime 5 (or √5) as well. Workable, but longer than the field argument, which uses only the sine.

### The cross pairs
As in study 5's `not_proportional`: Mathlib's `Submodule.exists_dual_map_eq_bot_of_notMem` gives a ℚ-linear map f on angle classes with f(θ) ≠ 0 and f(α) = f(β) = 0. Study 5's `lengthPart f` sends s·(L ⊗ θ) to s f(θ) L ≠ 0 and c·(a ⊗ α + b ⊗ β) to 0, so the invariants of similar copies differ, and study 2's theorem applies.

## Credits (borrowed lemmas, at the point of use in the files)
Mathlib: `Real.cos_add`, `Real.sin_add`, `Real.sin_two_mul`, `Real.sin_arccos`, `Real.cos_arccos`, `Real.sin_int_mul_two_pi_sub`, `Real.sin_eq_zero_iff`, `Real.sqrt_mul`, `irrational_sqrt_two`, `irrational_sqrt_natCast_iff`, `Irrational.ne_rat`, `Int.eq_nat_or_neg`, `Rat.mul_den_eq_num`, `Submodule.mem_span_pair`, `Submodule.exists_dual_map_eq_bot_of_notMem`, `Submodule.mem_map_of_mem`, `Submodule.subset_span`, `Matrix.cons_val_*`; the tactics `linear_combination`, `nlinarith`, `interval_cases`, `fin_cases`. Studies 1 to 7 of this canon: `tetDihedral_not_ratPi`, `mem_ratPi_iff`, `edgeTerm` (1); `not_scissorsCongruent_of_dehnSet_ne` (2); `dehnSet_similarCopy`, `IsPoly.similarCopy`, `sqrt5_sq` (4); `sqrt_one_sub_sq`, `sin_wordAlpha`, `cos_wordAlpha`, `sin_wordBeta`, `cos_wordBeta`, `wordR_sq`, `wordR_pos`, `lengthPart`, `lengthPart_tmul`, `lengthPart_smul`, `not_proportional`, `not_scissorsCongruent_of_not_proportional` (5); `cos_two_wordAlpha`, `cos_two_wordBeta`, `word_angles_int_indep`, `wordAnglesIndep` (6); `dehnSet_oct`, `dehnSet_co`, `dehnSet_tetra_tet`, `dehnSet_dod_ab`, `dehnSet_ico_ab`, `dehnSet_cleo_ab`, `dehnSet_axe_ab`, `dehnSet_fuji_ab`, `sqrt5_gt`, `sqrt5_lt`, `IsZeroWord`, `IsNonzeroWord`, `canon_not_scissorsCongruent` and the `isPoly_…` lemmas (7). Mathematics: Dehn (1901); Jessen's tensor form; Niven's theorem; the independence on paper is Conway, Radin and Sadun, "On angles whose squared trigonometric functions are rational" (1999; Splitting Theorem §1, Theorem 1), and for α and γ Ogievetsky and Papadopolos, "On quasiperiodic space tilings, inflation and Dehn invariants" (1999, arXiv:math-ph/9910006), Lemma 2, which rests on Conway–Radin–Sadun. This study adds the machine check.

## Sources checked
- Studies 1 to 7 of this canon (READMEs and Lean files); the paper draft `papers/2026-11-19-dehn-canon/paper.html`, §9 and §10 (open question 1 is the one closed here); the prior-art study `studies/2026-11-19-dehn-prior-art/`.
- Our reference library (349 PDF files): Conway–Radin–Sadun (read: abstract, introduction, Theorem 1, Theorem 2, the proof of Theorem 1 via the Splitting Theorem); Ogievetsky–Papadopolos, Dehn invariants paper (Lemma 2 read again: α = ⟨5⟩₁, γ = π/2 − 2⟨3⟩₅); Papadopolos–Ogievetsky on the inflation rules (its Lemma 2 is about matrices and triangle coverings, not angles).
- Pinned Mathlib (grep): `arccos` together with `LinearIndependent` or `Irrational`: only the irrationality of Chebyshev roots (`Chebyshev/RootsExtrema.lean`), not about these angles; Dehn invariant, scissors congruence: not found (as in studies 5 to 7).
- Web search (one query, Lean formalisation of the independence of arccos(1/3) and arccos(1/√5) modulo π): Wikipedia, "Dehn invariant" (states that the dihedral angles of the Platonic solids, omitting the tetrahedron or the octahedron, are a rational basis, after Conway–Radin–Sadun) and the arXiv copy of Conway–Radin–Sadun; no formal proof. A machine-checked proof that arccos(1/3) is independent of α and β modulo π, or of these fifteen non-congruences: not found in the sources checked.

## `#print axioms` (from `compile.log`)
All 29 theorems listed in `lean/Axioms8.lean` print `[propext, Classical.choice, Quot.sound]`; among them `tet_word_angles_indep`, `tet_word_angles_int_indep`, `tet_not_mem_span`, `not_scissorsCongruent_tet_ab`, the fifteen pair theorems, `canon_ab_not_scissorsCongruent`, `canon_cross_not_scissorsCongruent` and `canon_table`. No `native_decide`, no added axiom. `grep sorry` over the twenty-nine files of the chain finds only the header lines that say "No `sorry`".

## Limits of what is stated
- As in studies 2 to 7: dimension 3; the pieces of a scissors congruence are convex polytopes, finitely many, moved by isometries (reflections included); the solids are the half-space solids of studies 3 to 7 (equality with the convex hull of the corners is not stated for those read by edges). Zero invariant is not shown to imply scissors congruence (Sydler's direction).
- Lucky 7 is covered as the member t = 1.7566… of the cube ∩ octahedron line; every t in (1, 2) other than 3/2 is proved, so the numerical value of t needs no Lean bracket here.
- `TetFamily` is stated for the octahedron, the regular tetrahedron of study 3 and the cube ∩ octahedron line; `ABFamily` for the five solids above. Other solids join by giving their invariant in one of the two forms.

## Files and how to compile
`lean/Dehn8Indep.lean` (part AA), `lean/Dehn8Cross.lean` (part AB), `lean/Axioms8.lean`, `lean/compile_all8.sh`, `compile.log`; `checks/cross_check.py` and its output `checks/cross_check.out` (blocks 1–5 exact; block 6 floats; block 7 a floating-point search, |p|, |q|, |r| ≤ 40, for near relations with π: the closest is 1.8 × 10⁻⁶ from an integer, at (10, 37, −34), as expected for so many trials; floats only, no claim).
The files import study 7 (`DehnCanon.Dehn7Table`) and study 6 (`DehnCanon.Dehn6Indep`), and through them studies 1 to 7, all unchanged. Compiled in the Lean workspace of studies 1 to 7, all files in the folder `DehnCanon/`, by `bash DehnCanon/compile_all8.sh` from the workspace root; for short runs it takes a part argument (1, 2, 3, 4, check), and `compile.log` is the five runs in order (1, 2, 3, 4, check). The files on the compute host and the copies here have the same SHA-256.

## Leads
- **Same sign over θ.** The only undecided pairs of nonzero words in the canon now are those over θ with invariants of the same sign (e.g. Lucky 7 against the tetrahedron, cube ∩ octahedron with t < 3/2 against the octahedron). Their invariants are positive multiples of each other; they are decided by comparing invariant and volume at equal volume. That needs the volumes of the half-space solids in Lean (Mathlib's volume of a polytope is not in a ready form; the cut-and-sum machinery of study 2 may give it for the tetrahedron, octahedron and the cube ∩ octahedron line).
- **The field method for the fair dice.** The argument here works for any angle whose cosine and sine lie in a field that meets ℚ(√5) only in ℚ (by the same squaring step for any square-free d other than 1 and 5 in place of 2). Dice whose dihedral angles have tan² in other square-free classes (Conway–Radin–Sadun's d) can be added to the table by this file's lemmas with a new `InQ5`-style predicate; dice in the classes d = 1 and d = 5 need a prime argument as in study 6.
- **The paper.** §10, open question 1 (across the two families) is closed by this study; Figure 2's dashed arrow becomes a solid line, and §8 and §9 can list Theorem `tet_word_angles_indep` with the credit to Conway–Radin–Sadun and Ogievetsky–Papadopolos (not done here: the paper is not in this study's scope).
- From earlier studies, unchanged: the ten other fair dice; convex hulls; Sydler's converse; one Lean folder for publication (now twenty-nine files).
