/-
# The three fair dice: kernel-checked roll models

For each of the reflection groups A3, B3, H3 (Mathlib's `CoxeterMatrix.A 3`,
`CoxeterMatrix.B 3`, `CoxeterMatrix.H₃`) the faces of the die are `Fin N`
(N = 24, 48, 120) and the rolls are the tables of `RollingLaw.Data`.  Every
condition of `RollModel` and of `RollModel.Lifts` is a finite statement about
the tables, checked by the Lean kernel (`decide +kernel`; no `native_decide`).
The general theorems of `RollingLaw.Basic` and `RollingLaw.Coxeter` then give,
for each group:
* the generators (the rolls) are permutations of the N faces satisfying the
  Coxeter relations (`lifts`), so they generate a copy of the Coxeter group;
* `card_group`: the Coxeter group has exactly N elements;
* `length_le`, `exists_length_eq`: the longest element has length 6, 9, 15;
* `matsumoto`, `reduce`: Matsumoto's theorem and word reduction for Mathlib's
  Coxeter system of that matrix.
-/
import RollingLaw.Coxeter
import RollingLaw.Data.A3
import RollingLaw.Data.B3
import RollingLaw.Data.H3

namespace RollingLaw

open CoxeterSystem (alternatingWord)

/-! ## A3: the tetrakis hexahedron (24 faces) -/
namespace A3

/-- The Coxeter matrix (Mathlib). -/
abbrev M : CoxeterMatrix (Fin 3) := CoxeterMatrix.A 3

/-- Rolling the tetrakis hexahedron across an edge of type `i`. -/
def r (i : Fin 3) (x : Fin 24) : Fin 24 :=
  ⟨((Data.A3.rt.getD i.val []).getD x.val 0) % 24, Nat.mod_lt _ (by decide)⟩

/-- The rolling distance from face 0. -/
def d (x : Fin 24) : ℕ := Data.A3.dt.getD x.val 0

/-- The roll model of the tetrakis hexahedron; every field is a kernel check. -/
def model : RollModel M (Fin 24) where
  r := r
  o := 0
  d := d
  r_r := by decide +kernel
  d_r := by decide +kernel
  d_o := by decide +kernel
  eq_o := by decide +kernel
  down := by decide +kernel
  m_pos := by
    intro i j; fin_cases i <;> fin_cases j <;> simp [M, CoxeterMatrix.A]
  corner := by decide +kernel

/-- The rolls satisfy the Coxeter relations of `M`. -/
theorem lifts : model.Lifts := by
  unfold RollModel.Lifts; decide +kernel

/-- Every face is at distance at most 6, and exactly one face is at distance 6. -/
theorem d_le : ∀ x, model.d x ≤ 6 := by decide +kernel
theorem d_top : ∃ x, model.d x = 6 ∧ ∀ y, model.d y = 6 → y = x := by decide +kernel

/-- Mathlib's Coxeter system of `M`. -/
abbrev cs : CoxeterSystem M M.Group := M.toCoxeterSystem

/-- The Coxeter group `A3` has 24 elements. -/
theorem card_group : Nat.card M.Group = 24 := by
  rw [model.card_eq cs lifts, Nat.card_eq_fintype_card, Fintype.card_fin]

/-- Every element has length at most 6. -/
theorem length_le (w : M.Group) : cs.length w ≤ 6 := by
  rw [model.length_eq cs lifts]; exact d_le _

/-- Exactly one element has length 6 (the longest element). -/
theorem existsUnique_length_eq : ∃! w : M.Group, cs.length w = 6 := by
  obtain ⟨x, hx, hu⟩ := d_top
  refine ⟨(model.faceEquiv cs lifts).symm x, ?_, fun w hw => ?_⟩
  · show cs.length _ = _
    rw [model.length_eq cs lifts]
    exact (congrArg model.d ((model.faceEquiv cs lifts).apply_symm_apply x)).trans hx
  · apply (model.faceEquiv cs lifts).injective
    rw [Equiv.apply_symm_apply]
    exact hu _ ((model.length_eq cs lifts w).symm.trans hw)

