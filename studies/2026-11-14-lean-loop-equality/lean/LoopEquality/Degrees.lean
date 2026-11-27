module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Surgery

@[expose] public section

/-!
# The surgery keeps every degree (Lean paper, Milestone 2b)

Study 2026-11-15-polygon-bijection, Theorem A, proof step 2 ("every atom has degree 2").

A finite set `E` of edges (ordered pairs of atoms) has degree `deg E x` at the atom `x`: the number of its
edges with `x` at one end. `ht c` is the half-turn `p ↦ c − p` on every atom. Write `E'` for the image of
`E` under the surgery `surg c k`.

* Root atoms keep their degree: `deg E' x = deg E x` (`deg_surg_root`).
* If the half-turn carries the crossing edges of `E` into `E` (the crossing points are carried onto
  themselves, as in Theorem A), a far atom `x` of `E'` has the degree that `ht c x` has in `E`
  (`deg_surg_far`).

So the surgery of a polygon whose crossing points the half-turn keeps is again two-valent at every atom.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

/-- `x` is an end of the edge `e`. -/
def Ends (x : Atom) (e : Atom × Atom) : Prop := e.1 = x ∨ e.2 = x

open Classical in
/-- The degree of the edge set `E` at the atom `x`. -/
noncomputable def deg (E : Finset (Atom × Atom)) (x : Atom) : ℕ := (E.filter (Ends x)).card

/-- The half-turn `p ↦ c − p` on every atom (bilayer and level kept). -/
def ht (c : ℤ × ℤ) (a : Atom) : Atom := (a.1, c - a.2.1, a.2.2)

theorem ht_ht (c : ℤ × ℤ) (a : Atom) : ht c (ht c a) = a := by
  obtain ⟨j, p, u⟩ := a; simp [ht]

theorem isFar_ht {c : ℤ × ℤ} {k : ℤ} {a : Atom} : IsFar k (ht c a) ↔ IsFar k a := Iff.rfl

theorem twist_eq_ht {c : ℤ × ℤ} {k : ℤ} {a : Atom} (h : IsFar k a) : twist c k a = ht c a := twist_far h

/-- A crossing edge: one end in the far half, the other in the root half. -/
def IsCross (k : ℤ) (e : Atom × Atom) : Prop :=
  (IsFar k e.1 ∧ ¬ IsFar k e.2) ∨ (¬ IsFar k e.1 ∧ IsFar k e.2)

/-- The half-turn of an edge (both ends). -/
def htE (c : ℤ × ℤ) (e : Atom × Atom) : Atom × Atom := (ht c e.1, ht c e.2)

theorem htE_htE (c : ℤ × ℤ) (e : Atom × Atom) : htE c (htE c e) = e := by
  obtain ⟨a, b⟩ := e; simp [htE, ht_ht]

theorem isCross_htE {c : ℤ × ℤ} {k : ℤ} {e : Atom × Atom} : IsCross k (htE c e) ↔ IsCross k e := Iff.rfl

open Classical in
theorem card_filter_image_surg (c : ℤ × ℤ) (k : ℤ) (E : Finset (Atom × Atom)) (P : Atom × Atom → Prop) :
    ((E.image (surg c k)).filter P).card = (E.filter (fun e => P (surg c k e))).card := by
  rw [Finset.filter_image, Finset.card_image_of_injective _ (surg_injective c k)]

/-- Root atoms keep their degree. -/
theorem deg_surg_root (c : ℤ × ℤ) (k : ℤ) (E : Finset (Atom × Atom)) {x : Atom} (hx : ¬ IsFar k x) :
    deg (E.image (surg c k)) x = deg E x := by
  classical
  unfold deg
  rw [card_filter_image_surg]
  congr 1
  apply Finset.filter_congr
  intro e _
  by_cases hff : IsFar k e.1 ∧ IsFar k e.2
  · rw [surg_far hff]
    unfold Ends
    constructor
    · rintro (h | h)
      · exact absurd (h ▸ isFar_twist.mpr hff.1) hx
      · exact absurd (h ▸ isFar_twist.mpr hff.2) hx
    · rintro (h | h)
      · exact absurd (h ▸ hff.1) hx
      · exact absurd (h ▸ hff.2) hx
  · rw [surg_other hff]

