/-
Every face of the permutohedron comes from an ordered partition. DICTO, with Claude (Anthropic).
-/
import PermFaces.Count

/-!
# Every face of the permutohedron comes from an ordered partition

A face is a nonempty exposed face of `P n` (Mathlib `IsExposed`): the set of points of `P n` where a linear functional is
largest. Group the coordinates by the coefficient of the functional, largest coefficient first: this ordered partition is
`key`, and the face is `flagFace key`.
* `exposed_eq_flagFace`: every nonempty exposed face of `P n` is `flagFace key` for a surjective `key : Fin n → Fin m`.
* `exposed_eq_flagFace_of_finrank`: if its dimension is `n - k` (`k ≤ n`), then `m = k`.
* `ridge_eq_flagFace` (`k = 3`), `facet_eq_flagFace` (`k = 2`), `facet_eq_facet` (a facet is `facet S`, `∅ ≠ S ≠ univ`).
* `plateSet_eq_ridge_planes`: `plateSet n` is the set of planes through the centre and a face of dimension `n - 3`,
  a description with no partitions in it; `card_ridge_planes` counts these planes.
-/

open Finset

namespace PermFaces

variable {n m : ℕ}

/-! ### Summation by blocks -/

theorem sum_Ico_sub_succ (g : ℕ → ℝ) {b m : ℕ} (h : b ≤ m) :
    ∑ t ∈ Ico b m, (g t - g (t + 1)) = g b - g m := by
  induction m, h using Nat.le_induction with
  | base => simp
  | succ k hk ih => rw [sum_Ico_succ_top hk, ih]; ring

/-- A functional constant on blocks (`g b` on block `b`) is a combination of the sums over initial unions of blocks. -/
theorem sum_weights_low (key : Fin n → Fin m) (g : ℕ → ℝ) (hg : g m = 0) (x : Fin n → ℝ) :
    ∑ t ∈ range m, (g t - g (t + 1)) * ∑ i ∈ low key t, x i = ∑ i, g (key i) * x i := by
  classical
  calc ∑ t ∈ range m, (g t - g (t + 1)) * ∑ i ∈ low key t, x i
      = ∑ t ∈ range m, ∑ i, if (key i : ℕ) ≤ t then (g t - g (t + 1)) * x i else 0 := by
        refine sum_congr rfl fun t _ => ?_
        rw [low, mul_sum, sum_filter]
    _ = ∑ i, ∑ t ∈ range m, if (key i : ℕ) ≤ t then (g t - g (t + 1)) * x i else 0 := sum_comm
    _ = ∑ i, g (key i) * x i := by
        refine sum_congr rfl fun i _ => ?_
        have hI : (range m).filter (fun t => (key i : ℕ) ≤ t) = Ico (key i : ℕ) m := by
          ext t; simp only [mem_filter, mem_range, mem_Ico]; tauto
        rw [← sum_filter, ← sum_mul, hI, sum_Ico_sub_succ g (key i).isLt.le, hg, sub_zero]

/-- The union of all the blocks has the largest sum at every point of `P n`. -/
theorem sum_low_of_le (key : Fin n → Fin m) {x : Fin n → ℝ} (hx : x ∈ P n) {t : ℕ} (ht : m ≤ t + 1) :
    ∑ i ∈ low key t, x i = top n (low key t).card := by
  obtain ⟨π, hπ⟩ := exists_vertex_flag key
  have hlow : low key t = univ := by
    ext i; simp only [low, mem_filter, mem_univ, true_and, iff_true]; have := (key i).isLt; omega
  have hv : w n ∘ π ∈ P n := subset_convexHull ℝ _ ⟨π, rfl⟩
  have h1 := TauCeti.sum_eq_of_mem_convexHull_range_comp_perm hx
  have h2 := TauCeti.sum_eq_of_mem_convexHull_range_comp_perm hv
  rw [← hπ t, hlow]
  exact h1.trans h2.symm

