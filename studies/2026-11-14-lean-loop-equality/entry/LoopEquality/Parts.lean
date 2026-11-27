module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.Linkage
public import LoopEquality.Product
public import LoopEquality.Locality
public import LoopEquality.CorollaryA1
public import LoopEquality.Degree

@[expose] public section

/-!
# Product structure: two linkages and their crossings make a polygon (Lean paper, Milestone 3b, part 2)

Study 2026-11-15-polygon-bijection §3. At the cut of bilayer `k`, `loA k p = (k, p, 0)` (root side) and
`upA k p = (k, p, 1)` (far side) are the ends of the vertical bond `vert k p`.

* `IsLinkageOn L B`: degree 1 at the atoms of `B`, 0 or 2 elsewhere, no nonempty closed subset, no loops.
* `SingleCycle k P R F`: no nonempty proper set of crossing points is closed under both pairings
  (`Conn R (loA k p) (loA k q)` and `Conn F (upA k p) (upA k q)`).
* `parts_to_polygon`: a root linkage ending at the `loA k p`, a far linkage ending at the `upA k p`
  (`p ∈ P`), the vertical bonds at `P`, and `SingleCycle` give a polygon.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

def loA (k : ℤ) (p : ℤ × ℤ) : Atom := (k, p, 0)
def upA (k : ℤ) (p : ℤ × ℤ) : Atom := (k, p, 1)

theorem loA_inj {k : ℤ} {p q : ℤ × ℤ} (h : loA k p = loA k q) : p = q := congrArg (fun a : Atom => a.2.1) h
theorem upA_inj {k : ℤ} {p q : ℤ × ℤ} (h : upA k p = upA k q) : p = q := congrArg (fun a : Atom => a.2.1) h
theorem loA_ne_upA {k : ℤ} {p q : ℤ × ℤ} : loA k p ≠ upA k q := by
  intro h; unfold loA upA at h; simp only [Prod.mk.injEq] at h; exact absurd h.2.2 (by decide)

theorem not_isFar_loA (k : ℤ) (p : ℤ × ℤ) : ¬ IsFar k (loA k p) := by unfold IsFar loA; simp
theorem isFar_upA (k : ℤ) (p : ℤ × ℤ) : IsFar k (upA k p) := by unfold IsFar upA; simp

theorem vert_eq (k : ℤ) (p : ℤ × ℤ) : vert k p = s(loA k p, upA k p) := rfl

/-- A linkage with ends `B`. -/
def IsLinkageOn (L : Finset (Sym2 Atom)) (B : Finset Atom) : Prop :=
  (∀ w ∈ B, degS L w = 1) ∧ (∀ w ∉ B, degS L w = 0 ∨ degS L w = 2) ∧
    (∀ G ⊆ L, G.Nonempty → ¬ Closed G) ∧ (∀ e ∈ L, ¬ e.IsDiag)

/-- No nonempty proper set of crossing points is closed under both pairings. -/
def SingleCycle (k : ℤ) (P : Finset (ℤ × ℤ)) (R F : Finset (Sym2 Atom)) : Prop :=
  ∀ Q ⊆ P, Q.Nonempty → (∀ p ∈ Q, ∀ q ∈ P, Conn R (loA k p) (loA k q) → q ∈ Q) →
    (∀ p ∈ Q, ∀ q ∈ P, Conn F (upA k p) (upA k q) → q ∈ Q) → Q = P

theorem degS_union {A B : Finset (Sym2 Atom)} (h : Disjoint A B) (w : Atom) :
    degS (A ∪ B) w = degS A w + degS B w := by
  unfold degS; rw [Finset.filter_union, Finset.card_union_of_disjoint (Finset.disjoint_filter_filter h)]

theorem degS_mono {A B : Finset (Sym2 Atom)} (h : A ⊆ B) (w : Atom) : degS A w ≤ degS B w :=
  Finset.card_le_card (Finset.filter_subset_filter _ h)

