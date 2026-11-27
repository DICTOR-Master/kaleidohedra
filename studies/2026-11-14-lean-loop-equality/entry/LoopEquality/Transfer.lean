module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.Linkage
public import LoopEquality.Parts
public import LoopEquality.EverySite

@[expose] public section

/-!
# Flip transfer (Lean paper, Milestone 3c)

Study 2026-11-15-polygon-bijection §3, Lemma 1. The half-turn `htA c` of the far half carries far linkages
of `G σ` onto far linkages of `G (flipAt σ k)`, with ends, sizes and pairings carried along.

* `linkage_image`, `conn_image`: an involution of the atoms carries a linkage to a linkage (ends mapped) and
  keeps which ends are joined.
* `flip_transfer`: for a good centre `c`, a far linkage of `G σ` maps under `htS c` to a far linkage of
  `G (flipAt σ k)` with the same number of edges and the same pairing of its ends.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

section Involution

variable {g : Atom → Atom} (hg : ∀ a, g (g a) = a)
include hg

theorem invol_injective : Function.Injective g := fun a b h => by rw [← hg a, h, hg b]

theorem image_image_invol (L : Finset (Sym2 Atom)) :
    (L.image (Sym2.map g)).image (Sym2.map g) = L := by
  rw [Finset.image_image]
  conv_rhs => rw [← Finset.image_id (s := L)]
  apply Finset.image_congr
  intro e _
  exact map_left_inv hg e

theorem degS_image_invol (L : Finset (Sym2 Atom)) (w : Atom) :
    degS (L.image (Sym2.map g)) w = degS L (g w) := by
  conv_lhs => rw [← hg w]
  exact degS_map (invol_injective hg) L (g w)

theorem closed_image_invol {L : Finset (Sym2 Atom)} (h : Closed L) : Closed (L.image (Sym2.map g)) :=
  fun w => by rw [degS_image_invol hg]; exact h (g w)

theorem mem_image_invol {B : Finset Atom} {w : Atom} : w ∈ B.image g ↔ g w ∈ B := by
  constructor
  · intro h; obtain ⟨b, hb, rfl⟩ := Finset.mem_image.mp h; rwa [hg]
  · intro h; exact Finset.mem_image.mpr ⟨g w, h, hg w⟩

theorem linkage_image {L : Finset (Sym2 Atom)} {B : Finset Atom} (hL : IsLinkageOn L B) :
    IsLinkageOn (L.image (Sym2.map g)) (B.image g) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro w hw; rw [degS_image_invol hg]; exact hL.1 _ ((mem_image_invol hg).mp hw)
  · intro w hw; rw [degS_image_invol hg]; exact hL.2.1 _ (fun h => hw ((mem_image_invol hg).mpr h))
  · intro G hG hGne hGcl
    apply hL.2.2.1 (G.image (Sym2.map g))
    · intro e he
      obtain ⟨f, hf, rfl⟩ := Finset.mem_image.mp he
      obtain ⟨e', he', rfl⟩ := Finset.mem_image.mp (hG hf)
      rw [map_left_inv hg]; exact he'
    · exact hGne.image _
    · exact closed_image_invol hg hGcl
  · intro e he hd
    obtain ⟨f, hf, rfl⟩ := Finset.mem_image.mp he
    exact hL.2.2.2 f hf ((Sym2.isDiag_map (invol_injective hg)).mp hd)

theorem conn_image_of {L : Finset (Sym2 Atom)} {a b : Atom} (h : Conn L a b) :
    Conn (L.image (Sym2.map g)) (g a) (g b) := by
  induction h with
  | refl => exact Relation.ReflTransGen.refl
  | tail _ hbc ih =>
    refine ih.tail ⟨Finset.mem_image.mpr ⟨_, hbc.1, rfl⟩, fun e => hbc.2 (invol_injective hg e)⟩

theorem conn_image (L : Finset (Sym2 Atom)) (a b : Atom) :
    Conn L a b ↔ Conn (L.image (Sym2.map g)) (g a) (g b) := by
  refine ⟨conn_image_of hg, fun h => ?_⟩
  have := conn_image_of hg h
  rwa [image_image_invol hg, hg, hg] at this

end Involution

theorem htA_invol (c : ℤ × ℤ) : ∀ a, htA c (htA c a) = a := htA_htA c

theorem htA_upA (c : ℤ × ℤ) (k : ℤ) (p : ℤ × ℤ) : htA c (upA k p) = upA k (c - p) := rfl

/-- **Flip transfer.** For a good centre `c` of `σ` at `k`, the half-turn carries a far linkage of `G σ` with
ends at the `upA k p` (`p ∈ P`) to a far linkage of `G (flipAt σ k)` with ends at the `upA k (c - p)`, with
the same number of edges and the same pairing of its ends. -/
theorem flip_transfer {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {F : Finset (Sym2 Atom)}
    {P : Finset (ℤ × ℤ)} (hF : IsLinkageOn F (P.image (upA k))) (hFs : ∀ e ∈ F, ∀ w ∈ e, IsFar k w)
    (hFb : ∀ e ∈ F, BondS σ e) :
    IsLinkageOn (F.image (htS c)) ((P.image (fun p => c - p)).image (upA k)) ∧
      (∀ e ∈ F.image (htS c), ∀ w ∈ e, IsFar k w) ∧
      (∀ e ∈ F.image (htS c), BondS (flipAt σ k) e) ∧
      (F.image (htS c)).card = F.card ∧
      (∀ p q, Conn F (upA k p) (upA k q) ↔ Conn (F.image (htS c)) (upA k (c - p)) (upA k (c - q))) := by
  have hends : (P.image (fun p => c - p)).image (upA k) = (P.image (upA k)).image (htA c) := by
    rw [Finset.image_image, Finset.image_image]; rfl
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · rw [hends]; exact linkage_image (htA_invol c) hF
  · intro e he w hw
    obtain ⟨f, hf, rfl⟩ := Finset.mem_image.mp he
    obtain ⟨a, ha, rfl⟩ := Sym2.mem_map.mp hw
    exact (isFar_htA).mpr (hFs f hf a ha)
  · intro e he
    obtain ⟨f, hf, rfl⟩ := Finset.mem_image.mp he
    have hb := hFb f hf
    have hfs := hFs f hf
    induction f using Sym2.ind with
    | _ a b =>
      rw [bondS_mk] at hb
      have ha : IsFar k a := hfs a (Sym2.mem_mk_left a b)
      have hb' : IsFar k b := hfs b (Sym2.mem_mk_right a b)
      have := (flip_is_twist hc).2.2 a b ⟨fun _ => hb', fun _ => ha⟩
      rw [twist_eq_htA ha, twist_eq_htA hb'] at this
      show BondS (flipAt σ k) s(htA c a, htA c b)
      rw [bondS_mk]; exact this.mp hb
  · exact Finset.card_image_of_injective _ (Sym2.map.injective (invol_injective (htA_invol c)))
  · intro p q
    rw [← htA_upA, ← htA_upA]
    exact conn_image (htA_invol c) F _ _

end LoopEqualityProof
