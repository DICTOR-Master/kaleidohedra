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
* `ncard_polysA1_shift`, `ncard_polysA1_pos`, `diamond_isStacking`; `corollaryA_everySite`: for every stacking `σ` and every site `v`,
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

/-! ## Bilayer shift, planar translation, mirror -/

/-- Shift every atom up by `m` bilayers. -/
def shiftA (m : ℤ) (a : Atom) : Atom := (a.1 + m, a.2.1, a.2.2)

theorem shiftA_shiftA (m : ℤ) (a : Atom) : shiftA (-m) (shiftA m a) = a := by
  obtain ⟨j, p, u⟩ := a; simp [shiftA]

theorem bond_shiftA {σ : ℤ → ZMod 3} (m : ℤ) {a b : Atom} (h : Bond σ a b) :
    Bond (fun j => σ (j - m)) (shiftA m a) (shiftA m b) := by
  obtain ⟨ha, hb, hab⟩ := h
  obtain ⟨j, p, u⟩ := a
  obtain ⟨j', q, u'⟩ := b
  unfold IsSite at ha hb
  refine ⟨?_, ?_, ?_⟩
  · unfold IsSite shiftA; simpa using ha
  · unfold IsSite shiftA; simpa using hb
  · simp only [shiftA] at hab ⊢
    rcases hab with ⟨h1, h2, h3⟩ | ⟨h1, h2, h3, h4⟩ | ⟨h1, h2, h3, h4⟩
    · exact Or.inl ⟨by rw [h1], h2, h3⟩
    · exact Or.inr (Or.inl ⟨by rw [h1]; ring, h2, h3, h4⟩)
    · exact Or.inr (Or.inr ⟨by rw [h1]; ring, h2, h3, h4⟩)

theorem isCrossS_shift {m j : ℤ} {e : Sym2 Atom} :
    IsCrossS (j + m) (Sym2.map (shiftA m) e) ↔ IsCrossS j e := by
  induction e using Sym2.ind with
  | _ a b =>
    show IsCrossS (j + m) s(shiftA m a, shiftA m b) ↔ _
    rw [isCrossS_mk, isCrossS_mk]
    unfold IsFar shiftA; simp only [add_lt_add_iff_right, add_left_inj]

theorem crossN_shift (m : ℤ) (E : Finset (Sym2 Atom)) (j : ℤ) :
    crossN (E.image (Sym2.map (shiftA m))) (j + m) = crossN E j := by
  unfold crossN
  have hinj : Function.Injective (shiftA m) := fun a b h => by
    rw [← shiftA_shiftA m a, h, shiftA_shiftA]
  rw [Finset.filter_image, Finset.card_image_of_injective _ (Sym2.map.injective hinj)]
  congr 1
  exact Finset.filter_congr (fun e _ => isCrossS_shift)

theorem ncard_polysA1_shift (σ : ℤ → ZMod 3) (m : ℤ) (v : Atom) (l : ℕ) :
    (PolysA1 σ v l).ncard = (PolysA1 (fun j => σ (j - m)) (shiftA m v) l).ncard := by
  apply ncard_polysA1_iso (shiftA m) (shiftA (-m)) (shiftA_shiftA m)
    (fun a => by have := shiftA_shiftA (-m) a; rwa [neg_neg] at this)
    (fun a b h => bond_shiftA m h)
  · intro a b h
    have := bond_shiftA (-m) h
    simpa using this
  · intro E hE j
    have := crossN_shift m E (j - m)
    rw [sub_add_cancel] at this
    rw [this]; exact hE _
  · intro E hE j
    have := crossN_shift (-m) E (j + m)
    rw [add_neg_cancel_right] at this
    rw [this]; exact hE _

/-- Translate every atom by `d` in the plane. -/
def posA (d : ℤ × ℤ) (a : Atom) : Atom := (a.1, a.2.1 + d, a.2.2)

theorem posA_posA (d : ℤ × ℤ) (a : Atom) : posA (-d) (posA d a) = a := by
  obtain ⟨j, p, u⟩ := a; simp [posA]

theorem bond_posA {σ : ℤ → ZMod 3} {d : ℤ × ℤ} {s : ZMod 3} (hd : (d.1 : ZMod 3) = s ∧ (d.2 : ZMod 3) = s)
    {a b : Atom} (h : Bond σ a b) : Bond (fun j => σ j + s) (posA d a) (posA d b) := by
  obtain ⟨ha, hb, hab⟩ := h
  obtain ⟨j, ⟨p1, p2⟩, u⟩ := a
  obtain ⟨j', ⟨q1, q2⟩, u'⟩ := b
  unfold IsSite at ha hb
  refine ⟨?_, ?_, ?_⟩
  · unfold IsSite posA; simp only [Prod.fst_add, Prod.snd_add, Int.cast_add, hd.1, hd.2] at ha ⊢
    exact ⟨by rw [ha.1], by rw [ha.2]⟩
  · unfold IsSite posA; simp only [Prod.fst_add, Prod.snd_add, Int.cast_add, hd.1, hd.2] at hb ⊢
    exact ⟨by rw [hb.1], by rw [hb.2]⟩
  · simp only [posA] at hab ⊢
    rcases hab with ⟨h1, h2, h3⟩ | ⟨h1, h2, h3, h4⟩ | ⟨h1, h2, h3, h4⟩
    · exact Or.inl ⟨h1, by rw [h2], h3⟩
    · exact Or.inr (Or.inl ⟨h1, h2, h3, by rw [add_sub_add_right_eq_sub]; exact h4⟩)
    · exact Or.inr (Or.inr ⟨h1, h2, h3, by rw [add_sub_add_right_eq_sub]; exact h4⟩)

