/-
Lean formalization of DICTO's paper #117 (Zenodo 10.5281/zenodo.24411660). Part 4: cones and wedge angles.

The angle of a solid at a point is read from the set, as in DICTO's Dehn Canon (Palomar entry palomar-dehn):
`tcone P x` is the cone of directions that stay in `P` near `x`, `linSpace` the span of its two-way directions,
and `wedgeAngle T K` is `2π · area(T ∩ unit disc of Kᗮ) / area(unit disc of Kᗮ)`: the share of a small disc
across the line `K`. The definitions `tcone`, `linSpace`, `wedgeSet`, `wedgeAngle`, `sol`, `IsPoly`, `act`,
`cone`, `linCone` are imported from the Canon (files Dehn2Local, Dehn2Poly, Dehn2Cut), which this project
requires as a Lake dependency.

* `tcone_sol`, `local_sol`, `edge_shift`: near a point of a polytope, the polytope is its cone of directions.
* `wedge_sum`: closed convex cones invariant along `K`, covering space, with pairwise disjoint interiors, have
  wedge angles adding up to `2π` (areas add; overlaps are convex sets without interior, hence null).
* `face_angle`: a cone whose lineality space is a plane containing `K` has wedge angle `π`;
  `wedgeAngle_univ`: the whole space has `2π`.
No `sorry`.
-/
module

public import Packets.Canon.Dehn10Edges
public import Packets.Canon.Dehn7Dodeca
public import Packets.Canon.Dehn4Similar

@[expose] public section

open Set MeasureTheory Module Filter Topology
open scoped RealInnerProductSpace

namespace Packets

open DehnCanon.Library (tcone linSpace wedgeSet wedgeAngle sol act cone linCone)

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

section Poly

variable {ι : Type} {a : ι → E} {b : ι → ℝ}

lemma mem_linCone {A : Set ι} {v : E} : v ∈ linCone a A ↔ ∀ i ∈ A, ⟪a i, v⟫ = 0 := Iff.rfl

lemma cone_add {A : Set ι} {v w : E} (hv : v ∈ cone a A) (hw : w ∈ cone a A) : v + w ∈ cone a A := by
  intro i hi
  have h1 : ⟪a i, v⟫ ≤ 0 := hv i hi
  have h2 : ⟪a i, w⟫ ≤ 0 := hw i hi
  rw [inner_add_right]; linarith

lemma cone_smul {A : Set ι} {v : E} (hv : v ∈ cone a A) {s : ℝ} (hs : 0 ≤ s) : s • v ∈ cone a A := by
  intro i hi
  rw [inner_smul_right]
  exact mul_nonpos_of_nonneg_of_nonpos hs (hv i hi)

lemma linCone_subset {A : Set ι} {v : E} (hv : v ∈ linCone a A) : v ∈ cone a A :=
  fun i hi => (mem_linCone.1 hv i hi).le

lemma cone_lin {A : Set ι} {v : E} : (v ∈ cone a A ∧ -v ∈ cone a A) ↔ v ∈ linCone a A := by
  constructor
  · rintro ⟨h1, h2⟩ i hi
    have h3 : ⟪a i, v⟫ ≤ 0 := h1 i hi
    have h4 : ⟪a i, -v⟫ ≤ 0 := h2 i hi
    rw [inner_neg_right] at h4
    linarith
  · intro h
    refine ⟨linCone_subset h, linCone_subset (neg_mem h)⟩

lemma linSpace_cone (A : Set ι) : linSpace (cone a A) = linCone a A := by
  have : {v | v ∈ cone a A ∧ -v ∈ cone a A} = (linCone a A : Set E) := by
    ext v; exact cone_lin
  rw [linSpace, this, Submodule.span_eq]

lemma isClosed_cone (A : Set ι) : IsClosed (cone a A) := by
  have : cone a A = ⋂ i ∈ A, {v | ⟪a i, v⟫ ≤ 0} := by ext v; simp [cone]
  rw [this]
  exact isClosed_biInter fun i _ => isClosed_le (by fun_prop) continuous_const

lemma convex_cone (A : Set ι) : Convex ℝ (cone a A) :=
  fun _ hv _ hw _ _ hs ht _ => cone_add (cone_smul hv hs) (cone_smul hw ht)

