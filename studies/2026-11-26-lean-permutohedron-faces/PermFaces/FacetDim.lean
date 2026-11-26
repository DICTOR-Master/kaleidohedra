/-
The facets of the permutohedron have dimension n - 2 (step 3b of the restructured Vacuus entry, 26 Nov 2026).
DICTO, with Claude (Anthropic). Built on TauCeti (Rado's theorem) and PermFaces.Facets.
-/
import PermFaces.Facets

/-!
# Facet directions and dimension (step 3b)

For `∅ ≠ S ≠ univ`, the directions of the facet of `S` are exactly the vectors whose coordinates sum to `0` over `S` and over
its complement (`vectorSpan_facet`), a subspace of dimension `n - 2` (`finrank_vectorSpan_facet`).
-/

open Finset

namespace PermFaces

variable {n : ℕ}

/-- `v ↦ ∑_{i ∈ T} vᵢ` as a linear map. -/
def sumL (T : Finset (Fin n)) : (Fin n → ℝ) →ₗ[ℝ] ℝ where
  toFun v := ∑ i ∈ T, v i
  map_add' x y := by simp [sum_add_distrib]
  map_smul' c x := by simp [mul_sum]

/-- The pair of sums over `S` and over its complement. -/
def pairL (S : Finset (Fin n)) : (Fin n → ℝ) →ₗ[ℝ] ℝ × ℝ := (sumL S).prod (sumL Sᶜ)

/-- The directions predicted for the facet of `S`. -/
def dirs (S : Finset (Fin n)) : Submodule ℝ (Fin n → ℝ) := LinearMap.ker (pairL S)

theorem mem_dirs {S : Finset (Fin n)} {v : Fin n → ℝ} :
    v ∈ dirs S ↔ ∑ i ∈ S, v i = 0 ∧ ∑ i ∈ Sᶜ, v i = 0 := by
  simp [dirs, pairL, sumL, Prod.ext_iff]

theorem w_injective : Function.Injective (w n) := by
  intro i j h
  simp only [w] at h
  have h' : n - (i : ℕ) = n - (j : ℕ) := by exact_mod_cast h
  have hi := i.isLt; have hj := j.isLt
  exact Fin.ext (by omega)

/-- Directions of the facet lie in `dirs S`. -/
theorem vectorSpan_facet_le (S : Finset (Fin n)) : vectorSpan ℝ (facet S) ≤ dirs S := by
  rw [vectorSpan_def, Submodule.span_le]
  rintro _ ⟨x, ⟨hx, hxS⟩, y, ⟨hy, hyS⟩, rfl⟩
  have tx := TauCeti.sum_eq_of_mem_convexHull_range_comp_perm hx
  have ty := TauCeti.sum_eq_of_mem_convexHull_range_comp_perm hy
  rw [SetLike.mem_coe, mem_dirs]
  simp only [vsub_eq_sub, Pi.sub_apply, sum_sub_distrib]
  refine ⟨by rw [hxS, hyS, sub_self], ?_⟩
  have cx := sum_add_sum_compl S x; have cy := sum_add_sum_compl S y
  linarith

/-- `eᵢ - eⱼ` is a direction of the facet when `i, j` are on the same side of `S`. -/
theorem single_sub_mem {S : Finset (Fin n)} {i j : Fin n} (hij : i ≠ j) (hside : (i ∈ S ↔ j ∈ S)) :
    (Pi.single i 1 - Pi.single j 1 : Fin n → ℝ) ∈ vectorSpan ℝ (facet S) := by
  classical
  obtain ⟨π, hπ⟩ := exists_vertex_top S
  set y : Fin n → ℝ := w n ∘ π
  have hyP : y ∈ P n := subset_convexHull ℝ _ ⟨π, rfl⟩
  set s := Equiv.swap i j
  have hys : y ∘ s ∈ P n := (Equiv.Perm.comp_perm_mem_convexHull_range_comp_perm_iff s).2 hyP
  have hsum : ∑ k ∈ S, (y ∘ s) k = ∑ k ∈ S, y k := by
    have hmapS : S.map s.toEmbedding = S := by
      ext k; simp only [mem_map, Equiv.toEmbedding_apply]
      constructor
      · rintro ⟨m, hm, rfl⟩
        rcases eq_or_ne m i with rfl | hmi
        · simpa [s, Equiv.swap_apply_left] using hside.1 hm
        rcases eq_or_ne m j with rfl | hmj
        · simpa [s, Equiv.swap_apply_right] using hside.2 hm
        simpa [s, Equiv.swap_apply_of_ne_of_ne hmi hmj] using hm
      · intro hk; exact ⟨s k, by
          rcases eq_or_ne k i with rfl | hki
          · simpa [s, Equiv.swap_apply_left] using hside.1 hk
          rcases eq_or_ne k j with rfl | hkj
          · simpa [s, Equiv.swap_apply_right] using hside.2 hk
          simpa [s, Equiv.swap_apply_of_ne_of_ne hki hkj] using hk, by simp [s]⟩
    calc ∑ k ∈ S, (y ∘ s) k = ∑ k ∈ S.map s.toEmbedding, y k := by rw [sum_map]; rfl
      _ = ∑ k ∈ S, y k := by rw [hmapS]
  have h1 : y ∈ facet S := ⟨hyP, hπ⟩
  have h2 : y ∘ s ∈ facet S := ⟨hys, hsum.trans hπ⟩
  have hd : y -ᵥ y ∘ s = (y i - y j) • (Pi.single i 1 - Pi.single j 1 : Fin n → ℝ) := by
    funext k
    simp only [vsub_eq_sub, Pi.sub_apply, Function.comp_apply, Pi.smul_apply, smul_eq_mul]
    rcases eq_or_ne k i with rfl | hki
    · simp [s, Equiv.swap_apply_left, hij]
    rcases eq_or_ne k j with rfl | hkj
    · simp [s, Equiv.swap_apply_right, hij.symm]
    simp [s, Equiv.swap_apply_of_ne_of_ne hki hkj, hki, hkj]
  have hne : y i - y j ≠ 0 := sub_ne_zero.2 (fun h => hij (π.injective (w_injective h)))
  have := Submodule.smul_mem _ (y i - y j)⁻¹ (vsub_mem_vectorSpan ℝ h1 h2)
  rwa [hd, smul_smul, inv_mul_cancel₀ hne, one_smul] at this

/-- **The directions of a facet.** For `∅ ≠ S ≠ univ`, the vector span of the facet of `S` is `dirs S`. -/
theorem vectorSpan_facet {S : Finset (Fin n)} (hS : S.Nonempty) (hSc : Sᶜ.Nonempty) :
    vectorSpan ℝ (facet S) = dirs S := by
  classical
  refine le_antisymm (vectorSpan_facet_le S) ?_
  obtain ⟨i₀, hi₀⟩ := hS; obtain ⟨j₀, hj₀⟩ := hSc
  intro v hv
  rw [mem_dirs] at hv
  have hrep : v = ∑ i ∈ S, v i • (Pi.single i 1 - Pi.single i₀ 1 : Fin n → ℝ) +
      ∑ j ∈ Sᶜ, v j • (Pi.single j 1 - Pi.single j₀ 1 : Fin n → ℝ) := by
    funext k
    simp only [Pi.add_apply, Finset.sum_apply, Pi.smul_apply, Pi.sub_apply, smul_eq_mul, mul_sub, sum_sub_distrib,
      Pi.single_apply, mul_ite, mul_one, mul_zero, sum_ite_eq', ← sum_mul]
    by_cases hk : k ∈ S
    · have hk' : k ∉ Sᶜ := by simpa using hk
      have : (k = j₀) = False := by
        apply propext; constructor
        · rintro rfl; exact (mem_compl.1 hj₀) hk
        · intro h; exact h.elim
      simp [hk, hk', hv.1, hv.2]
      all_goals (split_ifs <;> simp_all)
    · have hk' : k ∈ Sᶜ := by simpa using hk
      simp [hk, hk', hv.1, hv.2]
      all_goals (split_ifs <;> simp_all)
  rw [hrep]
  refine Submodule.add_mem _ (Submodule.sum_mem _ fun i hi => ?_) (Submodule.sum_mem _ fun j hj => ?_)
  · rcases eq_or_ne i i₀ with rfl | h
    · simp
    · exact Submodule.smul_mem _ _ (single_sub_mem h (by simp [hi, hi₀]))
  · rcases eq_or_ne j j₀ with rfl | h
    · simp
    · exact Submodule.smul_mem _ _ (single_sub_mem h
        ⟨fun h' => absurd h' (mem_compl.1 hj), fun h' => absurd h' (mem_compl.1 hj₀)⟩)

/-- **Each facet has dimension `n - 2`.** -/
theorem finrank_vectorSpan_facet {S : Finset (Fin n)} (hS : S.Nonempty) (hSc : Sᶜ.Nonempty) :
    Module.finrank ℝ (vectorSpan ℝ (facet S)) = n - 2 := by
  classical
  rw [vectorSpan_facet hS hSc, dirs]
  obtain ⟨i₀, hi₀⟩ := hS; obtain ⟨j₀, hj₀⟩ := hSc
  have hsurj : LinearMap.range (pairL S) = ⊤ := by
    rw [LinearMap.range_eq_top]
    rintro ⟨a, b⟩
    refine ⟨a • Pi.single i₀ 1 + b • Pi.single j₀ 1, ?_⟩
    have hj : j₀ ∉ S := mem_compl.1 hj₀
    have hi : i₀ ∉ Sᶜ := by simpa using hi₀
    simp [pairL, sumL, Pi.single_apply, sum_add_distrib, ← mul_sum, sum_ite_eq', hi₀, hj, hi, hj₀]
  have := LinearMap.finrank_range_add_finrank_ker (pairL S)
  rw [hsurj, finrank_top, Module.finrank_prod, Module.finrank_self, Module.finrank_fin_fun] at this
  omega

end PermFaces
