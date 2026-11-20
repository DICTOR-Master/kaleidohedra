/-
Dehn–Hadwiger study, part 2: the hyperplane-cut identity in any dimension (DICTO, 20 Nov 2026).

`dehnHadwiger_cut`: for a convex polytope `P` in a finite-dimensional real inner product space and any hyperplane,
the Dehn–Hadwiger invariant of `P` is the sum of the invariants of the two parts. (An old ridge inside the
hyperplane: its angle splits in two. A new ridge inside a facet or inside the solid: its two angles sum to π or
2π, zero in ℝ/ℚπ. An old ridge crossing the hyperplane meets it in a set of one dimension less, of measure zero.)
The proof is the Canon's 3D proof (`DehnCanon.dehnSet_cut`) with lines replaced by codimension-2 subspaces;
the sign classifier `cls`, the tangent cones of `sol` and the sum `tsum1` are the Canon's, reused unchanged.
No `sorry`.
-/
import DehnHadwiger.DH1Def
import DehnCanon.Dehn2Cut

open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct DehnCanon

namespace DehnHadwiger

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E] {ι : Type}

lemma ridgeAngle_sol [Finite ι] (a : ι → E) (b : ι → ℝ) {x : E} (hx : x ∈ sol a b) :
    ridgeAngle (sol a b) x = thetaH (cone a (act a b x)) := by
  unfold ridgeAngle; rw [tcone_sol a b hx]

/-- **The angle class at a point under a hyperplane cut**: additive, except where a ridge crosses it. -/
lemma ridgeAngle_cut [Finite ι] (a : ι → E) (b : ι → ℝ) {c : E} (hc : c ≠ 0)
    (d : ℝ) (x : E)
    (hexc : ¬ (x ∈ sol a b ∧ ⟪c, x⟫ = d ∧ finrank ℝ (linCone a (act a b x)) + 2 = finrank ℝ E ∧
      ¬ linCone a (act a b x) ≤ (ℝ ∙ c)ᗮ)) :
    ridgeAngle (sol a b) x = ridgeAngle (sol a b ∩ hsLe c d) x + ridgeAngle (sol a b ∩ hsGe c d) x := by
  by_cases hx : x ∈ sol a b
  · rcases lt_trichotomy ⟪c, x⟫ d with hlt | heq | hgt
    · have h1 : x ∉ sol a b ∩ hsGe c d := fun h => by
        have := mem_hsGe.1 h.2; linarith
      rw [ridgeAngle_of_notMem h1, add_zero]
      unfold ridgeAngle
      rw [tcone_sol a b hx, tcone_cut_lt a b hx hlt]
    · have heq' : ⟪-c, x⟫ = -d := by rw [inner_neg_left, heq]
      have h2 : tcone (sol a b ∩ hsGe c d) x = cone a (act a b x) ∩ {v | ⟪-c, v⟫ ≤ 0} :=
        tcone_cut_eq a b hx heq'
      unfold ridgeAngle
      rw [tcone_sol a b hx, tcone_cut_eq a b hx heq, h2]
      exact thetaH_cut (cone_lin a _) (cone_add a _) (cone_smul a _) hc
        (fun h => hexc ⟨hx, heq, h.1, h.2⟩)
    · have h1 : x ∉ sol a b ∩ hsLe c d := fun h => by
        have := mem_hsLe.1 h.2; linarith
      have hlt' : ⟪-c, x⟫ < -d := by rw [inner_neg_left]; linarith
      have h2 : tcone (sol a b ∩ hsGe c d) x = cone a (act a b x) := tcone_cut_lt a b hx hlt'
      rw [ridgeAngle_of_notMem h1, zero_add]
      unfold ridgeAngle
      rw [tcone_sol a b hx, h2]
  · rw [ridgeAngle_of_notMem hx, ridgeAngle_of_notMem (fun h => hx h.1),
      ridgeAngle_of_notMem (fun h => hx h.1), add_zero]

lemma ridgeAngle_sol_congr [Finite ι] (a : ι → E) (b : ι → ℝ) {x y : E}
    (hmem : x ∈ sol a b ↔ y ∈ sol a b) (hact : act a b x = act a b y) :
    ridgeAngle (sol a b) x = ridgeAngle (sol a b) y := by
  by_cases hx : x ∈ sol a b
  · rw [ridgeAngle_sol a b hx, ridgeAngle_sol a b (hmem.1 hx), hact]
  · rw [ridgeAngle_of_notMem hx, ridgeAngle_of_notMem (fun h => hx (hmem.2 h))]

