module

public import GET.Exact

@[expose] public section

/-!
# Zones of parallelograms with exact data

`XPar` is a parallelogram whose corner and sides have coordinates in `ℤ[φ]`. Side equality, parallelism and the zone
relation of the statement are decided on the exact data, and `everyZoneHas_of_cert` proves `EveryZoneHas` from a
certificate: for each zone direction, the belt as a list (a spanning tree order), closed under the zone relation.
-/

namespace GET

open ZPhi GrunbaumK10 Set

/-! ## Segments -/

/-- two segments with distinct endpoints are equal exactly when their endpoints agree -/
theorem segment_eq_segment_iff {E : Type*} [AddCommGroup E] [Module ℝ E] {x y x' y' : E} (h : x ≠ y) :
    segment ℝ x y = segment ℝ x' y' ↔ (x = x' ∧ y = y') ∨ (x = y' ∧ y = x') := by
  constructor
  · intro hs
    have hx : x ∈ segment ℝ x' y' := hs ▸ left_mem_segment ℝ x y
    have hy : y ∈ segment ℝ x' y' := hs ▸ right_mem_segment ℝ x y
    have hx' : x' ∈ segment ℝ x y := hs ▸ left_mem_segment ℝ x' y'
    have hy' : y' ∈ segment ℝ x y := hs ▸ right_mem_segment ℝ x' y'
    rw [segment_eq_image'] at hx hy hx' hy'
    obtain ⟨s, ⟨hs0, hs1⟩, hxs⟩ := hx
    obtain ⟨t, ⟨ht0, ht1⟩, hyt⟩ := hy
    obtain ⟨a, ⟨ha0, ha1⟩, hxa⟩ := hx'
    obtain ⟨b, ⟨hb0, hb1⟩, hyb⟩ := hy'
    simp only at hxs hyt hxa hyb
    set d := y' - x' with hd
    have hd0 : d ≠ 0 := by
      intro h0
      apply h
      rw [← hxs, ← hyt, h0, smul_zero, smul_zero]
    have e1 : (s + a * (t - s)) • d = 0 := by
      have : x + a • (y - x) - x' = 0 := sub_eq_zero.mpr hxa
      rw [← hxs, ← hyt] at this
      rw [← this]; module
    have e2 : (s + b * (t - s) - 1) • d = 0 := by
      have : x + b • (y - x) - y' = 0 := sub_eq_zero.mpr hyb
      rw [← hxs, ← hyt, show y' = x' + d by rw [hd]; abel] at this
      rw [← this]; module
    have f1 := (smul_eq_zero.mp e1).resolve_right hd0
    have f2 := (smul_eq_zero.mp e2).resolve_right hd0
    have g1 : (b - a) * (t - s) = 1 := by linear_combination f2 - f1
    have g2 : (t - s) ^ 2 ≤ 1 := by nlinarith
    have g3 : (b - a) ^ 2 ≤ 1 := by nlinarith
    have g4 : (t - s) ^ 2 = 1 := by
      have : ((b - a) * (t - s)) ^ 2 = 1 := by rw [g1]; norm_num
      nlinarith
    have g5 : (t - s - 1) * (t - s + 1) = 0 := by linear_combination g4
    rcases mul_eq_zero.mp g5 with g | g
    · have hs' : s = 0 := by linarith
      have ht' : t = 1 := by linarith
      left
      constructor
      · rw [← hxs, hs', zero_smul, add_zero]
      · rw [← hyt, ht', one_smul, hd]; abel
    · have hs' : s = 1 := by linarith
      have ht' : t = 0 := by linarith
      right
      constructor
      · rw [← hxs, hs', one_smul, hd]; abel
      · rw [← hyt, ht', zero_smul, add_zero]
  · rintro (⟨rfl, rfl⟩ | ⟨rfl, rfl⟩)
    · rfl
    · exact segment_symm ℝ _ _

/-! ## Parallelograms with exact data -/

/-- a parallelogram with exact data -/
structure XPar where
  p : Fin 3 → ZPhi
  u : Fin 3 → ZPhi
  v : Fin 3 → ZPhi

/-- the parallelogram in `Space` -/
noncomputable def XPar.toPar (f : XPar) : Parallelogram := ⟨ev f.p, ev f.u, ev f.v⟩

/-- the exact corners -/
def XPar.corners (f : XPar) : Fin 4 → Fin 3 → ZPhi := ![f.p, f.p + f.u, f.p + f.u + f.v, f.p + f.v]

/-- the exact direction of side `a` -/
def XPar.dir (f : XPar) (a : Fin 4) : Fin 3 → ZPhi := f.corners (a + 1) - f.corners a

theorem XPar.toPar_corners (f : XPar) (a : Fin 4) : f.toPar.corners a = ev (f.corners a) := by
  fin_cases a <;> simp [XPar.toPar, Parallelogram.corners, XPar.corners, ev_add]

/-- sides `a` of `f` and `b` of `g` have the same endpoints -/
abbrev XPar.SideMatch (f g : XPar) (a b : Fin 4) : Prop :=
  (f.corners a = g.corners b ∧ f.corners (a + 1) = g.corners (b + 1)) ∨
    (f.corners a = g.corners (b + 1) ∧ f.corners (a + 1) = g.corners b)

theorem XPar.side_eq_iff (f g : XPar) (a b : Fin 4) (hf : f.dir a ≠ 0) :
    f.toPar.side a = g.toPar.side b ↔ f.SideMatch g a b := by
  have hne : f.corners a ≠ f.corners (a + 1) := by
    intro h; apply hf; rw [XPar.dir, h]
    funext c
    show (⟨(f.corners (a + 1) c).a - (f.corners (a + 1) c).a, (f.corners (a + 1) c).b - (f.corners (a + 1) c).b⟩ :
      ZPhi) = ⟨0, 0⟩
    simp
  unfold Parallelogram.side
  rw [XPar.toPar_corners, XPar.toPar_corners, XPar.toPar_corners, XPar.toPar_corners,
    segment_eq_segment_iff (ev_injective.ne hne)]
  simp only [ev_eq_iff]

/-- the exact zone relation: faces `i` and `j` share a side parallel to `d` -/
abbrev XAcross {m : ℕ} (X : Fin m → XPar) (d : Fin 3 → ZPhi) (i j : Fin m) : Prop :=
  ∃ a b : Fin 4, (X i).SideMatch (X j) a b ∧ xcross ((X i).dir a) d = 0

/-- every side of every face is non-degenerate -/
abbrev XNondeg {m : ℕ} (X : Fin m → XPar) : Prop := ∀ i, (X i).u ≠ 0 ∧ (X i).v ≠ 0 ∧ ∀ a : Fin 4, (X i).dir a ≠ 0

theorem across_iff {m : ℕ} {X : Fin m → XPar} (hX : XNondeg X) {d : Fin 3 → ZPhi} (hd : d ≠ 0) (i j : Fin m) :
    AcrossSideParallel (fun i => (X i).toPar) (ev d) i j ↔ XAcross X d i j := by
  unfold AcrossSideParallel
  refine exists_congr fun a => exists_congr fun b => ?_
  rw [XPar.side_eq_iff _ _ _ _ ((hX i).2.2 a), XPar.toPar_corners, XPar.toPar_corners, ← ev_sub]
  rw [parallel_iff hd]
  have := (hX i).2.2 a
  simp only [XPar.dir] at this
  exact and_congr_right fun _ => ⟨fun h => h.2, fun h => ⟨this, h⟩⟩

/-- the zone relation and side parallelism only depend on the direction up to a non-zero factor -/
theorem across_smul {m : ℕ} (F : Fin m → Parallelogram) {w : Space} {c : ℝ} (hc : c ≠ 0) (i j : Fin m) :
    AcrossSideParallel F (c • w) i j ↔ AcrossSideParallel F w i j := by
  unfold AcrossSideParallel
  refine exists_congr fun a => exists_congr fun b => and_congr_right fun _ => ?_
  constructor
  · rintro ⟨e, he, h⟩
    exact ⟨e * c, mul_ne_zero he hc, by rw [h, smul_smul]⟩
  · rintro ⟨e, he, h⟩
    exact ⟨e / c, div_ne_zero he hc, by rw [h, smul_smul, div_mul_cancel₀ _ hc]⟩

theorem hasSideParallel_smul (F : Parallelogram) {w : Space} {c : ℝ} (hc : c ≠ 0) :
    F.HasSideParallel (c • w) ↔ F.HasSideParallel w := by
  unfold Parallelogram.HasSideParallel
  have key : ∀ x : Space, (∃ e : ℝ, e ≠ 0 ∧ x = e • c • w) ↔ (∃ e : ℝ, e ≠ 0 ∧ x = e • w) := by
    intro x
    constructor
    · rintro ⟨e, he, h⟩
      exact ⟨e * c, mul_ne_zero he hc, by rw [h, smul_smul]⟩
    · rintro ⟨e, he, h⟩
      exact ⟨e / c, div_ne_zero he hc, by rw [h, smul_smul, div_mul_cancel₀ _ hc]⟩
  rw [key, key]

theorem zone_smul {m : ℕ} (F : Fin m → Parallelogram) (i : Fin m) {w : Space} {c : ℝ} (hc : c ≠ 0) :
    zone F i (c • w) = zone F i w := by
  unfold zone
  have : AcrossSideParallel F (c • w) = AcrossSideParallel F w := by
    funext i j; exact propext (across_smul F hc i j)
  rw [this]

/-! ## The zone certificate -/

/-- a zone direction and its belt, listed so that every face after the first shares a side with an earlier one -/
structure ZoneClass (m : ℕ) where
  d : Fin 3 → ZPhi
  belt : List (Fin m)

/-- the exact side-parallel test -/
abbrev XHasPar {m : ℕ} (X : Fin m → XPar) (j : Fin m) (d : Fin 3 → ZPhi) : Prop :=
  xcross (X j).u d = 0 ∨ xcross (X j).v d = 0

/-- the conditions on one zone class -/
abbrev ZoneClass.Ok {m : ℕ} (X : Fin m → XPar) (k : ℕ) (C : ZoneClass m) : Prop :=
  C.d ≠ 0 ∧
  (∀ j ∈ C.belt, ∀ l : Fin m, XAcross X C.d j l → l ∈ C.belt) ∧
  (∀ j : Fin m, j ∈ C.belt ↔ XHasPar X j C.d) ∧
  C.belt.Nodup ∧ C.belt.length = k ∧
  (∀ n : Fin C.belt.length, n.val = 0 ∨
    ∃ l : Fin C.belt.length, l < n ∧ XAcross X C.d (C.belt.get l) (C.belt.get n) ∧
      XAcross X C.d (C.belt.get n) (C.belt.get l))

instance {m : ℕ} (X : Fin m → XPar) (k : ℕ) (C : ZoneClass m) : Decidable (C.Ok X k) := by
  unfold ZoneClass.Ok
  have h1 : Decidable (∀ j ∈ C.belt, ∀ l : Fin m, XAcross X C.d j l → l ∈ C.belt) := inferInstance
  have h2 : Decidable (∀ j : Fin m, j ∈ C.belt ↔ XHasPar X j C.d) := inferInstance
  have h3 : Decidable (∀ n : Fin C.belt.length, n.val = 0 ∨
    ∃ l : Fin C.belt.length, l < n ∧ XAcross X C.d (C.belt.get l) (C.belt.get n) ∧
      XAcross X C.d (C.belt.get n) (C.belt.get l)) := inferInstance
  exact instDecidableAnd

/-- the whole certificate: non-degenerate sides, every class correct, and every face direction in some class -/
abbrev ZoneCert {m : ℕ} (X : Fin m → XPar) (k : ℕ) (Cs : List (ZoneClass m)) : Prop :=
  XNondeg X ∧ (∀ C ∈ Cs, C.Ok X k) ∧
  ∀ i : Fin m, (∃ C ∈ Cs, xcross (X i).u C.d = 0 ∧ i ∈ C.belt) ∧
    (∃ C ∈ Cs, xcross (X i).v C.d = 0 ∧ i ∈ C.belt)

theorem belt_reach {m : ℕ} {X : Fin m → XPar} {k : ℕ} {C : ZoneClass m} (hC : C.Ok X k)
    (h0 : 0 < C.belt.length) : ∀ (n : ℕ) (hn : n < C.belt.length),
      Relation.ReflTransGen (XAcross X C.d) (C.belt.get ⟨0, h0⟩) (C.belt.get ⟨n, hn⟩) ∧
      Relation.ReflTransGen (XAcross X C.d) (C.belt.get ⟨n, hn⟩) (C.belt.get ⟨0, h0⟩) := by
  obtain ⟨_, _, _, _, _, htree⟩ := hC
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    intro hn
    rcases htree ⟨n, hn⟩ with hz | ⟨l, hl, h1, h2⟩
    · simp only at hz; subst hz; exact ⟨.refl, .refl⟩
    · obtain ⟨a1, a2⟩ := ih l.val (Fin.lt_def.mp hl) l.isLt
      exact ⟨a1.tail h1, (Relation.ReflTransGen.single h2).trans a2⟩

theorem zone_eq_belt {m : ℕ} {X : Fin m → XPar} {k : ℕ} {C : ZoneClass m} (hC : C.Ok X k) {i : Fin m}
    (hi : i ∈ C.belt) : {j | Relation.ReflTransGen (XAcross X C.d) i j} = {j | j ∈ C.belt} := by
  ext j
  constructor
  · intro h
    induction h with
    | refl => exact hi
    | tail _ hab ih => exact hC.2.1 _ ih _ hab
  · intro hj
    obtain ⟨n, rfl⟩ := List.mem_iff_get.mp hj
    obtain ⟨ni, rfl⟩ := List.mem_iff_get.mp hi
    have h0 : 0 < C.belt.length := lt_of_le_of_lt (Nat.zero_le _) ni.isLt
    exact (belt_reach hC h0 ni.val ni.isLt).2.trans (belt_reach hC h0 n.val n.isLt).1

theorem hasSideParallel_iff {m : ℕ} {X : Fin m → XPar} (hX : XNondeg X) {d : Fin 3 → ZPhi} (hd : d ≠ 0)
    (j : Fin m) : (X j).toPar.HasSideParallel (ev d) ↔ XHasPar X j d := by
  unfold Parallelogram.HasSideParallel
  simp only [XPar.toPar]
  rw [parallel_iff hd, parallel_iff hd]
  have hu := (hX j).1
  have hv := (hX j).2.1
  constructor
  · rintro (h | h)
    · exact Or.inl h.2
    · exact Or.inr h.2
  · rintro (h | h)
    · exact Or.inl ⟨hu, h⟩
    · exact Or.inr ⟨hv, h⟩

/-- **`EveryZoneHas` from a zone certificate** -/
theorem everyZoneHas_of_cert {m : ℕ} (X : Fin m → XPar) (k : ℕ) (Cs : List (ZoneClass m))
    (h : ZoneCert X k Cs) : EveryZoneHas (fun i => (X i).toPar) k := by
  obtain ⟨hX, hCs, hcov⟩ := h
  have key : ∀ (i : Fin m) (x : Fin 3 → ZPhi), x ≠ 0 → (∃ C ∈ Cs, xcross x C.d = 0 ∧ i ∈ C.belt) →
      (zone (fun i => (X i).toPar) i (ev x)).ncard = k ∧
        zone (fun i => (X i).toPar) i (ev x) = {j | (X j).toPar.HasSideParallel (ev x)} := by
    intro i x hx ⟨C, hCm, hxC, hi⟩
    have hC := hCs C hCm
    obtain ⟨c, hc, hxc⟩ := (parallel_iff hC.1).mpr ⟨hx, hxC⟩
    have hz : zone (fun i => (X i).toPar) i (ev C.d) = {j | j ∈ C.belt} := by
      rw [← zone_eq_belt hC hi]
      unfold zone
      have : AcrossSideParallel (fun i => (X i).toPar) (ev C.d) = XAcross X C.d := by
        funext a b; exact propext (across_iff hX hC.1 a b)
      rw [this]
    rw [hxc, zone_smul _ _ hc, hz]
    refine ⟨?_, ?_⟩
    · have : {j | j ∈ C.belt} = ((C.belt.toFinset : Finset (Fin m)) : Set (Fin m)) := by
        ext j; simp
      rw [this, Set.ncard_coe_finset, List.toFinset_card_of_nodup hC.2.2.2.1, hC.2.2.2.2.1]
    · ext j
      simp only [Set.mem_setOf_eq]
      rw [hasSideParallel_smul _ hc, hasSideParallel_iff hX hC.1, hC.2.2.1 j]
  intro i w hw
  rcases hw with rfl | hw
  · exact key i _ (hX i).1 (hcov i).1
  · rw [Set.mem_singleton_iff] at hw
    subst hw
    exact key i _ (hX i).2.1 (hcov i).2

end GET
