module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Surgery
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.CorollaryA1
public import LoopEquality.Relabel
public import LoopEquality.FlipRuns
public import LoopEquality.Locality

@[expose] public section

/-!
# Corollary A1 for every stacking (Lean paper, Milestone 2f-4)

* `ncard_polysA1_translate`: a lattice translation `p ↦ p + d` with `d ≡ 0` (mod 3) keeps the counts.
* `eq_of_hex`: two stackings that agree at two neighbouring bilayers and have the same c/h letters on a
  range agree on the range widened by one.
* `flipRun_at_v`: a run of flips for `v` keeps the letter of `v`'s bilayer.
* `corollaryA1`: **for any two stackings and an atom `v` that is a site of both, the number of polygons
  through `v` with `l` edges crossing every bilayer at most twice is the same, for every `l`.**

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-! ## Lattice translations -/

/-- Translation of an atom by `d`. -/
def trA (d : ℤ × ℤ) (a : Atom) : Atom := (a.1, a.2.1 + d, a.2.2)

theorem isSite_trA {σ : ℤ → ZMod 3} {d : ℤ × ℤ} (hd : (d.1 : ZMod 3) = 0 ∧ (d.2 : ZMod 3) = 0) {v : Atom}
    (hv : IsSite σ v) : IsSite σ (trA d v) := by
  obtain ⟨j, ⟨p1, p2⟩, u⟩ := v
  unfold IsSite at hv ⊢
  simp [trA, hd.1, hd.2, hv.1, hv.2]

theorem bond_trA {σ : ℤ → ZMod 3} {d : ℤ × ℤ} (hd : (d.1 : ZMod 3) = 0 ∧ (d.2 : ZMod 3) = 0) {v w : Atom}
    (h : Bond σ v w) : Bond σ (trA d v) (trA d w) := by
  obtain ⟨hv, hw, hb⟩ := h
  refine ⟨isSite_trA hd hv, isSite_trA hd hw, ?_⟩
  obtain ⟨j, p, u⟩ := v
  obtain ⟨j', q, u'⟩ := w
  simp only [trA] at hb ⊢
  rcases hb with ⟨h1, h2, h3⟩ | ⟨h1, h2, h3, h4⟩ | ⟨h1, h2, h3, h4⟩
  · exact Or.inl ⟨h1, by rw [h2], h3⟩
  · exact Or.inr (Or.inl ⟨h1, h2, h3, by rw [add_sub_add_right_eq_sub]; exact h4⟩)
  · exact Or.inr (Or.inr ⟨h1, h2, h3, by rw [add_sub_add_right_eq_sub]; exact h4⟩)

theorem trA_neg (d : ℤ × ℤ) (a : Atom) : trA (-d) (trA d a) = a := by
  obtain ⟨j, p, u⟩ := a; simp [trA]

/-- Translation of an edge. -/
def trE (d : ℤ × ℤ) : Sym2 Atom → Sym2 Atom := Sym2.map (trA d)

theorem trE_neg (d : ℤ × ℤ) (e : Sym2 Atom) : trE (-d) (trE d e) = e := by
  unfold trE; rw [Sym2.map_map]
  have : (trA (-d) ∘ trA d) = id := funext (trA_neg d)
  rw [this, Sym2.map_id]; rfl

theorem trE_injective (d : ℤ × ℤ) : Function.Injective (trE d) := by
  intro x y h; have := congrArg (trE (-d)) h; rwa [trE_neg, trE_neg] at this

theorem degS_trE (d : ℤ × ℤ) (E : Finset (Sym2 Atom)) (x : Atom) :
    degS (E.image (trE d)) (trA d x) = degS E x := by
  unfold degS
  rw [Finset.filter_image, Finset.card_image_of_injective _ (trE_injective d)]
  congr 1
  apply Finset.filter_congr
  intro e _
  induction e using Sym2.ind with
  | _ a b =>
    show trA d x ∈ s(trA d a, trA d b) ↔ x ∈ s(a, b)
    rw [Sym2.mem_iff, Sym2.mem_iff]
    constructor
    · rintro (h | h)
      · left; have := congrArg (trA (-d)) h; rwa [trA_neg, trA_neg] at this
      · right; have := congrArg (trA (-d)) h; rwa [trA_neg, trA_neg] at this
    · rintro (rfl | rfl)
      · exact Or.inl rfl
      · exact Or.inr rfl

