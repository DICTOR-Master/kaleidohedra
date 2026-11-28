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
public import LoopEquality.Lemma7
public import LoopEquality.SingleArc

@[expose] public section

/-!
# Linkages of minimal size (Lean paper, L5, far side): structure

A far linkage ending at the upper atoms of `Q` with exactly `|Q|` edges:
* `edge_has_end`: every edge contains an end;
* `far_edge_shape`: an edge at the end `upA k p` is `s(upA k p, (k + 1, m, 0))` with `m - p ∈ shortVecs`;
* the other atoms (middles) are lower atoms of bilayer `k + 1`, each of degree 2.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

theorem edge_has_end {L : Finset (Sym2 Atom)} {B : Finset Atom} (hL : IsLinkageOn L B)
    (hno : ∀ e ∈ L, ∀ a ∈ B, ∀ b ∈ B, a ∈ e → b ∈ e → a = b) (hcard : L.card = B.card) :
    ∀ e ∈ L, ∃ b ∈ B, b ∈ e := by
  have hone : ∀ b ∈ B, ∃ e ∈ L, b ∈ e := fun b hb => by
    have := hL.1 b hb
    obtain ⟨e, he⟩ := Finset.card_pos.mp (by unfold degS at this; omega : 0 < (L.filter (fun e => b ∈ e)).card)
    exact ⟨e, (Finset.mem_filter.mp he).1, (Finset.mem_filter.mp he).2⟩
  choose! f hfL hfb using hone
  have hinj : Set.InjOn f B := fun a ha b hb hab => hno (f a) (hfL a ha) a ha b hb (hfb a ha) (hab ▸ hfb b hb)
  have himg : B.image f = L := by
    apply Finset.eq_of_subset_of_card_le
    · intro e he; obtain ⟨b, hb, rfl⟩ := Finset.mem_image.mp he; exact hfL b hb
    · rw [Finset.card_image_of_injOn hinj, hcard]
  intro e he
  rw [← himg] at he
  obtain ⟨b, hb, rfl⟩ := Finset.mem_image.mp he
  exact ⟨b, hb, hfb b hb⟩

theorem far_bond_shape {τ : ℤ → ZMod 3} {k : ℤ} {p : ℤ × ℤ} {w : Atom} (hb : Bond τ (upA k p) w)
    (hw : IsFar k w) : ∃ m : ℤ × ℤ, w = (k + 1, m, 0) ∧ m - p ∈ shortVecs := by
  obtain ⟨-, -, h⟩ := hb
  obtain ⟨j, m, u⟩ := w
  unfold upA at h
  simp only at h
  rcases h with ⟨h1, h2, h3⟩ | ⟨h1, -, h3, h4⟩ | ⟨-, -, h3, -⟩
  · subst h1; subst h2
    unfold IsFar at hw; simp only at hw
    have : u = 1 := by simpa using hw
    exact absurd this.symm h3
  · exact ⟨m, by rw [h1, h3], h4⟩
  · exact absurd h3 (by decide)

/-- A far linkage of `G τ` ending at the upper atoms of `Q` with exactly `|Q|` edges. -/
def MinF (τ : ℤ → ZMod 3) (k : ℤ) (Q : Finset (ℤ × ℤ)) (F : Finset (Sym2 Atom)) : Prop :=
  FarL τ k Q F ∧ F.card = Q.card

theorem minF_no2 {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : FarL τ k Q F) :
    ∀ e ∈ F, ∀ a ∈ Q.image (upA k), ∀ b ∈ Q.image (upA k), a ∈ e → b ∈ e → a = b := by
  intro e he a ha b hb hae hbe
  obtain ⟨p, -, rfl⟩ := Finset.mem_image.mp ha; obtain ⟨q, -, rfl⟩ := Finset.mem_image.mp hb
  by_contra hne
  have hbd := hF.2.2 e he
  induction e using Sym2.ind with
  | _ x y =>
    rw [bondS_mk] at hbd
    rcases Sym2.mem_iff.mp hae with rfl | rfl <;> rcases Sym2.mem_iff.mp hbe with h | h
    · exact hne h.symm
    · subst h; exact not_bond_upA hbd
    · subst h; exact not_bond_upA hbd
    · exact hne h.symm

/-- Every edge of a minimal far linkage is `s(upA k p, (k + 1, m, 0))` for an end point `p ∈ Q`. -/
theorem minF_edge {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : MinF τ k Q F)
    {e : Sym2 Atom} (he : e ∈ F) : ∃ p ∈ Q, ∃ m : ℤ × ℤ, e = s(upA k p, (k + 1, m, 0)) ∧ m - p ∈ shortVecs := by
  have hcard : F.card = (Q.image (upA k)).card := by
    rw [hF.2, Finset.card_image_of_injective _ (fun a b h => upA_inj h)]
  obtain ⟨b, hb, hbe⟩ := edge_has_end hF.1.1 (minF_no2 hF.1) hcard e he
  obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp hb
  have hbd := hF.1.2.2 e he
  have hfs := hF.1.2.1 e he
  induction e using Sym2.ind with
  | _ x y =>
    rw [bondS_mk] at hbd
    rcases Sym2.mem_iff.mp hbe with rfl | rfl
    · obtain ⟨m, rfl, hm⟩ := far_bond_shape hbd (hfs y (Sym2.mem_mk_right _ _))
      exact ⟨p, hp, m, rfl, hm⟩
    · obtain ⟨m, rfl, hm⟩ := far_bond_shape (bond_symm hbd) (hfs x (Sym2.mem_mk_left _ _))
      exact ⟨p, hp, m, Sym2.eq_swap, hm⟩

theorem mid_not_end {k : ℤ} {Q : Finset (ℤ × ℤ)} (m : ℤ × ℤ) : ((k + 1, m, 0) : Atom) ∉ Q.image (upA k) := by
  intro h; obtain ⟨p, -, hp⟩ := Finset.mem_image.mp h
  have := congrArg (fun a : Atom => a.1) hp; simp [upA] at this

