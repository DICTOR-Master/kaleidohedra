module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.Linkage
public import LoopEquality.Parts
public import LoopEquality.Counting
public import LoopEquality.Transfer
public import LoopEquality.Pairings
public import LoopEquality.BSym

@[expose] public section

/-!
# Single arcs are unchanged by the half-turn (#102, "Locality": Lemmas 5 and 6 for one arc)

* `fc_transfer`: for a good centre `c`, the far linkages of `G σ` ending at `P` with pairing `N` and `s` edges are as
  many as those of the flipped stacking ending at `c − P` with the half-turned pairing (flip transfer).
* `Fc_two`: for a crossing set of two points, the count of far linkages is the same at `P` and at `c − P`, in the same
  stacking (the flip transfer about `c`, then about the midpoint of the two image points).

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

theorem fc_transfer {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) (P : Finset (ℤ × ℤ))
    (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (s : ℕ) :
    Fc σ k P N s = Fc (flipAt σ k) k (gP c P) (gM c N) s := by
  have hc' := goodCentre_flipAt hc
  have hinv := htA_invol c
  have hS : htS c = Sym2.map (htA c) := rfl
  unfold Fc; congr 1
  apply Set.ncard_congr (fun F _ => F.image (htS c))
  · rintro F ⟨⟨hFl, hFs, hFb⟩, hs, hN⟩
    obtain ⟨t1, t2, t3, t4, -⟩ := flip_transfer hc hFl hFs hFb
    refine ⟨⟨t1, t2, t3⟩, by rw [t4, hs], ?_⟩
    have := pairF_image c k F (gP c P)
    rw [show (gP c P).image (fun p => c - p) = P from gP_gP c P] at this
    show pairF k (F.image (htS c)) (gP c P) = gM c N
    rw [this, hN]; rfl
  · intro F₁ _ F₂ _ h
    have := congrArg (fun X => X.image (htS c)) h
    rwa [hS, image_image_invol hinv, image_image_invol hinv] at this
  · rintro F ⟨⟨hFl, hFs, hFb⟩, hs, hN⟩
    obtain ⟨t1, t2, t3, t4, -⟩ := flip_transfer hc' hFl hFs hFb
    rw [flipAt_flipAt] at t3
    have e1 : (gP c P).image (fun p => c - p) = P := gP_gP c P
    rw [e1] at t1
    refine ⟨F.image (htS c), ⟨⟨t1, t2, t3⟩, by rw [t4, hs], ?_⟩, ?_⟩
    · have := pairF_image c k F P
      show pairF k (F.image (htS c)) P = N
      rw [this]
      show gM c (pairF k F (gP c P)) = N
      rw [hN, gM_gM]
    · show (F.image (htS c)).image (htS c) = F
      rw [hS]; exact image_image_invol hinv F

/-- The shape of a pairing: every point with itself, and symmetric. -/
def PairShape (Q : Finset (ℤ × ℤ)) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : Prop :=
  N ⊆ Q ×ˢ Q ∧ (∀ x ∈ Q, (x, x) ∈ N) ∧ ∀ x y, (x, y) ∈ N → (y, x) ∈ N

theorem pairF_shape (k : ℤ) (F : Finset (Sym2 Atom)) (Q : Finset (ℤ × ℤ)) : PairShape Q (pairF k F Q) := by
  refine ⟨pairF_sub k F Q, fun x hx => ?_, fun x y h => ?_⟩
  · exact Finset.mem_filter.mpr ⟨Finset.mem_product.mpr ⟨hx, hx⟩, Relation.ReflTransGen.refl⟩
  · obtain ⟨hm, hc⟩ := Finset.mem_filter.mp h
    obtain ⟨hx, hy⟩ := Finset.mem_product.mp hm
    exact Finset.mem_filter.mpr ⟨Finset.mem_product.mpr ⟨hy, hx⟩, conn_symm hc⟩

theorem Fc_zero_of_shape {σ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {s : ℕ}
    (h : ¬ PairShape Q N) : Fc σ k Q N s = 0 := by
  have e : FarSet σ k Q N s = ∅ := by
    ext F; simp only [FarSet, Set.mem_ofPred_eq, Set.mem_empty_iff_false, iff_false]
    rintro ⟨-, -, hN⟩; exact h (hN ▸ pairF_shape k F Q)
  unfold Fc; rw [e]; simp

/-- For two points `a ≠ b`, the half-turn about their midpoint (`d = a + b`) swaps them and keeps any pairing shape. -/
theorem swap_two {a b : ℤ × ℤ} {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} (hN : PairShape {a, b} N) :
    gP (a + b) {a, b} = {a, b} ∧ gM (a + b) N = N := by
  have hga : a + b - a = b := by abel
  have hgb : a + b - b = a := by abel
  refine ⟨by unfold gP; rw [Finset.image_insert, Finset.image_singleton, hga, hgb, Finset.pair_comm], ?_⟩
  obtain ⟨hsub, hdiag, hsym⟩ := hN
  have key : ∀ x ∈ N, gg (a + b) x ∈ N := by
    rintro ⟨x, y⟩ hxy
    have hm := Finset.mem_product.mp (hsub hxy)
    simp only [Finset.mem_insert, Finset.mem_singleton] at hm
    obtain ⟨hx, hy⟩ := hm
    simp only [gg]
    rcases hx with rfl | rfl <;> rcases hy with rfl | rfl
    · rw [hga]; exact hdiag b (by simp)
    · rw [hga, hgb]; exact hsym _ _ hxy
    · rw [hga, hgb]; exact hsym _ _ hxy
    · rw [hgb]; exact hdiag a (by simp)
  apply Finset.Subset.antisymm
  · intro x hx; obtain ⟨y, hy, rfl⟩ := Finset.mem_image.mp hx; exact key y hy
  · intro x hx; exact Finset.mem_image.mpr ⟨gg (a + b) x, key x hx, gg_gg _ x⟩

theorem shape_gM {c : ℤ × ℤ} {Q : Finset (ℤ × ℤ)} {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} (h : PairShape Q N) :
    PairShape (gP c Q) (gM c N) := by
  obtain ⟨hsub, hdiag, hsym⟩ := h
  refine ⟨gM_sub hsub, fun x hx => ?_, fun x y hxy => ?_⟩
  · exact mem_gM.mpr (by simp only [gg]; exact hdiag _ (mem_gP.mp hx))
  · rw [mem_gM] at hxy ⊢; simp only [gg] at hxy ⊢; exact hsym _ _ hxy

theorem goodCentre_sum {σ : ℤ → ZMod 3} {k : ℤ} {a b : ℤ × ℤ} (ha : (a.1 : ZMod 3) = σ k ∧ (a.2 : ZMod 3) = σ k)
    (hb : (b.1 : ZMod 3) = σ k ∧ (b.2 : ZMod 3) = σ k) : GoodCentre σ k (a + b) := by
  unfold GoodCentre; simp only [Prod.fst_add, Prod.snd_add, Int.cast_add, ha.1, ha.2, hb.1, hb.2]
  constructor <;> ring

/-- **Single arcs.** For a crossing set of two points of the position of bilayer `k`, the far counts at `P` and at its
half-turn `c − P` are equal, for every pairing and size. -/
theorem Fc_two {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {a b : ℤ × ℤ}
    (ha : (a.1 : ZMod 3) = σ k ∧ (a.2 : ZMod 3) = σ k) (hb : (b.1 : ZMod 3) = σ k ∧ (b.2 : ZMod 3) = σ k)
    (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (s : ℕ) :
    Fc σ k {a, b} N s = Fc σ k (gP c {a, b}) (gM c N) s := by
  set τ := flipAt σ k
  have hP : gP c {a, b} = {c - a, c - b} := by unfold gP; rw [Finset.image_insert, Finset.image_singleton]
  -- the half-turn image points are of the position of bilayer k too
  unfold GoodCentre at hc
  have ha' : ((c - a).1 : ZMod 3) = σ k ∧ ((c - a).2 : ZMod 3) = σ k := by
    simp only [Prod.fst_sub, Prod.snd_sub, Int.cast_sub, hc.1, hc.2, ha.1, ha.2]; constructor <;> ring
  have hb' : ((c - b).1 : ZMod 3) = σ k ∧ ((c - b).2 : ZMod 3) = σ k := by
    simp only [Prod.fst_sub, Prod.snd_sub, Int.cast_sub, hc.1, hc.2, hb.1, hb.2]; constructor <;> ring
  have hd := goodCentre_sum ha' hb'
  have h1 := fc_transfer (σ := σ) (k := k) ⟨hc.1, hc.2⟩ {a, b} N s
  have h2 := fc_transfer hd (gP c {a, b}) (gM c N) s
  by_cases hs : PairShape (gP c {a, b}) (gM c N)
  · rw [hP] at hs h1 h2
    obtain ⟨e1, e2⟩ := swap_two hs
    rw [e1, e2] at h2
    rw [h1, hP, h2]
  · rw [Fc_zero_of_shape hs]
    have : ¬ PairShape {a, b} N := fun h => hs (shape_gM h)
    rw [Fc_zero_of_shape this]

end LoopEqualityProof
