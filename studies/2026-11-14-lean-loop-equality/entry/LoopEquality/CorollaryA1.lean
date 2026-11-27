module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Surgery
public import LoopEquality.Polygons
public import LoopEquality.TheoremA

@[expose] public section

/-!
# Corollary A1 across one flip (Lean paper, Milestone 2e)

Study 2026-11-15-polygon-bijection, Corollary A1.

`crossN E j` is the number of edges of `E` crossing the cut at bilayer `j`. `PolysA1 σ v l` is the set of
polygons of `G σ` through `v` with `l` edges that cross every bilayer at most twice.

* `crossN_surg`: the surgery at bilayer `k` keeps the crossing number at every bilayer.
* `cross_eq_vert`: a crossing bond at bilayer `k` is the vertical bond `vert k p` at a point `p` of the
  position of bilayer `k`.
* `ncard_polysA1_flip`: for an atom `v` in the root half of bilayer `k`, `G σ` and `G (flipAt σ k)` have the
  same number of such polygons, for every length `l`. The half-turn is taken about the midpoint of each
  polygon's own two crossing points at `k` (Lemma 2); polygons not crossing `k` are unchanged.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-- The number of edges of `E` crossing the cut at bilayer `j`. -/
noncomputable def crossN (E : Finset (Sym2 Atom)) (j : ℤ) : ℕ := (E.filter (IsCrossS j)).card

/-- Polygons of `G σ` through `v` with `l` edges crossing every bilayer at most twice. -/
def PolysA1 (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) : Set (Finset (Sym2 Atom)) :=
  {E | IsPolygon σ E ∧ 0 < degS E v ∧ E.card = l ∧ ∀ j, crossN E j ≤ 2}

theorem isFar_htA_any {c : ℤ × ℤ} {j : ℤ} {a : Atom} : IsFar j (htA c a) ↔ IsFar j a := Iff.rfl

theorem isCrossS_surgS_any {c : ℤ × ℤ} {k j : ℤ} {e : Sym2 Atom} :
    IsCrossS j (surgS c k e) ↔ IsCrossS j e := by
  induction e using Sym2.ind with
  | _ a b =>
    by_cases hff : IsFar k a ∧ IsFar k b
    · rw [surgS_far hff, isCrossS_mk, isCrossS_mk, isFar_htA_any, isFar_htA_any]
    · rw [surgS_other hff]

theorem crossN_surg (c : ℤ × ℤ) (k j : ℤ) (E : Finset (Sym2 Atom)) :
    crossN (E.image (surgS c k)) j = crossN E j := by
  unfold crossN
  rw [Finset.filter_image, Finset.card_image_of_injective _ (surgS_injective c k)]
  congr 1
  exact Finset.filter_congr (fun e _ => isCrossS_surgS_any)

/-- A crossing bond at bilayer `k` is a vertical bond of bilayer `k`. -/
theorem cross_eq_vert {σ : ℤ → ZMod 3} {k : ℤ} {e : Sym2 Atom} (hb : BondS σ e) (hc : IsCrossS k e) :
    ∃ p : ℤ × ℤ, e = vert k p ∧ (p.1 : ZMod 3) = σ k ∧ (p.2 : ZMod 3) = σ k := by
  induction e using Sym2.ind with
  | _ a b =>
    rw [bondS_mk] at hb
    rw [isCrossS_mk] at hc
    have key : ∀ x y : Atom, Bond σ x y → IsFar k x → ¬ IsFar k y →
        ∃ p : ℤ × ℤ, s(x, y) = vert k p ∧ (p.1 : ZMod 3) = σ k ∧ (p.2 : ZMod 3) = σ k := by
      intro x y hxy hx hy
      obtain ⟨h1, h2, h3, h4, h5⟩ := cut hxy hx hy
      have hsy := hxy.2.1
      unfold IsSite at hsy
      rw [h2] at hsy
      have hxe : x = (k, y.2.1, 1) := Prod.ext h1 (Prod.ext h3 h4)
      have hye : y = (k, y.2.1, 0) := Prod.ext h2 (Prod.ext rfl h5)
      refine ⟨y.2.1, ?_, hsy.1, hsy.2⟩
      rw [vert, Sym2.eq_swap]
      exact congrArg₂ (fun a b => s(a, b)) hye hxe
    rcases hc with ⟨ha, hb'⟩ | ⟨ha, hb'⟩
    · exact key a b hb ha hb'
    · obtain ⟨p, hp, h⟩ := key b a (bond_symm hb) hb' ha
      exact ⟨p, by rw [Sym2.eq_swap]; exact hp, h⟩

theorem vert_inj {k : ℤ} {p q : ℤ × ℤ} (h : vert k p = vert k q) : p = q := by
  unfold vert at h
  rcases Sym2.eq_iff.mp h with h | h
  · exact congrArg (fun a : Atom => a.2.1) h.1
  · have := congrArg (fun a : Atom => a.2.2) h.1
    simp at this

