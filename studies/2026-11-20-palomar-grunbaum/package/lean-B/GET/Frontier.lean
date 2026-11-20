module

public import GET.ContactData

@[expose] public section

/-!
# The frontier of GET B is the union of its 30 faces

`⊇`: every face lies in a cell of `PB` and, by the face matching, in a cell of a translate `lat x + PB` (`x ≠ 0`);
since interiors of distinct translates are disjoint, no point of a face is interior to `PB`.

`⊆`: a frontier point of `PB` lies in a translate `lat x + PB` with `x ≠ 0` (the translates cover space and are
locally finite); so it lies in `cell_i ∩ (lat x + cell_j)`, and the exact contact test shows that every such contact
lies in a face of `PB`.
-/

namespace GET

open ZPhi GrunbaumK10 Set MeasureTheory
open scoped Pointwise

/-! ## Faces lie in cells -/

set_option maxHeartbeats 0 in
theorem XB_in_cells : ∀ i : Fin 30, ∃ n : Fin 16, ∀ a : Fin 4, ∃ b ∈ allB3, (XB i).corners a = cpt (CB n) b := by
  decide +kernel

theorem cpt_mem (c : Cell) (b : Fin 3 → Bool) : ev (cpt c b) ∈ cellSet c := by
  rw [ev_cpt]
  exact mem_cellSet_of c (fun k => if b k then 1 else 0) fun k => by
    split_ifs <;> exact ⟨by norm_num, by norm_num⟩

theorem FB_sub_PB (i : Fin 30) : (FB i).carrier ⊆ PB := by
  obtain ⟨n, hn⟩ := XB_in_cells i
  have hconv : Convex ℝ (cellSet (CB n)) := (convex_parallelepiped _).vadd _
  refine (carrier_subset_of_corners hconv fun a => ?_).trans (subset_iUnion (fun n => cellSet (CB n)) n)
  obtain ⟨b, _, hb⟩ := hn a
  rw [FB, XPar.toPar_corners, hb]
  exact cpt_mem _ b

/-! ## Face matching -/

theorem MB_ok : ∀ i : Fin 30, (XB i).u = (XB (MB i).1).u ∧ (XB i).v = (XB (MB i).1).v ∧
    (XB i).p = (XB (MB i).1).p + posn (lv (MB i).2) ∧ (MB i).2 ≠ 0 := by decide +kernel

theorem ev_posn_lv (x : Fin 3 → ℤ) : ev (posn (lv x)) = lat x := by
  have h := ev_posn_add_lv 0 x
  rw [zero_add] at h
  rw [h, ev_posn]
  simp

theorem carrier_vadd (t : Space) (p u v : Space) :
    t +ᵥ (⟨p, u, v⟩ : Parallelogram).carrier = (⟨t + p, u, v⟩ : Parallelogram).carrier := by
  ext z
  simp only [Parallelogram.carrier, Set.mem_vadd_set, mem_ofPred_eq, vadd_eq_add]
  constructor
  · rintro ⟨w, ⟨s, hs, r, hr, rfl⟩, rfl⟩
    exact ⟨s, hs, r, hr, by abel⟩
  · rintro ⟨s, hs, r, hr, rfl⟩
    exact ⟨_, ⟨s, hs, r, hr, rfl⟩, by abel⟩

theorem FB_match (i : Fin 30) : lat (MB i).2 +ᵥ (FB (MB i).1).carrier = (FB i).carrier := by
  obtain ⟨hu, hv, hp, _⟩ := MB_ok i
  simp only [FB, XPar.toPar]
  rw [carrier_vadd, hu, hv, hp, ev_add, ev_posn_lv, add_comm]

theorem lat_ne_zero {x : Fin 3 → ℤ} (hx : x ≠ 0) : lat x ≠ 0 := by
  intro h
  apply hx
  have := Fintype.linearIndependent_iff.mp bB_li (fun r => (x r : ℝ)) h
  funext r
  exact_mod_cast this r

theorem lat_zero : lat 0 = 0 := by simp [lat]

/-! ## Interior and closure of translates -/

theorem interior_vadd (a : Space) (S : Set Space) : interior (a +ᵥ S) = a +ᵥ interior S := by
  rw [← Set.image_vadd, ← Set.image_vadd]
  exact ((Homeomorph.addLeft a).image_interior S).symm

theorem closure_vadd (a : Space) (S : Set Space) : closure (a +ᵥ S) = a +ᵥ closure S := by
  rw [← Set.image_vadd, ← Set.image_vadd]
  exact ((Homeomorph.addLeft a).image_closure S).symm

theorem CB_det : ∀ n : Fin 16, det3 (axis (CB n).i) (axis (CB n).j) (axis (CB n).k) ≠ 0 := by
  decide +kernel

theorem PB_closure_interior : closure (interior PB) = PB := by
  apply le_antisymm
  · exact closure_minimal interior_subset isCompact_PB.isClosed
  · intro z hz
    obtain ⟨n, hn⟩ := mem_iUnion.mp hz
    have hdet := CB_det n
    rw [← closure_interior_cellSet _ hdet] at hn
    exact closure_mono (interior_mono (subset_iUnion (fun n => cellSet (CB n)) n)) hn

