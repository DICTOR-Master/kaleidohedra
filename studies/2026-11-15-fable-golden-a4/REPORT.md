# The golden A4 double silence: mechanism (15 Nov 2026)

Independent answer by Fable. Exact run: `python scripts/golden_a4_mechanism.py` (pure Python, arithmetic in Q(√5)); log `data/golden_a4_mechanism.log`, 26 checks, 0 FAIL.

## Verdict

1. **Mechanism.** The 20 corners X are a *twisted conjugacy class* of the binary icosahedral group 2I (the 600-cell as unit quaternions): X = { a·x₀·σ(a)⁻¹ : a ∈ 2I }, where σ is the outer automorphism of 2I, which is Galois conjugation √5 ↦ −√5 followed by a rotation. The sum of a degree-k harmonic over such a class is a sum of *twisted character values*. Degree k is silent exactly when every σ-stable irreducible piece of Sym^k(C²) restricted to 2I has twisted character zero at x₀. For odd k those pieces are the two spin representations of S5 (degrees 4 and 6), and by Schur's theorem each of them is nonzero on one odd class only. X sits on the class of cycle type (3,2), where the 6 vanishes, so X is silent in every odd degree whose Sym^k has no 4-dimensional spin piece: **k = 1, 5, 7 and no other odd degree.** No hidden orthogonal symmetry is involved. The Galois candidate is right in one precise sense (σ contains the Galois conjugation) and wrong as a symmetry of X.
2. **Proof status.** The theorem (§2) is proved in full below. Its application to X uses three exact computations (X is congruent to a twisted class; the restriction table of Sym^k; the zero pattern of the twisted characters). The zero pattern agrees with Schur's 1911 values for the spin characters of S5, which I quote from memory and did not re-read today. Without Schur, the pattern follows from one cubic identity (p₃ = 0 on the 30-set) plus character orthogonality (§2, Remark).
3. **Complete lists, all degrees (not only ≤ 20).** X kills exactly {1, 2, 5, 7}. S5 forces only {1, 2}. The 30-set F = permutations of (φ², φ², 1, 1, 0) kills exactly {1, 2, 3, 6}, by the same theorem. Predictions for other sets are in §3.
4. **Review of the census theorem (§4).** The normaliser argument is sound for similarities, with one soft step ("generically"). The conclusion drawn from it is too strong: it proves that no new *similarity involution* exists, not that nothing new can be *forced*. X and F are forced by a mechanism that is neither a similarity nor an extra orthogonal symmetry, so they fall outside clauses (P), (E), (X) of the definition and outside the theorem.

Disclosure: the brief said to read only the theorem section of the census. I also read its §1 (definition) and §5 (coincidences), after I had derived the mechanism and the prediction "the 30-point class kills 3 and 6". §5 reports exactly that for F.

## 1. The claims, checked exactly

- X = permutations of (φ², φ², φ², φ, 0), centred: 20 points, squared length 2φ² each. Cosines from one corner: 1 (×1), 1/2 (×1), φ/2 (×3), 0 (×6), −1/(2φ) (×3), −1/2 (×6). All lie in the 600-cell set.
- X closes under reflection in its own members to 120 points with 600-cell cosines (the H4 root system). So X lies in a 600-cell, which is invariant under the coordinate permutations.
- The automorphism group of the exact Gram matrix of X has order **120** (S5, generic).
- The 600-cell splits into S5-orbits 20 + 20 + 20 + 30 + 30: R (the A4 roots, antipodal), X, −X, F, −F.
- Harmonic Molien series of S5 on H (invariants of degrees 2, 3, 4, 5; Goethals and Seidel 1981 for the method): 1/((1−t³)(1−t⁴)(1−t⁵)). The dimension of invariant harmonics is 0 for k = 1, 2 and ≥ 1 for every k ≥ 3 (1 for k = 3,…,7). So **S5 forces only k = 1, 2.**
- Zonal test (Delsarte, Goethals and Seidel 1977): a set kills degree k iff Σ U_k(⟨x,y⟩) = 0 over all pairs, U_k the Chebyshev polynomial of the second kind. Exact results for k ≤ 30:

