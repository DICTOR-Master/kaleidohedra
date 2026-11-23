/-
Lean formalization of DICTO's paper #117 (Zenodo 10.5281/zenodo.24411660). Part 5: Lemma 2 and the
unconditional Theorem 4 (a), (b).

* `ConvexTiling`: a tiling of space by convex polytopes (bounded intersections of finitely many closed
  half-spaces) with interior points, covering space, with pairwise disjoint interiors, finitely many meeting
  some neighbourhood of each point. Nothing is assumed about how the tiles meet (face-to-face or not).
* `lemma2`: **Lemma 2 of the paper (angles round an edge).** At an edge point `x` of a tile `i` (a point where
  the two-way directions of the tile form a line `K`) there is a point `y` of the same edge, with the same cone
  for tile `i`, such that the tiles containing `y` are finitely many and their angles around `K` add up to `2π`;
  each of these angles is the tile's dihedral angle at an edge point, or `π` (the point lies inside a face of
  that tile), or `2π`. Angles are read from the sets (`wedgeAngle` of `tcone`: the share of a small disc across
  the edge), as in DICTO's Dehn Canon.
* `EdgeAngle P θ`: `θ` is a dihedral angle of the polytope `P`, read from the set at an edge point.
* `localAngleCondition_of_tiling`, and **Theorem 4 (a), (b) for tilings**: `theorem4a_tiling`,
  `theorem4b_tiling`.

Proof of Lemma 2: the point `y` is chosen on the edge away from the at most two end points, on that line, of
each of the finitely many tiles near `x`; then every tile containing `y` contains a segment of the edge line
through `y`, so its cone at `y` is invariant along `K`. Near `y` each tile is its cone (`local_sol`); the cones
cover space (the tiles cover a neighbourhood of `y`) and have pairwise disjoint interiors (the tiles do), so
`wedge_sum` gives `2π`. A cone whose two-way directions form a plane is a half-space: angle `π` (`face_angle`).
No `sorry`.
-/
module

public import Packets.Cones
public import Packets.Tiling

@[expose] public section

open Set MeasureTheory Module Filter Topology
open scoped RealInnerProductSpace

namespace Packets

open DehnCanon.Library (tcone linSpace wedgeSet wedgeAngle sol act cone linCone)

/-- **A tiling of space by convex polytopes.** -/
structure ConvexTiling (ι : Type*) (E : Type*) [NormedAddCommGroup E] [InnerProductSpace ℝ E] where
  /-- The tiles. -/
  P : ι → Set E
  poly : ∀ i, DehnCanon.Library.IsPoly (P i)
  nonempty_interior : ∀ i, (interior (P i)).Nonempty
  cover : ∀ x, ∃ i, x ∈ P i
  disjoint : Pairwise fun i j => Disjoint (interior (P i)) (interior (P j))
  locallyFinite : LocallyFinite P

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

lemma isClosed_sol {ι : Type} (a : ι → E) (b : ι → ℝ) : IsClosed (sol a b) := by
  have : sol a b = ⋂ i, {x | ⟪a i, x⟫ ≤ b i} := by ext x; simp [sol]
  rw [this]
  exact isClosed_iInter fun i => isClosed_le (by fun_prop) continuous_const

lemma isClosed_of_isPoly {P : Set E} (hP : DehnCanon.Library.IsPoly P) : IsClosed P := by
  obtain ⟨-, ι, _, a, b, rfl⟩ := hP; exact isClosed_sol a b

