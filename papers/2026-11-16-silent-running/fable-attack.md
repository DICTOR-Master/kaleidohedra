# Referee attack on #109, Silent Running: Twisted Silence (Version 1, 16 November 2026)

Cold read of `paper.html` (the PDF was spot-compared on ten key strings, not line by line). All recomputation is my own code, exact arithmetic (rationals and Q(√5), pure Python; the host has no sympy), run on the compute host in `fable-attack/`:

| script | log | what it checks |
|---|---|---|
| `q5lib.py` | (library) | exact Q(√5), icosians, Chebyshev and Gegenbauer recurrences |
| `a1_2I.py` | `a1_2I.log` | 2I, σ, twisted classes, Tables 1 and 2, Main theorem to k = 60, symmetry orders, Prop 3 values, Prop 5, ordinary classes |
| `a2_matrix.py` | `a2_matrix.log` | Sym6 with ξ on S²⁴ (k ≤ 40) and its Molien series; W(H3) on S⁸; W⁺(H4) on S¹⁵ with a product-rule test; 2T row |
| `a3_dial.py` | `a3_dial.log` (and `a3_dial_v1.log`, an earlier rational-arithmetic run, same counts) | the two edge circles of the dial, k ≤ 30, real roots by Sturm sequences |

Severity counts: FATAL 0, MAJOR 1, MINOR 8, NIT 8.

## What survived the attack (recomputed and confirmed)

- **Main theorem.** σ(w,x,y,z) = (w̄, −x̄, z̄, ȳ) is an automorphism of 2I (all 14 400 products), an involution, not inner (no conjugator), fixed subgroup of order 6. Twisted classes: 20, 20, 20, 30, 30. A Gram isomorphism of the whole 120-point ℝ⁵ configuration onto 2I exists that sends X, −X, F, −F, R to the five twisted classes. Direct exact tones from the ℝ⁵ coordinates and from the quaternions agree: X, −X silent exactly in 1, 2, 5, 7; F, −F in 1, 2, 3, 6; R in 2 and every odd degree, for all k ≤ 60 (the paper checks to 30). All tones are rational. |Aut(Gram)| = 120 for X, 120 for F, 240 for R. Controls (3,3,3,2,0), (1.7,1.7,1.7,0.6,0), (2,2,1,1,0), (3,3,2,2,0): silent in 1, 2 only (k ≤ 30). p₃(F) = 0 exactly. (`a1_2I.log`)
- **Table 2** and the multiplicities to k = 60, including V₁₅ = 4s + 2·6 and monotonicity under k ↦ k + 12. The "complete lists" argument is sound: 4s is present at k = 13, 17, 19 and 1 or 5 at 14, 18.
- **Theorem 1.** The proof is correct. The criterion predicted the direct signature of every class for all k ≤ 60.
- **Table 1, zeros and moduli.** With χ̃(Oᵢ)χ̃(Oⱼ) = dim π · Σ χ_π(xy)/(|Oᵢ||Oⱼ|) (trace of the product of two class sums, J² = 1): rows 1, 4, 5 are exactly (1,1,1), (2,−1,0), (1,1,−1); 4s vanishes on R and F, 6 on R and X; |χ̃₄ₛ(X)|² = 3, |χ̃₆(F)|² = 2; 2, 2′, 3, 3′ give zero. The values themselves are not as printed: see finding 2.
- **Proposition 3 (b), (c), (d).** 2u + 3v = 6 with (u, v) = (0, 2); the element x₀σ has order 6 on X (3-singular, so Brauer applies), 8 on F, 2 on R.
- **Theorem 4.** The argument in the statement (T_k = Σ m(k,ρ)F_ρ, F_ρ ≥ 0, F₂′ = Galois conjugate of F₂ for rational weights) is a complete proof with Table 2 and V₁₅. I did not recompute the kernels; they are not needed.
- **Proposition 5.** C ∪ (−σC) is silent exactly in 3, 4, 5, 9, 15 for k ≤ 60; all six pairs of 12-point classes checked.
- **Proposition 6 (c), Sym6.** ξ built independently (transpositions to triple transpositions, bijective homomorphism). Five twisted classes of sizes 180, 180, 180, 144, 36; each kills exactly degree 1 for k ≤ 40 on S²⁴; the harmonic Molien series of the twist group is 0, 1, 4, 38, 157, 858, … with its only zero at k = 1, matching `data/s6_twist.log`. (`a2_matrix.log`)
- **Proposition 7.** t³ = (U₃ + 2U₁)/8, t⁵ = (U₅ + 4U₃ + 5U₁)/32, t⁷ = (U₇ + 6U₅ + 14U₃ + 14U₁)/128 (by hand): p₅ = p₃ and p₇ = (7/8)p₃. Correct.
- **Proposition 8.** Proof correct.
- **Table 3b rows:** 2I (all six), 2T, W(H3) (only degree 1, k ≤ 30), W⁺(H4) (all signatures, k ≤ 20), Sym6 confirmed by computation; D16 and D24 confirmed by hand from the cosine rule.
- **§7 edge circles.** On C3 and C2, for k ≤ 30: degrees 3, 5 and every k ≥ 8 vanish only at the roots of s² + 3s + 1 (X on C3 for k = 5, 7; F on C2 for k = 3, 6) and at the antipodal point; the only other silences are 2 base points for k = 4, 2 for k = 6, and 4 (C3) or 2 (C2) for k = 7; no two of these coincide; none is rational with height ≤ 60. (`a3_dial.log`)
- **§6 E8.** h is harmonic on ℝ⁸ (Δh = 24r∥² − 24(r∥² + r⊥²) + 24r⊥² = 0), equals 5s² − 5s + 1 on S⁷, and is the only degree-4 harmonic invariant (3 invariants of degree 4, 2 of degree 2). By hand.
- **§5.** Vertex, edge, face and cell counts and the two edge lengths agree with the truncated and cantellated 5-cell (by hand from the coordinates).
- **Citations.** Fel'shtyn–Troitsky Theorem 4.3 and Lemma 5.1 say what the paper says they say. Koca et al. 2006 has eq. (31) and the split 20, 20₊, 20₋, 30₊, 30₋. Franzsen's Chapter 2 propositions are as described. arXiv:2607.01761 exists with the cited abstract.

