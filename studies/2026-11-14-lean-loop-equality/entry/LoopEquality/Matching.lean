module

public import Mathlib
public import LoopEquality.FourPoint

@[expose] public section

/-!
# A linkage with four ends pairs them by a matching

In a linkage on four ends, each end is joined to exactly one other end: the pairing relation of a far linkage on four
crossing points is `pr2 a b ∪ pr2 c d` for a split `{a, b} | {c, d}` of them.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

theorem linkage_deg_le_two {L : Finset (Sym2 Atom)} {B : Finset Atom} (hL : IsLinkageOn L B) (w : Atom) :
    degS L w ≤ 2 := by
  by_cases hw : w ∈ B
  · rw [hL.1 w hw]; omega
  · rcases hL.2.1 w hw with h | h <;> omega

theorem deg_one_mem {L : Finset (Sym2 Atom)} {B : Finset Atom} (hL : IsLinkageOn L B) {w : Atom}
    (h : degS L w = 1) : w ∈ B := by
  by_contra hw; rcases hL.2.1 w hw with h' | h' <;> omega

/-- **Four ends are paired.** -/
theorem linkage_four {L : Finset (Sym2 Atom)} {B : Finset Atom} (hL : IsLinkageOn L B) (hB : B.card = 4)
    {x : Atom} (hx : x ∈ B) :
    ∃ y z w, B = {x, y, z, w} ∧ y ≠ x ∧ z ≠ x ∧ w ≠ x ∧ y ≠ z ∧ y ≠ w ∧ z ≠ w ∧
      Conn L x y ∧ Conn L z w ∧ ¬ Conn L x z ∧ ¬ Conn L x w ∧
      ∀ u ∈ B, ∀ u' ∈ B, (Conn L u u' ↔ (Conn L x u ↔ Conn L x u')) := by
  have hle := linkage_deg_le_two hL
  have hnd := hL.2.2.2
  have d1 : ∀ u ∈ B, degS L u = 1 := hL.1
  obtain ⟨y, hyx, hy1, hxy⟩ := partner_exists L hnd hle (d1 x hx)
  have hyB := deg_one_mem hL hy1
  obtain ⟨z, hzB, hzx, hzy⟩ : ∃ z ∈ B, z ≠ x ∧ z ≠ y := by
    by_contra hno; push Not at hno
    have : B ⊆ {x, y} := fun u hu => by
      by_cases h1 : u = x
      · simp [h1]
      · simp [hno u hu h1]
    have := Finset.card_le_card this
    have := Finset.card_le_two (a := x) (b := y); omega
  obtain ⟨w, hwz, hw1, hzw⟩ := partner_exists L hnd hle (d1 z hzB)
  have hwB := deg_one_mem hL hw1
  -- x's only partner is y
  have px : ∀ u, degS L u = 1 → u ≠ x → Conn L x u → u = y := fun u hu hux hc =>
    (partner_unique L hnd hle (d1 x hx) hu hy1 hux hyx hc hxy)
  have hnxz : ¬ Conn L x z := fun h => hzy (px z (d1 z hzB) hzx h)
  have hwx : w ≠ x := fun h => hnxz (conn_symm (h ▸ hzw))
  have hwy : w ≠ y := fun h => hnxz (hxy.trans (conn_symm (h ▸ hzw)))
  have hnxw : ¬ Conn L x w := fun h => hwy (px w hw1 hwx h)
  have hBeq : B = {x, y, z, w} := by
    symm; apply Finset.eq_of_subset_of_card_le
    · intro u hu; simp only [Finset.mem_insert, Finset.mem_singleton] at hu
      rcases hu with rfl | rfl | rfl | rfl <;> assumption
    · rw [hB, Finset.card_insert_of_notMem (by simp [hyx.symm, hzx.symm, hwx.symm]),
        Finset.card_insert_of_notMem (by simp [hzy.symm, hwy.symm]),
        Finset.card_insert_of_notMem (by simp [hwz.symm]), Finset.card_singleton]
  refine ⟨y, z, w, hBeq, hyx, hzx, hwx, hzy.symm, hwy.symm, hwz.symm, hxy, hzw, hnxz, hnxw, ?_⟩
  -- the class of x is {x, y}; the class of z is {z, w}
  have cls : ∀ u ∈ B, (Conn L x u ∨ Conn L z u) ∧ ¬ (Conn L x u ∧ Conn L z u) := by
    intro u hu
    rw [hBeq] at hu
    simp only [Finset.mem_insert, Finset.mem_singleton] at hu
    refine ⟨?_, fun ⟨h1, h2⟩ => hnxz (h1.trans (conn_symm h2))⟩
    rcases hu with rfl | rfl | rfl | rfl
    · exact Or.inl Relation.ReflTransGen.refl
    · exact Or.inl hxy
    · exact Or.inr Relation.ReflTransGen.refl
    · exact Or.inr hzw
  intro u hu u' hu'
  obtain ⟨c1, n1⟩ := cls u hu
  obtain ⟨c2, n2⟩ := cls u' hu'
  constructor
  · intro h
    exact ⟨fun hu1 => hu1.trans h, fun hu2 => hu2.trans (conn_symm h)⟩
  · intro h
    rcases c1 with h1 | h1
    · exact (conn_symm h1).trans (h.mp h1)
    · have : ¬ Conn L x u := fun hx' => n1 ⟨hx', h1⟩
      have : ¬ Conn L x u' := fun hx' => this (h.mpr hx')
      rcases c2 with h2 | h2
      · exact absurd h2 this
      · exact (conn_symm h1).trans h2

/-- **The pairing of a far linkage on four crossing points is a matching.** -/
theorem pairF_four {τ : ℤ → ZMod 3} {k : ℤ} {P : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)}
    (hF : FarL τ k P F) (hP : P.card = 4) {a : ℤ × ℤ} (ha : a ∈ P) :
    ∃ b c d, P = {a, b, c, d} ∧ (∀ p ∈ ({a, b} : Finset (ℤ × ℤ)), ∀ q ∈ ({c, d} : Finset (ℤ × ℤ)), p ≠ q) ∧
      a ≠ b ∧ c ≠ d ∧ pairF k F P = pr2 a b ∪ pr2 c d := by
  have hinj : Function.Injective (upA k) := fun p q h => upA_inj h
  have hB : (P.image (upA k)).card = 4 := by rw [Finset.card_image_of_injective _ hinj, hP]
  obtain ⟨y, z, w, hBe, hyx, hzx, hwx, hyz, hyw, hzw, hxy, hzw', hnz, hnw, hcl⟩ :=
    linkage_four hF.1 hB (Finset.mem_image_of_mem _ ha)
  have mem : ∀ u ∈ ({upA k a, y, z, w} : Finset Atom), ∃ p ∈ P, upA k p = u := fun u hu => by
    rw [← hBe] at hu; exact Finset.mem_image.mp hu
  obtain ⟨b, hb, rfl⟩ := mem y (by simp)
  obtain ⟨c, hc, rfl⟩ := mem z (by simp)
  obtain ⟨d, hd, rfl⟩ := mem w (by simp)
  have ne : ∀ {p q : ℤ × ℤ}, upA k p ≠ upA k q → p ≠ q := fun h e => h (e ▸ rfl)
  have hPe : P = {a, b, c, d} := by
    apply Finset.image_injective hinj
    rw [hBe]; simp [Finset.image_insert]
  have hdis : ∀ p ∈ ({a, b} : Finset (ℤ × ℤ)), ∀ q ∈ ({c, d} : Finset (ℤ × ℤ)), p ≠ q := by
    intro p hp q hq
    simp only [Finset.mem_insert, Finset.mem_singleton] at hp hq
    rcases hp with rfl | rfl <;> rcases hq with rfl | rfl
    · exact ne hzx.symm
    · exact ne hwx.symm
    · exact ne hyz
    · exact ne hyw
  refine ⟨b, c, d, hPe, hdis, ne hyx.symm, ne hzw, ?_⟩
  have hPu : ∀ p, p ∈ P ↔ (p ∈ ({a, b} : Finset (ℤ × ℤ)) ∨ p ∈ ({c, d} : Finset (ℤ × ℤ))) := fun p => by
    rw [hPe, quad_eq, Finset.mem_union]
  have side : ∀ p ∈ P, (Conn F (upA k a) (upA k p) ↔ p ∈ ({a, b} : Finset (ℤ × ℤ))) := by
    intro p hp
    rw [hPe] at hp
    simp only [Finset.mem_insert, Finset.mem_singleton] at hp
    rcases hp with rfl | rfl | rfl | rfl
    · simp only [Finset.mem_insert, true_or, iff_true]; exact Relation.ReflTransGen.refl
    · simp only [Finset.mem_insert, Finset.mem_singleton, or_true, iff_true]; exact hxy
    · simp only [hnz, false_iff]; exact fun h => hdis _ h _ (by simp) rfl
    · simp only [hnw, false_iff]; exact fun h => hdis _ h _ (by simp) rfl
  ext ⟨p, q⟩
  simp only [pairF, pr2, Finset.mem_filter, Finset.mem_product, Finset.mem_union]
  constructor
  · rintro ⟨⟨hp, hq⟩, h⟩
    have h' := (hcl _ (Finset.mem_image_of_mem _ hp) _ (Finset.mem_image_of_mem _ hq)).mp h
    rw [side p hp, side q hq] at h'
    rcases (hPu p).mp hp with hp1 | hp1
    · exact Or.inl ⟨hp1, h'.mp hp1⟩
    · have hpn : p ∉ ({a, b} : Finset (ℤ × ℤ)) := fun h0 => hdis p h0 p hp1 rfl
      rcases (hPu q).mp hq with hq1 | hq1
      · exact absurd (h'.mpr hq1) hpn
      · exact Or.inr ⟨hp1, hq1⟩
  · intro h
    have hpq : p ∈ P ∧ q ∈ P := by
      rcases h with ⟨hp, hq⟩ | ⟨hp, hq⟩
      · exact ⟨(hPu p).mpr (Or.inl hp), (hPu q).mpr (Or.inl hq)⟩
      · exact ⟨(hPu p).mpr (Or.inr hp), (hPu q).mpr (Or.inr hq)⟩
    refine ⟨hpq, (hcl _ (Finset.mem_image_of_mem _ hpq.1) _ (Finset.mem_image_of_mem _ hpq.2)).mpr ?_⟩
    rw [side p hpq.1, side q hpq.2]
    rcases h with ⟨hp, hq⟩ | ⟨hp, hq⟩
    · exact ⟨fun _ => hq, fun _ => hp⟩
    · exact ⟨fun h0 => absurd rfl (hdis p h0 p hp), fun h0 => absurd rfl (hdis q h0 q hq)⟩

end LoopEqualityProof
