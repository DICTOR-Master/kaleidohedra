module

public import YantraCert.Sound

@[expose] public section

/-!
# Soundness of the tree walk

`checkTree_sound`: if the kernel has evaluated `checkTree C fuel c t` to `true`, then every point of the cell `c` is
`Good` for the chart `C`: some equation polynomial is nonzero there, or some admissibility test has `N * D < 0` there, or the
point lies in one of the chart's holes.
-/

namespace YantraCert

lemma nth_mem_or {α : Type} (d : α) (l : List α) (k : Nat) : nth d l k ∈ l ∨ nth d l k = d := by
  induction l generalizing k with
  | nil => right; rfl
  | cons a l ih =>
    cases k with
    | zero => left; exact List.mem_cons_self
    | succ j =>
      have e : nth d (a :: l) (j + 1) = nth d l j := rfl
      rw [e]
      rcases ih j with h | h
      · left; exact List.mem_cons_of_mem a h
      · right; exact h

lemma SP.sign_cases (p : SP) (m : Nat) (c : Cell) : p.sign m c = 0 ∨ p.sign m c = 1 ∨ p.sign m c = 2 := by
  unfold SP.sign SP.signMono SP.signSlope signOf
  cases Nat.beq m 0 <;> simp only [cond] <;> split <;> (try split) <;> simp

lemma dSP_eval (x y z : ℝ) : dSP.eval x y z = 0 := by simp [dSP, SP.eval, NP.eval]
lemma dSP_degOK : dSP.degOK = true := rfl

lemma Cell.mem_corner (c : Cell) : c.Mem ((c.ix : ℝ) / 2 ^ c.dx) ((c.iy : ℝ) / 2 ^ c.dy) ((c.iz : ℝ) / 2 ^ c.dz) := by
  refine ⟨le_rfl, ?_, le_rfl, ?_, le_rfl, ?_⟩ <;> gcongr <;> linarith

lemma Chart.degOK_F {C : Chart} (h : C.degOK = true) {p : SP} (hp : p ∈ C.F) : p.degOK = true := by
  unfold Chart.degOK at h; simp only [Bool.and_eq_true, List.all_eq_true] at h; exact h.1 p hp
lemma Chart.degOK_T {C : Chart} (h : C.degOK = true) {q : SP × SP} (hq : q ∈ C.T) :
    q.1.degOK = true ∧ q.2.degOK = true := by
  unfold Chart.degOK at h; simp only [Bool.and_eq_true, List.all_eq_true] at h; exact h.2 q hq

/-- a polynomial whose sign code is nonzero on a cell is nonzero on it; at the default it is impossible -/
lemma sign_ne (p : SP) (hd : p.degOK = true) (m : Nat) (c : Cell) (h : 0 < p.sign m c) (x y z : ℝ) (hc : c.Mem x y z) :
    p.eval x y z ≠ 0 := by
  have hs := p.sign_sound hd m c x y z hc
  rcases p.sign_cases m c with h0 | h1 | h2
  · omega
  · exact (hs.1 h1).ne'
  · exact (hs.2 h2).ne

lemma leafF_sound (C : Chart) (hdeg : C.degOK = true) (k m : Nat) (c : Cell) (h : C.leafF k m c = true) :
    C.Covered c := by
  intro x y z hc
  unfold Chart.leafF at h; rw [Nat.blt_eq] at h
  rcases nth_mem_or dSP C.F k with hm | hm
  · exact Or.inl ⟨_, hm, sign_ne _ (Chart.degOK_F hdeg hm) m c h x y z hc⟩
  · exfalso
    rw [hm] at h
    exact sign_ne dSP dSP_degOK m c h x y z hc (dSP_eval x y z)

lemma leafT_sound (C : Chart) (hdeg : C.degOK = true) (k mN mD : Nat) (c : Cell) (h : C.leafT k mN mD c = true) :
    C.Covered c := by
  intro x y z hc
  unfold Chart.leafT at h
  simp only [Bool.or_eq_true, Bool.and_eq_true, Nat.beq_eq] at h
  have key : ∀ q : SP × SP, q.1.degOK = true → q.2.degOK = true →
      ((q.1.sign mN c = 1 ∧ q.2.sign mD c = 2) ∨ (q.1.sign mN c = 2 ∧ q.2.sign mD c = 1)) →
      q.1.eval x y z * q.2.eval x y z < 0 := by
    intro q h1 h2 hh
    have sN := q.1.sign_sound h1 mN c x y z hc
    have sD := q.2.sign_sound h2 mD c x y z hc
    rcases hh with ⟨a, b⟩ | ⟨a, b⟩
    · exact mul_neg_of_pos_of_neg (sN.1 a) (sD.2 b)
    · exact mul_neg_of_neg_of_pos (sN.2 a) (sD.1 b)
  rcases nth_mem_or (dSP, dSP) C.T k with hm | hm
  · obtain ⟨h1, h2⟩ := Chart.degOK_T hdeg hm
    exact Or.inr (Or.inl ⟨_, hm, key _ h1 h2 h⟩)
  · exfalso
    rw [hm] at h
    have := key (dSP, dSP) dSP_degOK dSP_degOK h
    simp [dSP_eval] at this

