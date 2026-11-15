module

public import Mathlib
public import LoopEquality.Network
public import LoopEquality.Levels

@[expose] public section

/-!
# Walk counts at a site and along a bond (#102, Lemmas 1 and 2 (a), (b))

The torus integral of #102 is replaced by the group ring `ℤ[ℤ²]`: a walk's
planar displacement is the exponent of a monomial, and the number of walks
from `x` to `y` is the coefficient of `X^(p_y - p_x)` (`W_eq`). With the gauge
lemma of `Levels.lean` this gives, for every stacking and every atom:

* `W_site`: `W i x x = Sv i`;
* `W_nbr`: `W i x y = Vv i` along a vertical bond and `Cv i` along a slanted
  bond, in either direction;

where `Sv`, `Vv`, `Cv` do not depend on the stacking. For a slanted bond the
stacking decides between `g` and its conjugate, and the bond between the three
vectors of `D`; the conjugation `X^a ↦ X^(-a)` and the rotation of order 3
(`rho`) fix the gauge-invariant part `E`, which removes both choices.
-/

namespace LoopEqualityProof

open Finset AddMonoidAlgebra

/-- The group ring `ℤ[ℤ²]` of planar displacements. -/
abbrev Rg := AddMonoidAlgebra ℤ (ℤ × ℤ)

/-- `g = Σ_{d ∈ D} X^d`. -/
noncomputable def g0 : Rg := ∑ d ∈ triD, single d 1
/-- `ḡ = Σ_{d ∈ D} X^(-d)`. -/
noncomputable def g0c : Rg := ∑ d ∈ triD, single (-d) 1
/-- The displacements of an upward step across bond layer `k`. -/
noncomputable def gs (σ : ℤ → ZMod 3) (k : ℤ) : Rg := ∑ d ∈ triD, single (sd σ k d) 1
/-- The displacements of a downward step across bond layer `k`. -/
noncomputable def gsc (σ : ℤ → ZMod 3) (k : ℤ) : Rg := ∑ d ∈ triD, single (-(sd σ k d)) 1

/-- The level `2k + u` of an atom. -/
def lev (v : Atom) : ℤ := 2 * v.1 + (v.2.2.val : ℤ)

/-- Factor of a step `ℓ → ℓ + 1`. -/
noncomputable def up (σ : ℤ → ZMod 3) (l : ℤ) : Rg := if Even l then 1 else gs σ (l / 2)
/-- Factor of a step `ℓ → ℓ - 1`. -/
noncomputable def dn (σ : ℤ → ZMod 3) (l : ℤ) : Rg := if Even l then gsc σ ((l - 1) / 2) else 1
/-- The pair products, the same for every stacking: `1` or `g ḡ`. -/
noncomputable def Nf (l : ℤ) : Rg := if Even l then 1 else g0 * g0c

theorem gs_mul_gsc (σ : ℤ → ZMod 3) (k : ℤ) : gs σ k * gsc σ k = g0 * g0c := by
  unfold gs gsc sd
  split_ifs
  · rfl
  · simp only [neg_neg]; rw [mul_comm]; rfl

theorem even_iff' (l : ℤ) : Even l ↔ l % 2 = 0 := Int.even_iff

