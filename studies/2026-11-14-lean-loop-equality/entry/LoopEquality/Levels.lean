module

public import Mathlib

@[expose] public section

/-!
# The level chain and its gauge (any commutative ring)

A walk in the tetrahedral network of a stacking moves between neighbouring
levels `ℓ ↦ ℓ ± 1`. A step `ℓ → ℓ + 1` carries a factor `up ℓ` and a step
`ℓ → ℓ - 1` a factor `dn ℓ` (in the application: the generating function of
the planar displacements of that step). `Q i ℓ ℓ'` sums the products over all
level paths of length `i` from `ℓ` to `ℓ'`.

`Q_eq`: if `up ℓ * dn (ℓ + 1) = N ℓ` for every `ℓ`, then
`Q i ℓ ℓ' = H ℓ ℓ' * E N i ℓ ℓ'`, where `H` is the product of the factors along
the straight path and `E` depends only on `N`. This is the ring form of the
cancellation in #102: a walk crosses every layer outside the straight path as
often upwards as downwards, and each such pair contributes `N`.

`E_map`, `E_shift`, `E_refl`: `E` commutes with ring maps, and is invariant
under shifts and the reflection `ℓ ↦ 1 - ℓ` that preserve `N`.
-/

namespace LoopEqualityProof.Levels

open Finset

variable {R : Type*} [CommRing R]

/-- Sum over level paths of the products of the step factors. -/
def Q (up dn : ℤ → R) : ℕ → ℤ → ℤ → R
  | 0, l, l' => if l = l' then 1 else 0
  | i + 1, l, l' => up l * Q up dn i (l + 1) l' + dn l * Q up dn i (l - 1) l'

/-- The gauge-invariant part: depends only on the pair products `N`. -/
def E (N : ℤ → R) : ℕ → ℤ → ℤ → R
  | 0, l, l' => if l = l' then 1 else 0
  | i + 1, l, l' => (if l < l' then 1 else N l) * E N i (l + 1) l' +
      (if l' < l then 1 else N (l - 1)) * E N i (l - 1) l'

/-- The product of the step factors along the straight path from `l` to `l'`. -/
def H (up dn : ℤ → R) (l l' : ℤ) : R :=
  if l ≤ l' then ∏ j ∈ range (l' - l).toNat, up (l + j)
  else ∏ j ∈ range (l - l').toNat, dn (l - j)

variable (up dn : ℤ → R)

theorem H_self (l : ℤ) : H up dn l l = 1 := by simp [H]

theorem H_lt {l l' : ℤ} (h : l < l') : H up dn l l' = up l * H up dn (l + 1) l' := by
  have h1 : l ≤ l' := h.le
  have h2 : l + 1 ≤ l' := h
  simp only [H, if_pos h1, if_pos h2]
  have e : (l' - l).toNat = (l' - (l + 1)).toNat + 1 := by omega
  rw [e, prod_range_succ']
  simp only [Nat.cast_zero, add_zero, Nat.cast_add, Nat.cast_one]
  rw [mul_comm]
  congr 1
  refine prod_congr rfl (fun j _ => ?_)
  congr 1
  ring

theorem H_gt {l l' : ℤ} (h : l' < l) : H up dn l l' = dn l * H up dn (l - 1) l' := by
  have h1 : ¬ l ≤ l' := by omega
  by_cases h2 : l - 1 ≤ l'
  · have e : l - 1 = l' := by omega
    subst e
    simp only [H, if_neg h1, le_refl, if_true, sub_self, Int.toNat_zero, prod_range_zero, mul_one]
    have : (l - (l - 1)).toNat = 1 := by omega
    rw [this, prod_range_one]
    simp
  · simp only [H, if_neg h1, if_neg h2]
    have e : (l - l').toNat = (l - 1 - l').toNat + 1 := by omega
    rw [e, prod_range_succ']
    simp only [Nat.cast_zero, sub_zero, Nat.cast_add, Nat.cast_one]
    rw [mul_comm]
    congr 1
    refine prod_congr rfl (fun j _ => ?_)
    congr 1
    ring

theorem Q_eq (N : ℤ → R) (hN : ∀ l, up l * dn (l + 1) = N l) :
    ∀ i l l', Q up dn i l l' = H up dn l l' * E N i l l' := by
  intro i
  induction i with
  | zero =>
    intro l l'
    simp only [Q, E]
    by_cases h : l = l'
    · subst h; simp [H_self]
    · simp [h]
  | succ i ih =>
    intro l l'
    simp only [Q, E, ih]
    have hN' : dn l * up (l - 1) = N (l - 1) := by
      rw [← hN (l - 1), sub_add_cancel, mul_comm]
    rcases lt_trichotomy l l' with h | h | h
    · rw [if_pos h, if_neg (by omega), H_lt up dn (show l - 1 < l' by omega), sub_add_cancel,
        H_lt up dn h, ← hN']
      ring
    · subst h
      rw [if_neg (lt_irrefl _), if_neg (lt_irrefl _), H_self,
        H_gt up dn (show l < l + 1 by omega), add_sub_cancel_right, H_self,
        H_lt up dn (show l - 1 < l by omega), sub_add_cancel, H_self, ← hN l, ← hN']
      ring
    · rw [if_neg (by omega), if_pos h, H_gt up dn (show l' < l + 1 by omega), add_sub_cancel_right,
        H_gt up dn h, ← hN l]
      ring

theorem E_map {S : Type*} [CommRing S] (φ : R →+* S) (N : ℤ → R) :
    ∀ i l l', φ (E N i l l') = E (fun l => φ (N l)) i l l' := by
  intro i
  induction i with
  | zero => intro l l'; simp only [E]; split_ifs <;> simp
  | succ i ih =>
    intro l l'
    simp only [E, map_add, map_mul, ih, apply_ite φ, map_one]

theorem E_shift (N : ℤ → R) (c : ℤ) (hc : ∀ l, N (l + c) = N l) :
    ∀ i l l', E N i (l + c) (l' + c) = E N i l l' := by
  intro i
  induction i with
  | zero => intro l l'; simp only [E, add_left_inj]
  | succ i ih =>
    intro l l'
    simp only [E]
    rw [show l + c + 1 = (l + 1) + c by ring, show l + c - 1 = (l - 1) + c by ring, ih, ih, hc, hc]
    simp only [add_lt_add_iff_right]

theorem E_refl (N : ℤ → R) (hr : ∀ l, N (-l) = N l) :
    ∀ i l l', E N i (1 - l) (1 - l') = E N i l l' := by
  intro i
  induction i with
  | zero => intro l l'; simp only [E]; congr 1; apply propext; omega
  | succ i ih =>
    intro l l'
    simp only [E]
    have n1 : N (1 - l) = N (l - 1) := by rw [show 1 - l = -(l - 1) by ring, hr]
    have n2 : N (1 - l - 1) = N l := by rw [show 1 - l - 1 = -l by ring, hr]
    rw [n1, n2, show 1 - l + 1 = 1 - (l - 1) by ring, show 1 - l - 1 = 1 - (l + 1) by ring, ih, ih]
    have e1 : (1 - l < 1 - l') ↔ l' < l := by omega
    have e2 : (1 - l' < 1 - l) ↔ l < l' := by omega
    simp only [e1, e2]
    ring

end LoopEqualityProof.Levels
