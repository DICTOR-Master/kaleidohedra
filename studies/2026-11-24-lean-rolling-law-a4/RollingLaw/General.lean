/-
# Size-independent results used for every die (no data)

* `mem_iff_of_card`, `mirrorsCrossed`, `mirrorsCrossed_swaps`, `crosses_each_once`,
  `RollModel.isReflection_iff`, `RollModel.card_reflections`: copied unchanged from the 3D
  study (`RollingLaw/Die.lean`, `RollingLaw/Mirrors.lean` there), so that this project does not
  load the 3D dice.
* New here: `RollModel.roll_comm`, `RollModel.transitive`, `RollModel.transitive_unique`: the
  roll-preserving symmetries of a die (permutations of the faces that commute with every roll)
  act simply transitively on the faces. This is the combinatorial half of fairness.
-/
import RollingLaw.Coxeter

namespace RollingLaw

open CoxeterSystem (alternatingWord)

theorem mem_iff_of_card {β : Type*} [Fintype β] [DecidableEq β] (P : β → Prop) [DecidablePred P]
    (l : List β) (hn : l.Nodup) (hl : ∀ y ∈ l, P y) (hc : (Finset.univ.filter P).card = l.length) :
    ∀ y, P y ↔ y ∈ l := by
  have hsub : l.toFinset ⊆ Finset.univ.filter P := fun y hy => by
    simpa using hl y (List.mem_toFinset.mp hy)
  have heq := Finset.eq_of_subset_of_card_le hsub (by rw [hc, List.toFinset_card_of_nodup hn])
  intro y
  constructor
  · intro hy
    have : y ∈ Finset.univ.filter P := by simpa using hy
    rw [← heq] at this; exact List.mem_toFinset.mp this
  · exact hl y

section General
variable {B : Type*} {M : CoxeterMatrix B} {W : Type*} [Group W] (cs : CoxeterSystem M W)

/-- The mirrors crossed, in order, when rolling from the face of `w` along `ω`. -/
def mirrorsCrossed (w : W) (ω : List B) : List W :=
  (cs.leftInvSeq ω).map fun t => w * t * w⁻¹

/-- The `k`-th mirror crossed takes the face before the `k`-th roll to the face after it. -/
theorem mirrorsCrossed_swaps (w : W) (ω : List B) (k : ℕ) (hk : k < ω.length) :
    (mirrorsCrossed cs w ω)[k]'(by simp [mirrorsCrossed, hk]) *
        (w * cs.wordProd (ω.take k)) = w * cs.wordProd (ω.take (k + 1)) := by
  simp only [mirrorsCrossed, List.getElem_map, cs.getElem_leftInvSeq ω k hk]
  rw [List.take_add_one, List.getElem?_eq_getElem hk, Option.toList_some, cs.wordProd_append,
    cs.wordProd_singleton]
  group

