module

public import Mathlib
public import LoopEquality.Split
public import LoopEquality.BSym

@[expose] public section

/-!
# Far linkages on four points are pairs of disjoint arcs

For distinct `a, b, c, d`, the far linkages ending at `{a, b, c, d}` that join `a` to `b` and `c` to `d` correspond
one to one with pairs (arc from `a` to `b`, arc from `c` to `d`) with no atom in common, sizes adding up.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-- The pairing relation of one pair. -/
def pr2 (a b : ℤ × ℤ) : Finset ((ℤ × ℤ) × (ℤ × ℤ)) := ({a, b} : Finset (ℤ × ℤ)) ×ˢ {a, b}

/-- Pairs of far arcs, `a` to `b` and `c` to `d`, with no atom in common and `s` edges in all. -/
def TwoArcs (τ : ℤ → ZMod 3) (k : ℤ) (a b c d : ℤ × ℤ) (s : ℕ) : Set (Finset (Sym2 Atom) × Finset (Sym2 Atom)) :=
  {x | FarL τ k {a, b} x.1 ∧ pairF k x.1 {a, b} = pr2 a b ∧ FarL τ k {c, d} x.2 ∧ pairF k x.2 {c, d} = pr2 c d ∧
    x.1.card + x.2.card = s ∧ AtomDisj x.1 x.2}

theorem conn_last {L : Finset (Sym2 Atom)} {x y : Atom} (h : Conn L x y) (hxy : x ≠ y) : 0 < degS L y := by
  induction h with
  | refl => exact absurd rfl hxy
  | @tail c d _ hcd _ => exact degS_pos_of' hcd.1 (Sym2.mem_mk_right c d)

theorem conn_of_pairF {k : ℤ} {F : Finset (Sym2 Atom)} {Q : Finset (ℤ × ℤ)} {p q : ℤ × ℤ}
    (h : (p, q) ∈ pairF k F Q) : Conn F (upA k p) (upA k q) := (Finset.mem_filter.mp h).2

theorem pairF_full {k : ℤ} {F : Finset (Sym2 Atom)} {a b : ℤ × ℤ} (h : Conn F (upA k a) (upA k b)) :
    pairF k F {a, b} = pr2 a b := by
  ext ⟨p, q⟩
  simp only [pairF, pr2, Finset.mem_filter, Finset.mem_product, Finset.mem_insert, Finset.mem_singleton]
  constructor
  · rintro ⟨h1, -⟩; exact h1
  · rintro ⟨hp, hq⟩
    refine ⟨⟨hp, hq⟩, ?_⟩
    rcases hp with rfl | rfl <;> rcases hq with rfl | rfl
    · exact Relation.ReflTransGen.refl
    · exact h
    · exact conn_symm h
    · exact Relation.ReflTransGen.refl

theorem atomDisj_symm {L₁ L₂ : Finset (Sym2 Atom)} (h : AtomDisj L₁ L₂) : AtomDisj L₂ L₁ := fun w => (h w).symm

/-- In a union of two linkages with no common atom, the component of an end of the first is the first. -/
theorem compPart_union {L₁ L₂ : Finset (Sym2 Atom)} {x y : Atom} (h1 : IsLinkageOn L₁ {x, y}) (hxy : Conn L₁ x y)
    (hd : AtomDisj L₁ L₂) : compPart (L₁ ∪ L₂) x = L₁ := by
  have hx1 : degS L₁ x = 1 := h1.1 x (by simp)
  have hx2 : degS L₂ x = 0 := (hd x).resolve_left (by omega)
  ext e
  simp only [compPart, Finset.mem_filter, Finset.mem_union]
  constructor
  · rintro ⟨he, w, hw, hc⟩
    have hc1 := conn_union_left hd hx2 hc
    rcases he with he | he
    · exact he
    · exfalso
      have hw2 : 0 < degS L₂ w := degS_pos_of' he hw
      by_cases hxw : x = w
      · rw [← hxw] at hw2; omega
      · have := conn_last hc1 hxw
        rcases hd w with z | z <;> omega
  · intro he
    refine ⟨Or.inl he, ?_⟩
    obtain ⟨w, hw⟩ := exists_mem_sym2 e
    obtain ⟨b, hb, hwb⟩ := reaches_end h1 he hw
    refine ⟨w, hw, conn_mono Finset.subset_union_left ?_⟩
    rcases Finset.mem_insert.mp hb with rfl | hb
    · exact conn_symm hwb
    · rw [Finset.mem_singleton.mp hb] at hwb; exact hxy.trans (conn_symm hwb)