/-- A middle atom of a minimal far linkage has exactly two edges, to two different ends. -/
theorem minF_mid {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : MinF τ k Q F)
    {m : ℤ × ℤ} (hm : ((k + 1, m, 0) : Atom) ∈ atomsOf F) :
    ∃ p ∈ Q, ∃ q ∈ Q, p ≠ q ∧ F.filter (fun e => ((k + 1, m, 0) : Atom) ∈ e) =
      {s(upA k p, (k + 1, m, 0)), s(upA k q, (k + 1, m, 0))} := by
  set w : Atom := (k + 1, m, 0)
  have hdeg : degS F w = 2 := by
    rcases hF.1.1.2.1 w (mid_not_end m) with h | h
    · obtain ⟨e, he, hwe⟩ := mem_atomsOf.mp hm
      have : 0 < degS F w := Finset.card_pos.mpr ⟨e, Finset.mem_filter.mpr ⟨he, hwe⟩⟩
      omega
    · exact h
  obtain ⟨e1, e2, hne, heq⟩ := Finset.card_eq_two.mp hdeg
  have h1 : e1 ∈ F.filter (fun e => w ∈ e) := by rw [heq]; simp
  have h2 : e2 ∈ F.filter (fun e => w ∈ e) := by rw [heq]; simp
  obtain ⟨p, hp, m1, he1, -⟩ := minF_edge hF (Finset.mem_filter.mp h1).1
  obtain ⟨q, hq, m2, he2, -⟩ := minF_edge hF (Finset.mem_filter.mp h2).1
  have hw1 := (Finset.mem_filter.mp h1).2; have hw2 := (Finset.mem_filter.mp h2).2
  rw [he1, Sym2.mem_iff] at hw1; rw [he2, Sym2.mem_iff] at hw2
  have hm1 : m1 = m := by
    rcases hw1 with h | h
    · have := congrArg (fun a : Atom => a.1) h; simp [upA, w] at this
    · have := congrArg (fun a : Atom => a.2.1) h; simpa [w] using this.symm
  have hm2 : m2 = m := by
    rcases hw2 with h | h
    · have := congrArg (fun a : Atom => a.1) h; simp [upA, w] at this
    · have := congrArg (fun a : Atom => a.2.1) h; simpa [w] using this.symm
  subst hm1; subst hm2
  refine ⟨p, hp, q, hq, fun hpq => hne (by rw [he1, he2, hpq]), by rw [heq, he1, he2]⟩

/-! ## The swap of the middle atoms -/

/-- The sum of the positions of the neighbours of `w` in `F`. -/
noncomputable def nbSum (F : Finset (Sym2 Atom)) (w : Atom) : ℤ × ℤ :=
  ∑ a ∈ (atomsOf F).filter (fun a => s(a, w) ∈ F), a.2.1

/-- Each middle atom `(k + 1, m, 0)` moves to `(k + 1, p + q - m, 0)`, the centre of the other triangle on its two
ends `p, q`; the ends stay. -/
noncomputable def swapAt (k : ℤ) (F : Finset (Sym2 Atom)) (a : Atom) : Atom :=
  if a.1 = k + 1 ∧ a.2.2 = 0 then (k + 1, nbSum F a - a.2.1, 0) else a

noncomputable def swapF (k : ℤ) (F : Finset (Sym2 Atom)) : Finset (Sym2 Atom) := F.image (Sym2.map (swapAt k F))

theorem swapAt_upA (k : ℤ) (F : Finset (Sym2 Atom)) (p : ℤ × ℤ) : swapAt k F (upA k p) = upA k p := by
  unfold swapAt upA; simp

theorem minF_nb {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : MinF τ k Q F)
    {m p q : ℤ × ℤ} (hpq : p ≠ q)
    (hfil : F.filter (fun e => ((k + 1, m, 0) : Atom) ∈ e) = {s(upA k p, (k + 1, m, 0)), s(upA k q, (k + 1, m, 0))}) :
    nbSum F (k + 1, m, 0) = p + q := by
  set w : Atom := (k + 1, m, 0)
  have hp : s(upA k p, w) ∈ F := (Finset.mem_filter.mp (by rw [hfil]; simp : s(upA k p, w) ∈ F.filter (fun e => w ∈ e))).1
  have hq : s(upA k q, w) ∈ F := (Finset.mem_filter.mp (by rw [hfil]; simp : s(upA k q, w) ∈ F.filter (fun e => w ∈ e))).1
  have hset : (atomsOf F).filter (fun a => s(a, w) ∈ F) = {upA k p, upA k q} := by
    ext a
    simp only [Finset.mem_filter, Finset.mem_insert, Finset.mem_singleton]
    constructor
    · rintro ⟨-, ha⟩
      have : s(a, w) ∈ F.filter (fun e => w ∈ e) := Finset.mem_filter.mpr ⟨ha, Sym2.mem_mk_right _ _⟩
      rw [hfil] at this
      simp only [Finset.mem_insert, Finset.mem_singleton] at this
      rcases this with h | h
      · left; rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨h1, h2⟩
        · exact h1
        · exact absurd h2 (fun h => by have := congrArg (fun a : Atom => a.1) h; simp [w, upA] at this)
      · right; rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨h1, h2⟩
        · exact h1
        · exact absurd h2 (fun h => by have := congrArg (fun a : Atom => a.1) h; simp [w, upA] at this)
    · rintro (rfl | rfl)
      · exact ⟨mem_atomsOf.mpr ⟨_, hp, Sym2.mem_mk_left _ _⟩, hp⟩
      · exact ⟨mem_atomsOf.mpr ⟨_, hq, Sym2.mem_mk_left _ _⟩, hq⟩
  unfold nbSum
  rw [hset, Finset.sum_pair (fun h => hpq (upA_inj h))]
  rfl

theorem three_short (r : ZMod 3) :
    (shortVecs.filter (fun d : ℤ × ℤ => (d.1 : ZMod 3) = r ∧ (d.2 : ZMod 3) = r)).card ≤ 3 := by
  revert r; decide

