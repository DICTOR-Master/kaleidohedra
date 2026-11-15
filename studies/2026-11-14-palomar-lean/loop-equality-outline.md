# The Loop Equality (#102, Theorem 1): proof outline for the Lean formalisation (2026-11-15)

**Conclusion.** The formal proof follows #102 Section 2, with two simplifications. The torus integral is replaced by the group ring ℤ[ℤ²]: a walk's planar displacement is the exponent of a monomial, and "the number of walks ending at y" is a coefficient. And Lemma 3 of #102 is used in a form that never needs diamond's symmetry group: every count is shown equal to the count at a fixed reference bond of diamond of the same kind (vertical or slanted).

**Status:** outline fixed; the Lean files follow it one section per file (see `lean/LoopEquality/`).

## 0. The model (as in `lean/LoopEquality.lean`, the Challenge)

- Atoms: `(k, p, u)` with bilayer `k ∈ ℤ`, planar point `p ∈ ℤ²` (the point (i a₁ + j a₂)/3), and `u ∈ {0, 1}` (lower, upper). Its level is ℓ = 2k + u.
- Stacking: `σ : ℤ → ZMod 3` with `σ(k+1) ≠ σ(k)`. A site of G_σ is an atom with p ≡ (σ k, σ k) mod 3.
- Bonds: the vertical bond (k, p, 0)–(k, p, 1), and (k, p, 1)–(k+1, q, 0) for q − p one of the six short vectors.
- The Lean statement: for every stacking σ, site v and m ≥ 1, the number of maps f : ℤ/m → atoms with f(0) = v, f(i) bonded to f(i+1), and f(i+2) ≠ f(i) for all i (cyclic non-backtracking) equals the number at the site (0, (0,0), 0) of diamond (σ k = k mod 3). A separate theorem says these sets are finite, so `ncard` counts them.

## 1. Neighbours (file `Network.lean`)

Let D = {(1,1), (−2,1), (1,−2)} (the vector t and its two rotations), and s_k = +1 if σ(k+1) − σ(k) = 1, s_k = −1 if it is 2. The short vectors from a site of position σ k to a site of position σ(k+1) are exactly s_k·D. So a lower site (k,p,0) has the four neighbours (k,p,1) and (k−1, p − s_{k−1} d, 1), d ∈ D; an upper site (k,p,1) has (k,p,0) and (k+1, p + s_k d, 0), d ∈ D. Every site has exactly four neighbours, and the bond relation is symmetric and irreflexive. The stacking enters only through the signs s_k.

## 2. Walk counts through the group ring (files `Levels.lean`, `Network.lean`)

W_i(x, y) is the number of walks of length i from x to y. Let R = ℤ[ℤ²], g = Σ_{d∈D} X^d and ḡ = Σ X^{−d}.

