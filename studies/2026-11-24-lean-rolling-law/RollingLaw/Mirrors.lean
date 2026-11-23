/-
# The mirrors of each die, and the longest roll crosses each once

A *mirror* is a reflection of the Coxeter group (Mathlib's `IsReflection`:
a conjugate `w s_i w⁻¹` of a simple reflection). Rolling from the face of `w`
along `ω`, the `k`-th roll crosses the mirror `w t_k w⁻¹`, where `t_k` is the
`k`-th entry of Mathlib's left inversion sequence (`mirrorsCrossed`,
`mirrorsCrossed_swaps`: that mirror takes the face before the roll to the face after it).

General (`RollModel.isReflection_iff`, `RollModel.card_reflections`): with a
table of words reaching each face, the reflections correspond to the faces
`roll (word x ++ [i] ++ (word x).reverse) o`, so their number is a finite count.
General (`crosses_each_once`): if there are `n` mirrors, a reduced word of
length `n` crosses every mirror exactly once.
Per die: 6, 9, 15 mirrors (`A3.card_mirrors` …), and every longest shortest
roll (6, 9, 15 rolls) from any face crosses every mirror exactly once
(`A3.longest_crosses_each_once` …).
-/
import RollingLaw.Die

namespace RollingLaw

open CoxeterSystem (alternatingWord)

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
    ((Die.mem_iff_of_card _ _ hnd hmem (by simpa using hcard) t).mp ht)

end General

namespace RollModel
variable {B : Type*} {M : CoxeterMatrix B} {α : Type*} (R : RollModel M α)
variable {W : Type*} [Group W] (cs : CoxeterSystem M W) (hL : R.Lifts)
variable (nf : α → List B) (hnf : ∀ x, roll R.r (nf x) R.o = x)
include hL hnf

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

namespace A3

/-- the tabled shortest roll to each face -/
def nf (x : Fin 24) : List (Fin 3) := ((Data.A3.word.getD x.val []).map fun i => ⟨i % 3, Nat.mod_lt _ (by decide)⟩)

theorem roll_nf : ∀ x, roll r (nf x) 0 = x := by decide +kernel

theorem card_mirrors_q : (Finset.univ.image fun p : Fin 24 × Fin 3 =>
    roll r (nf p.1 ++ [p.2] ++ (nf p.1).reverse) 0).card = 6 := by decide +kernel

/-- **A3 has 6 mirrors.** -/
theorem card_mirrors : Nat.card {t : M.Group // cs.IsReflection t} = 6 := by
  rw [model.card_reflections cs lifts nf roll_nf]; exact card_mirrors_q

open Classical in
/-- **The longest shortest roll crosses every mirror exactly once**, from any face. -/
theorem longest_crosses_each_once {ω : List (Fin 3)} (hω : cs.IsReduced ω) (hl : ω.length = 6)
    (w : M.Group) {t : M.Group} (ht : cs.IsReflection t) : (mirrorsCrossed cs w ω).count t = 1 := by
  have : Fintype M.Group := Fintype.ofEquiv _ (model.faceEquiv cs lifts).symm
  exact crosses_each_once cs card_mirrors hω hl w t ht

end A3

namespace B3

/-- the tabled shortest roll to each face -/
def nf (x : Fin 48) : List (Fin 3) := ((Data.B3.word.getD x.val []).map fun i => ⟨i % 3, Nat.mod_lt _ (by decide)⟩)

theorem roll_nf : ∀ x, roll r (nf x) 0 = x := by decide +kernel

theorem card_mirrors_q : (Finset.univ.image fun p : Fin 48 × Fin 3 =>
    roll r (nf p.1 ++ [p.2] ++ (nf p.1).reverse) 0).card = 9 := by decide +kernel

/-- **B3 has 9 mirrors.** -/
theorem card_mirrors : Nat.card {t : M.Group // cs.IsReflection t} = 9 := by
  rw [model.card_reflections cs lifts nf roll_nf]; exact card_mirrors_q

open Classical in
/-- **The longest shortest roll crosses every mirror exactly once**, from any face. -/
theorem longest_crosses_each_once {ω : List (Fin 3)} (hω : cs.IsReduced ω) (hl : ω.length = 9)
    (w : M.Group) {t : M.Group} (ht : cs.IsReflection t) : (mirrorsCrossed cs w ω).count t = 1 := by
  have : Fintype M.Group := Fintype.ofEquiv _ (model.faceEquiv cs lifts).symm
  exact crosses_each_once cs card_mirrors hω hl w t ht

end B3

namespace H3

/-- the tabled shortest roll to each face -/
def nf (x : Fin 120) : List (Fin 3) := ((Data.H3.word.getD x.val []).map fun i => ⟨i % 3, Nat.mod_lt _ (by decide)⟩)

theorem roll_nf : ∀ x, roll r (nf x) 0 = x := by decide +kernel

theorem card_mirrors_q : (Finset.univ.image fun p : Fin 120 × Fin 3 =>
    roll r (nf p.1 ++ [p.2] ++ (nf p.1).reverse) 0).card = 15 := by decide +kernel

/-- **H3 has 15 mirrors.** -/
theorem card_mirrors : Nat.card {t : M.Group // cs.IsReflection t} = 15 := by
  rw [model.card_reflections cs lifts nf roll_nf]; exact card_mirrors_q

open Classical in
/-- **The longest shortest roll crosses every mirror exactly once**, from any face. -/
theorem longest_crosses_each_once {ω : List (Fin 3)} (hω : cs.IsReduced ω) (hl : ω.length = 15)
    (w : M.Group) {t : M.Group} (ht : cs.IsReflection t) : (mirrorsCrossed cs w ω).count t = 1 := by
  have : Fintype M.Group := Fintype.ofEquiv _ (model.faceEquiv cs lifts).symm
  exact crosses_each_once cs card_mirrors hω hl w t ht

end H3

end RollingLaw
