module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.Parts
public import LoopEquality.Counting
public import LoopEquality.Transfer
public import LoopEquality.TheoremB
public import LoopEquality.Pairings

@[expose] public section

/-!
# Theorem B in #102's form: `2 Δ = − Σ A_w · A_f` (Lean paper, step 2e)

#102, §5: `p_l(v; σ') − p_l(v; σ) = −½ Σ A_root(S, M, R) · A_far(S, M', F)`. Here, per site `v` below the cut and
with whole numbers, `2 · (#polygons after the flip − #polygons before) = − Σ_P Σ_{(M, M', r, s)} A_w · A_f`, where
`A_w(P, M, r) = W(P, M, r) − W(gP, gM, r)` and `A_f(P, M', s) = F(P, M', s) − F(gP, gM', s)`, `W` counting root
linkages through `v` and `F` far linkages by their ends `P`, pairing and size, and `g` the half-turn `p ↦ c − p`.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-! ## The half-turn on crossing sets and pairings -/

def gP (c : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : Finset (ℤ × ℤ) := P.image (fun p => c - p)
def gM (c : ℤ × ℤ) (M : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : Finset ((ℤ × ℤ) × (ℤ × ℤ)) := M.image (gg c)

theorem gP_gP (c : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : gP c (gP c P) = P := image_sub_sub c P

theorem gg_gg (c : ℤ × ℤ) (x : (ℤ × ℤ) × (ℤ × ℤ)) : gg c (gg c x) = x := by
  obtain ⟨p, q⟩ := x; simp [gg]

theorem gM_gM (c : ℤ × ℤ) (M : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : gM c (gM c M) = M := by
  unfold gM; rw [Finset.image_image]
  conv_rhs => rw [← Finset.image_id (s := M)]
  exact Finset.image_congr (fun x _ => gg_gg c x)

theorem card_gP (c : ℤ × ℤ) (P : Finset (ℤ × ℤ)) : (gP c P).card = P.card :=
  Finset.card_image_of_injective _ (fun a b h => by simpa using h)

theorem mem_gP {c : ℤ × ℤ} {P : Finset (ℤ × ℤ)} {p : ℤ × ℤ} : p ∈ gP c P ↔ c - p ∈ P := by
  unfold gP; constructor
  · rintro h; obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp h; simpa using hq
  · intro h; exact Finset.mem_image.mpr ⟨c - p, h, by simp⟩

theorem mem_gM {c : ℤ × ℤ} {M : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {x : (ℤ × ℤ) × (ℤ × ℤ)} : x ∈ gM c M ↔ gg c x ∈ M := by
  unfold gM; constructor
  · rintro h; obtain ⟨y, hy, rfl⟩ := Finset.mem_image.mp h; rwa [gg_gg]
  · intro h; exact Finset.mem_image.mpr ⟨gg c x, h, gg_gg c x⟩

theorem gM_sub {c : ℤ × ℤ} {P : Finset (ℤ × ℤ)} {M : Finset ((ℤ × ℤ) × (ℤ × ℤ))} (h : M ⊆ P ×ˢ P) :
    gM c M ⊆ gP c P ×ˢ gP c P := by
  intro x hx
  have := h (mem_gM.mp hx)
  obtain ⟨p, q⟩ := x
  simp only [gg, Finset.mem_product] at this ⊢
  exact ⟨mem_gP.mpr this.1, mem_gP.mpr this.2⟩

theorem oneCycle_g {c : ℤ × ℤ} {P : Finset (ℤ × ℤ)} {M N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} (h : OneCycleRel P M N) :
    OneCycleRel (gP c P) (gM c M) (gM c N) := by
  intro Q hQ hne h1 h2
  have key := h (gP c Q) (fun p hp => by
      have := hQ (mem_gP.mp hp); rw [mem_gP, sub_sub_cancel] at this; exact this)
    (by obtain ⟨q, hq⟩ := hne; exact ⟨c - q, mem_gP.mpr (by rwa [sub_sub_cancel])⟩)
    (fun p hp q hq hm => by
      rw [mem_gP] at hp ⊢
      have := h1 (c - p) hp (c - q) (mem_gP.mpr (by rwa [sub_sub_cancel])) (mem_gM.mpr (by simpa [gg] using hm))
      exact this)
    (fun p hp q hq hm => by
      rw [mem_gP] at hp ⊢
      exact h2 (c - p) hp (c - q) (mem_gP.mpr (by rwa [sub_sub_cancel])) (mem_gM.mpr (by simpa [gg] using hm)))
  have := congrArg (gP c) key
  rwa [gP_gP] at this

/-! ## The counts and their asymmetries -/

noncomputable def Wc (σ : ℤ → ZMod 3) (v : Atom) (k : ℤ) (P : Finset (ℤ × ℤ)) (M : Finset ((ℤ × ℤ) × (ℤ × ℤ)))
    (r : ℕ) : ℤ := (RootSet σ v k P M r).ncard
noncomputable def Fc (σ : ℤ → ZMod 3) (k : ℤ) (P : Finset (ℤ × ℤ)) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (s : ℕ) : ℤ :=
  (FarSet σ k P N s).ncard
noncomputable def Aw (σ : ℤ → ZMod 3) (v : Atom) (k : ℤ) (c : ℤ × ℤ) (P : Finset (ℤ × ℤ))
    (M : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (r : ℕ) : ℤ := Wc σ v k P M r - Wc σ v k (gP c P) (gM c M) r
noncomputable def Af (σ : ℤ → ZMod 3) (k : ℤ) (c : ℤ × ℤ) (P : Finset (ℤ × ℤ))
    (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (s : ℕ) : ℤ := Fc σ k P N s - Fc σ k (gP c P) (gM c N) s

theorem Af_g (σ : ℤ → ZMod 3) (k : ℤ) (c : ℤ × ℤ) (P : Finset (ℤ × ℤ)) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) (s : ℕ) :
    Af σ k c (gP c P) (gM c N) s = - Af σ k c P N s := by
  unfold Af; rw [gP_gP, gM_gM]; ring

/-! ## Each crossing set: the change is `− Σ W · A_f` -/

theorem ncard_partsCross_sum {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {P : Finset (ℤ × ℤ)}
    (hP : P.Nonempty) (hV : ∀ p ∈ P, BondS σ (vert k p)) :
    ((PartsCross σ v l k P).ncard : ℤ) =
      ∑ x ∈ idxSet l P P (OneCycleRel P), Wc σ v k P x.1.1 x.2.1 * Fc σ k P x.1.2 x.2.2 := by
  have hfin := partsCross_finite (v := v) (l := l) hP hV
  rw [partsCross_eq_gen] at hfin ⊢
  rw [ncard_genParts hfin]; push_cast; rfl

theorem idx_flip_mem {l : ℕ} {c : ℤ × ℤ} {P : Finset (ℤ × ℤ)} {x} (hx : x ∈ idxSet l P P (OneCycleRel P)) :
    ((x.1.1, gM c x.1.2), x.2) ∈ idxSet l P (gP c P) (fun M N => OneCycleRel P M (N.image (gg c))) := by
  simp only [idxSet, Finset.mem_filter, Finset.mem_product, Finset.mem_powerset] at hx ⊢
  refine ⟨⟨⟨hx.1.1.1, gM_sub hx.1.1.2⟩, hx.1.2⟩, hx.2.1, ?_⟩
  show OneCycleRel P x.1.1 (gM c (gM c x.1.2)); rw [gM_gM]; exact hx.2.2

theorem idx_flip_mem' {l : ℕ} {c : ℤ × ℤ} {P : Finset (ℤ × ℤ)} {x}
    (hx : x ∈ idxSet l P (gP c P) (fun M N => OneCycleRel P M (N.image (gg c)))) :
    ((x.1.1, gM c x.1.2), x.2) ∈ idxSet l P P (OneCycleRel P) := by
  simp only [idxSet, Finset.mem_filter, Finset.mem_product, Finset.mem_powerset] at hx ⊢
  refine ⟨⟨⟨hx.1.1.1, ?_⟩, hx.1.2⟩, hx.2.1, hx.2.2⟩
  have := gM_sub (c := c) hx.1.1.2; rwa [gP_gP] at this

theorem ncard_flipParts_sum {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c)
    {P : Finset (ℤ × ℤ)} (hP : P.Nonempty) (hV : ∀ p ∈ P, BondS σ (vert k p)) :
    ((FlipParts σ v l k P c).ncard : ℤ) =
      ∑ x ∈ idxSet l P P (OneCycleRel P), Wc σ v k P x.1.1 x.2.1 * Fc σ k (gP c P) (gM c x.1.2) x.2.2 := by
  have hfin := flipParts_finite (v := v) (l := l) hc hP hV
  rw [flipParts_eq_gen] at hfin ⊢
  rw [ncard_genParts hfin]; push_cast
  symm
  apply Finset.sum_nbij' (fun x => ((x.1.1, gM c x.1.2), x.2)) (fun x => ((x.1.1, gM c x.1.2), x.2))
  · intro x hx; exact idx_flip_mem hx
  · intro x hx; exact idx_flip_mem' hx
  · intro x _; simp [gM_gM]
  · intro x _; simp [gM_gM]
  · intro x _; rfl

/-- One crossing set: the flipped count minus the count is `− Σ W · A_f`. -/
theorem change_at {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c)
    {P : Finset (ℤ × ℤ)} (hP : P.Nonempty) (hV : ∀ p ∈ P, BondS σ (vert k p)) :
    ((FlipParts σ v l k P c).ncard : ℤ) - (PartsCross σ v l k P).ncard =
      - ∑ x ∈ idxSet l P P (OneCycleRel P), Wc σ v k P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 := by
  rw [ncard_flipParts_sum hc hP hV, ncard_partsCross_sum hP hV, ← Finset.sum_sub_distrib, ← Finset.sum_neg_distrib]
  apply Finset.sum_congr rfl; intro x _; unfold Af; ring

/-! ## The family of crossing sets, closed under the half-turn -/

theorem bondS_vert_iff {σ : ℤ → ZMod 3} {k : ℤ} {p : ℤ × ℤ} :
    BondS σ (vert k p) ↔ ((p.1 : ZMod 3) = σ k ∧ (p.2 : ZMod 3) = σ k) := by
  unfold vert; rw [bondS_mk]; unfold Bond IsSite
  simp only
  constructor
  · rintro ⟨h, -, -⟩; exact h
  · intro h; exact ⟨h, h, by simp⟩

theorem bondS_vert_g {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {p : ℤ × ℤ}
    (h : BondS σ (vert k p)) : BondS σ (vert k (c - p)) := by
  rw [bondS_vert_iff] at h ⊢
  unfold GoodCentre at hc
  simp only [Prod.fst_sub, Prod.snd_sub, Int.cast_sub, hc.1, hc.2, h.1, h.2]
  constructor <;> ring

/-- The crossing sets of Theorem B, closed under the half-turn: nonempty subsets of the window and its half-turn
whose vertical bonds are bonds. -/
noncomputable def famP (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) (k : ℤ) (c : ℤ × ℤ) : Finset (Finset (ℤ × ℤ)) :=
  (window v l ∪ gP c (window v l)).powerset.filter (fun P => P.Nonempty ∧ ∀ p ∈ P, BondS σ (vert k p))

theorem famP_g {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c)
    {P : Finset (ℤ × ℤ)} (hP : P ∈ famP σ v l k c) : gP c P ∈ famP σ v l k c := by
  simp only [famP, Finset.mem_filter, Finset.mem_powerset] at hP ⊢
  obtain ⟨hsub, ⟨q, hq⟩, hV⟩ := hP
  refine ⟨?_, ⟨c - q, mem_gP.mpr (by rwa [sub_sub_cancel])⟩, ?_⟩
  · intro p hp
    have h1 := hsub (mem_gP.mp hp)
    rcases Finset.mem_union.mp h1 with h | h
    · exact Finset.mem_union_right _ (mem_gP.mpr h)
    · rw [mem_gP, sub_sub_cancel] at h; exact Finset.mem_union_left _ h
  · intro p hp
    have := bondS_vert_g hc (hV _ (mem_gP.mp hp)); rwa [sub_sub_cancel] at this

theorem polysCross_window {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {P : Finset (ℤ × ℤ)} {E : Finset (Sym2 Atom)}
    (hE : E ∈ PolysCross σ v l k P) : P ⊆ window v l := by
  obtain ⟨hpoly, hv, hcard, hP⟩ := hE
  intro p hp
  have hb := polygon_in_box hpoly hv ((hP p).mp hp)
  rw [hcard, vert, Finset.mk_mem_sym2_iff] at hb
  exact Finset.mem_image.mpr ⟨_, hb.1, rfl⟩

/-- Outside the window the change vanishes. -/
theorem change_zero {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c)
    (hv : ¬ IsFar k v) {P : Finset (ℤ × ℤ)} (hP : P.Nonempty) (hV : ∀ p ∈ P, BondS σ (vert k p))
    (hw : ¬ P ⊆ window v l) :
    ((FlipParts σ v l k P c).ncard : ℤ) - (PartsCross σ v l k P).ncard = 0 := by
  rw [← theoremB_count hc hv hP hV, ← ncard_polysCross hv hP hV]
  have e1 : PolysCross (flipAt σ k) v l k P = ∅ := Set.eq_empty_of_forall_notMem (fun E hE => hw (polysCross_window hE))
  have e2 : PolysCross σ v l k P = ∅ := Set.eq_empty_of_forall_notMem (fun E hE => hw (polysCross_window hE))
  rw [e1, e2]; simp

/-! ## The symmetrisation -/

theorem idx_g_mem {l : ℕ} {c : ℤ × ℤ} {P : Finset (ℤ × ℤ)} {x} (hx : x ∈ idxSet l P P (OneCycleRel P)) :
    ((gM c x.1.1, gM c x.1.2), x.2) ∈ idxSet l (gP c P) (gP c P) (OneCycleRel (gP c P)) := by
  simp only [idxSet, Finset.mem_filter, Finset.mem_product, Finset.mem_powerset] at hx ⊢
  exact ⟨⟨⟨gM_sub hx.1.1.1, gM_sub hx.1.1.2⟩, hx.1.2⟩, by rw [card_gP]; exact hx.2.1, oneCycle_g hx.2.2⟩

theorem sum_g (σ : ℤ → ZMod 3) (v : Atom) (l : ℕ) (k : ℤ) (c : ℤ × ℤ) (P : Finset (ℤ × ℤ)) :
    ∑ x ∈ idxSet l (gP c P) (gP c P) (OneCycleRel (gP c P)), Wc σ v k (gP c P) x.1.1 x.2.1 * Af σ k c (gP c P) x.1.2 x.2.2 =
      - ∑ x ∈ idxSet l P P (OneCycleRel P), Wc σ v k (gP c P) (gM c x.1.1) x.2.1 * Af σ k c P x.1.2 x.2.2 := by
  rw [← Finset.sum_neg_distrib]
  symm
  apply Finset.sum_nbij' (fun x => ((gM c x.1.1, gM c x.1.2), x.2)) (fun x => ((gM c x.1.1, gM c x.1.2), x.2))
  · intro x hx; exact idx_g_mem hx
  · intro x hx; have := idx_g_mem (c := c) hx; rwa [gP_gP] at this
  · intro x _; simp [gM_gM]
  · intro x _; simp [gM_gM]
  · intro x _; simp only; rw [Af_g]; ring

/-- **Theorem B in #102's form.** For a good centre `c` of `σ` at `k` and `v` on the root side of `k`:
`2 · (#polygons through v with l edges after the flip − before) = − Σ_P Σ_{(M, M', r, s)} A_w(P, M, r) · A_f(P, M', s)`,
over the crossing sets `P` of `famP` (closed under the half-turn `g`) and the pairings `M, M'` of `P` closing into one
cycle with `r + |P| + s = l`. -/
theorem theoremB_sym {σ : ℤ → ZMod 3} {v : Atom} {l : ℕ} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c)
    (hv : ¬ IsFar k v) :
    2 * (((Polys (flipAt σ k) v l).ncard : ℤ) - (Polys σ v l).ncard) =
      - ∑ P ∈ famP σ v l k c, ∑ x ∈ idxSet l P P (OneCycleRel P), Aw σ v k c P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 := by
  -- the change as a sum over famP
  have hB := theoremB (v := v) (l := l) hc hv
  have hext : ∑ P ∈ (window v l).powerset.filter (fun P => P.Nonempty ∧ ∀ p ∈ P, BondS σ (vert k p)),
      (((FlipParts σ v l k P c).ncard : ℤ) - (PartsCross σ v l k P).ncard) =
      ∑ P ∈ famP σ v l k c, (((FlipParts σ v l k P c).ncard : ℤ) - (PartsCross σ v l k P).ncard) := by
    apply Finset.sum_subset
    · intro P hP
      simp only [famP, Finset.mem_filter, Finset.mem_powerset] at hP ⊢
      exact ⟨hP.1.trans Finset.subset_union_left, hP.2⟩
    · intro P hP hnot
      simp only [famP, Finset.mem_filter, Finset.mem_powerset] at hP hnot
      exact change_zero hc hv hP.2.1 hP.2.2 (fun h => hnot ⟨h, hP.2⟩)
  have hD : ((Polys (flipAt σ k) v l).ncard : ℤ) - (Polys σ v l).ncard =
      - ∑ P ∈ famP σ v l k c, ∑ x ∈ idxSet l P P (OneCycleRel P), Wc σ v k P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2 := by
    rw [hB, add_sub_cancel_left, hext, ← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro P hP
    simp only [famP, Finset.mem_filter] at hP
    exact change_at hc hP.2.1 hP.2.2
  -- symmetrise: reindex P ↦ gP
  set S := ∑ P ∈ famP σ v l k c, ∑ x ∈ idxSet l P P (OneCycleRel P), Wc σ v k P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2
  set S' := ∑ P ∈ famP σ v l k c, ∑ x ∈ idxSet l P P (OneCycleRel P),
    Wc σ v k (gP c P) (gM c x.1.1) x.2.1 * Af σ k c P x.1.2 x.2.2
  have hSS : S = - S' := by
    have : S = ∑ P ∈ famP σ v l k c, ∑ x ∈ idxSet l (gP c P) (gP c P) (OneCycleRel (gP c P)),
        Wc σ v k (gP c P) x.1.1 x.2.1 * Af σ k c (gP c P) x.1.2 x.2.2 := by
      apply Finset.sum_nbij' (gP c) (gP c)
      · intro P hP; exact famP_g hc hP
      · intro P hP; exact famP_g hc hP
      · intro P _; exact gP_gP c P
      · intro P _; exact gP_gP c P
      · intro P _; rw [gP_gP]
    rw [this, ← Finset.sum_neg_distrib]
    exact Finset.sum_congr rfl (fun P _ => sum_g σ v l k c P)
  have hsum : ∑ P ∈ famP σ v l k c, ∑ x ∈ idxSet l P P (OneCycleRel P), Aw σ v k c P x.1.1 x.2.1 * Af σ k c P x.1.2 x.2.2
      = S - S' := by
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl; intro P _
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl; intro x _
    unfold Aw; ring
  rw [hD, hsum, hSS]; ring

end LoopEqualityProof
