module

public import Mathlib
public import LoopEquality.Graph

@[expose] public section

/-!
# The loops at a vertex as an explicit function of the closed walks

Generic part (any symmetric loopless graph in which every vertex has `q + 1`
neighbours). If the closed-walk counts are the same at every vertex,
`W i x x = w i`, then the number of closed non-backtracking loops of length
`m` at any vertex is `FD (dataW q w) m false false`, an explicit integer
combination of `w 0, …, w (m + 1)` (`sum_F_eq`).

Proof. On a bond `(a, b)` the edge-sequence counts `F` and the counts `nb` obey
two linear recursions whose inputs are the non-backtracking walk counts `A j` on
the four pairs from `{a, b}` (#102, Lemma 3; the recursion of Hashimoto 1989 and
Bass 1992); `nbD`, `FD` are these recursions with the inputs as data (`F_eq_FD`).
They are additive in the data, so the sum over the `q + 1` bonds at `v` is the
recursion applied to the summed data. In the summed data only `A j v v`,
`A j b b`, `Σ_b A j v b` and `Σ_b A j b v` occur, and with
`A j x y = Σ_i cA q j i · W i x y` (the standard recursion
`A_{j+2} = A·A_{j+1} − q A_j`) and `Σ_b W i v b = W (i+1) v v` these are
explicit in `w`.
-/

namespace LoopEqualityProof.Graph

open Finset

variable {V : Type*} [DecidableEq V] {nbr : V → Finset V}

/-! ## Non-backtracking walks as explicit integer combinations of walks -/

/-- `A j = Σ_i cA q j i · W i` in a graph with `q + 1` neighbours everywhere. -/
def cA (q : ℕ) : ℕ → ℕ → ℤ
  | 0, i => if i = 0 then 1 else 0
  | 1, i => if i = 1 then 1 else 0
  | 2, i => (if i = 2 then 1 else 0) - ((q : ℤ) + 1) * (if i = 0 then 1 else 0)
  | j + 3, i => (if i = 0 then 0 else cA q (j + 2) (i - 1)) - (q : ℤ) * cA q (j + 1) i

theorem cA_eq_zero (q : ℕ) : ∀ j i, j < i → cA q j i = 0
  | 0, i, h => by simp only [cA]; rw [if_neg (by omega)]
  | 1, i, h => by simp only [cA]; rw [if_neg (by omega)]
  | 2, i, h => by simp only [cA]; rw [if_neg (by omega), if_neg (by omega)]; ring
  | j + 3, i, h => by
    simp only [cA]
    rw [if_neg (by omega), cA_eq_zero q (j + 2) (i - 1) (by omega),
      cA_eq_zero q (j + 1) i (by omega)]
    ring

theorem sum_cA_extend (q j N : ℕ) (h : j + 1 ≤ N) (f : ℕ → ℤ) :
    ∑ i ∈ range N, cA q j i * f i = ∑ i ∈ range (j + 1), cA q j i * f i := by
  symm
  apply sum_subset
  · intro x hx; simp only [mem_range] at hx ⊢; omega
  · intro i _ hi
    simp only [mem_range, not_lt] at hi
    rw [cA_eq_zero q j i (by omega), zero_mul]

