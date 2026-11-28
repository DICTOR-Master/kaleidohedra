module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.Linkage
public import LoopEquality.Parts
public import LoopEquality.Counting
public import LoopEquality.Pairings
public import LoopEquality.BSym
public import LoopEquality.EverySite

@[expose] public section

/-!
# Far counts do not change under translations that keep positions

* `conn_map_iff`: a bijection of the atoms carries paths to paths.
* `Fc_translate`: translating the crossing points and the pairing by `d ≡ 0` (mod 3) keeps the far count.
* `Fc_any_centre`: so the half-turn image count does not depend on the good centre chosen.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

theorem conn_map_of {f : Atom → Atom} (hf : Function.Injective f) {L : Finset (Sym2 Atom)} {a b : Atom}
    (h : Conn L a b) : Conn (L.image (Sym2.map f)) (f a) (f b) := by
  induction h with
  | refl => exact Relation.ReflTransGen.refl
  | tail _ hbc ih => exact ih.tail ⟨Finset.mem_image.mpr ⟨_, hbc.1, rfl⟩, fun e => hbc.2 (hf e)⟩

theorem conn_map_iff {f g : Atom → Atom} (hgf : ∀ a, g (f a) = a) (hfg : ∀ a, f (g a) = a)
    (L : Finset (Sym2 Atom)) (a b : Atom) : Conn L a b ↔ Conn (L.image (Sym2.map f)) (f a) (f b) := by
  have hf : Function.Injective f := fun x y h => by rw [← hgf x, h, hgf]
  have hg : Function.Injective g := fun x y h => by rw [← hfg x, h, hfg]
  refine ⟨conn_map_of hf, fun h => ?_⟩
  have := conn_map_of hg h
  rwa [Finset.image_image, show Sym2.map g ∘ Sym2.map f = id from funext (map_left_inv hgf), Finset.image_id,
    hgf, hgf] at this

