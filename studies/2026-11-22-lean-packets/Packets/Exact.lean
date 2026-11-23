/-
Lean formalization of DICTO's paper #117 (Zenodo 10.5281/zenodo.24411660). Exact arithmetic in ℤ[√d] for the
generated solids, checked by evaluation.

A number `x.1 + x.2 √d` is coded by a pair of integers (`Zd`), a vector of `ℝ³` by three such pairs (`V3`).
`ev`, `evv` give their real values; `zadd`, `zmul`, `zdot`, `det3` compute on codes, and `ev_add`, `ev_mul`,
`inner_evv`, `ind_of_det` say the codes compute the real values. `zpos` decides `0 < x.1 + x.2 √d` from integer
inequalities (`zpos_spec`). A solid given by integer codes (`Solid`) then gets its edge data (`IsEdgeData`),
boundedness and an interior point from tables checked by `decide +kernel`: every equation and sign is an integer
computation, so the proofs stay small (`isEdgeData_of`, `bounded_of`, `interior_of`).
No `sorry`.
-/
module

public import Packets.Canon.Dehn7Dodeca

@[expose] public section

open scoped RealInnerProductSpace
open Set

namespace PacketsGen

open DehnCanon.Library

/-- A number `x.1 + x.2 √d` with integer coordinates. -/
abbrev Zd := ℤ × ℤ

/-- A vector of `ℝ³` with coordinates in `ℤ[√d]`. -/
abbrev V3 := Fin 3 → Zd

section Arith

variable (d : ℕ)

noncomputable def ev (x : Zd) : ℝ := (x.1 : ℝ) + (x.2 : ℝ) * √(d : ℝ)

def zadd (x y : Zd) : Zd := (x.1 + y.1, x.2 + y.2)

def zsub (x y : Zd) : Zd := (x.1 - y.1, x.2 - y.2)

def zmul (x y : Zd) : Zd := (x.1 * y.1 + d * x.2 * y.2, x.1 * y.2 + x.2 * y.1)

lemma ev_add (x y : Zd) : ev d (zadd x y) = ev d x + ev d y := by simp only [ev, zadd]; push_cast; ring

lemma ev_sub (x y : Zd) : ev d (zsub x y) = ev d x - ev d y := by simp only [ev, zsub]; push_cast; ring

lemma ev_mul (x y : Zd) : ev d (zmul d x y) = ev d x * ev d y := by
  have h : √(d : ℝ) ^ 2 = d := Real.sq_sqrt (Nat.cast_nonneg d)
  simp only [ev, zmul]; push_cast
  linear_combination (-(x.2 : ℝ) * y.2) * h

/-- A certified test for `0 < x.1 + x.2 √d`. -/
def zpos (x : Zd) : Bool :=
  if 0 ≤ x.1 then (if 0 ≤ x.2 then decide (0 < x.1 ∨ 0 < x.2) else decide ((d : ℤ) * x.2 * x.2 < x.1 * x.1))
  else (if 0 < x.2 then decide (x.1 * x.1 < (d : ℤ) * x.2 * x.2) else false)

