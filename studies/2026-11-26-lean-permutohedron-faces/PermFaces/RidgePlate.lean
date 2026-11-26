/-
#120 Theorem 3 (i) on the real permutohedron ridge (step 4 of the restructured Vacuus entry, 26 Nov 2026).
DICTO, with Claude (Anthropic). Built on TauCeti (Rado's theorem), PermFaces.Flags and the plate equation of PermFaces.PermPlate.
-/
import PermFaces.Flags
import PermFaces.PermPlate

/-!
# The Vacuus plate of a permutohedron ridge (step 4)

A ridge of the permutohedron is the face of an ordered set partition into three nonempty blocks `B₁, B₂, B₃`
(`key : Fin n → Fin 3` surjective; `Flags.lean` proves it is exposed of dimension `n - 3`). Centre the permutohedron
(`c = (n+1)/2` in every coordinate). **`span_centred_ridge`**: the plane through the centre and the ridge is
`{y | ∑ y = 0, c(a+b)∑_{B₁} y + a(b+c)∑_{B₃} y = 0}` (`a, b, c` the block sizes): #120 Theorem 3 (i), now for the ridge itself.
`top_eq` gives the facet heights in closed form.
-/

open Finset

namespace PermFaces

variable {n : ℕ}

theorem sum_range_sub (k : ℕ) : k ≤ n → ∑ i ∈ range k, ((n - i : ℕ) : ℝ) = (k : ℝ) * (2 * n - k + 1) / 2 := by
  induction k with
  | zero => intro; simp
  | succ k ih =>
    intro hk
    rw [sum_range_succ, ih (by omega), Nat.cast_sub (by omega)]
    push_cast; ring

/-- The sum of the `k` largest entries of `(n, …, 1)`. -/
theorem top_eq {k : ℕ} (hk : k ≤ n) : top n k = (k : ℝ) * (2 * n - k + 1) / 2 := by
  have h := TauCeti.prefixSum_eq_sum_range (n := n) k (fun j : ℕ => ((n - j : ℕ) : ℝ))
  rw [min_eq_left hk] at h
  rw [← sum_range_sub k hk]; unfold top w; exact h

/-- The centre of the permutohedron. -/
noncomputable def centre (n : ℕ) : Fin n → ℝ := fun _ => ((n : ℝ) + 1) / 2

theorem sum_centre (T : Finset (Fin n)) : ∑ i ∈ T, centre n i = T.card * (((n : ℝ) + 1) / 2) := by
  simp [centre]

section Ridge

variable {key : Fin n → Fin 3}

theorem block_disjoint {b b' : Fin 3} (h : b ≠ b') : Disjoint (block key b) (block key b') := by
  rw [block, block, disjoint_filter]; intro i _ h1 h2; exact h (h1.symm.trans h2)

theorem block_union : block key 0 ∪ block key 1 ∪ block key 2 = univ := by
  ext i; simp only [block, mem_union, mem_filter, mem_univ, true_and, iff_true]
  have := (key i).isLt; rcases (key i) with ⟨k, hk⟩; interval_cases k <;> simp

theorem sum_three (v : Fin n → ℝ) : ∑ i, v i = ∑ i ∈ block key 0, v i + ∑ i ∈ block key 1, v i + ∑ i ∈ block key 2, v i := by
  rw [← block_union (key := key), sum_union (disjoint_union_left.2 ⟨block_disjoint (by decide), block_disjoint (by decide)⟩),
    sum_union (block_disjoint (by decide))]

theorem low0 : low key 0 = block key 0 := by
  ext i; simp only [low, block, mem_filter, mem_univ, true_and]; constructor
  · intro h; exact Fin.ext (by omega)
  · intro h; rw [h]; rfl

theorem low1 : low key 1 = block key 0 ∪ block key 1 := by
  ext i; simp only [low, block, mem_union, mem_filter, mem_univ, true_and]
  have := (key i).isLt; rcases hk : key i with ⟨k, hk'⟩; interval_cases k <;> simp [Fin.ext_iff]

theorem low2 : low key 2 = univ := by
  ext i; simp only [low, mem_filter, mem_univ, true_and, iff_true]; have := (key i).isLt; omega

theorem card_three : (block key 0).card + (block key 1).card + (block key 2).card = n := by
  have := congrArg Finset.card (block_union (key := key))
  rw [card_union_of_disjoint (disjoint_union_left.2 ⟨block_disjoint (by decide), block_disjoint (by decide)⟩),
    card_union_of_disjoint (block_disjoint (by decide)), card_univ, Fintype.card_fin] at this
  exact this

/-- The centred points of the ridge satisfy the two facet equations of `permFlat` (now proved from the facets of `P n`). -/
theorem centred_mem_permFlat {x : Fin n → ℝ} (hx : x ∈ flagFace key) :
    x - centre n ∈ VacuusResonus.permFlat (block key 0) (block key 1) (block key 2) := by
  obtain ⟨hP, h⟩ := hx
  have h0 := h 0; have h1 := h 1; have h2 := h 2
  simp only [Fin.val_zero, Fin.val_one, Fin.val_two] at h0 h1 h2
  rw [low0] at h0; rw [low1] at h1; rw [low2] at h2
  have hc := card_three (key := key)
  set a := (block key 0).card; set b := (block key 1).card; set c := (block key 2).card
  have d01 : Disjoint (block key 0) (block key 1) := block_disjoint (by decide)
  rw [sum_union d01, card_union_of_disjoint d01] at h1
  rw [card_univ, Fintype.card_fin] at h2
  rw [top_eq (by omega)] at h0 h1; rw [top_eq le_rfl] at h2
  have hs := sum_three (key := key) x
  refine ⟨?_, ?_, ?_⟩
  · simp only [Pi.sub_apply, sum_sub_distrib, sum_centre, h0]
    have : (n : ℝ) = a + b + c := by exact_mod_cast hc.symm
    rw [this]; ring
  · rw [sum_union d01]
    simp only [Pi.sub_apply, sum_sub_distrib, sum_centre]
    have hn : (n : ℝ) = a + b + c := by exact_mod_cast hc.symm
    push_cast at h1
    rw [hn] at h1 ⊢
    linear_combination h1
  · simp only [Pi.sub_apply, sum_sub_distrib, sum_centre, card_univ, Fintype.card_fin]
    rw [h2]; ring

/-- `vectorSpan` of the ridge lies in the span of the centred ridge. -/
theorem vectorSpan_le_span_centred :
    vectorSpan ℝ (flagFace key) ≤ Submodule.span ℝ ((fun x => x - centre n) '' flagFace key) := by
  rw [vectorSpan_def, Submodule.span_le]
  rintro _ ⟨x, hx, y, hy, rfl⟩
  have : x -ᵥ y = (x - centre n) - (y - centre n) := by simp [vsub_eq_sub]
  show x -ᵥ y ∈ Submodule.span ℝ _
  rw [this]
  exact Submodule.sub_mem _ (Submodule.subset_span ⟨x, hx, rfl⟩) (Submodule.subset_span ⟨y, hy, rfl⟩)

/-- **#120 Theorem 3 (i) on the real ridge.** For an ordered partition into three nonempty blocks, the plane through the
centre and the ridge (the face of `key`) is the Vacuus plate `permPlate B₁ B₂ B₃`. -/
theorem span_centred_ridge (hkey : Function.Surjective key) :
    Submodule.span ℝ ((fun x => x - centre n) '' flagFace key) =
      VacuusResonus.permPlate (block key 0) (block key 1) (block key 2) := by
  have ne : ∀ b, (block key b).Nonempty := fun b => by
    obtain ⟨i, hi⟩ := hkey b; exact ⟨i, by simp [block, hi]⟩
  have hspan := VacuusResonus.span_permFlat (block_disjoint (key := key) (by decide : (0 : Fin 3) ≠ 1))
    (block_disjoint (by decide : (0 : Fin 3) ≠ 2)) (block_disjoint (by decide : (1 : Fin 3) ≠ 2)) block_union (ne 0) (ne 1) (ne 2)
  rw [← hspan]
  apply le_antisymm
  · rw [Submodule.span_le]; rintro _ ⟨x, hx, rfl⟩
    exact Submodule.subset_span (centred_mem_permFlat hx)
  · rw [Submodule.span_le]; intro q hq
    obtain ⟨π, hπ⟩ := exists_vertex_flag key
    have hv : w n ∘ π ∈ flagFace key := ⟨subset_convexHull ℝ _ ⟨π, rfl⟩, fun t => hπ t⟩
    have hp0 := centred_mem_permFlat hv
    set p0 := w n ∘ π - centre n
    have hdiff : q - p0 ∈ LinearMap.ker (blockL key) := by
      rw [mem_ker_blockL]; intro b
      obtain ⟨q1, q2, q0⟩ := hq; obtain ⟨p1, p2, p0'⟩ := hp0
      have d01 : Disjoint (block key 0) (block key 1) := block_disjoint (by decide)
      rw [sum_union d01] at q2 p2
      have sq := sum_three (key := key) q; have sp := sum_three (key := key) p0
      simp only [Pi.sub_apply, sum_sub_distrib]
      fin_cases b <;> simp <;> linarith
    rw [← vectorSpan_flagFace hkey] at hdiff
    have : q = p0 + (q - p0) := by abel
    rw [SetLike.mem_coe, this]
    exact Submodule.add_mem _ (Submodule.subset_span ⟨_, hv, rfl⟩) (vectorSpan_le_span_centred hdiff)

end Ridge

end PermFaces