## Findings

### 1. MAJOR — Table 3b (four W(H4) rows), Figure 6 (hatched tiles), §10 "W(H4) in 16 dimensions": the "candidates" are an elementary corollary of the Main theorem
**Claim.** Classes of W⁺(H4) and W(H4) under Galois twists are silent in degree 3 on S¹⁵ (and 2, 3 for the 600-point left-only classes); status "candidate", "unforced 3", and an open problem ("whether a larger symmetry forces the zeros is open").
**Evidence.** A twisted class of W⁺(H4) = (2I × 2I)/± is a product O₁ × O₂ of classes of 2I (twisted × twisted for "Galois both", twisted × ordinary for "left only"). An entry of the matrix x ↦ a x b̄ is bilinear in (a, b), so a degree-k polynomial on ℝ¹⁶ restricts to a sum of products f(a)g(b) with f, g harmonic of degrees j, l ≤ k, j ≡ l ≡ k mod 2, and Σ over O₁ × O₂ factorises as (Σ_{O₁} f)(Σ_{O₂} g). For k = 3 the pairs are (1,1), (1,3), (3,1), (3,3): all vanish as soon as one factor is F (F kills 1 and 3) and the other kills 1. That is a proof of every "candidate" zero:
- 600 (×4) = X × ±F, F × ±X; 900 (×2) = F × ±F: silent in 3 because F is.
- left only, 30 (×2) and 360 (×4) = F × {±1}, F × (12-point class): signature 1, 3.
- left only, 600 (×2) = F × (20-point class): 1, 3 from F; 2 from F and the latitude class both killing 2.
`a2_matrix.py` tests the rule "silent in k iff every (j, l) ≠ (0, 0) is killed by one factor" against the direct exact sums for all 25 + 45 class products, k ≤ 20: agreement on every one ("product rule agrees with direct sums on all classes: True"). X × X rings in 3, as the rule says. The W(H4) rows 1200 (×2), 900 (×2) are unions of these (not run separately).
**Fix.** Replace "candidate" by "product of S³ classes; follows from F's silence in 1 and 3", drop the open problem and the hatched tiles, and say that W(H4) on S¹⁵ carries no silence beyond those of 2I. No stated theorem is false here; the paper lists as open something its own main theorem settles.