lemma zpos_spec {d : ℕ} (hd : 0 < d) {x : Zd} (h : zpos d x = true) : 0 < ev d x := by
  have hs : 0 < √(d : ℝ) := Real.sqrt_pos.2 (by exact_mod_cast hd)
  have h2 : √(d : ℝ) ^ 2 = d := Real.sq_sqrt (Nat.cast_nonneg d)
  unfold zpos at h; unfold ev
  split_ifs at h with h1 h3 h4
  · have h1' : (0 : ℝ) ≤ x.1 := by exact_mod_cast h1
    have h3' : (0 : ℝ) ≤ x.2 := by exact_mod_cast h3
    rcases of_decide_eq_true h with h | h
    · have : (0 : ℝ) < x.1 := by exact_mod_cast h
      nlinarith
    · have : (0 : ℝ) < x.2 := by exact_mod_cast h
      nlinarith
  · have h1' : (0 : ℝ) ≤ x.1 := by exact_mod_cast h1
    have h3' : (x.2 : ℝ) < 0 := by exact_mod_cast (lt_of_not_ge h3)
    have hq : (d : ℝ) * x.2 * x.2 < x.1 * x.1 := by exact_mod_cast of_decide_eq_true h
    by_contra hn
    push Not at hn
    have ht : (x.1 : ℝ) ≤ -(x.2 * √(d : ℝ)) := by linarith
    have hm := mul_self_le_mul_self h1' ht
    have e : -((x.2 : ℝ) * √(d : ℝ)) * -(x.2 * √(d : ℝ)) = d * x.2 * x.2 := by
      rw [show -((x.2 : ℝ) * √(d : ℝ)) * -(x.2 * √(d : ℝ)) = x.2 * x.2 * √(d : ℝ) ^ 2 by ring, h2]; ring
    linarith
  · have h1' : (x.1 : ℝ) < 0 := by exact_mod_cast (lt_of_not_ge h1)
    have h4' : (0 : ℝ) < x.2 := by exact_mod_cast h4
    have hq : (x.1 : ℝ) * x.1 < d * x.2 * x.2 := by exact_mod_cast of_decide_eq_true h
    by_contra hn
    push Not at hn
    have ht : (x.2 : ℝ) * √(d : ℝ) ≤ -x.1 := by linarith
    have hm := mul_self_le_mul_self (by positivity) ht
    have e : (x.2 : ℝ) * √(d : ℝ) * (x.2 * √(d : ℝ)) = d * x.2 * x.2 := by
      rw [show (x.2 : ℝ) * √(d : ℝ) * (x.2 * √(d : ℝ)) = x.2 * x.2 * √(d : ℝ) ^ 2 by ring, h2]; ring
    linarith

/-- A certified test for `0 ≤ x.1 + x.2 √d`. -/
def znn (x : Zd) : Bool := (x.1 == 0 && x.2 == 0) || zpos d x

lemma znn_spec {d : ℕ} (hd : 0 < d) {x : Zd} (h : znn d x = true) : 0 ≤ ev d x := by
  unfold znn at h
  rcases Bool.or_eq_true_iff.1 h with h | h
  · simp only [Bool.and_eq_true, beq_iff_eq] at h
    simp [ev, h.1, h.2]
  · exact (zpos_spec hd h).le

/-- A certified test for `x.1 + x.2 √d ≠ 0`. -/
def zne (x : Zd) : Bool := zpos d x || zpos d (-x.1, -x.2)

lemma zne_spec {d : ℕ} (hd : 0 < d) {x : Zd} (h : zne d x = true) : ev d x ≠ 0 := by
  unfold zne at h
  rcases Bool.or_eq_true_iff.1 h with h | h
  · exact (zpos_spec hd h).ne'
  · have := zpos_spec hd h
    have e : ev d (-x.1, -x.2) = -ev d x := by simp only [ev]; push_cast; ring
    rw [e] at this; linarith

/-! ### Vectors -/

noncomputable def evv (v : V3) : R3 := !₂[ev d (v 0), ev d (v 1), ev d (v 2)]

def zdot (u v : V3) : Zd := zadd (zadd (zmul d (u 0) (v 0)) (zmul d (u 1) (v 1))) (zmul d (u 2) (v 2))

lemma inner_evv (u v : V3) : ⟪evv d u, evv d v⟫ = ev d (zdot d u v) := by
  rw [evv, inner3, zdot, ev_add, ev_add, ev_mul, ev_mul, ev_mul]
  simp [evv]

/-- `a u + b v`. -/
def comb2 (a : Zd) (u : V3) (b : Zd) (v : V3) : V3 := fun t => zadd (zmul d a (u t)) (zmul d b (v t))

