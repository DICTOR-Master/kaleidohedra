module

public import GET.Frontier

@[expose] public section

/-!
# Faces of GET B meet properly

For two distinct faces, the exact test `meetOK` finds a normal (among the 15 `eₓ × e_y`) that separates them, and the
parameters of the first face that the separating normals force: either the faces are disjoint, or the forced
parameters leave one corner of the first face that is a corner of the second, or one side of the first face that is a
side of the second.
-/

namespace GET

open ZPhi GrunbaumK10 Set MeasureTheory
open scoped Pointwise

/-! ## Slab bounds of an exact parallelogram -/

/-- lower and upper bounds of `n · x` over an exact parallelogram -/
def xLo (n : Fin 3 → ZPhi) (f : XPar) : ZPhi := dot n f.p + negPart (dot n f.u) + negPart (dot n f.v)
def xHi (n : Fin 3 → ZPhi) (f : XPar) : ZPhi := dot n f.p + posPart (dot n f.u) + posPart (dot n f.v)

/-- the side vectors of an exact parallelogram -/
def XPar.sv (f : XPar) : Fin 2 → Fin 3 → ZPhi := ![f.u, f.v]

/-- the point with parameters `t` -/
noncomputable def fpoint (f : XPar) (t : Fin 2 → ℝ) : Space := ev f.p + t 0 • ev f.u + t 1 • ev f.v

theorem mem_carrier_iff (f : XPar) {z : Space} :
    z ∈ f.toPar.carrier ↔ ∃ t : Fin 2 → ℝ, (∀ k, t k ∈ Icc (0 : ℝ) 1) ∧ z = fpoint f t := by
  constructor
  · rintro ⟨s, hs, r, hr, rfl⟩
    exact ⟨![s, r], fun k => by fin_cases k <;> assumption, rfl⟩
  · rintro ⟨t, ht, rfl⟩
    exact ⟨t 0, ht 0, t 1, ht 1, rfl⟩

theorem inner_fpoint (n : Fin 3 → ZPhi) (f : XPar) (t : Fin 2 → ℝ) :
    inner ℝ (ev n) (fpoint f t) = toReal (dot n f.p) + ∑ k, t k * toReal (dot n (f.sv k)) := by
  simp only [fpoint, inner_add_right, inner_smul_right, inner_ev, Fin.sum_univ_two, XPar.sv,
    Matrix.cons_val_zero, Matrix.cons_val_one]
  ring

theorem xHi_eq (n : Fin 3 → ZPhi) (f : XPar) :
    toReal (xHi n f) = toReal (dot n f.p) + ∑ k, max (toReal (dot n (f.sv k))) 0 := by
  simp only [xHi, toReal_add, toReal_posPart, Fin.sum_univ_two, XPar.sv, Matrix.cons_val_zero,
    Matrix.cons_val_one, Matrix.head_cons]
  ring

theorem xLo_eq (n : Fin 3 → ZPhi) (f : XPar) :
    toReal (xLo n f) = toReal (dot n f.p) + ∑ k, min (toReal (dot n (f.sv k))) 0 := by
  simp only [xLo, toReal_add, toReal_negPart, Fin.sum_univ_two, XPar.sv, Matrix.cons_val_zero,
    Matrix.cons_val_one, Matrix.head_cons]
  ring

theorem x_bounds (n : Fin 3 → ZPhi) (f : XPar) {z : Space} (hz : z ∈ f.toPar.carrier) :
    toReal (xLo n f) ≤ inner ℝ (ev n) z ∧ inner ℝ (ev n) z ≤ toReal (xHi n f) := by
  obtain ⟨t, ht, rfl⟩ := (mem_carrier_iff f).mp hz
  rw [inner_fpoint, xLo_eq, xHi_eq]
  have h0 := part_bounds (dot n (f.sv 0)) (ht 0)
  have h1 := part_bounds (dot n (f.sv 1)) (ht 1)
  rw [toReal_negPart, toReal_posPart] at h0 h1
  simp only [Fin.sum_univ_two]
  constructor <;> linarith [h0.1, h0.2, h1.1, h1.2]

/-! ## Forced parameters of a face -/

def xhiTouch (n : Fin 3 → ZPhi) (f g : XPar) : Bool := nonneg (xLo n g - xHi n f)
def xloTouch (n : Fin 3 → ZPhi) (f g : XPar) : Bool := nonneg (xLo n f - xHi n g)

def xforce1 (n : Fin 3 → ZPhi) (f g : XPar) (k : Fin 2) : Bool :=
  (xhiTouch n f g && pos (dot n (f.sv k))) || (xloTouch n f g && pos (-(dot n (f.sv k))))
def xforce0 (n : Fin 3 → ZPhi) (f g : XPar) (k : Fin 2) : Bool :=
  (xhiTouch n f g && pos (-(dot n (f.sv k)))) || (xloTouch n f g && pos (dot n (f.sv k)))

