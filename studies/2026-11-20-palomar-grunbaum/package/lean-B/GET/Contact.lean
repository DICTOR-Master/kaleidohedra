module

public import GET.Cover

@[expose] public section

/-!
# Contacts between cells

Generic tools for the frontier and the meeting of faces: parallelograms are convex and contain their corners; a point
of a cell (or parallelogram) that is extreme along a normal has its parameters fixed in the directions where the normal
is not orthogonal. The exact test `contactOK c d` decides that two cells either do not meet, or meet inside one face
of GET B; `contact_sound` is its soundness.
-/

namespace GET

open ZPhi GrunbaumK10 Set MeasureTheory
open scoped Pointwise

/-! ## Parallelograms -/

theorem convex_carrier (F : Parallelogram) : Convex ℝ F.carrier := by
  rintro x ⟨s1, hs1, t1, ht1, rfl⟩ y ⟨s2, hs2, t2, ht2, rfl⟩ a b ha hb hab
  obtain rfl : b = 1 - a := by linarith
  refine ⟨a * s1 + (1 - a) * s2, ?_, a * t1 + (1 - a) * t2, ?_, by module⟩
  · simpa [smul_eq_mul] using (convex_Icc (0 : ℝ) 1) hs1 hs2 ha hb hab
  · simpa [smul_eq_mul] using (convex_Icc (0 : ℝ) 1) ht1 ht2 ha hb hab

theorem corner_mem_carrier (F : Parallelogram) (a : Fin 4) : F.corners a ∈ F.carrier := by
  have h0 : (0 : ℝ) ∈ Icc (0 : ℝ) 1 := ⟨le_refl _, zero_le_one⟩
  have h1 : (1 : ℝ) ∈ Icc (0 : ℝ) 1 := ⟨zero_le_one, le_refl _⟩
  fin_cases a
  · exact ⟨0, h0, 0, h0, by simp [Parallelogram.corners]⟩
  · exact ⟨1, h1, 0, h0, by simp [Parallelogram.corners]⟩
  · exact ⟨1, h1, 1, h1, by simp [Parallelogram.corners]⟩
  · exact ⟨0, h0, 1, h1, by simp [Parallelogram.corners]⟩

theorem carrier_subset_of_corners {F : Parallelogram} {S : Set Space} (hS : Convex ℝ S)
    (h : ∀ a, F.corners a ∈ S) : F.carrier ⊆ S := by
  rintro z ⟨s, hs, t, ht, rfl⟩
  have h0 : F.p ∈ S := by simpa [Parallelogram.corners] using h 0
  have h1 : F.p + F.u ∈ S := by simpa [Parallelogram.corners] using h 1
  have h2 : F.p + F.u + F.v ∈ S := by simpa [Parallelogram.corners] using h 2
  have h3 : F.p + F.v ∈ S := by simpa [Parallelogram.corners] using h 3
  have a1 := hS.add_smul_sub_mem h0 h1 hs
  have a2 := hS.add_smul_sub_mem h3 h2 hs
  have := hS.add_smul_sub_mem a1 a2 ht
  convert this using 1
  module

/-! ## Extreme parameters -/

theorem extreme_params {ι : Type*} [Fintype ι] (t a : ι → ℝ) (ht : ∀ i, t i ∈ Icc (0 : ℝ) 1)
    (h : ∑ i, max (a i) 0 ≤ ∑ i, t i * a i) (i : ι) : (0 < a i → t i = 1) ∧ (a i < 0 → t i = 0) := by
  have hle : ∀ j, t j * a j ≤ max (a j) 0 := by
    intro j
    obtain ⟨h0, h1⟩ := ht j
    rcases le_total 0 (a j) with ha | ha
    · rw [max_eq_left ha]; nlinarith
    · rw [max_eq_right ha]; nlinarith
  have heq := (Finset.sum_eq_sum_iff_of_le (fun j _ => hle j)).mp
    (le_antisymm (Finset.sum_le_sum fun j _ => hle j) h) i (Finset.mem_univ _)
  constructor
  · intro hp
    rw [max_eq_left hp.le] at heq
    exact mul_right_cancel₀ hp.ne' (heq.trans (one_mul _).symm)
  · intro hn
    rw [max_eq_right hn.le] at heq
    exact (mul_eq_zero.mp heq).resolve_right hn.ne