/-- In a linkage, every component that has an edge reaches an end: from any atom of an edge there is a path
to an atom of `B` (else the component would be a nonempty closed subset). -/
theorem reaches_end {L : Finset (Sym2 Atom)} {B : Finset Atom} (hL : IsLinkageOn L B) {e : Sym2 Atom}
    (he : e ∈ L) {a : Atom} (ha : a ∈ e) : ∃ b ∈ B, Conn L a b := by
  by_contra hno
  push Not at hno
  set C := compSet L a
  set K := L.filter (fun f => ∃ w ∈ f, w ∈ C)
  have hKcl : Closed K := by
    intro w
    by_cases hw : w ∈ C
    · have hdeg : degS K w = degS L w := by
        unfold degS; congr 1; ext f
        simp only [Finset.mem_filter, K]
        constructor
        · rintro ⟨⟨hf, -⟩, hwf⟩; exact ⟨hf, hwf⟩
        · rintro ⟨hf, hwf⟩; exact ⟨⟨hf, w, hwf, hw⟩, hwf⟩
      have hwB : w ∉ B := fun hB => hno w hB (Finset.mem_filter.mp hw).2
      rw [hdeg]
      rcases hL.2.1 w hwB with h | h <;> rw [h]
      · exact Even.zero
      · exact even_two
    · have : degS K w = 0 := by
        unfold degS
        rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
        intro f hf hwf
        obtain ⟨hfL, u, hu, huC⟩ := Finset.mem_filter.mp hf
        exact hw (compSet_closed L a f hfL u hu huC w hwf)
      rw [this]; exact Even.zero
  have hKne : K.Nonempty := ⟨e, Finset.mem_filter.mpr ⟨he, a, ha, mem_compSet_self L a⟩⟩
  exact hL.2.2.1 K (Finset.filter_subset _ _) hKne hKcl

theorem exists_mem_sym2 (e : Sym2 Atom) : ∃ a, a ∈ e := by
  induction e using Sym2.ind with | _ a b => exact ⟨a, Sym2.mem_mk_left a b⟩

theorem conn_mono {L M : Finset (Sym2 Atom)} (h : L ⊆ M) {a b : Atom} (hab : Conn L a b) : Conn M a b :=
  by
    induction hab with
    | refl => exact Relation.ReflTransGen.refl
    | tail _ hbc ih => exact ih.tail ⟨h hbc.1, hbc.2⟩

/-- The degree of the vertical bonds at `P`: 1 at the `loA k p` and `upA k p`, 0 elsewhere. -/
theorem degS_verts (k : ℤ) (P : Finset (ℤ × ℤ)) (w : Atom) :
    degS (P.image (vert k)) w =
      (if w ∈ P.image (loA k) then 1 else 0) + (if w ∈ P.image (upA k) then 1 else 0) := by
  unfold degS
  by_cases hl : w ∈ P.image (loA k)
  · obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp hl
    have hu : loA k p ∉ P.image (upA k) := by
      intro h; obtain ⟨q, -, hq⟩ := Finset.mem_image.mp h; exact loA_ne_upA hq.symm
    simp only [Finset.mem_image_of_mem _ hp, hu, ↓reduceIte, add_zero]
    rw [Finset.card_eq_one]; refine ⟨vert k p, ?_⟩
    ext e; simp only [Finset.mem_filter, Finset.mem_image, Finset.mem_singleton]
    constructor
    · rintro ⟨⟨q, hq, rfl⟩, hm⟩
      rw [vert_eq, Sym2.mem_iff] at hm
      rcases hm with h | h
      · rw [loA_inj h]
      · exact absurd h loA_ne_upA
    · rintro rfl; exact ⟨⟨p, hp, rfl⟩, by rw [vert_eq]; exact Sym2.mem_mk_left _ _⟩
  · by_cases hu : w ∈ P.image (upA k)
    · obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp hu
      simp only [hl, Finset.mem_image_of_mem _ hp, ↓reduceIte, zero_add]
      rw [Finset.card_eq_one]; refine ⟨vert k p, ?_⟩
      ext e; simp only [Finset.mem_filter, Finset.mem_image, Finset.mem_singleton]
      constructor
      · rintro ⟨⟨q, hq, rfl⟩, hm⟩
        rw [vert_eq, Sym2.mem_iff] at hm
        rcases hm with h | h
        · exact absurd h.symm loA_ne_upA
        · rw [upA_inj h]
      · rintro rfl; exact ⟨⟨p, hp, rfl⟩, by rw [vert_eq]; exact Sym2.mem_mk_right _ _⟩
    · simp only [hl, hu, ↓reduceIte, add_zero]
      rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
      rintro e he hm
      obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp he
      rw [vert_eq, Sym2.mem_iff] at hm
      rcases hm with rfl | rfl
      · exact hl (Finset.mem_image_of_mem _ hq)
      · exact hu (Finset.mem_image_of_mem _ hq)

