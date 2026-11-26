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
* `plate_eq_of_ne` (**#120 Theorem 3 (ii), a ≠ c**): two ridges share a plate only if the second is the first or the first
  read backwards. Of the six relabellings of the blocks, the other four force `2ab = 0` or `2bc = 0`.
* `middle_of_plate_eq` (**#120 Theorem 3 (ii), a = c**): the second ridge has the same middle block or its complement.
* `plate_eq_iff`: the complete characterisation (both directions).
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

/-- The weight of a coordinate depends only on its block. -/
noncomputable def W (key : Fin n → Fin 3) (p : Fin 3) : ℝ :=
  if p = 0 then sz key 2 * (sz key 0 + sz key 1) else if p = 2 then sz key 0 * (sz key 1 + sz key 2) else 0

theorem wt_eq_W (key : Fin n → Fin 3) (i : Fin n) : wt key i = W key (key i) := rfl

theorem W_zero (key : Fin n → Fin 3) : W key 0 = sz key 2 * (sz key 0 + sz key 1) := by
  unfold W; rw [if_pos rfl]
theorem W_one (key : Fin n → Fin 3) : W key 1 = 0 := by
  unfold W; rw [if_neg (by decide : (1 : Fin 3) ≠ 0), if_neg (by decide : (1 : Fin 3) ≠ 2)]
theorem W_two (key : Fin n → Fin 3) : W key 2 = sz key 0 * (sz key 1 + sz key 2) := by
  unfold W; rw [if_neg (by decide : (2 : Fin 3) ≠ 0), if_pos rfl]

theorem fin3 (x : Fin 3) : x = 0 ∨ x = 1 ∨ x = 2 := by revert x; decide

theorem fin3_perm (x y z : Fin 3) (hxy : x ≠ y) (hxz : x ≠ z) (hyz : y ≠ z) :
    (x = 0 ∧ y = 1 ∧ z = 2) ∨ (x = 2 ∧ y = 1 ∧ z = 0) ∨ (x = 0 ∧ y = 2 ∧ z = 1) ∨ (x = 1 ∧ y = 0 ∧ z = 2) ∨
      (x = 1 ∧ y = 2 ∧ z = 0) ∨ (x = 2 ∧ y = 0 ∧ z = 1) := by
  revert x y z; decide

/-- Relabelling: if `key' = π ∘ key` with `π` injective, block `π b` of `key'` is block `b` of `key`. -/
theorem sz_relabel {key key' : Fin n → Fin 3} {π : Fin 3 → Fin 3} (hπ : Function.Injective π)
    (hk : ∀ i, key' i = π (key i)) (b : Fin 3) : sz key' (π b) = sz key b := by
  simp only [sz]; congr 2; ext i; simp only [block, mem_filter, mem_univ, true_and, hk]; exact hπ.eq_iff

/-- **#120 Theorem 3 (ii), outer blocks of different sizes.** Two ridges share a plate only if the second is the first, or
the first read backwards. -/
theorem plate_eq_of_ne {key key' : Fin n → Fin 3} (hk : Function.Surjective key) (hk' : Function.Surjective key')
    (hac : sz key 0 ≠ sz key 2)
    (h : VacuusResonus.permPlate (block key 0) (block key 1) (block key 2) =
      VacuusResonus.permPlate (block key' 0) (block key' 1) (block key' 2)) :
    key' = key ∨ key' = Fin.rev ∘ key := by
  obtain ⟨l, m, hlm⟩ := affine_of_plate_eq h
  have hl := l_ne_zero hk' hlm
  have pa := sz_pos hk 0; have pb := sz_pos hk 1; have pc := sz_pos hk 2
  choose r hr using hk
  -- the weights of key at its three blocks are distinct
  have hxy : sz key 2 * (sz key 0 + sz key 1) ≠ sz key 0 * (sz key 1 + sz key 2) := by
    intro e; apply hac
    have h3 : sz key 1 * (sz key 2 - sz key 0) = 0 := by linear_combination e
    rcases mul_eq_zero.1 h3 with h4 | h4
    · linarith
    · linarith
  have q0 := mul_pos pc (add_pos pa pb); have q2 := mul_pos pa (add_pos pb pc)
  have Winj : Function.Injective (W key) := by
    intro p q e
    rcases fin3 p with rfl | rfl | rfl <;> rcases fin3 q with rfl | rfl | rfl <;>
      simp only [W_zero, W_one, W_two] at e <;>
      first | rfl | (exfalso; exact hxy e) | (exfalso; exact hxy e.symm) | (exfalso; linarith)
  obtain ⟨π, hπ⟩ : ∃ π : Fin 3 → Fin 3, ∀ b, π b = key' (r b) := ⟨_, fun _ => rfl⟩
  have E : ∀ b, W key' (π b) = l * W key b + m := by
    intro b; rw [hπ]; have := hlm (r b); rwa [wt_eq_W, wt_eq_W, hr] at this
  have πinj : Function.Injective π := by
    intro b b' e; apply Winj
    have h1 := E b; have h2 := E b'; rw [e] at h1
    exact mul_left_cancel₀ hl (by linarith)
  have πsurj : Function.Surjective π := Finite.injective_iff_surjective.1 πinj
  have W'inj : Function.Injective (W key') := by
    intro p q e
    obtain ⟨b, rfl⟩ := πsurj p; obtain ⟨b', rfl⟩ := πsurj q
    rw [E, E] at e; congr 1; exact Winj (mul_left_cancel₀ hl (by linarith))
  -- key' = π ∘ key
  have hkey : ∀ i, key' i = π (key i) := fun i =>
    W'inj (by rw [show W key' (key' i) = wt key' i from rfl, hlm i, wt_eq_W, E])
  have S := sz_relabel πinj hkey
  have S0 := S 0; have S1 := S 1; have S2 := S 2
  have E0 := E 0; have E1 := E 1; have E2 := E 2
  -- the six relabellings
  rcases fin3_perm (π 0) (π 1) (π 2) (πinj.ne (by decide)) (πinj.ne (by decide)) (πinj.ne (by decide)) with
    ⟨x0, x1, x2⟩ | ⟨x0, x1, x2⟩ | ⟨x0, x1, x2⟩ | ⟨x0, x1, x2⟩ | ⟨x0, x1, x2⟩ | ⟨x0, x1, x2⟩
  -- identity: the same ridge
  · left; funext i; rw [hkey i]
    rcases fin3 (key i) with hi | hi | hi <;> simp only [hi, x0, x1, x2]
  -- reversal: the same ridge read backwards
  · right; funext i; rw [hkey i]
    rcases fin3 (key i) with hi | hi | hi <;> simp only [Function.comp_apply, hi, x0, x1, x2] <;> decide
  all_goals
    exfalso
    rw [x0] at S0 E0; rw [x1] at S1 E1; rw [x2] at S2 E2
    simp only [W_zero, W_one, W_two] at E0 E1 E2
    simp only [S0, S1, S2] at E0 E1 E2
  -- (0 2 1): forces 2bc = 0
  · have hl1 : l = -1 := by
      have h3 : (l + 1) * (sz key 0 * (sz key 1 + sz key 2)) = 0 := by linear_combination E1 - E2
      rcases mul_eq_zero.1 h3 with h4 | h4 <;> linarith
    subst hl1
    have h5 : 2 * (sz key 1 * sz key 2) = 0 := by linear_combination E0 - E1
    linarith [mul_pos pb pc]
  -- (1 0 2): forces 2ab = 0
  · have hl1 : l = -1 := by
      have h3 : (l + 1) * (sz key 2 * (sz key 0 + sz key 1)) = 0 := by linear_combination E1 - E0
      rcases mul_eq_zero.1 h3 with h4 | h4 <;> linarith
    subst hl1
    have h5 : 2 * (sz key 0 * sz key 1) = 0 := by linear_combination E2 - E1
    linarith [mul_pos pa pb]
  -- (1 2 0): forces 2ab = 0
  · have hl1 : l = -1 := by
      have h3 : (l + 1) * (sz key 2 * (sz key 0 + sz key 1)) = 0 := by linear_combination E1 - E0
      rcases mul_eq_zero.1 h3 with h4 | h4 <;> linarith
    subst hl1
    have h5 : 2 * (sz key 0 * sz key 1) = 0 := by linear_combination E2 - E1
    linarith [mul_pos pa pb]
  -- (2 0 1): forces 2bc = 0
  · have hl1 : l = -1 := by
      have h3 : (l + 1) * (sz key 0 * (sz key 1 + sz key 2)) = 0 := by linear_combination E1 - E2
      rcases mul_eq_zero.1 h3 with h4 | h4 <;> linarith
    subst hl1
    have h5 : 2 * (sz key 1 * sz key 2) = 0 := by linear_combination E0 - E1
    linarith [mul_pos pb pc]

theorem sz_rev (key : Fin n → Fin 3) (b : Fin 3) : sz (Fin.rev ∘ key) b = sz key (Fin.rev b) := by
  simp only [sz]; congr 2; ext i; simp only [block, mem_filter, mem_univ, true_and, Function.comp_apply]
  constructor
  · intro h; rw [← h, Fin.rev_rev]
  · intro h; rw [h, Fin.rev_rev]

/-- Outer blocks of equal size: the weight is `0` on the middle block and one constant elsewhere. -/
theorem wt_two_level {key : Fin n → Fin 3} (hac : sz key 0 = sz key 2) (i : Fin n) :
    wt key i = if key i = 1 then 0 else sz key 2 * (sz key 0 + sz key 1) := by
  rcases fin3 (key i) with hi | hi | hi
  · rw [(wt_of key i).1 hi, if_neg (by rw [hi]; decide)]
  · rw [(wt_of key i).2.1 hi, if_pos hi]
  · rw [(wt_of key i).2.2 hi, if_neg (by rw [hi]; decide), hac]; ring

/-- If the first ridge has outer blocks of equal size, so has any ridge with the same plate. -/
theorem outer_eq_of_plate_eq {key key' : Fin n → Fin 3} (hk : Function.Surjective key) (hk' : Function.Surjective key')
    (hac : sz key 0 = sz key 2)
    (h : VacuusResonus.permPlate (block key 0) (block key 1) (block key 2) =
      VacuusResonus.permPlate (block key' 0) (block key' 1) (block key' 2)) : sz key' 0 = sz key' 2 := by
  have r0 : Fin.rev (0 : Fin 3) = 2 := rfl; have r2 : Fin.rev (2 : Fin 3) = 0 := rfl
  by_contra hne
  rcases plate_eq_of_ne hk' hk hne h.symm with e | e
  · rw [e] at hac; exact hne hac
  · apply hne; have h2 := hac; rw [e, sz_rev, sz_rev, r0, r2] at h2; exact h2.symm

/-- **#120 Theorem 3 (ii), outer blocks of equal size.** Two ridges share a plate only if the second has the same middle
block as the first, or its complement. (Its outer blocks are then of equal size too, by `plate_eq_of_ne`.) -/
theorem middle_of_plate_eq {key key' : Fin n → Fin 3} (hk : Function.Surjective key) (hk' : Function.Surjective key')
    (hac : sz key 0 = sz key 2)
    (h : VacuusResonus.permPlate (block key 0) (block key 1) (block key 2) =
      VacuusResonus.permPlate (block key' 0) (block key' 1) (block key' 2)) :
    block key' 1 = block key 1 ∨ block key' 1 = (block key 1)ᶜ := by
  have hac' := outer_eq_of_plate_eq hk hk' hac h
  obtain ⟨l, m, hlm⟩ := affine_of_plate_eq h
  have hl := l_ne_zero hk' hlm
  have hX := mul_pos (sz_pos hk 2) (add_pos (sz_pos hk 0) (sz_pos hk 1))
  have hX' := mul_pos (sz_pos hk' 2) (add_pos (sz_pos hk' 0) (sz_pos hk' 1))
  have hlX : l * (sz key 2 * (sz key 0 + sz key 1)) ≠ 0 := mul_ne_zero hl hX.ne'
  obtain ⟨i1, g1⟩ := hk 1
  have e1 := hlm i1; rw [wt_two_level hac' i1, wt_two_level hac i1, if_pos g1] at e1
  by_cases c1 : key' i1 = 1
  · rw [if_pos c1] at e1
    left; ext i; simp only [block, mem_filter, mem_univ, true_and]
    have ei := hlm i; rw [wt_two_level hac' i, wt_two_level hac i] at ei
    by_cases a : key i = 1 <;> by_cases b : key' i = 1 <;> simp only [a, b, ↓reduceIte, iff_self] at ei ⊢ <;>
      first | (exfalso; linarith) | (exfalso; exact hlX (by linarith))
  · rw [if_neg c1] at e1
    right; ext i; simp only [block, mem_filter, mem_univ, true_and, mem_compl]
    have ei := hlm i; rw [wt_two_level hac' i, wt_two_level hac i] at ei
    by_cases a : key i = 1 <;> by_cases b : key' i = 1 <;>
      simp only [a, b, ↓reduceIte, iff_self, not_true_eq_false, not_false_eq_true] at ei ⊢ <;>
      first | (exfalso; linarith) | (exfalso; exact hlX (by linarith))

/-- Affinely related weights (factor not zero) give the same plate. -/
theorem plateOf_affine {u v : Fin n → ℝ} {l m : ℝ} (hl : l ≠ 0) (h : ∀ i, v i = l * u i + m) :
    VacuusResonus.plateOf v = VacuusResonus.plateOf u := by
  ext y
  simp only [VacuusResonus.plateOf, Submodule.mem_inf, LinearMap.mem_ker, VacuusResonus.dotL, LinearMap.coe_mk,
    AddHom.coe_mk, one_mul]
  have e : ∑ i, v i * y i = l * ∑ i, u i * y i + m * ∑ i, y i := by
    simp only [h, add_mul, sum_add_distrib, mul_sum, mul_assoc]
  rw [e]
  constructor
  · rintro ⟨h1, h2⟩; refine ⟨h1, ?_⟩; rw [h1, mul_zero, add_zero] at h2; exact (mul_eq_zero.1 h2).resolve_left hl
  · rintro ⟨h1, h2⟩; exact ⟨h1, by rw [h1, h2]; ring⟩

theorem permPlate_eq_plateOf_wt (key : Fin n → Fin 3) :
    VacuusResonus.permPlate (block key 0) (block key 1) (block key 2) = VacuusResonus.plateOf (wt key) := by
  ext y; exact mem_permPlate_iff

/-- **#120 Theorem 3 (ii), complete.** Two ridges (ordered partitions into three nonempty blocks) have the same Vacuus plate
exactly when: the outer blocks differ in size and the second ridge is the first or the first read backwards; or both ridges
have outer blocks of equal size and the same middle block or complementary middle blocks. -/
theorem plate_eq_iff {key key' : Fin n → Fin 3} (hk : Function.Surjective key) (hk' : Function.Surjective key') :
    VacuusResonus.permPlate (block key 0) (block key 1) (block key 2) =
        VacuusResonus.permPlate (block key' 0) (block key' 1) (block key' 2) ↔
      (sz key 0 ≠ sz key 2 ∧ (key' = key ∨ key' = Fin.rev ∘ key)) ∨
      (sz key 0 = sz key 2 ∧ sz key' 0 = sz key' 2 ∧
        (block key' 1 = block key 1 ∨ block key' 1 = (block key 1)ᶜ)) := by
  constructor
  · intro h
    by_cases hac : sz key 0 = sz key 2
    · exact Or.inr ⟨hac, outer_eq_of_plate_eq hk hk' hac h, middle_of_plate_eq hk hk' hac h⟩
    · exact Or.inl ⟨hac, plate_eq_of_ne hk hk' hac h⟩
  · rintro (⟨-, rfl | rfl⟩ | ⟨hac, hac', hB | hB⟩)
    · rfl
    · rw [permPlate_eq_plateOf_wt, permPlate_eq_plateOf_wt, wt_rev]
    · rw [permPlate_eq_plateOf_wt, permPlate_eq_plateOf_wt]
      have hX := mul_pos (sz_pos hk 2) (add_pos (sz_pos hk 0) (sz_pos hk 1))
      have hX' := mul_pos (sz_pos hk' 2) (add_pos (sz_pos hk' 0) (sz_pos hk' 1))
      have hmem : ∀ i, key' i = 1 ↔ key i = 1 := fun i => by
        have := Finset.ext_iff.1 hB i; simpa [block] using this
      refine (plateOf_affine (l := sz key' 2 * (sz key' 0 + sz key' 1) / (sz key 2 * (sz key 0 + sz key 1))) (m := 0)
        (div_ne_zero hX'.ne' hX.ne') fun i => ?_).symm
      rw [wt_two_level hac' i, wt_two_level hac i]
      by_cases hi : key i = 1
      · rw [if_pos ((hmem i).2 hi), if_pos hi]; ring
      · rw [if_neg (fun h' => hi ((hmem i).1 h')), if_neg hi, div_mul_cancel₀ _ hX.ne', add_zero]
    · rw [permPlate_eq_plateOf_wt, permPlate_eq_plateOf_wt]
      have hX := mul_pos (sz_pos hk 2) (add_pos (sz_pos hk 0) (sz_pos hk 1))
      have hX' := mul_pos (sz_pos hk' 2) (add_pos (sz_pos hk' 0) (sz_pos hk' 1))
      have hmem : ∀ i, key' i = 1 ↔ ¬ key i = 1 := fun i => by
        have := Finset.ext_iff.1 hB i; simpa [block] using this
      refine (plateOf_affine (l := -(sz key' 2 * (sz key' 0 + sz key' 1) / (sz key 2 * (sz key 0 + sz key 1))))
        (m := sz key' 2 * (sz key' 0 + sz key' 1)) (neg_ne_zero.2 (div_ne_zero hX'.ne' hX.ne')) fun i => ?_).symm
      rw [wt_two_level hac' i, wt_two_level hac i]
      by_cases hi : key i = 1
      · rw [if_neg (fun h' => (hmem i).1 h' hi), if_pos hi]; ring
      · rw [if_pos ((hmem i).2 hi), if_neg hi, neg_mul, div_mul_cancel₀ _ hX.ne']; ring

end PermFaces