lemma inIv_sound {d i l lq h hq : Nat} (hb : inIv d i l lq h hq = true) {x : ℝ}
    (h1 : (i : ℝ) / 2 ^ d ≤ x) (h2 : x ≤ ((i : ℝ) + 1) / 2 ^ d) : (l : ℝ) ≤ x * lq ∧ x * hq ≤ h := by
  unfold inIv at hb
  simp only [Bool.and_eq_true, Nat.ble_eq] at hb
  obtain ⟨a, b⟩ := hb
  have a' : (l : ℝ) * 2 ^ d ≤ i * lq := by exact_mod_cast a
  have b' : ((i : ℝ) + 1) * hq ≤ h * 2 ^ d := by exact_mod_cast b
  have hd : (0 : ℝ) < 2 ^ d := by positivity
  have hlq : (0 : ℝ) ≤ lq := Nat.cast_nonneg _
  have hhq : (0 : ℝ) ≤ hq := Nat.cast_nonneg _
  constructor
  · have e1 : (i : ℝ) / 2 ^ d * lq ≤ x * lq := mul_le_mul_of_nonneg_right h1 hlq
    have e2 : (l : ℝ) ≤ (i : ℝ) / 2 ^ d * lq := by rw [div_mul_eq_mul_div, le_div_iff₀ hd]; linarith
    linarith
  · have e1 : x * hq ≤ ((i : ℝ) + 1) / 2 ^ d * hq := mul_le_mul_of_nonneg_right h2 hhq
    have e2 : ((i : ℝ) + 1) / 2 ^ d * hq ≤ h := by rw [div_mul_eq_mul_div, div_le_iff₀ hd]; linarith
    linarith

lemma HB.contains_sound (hb : HB) (c : Cell) (h : hb.contains c = true) (x y z : ℝ) (hc : c.Mem x y z) :
    hb.Mem x y z := by
  unfold HB.contains at h
  simp only [Bool.and_eq_true] at h
  obtain ⟨⟨hx, hy⟩, hz⟩ := h
  obtain ⟨x1, x2, y1, y2, z1, z2⟩ := hc
  obtain ⟨a1, a2⟩ := inIv_sound hx x1 x2
  obtain ⟨b1, b2⟩ := inIv_sound hy y1 y2
  obtain ⟨c1, c2⟩ := inIv_sound hz z1 z2
  exact ⟨a1, a2, b1, b2, c1, c2⟩

lemma dHB_contains (c : Cell) : dHB.contains c = false := by
  unfold HB.contains dHB inIv
  cases h : Nat.ble (1 * 2 ^ c.dx) (c.ix * 0)
  · simp
  · exfalso; rw [Nat.ble_eq] at h; simp at h

lemma leafH_sound (C : Chart) (k : Nat) (c : Cell) (h : C.leafH k c = true) : C.Covered c := by
  intro x y z hc
  unfold Chart.leafH at h
  rcases nth_mem_or dHB C.H k with hm | hm
  · exact Or.inr (Or.inr ⟨_, hm, HB.contains_sound _ c h x y z hc⟩)
  · rw [hm, dHB_contains] at h; exact absurd h (by simp)


lemma split1 {d i : Nat} {x : ℝ} (h1 : (i : ℝ) / 2 ^ d ≤ x) (h2 : x ≤ ((i : ℝ) + 1) / 2 ^ d) :
    ((((2 * i + 0 : Nat) : ℝ) / 2 ^ (d + 1) ≤ x ∧ x ≤ (((2 * i + 0 : Nat) : ℝ) + 1) / 2 ^ (d + 1))) ∨
    ((((2 * i + 1 : Nat) : ℝ) / 2 ^ (d + 1) ≤ x ∧ x ≤ (((2 * i + 1 : Nat) : ℝ) + 1) / 2 ^ (d + 1))) := by
  have e0 : (((2 * i + 0 : Nat) : ℝ)) / 2 ^ (d + 1) = (i : ℝ) / 2 ^ d := by
    rw [Nat.add_zero]; push_cast; rw [pow_succ]; field_simp
  have e2 : (((2 * i + 1 : Nat) : ℝ) + 1) / 2 ^ (d + 1) = ((i : ℝ) + 1) / 2 ^ d := by
    push_cast; rw [pow_succ]; field_simp; ring
  have e1 : (((2 * i + 0 : Nat) : ℝ) + 1) = ((2 * i + 1 : Nat) : ℝ) := by push_cast; ring
  rcases le_total x (((2 * i + 1 : Nat) : ℝ) / 2 ^ (d + 1)) with h | h
  · left; rw [e0, e1]; exact ⟨h1, h⟩
  · right; rw [e2]; exact ⟨h, h2⟩

