# The golden 5-cell candidate: why it is silent in degrees 5 and 7 (15 Nov 2026)

**Verdict (15 Nov 2026): the double silence is FORCED, and the mechanism is new to the census. The 20 corners, all permutations of (φ², φ², φ², φ, 0), are one of the five orbits into which the 5-cell's symmetry group S5 splits the 600-cell. On the 600-cell, degrees 5 and 7 see the same single S5-invariant function, so T₅ = T₇ = 0 is one condition, not two. That one condition is forced by whole-number arithmetic: the squared values u and v of that function on the two non-antipodal orbit types must be whole numbers with 2u + 3v = 6, so u = 0 or v = 0. Exactly one of the two golden members is therefore silent in degrees 5 and 7, and the other in degree 3. Which one is which is the classical spin character table of the double cover of S5 (Schur 1911). The second candidate, the permutations of (φ², φ², 1, 1, 0) with T₃ = T₆ = 0, is the partner orbit of the same 600-cell, and the same argument forces its zeros. Inside the 600-cell both members are therefore law-giving points of a new kind, a law forced by integrality. No involution forces them, and they lie outside the census's diagram-automorphism theorem. Double Vision (√5 → −√5) does act on the 600-cell, but it fixes every orbit, so it forces only that every tone is rational, not the zeros. With this, all 416 coincidences of the census are explained. A systematic exact search covered 820 subgroup orbits in the 600-cell, 24-cell, 120-cell and E8 roots. It found no other orbit with two silences that its symmetry does not force, except two 600-cell dodecahedra, which are conjugacy classes at angle π/3 and silent in degrees 2 and 5 by the classical Chebyshev rule. The golden pair is the only case of the new kind.**

DICTO asked for this follow-up on 15 Nov 2026. It closes lead 1 of studies/2026-11-15-law-giving-census, section 6, the one open candidate of that census. Computation, proofs and drafting were done with Claude (Anthropic).

## 1. The two sets and where they sit

The coordinates are the census's, R⁵ with the centre subtracted. S5 permutes the coordinates.

- X = all permutations of (φ², φ², φ², φ, 0): 20 points (A4 family o3o3x3t at t = φ).
- Y = all permutations of (φ², φ², 1, 1, 0): 30 points (A4 family o3x3o3t at t = 1/φ).

The closure of X under reflection in its own members has exactly 120 points: a 600-cell P. Y lies in the same P at the same radius, and no rescaling is needed (exact). P splits into five S5-orbits:

| orbit | size | what it is | tone zeros, k ≤ 30 (exact) |
|---|---|---|---|
| C1 = X | 20 | (3,2)-type class | 1, 2, 5, 7 |
| C2 = −X | 20 | (3,2)-type class | 1, 2, 5, 7 |
| C3 | 20 | transposition class (antipodal) | 1, 2 and every odd degree |
| C4 = Y | 30 | 4-cycle class | 1, 2, 3, 6 |
| C5 = −Y | 30 | 4-cycle class | 1, 2, 3, 6 |

The split 20 + 20 + 20 + 30 + 30 of the 600-cell under W(A4) is known: Koca, Ozdes Koca and Al-Ajmi, "Branching of the W(H4) polytopes and their dual polytopes under the Coxeter groups W(A4) and W(H3) represented by quaternions", Turk. J. Phys. 36 (2012), arXiv:1106.2957. Their paper gives the orbits but no tones.

The zeros up to degree 30 are exactly the census's (1, 2, 5, 7 and 1, 2, 3, 6), and no further zero appears up to degree 30.

## 2. The mechanism

**Step 1: tones on the 600-cell are sums of block contents.** The 600-cell's 120 vertices, as unit quaternions, are the binary icosahedral group 2I. The cosine ⟨x, y⟩ = Re(x y⁻¹) names the conjugacy class of x y⁻¹: there are 9 cosine values and 9 classes, with sizes 1, 1, 12, 12, 12, 12, 20, 20 and 30. On S³ the degree-k Gegenbauer polynomial is the Chebyshev U_k, and U_k(Re g) is the character of Sym^k(C²) at g. So for every subset O of the 600-cell