/-- An edge of a minimal far linkage, its partner end, and its image under the swap. -/
theorem swap_edge {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : MinF τ k Q F)
    {e : Sym2 Atom} (he : e ∈ F) : ∃ p ∈ Q, ∃ q ∈ Q, ∃ m : ℤ × ℤ, p ≠ q ∧ e = s(upA k p, (k + 1, m, 0)) ∧
      s(upA k q, (k + 1, m, 0)) ∈ F ∧ Sym2.map (swapAt k F) e = s(upA k p, (k + 1, p + q - m, 0)) ∧
      m - p ∈ shortVecs ∧ m - q ∈ shortVecs := by
  obtain ⟨p, hp, m, rfl, hmp⟩ := minF_edge hF he
  have hw : ((k + 1, m, 0) : Atom) ∈ atomsOf F := mem_atomsOf.mpr ⟨_, he, Sym2.mem_mk_right _ _⟩
  obtain ⟨p', hp', q', hq', hne, hfil⟩ := minF_mid hF hw
  have hsum := minF_nb hF hne hfil
  have hin : s(upA k p, ((k + 1, m, 0) : Atom)) ∈ F.filter (fun e => ((k + 1, m, 0) : Atom) ∈ e) :=
    Finset.mem_filter.mpr ⟨he, Sym2.mem_mk_right _ _⟩
  rw [hfil] at hin
  simp only [Finset.mem_insert, Finset.mem_singleton] at hin
  have hmid : swapAt k F ((k + 1, m, 0) : Atom) = (k + 1, nbSum F (k + 1, m, 0) - m, 0) := by
    unfold swapAt; simp
  have mem2 : ∀ r, s(upA k r, ((k + 1, m, 0) : Atom)) ∈ F → m - r ∈ shortVecs := fun r hr => by
    obtain ⟨r', -, m', h, h'⟩ := minF_edge hF hr
    rcases Sym2.eq_iff.mp h with ⟨h1, h2⟩ | ⟨h1, -⟩
    · rw [upA_inj h1]; have : m' = m := by have := congrArg (fun a : Atom => a.2.1) h2; simpa using this.symm
      rw [← this]; exact h'
    · exact absurd h1 (fun h => by have := congrArg (fun a : Atom => a.1) h; simp [upA] at this)
  have hp'F : s(upA k p', ((k + 1, m, 0) : Atom)) ∈ F := (Finset.mem_filter.mp (by rw [hfil]; simp :
    s(upA k p', ((k + 1, m, 0) : Atom)) ∈ F.filter (fun e => ((k + 1, m, 0) : Atom) ∈ e))).1
  have hq'F : s(upA k q', ((k + 1, m, 0) : Atom)) ∈ F := (Finset.mem_filter.mp (by rw [hfil]; simp :
    s(upA k q', ((k + 1, m, 0) : Atom)) ∈ F.filter (fun e => ((k + 1, m, 0) : Atom) ∈ e))).1
  rcases hin with h | h
  · have hpp : p = p' := by
      rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨h1, -⟩
      · exact upA_inj h1
      · exact absurd h1 (fun h => by have := congrArg (fun a : Atom => a.1) h; simp [upA] at this)
    subst hpp
    refine ⟨p, hp, q', hq', m, hne, rfl, hq'F, ?_, hmp, mem2 q' hq'F⟩
    show s(swapAt k F (upA k p), swapAt k F (k + 1, m, 0)) = _
    rw [swapAt_upA, hmid, hsum]
  · have hpp : p = q' := by
      rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨h1, -⟩
      · exact upA_inj h1
      · exact absurd h1 (fun h => by have := congrArg (fun a : Atom => a.1) h; simp [upA] at this)
    subst hpp
    refine ⟨p, hp, p', hp', m, fun h => hne h.symm, rfl, hp'F, ?_, hmp, mem2 p' hp'F⟩
    show s(swapAt k F (upA k p), swapAt k F (k + 1, m, 0)) = _
    rw [swapAt_upA, hmid, hsum, add_comm p']

/-- The edge at an end is unique. -/
theorem end_edge_unique {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : FarL τ k Q F)
    {p : ℤ × ℤ} (hp : p ∈ Q) {e e' : Sym2 Atom} (he : e ∈ F) (he' : e' ∈ F) (hpe : upA k p ∈ e) (hpe' : upA k p ∈ e') :
    e = e' := by
  have h1 := hF.1.1 _ (Finset.mem_image_of_mem _ hp)
  obtain ⟨x, hx⟩ := Finset.card_eq_one.mp h1
  have a : e ∈ F.filter (fun e => upA k p ∈ e) := Finset.mem_filter.mpr ⟨he, hpe⟩
  have b : e' ∈ F.filter (fun e => upA k p ∈ e) := Finset.mem_filter.mpr ⟨he', hpe'⟩
  rw [hx, Finset.mem_singleton] at a b; rw [a, b]

theorem site_of_bond_upA {τ : ℤ → ZMod 3} {k : ℤ} {p m : ℤ × ℤ} (h : Bond τ (upA k p) (k + 1, m, 0)) :
    ((p.1 : ZMod 3) = τ k ∧ (p.2 : ZMod 3) = τ k) ∧ ((m.1 : ZMod 3) = τ (k + 1) ∧ (m.2 : ZMod 3) = τ (k + 1)) := by
  obtain ⟨h1, h2, -⟩ := h; exact ⟨h1, h2⟩

/-- The swapped middle atoms are different for different middle atoms (a point of bilayer `k + 1` has at most three
neighbours among the crossing points). -/
theorem swap_mid_inj {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : MinF τ k Q F)
    {p1 q1 m1 p2 q2 m2 : ℤ × ℤ} (hp1 : p1 ∈ Q) (hq1 : q1 ∈ Q) (hp2 : p2 ∈ Q) (hq2 : q2 ∈ Q) (hne1 : p1 ≠ q1)
    (hne2 : p2 ≠ q2)
    (e1 : s(upA k p1, (k + 1, m1, 0)) ∈ F) (f1 : s(upA k q1, (k + 1, m1, 0)) ∈ F)
    (e2 : s(upA k p2, (k + 1, m2, 0)) ∈ F) (f2 : s(upA k q2, (k + 1, m2, 0)) ∈ F)
    (hx : p1 + q1 - m1 = p2 + q2 - m2) : m1 = m2 := by
  by_contra hm
  -- the four ends are different: each end has one edge
  have edge_m : ∀ {r a b : ℤ × ℤ}, r ∈ Q → s(upA k r, (k + 1, a, 0)) ∈ F → s(upA k r, (k + 1, b, 0)) ∈ F → a = b :=
    fun hr ha hb => by
      have := end_edge_unique hF.1 hr ha hb (Sym2.mem_mk_left _ _) (Sym2.mem_mk_left _ _)
      rcases Sym2.eq_iff.mp this with ⟨-, h⟩ | ⟨h, -⟩
      · have := congrArg (fun a : Atom => a.2.1) h; simpa using this
      · exact absurd h (fun h => by have := congrArg (fun a : Atom => a.1) h; simp [upA] at this)
  have d1 : p1 ≠ p2 := fun h => hm (edge_m hp1 e1 (h ▸ e2))
  have d2 : p1 ≠ q2 := fun h => hm (edge_m hp1 e1 (h ▸ f2))
  have d3 : q1 ≠ p2 := fun h => hm (edge_m hq1 f1 (h ▸ e2))
  have d4 : q1 ≠ q2 := fun h => hm (edge_m hq1 f1 (h ▸ f2))
  -- residues
  have b1 := bondS_mk.mp (hF.1.2.2 _ e1); have b2 := bondS_mk.mp (hF.1.2.2 _ f1)
  have b3 := bondS_mk.mp (hF.1.2.2 _ e2); have b4 := bondS_mk.mp (hF.1.2.2 _ f2)
  obtain ⟨sp1, sm1⟩ := site_of_bond_upA b1; obtain ⟨sq1, -⟩ := site_of_bond_upA b2
  obtain ⟨sp2, sm2⟩ := site_of_bond_upA b3; obtain ⟨sq2, -⟩ := site_of_bond_upA b4
  have v1 := (minF_edge hF e1); have v2 := (minF_edge hF f1); have v3 := (minF_edge hF e2); have v4 := (minF_edge hF f2)
  have sv : ∀ {r a : ℤ × ℤ}, s(upA k r, (k + 1, a, 0)) ∈ F → a - r ∈ shortVecs := fun {r a} h => by
    obtain ⟨r', -, a', he, hs⟩ := minF_edge hF h
    rcases Sym2.eq_iff.mp he with ⟨h1, h2⟩ | ⟨h1, -⟩
    · rw [upA_inj h1]; have : a' = a := by have := congrArg (fun a : Atom => a.2.1) h2; simpa using this.symm
      rw [← this]; exact hs
    · exact absurd h1 (fun h => by have := congrArg (fun a : Atom => a.1) h; simp [upA] at this)
  set x := p1 + q1 - m1 with hxdef
  set r : ZMod 3 := τ k - τ (k + 1)
  -- x - y ∈ shortVecs with residue r for y ∈ {p1, q1, p2, q2}
  have memT : ∀ y ∈ ({p1, q1, p2, q2} : Finset (ℤ × ℤ)),
      x - y ∈ shortVecs.filter (fun d : ℤ × ℤ => (d.1 : ZMod 3) = r ∧ (d.2 : ZMod 3) = r) := by
    intro y hy
    simp only [Finset.mem_insert, Finset.mem_singleton] at hy
    rw [Finset.mem_filter]
    have key : ∀ (b c : ℤ × ℤ), (b.1 : ZMod 3) = τ k → (b.2 : ZMod 3) = τ k → (c.1 : ZMod 3) = τ (k + 1) →
        (c.2 : ZMod 3) = τ (k + 1) → c - b ∈ shortVecs →
        -(c - b) ∈ shortVecs ∧ ((-(c - b)).1 : ZMod 3) = r ∧ ((-(c - b)).2 : ZMod 3) = r := by
      intro b c b1 b2 c1 c2 hs
      refine ⟨neg_mem_shortVecs hs, ?_, ?_⟩ <;> simp only [Prod.fst_neg, Prod.snd_neg, Prod.fst_sub, Prod.snd_sub,
        Int.cast_neg, Int.cast_sub, b1, b2, c1, c2] <;> ring
    rcases hy with h | h | h | h
    · rw [show x - y = -(m1 - q1) by rw [h, hxdef]; abel]
      exact key q1 m1 sq1.1 sq1.2 sm1.1 sm1.2 (sv f1)
    · rw [show x - y = -(m1 - p1) by rw [h, hxdef]; abel]
      exact key p1 m1 sp1.1 sp1.2 sm1.1 sm1.2 (sv e1)
    · rw [show x - y = -(m2 - q2) by rw [h, hx]; abel]
      exact key q2 m2 sq2.1 sq2.2 sm2.1 sm2.2 (sv f2)
    · rw [show x - y = -(m2 - p2) by rw [h, hx]; abel]
      exact key p2 m2 sp2.1 sp2.2 sm2.1 sm2.2 (sv e2)
  have hcard4 : ({p1, q1, p2, q2} : Finset (ℤ × ℤ)).card = 4 := by
    rw [Finset.card_insert_of_notMem (by simp [hne1, d1, d2]), Finset.card_insert_of_notMem (by simp [d3, d4]),
      Finset.card_pair hne2]
  have hle := Finset.card_le_card_of_injOn (fun y => x - y) (fun y hy => memT y hy)
    (fun a _ b _ h => by simpa using h)
  rw [hcard4] at hle
  have := three_short r
  omega

/-! ## Paths in a minimal far linkage -/

theorem minF_conn {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {G : Finset (Sym2 Atom)} (hG : MinF τ k Q G)
    {p q : ℤ × ℤ} (hp : p ∈ Q) (hq : q ∈ Q) :
    Conn G (upA k p) (upA k q) ↔ p = q ∨ ∃ m : ℤ × ℤ, s(upA k p, (k + 1, m, 0)) ∈ G ∧ s(upA k q, (k + 1, m, 0)) ∈ G := by
  constructor
  · intro h
    -- the edge at p, its middle w and the partner q0
    have h1 := hG.1.1.1 _ (Finset.mem_image_of_mem _ hp)
    obtain ⟨e, he⟩ := Finset.card_pos.mp (by unfold degS at h1; omega : 0 < (G.filter (fun e => upA k p ∈ e)).card)
    obtain ⟨heG, hpe⟩ := Finset.mem_filter.mp he
    obtain ⟨p', hp', q0, hq0, m, hne, rfl, hq0G, -, -, -⟩ := swap_edge hG heG
    have hpp : p' = p := by
      rcases Sym2.mem_iff.mp hpe with h | h
      · exact (upA_inj h).symm
      · exact absurd h (fun h => by have := congrArg (fun a : Atom => a.1) h; simp [upA] at this)
    subst hpp
    set w : Atom := (k + 1, m, 0)
    have hw : w ∈ atomsOf G := mem_atomsOf.mpr ⟨_, heG, Sym2.mem_mk_right _ _⟩
    obtain ⟨a, ha, b, hb, hab, hfil⟩ := minF_mid hG hw
    have reach : ∀ y, Conn G (upA k p') y → y = upA k p' ∨ y = w ∨ y = upA k q0 := by
      intro y hy
      induction hy with
      | refl => left; rfl
      | @tail b' y' _ hstep ih =>
        obtain ⟨hbyG, hne'⟩ := hstep
        rcases ih with rfl | rfl | rfl
        · have := end_edge_unique hG.1 hp' hbyG heG (Sym2.mem_mk_left _ _) (Sym2.mem_mk_left _ _)
          rcases Sym2.eq_iff.mp this with ⟨-, h2⟩ | ⟨h1, -⟩
          · right; left; exact h2
          · exact absurd h1 (fun h => by have := congrArg (fun a : Atom => a.1) h; simp [upA, w] at this)
        · have : s(w, y') ∈ G.filter (fun e => w ∈ e) := Finset.mem_filter.mpr ⟨hbyG, Sym2.mem_mk_left _ _⟩
          have hpw : s(upA k p', w) ∈ G.filter (fun e => w ∈ e) := Finset.mem_filter.mpr ⟨heG, Sym2.mem_mk_right _ _⟩
          have hqw : s(upA k q0, w) ∈ G.filter (fun e => w ∈ e) := Finset.mem_filter.mpr ⟨hq0G, Sym2.mem_mk_right _ _⟩
          have hdeg : (G.filter (fun e => w ∈ e)).card = 2 := by rw [hfil, Finset.card_pair (fun h => hab (by
            rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨h1, h2⟩
            · exact upA_inj h1
            · exact absurd h2 (fun h => by have := congrArg (fun a : Atom => a.1) h; simp [upA, w] at this)))]
          have hne2 : s(upA k p', w) ≠ s(upA k q0, w) := fun h => hne (by
            rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨h1, h2⟩
            · exact upA_inj h1
            · exact absurd h2 (fun h => by have := congrArg (fun a : Atom => a.1) h; simp [upA, w] at this))
          have hset : G.filter (fun e => w ∈ e) = {s(upA k p', w), s(upA k q0, w)} := by
            symm; apply Finset.eq_of_subset_of_card_le
            · intro x hx; simp only [Finset.mem_insert, Finset.mem_singleton] at hx
              rcases hx with rfl | rfl; exacts [hpw, hqw]
            · rw [hdeg, Finset.card_pair hne2]
          rw [hset] at this
          simp only [Finset.mem_insert, Finset.mem_singleton] at this
          rcases this with h | h
          · left; rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨-, h2⟩
            · exact absurd h1 (fun h => by have := congrArg (fun a : Atom => a.1) h; simp [upA, w] at this)
            · exact h2
          · right; right; rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨-, h2⟩
            · exact absurd h1 (fun h => by have := congrArg (fun a : Atom => a.1) h; simp [upA, w] at this)
            · exact h2
        · have := end_edge_unique hG.1 hq0 hbyG hq0G (Sym2.mem_mk_left _ _) (Sym2.mem_mk_left _ _)
          rcases Sym2.eq_iff.mp this with ⟨-, h2⟩ | ⟨h1, -⟩
          · right; left; exact h2
          · exact absurd h1 (fun h => by have := congrArg (fun a : Atom => a.1) h; simp [upA, w] at this)
    rcases reach _ h with h | h | h
    · left; exact (upA_inj h).symm
    · exact absurd h (fun h => by have := congrArg (fun a : Atom => a.1) h; simp [upA, w] at this)
    · right; exact ⟨m, heG, (upA_inj h) ▸ hq0G⟩
  · rintro (rfl | ⟨m, h1, h2⟩)
    · exact Relation.ReflTransGen.refl
    · have a1 : LAdj G (upA k p) (k + 1, m, 0) := ⟨h1, fun h => by
        have := congrArg (fun a : Atom => a.1) h; simp [upA] at this⟩
      have a2 : LAdj G (k + 1, m, 0) (upA k q) := ⟨by rw [Sym2.eq_swap]; exact h2, fun h => by
        have := congrArg (fun a : Atom => a.1) h; simp [upA] at this⟩
      exact (Relation.ReflTransGen.single a1).tail a2

/-! ## The swapped linkage is a minimal far linkage of the flipped stacking -/

theorem upA_ne_mid {k : ℤ} {p m : ℤ × ℤ} : upA k p ≠ ((k + 1, m, 0) : Atom) := fun h => by
  have := congrArg (fun a : Atom => a.1) h; simp [upA] at this

theorem mid_ne_upA {k : ℤ} {p m : ℤ × ℤ} : ((k + 1, m, 0) : Atom) ≠ upA k p := fun h => upA_ne_mid h.symm

theorem swapF_mem {k : ℤ} {F : Finset (Sym2 Atom)} {e' : Sym2 Atom} :
    e' ∈ swapF k F ↔ ∃ e ∈ F, Sym2.map (swapAt k F) e = e' := by
  unfold swapF; rw [Finset.mem_image]

theorem swap_bond {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : MinF τ k Q F)
    {p q m : ℤ × ℤ} (hpF : s(upA k p, (k + 1, m, 0)) ∈ F) (hqF : s(upA k q, (k + 1, m, 0)) ∈ F) :
    Bond (flipAt τ k) (upA k p) (k + 1, p + q - m, 0) := by
  have b1 := bondS_mk.mp (hF.1.2.2 _ hpF); have b2 := bondS_mk.mp (hF.1.2.2 _ hqF)
  obtain ⟨sp, sm⟩ := site_of_bond_upA b1; obtain ⟨sq, -⟩ := site_of_bond_upA b2
  obtain ⟨-, -, hb⟩ := b2
  have hmq : m - q ∈ shortVecs := by
    unfold upA at hb; simp only at hb
    rcases hb with ⟨h1, -, -⟩ | ⟨-, -, -, h4⟩ | ⟨-, -, h3, -⟩
    · omega
    · exact h4
    · exact absurd h3 (by decide)
  have fk : flipAt τ k k = τ k := flipAt_of_le le_rfl
  have fk1 : flipAt τ k (k + 1) = tog (τ k) (τ (k + 1)) := flipAt_of_lt (by omega)
  refine ⟨?_, ?_, Or.inr (Or.inl ⟨rfl, rfl, rfl, ?_⟩)⟩
  · unfold IsSite upA; simp only; rw [fk]; exact sp
  · unfold IsSite; simp only; rw [fk1]; unfold tog
    simp only [Prod.fst_sub, Prod.snd_sub, Prod.fst_add, Prod.snd_add, Int.cast_sub, Int.cast_add, sp.1, sp.2,
      sq.1, sq.2, sm.1, sm.2]
    constructor <;> ring
  · show (p + q - m) - (upA k p).2.1 ∈ shortVecs
    rw [show (upA k p).2.1 = p from rfl, show p + q - m - p = -(m - q) by abel]
    exact neg_mem_shortVecs hmq

theorem swap_inj {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : MinF τ k Q F) :
    Set.InjOn (Sym2.map (swapAt k F)) F := by
  intro e1 he1 e2 he2 h
  obtain ⟨p1, hp1, q1, -, m1, -, rfl, -, i1, -, -⟩ := swap_edge hF he1
  obtain ⟨p2, hp2, q2, -, m2, -, rfl, -, i2, -, -⟩ := swap_edge hF he2
  have h' := i1.symm.trans (h.trans i2)
  have hp : p1 = p2 := by
    rcases Sym2.eq_iff.mp h' with ⟨h1, -⟩ | ⟨h1, -⟩
    · exact upA_inj h1
    · exact absurd h1 upA_ne_mid
  subst hp
  exact end_edge_unique hF.1 hp1 he1 he2 (Sym2.mem_mk_left _ _) (Sym2.mem_mk_left _ _)

/-- The two edges at a middle atom. -/
theorem mid_pair {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : MinF τ k Q F)
    {p q m : ℤ × ℤ} (hpq : p ≠ q) (hpF : s(upA k p, (k + 1, m, 0)) ∈ F) (hqF : s(upA k q, (k + 1, m, 0)) ∈ F)
    {f : Sym2 Atom} (hf : f ∈ F) (hmf : ((k + 1, m, 0) : Atom) ∈ f) :
    f = s(upA k p, (k + 1, m, 0)) ∨ f = s(upA k q, (k + 1, m, 0)) := by
  have hw : ((k + 1, m, 0) : Atom) ∈ atomsOf F := mem_atomsOf.mpr ⟨_, hpF, Sym2.mem_mk_right _ _⟩
  obtain ⟨a, -, b, -, hab, hfil⟩ := minF_mid hF hw
  have mem : ∀ g ∈ F, ((k + 1, m, 0) : Atom) ∈ g → g = s(upA k a, (k + 1, m, 0)) ∨ g = s(upA k b, (k + 1, m, 0)) :=
    fun g hg hmg => by
      have : g ∈ F.filter (fun e => ((k + 1, m, 0) : Atom) ∈ e) := Finset.mem_filter.mpr ⟨hg, hmg⟩
      rw [hfil] at this; simpa using this
  have ep := mem _ hpF (Sym2.mem_mk_right _ _); have eq := mem _ hqF (Sym2.mem_mk_right _ _)
  have ef := mem f hf hmf
  have inj : ∀ {r t : ℤ × ℤ}, s(upA k r, ((k + 1, m, 0) : Atom)) = s(upA k t, (k + 1, m, 0)) → r = t := fun h => by
    rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨h1, -⟩
    · exact upA_inj h1
    · exact absurd h1 upA_ne_mid
  rcases ef with rfl | rfl <;> rcases ep with h1 | h1 <;> rcases eq with h2 | h2
  all_goals first
    | (left; exact h1.symm) | (right; exact h2.symm)
    | exact absurd ((inj h1).trans (inj h2).symm) hpq

/-- The edges of the swapped linkage at a swapped middle atom are the images of the two edges at the middle atom. -/
theorem mid_deg {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : MinF τ k Q F)
    {p q m : ℤ × ℤ} (hp : p ∈ Q) (hq : q ∈ Q) (hpq : p ≠ q) (hpF : s(upA k p, (k + 1, m, 0)) ∈ F)
    (hqF : s(upA k q, (k + 1, m, 0)) ∈ F) :
    (swapF k F).filter (fun e => ((k + 1, p + q - m, 0) : Atom) ∈ e) =
      {s(upA k p, (k + 1, p + q - m, 0)), s(upA k q, (k + 1, p + q - m, 0))} := by
  set x : Atom := (k + 1, p + q - m, 0)
  -- the image of q's edge
  have img : ∀ {r : ℤ × ℤ}, r ∈ Q → s(upA k r, ((k + 1, m, 0) : Atom)) ∈ F →
      ∃ t, (t = p ∨ t = q) ∧ t ≠ r ∧ Sym2.map (swapAt k F) s(upA k r, (k + 1, m, 0)) = s(upA k r, (k + 1, r + t - m, 0)) :=
    fun {r} hr hrF => by
      obtain ⟨r', -, t, -, n, hrt, he, htF, himg, -, -⟩ := swap_edge hF hrF
      have hr' : r' = r := by
        rcases Sym2.eq_iff.mp he with ⟨h1, -⟩ | ⟨h1, -⟩
        · exact (upA_inj h1).symm
        · exact absurd h1 upA_ne_mid
      have hn : n = m := by
        rcases Sym2.eq_iff.mp he with ⟨-, h2⟩ | ⟨h1, -⟩
        · have := congrArg (fun a : Atom => a.2.1) h2; simpa using this.symm
        · exact absurd h1 upA_ne_mid
      subst hr'; subst hn
      have ht := mid_pair hF hpq hpF hqF htF (Sym2.mem_mk_right _ _)
      refine ⟨t, ?_, fun h => hrt h.symm, himg⟩
      rcases ht with h | h
      · left; rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨h1, -⟩
        · exact upA_inj h1
        · exact absurd h1 upA_ne_mid
      · right; rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨h1, -⟩
        · exact upA_inj h1
        · exact absurd h1 upA_ne_mid
  obtain ⟨tp, htp, htp', ip⟩ := img hp hpF
  obtain ⟨tq, htq, htq', iq⟩ := img hq hqF
  have tp_q : tp = q := htp.resolve_left htp'
  have tq_p : tq = p := htq.resolve_right htq'
  rw [tp_q] at ip; rw [tq_p] at iq
  have ep : s(upA k p, x) ∈ swapF k F := swapF_mem.mpr ⟨_, hpF, ip⟩
  have eq : s(upA k q, x) ∈ swapF k F := swapF_mem.mpr ⟨_, hqF, by rw [iq, add_comm q p]⟩
  ext e'
  simp only [Finset.mem_filter, Finset.mem_insert, Finset.mem_singleton]
  constructor
  · rintro ⟨he', hxe'⟩
    obtain ⟨f, hf, rfl⟩ := swapF_mem.mp he'
    obtain ⟨r, hr, t, ht, n, hrt, rfl, htF, himg, -, -⟩ := swap_edge hF hf
    rw [himg] at hxe' ⊢
    have hx : p + q - m = r + t - n := by
      rcases Sym2.mem_iff.mp hxe' with h | h
      · exact absurd h mid_ne_upA
      · have := congrArg (fun a : Atom => a.2.1) h; simpa using this
    have hn : m = n := swap_mid_inj hF hp hq hr ht hpq hrt hpF hqF hf htF hx
    subst hn
    rw [← hx]
    rcases mid_pair hF hpq hpF hqF hf (Sym2.mem_mk_right _ _) with h | h
    · left; rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨h1, -⟩
      · rw [upA_inj h1]
      · exact absurd h1 upA_ne_mid
    · right; rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨h1, -⟩
      · rw [upA_inj h1]
      · exact absurd h1 upA_ne_mid
  · rintro (rfl | rfl)
    · exact ⟨ep, Sym2.mem_mk_right _ _⟩
    · exact ⟨eq, Sym2.mem_mk_right _ _⟩

theorem swapF_minF {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : MinF τ k Q F) :
    MinF (flipAt τ k) k Q (swapF k F) := by
  have hinj := swap_inj hF
  have hcard : (swapF k F).card = F.card := Finset.card_image_of_injOn hinj
  -- every edge of swapF
  have shape : ∀ e' ∈ swapF k F, ∃ e ∈ F, ∃ p ∈ Q, ∃ q ∈ Q, ∃ m : ℤ × ℤ, p ≠ q ∧ e = s(upA k p, (k + 1, m, 0)) ∧
      s(upA k q, (k + 1, m, 0)) ∈ F ∧ e' = s(upA k p, (k + 1, p + q - m, 0)) := by
    intro e' he'
    obtain ⟨e, he, rfl⟩ := swapF_mem.mp he'
    obtain ⟨p, hp, q, hq, m, hpq, rfl, hqF, himg, -, -⟩ := swap_edge hF he
    exact ⟨_, he, p, hp, q, hq, m, hpq, rfl, hqF, himg⟩
  have endDeg : ∀ p ∈ Q, degS (swapF k F) (upA k p) = 1 := by
    intro p hp
    have h1 := hF.1.1.1 _ (Finset.mem_image_of_mem _ hp)
    obtain ⟨e, he⟩ := Finset.card_pos.mp (by unfold degS at h1; omega : 0 < (F.filter (fun e => upA k p ∈ e)).card)
    obtain ⟨heF, hpe⟩ := Finset.mem_filter.mp he
    unfold degS; rw [Finset.card_eq_one]
    refine ⟨Sym2.map (swapAt k F) e, ?_⟩
    ext e'
    simp only [Finset.mem_filter, Finset.mem_singleton]
    constructor
    · rintro ⟨he', hpe'⟩
      obtain ⟨f, hf, rfl⟩ := swapF_mem.mp he'
      obtain ⟨r, hr, q, -, m, -, rfl, -, himg, -, -⟩ := swap_edge hF hf
      rw [himg] at hpe'
      have hrp : r = p := by
        rcases Sym2.mem_iff.mp hpe' with h | h
        · exact (upA_inj h).symm
        · exact absurd h upA_ne_mid
      subst hrp
      rw [end_edge_unique hF.1 hr hf heF (Sym2.mem_mk_left _ _) hpe]
    · rintro rfl
      refine ⟨swapF_mem.mpr ⟨e, heF, rfl⟩, ?_⟩
      have : swapAt k F (upA k p) = upA k p := swapAt_upA k F p
      rw [← this]; exact Sym2.mem_map.mpr ⟨_, hpe, rfl⟩
  refine ⟨⟨⟨fun b hb => ?_, fun y hy => ?_, fun G hG hGne hGcl => ?_, fun e' he' hd => ?_⟩, ?_, ?_⟩, ?_⟩
  · obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp hb; exact endDeg p hp
  · by_cases hex : ∃ e' ∈ swapF k F, y ∈ e'
    · right
      obtain ⟨e', he', hye'⟩ := hex
      obtain ⟨e, he, p, hp, q, hq, m, hpq, rfl, hqF, rfl⟩ := shape e' he'
      have hy : y = (k + 1, p + q - m, 0) := by
        rcases Sym2.mem_iff.mp hye' with rfl | rfl
        · exact absurd (Finset.mem_image_of_mem _ hp) hy
        · rfl
      subst hy
      unfold degS
      rw [mid_deg hF hp hq hpq he hqF, Finset.card_pair (fun h => hpq (by
        rcases Sym2.eq_iff.mp h with ⟨h1, -⟩ | ⟨h1, -⟩
        · exact upA_inj h1
        · exact absurd h1 upA_ne_mid))]
    · left
      unfold degS; rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
      intro e' he' hye'; exact hex ⟨e', he', hye'⟩
  · obtain ⟨e', he'⟩ := hGne
    obtain ⟨e, -, p, hp, q, -, m, -, -, -, rfl⟩ := shape e' (hG he')
    have h1 : 0 < degS G (upA k p) := Finset.card_pos.mpr ⟨_, Finset.mem_filter.mpr ⟨he', Sym2.mem_mk_left _ _⟩⟩
    have h2 : degS G (upA k p) ≤ 1 := (degS_mono hG _).trans (endDeg p hp).le
    obtain ⟨t, ht⟩ := hGcl (upA k p); omega
  · obtain ⟨e, -, p, -, q, -, m, -, -, -, rfl⟩ := shape e' he'
    exact upA_ne_mid (Sym2.mk_isDiag_iff.mp hd)
  · intro e' he' w hw
    obtain ⟨e, -, p, -, q, -, m, -, -, -, rfl⟩ := shape e' he'
    rcases Sym2.mem_iff.mp hw with rfl | rfl
    · exact isFar_upA k p
    · left; show k < k + 1; omega
  · intro e' he'
    obtain ⟨e, he, p, -, q, -, m, -, rfl, hqF, rfl⟩ := shape e' he'
    rw [bondS_mk]; exact swap_bond hF he hqF
  · rw [hcard]; exact hF.2

/-! ## Same pairing, the swap undoes itself, equal counts -/

theorem share_iff {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : MinF τ k Q F)
    {p q : ℤ × ℤ} (hp : p ∈ Q) (hq : q ∈ Q) (hpq : p ≠ q) :
    (∃ m : ℤ × ℤ, s(upA k p, (k + 1, m, 0)) ∈ swapF k F ∧ s(upA k q, (k + 1, m, 0)) ∈ swapF k F) ↔
      (∃ m : ℤ × ℤ, s(upA k p, (k + 1, m, 0)) ∈ F ∧ s(upA k q, (k + 1, m, 0)) ∈ F) := by
  constructor
  · rintro ⟨x, hpx, hqx⟩
    obtain ⟨f1, hf1, i1⟩ := swapF_mem.mp hpx
    obtain ⟨r1, hr1, t1, ht1, n1, hrt1, rfl, htF1, img1, -, -⟩ := swap_edge hF hf1
    obtain ⟨f2, hf2, i2⟩ := swapF_mem.mp hqx
    obtain ⟨r2, hr2, t2, ht2, n2, hrt2, rfl, htF2, img2, -, -⟩ := swap_edge hF hf2
    rw [img1] at i1; rw [img2] at i2
    have e1 : r1 = p ∧ r1 + t1 - n1 = x := by
      rcases Sym2.eq_iff.mp i1 with ⟨h1, h2⟩ | ⟨h1, -⟩
      · exact ⟨upA_inj h1, by have := congrArg (fun a : Atom => a.2.1) h2; simpa using this⟩
      · exact absurd h1 upA_ne_mid
    have e2 : r2 = q ∧ r2 + t2 - n2 = x := by
      rcases Sym2.eq_iff.mp i2 with ⟨h1, h2⟩ | ⟨h1, -⟩
      · exact ⟨upA_inj h1, by have := congrArg (fun a : Atom => a.2.1) h2; simpa using this⟩
      · exact absurd h1 upA_ne_mid
    have hn : n1 = n2 := swap_mid_inj hF hr1 ht1 hr2 ht2 hrt1 hrt2 hf1 htF1 hf2 htF2 (e1.2.trans e2.2.symm)
    refine ⟨n1, ?_, ?_⟩
    · rw [← e1.1]; exact hf1
    · rw [← e2.1, hn]; exact hf2
  · rintro ⟨m, hpF, hqF⟩
    refine ⟨p + q - m, ?_, ?_⟩
    · have := mid_deg hF hp hq hpq hpF hqF
      have h : s(upA k p, ((k + 1, p + q - m, 0) : Atom)) ∈ (swapF k F).filter
          (fun e => ((k + 1, p + q - m, 0) : Atom) ∈ e) := by rw [this]; simp
      exact (Finset.mem_filter.mp h).1
    · have := mid_deg hF hp hq hpq hpF hqF
      have h : s(upA k q, ((k + 1, p + q - m, 0) : Atom)) ∈ (swapF k F).filter
          (fun e => ((k + 1, p + q - m, 0) : Atom) ∈ e) := by rw [this]; simp
      exact (Finset.mem_filter.mp h).1

theorem swapF_pair {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : MinF τ k Q F) :
    pairF k (swapF k F) Q = pairF k F Q := by
  have hF' := swapF_minF hF
  ext ⟨p, q⟩
  simp only [pairF, Finset.mem_filter, Finset.mem_product]
  constructor
  · rintro ⟨⟨hp, hq⟩, hc⟩
    refine ⟨⟨hp, hq⟩, (minF_conn hF hp hq).mpr ?_⟩
    rcases (minF_conn hF' hp hq).mp hc with h | h
    · left; exact h
    · by_cases hpq : p = q
      · left; exact hpq
      · right; exact (share_iff hF hp hq hpq).mp h
  · rintro ⟨⟨hp, hq⟩, hc⟩
    refine ⟨⟨hp, hq⟩, (minF_conn hF' hp hq).mpr ?_⟩
    rcases (minF_conn hF hp hq).mp hc with h | h
    · left; exact h
    · by_cases hpq : p = q
      · left; exact hpq
      · right; exact (share_iff hF hp hq hpq).mpr h

theorem swapF_swapF {τ : ℤ → ZMod 3} {k : ℤ} {Q : Finset (ℤ × ℤ)} {F : Finset (Sym2 Atom)} (hF : MinF τ k Q F) :
    swapF k (swapF k F) = F := by
  have hF' := swapF_minF hF
  unfold swapF
  conv_rhs => rw [← Finset.image_id (s := F)]
  rw [Finset.image_image]
  apply Finset.image_congr
  intro e he
  obtain ⟨p, hp, q, hq, m, hpq, rfl, hqF, himg, -, -⟩ := swap_edge hF he
  simp only [Function.comp_apply, id]
  rw [himg]
  have hpx : s(upA k p, ((k + 1, p + q - m, 0) : Atom)) ∈ swapF k F := swapF_mem.mpr ⟨_, he, himg⟩
  have hnb := minF_nb hF' hpq (mid_deg hF hp hq hpq he hqF)
  show s(swapAt k (swapF k F) (upA k p), swapAt k (swapF k F) (k + 1, p + q - m, 0)) = _
  rw [swapAt_upA]
  have : swapAt k (swapF k F) ((k + 1, p + q - m, 0) : Atom) = (k + 1, m, 0) := by
    unfold swapAt; simp only [and_self, ↓reduceIte]
    rw [hnb]; congr 1; congr 1; abel
  rw [this]

/-- **Minimal far linkages do not see the next letter.** For `n = |Q|`, the far linkages with `n` edges are as many in
`G τ` as in the flipped stacking, for every pairing. -/
theorem Fc_min_flip {τ : ℤ → ZMod 3} {k : ℤ} (Q : Finset (ℤ × ℤ)) (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) :
    Fc τ k Q N Q.card = Fc (flipAt τ k) k Q N Q.card := by
  unfold Fc; congr 1
  apply Set.ncard_congr (fun F _ => swapF k F)
  · rintro F ⟨hFl, hs, hN⟩
    have hF : MinF τ k Q F := ⟨hFl, hs⟩
    obtain ⟨h1, h2⟩ := swapF_minF hF
    exact ⟨h1, h2, by rw [swapF_pair hF, hN]⟩
  · rintro F₁ F₂ ⟨h1, s1, -⟩ ⟨h2, s2, -⟩ h
    have := congrArg (swapF k) h
    rwa [swapF_swapF ⟨h1, s1⟩, swapF_swapF ⟨h2, s2⟩] at this
  · rintro G ⟨hGl, hs, hN⟩
    have hG : MinF (flipAt τ k) k Q G := ⟨hGl, hs⟩
    obtain ⟨h1, h2⟩ := swapF_minF hG
    rw [flipAt_flipAt] at h1
    exact ⟨swapF k G, ⟨h1, h2, by rw [swapF_pair hG, hN]⟩, swapF_swapF hG⟩

/-- **L5, far side.** At the minimal size `|P|`, the far asymmetry vanishes. -/
theorem Af_min {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) (P : Finset (ℤ × ℤ))
    (N : Finset ((ℤ × ℤ) × (ℤ × ℤ))) : Af σ k c P N P.card = 0 := by
  unfold Af
  rw [fc_transfer hc P N P.card, ← card_gP c P, Fc_min_flip (τ := flipAt σ k) (gP c P), flipAt_flipAt]
  simp

end LoopEqualityProof