theorem degS_zero_of_side {L : Finset (Sym2 Atom)} {Q : Atom → Prop} (hL : ∀ e ∈ L, ∀ w ∈ e, Q w) {w : Atom}
    (hw : ¬ Q w) : degS L w = 0 := by
  unfold degS; rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
  intro e he hwe; exact hw (hL e he w hwe)

/-- **Parts make a polygon.** A root linkage ending at the `loA k p`, a far linkage ending at the `upA k p`
(`p ∈ P`), the vertical bonds at `P`, and the single-cycle condition give a polygon. -/
theorem parts_to_polygon {σ : ℤ → ZMod 3} {k : ℤ} {P : Finset (ℤ × ℤ)} (hP : P.Nonempty)
    {R F : Finset (Sym2 Atom)} (hR : IsLinkageOn R (P.image (loA k))) (hF : IsLinkageOn F (P.image (upA k)))
    (hRs : ∀ e ∈ R, ∀ w ∈ e, ¬ IsFar k w) (hFs : ∀ e ∈ F, ∀ w ∈ e, IsFar k w)
    (hbond : ∀ e ∈ R ∪ P.image (vert k) ∪ F, BondS σ e) (hsc : SingleCycle k P R F) :
    IsPolygon σ (R ∪ P.image (vert k) ∪ F) := by
  set V := P.image (vert k) with hV
  set E := R ∪ V ∪ F with hE
  have hRV : Disjoint R V := by
    rw [Finset.disjoint_left]; intro e heR heV
    obtain ⟨p, -, rfl⟩ := Finset.mem_image.mp heV
    exact hRs _ heR (upA k p) (by rw [vert_eq]; exact Sym2.mem_mk_right _ _) (isFar_upA k p)
  have hRVF : Disjoint (R ∪ V) F := by
    rw [Finset.disjoint_left]; intro e heRV heF
    rcases Finset.mem_union.mp heRV with heR | heV
    · obtain ⟨a, ha⟩ := exists_mem_sym2 e
      exact hRs e heR a ha (hFs e heF a ha)
    · obtain ⟨p, -, rfl⟩ := Finset.mem_image.mp heV
      exact not_isFar_loA k p (hFs _ heF _ (by rw [vert_eq]; exact Sym2.mem_mk_left _ _))
  have hdeg : ∀ w, degS E w = degS R w + degS V w + degS F w := fun w => by
    rw [hE, degS_union hRVF, degS_union hRV]
  -- degree of E: 2 at the crossing atoms, 0 or 2 elsewhere
  have hdeg2 : ∀ w, degS E w = 0 ∨ degS E w = 2 := by
    intro w
    rw [hdeg, hV, degS_verts]
    by_cases hl : w ∈ P.image (loA k)
    · obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp hl
      have hu : loA k p ∉ P.image (upA k) := by
        intro h; obtain ⟨q, -, hq⟩ := Finset.mem_image.mp h; exact loA_ne_upA hq.symm
      have h1 := hR.1 _ hl
      have h0 := degS_zero_of_side hFs (not_isFar_loA k p)
      simp only [hl, hu, ↓reduceIte]; omega
    · by_cases hu : w ∈ P.image (upA k)
      · obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp hu
        have h1 := hF.1 _ hu
        have h0 := degS_zero_of_side (Q := fun w => ¬ IsFar k w) hRs (not_not.mpr (isFar_upA k p))
        simp only [hl, hu, ↓reduceIte]; omega
      · simp only [hl, hu, ↓reduceIte, add_zero]
        by_cases hfar : IsFar k w
        · have h0 := degS_zero_of_side (Q := fun w => ¬ IsFar k w) hRs (not_not.mpr hfar)
          rcases hF.2.1 w hu with h | h <;> omega
        · have h0 := degS_zero_of_side hFs hfar
          rcases hR.2.1 w hl with h | h <;> omega
  have hcl : Closed E := fun w => by rcases hdeg2 w with h | h <;> rw [h]; exacts [Even.zero, even_two]
  have hle : ∀ y, degS E y ≤ 2 := fun y => by rcases hdeg2 y with h | h <;> omega
  have hvE : ∀ p ∈ P, vert k p ∈ E := fun p hp =>
    Finset.mem_union_left _ (Finset.mem_union_right _ (Finset.mem_image_of_mem _ hp))
  have hRE : R ⊆ E := fun e he => Finset.mem_union_left _ (Finset.mem_union_left _ he)
  have hFE : F ⊆ E := fun e he => Finset.mem_union_right _ he
  refine ⟨?_, hbond, hcl, ?_⟩
  · obtain ⟨p, hp⟩ := hP; exact ⟨_, hvE p hp⟩
  intro G hGE hGne hGcl
  have hev : ∀ y, degS E y = 2 → Even (degS G y) := fun y _ => hGcl y
  -- from an atom touched by G, along a path of R or F
  have prop : ∀ {L : Finset (Sym2 Atom)}, L ⊆ E → ∀ {y z : Atom}, (∃ e ∈ G, y ∈ e) → Conn L y z → AllAt E G z :=
    fun hL _ _ hy hyz => propagate hGE hle hev hy (conn_mono hL hyz)
  have vlo : ∀ p, loA k p ∈ vert k p := fun p => by rw [vert_eq]; exact Sym2.mem_mk_left _ _
  have vup : ∀ p, upA k p ∈ vert k p := fun p => by rw [vert_eq]; exact Sym2.mem_mk_right _ _
  set Q := P.filter (fun p => vert k p ∈ G) with hQ
  have hQP : Q ⊆ P := Finset.filter_subset _ _
  -- Q is nonempty
  have hQne : Q.Nonempty := by
    obtain ⟨e, he⟩ := hGne
    obtain ⟨a, ha⟩ := exists_mem_sym2 e
    rcases Finset.mem_union.mp (hGE he) with heRV | heF
    · rcases Finset.mem_union.mp heRV with heR | heV
      · obtain ⟨b, hb, hab⟩ := reaches_end hR heR ha
        obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp hb
        exact ⟨q, Finset.mem_filter.mpr ⟨hq, prop hRE ⟨e, he, ha⟩ hab _ (hvE q hq) (vlo q)⟩⟩
      · obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp heV
        exact ⟨q, Finset.mem_filter.mpr ⟨hq, he⟩⟩
    · obtain ⟨b, hb, hab⟩ := reaches_end hF heF ha
      obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp hb
      exact ⟨q, Finset.mem_filter.mpr ⟨hq, prop hFE ⟨e, he, ha⟩ hab _ (hvE q hq) (vup q)⟩⟩
  have hQeq : Q = P := by
    apply hsc Q hQP hQne
    · intro p hp q hq hpq
      have hpG := (Finset.mem_filter.mp hp).2
      exact Finset.mem_filter.mpr ⟨hq, prop hRE ⟨_, hpG, vlo p⟩ hpq _ (hvE q hq) (vlo q)⟩
    · intro p hp q hq hpq
      have hpG := (Finset.mem_filter.mp hp).2
      exact Finset.mem_filter.mpr ⟨hq, prop hFE ⟨_, hpG, vup p⟩ hpq _ (hvE q hq) (vup q)⟩
  have hvG : ∀ p ∈ P, vert k p ∈ G := fun p hp => by
    rw [← hQeq] at hp; exact (Finset.mem_filter.mp hp).2
  apply Finset.Subset.antisymm hGE
  intro e he
  obtain ⟨a, ha⟩ := exists_mem_sym2 e
  rcases Finset.mem_union.mp he with heRV | heF
  · rcases Finset.mem_union.mp heRV with heR | heV
    · obtain ⟨b, hb, hab⟩ := reaches_end hR heR ha
      obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp hb
      exact prop hRE ⟨_, hvG q hq, vlo q⟩ (conn_symm hab) e he ha
    · obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp heV; exact hvG q hq
  · obtain ⟨b, hb, hab⟩ := reaches_end hF heF ha
    obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp hb
    exact prop hFE ⟨_, hvG q hq, vup q⟩ (conn_symm hab) e he ha