theorem A_eq_sum (hr : IsRegular nbr q) : ∀ (j : ℕ) (x y : V),
    (A nbr j x y : ℤ) = ∑ i ∈ range (j + 1), cA q j i * W nbr i x y
  | 0, x, y => by simp [A, W, cA]
  | 1, x, y => by
    have : A nbr 1 x y = W nbr 1 x y := rfl
    simp [cA, this]
  | 2, x, y => by
    rw [A_two hr]
    have h1 : ∀ z, A nbr 1 z y = W nbr 1 z y := fun _ => rfl
    have h2 : (∑ z ∈ nbr x, (W nbr 1 z y : ℤ)) = W nbr 2 x y := by
      show _ = ((∑ z ∈ nbr x, W nbr 1 z y : ℕ) : ℤ); push_cast; rfl
    have h0 : A nbr 0 x y = W nbr 0 x y := rfl
    simp only [h1, h2, h0, sum_range_succ, sum_range_zero, cA]
    norm_num
    ring
  | j + 3, x, y => by
    rw [A_succ_succ_succ hr, A_eq_sum hr (j + 1) x y]
    simp only [A_eq_sum hr (j + 2)]
    rw [sum_comm]
    have hW : ∀ i, (∑ z ∈ nbr x, cA q (j + 2) i * (W nbr i z y : ℤ)) =
        cA q (j + 2) i * W nbr (i + 1) x y := by
      intro i
      rw [← mul_sum]
      congr 1
      show _ = ((∑ z ∈ nbr x, W nbr i z y : ℕ) : ℤ)
      push_cast; rfl
    simp only [hW]
    simp only [cA, sub_mul, sum_sub_distrib]
    rw [sum_range_succ' (fun i => (if i = 0 then (0 : ℤ) else cA q (j + 2) (i - 1)) *
      (W nbr i x y : ℤ))]
    simp only [Nat.add_sub_cancel, if_neg (Nat.succ_ne_zero _), if_true, zero_mul, add_zero]
    rw [mul_sum]
    simp only [mul_assoc]
    rw [← mul_sum, ← mul_sum, sum_cA_extend q (j + 1) (j + 4) (by omega)]

/-! ## The bond recursions with the walk counts as data -/

/-- Counts `A j (pt s) (pt t)` on the two ends of a bond. -/
abbrev Data := Bool → Bool → ℕ → ℤ

/-- `nbD d k s t` stands for `nb k (pt s) (pt !s) (pt t)`. -/
def nbD (d : Data) : ℕ → Bool → Bool → ℤ
  | 0, s, t => d (!s) t 0
  | k + 1, s, t => d (!s) t (k + 1) - nbD d k (!s) t

/-- `FD d k s t` stands for `F k (pt s) (pt !s) (pt t) (pt !t)`. -/
def FD (d : Data) : ℕ → Bool → Bool → ℤ
  | 0, s, t => d s t 0
  | k + 1, s, t => nbD d k s t - FD d k s (!t)

theorem nbD_add (d e : Data) : ∀ k s t, nbD (d + e) k s t = nbD d k s t + nbD e k s t
  | 0, _, _ => rfl
  | k + 1, s, t => by simp only [nbD, nbD_add d e k, Pi.add_apply]; ring

theorem FD_add (d e : Data) : ∀ k s t, FD (d + e) k s t = FD d k s t + FD e k s t
  | 0, _, _ => rfl
  | k + 1, s, t => by simp only [FD, FD_add d e k, nbD_add]; ring

theorem nbD_zero : ∀ k s t, nbD 0 k s t = 0
  | 0, _, _ => rfl
  | k + 1, s, t => by simp only [nbD, nbD_zero k, Pi.zero_apply]; ring

theorem FD_zero : ∀ k s t, FD 0 k s t = 0
  | 0, _, _ => rfl
  | k + 1, s, t => by simp only [FD, FD_zero k, nbD_zero]; ring

theorem FD_sum {ι : Type*} [DecidableEq ι] (S : Finset ι) (d : ι → Data) (k : ℕ) (s t : Bool) :
    FD (∑ b ∈ S, d b) k s t = ∑ b ∈ S, FD (d b) k s t := by
  induction S using Finset.induction_on with
  | empty => simp [FD_zero]
  | insert b S hb ih => rw [sum_insert hb, sum_insert hb, FD_add, ih]

