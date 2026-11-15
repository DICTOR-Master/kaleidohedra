module

public import Mathlib
public import LoopEquality.Counts

@[expose] public section

/-!
# The closed walks at a site, explicitly (#102, Proposition)

For every stacking and every atom `x`, the number of closed walks of length `i`
at `x` is `closedWalks i`: `0` for odd `i`, and for `i = 2n`

  `W₂ₙ = Σ_{a ≤ n} C(n, a)² · H(a)`,  `H(a) = Σ_{i+j+k=a} (a! / (i! j! k!))²`,

where `H(a)` is the number of closed walks of length `2a` on the honeycomb net
(OEIS A002893). This is #102's Proposition ("the closed walks of diamond as a
chain"), which reads Peter Bala's comment on OEIS A002895 as walks: the values are
the Domb numbers 1, 4, 28, 256, 2716, … (C. Domb 1960; OEIS A002895). The
identity with Domb's closed form `Σ_k C(n,k)² C(2k,k) C(2n−2k,n−k)` is Bala's
and is checked here by `decide` for `n < 10` only (`chain_eq_domb_small`).

Proof. By `W_site` the count is the same for every stacking, so it is computed on
diamond, where a step up across a bond layer always carries `g` and a step down
`ḡ`. Two steps from an even level give the recursion `Qd_two`; its solution is
the constant term of the `n`-th power of `(1 + g Y)(1 + ḡ Y⁻¹)` in the Laurent
ring `ℤ[ℤ²][Y, Y⁻¹]` (`Qd_even_eq`), which is `Σ_a C(n,a)² (g ḡ)^a`; and the
constant term of `(g ḡ)^a` in `ℤ[ℤ²]` is `H(a)` (`coeff_zero_N_pow`), because the
exponent `i d₁ + j d₂ + k d₃` determines `(i, j, k)` when `i + j + k = a`.
-/

namespace LoopEqualityProof

open Finset AddMonoidAlgebra

/-- `H(a)`: closed walks of length `2a` on the honeycomb net (OEIS A002893),
written with multinomials `C(a, i) C(a - i, j) = a! / (i! j! (a-i-j)!)`. -/
def honeycomb (a : ℕ) : ℕ :=
  ∑ i ∈ range (a + 1), ∑ j ∈ range (a - i + 1), (a.choose i * (a - i).choose j) ^ 2

/-- The chain formula of #102: `Σ_{a ≤ n} C(n, a)² H(a)`. -/
def chainWalks (n : ℕ) : ℕ := ∑ a ∈ range (n + 1), n.choose a ^ 2 * honeycomb a

/-- Closed walks of length `i` at a site: `0` for odd `i`, `chainWalks (i/2)` for even `i`. -/
def closedWalks (i : ℕ) : ℕ := if i % 2 = 0 then chainWalks (i / 2) else 0

/-- The Domb numbers, OEIS A002895: `Σ_k C(n,k)² C(2k,k) C(2n-2k,n-k)`. -/
def domb (n : ℕ) : ℕ :=
  ∑ k ∈ range (n + 1), n.choose k ^ 2 * (2 * k).choose k * (2 * (n - k)).choose (n - k)

/-- Bala's identity (OEIS A002895, comment), checked for `n < 10`. -/
theorem chain_eq_domb_small : ∀ n < 10, chainWalks n = domb n := by decide

/-! ## Diamond's level factors -/

theorem sd_diamond (k : ℤ) (d : ℤ × ℤ) : sd diamond k d = d := by
  unfold sd diamond
  rw [if_pos (by push_cast; ring)]

theorem gs_diamond (k : ℤ) : gs diamond k = g0 := by
  unfold gs g0; simp only [sd_diamond]

theorem gsc_diamond (k : ℤ) : gsc diamond k = g0c := by
  unfold gsc g0c; simp only [sd_diamond]

theorem up_diamond (l : ℤ) : up diamond l = if Even l then 1 else g0 := by
  unfold up; rw [gs_diamond]

theorem dn_diamond (l : ℤ) : dn diamond l = if Even l then g0c else 1 := by
  unfold dn; rw [gsc_diamond]