T_k(O) = Σ_ρ m(k, ρ) · F_ρ(O),   F_ρ(O) = Σ_{x,y∈O} χ_ρ(x y⁻¹) ≥ 0,

where ρ runs over the 9 irreducible representations of 2I (dimensions 1, 2, 3, 4s, 5, 6, 2′, 3′, 4) and m(k, ρ) is the multiplicity of ρ in Sym^k (the McKay decomposition, McKay 1980). The script checks this identity exactly for every orbit and every k ≤ 30. A tone vanishes exactly when every block ρ in Sym^k has F_ρ(O) = 0. The decompositions are:

- Sym⁵ = 6
- Sym⁷ = 6 + 2′
- Sym³ = 4s
- Sym⁶ = 3′ + 4

**Step 2: degrees 5 and 7 are one condition.** S5 acts on the 600-cell as x ↦ a x α(a)⁻¹, where α is the outer automorphism of 2I. The 4-dimensional representation of A5 is 2 ⊗ 2′, so the action is twisted. An S5-orbit is therefore an α-twisted conjugacy class. On a twisted class, F_ρ = 0 automatically unless ρ is α-stable, and 2′ is not α-stable (α swaps 2 and 2′). So on every S5-orbit in the 600-cell, T₇ = 0 exactly when F₆ = 0, which is exactly when T₅ = 0. The codimension-2 coincidence of the census is codimension 1 here.

**Step 3: the twisted character table.** On a twisted class O, F_ρ(O) = |O|²·|χ̃_ρ(O)|²/dim ρ, where χ̃_ρ is the twisted character. Equivalently, χ̃_ρ is the character of the double cover 2·S5 on its odd coset. The computed squared values are all whole numbers:

| block (degree where it first appears) | C1, C2: (3,2)-type | C3: transpositions | C4, C5: 4-cycles |
|---|---|---|---|
| 1 (0) | 1 | 1 | 1 |
| 5 (4) | 1 | 1 | 1 |
| 4 (6), the standard representation of S5 | 1 | 4 | **0** |
| 4s (3), spin | 3 | 0 | **0** |
| 6 (5 and 7), spin | **0** | 0 | 2 |
| 2, 3, 2′, 3′ | 0 | 0 | 0 |

From this table, the script predicts every zero of all five orbits up to degree 30, and the predictions match the direct zeros exactly.

**Step 4: why the 0 in the 6-row is forced (integrality).** Put u = |χ̃₆(C1)|² and v = |χ̃₆(C4)|². The two spin values vanish on the antipodal class C3 (−1 acts as −1). Orthogonality of the character of 2·S5 over its odd coset gives 40u + 60v = 120, that is 2u + 3v = 6. Character values are algebraic integers, and every Galois conjugate of χ̃₆ is ±χ̃₆ (its restriction, the 6 of 2I, has a rational character). So u and v are whole numbers ≥ 0. The only solutions are (u, v) = (0, 2) and (3, 0). **The 6-block must vanish on the (3,2)-type pair or on the 4-cycle pair.** The same argument applies to the 4s-block, with u′ = 3 − u and v′ = 2 − v from the column relations, so it vanishes on the other pair. The actual values (0, 2) and (3, 0) are Schur's: a spin character of the pair type λ is nonzero on odd elements only on the class of cycle type λ. Here 6 = χ^(4,1) lives on 4-cycles and 4s = χ^(3,2) lives on (3,2)-type elements (Schur 1911, J. reine angew. Math. 139, 155–250, public domain).

The zeros forced in each orbit are:

- **C1 = X:** the 6-block is 0, so T₅ = T₇ = 0. The census's open candidate is explained.
- **C4 = Y:** the 4s-block is 0, so T₃ = 0. The standard character of S5 is 0 on a 4-cycle (fixed points − 1 = 0), so T₆ = 0.

T₃(X) ≠ 0 and T₅(Y) ≠ 0 are what the table requires.

