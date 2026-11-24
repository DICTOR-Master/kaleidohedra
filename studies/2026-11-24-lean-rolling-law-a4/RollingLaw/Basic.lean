/-
# The rolling law: the general part

A *roll model* for a Coxeter matrix `M` on letters `B` is a set of faces `α`
with a base face `o`, a roll `r i : α → α` across each edge type `i`, and a
distance `d : α → ℕ`, subject to finitely many local conditions
(`RollModel`).  For a finite die every condition is a finite check.

From these local conditions alone we prove, in general:
* `RollModel.d_roll_le`, `RollModel.exists_shortest`: `d x` is the number of
  rolls on a shortest roll from `o` to `x`;
* `RollModel.matsumoto`: any two shortest rolls from `o` to the same face are
  joined by corner moves (braid moves, `BraidEq M`);
* `RollModel.reduce`: every roll from `o` is brought to a shortest roll with
  the same end face by corner moves and cancelling back-and-forth rolls.

No property of any particular die is used in this file.
-/
import Mathlib

namespace RollingLaw

open CoxeterSystem (alternatingWord)

variable {B : Type*}

/-- Rolling along the word `ω` from face `x` (letters applied left to right). -/
def roll {α : Type*} (r : B → α → α) (ω : List B) (x : α) : α :=
  ω.foldl (fun y i => r i y) x

section rollLemmas
variable {α : Type*} (r : B → α → α)

@[simp] theorem roll_nil (x : α) : roll r [] x = x := rfl

@[simp] theorem roll_append (u v : List B) (x : α) :
    roll r (u ++ v) x = roll r v (roll r u x) := by
  simp [roll, List.foldl_append]

@[simp] theorem roll_cons (i : B) (ω : List B) (x : α) : roll r (i :: ω) x = roll r ω (r i x) :=
  rfl

@[simp] theorem roll_singleton (i : B) (x : α) : roll r [i] x = r i x := rfl

theorem roll_reverse_roll (hr : ∀ i x, r i (r i x) = x) (ω : List B) (x : α) :
    roll r ω (roll r ω.reverse x) = x := by
  induction ω using List.reverseRecOn generalizing x with
  | nil => rfl
  | append_singleton u a ih =>
    simp only [List.reverse_append, List.reverse_cons, List.reverse_nil, List.nil_append,
      List.singleton_append, roll_append, roll_singleton]
    rw [show roll r (a :: u.reverse) x = roll r u.reverse (r a x) from rfl, ih, hr]

end rollLemmas

/-- One corner move (braid move): an alternating word of length `M i j` in the
letters `i, j` is replaced by the other one. -/
inductive BraidStep (M : CoxeterMatrix B) : List B → List B → Prop
  | mk (p q : List B) (i j : B) :
      BraidStep M (p ++ alternatingWord i j (M i j) ++ q) (p ++ alternatingWord j i (M i j) ++ q)

/-- Two words are joined by corner moves. -/
def BraidEq (M : CoxeterMatrix B) : List B → List B → Prop := Relation.EqvGen (BraidStep M)

/-- Cancelling a back-and-forth roll `i i`. -/
inductive CancelStep : List B → List B → Prop
  | mk (p q : List B) (i : B) : CancelStep (p ++ [i, i] ++ q) (p ++ q)

/-- One corner move or one cancellation. -/
def MoveStep (M : CoxeterMatrix B) (u v : List B) : Prop := BraidStep M u v ∨ CancelStep u v

namespace BraidEq
variable {M : CoxeterMatrix B}