lemma ridgeAngle_cut_congr [Finite ι] (a : ι → E) (b : ι → ℝ) (c : E) (d : ℝ) {x y : E}
    (hmem : x ∈ sol a b ↔ y ∈ sol a b) (hact : act a b x = act a b y)
    (hle : ⟪c, x⟫ ≤ d ↔ ⟪c, y⟫ ≤ d) (heq : ⟪c, x⟫ = d ↔ ⟪c, y⟫ = d) :
    ridgeAngle (sol a b ∩ hsLe c d) x = ridgeAngle (sol a b ∩ hsLe c d) y := by
  rw [sol_inter_hsLe]
  apply ridgeAngle_sol_congr
  · rw [← sol_inter_hsLe]
    exact and_congr hmem hle
  · ext o
    cases o with
    | none => exact heq
    | some i => exact Set.ext_iff.1 hact i

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
lemma mem_linCone_of_act {a : ι → E} {b : ι → ℝ} {A : Set ι} {x y : E} (hx : act a b x = A)
    (hy : act a b y = A) : x - y ∈ linCone a A := by
  intro i hi
  have e1 : ⟪a i, x⟫ = b i := by
    have : i ∈ act a b x := by rw [hx]; exact hi
    exact this
  have e2 : ⟪a i, y⟫ = b i := by
    have : i ∈ act a b y := by rw [hy]; exact hi
    exact this
  rw [inner_sub_right, e1, e2, sub_self]

/-- The ridge points of a bounded polytope have finite total `(n-2)`-dimensional measure. -/
lemma support_finite [Finite ι] (a : ι → E) (b : ι → ℝ) (hb : Bornology.IsBounded (sol a b)) :
    μH[(finrank ℝ E - 2 : ℕ)] {x | ridgeAngle (sol a b) x ≠ 0} ≠ ⊤ := by
  classical
  let R : Set ι → Set E := fun A => {x | x ∈ sol a b ∧ act a b x = A ∧
    finrank ℝ (linCone a A) + 2 = finrank ℝ E}
  have hsub : {x | ridgeAngle (sol a b) x ≠ 0} ⊆ ⋃ A ∈ (Set.univ : Set (Set ι)), R A := by
    intro x hx
    have hx0 : ridgeAngle (sol a b) x ≠ 0 := hx
    have hxs : x ∈ sol a b := by
      by_contra hno; exact hx0 (ridgeAngle_of_notMem hno)
    rw [ridgeAngle_sol a b hxs] at hx0
    have hfr : finrank ℝ (linCone a (act a b x)) + 2 = finrank ℝ E := by
      by_contra hno
      apply hx0
      unfold thetaH
      rw [linSpace_cone, ite_eq_right hno]
    exact mem_biUnion (mem_univ (act a b x)) ⟨hxs, rfl, hfr⟩
  have hR : ∀ A ∈ (Set.univ : Set (Set ι)), μH[(finrank ℝ E - 2 : ℕ)] (R A) < ⊤ := by
    intro A _
    rcases (R A).eq_empty_or_nonempty with he | ⟨x0, hx0s, hx0A, hfr⟩
    · rw [he, measure_empty]; exact ENNReal.zero_lt_top
    · have hm : finrank ℝ E - 2 = finrank ℝ (linCone a A) := by omega
      rw [hm]
      refine lt_top_iff_ne_top.2 (hausdorff_affine_ne_top (linCone a A) x0
        (hb.subset fun x hx => hx.1) ?_)
      rintro x ⟨-, hxA, -⟩
      exact mem_linCone_of_act hxA hx0A
  exact ((measure_mono hsub).trans_lt (measure_biUnion_lt_top Set.finite_univ hR)).ne