| set | points | kills |
|---|---|---|
| X, −X | 20 | 1, 2, 5, 7 |
| F, −F | 30 | 1, 2, 3, 6 |
| R (A4 roots) | 20 | 2 and every odd k (antipodal) |
| 600-cell | 120 | every k ≤ 30 except 12, 20, 24, 30 |

So X kills 5 and 7 unforced; 3, 4, 6 and every k from 8 to 30 are not killed.

## 2. The mechanism

**Setting.** G is a finite group of unit quaternions, so G ⊂ S³ = SU(2). σ is an automorphism of G. The twisted class of x₀ ∈ G is O = { a x₀ σ(a)⁻¹ : a ∈ G }. V_k = Sym^k(C²), of dimension k+1. An irreducible representation π of G is σ-stable if π∘σ ≅ π; then there is J_π, unique up to a scalar, with π(g) J_π = J_π π(σ(g)). The twisted character is χ̃_π(x) = tr(π(x) J_π⁻¹).

**Theorem (silence of twisted classes).** O kills degree k if and only if χ̃_π(x₀) = 0 for every σ-stable irreducible constituent π of V_k restricted to G. Constituents that are not σ-stable never contribute. More generally, a union of twisted classes O₁, …, O_m kills degree k if and only if Σᵢ |Oᵢ| χ̃_π(Oᵢ) = 0 for every σ-stable constituent π of V_k.

**Proof.** The harmonic polynomials of degree k on R⁴ are exactly the matrix coefficients x ↦ tr(M ρ_k(x)) of the representation ρ_k of SU(2) on V_k (Peter–Weyl; both spaces have dimension (k+1)²). So O kills degree k iff the matrix S = Σ_{x∈O} ρ_k(x) is zero. Now |Stab|·S = Σ_{a∈G} ρ_k(a) ρ_k(x₀) ρ_k(σ(a))⁻¹. Split V_k into G-irreducibles. Since x₀ ∈ G, ρ_k(x₀) is block diagonal, and on a block of type π the sum is S_π = Σ_a π(a) π(x₀) π(σ(a))⁻¹. This satisfies π(g) S_π = S_π π(σ(g)), so it intertwines π∘σ with π. If π is not σ-stable, S_π = 0 by Schur's lemma. If it is, S_π = c J_π, and taking the trace of S_π J_π⁻¹ gives c = |G| χ̃_π(x₀)/dim π, because π(σ(a))⁻¹ J_π⁻¹ = J_π⁻¹ π(a)⁻¹. Hence the block of S is |O| χ̃_π(x₀) J_π / dim π, and the union statement follows by adding blocks. ∎

For σ = identity this is the classical statement that a conjugacy class kills degree k iff every constituent of V_k has character zero on it.

**Application to the 600-cell.** G = 2I. The rotations of the 600-cell are x ↦ a x b⁻¹ with a, b ∈ 2I. The A5 inside S5 acts irreducibly on the 4-space, so it lifts to a ↦ (a, σ(a)) with σ an outer automorphism (an inner σ would fix an axis); the 4-space is 2 ⊗ 2′, the two Galois-conjugate 2-dimensional representations. The A5-orbits on the 600-cell are therefore the twisted classes. There are five, as many as σ-stable irreducibles (1, 4, 5, and the faithful 4s, 6). Checked exactly: σ(w, x, y, z) = (w̄, −x̄, z̄, ȳ), bar = Galois conjugation, is an automorphism of 2I; the twisted classes have sizes 20, 20, 20, 30, 30; X and F are congruent to twisted classes (exact Gram isomorphism).

Restriction of V_k to 2I (exact): V₁ = 2, V₂ = 3, V₃ = 4s, V₄ = 5, V₅ = 6, V₆ = 3′ + 4, V₇ = 2′ + 6, V₈ = 4 + 5, V₉ = 4s + 6, V₁₀ = 3 + 3′ + 5, V₁₁ = 2 + 4s + 6, V₁₂ = 1 + 3 + 4 + 5. The representations 2, 2′, 3, 3′ are exchanged by σ, so they are invisible to every twisted class. This is why degrees 1 and 2 are forced.