lemma exists_small {δ : ℝ} (hδ : 0 < δ) (v : E) : ∃ t : ℝ, 0 < t ∧ ‖t • v‖ < δ := by
  refine ⟨δ / (2 * (‖v‖ + 1)), by positivity, ?_⟩
  rw [norm_smul, Real.norm_of_nonneg (by positivity), div_mul_eq_mul_div, div_lt_iff₀ (by positivity)]
  nlinarith [norm_nonneg v]

lemma inactive_near [Finite ι] (x : E) :
    ∃ δ > 0, ∀ w : E, ‖w‖ < δ → ∀ i, ⟪a i, x⟫ < b i → ⟪a i, x + w⟫ < b i := by
  have : ∀ᶠ w in 𝓝 (0 : E), ∀ i, ⟪a i, x⟫ < b i → ⟪a i, x + w⟫ < b i := by
    rw [eventually_all]
    intro i
    by_cases hi : ⟪a i, x⟫ < b i
    · have hc : Continuous fun w : E => ⟪a i, x + w⟫ := by fun_prop
      have hm := (isOpen_lt hc continuous_const).mem_nhds (show ⟪a i, x + 0⟫ < b i by simpa using hi)
      filter_upwards [hm] with w hw _ using hw
    · exact Eventually.of_forall fun w h => absurd h hi
  obtain ⟨δ, hδ, h⟩ := Metric.eventually_nhds_iff.1 this
  exact ⟨δ, hδ, fun w hw => h (by simpa using hw)⟩

/-- **Near a point of a polytope, the polytope is its cone of active constraints.** -/
lemma local_sol [Finite ι] {x : E} (hx : x ∈ sol a b) :
    ∃ δ > 0, ∀ w : E, ‖w‖ < δ → (x + w ∈ sol a b ↔ w ∈ cone a (act a b x)) := by
  obtain ⟨δ, hδ, h⟩ := inactive_near (a := a) (b := b) x
  refine ⟨δ, hδ, fun w hw => ⟨fun hs i hi => ?_, fun hc i => ?_⟩⟩
  · have h1 : ⟪a i, x + w⟫ ≤ b i := hs i
    have h2 : ⟪a i, x⟫ = b i := hi
    rw [inner_add_right, h2] at h1; linarith
  · by_cases hi : ⟪a i, x⟫ = b i
    · have h1 : ⟪a i, w⟫ ≤ 0 := hc i hi
      rw [inner_add_right, hi]; linarith
    · exact (h w hw i (lt_of_le_of_ne (hx i) hi)).le

/-- At a point of a polytope, the directions that stay inside are given by the active constraints. -/
lemma tcone_sol [Finite ι] {x : E} (hx : x ∈ sol a b) : tcone (sol a b) x = cone a (act a b x) := by
  obtain ⟨δ, hδ, h⟩ := local_sol hx
  ext v; constructor
  · rintro ⟨-, t, ht, hmem⟩ i hi
    have h1 : ⟪a i, x + t • v⟫ ≤ b i := hmem i
    have h2 : ⟪a i, x⟫ = b i := hi
    rw [inner_add_right, inner_smul_right, h2] at h1
    by_contra hpos
    have := mul_pos ht (not_le.1 hpos)
    linarith
  · intro hv
    obtain ⟨t, ht, htv⟩ := exists_small hδ v
    exact ⟨hx, t, ht, (h _ htv).2 (cone_smul hv ht.le)⟩