theorem refl (u : List B) : BraidEq M u u := Relation.EqvGen.refl u
theorem symm {u v : List B} (h : BraidEq M u v) : BraidEq M v u := Relation.EqvGen.symm _ _ h
theorem trans {u v w : List B} (h : BraidEq M u v) (h' : BraidEq M v w) : BraidEq M u w :=
  Relation.EqvGen.trans _ _ _ h h'

/-- Corner moves may be made inside any longer word. -/
theorem append {u v : List B} (h : BraidEq M u v) (p q : List B) :
    BraidEq M (p ++ u ++ q) (p ++ v ++ q) := by
  induction h with
  | rel a b hab =>
    obtain ⟨p', q', i, j⟩ := hab
    refine Relation.EqvGen.rel _ _ ?_
    simpa [List.append_assoc] using BraidStep.mk (M := M) (p ++ p') (q' ++ q) i j
  | refl => exact Relation.EqvGen.refl _
  | symm _ _ _ ih => exact Relation.EqvGen.symm _ _ ih
  | trans _ _ _ _ _ ih ih' => exact Relation.EqvGen.trans _ _ _ ih ih'

theorem append_right {u v : List B} (h : BraidEq M u v) (q : List B) :
    BraidEq M (u ++ q) (v ++ q) := by simpa using h.append [] q

theorem _root_.RollingLaw.BraidStep.symm {u v : List B} (h : BraidStep M u v) :
    BraidStep M v u := by
  obtain ⟨p, q, i, j⟩ := h
  have := BraidStep.mk (M := M) p q j i
  rwa [M.symmetric j i] at this

/-- Corner-move-equivalent words are joined by a chain of single corner moves. -/
theorem moves {u v : List B} (h : BraidEq M u v) : Relation.ReflTransGen (MoveStep M) u v := by
  suffices Relation.ReflTransGen (MoveStep M) u v ∧ Relation.ReflTransGen (MoveStep M) v u from
    this.1
  induction h with
  | rel a b hab => exact ⟨.single (Or.inl hab), .single (Or.inl hab.symm)⟩
  | refl => exact ⟨.refl, .refl⟩
  | symm _ _ _ ih => exact ⟨ih.2, ih.1⟩
  | trans _ _ _ _ _ ih ih' => exact ⟨ih.1.trans ih'.1, ih'.2.trans ih.2⟩

end BraidEq


/-- A roll model of the Coxeter matrix `M`: faces `α`, base face `o`, rolls
`r i`, distance `d`, and the local conditions that a finite die can check one
face at a time. -/
structure RollModel (M : CoxeterMatrix B) (α : Type*) where
  /-- rolling across an edge of type `i` -/
  r : B → α → α
  /-- the base face -/
  o : α
  /-- the distance from the base face -/
  d : α → ℕ
  /-- rolling back undoes a roll -/
  r_r : ∀ i x, r i (r i x) = x
  /-- each roll changes the distance by exactly one -/
  d_r : ∀ i x, d (r i x) = d x + 1 ∨ d (r i x) + 1 = d x
  d_o : d o = 0
  eq_o : ∀ x, d x = 0 → x = o
  /-- every face other than the base face has a roll towards the base face -/
  down : ∀ x, x ≠ o → ∃ i, d (r i x) + 1 = d x
  /-- corners have finite valence -/
  m_pos : ∀ i j, M i j ≠ 0
  /-- the corner condition: if rolls `a ≠ b` both lead towards the base face,
  then rolling back alternately round the corner of valence `2 M a b` keeps
  leading towards it for `M a b` steps, and both ways round reach the same face. -/
  corner : ∀ x a b, a ≠ b → d (r a x) + 1 = d x → d (r b x) + 1 = d x →
    d (roll r (alternatingWord b a (M a b)).reverse x) + M a b = d x ∧
    roll r (alternatingWord b a (M a b)).reverse x = roll r (alternatingWord a b (M a b)).reverse x

namespace RollModel
variable {M : CoxeterMatrix B} {α : Type*} (R : RollModel M α)

/-- A roll from the base face is *shortest* when its length is the distance of its end face. -/
def Shortest (ω : List B) : Prop := R.d (roll R.r ω R.o) = ω.length

theorem d_r_le (i : B) (x : α) : R.d (R.r i x) ≤ R.d x + 1 := by
  rcases R.d_r i x with h | h <;> omega

theorem le_d_r (i : B) (x : α) : R.d x ≤ R.d (R.r i x) + 1 := by
  have := R.d_r_le i (R.r i x); rwa [R.r_r] at this

/-- Each roll changes the distance by at most one. -/
theorem d_roll_le (ω : List B) (x : α) : R.d (roll R.r ω x) ≤ R.d x + ω.length := by
  induction ω using List.reverseRecOn with
  | nil => simp
  | append_singleton u a ih =>
    simp only [roll_append, roll_singleton, List.length_append, List.length_singleton]
    have := R.d_r_le a (roll R.r u x); omega

/-- No roll from the base face is shorter than the distance of its end face. -/
theorem d_le_length (ω : List B) : R.d (roll R.r ω R.o) ≤ ω.length := by
  simpa [R.d_o] using R.d_roll_le ω R.o

/-- Every face is reached from the base face by a roll of length its distance. -/
theorem exists_shortest (x : α) : ∃ ω : List B, roll R.r ω R.o = x ∧ ω.length = R.d x := by
  induction h : R.d x using Nat.strong_induction_on generalizing x with
  | _ n ih =>
    by_cases hx : x = R.o
    · subst hx; exact ⟨[], rfl, by simp [R.d_o, ← h]⟩
    · obtain ⟨i, hi⟩ := R.down x hx
      obtain ⟨ω, h1, h2⟩ := ih _ (by omega) (R.r i x) rfl
      exact ⟨ω ++ [i], by simp [h1, R.r_r], by simp [h2]; omega⟩

/-- A chosen shortest roll to each face. -/
noncomputable def sw (x : α) : List B := (R.exists_shortest x).choose

theorem roll_sw (x : α) : roll R.r (R.sw x) R.o = x := (R.exists_shortest x).choose_spec.1
theorem length_sw (x : α) : (R.sw x).length = R.d x := (R.exists_shortest x).choose_spec.2

theorem concat_of_length {ω : List B} {n : ℕ} (h : ω.length = n + 1) :
    ∃ u a, ω = u ++ [a] := by
  rcases List.eq_nil_or_concat ω with rfl | ⟨u, a, rfl⟩
  · simp at h
  · exact ⟨u, a, by simp⟩

/-- **Matsumoto's theorem for a roll model.** Two shortest rolls from the base
face to the same face are joined by corner moves. -/
theorem matsumoto : ∀ (n : ℕ) (ω ω' : List B), roll R.r ω R.o = roll R.r ω' R.o →
    ω.length = n → ω'.length = n → R.d (roll R.r ω R.o) = n → BraidEq M ω ω' := by
  intro n
  induction n with
  | zero =>
    intro ω ω' _ h h' _
    rw [List.length_eq_zero_iff.mp h, List.length_eq_zero_iff.mp h']
    exact BraidEq.refl _
  | succ n ih =>
    -- same last roll
    have same : ∀ u v (a : B), roll R.r (u ++ [a]) R.o = roll R.r (v ++ [a]) R.o →
        u.length = n → v.length = n → R.d (roll R.r (u ++ [a]) R.o) = n + 1 →
        BraidEq M (u ++ [a]) (v ++ [a]) := by
      intro u v a he hu hv hd
      simp only [roll_append, roll_singleton] at he hd
      have he' : roll R.r u R.o = roll R.r v R.o := by
        have := congrArg (R.r a) he; rwa [R.r_r, R.r_r] at this
      have h1 := R.d_le_length u
      have h2 := R.d_r_le a (roll R.r u R.o)
      exact (ih u v he' hu hv (by omega)).append_right [a]
    intro ω ω' he h h' hd
    obtain ⟨u, a, rfl⟩ := concat_of_length h
    obtain ⟨v, b, rfl⟩ := concat_of_length h'
    simp only [List.length_append, List.length_singleton, Nat.add_right_cancel_iff] at h h'
    by_cases hab : a = b
    · subst hab; exact same u v a he h h' hd
    -- two different last rolls: go round the corner
    set x := roll R.r (u ++ [a]) R.o with hx
    have hua : roll R.r u R.o = R.r a x := by simp [hx, R.r_r]
    have hvb : roll R.r v R.o = R.r b x := by
      rw [he]; simp [R.r_r]
    have lx : R.d x = n + 1 := hd
    have da : R.d (R.r a x) + 1 = R.d x := by
      have h1 := R.d_le_length u; have h2 := R.le_d_r a x; rw [hua] at h1; omega
    have db : R.d (R.r b x) + 1 = R.d x := by
      have h1 := R.d_le_length v; have h2 := R.le_d_r b x; rw [hvb] at h1; omega
    obtain ⟨hc1, hc2⟩ := R.corner x a b hab da db
    set m := M a b with hm
    obtain ⟨k, hk⟩ : ∃ k, m = k + 1 := Nat.exists_eq_succ_of_ne_zero (R.m_pos a b)
    set y := roll R.r (alternatingWord b a m).reverse x
    obtain ⟨ρ, hρ, hρl⟩ := R.exists_shortest y
    -- the two ways round the corner
    have wa : roll R.r (ρ ++ alternatingWord b a m) R.o = x := by
      rw [roll_append, hρ]; exact roll_reverse_roll _ R.r_r _ _
    have wb : roll R.r (ρ ++ alternatingWord a b m) R.o = x := by
      rw [roll_append, hρ, hc2]; exact roll_reverse_roll _ R.r_r _ _
    have ea : ρ ++ alternatingWord b a m = (ρ ++ alternatingWord a b k) ++ [a] := by
      rw [hk, CoxeterSystem.alternatingWord_succ]; simp
    have eb : ρ ++ alternatingWord a b m = (ρ ++ alternatingWord b a k) ++ [b] := by
      rw [hk, CoxeterSystem.alternatingWord_succ]; simp
    have step : BraidEq M (ρ ++ alternatingWord b a m) (ρ ++ alternatingWord a b m) := by
      have := BraidStep.mk (M := M) ρ [] b a
      rw [M.symmetric b a] at this
      exact Relation.EqvGen.rel _ _ (by simpa using this)
    refine BraidEq.trans (v := ρ ++ alternatingWord b a m) ?_ (step.trans ?_)
    · rw [ea]
      refine same _ _ a ?_ h ?_ hd
      · rw [← ea, wa]
      · simp [CoxeterSystem.length_alternatingWord]; omega
    · rw [eb]
      refine same _ _ b ?_ ?_ h' ?_
      · rw [← eb, wb, he]
      · simp [CoxeterSystem.length_alternatingWord]; omega
      · rw [← eb, wb]; exact hd

/-- `ω` is a shortest roll from face `f` to face `g`. -/
def ShortestRoll (f g : α) (ω : List B) : Prop :=
  roll R.r ω f = g ∧ ∀ η : List B, roll R.r η f = g → ω.length ≤ η.length

/-- Matsumoto's theorem, stated for shortest rolls. -/
theorem matsumoto_shortest {ω ω' : List B} (hω : R.Shortest ω) (hω' : R.Shortest ω')
    (he : roll R.r ω R.o = roll R.r ω' R.o) : BraidEq M ω ω' :=
  R.matsumoto ω.length ω ω' he rfl (by rw [← hω', ← he, hω]) hω

/-- **Word reduction.** Every roll from the base face is turned into a shortest
roll with the same end face by corner moves and cancellations of back-and-forth rolls. -/
theorem reduce (ω : List B) : ∃ ω', Relation.ReflTransGen (MoveStep M) ω ω' ∧
    R.Shortest ω' ∧ roll R.r ω' R.o = roll R.r ω R.o := by
  induction h : ω.length using Nat.strong_induction_on generalizing ω with
  | _ n ih =>
    by_cases hs : R.Shortest ω
    · exact ⟨ω, .refl, hs, rfl⟩
    -- the first roll that does not move away from the base face
    have key : ∀ t : List B, ∀ u, ω = u ++ t → R.Shortest u →
        ∃ u i t', ω = u ++ [i] ++ t' ∧ R.Shortest u ∧ ¬ R.Shortest (u ++ [i]) := by
      intro t
      induction t with
      | nil => intro u hu hsu; subst hu; simp at hs hsu; exact absurd hsu hs
      | cons i t iht =>
        intro u hu hsu
        by_cases hsi : R.Shortest (u ++ [i])
        · exact iht (u ++ [i]) (by simp [hu]) hsi
        · exact ⟨u, i, t, by simp [hu], hsu, hsi⟩
    obtain ⟨u, i, t, rfl, hu, hui⟩ := key ω [] (by simp) (by simp [Shortest, R.d_o])
    unfold Shortest at hu hui
    simp only [roll_append, roll_singleton, List.length_append, List.length_singleton] at hu hui
    have hd : R.d (R.r i (roll R.r u R.o)) + 1 = R.d (roll R.r u R.o) := by
      rcases R.d_r i (roll R.r u R.o) with h1 | h1 <;> omega
    -- u is corner-move-equivalent to a shortest roll ending in i
    set z := R.r i (roll R.r u R.o)
    have hz : roll R.r (R.sw z ++ [i]) R.o = roll R.r u R.o := by simp [R.roll_sw, z, R.r_r]
    have hb : BraidEq M u (R.sw z ++ [i]) :=
      R.matsumoto_shortest hu (by unfold Shortest; rw [hz, hu]; simp [R.length_sw]; omega) hz.symm
    have hm : Relation.ReflTransGen (MoveStep M) (u ++ [i] ++ t) (R.sw z ++ t) := by
      have h1 := (hb.append [] ([i] ++ t)).moves
      simp only [List.nil_append, List.append_assoc] at h1
      rw [List.append_assoc]
      refine (h1.trans (Relation.ReflTransGen.single (Or.inr ?_)))
      simpa [List.append_assoc] using CancelStep.mk (R.sw z) t i
    obtain ⟨ω', h1, h2, h3⟩ := ih (R.sw z ++ t).length
      (by simp [R.length_sw, ← h]; omega) (R.sw z ++ t) rfl
    refine ⟨ω', hm.trans h1, h2, ?_⟩
    rw [h3]; simp [R.roll_sw, z]

end RollModel

end RollingLaw