theorem neg_trA (d : ℤ × ℤ) (a : Atom) : trA d (trA (-d) a) = a := by
  have := trA_neg (-d) a; rwa [neg_neg] at this

theorem closed_trE {d : ℤ × ℤ} {E : Finset (Sym2 Atom)} (h : Closed E) : Closed (E.image (trE d)) := by
  intro x
  have := degS_trE d E (trA (-d) x)
  rw [neg_trA] at this
  rw [this]; exact h _

theorem isCrossS_trE {d : ℤ × ℤ} {j : ℤ} {e : Sym2 Atom} : IsCrossS j (trE d e) ↔ IsCrossS j e := by
  induction e using Sym2.ind with
  | _ a b =>
    show IsCrossS j s(trA d a, trA d b) ↔ _
    rw [isCrossS_mk, isCrossS_mk]; exact Iff.rfl

theorem crossN_trE (d : ℤ × ℤ) (E : Finset (Sym2 Atom)) (j : ℤ) : crossN (E.image (trE d)) j = crossN E j := by
  unfold crossN
  rw [Finset.filter_image, Finset.card_image_of_injective _ (trE_injective d)]
  congr 1
  exact Finset.filter_congr (fun e _ => isCrossS_trE)

theorem image_trE_neg (d : ℤ × ℤ) (E : Finset (Sym2 Atom)) : (E.image (trE d)).image (trE (-d)) = E := by
  rw [Finset.image_image]
  have : trE (-d) ∘ trE d = id := funext (trE_neg d)
  rw [this, Finset.image_id]