/-- **Matsumoto's theorem for A3.** -/
theorem matsumoto {ω ω' : List (Fin 3)} (hω : cs.IsReduced ω) (hω' : cs.IsReduced ω')
    (h : cs.wordProd ω = cs.wordProd ω') : BraidEq M ω ω' :=
  model.matsumoto_cs cs lifts hω hω' h

/-- **Word reduction for A3.** -/
theorem reduce (ω : List (Fin 3)) : ∃ ω', Relation.ReflTransGen (MoveStep M) ω ω' ∧
    cs.IsReduced ω' ∧ cs.wordProd ω' = cs.wordProd ω :=
  model.reduce_cs cs lifts ω

end A3

/-! ## B3: the disdyakis dodecahedron (48 faces) -/
namespace B3

/-- The Coxeter matrix (Mathlib). -/
abbrev M : CoxeterMatrix (Fin 3) := CoxeterMatrix.B 3

/-- Rolling the disdyakis dodecahedron across an edge of type `i`. -/
def r (i : Fin 3) (x : Fin 48) : Fin 48 :=
  ⟨((Data.B3.rt.getD i.val []).getD x.val 0) % 48, Nat.mod_lt _ (by decide)⟩

/-- The rolling distance from face 0. -/
def d (x : Fin 48) : ℕ := Data.B3.dt.getD x.val 0

/-- The roll model of the disdyakis dodecahedron; every field is a kernel check. -/
def model : RollModel M (Fin 48) where
  r := r
  o := 0
  d := d
  r_r := by decide +kernel
  d_r := by decide +kernel
  d_o := by decide +kernel
  eq_o := by decide +kernel
  down := by decide +kernel
  m_pos := by
    intro i j; fin_cases i <;> fin_cases j <;> simp [M, CoxeterMatrix.B]
  corner := by decide +kernel

/-- The rolls satisfy the Coxeter relations of `M`. -/
theorem lifts : model.Lifts := by
  unfold RollModel.Lifts; decide +kernel

/-- Every face is at distance at most 9, and exactly one face is at distance 9. -/
theorem d_le : ∀ x, model.d x ≤ 9 := by decide +kernel
theorem d_top : ∃ x, model.d x = 9 ∧ ∀ y, model.d y = 9 → y = x := by decide +kernel

/-- Mathlib's Coxeter system of `M`. -/
abbrev cs : CoxeterSystem M M.Group := M.toCoxeterSystem

/-- The Coxeter group `B3` has 48 elements. -/
theorem card_group : Nat.card M.Group = 48 := by
  rw [model.card_eq cs lifts, Nat.card_eq_fintype_card, Fintype.card_fin]

/-- Every element has length at most 9. -/
theorem length_le (w : M.Group) : cs.length w ≤ 9 := by
  rw [model.length_eq cs lifts]; exact d_le _

/-- Exactly one element has length 9 (the longest element). -/
theorem existsUnique_length_eq : ∃! w : M.Group, cs.length w = 9 := by
  obtain ⟨x, hx, hu⟩ := d_top
  refine ⟨(model.faceEquiv cs lifts).symm x, ?_, fun w hw => ?_⟩
  · show cs.length _ = _
    rw [model.length_eq cs lifts]
    exact (congrArg model.d ((model.faceEquiv cs lifts).apply_symm_apply x)).trans hx
  · apply (model.faceEquiv cs lifts).injective
    rw [Equiv.apply_symm_apply]
    exact hu _ ((model.length_eq cs lifts w).symm.trans hw)

/-- **Matsumoto's theorem for B3.** -/
theorem matsumoto {ω ω' : List (Fin 3)} (hω : cs.IsReduced ω) (hω' : cs.IsReduced ω')
    (h : cs.wordProd ω = cs.wordProd ω') : BraidEq M ω ω' :=
  model.matsumoto_cs cs lifts hω hω' h

/-- **Word reduction for B3.** -/
theorem reduce (ω : List (Fin 3)) : ∃ ω', Relation.ReflTransGen (MoveStep M) ω ω' ∧
    cs.IsReduced ω' ∧ cs.wordProd ω' = cs.wordProd ω :=
  model.reduce_cs cs lifts ω

end B3

/-! ## H3: the disdyakis triacontahedron (120 faces) -/
namespace H3

/-- The Coxeter matrix (Mathlib). -/
abbrev M : CoxeterMatrix (Fin 3) := CoxeterMatrix.H₃

/-- Rolling the disdyakis triacontahedron across an edge of type `i`. -/
def r (i : Fin 3) (x : Fin 120) : Fin 120 :=
  ⟨((Data.H3.rt.getD i.val []).getD x.val 0) % 120, Nat.mod_lt _ (by decide)⟩

/-- The rolling distance from face 0. -/
def d (x : Fin 120) : ℕ := Data.H3.dt.getD x.val 0

/-- The roll model of the disdyakis triacontahedron; every field is a kernel check. -/
def model : RollModel M (Fin 120) where
  r := r
  o := 0
  d := d
  r_r := by decide +kernel
  d_r := by decide +kernel
  d_o := by decide +kernel
  eq_o := by decide +kernel
  down := by decide +kernel
  m_pos := by
    intro i j; fin_cases i <;> fin_cases j <;> simp [M, CoxeterMatrix.H₃]
  corner := by decide +kernel

/-- The rolls satisfy the Coxeter relations of `M`. -/
theorem lifts : model.Lifts := by
  unfold RollModel.Lifts; decide +kernel

/-- Every face is at distance at most 15, and exactly one face is at distance 15. -/
theorem d_le : ∀ x, model.d x ≤ 15 := by decide +kernel
theorem d_top : ∃ x, model.d x = 15 ∧ ∀ y, model.d y = 15 → y = x := by decide +kernel

/-- Mathlib's Coxeter system of `M`. -/
abbrev cs : CoxeterSystem M M.Group := M.toCoxeterSystem

/-- The Coxeter group `H3` has 120 elements. -/
theorem card_group : Nat.card M.Group = 120 := by
  rw [model.card_eq cs lifts, Nat.card_eq_fintype_card, Fintype.card_fin]

/-- Every element has length at most 15. -/
theorem length_le (w : M.Group) : cs.length w ≤ 15 := by
  rw [model.length_eq cs lifts]; exact d_le _

/-- Exactly one element has length 15 (the longest element). -/
theorem existsUnique_length_eq : ∃! w : M.Group, cs.length w = 15 := by
  obtain ⟨x, hx, hu⟩ := d_top
  refine ⟨(model.faceEquiv cs lifts).symm x, ?_, fun w hw => ?_⟩
  · show cs.length _ = _
    rw [model.length_eq cs lifts]
    exact (congrArg model.d ((model.faceEquiv cs lifts).apply_symm_apply x)).trans hx
  · apply (model.faceEquiv cs lifts).injective
    rw [Equiv.apply_symm_apply]
    exact hu _ ((model.length_eq cs lifts w).symm.trans hw)

/-- **Matsumoto's theorem for H3.** -/
theorem matsumoto {ω ω' : List (Fin 3)} (hω : cs.IsReduced ω) (hω' : cs.IsReduced ω')
    (h : cs.wordProd ω = cs.wordProd ω') : BraidEq M ω ω' :=
  model.matsumoto_cs cs lifts hω hω' h

/-- **Word reduction for H3.** -/
theorem reduce (ω : List (Fin 3)) : ∃ ω', Relation.ReflTransGen (MoveStep M) ω ω' ∧
    cs.IsReduced ω' ∧ cs.wordProd ω' = cs.wordProd ω :=
  model.reduce_cs cs lifts ω

end H3

end RollingLaw