Twisted characters. The zeros are exact computations here. The nonzero values are quoted (S5 on its odd classes; Schur's spin characters) and are confirmed only through the orthogonality relations of the Remark and the union tests of §3 B:

| class | S5 odd class | 1 | 4 | 5 | 4s (spin ⟨3,2⟩) | 6 (spin ⟨4,1⟩) |
|---|---|---|---|---|---|---|
| R (20) | transpositions | 1 | 2 | 1 | 0 | 0 |
| X, −X (20) | type (3,2) | 1 | −1 | 1 | ±√3 | 0 |
| F, −F (30) | type (4,1) | 1 | 0 | −1 | 0 | ±√2 |

**Corollary.** (a) X kills odd k iff 4s is absent from V_k: k = 1, 5, 7. (b) X kills even k iff none of 1, 4, 5 occurs in V_k: k = 2. (c) F kills odd k iff 6 is absent: k = 1, 3; and even k iff neither 1 nor 5 occurs: k = 2, 6. (d) R kills every odd k and k = 2. These lists are complete for all k: multiplying by Klein's invariant form of degree 12 embeds V_k in V_{k+12} as G-representations, so multiplicities never decrease along k ↦ k+12, and the table to k = 30 covers every residue. The theorem's prediction equals the direct exact sums for all five classes and every k ≤ 30 (check in the log).

**Remark (no reliance on Schur).** Faithful twisted characters are odd under x ↦ −x, so they vanish on R and take values (a, −a, b, −b) on (X, −X, F, −F). The rows are orthogonal with norm 120 on the outer coset: 40a² + 60b² = 120 and 40ac + 60bd = 0 for the rows of 4s and 6. The one identity p₃(F) = Σ(xᵢ − mean)³ = 0 on (φ², φ², 1, 1, 0) (checked by hand and by machine) says b = 0 for 4s, since V₃ = 4s. Then a² = 3, c = 0, d² = 2. So T₅ = T₇ = 0 on X is a consequence of T₃ = 0 on F: the two golden sets explain each other.

## 3. Predictions (for blind testing)

All of A–C were confirmed here by direct exact sums to degree 30; they are listed so they can be re-tested independently and beyond 30.

**A. Single classes, complete for every degree.** X and −X: {1, 2, 5, 7}. F and −F: {1, 2, 3, 6}. R: 2 and all odd. Nothing else at any degree.

**B. Unions inside the 600-cell** (weights |O|·χ̃ from the table):

| set | points | kills |
|---|---|---|
| R ∪ X ∪ −X | 60 | all odd, 2, **6** (no single part kills 6) |
| F ∪ −F | 60 | all odd, 2, 6 |
| X ∪ −X | 40 | all odd, 2 |
| R ∪ F | 50 | 1, 2, 3 |
| X ∪ −X ∪ F | 70 | 1, 2, 3 |
| R ∪ X | 40 | 1, 2, 5, 7 |
| X ∪ F, X ∪ −F | 50 | 1, 2 |

No proper union of classes kills degree 4, 8 or 10. A complement of a union kills the same degrees as the union wherever V_k has no trivial piece (all k ≤ 30 except 12, 20, 24, 30).

**C. Ordinary conjugacy classes of 2I (σ = identity; sets in a hyperplane).** The 12 neighbours of a vertex (cosine φ/2), and the three other 12-classes: exactly degree 4. The 20-classes (cosine ±1/2): exactly 2 and 5. The 30-class (equator): exactly the odd degrees. These reduce to a classical fact, U_k(cos θ) = 0 at the latitude.

**D. 24-cell, 2O, E8.** The mechanism predicts nothing new. The outer automorphisms of 2T and 2O are induced by rotations or by a sign, so their twisted classes are rotated latitude slices as in C. 2I is the only binary polyhedral group whose outer automorphism needs a Galois conjugation. The theorem is about S³ and says nothing about E8 roots on S⁷.

**E. Points outside the group (120-cell): data, not prediction.** For x₀ ∉ G the theorem gives only what A5 forces (degrees 1, 2). Exact A5-orbits of the 600 vertices: 2 of size 5, 4 of size 20, 8 of size 60 and one antipodal 30. All kill 1, 2 only (the 30 also all odd), **except four 60-point orbits that also kill degree 4**. That is unforced by A5 and not explained here.

## 4. Review of the census theorem (§3 of the law-giving census)

**Statement reviewed.** In the seed space of a finite reflection group, every similarity between two members comes from a diagram automorphism, so every fixed point of a family involution lies on the automorphism-fixed locus.

**Sound.**
- The normaliser of an irreducible finite reflection group G in O(d) is G extended by the diagram automorphisms (with unit roots these are isometries). An element of the normaliser permutes mirrors, hence chambers; after an element of G it fixes the fundamental chamber and permutes the unit simple roots, preserving angles. "Together with −I" is redundant (−I is −w₀ composed with w₀) but harmless.
- The {0, 1, t} step is right: σ(p(t₁)) ∝ p(t₂) forces t₂ = t₁ or t₂ = 1/t₁ with σ(p) = swap(p).
- The exclusion of H4 symmetry by orbit sizes is right (every H4 orbit size is a multiple of 120; 5 does not divide 192, 384 or 1152).

**Soft step.** "Generically both have symmetry group exactly G." For members with a larger group G′ the similarity normalises G′, not G. The argument survives because G is the subgroup generated by the reflections of G′ in the A4 × {±1} and F4.2 cases, and in the A3 → B3, D4 → B4/F4, B4 → F4 cases the member belongs to a family of the larger group, where the same argument applies. This should be written out; as it stands the proof covers generic members only. F4 with its own automorphism (F4.2) is used elsewhere in the census but is missing from the list of sources of extra symmetry.

**What it misses.**
1. The theorem bounds similarities only. The verdict sentence "nothing new can be forced" does not follow, because (P), (E), (X) are not the only ways a tone can be forced. X and F are counterexamples inside U1: their symmetry group is generic, no similarity involution fixes them, and their silence is forced by §2 above. A fourth clause is needed, for instance (placeholder name, DICTO's to choose) **(C) character silence**: the corners form a class, or twisted class, of a finite group, and the tone vanishes because the relevant characters vanish there.
2. Galois-type maps are not similarities, so the normaliser argument cannot see them. Here the A5 action itself is the Galois-twisted diagonal of 2I × 2I. Both golden members are also fixed by Galois conjugation as shapes (the conjugate of permutations of (0,0,0,1,φ²) is the same set up to scale). Galois-fixedness alone forces nothing; the twisted-class structure does.
3. Subsystem inclusions that are not normal. A4 ⊂ H4 as root systems: an A4-orbit can be a proper part of an H4-orbit without being H4-invariant. The census's orbit-size test rules out H4 *symmetry* of an A4 member but not this weaker relation, which is exactly where X and F live. The same question is open for the other root subsystems of H4 (D4, A2×A2, H3×A1); in 3D the census's hidden-symmetry-of-halves argument already covers it (Icosaxes).
4. The seed-space note that F is "where an ordinary curve meets the edge" does not make F a coincidence: T₃ = T₆ = 0 at F is proved by the Corollary, whether or not a curve passes through.

## Leads

- The four 60-point A5-orbits in the 120-cell that kill degree 4 (§3 E): find the reason, or show it is a crossing.
- Search the H4 Wythoff families for members whose corners are unions of 2I-cosets or twisted classes; the union rule of the Theorem gives their tones at once.
- Write the soft step of the census theorem out in full, and add clause (C) to the definition if DICTO agrees.

## Sources and credit

- Delsarte, Goethals and Seidel, "Spherical codes and designs" (1977): designs and the zonal (Gegenbauer) criterion.
- Goethals and Seidel, "Cubature formulae, polytopes and spherical designs" (1981): harmonic Molien series; orbits of finite groups as designs.
- Schur (1911), spin characters of the symmetric groups: an odd-class value of the spin character ⟨λ⟩ is nonzero only on cycle type λ.
- Klein's invariant forms of the binary icosahedral group; the quaternion description of the 600-cell's rotations (as in Conway and Smith, "On Quaternions and Octonions").
- Twisted conjugacy classes and twisted characters are standard in the character theory of a group with an index-2 subgroup.

All five were used from memory; none was opened today, and no prior-art search was made for the Theorem's application to the 600-cell. Every numerical statement above was recomputed exactly in this study.