theorem extreme_params_min {ι : Type*} [Fintype ι] (t a : ι → ℝ) (ht : ∀ i, t i ∈ Icc (0 : ℝ) 1)
    (h : ∑ i, t i * a i ≤ ∑ i, min (a i) 0) (i : ι) : (a i < 0 → t i = 1) ∧ (0 < a i → t i = 0) := by
  have e : ∀ x : ℝ, max (-x) 0 = -min x 0 := by
    intro x
    rcases le_total x 0 with hx | hx
    · rw [min_eq_left hx, max_eq_left (neg_nonneg.mpr hx)]
    · rw [min_eq_right hx, max_eq_right (neg_nonpos.mpr hx), neg_zero]
  have h' : ∑ i, max (-a i) 0 ≤ ∑ i, t i * (-a i) := by
    simp only [e, mul_neg, Finset.sum_neg_distrib]
    linarith
  have := extreme_params t (fun i => -a i) ht h' i
  exact ⟨fun hn => this.1 (neg_pos.mpr hn), fun hp => this.2 (neg_neg_of_pos hp)⟩

theorem toReal_posPart (a : ZPhi) : toReal (posPart a) = max (toReal a) 0 := by
  unfold posPart
  split_ifs with h
  · rw [max_eq_left (pos_sound h).le]
  · rw [toReal_zero, max_eq_right (not_pos_le (Bool.eq_false_iff.mpr h))]

theorem toReal_negPart (a : ZPhi) : toReal (negPart a) = min (toReal a) 0 := by
  unfold negPart
  split_ifs with h
  · rw [toReal_zero, min_eq_right (pos_sound h).le]
  · rw [min_eq_left (not_pos_le (Bool.eq_false_iff.mpr h))]

/-! ## Points of a cell -/

/-- the three axes of a cell -/
def Cell.sl (c : Cell) : Fin 3 → Fin 6 := ![c.i, c.j, c.k]

/-- the point of a cell with parameters `t` -/
noncomputable def cpoint (c : Cell) (t : Fin 3 → ℝ) : Space :=
  ev (posn c.p) + (t 0 • ax c.i + t 1 • ax c.j + t 2 • ax c.k)

theorem inner_cpoint (n : Fin 3 → ZPhi) (c : Cell) (t : Fin 3 → ℝ) :
    inner ℝ (ev n) (cpoint c t) =
      toReal (dot n (posn c.p)) + ∑ k, t k * toReal (dot n (axis (c.sl k))) := by
  simp only [cpoint, inner_add_right, inner_smul_right, ax, inner_ev, Fin.sum_univ_three, Cell.sl,
    Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two, Matrix.head_cons, Matrix.tail_cons]

theorem cellHi_eq (n : Fin 3 → ZPhi) (c : Cell) :
    toReal (cellHi n c) = toReal (dot n (posn c.p)) + ∑ k, max (toReal (dot n (axis (c.sl k)))) 0 := by
  simp only [cellHi, toReal_add, toReal_posPart, Fin.sum_univ_three, Cell.sl,
    Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two, Matrix.head_cons, Matrix.tail_cons]
  ring

theorem cellLo_eq (n : Fin 3 → ZPhi) (c : Cell) :
    toReal (cellLo n c) = toReal (dot n (posn c.p)) + ∑ k, min (toReal (dot n (axis (c.sl k)))) 0 := by
  simp only [cellLo, toReal_add, toReal_negPart, Fin.sum_univ_three, Cell.sl,
    Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two, Matrix.head_cons, Matrix.tail_cons]
  ring

/-! ## Forced parameters -/

/-- the cell `c` lies below `d` along `n` (they can only meet on the top of `c`) -/
def hiTouch (n : Fin 3 → ZPhi) (c d : Cell) : Bool := nonneg (cellLo n d - cellHi n c)
/-- the cell `c` lies above `d` along `n` -/
def loTouch (n : Fin 3 → ZPhi) (c d : Cell) : Bool := nonneg (cellLo n c - cellHi n d)