/-- `a u + b v + c w`. -/
def comb3 (a : Zd) (u : V3) (b : Zd) (v : V3) (c : Zd) (w : V3) : V3 :=
  fun t => zadd (zadd (zmul d a (u t)) (zmul d b (v t))) (zmul d c (w t))

lemma evv_comb2 (a : Zd) (u : V3) (b : Zd) (v : V3) :
    evv d (comb2 d a u b v) = ev d a • evv d u + ev d b • evv d v := by
  ext t; fin_cases t <;> simp [evv, comb2, ev_add, ev_mul]

lemma evv_comb3 (a : Zd) (u : V3) (b : Zd) (v : V3) (c : Zd) (w : V3) :
    evv d (comb3 d a u b v c w) = ev d a • evv d u + ev d b • evv d v + ev d c • evv d w := by
  ext t; fin_cases t <;> simp [evv, comb3, ev_add, ev_mul]

def veq (u v : V3) : Bool := u 0 == v 0 && u 1 == v 1 && u 2 == v 2

lemma veq_spec {u v : V3} (h : veq u v = true) : u = v := by
  simp only [veq, Bool.and_eq_true, beq_iff_eq] at h
  funext t; fin_cases t
  · exact h.1.1
  · exact h.1.2
  · exact h.2

/-- The determinant of three vectors. -/
def det3 (u v w : V3) : Zd :=
  zadd (zsub (zmul d (u 0) (zsub (zmul d (v 1) (w 2)) (zmul d (v 2) (w 1))))
    (zmul d (u 1) (zsub (zmul d (v 0) (w 2)) (zmul d (v 2) (w 0)))))
    (zmul d (u 2) (zsub (zmul d (v 0) (w 1)) (zmul d (v 1) (w 0))))

lemma ind_of_det {d : ℕ} (hd : 0 < d) {u v w : V3} (h : zne d (det3 d u v w) = true) (x : R3)
    (h1 : ⟪evv d u, x⟫ = 0) (h2 : ⟪evv d v, x⟫ = 0) (h3 : ⟪evv d w, x⟫ = 0) : x = 0 :=
  ind3 (D := ev d (det3 d u v w)) (by simp [evv, det3, ev_add, ev_sub, ev_mul]) (zne_spec hd h) x h1 h2 h3

end Arith

/-! ### Solids given by codes -/

/-- A solid given by integer codes: normals, offsets, corners, and for each edge its faces and corners. -/
structure Solid (d F K E : ℕ) where
  N : Fin F → V3
  B : Fin F → Zd
  P : Fin K → V3
  fi : Fin E → Fin F
  fj : Fin E → Fin F
  vk : Fin E → Fin K
  vl : Fin E → Fin K

