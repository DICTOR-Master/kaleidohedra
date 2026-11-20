module

public import GET.Calib

@[expose] public section

/-!
# The 30 faces of GET B in `Space`

The faces are `FB i = (XB i).toPar`, with the exact data `XB` of `GET.Certs`. This module proves the face-level
claims: the exact data are the faces of the six-axis model, every face is a golden rhombus, any two faces are
congruent, every zone has 10 faces, and two distinct faces that share a side are not coplanar.
-/

namespace GET

open ZPhi GrunbaumK10 Set

/-- the faces of GET B -/
noncomputable def FB (i : Fin 30) : Parallelogram := (XB i).toPar

/-- the exact data are the faces of the model: corner `posn p`, sides `axis a`, `axis b` -/
theorem XB_model : ∀ i : Fin 30, (XB i).p = posn (facesB.getD i ⟨0, 0, 0, 0⟩).p ∧
    (XB i).u = axis (facesB.getD i ⟨0, 0, 0, 0⟩).a ∧ (XB i).v = axis (facesB.getD i ⟨0, 0, 0, 0⟩).b := by
  decide +kernel

/-! ## Zones -/

theorem ZB_cert : ZoneCert XB 10 ZB := by decide +kernel

theorem FB_zones : EveryZoneHas FB 10 := everyZoneHas_of_cert XB 10 ZB ZB_cert

/-! ## Golden rhombi -/

/-- the shape of a golden rhombus with `|u|² = |v|² = 2 + φ`, diagonals `|u ± v|² ∈ {4 + 4φ, 4}` -/
abbrev XPar.Golden (f : XPar) : Prop :=
  dot f.u f.u = ⟨2, 1⟩ ∧ dot f.v f.v = ⟨2, 1⟩ ∧ xcross f.u f.v ≠ 0 ∧
    ((dot (f.u + f.v) (f.u + f.v) = ⟨4, 4⟩ ∧ dot (f.u - f.v) (f.u - f.v) = ⟨4, 0⟩) ∨
     (dot (f.u + f.v) (f.u + f.v) = ⟨4, 0⟩ ∧ dot (f.u - f.v) (f.u - f.v) = ⟨4, 4⟩))

theorem XB_golden : ∀ i : Fin 30, (XB i).Golden := by decide +kernel

theorem sqrt_four : Real.sqrt (toReal ⟨4, 0⟩) = 2 := by
  rw [show toReal ⟨4, 0⟩ = 2 ^ 2 by simp [toReal]; norm_num]
  exact Real.sqrt_sq (by norm_num)

theorem sqrt_four_phi : Real.sqrt (toReal ⟨4, 4⟩) = 2 * Real.goldenRatio := by
  rw [show toReal ⟨4, 4⟩ = (2 * Real.goldenRatio) ^ 2 by
    simp [toReal]; nlinarith [Real.goldenRatio_sq]]
  exact Real.sqrt_sq (by positivity)

theorem XPar.golden_norms {f : XPar} (h : f.Golden) :
    ‖f.toPar.u‖ = Real.sqrt (toReal ⟨2, 1⟩) ∧ ‖f.toPar.v‖ = Real.sqrt (toReal ⟨2, 1⟩) ∧
    ((‖f.toPar.u + f.toPar.v‖ = 2 * Real.goldenRatio ∧ ‖f.toPar.u - f.toPar.v‖ = 2) ∨
     (‖f.toPar.u + f.toPar.v‖ = 2 ∧ ‖f.toPar.u - f.toPar.v‖ = 2 * Real.goldenRatio)) := by
  obtain ⟨hu, hv, _, hd⟩ := h
  simp only [XPar.toPar]
  rw [← ev_add, ← ev_sub, norm_ev, norm_ev, norm_ev, norm_ev, hu, hv]
  refine ⟨rfl, rfl, ?_⟩
  rcases hd with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · left; rw [h1, h2, sqrt_four, sqrt_four_phi]; exact ⟨rfl, rfl⟩
  · right; rw [h1, h2, sqrt_four, sqrt_four_phi]; exact ⟨rfl, rfl⟩

theorem XPar.golden_isGoldenRhombus {f : XPar} (h : f.Golden) : f.toPar.IsGoldenRhombus := by
  obtain ⟨hu, hv, hd⟩ := XPar.golden_norms h
  refine ⟨⟨linearIndependent_ev2 h.2.2.1, by rw [hu, hv]⟩, ?_⟩
  rcases hd with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · left; rw [h1, h2]; ring
  · right; rw [h1, h2]; ring

