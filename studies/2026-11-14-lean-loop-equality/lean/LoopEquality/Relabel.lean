module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Surgery
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.CorollaryA1

@[expose] public section

/-!
# Relabelling the positions (Lean paper, Milestone 2f-1)

The half-turn `p ↦ c − p` of the whole network, with `c ≡ 2a` (mod 3) in both coordinates, maps `G σ` onto
`G (tog a ∘ σ)`, the stacking with every letter swapped by `tog a`. It keeps bilayers and levels, so it keeps
polygons, their lengths, and their crossing numbers at every bilayer.

* `isSite_htA`, `bond_htA`: sites and bonds go to sites and bonds.
* `ncard_polysA1_relabel`: `G σ` at `v` and `G (tog a ∘ σ)` at `htA c v` have equally many polygons of each
  length crossing every bilayer at most twice.
* `ncard_polysA1_mirror`: the mirror (bilayer `j ↦ −j`, lower and upper exchanged) keeps the counts.
* `ncard_polysA1_flipBelow`: the counts at `v` are kept across a flip *below* `v` (`flipBelow σ k` swaps the
  letters below bilayer `k`), by the mirror and the flip above (`mirS_flipBelow`).

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

theorem isSite_htA {σ : ℤ → ZMod 3} {a : ZMod 3} {c : ℤ × ℤ} (hc : (c.1 : ZMod 3) = 2 * a ∧ (c.2 : ZMod 3) = 2 * a)
    {v : Atom} (hv : IsSite σ v) : IsSite (fun j => tog a (σ j)) (htA c v) := by
  obtain ⟨j, ⟨p1, p2⟩, u⟩ := v
  unfold IsSite at hv ⊢
  simp [htA, hc.1, hc.2, hv.1, hv.2, tog]

theorem bond_htA {σ : ℤ → ZMod 3} {a : ZMod 3} {c : ℤ × ℤ} (hc : (c.1 : ZMod 3) = 2 * a ∧ (c.2 : ZMod 3) = 2 * a)
    {v w : Atom} (h : Bond σ v w) : Bond (fun j => tog a (σ j)) (htA c v) (htA c w) := by
  obtain ⟨hv, hw, hb⟩ := h
  refine ⟨isSite_htA hc hv, isSite_htA hc hw, ?_⟩
  obtain ⟨j, p, u⟩ := v
  obtain ⟨j', q, u'⟩ := w
  simp only [htA] at hb ⊢
  rcases hb with ⟨h1, h2, h3⟩ | ⟨h1, h2, h3, h4⟩ | ⟨h1, h2, h3, h4⟩
  · exact Or.inl ⟨h1, by rw [h2], h3⟩
  · refine Or.inr (Or.inl ⟨h1, h2, h3, ?_⟩)
    have : c - q - (c - p) = -(q - p) := by abel
    rw [this]; exact neg_mem_shortVecs h4
  · refine Or.inr (Or.inr ⟨h1, h2, h3, ?_⟩)
    have : c - p - (c - q) = -(p - q) := by abel
    rw [this]; exact neg_mem_shortVecs h4

theorem htS_injective (c : ℤ × ℤ) : Function.Injective (htS c) := by
  intro x y h; have := congrArg (htS c) h; rwa [htS_htS, htS_htS] at this

theorem degS_htS (c : ℤ × ℤ) (E : Finset (Sym2 Atom)) (x : Atom) :
    degS (E.image (htS c)) (htA c x) = degS E x := by
  unfold degS
  rw [Finset.filter_image, Finset.card_image_of_injective _ (htS_injective c)]
  congr 1
  apply Finset.filter_congr
  intro e _
  induction e using Sym2.ind with
  | _ a b =>
    show htA c x ∈ s(htA c a, htA c b) ↔ x ∈ s(a, b)
    rw [Sym2.mem_iff, Sym2.mem_iff]
    constructor
    · rintro (h | h)
      · left; have := congrArg (htA c) h; rwa [htA_htA, htA_htA] at this
      · right; have := congrArg (htA c) h; rwa [htA_htA, htA_htA] at this
    · rintro (rfl | rfl)
      · exact Or.inl rfl
      · exact Or.inr rfl

theorem closed_htS {c : ℤ × ℤ} {E : Finset (Sym2 Atom)} (h : Closed E) : Closed (E.image (htS c)) := by
  intro x
  have := degS_htS c E (htA c x)
  rw [htA_htA] at this
  rw [this]; exact h _