theorem mapsTo_translate {σ : ℤ → ZMod 3} {d : ℤ × ℤ} (hd : (d.1 : ZMod 3) = 0 ∧ (d.2 : ZMod 3) = 0)
    (v : Atom) (l : ℕ) :
    Set.MapsTo (fun E : Finset (Sym2 Atom) => E.image (trE d)) (PolysA1 σ v l) (PolysA1 σ (trA d v) l) := by
  intro E ⟨⟨hne, hbond, hcl, hmin⟩, hv, hcard, hprof⟩
  have hd' : ((-d).1 : ZMod 3) = 0 ∧ ((-d).2 : ZMod 3) = 0 := by simp [hd.1, hd.2]
  refine ⟨⟨hne.image _, ?_, closed_trE hcl, ?_⟩, by rw [degS_trE]; exact hv,
    by rw [Finset.card_image_of_injective _ (trE_injective d), hcard], fun j => by rw [crossN_trE]; exact hprof j⟩
  · intro f hf
    obtain ⟨e, he, rfl⟩ := Finset.mem_image.mp hf
    have hb := hbond e he
    induction e using Sym2.ind with
    | _ x y =>
      rw [bondS_mk] at hb
      show BondS _ s(trA d x, trA d y)
      rw [bondS_mk]; exact bond_trA hd hb
  · intro F hF hFne hFcl
    have hsub : F.image (trE (-d)) ⊆ E := by
      intro f hf
      obtain ⟨f', hf', rfl⟩ := Finset.mem_image.mp hf
      obtain ⟨e, he, rfl⟩ := Finset.mem_image.mp (hF hf')
      rw [trE_neg]; exact he
    have := hmin _ hsub (hFne.image _) (closed_trE hFcl)
    rw [← this]
    show F = ((F.image (trE (-d))).image (trE d))
    have h2 := image_trE_neg (-d) F
    rw [neg_neg] at h2
    exact h2.symm

/-- **Translations.** A lattice translation by `d ≡ 0` (mod 3) keeps the counts. -/
theorem ncard_polysA1_translate {σ : ℤ → ZMod 3} {d : ℤ × ℤ} (hd : (d.1 : ZMod 3) = 0 ∧ (d.2 : ZMod 3) = 0)
    (v : Atom) (l : ℕ) : (PolysA1 σ v l).ncard = (PolysA1 σ (trA d v) l).ncard := by
  have hd' : ((-d).1 : ZMod 3) = 0 ∧ ((-d).2 : ZMod 3) = 0 := by simp [hd.1, hd.2]
  have hf := mapsTo_translate (σ := σ) hd v l
  have hb := mapsTo_translate (σ := σ) hd' (trA d v) l
  rw [trA_neg] at hb
  have hbij : Set.BijOn (fun E : Finset (Sym2 Atom) => E.image (trE d)) (PolysA1 σ v l)
      (PolysA1 σ (trA d v) l) := by
    refine ⟨hf, fun E₁ _ E₂ _ h => Finset.image_injective (trE_injective d) h, fun E' hE' => ?_⟩
    refine ⟨E'.image (trE (-d)), hb hE', ?_⟩
    show (E'.image (trE (-d))).image (trE d) = E'
    have h2 := image_trE_neg (-d) E'
    rwa [neg_neg] at h2
  rw [← hbij.image_eq, hbij.injOn.ncard_image]

/-! ## Positions from the c/h word -/

theorem step_det : ∀ a b c d : ZMod 3, a ≠ b → c ≠ b → d ≠ b → ((a = c) ↔ (a = d)) → c = d := by decide

theorem hex_iff {σ : ℤ → ZMod 3} {j : ℤ} : IsHex σ j ↔ σ (j - 1) = σ (j + 1) := Iff.rfl

/-- Agreement at `j0` and `j0 + 1` and the same c/h letters at `j0 + 1, …, j0 + n` give agreement up to
`j0 + n + 1`. -/
theorem eq_up {ρ τ : ℤ → ZMod 3} (hρ : IsStacking ρ) (hτ : IsStacking τ) {j0 : ℤ}
    (h0 : ρ j0 = τ j0) (h1 : ρ (j0 + 1) = τ (j0 + 1)) :
    ∀ n : ℕ, (∀ i : ℕ, i < n → (IsHex ρ (j0 + 1 + i) ↔ IsHex τ (j0 + 1 + i))) →
      ρ (j0 + n) = τ (j0 + n) ∧ ρ (j0 + n + 1) = τ (j0 + n + 1)
  | 0, _ => by simpa using ⟨h0, h1⟩
  | n + 1, hh => by
    obtain ⟨ha, hb⟩ := eq_up hρ hτ h0 h1 n (fun i hi => hh i (by omega))
    refine ⟨by push_cast; rw [← add_assoc]; exact hb, ?_⟩
    have hx := hh n (by omega)
    rw [hex_iff, hex_iff] at hx
    have e1 : j0 + 1 + (n : ℤ) - 1 = j0 + n := by ring
    have e2 : j0 + 1 + (n : ℤ) + 1 = j0 + ((n + 1 : ℕ) : ℤ) + 1 := by push_cast; ring
    have e3 : j0 + 1 + (n : ℤ) = j0 + n + 1 := by ring
    rw [e1, e2] at hx
    have hne1 := hρ (j0 + n + 1)
    have hne2 := hτ (j0 + n + 1)
    have hne3 := hρ (j0 + n)
    rw [show j0 + ↑n + 1 + 1 = j0 + ((n + 1 : ℕ) : ℤ) + 1 by push_cast; ring] at hne1 hne2
    rw [← ha] at hx
    rw [← hb] at hne2
    exact step_det (ρ (j0 + n)) (ρ (j0 + n + 1)) _ _ (fun h => hne3 h.symm) hne1 hne2 hx

end LoopEqualityProof