theorem FB_golden (i : Fin 30) : (FB i).IsGoldenRhombus := XPar.golden_isGoldenRhombus (XB_golden i)

/-! ## Congruence -/

theorem dist_corners (F : Parallelogram) (a b : Fin 4) :
    dist (F.corners a) (F.corners b) =
      ‖(![0, F.u, F.u + F.v, F.v] : Fin 4 → Space) a - (![0, F.u, F.u + F.v, F.v] : Fin 4 → Space) b‖ := by
  rw [dist_eq_norm]
  congr 1
  fin_cases a <;> fin_cases b <;> simp [Parallelogram.corners] <;> abel

/-- parallelograms with the same side lengths and diagonals have congruent corners -/
theorem congruent_of_norms {F G : Parallelogram} (h1 : ‖F.u‖ = ‖G.u‖) (h2 : ‖F.v‖ = ‖G.v‖)
    (h3 : ‖F.u + F.v‖ = ‖G.u + G.v‖) (h4 : ‖F.u - F.v‖ = ‖G.u - G.v‖) : Congruent F.corners G.corners := by
  rw [congruent_iff_dist_eq]
  intro a b
  rw [dist_corners, dist_corners]
  have h4' : ‖F.v - F.u‖ = ‖G.v - G.u‖ := by rw [norm_sub_rev, h4, norm_sub_rev]
  have h3' : ‖-F.v + -F.u‖ = ‖-G.v + -G.u‖ := by
    rw [← neg_add, ← neg_add, norm_neg, norm_neg, add_comm, h3, add_comm]
  fin_cases a <;> fin_cases b <;>
    simp [norm_neg, h1, h2, h3, h3', h4, h4', add_sub_cancel_left, add_sub_cancel_right, sub_add_cancel_left]

/-- relabelling the corners of `⟨p, u, v⟩` by a rotation gives the corners of `⟨p + u, v, -u⟩` -/
theorem corners_rotate (F : Parallelogram) :
    F.corners ∘ (finRotate 4) = (⟨F.p + F.u, F.v, -F.u⟩ : Parallelogram).corners := by
  funext a
  fin_cases a <;> simp [Parallelogram.corners, finRotate_apply] <;> abel

/-- the reference golden rhombus -/
noncomputable def RG : Parallelogram := ⟨0, ev (axis 0), ev (axis 4)⟩

theorem RG_norms : ‖RG.u‖ = Real.sqrt (toReal ⟨2, 1⟩) ∧ ‖RG.v‖ = Real.sqrt (toReal ⟨2, 1⟩) ∧
    ‖RG.u + RG.v‖ = 2 * Real.goldenRatio ∧ ‖RG.u - RG.v‖ = 2 := by
  have h : (⟨0, axis 0, axis 4⟩ : XPar).Golden ∧
      dot (axis 0 + axis 4) (axis 0 + axis 4) = ⟨4, 4⟩ := by decide +kernel
  obtain ⟨hu, hv, hd⟩ := XPar.golden_norms h.1
  refine ⟨hu, hv, ?_⟩
  rcases hd with hd | ⟨h1, _⟩
  · exact hd
  · exfalso
    have : ‖ev (axis 0 + axis 4)‖ = 2 * Real.goldenRatio := by rw [norm_ev, h.2, sqrt_four_phi]
    simp only [XPar.toPar] at h1
    rw [← ev_add, this] at h1
    nlinarith [Real.one_lt_goldenRatio]