/-- **The maximisers of a block-constant functional with strictly decreasing values form the face of the partition.** -/
theorem maximiser_eq_flagFace (key : Fin n → Fin m) (g : ℕ → ℝ) (hg0 : g m = 0)
    (hanti : ∀ t, t + 1 < m → g (t + 1) < g t) :
    {x | x ∈ P n ∧ ∀ y ∈ P n, ∑ i, g (key i) * y i ≤ ∑ i, g (key i) * x i} = flagFace key := by
  classical
  obtain ⟨π, hπ⟩ := exists_vertex_flag key
  have hvP : w n ∘ π ∈ P n := subset_convexHull ℝ _ ⟨π, rfl⟩
  have hle : ∀ y ∈ P n, ∀ t ∈ range m, (g t - g (t + 1)) * ∑ i ∈ low key t, y i ≤
      (g t - g (t + 1)) * top n (low key t).card := by
    intro y hy t _
    by_cases h : t + 1 < m
    · exact mul_le_mul_of_nonneg_left (sum_le_top hy _) (sub_pos.2 (hanti t h)).le
    · rw [sum_low_of_le key hy (by omega)]
  have hv : ∑ i, g (key i) * (w n ∘ π) i = ∑ t ∈ range m, (g t - g (t + 1)) * top n (low key t).card := by
    rw [← sum_weights_low key g hg0]; exact sum_congr rfl fun t _ => by rw [hπ t]
  ext x
  simp only [flagFace, Set.mem_ofPred_eq]
  constructor
  · rintro ⟨hx, hmax⟩
    refine ⟨hx, fun t => ?_⟩
    have hge := hmax _ hvP
    rw [hv, ← sum_weights_low key g hg0 x] at hge
    have heq := (sum_eq_sum_iff_of_le (hle x hx)).1 (le_antisymm (sum_le_sum (hle x hx)) hge) t
      (mem_range.2 t.isLt)
    by_cases h : (t : ℕ) + 1 < m
    · exact mul_left_cancel₀ (sub_pos.2 (hanti t h)).ne' heq
    · exact sum_low_of_le key hx (by omega)
  · rintro ⟨hx, heq⟩
    refine ⟨hx, fun y hy => ?_⟩
    rw [← sum_weights_low key g hg0 y, ← sum_weights_low key g hg0 x]
    refine (sum_le_sum (hle y hy)).trans (le_of_eq (sum_congr rfl fun t ht => ?_))
    exact congrArg (fun z => (g t - g (t + 1)) * z) (heq ⟨t, mem_range.1 ht⟩).symm

/-! ### The ordered partition of a functional -/

/-- Group the coordinates by the value of `c`, largest value first. -/
theorem exists_key (c : Fin n → ℝ) :
    ∃ (m : ℕ) (key : Fin n → Fin m) (g : ℕ → ℝ), Function.Surjective key ∧ g m = 0 ∧
      (∀ t, t + 1 < m → g (t + 1) < g t) ∧ ∀ i, g (key i) = c i := by
  classical
  obtain ⟨V, hV⟩ : ∃ V : Finset ℝ, ∀ v, v ∈ V ↔ ∃ i, -c i = v :=
    ⟨univ.image fun i => -c i, fun v => by simp⟩
  obtain ⟨m, hm⟩ : ∃ m, V.card = m := ⟨_, rfl⟩
  have hmem : ∀ i, -c i ∈ V := fun i => (hV _).2 ⟨i, rfl⟩
  let e : Fin m ≃o V := V.orderIsoOfFin hm
  refine ⟨m, fun i => e.symm ⟨-c i, hmem i⟩,
    fun t => if h : t < m then -((e ⟨t, h⟩ : V) : ℝ) else 0, ?_, ?_, ?_, ?_⟩
  · intro b
    obtain ⟨i, hi⟩ := (hV _).1 (e b).2
    exact ⟨i, e.symm_apply_eq.2 (Subtype.ext hi)⟩
  · simp
  · intro t ht
    have h1 : t < m := by omega
    have hlt : e ⟨t, h1⟩ < e ⟨t + 1, ht⟩ := e.strictMono (Fin.mk_lt_mk.2 (Nat.lt_succ_self t))
    simp only [ht, h1, ↓reduceDIte]
    exact neg_lt_neg (Subtype.coe_lt_coe.2 hlt)
  · intro i
    simp only [Fin.is_lt, ↓reduceDIte, Fin.eta, OrderIso.apply_symm_apply, neg_neg]