/-- The centre of the half-turn for a crossing set `S`: `p + q` when `S = {vert k p, vert k q}`,
otherwise `c₀`. It does not depend on the order of `p` and `q`. -/
noncomputable def centreOf (k : ℤ) (c₀ : ℤ × ℤ) (S : Finset (Sym2 Atom)) : ℤ × ℤ :=
  if h : ∃ p q : ℤ × ℤ, p ≠ q ∧ S = {vert k p, vert k q} then h.choose + h.choose_spec.choose else c₀

theorem sum_eq_of_pair_eq {k : ℤ} {p q p' q' : ℤ × ℤ} (hne : p' ≠ q')
    (hS : ({vert k p, vert k q} : Finset (Sym2 Atom)) = {vert k p', vert k q'}) : p' + q' = p + q := by
  have hp : vert k p' ∈ ({vert k p, vert k q} : Finset (Sym2 Atom)) := by rw [hS]; simp
  have hq : vert k q' ∈ ({vert k p, vert k q} : Finset (Sym2 Atom)) := by rw [hS]; simp
  simp only [Finset.mem_insert, Finset.mem_singleton] at hp hq
  rcases hp with hp | hp <;> rcases hq with hq | hq
  · exact absurd ((vert_inj hp).trans (vert_inj hq).symm) hne
  · rw [vert_inj hp, vert_inj hq]
  · rw [vert_inj hp, vert_inj hq, add_comm]
  · exact absurd ((vert_inj hp).trans (vert_inj hq).symm) hne

theorem centreOf_pair {k : ℤ} {c₀ : ℤ × ℤ} {p q : ℤ × ℤ} (hpq : p ≠ q) :
    centreOf k c₀ {vert k p, vert k q} = p + q := by
  unfold centreOf
  split
  next h =>
    obtain ⟨hne, hS⟩ := h.choose_spec.choose_spec
    exact sum_eq_of_pair_eq hne hS
  next h => exact absurd ⟨p, q, hpq, rfl⟩ h

/-- A good default centre for the letter of bilayer `k`. -/
noncomputable def cDefault (σ : ℤ → ZMod 3) (k : ℤ) : ℤ × ℤ := (((2 * σ k).val : ℤ), ((2 * σ k).val : ℤ))

theorem goodCentre_cDefault (σ : ℤ → ZMod 3) (k : ℤ) : GoodCentre σ k (cDefault σ k) := by
  unfold GoodCentre cDefault; simp

