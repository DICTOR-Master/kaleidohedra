module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.CorollaryA1
public import LoopEquality.Relabel
public import LoopEquality.Assembly

@[expose] public section

/-!
# Every site counts the same (Lean paper, Milestone 2g)

The Fable review of 28 November 2026 found that `corollaryA1` compares one fixed atom across stackings; here
the count at any site of any stacking is compared with the count at diamond's site `(0, (0, 0), 0)`.

* `ncard_polysA1_iso`: a bijection of atoms that carries bonds to bonds in both directions and keeps the
  condition "every bilayer crossed at most twice" keeps the counts.
* `shiftA` (bilayer shift), `posA` (planar translation by `d ≡ (s, s)`, which adds `s` to every letter):
  both keep the counts.
* `corollaryA_everySite`: for every stacking `σ` and every site `v`,
  `#(PolysA1 σ v l) = #(PolysA1 diamond (0, (0, 0), 0) l)`.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-! ## A general relabelling of atoms -/

theorem map_left_inv {f g : Atom → Atom} (h : ∀ a, g (f a) = a) (e : Sym2 Atom) :
    Sym2.map g (Sym2.map f e) = e := by
  induction e using Sym2.ind with
  | _ a b => show s(g (f a), g (f b)) = s(a, b); rw [h, h]

theorem degS_map {φ : Atom → Atom} (hφ : Function.Injective φ) (E : Finset (Sym2 Atom)) (x : Atom) :
    degS (E.image (Sym2.map φ)) (φ x) = degS E x := by
  unfold degS
  rw [Finset.filter_image, Finset.card_image_of_injective _ (Sym2.map.injective hφ)]
  congr 1
  apply Finset.filter_congr
  intro e _
  induction e using Sym2.ind with
  | _ a b =>
    show φ x ∈ s(φ a, φ b) ↔ x ∈ s(a, b)
    rw [Sym2.mem_iff, Sym2.mem_iff, hφ.eq_iff, hφ.eq_iff]

theorem ncard_polysA1_iso {σ σ' : ℤ → ZMod 3} (φ ψ : Atom → Atom) (hψφ : ∀ a, ψ (φ a) = a)
    (hφψ : ∀ a, φ (ψ a) = a) (hb : ∀ a b, Bond σ a b → Bond σ' (φ a) (φ b))
    (hb' : ∀ a b, Bond σ' a b → Bond σ (ψ a) (ψ b))
    (hcr : ∀ E : Finset (Sym2 Atom), (∀ j, crossN E j ≤ 2) → ∀ j, crossN (E.image (Sym2.map φ)) j ≤ 2)
    (hcr' : ∀ E : Finset (Sym2 Atom), (∀ j, crossN E j ≤ 2) → ∀ j, crossN (E.image (Sym2.map ψ)) j ≤ 2)
    (v : Atom) (l : ℕ) : (PolysA1 σ v l).ncard = (PolysA1 σ' (φ v) l).ncard := by
  have hφi : Function.Injective φ := fun a b h => by rw [← hψφ a, h, hψφ]
  have hψi : Function.Injective ψ := fun a b h => by rw [← hφψ a, h, hφψ]
  have mapmap : ∀ E : Finset (Sym2 Atom), (E.image (Sym2.map φ)).image (Sym2.map ψ) = E := by
    intro E; rw [Finset.image_image]
    have : Sym2.map ψ ∘ Sym2.map φ = id := by
      funext e; exact map_left_inv hψφ e
    rw [this, Finset.image_id]
  have mapmap' : ∀ E : Finset (Sym2 Atom), (E.image (Sym2.map ψ)).image (Sym2.map φ) = E := by
    intro E; rw [Finset.image_image]
    have : Sym2.map φ ∘ Sym2.map ψ = id := by
      funext e; exact map_left_inv hφψ e
    rw [this, Finset.image_id]
  have closed_map : ∀ (χ ω : Atom → Atom), Function.Injective χ → (∀ a, χ (ω a) = a) →
      ∀ E : Finset (Sym2 Atom), Closed E → Closed (E.image (Sym2.map χ)) := by
    intro χ ω hχ hχω E hE x
    rw [← hχω x, degS_map hχ]; exact hE _
  have maps : ∀ (τ τ' : ℤ → ZMod 3) (χ ω : Atom → Atom), Function.Injective χ → (∀ a, χ (ω a) = a) →
      (∀ a, ω (χ a) = a) → (∀ a b, Bond τ a b → Bond τ' (χ a) (χ b)) →
      (∀ E : Finset (Sym2 Atom), (∀ j, crossN E j ≤ 2) → ∀ j, crossN (E.image (Sym2.map χ)) j ≤ 2) →
      (∀ E : Finset (Sym2 Atom), (E.image (Sym2.map χ)).image (Sym2.map ω) = E) →
      (∀ E : Finset (Sym2 Atom), Closed E → Closed (E.image (Sym2.map ω))) →
      ∀ w, Set.MapsTo (fun E : Finset (Sym2 Atom) => E.image (Sym2.map χ)) (PolysA1 τ w l) (PolysA1 τ' (χ w) l) := by
    intro τ τ' χ ω hχ hχω hωχ hbχ hcrχ hmm hclω w E ⟨⟨hne, hbond, hcl, hmin⟩, hv, hcard, hprof⟩
    refine ⟨⟨hne.image _, ?_, closed_map χ ω hχ hχω E hcl, ?_⟩, by rw [degS_map hχ]; exact hv,
      by rw [Finset.card_image_of_injective _ (Sym2.map.injective hχ), hcard], hcrχ E hprof⟩
    · intro f hf
      obtain ⟨e, he, rfl⟩ := Finset.mem_image.mp hf
      have hbe := hbond e he
      induction e using Sym2.ind with
      | _ x y =>
        rw [bondS_mk] at hbe
        show BondS _ s(χ x, χ y)
        rw [bondS_mk]; exact hbχ x y hbe
    · intro F hF hFne hFcl
      have hsub : F.image (Sym2.map ω) ⊆ E := by
        intro f hf
        obtain ⟨f', hf', rfl⟩ := Finset.mem_image.mp hf
        obtain ⟨e, he, rfl⟩ := Finset.mem_image.mp (hF hf')
        have : Sym2.map ω (Sym2.map χ e) = e := map_left_inv hωχ e
        rw [this]; exact he
      have := hmin _ hsub (hFne.image _) (hclω F hFcl)
      rw [← this]
      show F = (F.image (Sym2.map ω)).image (Sym2.map χ)
      rw [Finset.image_image]
      have : Sym2.map χ ∘ Sym2.map ω = id := by
        funext e; exact map_left_inv hχω e
      rw [this, Finset.image_id]
  have hf := maps σ σ' φ ψ hφi hφψ hψφ hb hcr mapmap (closed_map ψ φ hψi hψφ) v
  have hg := maps σ' σ ψ φ hψi hψφ hφψ hb' hcr' mapmap' (closed_map φ ψ hφi hφψ) (φ v)
  rw [hψφ] at hg
  have hbij : Set.BijOn (fun E : Finset (Sym2 Atom) => E.image (Sym2.map φ)) (PolysA1 σ v l)
      (PolysA1 σ' (φ v) l) :=
    ⟨hf, fun E₁ _ E₂ _ h => Finset.image_injective (Sym2.map.injective hφi) h,
      fun E' hE' => ⟨E'.image (Sym2.map ψ), hg hE', mapmap' E'⟩⟩
  rw [← hbij.image_eq, hbij.injOn.ncard_image]

end LoopEqualityProof
