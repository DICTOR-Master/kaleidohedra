module

public import GET.Sphere

@[expose] public section

/-!
# The radial projection of GET B from its centre is injective

The centre is `c₀ = (0, φ, 1 + φ)`, a point of the cell `CB 15`. For one face, the face plane misses `c₀`, so a ray
meets the face at most once. For two faces `i < j`, the certificate `SPB` gives a normal `m` with `m · (z - c₀) ≤ 0`
on face `i` and `≥ 0` on face `j`; two points on one ray then lie on the plane `m · (z - c₀) = 0`, where the faces
touch it in a corner or a side, and the rays through these touching sets meet only at common points.
-/

namespace GET

open ZPhi GrunbaumK10 Set
open scoped Pointwise

/-- the centre `(0, φ, 1 + φ)` -/
def c0x : Fin 3 → ZPhi := ![⟨0, 0⟩, ⟨0, 1⟩, ⟨1, 1⟩]

/-- the centre in `Space` -/
noncomputable def c0 : Space := ev c0x

/-- exact scalar multiple -/
def zsm (x : ZPhi) (v : Fin 3 → ZPhi) : Fin 3 → ZPhi := fun k => x * v k

theorem ev_zsm (x : ZPhi) (v : Fin 3 → ZPhi) : ev (zsm x v) = toReal x • ev v := by
  unfold ev
  rw [← WithLp.toLp_smul]
  congr 1
  funext k
  simp [rv, zsm, toReal_mul]

/-- the parameters of the centre in the cell `CB 15` -/
def tc0 : Fin 3 → ZPhi := ![⟨2, -1⟩, ⟨-1, 1⟩, ⟨2, -1⟩]

theorem c0_cell : c0x = posn (CB 15).p + zsm (tc0 0) (axis (CB 15).i) + zsm (tc0 1) (axis (CB 15).j) +
      zsm (tc0 2) (axis (CB 15).k) ∧
    ∀ k, nonneg (tc0 k) = true ∧ nonneg (⟨1, 0⟩ - tc0 k) = true := by decide +kernel

theorem c0_eq_cpoint {c : Cell} {t : Fin 3 → ZPhi}
    (h : c0x = posn c.p + zsm (t 0) (axis c.i) + zsm (t 1) (axis c.j) + zsm (t 2) (axis c.k)) :
    c0 = cpoint c fun k => toReal (t k) := by
  rw [c0, h]
  simp only [ev_add, ev_zsm, cpoint, ax]
  abel

theorem c0_mem : c0 ∈ PB := by
  refine mem_iUnion.mpr ⟨15, ?_⟩
  have h := c0_cell
  rw [c0_eq_cpoint h.1]
  refine mem_cellSet_of (CB 15) (fun k => toReal (tc0 k)) fun k => ⟨nonneg_sound (h.2 k).1, ?_⟩
  have h2 : nonneg (⟨1, 0⟩ - tc0 k) = true := (h.2 k).2
  have := nonneg_sound h2
  rw [toReal_sub] at this
  have h1 : toReal (⟨1, 0⟩ : ZPhi) = 1 := by simp [toReal]
  linarith

/-! ## One face -/

/-- the face plane misses the centre -/
theorem B_planes : ∀ i : Fin 30, dot (xcross (XB i).u (XB i).v) (XB i).u = 0 ∧
    dot (xcross (XB i).u (XB i).v) (XB i).v = 0 ∧ dot (xcross (XB i).u (XB i).v) ((XB i).p - c0x) ≠ 0 := by
  decide +kernel

theorem toReal_ne_zero {x : ZPhi} (h : x ≠ 0) : toReal x ≠ 0 := by
  intro h0; apply h; apply toReal_injective; rw [h0, toReal_zero]

theorem plane_value (i : Fin 30) {z : Space} (hz : z ∈ (FB i).carrier) :
    inner ℝ (ev (xcross (XB i).u (XB i).v)) (z - c0) =
      toReal (dot (xcross (XB i).u (XB i).v) ((XB i).p - c0x)) := by
  obtain ⟨t, _, rfl⟩ := (mem_carrier_iff (XB i)).mp hz
  obtain ⟨hu, hv, _⟩ := B_planes i
  rw [← inner_ev, ev_sub, inner_sub_right, inner_sub_right, inner_ev, inner_fpoint, c0, inner_ev]
  simp only [Fin.sum_univ_two, XPar.sv, Matrix.cons_val_zero, Matrix.cons_val_one, hu, hv, toReal_zero]
  ring