/-! ### Every face comes from an ordered partition -/

/-- **Every nonempty exposed face of the permutohedron is the face of an ordered partition into nonempty blocks.** -/
theorem exposed_eq_flagFace {F : Set (Fin n → ℝ)} (hF : IsExposed ℝ (P n) F) (hne : F.Nonempty) :
    ∃ (m : ℕ) (key : Fin n → Fin m), Function.Surjective key ∧ F = flagFace key := by
  classical
  obtain ⟨l, rfl⟩ := hF hne
  obtain ⟨m, key, g, hsurj, hg0, hanti, hgk⟩ := exists_key (fun i => l (fun j => if i = j then 1 else 0))
  refine ⟨m, key, hsurj, ?_⟩
  have hl : ∀ x, l x = ∑ i, g (key i) * x i := by
    intro x
    calc l x = (l : (Fin n → ℝ) →ₗ[ℝ] ℝ) x := rfl
      _ = ∑ i, x i • (l : (Fin n → ℝ) →ₗ[ℝ] ℝ) (fun j => if i = j then 1 else 0) :=
        LinearMap.pi_apply_eq_sum_univ _ x
      _ = ∑ i, g (key i) * x i := sum_congr rfl fun i _ => by
        show x i * l (fun j => if i = j then 1 else 0) = g (key i) * x i
        rw [hgk i]; exact mul_comm _ _
  rw [← maximiser_eq_flagFace key g hg0 hanti]
  ext x
  simp only [Set.mem_ofPred_eq, hl]

/-- A nonempty exposed face of dimension `n - k` is the face of an ordered partition into `k` nonempty blocks. -/
theorem exposed_eq_flagFace_of_finrank {F : Set (Fin n → ℝ)} {k : ℕ} (hk : k ≤ n) (hF : IsExposed ℝ (P n) F)
    (hne : F.Nonempty) (hd : Module.finrank ℝ (vectorSpan ℝ F) = n - k) :
    ∃ key : Fin n → Fin k, Function.Surjective key ∧ F = flagFace key := by
  obtain ⟨m, key, hsurj, rfl⟩ := exposed_eq_flagFace hF hne
  have hmn : m ≤ n := by simpa using Fintype.card_le_of_surjective key hsurj
  rw [finrank_vectorSpan_flagFace hsurj] at hd
  obtain rfl : m = k := by omega
  exact ⟨key, hsurj, rfl⟩

/-- **Every ridge (nonempty exposed face of dimension `n - 3`) is the face of an ordered partition into three nonempty
blocks.** -/
theorem ridge_eq_flagFace (hn : 3 ≤ n) {F : Set (Fin n → ℝ)} (hF : IsExposed ℝ (P n) F) (hne : F.Nonempty)
    (hd : Module.finrank ℝ (vectorSpan ℝ F) = n - 3) :
    ∃ key : Fin n → Fin 3, Function.Surjective key ∧ F = flagFace key :=
  exposed_eq_flagFace_of_finrank hn hF hne hd

/-- Every facet (nonempty exposed face of dimension `n - 2`) is the face of an ordered partition into two nonempty blocks. -/
theorem facet_eq_flagFace (hn : 2 ≤ n) {F : Set (Fin n → ℝ)} (hF : IsExposed ℝ (P n) F) (hne : F.Nonempty)
    (hd : Module.finrank ℝ (vectorSpan ℝ F) = n - 2) :
    ∃ key : Fin n → Fin 2, Function.Surjective key ∧ F = flagFace key :=
  exposed_eq_flagFace_of_finrank hn hF hne hd