/-- the normal `n` forces the parameter `k` of `c` to be `1` on `c ∩ d` -/
def force1 (n : Fin 3 → ZPhi) (c d : Cell) (k : Fin 3) : Bool :=
  (hiTouch n c d && pos (dot n (axis (c.sl k)))) || (loTouch n c d && pos (-(dot n (axis (c.sl k)))))
/-- the normal `n` forces the parameter `k` of `c` to be `0` on `c ∩ d` -/
def force0 (n : Fin 3 → ZPhi) (c d : Cell) (k : Fin 3) : Bool :=
  (hiTouch n c d && pos (-(dot n (axis (c.sl k))))) || (loTouch n c d && pos (dot n (axis (c.sl k))))

theorem force_sound {n : Fin 3 → ZPhi} {c d : Cell} {t : Fin 3 → ℝ} (ht : ∀ k, t k ∈ Icc (0 : ℝ) 1)
    (hd : cpoint c t ∈ cellSet d) (k : Fin 3) :
    (force1 n c d k = true → t k = 1) ∧ (force0 n c d k = true → t k = 0) := by
  have hb := cell_bounds n d hd
  rw [inner_cpoint] at hb
  set a : Fin 3 → ℝ := fun k => toReal (dot n (axis (c.sl k))) with ha
  have hhi : hiTouch n c d = true → ∑ k, max (a k) 0 ≤ ∑ k, t k * a k := by
    intro h
    have := nonneg_sound h
    rw [toReal_sub, cellHi_eq] at this
    simp only [ha]
    linarith [hb.1]
  have hlo : loTouch n c d = true → ∑ k, t k * a k ≤ ∑ k, min (a k) 0 := by
    intro h
    have := nonneg_sound h
    rw [toReal_sub, cellLo_eq] at this
    simp only [ha]
    linarith [hb.2]
  have hneg : ∀ x : ZPhi, pos (-x) = true → toReal x < 0 := by
    intro x hx; have := pos_sound hx; rw [toReal_neg] at this; linarith
  constructor
  · intro h
    simp only [force1, Bool.or_eq_true, Bool.and_eq_true] at h
    rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩
    · exact (extreme_params t a ht (hhi h1) k).1 (pos_sound h2)
    · exact (extreme_params_min t a ht (hlo h1) k).1 (hneg _ h2)
  · intro h
    simp only [force0, Bool.or_eq_true, Bool.and_eq_true] at h
    rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩
    · exact (extreme_params t a ht (hhi h1) k).2 (hneg _ h2)
    · exact (extreme_params_min t a ht (hlo h1) k).2 (pos_sound h2)

/-! ## The contact test -/

/-- some normal forces parameter `k` to `1` -/
def F1 (c d : Cell) (k : Fin 3) : Bool := pairs15.any fun xy => force1 (nrm xy.1 xy.2) c d k
/-- some normal forces parameter `k` to `0` -/
def F0 (c d : Cell) (k : Fin 3) : Bool := pairs15.any fun xy => force0 (nrm xy.1 xy.2) c d k

/-- some normal separates the cells strictly -/
def strictSep (c d : Cell) : Bool := pairs15.any fun xy =>
  pos (cellLo (nrm xy.1 xy.2) d - cellHi (nrm xy.1 xy.2) c) ||
    pos (cellLo (nrm xy.1 xy.2) c - cellHi (nrm xy.1 xy.2) d)

/-- some parameter is forced to both values -/
def conflict (c d : Cell) : Bool := (List.finRange 3).any fun k => F1 c d k && F0 c d k

/-- the corner pattern `b` agrees with the forced parameters -/
def consistent (c d : Cell) (b : Fin 3 → Bool) : Bool :=
  (List.finRange 3).all fun k => (!F1 c d k || b k) && (!F0 c d k || !b k)

