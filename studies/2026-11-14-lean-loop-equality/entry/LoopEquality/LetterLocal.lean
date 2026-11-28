module

public import Mathlib
public import LoopEquality.Height

@[expose] public section

/-!
# The (6, 6) terms see only the letters of bilayers `k - 1`, `k`, `k + 1`

A far linkage with 6 edges on four crossing points is two arcs of 2 and 4 edges, so it stays in bilayers `k` and `k + 1`
(`Height.lean`); the root side, through the mirror, in `k - 1` and `k`. Hence `G16` is the same for two stackings that
agree there.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-- A far linkage on four points, paired `a b | c d`, splits into its two arcs. -/
theorem split_farSet {τ : ℤ → ZMod 3} {k : ℤ} {a b c d : ℤ × ℤ}
    (hdis : ∀ p ∈ ({a, b} : Finset (ℤ × ℤ)), ∀ q ∈ ({c, d} : Finset (ℤ × ℤ)), p ≠ q) {s : ℕ} {F : Finset (Sym2 Atom)}
    (hF : F ∈ FarSet τ k {a, b, c, d} (pr2 a b ∪ pr2 c d) s) :
    (compPart F (upA k a), restPart F (upA k a)) ∈ TwoArcs τ k a b c d s := by
  obtain ⟨hFl, hs, hN⟩ := hF
  set x₀ := upA k a
  have hconn : ∀ p ∈ ({a, b, c, d} : Finset (ℤ × ℤ)), (Conn F x₀ (upA k p) ↔ p ∈ ({a, b} : Finset (ℤ × ℤ))) := by
    intro p hp
    have : (a, p) ∈ pairF k F {a, b, c, d} ↔ Conn F x₀ (upA k p) := by
      simp only [pairF, Finset.mem_filter, Finset.mem_product]
      exact ⟨fun h => h.2, fun h => ⟨⟨by simp, hp⟩, h⟩⟩
    rw [← this, hN]
    simp only [pr2, Finset.mem_union, Finset.mem_product]
    have ha : a ∈ ({a, b} : Finset (ℤ × ℤ)) := by simp
    constructor
    · rintro (⟨-, h⟩ | ⟨h, -⟩)
      · exact h
      · exact absurd rfl (hdis a ha a h)
    · intro h; exact Or.inl ⟨ha, h⟩
  have f1 : (({a, b, c, d} : Finset (ℤ × ℤ)).image (upA k)).filter (Conn F x₀) = ({a, b} : Finset (ℤ × ℤ)).image (upA k) := by
    ext w; simp only [Finset.mem_filter, Finset.mem_image]
    constructor
    · rintro ⟨⟨p, hp, rfl⟩, hc⟩; exact ⟨p, (hconn p hp).mp hc, rfl⟩
    · rintro ⟨p, hp, rfl⟩
      have hpP : p ∈ ({a, b, c, d} : Finset (ℤ × ℤ)) := by rw [quad_eq]; exact Finset.mem_union_left _ hp
      exact ⟨⟨p, hpP, rfl⟩, (hconn p hpP).mpr hp⟩
  have f2 : (({a, b, c, d} : Finset (ℤ × ℤ)).image (upA k)).filter (fun w => ¬ Conn F x₀ w) =
      ({c, d} : Finset (ℤ × ℤ)).image (upA k) := by
    ext w; simp only [Finset.mem_filter, Finset.mem_image]
    constructor
    · rintro ⟨⟨p, hp, rfl⟩, hc⟩
      refine ⟨p, ?_, rfl⟩
      rw [quad_eq] at hp
      rcases Finset.mem_union.mp hp with h | h
      · exact absurd ((hconn p (by rw [quad_eq]; exact Finset.mem_union_left _ h)).mpr h) hc
      · exact h
    · rintro ⟨p, hp, rfl⟩
      have hpP : p ∈ ({a, b, c, d} : Finset (ℤ × ℤ)) := by rw [quad_eq]; exact Finset.mem_union_right _ hp
      refine ⟨⟨p, hpP, rfl⟩, fun hc => ?_⟩
      exact hdis p ((hconn p hpP).mp hc) p hp rfl
  have hab : Conn F (upA k a) (upA k b) := (hconn b (by simp)).mpr (by simp)
  have hcd : Conn F (upA k c) (upA k d) := by
    have : (c, d) ∈ pairF k F {a, b, c, d} := by rw [hN]; simp [pr2]
    exact conn_of_pairF this
  have hnc : ¬ Conn F x₀ (upA k c) := fun h =>
    hdis c ((hconn c (by simp)).mp h) c (by simp) rfl
  refine ⟨⟨?_, ?_, ?_⟩, ?_, ⟨?_, ?_, ?_⟩, ?_, ?_, ?_⟩
  · rw [← f1]; exact linkage_compPart hFl.1 x₀
  · intro e he w hw; exact hFl.2.1 e (Finset.filter_subset _ _ he) w hw
  · intro e he; exact hFl.2.2 e (Finset.filter_subset _ _ he)
  · exact pairF_full (conn_compPart Relation.ReflTransGen.refl hab)
  · rw [← f2]; exact linkage_restPart hFl.1 x₀
  · intro e he w hw; exact hFl.2.1 e (Finset.filter_subset _ _ he) w hw
  · intro e he; exact hFl.2.2 e (Finset.filter_subset _ _ he)
  · exact pairF_full (conn_restPart hnc hcd)
  · rw [← Finset.card_union_of_disjoint (disjoint_compPart_restPart F x₀), compPart_union_restPart, hs]
  · exact compPart_restPart_atoms F x₀

