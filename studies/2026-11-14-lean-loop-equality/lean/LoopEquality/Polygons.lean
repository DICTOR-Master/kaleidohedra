module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Surgery

@[expose] public section

/-!
# The surgery on unordered edges (Lean paper, Milestone 2c, part 1)

Edges are unordered pairs `Sym2 Atom`. `surgS c k` moves a far–far edge by the half-turn and keeps every
other edge; `degS E x` is the number of edges of `E` at the atom `x`; `htS c` is the half-turn of an edge.

* `surgS_surgS`, `surgS_injective`: the surgery undoes itself.
* `degS_surg_root`: root atoms keep their degree.
* `degS_surg_far`: if the half-turn carries the crossing edges of `E` into `E`, a far atom `x` has after
  the surgery the degree that `ht c x` had before.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

/-- The half-turn `p ↦ c − p` on every atom (bilayer and level kept). -/
def htA (c : ℤ × ℤ) (a : Atom) : Atom := (a.1, c - a.2.1, a.2.2)

theorem htA_htA (c : ℤ × ℤ) (a : Atom) : htA c (htA c a) = a := by
  obtain ⟨j, p, u⟩ := a; simp [htA]

theorem isFar_htA {c : ℤ × ℤ} {k : ℤ} {a : Atom} : IsFar k (htA c a) ↔ IsFar k a := Iff.rfl

theorem twist_eq_htA {c : ℤ × ℤ} {k : ℤ} {a : Atom} (h : IsFar k a) : twist c k a = htA c a := twist_far h

