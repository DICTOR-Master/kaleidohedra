# Referee proof check: Tang, "Lusztig's Fourier matrix conjecture for finite noncrystallographic Coxeter groups" (aiXiv 2611.01161)

Source checked: `pkg/Lusztig_Fourier_Conjecture.tex` (1500 lines, dated 12 Nov 2026). Line numbers below refer to that file.
Already done before this check, and not repeated here: the author's full verification chain and 7 extra checks were rerun and passed (74×74 certificate, 5476 entries, T^60 = I, error < 3.4e-140, S = F).

My own checks (I did not import or run any of the author's code):
- `check/referee_checks.py` → `referee_checks_out.txt` / `.json`. It covers the separation-bound arithmetic, decoding the appendix HS4 matrix plus its exact identities, modular-data sanity checks on the target, the pointed and Fibonacci matrices against CHEVIE formulas I reimplemented from the GAP source text, the SU(2)_8 / K4 table, the D0 dimension, the Gram determinants, the family counts from CHEVIE `coxh3.g` / `coxh4.g`, the Alvis rank-24 ring (read from the author's parsed JSON) and H4 word lengths from my own root system.
- `check/crossed_fusion_check.py` → `crossed_fusion_check_out.txt`. This is my own model of the based ring of C0(A3) ⋊ C2 with the paper's labelling. It checks associativity, the duality formula, all 48 tube-corner dimensions against Table `tab:frames`, and the selected-algebra dimensions 306/153.

Status labels used below:
- **Verified**: I did the working myself.
- **Verified mod citation**: the deduction is correct, given a cited theorem I could not open here.
- **Computation only**: the step rests on the finite computation that we reran. I did not redo it independently.
- **Gap**: a step that is stated or sketched but not proved in the paper.
- **Error**: a false statement.

---

## 0. Overall verdict

**No mathematical errors found. Several gaps, all of the "sketched / asserted / outsourced" kind. One external dependency is decisive and unrefereed.**

- The written chain is logically coherent. Every arithmetic and combinatorial claim I could test is correct: the separation bound, all 48 corner dimensions, the K4 table, the Alvis products, the dimensions, the family counts, the small Fourier matrices, the unit identification and the HS4 identities.
- For the middle H4 cell, the result is **conditional on He–Liu, arXiv:2610.41811v1** (preprint, 30 Oct 2026, not refereed). That paper supplies:
  - the fixed-seed uniqueness D0 ≃ C0(A3), and
  - the regular endofunctor model whose tube algebra is actually computed (§6, line 801).
- The three pointed cells (H3 a=3, H4 a=3, H4 a=18) rest on Lemma `lem:symmetric`. That lemma's key step is only sketched. It decides between twisted and untwisted Vec_{C2}. The two choices give **different** S-matrices: the untwisted choice gives exactly the *pairing* form LTQZ2, the twisted choice gives the *modular* form TQZ (my check 11a–c). The paper's answer contradicts Rogel's thesis Thm 5.39. The conflict is recorded in the author's audit notes but not mentioned in the paper.
- Corollary `cor:products` (all finite Coxeter groups) goes beyond what the paper proves for the Weyl-group factors.

---

## 1. Main theorem and reduction (lines 79–132, 1087–1126)

| Item | Status | Working |
|---|---|---|
| Irreducible noncrystallographic types are I2(m) (m=5 or m≥7), H3, H4 | Verified | Standard classification. Minor wording: Thm 1 line 105 says "every I2(m), m≥3", which includes the crystallographic A2, B2, G2. This is harmless. |
| H3 has 7 two-sided cells, H4 has 13; table rows (lines 1104–1119) | Verified against CHEVIE | Parsed `chevie_coxh3.g` / `chevie_coxh4.g` (7a/7b). H3: 7 families, 16 unipotents, a ∈ {0,2,5,15} singletons, {1,6} Dihedral(5), {3} TQZ. H4: 13 families, 104 unipotents; singletons a ∈ {0,4,5,15,16,60}, Dihedral(5) a ∈ {1,2,22,31}, TQZ a ∈ {3,18}, HS4 (74) a=6. Center ranks equal family sizes: 1, 4, 4, 74. Number of two-sided cells = number of families is standard. |
| Corner ranks per cell (1, 2, 2, 24) | Verified mod citation | Cited from RT Example 5.1. The a=6 rank 24 is consistent with the Alvis data (8a–f). |
| Dihedral center-rank formula (lines 1092–1098) | Verified | Equals the CHEVIE Dihedral(e) family size for every m = 3..40 (7c). |
| Dihedral case (lines 1090–1099) | Verified mod citation | Rests entirely on RT Thm 4.8 and 4.21. I could not check RT. I did check one point independently: in the a=1 dihedral cell, the diagonal H-cell is {s, sts, ststs, …} (all odd lengths). So the sign character ε of Prop 3.1 is trivial and the EW pivot is the positive one. No pivotal sign subtlety can arise here. |
| Assembly (proof of Thm, lines 1122–1126) | Verified (given the components) | Every row of the table is covered. |

---

## 2. Conventions: spherical structure and modular Fourier matrices (lines 85–98, 433–452)

- **Normalisation (eq. Sdef)**: Dim Z(C) = (Dim C)², so the denominator is Dim C. **Verified** (standard).
- **Convention 1.1, F^mod = F^pair · P_♭.**
  - *Fibonacci block.* I reimplemented CHEVIE `Dihedral(5)` from the GAP text. Its `fourierMat` is already **exactly** eq. (FibS), in the natural order [0,1],[0,2],[1,2],[1,3] (4e). Its trace is 0. Swapping the last two columns gives trace 2 (4c).
    - So the paper's remark "unconverted pairing trace 2, (FibS) trace 0" is **verified**, where "pairing" means Lusztig's / Broué–Malle's original matrix.
    - Clarity point (not an error): CHEVIE's Dihedral(5) matrix is already the modular one; CHEVIE's `perm=(3,4)` records ♭. A reader who takes CHEVIE as "the" Fourier matrix, as the paper does for HS4, needs no conversion.
  - *eq. (FibS)* equals the tensor square of the Fibonacci S matrix, in the order (1,1),(u,u),(1,u),(u,1) (4a). **Verified.**
  - *Pointed block.* CHEVIE `TQZ(2,-1,[1,-1])`, reimplemented from the GAP text, equals eq. (pointedS) entrywise in the paper's order (0,1),(0,-1),(1,i),(1,-i) (3d). Its square is I, so ♭ is trivial for TQZ (3f). **Verified.**
  - *HS4.* F is symmetric and F² = I exactly (2b–d). (F T^{±1})³ = F² with λ = 1, to 1e-15, using the appendix t-vector (2l). The Gauss sum has |Σ d²θ| = D (2m). The Verlinde fusion coefficients come out as nonnegative integers (2n). So the HS4 block is already a modular (S,T) pair, consistent with "no additional one-sided permutation" (line 97). **Verified** as a property of the target.
- Whether "the Fourier matrix" in Lusztig's conjecture *means* the modular form is a convention, cited to Lacabanne §3.1 and RT §4.6. I could not check those references.

**Important observation (my checks 11a–c):** for the order-two pointed corners, the convention is not cosmetic.
- Z(Vec_{C2}) (untwisted) with EW dimensions (1,1,−1,−1) has S equal to CHEVIE's `LTQZ2`, the Lusztig pairing form, exactly.
- Z(Vec_{C2}^−) with the same dimensions gives `TQZ`, the modular form.
- No simultaneous permutation turns one into the other.
- So the theorem's assertion for these three cells depends jointly on (a) the modular convention and (b) ω = −1 (see §4).

---

## 3. Relative Hodge–Riemann and pivotal signs (Prop 3.1 `prop:sign`, lines 232–343)

| Step | Status | Working |
|---|---|---|
| Cup/cap adjointness, one colour (lines 258–273) | Verified (formal) | The displayed identity is the stated Frobenius normalisation. Extension through tensor products and projectors is asserted, citing EW §2.4 / Soergel calculus. |
| eq. (adj-bend) S_Y(T_X(v)^†) = v^† | Plausible, not re-derived | Snake identity plus (capadjoints). Lines 284–288. |
| eq. (EWadjunction): 1_Y = T_X(e_X)M^a u and μ_Y = S_Y(u)M^a | **Verified mod citation (critical)** | This is a transcription of EW §5 (Prop 5.6, Remark 5.8) that I cannot check here. Everything downstream depends on its exact form, including which side the M^a sits on and the handedness. The author's audit notes say this was a point of repeated review. |
| eq. (Gramtrace) from (adj-bend) + (EWadjunction) | Verified | Put T_X(e_X)^† = cu. Then c·u^†M^a u = 1, and S_Y(u) = c⁻¹e_X^†, so dim^R = c⁻¹ e_X^† M^a e_X. |
| Degree −a line is primitive | Verified | Uses deg h_{x,y,z} ≤ a(z) (the a-function bound; holds via EW positivity). M^{a+1} sends degree −a to degree a+2, where everything vanishes. |
| eq. (RHRsigns) | Verified mod citation | The RHR sign (−1)^{(ℓ(x)+ℓ(y)−ℓ(z)−k)/2} applied to (x, x⁻¹, d) and (x⁻¹, d, x⁻¹) gives exactly the two displayed exponents. |
| sgn dim^R_EW(A_x) = (−1)^{ℓ(x)−a} | Verified | (ℓ(d)−a)/2 + (2ℓ(x)−ℓ(d)−a)/2 = ℓ(x)−a; checked exhaustively in 10a. Integrality: ℓ(d) − a = 2δ(d). |
| ε is a monoidal automorphism of Id | Verified | Parity (eq. parity) with k = −a. |
| Positive multiplicative character = FPdim; uniqueness of positive spherical structure (ENO Prop 8.23); sphericality; ε_{x⁻¹} = ε_x | Verified | Standard. Each step is correct. |
| Cor 3.2: S_EW = D_δ S_+ D_δ | Verified | The pivotal twist multiplies traces by δ_Zδ_{Z'}. |
| Lemma 2.1 `lem:corner` (corner restriction is pivotal / ribbon) | Verified mod citation | Rests on RT Prop 3.8. Proof is brief but standard. |
| §2.4 upper vs lower truncation (lines 221–228) | Gap (sketch) | M_12 and M_23 commute (true: ρ is inserted in different slots). The claims that ϑ is a monoidal comparison and that its dual is ϑ_{Y^∨,X^∨} are asserted, citing EW Rem 5.7. This only matters for comparison with Lusztig's original upper-truncation formulation. |

Consistency checks I did:
- The Fib-corner sign character is forced to be trivial (t² = 1 and t² = t give t = 1, check 4i).
- In the middle cell, all nine Alvis representative words have even length (10…44) under a,b,c,d → s4,s3,s2,s1 (9d). This agrees with ε ≡ 1 there.
- The unit x2 is an involution of length 14, so ℓ − a = 8 is even.

---

## 4. Pointed and Fibonacci corners (§4, lines 345–454)

**Lemma 4.1 `lem:symmetric` (lines 350–371). Gap: the key step is a sketch.**
- *What it is for.* It asserts that the Frobenius–Schur-type sign of B_x for the ordinary pivot is +1. That is, q^∨ j = q rather than −q.
- *What the proof gives.* (i) Hom⁰(B_x, B_x^∨) is one-dimensional, so q^∨ j = ±q. (ii) In the balanced realisation, rotating a rank-two rex move gives the coefficient [m−1] = sin((m−1)π/m)/sin(π/m) = 1. I checked (ii); it is trivially true.
- *What is missing.* The decisive sentence, "Thus q and q^∨j preserve the same one-tensor", needs a careful bookkeeping of how the top-summand projector and its rotation act on the bottom one-tensor of B_x^∨. That bookkeeping is not written out.
- The isometry rescaling (second paragraph) is fine.

**Prop 4.2 `prop:pointed` (lines 373–388). Verified, given Lemma 4.1. One transfer step is not stated.**
- *Working.* With a symmetric q, dinaturality gives ev_{X^∨}(j⊗1)(1⊗q) = ev_X(q^∨j⊗1) = ev_X(q⊗1). So dim^R(X) equals the pairing∘copairing composite of a single self-duality. In a unit-normalised skeletal Vec_{C2}^ω, the snake identity forces that composite to be ω(x,x,x)⁻¹ = ω (check 3h). Hence ω = dim_EW(A_x) = (−1)^{ℓ(x)−a}.
- *Missing line.* The argument needs truncated duals of degree-0 maps to agree with ordinary duals, so that Lemma 4.1 (a statement about the ordinary Soergel category) transfers to the asymptotic category. This is plausible, because a bimodule map commutes with middle insertion of ρ, but it is not stated.

**Cell data for the pointed corners (lines 390–407). Verified (lengths), verified mod citation (cells).**
- With m12 = 5 and m23 = m34 = 3, my own H4 root system (120 roots, ℓ(w0) = 60, w0 = −1) gives:
  - ℓ(232) = 3, ℓ(232123) = 6, both involutions;
  - ℓ(w0·232) = 57, ℓ(w0·232123) = 54 (9b).
- The unit must have ℓ ≡ a (mod 2): 3 ≡ 3 and 54 ≡ 18. So ω = (−1)^{6−3} = (−1)^{57−18} = −1. **Verified.**
- Since w0 is central, w0 maps diagonal H-cells to diagonal H-cells. The a=3 ↔ a=18 correspondence agrees with CHEVIE: unipotents 18,20 have a=3 and A=42, and 60 − 42 = 18.
- That {232, 232123} *is* the diagonal H-cell is cited (Rogel thesis §1.4.3–4; RT Ex 5.1). I did not recompute KL cells. "Corresponding parabolic diagonal corner of H4" (line 391) is not argued: the H4 left cell can be larger than the parabolic one. The rank 2 is taken from RT.

**Pointed S matrix (eq. pointedS) and Remark 4.3. Verified.**
- Semion ⊠ antisemion with D = diag(1,1,−1,−1) gives eq. (pointedS) (3b).
- It equals CHEVIE TQZ in the stated order (3d).
- Swapping the first two indices of S_+ gives the same matrix, as Remark 4.3 says.

**Conflict to flag (not addressed in the paper).**
- Rogel's thesis Thm 5.39 identifies this corner as *untwisted* Vec(C2). The author's `SOURCES_AND_AUDIT.md` §3 records the conflict; the paper does not mention it.
- By my check 11a, untwisted + EW pivot gives exactly the pairing matrix LTQZ2. So the two sources would disagree on whether the modular-convention conjecture holds for these cells.
- Independent evidence for the paper's ω = −1: the CHEVIE Frobenius eigenvalues of these families are (1,1,±i) (3e). Z(Vec_{C2}) has twists (1,1,1,−1) and no ±i, so only the twisted corner is compatible with the full (S,T) modular data.
- The paper's written proof of ω = −1 is still only as strong as Lemma 4.1. The author's package reports a direct Q(φ) Soergel computation for H3 a=3 giving Ω = −1, but that computation is not in the paper.

**Fibonacci corners (lines 433–454). Verified mod citation (Ostrik).**
- The sign character is trivial, so dim u = φ, which is the positive Fib branch.
- The Fib F-block squares to I (4f).
- A diagonal tensorator commuting with it must satisfy λ = μ² (I re-derived this; it is used in §5.3).

---

## 5. Morita equivalence for the a=6 H4 cell (§5, lines 455–747)

| Step | Status | Working |
|---|---|---|
| Alvis corner: eqs. (alvis1–3), generation by a0,b, FPdim = D = 1080+480√5 | Verified against the author's parse of Alvis | On `alvis_ring_24.json` (data only), with N[i][j][k] = coefficient of x_k in x_i·x_j: associative with unit x2. The products are exactly as stated, including a0b = x15 and ba0 = x14 (8c). a0 and b reach all 24 basis elements (8f). Σ FPdim² = D (8d). The K4 sub-table is exact (8g). The opposite convention swaps x14 and x15, which is harmless because only their distinctness is used. Not done: re-parsing Alvis's original tables. |
| Independent cross-check of D | Verified | HS4 entry F[9,9] = (9−4√5)/120 = 1/D exactly (2g). |
| Aut_⊗(Id_C) = 1 (eq. AutC) | Verified | a0² ∋ 1, a0 and b² ∋ 1, b, plus generation. |
| K4 table = even part of SU(2)_8, dims (1,φ²,2φ,φ²,1) | Verified | Truncated Clebsch–Gordan computation (5a–c). |
| A = 1⊕g is a separable algebra: ω restricted to ⟨g⟩ is cohomologically trivial | Verified | add(b) is a rank-one ⟨g⟩-module category, so dμ = ω. |
| D := _A C_A, Dim = FPdim = D, unique positive spherical structure | Verified mod citation | ENO. |
| h = A_τ is invertible, not the unit, h⊗h ≅ 1 with trivial associator; T = conjugation by h | Verified | Hom(A, A_τ) = 0 by the g-sign argument. The associativity identity holds because τ is an algebra automorphism. |
| B ≃ Fib ⊠ Vec_{C2} | Verified in outline, terse (Gap, minor) | Aut 2-group of Fib is trivial: λ = μ² (check 4f/4g), and t² = 1 = t. The step "their two coherence equations are its pentagon" (line 553) is asserted. |
| E ≃ SO(3)_q tensor equivalence; g is a transparent boson | Verified mod citation (EO Thm A.3) | Twist and monodromies equal 1 for *any* primitive 20th root (q^{40} = q^{20k} = 1), so the conclusion does not depend on which q. My SU(2)_8 computation gives θ_8 = 1 and monodromy 1 with every even label (5d). |
| K = E_A has rank 4 with dims 1, φ, φ, φ²; p, q self-dual; p² = 1+p, pq = r; K ≃ ⟨p⟩⊠⟨q⟩ | Verified | Re-derived the duality and Frobenius-reciprocity argument line by line. Dim K = Dim E / 2 = (1+φ²)² (5e). |
| _A E_A = K ⋊ C2 (line 585) | **Gap (uncited)** | Stated without proof or reference. True as a standard fact (Morita dual of an equivariantization), but should be cited. |
| T(p) = q | Verified | The module structures on b differ by the sign of g, and τ swaps them. The "rank 8 ≠ 5" equivariantization check is correct. |
| Mixed products (eq. mixedproducts); p, m, q distinct; endpoints commute; middle generator commutes with neither | Verified | Free-module presentation plus the Alvis products above. |
| Lemma 5.1 `lem:matching` (based ring → Coxeter system with the Hecke–Fibonacci rule) | **Verified, full proof re-derived** | N_s symmetric with N_s² = I+N_s gives an exactly-one-off-diagonal matching with ε(Pb) = 1−ε(b). Commutation L_sR_t = R_tL_s gives P_sQ_t = Q_tP_s (I also handled the coincidence case P_sQ_t b = b, which the paper glosses). Q_t(1) = P_t(1) = x_t. Simple transitivity holds. The first-change argument gives the exchange condition. |
| Lemma 5.2 `lem:A3` | Verified mod citation (HL) | Path diagram p–m–q with equal labels k, because T swaps the endpoints. det G = 1 − 2cos²(π/k) > 0 only for k = 3: k=4 gives 0, k≥5 is negative (6c). The positive-definiteness sketch for a finite Coxeter group is standard. HL's fixed-seed hypotheses are met. |
| FPdim D0 = 540+240√5; D = D0 ⊕ D0h | Verified | Σ_{w∈S4} φ^{2ℓ(w)} = 540+240√5, and twice that is D (6a/b; also from my own model). |
| Lemma 5.3 `lem:marked` | Gap (terse) | Correct: the stationary maps are intrinsic, the loop scalar κ ≠ 0 forces c = 1, and Aut(Id) = 1. The assertion that "these reductions … and braid maps generate all matrix units" (line 711) is the crux of naturality and is asserted, not proved. Plausible, by path-basis counting. The value −φ⁻¹ is the (2,2) entry of the Fib F-block, consistent with eq. (loopscalar). |
| T ≅ σ as actions; C2 coherence | Verified | Any autoequivalence restricted to ⟨Y_s⟩ is automatically "marked", because Fib's Aut 2-group is trivial. The discrepancy between the two actions lies in Aut_⊗(Id_{D0}) = 1. |
| Prop 5.4 `prop:morita` | Verified mod citation | The crossed-product functor is well defined and essentially surjective by (Dgrading). The braided equivalence of centres is ribbon by uniqueness of the positive pivot (ENO). EW pivot = positive pivot by (AutC). Lemma 2.1 identifies the result with Z(A_c). |

---

## 6. Model, tube centre, the 74 objects (§§6–7, lines 748–982)

Most of this section is **computation only**: the rank 40 + 32 + 2, the frame ranks, R² = I, T^60 = I, the 96 snake identities and the twist orders 60, 30, 2. The finite computation was rerun and passed. The mathematical scaffolding I checked:

- **The model is a realisation of C0(A3) ⋊_σ C2.** Verified mod citation (HL §§4–6, line 801). This is the second place where HL is load-bearing.
- **Fusion combinatorics.** My own construction of the 48-label based ring (BFS word order, σ(w)(i) = 3 − w(3−i), (w,g)·(w',g') = X_w X_{σ^g w'} h^{g+g'}) gives:
  - an associative ring;
  - the paper's duality formula;
  - all 48 tube-corner dimensions Σ_s Σ_k N_{si}^k N_{is}^k equal to Table `tab:frames` (48, 22, …, 666; 16, …, 778), with no mismatch;
  - selected-boundary algebras of dimension 306 with an even part of 153, both sectors;
  - J0 and J1 fixed by σ;
  - label 47 = (w0, 1).
  
  **Verified.**
- **Lemma 7.1 `lem:frames`.** Verified. I re-derived it with block-matrix decomposition. The inductive use of already-visible sources is valid, because e_j ∈ TeT when I_j = 0.
- **The missing-ideal logic (lines 902–921).** Verified as logic: the surjections show kernel ⊆ I_47, and the visibility of 45 shows I_47 ⊆ kernel. The rank numbers themselves are computation only.
- **I_47 ≅ M2 ⊕ M2, giving 2 objects with n_Z = m_47 = 2.** Logic verified.
  - Independent consistency check: the underlying object is 2·X_{(w0,1)} of dimension 2φ⁶ = 18+8√5. This equals D·F[9,73] and D·F[9,74] exactly (2j).
  - The two objects contribute 8 to dim T_47 = 778, matching the 8-dimensional kernel.
- **Dimension formula (eq. tubedim).** Verified on the toy cases Vec and Vec_{C2}.
- **Rotation normalisation (GI).** Verified mod citation. The orientation is irrelevant because F is real (F² = I).
- **Consistency observation.** The author's notes give rank 29 for the ordinary Z(C0(A3)). A C2-gauging count with f = 17 σ-fixed simples, all twisted-sector objects fixed, gives 2·17 + 12/2 = 40 and 2·17 = 34 = 32 + 2. This matches the 40 / 34 split by boundary parity. It is only a consistency check, and the 29 is not in the paper.

---

## 7. Exact comparison and separation bound (§8, lines 983–1086). Redone.

- **Lemma 8.1 `lem:primitive`.** Verified.
- **eq. (ABchecks).** Verified exactly with Python integers: A and B symmetric, A² + 5B² = 14400·I, AB + BA = 0 (2b–d). Both real embeddings are orthogonal (2e).
- **eq. (DFintegral).** Verified: D/120 = 9+4√5 and D√5/120 = 20+9√5 (1g).
- **Lemma 8.2 `lem:separation`.** Verified. Working:
  - N_{Q(√5)/Q}(1080+480√5) = 1080² − 5·480² = 14400 (1a).
  - [Q(ζ60):Q] = φ(60) = 16 (1b), so N_L(D) = 14400⁸.
  - √5 = ζ5 − ζ5² − ζ5³ + ζ5⁴ lies in L (1f), so F_kl ∈ L.
  - D·S_ij is an algebraic integer by balancing: integer N, roots of unity θ, algebraic-integer dimensions.
  - All Galois conjugates of S are unitary (L is abelian), and all conjugates of F are orthogonal, so |σ(δ)| ≤ 2.
  - Hence 1 ≤ 14400⁸ · |δ|² · 2¹⁴, which gives |δ| ≥ 1/(2⁷·14400⁴) = 1/5503765708800000000 ≈ 1.8169e−19 (1c, 1d).
  - The certified error 3.422e−140 is far below this (1e).
  - S ∈ Q(ζ60) follows from Ng–Schauenburg (entries of S lie in Q_N with N = ord T = 60). The theorem is correct; I did not verify the exact proposition numbers "Prop 5.7 / Rem 5.8".
- **Prop 8.3 `prop:74S`, unit identification.** Verified.
  - Row 9 is the *only* strictly positive row of F (2f).
  - D·F[9,·] is positive, with Σ(D·F_{9j})² = D² exactly (2h, 2i).
  - The 5476-entry equality itself is computation only (rerun).

---

## 8. Remaining cells and the corollary (§9)

- Rank-1, Fibonacci and pointed cells: as in §4 above. They rest on Lemma 4.1 for the pointed cells, on Ostrik for Fib, and on RT / Rogel for the cell data.
- **Cor 9.1 `cor:products`: Gap.**
  - The direct-product statement is fine.
  - The final sentence, "holds for arbitrary finite Coxeter groups … using the established Weyl-group case", needs the Weyl case *in the same conventions*: Soergel realisation, inherited EW pivot, modular convention. The proof only cites Lusztig 2015 and RT §3.4.
  - Pivot signs and the pairing/modular distinction are exactly what my check 11a shows can change the answer. CHEVIE uses the Lusztig-form LTQZ2 for E7/E8 families.
  - This is an extra claim, outside Theorem 1.

---

## 9. Scope caveat: where is "identification with the original H4 cell" proved?

The certificate's scope string (`full74_S_exact_certificate*.json`, key `scope`) defers the identification to a "separate mathematical interface". In the paper that interface is:

1. **§5 (lines 455–747), culminating in Prop 5.4 `prop:morita`**, eq. (ribbon): Z(A_c) ≃_ribbon Z(C0(A3) ⋊_σ C2). It uses Lemmas 5.1–5.3, the constructions of A, h and T, and the grading (Dgrading).
2. **Prop 3.1 + (AutC)**: the inherited EW pivot equals the positive one on this corner.
3. **Lemma 2.1**: the corner reduces to the full cell, pivot and traces included.
4. **§2.4**: the lower-truncation convention matches Lusztig's upper one.
5. **§6, line 801 (HL §§4–6)**: the computed regular model *is* C0(A3) ⋊_σ C2 with σ strict.

**Completeness.**
- The interface is proved in the paper modulo the external inputs listed in §10.
- Steps 1–3 are written out. I checked them as above and found no error.
- Within them there are three terse points:
  - _A E_A = K ⋊ C2 is uncited;
  - the generation claim in Lemma 5.3 is asserted;
  - the mixed-associator coherence in B ≃ Fib ⊠ Vec_{C2} is asserted.
- Step 4 is a sketch.
- Step 5, and the equivalence D0 ≃ C0(A3) in Lemma 5.2, are not proved in the paper. Both are imported from He–Liu (arXiv:2610.41811v1, unrefereed, posted 30 Oct 2026).

So the interface is complete *conditionally on HL*, not unconditionally. The paper is transparent about this (lines 217, 1285).

---

## 10. What rests only on cited results

- **He–Liu, arXiv:2610.41811v1, Thms 1.3 and 1.5 plus §§4–6.** Unrefereed and the most load-bearing input. It supplies the existence of C0(A3), the fixed-seed tensor uniqueness, and the unitary regular endofunctor model used for every tube computation.
- **Elias–Williamson (JEMS 2021) Thm 3.4, Prop 5.6, Rem 5.7–5.8.** Relative hard Lefschetz and Hodge–Riemann, rigidity of the truncation, the explicit Hom-adjunction including where M^a sits, and the inherited pivot. Also EW Soergel calculus §5.6 for rex-move rotation.
- **Etingof–Ostrik Thm A.3.** K_l (l=4) categories are SO(3)_q.
- **Ostrik 2003.** Rank-2 classification (Fib vs Yang–Lee).
- **ENO 2005 Thm 2.15, Cor 8.14, Prop 8.23.** Morita invariance of dimensions; uniqueness of the positive spherical structure.
- **Ng–Schauenburg 2010.** Normalised S lies in Q(ζ_{ord T}).
- **Grossman–Izumi §2.3.** Tube-algebra rotation normalisation.
- **Rogel–Thiel (Represent. Theory 2026).** Prop 3.8 (corner reduction), Thms 4.8 and 4.21 (the whole dihedral case), Example 5.1 (cell and corner data), §4.6 (Fourier convention). Also Lacabanne §3.1 for the convention.
- **Alvis 2008.** Rank-24 ring. I checked the paper's claims against the author's parse, not against the original tables.
- **Rogel thesis §1.4.** H3 a=3 diagonal H-cell {232, 232123}.
- **Lusztig CRM monograph Cor 11.7(d).** w0 maps cells to cells.
- **CHEVIE (Michel).** The target HS4 data; the appendix itself fully specifies it.
- **Weyl-group case** (for Cor 9.1 only): Lusztig 2015 via RT §3.4.

Checked only by the reran computation: every rank in §§6–7, the R and T matrices, the primitive idempotent enclosures, the 74×74 S enclosure, and the 5476 comparisons.

---

## 11. List of gaps (none is an error)

| # | Location | Kind | Severity |
|---|---|---|---|
| G1 | Lemma 4.1 `lem:symmetric`, lines 358–363 ("Thus q and q^∨j preserve the same one-tensor") | Key step sketched | **High for the 3 pointed cells.** It decides twisted vs untwisted, which changes S (pairing vs modular form). It conflicts with Rogel's thesis Thm 5.39, and the paper does not mention this. Twist data supports the paper's answer. |
| G2 | Prop 4.2, line 381 | Transfer of the ordinary symmetric self-duality to truncated duality is not stated | Low. |
| G3 | eq. (EWadjunction), lines 292–297 | Exact form taken from EW §5; not checkable here | Medium. Prop 3.1's signs depend on it. |
| G4 | §2.4, lines 221–228 | Sketch of the upper/lower truncation comparison | Low to medium. |
| G5 | Line 585: "_A E_A is the crossed product of K…" | No proof or citation | Low (standard). |
| G6 | Lemma 5.3, line 711: "…generate all matrix units" | Asserted | Medium (crux of marked rigidity). |
| G7 | Line 553: B ≃ Fib ⊠ Vec_{C2} coherence | Asserted | Low. |
| G8 | Lemma 5.2 and §6 line 801 | Outsourced to HL (unrefereed preprint) | **High: conditional dependency for the a=6 cell.** |
| G9 | Lines 391, 396, 1102 | Cell and corner data, including "corresponding parabolic diagonal corner of H4", cited and not argued | Low to medium. |
| G10 | Cor 9.1, lines 1134, 1142 | Weyl-group case in the same conventions not established | Medium (claim beyond the main theorem). |
| G11 | Line 105 | "every I2(m), m≥3" includes crystallographic types | Wording only. |