/-- **Sliding along an edge.** Moving a point of a polytope a little along a direction of the lineality space
of its cone keeps it in the polytope with the same active constraints. -/
lemma edge_shift [Finite ι] {x : E} (hx : x ∈ sol a b) {d : E} (hd : d ∈ linCone a (act a b x)) :
    ∃ ε > 0, ∀ s : ℝ, |s| < ε → x + s • d ∈ sol a b ∧ act a b (x + s • d) = act a b x := by
  obtain ⟨δ, hδ, h⟩ := inactive_near (a := a) (b := b) x
  refine ⟨δ / (‖d‖ + 1), by positivity, fun s hs => ?_⟩
  have hn : ‖s • d‖ < δ := by
    rw [norm_smul, Real.norm_eq_abs]
    have h1 : |s| * (‖d‖ + 1) < δ := by rwa [lt_div_iff₀ (by positivity)] at hs
    nlinarith [abs_nonneg s]
  have key : ∀ i, (⟪a i, x + s • d⟫ = b i ↔ ⟪a i, x⟫ = b i) ∧ ⟪a i, x + s • d⟫ ≤ b i := by
    intro i
    by_cases hi : ⟪a i, x⟫ = b i
    · have h0 : ⟪a i, d⟫ = 0 := mem_linCone.1 hd i hi
      rw [inner_add_right, inner_smul_right, h0, mul_zero, add_zero]
      exact ⟨Iff.rfl, hi.le⟩
    · have hlt := h _ hn i (lt_of_le_of_ne (hx i) hi)
      exact ⟨⟨fun e => absurd e hlt.ne, fun e => absurd e hi⟩, hlt.le⟩
  exact ⟨fun i => (key i).2, Set.ext fun i => (key i).1⟩

end Poly

/-! ### Wedge angles -/

section Wedge