theorem arc_len_ge2 {τ : ℤ → ZMod 3} {k : ℤ} {a b : ℤ × ℤ} (hab : a ≠ b) {i : ℕ} {l : List Atom}
    (hl : l ∈ FarPaths τ k a b i) : 2 ≤ i := by
  have h1 := farPaths_len hab hl
  have h2 := farPaths_even hl
  rw [hl.2.2.2.1] at h1; omega

/-- Atoms of a far linkage with 6 edges on four points lie in bilayers `k` and `k + 1`. -/
theorem farSet6_layers {τ : ℤ → ZMod 3} {k : ℤ} {P : Finset (ℤ × ℤ)} {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))}
    {F : Finset (Sym2 Atom)} (hF : F ∈ FarSet τ k P N 6) (hP : P.card = 4) :
    ∀ e ∈ F, ∀ w ∈ e, k ≤ w.1 ∧ w.1 ≤ k + 1 := by
  obtain ⟨a, ha⟩ : P.Nonempty := Finset.card_pos.mp (by omega)
  obtain ⟨b, c, d, hPe, hdis, hab, hcd, hN⟩ := pairF_four hF.1 hP ha
  have hF' : F ∈ FarSet τ k {a, b, c, d} (pr2 a b ∪ pr2 c d) 6 := by
    rw [← hPe, ← hN]; exact ⟨hF.1, hF.2.1, rfl⟩
  obtain ⟨h1, hp1, h2, hp2, hs, -⟩ := split_farSet hdis hF'
  set F₁ := compPart F (upA k a); set F₂ := restPart F (upA k a)
  obtain ⟨l₁, hl₁, e1⟩ := arc_to_farPath hab ⟨h1, rfl, hp1⟩
  obtain ⟨l₂, hl₂, e2⟩ := arc_to_farPath hcd ⟨h2, rfl, hp2⟩
  have g1 := arc_len_ge2 hab hl₁
  have g2 := arc_len_ge2 hcd hl₂
  intro e he w hw
  have hu : F₁ ∪ F₂ = F := compPart_union_restPart F (upA k a)
  rw [← hu] at he
  rcases Finset.mem_union.mp he with he | he
  · have e1' : pathEdges l₁ = F₁ := e1
    rw [← e1'] at he
    exact arc_layer (by omega) hl₁ (atom_of_pathEdges he w hw)
  · have e2' : pathEdges l₂ = F₂ := e2
    rw [← e2'] at he
    exact arc_layer (by omega) hl₂ (atom_of_pathEdges he w hw)

theorem bond_letters {σ σ' : ℤ → ZMod 3} {x y : Atom} (hx : σ x.1 = σ' x.1) (hy : σ y.1 = σ' y.1) :
    Bond σ x y ↔ Bond σ' x y := by
  unfold Bond IsSite; rw [hx, hy]

theorem farSet6_congr {σ σ' : ℤ → ZMod 3} {k : ℤ} (h0 : σ k = σ' k) (h1 : σ (k + 1) = σ' (k + 1))
    {P : Finset (ℤ × ℤ)} (hP : P.card = 4) {N : Finset ((ℤ × ℤ) × (ℤ × ℤ))} {F : Finset (Sym2 Atom)}
    (hF : F ∈ FarSet σ k P N 6) : F ∈ FarSet σ' k P N 6 := by
  have hl := farSet6_layers hF hP
  refine ⟨⟨hF.1.1, hF.1.2.1, ?_⟩, hF.2.1, hF.2.2⟩
  intro e he
  have hb := hF.1.2.2 e he
  induction e using Sym2.ind with
  | _ x y =>
    rw [bondS_mk] at hb ⊢
    have lx := hl _ he x (Sym2.mem_mk_left _ _)
    have ly := hl _ he y (Sym2.mem_mk_right _ _)
    have ex : σ x.1 = σ' x.1 := by
      rcases (show x.1 = k ∨ x.1 = k + 1 by omega) with e | e <;> rw [e] <;> assumption
    have ey : σ y.1 = σ' y.1 := by
      rcases (show y.1 = k ∨ y.1 = k + 1 by omega) with e | e <;> rw [e] <;> assumption
    exact (bond_letters ex ey).mp hb

theorem Fc6_congr {σ σ' : ℤ → ZMod 3} {k : ℤ} (h0 : σ k = σ' k) (h1 : σ (k + 1) = σ' (k + 1))
    {P : Finset (ℤ × ℤ)} (hP : P.card = 4) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : Fc σ k P N 6 = Fc σ' k P N 6 := by
  unfold Fc; congr 2; ext F
  exact ⟨farSet6_congr h0 h1 hP, farSet6_congr h0.symm h1.symm hP⟩

theorem Af6_congr {σ σ' : ℤ → ZMod 3} {k : ℤ} (h0 : σ k = σ' k) (h1 : σ (k + 1) = σ' (k + 1)) (c : ℤ × ℤ)
    {P : Finset (ℤ × ℤ)} (hP : P.card = 4) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : Af σ k c P N 6 = Af σ' k c P N 6 := by
  unfold Af; rw [Fc6_congr h0 h1 hP, Fc6_congr h0 h1 (by rw [card_gP]; exact hP)]

theorem Wc6_congr {σ σ' : ℤ → ZMod 3} {k : ℤ} (h0 : σ k = σ' k) (hm : σ (k - 1) = σ' (k - 1)) (v : Atom)
    {P : Finset (ℤ × ℤ)} (hP : P.card = 4) (M : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : Wc σ v k P M 6 = Wc σ' v k P M 6 := by
  rw [Wc_mir, Wc_mir]
  have e0 : mirS σ (-k) = mirS σ' (-k) := by simp [mirS, h0]
  have e1 : mirS σ (-k + 1) = mirS σ' (-k + 1) := by
    simp only [mirS, neg_add, neg_neg]; rw [show k + -1 = k - 1 by ring]; exact hm
  congr 2; ext F
  exact ⟨fun ⟨hF, hv⟩ => ⟨farSet6_congr e0 e1 hP hF, hv⟩, fun ⟨hF, hv⟩ => ⟨farSet6_congr e0.symm e1.symm hP hF, hv⟩⟩

/-- **`G16` sees only the letters of bilayers `k - 1`, `k`, `k + 1`.** -/
theorem G16_congr {σ σ' : ℤ → ZMod 3} {k : ℤ} (hm : σ (k - 1) = σ' (k - 1)) (h0 : σ k = σ' k)
    (h1 : σ (k + 1) = σ' (k + 1)) (c : ℤ × ℤ) (a : Atom) (P : Finset (ℤ × ℤ)) : G16 σ k c a P = G16 σ' k c a P := by
  unfold G16
  apply Finset.sum_congr rfl; intro x _
  split_ifs with hcond
  · rw [hcond.2.1, hcond.2.2, Wc6_congr h0 hm a hcond.1, Af6_congr h0 h1 c hcond.1]
  · rfl

end LoopEqualityProof