/-- The cones at `y` of the tiles containing `y` cover space. -/
lemma cover_tcone {ι : Type*} (T : ConvexTiling ι E) {y : E} {U : Set E} (hU : U ∈ 𝓝 y) {F : Finset ι}
    (hF : ∀ j, (T.P j ∩ U).Nonempty → j ∈ F) (v : E) : ∃ j ∈ F, v ∈ tcone (T.P j) y := by
  by_contra hcon
  push Not at hcon
  have hlim : Tendsto (fun t : ℝ => y + t • v) (𝓝[>] 0) (𝓝 y) :=
    ((continuous_const.add (continuous_id.smul continuous_const)).tendsto' 0 y (by simp)).mono_left
      nhdsWithin_le_nhds
  have hev : ∀ j ∈ F, ∀ᶠ t in 𝓝[>] (0 : ℝ), y + t • v ∉ T.P j := by
    intro j hj
    by_cases hy : y ∈ T.P j
    · filter_upwards [self_mem_nhdsWithin] with t ht hmem
      exact hcon j hj ⟨hy, t, ht, hmem⟩
    · exact hlim.eventually_mem ((isClosed_of_isPoly (T.poly j)).isOpen_compl.mem_nhds hy)
  have hall : ∀ᶠ t in 𝓝[>] (0 : ℝ), ∀ j ∈ F, y + t • v ∉ T.P j := (eventually_all_finset F).2 hev
  obtain ⟨t, ht1, ht2⟩ := (hall.and (hlim.eventually_mem hU)).exists
  obtain ⟨k, hk⟩ := T.cover (y + t • v)
  exact ht1 k (hF k ⟨_, hk, ht2⟩) hk

/-- The cones at `y` of two different tiles have disjoint interiors. -/
lemma interior_tcone_inter {ι : Type*} (T : ConvexTiling ι E) {j k : ι} (hjk : j ≠ k) (y : E) :
    interior (tcone (T.P j) y ∩ tcone (T.P k) y) = ∅ := by
  rw [← Set.not_nonempty_iff_eq_empty]
  rintro ⟨v, hv⟩
  have hv' := interior_subset hv
  have hyj : y ∈ T.P j := hv'.1.1
  have hyk : y ∈ T.P k := hv'.2.1
  obtain ⟨-, ιa, _, a, b, hPa⟩ := T.poly j
  obtain ⟨-, ιc, _, c, e, hPc⟩ := T.poly k
  rw [hPa] at hyj
  rw [hPc] at hyk
  rw [hPa, hPc, tcone_sol hyj, tcone_sol hyk] at hv
  obtain ⟨δ1, hδ1, h1⟩ := local_sol hyj
  obtain ⟨δ2, hδ2, h2⟩ := local_sol hyk
  obtain ⟨ρ, hρ, hball⟩ := Metric.isOpen_iff.1 isOpen_interior v hv
  have hδ : 0 < min δ1 δ2 := lt_min hδ1 hδ2
  obtain ⟨t, ht, htv⟩ : ∃ t : ℝ, 0 < t ∧ t * (‖v‖ + ρ) < min δ1 δ2 :=
    ⟨min δ1 δ2 / (2 * (‖v‖ + ρ)), by positivity, by
      rw [div_mul_eq_mul_div, div_lt_iff₀ (by positivity)]; nlinarith [norm_nonneg v]⟩
  have hsub : Metric.ball (y + t • v) (t * ρ) ⊆ T.P j ∩ T.P k := by
    intro z hz
    rw [Metric.mem_ball, dist_eq_norm] at hz
    have hu : t⁻¹ • (z - y) ∈ Metric.ball v ρ := by
      rw [Metric.mem_ball, dist_eq_norm]
      have : t⁻¹ • (z - y) - v = t⁻¹ • (z - (y + t • v)) := by
        rw [smul_sub, smul_sub, smul_add, smul_smul, inv_mul_cancel₀ ht.ne', one_smul]; abel
      rw [this, norm_smul, Real.norm_of_nonneg (inv_nonneg.2 ht.le), inv_mul_lt_iff₀ ht]
      exact hz
    have hcone := interior_subset (hball hu)
    have hw : z - y ∈ cone a (act a b y) ∩ cone c (act c e y) := by
      have : z - y = t • (t⁻¹ • (z - y)) := by rw [smul_smul, mul_inv_cancel₀ ht.ne', one_smul]
      rw [this]; exact ⟨cone_smul hcone.1 ht.le, cone_smul hcone.2 ht.le⟩
    have hwn : ‖z - y‖ < min δ1 δ2 := by
      have e1 : z - y = (z - (y + t • v)) + t • v := by abel
      have e2 : ‖z - y‖ ≤ ‖z - (y + t • v)‖ + t * ‖v‖ := by
        rw [e1]
        refine (norm_add_le _ _).trans ?_
        rw [norm_smul, Real.norm_of_nonneg ht.le]
      nlinarith
    have hz' : z = y + (z - y) := by abel
    rw [hPa, hPc, hz']
    exact ⟨(h1 _ (lt_of_lt_of_le hwn (min_le_left _ _))).2 hw.1,
      (h2 _ (lt_of_lt_of_le hwn (min_le_right _ _))).2 hw.2⟩
  have hint : y + t • v ∈ interior (T.P j) ∩ interior (T.P k) := by
    rw [← interior_inter]
    exact interior_maximal hsub Metric.isOpen_ball (Metric.mem_ball_self (by positivity))
  exact Set.disjoint_iff.1 (T.disjoint hjk) hint

section Angles

variable [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] [Fact (finrank ℝ E = 3)]

/-- One entry of the ring: the cone at `y` of a tile containing `y` with `±d` among its directions. -/
lemma ring_entry {P : Set E} (hP : DehnCanon.Library.IsPoly P) (hint : (interior P).Nonempty) {y d : E} (hy : y ∈ P)
    (hd0 : d ≠ 0) (hd : d ∈ tcone P y) (hnd : -d ∈ tcone P y) :
    IsClosed (tcone P y) ∧ Convex ℝ (tcone P y) ∧ (∀ v ∈ tcone P y, ∀ k ∈ ℝ ∙ d, v + k ∈ tcone P y) ∧
      ((finrank ℝ (linSpace (tcone P y)) = 1 ∧ linSpace (tcone P y) = ℝ ∙ d) ∨
        wedgeAngle (tcone P y) (ℝ ∙ d) = Real.pi ∨ wedgeAngle (tcone P y) (ℝ ∙ d) = 2 * Real.pi) := by
  obtain ⟨-, ιc, _, c, e, rfl⟩ := hP
  have ht := tcone_sol hy
  rw [ht] at hd hnd ⊢
  have hdL : d ∈ linCone c (act c e y) := cone_lin.1 ⟨hd, hnd⟩
  have hKL : ℝ ∙ d ≤ linCone c (act c e y) := (Submodule.span_singleton_le_iff_mem _ _).2 hdL
  refine ⟨isClosed_cone _, convex_cone _, fun v hv k hk => cone_add hv (linCone_subset (hKL hk)), ?_⟩
  rw [linSpace_cone]
  have h3 : finrank ℝ E = 3 := Fact.out
  have hle3 : finrank ℝ (linCone c (act c e y)) ≤ 3 := h3 ▸ Submodule.finrank_le _
  have hge1 : 1 ≤ finrank ℝ (linCone c (act c e y)) := by
    have := Submodule.finrank_mono hKL; rwa [finrank_span_singleton hd0] at this
  rcases (by omega : finrank ℝ (linCone c (act c e y)) = 1 ∨ finrank ℝ (linCone c (act c e y)) = 2 ∨
      finrank ℝ (linCone c (act c e y)) = 3) with h | h | h
  · left
    exact ⟨h, (Submodule.eq_of_le_of_finrank_eq hKL (by rw [finrank_span_singleton hd0, h])).symm⟩
  · right; left
    refine face_angle (isClosed_cone _) (L := linCone c (act c e y)) (fun v hv w hw => cone_add hv hw)
      (fun v hv s hs => cone_smul hv hs) (fun v hv => linCone_subset hv)
      (fun v h1 h2 => cone_lin.1 ⟨h1, h2⟩) hKL h ?_
    by_contra hcon
    push Not at hcon
    obtain ⟨z, hz⟩ := hint
    have hsub : (fun w => y + w) ⁻¹' interior (sol c e) ⊆ (linCone c (act c e y) : Set E) := by
      intro w hw
      apply hcon
      rw [← ht]
      exact ⟨hy, 1, one_pos, by simpa using interior_subset hw⟩
    have hopen : IsOpen ((fun w => y + w) ⁻¹' interior (sol c e)) :=
      isOpen_interior.preimage (by fun_prop)
    have htop := Submodule.eq_top_of_nonempty_interior' (linCone c (act c e y))
      ⟨z - y, interior_maximal hsub hopen (by simpa using hz)⟩
    rw [htop, finrank_top] at h
    omega
  · right; right
    have htop : linCone c (act c e y) = ⊤ := Submodule.eq_top_of_finrank_eq (h.trans h3.symm)
    have : cone c (act c e y) = univ :=
      eq_univ_of_forall fun v => linCone_subset (htop ▸ Submodule.mem_top)
    rw [this]; exact wedgeAngle_univ _

/-- **Lemma 2 of the paper: angles round an edge.** -/
theorem lemma2 {ι : Type*} (T : ConvexTiling ι E) {i : ι} {x : E} (hx : x ∈ T.P i)
    (h1 : finrank ℝ (linSpace (tcone (T.P i) x)) = 1) :
    ∃ (J : Finset ι) (ω : ι → ℝ), i ∈ J ∧
      ω i = wedgeAngle (tcone (T.P i) x) (linSpace (tcone (T.P i) x)) ∧
      (∀ j ∈ J, (∃ y ∈ T.P j, finrank ℝ (linSpace (tcone (T.P j) y)) = 1 ∧
          ω j = wedgeAngle (tcone (T.P j) y) (linSpace (tcone (T.P j) y))) ∨
        ω j = Real.pi ∨ ω j = 2 * Real.pi) ∧
      ∑ j ∈ J, ω j = 2 * Real.pi := by
  classical
  set K := linSpace (tcone (T.P i) x) with hKdef
  obtain ⟨-, ιa, _, a, b, hPi⟩ := T.poly i
  have hxs : x ∈ sol a b := hPi ▸ hx
  have hKlin : K = linCone a (act a b x) := by rw [hKdef, hPi, tcone_sol hxs, linSpace_cone]
  have hKbot : K ≠ ⊥ := by intro h; rw [h, finrank_bot] at h1; exact zero_ne_one h1
  obtain ⟨d, hdK, hd0⟩ := Submodule.exists_mem_ne_zero_of_ne_bot hKbot
  have hKd : K = ℝ ∙ d := (Submodule.eq_of_le_of_finrank_eq
    ((Submodule.span_singleton_le_iff_mem _ _).2 hdK) (by rw [finrank_span_singleton hd0, h1])).symm
  obtain ⟨ε1, hε1, hshift⟩ := edge_shift hxs (hKlin ▸ hdK)
  obtain ⟨U, hU, hUfin⟩ := T.locallyFinite x
  obtain ⟨r, hr, hball⟩ := Metric.mem_nhds_iff.1 hU
  have hdn : 0 < ‖d‖ := norm_pos_iff.2 hd0
  have hεpos : 0 < min ε1 (r / ‖d‖) := lt_min hε1 (div_pos hr hdn)
  set F := hUfin.toFinset
  have hFmem : ∀ j, (T.P j ∩ Metric.ball x r).Nonempty → j ∈ F := by
    rintro j ⟨z, hz1, hz2⟩
    exact hUfin.mem_toFinset.2 ⟨z, hz1, hball hz2⟩
  let S : ι → Set ℝ := fun j => {s | x + s • d ∈ T.P j}
  let B : Finset ℝ := F.biUnion fun j => {sInf (S j), sSup (S j)}
  obtain ⟨s, ⟨hs1, hs2⟩, hsB⟩ :=
    ((Set.Ioo_infinite (show -min ε1 (r / ‖d‖) < min ε1 (r / ‖d‖) by linarith)).sdiff
      B.finite_toSet).nonempty
  have hsabs : |s| < min ε1 (r / ‖d‖) := abs_lt.2 ⟨hs1, hs2⟩
  obtain ⟨hyS, hact⟩ := hshift s (lt_of_lt_of_le hsabs (min_le_left _ _))
  have hyB : x + s • d ∈ Metric.ball x r := by
    rw [Metric.mem_ball, dist_eq_norm, add_sub_cancel_left, norm_smul, Real.norm_eq_abs]
    have := lt_of_lt_of_le hsabs (min_le_right _ _)
    rwa [lt_div_iff₀ hdn] at this
  set y := x + s • d with hydef
  have hyPi : y ∈ T.P i := hPi ▸ hyS
  have hTi : tcone (T.P i) y = tcone (T.P i) x := by rw [hPi, tcone_sol hyS, tcone_sol hxs, hact]
  have hpm : ∀ j, y ∈ T.P j → d ∈ tcone (T.P j) y ∧ -d ∈ tcone (T.P j) y := by
    intro j hyj
    have hjF : j ∈ F := hFmem j ⟨y, hyj, hyB⟩
    have hsS : s ∈ S j := hyj
    obtain ⟨C, hC⟩ := isBounded_iff_forall_norm_le.1 (T.poly j).1
    have hbdd : ∀ s' ∈ S j, |s'| ≤ (C + ‖x‖) / ‖d‖ := by
      intro s' hs'
      rw [le_div_iff₀ hdn]
      have e1 : ‖x + s' • d‖ ≤ C := hC _ hs'
      have e2 : ‖s' • d‖ ≤ ‖x + s' • d‖ + ‖x‖ := by
        have := norm_sub_le (x + s' • d) x; rwa [add_sub_cancel_left] at this
      rw [norm_smul, Real.norm_eq_abs] at e2
      linarith
    have hbA : BddAbove (S j) := ⟨_, fun s' h => (le_abs_self s').trans (hbdd s' h)⟩
    have hbB : BddBelow (S j) := ⟨-((C + ‖x‖) / ‖d‖), fun s' h => by
      have := hbdd s' h; rw [abs_le] at this; linarith⟩
    have hne1 : s ≠ sInf (S j) := fun h => hsB (Finset.mem_coe.2 (Finset.mem_biUnion.2 ⟨j, hjF, by simp [h]⟩))
    have hne2 : s ≠ sSup (S j) := fun h => hsB (Finset.mem_coe.2 (Finset.mem_biUnion.2 ⟨j, hjF, by simp [h]⟩))
    obtain ⟨s2, hs2, hlt2⟩ := exists_lt_of_lt_csSup ⟨s, hsS⟩ (lt_of_le_of_ne (le_csSup hbA hsS) hne2)
    obtain ⟨s1, hs1', hlt1⟩ :=
      exists_lt_of_csInf_lt ⟨s, hsS⟩ (lt_of_le_of_ne (csInf_le hbB hsS) (Ne.symm hne1))
    refine ⟨⟨hyj, s2 - s, by linarith, ?_⟩, ⟨hyj, s - s1, by linarith, ?_⟩⟩
    · have : y + (s2 - s) • d = x + s2 • d := by rw [hydef, add_assoc, ← add_smul, add_sub_cancel]
      rw [this]; exact hs2
    · have : y + (s - s1) • -d = x + s1 • d := by
        rw [hydef, smul_neg, ← sub_eq_add_neg, add_sub_assoc, ← sub_smul, sub_sub_cancel]
      rw [this]; exact hs1'
  set J := F.filter (fun j => y ∈ T.P j)
  have hJ : ∀ j, j ∈ J ↔ y ∈ T.P j := fun j =>
    ⟨fun h => (Finset.mem_filter.1 h).2, fun h => Finset.mem_filter.2 ⟨hFmem j ⟨y, h, hyB⟩, h⟩⟩
  have hfacts := fun j (hj : j ∈ J) => ring_entry (T.poly j) (T.nonempty_interior j) ((hJ j).1 hj) hd0
    (hpm j ((hJ j).1 hj)).1 (hpm j ((hJ j).1 hj)).2
  refine ⟨J, fun j => wedgeAngle (tcone (T.P j) y) K, (hJ i).2 hyPi, ?_, ?_, ?_⟩
  · show wedgeAngle (tcone (T.P i) y) K = _
    rw [hTi]
  · intro j hj
    obtain ⟨-, -, -, hc⟩ := hfacts j hj
    rw [← hKd] at hc
    rcases hc with ⟨hf, hL⟩ | h | h
    · left
      refine ⟨y, (hJ j).1 hj, hf, ?_⟩
      show wedgeAngle (tcone (T.P j) y) K = _
      rw [hL]
    · right; left; exact h
    · right; right; exact h
  · refine wedge_sum J (fun j => tcone (T.P j) y) K (fun j hj => (hfacts j hj).1)
      (fun j hj => (hfacts j hj).2.1) (fun j hj => hKd ▸ (hfacts j hj).2.2.1) (fun v => ?_)
      (fun j _ k _ hjk => interior_tcone_inter T hjk y)
    obtain ⟨j, -, hv⟩ := cover_tcone T (Metric.isOpen_ball.mem_nhds hyB) hFmem v
    exact ⟨j, (hJ j).2 hv.1, hv⟩

/-- `θ` is a dihedral angle of `P`, read from the set at an edge point. -/
def EdgeAngle (P : Set E) (θ : ℝ) : Prop :=
  ∃ x ∈ P, finrank ℝ (linSpace (tcone P x)) = 1 ∧ wedgeAngle (tcone P x) (linSpace (tcone P x)) = θ

/-- **Lemma 2 gives the local angle condition** for every tiling by convex polytopes, with `ok j` the dihedral
angles of tile `j` and any lists `ang j` of dihedral angles of the tiles. -/
theorem localAngleCondition_of_tiling {ι : Type*} (T : ConvexTiling ι E) (ang : ι → List ℝ)
    (h : ∀ i, ∀ θ ∈ ang i, EdgeAngle (T.P i) θ) : LocalAngleCondition ang fun i => EdgeAngle (T.P i) := by
  intro t θ hθ
  obtain ⟨x, hx, h1, rfl⟩ := h t θ hθ
  obtain ⟨J, ω, hJ, hω, hcls, hsum⟩ := lemma2 T hx h1
  refine ⟨J, ω, hJ, hω, fun j hj => ?_, hsum⟩
  rcases hcls j hj with ⟨y, hy, hy1, hωj⟩ | h' | h'
  · exact Or.inl ⟨y, hy, hy1, hωj.symm⟩
  · exact Or.inr (Or.inl h')
  · exact Or.inr (Or.inr h')

/-- **Theorem 4 (a)** for tilings by convex polytopes, given the dihedral angles of the tiles (`ang i` lists
dihedral angles of tile `i`; `AllowedA` says which piece's angles the tile has). -/
theorem theorem4a_tiling {ι : Type*} (T : ConvexTiling ι E) (ang : ι → List ℝ)
    (h : ∀ i, ∀ θ ∈ ang i, EdgeAngle (T.P i) θ) (hk : ∀ i, AllowedA (ang i) (EdgeAngle (T.P i))) (i : ι) :
    ang i ≠ pyrD ∧ ang i ≠ ti ∧ ang i ≠ dod ∧ ang i ≠ ico ∧ ang i ≠ tid :=
  theorem4a ang _ (localAngleCondition_of_tiling T ang h) hk i

/-- **Theorem 4 (b)** for tilings by convex polytopes, given the dihedral angles of the tiles. -/
theorem theorem4b_tiling {ι : Type*} (T : ConvexTiling ι E) (ang : ι → List ℝ)
    (h : ∀ i, ∀ θ ∈ ang i, EdgeAngle (T.P i) θ) (hk : ∀ i, AllowedB (ang i) (EdgeAngle (T.P i))) (i : ι) :
    ang i ≠ pyrI ∧ ang i ≠ td ∧ ang i ≠ dod ∧ ang i ≠ ico ∧ ang i ≠ tid :=
  theorem4b ang _ (localAngleCondition_of_tiling T ang h) hk i

end Angles

end Packets