theorem xforce_sound {n : Fin 3 → ZPhi} {f g : XPar} {t : Fin 2 → ℝ} (ht : ∀ k, t k ∈ Icc (0 : ℝ) 1)
    (hg : fpoint f t ∈ g.toPar.carrier) (k : Fin 2) :
    (xforce1 n f g k = true → t k = 1) ∧ (xforce0 n f g k = true → t k = 0) := by
  have hb := x_bounds n g hg
  rw [inner_fpoint] at hb
  set a : Fin 2 → ℝ := fun k => toReal (dot n (f.sv k)) with ha
  have hhi : xhiTouch n f g = true → ∑ k, max (a k) 0 ≤ ∑ k, t k * a k := by
    intro h
    have := nonneg_sound h
    rw [toReal_sub, xHi_eq] at this
    simp only [ha]
    linarith [hb.1]
  have hlo : xloTouch n f g = true → ∑ k, t k * a k ≤ ∑ k, min (a k) 0 := by
    intro h
    have := nonneg_sound h
    rw [toReal_sub, xLo_eq] at this
    simp only [ha]
    linarith [hb.2]
  have hneg : ∀ x : ZPhi, pos (-x) = true → toReal x < 0 := by
    intro x hx; have := pos_sound hx; rw [toReal_neg] at this; linarith
  constructor
  · intro h
    simp only [xforce1, Bool.or_eq_true, Bool.and_eq_true] at h
    rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩
    · exact (extreme_params t a ht (hhi h1) k).1 (pos_sound h2)
    · exact (extreme_params_min t a ht (hlo h1) k).1 (hneg _ h2)
  · intro h
    simp only [xforce0, Bool.or_eq_true, Bool.and_eq_true] at h
    rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩
    · exact (extreme_params t a ht (hhi h1) k).2 (hneg _ h2)
    · exact (extreme_params_min t a ht (hlo h1) k).2 (pos_sound h2)

/-! ## The meeting test -/

def G1 (f g : XPar) (k : Fin 2) : Bool := pairs15.any fun xy => xforce1 (nrm xy.1 xy.2) f g k
def G0 (f g : XPar) (k : Fin 2) : Bool := pairs15.any fun xy => xforce0 (nrm xy.1 xy.2) f g k

def xstrict (f g : XPar) : Bool := pairs15.any fun xy =>
  pos (xLo (nrm xy.1 xy.2) g - xHi (nrm xy.1 xy.2) f) || pos (xLo (nrm xy.1 xy.2) f - xHi (nrm xy.1 xy.2) g)

/-- the parameters of corner `a`: `(0,0), (1,0), (1,1), (0,1)` -/
def cornerForced (f g : XPar) (a : Fin 4) : Bool :=
  match a with
  | 0 => G0 f g 0 && G0 f g 1
  | 1 => G1 f g 0 && G0 f g 1
  | 2 => G1 f g 0 && G1 f g 1
  | 3 => G0 f g 0 && G1 f g 1

/-- side `a` is selected by one forced parameter -/
def sideForced (f g : XPar) (a : Fin 4) : Bool :=
  match a with
  | 0 => G0 f g 1
  | 1 => G1 f g 0
  | 2 => G1 f g 1
  | 3 => G0 f g 0

def meetOK (f g : XPar) : Bool :=
  xstrict f g ||
  (List.finRange 4).any (fun a => cornerForced f g a &&
    (List.finRange 4).any fun b => decide (f.corners a = g.corners b)) ||
  (List.finRange 4).any (fun a => sideForced f g a &&
    (List.finRange 4).any fun b => decide (f.SideMatch g a b))

theorem B_meet : ∀ i j : Fin 30, i ≠ j → meetOK (XB i) (XB j) = true := by decide +kernel

theorem side_subset_carrier (F : Parallelogram) (a : Fin 4) : F.side a ⊆ F.carrier :=
  (convex_carrier F).segment_subset (corner_mem_carrier F a) (corner_mem_carrier F (a + 1))

theorem fpoint_corner (f : XPar) (a : Fin 4) (t : Fin 2 → ℝ)
    (h : t = ![if a = 1 ∨ a = 2 then 1 else 0, if a = 2 ∨ a = 3 then 1 else 0]) :
    fpoint f t = f.toPar.corners a := by
  subst h
  rw [XPar.toPar_corners]
  fin_cases a <;> simp [fpoint, XPar.corners, ev_add]