def trP (d : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : Finset (ℤ × ℤ) := P.image (fun p => p + d)
def trM (d : ℤ × ℤ) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : Finset ((ℤ × ℤ) × (ℤ × ℤ)) :=
  N.image (fun x => (x.1 + d, x.2 + d))

theorem posA_upA (d : ℤ × ℤ) (k : ℤ) (p : ℤ × ℤ) : posA d (upA k p) = upA k (p + d) := rfl

theorem farSet_translate {σ : ℤ → ZMod 3} {k : ℤ} {d : ℤ × ℤ} (hd : (d.1 : ZMod 3) = 0 ∧ (d.2 : ZMod 3) = 0)
    {P : Finset (ℤ × ℤ)} {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {s : ℕ} {F : Finset (Sym2 Atom)}
    (hF : F ∈ FarSet σ k P N s) : F.image (Sym2.map (posA d)) ∈ FarSet σ k (trP d P) (trM d N) s := by
  have hσ : (fun j => σ j + 0) = σ := by funext j; simp
  have hinv : ∀ a, posA (-d) (posA d a) = a := posA_posA d
  have hinv' : ∀ a, posA d (posA (-d) a) = a := fun a => by have := posA_posA (-d) a; rwa [neg_neg] at this
  have hinj : Function.Injective (posA d) := fun a b h => by rw [← hinv a, h, hinv]
  obtain ⟨⟨hFl, hFs, hFb⟩, hs, hN⟩ := hF
  refine ⟨⟨?_, ?_, ?_⟩, ?_, ?_⟩
  · -- linkage, ends translated
    have hends : (trP d P).image (upA k) = (P.image (upA k)).image (posA d) := by
      unfold trP; rw [Finset.image_image, Finset.image_image]; rfl
    rw [hends]
    refine ⟨fun w hw => ?_, fun w hw => ?_, fun G hG hGne hGcl => ?_, fun e he hdg => ?_⟩
    · have : w = posA d (posA (-d) w) := (hinv' w).symm
      rw [this, degS_map hinj]; apply hFl.1
      obtain ⟨b, hb, rfl⟩ := Finset.mem_image.mp hw; rwa [hinv]
    · rw [← hinv' w, degS_map hinj]; apply hFl.2.1
      intro h; exact hw (by rw [← hinv' w]; exact Finset.mem_image_of_mem _ h)
    · apply hFl.2.2.1 (G.image (Sym2.map (posA (-d))))
      · intro e he; obtain ⟨f, hf, rfl⟩ := Finset.mem_image.mp he
        obtain ⟨e', he', rfl⟩ := Finset.mem_image.mp (hG hf); rw [map_left_inv hinv]; exact he'
      · exact hGne.image _
      · intro w
        have hinj' : Function.Injective (posA (-d)) := fun a b h => by rw [← hinv' a, h, hinv']
        rw [← hinv w, degS_map hinj']; exact hGcl _
    · obtain ⟨f, hf, rfl⟩ := Finset.mem_image.mp he
      exact hFl.2.2.2 f hf ((Sym2.isDiag_map hinj).mp hdg)
  · intro e he w hw
    obtain ⟨f, hf, rfl⟩ := Finset.mem_image.mp he
    obtain ⟨a, ha, rfl⟩ := Sym2.mem_map.mp hw
    exact hFs f hf a ha
  · intro e he
    obtain ⟨f, hf, rfl⟩ := Finset.mem_image.mp he
    have hb := hFb f hf
    induction f using Sym2.ind with
    | _ a b =>
      rw [bondS_mk] at hb
      show BondS σ s(posA d a, posA d b)
      rw [bondS_mk]; have := bond_posA hd hb; rwa [hσ] at this
  · rw [Finset.card_image_of_injective _ (Sym2.map.injective hinj), hs]
  · -- the pairing, translated
    rw [← hN]
    ext ⟨p, q⟩
    simp only [pairF, trM, trP, Finset.mem_filter, Finset.mem_product, Finset.mem_image, Prod.mk.injEq]
    constructor
    · rintro ⟨⟨⟨p', hp', rfl⟩, ⟨q', hq', rfl⟩⟩, hc⟩
      refine ⟨(p', q'), ⟨⟨hp', hq'⟩, ?_⟩, rfl, rfl⟩
      rw [conn_map_iff hinv hinv' F, posA_upA, posA_upA]; exact hc
    · rintro ⟨⟨p', q'⟩, ⟨⟨hp', hq'⟩, hc⟩, rfl, rfl⟩
      exact ⟨⟨⟨p', hp', rfl⟩, ⟨q', hq', rfl⟩⟩, by rw [← posA_upA, ← posA_upA, ← conn_map_iff hinv hinv' F]; exact hc⟩

theorem trP_neg (d : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : trP (-d) (trP d P) = P := by
  unfold trP; rw [Finset.image_image]; conv_rhs => rw [← Finset.image_id (s := P)]
  exact Finset.image_congr (fun p _ => by simp)

theorem trM_neg (d : ℤ × ℤ) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : trM (-d) (trM d N) = N := by
  unfold trM; rw [Finset.image_image]; conv_rhs => rw [← Finset.image_id (s := N)]
  exact Finset.image_congr (fun x _ => by simp)

/-- **Translation.** Far counts do not change when the crossing points and the pairing are translated by `d ≡ 0`. -/
theorem Fc_translate {σ : ℤ → ZMod 3} {k : ℤ} {d : ℤ × ℤ} (hd : (d.1 : ZMod 3) = 0 ∧ (d.2 : ZMod 3) = 0)
    (P : Finset (ℤ × ℤ)) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (s : ℕ) :
    Fc σ k (trP d P) (trM d N) s = Fc σ k P N s := by
  have hd' : ((-d).1 : ZMod 3) = 0 ∧ ((-d).2 : ZMod 3) = 0 := by simp [hd.1, hd.2]
  have hinv : ∀ a, posA (-d) (posA d a) = a := posA_posA d
  have hinv' : ∀ a, posA d (posA (-d) a) = a := fun a => by have := posA_posA (-d) a; rwa [neg_neg] at this
  have hinj : Function.Injective (posA d) := fun a b h => by rw [← hinv a, h, hinv]
  unfold Fc; congr 1; symm
  apply Set.ncard_congr (fun F _ => F.image (Sym2.map (posA d)))
  · intro F hF; exact farSet_translate hd hF
  · intro F₁ F₂ _ _ h; exact Finset.image_injective (Sym2.map.injective hinj) h
  · intro G hG
    have h2 := farSet_translate hd' hG
    rw [trP_neg, trM_neg] at h2
    refine ⟨_, h2, ?_⟩
    show (G.image (Sym2.map (posA (-d)))).image (Sym2.map (posA d)) = G
    rw [Finset.image_image, show Sym2.map (posA d) ∘ Sym2.map (posA (-d)) = id from funext (map_left_inv hinv'),
      Finset.image_id]

theorem gP_eq_trP (c c' : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : gP c' P = trP (c' - c) (gP c P) := by
  unfold gP trP; rw [Finset.image_image]; exact Finset.image_congr (fun p _ => by simp only [Function.comp_apply]; abel)

theorem gM_eq_trM (c c' : ℤ × ℤ) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : gM c' N = trM (c' - c) (gM c N) := by
  unfold gM trM; rw [Finset.image_image]; exact Finset.image_congr (fun x _ => by simp only [gg, Function.comp_apply, Prod.mk.injEq]; constructor <;> abel)

theorem gP_gP' (c c' : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : gP c (gP c' P) = trP (c - c') P := by
  unfold gP trP; rw [Finset.image_image]; exact Finset.image_congr (fun p _ => by simp only [Function.comp_apply]; abel)

theorem gM_gM' (c c' : ℤ × ℤ) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : gM c (gM c' N) = trM (c - c') N := by
  unfold gM trM; rw [Finset.image_image]; exact Finset.image_congr (fun x _ => by simp only [gg, Function.comp_apply, Prod.mk.injEq]; constructor <;> abel)

theorem diff_good {σ : ℤ → ZMod 3} {k : ℤ} {c c' : ℤ × ℤ} (hc : GoodCentre σ k c) (hc' : GoodCentre σ k c') :
    ((c' - c).1 : ZMod 3) = 0 ∧ ((c' - c).2 : ZMod 3) = 0 := by
  unfold GoodCentre at hc hc'
  simp only [Prod.fst_sub, Prod.snd_sub, Int.cast_sub, hc.1, hc.2, hc'.1, hc'.2, sub_self, and_self]

/-- **Any good half-turn reverses the far asymmetry.** -/
theorem Af_any_centre {σ : ℤ → ZMod 3} {k : ℤ} {c c' : ℤ × ℤ} (hc : GoodCentre σ k c) (hc' : GoodCentre σ k c')
    (P : Finset (ℤ × ℤ)) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (s : ℕ) :
    Af σ k c (gP c' P) (gM c' N) s = - Af σ k c P N s := by
  unfold Af
  rw [gP_eq_trP c c' P, gM_eq_trM c c' N, Fc_translate (diff_good hc hc'), ← gP_eq_trP, ← gM_eq_trM, gP_gP' c c' P,
    gM_gM' c c' N, Fc_translate (diff_good hc' hc)]
  ring

end LoopEqualityProof