/-- #102 Lemma 3, explicitly: on a bond, the counts `F` are the recursion `FD`
applied to the non-backtracking walk counts on the ends. -/
theorem F_eq_FD (hr : IsRegular nbr q) (pt : Bool → V) (hadj : pt true ∈ nbr (pt false)) :
    ∀ k s t, (F nbr k (pt s) (pt (!s)) (pt t) (pt (!t)) : ℤ) =
      FD (fun s t j => A nbr j (pt s) (pt t)) k s t := by
  have hne : pt false ≠ pt true := fun h => hr.irrefl _ (h ▸ hadj)
  have hinj : ∀ s t, pt s = pt t ↔ s = t := by
    intro s t; cases s <;> cases t <;> simp [hne, hne.symm]
  have hall : ∀ s, pt (!s) ∈ nbr (pt s) := by
    intro s; cases s
    · exact hadj
    · exact hr.symm _ _ hadj
  have hnb : ∀ k s t, (nb nbr k (pt s) (pt (!s)) (pt t) : ℤ) =
      nbD (fun s t j => A nbr j (pt s) (pt t)) k s t := by
    intro k
    induction k with
    | zero => intro s t; simp only [nb, nbD, A]
    | succ k ih =>
      intro s t
      have e1 := nb_add (hr.symm _ _ (hall s)) k (pt t)
      have i1 := ih (!s) t
      rw [Bool.not_not] at i1
      simp only [nbD]
      rw [← i1]
      have : ((nb nbr (k + 1) (pt s) (pt (!s)) (pt t) : ℕ) : ℤ) =
          (A nbr (k + 1) (pt (!s)) (pt t) : ℤ) - (nb nbr k (pt (!s)) (pt s) (pt t) : ℤ) := by
        rw [← e1]; push_cast; ring
      exact this
  intro k
  induction k with
  | zero =>
    intro s t
    cases s <;> cases t <;> simp [F, FD, A, hinj]
  | succ k ih =>
    intro s t
    have e1 := F_add hr.symm k (pt s) (pt (!s)) (pt t) (pt (!t)) (hr.symm _ _ (hall s))
    rw [if_pos (hall t)] at e1
    have i1 := ih s (!t)
    rw [Bool.not_not] at i1
    simp only [FD]
    rw [← i1, ← hnb k s t, ← e1]
    push_cast; ring

/-! ## The sum over the bonds at a vertex -/

/-- The summed data at a vertex of a graph with `q + 1` neighbours everywhere
and closed-walk counts `w`. -/
def dataW (q : ℕ) (w : ℕ → ℤ) : Data := fun s t j =>
  if s = t then ((q : ℤ) + 1) * ∑ i ∈ range (j + 1), cA q j i * w i
  else ∑ i ∈ range (j + 1), cA q j i * w (i + 1)

/-- **Local loop formula.** In a graph with `q + 1` neighbours at every vertex
and the same closed-walk counts `w i` at every vertex, the loops at `v` through
its bonds number `FD (dataW q w) m false false`. -/
theorem sum_F_eq (hr : IsRegular nbr q) (w : ℕ → ℤ) (hw : ∀ x i, (W nbr i x x : ℤ) = w i)
    (v : V) (m : ℕ) :
    ((∑ b ∈ nbr v, F nbr m v b v b : ℕ) : ℤ) = FD (dataW q w) m false false := by
  push_cast
  have hb : ∀ b ∈ nbr v, (F nbr m v b v b : ℤ) =
      FD (fun s t j => A nbr j (if s then b else v) (if t then b else v)) m false false := by
    intro b hb
    exact F_eq_FD hr (fun s => if s then b else v) hb m false false
  rw [sum_congr rfl hb, ← FD_sum]
  congr 1
  funext s t j
  rw [Finset.sum_apply, Finset.sum_apply, Finset.sum_apply]
  simp only [A_eq_sum hr]
  have hc : ((nbr v).card : ℤ) = (q : ℤ) + 1 := by rw [hr.card]; push_cast; ring
  cases s <;> cases t <;> simp only [dataW, Bool.false_eq_true, if_false, if_true]
  · simp only [hw, sum_const, nsmul_eq_mul, hc]
  · rw [sum_comm]
    refine sum_congr rfl (fun i _ => ?_)
    rw [← mul_sum, ← hw v (i + 1)]
    congr 1
    rw [W_succ_right hr.symm]; push_cast; rfl
  · rw [sum_comm]
    refine sum_congr rfl (fun i _ => ?_)
    rw [← mul_sum, ← hw v (i + 1)]
    congr 1
    show _ = ((∑ z ∈ nbr v, W nbr i z v : ℕ) : ℤ)
    push_cast; rfl
  · simp only [hw, sum_const, nsmul_eq_mul, hc]

end LoopEqualityProof.Graph