theorem crossN_posA (d : ℤ × ℤ) (E : Finset (Sym2 Atom)) (j : ℤ) :
    crossN (E.image (Sym2.map (posA d))) j = crossN E j := by
  unfold crossN
  have hinj : Function.Injective (posA d) := fun a b h => by rw [← posA_posA d a, h, posA_posA]
  rw [Finset.filter_image, Finset.card_image_of_injective _ (Sym2.map.injective hinj)]
  congr 1
  apply Finset.filter_congr
  intro e _
  induction e using Sym2.ind with
  | _ a b => show IsCrossS j s(posA d a, posA d b) ↔ _; rw [isCrossS_mk, isCrossS_mk]; exact Iff.rfl

theorem ncard_polysA1_pos (σ : ℤ → ZMod 3) {d : ℤ × ℤ} {s : ZMod 3}
    (hd : (d.1 : ZMod 3) = s ∧ (d.2 : ZMod 3) = s) (v : Atom) (l : ℕ) :
    (PolysA1 σ v l).ncard = (PolysA1 (fun j => σ j + s) (posA d v) l).ncard := by
  have hd' : ((-d).1 : ZMod 3) = -s ∧ ((-d).2 : ZMod 3) = -s := by
    refine ⟨?_, ?_⟩ <;> simp only [Prod.fst_neg, Prod.snd_neg, Int.cast_neg, hd.1, hd.2] <;> rfl
  apply ncard_polysA1_iso (posA d) (posA (-d)) (posA_posA d)
    (fun a => by have := posA_posA (-d) a; rwa [neg_neg] at this) (fun a b h => bond_posA hd h)
  · intro a b h
    have := bond_posA hd' h
    have e : (fun j => σ j + s + -s) = σ := by funext j; exact add_neg_cancel_right (σ j) s
    rwa [e] at this
  · intro E hE j; rw [crossN_posA]; exact hE j
  · intro E hE j; rw [crossN_posA]; exact hE j

theorem ncard_polysA1_mir (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) :
    (PolysA1 σ v l).ncard = (PolysA1 (mirS σ) (mirA v) l).ncard := ncard_polysA1_mirror σ v l

theorem diamond_isStacking : IsStacking diamond := by
  intro k
  unfold diamond
  push_cast
  intro h
  have : (1 : ZMod 3) = 0 := by linear_combination h
  exact absurd this (by decide)

/-- **Every site counts the same.** For every stacking `σ` and every site `v` of it, the polygons through
`v` with `l` edges crossing every bilayer at most twice are as many as at diamond's site `(0, (0, 0), 0)`. -/
theorem corollaryA_everySite {σ : ℤ → ZMod 3} (hσ : IsStacking σ) {v : Atom} (hv : IsSite σ v) (l : ℕ) :
    (PolysA1 σ v l).ncard = (PolysA1 diamond (0, (0, 0), 0) l).ncard := by
  obtain ⟨j, p, u⟩ := v
  -- 1. shift v's bilayer to 0
  set σ1 : ℤ → ZMod 3 := fun i => σ (i - -j) with hσ1
  have h1 := ncard_polysA1_shift σ (-j) (j, p, u) l
  have hs1 : shiftA (-j) (j, p, u) = (0, p, u) := by simp [shiftA]
  rw [hs1] at h1
  have hσ1s : IsStacking σ1 := by
    intro i h
    apply hσ (i + j)
    have h' : σ (i + 1 - -j) = σ (i - -j) := h
    rwa [show i + 1 - -j = i + j + 1 by ring, show i - -j = i + j by ring] at h'
  have hv1 : IsSite σ1 (0, p, u) := by unfold IsSite at hv ⊢; simpa [hσ1] using hv
  -- 2. make it a lower atom (mirror at bilayer 0 if it is upper)
  obtain ⟨σ2, hσ2s, hv2, h2⟩ : ∃ σ2 : ℤ → ZMod 3, IsStacking σ2 ∧ IsSite σ2 (0, p, 0) ∧
      (PolysA1 σ1 (0, p, u) l).ncard = (PolysA1 σ2 (0, p, 0) l).ncard := by
    fin_cases u
    · exact ⟨σ1, hσ1s, hv1, rfl⟩
    · refine ⟨mirS σ1, mirS_isStacking hσ1s, ?_, ?_⟩
      · have := isSite_mirA hv1; simpa [mirA] using this
      · have := ncard_polysA1_mir σ1 (0, p, 1) l; simpa [mirA] using this
  -- 3. translate the point to (0, 0) and the letter to 0
  have hd : ((-p).1 : ZMod 3) = -σ2 0 ∧ ((-p).2 : ZMod 3) = -σ2 0 := by
    unfold IsSite at hv2; simp only at hv2
    refine ⟨?_, ?_⟩ <;> simp only [Prod.fst_neg, Prod.snd_neg, Int.cast_neg, hv2.1, hv2.2] <;> rfl
  have h3 := ncard_polysA1_pos σ2 hd (0, p, 0) l
  have hp : posA (-p) (0, p, 0) = (0, (0, 0), 0) := by simp [posA]; rfl
  rw [hp] at h3
  set σ3 : ℤ → ZMod 3 := fun i => σ2 i + -σ2 0 with hσ3
  have hσ3s : IsStacking σ3 := fun i h => hσ2s i (add_right_cancel h)
  have hv3 : IsSite σ3 (0, (0, 0), 0) := by
    unfold IsSite
    refine ⟨?_, ?_⟩ <;> simp only [hσ3, Int.cast_zero] <;> exact (add_neg_cancel _).symm
  have hvd : IsSite diamond (0, (0, 0), 0) := by unfold IsSite diamond; simp
  -- 4. compare with diamond
  have h4 := corollaryA1 hσ3s diamond_isStacking hv3 hvd l
  rw [h1, h2, h3, h4]

end LoopEqualityProof