open Classical in
/-- The surgery on an unordered edge. -/
noncomputable def surgS (c : ℤ × ℤ) (k : ℤ) : Sym2 Atom → Sym2 Atom :=
  Sym2.lift ⟨fun a b => if IsFar k a ∧ IsFar k b then s(twist c k a, twist c k b) else s(a, b), by
    intro a b
    by_cases h : IsFar k a ∧ IsFar k b
    · simp [h.1, h.2, Sym2.eq_swap]
    · have h' : ¬ (IsFar k b ∧ IsFar k a) := fun h' => h ⟨h'.2, h'.1⟩
      simp only [h, h', ↓reduceIte, Sym2.eq_swap]⟩

theorem surgS_far {c : ℤ × ℤ} {k : ℤ} {a b : Atom} (h : IsFar k a ∧ IsFar k b) :
    surgS c k s(a, b) = s(htA c a, htA c b) := by
  simp only [surgS, Sym2.lift_mk, h, and_self, ↓reduceIte, twist_eq_htA h.1, twist_eq_htA h.2]

theorem surgS_other {c : ℤ × ℤ} {k : ℤ} {a b : Atom} (h : ¬ (IsFar k a ∧ IsFar k b)) :
    surgS c k s(a, b) = s(a, b) := by
  simp only [surgS, Sym2.lift_mk, h, ↓reduceIte]

theorem surgS_surgS (c : ℤ × ℤ) (k : ℤ) (e : Sym2 Atom) : surgS c k (surgS c k e) = e := by
  induction e using Sym2.ind with
  | _ a b =>
    by_cases h : IsFar k a ∧ IsFar k b
    · rw [surgS_far h, surgS_far ⟨isFar_htA.mpr h.1, isFar_htA.mpr h.2⟩, htA_htA, htA_htA]
    · rw [surgS_other h, surgS_other h]

theorem surgS_injective (c : ℤ × ℤ) (k : ℤ) : Function.Injective (surgS c k) := by
  intro x y h
  have := congrArg (surgS c k) h
  rwa [surgS_surgS, surgS_surgS] at this

open Classical in
/-- The degree of the edge set `E` at the atom `x`. -/
noncomputable def degS (E : Finset (Sym2 Atom)) (x : Atom) : ℕ := (E.filter (fun e => x ∈ e)).card

/-- The half-turn of an edge. -/
def htS (c : ℤ × ℤ) : Sym2 Atom → Sym2 Atom := Sym2.map (htA c)

theorem htS_htS (c : ℤ × ℤ) (e : Sym2 Atom) : htS c (htS c e) = e := by
  unfold htS; rw [Sym2.map_map]
  have : (htA c ∘ htA c) = id := funext (htA_htA c)
  rw [this, Sym2.map_id]; rfl

/-- A crossing edge: one end far, the other in the root half. -/
def IsCrossS (k : ℤ) (e : Sym2 Atom) : Prop :=
  Sym2.lift ⟨fun a b => (IsFar k a ∧ ¬ IsFar k b) ∨ (¬ IsFar k a ∧ IsFar k b), by
    intro a b; dsimp only; exact propext (by tauto)⟩ e

theorem isCrossS_mk {k : ℤ} {a b : Atom} :
    IsCrossS k s(a, b) ↔ (IsFar k a ∧ ¬ IsFar k b) ∨ (¬ IsFar k a ∧ IsFar k b) := by
  simp only [IsCrossS, Sym2.lift_mk]

theorem isCrossS_htS {c : ℤ × ℤ} {k : ℤ} {e : Sym2 Atom} : IsCrossS k (htS c e) ↔ IsCrossS k e := by
  induction e using Sym2.ind with
  | _ a b =>
    show IsCrossS k s(htA c a, htA c b) ↔ IsCrossS k s(a, b)
    rw [isCrossS_mk, isCrossS_mk]; exact Iff.rfl

/-- Root atoms keep their degree. -/
theorem degS_surg_root (c : ℤ × ℤ) (k : ℤ) (E : Finset (Sym2 Atom)) {x : Atom} (hx : ¬ IsFar k x) :
    degS (E.image (surgS c k)) x = degS E x := by
  classical
  unfold degS
  rw [Finset.filter_image, Finset.card_image_of_injective _ (surgS_injective c k)]
  congr 1
  apply Finset.filter_congr
  intro e _
  induction e using Sym2.ind with
  | _ a b =>
    by_cases hff : IsFar k a ∧ IsFar k b
    · rw [surgS_far hff, Sym2.mem_iff, Sym2.mem_iff]
      constructor
      · rintro (h | h)
        · exact absurd (h ▸ isFar_htA.mpr hff.1) hx
        · exact absurd (h ▸ isFar_htA.mpr hff.2) hx
      · rintro (h | h)
        · exact absurd (h ▸ hff.1) hx
        · exact absurd (h ▸ hff.2) hx
    · rw [surgS_other hff]

open Classical in
/-- Far atoms: with the crossing edges of `E` carried into `E` by the half-turn, the far atom `x` has
after the surgery the degree that `htA c x` had before. -/
theorem degS_surg_far (c : ℤ × ℤ) (k : ℤ) (E : Finset (Sym2 Atom))
    (hP : ∀ e ∈ E, IsCrossS k e → htS c e ∈ E) {x : Atom} (hx : IsFar k x) :
    degS (E.image (surgS c k)) x = degS E (htA c x) := by
  unfold degS
  rw [Finset.filter_image, Finset.card_image_of_injective _ (surgS_injective c k)]
  have hff_of : ∀ a b : Atom, ¬ IsCrossS k s(a, b) → (IsFar k a ∨ IsFar k b) → IsFar k a ∧ IsFar k b := by
    intro a b h1 h2; rw [isCrossS_mk] at h1
    by_cases ha : IsFar k a <;> by_cases hb : IsFar k b <;> simp_all
  have hsplit1 : E.filter (fun e => x ∈ surgS c k e) =
      E.filter (fun e => ¬ IsCrossS k e ∧ htA c x ∈ e) ∪ E.filter (fun e => IsCrossS k e ∧ x ∈ e) := by
    ext e
    simp only [Finset.mem_filter, Finset.mem_union]
    induction e using Sym2.ind with
    | _ a b =>
      by_cases hff : IsFar k a ∧ IsFar k b
      · have hnc : ¬ IsCrossS k s(a, b) := by rw [isCrossS_mk]; tauto
        rw [surgS_far hff, Sym2.mem_iff, Sym2.mem_iff]
        constructor
        · rintro ⟨he, h | h⟩
          · exact Or.inl ⟨he, hnc, Or.inl (by rw [h, htA_htA])⟩
          · exact Or.inl ⟨he, hnc, Or.inr (by rw [h, htA_htA])⟩
        · rintro (⟨he, -, h | h⟩ | ⟨he, hc, -⟩)
          · exact ⟨he, Or.inl (by rw [← h, htA_htA])⟩
          · exact ⟨he, Or.inr (by rw [← h, htA_htA])⟩
          · exact absurd hc hnc
      · rw [surgS_other hff, Sym2.mem_iff, Sym2.mem_iff]
        constructor
        · rintro ⟨he, h⟩
          right; refine ⟨he, ?_, h⟩
          rw [isCrossS_mk]
          rcases h with h | h
          · subst h; exact Or.inl ⟨hx, fun h2 => hff ⟨hx, h2⟩⟩
          · subst h; exact Or.inr ⟨fun h1 => hff ⟨h1, hx⟩, hx⟩
        · rintro (⟨he, hnc, h⟩ | ⟨he, -, h⟩)
          · have hx' : IsFar k (htA c x) := isFar_htA.mpr hx
            have := hff_of a b hnc (by rcases h with h | h <;> [exact Or.inl (h ▸ hx'); exact Or.inr (h ▸ hx')])
            exact absurd this hff
          · exact ⟨he, h⟩
  have hsplit2 : E.filter (fun e => htA c x ∈ e) =
      E.filter (fun e => ¬ IsCrossS k e ∧ htA c x ∈ e) ∪
      E.filter (fun e => IsCrossS k e ∧ htA c x ∈ e) := by
    ext e
    simp only [Finset.mem_filter, Finset.mem_union]
    constructor
    · rintro ⟨he, h⟩
      by_cases hc : IsCrossS k e
      · exact Or.inr ⟨he, hc, h⟩
      · exact Or.inl ⟨he, hc, h⟩
    · rintro (⟨he, -, h⟩ | ⟨he, -, h⟩) <;> exact ⟨he, h⟩
  have hdisj : ∀ (y z : Atom), Disjoint (E.filter (fun e => ¬ IsCrossS k e ∧ y ∈ e))
      (E.filter (fun e => IsCrossS k e ∧ z ∈ e)) := by
    intro y z
    rw [Finset.disjoint_filter]
    intro e _ h1 h2
    exact h1.1 h2.1
  rw [hsplit1, hsplit2, Finset.card_union_of_disjoint (hdisj _ _), Finset.card_union_of_disjoint (hdisj _ _)]
  congr 1
  apply Finset.card_bij (fun e _ => htS c e)
  · intro e he
    simp only [Finset.mem_filter] at he ⊢
    refine ⟨hP e he.1 he.2.1, isCrossS_htS.mpr he.2.1, ?_⟩
    unfold htS
    exact Sym2.mem_map.mpr ⟨x, he.2.2, rfl⟩
  · intro a _ b _ h
    have := congrArg (htS c) h
    rwa [htS_htS, htS_htS] at this
  · intro e he
    simp only [Finset.mem_filter] at he
    refine ⟨htS c e, ?_, htS_htS c e⟩
    simp only [Finset.mem_filter]
    refine ⟨hP e he.1 he.2.1, isCrossS_htS.mpr he.2.1, ?_⟩
    unfold htS
    exact Sym2.mem_map.mpr ⟨htA c x, he.2.2, htA_htA c x⟩

end LoopEqualityProof