### 2. MINOR — Table 1, Theorem 2 proof ("a² = 3", "d² = 2"), Proposition 3 (a): the nonzero spin values are ±i√3 and ±i√2 in G⁺, not ±√3 and ±√2
**Claim.** Table 1 gives χ̃₄ₛ(X) = ±√3, χ̃₆(F) = ±√2, "equivalently, characters of the double cover G⁺ on its odd coset", with π̂(σ) = J⁻¹, σ an involution.
**Evidence.** With J² = 1, χ̃(O)² = dim π · Σ_{x,y∈O} χ_π(xy)/|O|². `a1_2I.log`: for 4s the diagonal entries on X, −X are −3 (and +3 between X and −X); for 6 on F, −F they are −2 (and +2). So χ̃₄ₛ(X) = ±i√3, χ̃₆(F) = ±i√2. Independent check: x₀σ has order 6 on X (log: "order of x.sigma = 6"), so a character value there is a sum of sixth roots of unity and lies in ℚ(√−3), which does not contain √3. The real values are those of the other (isoclinic) double cover, in which transpositions lift to elements of order 4; in G⁺ they lift to involutions (σ² = 1). "Confirmed by orthogonality" cannot tell the two apart: orthogonality sees only moduli.
**Consequence.** None for the zeros or the theorems. The relations in the proof should read 40|a|² + 60|b|² = 120 and 40a c̄ + 60b d̄ = 0; the argument then goes through unchanged.
**Fix.** Print ±i√3, ±i√2 (or state J² = −1 on the faithful rows and say this is the other cover), and say which of the two double covers of S5 is G⁺.

### 3. MINOR — §6 "Ordinary classes of 2I are latitude slices … These are the classical Chebyshev zeros"; §9; the census test "a single latitude with U_k(cos θ) = 0"
**Claim.** The 12-point classes kill exactly 4, the 20-point classes exactly 2 and 5, explained as Chebyshev zeros.
**Evidence.** The signatures are right (k ≤ 60). The explanation is only half of one: U_k(cos 36°) = 0 for k = 4, 9, 14, 19, … and U_k(cos 60°) = 0 for k = 2, 5, 8, 11, …, yet the classes are silent only in 4, and only in 2 and 5 (`a1_2I.log`, last column). A Chebyshev zero kills only the zonal harmonic about the axis; it gives silence only while the zonal harmonic is the only invariant of the class's stabiliser, which for the icosahedral group holds up to degree 5 (its first non-constant invariant on the 3-space has degree 6). As a census test, "single latitude with U_k = 0" is not a sufficient mechanism on its own.
**Fix.** Add the sentence above, or cite Theorem 1 with σ = id (5 has defect zero for the prime 5; 3 and 6 for the prime 3).

### 4. MINOR — Proposition 6 (c) and the abstract: the list "I2(n) (n = 5 or n ≥ 7)" includes two groups with no genuine twist; one step is unproved; the scope is undefined
**Evidence.** (i) For I2(n) with n even, ρ_m ≅ ρ₁ ⊗ λ when m ≡ ±(1 + n/2). For n = 8 the units are ±1, ±3 and 3 ≡ −5; for n = 12 they are ±1, ±5 and 5 ≡ −7. So every Galois twist of I2(8) and I2(12) falls under (a) or (b). The paper's own D16 row (σ₇, 7 ≡ −9) is such a case (b). A twist outside (a) and (b) exists exactly for n = 5, 7, 9, 10, 11 and n ≥ 13. The abstract's "where genuine twists exist (I2(n), …)" needs this. (ii) "ρ∘σ is again a reflection representation, hence a Galois conjugate of the geometric one" is asserted with no proof or citation. (iii) "and their binary covers" is not defined for a general reflection group; only the subgroups of SU(2) are treated. (iv) The classification concerns only the defining representation.
**Fix.** State the list of n, cite or prove (ii), and state the scope as "the reflection representation of a finite irreducible Coxeter group, and the finite subgroups of SU(2)".

