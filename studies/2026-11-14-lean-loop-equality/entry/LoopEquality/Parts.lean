module

public import Mathlib
public import LoopEquality.Defs
public import LoopEquality.Twist
public import LoopEquality.Polygons
public import LoopEquality.TheoremA
public import LoopEquality.Linkage
public import LoopEquality.Product
public import LoopEquality.Locality

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

end LoopEqualityProof