/-- The edges of `L` that meet a set `T` closed under the edges of `L`: degree is all or nothing. -/
theorem degS_filter_closed {L : Finset (Sym2 Atom)} (T : Atom → Prop)
    (hT : ∀ a b, s(a, b) ∈ L → T a → T b) (w : Atom) :
    degS (L.filter (fun e => ∃ a ∈ e, T a)) w = if T w then degS L w else 0 := by
  unfold degS
  split
  · rename_i hw
    congr 1; ext e; simp only [Finset.mem_filter]
    constructor
    · rintro ⟨⟨he, -⟩, hwe⟩; exact ⟨he, hwe⟩
    · rintro ⟨he, hwe⟩; exact ⟨⟨he, w, hwe, hw⟩, hwe⟩
  · rename_i hw
    rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
    rintro e he hwe
    obtain ⟨heL, a, hae, ha⟩ := Finset.mem_filter.mp he
    induction e using Sym2.ind with
    | _ x y =>
      rcases Sym2.mem_iff.mp hwe with rfl | rfl <;> rcases Sym2.mem_iff.mp hae with rfl | rfl
      · exact hw ha
      · exact hw (hT _ _ (by rw [Sym2.eq_swap]; exact heL) ha)
      · exact hw (hT _ _ heL ha)
      · exact hw ha

