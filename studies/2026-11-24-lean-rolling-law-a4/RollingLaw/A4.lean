/-
# The A4 die (120 faces): the combinatorial rolling law, mirrors, transitivity

The A4 die is the polar of the A4 permutahedron (corners: the 120 permutations of
(5,4,3,2,1)). Its faces are `Fin 120`; rolling across a ridge of type `i` (`i = 0..3`) is the
table `Data.A4.rt`. Mathlib's Coxeter matrix is `CoxeterMatrix.A 4` (there is no separate
`A₄`). Every finite condition is checked by the Lean kernel (`decide +kernel`; no
`native_decide`); the general theorems (`RollingLaw.Basic`, `RollingLaw.Coxeter`,
`RollingLaw.General`) then give:
* `roll_corner`, `corner_injective`, `corner_perm`: face `x` is dual to the corner
  `corner x` of the permutahedron (120 distinct permutations of (5,4,3,2,1)), and rolling across
  the ridge of type `i` swaps the entries `5 - i`, `4 - i` (one edge of the permutahedron);
* `card_group` (120), `length_le` (10), `existsUnique_length_eq` (one longest element);
* `matsumoto`, `reduce`, `rolling_law`, `rolling_reduce`: the rolling law;
* `card_mirrors` (10), `longest_crosses_each_once`;
* `transitive`, `transitive_unique`: the roll-preserving symmetries act simply transitively.
Not proved here: that the tables are the facets and ridges of the convex die in ℝ⁴ (the
geometric step M4; see the README).
-/
import RollingLaw.General
import RollingLaw.Data.A4

namespace RollingLaw

open CoxeterSystem (alternatingWord)

namespace A4

/-- The Coxeter matrix (Mathlib). -/
abbrev M : CoxeterMatrix (Fin 4) := CoxeterMatrix.A 4

/-- Rolling the A4 die across a ridge of type `i`. -/
def r (i : Fin 4) (x : Fin 120) : Fin 120 :=
  ⟨((Data.A4.rt.getD i.val []).getD x.val 0) % 120, Nat.mod_lt _ (by decide)⟩

/-- The rolling distance from face 0. -/
def d (x : Fin 120) : ℕ := Data.A4.dt.getD x.val 0

/-- The corner of the permutahedron dual to face `x`. -/
def corner (x : Fin 120) : List ℕ := Data.A4.corner.getD x.val []

/-- Swapping the values `5 - i` and `4 - i`: one edge of the permutahedron. -/
def swapv (i : Fin 4) (v : ℕ) : ℕ :=
  if v = 5 - i.val then 4 - i.val else if v = 4 - i.val then 5 - i.val else v

/-- Face 0 is dual to the corner (5,4,3,2,1). -/
theorem corner_zero : corner 0 = [5, 4, 3, 2, 1] := by decide +kernel

/-- Every face is dual to a permutation of (5,4,3,2,1). -/
theorem corner_perm : ∀ x, (corner x).isPerm [5, 4, 3, 2, 1] = true := by decide +kernel

/-- Different faces are dual to different corners (so all 120 permutations occur). -/
theorem corner_injective : ∀ x y, corner x = corner y → x = y := by decide +kernel

/-- Rolling across the ridge of type `i` follows the edge of the permutahedron that swaps the
values `5 - i` and `4 - i` (right multiplication by the simple reflection `s_i`). -/
theorem roll_corner : ∀ i x, corner (r i x) = (corner x).map (swapv i) := by decide +kernel

/-- The roll model of the A4 die; every field is a kernel check. -/
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
    intro i j; fin_cases i <;> fin_cases j <;> simp [M, CoxeterMatrix.A]
  corner := by decide +kernel

/-- The rolls satisfy the Coxeter relations of `M`. -/
theorem lifts : model.Lifts := by
  unfold RollModel.Lifts; decide +kernel

/-- Every face is at distance at most 10, and exactly one face is at distance 10. -/
theorem d_le : ∀ x, model.d x ≤ 10 := by decide +kernel
theorem d_top : ∃ x, model.d x = 10 ∧ ∀ y, model.d y = 10 → y = x := by decide +kernel

/-- Mathlib's Coxeter system of `M`. -/
abbrev cs : CoxeterSystem M M.Group := M.toCoxeterSystem

/-- The Coxeter group `A4` has 120 elements. -/
theorem card_group : Nat.card M.Group = 120 := by
  rw [model.card_eq cs lifts, Nat.card_eq_fintype_card, Fintype.card_fin]