open Classical in
/-- If there are exactly `n` mirrors, a reduced word of length `n` crosses each exactly once,
from any starting face. -/
theorem crosses_each_once [Fintype W] {n : ℕ} (hn : Nat.card {t : W // cs.IsReflection t} = n)
    {ω : List B} (hω : cs.IsReduced ω) (hl : ω.length = n) (w : W) (t : W)
    (ht : cs.IsReflection t) : (mirrorsCrossed cs w ω).count t = 1 := by
  have hnd : (mirrorsCrossed cs w ω).Nodup :=
    hω.nodup_leftInvSeq.map (fun a b h => by simpa using h)
  have hmem : ∀ u ∈ mirrorsCrossed cs w ω, cs.IsReflection u := by
    intro u hu
    obtain ⟨v, hv, rfl⟩ := List.mem_map.mp hu
    exact (cs.isReflection_of_mem_leftInvSeq ω hv).conj w
  have hcard : (Finset.univ.filter cs.IsReflection).card = (mirrorsCrossed cs w ω).length := by
    rw [← Fintype.card_subtype, ← Nat.card_eq_fintype_card, hn]
    simp [mirrorsCrossed, hl]
  exact List.count_eq_one_of_mem hnd
    ((mem_iff_of_card _ _ hnd hmem (by simpa using hcard) t).mp ht)

end General

namespace RollModel
variable {B : Type*} {M : CoxeterMatrix B} {α : Type*} (R : RollModel M α)

/-- A permutation of the faces that commutes with every roll commutes with every roll sequence. -/
theorem roll_comm (σ : α → α) (hσ : ∀ i z, σ (R.r i z) = R.r i (σ z)) (ω : List B) (z : α) :
    σ (roll R.r ω z) = roll R.r ω (σ z) := by
  induction ω generalizing z with
  | nil => rfl
  | cons i ω ih => simp only [roll_cons]; rw [ih, hσ]

/-- A roll-preserving symmetry is determined by the image of one face. -/
theorem transitive_unique (σ τ : α → α) (hσ : ∀ i z, σ (R.r i z) = R.r i (σ z))
    (hτ : ∀ i z, τ (R.r i z) = R.r i (τ z)) (x : α) (h : σ x = τ x) : σ = τ := by
  have ho : σ R.o = τ R.o := by
    have hx := R.roll_sw x
    have e1 := R.roll_comm σ hσ (R.sw x).reverse x
    have e2 := R.roll_comm τ hτ (R.sw x).reverse x
    have back : roll R.r (R.sw x).reverse x = R.o := by
      have := roll_reverse_roll R.r R.r_r (R.sw x).reverse R.o
      rw [List.reverse_reverse, hx] at this
      exact this
    rw [back] at e1 e2; rw [e1, e2, h]
  funext z
  rw [← R.roll_sw z, R.roll_comm σ hσ, R.roll_comm τ hτ, ho]

variable {W : Type*} [Group W] (cs : CoxeterSystem M W) (hL : R.Lifts)
include cs hL

theorem faceEquiv_symm_r (i : B) (z : α) :
    (R.faceEquiv cs hL).symm (R.r i z) = (R.faceEquiv cs hL).symm z * cs.simple i := by
  apply (R.faceEquiv cs hL).injective
  rw [Equiv.apply_symm_apply]
  show _ = R.face cs hL _
  rw [face_mul_simple]
  exact congrArg (R.r i) ((R.faceEquiv cs hL).apply_symm_apply z).symm

/-- **The roll-preserving symmetries act transitively**: for any two faces `x, y` there is a
permutation of the faces taking `x` to `y` and commuting with every roll. -/
theorem transitive (x y : α) :
    ∃ σ : α ≃ α, σ x = y ∧ ∀ i z, σ (R.r i z) = R.r i (σ z) := by
  set e := R.faceEquiv cs hL
  set g := e.symm y * (e.symm x)⁻¹
  refine ⟨e.symm.trans ((Equiv.mulLeft g).trans e), ?_, fun i z => ?_⟩
  · simp [g]
  · simp only [Equiv.trans_apply, Equiv.coe_mulLeft]
    rw [R.faceEquiv_symm_r cs hL, ← mul_assoc]
    show R.face cs hL _ = R.r i (R.face cs hL _)
    rw [face_mul_simple]

variable (nf : α → List B) (hnf : ∀ x, roll R.r (nf x) R.o = x)
include hnf

theorem wordProd_nf (w : W) : cs.wordProd (nf (R.face cs hL w)) = w :=
  R.face_injective cs hL (by rw [face_wordProd, hnf])

/-- The reflections are the elements whose faces are `roll (nf x ++ [i] ++ (nf x).reverse) o`. -/
theorem isReflection_iff (t : W) : cs.IsReflection t ↔
    ∃ x i, R.face cs hL t = roll R.r (nf x ++ [i] ++ (nf x).reverse) R.o := by
  constructor
  · rintro ⟨w, i, rfl⟩
    refine ⟨R.face cs hL w, i, ?_⟩
    rw [← face_wordProd R cs hL]
    simp [cs.wordProd_append, cs.wordProd_cons, R.wordProd_nf cs hL nf hnf, mul_assoc]
  · rintro ⟨x, i, h⟩
    rw [← face_wordProd R cs hL] at h
    refine ⟨cs.wordProd (nf x), i, R.face_injective cs hL ?_⟩
    rw [h]; simp [cs.wordProd_append, cs.wordProd_cons, mul_assoc]

/-- The number of reflections is a finite count over faces. -/
theorem card_reflections [Fintype α] [DecidableEq α] [Fintype B] :
    Nat.card {t : W // cs.IsReflection t} =
      (Finset.univ.image fun p : α × B => roll R.r (nf p.1 ++ [p.2] ++ (nf p.1).reverse) R.o).card := by
  rw [← Nat.card_eq_finsetCard]
  refine Nat.card_congr ((R.faceEquiv cs hL).subtypeEquiv fun t => ?_)
  rw [R.isReflection_iff cs hL nf hnf]
  simp only [faceEquiv, Finset.mem_image, Finset.mem_univ, true_and,
    Prod.exists, roll_append]
  exact ⟨fun ⟨x, i, h⟩ => ⟨x, i, h.symm⟩, fun ⟨x, i, h⟩ => ⟨x, i, h.symm⟩⟩

end RollModel

end RollingLaw
