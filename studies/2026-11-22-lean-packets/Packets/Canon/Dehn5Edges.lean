/-
Lean study 5 of the shape-language canon (DICTO, 19 Nov 2026), part P: reading the edges of a convex solid
that is not a tetrahedron.

`IsEdgeData n b p fi fj vk vl`: a bounded solid `sol n b` (faces `m`, half-spaces `⟪n m, x⟫ ≤ b m`), its
corners `p k`, and a list of edges `e`: the edge `e` lies on the two faces `fi e`, `fj e` and joins the corners
`p (vk e)`, `p (vl e)`. The fields are finitely many facts about the corner-face table, and one fact about the
points of the solid, `cover`: a point of the solid on two different faces lies on the closed segment of an edge
with these two faces, or is a corner.

* `mem_segment_of_tight`: how `cover` is proved for the two faces of an edge. A third face `c` through the
  second corner only, with the three normals independent, gives the position along the line of the two faces;
  a fourth face `c'` through the first corner only bounds it on the other side.
* `eq_of_tight`: how `cover` is proved for two faces that share only a corner `P`: if two more faces `c`, `c'`
  through `P` satisfy `n c + μ n c' = a n i + a' n j` with `μ > 0`, the only point of the solid on the faces
  `i` and `j` is `P`.
* `IsEdgeData.faceSet_edge`: the points of the solid where exactly the two faces of an edge are tight are the
  open segment between its two corners.
* `IsEdgeData.faceSet_subset_corners`: any other set of faces whose common direction space is a line is tight
  only at corners (no other wedge points).
* `IsEdgeData.dehnSet_eq` (**the edge reading**): `dehnSet (sol n b)` = Σ over the edges of
  (distance of the two corners) ⊗ (angle class of the cone of the two faces).

The solid is not assumed simple: any number of faces may meet at a corner, and three faces with dependent
normals are allowed (in FUJI: two opposite side faces and the hexagon).

Why not a generalisation of study 4's `IsTetraData`: that structure rests on barycentric coordinates, one face
per corner, which only a simplex has. Here the same job is done edge by edge with one-dimensional coordinates
along each edge. A tetrahedron also satisfies `IsEdgeData`; study 4's lemma is kept as it is.

Credits: Mathlib `mem_openSegment_of_ne_left_right`, `Set.Finite.measure_zero`, `Finset.sum_subset`,
`Finset.sum_image`; study 2's `dehnSet_eq_dehn_edgeList` (through `dehnSet_eq_sum_faceSet`), study 3's
`finrank_linCone_ne_one_of_subsingleton`, study 4's `hausdorff_openSegment`.
No `sorry`.
-/
module

public import Packets.Canon.Dehn5Angles

@[expose] public section

open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct

namespace DehnCanon.Library

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

section tight

variable {ι : Type} {n : ι → E} {b : ι → ℝ}