**What kind of law this is.** It is forced, but not by (P) parity, (E) evenness or (X) extra symmetry: the symmetry group of X is exactly S5 (census), and no isometry beyond S5 × {±1} normalises S5. The law is forced by the arithmetic of the twisted characters (integrality plus orthogonality). We name this kind **(R) representation forcing**: the orbit is a twisted conjugacy class of a finite group whose elements are the corners of a polytope, and a tone vanishes because a twisted character value is forced to be 0. This is a new kind next to (P), (E) and (X). The census theorem (every involution fixed point lies on the automorphism-fixed locus) is untouched, because (R) uses no involution of the family. The law holds at the member because the member is a 600-cell orbit. Neighbouring members leave the 600-cell, and the control member t = 2 has an infinite reflection closure and only the trivial zeros 1 and 2.

**Double Vision checked and ruled out as the cause.** Galois conjugation √5 → −√5 maps P to P/φ², so Φ = φ²·σ permutes the 600-cell and sends each cosine c to σ(c) (exact). Φ fixes all five orbits setwise. It therefore forces only that every tone of every orbit is rational, which the script confirms exactly. It forces no zero.

## 3. Spherical designs and prior art

- X is a spherical 2-design that is not a 3-design. In the language of designs of harmonic index (Bannai, Okuda and Tagami, J. Approx. Theory 195 (2015) 1–18, arXiv:1308.5101), X is a design of harmonic index set {1, 2, 5, 7}.
- Y is a spherical 3-design that is not a 4-design, with the extra index 6.
- Every S5-orbit is a 2-design, because S5 acts irreducibly on R⁴ (Delsarte, Goethals and Seidel 1977, the design definition; de la Harpe and Pache, the criterion for group orbits).
- **Prior art:** none found for the twisted-character mechanism or for these two sets as designs. Sources checked:
  - Koca et al. 2012 (above): the orbit split only;
  - errorcorrectionzoo.org, pages for the 600-cell and spherical designs (the 600-cell is an 11-design, Boyvalenkov and Danev 2001);
  - Bannai, Okuda and Tagami 2015 and its follow-ups (arXiv:1507.05373; Zhu, Bannai, Kim and Yu, Electron. J. Combin. 24(2) P2.14);
  - de la Harpe and Pache, "Spherical designs and finite group representations" (unige.ch), abstract only;
  - three web searches (standard): "600-cell W(A4) orbits 20 20 20 30 30 Koca"; "spherical designs of harmonic index orbits character zeros"; "spherical design twisted conjugacy spin characters binary icosahedral".
- Goethals and Seidel 1981, "Cubature formulae, polytopes and spherical designs", was not read (no free copy found this session). Sloane's table of spherical designs lists designs by strength t, so a harmonic-index set {1, 2, 5, 7} is outside its scope.

## 4. Systematic search for the same mechanism (exact)

For each of four polytopes P, every K-orbit O in P was taken, for K in a list of reflection subgroups of Aut(P) (each found as a root subsystem, by exhaustive search) and their rotation subgroups. For each orbit:

- the tones k ≤ 20 were computed exactly;
- S = Stab(O) in Aut(P) was found by enumerating H4 (14400 elements) or W(F4) (1152);
- h_k(S), the number of S-invariant harmonics of degree k, was computed by Molien.

A zero with h_k(S) > 0 is **genuine**: the symmetry of O does not force it. The blocks of P are:

- 600-cell: the 9 characters of 2I;
- 24-cell: the 5 real characters of 2T;
- E8: harmonic degrees 0–4, which are its 5 eigenspaces (a 7-design).

On every orbit the block identity and the zero prediction from vanishing blocks were checked exactly.

| polytope | subgroups (realised) | distinct orbits | with a genuine zero | with ≥ 2 genuine zeros |
|---|---|---|---|---|
| 600-cell | A4, D4, A2A2, I2(5)², H3A1, A1⁴, H3, A3, A2A1, I2(5)A1, H4 (+ rotation subgroups) | 115 | 15 | 6 |
| 24-cell | B4, D4, A2A2, B3A1, A3A1, A1⁴, B2B2, B3, A3, A2A1, F4 (+ rotation) | 25 | 4 | 0 |
| 120-cell | as the 600-cell | 501 | 36 | 0 |
| E8 roots | A8, D8, E7A1, E6A2, A4A4, D4D4, A2⁴, A1⁸, D5A3, A7A1, D6A1A1, A5A2A1, A3A3A1A1, E7, E6, D4, A4, E8 (+ rotation) | 179 | 5 | 0 |

The six 600-cell orbits with two genuine zeros are:

