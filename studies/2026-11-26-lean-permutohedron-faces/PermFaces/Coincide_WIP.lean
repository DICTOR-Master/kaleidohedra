/- WORK IN PROGRESS (26 Nov 2026 night): the classification proof; compile errors still to fix. Not imported. -/
import PermFaces.Coincide
open Finset
namespace PermFaces
variable {n : ℕ}
/-- The weight of a coordinate depends only on its block. -/
noncomputable def W (key : Fin n → Fin 3) (p : Fin 3) : ℝ :=
  if p = 0 then sz key 2 * (sz key 0 + sz key 1) else if p = 2 then sz key 0 * (sz key 1 + sz key 2) else 0

theorem wt_eq_W (key : Fin n → Fin 3) (i : Fin n) : wt key i = W key (key i) := rfl

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
  choose r hr using hk
  have pa := sz_pos (key := key) (fun b => ⟨r b, hr b⟩) 0; have pb := sz_pos (key := key) (fun b => ⟨r b, hr b⟩) 1
  have pc := sz_pos (key := key) (fun b => ⟨r b, hr b⟩) 2
  have pa' := sz_pos hk' 0; have pb' := sz_pos hk' 1; have pc' := sz_pos hk' 2
  -- the weights of key at its three blocks are distinct
  have hxy : sz key 2 * (sz key 0 + sz key 1) ≠ sz key 0 * (sz key 1 + sz key 2) := by
    intro e; apply hac
    have : sz key 1 * (sz key 2 - sz key 0) = 0 := by linarith
    rcases mul_eq_zero.1 this with h | h
    · linarith
    · linarith
  set π : Fin 3 → Fin 3 := fun b => key' (r b)
  have Wk : ∀ b, wt key (r b) = W key b := fun b => by rw [wt_eq_W, hr]
  have E : ∀ b, W key' (π b) = l * W key b + m := fun b => by rw [← Wk, ← wt_eq_W]; exact hlm (r b)
  have W0 : W key 0 = sz key 2 * (sz key 0 + sz key 1) := rfl
  have W1 : W key 1 = 0 := rfl
  have W2 : W key 2 = sz key 0 * (sz key 1 + sz key 2) := rfl
  -- π is injective: distinct weights of key give distinct weights of key'
  have Wd : ∀ b b', b ≠ b' → W key b ≠ W key b' := by
    intro b b' hbb'
    fin_cases b <;> fin_cases b' <;> simp_all [W] <;> first | exact hxy | exact (Ne.symm hxy) | nlinarith | (intro e; nlinarith)
  have πinj : Function.Injective π := by
    intro b b' he
    by_contra hne
    have := E b; have := E b'
    rw [show π b = π b' from he] at *
    exact Wd b b' hne (by
      have h1 := E b; have h2 := E b'; rw [he] at h1
      have : l * W key b = l * W key b' := by linarith
      exact mul_left_cancel₀ hl this)
  -- key' = π ∘ key
  have Wd' : ∀ p q : Fin 3, W key' p = W key' q → p ≠ q → (p ≠ 1 ∧ q ≠ 1) := by
    intro p q e hpq
    fin_cases p <;> fin_cases q <;> simp_all [W] <;> nlinarith
  have hkey : ∀ i, key' i = π (key i) := by
    intro i
    have h1 : W key' (key' i) = W key' (π (key i)) := by
      rw [← wt_eq_W, hlm, wt_eq_W, E]
    by_contra hne
    -- equal weights of key' at two different labels force those labels to be 0 and 2 with equal outer sizes
    obtain ⟨hp, hq⟩ := Wd' _ _ h1 hne
    -- then π maps the blocks of key onto 0, 1, 2; the label 1 is π b₁ for some b₁, and W key' 0 = W key' 2
    have hsurjπ : Function.Surjective π := Finite.injective_iff_surjective.1 πinj
    obtain ⟨b0, hb0⟩ := hsurjπ 0; obtain ⟨b2, hb2⟩ := hsurjπ 2
    have e02 : W key' 0 = W key' 2 := by
      rcases hp' : key' i with ⟨p, hpp⟩; rcases hq' : π (key i) with ⟨q, hqq⟩
      rw [hp', hq'] at h1 hne hp hq
      interval_cases p <;> interval_cases q <;> simp_all
    have := E b0; have := E b2; rw [hb0] at *; rw [hb2] at *
    have hb02 : b0 ≠ b2 := fun e => by rw [e] at hb0; rw [hb0] at hb2; exact absurd hb2 (by decide)
    exact Wd b0 b2 hb02 (mul_left_cancel₀ hl (by linarith))
  -- sizes are relabelled
  have S := sz_relabel πinj hkey
  -- the six relabellings
  have Eb := fun b => E b
  rcases h0 : π 0 with ⟨p0, hp0⟩; rcases h1 : π 1 with ⟨p1, hp1⟩; rcases h2 : π 2 with ⟨p2, hp2⟩
  have S0 := S 0; have S1 := S 1; have S2 := S 2
  have E0 := E 0; have E1 := E 1; have E2 := E 2
  rw [h0] at S0 E0; rw [h1] at S1 E1; rw [h2] at S2 E2
  have i01 : π 0 ≠ π 1 := πinj.ne (by decide); have i02 : π 0 ≠ π 2 := πinj.ne (by decide)
  have i12 : π 1 ≠ π 2 := πinj.ne (by decide)
  rw [h0, h1] at i01; rw [h0, h2] at i02; rw [h1, h2] at i12
  interval_cases p0 <;> interval_cases p1 <;> interval_cases p2 <;> simp_all [W]
  -- identity
  · left; funext i; rw [hkey]; rcases hki : key i with ⟨k, hk⟩; interval_cases k <;> simp_all
  -- (0 2 1), (1 0 2), (1 2 0), (2 0 1): contradictions; (2 1 0): reversal
  all_goals first
    | (right; funext i; rw [hkey, Function.comp_apply]; rcases hki : key i with ⟨k, hk⟩; interval_cases k <;> simp_all <;> rfl)
    | (exfalso; nlinarith [mul_pos pa pb, mul_pos pb pc, mul_pos pa pc])

end PermFaces