/-- every golden face is congruent to the reference rhombus, after relabelling -/
theorem XPar.golden_congr_ref {f : XPar} (h : f.Golden) :
    ∃ σ : Equiv.Perm (Fin 4), Congruent (f.toPar.corners ∘ σ) RG.corners := by
  obtain ⟨hu, hv, hd⟩ := XPar.golden_norms h
  obtain ⟨ru, rv', r3, r4⟩ := RG_norms
  rcases hd with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · exact ⟨1, congruent_of_norms (by rw [hu, ru]) (by rw [hv, rv']) (by rw [h1, r3]) (by rw [h2, r4])⟩
  · refine ⟨finRotate 4, ?_⟩
    rw [corners_rotate]
    apply congruent_of_norms
    · simp only; rw [hv, ru]
    · simp only; rw [norm_neg, hu, rv']
    · simp only; rw [← sub_eq_add_neg, norm_sub_rev, h2, r3]
    · simp only; rw [sub_neg_eq_add, add_comm, h1, r4]

theorem facesCongruent_of_golden {f g : XPar} (hf : f.Golden) (hg : g.Golden) :
    FacesCongruent f.toPar g.toPar := by
  obtain ⟨σ, hσ⟩ := XPar.golden_congr_ref hf
  obtain ⟨τ, hτ⟩ := XPar.golden_congr_ref hg
  refine ⟨τ.symm.trans σ, ?_⟩
  have e1 : f.toPar.corners ∘ ⇑(τ.symm.trans σ) = (f.toPar.corners ∘ σ) ∘ τ.symm := by
    funext a; simp
  have e2 : g.toPar.corners = (g.toPar.corners ∘ τ) ∘ τ.symm := by
    funext a; simp
  rw [e1, e2]
  exact (hσ.trans hτ.symm).index_map _

theorem FB_rhombicMonohedral : IsRhombicMonohedral FB :=
  ⟨fun i => (FB_golden i).1, fun i j => facesCongruent_of_golden (XB_golden i) (XB_golden j)⟩

/-! ## Adjacent faces are not coplanar -/

theorem not_coplanar_of_three {s : Set Space} {x y z : Space} (hx : x ∈ vectorSpan ℝ s)
    (hy : y ∈ vectorSpan ℝ s) (hz : z ∈ vectorSpan ℝ s) (hli : LinearIndependent ℝ ![x, y, z]) :
    ¬ Coplanar ℝ s := by
  rw [coplanar_iff_finrank_le_two]
  intro h
  have h1 : Submodule.span ℝ (Set.range ![x, y, z]) ≤ vectorSpan ℝ s := by
    rw [Submodule.span_le]
    rintro _ ⟨i, rfl⟩
    fin_cases i
    · exact hx
    · exact hy
    · exact hz
  have h2 := Submodule.finrank_mono h1
  rw [finrank_span_eq_card hli] at h2
  simp at h2
  omega

/-- the exact check: two distinct faces that share a side span three independent directions -/
abbrev AdjacentSpan (X : Fin 30 → XPar) : Prop :=
  ∀ i j : Fin 30, i ≠ j → (∃ a b : Fin 4, (X i).SideMatch (X j) a b) →
    (det3 (X i).u (X i).v (X j).u ≠ 0 ∨ det3 (X i).u (X i).v (X j).v ≠ 0)

theorem XB_adjacentSpan : AdjacentSpan XB := by decide +kernel

theorem XB_nondeg : XNondeg XB := ZB_cert.1

theorem FB_not_coplanar : ∀ i j, i ≠ j → Adjacent FB i j →
    ¬ Coplanar ℝ (range (FB i).corners ∪ range (FB j).corners) := by
  intro i j hij ⟨a, b, hab⟩
  rw [FB, FB, XPar.side_eq_iff _ _ _ _ ((XB_nondeg i).2.2 a)] at hab
  have hmem : ∀ (F : Parallelogram) (c d : Fin 4), F = FB i ∨ F = FB j →
      F.corners c -ᵥ F.corners d ∈ vectorSpan ℝ (range (FB i).corners ∪ range (FB j).corners) := by
    intro F c d hF
    apply vsub_mem_vectorSpan
    · rcases hF with rfl | rfl
      · exact Or.inl ⟨c, rfl⟩
      · exact Or.inr ⟨c, rfl⟩
    · rcases hF with rfl | rfl
      · exact Or.inl ⟨d, rfl⟩
      · exact Or.inr ⟨d, rfl⟩
  have hu : ∀ F : Parallelogram, F.corners 1 -ᵥ F.corners 0 = F.u := by
    intro F; simp [Parallelogram.corners]
  have hv : ∀ F : Parallelogram, F.corners 3 -ᵥ F.corners 0 = F.v := by
    intro F; simp [Parallelogram.corners]
  have mi_u := hu (FB i) ▸ hmem (FB i) 1 0 (Or.inl rfl)
  have mi_v := hv (FB i) ▸ hmem (FB i) 3 0 (Or.inl rfl)
  have mj_u := hu (FB j) ▸ hmem (FB j) 1 0 (Or.inr rfl)
  have mj_v := hv (FB j) ▸ hmem (FB j) 3 0 (Or.inr rfl)
  rcases XB_adjacentSpan i j hij ⟨a, b, hab⟩ with h | h
  · exact not_coplanar_of_three mi_u mi_v mj_u (linearIndependent_ev3 h)
  · exact not_coplanar_of_three mi_u mi_v mj_v (linearIndependent_ev3 h)

end GET