- **Level generating function.** For levels ℓ, ℓ′ let Q_i(ℓ, ℓ′) ∈ R be the sum over level paths from ℓ to ℓ′ of the product of the step factors: up(ℓ) for ℓ → ℓ+1 and dn(ℓ) for ℓ → ℓ−1, where up(2k) = 1, up(2k+1) = g if s_k = +1 and ḡ if s_k = −1, and dn(ℓ) = conj(up(ℓ−1)). Then W_i(x, y) is the coefficient of X^{p_y − p_x} in Q_i(ℓ_x, ℓ_y) (#102 Lemma 1, with the integral replaced by a coefficient; induction on i).
- **Gauge lemma (any commutative ring).** If up(ℓ)·dn(ℓ+1) = N(ℓ) for all ℓ, then Q_i(ℓ, ℓ′) = H(ℓ, ℓ′)·E_i(ℓ, ℓ′), where H is the product of the step factors along the straight path from ℓ to ℓ′ and E_i is defined by a recursion that uses only N. Here N(ℓ) = 1 for even ℓ and gḡ for odd ℓ, whatever the stacking (#102 fact (i)). This is the ring form of "a closed walk crosses every bond layer as often up as down".
- **Invariances of E.** E_i(ℓ+2c, ℓ′+2c) = E_i(ℓ, ℓ′) and E_i(1−ℓ, 1−ℓ′) = E_i(ℓ, ℓ′) (shift and the reflection of #102 Lemma 2(a)); and E_i is fixed by every ring map that fixes gḡ, in particular by conj (X^a ↦ X^{−a}) and by the rotation ρ of ℤ² of order 3 with ρ(D) = D.
- **Consequences (#102 Lemma 2 (a), (b)).**
  - Same site: W_i(x, x) = coeff₀ E_i(0, 0) for every site of every stacking.
  - Vertical bond: W_i(x, y) = coeff₀ E_i(0, 1).
  - Slanted bond from (k,p,1) to (k+1, p + s d, 0): W_i = coeff_{sd}(g_s E_i(1, 2)). For s = −1 apply conj; for d ∈ D apply ρ. So it equals coeff_{d₀}(g E_i(1, 2)) for all slanted bonds.
  - In the other direction W_i(y, x) = W_i(x, y), because the bond relation is symmetric.

  So W at a site and along a bond does not depend on the stacking or on the place, only on the kind of bond. #102 proves the equality of the two kinds through diamond's symmetry; the formal proof does not need it.

## 3. From walks to loops (file `Graph.lean`; any graph with four neighbours at every vertex)

This is #102 Lemma 3 together with the standard recursion for non-backtracking walks (Hashimoto 1989; for the closed walks themselves, Nagle 1966 and Thorpe 1972).

- A_j(x, y): non-backtracking walks of length j. With q + 1 = 4 neighbours everywhere, A₀ = W₀, A₁ = W₁, A₂ = A·A₁ − 4A₀, A_{j+2} = A·A_{j+1} − 3A_j (j ≥ 1). Hence A_j(x, y) = Σ_i c_{j,i} W_i(x, y) with integers c_{j,i} that depend only on j and i (written as a polynomial p_j evaluated on the walk counts).
- nb_k(a, b, y): non-backtracking walks from b with previous vertex a, of length k, ending at y. Then nb_{k+1}(a, b, y) + nb_k(b, a, y) = A_{k+1}(b, y).
- F_k(a, b; c, d): non-backtracking edge sequences e₀, …, e_k with e₀ = (a, b) and e_k = (c, d) (the entry of the k-th power of the Hashimoto matrix). Then F_{k+1}(a, b; c, d) + F_k(a, b; d, c) = [d ~ c]·nb_k(a, b, c).
- **Transfer lemma.** If two such graphs have bonds (a, b) and (a′, b′) with equal A_j on the four pairs from {a, b} and from {a′, b′}, then F_k(a, b; a, b) = F_k(a′, b′; a′, b′) for every k. This is proved by induction on k: the identities above determine nb and F on these pairs from A.
- **Loops.** For m ≥ 3, a closed non-backtracking loop f of length m at v is the same as an edge sequence e_i = (f(i), f(i+1)), i = 0, …, m, with e_m = e₀. So the number of loops is Σ_{b ~ v} F_m(v, b; v, b). For m = 1, 2 there are no loops: f(i+2) = f(i).

## 4. The theorem (file `Main.lean`)

Take a site v of G_σ and m ≥ 3. Its four bonds are one vertical bond and three slanted bonds. By Section 2, each has the same W (and so, by Section 3, the same A) on its four pairs as the reference bond of its kind in diamond: (0,(0,0),0)–(0,(0,0),1) or (0,(0,0),1)–(1,(1,1),0). By the transfer lemma each term F_m(v, b; v, b) equals the reference value of its kind, so the number of loops at v is T_vert + 3·T_slant. That is the same for every site of every stacking, in particular for diamond's (0,(0,0),0). Finiteness comes from the same bijection: the loops at v inject into a finite set of edge sequences.

## 5. Correspondence with #102

| #102 | Formal proof |
|---|---|
| Lemma 1 (torus integral) | coefficient in ℤ[ℤ²] of Q_i (Section 2) |
| facts (i), (ii) | (i): up·dn = N with N independent of σ; (ii) replaced by the order-3 rotation fixing D and by conj |
| Lemma 2 (a), (b) | Section 2 consequences (Lemma 2 (c) is not needed for Theorem 1) |
| Lemma 3 and the A_j recursion | Section 3 |
| Proof of Theorem 1 (counts at every site equal diamond's) | Section 4 |
| the explicit series and values (Ihara–Bass, Domb numbers) | **not formalised**; the Lean statement is the equality with diamond's count, which is the content of Theorem 1 |

No extra hypothesis is needed: the statement holds for every m ≥ 1 (for m = 1, 2 both counts are 0).

## 6. Correspondence notes: Lean names and #102 (formal proof finished 15 Nov 2026)

| Lean declaration (file) | Meaning | #102 |
|---|---|---|
| `IsStacking`, `diamond`, `Atom`, `IsSite`, `shortVecs`, `Bond`, `nbLoops` (`Defs.lean` = the Challenge definitions, unchanged) | stacking, network, loops | Section 1, "The network of a stacking", "Loops" |
| `triD`, `sd σ k d` (`Network.lean`) | D and ε_k·d | Section 2, "Levels" |
| `nbr`, `regular`, `bond_iff` (`Network.lean`) | four neighbours; Bond ↔ neighbour at a site | "Every atom has four bonds" |
| `Graph.W`, `W_eq` (`Graph.lean`, `Counts.lean`) | walk counts as coefficients in ℤ[ℤ²] | Lemma 1 |
| `Levels.Q_eq`, `Levels.E_shift`, `Levels.E_refl`, `Levels.E_map` (`Levels.lean`) | gauge: Q = H·E, with E depending only on N = up·dn | fact (i), and the reflection in Lemma 2 (a) |
| `W_site`, `W_vert`, `W_cross`, `W_nbr` (`Counts.lean`) | site and bond walk counts are independent of the stacking | Lemma 2 (a), (b); closed walks: Nagle 1966, Thorpe 1972 |
| `rhoE`, `E_inv`, `coeff_gs_cross` (`Counts.lean`) | the conjugation and order-3 rotation remove the choice of triangle and of bond | fact (ii), in the weaker form needed |
| `Graph.A_eq_ev`, `Graph.nb_add`, `Graph.F_add`, `Graph.transfer` (`Graph.lean`) | non-backtracking recursion; loops through a bond determined by walks | Lemma 3 (standard recursion: Hashimoto 1989, Bass 1992) |
| `Graph.loops_ncard` (`Graph.lean`) | loops at v = Σ_b F_m(v, b; v, b), finitely many | "t_m(v) = Σ τ_m(e)" in the proof of Theorem 1 |
| `F_bond`, `total`, `loop_equality`, `nbLoops_finite` (`Main.lean`) | every site: T_vert + 3·T_slant | proof of Theorem 1 |

**Credits at the point of use.** The equality of closed-walk counts (`W_site`) is Nagle's observation for ice (1966) and Thorpe's theorem for periodic polytypes (1972); the formal proof reproves it for all stackings, aperiodic ones included. The layer-gauge mechanism is the one of He, Wilson and Ganesh (2024) for band structures. The non-backtracking recursion is standard (Ihara 1966; Hashimoto 1989; Bass 1992).

**Differences from #102.**
- Diamond's 24 symmetries are not used; each bond is compared with a reference bond of diamond of the same kind. So the formal proof does not show that vertical and slanted bonds have the same count, and Theorem 1 does not need it.
- Lemma 2 (c) is not needed for Theorem 1.
- The neighbour formula is applied at every atom, not only at sites, so the neighbour graph is 4-regular everywhere; at sites it agrees with `Bond` (`bond_iff`).
- **No extra hypothesis was needed.**