theorem conn_step {L : Finset (Sym2 Atom)} {x a b : Atom} (h : Conn L x a) (hab : s(a, b) ∈ L) : Conn L x b := by
  by_cases e : a = b
  · rw [← e]; exact h
  · exact h.tail ⟨hab, e⟩

/-- An edge of a polygon either stays on the root side, stays on the far side, or is a vertical bond. -/
theorem edge_trichotomy {σ : ℤ → ZMod 3} {k : ℤ} {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E)
    {e : Sym2 Atom} (he : e ∈ E) :
    (∀ w ∈ e, ¬ IsFar k w) ∨ (∀ w ∈ e, IsFar k w) ∨ ∃ p, e = vert k p := by
  by_cases hc : IsCrossS k e
  · obtain ⟨p, hp, -⟩ := cross_eq_vert (hE.2.1 e he) hc
    exact Or.inr (Or.inr ⟨p, hp⟩)
  · induction e using Sym2.ind with
    | _ a b =>
      rw [isCrossS_mk] at hc
      by_cases ha : IsFar k a
      · right; left; intro w hw
        rcases Sym2.mem_iff.mp hw with rfl | rfl
        · exact ha
        · by_contra hb; exact hc (Or.inl ⟨ha, hb⟩)
      · left; intro w hw
        rcases Sym2.mem_iff.mp hw with rfl | rfl
        · exact ha
        · intro hb; exact hc (Or.inr ⟨ha, hb⟩)

theorem degS_three {k : ℤ} {P : Finset (ℤ × ℤ)} {R F : Finset (Sym2 Atom)}
    (hRs : ∀ e ∈ R, ∀ w ∈ e, ¬ IsFar k w) (hFs : ∀ e ∈ F, ∀ w ∈ e, IsFar k w) (w : Atom) :
    degS (R ∪ P.image (vert k) ∪ F) w = degS R w + degS (P.image (vert k)) w + degS F w := by
  have hRV : Disjoint R (P.image (vert k)) := by
    rw [Finset.disjoint_left]; intro e heR heV
    obtain ⟨p, -, rfl⟩ := Finset.mem_image.mp heV
    exact hRs _ heR (upA k p) (by rw [vert_eq]; exact Sym2.mem_mk_right _ _) (isFar_upA k p)
  have hRVF : Disjoint (R ∪ P.image (vert k)) F := by
    rw [Finset.disjoint_left]; intro e heRV heF
    rcases Finset.mem_union.mp heRV with heR | heV
    · obtain ⟨a, ha⟩ := exists_mem_sym2 e
      exact hRs e heR a ha (hFs e heF a ha)
    · obtain ⟨p, -, rfl⟩ := Finset.mem_image.mp heV
      exact not_isFar_loA k p (hFs _ heF _ (by rw [vert_eq]; exact Sym2.mem_mk_left _ _))
  rw [degS_union hRVF, degS_union hRV]