/-- The points where a ridge crosses the cutting hyperplane have measure zero. -/
lemma exc_null [Finite ι] (a : ι → E) (b : ι → ℝ) (c : E) (d : ℝ) :
    μH[(finrank ℝ E - 2 : ℕ)] {x | x ∈ sol a b ∧ ⟪c, x⟫ = d ∧
      finrank ℝ (linCone a (act a b x)) + 2 = finrank ℝ E ∧
      ¬ linCone a (act a b x) ≤ (ℝ ∙ c)ᗮ} = 0 := by
  classical
  let Xs : Set ι → Set E := fun A => {x | act a b x = A ∧ ⟪c, x⟫ = d ∧
    finrank ℝ (linCone a A) + 2 = finrank ℝ E ∧ ¬ linCone a A ≤ (ℝ ∙ c)ᗮ}
  have hsub : {x | x ∈ sol a b ∧ ⟪c, x⟫ = d ∧ finrank ℝ (linCone a (act a b x)) + 2 = finrank ℝ E ∧
      ¬ linCone a (act a b x) ≤ (ℝ ∙ c)ᗮ} ⊆ ⋃ A, Xs A := by
    rintro x ⟨-, h2, h3, h4⟩
    exact mem_iUnion.2 ⟨act a b x, rfl, h2, h3, h4⟩
  have hXs : ∀ A, μH[(finrank ℝ E - 2 : ℕ)] (Xs A) = 0 := by
    intro A
    rcases (Xs A).eq_empty_or_nonempty with he | ⟨x0, hx0A, hx0d, hfr, hnot⟩
    · rw [he, measure_empty]
    · set W : Submodule ℝ E := linCone a A ⊓ (ℝ ∙ c)ᗮ
      have hlt : W < linCone a A := lt_of_le_of_ne inf_le_left (fun h => hnot (h ▸ inf_le_right))
      have hW : finrank ℝ W < finrank ℝ E - 2 := by
        have := Submodule.finrank_lt_finrank_of_lt hlt; omega
      apply hausdorff_affine_null W x0 _ hW
      rintro x ⟨hxA, hxd, -, -⟩
      refine Submodule.mem_inf.2 ⟨mem_linCone_of_act hxA hx0A, ?_⟩
      rw [Submodule.mem_orthogonal_singleton_iff_inner_right, inner_sub_right, hxd, hx0d, sub_self]
  exact measure_mono_null hsub (measure_iUnion_null_iff.2 hXs)

/-- **The cut identity.** For a convex polytope `P` and the hyperplane `⟪c, x⟫ = d`, `c ≠ 0`:
`dehnHadwiger P = dehnHadwiger (P ∩ {⟪c,x⟫ ≤ d}) + dehnHadwiger (P ∩ {⟪c,x⟫ ≥ d})`. -/
theorem dehnHadwiger_cut {P : Set E} (hP : IsPoly P) (c : E) (d : ℝ) (hc : c ≠ 0) :
    dehnHadwiger P = dehnHadwiger (P ∩ hsLe c d) + dehnHadwiger (P ∩ hsGe c d) := by
  classical
  obtain ⟨hb, ι, _, a, b, rfl⟩ := hP
  show tsum1 μH[(finrank ℝ E - 2 : ℕ)] (ridgeAngle (sol a b)) =
    tsum1 μH[(finrank ℝ E - 2 : ℕ)] (ridgeAngle (sol a b ∩ hsLe c d)) +
      tsum1 μH[(finrank ℝ E - 2 : ℕ)] (ridgeAngle (sol a b ∩ hsGe c d))
  apply tsum1_add _ (cls a b c d) (cls_meas a b c d)
  · intro x y hxy
    obtain ⟨h1, h2, h3, h4, -⟩ := cls_facts a b c d hxy
    exact ridgeAngle_cut_congr a b c d h1 h2 h3 h4
  · intro x y hxy
    obtain ⟨h1, h2, -, h4, h5⟩ := cls_facts a b c d hxy
    refine ridgeAngle_cut_congr a b (-c) (-d) h1 h2 ?_ ?_
    · rw [inner_neg_left, inner_neg_left, neg_le_neg_iff, neg_le_neg_iff]; exact h5
    · rw [inner_neg_left, inner_neg_left, neg_inj, neg_inj]; exact h4
  · rw [sol_inter_hsLe]
    apply support_finite
    rw [← sol_inter_hsLe]; exact hb.subset inter_subset_left
  · show μH[(finrank ℝ E - 2 : ℕ)] {x | ridgeAngle (sol a b ∩ hsLe (-c) (-d)) x ≠ 0} ≠ ⊤
    rw [sol_inter_hsLe]
    apply support_finite
    rw [← sol_inter_hsLe]; exact hb.subset inter_subset_left
  · refine measure_mono_null ?_ (exc_null a b c d)
    intro x hx
    by_contra hno
    exact hx (ridgeAngle_cut a b hc d x hno)

end DehnHadwiger