open Classical in
/-- Far atoms: with the crossing edges of `E` carried into `E` by the half-turn, the far atom `x` has in
the surgered set the degree that `ht c x` has in `E`. -/
theorem deg_surg_far (c : ℤ × ℤ) (k : ℤ) (E : Finset (Atom × Atom))
    (hP : ∀ e ∈ E, IsCross k e → htE c e ∈ E) {x : Atom} (hx : IsFar k x) :
    deg (E.image (surg c k)) x = deg E (ht c x) := by
  unfold deg
  rw [card_filter_image_surg]
  -- split both sides into far–far edges and crossing edges
  have hsplit1 : E.filter (fun e => Ends x (surg c k e)) =
      E.filter (fun e => (IsFar k e.1 ∧ IsFar k e.2) ∧ Ends (ht c x) e) ∪
      E.filter (fun e => IsCross k e ∧ Ends x e) := by
    ext e
    simp only [Finset.mem_filter, Finset.mem_union]
    constructor
    · rintro ⟨he, h⟩
      by_cases hff : IsFar k e.1 ∧ IsFar k e.2
      · rw [surg_far hff, twist_eq_ht hff.1, twist_eq_ht hff.2] at h
        left; refine ⟨he, hff, ?_⟩
        unfold Ends at h ⊢
        rcases h with h | h
        · left; rw [← h, ht_ht]
        · right; rw [← h, ht_ht]
      · rw [surg_other hff] at h
        right; refine ⟨he, ?_, h⟩
        unfold IsCross
        unfold Ends at h
        rcases h with h | h
        · subst h; exact Or.inl ⟨hx, fun h2 => hff ⟨hx, h2⟩⟩
        · subst h; exact Or.inr ⟨fun h1 => hff ⟨h1, hx⟩, hx⟩
    · rintro (⟨he, hff, h⟩ | ⟨he, hcr, h⟩)
      · refine ⟨he, ?_⟩
        rw [surg_far hff, twist_eq_ht hff.1, twist_eq_ht hff.2]
        unfold Ends at h ⊢
        rcases h with h | h
        · left; rw [h, ht_ht]
        · right; rw [h, ht_ht]
      · refine ⟨he, ?_⟩
        have hff : ¬ (IsFar k e.1 ∧ IsFar k e.2) := by
          unfold IsCross at hcr; tauto
        rw [surg_other hff]; exact h
  have hsplit2 : E.filter (fun e => Ends (ht c x) e) =
      E.filter (fun e => (IsFar k e.1 ∧ IsFar k e.2) ∧ Ends (ht c x) e) ∪
      E.filter (fun e => IsCross k e ∧ Ends (ht c x) e) := by
    ext e
    simp only [Finset.mem_filter, Finset.mem_union]
    have hx' : IsFar k (ht c x) := isFar_ht.mpr hx
    constructor
    · rintro ⟨he, h⟩
      by_cases hff : IsFar k e.1 ∧ IsFar k e.2
      · exact Or.inl ⟨he, hff, h⟩
      · right; refine ⟨he, ?_, h⟩
        unfold IsCross
        unfold Ends at h
        rcases h with h | h
        · rw [← h] at hx'; exact Or.inl ⟨hx', fun h2 => hff ⟨hx', h2⟩⟩
        · rw [← h] at hx'; exact Or.inr ⟨fun h1 => hff ⟨h1, hx'⟩, hx'⟩
    · rintro (⟨he, -, h⟩ | ⟨he, -, h⟩) <;> exact ⟨he, h⟩
  have hdisj : ∀ (y z : Atom), Disjoint
      (E.filter (fun e => (IsFar k e.1 ∧ IsFar k e.2) ∧ Ends y e))
      (E.filter (fun e => IsCross k e ∧ Ends z e)) := by
    intro y z
    rw [Finset.disjoint_filter]
    intro e _ h1 h2
    unfold IsCross at h2
    rcases h2.1 with h | h
    · exact h.2 h1.1.2
    · exact h.1 h1.1.1
  rw [hsplit1, hsplit2, Finset.card_union_of_disjoint (hdisj _ _), Finset.card_union_of_disjoint (hdisj _ _)]
  congr 1
  -- the crossing edges at `x` and at `ht c x` correspond under the half-turn of edges
  apply Finset.card_bij (fun e _ => htE c e)
  · intro e he
    simp only [Finset.mem_filter] at he ⊢
    refine ⟨hP e he.1 he.2.1, isCross_htE.mpr he.2.1, ?_⟩
    unfold Ends htE at *
    rcases he.2.2 with h | h
    · left; rw [h]
    · right; rw [h]
  · intro a _ b _ h
    have := congrArg (htE c) h
    rwa [htE_htE, htE_htE] at this
  · intro e he
    simp only [Finset.mem_filter] at he
    refine ⟨htE c e, ?_, htE_htE c e⟩
    simp only [Finset.mem_filter]
    refine ⟨hP e he.1 he.2.1, isCross_htE.mpr he.2.1, ?_⟩
    unfold Ends htE at *
    rcases he.2.2 with h | h
    · left; simp only; rw [h, ht_ht]
    · right; simp only; rw [h, ht_ht]

end LoopEqualityProof
