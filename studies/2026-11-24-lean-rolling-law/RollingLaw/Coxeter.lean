/-
# The rolling law in Mathlib's Coxeter groups

Given a Coxeter system `cs : CoxeterSystem M W` (Mathlib) and a roll model `R`
for `M` whose rolls satisfy the Coxeter relations (`Lifts`), we prove, in
general:
* `RollModel.face`: the map `W → α`, `w ↦ face of w`, with
  `face (π ω) = roll ω o` (`face_wordProd`);
* `RollModel.faceEquiv`: it is a bijection (so `Nat.card W = Nat.card α`);
* `RollModel.length_eq`: Mathlib's length `cs.length w` is the distance `d (face w)`;
* `RollModel.matsumoto_cs`: Matsumoto's theorem for `cs` — two reduced words
  (`cs.IsReduced`) with the same product are joined by braid moves;
* `RollModel.reduce_cs`: every word is brought to a reduced word with the same
  product by braid moves and cancellations `i i ↦ []`.
-/
import RollingLaw.Basic

namespace RollingLaw

open CoxeterSystem (alternatingWord)

variable {B : Type*} {M : CoxeterMatrix B} {α : Type*}

namespace RollModel
variable (R : RollModel M α)

/-- The rolls satisfy the Coxeter relations: going `M i j` times round the
corner `i, j` returns every face to itself. -/
def Lifts : Prop := ∀ i j x, (fun y => R.r i (R.r j y))^[M i j] x = x

/-- The roll across edges of type `i`, as a permutation of the faces. -/
def rPerm (i : B) : Equiv.Perm α := Function.Involutive.toPerm (R.r i) (R.r_r i)

theorem isLiftable (h : R.Lifts) : M.IsLiftable R.rPerm := by
  intro i j
  ext x
  rw [Equiv.Perm.coe_pow, Equiv.Perm.one_apply]
  exact h i j x

variable {W : Type*} [Group W] (cs : CoxeterSystem M W)