theorem c0_not_mem (i : Fin 30) : c0 ∉ (FB i).carrier := by
  intro h
  have := plane_value i h
  rw [sub_self, inner_zero_right] at this
  exact toReal_ne_zero (B_planes i).2.2 this.symm

theorem same_face (i : Fin 30) {z₁ z₂ : Space} (h₁ : z₁ ∈ (FB i).carrier) (h₂ : z₂ ∈ (FB i).carrier) {l : ℝ}
    (hl : z₂ - c0 = l • (z₁ - c0)) : z₁ = z₂ := by
  have e1 := plane_value i h₁
  have e2 := plane_value i h₂
  rw [hl, inner_smul_right, e1] at e2
  have hne := toReal_ne_zero (B_planes i).2.2
  have : l = 1 := by
    have := mul_right_cancel₀ hne (e2.trans (one_mul _).symm)
    exact this
  rw [this, one_smul, sub_left_inj] at hl
  exact hl.symm

/-! ## Two faces -/

/-- the corner of an exact parallelogram with parameters `a, b ∈ {0, 1}` -/
def xc (f : XPar) (a b : Bool) : Fin 3 → ZPhi := f.p + (bif a then f.u else 0) + (bif b then f.v else 0)

/-- the corner or side left by the forced parameters -/
def segOf (f : XPar) : Option Bool → Option Bool → Option ((Fin 3 → ZPhi) × (Fin 3 → ZPhi))
  | some a, some b => some (xc f a b, xc f a b)
  | some a, none => some (xc f a false, xc f a true)
  | none, some b => some (xc f false b, xc f true b)
  | none, none => none

/-- the pattern of a parameter at the maximum of `m · z` -/
def patMax (m w : Fin 3 → ZPhi) : Option Bool :=
  if pos (dot m w) then some true else if pos (-(dot m w)) then some false else none

/-- the pattern of a parameter at the minimum of `m · z` -/
def patMin (m w : Fin 3 → ZPhi) : Option Bool :=
  if pos (dot m w) then some false else if pos (-(dot m w)) then some true else none

/-- rays from the centre through the two touching sets meet only at common points -/
def rayOK (A B A' B' : Fin 3 → ZPhi) : Bool :=
  decide ((A = B ∧ A' = B' ∧ (A = A' ∨ xcross (A - c0x) (A' - c0x) ≠ 0)) ∨
    ((A' = A ∨ A' = B) ∧ (B' = A ∨ B' = B) ∧ xcross (A - c0x) (B - c0x) ≠ 0) ∨
    ((A = A' ∨ A = B') ∧ (B = A' ∨ B = B') ∧ xcross (A' - c0x) (B' - c0x) ≠ 0))

/-- the cone-separation test for faces `f`, `g` with normal `m` -/
def sphOK (m : Fin 3 → ZPhi) (f g : XPar) : Bool :=
  nonneg (dot m c0x - xHi m f) && nonneg (xLo m g - dot m c0x) &&
  (pos (dot m c0x - xHi m f) || pos (xLo m g - dot m c0x) ||
    match segOf f (patMax m f.u) (patMax m f.v), segOf g (patMin m g.u) (patMin m g.v) with
    | some (A, B), some (A', B') => rayOK A B A' B'
    | _, _ => false)

theorem B_sph_all : SPB.all (fun e => sphOK e.2 (XB e.1.1) (XB e.1.2)) = true := by decide +kernel

theorem B_sph_cover : ∀ i j : Fin 30, i < j → ∃ e ∈ SPB, e.1 = (i, j) := by decide +kernel

theorem ev_xc (f : XPar) (a b : Bool) :
    ev (xc f a b) = ev f.p + (if a then (1 : ℝ) else 0) • ev f.u + (if b then (1 : ℝ) else 0) • ev f.v := by
  simp only [xc, ev_add, ev_bif]