theorem crossN_htS (c : ℤ × ℤ) (E : Finset (Sym2 Atom)) (j : ℤ) : crossN (E.image (htS c)) j = crossN E j := by
  unfold crossN
  rw [Finset.filter_image, Finset.card_image_of_injective _ (htS_injective c)]
  congr 1
  exact Finset.filter_congr (fun e _ => isCrossS_htS)

theorem image_htS_htS (c : ℤ × ℤ) (E : Finset (Sym2 Atom)) : (E.image (htS c)).image (htS c) = E := by
  rw [Finset.image_image]
  have : htS c ∘ htS c = id := funext (htS_htS c)
  rw [this, Finset.image_id]

theorem tog_tog_fun (a : ZMod 3) (σ : ℤ → ZMod 3) : (fun j => tog a (tog a (σ j))) = σ := by
  funext j; exact tog_tog a (σ j)

theorem mapsTo_relabel {σ : ℤ → ZMod 3} {a : ZMod 3} {c : ℤ × ℤ}
    (hc : (c.1 : ZMod 3) = 2 * a ∧ (c.2 : ZMod 3) = 2 * a) (v : Atom) (l : ℕ) :
    Set.MapsTo (fun E : Finset (Sym2 Atom) => E.image (htS c)) (PolysA1 σ v l)
      (PolysA1 (fun j => tog a (σ j)) (htA c v) l) := by
  intro E ⟨⟨hne, hbond, hcl, hmin⟩, hv, hcard, hprof⟩
  refine ⟨⟨hne.image _, ?_, closed_htS hcl, ?_⟩, by rw [degS_htS]; exact hv,
    by rw [Finset.card_image_of_injective _ (htS_injective c), hcard], fun j => by rw [crossN_htS]; exact hprof j⟩
  · intro f hf
    obtain ⟨e, he, rfl⟩ := Finset.mem_image.mp hf
    have hb := hbond e he
    induction e using Sym2.ind with
    | _ x y =>
      rw [bondS_mk] at hb
      show BondS _ s(htA c x, htA c y)
      rw [bondS_mk]; exact bond_htA hc hb
  · intro F hF hFne hFcl
    have hsub : F.image (htS c) ⊆ E := by
      intro f hf
      obtain ⟨f', hf', rfl⟩ := Finset.mem_image.mp hf
      obtain ⟨e, he, rfl⟩ := Finset.mem_image.mp (hF hf')
      rw [htS_htS]; exact he
    have := hmin _ hsub (hFne.image _) (closed_htS hFcl)
    rw [← this]; exact (image_htS_htS c F).symm

/-- **Relabelling.** `G σ` at `v` and `G (tog a ∘ σ)` at `htA c v` (`c ≡ 2a`) have the same number of
polygons of each length crossing every bilayer at most twice. -/
theorem ncard_polysA1_relabel {σ : ℤ → ZMod 3} {a : ZMod 3} {c : ℤ × ℤ}
    (hc : (c.1 : ZMod 3) = 2 * a ∧ (c.2 : ZMod 3) = 2 * a) (v : Atom) (l : ℕ) :
    (PolysA1 σ v l).ncard = (PolysA1 (fun j => tog a (σ j)) (htA c v) l).ncard := by
  have hf := mapsTo_relabel (σ := σ) hc v l
  have hb := mapsTo_relabel (σ := fun j => tog a (σ j)) hc (htA c v) l
  rw [tog_tog_fun, htA_htA] at hb
  have hbij : Set.BijOn (fun E : Finset (Sym2 Atom) => E.image (htS c)) (PolysA1 σ v l)
      (PolysA1 (fun j => tog a (σ j)) (htA c v) l) := by
    refine ⟨hf, fun E₁ _ E₂ _ h => Finset.image_injective (htS_injective c) h, fun E' hE' => ?_⟩
    exact ⟨E'.image (htS c), hb hE', image_htS_htS c E'⟩
  rw [← hbij.image_eq, hbij.injOn.ncard_image]

/-- The mirror of an atom: bilayer `j ↦ −j`, lower and upper exchanged, planar point kept. -/
def mirA (a : Atom) : Atom := (-a.1, a.2.1, 1 - a.2.2)

theorem mirA_mirA (a : Atom) : mirA (mirA a) = a := by
  obtain ⟨j, p, u⟩ := a
  simp only [mirA, neg_neg, Prod.mk.injEq, true_and]
  fin_cases u <;> rfl

/-- The mirrored stacking. -/
def mirS (σ : ℤ → ZMod 3) (i : ℤ) : ZMod 3 := σ (-i)

theorem mirS_isStacking {σ : ℤ → ZMod 3} (hσ : IsStacking σ) : IsStacking (mirS σ) := by
  intro i
  unfold mirS
  have := hσ (-(i + 1))
  rw [show -(i + 1) + 1 = -i by ring] at this
  exact fun h => this h.symm

theorem isSite_mirA {σ : ℤ → ZMod 3} {v : Atom} (hv : IsSite σ v) : IsSite (mirS σ) (mirA v) := by
  obtain ⟨j, p, u⟩ := v
  unfold IsSite mirS mirA at *
  simpa using hv

theorem bond_mirA {σ : ℤ → ZMod 3} {v w : Atom} (h : Bond σ v w) : Bond (mirS σ) (mirA v) (mirA w) := by
  obtain ⟨hv, hw, hb⟩ := h
  refine ⟨isSite_mirA hv, isSite_mirA hw, ?_⟩
  obtain ⟨j, p, u⟩ := v
  obtain ⟨j', q, u'⟩ := w
  simp only [mirA] at hb ⊢
  rcases hb with ⟨h1, h2, h3⟩ | ⟨h1, h2, h3, h4⟩ | ⟨h1, h2, h3, h4⟩
  · refine Or.inl ⟨by rw [h1], h2, ?_⟩
    intro h; apply h3
    have := congrArg (fun x : Fin 2 => 1 - x) h
    simpa using this
  · subst h2; subst h3
    refine Or.inr (Or.inr ⟨by omega, by decide, by decide, ?_⟩)
    have : p - q = -(q - p) := by abel
    rw [this]; exact neg_mem_shortVecs h4
  · subst h2; subst h3
    refine Or.inr (Or.inl ⟨by omega, by decide, by decide, ?_⟩)
    have : q - p = -(p - q) := by abel
    rw [this]; exact neg_mem_shortVecs h4

theorem isFar_mirA {k : ℤ} {a : Atom} : IsFar (-k) (mirA a) ↔ ¬ IsFar k a := by
  obtain ⟨j, p, u⟩ := a
  unfold IsFar mirA
  simp only
  fin_cases u <;> simp <;> omega

/-- The mirror of an edge. -/
def mirE : Sym2 Atom → Sym2 Atom := Sym2.map mirA

theorem mirE_mirE (e : Sym2 Atom) : mirE (mirE e) = e := by
  unfold mirE; rw [Sym2.map_map]
  have : (mirA ∘ mirA) = id := funext mirA_mirA
  rw [this, Sym2.map_id]; rfl

theorem mirE_injective : Function.Injective mirE := by
  intro x y h; have := congrArg mirE h; rwa [mirE_mirE, mirE_mirE] at this

theorem isCrossS_mirE {k : ℤ} {e : Sym2 Atom} : IsCrossS (-k) (mirE e) ↔ IsCrossS k e := by
  induction e using Sym2.ind with
  | _ a b =>
    show IsCrossS (-k) s(mirA a, mirA b) ↔ _
    rw [isCrossS_mk, isCrossS_mk, isFar_mirA, isFar_mirA]
    by_cases ha : IsFar k a <;> by_cases hb : IsFar k b <;> simp [ha, hb]

theorem degS_mirE (E : Finset (Sym2 Atom)) (x : Atom) : degS (E.image mirE) (mirA x) = degS E x := by
  unfold degS
  rw [Finset.filter_image, Finset.card_image_of_injective _ mirE_injective]
  congr 1
  apply Finset.filter_congr
  intro e _
  induction e using Sym2.ind with
  | _ a b =>
    show mirA x ∈ s(mirA a, mirA b) ↔ x ∈ s(a, b)
    rw [Sym2.mem_iff, Sym2.mem_iff]
    constructor
    · rintro (h | h)
      · left; have := congrArg mirA h; rwa [mirA_mirA, mirA_mirA] at this
      · right; have := congrArg mirA h; rwa [mirA_mirA, mirA_mirA] at this
    · rintro (rfl | rfl)
      · exact Or.inl rfl
      · exact Or.inr rfl

theorem closed_mirE {E : Finset (Sym2 Atom)} (h : Closed E) : Closed (E.image mirE) := by
  intro x
  have := degS_mirE E (mirA x)
  rw [mirA_mirA] at this
  rw [this]; exact h _

theorem crossN_mirE (E : Finset (Sym2 Atom)) (j : ℤ) : crossN (E.image mirE) (-j) = crossN E j := by
  unfold crossN
  rw [Finset.filter_image, Finset.card_image_of_injective _ mirE_injective]
  congr 1
  exact Finset.filter_congr (fun e _ => isCrossS_mirE)

theorem image_mirE_mirE (E : Finset (Sym2 Atom)) : (E.image mirE).image mirE = E := by
  rw [Finset.image_image]
  have : mirE ∘ mirE = id := funext mirE_mirE
  rw [this, Finset.image_id]

theorem mirS_mirS (σ : ℤ → ZMod 3) : mirS (mirS σ) = σ := by
  funext i; simp [mirS]

theorem mapsTo_mirror {σ : ℤ → ZMod 3} (v : Atom) (l : ℕ) :
    Set.MapsTo (fun E : Finset (Sym2 Atom) => E.image mirE) (PolysA1 σ v l) (PolysA1 (mirS σ) (mirA v) l) := by
  intro E ⟨⟨hne, hbond, hcl, hmin⟩, hv, hcard, hprof⟩
  refine ⟨⟨hne.image _, ?_, closed_mirE hcl, ?_⟩, by rw [degS_mirE]; exact hv,
    by rw [Finset.card_image_of_injective _ mirE_injective, hcard], fun j => ?_⟩
  · intro f hf
    obtain ⟨e, he, rfl⟩ := Finset.mem_image.mp hf
    have hb := hbond e he
    induction e using Sym2.ind with
    | _ x y =>
      rw [bondS_mk] at hb
      show BondS _ s(mirA x, mirA y)
      rw [bondS_mk]; exact bond_mirA hb
  · intro F hF hFne hFcl
    have hsub : F.image mirE ⊆ E := by
      intro f hf
      obtain ⟨f', hf', rfl⟩ := Finset.mem_image.mp hf
      obtain ⟨e, he, rfl⟩ := Finset.mem_image.mp (hF hf')
      rw [mirE_mirE]; exact he
    have := hmin _ hsub (hFne.image _) (closed_mirE hFcl)
    rw [← this]; exact (image_mirE_mirE F).symm
  · have := crossN_mirE E (-j)
    rw [neg_neg] at this
    rw [this]; exact hprof (-j)

/-- **Mirror.** `G σ` at `v` and the mirrored network at `mirA v` have the same number of polygons of each
length crossing every bilayer at most twice. -/
theorem ncard_polysA1_mirror (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) :
    (PolysA1 σ v l).ncard = (PolysA1 (mirS σ) (mirA v) l).ncard := by
  have hf := mapsTo_mirror (σ := σ) v l
  have hb := mapsTo_mirror (σ := mirS σ) (mirA v) l
  rw [mirS_mirS, mirA_mirA] at hb
  have hbij : Set.BijOn (fun E : Finset (Sym2 Atom) => E.image mirE) (PolysA1 σ v l)
      (PolysA1 (mirS σ) (mirA v) l) :=
    ⟨hf, fun E₁ _ E₂ _ h => Finset.image_injective mirE_injective h,
      fun E' hE' => ⟨E'.image mirE, hb hE', image_mirE_mirE E'⟩⟩
  rw [← hbij.image_eq, hbij.injOn.ncard_image]

/-- The stacking with the letters *below* bilayer `k` swapped by `tog (σ k)` (the c/h letter of bilayer `k`
flipped, the positions at and above `k` kept). -/
def flipBelow (σ : ℤ → ZMod 3) (k : ℤ) (j : ℤ) : ZMod 3 := if k ≤ j then σ j else tog (σ k) (σ j)

theorem mirS_flipBelow (σ : ℤ → ZMod 3) (k : ℤ) : mirS (flipBelow σ k) = flipAt (mirS σ) (-k) := by
  funext i
  unfold mirS flipBelow flipAt
  by_cases h : i ≤ -k
  · simp only [show k ≤ -i by omega, h, ↓reduceIte]
  · simp only [show ¬ k ≤ -i by omega, h, ↓reduceIte, neg_neg]

/-- **Corollary A1 across a flip below `v`.** If `v` lies in the far half of bilayer `k`, flipping the
c/h letter of bilayer `k` by changing the letters below `k` keeps the counts at `v`. -/
theorem ncard_polysA1_flipBelow {σ : ℤ → ZMod 3} {k : ℤ} {v : Atom} (hv : IsFar k v) (l : ℕ) :
    (PolysA1 (flipBelow σ k) v l).ncard = (PolysA1 σ v l).ncard := by
  rw [ncard_polysA1_mirror (flipBelow σ k) v l, mirS_flipBelow, ncard_polysA1_mirror σ v l]
  have hroot : ¬ IsFar (-k) (mirA v) := fun h => (isFar_mirA.mp h) hv
  exact (ncard_polysA1_flip hroot l).symm

end LoopEqualityProof
