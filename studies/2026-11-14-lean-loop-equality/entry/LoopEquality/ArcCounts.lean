module

public import Mathlib
public import LoopEquality.PathPairs
public import LoopEquality.Pairing14

@[expose] public section

/-!
# Computable counts: meeting arc pairs and root linkages through an atom

`meetCountL` counts pairs of far arcs (`a`–`b`, `c`–`d`, `s` edges in all) that share an atom; `throughCountL` counts
pairs with no common atom that pass through `w`. Both are evaluated on the enumerated paths, and both equal the
abstract counts: `ncard_meetPairs`, `Wc_four`, `Af_four_enum`.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

def disjB (l₁ l₂ : List Atom) : Bool := l₁.all (fun w => !(l₂.contains w))

theorem disjB_iff {l₁ l₂ : List Atom} : disjB l₁ l₂ = true ↔ ∀ w ∈ l₁, w ∉ l₂ := by
  simp [disjB]

def meetCountL (τ : ℤ → ZMod 3) (k : ℤ) (a b c d : ℤ × ℤ) (s : ℕ) : ℤ :=
  ∑ i ∈ Finset.range (s + 1), (((arcList τ k a b i) ×ˢ (arcList τ k c d (s - i))).filter
    (fun x => !disjB x.1 x.2)).length

def throughCountL (τ : ℤ → ZMod 3) (k : ℤ) (a b c d : ℤ × ℤ) (s : ℕ) (w : Atom) : ℤ :=
  ∑ i ∈ Finset.range (s + 1), (((arcList τ k a b i) ×ˢ (arcList τ k c d (s - i))).filter
    (fun x => disjB x.1 x.2 && (x.1.contains w || x.2.contains w))).length

theorem atomDisj_paths {l₁ l₂ : List Atom} (h1 : 2 ≤ l₁.length) (h2 : 2 ≤ l₂.length) :
    AtomDisj (pathEdges l₁) (pathEdges l₂) ↔ disjB l₁ l₂ = true := by
  rw [disjB_iff]
  constructor
  · intro h w hw1 hw2
    rcases h w with z | z
    · exact degS_pathEdges_out' h1 hw1 z
    · exact degS_pathEdges_out' h2 hw2 z
  · intro h w
    by_cases hw : w ∈ l₁
    · right; rw [degS_pathEdges_out (h w hw)]
    · left; exact degS_pathEdges_out hw
where degS_pathEdges_out' {l : List Atom} (h : 2 ≤ l.length) {w : Atom} (hw : w ∈ l) : degS (pathEdges l) w ≠ 0 :=
  (mem_path_deg h hw).ne'

theorem degS_union_pos (A B : Finset (Sym2 Atom)) (w : Atom) :
    0 < degS (A ∪ B) w ↔ 0 < degS A w ∨ 0 < degS B w := by
  unfold degS
  simp only [Finset.card_pos, Finset.filter_union, Finset.union_nonempty]

section
variable {τ : ℤ → ZMod 3} {k : ℤ} {a b c d : ℤ × ℤ}

theorem ncard_meetPairs (hab : a ≠ b) (hcd : c ≠ d) (s : ℕ) :
    ((MeetPairs τ k a b c d s).ncard : ℤ) = meetCountL τ k a b c d s := by
  unfold MeetPairs meetCountL
  rw [ncard_arcPairs_cond hab hcd s (fun x => ¬ AtomDisj x.1 x.2) (fun x => !disjB x.1 x.2) (by
    intro i l₁ l₂ h1 h2
    rw [atomDisj_paths (farPaths_len hab h1) (farPaths_len hcd h2)]
    simp)]
  simp only [Nat.cast_sum]

theorem ncard_twoArcs_through (hab : a ≠ b) (hcd : c ≠ d) (s : ℕ) (w : Atom) :
    (({x | x ∈ TwoArcs τ k a b c d s ∧ 0 < degS (x.1 ∪ x.2) w} : Set _).ncard : ℤ) =
      throughCountL τ k a b c d s w := by
  have e : {x | x ∈ TwoArcs τ k a b c d s ∧ 0 < degS (x.1 ∪ x.2) w} =
      {x | x ∈ ArcPairs τ k a b c d s ∧ (AtomDisj x.1 x.2 ∧ 0 < degS (x.1 ∪ x.2) w)} := by
    ext x; simp only [TwoArcs, ArcPairs, Set.mem_setOf_eq]
    constructor
    · rintro ⟨⟨h1, h2, h3, h4, h5, h6⟩, h7⟩; exact ⟨⟨h1, h2, h3, h4, h5⟩, h6, h7⟩
    · rintro ⟨⟨h1, h2, h3, h4, h5⟩, h6, h7⟩; exact ⟨⟨h1, h2, h3, h4, h5, h6⟩, h7⟩
  rw [e]; unfold throughCountL
  rw [ncard_arcPairs_cond hab hcd s (fun x => AtomDisj x.1 x.2 ∧ 0 < degS (x.1 ∪ x.2) w)
    (fun x => disjB x.1 x.2 && (x.1.contains w || x.2.contains w)) (by
    intro i l₁ l₂ h1 h2
    simp only
    rw [atomDisj_paths (farPaths_len hab h1) (farPaths_len hcd h2), degS_union_pos,
      deg_path (farPaths_len hab h1), deg_path (farPaths_len hcd h2)]
    simp)]
  simp only [Nat.cast_sum]

end

/-- **Root counts at four points, from the enumeration** (through the mirror). -/
theorem Wc_four {σ : ℤ → ZMod 3} {v : Atom} {k : ℤ} {p q r t : ℤ × ℤ}
    (hdis : ∀ x ∈ ({p, q} : Finset (ℤ × ℤ)), ∀ y ∈ ({r, t} : Finset (ℤ × ℤ)), x ≠ y) (hpq : p ≠ q) (hrt : r ≠ t)
    (s : ℕ) : Wc σ v k {p, q, r, t} (pr2 p q ∪ pr2 r t) s = throughCountL (mirS σ) (-k) p q r t s (mirA v) := by
  rw [Wc_mir]
  have := fc_four_pred (τ := mirS σ) (k := -k) hdis s (fun F => 0 < degS F (mirA v))
  rw [← ncard_twoArcs_through hpq hrt]
  exact_mod_cast this

/-- **The far asymmetry at four points, from the enumeration.** -/
theorem Af_four_enum {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {a b e f : ℤ × ℤ}
    (hV : ∀ p ∈ ({a, b, e, f} : Finset (ℤ × ℤ)), (p.1 : ZMod 3) = σ k ∧ (p.2 : ZMod 3) = σ k)
    (hdis : ∀ p ∈ ({a, b} : Finset (ℤ × ℤ)), ∀ q ∈ ({e, f} : Finset (ℤ × ℤ)), p ≠ q) (hab : a ≠ b) (hef : e ≠ f)
    (s : ℕ) :
    Af σ k c {a, b, e, f} (pr2 a b ∪ pr2 e f) s =
      meetCountL σ k (c - a) (c - b) (c - e) (c - f) s - meetCountL σ k a b e f s := by
  rw [Af_four hc hV hdis, ncard_meetPairs hab hef, ncard_meetPairs (by intro h; exact hab (by simpa using h))
    (by intro h; exact hef (by simpa using h))]

end LoopEqualityProof