theorem restPart_union {L₁ L₂ : Finset (Sym2 Atom)} {x y : Atom} (h1 : IsLinkageOn L₁ {x, y}) (hxy : Conn L₁ x y)
    (hd : AtomDisj L₁ L₂) : restPart (L₁ ∪ L₂) x = L₂ := by
  have hc := compPart_union h1 hxy hd
  have hu := compPart_union_restPart (L₁ ∪ L₂) x
  have hdis := disjoint_compPart_restPart (L₁ ∪ L₂) x
  have hD := disjoint_of_atomDisj hd
  rw [hc] at hu hdis
  ext e
  constructor
  · intro he
    have : e ∈ L₁ ∪ L₂ := hu ▸ Finset.mem_union_right _ he
    rcases Finset.mem_union.mp this with h | h
    · exact absurd he (Finset.disjoint_left.mp hdis h)
    · exact h
  · intro he
    have : e ∈ L₁ ∪ restPart (L₁ ∪ L₂) x := hu.symm ▸ Finset.mem_union_right _ he
    rcases Finset.mem_union.mp this with h | h
    · exact absurd he (Finset.disjoint_left.mp hD h)
    · exact h

section Four

variable {τ : ℤ → ZMod 3} {k : ℤ} {a b c d : ℤ × ℤ}

theorem image_pair (k : ℤ) (a b : ℤ × ℤ) : ({a, b} : Finset (ℤ × ℤ)).image (upA k) = {upA k a, upA k b} := by
  simp [Finset.image_insert]

theorem quad_eq (a b c d : ℤ × ℤ) : ({a, b, c, d} : Finset (ℤ × ℤ)) = {a, b} ∪ {c, d} := by
  ext x; simp only [Finset.mem_insert, Finset.mem_singleton, Finset.mem_union]; tauto

theorem upA_ne {k : ℤ} {p q : ℤ × ℤ} (h : p ≠ q) : upA k p ≠ upA k q := fun e => h (upA_inj e)

/-- In the union of two arcs with no common atom, a path from an end of the first stays in the first. -/
theorem union_conn_iff {x : Finset (Sym2 Atom) × Finset (Sym2 Atom)} (hx : x ∈ TwoArcs τ k a b c d s)
    (hdis : ∀ p ∈ ({a, b} : Finset (ℤ × ℤ)), ∀ q ∈ ({c, d} : Finset (ℤ × ℤ)), p ≠ q)
    {p q : ℤ × ℤ} (hp : p ∈ ({a, b, c, d} : Finset (ℤ × ℤ))) (hq : q ∈ ({a, b, c, d} : Finset (ℤ × ℤ))) :
    Conn (x.1 ∪ x.2) (upA k p) (upA k q) ↔
      (p ∈ ({a, b} : Finset (ℤ × ℤ)) ∧ q ∈ ({a, b} : Finset (ℤ × ℤ))) ∨
      (p ∈ ({c, d} : Finset (ℤ × ℤ)) ∧ q ∈ ({c, d} : Finset (ℤ × ℤ))) := by
  obtain ⟨h1, hp1, h2, hp2, -, hd⟩ := hx
  have e1 : ∀ r ∈ ({a, b} : Finset (ℤ × ℤ)), degS x.1 (upA k r) = 1 := fun r hr =>
    h1.1.1 _ (Finset.mem_image_of_mem _ hr)
  have e2 : ∀ r ∈ ({c, d} : Finset (ℤ × ℤ)), degS x.2 (upA k r) = 1 := fun r hr =>
    h2.1.1 _ (Finset.mem_image_of_mem _ hr)
  have z1 : ∀ r ∈ ({a, b} : Finset (ℤ × ℤ)), degS x.2 (upA k r) = 0 := fun r hr =>
    (hd _).resolve_left (by rw [e1 r hr]; omega)
  have z2 : ∀ r ∈ ({c, d} : Finset (ℤ × ℤ)), degS x.1 (upA k r) = 0 := fun r hr =>
    (hd _).resolve_right (by rw [e2 r hr]; omega)
  rw [quad_eq] at hp hq
  constructor
  · intro hc
    rcases Finset.mem_union.mp hp with hpa | hpc
    · have hc1 := conn_union_left hd (z1 p hpa) hc
      rcases Finset.mem_union.mp hq with hqa | hqc
      · exact Or.inl ⟨hpa, hqa⟩
      · exfalso
        have := conn_last hc1 (upA_ne (hdis p hpa q hqc)); rw [z2 q hqc] at this; omega
    · rw [Finset.union_comm] at hc
      have hc2 := conn_union_left (atomDisj_symm hd) (z2 p hpc) hc
      rcases Finset.mem_union.mp hq with hqa | hqc
      · exfalso
        have := conn_last hc2 (upA_ne (fun e => hdis q hqa p hpc e.symm)); rw [z1 q hqa] at this; omega
      · exact Or.inr ⟨hpc, hqc⟩
  · rintro (⟨hpa, hqa⟩ | ⟨hpc, hqc⟩)
    · have : (p, q) ∈ pairF k x.1 {a, b} := by rw [hp1]; exact Finset.mem_product.mpr ⟨hpa, hqa⟩
      exact conn_mono Finset.subset_union_left (conn_of_pairF this)
    · have : (p, q) ∈ pairF k x.2 {c, d} := by rw [hp2]; exact Finset.mem_product.mpr ⟨hpc, hqc⟩
      exact conn_mono Finset.subset_union_right (conn_of_pairF this)