lemma split_mem (c : Cell) (x y z : ℝ) (hc : c.Mem x y z) : (c.split 0).Mem x y z ∨ (c.split 1).Mem x y z := by
  obtain ⟨x1, x2, y1, y2, z1, z2⟩ := hc
  unfold Cell.split
  cases (Nat.ble c.dx c.dy && Nat.ble c.dx c.dz)
  · cases Nat.ble c.dy c.dz
    · simp only [cond]
      rcases split1 z1 z2 with ⟨a, b⟩ | ⟨a, b⟩
      · left; exact ⟨x1, x2, y1, y2, a, b⟩
      · right; exact ⟨x1, x2, y1, y2, a, b⟩
    · simp only [cond]
      rcases split1 y1 y2 with ⟨a, b⟩ | ⟨a, b⟩
      · left; exact ⟨x1, x2, a, b, z1, z2⟩
      · right; exact ⟨x1, x2, a, b, z1, z2⟩
  · simp only [cond]
    rcases split1 x1 x2 with ⟨a, b⟩ | ⟨a, b⟩
    · left; exact ⟨a, b, y1, y2, z1, z2⟩
    · right; exact ⟨a, b, y1, y2, z1, z2⟩

lemma Chart.covered_split (C : Chart) (c : Cell) (h0 : C.Covered (c.split 0)) (h1 : C.Covered (c.split 1)) :
    C.Covered c := by
  intro x y z hc
  rcases split_mem c x y z hc with h | h
  · exact h0 x y z h
  · exact h1 x y z h

lemma go_sound (C : Chart) (hdeg : C.degOK = true) (fuel : Nat) :
    ∀ (c : Cell) (t r : TC), go C fuel c t = some r → C.Covered c := by
  induction fuel with
  | zero => intro c t r h; exact absurd h (by simp [go])
  | succ n ih =>
    intro c t r h
    cases t with
    | done => exact absurd h (by simp [go])
    | node t =>
      have e : go C (n + 1) c (.node t) =
          Option.casesOn (motive := fun _ => Option TC) (go C n (c.split 0) t) none (fun t' => go C n (c.split 1) t') := rfl
      rw [e] at h
      cases h0 : go C n (c.split 0) t with
      | none => rw [h0] at h; exact absurd h (by simp)
      | some t' =>
        rw [h0] at h
        exact C.covered_split c (ih _ _ _ h0) (ih _ _ _ h)
    | leafF k m t =>
      have e : go C (n + 1) c (.leafF k m t) = cond (C.leafF k m c) (some t) none := rfl
      rw [e] at h
      cases hb : C.leafF k m c
      · rw [hb] at h; exact absurd h (by simp)
      · exact leafF_sound C hdeg k m c hb
    | leafT k mN mD t =>
      have e : go C (n + 1) c (.leafT k mN mD t) = cond (C.leafT k mN mD c) (some t) none := rfl
      rw [e] at h
      cases hb : C.leafT k mN mD c
      · rw [hb] at h; exact absurd h (by simp)
      · exact leafT_sound C hdeg k mN mD c hb
    | leafH k t =>
      have e : go C (n + 1) c (.leafH k t) = cond (C.leafH k c) (some t) none := rfl
      rw [e] at h
      cases hb : C.leafH k c
      · rw [hb] at h; exact absurd h (by simp)
      · exact leafH_sound C k c hb

theorem checkTree_sound (C : Chart) (hdeg : C.degOK = true) (fuel : Nat) (c : Cell) (t : TC)
    (h : checkTree C fuel c t = true) : C.Covered c := by
  unfold checkTree at h
  cases hg : go C fuel c t with
  | none => rw [hg] at h; exact absurd h (by simp)
  | some r => exact go_sound C hdeg fuel c t r hg

/-- the root cell is the unit cube -/
theorem Chart.good_of_root (C : Chart) (h : C.Covered ⟨0, 0, 0, 0, 0, 0⟩) (x y z : ℝ)
    (hx : 0 ≤ x ∧ x ≤ 1) (hy : 0 ≤ y ∧ y ≤ 1) (hz : 0 ≤ z ∧ z ≤ 1) : C.Good x y z :=
  h x y z ⟨by simpa using hx.1, by simpa using hx.2, by simpa using hy.1, by simpa using hy.2,
    by simpa using hz.1, by simpa using hz.2⟩

end YantraCert