/-- **A point of the solid on the two faces of an edge lies on the edge.** `P`, `Q` are the two corners of the
edge of the faces `i`, `j`. The face `c` passes through `Q` and not through `P`, the face `c'` through `P` and
not through `Q`, and the normals of `i`, `j`, `c` have no common perpendicular direction. -/
lemma mem_segment_of_tight {P Q : E} {i j c c' : ι}
    (hind : ∀ v : E, ⟪n i, v⟫ = 0 → ⟪n j, v⟫ = 0 → ⟪n c, v⟫ = 0 → v = 0)
    (hiP : ⟪n i, P⟫ = b i) (hiQ : ⟪n i, Q⟫ = b i) (hjP : ⟪n j, P⟫ = b j) (hjQ : ⟪n j, Q⟫ = b j)
    (hcQ : ⟪n c, Q⟫ = b c) (hcP : ⟪n c, P⟫ < b c) (hc'P : ⟪n c', P⟫ = b c') (hc'Q : ⟪n c', Q⟫ < b c')
    {x : E} (hx : x ∈ sol n b) (hi : ⟪n i, x⟫ = b i) (hj : ⟪n j, x⟫ = b j) :
    x ∈ segment ℝ P Q := by
  have hd : 0 < b c - ⟪n c, P⟫ := sub_pos.2 hcP
  obtain ⟨t, ht⟩ : ∃ t : ℝ, t = (b c - ⟪n c, x⟫) / (b c - ⟪n c, P⟫) := ⟨_, rfl⟩
  have ht0 : 0 ≤ t := by rw [ht]; exact div_nonneg (sub_nonneg.2 (hx c)) hd.le
  have htd : t * (b c - ⟪n c, P⟫) = b c - ⟪n c, x⟫ := by rw [ht]; exact div_mul_cancel₀ _ hd.ne'
  have hxy : x - (t • P + (1 - t) • Q) = 0 := by
    apply hind
    · rw [inner_sub_right, inner_add_right, inner_smul_right, inner_smul_right, hi, hiP, hiQ]; ring
    · rw [inner_sub_right, inner_add_right, inner_smul_right, inner_smul_right, hj, hjP, hjQ]; ring
    · rw [inner_sub_right, inner_add_right, inner_smul_right, inner_smul_right, hcQ]
      linear_combination htd
  have hxy' : x = t • P + (1 - t) • Q := sub_eq_zero.1 hxy
  have h1 : 0 ≤ 1 - t := by
    have h2 : ⟪n c', t • P + (1 - t) • Q⟫ ≤ b c' := hxy' ▸ hx c'
    rw [inner_add_right, inner_smul_right, inner_smul_right, hc'P] at h2
    by_contra hneg
    push Not at hneg
    nlinarith [mul_pos_of_neg_of_neg hneg (sub_neg.2 hc'Q)]
  exact ⟨t, 1 - t, ht0, h1, by ring, hxy'.symm⟩

/-- **Two faces that share only a corner.** `P` lies on the faces `i`, `j`, `c`, `c'`; the normals of
`i`, `j`, `c` have no common perpendicular direction; and `n c + μ n c' = a n i + a' n j` with `μ > 0`.
Then `P` is the only point of the solid on both faces `i` and `j`. -/
lemma eq_of_tight {P : E} {i j c c' : ι}
    (hind : ∀ v : E, ⟪n i, v⟫ = 0 → ⟪n j, v⟫ = 0 → ⟪n c, v⟫ = 0 → v = 0)
    (hcP : ⟪n c, P⟫ = b c) (hc'P : ⟪n c', P⟫ = b c') (hiP : ⟪n i, P⟫ = b i) (hjP : ⟪n j, P⟫ = b j)
    {μ a a' : ℝ} (hμ : 0 < μ) (hrel : n c + μ • n c' = a • n i + a' • n j)
    {x : E} (hx : x ∈ sol n b) (hi : ⟪n i, x⟫ = b i) (hj : ⟪n j, x⟫ = b j) : x = P := by
  rw [← sub_eq_zero]
  have hi0 : ⟪n i, x - P⟫ = 0 := by rw [inner_sub_right, hi, hiP, sub_self]
  have hj0 : ⟪n j, x - P⟫ = 0 := by rw [inner_sub_right, hj, hjP, sub_self]
  have hc0 : ⟪n c, x - P⟫ ≤ 0 := by rw [inner_sub_right, hcP]; exact sub_nonpos.2 (hx c)
  have hc'0 : ⟪n c', x - P⟫ ≤ 0 := by rw [inner_sub_right, hc'P]; exact sub_nonpos.2 (hx c')
  have h := congrArg (fun w => ⟪w, x - P⟫) hrel
  simp only [inner_add_left, real_inner_smul_left] at h
  rw [hi0, hj0] at h
  have h2 : μ * ⟪n c', x - P⟫ ≤ 0 := mul_nonpos_of_nonneg_of_nonpos hμ.le hc'0
  exact hind _ hi0 hj0 (le_antisymm hc0 (by linarith))

end tight

/-- The data of a bounded convex solid with its corners and edges: faces `m` with outward normals `n m` and
offsets `b m`, corners `p k`, and for each edge `e` its two faces `fi e`, `fj e` and its two corners
`p (vk e)`, `p (vl e)`. -/
structure IsEdgeData {ι κ ε : Type} (n : ι → E) (b : ι → ℝ) (p : κ → E) (fi fj : ε → ι) (vk vl : ε → κ) :
    Prop where
  /-- The solid is bounded. -/
  bounded : Bornology.IsBounded (sol n b)
  /-- The corners are points of the solid. -/
  corner_mem : ∀ k, p k ∈ sol n b
  /-- At least three faces pass through every corner. -/
  corner_three : ∀ k, ∃ m₁ m₂ m₃, m₁ ≠ m₂ ∧ m₁ ≠ m₃ ∧ m₂ ≠ m₃ ∧
    ⟪n m₁, p k⟫ = b m₁ ∧ ⟪n m₂, p k⟫ = b m₂ ∧ ⟪n m₃, p k⟫ = b m₃
  /-- The two faces of an edge are different. -/
  faces_ne : ∀ e, fi e ≠ fj e
  /-- Different edges have different pairs of faces. -/
  faces_inj : ∀ e e', ({fi e, fj e} : Set ι) = {fi e', fj e'} → e = e'
  /-- The two corners of an edge lie on its two faces. -/
  tight : ∀ e, ⟪n (fi e), p (vk e)⟫ = b (fi e) ∧ ⟪n (fi e), p (vl e)⟫ = b (fi e) ∧
    ⟪n (fj e), p (vk e)⟫ = b (fj e) ∧ ⟪n (fj e), p (vl e)⟫ = b (fj e)
  /-- Every other face misses one of the two corners of the edge. -/
  other : ∀ e m, m ≠ fi e → m ≠ fj e → ⟪n m, p (vk e)⟫ < b m ∨ ⟪n m, p (vl e)⟫ < b m
  /-- A point of the solid on two different faces lies on the closed segment of an edge with these two faces,
  or is a corner. -/
  cover : ∀ x ∈ sol n b, ∀ i j, i ≠ j → ⟪n i, x⟫ = b i → ⟪n j, x⟫ = b j →
    (∃ e, ({i, j} : Set ι) = {fi e, fj e} ∧ x ∈ segment ℝ (p (vk e)) (p (vl e))) ∨ ∃ k, x = p k

namespace IsEdgeData

variable {ι κ ε : Type} {n : ι → E} {b : ι → ℝ} {p : κ → E} {fi fj : ε → ι} {vk vl : ε → κ}

/-- At a corner the set of tight faces is not a pair. -/
lemma act_corner_ne_pair (h : IsEdgeData n b p fi fj vk vl) (k : κ) (i j : ι) :
    act n b (p k) ≠ {i, j} := by
  obtain ⟨m₁, m₂, m₃, h12, h13, h23, t1, t2, t3⟩ := h.corner_three k
  intro hA
  have a1 : m₁ ∈ ({i, j} : Set ι) := hA ▸ (show m₁ ∈ act n b (p k) from t1)
  have a2 : m₂ ∈ ({i, j} : Set ι) := hA ▸ (show m₂ ∈ act n b (p k) from t2)
  have a3 : m₃ ∈ ({i, j} : Set ι) := hA ▸ (show m₃ ∈ act n b (p k) from t3)
  rw [mem_insert_iff, mem_singleton_iff] at a1 a2 a3
  rcases a1 with a1 | a1 <;> rcases a2 with a2 | a2 <;> rcases a3 with a3 | a3
  · exact h12 (a1.trans a2.symm)
  · exact h12 (a1.trans a2.symm)
  · exact h13 (a1.trans a3.symm)
  · exact h23 (a2.trans a3.symm)
  · exact h23 (a2.trans a3.symm)
  · exact h13 (a1.trans a3.symm)
  · exact h12 (a1.trans a2.symm)
  · exact h12 (a1.trans a2.symm)

/-- The two corners of an edge are different points. -/
lemma corner_ne (h : IsEdgeData n b p fi fj vk vl) (e : ε) : p (vk e) ≠ p (vl e) := by
  intro heq
  apply h.act_corner_ne_pair (vk e) (fi e) (fj e)
  ext m
  constructor
  · intro hm
    have hm' : ⟪n m, p (vk e)⟫ = b m := hm
    by_contra hno
    rw [mem_insert_iff, mem_singleton_iff, not_or] at hno
    rcases h.other e m hno.1 hno.2 with h1 | h1
    · exact h1.ne hm'
    · rw [← heq] at h1; exact h1.ne hm'
  · rintro (rfl | rfl)
    · exact (h.tight e).1
    · exact (h.tight e).2.2.1

/-- **The edges**: the points of the solid where exactly the two faces of the edge `e` are tight are the points
of the open segment between its two corners. -/
theorem faceSet_edge (h : IsEdgeData n b p fi fj vk vl) (e : ε) :
    faceSet n b {fi e, fj e} = openSegment ℝ (p (vk e)) (p (vl e)) := by
  obtain ⟨tik, til, tjk, tjl⟩ := h.tight e
  apply Subset.antisymm
  · rintro x ⟨hx, hA⟩
    have hi : ⟪n (fi e), x⟫ = b (fi e) :=
      show fi e ∈ act n b x from hA ▸ mem_insert _ _
    have hj : ⟪n (fj e), x⟫ = b (fj e) :=
      show fj e ∈ act n b x from hA ▸ mem_insert_of_mem _ rfl
    rcases h.cover x hx _ _ (h.faces_ne e) hi hj with ⟨e', he', hseg⟩ | ⟨k, rfl⟩
    · obtain rfl := h.faces_inj e e' he'
      refine mem_openSegment_of_ne_left_right (fun hP => ?_) (fun hQ => ?_) hseg
      · exact h.act_corner_ne_pair (vk e) _ _ (by rw [hP]; exact hA)
      · exact h.act_corner_ne_pair (vl e) _ _ (by rw [hQ]; exact hA)
    · exact absurd hA (h.act_corner_ne_pair k _ _)
  · rintro _ ⟨α, β, hα, hβ, hab, rfl⟩
    refine ⟨convex_sol n b (h.corner_mem _) (h.corner_mem _) hα.le hβ.le hab, ?_⟩
    ext m
    show ⟪n m, α • p (vk e) + β • p (vl e)⟫ = b m ↔ m ∈ ({fi e, fj e} : Set ι)
    rw [inner_add_right, inner_smul_right, inner_smul_right, mem_insert_iff, mem_singleton_iff]
    constructor
    · intro hm
      by_contra hno
      rw [not_or] at hno
      have hP : ⟪n m, p (vk e)⟫ ≤ b m := h.corner_mem (vk e) m
      have hQ : ⟪n m, p (vl e)⟫ ≤ b m := h.corner_mem (vl e) m
      have e1 : α * (b m - ⟪n m, p (vk e)⟫) + β * (b m - ⟪n m, p (vl e)⟫) = 0 := by
        linear_combination (b m) * hab - hm
      rcases h.other e m hno.1 hno.2 with h1 | h1
      · nlinarith [mul_pos hα (sub_pos.2 h1), mul_nonneg hβ.le (sub_nonneg.2 hQ)]
      · nlinarith [mul_pos hβ (sub_pos.2 h1), mul_nonneg hα.le (sub_nonneg.2 hP)]
    · rintro (rfl | rfl)
      · rw [tik, til]; linear_combination (b (fi e)) * hab
      · rw [tjk, tjl]; linear_combination (b (fj e)) * hab

variable [FiniteDimensional ℝ E] [Fact (finrank ℝ E = 3)]

/-- **No other wedge points**: a set of faces whose common direction space is a line, and which is not the pair
of faces of an edge, is tight only at corners. -/
theorem faceSet_subset_corners [Nonempty ι] (h : IsEdgeData n b p fi fj vk vl) {A : Set ι}
    (hfin : finrank ℝ (linCone n A) = 1) (hA : ∀ e, A ≠ {fi e, fj e}) :
    faceSet n b A ⊆ Set.range p := by
  rintro x ⟨hx, hact⟩
  obtain ⟨i, hi, j, hj, hij⟩ : ∃ i ∈ A, ∃ j ∈ A, i ≠ j := by
    by_contra hno
    push Not at hno
    rcases A.eq_empty_or_nonempty with he | ⟨i, hi⟩
    · exact finrank_linCone_ne_one_of_subsingleton n (i := Classical.arbitrary ι)
        (by rw [he]; exact empty_subset _) hfin
    · exact finrank_linCone_ne_one_of_subsingleton n (i := i) (fun j hj => (hno i hi j hj).symm) hfin
  have hi' : ⟪n i, x⟫ = b i := show i ∈ act n b x from hact ▸ hi
  have hj' : ⟪n j, x⟫ = b j := show j ∈ act n b x from hact ▸ hj
  rcases h.cover x hx i j hij hi' hj' with ⟨e, -, hseg⟩ | ⟨k, rfl⟩
  · by_cases hP : p (vk e) = x
    · exact ⟨_, hP⟩
    by_cases hQ : p (vl e) = x
    · exact ⟨_, hQ⟩
    exfalso
    have hopen : x ∈ faceSet n b {fi e, fj e} := by
      rw [h.faceSet_edge e]; exact mem_openSegment_of_ne_left_right hP hQ hseg
    exact hA e (hact.symm.trans hopen.2)
  · exact ⟨k, rfl⟩

variable [MeasurableSpace E] [BorelSpace E]

/-- **The edge reading.** The Dehn invariant of the solid is the sum over its edges of
(distance of the two corners of the edge) ⊗ (angle class of the cone of the two faces through the edge). -/
theorem dehnSet_eq [Fintype ι] [Nonempty ι] [Finite κ] [Fintype ε] (h : IsEdgeData n b p fi fj vk vl) :
    dehnSet (sol n b) =
      ∑ e, dist (p (vk e)) (p (vl e)) ⊗ₜ[ℚ] theta (cone n ({fi e, fj e} : Set ι)) := by
  classical
  let F : ε → Set ι := fun e => {fi e, fj e}
  have hinj : Function.Injective F := fun e e' he => h.faces_inj e e' he
  have hzero : ∀ A ∈ (Finset.univ : Finset (Set ι)), A ∉ Finset.univ.image F →
      (μH[1] (faceSet n b A)).toReal ⊗ₜ[ℚ] theta (cone n A) = 0 := by
    intro A _ hA
    by_cases hfin : finrank ℝ (linCone n A) = 1
    · have hsub := h.faceSet_subset_corners hfin
        (fun e he => hA (Finset.mem_image.2 ⟨e, Finset.mem_univ _, he.symm⟩))
      have hnull : μH[1] (Set.range p) = 0 := by
        have := nullSingletonClass_hausdorff E (d := 1) one_pos
        exact (Set.finite_range p).measure_zero _
      rw [measure_mono_null hsub hnull, ENNReal.toReal_zero, TensorProduct.zero_tmul]
    · unfold theta; rw [linSpace_cone, ite_eq_right hfin, TensorProduct.tmul_zero]
  rw [dehnSet_eq_sum_faceSet n b h.bounded,
    ← Finset.sum_subset (Finset.subset_univ (Finset.univ.image F)) hzero,
    Finset.sum_image (fun e _ e' _ he => hinj he)]
  apply Finset.sum_congr rfl
  intro e _
  show (μH[1] (faceSet n b {fi e, fj e})).toReal ⊗ₜ[ℚ] _ = _
  rw [h.faceSet_edge e, hausdorff_openSegment (h.corner_ne e)]

end IsEdgeData

end DehnCanon.Library