/-- The crossing set at `k` of a polygon in `PolysA1` is empty or two vertical bonds at points `p ≠ q`
of the position of bilayer `k`. -/
theorem cross_set_cases {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {E : Finset (Sym2 Atom)}
    (hE : E ∈ PolysA1 σ v l) (k : ℤ) :
    E.filter (IsCrossS k) = ∅ ∨ ∃ p q : ℤ × ℤ, p ≠ q ∧ E.filter (IsCrossS k) = {vert k p, vert k q} ∧
      ((p.1 : ZMod 3) = σ k ∧ (p.2 : ZMod 3) = σ k) ∧ ((q.1 : ZMod 3) = σ k ∧ (q.2 : ZMod 3) = σ k) := by
  obtain ⟨⟨hne, hbond, hcl, -⟩, -, -, hprof⟩ := hE
  have hnd : ∀ e ∈ E, ¬ e.IsDiag := by
    intro e he hd
    have hb := hbond e he
    induction e using Sym2.ind with
    | _ a b => rw [bondS_mk] at hb; exact bond_ne hb (Sym2.mk_isDiag_iff.mp hd)
  have hev := even_card_cross k E hcl hnd
  have hle := hprof k
  unfold crossN at hle
  rcases Nat.lt_or_ge (E.filter (IsCrossS k)).card 1 with h0 | h1
  · left; exact Finset.card_eq_zero.mp (by omega)
  · right
    have h2 : (E.filter (IsCrossS k)).card = 2 := by rcases hev with ⟨m, hm⟩; omega
    obtain ⟨e₁, e₂, hne12, heq⟩ := Finset.card_eq_two.mp h2
    have he₁ : e₁ ∈ E.filter (IsCrossS k) := by rw [heq]; simp
    have he₂ : e₂ ∈ E.filter (IsCrossS k) := by rw [heq]; simp
    obtain ⟨p, hp, hps⟩ := cross_eq_vert (hbond e₁ (Finset.mem_filter.mp he₁).1) (Finset.mem_filter.mp he₁).2
    obtain ⟨q, hq, hqs⟩ := cross_eq_vert (hbond e₂ (Finset.mem_filter.mp he₂).1) (Finset.mem_filter.mp he₂).2
    refine ⟨p, q, fun h => hne12 (by rw [hp, hq, h]), by rw [heq, hp, hq], hps, hqs⟩

/-- The surgery at `k` about the centre read from the polygon's own crossing set. -/
noncomputable def flipMap (σ : ℤ → ZMod 3) (k : ℤ) (E : Finset (Sym2 Atom)) : Finset (Sym2 Atom) :=
  E.image (surgS (centreOf k (cDefault σ k) (E.filter (IsCrossS k))) k)

theorem mapsTo_flipMap {σ : ℤ → ZMod 3} {k : ℤ} {v : Atom} (hv : ¬ IsFar k v) (l : ℕ) :
    Set.MapsTo (flipMap σ k) (PolysA1 σ v l) (PolysA1 (flipAt σ k) v l) := by
  intro E hE
  have hE' := hE
  obtain ⟨hpoly, hvE, hcard, hprof⟩ := hE'
  rcases cross_set_cases hE k with h0 | ⟨p, q, hpq, hS, hp, hq⟩
  · -- no crossing at k
    have hm := mapsTo_surgery (goodCentre_cDefault σ k) hv (S := ∅) (by simp) (by simp)
      (show E ∈ PolysThrough σ k v ∅ from ⟨hpoly, hvE, h0⟩)
    obtain ⟨hpoly', hv', -⟩ := hm
    have hc : centreOf k (cDefault σ k) (E.filter (IsCrossS k)) = cDefault σ k := by
      rw [h0]
      unfold centreOf
      split
      next h =>
        obtain ⟨p, q, -, h⟩ := h
        have : vert k p ∈ (∅ : Finset (Sym2 Atom)) := by rw [h]; simp
        simp at this
      next => rfl
    refine ⟨by rw [flipMap, hc]; exact hpoly', by rw [flipMap, hc]; exact hv', ?_, ?_⟩
    · rw [flipMap, Finset.card_image_of_injective _ (surgS_injective _ k), hcard]
    · intro j; rw [flipMap, crossN_surg]; exact hprof j
  · have hc : centreOf k (cDefault σ k) (E.filter (IsCrossS k)) = p + q := by rw [hS, centreOf_pair hpq]
    have hb := (bijOn_two_crossings hv hp hq).mapsTo (show E ∈ PolysThrough σ k v {vert k p, vert k q} from
      ⟨hpoly, hvE, hS⟩)
    obtain ⟨hpoly', hv', -⟩ := hb
    refine ⟨by rw [flipMap, hc]; exact hpoly', by rw [flipMap, hc]; exact hv', ?_, ?_⟩
    · rw [flipMap, Finset.card_image_of_injective _ (surgS_injective _ k), hcard]
    · intro j; rw [flipMap, crossN_surg]; exact hprof j

theorem cDefault_flipAt (σ : ℤ → ZMod 3) (k : ℤ) : cDefault (flipAt σ k) k = cDefault σ k := by
  unfold cDefault; rw [flipAt_of_le le_rfl]

theorem flipMap_flipMap {σ : ℤ → ZMod 3} {k : ℤ} (E : Finset (Sym2 Atom)) :
    flipMap (flipAt σ k) k (flipMap σ k E) = E := by
  unfold flipMap
  have hS : (E.image (surgS (centreOf k (cDefault σ k) (E.filter (IsCrossS k))) k)).filter (IsCrossS k) =
      E.filter (IsCrossS k) := cross_image_surgS E
  rw [hS, cDefault_flipAt, Finset.image_image]
  have : surgS (centreOf k (cDefault σ k) (E.filter (IsCrossS k))) k ∘
      surgS (centreOf k (cDefault σ k) (E.filter (IsCrossS k))) k = id := funext (surgS_surgS _ k)
  rw [this, Finset.image_id]

/-- **Corollary A1 across one flip.** For an atom `v` in the root half of bilayer `k` and every length
`l`, the polygons through `v` with `l` edges crossing every bilayer at most twice are equally many in
`G σ` and in `G (flipAt σ k)`. -/
theorem ncard_polysA1_flip {σ : ℤ → ZMod 3} {k : ℤ} {v : Atom} (hv : ¬ IsFar k v) (l : ℕ) :
    (PolysA1 σ v l).ncard = (PolysA1 (flipAt σ k) v l).ncard := by
  have hmaps := mapsTo_flipMap (σ := σ) hv l
  have hback := mapsTo_flipMap (σ := flipAt σ k) hv l
  rw [flipAt_flipAt] at hback
  have hbij : Set.BijOn (flipMap σ k) (PolysA1 σ v l) (PolysA1 (flipAt σ k) v l) := by
    refine ⟨hmaps, ?_, ?_⟩
    · intro E₁ _ E₂ _ h
      have := congrArg (flipMap (flipAt σ k) k) h
      rwa [flipMap_flipMap, flipMap_flipMap] at this
    · intro E' hE'
      refine ⟨flipMap (flipAt σ k) k E', hback hE', ?_⟩
      have := flipMap_flipMap (σ := flipAt σ k) (k := k) E'
      rwa [flipAt_flipAt] at this
  rw [← hbij.image_eq, hbij.injOn.ncard_image]

end LoopEqualityProof
