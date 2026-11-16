# Theorem 1 (twisted silence): step-by-step audit (17 November 2026)

This audit answers review item 10 for #109 Version 2. It checks the proof as printed in Version 2, step by step, and lists every assumption it uses. Computation with Claude (Anthropic). No specialist has reviewed it.

**Statement (Version 2).** G is a finite group, σ ∈ Aut(G), x₀ ∈ G, and O = {a x₀ σ(a)⁻¹ : a ∈ G}. Π is a finite-dimensional complex representation of G. Then Σ_{x∈O} Π(x) = 0 if and only if χ̃_π(x₀) = 0 for every σ-stable irreducible constituent π of Π.

| step | claim | check | status |
|---|---|---|---|
| 1 | Each point of O is hit \|Stab\| times as a runs over G, so \|Stab\|·S = Σ_a Π(a)Π(x₀)Π(σ(a))⁻¹ | The map a ↦ a x₀ σ(a)⁻¹ is the orbit map of the twisted action g·x = g x σ(g)⁻¹. That is a group action: (gh)·x = g(h x σ(h)⁻¹)σ(g)⁻¹, since σ is a homomorphism. Fibres are cosets of the stabiliser. | ok |
| 2 | Each factor preserves the G-isotypic blocks of Π | Π(a), Π(x₀) and Π(σ(a)) are all values of Π on G, and isotypic blocks are G-invariant. On a block π ⊗ ℂᵐ, G acts as π(·) ⊗ 1, so it is enough to treat m = 1. This is added in Version 2. | ok |
| 3 | S_π = Σ_a π(a)π(x₀)π(σ(a))⁻¹ satisfies π(g)S_π = S_π π(σ(g)) | Substitute b = ga: Σ_b π(b)π(x₀)π(σ(g⁻¹b))⁻¹ = Σ_b π(b)π(x₀)π(σ(b))⁻¹π(σ(g)). | ok |
| 4 | S_π = 0 unless π∘σ ≅ π; otherwise S_π = cJ_π | Schur's lemma for irreducible complex representations. S_π ∈ Hom_G(π∘σ, π), which is 0 or 1-dimensional. J_π is unique up to a scalar. | ok (needs ℂ, π irreducible) |
| 5 | c = \|G\|χ̃_π(x₀)/dim π | From π(a)J = Jπ(σ(a)) we get π(σ(a))⁻¹J⁻¹ = J⁻¹π(a)⁻¹. So tr(S_π J⁻¹) = Σ_a tr(π(a)π(x₀)J⁻¹π(a)⁻¹) = \|G\|χ̃_π(x₀), and tr(cJJ⁻¹) = c·dim π. | ok |
| 6 | The block is \|O\|χ̃_π(x₀)J_π/dim π, zero exactly when χ̃_π(x₀) = 0 | Divide by \|Stab\| = \|G\|/\|O\|. J_π is invertible, so the block vanishes exactly when χ̃_π(x₀) = 0. | ok |
| 7 | S = 0 exactly when every block is 0 | Π is the direct sum of its isotypic blocks. Blocks that are not σ-stable are 0 by step 4. | ok |
| 8 | Unions: Σ_i \|O_i\|χ̃_π(O_i) = 0 for every σ-stable π | Add the blocks. The same J_π is used for every class, so the scalars add. | ok |
| 9 | On S³, S = 0 is silence in degree k | The degree-k harmonics on S³ ⊂ ℍ are exactly the functions x ↦ tr(M V_k(x)), M ∈ End(V_k), by Peter–Weyl; both spaces have dimension (k+1)². Σ_x tr(M V_k(x)) = tr(MS) vanishes for every M exactly when S = 0. Real harmonics are the real parts, so real and complex silence agree. | ok |

**Assumptions used, now stated in Version 2:**
- complex coefficients;
- π irreducible, for Schur's lemma;
- G finite, so that the sum is finite;
- Π finite-dimensional.

**Not used:**
- unitarity;
- the compact group H;
- irreducibility of Π.

Version 1 named these among the hypotheses. Version 2 drops them (referee finding 8).

**Scale of J.** χ̃_π is defined only up to the scale of J_π, so its zeros do not depend on that scale. For σ an involution, Version 2 fixes J² = 1. With that choice the spin values are ±i√3 and ±i√2 (Table 1, corrected in Version 2).

**Equivalence asked about by the reviewer.** "Vanishing of the representation sum" is equivalent to "vanishing of the twisted characters of the σ-stable constituents". Both directions are in step 6: the block equals a nonzero matrix times χ̃_π(x₀). There is no gap.

**Prior form.** By Proposition 3 (a), S is the image of the class sum of x₀σ in G ⋊ ⟨σ⟩. Steps 3–6 are Frobenius's central-character computation done inside the coset Gσ. Version 2 credits this.

**Verdict.** No gap found. The criterion was tested against direct exact sums:
- every twisted and ordinary class of 2I up to k = 60 (second implementation, a1_2I.log);
- all 38 classes of 2T, 2O and 2I up to k = 40, and every tested dihedral class (study 2026-11-15-twisted-silence-groups).