theorem meet_sound {f g : XPar} (hf : ∀ a : Fin 4, f.dir a ≠ 0) (h : meetOK f g = true) : MeetProperly f.toPar g.toPar := by
  have hF1 : ∀ t : Fin 2 → ℝ, (∀ k, t k ∈ Icc (0 : ℝ) 1) → fpoint f t ∈ g.toPar.carrier →
      ∀ k, G1 f g k = true → t k = 1 := by
    intro t ht hg k hk
    simp only [G1, List.any_eq_true] at hk
    obtain ⟨xy, _, hxy⟩ := hk
    exact (xforce_sound ht hg k).1 hxy
  have hF0 : ∀ t : Fin 2 → ℝ, (∀ k, t k ∈ Icc (0 : ℝ) 1) → fpoint f t ∈ g.toPar.carrier →
      ∀ k, G0 f g k = true → t k = 0 := by
    intro t ht hg k hk
    simp only [G0, List.any_eq_true] at hk
    obtain ⟨xy, _, hxy⟩ := hk
    exact (xforce_sound ht hg k).2 hxy
  simp only [meetOK, Bool.or_eq_true, List.any_eq_true, Bool.and_eq_true, decide_eq_true_eq] at h
  rcases h with (h | ⟨a, _, hc, b, _, hab⟩) | ⟨a, _, hs, b, _, hab⟩
  · -- disjoint
    left
    ext z
    simp only [mem_inter_iff, mem_empty_iff_false, iff_false, not_and]
    intro hzf hzg
    simp only [xstrict, List.any_eq_true, Bool.or_eq_true] at h
    obtain ⟨xy, _, hxy⟩ := h
    have b1 := x_bounds (nrm xy.1 xy.2) f hzf
    have b2 := x_bounds (nrm xy.1 xy.2) g hzg
    rcases hxy with hxy | hxy
    · have := pos_sound hxy; rw [toReal_sub] at this; linarith [b1.2, b2.1]
    · have := pos_sound hxy; rw [toReal_sub] at this; linarith [b1.1, b2.2]
  · -- a common corner
    right; left
    refine ⟨a, b, by rw [XPar.toPar_corners, XPar.toPar_corners, hab], ?_⟩
    ext z
    simp only [mem_inter_iff, mem_singleton_iff]
    constructor
    · rintro ⟨hzf, hzg⟩
      obtain ⟨t, ht, rfl⟩ := (mem_carrier_iff f).mp hzf
      apply fpoint_corner
      have e1 := hF1 t ht hzg
      have e0 := hF0 t ht hzg
      fin_cases a <;> simp only [cornerForced, Bool.and_eq_true] at hc <;> funext k <;> fin_cases k
      · simp [e0 0 hc.1]
      · simp [e0 1 hc.2]
      · simp [e1 0 hc.1]
      · simp [e0 1 hc.2]
      · simp [e1 0 hc.1]
      · simp [e1 1 hc.2]
      · simp [e0 0 hc.1]
      · simp [e1 1 hc.2]
    · rintro rfl
      refine ⟨corner_mem_carrier _ a, ?_⟩
      rw [XPar.toPar_corners, hab, ← XPar.toPar_corners]
      exact corner_mem_carrier _ b
  · -- a common side
    right; right
    have hside : f.toPar.side a = g.toPar.side b :=
      (XPar.side_eq_iff f g a b (hf a)).mpr hab
    refine ⟨a, b, hside, ?_⟩
    ext z
    simp only [mem_inter_iff]
    constructor
    · rintro ⟨hzf, hzg⟩
      obtain ⟨t, ht, rfl⟩ := (mem_carrier_iff f).mp hzf
      have e1 := hF1 t ht hzg
      have e0 := hF0 t ht hzg
      unfold Parallelogram.side
      rw [segment_eq_image']
      fin_cases a
      · refine ⟨t 0, ht 0, ?_⟩
        have := e0 1 (by simpa [sideForced] using hs)
        simp [fpoint, XPar.toPar, Parallelogram.corners, this]
      · refine ⟨t 1, ht 1, ?_⟩
        have := e1 0 (by simpa [sideForced] using hs)
        simp [fpoint, XPar.toPar, Parallelogram.corners, this] <;> abel
      · refine ⟨1 - t 0, ⟨by linarith [(ht 0).2], by linarith [(ht 0).1]⟩, ?_⟩
        have := e1 1 (by simpa [sideForced] using hs)
        simp [fpoint, XPar.toPar, Parallelogram.corners, this] <;> module
      · refine ⟨1 - t 1, ⟨by linarith [(ht 1).2], by linarith [(ht 1).1]⟩, ?_⟩
        have := e0 0 (by simpa [sideForced] using hs)
        simp [fpoint, XPar.toPar, Parallelogram.corners, this] <;> module
    · intro hz
      exact ⟨side_subset_carrier _ a hz, side_subset_carrier _ b (hside ▸ hz)⟩

theorem FB_meet : ∀ i j, i ≠ j → MeetProperly (FB i) (FB j) := by
  intro i j hij
  exact meet_sound (XB_nondeg i).2.2 (B_meet i j hij)

end GET