theorem up_dn (σ : ℤ → ZMod 3) (l : ℤ) : up σ l * dn σ (l + 1) = Nf l := by
  unfold up dn Nf
  by_cases h : Even l
  · have h' : ¬ Even (l + 1) := by rw [even_iff'] at h ⊢; omega
    rw [if_pos h, if_neg h', if_pos h, one_mul]
  · have h' : Even (l + 1) := by rw [even_iff'] at h ⊢; omega
    rw [if_neg h, if_pos h', if_neg h, show (l + 1 - 1) / 2 = l / 2 by ring_nf, gs_mul_gsc]

theorem coeff_single_mul' (a b : ℤ × ℤ) (x : Rg) :
    (single a (1 : ℤ) * x).coeff b = x.coeff (-a + b) := by
  rw [coeff_single_mul_apply, one_mul]

theorem coeff_gs_mul (σ : ℤ → ZMod 3) (k : ℤ) (x : Rg) (a : ℤ × ℤ) :
    (gs σ k * x).coeff a = ∑ d ∈ triD, x.coeff (-(sd σ k d) + a) := by
  unfold gs
  rw [sum_mul, coeff_sum, Finsupp.finsetSum_apply]
  exact sum_congr rfl (fun d _ => coeff_single_mul' _ _ _)

theorem coeff_gsc_mul (σ : ℤ → ZMod 3) (k : ℤ) (x : Rg) (a : ℤ × ℤ) :
    (gsc σ k * x).coeff a = ∑ d ∈ triD, x.coeff (sd σ k d + a) := by
  unfold gsc
  rw [sum_mul, coeff_sum, Finsupp.finsetSum_apply]
  refine sum_congr rfl (fun d _ => ?_)
  rw [coeff_single_mul', neg_neg]

theorem lev_mk (k : ℤ) (p : ℤ × ℤ) (u : Fin 2) : lev (k, p, u) = 2 * k + (u.val : ℤ) := rfl

theorem coeff_one' (a : ℤ × ℤ) : (1 : Rg).coeff a = if a = 0 then 1 else 0 := by
  rw [one_def, coeff_single, Finsupp.single_apply]
  by_cases h : a = 0
  · simp [h]
  · simp [h, Ne.symm h]

/-! ## Walk counts as coefficients (#102, Lemma 1) -/

theorem W_eq (σ : ℤ → ZMod 3) (i : ℕ) : ∀ x y : Atom,
    (Graph.W (nbr σ) i x y : ℤ) = (Levels.Q (up σ) (dn σ) i (lev x) (lev y)).coeff (y.2.1 - x.2.1) := by
  induction i with
  | zero =>
    rintro ⟨k, p, u⟩ ⟨k', q, u'⟩
    show ((if ((k, p, u) : Atom) = (k', q, u') then 1 else 0 : ℕ) : ℤ) =
      (if lev (k, p, u) = lev (k', q, u') then (1 : Rg) else 0).coeff (q - p)
    have hu := u.isLt
    have hu' := u'.isLt
    by_cases h : lev (k, p, u) = lev (k', q, u')
    · have h' := h
      rw [lev_mk, lev_mk] at h'
      have hk : k = k' := by omega
      have huu : u = u' := Fin.ext (by omega)
      subst hk huu
      rw [if_pos h, coeff_one']
      by_cases hp : p = q
      · subst hp; simp
      · have : q - p ≠ 0 := sub_ne_zero.2 (Ne.symm hp)
        rw [if_neg this, if_neg (by simp [hp])]
        rfl
    · rw [if_neg h, if_neg]
      · rfl
      · intro he
        exact h (by rw [he])
  | succ i ih =>
    rintro ⟨k, p, u⟩ y
    rcases fin2_cases u with rfl | rfl
    · rw [show Graph.W (nbr σ) (i + 1) (k, p, 0) y = ∑ z ∈ nbr σ (k, p, 0), Graph.W (nbr σ) i z y
        from rfl, nbr_lower, sum_insert (by simp), sum_image]
      · push_cast
        simp only [ih, Levels.Q, lev_mk, Fin.val_zero, Fin.val_one, Nat.cast_zero, Nat.cast_one,
          add_zero]
        have e1 : Even (2 * k) := ⟨k, by ring⟩
        rw [up, dn, if_pos e1, if_pos e1, one_mul, coeff_add, Finsupp.add_apply,
          coeff_gsc_mul, show (2 * k - 1) / 2 = k - 1 by omega]
        congr 1
        refine sum_congr rfl (fun d _ => ?_)
        rw [show 2 * (k - 1) + 1 = 2 * k - 1 by ring]
        congr 1
        abel
      · intro d _ d' _ h
        simp only [Prod.mk.injEq, sub_right_inj, true_and, and_true] at h
        exact sd_injective σ _ h
    · rw [show Graph.W (nbr σ) (i + 1) (k, p, 1) y = ∑ z ∈ nbr σ (k, p, 1), Graph.W (nbr σ) i z y
        from rfl, nbr_upper, sum_insert (by simp), sum_image]
      · push_cast
        simp only [ih, Levels.Q, lev_mk, Fin.val_zero, Fin.val_one, Nat.cast_zero, Nat.cast_one,
          add_zero]
        have e1 : ¬ Even (2 * k + 1) := by rw [even_iff']; omega
        rw [up, dn, if_neg e1, if_neg e1, one_mul, coeff_add, Finsupp.add_apply,
          coeff_gs_mul, show (2 * k + 1) / 2 = k by omega, add_comm]
        congr 1
        · refine sum_congr rfl (fun d _ => ?_)
          rw [show 2 * (k + 1) = 2 * k + 1 + 1 by ring]
          congr 1
          abel
        · rw [show 2 * k + 1 - 1 = 2 * k by ring]
      · intro d _ d' _ h
        simp only [Prod.mk.injEq, add_right_inj, true_and, and_true] at h
        exact sd_injective σ _ h

/-! ## The gauge-invariant part and its symmetries -/

theorem Q_eq' (σ : ℤ → ZMod 3) (i : ℕ) (l l' : ℤ) :
    Levels.Q (up σ) (dn σ) i l l' = Levels.H (up σ) (dn σ) l l' * Levels.E Nf i l l' :=
  Levels.Q_eq (up σ) (dn σ) Nf (up_dn σ) i l l'

theorem Nf_shift (c : ℤ) (l : ℤ) : Nf (l + 2 * c) = Nf l := by
  unfold Nf
  have : Even (l + 2 * c) ↔ Even l := by rw [even_iff', even_iff']; omega
  by_cases h : Even l
  · rw [if_pos (this.2 h), if_pos h]
  · rw [if_neg (fun h' => h (this.1 h')), if_neg h]

theorem Nf_neg (l : ℤ) : Nf (-l) = Nf l := by
  unfold Nf; simp only [even_neg]

theorem E_two_mul (i : ℕ) (l l' k : ℤ) : Levels.E Nf i (l + 2 * k) (l' + 2 * k) = Levels.E Nf i l l' :=
  Levels.E_shift Nf (2 * k) (Nf_shift k) i l l'

/-- The rotation of order 3 of the triangular lattice, `(i, j) ↦ (-i-j, i)`;
it permutes `D` cyclically. -/
def rhoE : (ℤ × ℤ) ≃+ (ℤ × ℤ) where
  toFun a := (-a.1 - a.2, a.1)
  invFun a := (a.2, -a.1 - a.2)
  left_inv a := by ext <;> simp
  right_inv a := by ext <;> simp <;> ring
  map_add' a b := by ext <;> simp <;> ring

theorem rhoE_apply (a : ℤ × ℤ) : rhoE a = (-a.1 - a.2, a.1) := rfl

theorem triD_sum (f : ℤ × ℤ → Rg) : ∑ d ∈ triD, f d = f (1, 1) + f (-2, 1) + f (1, -2) := by
  rw [triD, sum_insert (by decide), sum_insert (by decide), sum_singleton, add_assoc]

theorem triD_sum_int (f : ℤ × ℤ → ℤ) : ∑ d ∈ triD, f d = f (1, 1) + f (-2, 1) + f (1, -2) := by
  rw [triD, sum_insert (by decide), sum_insert (by decide), sum_singleton, add_assoc]

/-- A ring automorphism of `ℤ[ℤ²]` from an automorphism of `ℤ²`. -/
noncomputable def mapR (e : (ℤ × ℤ) ≃+ (ℤ × ℤ)) : Rg ≃+* Rg :=
  AddMonoidAlgebra.mapDomainRingEquiv ℤ e

theorem mapR_single (e : (ℤ × ℤ) ≃+ (ℤ × ℤ)) (a : ℤ × ℤ) (r : ℤ) :
    mapR e (single a r) = single (e a) r := by
  simp [mapR]

theorem coeff_mapR (e : (ℤ × ℤ) ≃+ (ℤ × ℤ)) (x : Rg) (a : ℤ × ℤ) :
    (mapR e x).coeff (e a) = x.coeff a := by
  simp [mapR, Finsupp.equivMapDomain_apply]

theorem mapR_Nf (e : (ℤ × ℤ) ≃+ (ℤ × ℤ)) (h : mapR e (g0 * g0c) = g0 * g0c) (l : ℤ) :
    mapR e (Nf l) = Nf l := by
  unfold Nf
  split_ifs
  · exact map_one _
  · exact h

theorem E_inv (e : (ℤ × ℤ) ≃+ (ℤ × ℤ)) (h : mapR e (g0 * g0c) = g0 * g0c) (i : ℕ) (l l' : ℤ)
    (a : ℤ × ℤ) : (Levels.E Nf i l l').coeff (e a) = (Levels.E Nf i l l').coeff a := by
  have h1 := Levels.E_map (mapR e : Rg →+* Rg) Nf i l l'
  have h2 : (fun l => (mapR e : Rg →+* Rg) (Nf l)) = Nf := funext fun l => mapR_Nf e h l
  rw [h2] at h1
  rw [← coeff_mapR e (Levels.E Nf i l l') a]
  congr 2
  exact h1.symm

theorem rho_fix : mapR rhoE (g0 * g0c) = g0 * g0c := by
  rw [map_mul]
  congr 1
  · unfold g0
    rw [map_sum, triD_sum, triD_sum]
    simp only [mapR_single, rhoE_apply]
    norm_num
    abel
  · unfold g0c
    rw [map_sum, triD_sum, triD_sum]
    simp only [mapR_single, rhoE_apply]
    norm_num
    abel

theorem neg_fix : mapR (AddEquiv.neg (ℤ × ℤ)) (g0 * g0c) = g0 * g0c := by
  rw [map_mul, mul_comm]
  congr 1
  · unfold g0 g0c
    rw [map_sum]
    simp only [mapR_single]
    rfl
  · unfold g0 g0c
    rw [map_sum]
    simp only [mapR_single, AddEquiv.neg_apply, neg_neg]

/-! ## The three values -/

/-- Closed walks at a site. -/
noncomputable def Sv (i : ℕ) : ℤ := (Levels.E Nf i 0 0).coeff 0
/-- Walks along a vertical bond. -/
noncomputable def Vv (i : ℕ) : ℤ := (Levels.E Nf i 0 1).coeff 0
/-- Walks along a slanted bond. -/
noncomputable def Cv (i : ℕ) : ℤ := (g0 * Levels.E Nf i 1 2).coeff (1, 1)

theorem W_site (σ : ℤ → ZMod 3) (x : Atom) (i : ℕ) : (Graph.W (nbr σ) i x x : ℤ) = Sv i := by
  rw [W_eq, sub_self, Q_eq', Levels.H_self, one_mul]
  obtain ⟨k, p, u⟩ := x
  rw [lev_mk]
  rcases fin2_cases u with rfl | rfl
  · have := E_two_mul i 0 0 k
    simp only [zero_add] at this
    simp only [Fin.val_zero, Nat.cast_zero, add_zero, this]
    rfl
  · have := E_two_mul i 1 1 k
    simp only [Fin.val_one, Nat.cast_one, add_comm (2 * k) 1, this]
    have h2 := Levels.E_refl Nf Nf_neg i 0 0
    simp only [sub_zero] at h2
    rw [h2]
    rfl

theorem W_vert (σ : ℤ → ZMod 3) (k : ℤ) (p : ℤ × ℤ) (i : ℕ) :
    (Graph.W (nbr σ) i (k, p, 0) (k, p, 1) : ℤ) = Vv i := by
  rw [W_eq, sub_self, Q_eq', lev_mk, lev_mk]
  simp only [Fin.val_zero, Fin.val_one, Nat.cast_zero, Nat.cast_one, add_zero]
  rw [Levels.H_lt _ _ (show 2 * k < 2 * k + 1 by omega), Levels.H_self, up,
    if_pos ⟨k, by ring⟩, one_mul, one_mul]
  have := E_two_mul i 0 1 k
  simp only [zero_add] at this
  rw [add_comm (2 * k) 1, this]
  rfl

theorem T_eq (e : Rg) (hn : ∀ a, e.coeff (-a) = e.coeff a) (hr : ∀ a, e.coeff (rhoE a) = e.coeff a)
    {d : ℤ × ℤ} (hd : d ∈ triD) :
    ∑ d' ∈ triD, e.coeff (-d' + d) = ∑ d' ∈ triD, e.coeff (-d' + (1, 1)) := by
  have r1 : e.coeff (-3, 3) = e.coeff (3, 0) := by
    have := hr (3, 0); rw [rhoE_apply] at this; norm_num at this; exact this
  have r2 : e.coeff (-3, 0) = e.coeff (0, 3) := by
    have := hr (0, 3); rw [rhoE_apply] at this; norm_num at this; exact this
  have r3 : e.coeff (0, -3) = e.coeff (-3, 3) := by
    have := hr (-3, 3); rw [rhoE_apply] at this; norm_num at this; exact this
  have r4 : e.coeff (3, -3) = e.coeff (-3, 0) := by
    have := hr (-3, 0); rw [rhoE_apply] at this; norm_num at this; exact this
  simp only [triD, mem_insert, mem_singleton] at hd
  rw [triD_sum_int, triD_sum_int]
  rcases hd with rfl | rfl | rfl <;> norm_num <;> linarith

theorem coeff_gs_cross (σ : ℤ → ZMod 3) (k : ℤ) (e : Rg) (hn : ∀ a, e.coeff (-a) = e.coeff a)
    (hr : ∀ a, e.coeff (rhoE a) = e.coeff a) {d : ℤ × ℤ} (hd : d ∈ triD) :
    (gs σ k * e).coeff (sd σ k d) = (g0 * e).coeff (1, 1) := by
  rw [coeff_gs_mul]
  have hg : (g0 * e).coeff (1, 1) = ∑ d' ∈ triD, e.coeff (-d' + (1, 1)) := by
    unfold g0
    rw [sum_mul, coeff_sum, Finsupp.finsetSum_apply]
    exact sum_congr rfl (fun d _ => coeff_single_mul' _ _ _)
  rw [hg, ← T_eq e hn hr hd]
  unfold sd
  split_ifs
  · rfl
  · refine sum_congr rfl (fun d' _ => ?_)
    rw [← hn]
    congr 1
    abel

theorem W_cross (σ : ℤ → ZMod 3) (k : ℤ) (p : ℤ × ℤ) {d : ℤ × ℤ} (hd : d ∈ triD) (i : ℕ) :
    (Graph.W (nbr σ) i (k, p, 1) (k + 1, p + sd σ k d, 0) : ℤ) = Cv i := by
  rw [W_eq, add_sub_cancel_left, Q_eq', lev_mk, lev_mk]
  simp only [Fin.val_zero, Fin.val_one, Nat.cast_zero, Nat.cast_one, add_zero]
  rw [Levels.H_lt _ _ (show 2 * k + 1 < 2 * (k + 1) by omega),
    show 2 * k + 1 + 1 = 2 * (k + 1) by ring, Levels.H_self, mul_one, up,
    if_neg (by rw [even_iff']; omega), show (2 * k + 1) / 2 = k by omega]
  have := E_two_mul i 1 2 k
  rw [add_comm (2 * k) 1, show 2 * (k + 1) = 2 + 2 * k by ring, this]
  exact coeff_gs_cross σ k _
    (fun a => by
      have := E_inv (AddEquiv.neg (ℤ × ℤ)) neg_fix i 1 2 a
      simpa using this)
    (fun a => E_inv rhoE rho_fix i 1 2 a) hd

/-- Walks along a bond: the value depends only on the kind of bond. -/
theorem W_nbr (σ : ℤ → ZMod 3) {x y : Atom} (hy : y ∈ nbr σ x) (i : ℕ) :
    (Graph.W (nbr σ) i x y : ℤ) = if x.1 = y.1 then Vv i else Cv i := by
  have hs := (regular σ).symm
  obtain ⟨k, p, u⟩ := x
  rcases fin2_cases u with rfl | rfl
  · rw [nbr_lower] at hy
    simp only [mem_insert, mem_image] at hy
    rcases hy with rfl | ⟨d, hd, rfl⟩
    · rw [W_vert, if_pos rfl]
    · rw [Graph.W_symm hs, if_neg (by dsimp only; omega)]
      have : ((k, p, 0) : Atom) = (k - 1 + 1, p - sd σ (k - 1) d + sd σ (k - 1) d, 0) := by simp
      rw [this, W_cross σ _ _ hd]
  · rw [nbr_upper] at hy
    simp only [mem_insert, mem_image] at hy
    rcases hy with rfl | ⟨d, hd, rfl⟩
    · rw [Graph.W_symm hs, W_vert, if_pos rfl]
    · rw [W_cross σ _ _ hd, if_neg (by simp)]

end LoopEqualityProof