/-- How two faces meet: along an edge, at one corner, or not at all (a Farkas certificate). -/
inductive Cert (F K E : ℕ) where
  | edge (e : Fin E) (c cp : Fin F)
  | corner (k : Fin K) (c cp : Fin F) (l μ a a' : Zd)
  | farkas (a a' : Zd) (c1 c2 c3 : Fin F) (μ1 μ2 μ3 : Zd)
  | none

/-- A bound `⟪λ u, x⟫ ≤ Σ μ b` for an axis direction `u`. -/
structure BCert (F : ℕ) where
  c1 : Fin F
  c2 : Fin F
  c3 : Fin F
  μ1 : Zd
  μ2 : Zd
  μ3 : Zd
  lam : Zd

namespace Solid

variable {d F K E : ℕ} (S : Solid d F K E)

noncomputable def n (m : Fin F) : R3 := evv d (S.N m)
noncomputable def b (m : Fin F) : ℝ := ev d (S.B m)
noncomputable def p (k : Fin K) : R3 := evv d (S.P k)

def tight (m : Fin F) (k : Fin K) : Bool := zdot d (S.N m) (S.P k) == S.B m

def below (m : Fin F) (k : Fin K) : Bool := zpos d (zsub (S.B m) (zdot d (S.N m) (S.P k)))

lemma tight_spec {m : Fin F} {k : Fin K} (h : S.tight m k = true) : ⟪S.n m, S.p k⟫ = S.b m := by
  simp only [tight, beq_iff_eq] at h
  rw [n, p, inner_evv, h, b]

lemma below_spec (hd : 0 < d) {m : Fin F} {k : Fin K} (h : S.below m k = true) :
    ⟪S.n m, S.p k⟫ < S.b m := by
  have := zpos_spec hd h
  rw [ev_sub] at this
  rw [n, p, inner_evv, b]; linarith

def certOK (i j : Fin F) : Cert F K E → Bool
  | .edge e c cp => S.fi e == i && S.fj e == j && S.tight i (S.vk e) && S.tight i (S.vl e) &&
      S.tight j (S.vk e) && S.tight j (S.vl e) && S.tight c (S.vl e) && S.below c (S.vk e) &&
      S.tight cp (S.vk e) && S.below cp (S.vl e) && zne d (det3 d (S.N i) (S.N j) (S.N c))
  | .corner k c cp l μ a a' => S.tight c k && S.tight cp k && S.tight i k && S.tight j k &&
      zne d (det3 d (S.N i) (S.N j) (S.N c)) && zpos d l && zpos d μ &&
      veq (comb2 d l (S.N c) μ (S.N cp)) (comb2 d a (S.N i) a' (S.N j))
  | .farkas a a' c1 c2 c3 μ1 μ2 μ3 => znn d μ1 && znn d μ2 && znn d μ3 &&
      veq (comb2 d a (S.N i) a' (S.N j)) (comb3 d μ1 (S.N c1) μ2 (S.N c2) μ3 (S.N c3)) &&
      zpos d (zsub (zadd (zmul d a (S.B i)) (zmul d a' (S.B j)))
        (zadd (zadd (zmul d μ1 (S.B c1)) (zmul d μ2 (S.B c2))) (zmul d μ3 (S.B c3))))
  | .none => false

lemma n_comb2 (a : Zd) (u : Fin F) (b : Zd) (v : Fin F) :
    evv d (comb2 d a (S.N u) b (S.N v)) = ev d a • S.n u + ev d b • S.n v := evv_comb2 d _ _ _ _

theorem cover_of_cert (hd : 0 < d) {i j : Fin F} {z : Cert F K E} (h : S.certOK i j z = true)
    {x : R3} (hx : x ∈ sol S.n S.b) (hi : ⟪S.n i, x⟫ = S.b i) (hj : ⟪S.n j, x⟫ = S.b j) :
    (∃ e, ({i, j} : Set (Fin F)) = {S.fi e, S.fj e} ∧ x ∈ segment ℝ (S.p (S.vk e)) (S.p (S.vl e))) ∨
      ∃ k, x = S.p k := by
  cases z with
  | edge e c cp =>
    simp only [certOK, Bool.and_eq_true, beq_iff_eq] at h
    obtain ⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨h1, h2⟩, t1⟩, t2⟩, t3⟩, t4⟩, t5⟩, b5⟩, t6⟩, b6⟩, hdet⟩ := h
    subst h1; subst h2
    exact Or.inl ⟨e, rfl, mem_segment_of_tight (n := S.n) (b := S.b) (i := S.fi e) (j := S.fj e) (c := c)
      (c' := cp) (ind_of_det hd hdet) (S.tight_spec t1) (S.tight_spec t2)
      (S.tight_spec t3) (S.tight_spec t4) (S.tight_spec t5) (S.below_spec hd b5) (S.tight_spec t6)
      (S.below_spec hd b6) hx hi hj⟩
  | corner k c cp l μ a a' =>
    simp only [certOK, Bool.and_eq_true] at h
    obtain ⟨⟨⟨⟨⟨⟨⟨t1, t2⟩, t3⟩, t4⟩, hdet⟩, hl⟩, hμ⟩, hv⟩ := h
    have hl' := zpos_spec hd hl
    have hrel := congrArg (evv d) (veq_spec hv)
    rw [S.n_comb2, S.n_comb2] at hrel
    refine Or.inr ⟨k, eq_of_tight (n := S.n) (b := S.b) (i := i) (j := j) (c := c) (c' := cp)
      (ind_of_det hd hdet) (S.tight_spec t1) (S.tight_spec t2) (S.tight_spec t3)
      (S.tight_spec t4) (μ := ev d μ / ev d l) (a := ev d a / ev d l) (a' := ev d a' / ev d l)
      (div_pos (zpos_spec hd hμ) hl') ?_ hx hi hj⟩
    have e1 : S.n c = (ev d l)⁻¹ • (ev d l • S.n c) := by
      rw [smul_smul, inv_mul_cancel₀ hl'.ne', one_smul]
    rw [e1, show ev d l • S.n c = ev d a • S.n i + ev d a' • S.n j - ev d μ • S.n cp by rw [← hrel]; abel]
    simp only [div_eq_inv_mul, mul_smul, smul_add, smul_sub]
    abel
  | farkas a a' c1 c2 c3 μ1 μ2 μ3 =>
    simp only [certOK, Bool.and_eq_true] at h
    obtain ⟨⟨⟨⟨h1, h2⟩, h3⟩, hv⟩, hg⟩ := h
    have hrel := congrArg (evv d) (veq_spec hv)
    rw [S.n_comb2, evv_comb3] at hrel
    have hg' := zpos_spec hd hg
    simp only [ev_sub, ev_add, ev_mul] at hg'
    exact (false_of_comb (n := S.n) (b := S.b) (znn_spec hd h1) (znn_spec hd h2) (znn_spec hd h3) hrel
      (by simp only [b]; linarith) hx hi hj).elim
  | none => simp [certOK] at h

/-- **Edge data from checked tables.** -/
theorem isEdgeData_of (hd : 0 < d) (hbd : Bornology.IsBounded (sol S.n S.b))
    (hmem : ∀ m k, S.tight m k = true ∨ S.below m k = true)
    (T : Fin K → Fin F × Fin F × Fin F)
    (hT : ∀ k, (T k).1 ≠ (T k).2.1 ∧ (T k).1 ≠ (T k).2.2 ∧ (T k).2.1 ≠ (T k).2.2 ∧
      S.tight (T k).1 k = true ∧ S.tight (T k).2.1 k = true ∧ S.tight (T k).2.2 k = true)
    (hlt : ∀ e, S.fi e < S.fj e) (hinj : ∀ e e', S.fi e = S.fi e' → S.fj e = S.fj e' → e = e')
    (htight : ∀ e, S.tight (S.fi e) (S.vk e) = true ∧ S.tight (S.fi e) (S.vl e) = true ∧
      S.tight (S.fj e) (S.vk e) = true ∧ S.tight (S.fj e) (S.vl e) = true)
    (hother : ∀ e m, m ≠ S.fi e → m ≠ S.fj e → S.below m (S.vk e) = true ∨ S.below m (S.vl e) = true)
    (Ct : Fin F → Fin F → Cert F K E) (hcov : ∀ i j, i < j → S.certOK i j (Ct i j) = true) :
    IsEdgeData S.n S.b S.p S.fi S.fj S.vk S.vl where
  bounded := hbd
  corner_mem := fun k m => by
    rcases hmem m k with h | h
    · exact (S.tight_spec h).le
    · exact (S.below_spec hd h).le
  corner_three := fun k => by
    obtain ⟨h1, h2, h3, t1, t2, t3⟩ := hT k
    exact ⟨_, _, _, h1, h2, h3, S.tight_spec t1, S.tight_spec t2, S.tight_spec t3⟩
  faces_ne := fun e => (hlt e).ne
  faces_inj := fun e e' h => by
    rcases Set.pair_eq_pair_iff.1 h with ⟨h1, h2⟩ | ⟨h1, h2⟩
    · exact hinj e e' h1 h2
    · have a := hlt e
      rw [h1, h2] at a
      exact absurd a (lt_asymm (hlt e'))
  tight := fun e => by
    obtain ⟨t1, t2, t3, t4⟩ := htight e
    exact ⟨S.tight_spec t1, S.tight_spec t2, S.tight_spec t3, S.tight_spec t4⟩
  other := fun e m h1 h2 => by
    rcases hother e m h1 h2 with h | h
    · exact Or.inl (S.below_spec hd h)
    · exact Or.inr (S.below_spec hd h)
  cover := fun x hx i j hij hi hj => by
    rcases lt_or_gt_of_ne hij with h | h
    · exact S.cover_of_cert hd (hcov i j h) hx hi hj
    · rcases S.cover_of_cert hd (hcov j i h) hx hj hi with ⟨e, he, hseg⟩ | hk
      · exact Or.inl ⟨e, (Set.pair_comm i j).trans he, hseg⟩
      · exact Or.inr hk

/-- The axis directions `±e₀, ±e₁, ±e₂`. -/
def axis : Fin 6 → V3 := ![![(1, 0), (0, 0), (0, 0)], ![(-1, 0), (0, 0), (0, 0)], ![(0, 0), (1, 0), (0, 0)],
  ![(0, 0), (-1, 0), (0, 0)], ![(0, 0), (0, 0), (1, 0)], ![(0, 0), (0, 0), (-1, 0)]]

def bOK (u : V3) (c : BCert F) : Bool :=
  znn d c.μ1 && znn d c.μ2 && znn d c.μ3 && zpos d c.lam &&
    veq (comb3 d c.μ1 (S.N c.c1) c.μ2 (S.N c.c2) c.μ3 (S.N c.c3)) (fun t => zmul d c.lam (u t))

/-- The bound given by a checked certificate: `⟪u, x⟫ ≤ Σ μ b / λ`. -/
lemma le_of_bcert (hd : 0 < d) {u : V3} {c : BCert F} (h : S.bOK u c = true) {x : R3}
    (hx : x ∈ sol S.n S.b) :
    ⟪evv d u, x⟫ ≤ (ev d c.μ1 * S.b c.c1 + ev d c.μ2 * S.b c.c2 + ev d c.μ3 * S.b c.c3) / ev d c.lam := by
  simp only [bOK, Bool.and_eq_true] at h
  obtain ⟨⟨⟨⟨h1, h2⟩, h3⟩, hl⟩, hv⟩ := h
  have hl' := zpos_spec hd hl
  have hrel := congrArg (evv d) (veq_spec hv)
  rw [evv_comb3] at hrel
  have hu : evv d (fun t => zmul d c.lam (u t)) = ev d c.lam • evv d u := by
    ext t; fin_cases t <;> simp [evv, ev_mul]
  rw [hu] at hrel
  have key : ev d c.lam * ⟪evv d u, x⟫ = ev d c.μ1 * ⟪S.n c.c1, x⟫ + ev d c.μ2 * ⟪S.n c.c2, x⟫ +
      ev d c.μ3 * ⟪S.n c.c3, x⟫ := by
    rw [← real_inner_smul_left, ← hrel]
    simp only [inner_add_left, real_inner_smul_left, n]
  rw [le_div_iff₀ hl', mul_comm, key]
  have e1 := mul_le_mul_of_nonneg_left (hx c.c1) (znn_spec hd h1)
  have e2 := mul_le_mul_of_nonneg_left (hx c.c2) (znn_spec hd h2)
  have e3 := mul_le_mul_of_nonneg_left (hx c.c3) (znn_spec hd h3)
  linarith

theorem bounded_of (hd : 0 < d) (Bc : Fin 6 → BCert F) (h : ∀ t, S.bOK (axis t) (Bc t) = true) :
    Bornology.IsBounded (sol S.n S.b) := by
  let M : Fin 6 → ℝ := fun t =>
    (ev d (Bc t).μ1 * S.b (Bc t).c1 + ev d (Bc t).μ2 * S.b (Bc t).c2 + ev d (Bc t).μ3 * S.b (Bc t).c3) /
      ev d (Bc t).lam
  refine bounded_of_coords (∑ t, |M t|) (fun x hx r => ?_)
  have hb : ∀ t, ⟪evv d (axis t), x⟫ ≤ |M t| := fun t => (S.le_of_bcert hd (h t) hx).trans (le_abs_self _)
  have hs : ∀ t, |M t| ≤ ∑ t, |M t| := fun t =>
    Finset.single_le_sum (f := fun t => |M t|) (fun _ _ => abs_nonneg _) (Finset.mem_univ t)
  have e0 : ⟪evv d (axis 0), x⟫ = x 0 := by simp [axis, evv, ev, inner3]
  have e1 : ⟪evv d (axis 1), x⟫ = -x 0 := by simp [axis, evv, ev, inner3]
  have e2 : ⟪evv d (axis 2), x⟫ = x 1 := by simp [axis, evv, ev, inner3]
  have e3 : ⟪evv d (axis 3), x⟫ = -x 1 := by simp [axis, evv, ev, inner3]
  have e4 : ⟪evv d (axis 4), x⟫ = x 2 := by simp [axis, evv, ev, inner3]
  have e5 : ⟪evv d (axis 5), x⟫ = -x 2 := by simp [axis, evv, ev, inner3]
  have a0 := hb 0; have a1 := hb 1; have a2 := hb 2; have a3 := hb 3; have a4 := hb 4; have a5 := hb 5
  rw [e0] at a0; rw [e1] at a1; rw [e2] at a2; rw [e3] at a3; rw [e4] at a4; rw [e5] at a5
  have s0 := hs 0; have s1 := hs 1; have s2 := hs 2; have s3 := hs 3; have s4 := hs 4; have s5 := hs 5
  rw [abs_le]
  fin_cases r
  · exact ⟨by simp only [Fin.zero_eta]; linarith, by simp only [Fin.zero_eta]; linarith⟩
  · exact ⟨by simp only [Fin.mk_one]; linarith, by simp only [Fin.mk_one]; linarith⟩
  · exact ⟨by simp only [Fin.reduceFinMk]; linarith, by simp only [Fin.reduceFinMk]; linarith⟩

/-- An interior point `z / λ` checked by integer signs. -/
theorem interior_of (hd : 0 < d) (z : V3) (lam : Zd) (hl : zpos d lam = true)
    (h : ∀ m, zpos d (zsub (zmul d lam (S.B m)) (zdot d (S.N m) z)) = true) :
    (interior (sol S.n S.b)).Nonempty := by
  have hl' := zpos_spec hd hl
  refine ⟨(ev d lam)⁻¹ • evv d z, mem_interior_iff_mem_nhds.2 (Filter.mem_of_superset ((isOpen_iInter_of_finite
    fun m => isOpen_lt (by fun_prop : Continuous fun x : R3 => ⟪S.n m, x⟫) continuous_const).mem_nhds
    (Set.mem_iInter.2 fun m => ?_)) fun x hx m => (Set.mem_iInter.1 hx m).le)⟩
  have := zpos_spec hd (h m)
  rw [ev_sub, ev_mul] at this
  show ⟪S.n m, (ev d lam)⁻¹ • evv d z⟫ < S.b m
  rw [real_inner_smul_right, n, inner_evv, b, inv_mul_lt_iff₀ hl']
  linarith

lemma inner_n (i j : Fin F) : ⟪S.n i, S.n j⟫ = ev d (zdot d (S.N i) (S.N j)) := inner_evv d _ _

end Solid

end PacketsGen