/-- the exact corner of a cell with pattern `b` -/
def cpt (c : Cell) (b : Fin 3 → Bool) : Fin 3 → ZPhi :=
  posn c.p + (bif b 0 then axis c.i else 0) + (bif b 1 then axis c.j else 0) + (bif b 2 then axis c.k else 0)

/-- the eight corner patterns -/
def allB3 : List (Fin 3 → Bool) :=
  [![false, false, false], ![true, false, false], ![false, true, false], ![true, true, false],
   ![false, false, true], ![true, false, true], ![false, true, true], ![true, true, true]]

theorem mem_allB3 : ∀ b : Fin 3 → Bool, b ∈ allB3 := by decide

/-- every allowed corner of `c` is a corner of one face of GET B -/
def subInFace (c d : Cell) : Bool :=
  (List.finRange 30).any fun f => allB3.all fun b =>
    !consistent c d b || (List.finRange 4).any fun a => decide ((XB f).corners a = cpt c b)

/-- the contact test: no contact, or the contact lies in one face of GET B -/
def contactOK (c d : Cell) : Bool := strictSep c d || conflict c d || subInFace c d

theorem ev_bif (x : Bool) (y : Fin 3 → ZPhi) : ev (bif x then y else 0) = (if x then (1 : ℝ) else 0) • ev y := by
  cases x <;> simp [ev_zero]

theorem ev_cpt (c : Cell) (b : Fin 3 → Bool) :
    ev (cpt c b) = cpoint c fun k => if b k then 1 else 0 := by
  simp only [cpt, cpoint, ev_add, ev_bif, ax]
  abel

/-- one parameter at a time: a forced parameter takes its value, a free one ranges over a segment -/
theorem step_mem {S : Set Space} (hS : Convex ℝ S) {a w : Space} {s : ℝ} (hs : s ∈ Icc (0 : ℝ) 1)
    {f1 f0 : Prop} (h1 : f1 → s = 1) (h0 : f0 → s = 0)
    (h : ∀ b : Bool, (f1 → b = true) → (f0 → b = false) → a + (if b then (1 : ℝ) else 0) • w ∈ S) :
    a + s • w ∈ S := by
  by_cases g1 : f1
  · have := h1 g1
    by_cases g0 : f0
    · have := h0 g0; linarith
    · have := h true (fun _ => rfl) (fun h => absurd h g0)
      simpa [h1 g1] using this
  · by_cases g0 : f0
    · have := h false (fun h => absurd h g1) (fun _ => rfl)
      simpa [h0 g0] using this
    · have hf := h false (fun h => absurd h g1) (fun h => absurd h g0)
      have ht := h true (fun h => absurd h g1) (fun h => absurd h g0)
      simp only [Bool.false_eq_true, ite_false, zero_smul, add_zero, ite_true, one_smul] at hf ht
      have := hS.add_smul_sub_mem hf ht hs
      simpa using this

