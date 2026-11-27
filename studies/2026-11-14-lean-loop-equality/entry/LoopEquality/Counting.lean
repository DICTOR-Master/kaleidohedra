module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.Linkage
public import LoopEquality.Parts
public import LoopEquality.Transfer

@[expose] public section

/-!
# Counting towards Theorem B (Lean paper, Milestone 3d)

* `bond_root_flip`: bonds between root-side atoms are the same in `G σ` and `G (flipAt σ k)`.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

theorem bond_root_flip {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {a b : Atom}
    (ha : ¬ IsFar k a) (hb : ¬ IsFar k b) : Bond σ a b ↔ Bond (flipAt σ k) a b := by
  have := (flip_is_twist hc).2.2 a b ⟨fun h => absurd h ha, fun h => absurd h hb⟩
  rwa [twist_root ha, twist_root hb] at this

/-- A root-side linkage of `G σ` ending at the `loA k p`, `p ∈ P`. -/
def RootL (σ : ℤ → ZMod 3) (k : ℤ) (P : Finset (ℤ × ℤ)) (R : Finset (Sym2 Atom)) : Prop :=
  IsLinkageOn R (P.image (loA k)) ∧ (∀ e ∈ R, ∀ w ∈ e, ¬ IsFar k w) ∧ ∀ e ∈ R, BondS σ e

/-- A far-side linkage of `G σ` ending at the `upA k p`, `p ∈ P`. -/
def FarL (σ : ℤ → ZMod 3) (k : ℤ) (P : Finset (ℤ × ℤ)) (F : Finset (Sym2 Atom)) : Prop :=
  IsLinkageOn F (P.image (upA k)) ∧ (∀ e ∈ F, ∀ w ∈ e, IsFar k w) ∧ ∀ e ∈ F, BondS σ e

/-- Polygons of `G σ` through `v` with `l` edges whose vertical bonds at bilayer `k` are exactly those at `P`. -/
def PolysCross (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) (k : ℤ) (P : Finset (ℤ × ℤ)) : Set (Finset (Sym2 Atom)) :=
  {E | IsPolygon σ E ∧ 0 < degS E v ∧ E.card = l ∧ ∀ p, p ∈ P ↔ vert k p ∈ E}

/-- Pairs (root linkage through `v`, far linkage) with ends at `P`, sizes adding to `l`, forming one cycle. -/
def PartsCross (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) (k : ℤ) (P : Finset (ℤ × ℤ)) :
    Set (Finset (Sym2 Atom) × Finset (Sym2 Atom)) :=
  {RF | RootL σ k P RF.1 ∧ FarL σ k P RF.2 ∧ 0 < degS RF.1 v ∧ RF.1.card + P.card + RF.2.card = l ∧
    SingleCycle k P RF.1 RF.2}

theorem disj_three {k : ℤ} {P : Finset (ℤ × ℤ)} {R F : Finset (Sym2 Atom)}
    (hRs : ∀ e ∈ R, ∀ w ∈ e, ¬ IsFar k w) (hFs : ∀ e ∈ F, ∀ w ∈ e, IsFar k w) :
    Disjoint R (P.image (vert k)) ∧ Disjoint (R ∪ P.image (vert k)) F := by
  constructor
  · rw [Finset.disjoint_left]; intro e heR heV
    obtain ⟨p, -, rfl⟩ := Finset.mem_image.mp heV
    exact hRs _ heR (upA k p) (by rw [vert_eq]; exact Sym2.mem_mk_right _ _) (isFar_upA k p)
  · rw [Finset.disjoint_left]; intro e heRV heF
    rcases Finset.mem_union.mp heRV with heR | heV
    · obtain ⟨a, ha⟩ := exists_mem_sym2 e
      exact hRs e heR a ha (hFs e heF a ha)
    · obtain ⟨p, -, rfl⟩ := Finset.mem_image.mp heV
      exact not_isFar_loA k p (hFs _ heF _ (by rw [vert_eq]; exact Sym2.mem_mk_left _ _))

theorem card_three {k : ℤ} {P : Finset (ℤ × ℤ)} {R F : Finset (Sym2 Atom)}
    (hRs : ∀ e ∈ R, ∀ w ∈ e, ¬ IsFar k w) (hFs : ∀ e ∈ F, ∀ w ∈ e, IsFar k w) :
    (R ∪ P.image (vert k) ∪ F).card = R.card + P.card + F.card := by
  obtain ⟨h1, h2⟩ := disj_three (P := P) hRs hFs
  rw [Finset.card_union_of_disjoint h2, Finset.card_union_of_disjoint h1,
    Finset.card_image_of_injective _ (fun p q h => vert_inj h)]

theorem filter_root_three {k : ℤ} {P : Finset (ℤ × ℤ)} {R F : Finset (Sym2 Atom)}
    (hRs : ∀ e ∈ R, ∀ w ∈ e, ¬ IsFar k w) (hFs : ∀ e ∈ F, ∀ w ∈ e, IsFar k w) :
    (R ∪ P.image (vert k) ∪ F).filter (fun e => ∀ w ∈ e, ¬ IsFar k w) = R := by
  ext e; simp only [Finset.mem_filter, Finset.mem_union]
  constructor
  · rintro ⟨(h | h) | h, hr⟩
    · exact h
    · obtain ⟨p, -, rfl⟩ := Finset.mem_image.mp h
      exact absurd (isFar_upA k p) (hr _ (by rw [vert_eq]; exact Sym2.mem_mk_right _ _))
    · obtain ⟨a, ha⟩ := exists_mem_sym2 e
      exact absurd (hFs e h a ha) (hr a ha)
  · intro h; exact ⟨Or.inl (Or.inl h), hRs e h⟩

theorem filter_far_three {k : ℤ} {P : Finset (ℤ × ℤ)} {R F : Finset (Sym2 Atom)}
    (hRs : ∀ e ∈ R, ∀ w ∈ e, ¬ IsFar k w) (hFs : ∀ e ∈ F, ∀ w ∈ e, IsFar k w) :
    (R ∪ P.image (vert k) ∪ F).filter (fun e => ∀ w ∈ e, IsFar k w) = F := by
  ext e; simp only [Finset.mem_filter, Finset.mem_union]
  constructor
  · rintro ⟨(h | h) | h, hf⟩
    · obtain ⟨a, ha⟩ := exists_mem_sym2 e
      exact absurd (hf a ha) (hRs e h a ha)
    · obtain ⟨p, -, rfl⟩ := Finset.mem_image.mp h
      exact absurd (hf _ (by rw [vert_eq]; exact Sym2.mem_mk_left _ _)) (not_isFar_loA k p)
    · exact h
  · intro h; exact ⟨Or.inr h, hFs e h⟩

/-- At a root-side atom, the degree in `R ∪ V ∪ F` is positive exactly when it is positive in `R`. -/
theorem degS_pos_root {k : ℤ} {P : Finset (ℤ × ℤ)} {R F : Finset (Sym2 Atom)}
    (hR : IsLinkageOn R (P.image (loA k))) (hRs : ∀ e ∈ R, ∀ w ∈ e, ¬ IsFar k w)
    (hFs : ∀ e ∈ F, ∀ w ∈ e, IsFar k w) {v : Atom} (hv : ¬ IsFar k v) :
    0 < degS (R ∪ P.image (vert k) ∪ F) v ↔ 0 < degS R v := by
  rw [degS_three hRs hFs, degS_verts, degS_zero_of_side hFs hv]
  simp only [loA_notMem_upA hv, ↓reduceIte, add_zero]
  constructor
  · intro h
    by_cases hl : v ∈ P.image (loA k)
    · rw [hR.1 v hl]; exact Nat.one_pos
    · simp only [hl, ↓reduceIte, add_zero] at h; exact h
  · intro h; omega

/-- **Product structure, counted.** For `v` on the root side and a nonempty crossing set `P` whose vertical
bonds are bonds, the polygons through `v` crossing bilayer `k` exactly at `P` correspond one to one with the
pairs (root linkage through `v`, far linkage) forming one cycle. -/
theorem ncard_polysCross {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {P : Finset (ℤ × ℤ)}
    (hv : ¬ IsFar k v) (hP : P.Nonempty) (hV : ∀ p ∈ P, BondS σ (vert k p)) :
    (PolysCross σ v l k P).ncard = (PartsCross σ v l k P).ncard := by
  apply Set.ncard_congr (fun E _ => (E.filter (fun e => ∀ w ∈ e, ¬ IsFar k w),
    E.filter (fun e => ∀ w ∈ e, IsFar k w)))
  · rintro E ⟨hE, hdv, hcard, hPdef⟩
    obtain ⟨hsplit, hRl, hFl, hsc⟩ := polygon_to_parts hE hPdef hP rfl rfl
    set R := E.filter (fun e => ∀ w ∈ e, ¬ IsFar k w)
    set F := E.filter (fun e => ∀ w ∈ e, IsFar k w)
    have hRs : ∀ e ∈ R, ∀ w ∈ e, ¬ IsFar k w := fun e he => (Finset.mem_filter.mp he).2
    have hFs : ∀ e ∈ F, ∀ w ∈ e, IsFar k w := fun e he => (Finset.mem_filter.mp he).2
    refine ⟨⟨hRl, hRs, fun e he => hE.2.1 e (Finset.filter_subset _ _ he)⟩,
      ⟨hFl, hFs, fun e he => hE.2.1 e (Finset.filter_subset _ _ he)⟩, ?_, ?_, hsc⟩
    · rw [← degS_pos_root hRl hRs hFs hv, ← hsplit]; exact hdv
    · rw [← card_three hRs hFs, ← hsplit, hcard]
  · rintro E E' ⟨hE, -, -, hP1⟩ ⟨hE', -, -, hP2⟩ h
    obtain ⟨hs1, -⟩ := polygon_to_parts hE hP1 hP rfl rfl
    obtain ⟨hs2, -⟩ := polygon_to_parts hE' hP2 hP rfl rfl
    simp only [Prod.mk.injEq] at h
    rw [hs1, hs2, h.1, h.2]
  · rintro ⟨R, F⟩ ⟨⟨hRl, hRs, hRb⟩, ⟨hFl, hFs, hFb⟩, hdv, hcard, hsc⟩
    refine ⟨R ∪ P.image (vert k) ∪ F, ⟨?_, ?_, ?_, ?_⟩, ?_⟩
    · apply parts_to_polygon hP hRl hFl hRs hFs _ hsc
      intro e he
      rcases Finset.mem_union.mp he with h | h
      · rcases Finset.mem_union.mp h with h | h
        · exact hRb e h
        · obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp h; exact hV p hp
      · exact hFb e h
    · rw [degS_pos_root hRl hRs hFs hv]; exact hdv
    · rw [card_three hRs hFs]; exact hcard
    · intro p
      constructor
      · intro hp; exact Finset.mem_union_left _ (Finset.mem_union_right _ (Finset.mem_image_of_mem _ hp))
      · intro h
        rcases Finset.mem_union.mp h with h | h
        · rcases Finset.mem_union.mp h with h | h
          · exact absurd (isFar_upA k p) (hRs _ h _ (by rw [vert_eq]; exact Sym2.mem_mk_right _ _))
          · obtain ⟨q, hq, hqp⟩ := Finset.mem_image.mp h; rw [← vert_inj hqp]; exact hq
        · exact absurd (hFs _ h _ (by rw [vert_eq]; exact Sym2.mem_mk_left _ _)) (not_isFar_loA k p)
    · simp only [filter_root_three hRs hFs, filter_far_three hRs hFs]

end LoopEqualityProof
