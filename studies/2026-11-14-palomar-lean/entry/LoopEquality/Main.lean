module

public import Mathlib
public import LoopEquality.Counts

@[expose] public section

/-!
# The Loop Equality (DICTO, paper #102, Theorem 1)

`nbLoops_finite` and `loop_equality` are the two statements of the Challenge
(`LoopEquality.lean`), proved here.

Proof (#102, Section 2): along every bond the walk counts on the four pairs of
its ends are those of a fixed reference bond of diamond of the same kind
(`Counts.lean`); by #102 Lemma 3 (`Graph.transfer`) so are the closed
non-backtracking loops whose first step is that bond (`F_bond`). Every site has
one vertical and three slanted bonds, so the number of loops at any site of any
stacking is `Tv m + 3 Tc m` (`total`), the number at diamond's site.
-/

namespace LoopEqualityProof

open Finset

/-! ## Walk counts on the ends of a bond agree with a reference bond of the same kind -/

theorem W_pair_eq (σ τ : ℤ → ZMod 3) {x y x' y' : Atom} (hy : y ∈ nbr σ x) (hy' : y' ∈ nbr τ x')
    (hk : x.1 = y.1 ↔ x'.1 = y'.1) (s t : Bool) (i : ℕ) :
    Graph.W (nbr σ) i (if s then y else x) (if t then y else x) =
      Graph.W (nbr τ) i (if s then y' else x') (if t then y' else x') := by
  have hb : (Graph.W (nbr σ) i x y : ℤ) = Graph.W (nbr τ) i x' y' := by
    rw [W_nbr σ hy, W_nbr τ hy']
    by_cases h : x.1 = y.1
    · rw [if_pos h, if_pos (hk.1 h)]
    · rw [if_neg h, if_neg (fun h' => h (hk.2 h'))]
  cases s <;> cases t <;> simp only [Bool.false_eq_true, if_false, if_true]
  · exact_mod_cast (W_site σ x i).trans (W_site τ x' i).symm
  · exact_mod_cast hb
  · rw [Graph.W_symm (regular σ).symm, Graph.W_symm (regular τ).symm]
    exact_mod_cast hb
  · exact_mod_cast (W_site σ y i).trans (W_site τ y' i).symm

/-- #102 Lemma 3 applied: loops through a bond depend only on its kind. -/
theorem F_kind (σ τ : ℤ → ZMod 3) {x y x' y' : Atom} (hy : y ∈ nbr σ x) (hy' : y' ∈ nbr τ x')
    (hk : x.1 = y.1 ↔ x'.1 = y'.1) (m : ℕ) :
    Graph.F (nbr σ) m x y x y = Graph.F (nbr τ) m x' y' x' y' :=
  Graph.transfer (regular σ) (regular τ) (fun s => if s then y else x)
    (fun s => if s then y' else x') hy hy'
    (fun j s t => Graph.A_congr (regular σ) (regular τ) (fun i => W_pair_eq σ τ hy hy' hk s t i) j) m

/-! ## Reference bonds of diamond -/

/-- Diamond's site `(0, (0,0), 0)`. -/
def v0 : Atom := (0, (0, 0), 0)
/-- The upper atom above it. -/
def v1 : Atom := (0, (0, 0), 1)
/-- A lower atom of the next bilayer bonded to `v1`. -/
def c0 : Atom := (1, (1, 1), 0)

theorem v1_mem : v1 ∈ nbr diamond v0 := by
  rw [v0, v1, nbr_lower]; exact mem_insert_self _ _

theorem c0_mem : c0 ∈ nbr diamond v1 := by
  rw [v1, c0, nbr_upper]
  refine mem_insert_of_mem (mem_image.2 ⟨(1, 1), by decide, ?_⟩)
  unfold sd diamond
  decide

/-- Loops at diamond's site through its vertical bond. -/
noncomputable def Tv (m : ℕ) : ℕ := Graph.F (nbr diamond) m v0 v1 v0 v1
/-- Loops through a slanted bond of diamond. -/
noncomputable def Tc (m : ℕ) : ℕ := Graph.F (nbr diamond) m v1 c0 v1 c0

theorem F_bond (σ : ℤ → ZMod 3) {x y : Atom} (hy : y ∈ nbr σ x) (m : ℕ) :
    Graph.F (nbr σ) m x y x y = if x.1 = y.1 then Tv m else Tc m := by
  by_cases h : x.1 = y.1
  · rw [if_pos h]
    exact F_kind σ diamond hy v1_mem (iff_of_true h rfl) m
  · rw [if_neg h]
    exact F_kind σ diamond hy c0_mem (iff_of_false h (by decide)) m

/-- The loops at any atom of any stacking: one vertical and three slanted bonds. -/
theorem total (σ : ℤ → ZMod 3) (x : Atom) (m : ℕ) :
    ∑ y ∈ nbr σ x, Graph.F (nbr σ) m x y x y = Tv m + 3 * Tc m := by
  rw [sum_congr rfl (fun y hy => F_bond σ hy m)]
  obtain ⟨k, p, u⟩ := x
  rcases fin2_cases u with rfl | rfl
  · rw [nbr_lower, sum_insert (by simp), sum_image, if_pos rfl,
      sum_congr rfl (fun d _ => if_neg (show ¬ k = k - 1 by omega)), sum_const, triD_card,
      smul_eq_mul]
    intro d _ d' _ h
    simp only [Prod.mk.injEq, sub_right_inj, true_and, and_true] at h
    exact sd_injective σ _ h
  · rw [nbr_upper, sum_insert (by simp), sum_image, if_pos rfl,
      sum_congr rfl (fun d _ => if_neg (show ¬ k = k + 1 by omega)), sum_const, triD_card,
      smul_eq_mul]
    intro d _ d' _ h
    simp only [Prod.mk.injEq, add_right_inj, true_and, and_true] at h
    exact sd_injective σ _ h

/-! ## From the Challenge's loops to the graph's loops -/

theorem nbLoops_small (σ : ℤ → ZMod 3) (v : Atom) {m : ℕ} [NeZero m] (hm : m ≤ 2) :
    nbLoops σ v m = ∅ := by
  ext f
  simp only [nbLoops, Set.mem_setOf_eq, Set.mem_empty_iff_false, iff_false]
  rintro ⟨-, h⟩
  have h1 := NeZero.pos m
  have e : (0 + 2 : Fin m) = 0 := by
    interval_cases m <;> rfl
  exact (h 0).2 (by rw [e])

theorem nbLoops_eq {σ : ℤ → ZMod 3} (hσ : IsStacking σ) {v : Atom} (hv : IsSite σ v) (m : ℕ)
    [NeZero m] : nbLoops σ v m = Graph.loops (nbr σ) v m := by
  ext f
  simp only [nbLoops, Graph.loops, Set.mem_setOf_eq]
  constructor
  · rintro ⟨h0, h⟩
    exact ⟨h0, fun i => ⟨(bond_iff hσ (h i).1.1).1 (h i).1, (h i).2⟩⟩
  · rintro ⟨h0, h⟩
    have hs : ∀ n (hn : n < m), IsSite σ (f ⟨n, hn⟩) := by
      intro n
      induction n with
      | zero =>
        intro hn
        have e : (⟨0, hn⟩ : Fin m) = 0 := Fin.ext (by simp)
        rw [e, h0]; exact hv
      | succ n ih =>
        intro hn
        have e : (⟨n + 1, hn⟩ : Fin m) = ⟨n, by omega⟩ + 1 :=
          Fin.ext (by rw [Graph.fin_val_add_one]; simp [Nat.mod_eq_of_lt hn])
        rw [e]
        exact site_of_mem_nbr hσ (ih (by omega)) (h _).1
    exact ⟨h0, fun i => ⟨(bond_iff hσ (hs i.val i.isLt)).2 (h i).1, (h i).2⟩⟩

/-! ## Finiteness for every `σ` and `v` -/

theorem short_bound {δ : ℤ × ℤ} (hs : δ ∈ shortVecs) :
    -2 ≤ δ.1 ∧ δ.1 ≤ 2 ∧ -2 ≤ δ.2 ∧ δ.2 ≤ 2 := by
  simp only [shortVecs, mem_insert, mem_singleton] at hs
  rcases hs with rfl | rfl | rfl | rfl | rfl | rfl <;> decide

theorem bond_close {σ : ℤ → ZMod 3} {a b : Atom} (h : Bond σ a b) :
    a.1 - 1 ≤ b.1 ∧ b.1 ≤ a.1 + 1 ∧ a.2.1.1 - 2 ≤ b.2.1.1 ∧ b.2.1.1 ≤ a.2.1.1 + 2 ∧
      a.2.1.2 - 2 ≤ b.2.1.2 ∧ b.2.1.2 ≤ a.2.1.2 + 2 := by
  obtain ⟨-, -, h⟩ := h
  rcases h with ⟨h1, h2, -⟩ | ⟨h1, -, -, hs⟩ | ⟨h1, -, -, hs⟩
  · rw [← h2]; omega
  · have := short_bound hs
    simp only [Prod.fst_sub, Prod.snd_sub] at this
    omega
  · have := short_bound hs
    simp only [Prod.fst_sub, Prod.snd_sub] at this
    omega

theorem nbLoops_finite (σ : ℤ → ZMod 3) (v : Atom) (m : ℕ) [NeZero m] :
    (nbLoops σ v m).Finite := by
  let B : Finset Atom := Icc (v.1 - m) (v.1 + m) ×ˢ
    ((Icc (v.2.1.1 - 2 * m) (v.2.1.1 + 2 * m) ×ˢ Icc (v.2.1.2 - 2 * m) (v.2.1.2 + 2 * m)) ×ˢ univ)
  refine Set.Finite.subset (Set.Finite.pi (t := fun _ : Fin m => (B : Set Atom))
    (fun _ => B.finite_toSet)) ?_
  intro f hf
  obtain ⟨h0, h⟩ := hf
  have key : ∀ n (hn : n < m), v.1 - n ≤ (f ⟨n, hn⟩).1 ∧ (f ⟨n, hn⟩).1 ≤ v.1 + n ∧
      v.2.1.1 - 2 * n ≤ (f ⟨n, hn⟩).2.1.1 ∧ (f ⟨n, hn⟩).2.1.1 ≤ v.2.1.1 + 2 * n ∧
      v.2.1.2 - 2 * n ≤ (f ⟨n, hn⟩).2.1.2 ∧ (f ⟨n, hn⟩).2.1.2 ≤ v.2.1.2 + 2 * n := by
    intro n
    induction n with
    | zero =>
      intro hn
      have e : (⟨0, hn⟩ : Fin m) = 0 := Fin.ext (by simp)
      rw [e, h0]; simp
    | succ n ih =>
      intro hn
      have e : (⟨n + 1, hn⟩ : Fin m) = ⟨n, by omega⟩ + 1 :=
        Fin.ext (by rw [Graph.fin_val_add_one]; simp [Nat.mod_eq_of_lt hn])
      have := bond_close (h ⟨n, by omega⟩).1
      have := ih (by omega)
      rw [e]
      push_cast
      omega
  simp only [Set.mem_pi, Set.mem_univ, true_implies, mem_coe, B, mem_product, mem_Icc, mem_univ,
    and_true]
  intro i
  have := key i.val i.isLt
  simp only [Fin.eta] at this
  have hi := i.isLt
  omega

/-! ## The theorem -/

theorem diamond_isStacking : IsStacking diamond := by
  intro k h
  unfold diamond at h
  push_cast at h
  have h2 : (1 : ZMod 3) = 0 := by linear_combination h
  exact absurd h2 (by decide)

theorem v0_isSite : IsSite diamond v0 := by
  unfold IsSite diamond v0; simp

/-- **The Loop Equality (#102, Theorem 1).** -/
theorem loop_equality (σ : ℤ → ZMod 3) (hσ : IsStacking σ) (v : Atom) (hv : IsSite σ v)
    (m : ℕ) [NeZero m] :
    (nbLoops σ v m).ncard = (nbLoops diamond (0, (0, 0), 0) m).ncard := by
  by_cases hm : m ≤ 2
  · rw [nbLoops_small σ v hm, nbLoops_small diamond _ hm]
  · have hm3 : 3 ≤ m := by omega
    rw [nbLoops_eq hσ hv, show ((0, (0, 0), 0) : Atom) = v0 from rfl,
      nbLoops_eq diamond_isStacking v0_isSite, (Graph.loops_ncard hm3 v).2,
      (Graph.loops_ncard hm3 v0).2, total, total]

end LoopEqualityProof