theorem contact_sound {c d : Cell} (h : contactOK c d = true) : cellSet c ∩ cellSet d ⊆ ⋃ i, (FB i).carrier := by
  rintro z ⟨hc, hd⟩
  obtain ⟨t, ht, rfl⟩ := mem_cellSet.mp hc
  have hd' : cpoint c t ∈ cellSet d := hd
  have hF1 : ∀ k, F1 c d k = true → t k = 1 := by
    intro k hk
    simp only [F1, List.any_eq_true] at hk
    obtain ⟨xy, _, hxy⟩ := hk
    exact (force_sound ht hd' k).1 hxy
  have hF0 : ∀ k, F0 c d k = true → t k = 0 := by
    intro k hk
    simp only [F0, List.any_eq_true] at hk
    obtain ⟨xy, _, hxy⟩ := hk
    exact (force_sound ht hd' k).2 hxy
  simp only [contactOK, Bool.or_eq_true] at h
  rcases h with (h | h) | h
  · exfalso
    simp only [strictSep, List.any_eq_true, Bool.or_eq_true] at h
    obtain ⟨xy, _, hxy⟩ := h
    have b1 := cell_bounds (nrm xy.1 xy.2) c hc
    have b2 := cell_bounds (nrm xy.1 xy.2) d hd
    rcases hxy with hxy | hxy
    · have := pos_sound hxy; rw [toReal_sub] at this; linarith [b1.2, b2.1]
    · have := pos_sound hxy; rw [toReal_sub] at this; linarith [b1.1, b2.2]
  · exfalso
    simp only [conflict, List.any_eq_true, Bool.and_eq_true] at h
    obtain ⟨k, _, h1, h0⟩ := h
    have := hF1 k h1; have := hF0 k h0; linarith
  · simp only [subInFace, List.any_eq_true, List.all_eq_true] at h
    obtain ⟨f, _, hf⟩ := h
    refine mem_iUnion.mpr ⟨f, ?_⟩
    have hS := convex_carrier (FB f)
    have hcorner : ∀ b : Fin 3 → Bool, (∀ k, F1 c d k = true → b k = true) → (∀ k, F0 c d k = true → b k = false) →
        cpoint c (fun k => if b k then 1 else 0) ∈ (FB f).carrier := by
      intro b hb1 hb0
      have hcons : consistent c d b = true := by
        simp only [consistent, List.all_eq_true, Bool.and_eq_true, Bool.or_eq_true, Bool.not_eq_true']
        intro k _
        constructor
        · by_cases g : F1 c d k = true
          · exact Or.inr (hb1 k g)
          · exact Or.inl (Bool.eq_false_iff.mpr g)
        · by_cases g : F0 c d k = true
          · exact Or.inr (by rw [hb0 k g])
          · exact Or.inl (Bool.eq_false_iff.mpr g)
      have := hf b (mem_allB3 b)
      simp only [Bool.or_eq_true, Bool.not_eq_true', List.any_eq_true, decide_eq_true_eq] at this
      rcases this with hc' | ⟨a, _, ha⟩
      · rw [hcons] at hc'; exact absurd hc' (by decide)
      · rw [← ev_cpt, ← ha, ← XPar.toPar_corners]
        exact corner_mem_carrier _ a
    -- three steps
    show ev (posn c.p) + (t 0 • ax c.i + t 1 • ax c.j + t 2 • ax c.k) ∈ (FB f).carrier
    have e0 : ev (posn c.p) + (t 0 • ax c.i + t 1 • ax c.j + t 2 • ax c.k) =
        (ev (posn c.p) + (t 1 • ax c.j + t 2 • ax c.k)) + t 0 • ax c.i := by abel
    rw [e0]
    refine step_mem hS (ht 0) (hF1 0) (hF0 0) fun b0 hb0 hc0 => ?_
    have e1 : ev (posn c.p) + (t 1 • ax c.j + t 2 • ax c.k) + (if b0 then (1 : ℝ) else 0) • ax c.i =
        (ev (posn c.p) + ((if b0 then (1 : ℝ) else 0) • ax c.i + t 2 • ax c.k)) + t 1 • ax c.j := by abel
    rw [e1]
    refine step_mem hS (ht 1) (hF1 1) (hF0 1) fun b1 hb1 hc1 => ?_
    have e2 : ev (posn c.p) + ((if b0 then (1 : ℝ) else 0) • ax c.i + t 2 • ax c.k) +
        (if b1 then (1 : ℝ) else 0) • ax c.j =
        (ev (posn c.p) + ((if b0 then (1 : ℝ) else 0) • ax c.i + (if b1 then (1 : ℝ) else 0) • ax c.j)) +
          t 2 • ax c.k := by abel
    rw [e2]
    refine step_mem hS (ht 2) (hF1 2) (hF0 2) fun b2 hb2 hc2 => ?_
    have := hcorner ![b0, b1, b2]
      (fun k hk => by fin_cases k <;> simp_all) (fun k hk => by fin_cases k <;> simp_all)
    convert this using 1
    show _ = ev (posn c.p) + ((if b0 then (1 : ℝ) else 0) • ax c.i + (if b1 then (1 : ℝ) else 0) • ax c.j +
      (if b2 then (1 : ℝ) else 0) • ax c.k)
    abel

end GET
