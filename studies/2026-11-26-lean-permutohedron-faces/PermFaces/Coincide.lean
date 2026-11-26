/-
When do two permutohedron ridges share a Vacuus plate? (#120 Theorem 3 (ii); step 5 of the restructured entry, 26 Nov 2026.)
DICTO, with Claude (Anthropic). Built on PermFaces.RidgePlate and PermFaces.PlateEq.
-/
import PermFaces.RidgePlate
import PermFaces.PlateEq

/-!
# Plate coincidences (step 5)

A ridge is an ordered partition `key : Fin n → Fin 3` into nonempty blocks `B₁, B₂, B₃` of sizes `a, b, c`. Its plate is
`plateOf (wt key)` with weights `c(a+b)` on `B₁`, `0` on `B₂`, `a(b+c)` on `B₃` (`permPlate_eq_plateOf`).
* `mem_permPlate_iff`: the plate in weight form; `affine_of_plate_eq`: equal plates give affinely related weights;
  `wt_rev`: a ridge read backwards has the same weights; `l_ne_zero`: the affine factor is not zero.
* In progress (Coincide_WIP.lean, not built): `plate_eq_of_ne` (**#120 Theorem 3 (ii), a ≠ c**: the second ridge is the
  first or the first read backwards) and the a = c case (middle block equal or complementary).
-/

open Finset

namespace PermFaces

variable {n : ℕ}

/-- Block sizes. -/
def sz (key : Fin n → Fin 3) (b : Fin 3) : ℝ := (block key b).card

/-- The plate weights: `c(a+b)` on `B₁`, `0` on `B₂`, `a(b+c)` on `B₃`. -/
noncomputable def wt (key : Fin n → Fin 3) (i : Fin n) : ℝ :=
  if key i = 0 then sz key 2 * (sz key 0 + sz key 1) else if key i = 2 then sz key 0 * (sz key 1 + sz key 2) else 0

theorem sum_block_const (key : Fin n → Fin 3) (b : Fin 3) (k : ℝ) (y : Fin n → ℝ) (f : Fin n → ℝ)
    (hf : ∀ i, key i = b → f i = k) : ∑ i ∈ block key b, f i * y i = k * ∑ i ∈ block key b, y i := by
  rw [mul_sum]; exact sum_congr rfl fun i hi => by rw [hf i (by simpa [block] using hi)]

/-- The plate of a ridge in weight form. -/
theorem mem_permPlate_iff {key : Fin n → Fin 3} {y : Fin n → ℝ} :
    y ∈ VacuusResonus.permPlate (block key 0) (block key 1) (block key 2) ↔ y ∈ VacuusResonus.plateOf (wt key) := by
  have hsplit := sum_three (key := key) (fun i => wt key i * y i)
  rw [sum_block_const key 0 (sz key 2 * (sz key 0 + sz key 1)) y (wt key) (fun i h => by simp [wt, h]),
    sum_block_const key 1 0 y (wt key) (fun i h => by simp [wt, h]),
    sum_block_const key 2 (sz key 0 * (sz key 1 + sz key 2)) y (wt key) (fun i h => by simp [wt, h])] at hsplit
  simp only [VacuusResonus.permPlate, VacuusResonus.plateOf, Submodule.mem_mk, AddSubmonoid.mem_mk,
    AddSubsemigroup.mem_mk, Set.mem_setOf_eq, Submodule.mem_inf, LinearMap.mem_ker, VacuusResonus.dotL, LinearMap.coe_mk,
    AddHom.coe_mk, one_mul]
  rw [hsplit]; simp only [sz, zero_mul, add_zero]

theorem sz_pos {key : Fin n → Fin 3} (hk : Function.Surjective key) (b : Fin 3) : 0 < sz key b := by
  obtain ⟨i, hi⟩ := hk b
  simp only [sz, Nat.cast_pos, card_pos]; exact ⟨i, by simp [block, hi]⟩

theorem wt_of (key : Fin n → Fin 3) (i : Fin n) :
    (key i = 0 → wt key i = sz key 2 * (sz key 0 + sz key 1)) ∧ (key i = 1 → wt key i = 0) ∧
      (key i = 2 → wt key i = sz key 0 * (sz key 1 + sz key 2)) := by
  refine ⟨fun h => by simp [wt, h], fun h => by simp [wt, h], fun h => by simp [wt, h]⟩

/-- Equal plates give affinely related weights. -/
theorem affine_of_plate_eq {key key' : Fin n → Fin 3}
    (h : VacuusResonus.permPlate (block key 0) (block key 1) (block key 2) =
      VacuusResonus.permPlate (block key' 0) (block key' 1) (block key' 2)) :
    ∃ l m : ℝ, ∀ i, wt key' i = l * wt key i + m := by
  apply VacuusResonus.affine_of_plateOf_le
  intro y hy
  have := (mem_permPlate_iff (key := key)).2 hy
  rw [h] at this; exact (mem_permPlate_iff (key := key')).1 this

/-- Reading a ridge backwards gives the same weights. -/
theorem wt_rev (key : Fin n → Fin 3) : wt (Fin.rev ∘ key) = wt key := by
  have hb : ∀ b : Fin 3, block (Fin.rev ∘ key) b = block key (Fin.rev b) := by
    intro b; ext i; simp only [block, mem_filter, mem_univ, true_and, Function.comp_apply]
    constructor
    · intro h; rw [← h, Fin.rev_rev]
    · intro h; rw [h, Fin.rev_rev]
  have hs : ∀ b, sz (Fin.rev ∘ key) b = sz key (Fin.rev b) := fun b => by simp only [sz, hb]
  have r0 : Fin.rev (0 : Fin 3) = 2 := rfl; have r1 : Fin.rev (1 : Fin 3) = 1 := rfl; have r2 : Fin.rev (2 : Fin 3) = 0 := rfl
  funext i
  rcases hk : key i with ⟨k, hk'⟩
  interval_cases k
  · have h' : (Fin.rev ∘ key) i = 2 := by rw [Function.comp_apply, hk]; rfl
    rw [(wt_of _ i).2.2 h', (wt_of key i).1 hk, hs, hs, hs, r0, r1, r2]; ring
  · have h' : (Fin.rev ∘ key) i = 1 := by rw [Function.comp_apply, hk]; rfl
    rw [(wt_of _ i).2.1 h', (wt_of key i).2.1 hk]
  · have h' : (Fin.rev ∘ key) i = 0 := by rw [Function.comp_apply, hk]; rfl
    rw [(wt_of _ i).1 h', (wt_of key i).2.2 hk, hs, hs, hs, r0, r1, r2]; ring

/-- If the weights are affinely related, `l ≠ 0`. -/
theorem l_ne_zero {key key' : Fin n → Fin 3} (hk' : Function.Surjective key') {l m : ℝ}
    (hlm : ∀ i, wt key' i = l * wt key i + m) : l ≠ 0 := by
  rintro rfl
  obtain ⟨j0, g0⟩ := hk' 0; obtain ⟨j1, g1⟩ := hk' 1
  have e0 := hlm j0; have e1 := hlm j1
  rw [(wt_of key' j0).1 g0] at e0; rw [(wt_of key' j1).2.1 g1] at e1
  have := sz_pos hk' 0; have := sz_pos hk' 1; have := sz_pos hk' 2
  simp at e0 e1; nlinarith


end PermFaces
