# Independent check: #109 Silent Running, Proposition 6 (c)

Written from scratch on 17 November 2026, without opening any earlier scripts of #109 or its studies.
Statements and definitions were taken from the paper only. Computation with Claude (Anthropic).

## What was checked

Proposition 6 sorts an automorphism σ of a finite irreducible Coxeter group W into three cases, using its
reflection (defining) representation ρ with character χ:
(a) ρ∘σ ≅ ρ; (b) ρ∘σ ≅ ρ ⊗ λ for a one-dimensional λ ≠ 1; (c) otherwise. The paper says that (c) comes from Galois
conjugation, "which exists only for I2(n) (n = 5 or n ≥ 7), H3 and H4", or is the outer automorphism ξ of W(A5) = Sym6.

## Method (all exact)

- `scripts/dihedral_cases.py`: for I2(n), n = 3..40, the group D_n as pairs r^k s^e. Every automorphism is found by brute
  force (images of the two Coxeter generators: involutions whose product has order n and that generate; the homomorphism
  property is then checked on all pairs). Characters are exact in Z[ζ_n] (polynomials mod the cyclotomic polynomial,
  python-flint). Each σ is compared with χ, with χ·λ for every one-dimensional λ, and, in case (c), with every Galois
  conjugate χ_j (ζ ↦ ζ^j) times every λ.
- `scripts/coxeter_aut.py`: for A3, B3, H3, A4, B4, D4, F4, H4, A5. Roots are integer vectors over Z[φ] in the simple-root
  basis, W acts faithfully on them as permutations, and the trace of g is the sum of the α_i-coefficients of g(α_i),
  exact in Z[φ]. An automorphism is a tuple of involutions (t_i) with ord(t_i t_j) = m_ij that gives a bijection
  W → W (the Coxeter presentation makes it a homomorphism). Pruning: t_i lies in a class of the same size as s_i.
  Mod inner: t_1 runs over one element per candidate class and |Aut| = Σ |class| · #{σ : σ(s_1) = that element}.
  For each σ: χ∘σ against χ, χ·λ (all one-dimensional λ), the Galois conjugate χ' (√5 ↦ −√5) and χ'·λ; and whether σ is inner.

## Commands (on the compute host, in this folder)

    python scripts/dihedral_cases.py 40 data/dihedral_cases.json      # 15 s
    python scripts/coxeter_aut.py A3,B3,H3,A4,B4,D4,F4,H4,A5 24 data/coxeter_aut.json   # under 1 min, 24 cores

Logs: `logs/dihedral_cases.log`, `logs/coxeter_aut.log`, both ending `FINAL ok`.

## Results

**I2(n), n = 3..40 (`logs/dihedral_cases.log`).** |Aut(D_n)| = n·φ(n) in every case. σ(r) = r^a:
case (a) iff a ≡ ±1; case (b) iff n is even and a ≡ ±(1 + n/2) (mod n); case (c) otherwise, and every case-(c)
character is exactly a Galois conjugate χ_a of χ.

- Case (c) exists for **n = 5, 7, 9, 10, 11 and every n from 13 to 40**. None for n = 3, 4, 6, 8, 12.
- For n = 8 the only Galois twist (a = 3) and for n = 12 the only one (a = 5) are case (b): ρ_3 ≅ ρ_1 ⊗ λ for n = 8 and
  ρ_5 ≅ ρ_1 ⊗ λ for n = 12, where λ(r) = −1.
- The earlier attack's list: **MATCH**. The paper's wording "I2(n) (n = 5 or n ≥ 7)": **MISMATCH** at n = 8 and n = 12,
  which have Galois conjugation but no case (c).

**Other types (`logs/coxeter_aut.log`).**

| W | order | |Out| | case (a), outer classes incl. inner | case (b) | case (c) |
|---|---|---|---|---|---|
| A3 | 24 | 1 | 1 | 0 | 0 |
| B3 | 48 | 2 | 1 | 1 | 0 |
| H3 | 120 | 2 | 1 | 0 | 1: χ∘σ = χ' (Galois) |
| A4 | 120 | 1 | 1 | 0 | 0 |
| B4 | 384 | 4 | 1 | 3 | 0 |
| D4 | 192 | 12 | 6 (graph automorphisms) | 6 | 0 |
| F4 | 1152 | 8 | 2 (inner, graph) | 6 | 0 |
| H4 | 14400 | 4 | 1 | 1 (λ = sign) | 2: χ∘σ = χ' and χ∘σ = χ'·sign |
| A5 | 720 | 2 | 1 | 0 | 1: ξ, not Galois |

- H3 (|Aut| = 120) and H4 (|Aut| = 28800 = 4 · 7200): every case-(c) automorphism has χ∘σ equal to the Galois conjugate χ',
  possibly times the sign character. **MATCH.**
- Weyl groups A3, A4, B3, B4, D4, F4: no case (c). **MATCH.**
- A5: ξ is case (c) and is not a Galois twist (all characters rational); it sends the transposition class (trace 3)
  to the triple-transposition class (trace −1), as the paper says. **MATCH.**
- The counts are consistent with the structure the paper quotes from Franzsen's thesis (2001), Propositions 2.4 and
  2.8–2.13: every outer class is a reflection-preserving class (inner, graph or Galois) followed by a central twist
  w ↦ w·w0^λ(w), or not, except ξ for A5. For example, H4: {inner, Galois} × {no twist, twist} gives |Out| = 4; F4:
  {inner, graph} × 4 one-dimensional characters gives 8; D4: 6 graph classes × 2 gives 12. This was matched by the
  counts and the case of each class, not by writing each class as such a product. Franzsen's thesis was not opened;
  the comparison is with the paper's summary of it only.

## Proposed correction for Version 2

Replace "which exists only for I2(n) (n = 5 or n ≥ 7)" by "which gives case (c) only for I2(n) with n = 5, 7, 9, 10, 11
or n ≥ 13 (for n = 8 and 12 the Galois twist is ρ_1 ⊗ λ, case (b)); ρ_m ≅ ρ_1 ⊗ λ exactly when n is even and
m ≡ ±(1 + n/2) mod n." The list was checked by brute force for n ≤ 40. The rule for all n follows from the character
values 2cos(2πmk/n) and (−1)^k on rotations.

## Not covered

- The general step "ρ∘σ is again a reflection representation, hence a Galois conjugate of the geometric one" is not
  proved here. It is confirmed by brute force for every case-(c) automorphism of I2(n) (n ≤ 40), H3 and H4.
- Binary covers (2T, 2O, 2I, 2D_n), A_n for n ≥ 6, B_n/D_n for n ≥ 5, E6–E8 and the S²⁴ twisted classes of ξ were not
  recomputed.
- Franzsen's thesis was not fetched.