/-- Level sums of diamond. -/
noncomputable abbrev Qd := Levels.Q (up diamond) (dn diamond)

theorem Qd_two (i : ℕ) (k l' : ℤ) :
    Qd (i + 2) (2 * k) l' =
      g0 * Qd i (2 * k + 2) l' + (1 + g0 * g0c) * Qd i (2 * k) l' + g0c * Qd i (2 * k - 2) l' := by
  have e0 : Even (2 * k) := ⟨k, by ring⟩
  have e1 : ¬ Even (2 * k + 1) := by rw [even_iff']; omega
  have e2 : ¬ Even (2 * k - 1) := by rw [even_iff']; omega
  simp only [Qd, Levels.Q, up_diamond, dn_diamond, if_pos e0, if_neg e1, if_neg e2]
  rw [show 2 * k + 1 + 1 = 2 * k + 2 by ring, show 2 * k + 1 - 1 = 2 * k by ring,
    show 2 * k - 1 + 1 = 2 * k by ring, show 2 * k - 1 - 1 = 2 * k - 2 by ring]
  ring

/-! ## The Laurent ring `ℤ[ℤ²][Y, Y⁻¹]` -/

/-- Laurent polynomials in `Y` over `ℤ[ℤ²]`. -/
abbrev Lr := AddMonoidAlgebra Rg ℤ

/-- Two steps from an even level, as a Laurent polynomial in the bilayer shift `Y`. -/
noncomputable def Pl : Lr := single 1 g0 + single 0 (1 + g0 * g0c) + single (-1) g0c

theorem coeff_one_Lr (a : ℤ) : (1 : Lr).coeff a = if a = 0 then 1 else 0 := by
  rw [one_def, coeff_single, Finsupp.single_apply]
  by_cases h : a = 0
  · simp [h]
  · simp [h, Ne.symm h]

theorem coeff_single_mul_Lr (a b : ℤ) (r : Rg) (x : Lr) :
    (single a r * x).coeff b = r * x.coeff (-a + b) := coeff_single_mul_apply ..

theorem Qd_even_eq (n : ℕ) : ∀ k : ℤ, Qd (2 * n) (2 * k) 0 = (Pl ^ n).coeff (-k) := by
  induction n with
  | zero =>
    intro k
    simp only [pow_zero, coeff_one_Lr, Qd, Levels.Q]
    congr 1
    apply propext; omega
  | succ n ih =>
    intro k
    rw [show 2 * (n + 1) = 2 * n + 2 by ring, Qd_two, pow_succ',
      show 2 * k + 2 = 2 * (k + 1) by ring, show 2 * k - 2 = 2 * (k - 1) by ring, ih, ih, ih]
    generalize Pl ^ n = X
    rw [Pl]
    simp only [add_mul, coeff_add, Finsupp.add_apply, coeff_single_mul_Lr]
    rw [show -(k + 1) = -1 + -k by ring, show -(k - 1) = -(-1) + -k by ring,
      show -k = -0 + -k by ring]
    ring_nf

theorem Pl_eq : Pl = (1 + single 1 g0) * (1 + single (-1) g0c) := by
  simp only [Pl, add_mul, mul_add, one_mul, mul_one, single_mul_single]
  rw [show (1 : ℤ) + -1 = 0 by norm_num, single_add, ← one_def]
  abel

theorem one_add_single_pow (m : ℤ) (r : Rg) (n : ℕ) :
    (1 + single m r : Lr) ^ n =
      ∑ a ∈ range (n + 1), single ((a : ℤ) * m) ((n.choose a : ℤ) • r ^ a) := by
  rw [add_comm, add_pow]
  refine sum_congr rfl (fun a _ => ?_)
  rw [one_pow, mul_one, single_pow, mul_comm, ← nsmul_eq_mul, smul_single, nsmul_eq_mul,
    natCast_zsmul]

theorem coeff_zero_Pl_pow (n : ℕ) :
    (Pl ^ n).coeff 0 = ∑ a ∈ range (n + 1), ((n.choose a ^ 2 : ℕ) : ℤ) • (g0 * g0c) ^ a := by
  rw [Pl_eq, mul_pow, one_add_single_pow, one_add_single_pow, sum_mul_sum, coeff_sum,
    Finsupp.finsetSum_apply]
  refine sum_congr rfl (fun a _ => ?_)
  rw [coeff_sum, Finsupp.finsetSum_apply]
  simp only [single_mul_single, coeff_single, Finsupp.single_apply]
  have : ∀ b ∈ range (n + 1), (if (a : ℤ) * 1 + (b : ℤ) * -1 = 0 then
      ((n.choose a : ℤ) • g0 ^ a) * ((n.choose b : ℤ) • g0c ^ b) else 0) =
      if a = b then ((n.choose a : ℤ) • g0 ^ a) * ((n.choose b : ℤ) • g0c ^ b) else 0 := by
    intro b _
    congr 1
    apply propext; omega
  rw [sum_congr rfl this, sum_ite_eq]
  rw [if_pos (by assumption), smul_mul_smul_comm, mul_pow]
  congr 1
  push_cast; ring

/-! ## The constant term of `(g ḡ)^a` -/

/-- The exponent `i d₁ + j d₂ + (a-i-j) d₃`. -/
def expo (a i j : ℕ) : ℤ × ℤ := (i • ((1 : ℤ), (1 : ℤ)) + j • ((-2 : ℤ), (1 : ℤ))) + (a - (i + j)) • ((1 : ℤ), (-2 : ℤ))

theorem expo_inj {a i j i' j' : ℕ} (h : i + j ≤ a) (h' : i' + j' ≤ a)
    (he : expo a i j = expo a i' j') : i = i' ∧ j = j' := by
  simp only [expo, Prod.smul_mk, Prod.mk_add_mk, Prod.mk.injEq, nsmul_eq_mul] at he
  push_cast [Nat.cast_sub h, Nat.cast_sub h'] at he
  obtain ⟨h1, h2⟩ := he
  constructor <;> omega

theorem single_mul_natCast (m : ℤ × ℤ) (r : ℤ) (n : ℕ) :
    (single m r : Rg) * (n : Rg) = single m (r * n) := by
  rw [mul_comm, ← nsmul_eq_mul, smul_single, nsmul_eq_mul, mul_comm]

theorem trinom (x y z : ℤ × ℤ) (a : ℕ) :
    (single x (1 : ℤ) + single y 1 + single z 1 : Rg) ^ a =
      ∑ i ∈ range (a + 1), ∑ j ∈ range (a - i + 1),
        single ((i • x + j • y) + (a - (i + j)) • z) ((a.choose i * (a - i).choose j : ℕ) : ℤ) := by
  rw [add_assoc, add_pow]
  refine sum_congr rfl (fun i _ => ?_)
  rw [add_pow, mul_sum, sum_mul]
  refine sum_congr rfl (fun j _ => ?_)
  simp only [single_pow, one_pow, single_mul_single, single_mul_natCast, mul_one, one_mul]
  congr 1
  · rw [Nat.sub_sub]; abel
  · push_cast; ring

theorem g0_eq : g0 = single ((1 : ℤ), (1 : ℤ)) 1 + single ((-2 : ℤ), (1 : ℤ)) 1 + single ((1 : ℤ), (-2 : ℤ)) 1 := by
  unfold g0; rw [triD_sum]

theorem g0c_eq : g0c = single (-((1 : ℤ), (1 : ℤ))) 1 + single (-((-2 : ℤ), (1 : ℤ))) 1 +
    single (-((1 : ℤ), (-2 : ℤ))) 1 := by
  unfold g0c; rw [triD_sum (fun d => single (-d) 1)]

theorem expo_neg (a i j : ℕ) :
    (i • (-((1 : ℤ), (1 : ℤ))) + j • (-((-2 : ℤ), (1 : ℤ)))) + (a - (i + j)) • (-((1 : ℤ), (-2 : ℤ))) =
      -expo a i j := by
  simp only [expo, smul_neg, neg_add]

theorem coeff_zero_N_pow (a : ℕ) : ((g0 * g0c) ^ a).coeff 0 = (honeycomb a : ℤ) := by
  rw [mul_pow, g0_eq, g0c_eq, trinom, trinom]
  simp only [expo_neg]
  unfold honeycomb
  rw [sum_sigma', sum_sigma', sum_sigma', sum_mul_sum, coeff_sum, Finsupp.finsetSum_apply]
  push_cast
  refine sum_congr rfl (fun p hp => ?_)
  rw [coeff_sum, Finsupp.finsetSum_apply]
  have key : ∀ p' ∈ (range (a + 1)).sigma (fun i => range (a - i + 1)),
      (single (expo a p.1 p.2) ((a.choose p.1 * (a - p.1).choose p.2 : ℕ) : ℤ) *
        single (-expo a p'.1 p'.2) ((a.choose p'.1 * (a - p'.1).choose p'.2 : ℕ) : ℤ)).coeff 0 =
      if p' = p then ((a.choose p.1 : ℤ) * ((a - p.1).choose p.2 : ℤ)) ^ 2 else 0 := by
    intro p' hp'
    rw [single_mul_single, coeff_single, Finsupp.single_apply]
    simp only [mem_sigma, mem_range] at hp hp'
    by_cases h : p' = p
    · subst h
      simp [sq]
    · rw [if_neg h, if_neg]
      intro he
      have := expo_inj (show p.1 + p.2 ≤ a by omega) (show p'.1 + p'.2 ≤ a by omega)
        (by rw [← sub_eq_zero, sub_eq_add_neg]; exact he)
      obtain ⟨i, j⟩ := p
      obtain ⟨i', j'⟩ := p'
      simp only at this
      obtain ⟨rfl, rfl⟩ := this
      exact h rfl
  have e : ∀ p' ∈ (range (a + 1)).sigma (fun i => range (a - i + 1)),
      (single (expo a p.1 p.2) ((a.choose p.1 : ℤ) * ((a - p.1).choose p.2 : ℤ)) *
        single (-expo a p'.1 p'.2) ((a.choose p'.1 : ℤ) * ((a - p'.1).choose p'.2 : ℤ))).coeff 0 =
      if p' = p then ((a.choose p.1 : ℤ) * ((a - p.1).choose p.2 : ℤ)) ^ 2 else 0 := by
    intro p' hp'
    have := key p' hp'
    push_cast at this
    exact this
  simp only [expo] at e ⊢
  rw [sum_congr rfl e, sum_ite_eq', if_pos hp]

/-! ## The theorem -/

theorem Qd_parity (i : ℕ) : ∀ l l' : ℤ, (i : ℤ) % 2 ≠ (l' - l) % 2 → Qd i l l' = 0 := by
  induction i with
  | zero =>
    intro l l' h
    simp only [Qd, Levels.Q]
    rw [if_neg]; omega
  | succ i ih =>
    intro l l' h
    simp only [Qd, Levels.Q] at ih ⊢
    rw [ih (l + 1) l' (by push_cast at h; omega), ih (l - 1) l' (by push_cast at h; omega)]
    ring

theorem Sv_eq (i : ℕ) : Sv i = (Qd i 0 0).coeff 0 := by
  rw [Sv, Qd, Q_eq', Levels.H_self, one_mul]

/-- **Closed walks at every site of every stacking** (#102, Lemma 2 (a) and
the Proposition): the number of closed walks of length `i` at any atom of the
network of any stacking is `closedWalks i`. -/
theorem W_closed (σ : ℤ → ZMod 3) (x : Atom) (i : ℕ) :
    Graph.W (nbr σ) i x x = closedWalks i := by
  have h := W_site σ x i
  rw [Sv_eq] at h
  zify
  rw [h, closedWalks]
  split_ifs with hi
  · obtain ⟨n, rfl⟩ : ∃ n, i = 2 * n := ⟨i / 2, by omega⟩
    have e := Qd_even_eq n 0
    simp only [mul_zero, neg_zero] at e
    rw [e, coeff_zero_Pl_pow, coeff_sum, Finsupp.finsetSum_apply,
      show 2 * n / 2 = n by omega, chainWalks]
    push_cast
    refine sum_congr rfl (fun a _ => ?_)
    rw [coeff_smul, Finsupp.smul_apply, coeff_zero_N_pow, smul_eq_mul]
  · rw [Qd_parity i 0 0 (by omega)]
    simp

end LoopEqualityProof