/-- Braid-equivalent words have the same product (Mathlib's braid relation). -/
theorem wordProd_eq_of_braidEq {u v : List B} (h : BraidEq M u v) :
    cs.wordProd u = cs.wordProd v := by
  induction h with
  | rel a b hab =>
    obtain ⟨p, q, i, j⟩ := hab
    have hb := cs.wordProd_braidWord_eq i j
    simp only [CoxeterSystem.braidWord] at hb
    rw [M.symmetric j i] at hb
    simp only [cs.wordProd_append, hb]
  | refl => rfl
  | symm _ _ _ ih => exact ih.symm
  | trans _ _ _ _ _ ih ih' => exact ih.trans ih'

variable (hL : R.Lifts)
include cs hL

/-- The action of `W` on the faces. -/
noncomputable def act : W →* Equiv.Perm α := cs.lift ⟨R.rPerm, R.isLiftable hL⟩

/-- The face of `w`: the face reached from the base face by any word for `w`. -/
noncomputable def face (w : W) : α := R.act cs hL w⁻¹ R.o

theorem face_mul_simple (w : W) (i : B) : R.face cs hL (w * cs.simple i) = R.r i (R.face cs hL w) := by
  simp only [face, mul_inv_rev, CoxeterSystem.inv_simple, map_mul, Equiv.Perm.coe_mul,
    Function.comp_apply]
  rw [act, cs.lift_apply_simple]
  rfl

theorem face_one : R.face cs hL 1 = R.o := by simp [face]

theorem face_wordProd (ω : List B) : R.face cs hL (cs.wordProd ω) = roll R.r ω R.o := by
  induction ω using List.reverseRecOn with
  | nil => simp [CoxeterSystem.wordProd, face_one]
  | append_singleton u a ih =>
    rw [cs.wordProd_append, cs.wordProd_singleton, face_mul_simple, ih]; simp

/-- Every element is the product of the chosen shortest roll to its face. -/
theorem eq_wordProd_sw (w : W) : w = cs.wordProd (R.sw (R.face cs hL w)) := by
  induction w using cs.simple_induction_right with
  | one =>
    rw [face_one]
    have : R.sw R.o = [] := List.length_eq_zero_iff.mp (by rw [R.length_sw, R.d_o])
    simp [this]
  | mul_simple_right w i ih =>
    rw [face_mul_simple]
    set x := R.face cs hL w
    rcases R.d_r i x with hup | hdown
    · -- rolling away from the base face
      have h1 : R.Shortest (R.sw x ++ [i]) := by
        simp [Shortest, R.roll_sw, R.length_sw, hup]
      have h2 : R.Shortest (R.sw (R.r i x)) := by simp [Shortest, R.roll_sw, R.length_sw]
      have := wordProd_eq_of_braidEq cs (R.matsumoto_shortest h1 h2 (by simp [R.roll_sw]))
      rw [← this, cs.wordProd_append, cs.wordProd_singleton, ← ih]
    · -- rolling towards the base face
      have h1 : R.Shortest (R.sw (R.r i x) ++ [i]) := by
        simp [Shortest, R.roll_sw, R.length_sw, R.r_r, hdown]
      have h2 : R.Shortest (R.sw x) := by simp [Shortest, R.roll_sw, R.length_sw]
      have := wordProd_eq_of_braidEq cs (R.matsumoto_shortest h1 h2 (by simp [R.roll_sw, R.r_r]))
      rw [cs.wordProd_append, cs.wordProd_singleton, ← ih] at this
      rw [← this, mul_assoc, cs.simple_mul_simple_self, mul_one]

theorem face_injective : Function.Injective (R.face cs hL) := by
  intro w w' h
  rw [R.eq_wordProd_sw cs hL w, R.eq_wordProd_sw cs hL w', h]

theorem face_surjective : Function.Surjective (R.face cs hL) := fun x =>
  ⟨cs.wordProd (R.sw x), by rw [face_wordProd, R.roll_sw]⟩

/-- The faces of the die are the elements of the Coxeter group. -/
noncomputable def faceEquiv : W ≃ α :=
  Equiv.ofBijective _ ⟨R.face_injective cs hL, R.face_surjective cs hL⟩

theorem card_eq : Nat.card W = Nat.card α := Nat.card_congr (R.faceEquiv cs hL)

/-- Mathlib's Coxeter length is the rolling distance. -/
theorem length_eq (w : W) : cs.length w = R.d (R.face cs hL w) := by
  apply le_antisymm
  · conv_lhs => rw [R.eq_wordProd_sw cs hL w]
    exact (cs.length_wordProd_le _).trans (R.length_sw _).le
  · obtain ⟨ω, hω, rfl⟩ := cs.exists_isReduced w
    rw [hω.eq, face_wordProd]; exact R.d_le_length ω

theorem isReduced_iff (ω : List B) : cs.IsReduced ω ↔ R.Shortest ω := by
  rw [CoxeterSystem.IsReduced, R.length_eq cs hL, R.face_wordProd cs hL, Shortest]

/-- **Matsumoto's theorem** for `cs`: two reduced words with the same product
are joined by braid moves. -/
theorem matsumoto_cs {ω ω' : List B} (hω : cs.IsReduced ω) (hω' : cs.IsReduced ω')
    (h : cs.wordProd ω = cs.wordProd ω') : BraidEq M ω ω' := by
  rw [R.isReduced_iff cs hL] at hω hω'
  refine R.matsumoto_shortest hω hω' ?_
  rw [← face_wordProd R cs hL, ← face_wordProd R cs hL, h]

/-- **Word reduction** for `cs`: every word is brought to a reduced word with the
same product by braid moves and cancellations. -/
theorem reduce_cs (ω : List B) : ∃ ω', Relation.ReflTransGen (MoveStep M) ω ω' ∧
    cs.IsReduced ω' ∧ cs.wordProd ω' = cs.wordProd ω := by
  obtain ⟨ω', h1, h2, h3⟩ := R.reduce ω
  refine ⟨ω', h1, (R.isReduced_iff cs hL ω').mpr h2, R.face_injective cs hL ?_⟩
  rw [face_wordProd, face_wordProd, h3]

end RollModel

end RollingLaw
