module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.CorollaryA1
public import LoopEquality.Finiteness
public import LoopEquality.Parts
public import LoopEquality.Counting
public import LoopEquality.TheoremB
public import LoopEquality.EverySite
public import LoopEquality.Lemma7

@[expose] public section

/-!
# Theorem 5 (a) of #102 for short polygons (Lean paper, milestone M1)

* `three_crossN_le`: a polygon crossing a bilayer `n` times has at least `3 n` edges (`n` vertical bonds and, on each
  side, a linkage with `n` ends, which has at least `n` edges).
* `polys_eq_polysA1`: so a polygon with at most 11 edges crosses every bilayer at most twice.
* `theorem5a_short`: for `l ≤ 11`, every site of every stacking has as many polygons with `l` edges as diamond's site.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

theorem crossing_eq_verts {σ : ℤ → ZMod 3} {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E) (k : ℤ)
    {P : Finset (ℤ × ℤ)} (hPdef : ∀ p, p ∈ P ↔ vert k p ∈ E) : E.filter (IsCrossS k) = P.image (vert k) := by
  ext e
  simp only [Finset.mem_filter, Finset.mem_image]
  constructor
  · rintro ⟨he, hc⟩
    obtain ⟨p, rfl, -⟩ := cross_eq_vert (hE.2.1 e he) hc
    exact ⟨p, (hPdef p).mpr he, rfl⟩
  · rintro ⟨p, hp, rfl⟩
    refine ⟨(hPdef p).mp hp, ?_⟩
    rw [vert_eq, isCrossS_mk]; exact Or.inr ⟨not_isFar_loA k p, isFar_upA k p⟩

theorem three_crossN_le {σ : ℤ → ZMod 3} {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E) {v : Atom}
    (hv : 0 < degS E v) (k : ℤ) : 3 * crossN E k ≤ E.card := by
  set P := ((box v (2 * E.card)).image (fun a => a.2.1)).filter (fun p => vert k p ∈ E) with hP
  have hPdef : ∀ p, p ∈ P ↔ vert k p ∈ E := by
    intro p; rw [hP, Finset.mem_filter]
    refine ⟨fun h => h.2, fun h => ⟨?_, h⟩⟩
    have hb := polygon_in_box hE hv h
    rw [vert, Finset.mk_mem_sym2_iff] at hb
    exact Finset.mem_image.mpr ⟨_, hb.1, rfl⟩
  have hcard : crossN E k = P.card := by
    unfold crossN; rw [crossing_eq_verts hE k hPdef, Finset.card_image_of_injective _ (fun a b h => vert_inj h)]
  rcases P.eq_empty_or_nonempty with he | hne
  · rw [hcard, he]; simp
  obtain ⟨hsplit, hRl, hFl, -⟩ := polygon_to_parts hE hPdef hne rfl rfl
  set R := E.filter (fun e => ∀ w ∈ e, ¬ IsFar k w)
  set F := E.filter (fun e => ∀ w ∈ e, IsFar k w)
  have hRs : ∀ e ∈ R, ∀ w ∈ e, ¬ IsFar k w := fun e he => (Finset.mem_filter.mp he).2
  have hFs : ∀ e ∈ F, ∀ w ∈ e, IsFar k w := fun e he => (Finset.mem_filter.mp he).2
  have h1 := rootL_card ⟨hRl, hRs, fun e he => hE.2.1 e (Finset.filter_subset _ _ he)⟩
  have h2 := farL_card ⟨hFl, hFs, fun e he => hE.2.1 e (Finset.filter_subset _ _ he)⟩
  have h3 := card_three (P := P) hRs hFs
  rw [← hsplit] at h3
  omega

/-- A polygon with at most 11 edges crosses every bilayer at most twice. -/
theorem polys_eq_polysA1 (σ : ℤ → ZMod 3) (v : Atom) {l : ℕ} (hl : l < 12) : Polys σ v l = PolysA1 σ v l := by
  ext E
  constructor
  · rintro ⟨hE, hv, hcard⟩
    refine ⟨hE, hv, hcard, fun j => ?_⟩
    have h3 := three_crossN_le hE hv j
    have hnd : ∀ e ∈ E, ¬ e.IsDiag := fun e he hd => by
      have hb := hE.2.1 e he
      induction e using Sym2.ind with
      | _ a b => rw [bondS_mk] at hb; exact bond_ne hb (Sym2.mk_isDiag_iff.mp hd)
    obtain ⟨m, hm⟩ := even_card_cross j E hE.2.2.1 hnd
    unfold crossN at h3 ⊢
    omega
  · rintro ⟨hE, hv, hcard, -⟩; exact ⟨hE, hv, hcard⟩

/-- **Theorem 5 (a) of #102 for l ≤ 11.** For every stacking and every site `v` of it, the polygons through `v` with
`l ≤ 11` edges are as many as at diamond's site `(0, (0, 0), 0)`. -/
theorem theorem5a_short {σ : ℤ → ZMod 3} (hσ : IsStacking σ) {v : Atom} (hv : IsSite σ v) {l : ℕ} (hl : l < 12) :
    (Polys σ v l).ncard = (Polys diamond (0, (0, 0), 0) l).ncard := by
  rw [polys_eq_polysA1 σ v hl, polys_eq_polysA1 diamond _ hl]
  exact corollaryA_everySite hσ hv l

end LoopEqualityProof
