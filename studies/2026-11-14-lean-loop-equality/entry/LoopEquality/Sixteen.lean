module

public import Mathlib
public import LoopEquality.Regroup
public import LoopEquality.MinRoot
public import LoopEquality.Split

@[expose] public section

/-!
# Toward one flip keeping the polygons of length 16

The surviving terms at `l = 16`: four crossing points, six edges on each side.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-- The surviving terms of Theorem B at `l = 16` for the atom `a` and the crossing set `P`. -/
noncomputable def G16 (σ : ℤ → ZMod 3) (k : ℤ) (c : ℤ × ℤ) (a : Atom) (P : Finset (ℤ × ℤ)) : ℤ :=
  ∑ x ∈ idxSet 16 P P (OneCycleRel P),
    if P.card = 4 ∧ x.2.1 = 6 ∧ x.2.2 = 6 then Wc σ a k P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 else 0

theorem trP_as_g (d : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : trP d P = gP d (gP 0 P) := by
  rw [gP_gP']; simp

theorem trM_as_g (d : ℤ × ℤ) (M : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : trM d M = gM d (gM 0 M) := by
  rw [gM_gM']; simp

theorem idx_tr_mem {l : ℕ} {d : ℤ × ℤ} {P : Finset (ℤ × ℤ)} {x} (hx : x ∈ idxSet l P P (OneCycleRel P)) :
    ((trM d x.1.1, trM d x.1.2), x.2) ∈ idxSet l (trP d P) (trP d P) (OneCycleRel (trP d P)) := by
  rw [trP_as_g, trM_as_g, trM_as_g]
  exact idx_g_mem (c := d) (idx_g_mem (c := 0) hx)

theorem trM_trM_neg (d : ℤ × ℤ) (M : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : trM (-d) (trM d M) = M := trM_neg d M

theorem trP_trP_neg (d : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : trP (-d) (trP d P) = P := trP_neg d P

theorem card_trP (d : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : (trP d P).card = P.card := by
  unfold trP; exact Finset.card_image_of_injective _ (fun p q h => by simpa using h)

/-- **The surviving terms are invariant under joint lattice translations.** -/
theorem G16_translate (σ : ℤ → ZMod 3) (k : ℤ) (c : ℤ × ℤ) {d : ℤ × ℤ} (hd : GoodVec d) (a : Atom)
    (P : Finset (ℤ × ℤ)) : G16 σ k c (posA d a) (trP d P) = G16 σ k c a P := by
  unfold G16
  symm
  apply Finset.sum_nbij' (fun x => ((trM d x.1.1, trM d x.1.2), x.2)) (fun x => ((trM (-d) x.1.1, trM (-d) x.1.2), x.2))
  · intro x hx; exact idx_tr_mem hx
  · intro x hx; have := idx_tr_mem (d := -d) hx; rwa [trP_trP_neg] at this
  · intro x _; simp [trM_trM_neg]
  · intro x _
    have : ∀ M, trM d (trM (-d) M) = M := fun M => by have := trM_neg (-d) M; rwa [neg_neg] at this
    simp [this]
  · intro x _
    simp only [card_trP]
    split_ifs
    · rw [Wc_translate hd, Af_translate hd]
    · rfl

theorem goodVec_sc (f : ℤ × ℤ) : GoodVec (sc f) := by
  unfold GoodVec sc; push_cast
  constructor <;> rw [show (3 : ZMod 3) = 0 from rfl, zero_mul]

/-! ## Reduction to the (6, 6) terms -/

/-- A crossing set carrying a root linkage has vertical bonds at all its points. -/
theorem bonds_of_Wc {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {P : Finset (ℤ × ℤ)} {M : Finset ((ℤ × ℤ) × (ℤ × ℤ))}
    {r : ℕ} (h : Wc σ v k P M r ≠ 0) : ∀ p ∈ P, BondS σ (vert k p) := by
  obtain ⟨R, hR⟩ : (RootSet σ v k P M r).Nonempty := by
    rw [Set.nonempty_iff_ne_empty]; intro h0; apply h; unfold Wc; rw [h0]; simp
  intro p hp
  have hd : degS R (loA k p) = 1 := hR.1.1.1 _ (Finset.mem_image_of_mem _ hp)
  obtain ⟨e, he, hpe⟩ := exists_edge_of_degS (by omega : 0 < degS R (loA k p))
  have hb := hR.1.2.2 e he
  have hsite : IsSite σ (loA k p) := by
    induction e using Sym2.ind with
    | _ x y =>
      rw [bondS_mk] at hb
      rcases Sym2.mem_iff.mp hpe with h1 | h1
      · rw [h1]; exact hb.1
      · rw [h1]; exact hb.2.1
  rw [bondS_vert_iff]; exact hsite

theorem G16_support {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {v : Atom} (hv : ¬ IsFar k v)
    {P : Finset (ℤ × ℤ)} (h : G16 σ k c v P ≠ 0) : P ∈ famP σ v 16 k c ∧ P.Nonempty := by
  unfold G16 at h
  obtain ⟨x, hx, hne⟩ := Finset.exists_ne_zero_of_sum_ne_zero h
  split_ifs at hne with hcond
  · have hW := left_ne_zero_of_mul hne
    have hA := right_ne_zero_of_mul hne
    have hx' := Finset.mem_filter.mp hx
    have hPne : P.Nonempty := Finset.card_pos.mp (by omega)
    have hV := bonds_of_Wc hW
    have hw := window_of_term hc hv hPne hV hx'.2.2 hW hA
    rw [hx'.2.1] at hw
    refine ⟨?_, hPne⟩
    simp only [famP, Finset.mem_filter, Finset.mem_powerset]
    exact ⟨hw.trans Finset.subset_union_left, hPne, hV⟩
  · exact absurd rfl hne

/-- At `l = 16` every term is a minimal-root term or a (6, 6) term. -/
theorem term16 {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {P : Finset (ℤ × ℤ)}
    (hP : P ∈ famP σ v 16 k c) {x} (hx : x ∈ idxSet 16 P P (OneCycleRel P)) :
    Wc σ v k P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 =
      (if x.2.1 = P.card then Wc σ v k P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 else 0) +
      (if P.card = 4 ∧ x.2.1 = 6 ∧ x.2.2 = 6 then Wc σ v k P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 else 0) := by
  have hsum := (Finset.mem_filter.mp hx).2.1
  simp only [famP, Finset.mem_filter] at hP
  obtain ⟨-, hne, hV⟩ := hP
  by_cases h1 : x.2.1 = P.card
  · rw [if_pos h1, if_neg (by omega), add_zero]
  rw [if_neg h1, zero_add]
  by_cases h2 : P.card = 4 ∧ x.2.1 = 6 ∧ x.2.2 = 6
  · rw [if_pos h2]
  rw [if_neg h2]
  by_cases hr : x.2.1 < P.card
  · rw [Wc_zero hr, zero_mul]
  by_cases hs : x.2.2 < P.card
  · rw [Af_zero hs, mul_zero]
  by_cases hev : Even P.card
  swap
  · rw [Af_odd hev, mul_zero]
  by_cases hro : Even x.2.1
  swap
  · rw [Wc_odd_size hro, zero_mul]
  have hpos : 0 < P.card := Finset.card_pos.mpr hne
  obtain ⟨t, ht⟩ := hev
  obtain ⟨u, hu⟩ := hro
  have h24 : P.card = 2 ∨ P.card = 4 := by omega
  rcases h24 with h2' | h4
  · obtain ⟨a, b, hab, rfl⟩ := Finset.card_eq_two.mp h2'
    have ha := bondS_vert_iff.mp (hV a (by simp)); have hb := bondS_vert_iff.mp (hV b (by simp))
    have : Af σ k c {a, b} x.1.2 x.2.2 = 0 := by unfold Af; rw [Fc_two hc ha hb]; simp
    rw [this, mul_zero]
  · have : x.2.2 = P.card := by omega
    rw [this, Af_min hc, mul_zero]

/-- **At `l = 16` the change is carried by the (6, 6) terms alone.** -/
theorem sumWc_16_iff {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) (hv : ¬ IsFar k v) :
    ∑ P ∈ famP σ v 16 k c, ∑ x ∈ idxSet 16 P P (OneCycleRel P), Wc σ v k P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 =
      ∑ P ∈ famP σ v 16 k c, G16 σ k c v P := by
  rw [Finset.sum_congr rfl (fun P hP => Finset.sum_congr rfl (fun x hx => term16 hc hP hx))]
  simp only [Finset.sum_add_distrib]
  rw [minRoot_zero hc hv, zero_add]
  rfl

/-! ## The shifts of `v` that can matter for a shape -/

/-- Shifts `f` with `v + 3 f` within 12 of a point of `S`. -/
def T16 (v : Atom) (S : Finset (ℤ × ℤ)) : Finset (ℤ × ℤ) :=
  S.biUnion (fun p =>
    Finset.Icc ((p.1 - v.2.1.1 - 12) / 3 - 1) ((p.1 - v.2.1.1 + 12) / 3 + 1) ×ˢ
    Finset.Icc ((p.2 - v.2.1.2 - 12) / 3 - 1) ((p.2 - v.2.1.2 + 12) / 3 + 1))

/-- An atom on a root linkage with `r` edges at `S` lies within `2 r` of a point of `S`. -/
theorem near_of_Wc {σ : ℤ → ZMod 3} {a : Atom} {k : ℤ} {S : Finset (ℤ × ℤ)} {M : Finset ((ℤ × ℤ) × (ℤ × ℤ))}
    {r : ℕ} (h : Wc σ a k S M r ≠ 0) :
    ∃ p ∈ S, |a.2.1.1 - p.1| ≤ 2 * r ∧ |a.2.1.2 - p.2| ≤ 2 * r := by
  rw [Wc_mir] at h
  obtain ⟨F, hF, hw⟩ := Set.nonempty_of_ncard_ne_zero (by exact_mod_cast h)
  obtain ⟨e, he, hae⟩ := exists_edge_of_degS hw
  have hbox := farL_in_box hF.1 he
  rw [hF.2.1] at hbox
  induction e using Sym2.ind with
  | _ x y =>
    rw [Finset.mk_mem_sym2_iff] at hbox
    have hin : mirA a ∈ S.biUnion (fun p => box (upA (-k) p) (2 * r)) := by
      rcases Sym2.mem_iff.mp hae with h1 | h1
      · rw [h1]; exact hbox.1
      · rw [h1]; exact hbox.2
    obtain ⟨p, hp, hb⟩ := Finset.mem_biUnion.mp hin
    simp only [box, upA, mirA, Finset.mem_product, Finset.mem_Icc, Finset.mem_univ, and_true] at hb
    refine ⟨p, hp, ?_, ?_⟩ <;> rw [abs_le] <;> constructor <;> omega

theorem mem_T16 {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} {v : Atom} {S : Finset (ℤ × ℤ)} {f : ℤ × ℤ}
    (h : G16 σ k c (posA (sc f) v) S ≠ 0) : f ∈ T16 v S := by
  unfold G16 at h
  obtain ⟨x, -, hne⟩ := Finset.exists_ne_zero_of_sum_ne_zero h
  split_ifs at hne with hcond
  · have hW := left_ne_zero_of_mul hne
    obtain ⟨p, hp, h1, h2⟩ := near_of_Wc hW
    rw [hcond.2.1] at h1 h2
    simp only [posA, sc, Prod.fst_add, Prod.snd_add] at h1 h2
    rw [abs_le] at h1 h2
    refine Finset.mem_biUnion.mpr ⟨p, hp, Finset.mem_product.mpr ⟨Finset.mem_Icc.mpr ⟨?_, ?_⟩, Finset.mem_Icc.mpr ⟨?_, ?_⟩⟩⟩ <;>
      push_cast at h1 h2 <;> omega
  · exact absurd rfl hne

/-- **Regrouped form of the (6, 6) sum**, for any list `Z` of class representatives containing every class that
carries a non-zero term. -/
theorem sum16_regroup {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {v : Atom} (hv : ¬ IsFar k v)
    (Z : Finset (Finset (ℤ × ℤ))) (hZ : ∀ P, G16 σ k c v P ≠ 0 → nrm P ∈ Z) (hZn : ∀ S ∈ Z, nrm S = S) :
    ∑ P ∈ famP σ v 16 k c, G16 σ k c v P = ∑ S ∈ Z, ∑ f ∈ T16 v S, G16 σ k c (posA (sc f) v) S :=
  regroup (G16 σ k c) v (fun f a P => G16_translate σ k c (goodVec_sc f) a P) _ (fun P h => (G16_support hc hv h).1)
    (fun P h => (G16_support hc hv h).2) Z hZ hZn (T16 v) (fun S f h => mem_T16 h)

end LoopEqualityProof
