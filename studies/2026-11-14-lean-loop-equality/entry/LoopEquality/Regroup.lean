module

public import Mathlib
public import LoopEquality.Matching
public import LoopEquality.Pairing14

@[expose] public section

/-!
# Translation invariance of the root counts and the far asymmetry

Toward regrouping the crossing sets of Theorem B by translation class.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

def GoodVec (d : ℤ × ℤ) : Prop := (d.1 : ZMod 3) = 0 ∧ (d.2 : ZMod 3) = 0

theorem goodVec_neg {d : ℤ × ℤ} (h : GoodVec d) : GoodVec (-d) := by
  unfold GoodVec at *; simp [h.1, h.2]

theorem mirA_posA (d : ℤ × ℤ) (a : Atom) : mirA (posA d a) = posA d (mirA a) := rfl

theorem degS_posA {F : Finset (Sym2 Atom)} (d : ℤ × ℤ) (w : Atom) :
    degS (F.image (Sym2.map (posA d))) (posA d w) = degS F w := by
  have hinv : ∀ a, posA (-d) (posA d a) = a := posA_posA d
  have hinj : Function.Injective (posA d) := fun a b h => by rw [← hinv a, h, hinv]
  unfold degS
  rw [Finset.filter_image, Finset.card_image_of_injective _ (Sym2.map.injective hinj)]
  congr 1; ext e; simp only [Finset.mem_filter, Function.comp, Sym2.mem_map]
  constructor
  · rintro ⟨he, b, hb, hbw⟩; exact ⟨he, (hinj hbw) ▸ hb⟩
  · rintro ⟨he, hw⟩; exact ⟨he, w, hw, rfl⟩