- **The golden pair and their negatives (C1, C2 and C4, C5):** one twisted block each, explained above.
- **The two 20-point conjugacy classes of 2I with Re = ±1/2** (a dodecahedron in a hyperplane, stabiliser W(H3)): zeros 2 and 5. These are ordinary character zeros in two different blocks (3 and 6). An ordinary class has a single rotation angle θ, and χ_Sym^k = U_k(cos θ) = sin((k+1)θ)/sin θ vanishes when (k + 1)θ is a multiple of π. With θ = π/3, that gives k = 2 and k = 5. This is the classical Chebyshev zero at a rational angle (the same rule gives the single zeros k = 4 at θ = π/5 and k = 3 at θ = π/4 in the table). It is forced and known, and it is two independent conditions met by one angle, not one block seen in two degrees.

In the 120-cell (36 orbits with a genuine zero, k ≤ 20) and the 24-cell (4), no orbit has two genuine zeros. For E8, Stab(O) was not enumerated (W(E8) has 696,729,600 elements). Each zero was judged against the listed subgroups for which O is an orbit, plus −I ∈ W(E8) for antipodal orbits. A first run without the −I check flagged 20 orbits silent in every odd degree. All 20 are antipodal, so this is the census's kind (X), and the corrected run flags none. That run also shows the E8 form of the collapse: the roots are a 7-design with 5 cosines, so every odd degree is a nonnegative mix of the degree-1 and degree-3 blocks. The 5 remaining single genuine zeros are T₂ = 0 on 64-point orbits. Limits: one realisation per subsystem type (E8 has two classes for some types, for example A7 and A5A1); the 120-cell blocks were not computed, since its 31 cosine relations are not used as a scheme here; isometries of O outside Aut(P) were not searched.

**Answer to step (3): the twisted-class mechanism yields exactly one double silence in this universe, the golden 5-cell pair.**

## 5. Controls (all passed)

| control | result |
|---|---|
| control member t = 2, permutations of (3, 3, 3, 2, 0) | reflection closure > 600 points (no 600-cell); zeros only 1, 2 |
| every one of the five S5-orbits | zero set predicted from the twisted table = direct zeros, k ≤ 30 |
| wrong claim "the 6-block vanishes on C4" | rejected (T₅(C4) ≠ 0) |
| wrong claim "X is a 3-design" | rejected (T₃(X) ≠ 0) |
| wrong mechanism "Double Vision forces the zero" | rejected: Φ fixes every orbit |
| wrong mechanism "every S5-orbit of the 600-cell is silent in 5 and 7" | rejected (C4, C5) |
| systematic search re-finds the census 20-set type (genuine zeros 5, 7) | yes |
| identity T_k = Σ m(k, ρ) F_ρ on every orbit of the 600-cell, 24-cell and E8 searches | exact, 0 failures |

## Method, files, runs

- `scripts/q5.py`: exact Q(√5) arithmetic and Gegenbauer polynomials.
- `scripts/golden_mech.py`: sections A–G above.
- `scripts/systematic.py`: the search of section 4.
- `data/golden-mech.log` (k ≤ 30) and `data/golden-mech-pilot.log`.
- `data/systematic-600-24.log`, `data/systematic-120.log` and `data/systematic-E8.log`, plus the pilot logs.

Runs went through the job gate on the two compute hosts:

- gac-pilot, gac-mech: FINAL ok;
- gac-sys-pilot, gac-sys-a (600-cell and 24-cell): FINAL ok;
- gac-sys-p120, gac-sys-120: FINAL ok;
- gac-sys-pE8 (pilot; stopped by its 280 s cap after the subgroup phase, which gave the rate), gac-sys-E8 (twice; the second adds the −I check): FINAL ok.

Nothing is left running.

Credits at the point of use: Schur 1911 (spin characters of the double covers of the symmetric groups); McKay 1980 (Sym^k of the binary polyhedral groups); Koca, Ozdes Koca and Al-Ajmi 2012 (the W(A4) split of the 600-cell); Delsarte, Goethals and Seidel 1977, and Bannai, Okuda and Tagami 2015 (designs and harmonic index); Molien 1897 (invariant counts).

DICTO · dictospheres.com
