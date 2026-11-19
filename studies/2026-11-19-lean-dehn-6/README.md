# Lean study 6 of the shape-language canon: no two of the three words are scissors congruent (19 November 2026)

**Question (DICTO's canon, continued from study 5):** study 5 proved that no similar copies of two different words among CLEO, AXE, FUJI are scissors congruent, but only under a hypothesis, `WordAnglesIndep`: the two angles α = arccos(1/√5) = 63.43…° and β = 79.18…° (cos² β = 1/3 − 2√5/15) are independent modulo π over ℚ. Prove the hypothesis in Lean.

**Result:** proved. `WordAnglesIndep` is a theorem, and the six results of study 5, part 5, hold with no hypothesis. Two new Lean files (299 lines) compile with Lean v4.35.0-rc2 and the pinned Mathlib, with the nineteen files of studies 1 to 5 unchanged: no errors, no warnings, no `sorry`, only the three standard axioms (`compile.log`).

## Proved in Lean (theorem names, statements)

### 1. Independence (`lean/Dehn6Indep.lean`)
```lean
theorem word_angles_int_indep (p q : ℤ) (h : (p : ℝ) * wordAlpha + q * wordBeta ∈ ratPi) :
    p = 0 ∧ q = 0
```
If p α + q β is a rational multiple of π, with integers p and q, then p = q = 0. Steps:
- `cos_two_wordAlpha`: cos 2α = −3/5. `cos_two_wordBeta`: cos 2β = −(10 + 8√5)/30.
- `wordSeqA_cos`: 2·5ⁿ cos(2nα) = d_n, an integer (d₀ = 2, d₁ = −6, d_{n+2} = −6 d_{n+1} − 25 d_n).
- `wordSeqB_cos`: 2·15ⁿ cos(2nβ) = a_n + b_n √5 with integers a_n, b_n ((a₀, b₀) = (2, 0), (a₁, b₁) = (−10, −8), then x_{n+2} = −(10 + 8√5) x_{n+1} − 225 x_n written in the two coordinates).
- `wordSeqB_norm`: 3 does not divide a_n² − 5 b_n² for n ≥ 1.
- `word_double_angles`: a relation P·2α + Q·2β = m·2π with integers P, Q, m has Q = 0.

### 2. The hypothesis of study 5, and the six results without it (`lean/Dehn6Pairs.lean`)
- `wordAnglesIndep : WordAnglesIndep`: modulo π, α is not a rational multiple of β and β is not a rational multiple of α.
- `Unconditional.cleo_axe_not_proportional`, `Unconditional.cleo_fuji_not_proportional`, `Unconditional.axe_fuji_not_proportional`: no real multiple of the Dehn invariant of one word is the Dehn invariant of another.
- `Unconditional.cleo_axe_not_scissorsCongruent`, `Unconditional.cleo_fuji_not_scissorsCongruent`, `Unconditional.axe_fuji_not_scissorsCongruent`: **no similar copy of one word is scissors congruent to a similar copy of another** (any sizes, any positions).
```lean
theorem Unconditional.cleo_axe_not_scissorsCongruent {C A : Set R3}
    (hC : IsSimilarCopy cleoSet C) (hA : IsSimilarCopy axeSet A) : ¬ ScissorsCongruent C A
theorem Unconditional.cleo_fuji_not_scissorsCongruent {C F : Set R3}
    (hC : IsSimilarCopy cleoSet C) (hF : IsSimilarCopy fujiSet F) : ¬ ScissorsCongruent C F
theorem Unconditional.axe_fuji_not_scissorsCongruent {A F : Set R3}
    (hA : IsSimilarCopy axeSet A) (hF : IsSimilarCopy fujiSet F) : ¬ ScissorsCongruent A F
```
The six statements keep the names of study 5 and stand in the namespace `Unconditional`, because the conditional theorems of study 5 (same names, with the hypothesis as an argument) are kept unchanged. Each is the conditional theorem applied to `wordAnglesIndep`.

## Method

### The argument on paper
The argument of study 5's Leads (checked first: `checks/indep_check.py`, exact arithmetic) is the classical one: e^{2iα} = (−3 + 4i)/5 and e^{2iβ} = (−(5 + 4√5) + (10 − 2√5)i)/15 lie in ℚ(√5, i); a relation pα + qβ ∈ ℚπ makes a product of powers of them a root of unity; a root of unity has valuation 0 at every prime; e^{2iβ} has nonzero valuation at a prime above 3 and e^{2iα} has none.

The form proved here reads the valuation at 3 from real parts only:
1. Let P·2α + Q·2β = m·2π with integers. Then cos(2Qβ) = cos(2Pα), and since cos is even, cos(2jβ) = cos(2kα) with j = |Q|, k = |P|.
2. By cos((n+2)x) = 2 cos x cos((n+1)x) − cos(nx): 2·5ᵏ cos(2kα) = d_k is an integer, and 2·15ʲ cos(2jβ) = a_j + b_j √5 with integers a_j, b_j (this is 15ʲ(zʲ + z⁻ʲ) for z = e^{2iβ}).
3. So 5ᵏ(a_j + b_j √5) = 15ʲ d_k. As √5 is irrational, 5ᵏ b_j = 0 and 5ᵏ a_j = 15ʲ d_k. If j ≥ 1 then b_j = 0 and 3 divides a_j, so 3 divides a_j² − 5 b_j².
4. But (a, b) ↦ (−10a − 40b, −8a − 10b) is multiplication by −(10 + 8√5) in ℤ[√5], of norm 100 − 320 = −220, so a_{n+1}² − 5 b_{n+1}² = −220 (a_n² − 5 b_n²) + 225 K with an integer K. The first value is −220, not divisible by 3, and −220 is not divisible by 3, so 3 never divides a_n² − 5 b_n² for n ≥ 1. (3 stays prime in ℤ[√5]: a² − 5b² is divisible by 3 only if a and b both are.)
5. So j = 0, that is Q = 0. Then P·2α = m·2π, and P = 0 because α is not a rational multiple of π (study 4's `wordAlpha_not_ratPi`, Niven's theorem).

A relation with rational coefficients is multiplied by the denominators to reach step 1.

### Why this formalization (the cheapest of those weighed)
- **Chosen: integer recurrences for 2·15ⁿ cos(2nβ) and 2·5ⁿ cos(2nα).** Everything is a statement about real numbers and integers: two sequences of integers, one identity by `ring`, one divisibility by `omega`, the irrationality of √5 (already in study 4). No complex numbers, no number field, no ideals, no ring of four coordinates. The real part suffices because z + 1/z is already not integral at 3.
- Norms of e^{2iβ} itself to ℚ: no use. |e^{2iβ}| = 1, so its field norm is 1 (`checks/indep_check.out`, line 3). The norm that separates is that of 15ⁿ(zⁿ + z⁻ⁿ) in ℚ(√5), which is what step 4 uses.
- A concrete ring ℤ[√5][i] with four integer coordinates and a ring map to the field of 9 elements: sound (3 splits into two primes there; the element −(5 + 4√5) + (10 − 2√5)i lies in one of them only), but it needs a new ring structure or the uniqueness of four coordinates in ℂ. More to write than two recurrences.
- Mathlib's number fields and valuations at prime ideals of ℚ(√5, i): the heaviest; not needed.
- The prime 5 (e^{2iα} has nonzero valuation above 5) is not needed: once Q = 0, Niven's theorem as in study 4 gives P = 0.

### Exact check before the proof (`checks/indep_check.py`, output `checks/indep_check.out`)
Exact fractions in ℚ(√5) and ℚ(√5)[i], run on the compute host: the two values e^{2iα}, e^{2iβ} and their modulus 1; the two recurrences against direct powers for n = 0 to 60; 3 ∤ a_n² − 5 b_n² and the step modulo 225 for n = 1 to 2000; no equality cos(2jβ) = cos(2kα) for 1 ≤ j ≤ 60, 0 ≤ k ≤ 60. The last block is a floating-point sanity check only.

## Credits (borrowed lemmas, at the point of use in the files)
Mathlib: `Real.cos_add`, `Real.cos_sub`, `Real.cos_two_mul`, `Real.cos_neg`, `Real.cos_int_mul_two_pi_sub`, `Nat.twoStepInduction`, `Irrational.ne_rat`, `Int.prime_three`, `Int.natAbs_eq`, `Rat.mul_den_eq_num`, `Submodule.mem_span_singleton`, `Submodule.Quotient.eq`, `Submodule.smul_mem`; the tactics `omega`, `ring`, `linear_combination`. Studies 4 and 5 of this canon: `irrational_sqrt5`, `wordAlpha_not_ratPi` (Niven's theorem `niven`), `cos_wordAlpha`, `cos_wordBeta`, `wordR_sq`, `WordAnglesIndep` and the six conditional theorems. Mathematics: Dehn (1901); Jessen's tensor form; Niven's theorem; the root-of-unity and valuation argument for independence of angles is classical (it is the standard way to show that arccos values are independent of π, as for arccos(1/3)); the recurrence is that of the Chebyshev polynomials.

## Sources checked
- Study 5 (README Leads, `Dehn5Angles.lean`, `Dehn5Pairs.lean`) and study 4 (`Dehn4Words.lean`) of this canon.
- Pinned Mathlib (grep, in study 5 and here): independence over ℚ of arccos values and π: not found (`NumberTheory/Niven.lean` has Niven's theorem); `NumberTheory/Zsqrtd/Basic.lean` has ℤ[√d] with its norm, looked at and not used (two integer coordinates were enough).
- No web search was made in this study. A machine-checked proof that these two angles are independent modulo π, or of these three non-congruences: not found in the sources checked.

## `#print axioms` (from `compile.log`)
The 14 theorems listed in `lean/Axioms6.lean` print `[propext, Classical.choice, Quot.sound]` (`wordSeqB_norm`, a statement about integers, prints `[propext, Quot.sound]`). Among them `word_angles_int_indep`, `wordAnglesIndep` and the six `Unconditional` theorems. No `native_decide`, no added axioms. `grep sorry` over the twenty-one files of the chain finds only the header lines that say "No `sorry`".

## Limits of what is stated
- As in studies 2 to 5: dimension 3; pieces of a scissors congruence are convex polytopes, finitely many, moved by isometries (reflections included). FUJI is the solid cut out by the seven half-spaces of study 5.
- Proved: the Dehn invariants of two different words are not real multiples of each other. Not stated in Lean: which sums of several words have invariant zero (see Leads).
- Zero invariant is not shown to imply scissors congruence (Sydler's direction), as before.

## Files and how to compile
`lean/Dehn6Indep.lean` (part S), `lean/Dehn6Pairs.lean` (part T), `lean/Axioms6.lean`, `lean/compile_all6.sh`, `compile.log`; `checks/indep_check.py` and its output.
The files import study 5 (`DehnCanon.Dehn5Angles`, `DehnCanon.Dehn5Pairs`) and through it studies 1 to 4, all unchanged. Compiled in the Lean workspace of studies 1 to 5, all files in the folder `DehnCanon/`, by `bash DehnCanon/compile_all6.sh` from the workspace root: it compiles the twenty-one files of the chain in dependency order, prints the axioms and greps for `sorry`, `native_decide` and `axiom`. The files on the compute host and the copies here have the same SHA-256.

## Leads
- **Which sums of words cancel.** With independence now proved, x CLEO + y AXE + z FUJI (similar copies with scale factors x, y, z > 0) has invariant zero exactly if 3x + (1 + g)y + (9 − 3g)z = 0 and 3g x + 6y + (12 − 3g)z = 0, g = (√5 − 1)/2. All six coefficients are positive, so no collection of the three words alone has invariant zero. By hand; a short Lean statement from `wordAnglesIndep` and study 5's `lengthPart`.
- **α, β, and the angles of other solids.** The same recurrence method gives independence modulo π for any pair of angles whose doubled cosines lie in a quadratic field and where one is not integral at a prime at which the other is; ready for the dihedral angles of the fair dice and of the Platonic solids against α and β.
- `wordSeqB_norm` proves a little more than used: 2·15ⁿ cos(2nβ) is never divisible by 3 in ℤ[√5], so β alone is not a rational multiple of π, with no use of Niven's theorem (not stated separately).
- From study 5, unchanged: the edge reading for the octahedron, dodecahedron, icosahedron and the fair dice; a general proof of `cover`; Sydler's converse; one Lean folder for publication (now twenty-one files).