/-- **Root counts are invariant under lattice translations** (of the crossing set, the pairing and `v` together). -/
theorem Wc_translate {σ : ℤ → ZMod 3} {k : ℤ} {d : ℤ × ℤ} (hd : GoodVec d) (v : Atom) (P : Finset (ℤ × ℤ))
    (M : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (r : ℕ) :
    Wc σ (posA d v) k (trP d P) (trM d M) r = Wc σ v k P M r := by
  rw [Wc_mir, Wc_mir]
  have hd' := goodVec_neg hd
  have hinv : ∀ a, posA (-d) (posA d a) = a := posA_posA d
  have hinv' : ∀ a, posA d (posA (-d) a) = a := fun a => by have := posA_posA (-d) a; rwa [neg_neg] at this
  have hinj : Function.Injective (posA d) := fun a b h => by rw [← hinv a, h, hinv]
  congr 1
  symm
  apply Set.ncard_congr (fun F _ => F.image (Sym2.map (posA d)))
  · rintro F ⟨hF, hv⟩
    refine ⟨farSet_translate hd hF, ?_⟩
    rw [mirA_posA, degS_posA]; exact hv
  · intro F₁ F₂ _ _ h; exact Finset.image_injective (Sym2.map.injective hinj) h
  · rintro G ⟨hG, hv⟩
    have h2 := farSet_translate hd' hG
    rw [trP_neg, trM_neg] at h2
    refine ⟨_, ⟨h2, ?_⟩, ?_⟩
    · have := degS_posA (F := G) (-d) (posA d (mirA v))
      rw [hinv] at this
      rw [this, ← mirA_posA]; exact hv
    · show (G.image (Sym2.map (posA (-d)))).image (Sym2.map (posA d)) = G
      rw [Finset.image_image, show Sym2.map (posA d) ∘ Sym2.map (posA (-d)) = id from funext (map_left_inv hinv'),
        Finset.image_id]

theorem gP_trP (c d : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : gP c (trP d P) = trP (-d) (gP c P) := by
  unfold gP trP; rw [Finset.image_image, Finset.image_image]; congr 1; funext p; simp; abel

theorem gM_trM (c d : ℤ × ℤ) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : gM c (trM d N) = trM (-d) (gM c N) := by
  unfold gM trM; rw [Finset.image_image, Finset.image_image]; congr 1; funext x; simp [gg]; constructor <;> abel

/-- **The far asymmetry is invariant under lattice translations.** -/
theorem Af_translate {σ : ℤ → ZMod 3} {k : ℤ} {c d : ℤ × ℤ} (hd : GoodVec d) (P : Finset (ℤ × ℤ))
    (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (s : ℕ) : Af σ k c (trP d P) (trM d N) s = Af σ k c P N s := by
  unfold Af
  rw [Fc_translate hd, gP_trP, gM_trM, Fc_translate (goodVec_neg hd)]

/-! ## One representative per translation class -/

/-- The lattice vector `3 f`. -/
def sc (f : ℤ × ℤ) : ℤ × ℤ := (3 * f.1, 3 * f.2)

theorem sc_add (f g : ℤ × ℤ) : sc (f + g) = sc f + sc g := by unfold sc; ext <;> simp <;> ring
theorem sc_neg (f : ℤ × ℤ) : sc (-f) = - sc f := by unfold sc; ext <;> simp

theorem trP_trP (d e : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : trP d (trP e P) = trP (e + d) P := by
  unfold trP; rw [Finset.image_image]; congr 1; funext p; simp [add_assoc]

theorem trP_zero (P : Finset (ℤ × ℤ)) : trP 0 P = P := by unfold trP; simp

def psum (P : Finset (ℤ × ℤ)) : ℤ × ℤ := ∑ p ∈ P, p

theorem psum_trP (d : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : psum (trP d P) = psum P + (P.card : ℤ) • d := by
  unfold psum trP
  rw [Finset.sum_image (fun p _ q _ h => by simpa using h), Finset.sum_add_distrib, Finset.sum_const]
  simp

/-- The class shift: `nrm P = trP (sc (shift P)) P` has its coordinate sum in `[0, 3|P|)²`. -/
def shift (P : Finset (ℤ × ℤ)) : ℤ × ℤ :=
  (-((psum P).1 / (3 * P.card)), -((psum P).2 / (3 * P.card)))

def nrm (P : Finset (ℤ × ℤ)) : Finset (ℤ × ℤ) := trP (sc (shift P)) P

theorem shift_trP {P : Finset (ℤ × ℤ)} (hP : P.Nonempty) (f : ℤ × ℤ) : shift (trP (sc f) P) = shift P - f := by
  have hpos : (0 : ℤ) < 3 * P.card := by have := hP.card_pos; omega
  have hcard : (trP (sc f) P).card = P.card := by
    unfold trP; exact Finset.card_image_of_injective _ (fun p q h => by simpa using h)
  unfold shift
  rw [psum_trP, hcard]
  simp only [sc, Prod.fst_add, Prod.snd_add, Prod.smul_fst, Prod.smul_snd, smul_eq_mul, Prod.fst_sub, Prod.snd_sub]
  have e1 : (psum P).1 + ↑P.card * (3 * f.1) = (psum P).1 + f.1 * (3 * ↑P.card) := by ring
  have e2 : (psum P).2 + ↑P.card * (3 * f.2) = (psum P).2 + f.2 * (3 * ↑P.card) := by ring
  rw [e1, e2, Int.add_mul_ediv_right _ _ hpos.ne', Int.add_mul_ediv_right _ _ hpos.ne']
  ext <;> simp <;> ring

theorem nrm_trP {P : Finset (ℤ × ℤ)} (hP : P.Nonempty) (f : ℤ × ℤ) : nrm (trP (sc f) P) = nrm P := by
  unfold nrm; rw [shift_trP hP, trP_trP, ← sc_add]; congr 2; abel

theorem trP_nonempty {P : Finset (ℤ × ℤ)} (d : ℤ × ℤ) : (trP d P).Nonempty ↔ P.Nonempty := by
  unfold trP; exact Finset.image_nonempty

theorem shift_nrm {P : Finset (ℤ × ℤ)} (hP : P.Nonempty) : shift (nrm P) = 0 := by
  unfold nrm; rw [shift_trP hP]; simp

/-- **Regrouping by translation class.** For `G` invariant under joint lattice translations of an atom and a
crossing set: summing `G v` over crossing sets equals summing `G` over class representatives `S` and the translates
`v + 3 f` of `v`. -/
theorem regroup (G : Atom → Finset (ℤ × ℤ) → ℤ) (v : Atom)
    (hG : ∀ f a P, G (posA (sc f) a) (trP (sc f) P) = G a P)
    (A : Finset (Finset (ℤ × ℤ))) (hA : ∀ P, G v P ≠ 0 → P ∈ A) (hne : ∀ P, G v P ≠ 0 → P.Nonempty)
    (Z : Finset (Finset (ℤ × ℤ))) (hZ : ∀ P, G v P ≠ 0 → nrm P ∈ Z) (hZn : ∀ S ∈ Z, nrm S = S)
    (T : Finset (ℤ × ℤ) → Finset (ℤ × ℤ)) (hT : ∀ S f, G (posA (sc f) v) S ≠ 0 → f ∈ T S) :
    ∑ P ∈ A, G v P = ∑ S ∈ Z, ∑ f ∈ T S, G (posA (sc f) v) S := by
  have sc0 : sc 0 = 0 := by simp [sc]
  have hinvP : ∀ f P, trP (sc (-f)) (trP (sc f) P) = P := fun f P => by
    rw [trP_trP, ← sc_add, add_neg_cancel, sc0, trP_zero]
  have hGv : ∀ f S, G (posA (sc f) v) S = G v (trP (sc (-f)) S) := fun f S => by
    have := hG f v (trP (sc (-f)) S)
    rw [trP_trP, ← sc_add, neg_add_cancel, sc0, trP_zero] at this
    exact this
  calc ∑ P ∈ A, G v P = ∑ P ∈ A.filter (fun P => G v P ≠ 0), G v P := (Finset.sum_filter_ne_zero _).symm
    _ = ∑ x ∈ (Z.sigma T).filter (fun x => G (posA (sc x.2) v) x.1 ≠ 0), G (posA (sc x.2) v) x.1 := by
      apply Finset.sum_nbij' (fun P => (⟨nrm P, shift P⟩ : (_ : Finset (ℤ × ℤ)) × (ℤ × ℤ)))
        (fun x => trP (sc (-x.2)) x.1)
      · intro P hP
        obtain ⟨-, hP⟩ := Finset.mem_filter.mp hP
        have e : G (posA (sc (shift P)) v) (nrm P) = G v P := hG (shift P) v P
        exact Finset.mem_filter.mpr ⟨Finset.mem_sigma.mpr ⟨hZ P hP, hT _ _ (by rw [e]; exact hP)⟩,
          by simp only; rw [e]; exact hP⟩
      · rintro ⟨S, f⟩ hx
        obtain ⟨-, hx⟩ := Finset.mem_filter.mp hx
        simp only at hx ⊢
        rw [hGv] at hx
        exact Finset.mem_filter.mpr ⟨hA _ hx, hx⟩
      · intro P hP
        obtain ⟨-, hP⟩ := Finset.mem_filter.mp hP
        simp only [nrm]; exact hinvP _ _
      · rintro ⟨S, f⟩ hx
        obtain ⟨hmem, hx⟩ := Finset.mem_filter.mp hx
        obtain ⟨hS, -⟩ := Finset.mem_sigma.mp hmem
        simp only at hx ⊢
        rw [hGv] at hx
        have hneS : S.Nonempty := (trP_nonempty _).mp (hne _ hx)
        have hSn := hZn S hS
        have h0 : shift S = 0 := by rw [← hSn]; exact shift_nrm hneS
        rw [nrm_trP hneS, hSn, shift_trP hneS, h0, zero_sub, neg_neg]
      · intro P _
        exact (hG (shift P) v P).symm
    _ = ∑ x ∈ Z.sigma T, G (posA (sc x.2) v) x.1 := Finset.sum_filter_ne_zero _
    _ = ∑ S ∈ Z, ∑ f ∈ T S, G (posA (sc f) v) S := Finset.sum_sigma _ _ _

end LoopEqualityProof