### 5. MINOR — two meanings of "unforced" (§2 against Table 3b)
§2: unforced = the full symmetry group has an invariant harmonic in that degree. Table 3b: forced = no invariant harmonic of the twist group. Under §2 the odd degrees of R are forced (by −1, as the row's own status says), yet the row lists "unforced: odd"; the same for the 30-point class and the 2O classes. **Fix:** rename the Table 3b columns ("forced by the twist group / not") or move the antipodal degrees to "forced".

### 6. MINOR — abstract against §7: "a dial shows the double silences are isolated points"
Proved exactly only on the two edge circles (confirmed, `a3_dial.log`). On faces and in the interior the evidence is a Newton search from 300 starts, degrees ≤ 12, which §7 itself calls not exhaustive, and "numerical elsewhere". **Fix:** "on the edge circles the double silences are isolated points (exact); a certified search found no others".

### 7. MINOR — credit for the solids A and B (status box, §5)
**Claim.** Koca et al. list the orbits "only as W(A4) orbit labels, without hulls"; "the description of their hulls as the solids A and B … is DICTO's".
**Evidence.** Koca, Ozdes Koca, Al-Ajmi, eq. (30), reads 600-cell = (0,0,1,τ) + (τ,1,0,0) + (τ,0,0,τ) + (1,0,τ,0) + (0,τ,0,1), and the next line: "The first three are the polytopes with 20 vertices each and the last two polytopes have 30 vertices each." A Dynkin label (τ,1,0,0) of A4 is the Wythoff description of a truncated 5-cell with edge lengths in ratio τ, and (1,0,τ,0) of a cantellated 5-cell: the combinatorial type and the golden edge ratio are in the labels, and the authors call them polytopes.
**Fix.** "Koca et al. give the orbits as W(A4) polytopes by Dynkin label; the cells, edge lengths and face counts are worked out here."

### 8. MINOR — Theorem 1: credit and hypotheses
(i) By Proposition 3 (a), Σ_{x∈O} Π(x) is the image of a class sum of G ⋊ ⟨σ⟩ in the coset Gσ, and Theorem 1 is the classical statement that a class sum acts on an irreducible representation by the scalar |C|χ(g)/χ(1) (Frobenius's central character), applied to the extended group. Characters on the coset Gσ are also classical (Shintani descent, which Appendix A lists by title only). The paper credits only Fel'shtyn–Troitsky; that credit is accurate but the older, shorter route deserves a sentence. (ii) H, its compactness and the irreducibility of Π play no part: the statement and proof are about a finite-dimensional representation of G. This is from my own knowledge of the standard theory; I did not find a paper stating it for designs.
**Fix.** One sentence of credit; state Theorem 1 for any finite-dimensional representation of G.

### 9. MINOR — Proposition 5 and §10: "exactly … for k ≤ 20" and the open problem "the class-pair rule for all k" are already settled by the paper's own method
Odd k is silent iff V_k has no 2 or 2′; even k iff V_k is a multiple of 5. Multiplicities do not decrease under k ↦ k + 12 (Klein's form, as in Theorem 2), 2 or 2′ occurs at k = 1, 7, 11, 13, 17, 19, 21, 27, and a constituent other than 5 at every even k from 6 to 16. So the signature is {3, 4, 5, 9, 15} for all k. Direct sums confirm it to k = 60 (`a1_2I.log`). **Fix:** state Proposition 5 for all k and remove that half of the open problem.

### NITs
10. **Prop 6 (b), proof.** "tr(x) takes two values ±c" holds when ρ∘σ = ρ ⊗ λ on the nose (2O). In general ρ∘σ = λ·nρn⁻¹ and the two hyperplanes are tr(xn) = ±c; the invariant line is spanned by n⁻¹, not the identity.
11. **Theorem 4.** T_k of a weighting is never defined. T₇ = 0 ⇒ T₅ = 0 and T₉ = 0 ⇔ T₁₅ = 0 hold for every real weighting; rationality is needed only for T₁. The label "computed for k ≤ 20" undersells a statement the given argument proves outright.
12. **Prop 5.** "C ∪ −C kills every odd degree": it also kills 4.
13. **§1.** "The ordinary orbits of a symmetry group ring in every degree the group allows" is true of generic orbits only (the paper's own latitude classes are counterexamples).
14. **Prop 8.** The proved equivalence concerns degree 1. "The forced silences 1 and 2 … are its systematic absences" is a naming by analogy, not part of what is proved; the label "Exact" covers the first sentence only.
15. **Theorem 2, proof.** "so it lifts to a ↦ (a, σ(a))" skips a step (the preimage of A5 in 2I × 2I is a copy of 2I that projects isomorphically to both factors, because 2I has no subgroup A5). The exact check covers it.
16. **Prop 6 proof.** "[18, Propositions 2.4, 2.8–2.13]": 2.12 in Franzsen's thesis is a Notation, not a proposition.
17. **Prop 3 (c).** Schur's odd-class rule is cited to a paper marked "Not read", and Appendix A notes that the two modern sources opened do not state it. A readable source should be cited (from memory, to be checked: Hoffman and Humphreys, Projective Representations of the Symmetric Groups, 1992; Stembridge, Adv. Math. 74 (1989)). The paper's fallback (p₃(F) = 0) makes the result independent of it.

## Overall verdict

The core of the paper is correct. The Main theorem, Theorem 1, Theorem 2 (zeros and moduli), Proposition 3 (b)–(d), Theorem 4, Propositions 5, 7, 8, the Sym6 case of Proposition 6 and the edge-circle dial all survive independent exact recomputation, several beyond the paper's own range. I found no counterexample to any theorem, and no FATAL flaw.

One revision is substantive (finding 1): the W(H4) "candidates" and their open problem are products of 2I classes and follow from the Main theorem in three lines. One table has wrong values (finding 2: a factor i on the two spin rows), with no effect on any result. The rest are imprecise statements, a mismatch of definitions, an overclaim in the abstract, and credit that should be widened.

On novelty: I found no source stating the signatures {1, 2, 5, 7} and {1, 2, 3, 6}, or twisted classes used to explain design zeros. Theorem 1 itself is classical representation theory in new clothes, and the paper's own credit line says nearly as much. The new content is the 600-cell application.

## Sources checked

Opened and read in part (16–17 November 2026): Fel'shtyn–Troitsky, arXiv:1704.09013v2 (Theorem 4.3, Lemma 5.1, full statements and proofs); Koca, Koç, Al-Barwani, Al-Farsi, arXiv:hep-th/0510191 (§7, eqs. (27)–(34)); Koca, Ozdes Koca, Al-Ajmi, arXiv:1106.2957 (§4.1, eq. (30)–(35)); Franzsen, Automorphisms of Coxeter groups, PhD thesis, Sydney 2001 (statements of Propositions 2.4, 2.8, 2.9, 2.10, 2.11, 2.13). Abstract only: Misawa–Nishimura arXiv:2607.01761; Kaposi et al., Generalized group designs, arXiv:2405.00919. Web searches (four): twisted conjugacy classes with spherical design or harmonic index (only the algebraic-group sense of "spherical": Lu, Carnovale arXiv:1104.0216, arXiv:1001.4001); conjugacy classes of finite subgroups of SU(2) as designs (Roy–Suda arXiv:1104.4692, arXiv:1912.07151, Hirao–Nozaki–Tasaka arXiv:2507.01358, Mohammadpour–Waldron arXiv:2308.02499, arXiv:2409.14811: titles and snippets only); 600-cell subsets as designs (Cohn–Kumar arXiv:math/0607446, snippet only); Schur's spin characters on odd classes (no result stating the rule). None states the paper's theorem or signatures.

## Not checked

- The census: the 3232 sets, Table 3a, the 3000 random subsets, the span tests, the 120-cell lead (rank 525), unions of several twisted classes. Only the sum 808 + 1482 + 144 + 257 + 541 = 3232 and agreement with the study README.
- §7 faces and interior: the 259 roots, 55 Krawczyk certificates, the list of two-degree pairs.
- §8 quasicrystal pilot (16 488 peaks) and §9 (416 coincidences, 820 orbits).
- Table 3b: the 2O rows by computation (consistent by a hand count: six σ-stable irreducibles, six classes); the W(H4) rows with reflections; the forced columns for W(H3) and W(H4).
- Figures were not regenerated; the PDF was compared with the HTML on ten key strings only.
- Proposition 6 (c) beyond Sym6 and the dihedral remark: the quoted classification was read in statement only.
- Bibliographic details of the 40 references (volumes, pages, DOIs).
- Brauer–Nesbitt, Schur 1911, Goethals–Seidel 1981, Sobolev 1962, Delsarte–Goethals–Seidel 1977 were not opened.

## Process notes

Every run was a foreground pilot under five minutes on the compute host. A request with an 1800 s timeout was refused by the launch guard before anything ran; all runs then used timeouts of 240–280 s. One run (the first dial script, 256 s) was moved to the background by the harness and finished by itself with exit 0. A second version of that script failed its own self-test (a sign bug in my integer Sturm code); it was fixed, passes the self-test, and gives the same counts as the first run. Nothing is still running. Nothing was edited in the paper, committed or pushed.

## Comparison with the earlier report (read only after the verdicts above were written)

`studies/2026-11-15-fable-golden-a4/REPORT.md` was opened after this report was complete, and only skimmed for points of disagreement.

- **Disagreement (finding 2).** The earlier report's twisted character table also prints ±√3 and ±√2 on the spin rows. This attack computes χ̃² = −3 and −2 with J² = 1, and the order-6 argument rules out a real √3 in G⁺. The earlier table has the same factor-i slip; the paper inherited it.
- **Not in the earlier report (as far as the skim shows):** the product explanation of the W(H4) classes (finding 1), the I2(8), I2(12) exclusion (finding 4), and the incompleteness of the Chebyshev explanation (finding 3).
- No disagreement on the Main theorem, the signatures, or the zeros of Table 1.

A cosmetic note on my own log: in `a2_matrix.log` the "class size mod ±" printed for products with R as one factor is halved wrongly (R × F shows 300; the class has 600 elements). The sizes are labels only and enter no computation.