/-- The face of a two-block partition is the facet of its first block. -/
theorem flagFace_two (key : Fin n → Fin 2) : flagFace key = facet (low key 0) := by
  ext x
  simp only [flagFace, facet, Set.mem_ofPred_eq]
  constructor
  · rintro ⟨hx, h⟩; exact ⟨hx, by simpa using h 0⟩
  · rintro ⟨hx, h⟩
    refine ⟨hx, fun t => ?_⟩
    rcases Nat.eq_zero_or_pos (t : ℕ) with h0 | h1
    · rw [h0]; exact h
    · exact sum_low_of_le key hx (by omega)

/-- **Every facet is `facet S` for a set of coordinates `∅ ≠ S ≠ univ`.** -/
theorem facet_eq_facet (hn : 2 ≤ n) {F : Set (Fin n → ℝ)} (hF : IsExposed ℝ (P n) F) (hne : F.Nonempty)
    (hd : Module.finrank ℝ (vectorSpan ℝ F) = n - 2) :
    ∃ S : Finset (Fin n), S.Nonempty ∧ Sᶜ.Nonempty ∧ F = facet S := by
  obtain ⟨key, hsurj, rfl⟩ := facet_eq_flagFace hn hF hne hd
  obtain ⟨i, hi⟩ := hsurj 0
  obtain ⟨j, hj⟩ := hsurj 1
  refine ⟨low key 0, ⟨i, ?_⟩, ⟨j, ?_⟩, flagFace_two key⟩
  · simp [low, hi]
  · simp [low, hj]

/-! ### The plates, with no partitions in the definition -/

/-- The planes through the centre and a ridge of the permutohedron, a ridge being a nonempty exposed face of dimension
`n - 3`. -/
def ridgePlanes (n : ℕ) : Set (Submodule ℝ (Fin n → ℝ)) :=
  {Q | ∃ F : Set (Fin n → ℝ), IsExposed ℝ (P n) F ∧ F.Nonempty ∧
    Module.finrank ℝ (vectorSpan ℝ F) = n - 3 ∧ Submodule.span ℝ ((fun x => x - centre n) '' F) = Q}

/-- **The plates of the ordered three-block partitions are exactly the planes through the centre and the ridges.** -/
theorem plateSet_eq_ridge_planes (hn : 3 ≤ n) : plateSet n = ridgePlanes n := by
  ext Q
  constructor
  · rintro ⟨key, hsurj, rfl⟩
    obtain ⟨π, hπ⟩ := exists_vertex_flag key
    exact ⟨flagFace key, flagFace_isExposed key, ⟨w n ∘ π, subset_convexHull ℝ _ ⟨π, rfl⟩, fun t => hπ t⟩,
      finrank_vectorSpan_flagFace hsurj, span_centred_ridge hsurj⟩
  · rintro ⟨F, hF, hne, hd, rfl⟩
    obtain ⟨key, hsurj, rfl⟩ := ridge_eq_flagFace hn hF hne hd
    exact ⟨key, hsurj, (span_centred_ridge hsurj).symm⟩

/-- **The number of planes through the centre and a ridge of the permutohedron** (`n ≥ 3`): the closed formula of
`card_plateSet` (OEIS A402191). -/
theorem card_ridge_planes (hn : 3 ≤ n) :
    (ridgePlanes n).ncard =
      ∑ t ∈ sizes n, n.factorial / ((t 0).factorial * (t 1).factorial * (t 2).factorial) +
        (if Even n then 2 ^ (n - 2) - 1 else 2 ^ (n - 1) - 1) := by
  rw [← plateSet_eq_ridge_planes hn]; exact card_plateSet hn

end PermFaces