/-- **Far linkages on four points, paired `a b | c d`, are pairs of disjoint arcs.** -/
theorem fc_four (hdis : ∀ p ∈ ({a, b} : Finset (ℤ × ℤ)), ∀ q ∈ ({c, d} : Finset (ℤ × ℤ)), p ≠ q) (s : ℕ) :
    Fc τ k {a, b, c, d} (pr2 a b ∪ pr2 c d) s = (TwoArcs τ k a b c d s).ncard := by
  unfold Fc
  congr 1
  symm
  apply Set.ncard_congr (fun x _ => x.1 ∪ x.2)
  · intro x hx
    obtain ⟨h1, hp1, h2, hp2, hs, hd⟩ := hx
    have hD := disjoint_of_atomDisj hd
    refine ⟨⟨?_, ?_, ?_⟩, ?_, ?_⟩
    · rw [quad_eq, Finset.image_union]; exact linkage_union h1.1 h2.1 hd
    · intro e he w hw
      rcases Finset.mem_union.mp he with h | h
      · exact h1.2.1 e h w hw
      · exact h2.2.1 e h w hw
    · intro e he
      rcases Finset.mem_union.mp he with h | h
      · exact h1.2.2 e h
      · exact h2.2.2 e h
    · rw [Finset.card_union_of_disjoint hD]; exact hs
    · ext ⟨p, q⟩
      simp only [pairF, Finset.mem_filter, Finset.mem_product, pr2, Finset.mem_union]
      constructor
      · rintro ⟨⟨hp, hq⟩, hc⟩
        exact (union_conn_iff ⟨h1, hp1, h2, hp2, hs, hd⟩ hdis hp hq).mp hc
      · intro h
        have hp : p ∈ ({a, b, c, d} : Finset (ℤ × ℤ)) := by
          rw [quad_eq]; rcases h with ⟨h, -⟩ | ⟨h, -⟩
          · exact Finset.mem_union_left _ h
          · exact Finset.mem_union_right _ h
        have hq : q ∈ ({a, b, c, d} : Finset (ℤ × ℤ)) := by
          rw [quad_eq]; rcases h with ⟨-, h⟩ | ⟨-, h⟩
          · exact Finset.mem_union_left _ h
          · exact Finset.mem_union_right _ h
        exact ⟨⟨hp, hq⟩, (union_conn_iff ⟨h1, hp1, h2, hp2, hs, hd⟩ hdis hp hq).mpr h⟩
  · intro x y hx hy hxy
    have hxl : IsLinkageOn x.1 {upA k a, upA k b} := by rw [← image_pair]; exact hx.1.1
    have hyl : IsLinkageOn y.1 {upA k a, upA k b} := by rw [← image_pair]; exact hy.1.1
    have hxc : Conn x.1 (upA k a) (upA k b) := conn_of_pairF (by rw [hx.2.1]; simp [pr2])
    have hyc : Conn y.1 (upA k a) (upA k b) := conn_of_pairF (by rw [hy.2.1]; simp [pr2])
    have c1 := compPart_union hxl hxc hx.2.2.2.2.2
    have c2 := compPart_union hyl hyc hy.2.2.2.2.2
    have r1 := restPart_union hxl hxc hx.2.2.2.2.2
    have r2 := restPart_union hyl hyc hy.2.2.2.2.2
    change x.1 ∪ x.2 = y.1 ∪ y.2 at hxy
    rw [hxy] at c1 r1
    exact Prod.ext (c1.symm.trans c2) (r1.symm.trans r2)
  · intro F hF
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
    refine ⟨(compPart F x₀, restPart F x₀), ⟨⟨?_, ?_, ?_⟩, ?_, ⟨?_, ?_, ?_⟩, ?_, ?_, ?_⟩, ?_⟩
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
    · exact compPart_union_restPart F x₀