/-- Every element has length at most 10. -/
theorem length_le (w : M.Group) : cs.length w ≤ 10 := by
  rw [model.length_eq cs lifts]; exact d_le _

/-- Exactly one element has length 10 (the longest element). -/
theorem existsUnique_length_eq : ∃! w : M.Group, cs.length w = 10 := by
  obtain ⟨x, hx, hu⟩ := d_top
  refine ⟨(model.faceEquiv cs lifts).symm x, ?_, fun w hw => ?_⟩
  · show cs.length _ = _
    rw [model.length_eq cs lifts]
    exact (congrArg model.d ((model.faceEquiv cs lifts).apply_symm_apply x)).trans hx
  · apply (model.faceEquiv cs lifts).injective
    rw [Equiv.apply_symm_apply]
    exact hu _ ((model.length_eq cs lifts w).symm.trans hw)

/-- **Matsumoto's theorem for A4.** -/
theorem matsumoto {ω ω' : List (Fin 4)} (hω : cs.IsReduced ω) (hω' : cs.IsReduced ω')
    (h : cs.wordProd ω = cs.wordProd ω') : BraidEq M ω ω' :=
  model.matsumoto_cs cs lifts hω hω' h

/-- **Word reduction for A4.** -/
theorem reduce (ω : List (Fin 4)) : ∃ ω', Relation.ReflTransGen (MoveStep M) ω ω' ∧
    cs.IsReduced ω' ∧ cs.wordProd ω' = cs.wordProd ω :=
  model.reduce_cs cs lifts ω

/-- **The rolling law on the A4 die.** Two shortest rolls between the same two faces are joined
by corner moves. -/
theorem rolling_law {f g : Fin 120} {ω ω' : List (Fin 4)} (h : model.ShortestRoll f g ω)
    (h' : model.ShortestRoll f g ω') : BraidEq M ω ω' :=
  model.rolling_law cs lifts h h'

/-- Every roll is brought to a shortest roll between the same two faces by corner moves and
cancelling back-and-forth rolls. -/
theorem rolling_reduce (f : Fin 120) (ω : List (Fin 4)) :
    ∃ ω', Relation.ReflTransGen (MoveStep M) ω ω' ∧ model.ShortestRoll f (roll r ω f) ω' :=
  model.rolling_reduce cs lifts f ω

/-! ### Mirrors -/

/-- the tabled shortest roll to each face -/
def nf (x : Fin 120) : List (Fin 4) :=
  ((Data.A4.word.getD x.val []).map fun i => ⟨i % 4, Nat.mod_lt _ (by decide)⟩)

theorem roll_nf : ∀ x, roll r (nf x) 0 = x := by decide +kernel

theorem card_mirrors_q : (Finset.univ.image fun p : Fin 120 × Fin 4 =>
    roll r (nf p.1 ++ [p.2] ++ (nf p.1).reverse) 0).card = 10 := by decide +kernel

/-- **A4 has 10 mirrors.** -/
theorem card_mirrors : Nat.card {t : M.Group // cs.IsReflection t} = 10 := by
  rw [model.card_reflections cs lifts nf roll_nf]; exact card_mirrors_q

open Classical in
/-- **The longest shortest roll crosses every mirror exactly once**, from any face. -/
theorem longest_crosses_each_once {ω : List (Fin 4)} (hω : cs.IsReduced ω) (hl : ω.length = 10)
    (w : M.Group) {t : M.Group} (ht : cs.IsReflection t) : (mirrorsCrossed cs w ω).count t = 1 := by
  have : Fintype M.Group := Fintype.ofEquiv _ (model.faceEquiv cs lifts).symm
  exact crosses_each_once cs card_mirrors hω hl w t ht

/-! ### Transitivity (the combinatorial half of fairness) -/

/-- **Any face can be taken to any other** by a permutation of the 120 faces that commutes with
every roll. -/
theorem transitive (x y : Fin 120) :
    ∃ σ : Fin 120 ≃ Fin 120, σ x = y ∧ ∀ i z, σ (r i z) = r i (σ z) :=
  model.transitive cs lifts x y

/-- Such a permutation is determined by the image of one face (with `transitive`: one such permutation for each target face). -/
theorem transitive_unique (σ τ : Fin 120 → Fin 120) (hσ : ∀ i z, σ (r i z) = r i (σ z))
    (hτ : ∀ i z, τ (r i z) = r i (τ z)) (x : Fin 120) (h : σ x = τ x) : σ = τ :=
  model.transitive_unique σ τ hσ hτ x h

end A4

end RollingLaw
