/-
Dehn–Hadwiger study, part 13: the invariant of the regular 600-cell (DICTO, 20 Nov 2026).

* `adj_class`: two facets of the 600-cell across a triangle (normals of squared length 8 with dot product
  −2 + 6φ) meet at the dihedral angle 4π/3 − arccos(1/4): the 600-cell's angle is 4π/3 minus the 5-cell's.
* `cell600_pair`: at every ridge point of the 600-cell the two facets that give the angle are neighbours across a
  triangle. Proof: take the facet `p`, its corners `v j` and its neighbours `n j` (part 12's checked data). If a
  neighbour is tight too, it lies in the plane of the two tight normals and so is the other one
  (`eq_of_mem_span_pair`). If no neighbour is tight, the point is inside the facet: a barycentric combination of the
  four corners with positive weights (`facet_bary`); the second tight facet then contains all four corners, so its
  normal is the normal of `p`, against independence.
* `dehnHadwiger_cell600_eq`: the invariant is (area of the ridge points) ⊗ (4π/3 − arccos(1/4)).
No `sorry`.
-/
import DehnHadwiger.DH12Data
import DehnHadwiger.DH7Cell5

open scoped RealInnerProductSpace
open Set MeasureTheory Measure Module TensorProduct DehnCanon

namespace DehnHadwiger


/-! ### From the whole-number checks to facts about vectors -/

lemma gval_sub (c d : ℤ × ℤ) : gval (c - d) = gval c - gval d := by
  unfold gval; simp only [Prod.fst_sub, Prod.snd_sub]; push_cast; ring

lemma gval_gmul (c d : ℤ × ℤ) : gval (gmul c d) = gval c * gval d := gval_mul c d

/-- `z` is one of the 600 normals. -/
def NZ (z : Fin 4 → ℤ × ℤ) : Prop := ∃ k < 600, (L8get k).toZ = z

/-- `w` is one of the 120 corners, doubled. -/
def CZ (w : Fin 4 → ℤ × ℤ) : Prop := ∃ c < 120, (V8get c).toZ = w

/-- The facet `k`, a corner of it, and the facet across the triangle opposite that corner. -/
def recP (k : ℕ) : Fin 4 → ℤ × ℤ := (L8get k).toZ
def recV (k j : ℕ) : Fin 4 → ℤ × ℤ := (V8get ((recs600.getD k []).getD j 0)).toZ
def recN (k j : ℕ) : Fin 4 → ℤ × ℤ := (L8get ((recs600.getD k []).getD (j + 4) 0)).toZ

attribute [local irreducible] L8get V8get recs600 idx600 pos600 tab0 tab1 tab2 words120 rep120

lemma key8_inj {p q : Q8} (h : key8 p = key8 q) : p = q := by
  cases p; cases q
  simp only [key8, List.cons.injEq, and_true] at h
  obtain ⟨h0, h1, h2, h3, h4, h5, h6, h7⟩ := h
  subst h0 h1 h2 h3 h4 h5 h6 h7; rfl

lemma mem_L600 {z : Fin 4 → ℤ × ℤ} (hz : z ∈ cell600Z) : NZ z := by
  obtain ⟨p, hp, rfl⟩ := List.mem_iff_getElem.1 hz
  obtain ⟨h1, h2⟩ := zipOK_get cell600Z idx600 p chk_zip hp
  refine ⟨_, h2, ?_⟩
  rw [List.getD_eq_getElem _ _ hp] at h1
  exact (eq_of_key h1).symm

lemma L600_sub {z : Fin 4 → ℤ × ℤ} (hz : NZ z) : z ∈ cell600Z := by
  obtain ⟨k, hk, rfl⟩ := hz
  obtain ⟨hl, -, -, -, -, hpl, hcl⟩ := chk_lengths
  obtain ⟨e1, e2⟩ := posOK_get pos600 0 k chk_pos (by rw [hpl]; exact hk)
  rw [zero_add] at e1
  obtain ⟨f1, -⟩ := zipOK_get cell600Z idx600 _ chk_zip (by rw [hcl]; exact e2)
  rw [e1] at f1
  rw [← eq_of_key f1]
  have hp2 : pos600.getD k 0 < cell600Z.length := by rw [hcl]; exact e2
  rw [List.getD_eq_getElem _ _ hp2]; exact List.getElem_mem hp2

lemma inner_self_L600 {z : Fin 4 → ℤ × ℤ} (hz : NZ z) : ⟪gvec z, gvec z⟫ = 8 := by
  obtain ⟨k, hk, rfl⟩ := hz
  have h := List.all_eq_true.1 chk_norm k (List.mem_range.2 hk)
  rw [beq_iff_eq] at h
  rw [inner_gvec, gdot_toZ, h]; simp [gval]

lemma gvec_ne_zero_L600 {z : Fin 4 → ℤ × ℤ} (hz : NZ z) : gvec z ≠ 0 := by
  intro h; have := inner_self_L600 hz; rw [h, inner_zero_left] at this; norm_num at this

lemma gen_closed (g : ℕ) {q : Q8} (hq : ∃ k < 600, L8get k = q) : ∃ k < 600, L8get k = gen g q := by
  obtain ⟨k, hk, rfl⟩ := hq
  obtain ⟨l0, l1, l2, -⟩ := (⟨chk_lengths.2.1, chk_lengths.2.2.1, chk_lengths.2.2.2.1, trivial⟩ :
    tab0.length = 600 ∧ tab1.length = 600 ∧ tab2.length = 600 ∧ True)
  obtain ⟨t0, t1, t2⟩ := chk_tabs
  have key : ∀ (h : ℕ) (ts : List ℕ), tabOK h ts 0 = true → ts.length = 600 → gen g = gen h →
      ∃ k' < 600, L8get k' = gen g (L8get k) := by
    intro h ts ht hl hg
    obtain ⟨e1, e2⟩ := tabOK_get h ts 0 k ht (by rw [hl]; exact hk)
    rw [zero_add] at e1
    exact ⟨_, e2, by rw [hg]; exact (key8_inj e1).symm⟩
  match g with
  | 0 => exact key 0 tab0 t0 l0 rfl
  | 1 => exact key 1 tab1 t1 l1 rfl
  | n + 2 => exact key 2 tab2 t2 l2 rfl

lemma applyW_closed : ∀ (w : List ℕ) {q : Q8}, (∃ k < 600, L8get k = q) → ∃ k < 600, L8get k = applyW w q
  | [], _, h => h
  | g :: w, _, h => applyW_closed w (gen_closed g h)

lemma dot8_gen (g : ℕ) (p q : Q8) : dot8 (gen g p) (gen g q) = dot8 p q := by
  match g with
  | 0 => simp only [gen, dot8]; ext <;> ring
  | 1 => simp only [gen, dot8]; ext <;> ring
  | n + 2 => simp only [gen, dot8]; ext <;> ring

lemma dot8_applyW : ∀ (w : List ℕ) (p q : Q8), dot8 (applyW w p) (applyW w q) = dot8 p q
  | [], _, _ => rfl
  | g :: w, p, q => by simp only [applyW]; rw [dot8_applyW w, dot8_gen]

lemma corner_le {w z : Fin 4 → ℤ × ℤ} (hw : CZ w) (hz : NZ z) :
    ⟪gvec z, (1 / 2 : ℝ) • gvec w⟫ ≤ 1 := by
  obtain ⟨c, hc, rfl⟩ := hw
  obtain ⟨k, hk, rfl⟩ := hz
  obtain ⟨e1, e2⟩ := cornerOK_get words120 rep120 0 c chk_corners (by rw [chk_lengths.2.2.2.2.1]; exact hc)
  rw [zero_add] at e1
  obtain ⟨k', hk', hk'e⟩ := applyW_closed (words120.getD c []) ⟨k, hk, rfl⟩
  have hd : dot8 (L8get k) (V8get c) = dot8 (L8get k') (V8get (rep120.getD c 0)) := by
    rw [← dot8_applyW (words120.getD c []), hk'e, key8_inj e1]
  have h : gnonneg ((2, 0) - dot8 (L8get k') (V8get (rep120.getD c 0))) = true :=
    List.all_eq_true.1 (List.all_eq_true.1 chk_reps _ e2) k' (List.mem_range.2 hk')
  have h1 := gnonneg_sound h
  rw [gval_sub, ← hd] at h1
  have h2 : gval ((2 : ℤ), (0 : ℤ)) = 2 := by simp [gval]
  rw [inner_half_gvec, gdot_toZ]; rw [h2] at h1; linarith

/-- Four ℤ[φ] vectors whose sum, doubled, is `(−2 + 6φ)` times a fifth: the same for the real vectors. -/
lemma sum_gvec {n0 n1 n2 n3 p : Fin 4 → ℤ × ℤ}
    (h : ∀ m, gmul (2, 0) (n0 m + n1 m + n2 m + n3 m) = gmul (-2, 6) (p m)) :
    gvec n0 + gvec n1 + gvec n2 + gvec n3 = (gval (-2, 6) / 2) • gvec p := by
  have e : ∀ m, gval (n0 m) + gval (n1 m) + gval (n2 m) + gval (n3 m) = gval (-2, 6) / 2 * gval (p m) := by
    intro m
    have := congrArg gval (h m)
    rw [gval_gmul, gval_gmul, gval_add, gval_add, gval_add] at this
    have h2 : gval ((2 : ℤ), (0 : ℤ)) = 2 := by simp [gval]
    rw [h2] at this; linarith
  ext m
  fin_cases m <;> simp [gvec, e]

/-- The checked facts for the facet `k`, as vector facts. -/
structure RecFacts (k : ℕ) : Prop where
  vin : ∀ j < 4, (recs600.getD k []).getD j 0 < 120
  nin : ∀ j < 4, (recs600.getD k []).getD (j + 4) 0 < 600
  pv : ∀ j < 4, gdot (recP k) (recV k j) = (2, 0)
  pn : ∀ j < 4, gdot (recP k) (recN k j) = (-2, 6)
  nv : ∀ i < 4, ∀ j < 4, gdot (recN k i) (recV k j) = if i = j then (-8, 6) else (2, 0)
  sum : ∀ m, gmul (2, 0) (recN k 0 m + recN k 1 m + recN k 2 m + recN k 3 m) = gmul (-2, 6) (recP k m)

lemma recFacts {k : ℕ} (hk : k < 600) : RecFacts k := by
  have h := recsOK_get recs600 0 k chk_recs (by rw [chk_lengths.1]; exact hk)
  rw [zero_add] at h
  simp only [recOK, Bool.and_eq_true, List.all_eq_true, List.mem_range, beq_iff_eq, decide_eq_true_eq] at h
  obtain ⟨⟨h1, h2⟩, h3⟩ := h
  refine ⟨fun j hj => (h1 j hj).1.1.1, fun j hj => (h1 j hj).1.1.2, fun j hj => ?_, fun j hj => ?_,
    fun i hi j hj => ?_, fun m => ?_⟩
  · simp only [recP, recV, gdot_toZ]; exact (h1 j hj).1.2
  · simp only [recP, recN, gdot_toZ]; exact (h1 j hj).2
  · simp only [recN, recV, gdot_toZ]; exact h2 i hi j hj
  · simp only [recN, recP]; exact congrFun (veq_sound h3) m

lemma recV_mem {k j : ℕ} (hk : k < 600) (hj : j < 4) : CZ (recV k j) := ⟨_, (recFacts hk).vin j hj, rfl⟩

lemma recN_mem {k j : ℕ} (hk : k < 600) (hj : j < 4) : NZ (recN k j) := ⟨_, (recFacts hk).nin j hj, rfl⟩

lemma exists_rec {z : Fin 4 → ℤ × ℤ} (hz : NZ z) : ∃ k < 600, recP k = z := hz

/-! ### The angle between neighbouring facets -/

lemma arccos_quarter_ge : Real.pi / 3 ≤ Real.arccos (1 / 4) := by
  by_contra h
  push Not at h
  have := Real.cos_lt_cos_of_nonneg_of_le_pi (Real.arccos_nonneg _) (by linarith [Real.pi_pos]) h
  rw [Real.cos_arccos (by norm_num) (by norm_num), Real.cos_pi_div_three] at this
  norm_num at this

/-- **The 600-cell's dihedral angle.** Two facets with normals of squared length 8 and dot product −2 + 6φ meet at
the angle 4π/3 − arccos(1/4). -/
lemma adj_class {z w : Fin 4 → ℤ × ℤ} (hz : ⟪gvec z, gvec z⟫ = 8) (hw : ⟪gvec w, gvec w⟫ = 8)
    (hzw : gdot z w = (-2, 6)) :
    (Submodule.Quotient.mk (Real.pi - InnerProductGeometry.angle (gvec z) (gvec w)) : Angle) =
      Submodule.Quotient.mk (4 * Real.pi / 3 - Real.arccos (1 / 4)) := by
  have hz' : ‖gvec z‖ ^ 2 = 8 := by rw [← real_inner_self_eq_norm_sq]; exact hz
  have hw' : ‖gvec w‖ ^ 2 = 8 := by rw [← real_inner_self_eq_norm_sq]; exact hw
  have hnn : ‖gvec z‖ * ‖gvec w‖ = 8 := by
    have h0 : 0 ≤ ‖gvec z‖ * ‖gvec w‖ := by positivity
    have h1 : (‖gvec z‖ * ‖gvec w‖) ^ 2 = 64 := by rw [mul_pow, hz', hw']; norm_num
    nlinarith
  have s5 : √5 * √5 = 5 := Real.mul_self_sqrt (by norm_num)
  have hr : √(1 - (1 / 4 : ℝ) ^ 2) * √3 = 3 * √5 / 4 := by
    rw [← Real.sqrt_mul (by norm_num), show (1 - (1 / 4 : ℝ) ^ 2) * 3 = (3 / 4) ^ 2 * 5 by norm_num,
      Real.sqrt_mul (by positivity), Real.sqrt_sq (by norm_num)]
    ring
  have hcos : Real.cos (Real.arccos (1 / 4) - Real.pi / 3) = gval (-2, 6) / 8 := by
    rw [Real.cos_sub, Real.cos_arccos (by norm_num) (by norm_num), Real.sin_arccos, Real.cos_pi_div_three,
      Real.sin_pi_div_three, gval_eq]
    have : √(1 - (1 / 4 : ℝ) ^ 2) * (√3 / 2) = 3 * √5 / 8 := by rw [← mul_div_assoc, hr]; ring
    rw [this]; push_cast; ring
  have hang : InnerProductGeometry.angle (gvec z) (gvec w) = Real.arccos (1 / 4) - Real.pi / 3 := by
    unfold InnerProductGeometry.angle
    rw [inner_gvec, hzw, hnn, ← hcos, Real.arccos_cos (by linarith [arccos_quarter_ge])
      (by linarith [Real.arccos_le_pi (1 / 4), Real.pi_pos])]
  rw [hang]; congr 1; ring

lemma angle600_not_ratPi : 4 * Real.pi / 3 - Real.arccos (1 / 4) ∉ ratPi := by
  intro h
  apply arccos_quarter_not_ratPi
  have h43 : 4 * Real.pi / 3 ∈ ratPi := (mem_ratPi_iff _).2 ⟨4 / 3, by push_cast; ring⟩
  have := ratPi.sub_mem h43 h
  rwa [sub_sub_cancel] at this

/-! ### The ridge points of the 600-cell -/

lemma c600_lt : gval (-8, 6) / 2 < 1 := by
  rw [gval_eq]
  have : √5 < 7 / 3 := (Real.sqrt_lt' (by norm_num)).2 (by norm_num)
  push_cast; linarith

lemma c600_pos : 0 < gval (-8, 6) / 2 := by
  rw [gval_eq]
  have : 5 / 3 < √5 := (Real.lt_sqrt (by norm_num)).2 (by norm_num)
  push_cast; linarith

/-- **At a ridge point of the 600-cell the two facets are neighbours across a triangle.** -/
theorem cell600_pair {x : R4} (hx : x ∈ cell600) {p q : {z // z ∈ cell600Z}}
    (hp : p ∈ act (fun z : {z // z ∈ cell600Z} => gvec z.1) (fun _ => 1) x)
    (hq : q ∈ act (fun z : {z // z ∈ cell600Z} => gvec z.1) (fun _ => 1) x)
    (hli : LinearIndependent ℝ ![gvec p.1, gvec q.1])
    (hspan : ∀ r ∈ act (fun z : {z // z ∈ cell600Z} => gvec z.1) (fun _ => 1) x,
      gvec r.1 ∈ Submodule.span ℝ (Set.range ![gvec p.1, gvec q.1])) :
    (Submodule.Quotient.mk (Real.pi - InnerProductGeometry.angle (gvec p.1) (gvec q.1)) : Angle) =
      Submodule.Quotient.mk (4 * Real.pi / 3 - Real.arccos (1 / 4)) := by
  have hpL := mem_L600 p.2
  have hqL := mem_L600 q.2
  obtain ⟨k, hk, hkp⟩ := exists_rec hpL
  have R := recFacts hk
  set c : ℝ := gval (-8, 6) / 2 with hc
  have hc1 : c ≠ 1 := c600_lt.ne
  have hc3 : c ≠ -3 := by linarith [c600_pos]
  let vR : Fin 4 → R4 := fun j => (1 / 2 : ℝ) • gvec (recV k j)
  let nR : Fin 4 → R4 := fun j => gvec (recN k j)
  have hpx : ⟪gvec p.1, x⟫ = 1 := by simpa only [act, Set.mem_ofPred_eq] using hp
  have hqx : ⟪gvec q.1, x⟫ = 1 := by simpa only [act, Set.mem_ofPred_eq] using hq
  have hxle : ∀ z (hz : z ∈ cell600Z), ⟪gvec z, x⟫ ≤ 1 := fun z hz => hx ⟨z, hz⟩
  have hpv : ∀ j : Fin 4, ⟪gvec p.1, vR j⟫ = 1 := by
    intro j
    show ⟪gvec p.1, (1 / 2 : ℝ) • gvec (recV k j)⟫ = 1
    rw [inner_half_gvec, ← hkp, R.pv j j.2]; simp [gval]
  have hnv : ∀ i j : Fin 4, ⟪nR i, vR j⟫ = if i = j then c else 1 := by
    intro i j
    show ⟪gvec (recN k i), (1 / 2 : ℝ) • gvec (recV k j)⟫ = _
    rw [inner_half_gvec, R.nv i i.2 j j.2]
    simp only [Fin.val_inj]
    split_ifs
    · rfl
    · simp [gval]
  have hsum : ∑ i, nR i = (3 + c) • gvec p.1 := by
    rw [← hkp, Fin.sum_univ_four]
    have h3 : (3 + c) = gval (-2, 6) / 2 := by rw [hc]; simp [gval]; ring
    rw [h3]
    exact sum_gvec R.sum
  by_cases hact : ∃ j : Fin 4, ⟪nR j, x⟫ = 1
  · obtain ⟨j, hj⟩ := hact
    have hjL := recN_mem hk j.2
    have hjact : (⟨recN k j, L600_sub hjL⟩ : {z // z ∈ cell600Z}) ∈
        act (fun z : {z // z ∈ cell600Z} => gvec z.1) (fun _ => 1) x := by
      simp only [act, Set.mem_ofPred_eq]; exact hj
    rcases eq_of_mem_span_pair (inner_self_L600 hpL) (inner_self_L600 hqL) (inner_self_L600 hjL) hpx hqx hj hli
      (hspan _ hjact) with h | h
    · exfalso
      have e1 := hnv j j
      rw [ite_eq_left rfl] at e1
      have e2 := hpv j
      change ⟪gvec (recN k j), vR j⟫ = c at e1
      rw [h] at e1
      exact hc1 (e1.symm.trans e2)
    · rw [← h, ← hkp]
      exact adj_class (by rw [hkp]; exact inner_self_L600 hpL) (inner_self_L600 hjL) (R.pn j j.2)
  · exfalso
    push Not at hact
    have hlt : ∀ j, ⟪nR j, x⟫ < 1 := fun j => lt_of_le_of_ne (hxle _ (L600_sub (recN_mem hk j.2))) (hact j)
    have hE : finrank ℝ R4 = 4 := by simp
    have bary := facet_bary hE hc1 hc3 hnv hsum hpx
    set μ : Fin 4 → ℝ := fun j => (1 - ⟪nR j, x⟫) / (1 - c) with hμ
    have hμpos : ∀ j, 0 < μ j := fun j => div_pos (by linarith [hlt j]) (by linarith [c600_lt])
    have hpsum : ∑ j, μ j = 1 := by
      have := congrArg (fun y => ⟪gvec p.1, y⟫) bary
      simp only [inner_sum, inner_smul_right, hpv, mul_one] at this
      rw [← this, hpx]
    have hqv : ∀ j, ⟪gvec q.1, vR j⟫ ≤ 1 := fun j => corner_le (recV_mem hk j.2) hqL
    have hqsum : ∑ j, μ j * ⟪gvec q.1, vR j⟫ = 1 := by
      have := congrArg (fun y => ⟪gvec q.1, y⟫) bary
      simp only [inner_sum, inner_smul_right] at this
      rw [← this, hqx]
    have hzero : ∑ j, μ j * (1 - ⟪gvec q.1, vR j⟫) = 0 := by
      simp only [mul_sub, mul_one, Finset.sum_sub_distrib, hpsum, hqsum, sub_self]
    have hterm := (Finset.sum_eq_zero_iff_of_nonneg (fun j _ =>
      mul_nonneg (hμpos j).le (by linarith [hqv j]))).1 hzero
    have hqv1 : ∀ j, ⟪gvec q.1 - gvec p.1, vR j⟫ = 0 := by
      intro j
      have h1 := hterm j (Finset.mem_univ _)
      rcases mul_eq_zero.1 h1 with h | h
      · exact absurd h (hμpos j).ne'
      · rw [inner_sub_left, hpv j]; linarith
    have hvind : LinearIndependent ℝ vR :=
      linIndep_of_pairing hc1 hc3 (n := vR) (v := nR) (fun i j => by
        rw [real_inner_comm, hnv j i]
        simp only [eq_comm])
    have hz := eq_zero_of_inner_four hE hvind (fun j => by rw [real_inner_comm]; exact hqv1 j)
    rw [sub_eq_zero] at hz
    have := LinearIndependent.pair_iff.1 hli 1 (-1) (by rw [hz]; simp)
    exact one_ne_zero this.1

/-- **The invariant of the regular 600-cell**: (area of its ridge points) ⊗ (4π/3 − arccos(1/4)). -/
theorem dehnHadwiger_cell600_eq : dehnHadwiger cell600 =
    (μH[(finrank ℝ R4 - 2 : ℕ)]
      {x | ridgeAngle cell600 x = Submodule.Quotient.mk (4 * Real.pi / 3 - Real.arccos (1 / 4))}).toReal
      ⊗ₜ[ℚ] (Submodule.Quotient.mk (4 * Real.pi / 3 - Real.arccos (1 / 4)) : Angle) := by
  unfold cell600
  apply dehnHadwiger_sol_eq_single_ridge _ _ (fun z => gvec_ne_zero_L600 (mem_L600 z.2))
  intro x hx p hp q hq hli hspan
  exact cell600_pair hx hp hq hli hspan

end DehnHadwiger