variable [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

omit [FiniteDimensional ℝ E] in
lemma measurableSet_wedge {T : Set E} (hT : IsClosed T) (K : Submodule ℝ E) :
    MeasurableSet (wedgeSet T K) := by
  show MeasurableSet ({w : Kᗮ | (w : E) ∈ T} ∩ {w : Kᗮ | ‖w‖ < 1})
  exact (hT.measurableSet.preimage measurable_subtype_coe).inter
    (measurableSet_lt continuous_norm.measurable measurable_const)

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
lemma wedgeSet_subset_ball (T : Set E) (K : Submodule ℝ E) : wedgeSet T K ⊆ Metric.ball (0 : Kᗮ) 1 := by
  intro w hw; simpa using hw.2

lemma wedge_vol_ne_top (T : Set E) (K : Submodule ℝ E) : volume (wedgeSet T K) ≠ ⊤ :=
  ((measure_mono (wedgeSet_subset_ball T K)).trans_lt measure_ball_lt_top).ne

lemma ball_vol_toReal_ne (K : Submodule ℝ E) : (volume (Metric.ball (0 : Kᗮ) 1)).toReal ≠ 0 :=
  ENNReal.toReal_ne_zero.2 ⟨(Metric.measure_ball_pos _ _ one_pos).ne', measure_ball_lt_top.ne⟩

/-- The whole space has wedge angle `2π`. -/
lemma wedgeAngle_univ (K : Submodule ℝ E) : wedgeAngle (univ : Set E) K = 2 * Real.pi := by
  have : wedgeSet (univ : Set E) K = Metric.ball 0 1 := by ext w; simp [wedgeSet]
  rw [wedgeAngle, this, div_self (ball_vol_toReal_ne K), mul_one]

/-- **The disc is shared.** Closed convex cones `T j`, invariant along `K`, covering the space, with pairwise
disjoint interiors, have wedge angles around `K` adding up to `2π`. -/
theorem wedge_sum {κ : Type*} (J : Finset κ) (T : κ → Set E) (K : Submodule ℝ E)
    (hcl : ∀ j ∈ J, IsClosed (T j)) (hcv : ∀ j ∈ J, Convex ℝ (T j))
    (hK : ∀ j ∈ J, ∀ v ∈ T j, ∀ k ∈ K, v + k ∈ T j) (hcov : ∀ v, ∃ j ∈ J, v ∈ T j)
    (hdisj : ∀ j ∈ J, ∀ k ∈ J, j ≠ k → interior (T j ∩ T k) = ∅) :
    ∑ j ∈ J, wedgeAngle (T j) K = 2 * Real.pi := by
  have hU : (⋃ j ∈ J, wedgeSet (T j) K) = Metric.ball 0 1 := by
    ext w
    simp only [mem_iUnion, wedgeSet, mem_ofPred_eq, Metric.mem_ball, dist_zero_right, exists_prop]
    constructor
    · rintro ⟨j, -, -, h⟩; exact h
    · intro h; obtain ⟨j, hj, hv⟩ := hcov w; exact ⟨j, hj, hv, h⟩
  have hnull : ∀ j ∈ J, ∀ k ∈ J, j ≠ k → volume (wedgeSet (T j) K ∩ wedgeSet (T k) K) = 0 := by
    intro j hj k hk hjk
    set C : Set Kᗮ := Kᗮ.subtype ⁻¹' (T j ∩ T k) with hCdef
    have hC : Convex ℝ C := ((hcv j hj).inter (hcv k hk)).linear_preimage Kᗮ.subtype
    have hint : interior C = ∅ := by
      rw [← Set.not_nonempty_iff_eq_empty]
      rintro ⟨w0, hw0⟩
      let f : E → Kᗮ := fun e => ⟨e - K.starProjection e, K.sub_starProjection_mem_orthogonal e⟩
      have hf : Continuous f :=
        (continuous_id.sub K.starProjection.continuous).subtype_mk _
      have hsub : f ⁻¹' interior C ⊆ T j ∩ T k := by
        intro e he
        have hfe : ((f e : Kᗮ) : E) ∈ T j ∩ T k := (interior_subset he : f e ∈ C)
        have hk' : K.starProjection e ∈ K := K.starProjection_apply_mem e
        have he' : e = ((f e : Kᗮ) : E) + K.starProjection e := by simp [f]
        rw [he']
        exact ⟨hK j hj _ hfe.1 _ hk', hK k hk _ hfe.2 _ hk'⟩
      have hfw : f w0 = w0 := by
        apply Subtype.ext
        simp [f, (Submodule.starProjection_apply_eq_zero_iff K).2 w0.2]
      have hmem : (w0 : E) ∈ interior (T j ∩ T k) :=
        interior_maximal hsub (isOpen_interior.preimage hf) (by show f w0 ∈ interior C; rwa [hfw])
      rw [hdisj j hj k hk hjk] at hmem
      exact hmem
    have hsubC : wedgeSet (T j) K ∩ wedgeSet (T k) K ⊆ frontier C := by
      intro w hw
      rw [frontier, hint, sdiff_empty]
      exact subset_closure ⟨hw.1.1, hw.2.1⟩
    exact measure_mono_null hsubC (hC.addHaar_frontier volume)
  have hsum := measure_biUnion_finset₀ (μ := volume) (s := J) (f := fun j => wedgeSet (T j) K)
    (fun j hj k hk hjk => hnull j hj k hk hjk)
    (fun j hj => (measurableSet_wedge (hcl j hj) K).nullMeasurableSet)
  rw [hU] at hsum
  simp only [wedgeAngle]
  rw [← Finset.mul_sum, ← Finset.sum_div, ← ENNReal.toReal_sum (fun j _ => wedge_vol_ne_top (T j) K),
    ← hsum, div_self (ball_vol_toReal_ne K), mul_one]

/-- **A face has angle π.** A convex cone `T` whose two-way directions form a plane `L ⊇ K`, and which is not
`L` itself, has wedge angle `π` around `K`. -/
theorem face_angle [Fact (finrank ℝ E = 3)] {T : Set E} (hT : IsClosed T) {L K : Submodule ℝ E}
    (hadd : ∀ v ∈ T, ∀ w ∈ T, v + w ∈ T) (hsm : ∀ v ∈ T, ∀ s : ℝ, 0 ≤ s → s • v ∈ T)
    (hLT : ∀ v ∈ L, v ∈ T) (hlin : ∀ v, v ∈ T → -v ∈ T → v ∈ L) (hKL : K ≤ L)
    (hL2 : finrank ℝ L = 2) (hu : ∃ u ∈ T, u ∉ L) : wedgeAngle T K = Real.pi := by
  have h3 : finrank ℝ E = 3 := Fact.out
  have hor : ∀ w : E, w ∈ T ∨ -w ∈ T := by
    intro w
    by_cases hw : w ∈ L
    · exact Or.inl (hLT w hw)
    obtain ⟨u, huT, huL⟩ := hu
    have hw0 : w ≠ 0 := fun h => hw (h ▸ L.zero_mem)
    have hsup : L ⊔ ℝ ∙ w = ⊤ := by
      apply Submodule.eq_top_of_finrank_eq
      have h1 := Submodule.finrank_sup_add_finrank_inf_eq L (ℝ ∙ w)
      have h2 : L ⊓ ℝ ∙ w = ⊥ := by
        rw [eq_bot_iff]
        intro z hz
        obtain ⟨hzL, hzw⟩ := Submodule.mem_inf.1 hz
        obtain ⟨c, rfl⟩ := Submodule.mem_span_singleton.1 hzw
        by_cases hc : c = 0
        · simp [hc]
        · exfalso; apply hw
          have := L.smul_mem c⁻¹ hzL
          rwa [smul_smul, inv_mul_cancel₀ hc, one_smul] at this
      rw [h2, finrank_bot, finrank_span_singleton hw0, hL2] at h1
      omega
    have hu' : u ∈ L ⊔ ℝ ∙ w := hsup ▸ Submodule.mem_top
    obtain ⟨l, hl, m, hm, rfl⟩ := Submodule.mem_sup.1 hu'
    obtain ⟨c, rfl⟩ := Submodule.mem_span_singleton.1 hm
    have hc : c ≠ 0 := by rintro rfl; apply huL; simpa using hl
    have hcw : c • w ∈ T := by
      have := hadd _ huT _ (hLT _ (L.neg_mem hl)); simpa using this
    rcases lt_or_gt_of_ne hc with hneg | hpos
    · right
      have := hsm _ hcw (-c)⁻¹ (inv_nonneg.2 (by linarith))
      rwa [smul_smul, show (-c)⁻¹ * c = -1 by field_simp, neg_one_smul] at this
    · left
      have := hsm _ hcw c⁻¹ (inv_nonneg.2 hpos.le)
      rwa [smul_smul, inv_mul_cancel₀ hc, one_smul] at this
  have hLtop : L ≠ ⊤ := by
    intro h; rw [h, finrank_top] at hL2; omega
  set N : Submodule ℝ Kᗮ := L.comap Kᗮ.subtype
  have hN : N ≠ ⊤ := by
    intro h; apply hLtop
    rw [eq_top_iff]
    intro e _
    have hp : K.starProjection e ∈ L := hKL (K.starProjection_apply_mem e)
    have hq : (⟨e - K.starProjection e, K.sub_starProjection_mem_orthogonal e⟩ : Kᗮ) ∈ N :=
      h ▸ Submodule.mem_top
    have hq' : e - K.starProjection e ∈ L := hq
    simpa using L.add_mem hq' hp
  set W := wedgeSet T K
  have hW : MeasurableSet W := measurableSet_wedge hT K
  have hnull : volume (W ∩ -W) = 0 := by
    refine measure_mono_null ?_ (Measure.addHaar_submodule volume N hN)
    rintro w ⟨h1, h2⟩
    show (w : E) ∈ L
    exact hlin _ h1.1 (by simpa [W, wedgeSet] using h2.1)
  have hunion : W ∪ -W = Metric.ball 0 1 := by
    ext w
    simp only [W, wedgeSet, mem_union, Set.mem_neg, mem_ofPred_eq, Metric.mem_ball, dist_zero_right,
      Submodule.coe_neg, norm_neg]
    constructor
    · rintro (h | h) <;> exact h.2
    · intro h; rcases hor w with h' | h'
      · exact Or.inl ⟨h', h⟩
      · exact Or.inr ⟨h', h⟩
  have hneg : volume (-W) = volume W := Measure.measure_neg volume W
  have hm := measure_union₀ (μ := volume) (s := W) (t := -W) hW.neg.nullMeasurableSet hnull
  rw [hunion, hneg] at hm
  have hD : (volume (Metric.ball (0 : Kᗮ) 1)).toReal = 2 * (volume W).toReal := by
    rw [hm, ENNReal.toReal_add (wedge_vol_ne_top T K) (wedge_vol_ne_top T K)]; ring
  have hD0 := ball_vol_toReal_ne K
  rw [hD] at hD0
  have hW0 : (volume W).toReal ≠ 0 := right_ne_zero_of_mul hD0
  rw [wedgeAngle, hD]
  change 2 * Real.pi * ((volume W).toReal / (2 * (volume W).toReal)) = Real.pi
  field_simp

end Wedge

end Packets