theorem loA_notMem_upA {k : ℤ} {P : Finset (ℤ × ℤ)} {w : Atom} (hw : ¬ IsFar k w) : w ∉ P.image (upA k) := by
  intro h; obtain ⟨q, -, rfl⟩ := Finset.mem_image.mp h; exact hw (isFar_upA k q)

theorem upA_notMem_loA {k : ℤ} {P : Finset (ℤ × ℤ)} {w : Atom} (hw : IsFar k w) : w ∉ P.image (loA k) := by
  intro h; obtain ⟨q, -, rfl⟩ := Finset.mem_image.mp h; exact not_isFar_loA k q hw

/-- **A polygon splits into parts.** A polygon crossing bilayer `k` at the points `P` is a root linkage, the
vertical bonds at `P` and a far linkage, and its crossing points satisfy the single-cycle condition. -/
theorem polygon_to_parts {σ : ℤ → ZMod 3} {k : ℤ} {E : Finset (Sym2 Atom)} (hE : IsPolygon σ E)
    {P : Finset (ℤ × ℤ)} (hPdef : ∀ p, p ∈ P ↔ vert k p ∈ E) (hP : P.Nonempty)
    {R F : Finset (Sym2 Atom)} (hRdef : R = E.filter (fun e => ∀ w ∈ e, ¬ IsFar k w))
    (hFdef : F = E.filter (fun e => ∀ w ∈ e, IsFar k w)) :
    E = R ∪ P.image (vert k) ∪ F ∧ IsLinkageOn R (P.image (loA k)) ∧ IsLinkageOn F (P.image (upA k)) ∧
      SingleCycle k P R F := by
  have hRs : ∀ e ∈ R, ∀ w ∈ e, ¬ IsFar k w := by rw [hRdef]; intro e he; exact (Finset.mem_filter.mp he).2
  have hFs : ∀ e ∈ F, ∀ w ∈ e, IsFar k w := by rw [hFdef]; intro e he; exact (Finset.mem_filter.mp he).2
  have hRE : R ⊆ E := by rw [hRdef]; exact Finset.filter_subset _ _
  have hFE : F ⊆ E := by rw [hFdef]; exact Finset.filter_subset _ _
  have hnd := polygon_nodiag hE
  have hsplit : E = R ∪ P.image (vert k) ∪ F := by
    apply Finset.Subset.antisymm
    · intro e he
      rcases edge_trichotomy (k := k) hE he with h | h | ⟨p, rfl⟩
      · exact Finset.mem_union_left _ (Finset.mem_union_left _ (by rw [hRdef]; exact Finset.mem_filter.mpr ⟨he, h⟩))
      · exact Finset.mem_union_right _ (by rw [hFdef]; exact Finset.mem_filter.mpr ⟨he, h⟩)
      · exact Finset.mem_union_left _ (Finset.mem_union_right _
          (Finset.mem_image_of_mem _ ((hPdef p).mpr he)))
    · intro e he
      rcases Finset.mem_union.mp he with h | h
      · rcases Finset.mem_union.mp h with h | h
        · exact hRE h
        · obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp h; exact (hPdef p).mp hp
      · exact hFE h
  have hdeg : ∀ w, degS E w = degS R w + degS (P.image (vert k)) w + degS F w := fun w => by
    conv_lhs => rw [hsplit]
    exact degS_three hRs hFs w
  have hE02 : ∀ w, degS E w = 0 ∨ degS E w = 2 := by
    intro w; have h1 := polygon_deg_le_two hE w; obtain ⟨m, hm⟩ := hE.2.2.1 w; omega
  have vlo : ∀ p, loA k p ∈ vert k p := fun p => by rw [vert_eq]; exact Sym2.mem_mk_left _ _
  have vup : ∀ p, upA k p ∈ vert k p := fun p => by rw [vert_eq]; exact Sym2.mem_mk_right _ _
  have hpos : ∀ p ∈ P, ∀ w ∈ vert k p, 0 < degS E w := fun p hp w hw =>
    Finset.card_pos.mpr ⟨_, Finset.mem_filter.mpr ⟨(hPdef p).mp hp, hw⟩⟩
  -- the root linkage
  have hRlink : IsLinkageOn R (P.image (loA k)) := by
    refine ⟨?_, ?_, ?_, fun e he => hnd e (hRE he)⟩
    · intro w hw
      obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp hw
      have h := hdeg (loA k p)
      rw [degS_verts] at h
      simp only [hw, loA_notMem_upA (not_isFar_loA k p), ↓reduceIte, add_zero] at h
      have h0 := degS_zero_of_side hFs (not_isFar_loA k p)
      have := hpos p hp _ (vlo p)
      rcases hE02 (loA k p) with h2 | h2 <;> omega
    · intro w hw
      by_cases hfar : IsFar k w
      · left; exact degS_zero_of_side (Q := fun w => ¬ IsFar k w) hRs (not_not.mpr hfar)
      · have h := hdeg w
        rw [degS_verts] at h
        simp only [hw, loA_notMem_upA hfar, ↓reduceIte, add_zero] at h
        have h0 := degS_zero_of_side hFs hfar
        rcases hE02 w with h2 | h2 <;> omega
    · intro G hGR hGne hGcl
      have hGE := hE.2.2.2 G (hGR.trans hRE) hGne hGcl
      obtain ⟨p, hp⟩ := hP
      have : vert k p ∈ R := hGR (hGE ▸ (hPdef p).mp hp)
      exact hRs _ this _ (vup p) (isFar_upA k p)
  -- the far linkage
  have hFlink : IsLinkageOn F (P.image (upA k)) := by
    refine ⟨?_, ?_, ?_, fun e he => hnd e (hFE he)⟩
    · intro w hw
      obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp hw
      have h := hdeg (upA k p)
      rw [degS_verts] at h
      simp only [hw, upA_notMem_loA (isFar_upA k p), ↓reduceIte, zero_add] at h
      have h0 := degS_zero_of_side (Q := fun w => ¬ IsFar k w) hRs (not_not.mpr (isFar_upA k p))
      have := hpos p hp _ (vup p)
      rcases hE02 (upA k p) with h2 | h2 <;> omega
    · intro w hw
      by_cases hfar : IsFar k w
      · have h := hdeg w
        rw [degS_verts] at h
        simp only [hw, upA_notMem_loA hfar, ↓reduceIte, add_zero] at h
        have h0 := degS_zero_of_side (Q := fun w => ¬ IsFar k w) hRs (not_not.mpr hfar)
        rcases hE02 w with h2 | h2 <;> omega
      · left; exact degS_zero_of_side hFs hfar
    · intro G hGF hGne hGcl
      have hGE := hE.2.2.2 G (hGF.trans hFE) hGne hGcl
      obtain ⟨p, hp⟩ := hP
      have : vert k p ∈ F := hGF (hGE ▸ (hPdef p).mp hp)
      exact not_isFar_loA k p (hFs _ this _ (vlo p))
  refine ⟨hsplit, hRlink, hFlink, ?_⟩
  -- the single-cycle condition
  intro Q hQP hQne hQR hQF
  set TR : Atom → Prop := fun a => ∃ q ∈ Q, Conn R (loA k q) a with hTR
  set TF : Atom → Prop := fun a => ∃ q ∈ Q, Conn F (upA k q) a with hTF
  have hTRc : ∀ a b, s(a, b) ∈ R → TR a → TR b := fun a b hab ⟨q, hq, h⟩ => ⟨q, hq, conn_step h hab⟩
  have hTFc : ∀ a b, s(a, b) ∈ F → TF a → TF b := fun a b hab ⟨q, hq, h⟩ => ⟨q, hq, conn_step h hab⟩
  set GR := R.filter (fun e => ∃ a ∈ e, TR a) with hGR
  set GF := F.filter (fun e => ∃ a ∈ e, TF a) with hGF
  set G := GR ∪ Q.image (vert k) ∪ GF with hG
  have hGRs : ∀ e ∈ GR, ∀ w ∈ e, ¬ IsFar k w := fun e he => hRs e (Finset.mem_filter.mp he).1
  have hGFs : ∀ e ∈ GF, ∀ w ∈ e, IsFar k w := fun e he => hFs e (Finset.mem_filter.mp he).1
  -- degree of GR: 1 at the loA of Q, even elsewhere
  have hR1 : ∀ w, (w ∈ Q.image (loA k) → degS GR w = 1) ∧ (w ∉ Q.image (loA k) → Even (degS GR w)) := by
    intro w
    rw [hGR, degS_filter_closed TR hTRc w]
    constructor
    · intro hw
      obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp hw
      have : TR (loA k q) := ⟨q, hq, Relation.ReflTransGen.refl⟩
      simp only [this, ↓reduceIte]
      exact hRlink.1 _ (Finset.mem_image_of_mem _ (hQP hq))
    · intro hw
      split
      · rename_i ht
        have hwP : w ∉ P.image (loA k) := by
          intro h; obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp h
          obtain ⟨q, hq, hc⟩ := ht
          exact hw (Finset.mem_image_of_mem _ (hQR q hq p hp hc))
        rcases hRlink.2.1 w hwP with h | h <;> rw [h]
        · exact Even.zero
        · exact even_two
      · exact Even.zero
  have hF1 : ∀ w, (w ∈ Q.image (upA k) → degS GF w = 1) ∧ (w ∉ Q.image (upA k) → Even (degS GF w)) := by
    intro w
    rw [hGF, degS_filter_closed TF hTFc w]
    constructor
    · intro hw
      obtain ⟨q, hq, rfl⟩ := Finset.mem_image.mp hw
      have : TF (upA k q) := ⟨q, hq, Relation.ReflTransGen.refl⟩
      simp only [this, ↓reduceIte]
      exact hFlink.1 _ (Finset.mem_image_of_mem _ (hQP hq))
    · intro hw
      split
      · rename_i ht
        have hwP : w ∉ P.image (upA k) := by
          intro h; obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp h
          obtain ⟨q, hq, hc⟩ := ht
          exact hw (Finset.mem_image_of_mem _ (hQF q hq p hp hc))
        rcases hFlink.2.1 w hwP with h | h <;> rw [h]
        · exact Even.zero
        · exact even_two
      · exact Even.zero
  have hGcl : Closed G := by
    intro w
    rw [hG, degS_three hGRs hGFs w, degS_verts]
    by_cases hl : w ∈ Q.image (loA k) <;> by_cases hu : w ∈ Q.image (upA k)
    · rw [(hR1 w).1 hl, (hF1 w).1 hu]; simp only [hl, hu, ↓reduceIte]; exact ⟨2, rfl⟩
    · rw [(hR1 w).1 hl]; obtain ⟨m, hm⟩ := (hF1 w).2 hu
      simp only [hl, hu, ↓reduceIte]; exact ⟨m + 1, by omega⟩
    · rw [(hF1 w).1 hu]; obtain ⟨m, hm⟩ := (hR1 w).2 hl
      simp only [hl, hu, ↓reduceIte]; exact ⟨m + 1, by omega⟩
    · obtain ⟨m, hm⟩ := (hR1 w).2 hl; obtain ⟨n, hn⟩ := (hF1 w).2 hu
      simp only [hl, hu, ↓reduceIte, add_zero]; exact ⟨m + n, by omega⟩
  have hGE : G ⊆ E := by
    rw [hsplit, hG]
    apply Finset.union_subset_union (Finset.union_subset_union (Finset.filter_subset _ _) _)
      (Finset.filter_subset _ _)
    exact Finset.image_subset_image hQP
  have hGne : G.Nonempty := by
    obtain ⟨q, hq⟩ := hQne
    exact ⟨_, Finset.mem_union_left _ (Finset.mem_union_right _ (Finset.mem_image_of_mem _ hq))⟩
  have hGeq := hE.2.2.2 G hGE hGne hGcl
  apply Finset.Subset.antisymm hQP
  intro p hp
  have hv : vert k p ∈ G := hGeq ▸ (hPdef p).mp hp
  rcases Finset.mem_union.mp hv with h | h
  · rcases Finset.mem_union.mp h with h | h
    · exact absurd (isFar_upA k p) (hGRs _ h _ (vup p))
    · obtain ⟨q, hq, hqp⟩ := Finset.mem_image.mp h; rw [← vert_inj hqp]; exact hq
  · exact absurd (hGFs _ h _ (vlo p)) (not_isFar_loA k p)

end LoopEqualityProof