theorem segOf_sound {f : XPar} {o₀ o₁ : Option Bool} {A B : Fin 3 → ZPhi} (hs : segOf f o₀ o₁ = some (A, B))
    {t : Fin 2 → ℝ} (ht : ∀ k, t k ∈ Icc (0 : ℝ) 1)
    (h₀ : ∀ b, o₀ = some b → t 0 = if b then 1 else 0) (h₁ : ∀ b, o₁ = some b → t 1 = if b then 1 else 0) :
    fpoint f t ∈ segment ℝ (ev A) (ev B) := by
  rw [segment_eq_image']
  match o₀, o₁, hs with
  | some a, some b, hs =>
    simp only [segOf, Option.some.injEq, Prod.mk.injEq] at hs
    obtain ⟨rfl, rfl⟩ := hs
    refine ⟨0, ⟨le_refl _, zero_le_one⟩, ?_⟩
    beta_reduce
    rw [zero_smul, add_zero, ev_xc, fpoint, h₀ a rfl, h₁ b rfl]
  | some a, none, hs =>
    simp only [segOf, Option.some.injEq, Prod.mk.injEq] at hs
    obtain ⟨rfl, rfl⟩ := hs
    refine ⟨t 1, ht 1, ?_⟩
    beta_reduce
    rw [ev_xc, ev_xc, fpoint, h₀ a rfl]
    simp only [Bool.false_eq_true, ite_false, ite_true, zero_smul, add_zero, one_smul]
    abel
  | none, some b, hs =>
    simp only [segOf, Option.some.injEq, Prod.mk.injEq] at hs
    obtain ⟨rfl, rfl⟩ := hs
    refine ⟨t 0, ht 0, ?_⟩
    beta_reduce
    rw [ev_xc, ev_xc, fpoint, h₁ b rfl]
    simp only [Bool.false_eq_true, ite_false, ite_true, zero_smul, add_zero, one_smul]
    abel
  | none, none, hs => simp [segOf] at hs

theorem indep_of_xcross {u v : Fin 3 → ZPhi} (h : xcross (u - c0x) (v - c0x) ≠ 0) :
    LinearIndependent ℝ ![ev u - c0, ev v - c0] := by
  have := linearIndependent_ev2 h
  rwa [ev_sub, ev_sub] at this

/-- a ray from the centre meets a segment whose line misses the centre at most once -/
theorem seg_ray {a b z₁ z₂ : Space} (hind : LinearIndependent ℝ ![a - c0, b - c0])
    (h₁ : z₁ ∈ segment ℝ a b) (h₂ : z₂ ∈ segment ℝ a b) {l : ℝ} (hl : z₂ - c0 = l • (z₁ - c0)) : z₁ = z₂ := by
  rw [segment_eq_image'] at h₁ h₂
  obtain ⟨s, _, rfl⟩ := h₁
  obtain ⟨s', _, rfl⟩ := h₂
  have e : ((1 - s') - l * (1 - s)) • (a - c0) + (s' - l * s) • (b - c0) = 0 := by
    have : a + s' • (b - a) - c0 - l • (a + s • (b - a) - c0) = 0 := sub_eq_zero.mpr hl
    rw [← this]; module
  have := LinearIndependent.pair_iff.mp hind _ _ e
  have hl1 : l = 1 := by linarith [this.1, this.2]
  have hs : s' = s := by rw [hl1] at this; linarith [this.2]
  rw [hs]

theorem rayOK_sound {A B A' B' : Fin 3 → ZPhi} (h : rayOK A B A' B' = true) {z₁ z₂ : Space}
    (h₁ : z₁ ∈ segment ℝ (ev A) (ev B)) (h₂ : z₂ ∈ segment ℝ (ev A') (ev B')) {l : ℝ} (hl0 : 0 < l)
    (hl : z₂ - c0 = l • (z₁ - c0)) : z₁ = z₂ := by
  simp only [rayOK, decide_eq_true_eq] at h
  rcases h with ⟨rfl, rfl, h⟩ | ⟨hA', hB', hx⟩ | ⟨hA, hB, hx⟩
  · rw [segment_same, mem_singleton_iff] at h₁ h₂
    subst h₁; subst h₂
    rcases h with rfl | hx
    · rfl
    · exfalso
      have hind := indep_of_xcross hx
      have e : l • (ev A - c0) + (-1 : ℝ) • (ev A' - c0) = 0 := by rw [← hl]; module
      have := (LinearIndependent.pair_iff.mp hind _ _ e).2
      norm_num at this
  · have hsub : segment ℝ (ev A') (ev B') ⊆ segment ℝ (ev A) (ev B) := by
      apply (convex_segment _ _).segment_subset
      · rcases hA' with rfl | rfl
        · exact left_mem_segment _ _ _
        · exact right_mem_segment _ _ _
      · rcases hB' with rfl | rfl
        · exact left_mem_segment _ _ _
        · exact right_mem_segment _ _ _
    exact seg_ray (indep_of_xcross hx) h₁ (hsub h₂) hl
  · have hsub : segment ℝ (ev A) (ev B) ⊆ segment ℝ (ev A') (ev B') := by
      apply (convex_segment _ _).segment_subset
      · rcases hA with rfl | rfl
        · exact left_mem_segment _ _ _
        · exact right_mem_segment _ _ _
      · rcases hB with rfl | rfl
        · exact left_mem_segment _ _ _
        · exact right_mem_segment _ _ _
    exact seg_ray (indep_of_xcross hx) (hsub h₁) h₂ hl

theorem sph_sound {m : Fin 3 → ZPhi} {f g : XPar} (h : sphOK m f g = true) {z₁ z₂ : Space}
    (h₁ : z₁ ∈ f.toPar.carrier) (h₂ : z₂ ∈ g.toPar.carrier) {l : ℝ} (hl0 : 0 < l)
    (hl : z₂ - c0 = l • (z₁ - c0)) : z₁ = z₂ := by
  simp only [sphOK, Bool.and_eq_true, Bool.or_eq_true] at h
  obtain ⟨⟨hF, hG⟩, h⟩ := h
  have bF := x_bounds m f h₁
  have bG := x_bounds m g h₂
  have nF := nonneg_sound hF
  have nG := nonneg_sound hG
  rw [toReal_sub] at nF nG
  have hc : inner ℝ (ev m) c0 = toReal (dot m c0x) := by rw [c0, inner_ev]
  -- both points lie on the plane `m · (z - c₀) = 0`
  have k1 : inner ℝ (ev m) (z₁ - c0) ≤ 0 := by rw [inner_sub_right, hc]; linarith [bF.2]
  have k2 : 0 ≤ inner ℝ (ev m) (z₂ - c0) := by rw [inner_sub_right, hc]; linarith [bG.1]
  have k3 : inner ℝ (ev m) (z₂ - c0) = l * inner ℝ (ev m) (z₁ - c0) := by rw [hl, inner_smul_right]
  have q1 : inner ℝ (ev m) z₁ = toReal (dot m c0x) := by
    have : inner ℝ (ev m) (z₁ - c0) = 0 := by nlinarith
    rw [inner_sub_right, hc] at this; linarith
  have q2 : inner ℝ (ev m) z₂ = toReal (dot m c0x) := by
    have : inner ℝ (ev m) (z₂ - c0) = 0 := by
      have : inner ℝ (ev m) (z₁ - c0) = 0 := by nlinarith
      rw [k3, this, mul_zero]
    rw [inner_sub_right, hc] at this; linarith
  rcases h with (h | h) | h
  · exfalso; have := pos_sound h; rw [toReal_sub] at this; linarith [bF.2]
  · exfalso; have := pos_sound h; rw [toReal_sub] at this; linarith [bG.1]
  · obtain ⟨t, ht, rfl⟩ := (mem_carrier_iff f).mp h₁
    obtain ⟨t', ht', rfl⟩ := (mem_carrier_iff g).mp h₂
    -- forced parameters
    have sF : ∑ k, max (toReal (dot m (f.sv k))) 0 ≤ ∑ k, t k * toReal (dot m (f.sv k)) := by
      have := xHi_eq m f; rw [inner_fpoint] at q1; linarith
    have sG : ∑ k, t' k * toReal (dot m (g.sv k)) ≤ ∑ k, min (toReal (dot m (g.sv k))) 0 := by
      have := xLo_eq m g; rw [inner_fpoint] at q2; linarith
    have hneg : ∀ x : ZPhi, pos (-x) = true → toReal x < 0 := by
      intro x hx; have := pos_sound hx; rw [toReal_neg] at this; linarith
    have pF : ∀ k : Fin 2, ∀ b, patMax m (f.sv k) = some b → t k = if b then 1 else 0 := by
      intro k b hb
      have e := extreme_params t _ ht sF k
      unfold patMax at hb
      split_ifs at hb with p1 p2
      · cases hb; simpa using e.1 (pos_sound p1)
      · cases hb; simpa using e.2 (hneg _ p2)
    have pG : ∀ k : Fin 2, ∀ b, patMin m (g.sv k) = some b → t' k = if b then 1 else 0 := by
      intro k b hb
      have e := extreme_params_min t' _ ht' sG k
      unfold patMin at hb
      split_ifs at hb with p1 p2
      · cases hb; simpa using e.2 (pos_sound p1)
      · cases hb; simpa using e.1 (hneg _ p2)
    revert h
    cases hsf : segOf f (patMax m f.u) (patMax m f.v) with
    | none => simp
    | some s =>
      cases hsg : segOf g (patMin m g.u) (patMin m g.v) with
      | none => simp
      | some s' =>
        obtain ⟨A, B⟩ := s
        obtain ⟨A', B'⟩ := s'
        intro h
        apply rayOK_sound h _ _ hl0 hl
        · exact segOf_sound hsf ht (pF 0) (pF 1)
        · exact segOf_sound hsg ht' (pG 0) (pG 1)

/-- two points of the faces on one ray from the centre are equal -/
theorem faces_ray {i j : Fin 30} {z₁ z₂ : Space} (h₁ : z₁ ∈ (FB i).carrier) (h₂ : z₂ ∈ (FB j).carrier)
    {l : ℝ} (hl0 : 0 < l) (hl : z₂ - c0 = l • (z₁ - c0)) : z₁ = z₂ := by
  have key : ∀ i j : Fin 30, i < j → ∀ z₁ z₂ : Space, z₁ ∈ (FB i).carrier → z₂ ∈ (FB j).carrier →
      ∀ l : ℝ, 0 < l → z₂ - c0 = l • (z₁ - c0) → z₁ = z₂ := by
    intro i j hij z₁ z₂ h₁ h₂ l hl0 hl
    obtain ⟨e, he, hej⟩ := B_sph_cover i j hij
    have := List.all_eq_true.mp B_sph_all e he
    rw [hej] at this
    exact sph_sound this h₁ h₂ hl0 hl
  rcases lt_trichotomy i j with h | rfl | h
  · exact key i j h z₁ z₂ h₁ h₂ l hl0 hl
  · exact same_face i h₁ h₂ hl
  · have hl' : z₁ - c0 = l⁻¹ • (z₂ - c0) := by rw [hl, smul_smul, inv_mul_cancel₀ hl0.ne', one_smul]
    exact (key j i h z₂ z₁ h₂ h₁ l⁻¹ (inv_pos.mpr hl0) hl').symm

/-- **the frontier of GET B is homeomorphic to the sphere** -/
theorem PB_sphere : Nonempty (frontier PB ≃ₜ Metric.sphere (0 : Space) 1) := by
  apply sphere_of_radial isCompact_PB c0_mem
  · rw [PB_frontier]
    intro h
    obtain ⟨i, hi⟩ := mem_iUnion.mp h
    exact c0_not_mem i hi
  · intro z₁ h₁ z₂ h₂ l hl0 hl
    rw [PB_frontier] at h₁ h₂
    obtain ⟨i, hi⟩ := mem_iUnion.mp h₁
    obtain ⟨j, hj⟩ := mem_iUnion.mp h₂
    exact faces_ray hi hj hl0 hl

end GET