/-! ## `⊇` -/

theorem FB_sub_frontier (i : Fin 30) : (FB i).carrier ⊆ frontier PB := by
  intro z hz
  rw [frontier, isCompact_PB.isClosed.closure_eq]
  refine ⟨FB_sub_PB i hz, fun hint => ?_⟩
  set x := (MB i).2
  have hx := (MB_ok i).2.2.2
  have hz' : z ∈ lat x +ᵥ PB := by
    rw [← FB_match i] at hz
    obtain ⟨w, hw, rfl⟩ := Set.mem_vadd_set.mp hz
    exact Set.vadd_mem_vadd_set (FB_sub_PB _ hw)
  rw [← PB_closure_interior, ← closure_vadd, mem_closure_iff] at hz'
  obtain ⟨y, hy1, hy2⟩ := hz' (interior PB) isOpen_interior hint
  rw [← interior_vadd] at hy2
  have hd := PB_disjoint (lat_mem 0) (lat_mem x) (by rw [lat_zero]; exact (lat_ne_zero hx).symm)
  rw [lat_zero, zero_vadd] at hd
  exact Set.disjoint_left.mp hd hy1 hy2

/-! ## `⊆` -/

theorem frontier_in_translate {z : Space} (hz : z ∈ frontier PB) :
    ∃ x : Fin 3 → ℤ, x ≠ 0 ∧ z ∈ lat x +ᵥ PB := by
  rw [frontier, isCompact_PB.isClosed.closure_eq] at hz
  by_contra hcon
  push Not at hcon
  set W := ⋃ g : GB, (if (g : Space) = 0 then (∅ : Set Space) else (g : Space) +ᵥ PB)
  have hW : IsClosed W := by
    refine (translates_locallyFinite.subset fun g => ?_).isClosed_iUnion fun g => ?_
    · split_ifs <;> simp
    · split_ifs
      · exact isClosed_empty
      · rw [← Set.image_vadd]; exact (isCompact_PB.image (continuous_const.add continuous_id)).isClosed
  have hzW : z ∉ W := by
    intro h
    obtain ⟨g, hg⟩ := mem_iUnion.mp h
    split_ifs at hg with h0
    · exact hg
    · have hgl : (g : Space) ∈ lattice bB := by rw [lattice_eq]; exact g.2
      obtain ⟨x, hx⟩ := mem_lattice.mp hgl
      have hx0 : x ≠ 0 := by rintro rfl; exact h0 (by rw [hx, lat_zero])
      exact hcon x hx0 (hx ▸ hg)
  have hsub : Wᶜ ⊆ PB := by
    intro y hy
    have : y ∈ ⋃ t ∈ lattice bB, t +ᵥ PB := by rw [PB_cover]; exact mem_univ y
    obtain ⟨t, ht, hyt⟩ := mem_iUnion₂.mp this
    by_cases h0 : t = 0
    · rw [h0, zero_vadd] at hyt; exact hyt
    · exfalso
      apply hy
      have htG : t ∈ GB := by rw [← SetLike.mem_coe, ← lattice_eq]; exact ht
      refine mem_iUnion.mpr ⟨⟨t, htG⟩, ?_⟩
      simp only [h0, ite_false]
      exact hyt
  exact hz.2 (interior_maximal hsub hW.isOpen_compl hzW)

theorem frontier_sub_FB : frontier PB ⊆ ⋃ i, (FB i).carrier := by
  intro z hz
  have hzP : z ∈ PB := by
    have := frontier_subset_closure hz
    rwa [isCompact_PB.isClosed.closure_eq] at this
  obtain ⟨x, hx0, hzx⟩ := frontier_in_translate hz
  obtain ⟨i, hi⟩ := mem_iUnion.mp hzP
  obtain ⟨w, hw, rfl⟩ := Set.mem_vadd_set.mp hzx
  obtain ⟨j, hj⟩ := mem_iUnion.mp hw
  have hne : (cellSet (CB i) ∩ (lat x +ᵥ cellSet (CB j))).Nonempty := ⟨_, hi, Set.vadd_mem_vadd_set hj⟩
  have hb := coeff_bound hne
  have hx3 : x = ![x 0, x 1, x 2] := by funext k; fin_cases k <;> rfl
  have m : ∀ r, x r ∈ L3 := by
    intro r; have := hb r; simp only [L3, List.mem_cons, List.not_mem_nil, or_false]; omega
  have hnz : ¬ (x 0 = 0 ∧ x 1 = 0 ∧ x 2 = 0) := by
    rintro ⟨h0, h1, h2⟩; apply hx0; rw [hx3, h0, h1, h2]; funext k; fin_cases k <;> rfl
  have hc := B_contacts _ (m 0) _ (m 1) _ (m 2) hnz i j
  rw [← hx3] at hc
  apply contact_sound hc
  refine ⟨hi, ?_⟩
  rw [cellSet_shift]
  exact Set.vadd_mem_vadd_set hj

/-- **the frontier of GET B is the union of its 30 faces** -/
theorem PB_frontier : frontier PB = ⋃ i, (FB i).carrier :=
  le_antisymm frontier_sub_FB (iUnion_subset FB_sub_frontier)

end GET