/-- The same correspondence, with any condition `Q` on the linkage (read on the union of the two arcs). -/
theorem fc_four_pred (hdis : ∀ p ∈ ({a, b} : Finset (ℤ × ℤ)), ∀ q ∈ ({c, d} : Finset (ℤ × ℤ)), p ≠ q) (s : ℕ)
    (Q : Finset (Sym2 Atom) → Prop) :
    ({F | F ∈ FarSet τ k {a, b, c, d} (pr2 a b ∪ pr2 c d) s ∧ Q F} : Set (Finset (Sym2 Atom))).ncard =
      ({x | x ∈ TwoArcs τ k a b c d s ∧ Q (x.1 ∪ x.2)} : Set (Finset (Sym2 Atom) × Finset (Sym2 Atom))).ncard := by
  symm
  apply Set.ncard_congr (fun x _ => x.1 ∪ x.2)
  · rintro x ⟨hx, hQ⟩
    refine ⟨?_, hQ⟩
    obtain ⟨h1, hp1, h2, hp2, hs, hd⟩ := hx
    have hD := disjoint_of_atomDisj hd
    refine ⟨⟨?_, ?_, ?_⟩, ?_, ?_⟩
    · rw [quad_eq, Finset.image_union]; exact linkage_union h1.1 h2.1 hd
    · intro e he w hw
      rcases Finset.mem_union.mp he with h | h
      · exact h1.2.1 e h w hw
      · exact h2.2.1 e h w hw
    · intro e he
      rcases Finset.mem_union.mp he with h | h
      · exact h1.2.2 e h
      · exact h2.2.2 e h
    · rw [Finset.card_union_of_disjoint hD]; exact hs
    · ext ⟨p, q⟩
      simp only [pairF, Finset.mem_filter, Finset.mem_product, pr2, Finset.mem_union]
      constructor
      · rintro ⟨⟨hp, hq⟩, hc⟩
        exact (union_conn_iff ⟨h1, hp1, h2, hp2, hs, hd⟩ hdis hp hq).mp hc
      · intro h
        have hp : p ∈ ({a, b, c, d} : Finset (ℤ × ℤ)) := by
          rw [quad_eq]; rcases h with ⟨h, -⟩ | ⟨h, -⟩
          · exact Finset.mem_union_left _ h
          · exact Finset.mem_union_right _ h
        have hq : q ∈ ({a, b, c, d} : Finset (ℤ × ℤ)) := by
          rw [quad_eq]; rcases h with ⟨-, h⟩ | ⟨-, h⟩
          · exact Finset.mem_union_left _ h
          · exact Finset.mem_union_right _ h
        exact ⟨⟨hp, hq⟩, (union_conn_iff ⟨h1, hp1, h2, hp2, hs, hd⟩ hdis hp hq).mpr h⟩
  · rintro x y ⟨hx, -⟩ ⟨hy, -⟩ hxy
    have hxl : IsLinkageOn x.1 {upA k a, upA k b} := by rw [← image_pair]; exact hx.1.1
    have hyl : IsLinkageOn y.1 {upA k a, upA k b} := by rw [← image_pair]; exact hy.1.1
    have hxc : Conn x.1 (upA k a) (upA k b) := conn_of_pairF (by rw [hx.2.1]; simp [pr2])
    have hyc : Conn y.1 (upA k a) (upA k b) := conn_of_pairF (by rw [hy.2.1]; simp [pr2])
    have c1 := compPart_union hxl hxc hx.2.2.2.2.2
    have c2 := compPart_union hyl hyc hy.2.2.2.2.2
    have r1 := restPart_union hxl hxc hx.2.2.2.2.2
    have r2 := restPart_union hyl hyc hy.2.2.2.2.2
    change x.1 ∪ x.2 = y.1 ∪ y.2 at hxy
    rw [hxy] at c1 r1
    exact Prod.ext (c1.symm.trans c2) (r1.symm.trans r2)
  · rintro F ⟨hF, hQ⟩
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
    refine ⟨(compPart F x₀, restPart F x₀), ⟨⟨⟨?_, ?_, ?_⟩, ?_, ⟨?_, ?_, ?_⟩, ?_, ?_, ?_⟩, by
      show Q (compPart F x₀ ∪ restPart F x₀); rw [compPart_union_restPart]; exact hQ⟩, ?_⟩
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
    · exact compPart_union_restPart F x₀

end Four

end LoopEqualityProof
