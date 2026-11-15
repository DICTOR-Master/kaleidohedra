module

public import Mathlib

@[expose] public section

/-!
# Walks and non-backtracking walks on a regular graph

Generic part of the proof of the Loop Equality (DICTO, paper #102). A graph is
given by its neighbour sets `nbr : V → Finset V`; it is symmetric, has no
loops, and every vertex has `q + 1` neighbours (`IsRegular`).

* `W i x y`: walks of length `i` from `x` to `y`.
* `nb k p c y`: non-backtracking walks of length `k` from `c` to `y` whose
  first step does not go to `p` (the vertex before `c`).
* `A j x y`: non-backtracking walks of length `j` from `x` to `y`.
* `F k a b c d`: non-backtracking sequences of `k + 1` directed edges from
  `(a, b)` to `(c, d)` (the entries of the powers of Hashimoto's edge matrix).

Results:
* `A_eq_ev`: `A j x y = Σ_i c_{j,i} W i x y` with integers depending only on
  `q, j, i` (the polynomial `pol q j`): the standard recursion
  `A_{j+2} = A·A_{j+1} - q A_j` for non-backtracking walks.
* `transfer`: on a bond `(a, b)`, the counts `F k a b a b` are determined by
  the counts `A j` on the four pairs from `{a, b}` (#102, Lemma 3).
* `loops_ncard`: the closed non-backtracking loops of length `m ≥ 3` at `v`,
  as maps `Fin m → V`, are finitely many and number `Σ_{b ~ v} F m v b v b`.
-/

namespace LoopEqualityProof.Graph

open Finset Polynomial

variable {V : Type*} [DecidableEq V] (nbr : V → Finset V)

/-- Walks of length `i` from `x` to `y`. -/
def W : ℕ → V → V → ℕ
  | 0, x, y => if x = y then 1 else 0
  | i + 1, x, y => ∑ z ∈ nbr x, W i z y

/-- Non-backtracking walks of length `k` from `c` to `y` whose first step
avoids `p`. -/
def nb : ℕ → V → V → V → ℕ
  | 0, _, c, y => if c = y then 1 else 0
  | k + 1, p, c, y => ∑ z ∈ (nbr c).erase p, nb k c z y

/-- Non-backtracking walks of length `j` from `x` to `y`. -/
def A : ℕ → V → V → ℕ
  | 0, x, y => if x = y then 1 else 0
  | j + 1, x, y => ∑ z ∈ nbr x, nb nbr j x z y

/-- Non-backtracking sequences of `k + 1` directed edges, the first `(a, b)`,
the last `(c, d)`. -/
def F : ℕ → V → V → V → V → ℕ
  | 0, a, b, c, d => if a = c ∧ b = d then 1 else 0
  | k + 1, a, b, c, d => ∑ z ∈ (nbr b).erase a, F k b z c d

/-- A symmetric loopless graph in which every vertex has `q + 1` neighbours. -/
structure IsRegular (q : ℕ) : Prop where
  symm : ∀ x y, y ∈ nbr x → x ∈ nbr y
  irrefl : ∀ x, x ∉ nbr x
  card : ∀ x, (nbr x).card = q + 1

variable {nbr}

/-! ## Walks -/

theorem W_succ_right (hs : ∀ x y, y ∈ nbr x → x ∈ nbr y) (i : ℕ) (x y : V) :
    W nbr (i + 1) x y = ∑ z ∈ nbr y, W nbr i x z := by
  induction i generalizing x y with
  | zero =>
    simp only [W]
    rw [sum_ite_eq', sum_ite_eq]
    by_cases h : y ∈ nbr x
    · simp [h, hs _ _ h]
    · have : x ∉ nbr y := fun h' => h (hs _ _ h')
      simp [h, this]
  | succ i ih =>
    rw [show W nbr (i + 1 + 1) x y = ∑ z ∈ nbr x, W nbr (i + 1) z y from rfl]
    rw [sum_congr rfl (fun z _ => ih z y), sum_comm]
    rfl

theorem W_symm (hs : ∀ x y, y ∈ nbr x → x ∈ nbr y) (i : ℕ) (x y : V) :
    W nbr i x y = W nbr i y x := by
  induction i generalizing x y with
  | zero => simp only [W]; by_cases h : x = y <;> simp [h, eq_comm]
  | succ i ih =>
    rw [W_succ_right hs i y x]
    show ∑ z ∈ nbr x, W nbr i z y = _
    simp_rw [ih]

/-! ## Non-backtracking walks -/

theorem nb_add {a b : V} (h : a ∈ nbr b) (k : ℕ) (y : V) :
    nb nbr (k + 1) a b y + nb nbr k b a y = A nbr (k + 1) b y :=
  sum_erase_add _ _ h

theorem F_add (hs : ∀ x y, y ∈ nbr x → x ∈ nbr y) (k : ℕ) :
    ∀ a b c d : V, a ∈ nbr b →
      F nbr (k + 1) a b c d + F nbr k a b d c = if d ∈ nbr c then nb nbr k a b c else 0 := by
  induction k with
  | zero =>
    intro a b c d hab
    show (∑ z ∈ (nbr b).erase a, if b = c ∧ z = d then 1 else 0) +
      (if a = d ∧ b = c then 1 else 0) = if d ∈ nbr c then (if b = c then 1 else 0) else 0
    by_cases hbc : b = c
    · subst hbc
      simp only [true_and]
      rw [sum_ite_eq']
      by_cases hda : d = a
      · subst hda; simp [hab]
      · simp [hda, Ne.symm hda]
    · simp [hbc]
  | succ k ih =>
    intro a b c d hab
    rw [show F nbr (k + 1 + 1) a b c d = ∑ z ∈ (nbr b).erase a, F nbr (k + 1) b z c d from rfl,
      show F nbr (k + 1) a b d c = ∑ z ∈ (nbr b).erase a, F nbr k b z d c from rfl,
      ← sum_add_distrib,
      sum_congr rfl (fun z hz => ih b z c d (hs _ _ (mem_of_mem_erase hz)))]
    by_cases h : d ∈ nbr c
    · simp only [h, if_true]; rfl
    · simp [h]

theorem sum_nb_zero (hr : IsRegular nbr q) (x y : V) :
    ∑ z ∈ nbr x, nb nbr 0 z x y = (q + 1) * (if x = y then 1 else 0) := by
  simp only [nb, sum_const, hr.card, smul_eq_mul]

theorem sum_nb_succ (hr : IsRegular nbr q) (j : ℕ) (x y : V) :
    ∑ z ∈ nbr x, nb nbr (j + 1) z x y = q * A nbr (j + 1) x y := by
  have key : ∀ z ∈ nbr x,
      nb nbr (j + 1) z x y + nb nbr j x z y = A nbr (j + 1) x y := by
    intro z hz
    exact sum_erase_add _ _ hz
  have h1 := sum_congr rfl key
  rw [sum_add_distrib, sum_const, hr.card, smul_eq_mul] at h1
  have h2 : ∑ z ∈ nbr x, nb nbr j x z y = A nbr (j + 1) x y := rfl
  rw [h2] at h1
  have h3 : (q + 1) * A nbr (j + 1) x y = q * A nbr (j + 1) x y + A nbr (j + 1) x y := by ring
  omega

theorem sum_A_succ (hr : IsRegular nbr q) (j : ℕ) (x y : V) :
    ∑ z ∈ nbr x, A nbr (j + 1) z y = A nbr (j + 2) x y + ∑ z ∈ nbr x, nb nbr j z x y := by
  have : ∀ z ∈ nbr x, A nbr (j + 1) z y = nb nbr (j + 1) x z y + nb nbr j z x y := by
    intro z hz
    exact (nb_add (hr.symm _ _ hz) j y).symm
  rw [sum_congr rfl this, sum_add_distrib]
  rfl

theorem A_two (hr : IsRegular nbr q) (x y : V) :
    (A nbr 2 x y : ℤ) = ∑ z ∈ nbr x, (A nbr 1 z y : ℤ) - (q + 1) * (A nbr 0 x y : ℤ) := by
  have h := sum_A_succ hr 0 x y
  rw [sum_nb_zero hr] at h
  have h0 : A nbr 0 x y = if x = y then 1 else 0 := rfl
  rw [h0]
  have : (∑ z ∈ nbr x, (A nbr 1 z y : ℤ)) = ((∑ z ∈ nbr x, A nbr 1 z y : ℕ) : ℤ) := by
    push_cast; rfl
  rw [this, h]
  push_cast
  ring

theorem A_succ_succ_succ (hr : IsRegular nbr q) (j : ℕ) (x y : V) :
    (A nbr (j + 3) x y : ℤ) =
      ∑ z ∈ nbr x, (A nbr (j + 2) z y : ℤ) - q * (A nbr (j + 1) x y : ℤ) := by
  have h := sum_A_succ hr (j + 1) x y
  rw [sum_nb_succ hr] at h
  have : (∑ z ∈ nbr x, (A nbr (j + 2) z y : ℤ)) = ((∑ z ∈ nbr x, A nbr (j + 2) z y : ℕ) : ℤ) := by
    push_cast; rfl
  rw [this, h]
  push_cast
  ring

/-! ## Non-backtracking walks as integer combinations of walks -/

variable (nbr) in
/-- Evaluation of a polynomial `Σ cᵢ Xⁱ` on the walk counts: `Σ cᵢ W i x y`. -/
noncomputable def ev (x y : V) : ℤ[X] →+ ℤ where
  toFun p := p.sum (fun i a => a * (W nbr i x y : ℤ))
  map_zero' := by simp
  map_add' p r := sum_add_index p r _ (fun _ => zero_mul _) (fun _ _ _ => add_mul _ _ _)

theorem ev_monomial (x y : V) (n : ℕ) (a : ℤ) :
    ev nbr x y (monomial n a) = a * W nbr n x y := by
  show (monomial n a).sum (fun i a => a * (W nbr i x y : ℤ)) = _
  exact sum_monomial_index a (fun i a => a * (W nbr i x y : ℤ)) (zero_mul _)

theorem ev_one (x y : V) : ev nbr x y 1 = W nbr 0 x y := by
  rw [← monomial_zero_one, ev_monomial, one_mul]

theorem ev_X_mul (x y : V) (p : ℤ[X]) :
    ev nbr x y (X * p) = ∑ z ∈ nbr x, ev nbr z y p := by
  induction p using Polynomial.induction_on' with
  | add p r hp hr => simp only [mul_add, map_add, hp, hr, sum_add_distrib]
  | monomial n a =>
    rw [X_mul_monomial, ev_monomial]
    simp only [ev_monomial]
    rw [← mul_sum]
    congr 1
    show ((∑ z ∈ nbr x, W nbr n z y : ℕ) : ℤ) = _
    push_cast
    rfl

theorem ev_congr {V' : Type*} [DecidableEq V'] {nbr' : V' → Finset V'} {x y : V} {x' y' : V'}
    (h : ∀ i, W nbr i x y = W nbr' i x' y') (p : ℤ[X]) : ev nbr x y p = ev nbr' x' y' p := by
  show p.sum (fun i a => a * (W nbr i x y : ℤ)) = p.sum (fun i a => a * (W nbr' i x' y' : ℤ))
  simp only [h]

/-- The polynomials with `A j = pol q j (W)`. -/
noncomputable def pol (q : ℕ) : ℕ → ℤ[X]
  | 0 => 1
  | 1 => X
  | 2 => X * X - ((q : ℤ) + 1) • (1 : ℤ[X])
  | j + 3 => X * pol q (j + 2) - (q : ℤ) • pol q (j + 1)

theorem A_eq_ev (hr : IsRegular nbr q) : ∀ (j : ℕ) (x y : V), (A nbr j x y : ℤ) = ev nbr x y (pol q j)
  | 0, x, y => by rw [pol, ev_one]; rfl
  | 1, x, y => by
    rw [pol, ← mul_one X, ev_X_mul]
    simp only [ev_one]
    show ((∑ z ∈ nbr x, nb nbr 0 x z y : ℕ) : ℤ) = _
    push_cast
    rfl
  | 2, x, y => by
    rw [A_two hr, pol, map_sub, map_zsmul, ev_X_mul, ev_one, smul_eq_mul]
    congr 1
    · refine sum_congr rfl (fun z _ => ?_)
      rw [A_eq_ev hr 1 z y, pol]
  | j + 3, x, y => by
    rw [A_succ_succ_succ hr, pol, map_sub, map_zsmul, ev_X_mul, smul_eq_mul, A_eq_ev hr (j + 1) x y]
    congr 1
    exact sum_congr rfl (fun z _ => A_eq_ev hr (j + 2) z y)

theorem A_congr {V' : Type*} [DecidableEq V'] {nbr' : V' → Finset V'} {q : ℕ}
    (hr : IsRegular nbr q) (hr' : IsRegular nbr' q) {x y : V} {x' y' : V'}
    (h : ∀ i, W nbr i x y = W nbr' i x' y') (j : ℕ) : A nbr j x y = A nbr' j x' y' := by
  have := A_eq_ev hr j x y
  rw [ev_congr h, ← A_eq_ev hr' j x' y'] at this
  exact_mod_cast this

/-! ## Lemma 3 of #102: loops through a bond are determined by walks -/

theorem transfer {V' : Type*} [DecidableEq V'] {nbr' : V' → Finset V'} {q : ℕ}
    (hr : IsRegular nbr q) (hr' : IsRegular nbr' q) (pt : Bool → V) (pt' : Bool → V')
    (hadj : pt true ∈ nbr (pt false)) (hadj' : pt' true ∈ nbr' (pt' false))
    (hA : ∀ j s t, A nbr j (pt s) (pt t) = A nbr' j (pt' s) (pt' t)) (k : ℕ) :
    F nbr k (pt false) (pt true) (pt false) (pt true) =
      F nbr' k (pt' false) (pt' true) (pt' false) (pt' true) := by
  have hne : pt false ≠ pt true := fun h => hr.irrefl _ (h ▸ hadj)
  have hne' : pt' false ≠ pt' true := fun h => hr'.irrefl _ (h ▸ hadj')
  have hinj : ∀ s t, pt s = pt t ↔ s = t := by
    intro s t; cases s <;> cases t <;> simp [hne, hne.symm]
  have hinj' : ∀ s t, pt' s = pt' t ↔ s = t := by
    intro s t; cases s <;> cases t <;> simp [hne', hne'.symm]
  have hall : ∀ s, pt (!s) ∈ nbr (pt s) := by
    intro s; cases s
    · exact hadj
    · exact hr.symm _ _ hadj
  have hall' : ∀ s, pt' (!s) ∈ nbr' (pt' s) := by
    intro s; cases s
    · exact hadj'
    · exact hr'.symm _ _ hadj'
  -- the non-backtracking walk counts on the bond
  have hnb : ∀ k s t, nb nbr k (pt s) (pt (!s)) (pt t) = nb nbr' k (pt' s) (pt' (!s)) (pt' t) := by
    intro k
    induction k with
    | zero => intro s t; simp only [nb, hinj, hinj']
    | succ k ih =>
      intro s t
      have e1 := nb_add (hr.symm _ _ (hall s)) k (pt t)
      have e2 := nb_add (hr'.symm _ _ (hall' s)) k (pt' t)
      have i1 := ih (!s) t
      rw [Bool.not_not] at i1
      have a1 := hA (k + 1) (!s) t
      omega
  have hF : ∀ k s t, F nbr k (pt s) (pt (!s)) (pt t) (pt (!t)) =
      F nbr' k (pt' s) (pt' (!s)) (pt' t) (pt' (!t)) := by
    intro k
    induction k with
    | zero => intro s t; simp only [F, hinj, hinj']
    | succ k ih =>
      intro s t
      have e1 := F_add hr.symm k (pt s) (pt (!s)) (pt t) (pt (!t)) (hr.symm _ _ (hall s))
      have e2 := F_add hr'.symm k (pt' s) (pt' (!s)) (pt' t) (pt' (!t)) (hr'.symm _ _ (hall' s))
      rw [if_pos (hall t)] at e1
      rw [if_pos (hall' t)] at e2
      have i1 := ih s (!t)
      rw [Bool.not_not] at i1
      have n1 := hnb k s t
      omega
  exact hF k false false

/-! ## Closed non-backtracking loops as edge sequences -/

omit [DecidableEq V] in
/-- `Fin.cons a` as an embedding. -/
def consEmb {n : ℕ} (a : V) : (Fin (n + 1) → V) ↪ (Fin (n + 2) → V) :=
  ⟨fun w => Fin.cons a w, Fin.cons_right_injective (α := fun _ => V) a⟩

omit [DecidableEq V] in
@[simp] theorem consEmb_apply {n : ℕ} (a : V) (w : Fin (n + 1) → V) :
    consEmb a w = Fin.cons a w := rfl

variable (nbr) in
/-- Non-backtracking vertex sequences `a, b, w 2, …, w (k+1)` (no condition on
the first edge). -/
def nbw : (k : ℕ) → V → V → Finset (Fin (k + 2) → V)
  | 0, a, b => {![a, b]}
  | k + 1, a, b => ((nbr b).erase a).biUnion fun z =>
      (nbw k b z).map (consEmb a)

omit [DecidableEq V] in
theorem cons_mk_succ {n : ℕ} (a : V) (w : Fin (n + 1) → V) (i : ℕ) (h : i + 1 < n + 2) :
    (Fin.cons a w : Fin (n + 2) → V) ⟨i + 1, h⟩ = w ⟨i, by omega⟩ :=
  Fin.cons_succ (α := fun _ => V) a w ⟨i, by omega⟩

theorem mem_nbw (k : ℕ) : ∀ (a b : V) (w : Fin (k + 2) → V), w ∈ nbw nbr k a b ↔
    w 0 = a ∧ w 1 = b ∧ ∀ i (h : i + 2 < k + 2),
      w ⟨i + 2, h⟩ ∈ nbr (w ⟨i + 1, by omega⟩) ∧ w ⟨i + 2, h⟩ ≠ w ⟨i, by omega⟩ := by
  induction k with
  | zero =>
    intro a b w
    simp only [nbw, mem_singleton]
    constructor
    · rintro rfl; simp
    · rintro ⟨h0, h1, -⟩
      funext i
      fin_cases i
      · simpa using h0
      · simpa using h1
  | succ k ih =>
    intro a b w
    simp only [nbw, mem_biUnion, mem_map, consEmb_apply, mem_erase]
    constructor
    · rintro ⟨z, ⟨hza, hzb⟩, w', hw', rfl⟩
      rw [ih] at hw'
      obtain ⟨h0, h1, hrest⟩ := hw'
      refine ⟨rfl, ?_, ?_⟩
      · rw [show (1 : Fin (k + 1 + 2)) = ⟨0 + 1, by omega⟩ from rfl, cons_mk_succ, ← h0]; rfl
      · intro i h
        rw [cons_mk_succ, cons_mk_succ]
        rcases i with _ | i
        · refine ⟨?_, ?_⟩
          · rw [show (⟨0 + 1, _⟩ : Fin (k + 2)) = 1 from rfl, h1,
              show (⟨0, _⟩ : Fin (k + 2)) = 0 from rfl, h0]; exact hzb
          · rw [show (⟨0 + 1, _⟩ : Fin (k + 2)) = 1 from rfl, h1]
            exact hza
        · rw [cons_mk_succ]
          exact hrest i (by omega)
    · rintro ⟨h0, h1, hrest⟩
      refine ⟨w ⟨2, by omega⟩, ⟨?_, ?_⟩, Fin.tail w, ?_, ?_⟩
      · have := (hrest 0 (by omega)).2
        rw [← h0]; exact this
      · have := (hrest 0 (by omega)).1
        rw [← h1]; exact this
      · rw [ih]
        refine ⟨h1, rfl, ?_⟩
        intro i h
        exact hrest (i + 1) (by omega)
      · rw [← h0]; exact Fin.cons_self_tail w

theorem nbw_zero {k : ℕ} {a b : V} {w : Fin (k + 2) → V} (h : w ∈ nbw nbr k a b) : w 0 = a :=
  ((mem_nbw k a b w).1 h).1

theorem nbw_one {k : ℕ} {a b : V} {w : Fin (k + 2) → V} (h : w ∈ nbw nbr k a b) : w 1 = b :=
  ((mem_nbw k a b w).1 h).2.1

theorem card_filter_nbw (k : ℕ) : ∀ a b c d : V,
    ((nbw nbr k a b).filter (fun w => w ⟨k, by omega⟩ = c ∧ w ⟨k + 1, by omega⟩ = d)).card =
      F nbr k a b c d := by
  induction k with
  | zero =>
    intro a b c d
    simp only [nbw, filter_singleton, F]
    by_cases h : a = c ∧ b = d
    · rw [if_pos (by simpa using h), if_pos h, card_singleton]
    · rw [if_neg (by simpa using h), if_neg h, card_empty]
  | succ k ih =>
    intro a b c d
    simp only [nbw]
    rw [filter_biUnion, card_biUnion]
    · show _ = ∑ z ∈ (nbr b).erase a, F nbr k b z c d
      refine sum_congr rfl (fun z _ => ?_)
      rw [filter_map, card_map, ← ih b z c d]
      congr 1
    · intro z₁ _ z₂ _ hz
      simp only [Function.onFun]
      rw [disjoint_left]
      intro w hw₁ hw₂
      simp only [mem_filter, mem_map, consEmb_apply] at hw₁ hw₂
      obtain ⟨⟨w₁, hw₁, rfl⟩, -⟩ := hw₁
      obtain ⟨⟨w₂, hw₂, he⟩, -⟩ := hw₂
      have e := congrFun he ⟨2, by omega⟩
      rw [show (⟨2, _⟩ : Fin (k + 1 + 2)) = ⟨1 + 1, by omega⟩ from rfl, cons_mk_succ,
        cons_mk_succ, show (⟨1, _⟩ : Fin (k + 2)) = 1 from rfl, nbw_one hw₁, nbw_one hw₂] at e
      exact hz e.symm

variable (nbr) in
/-- Closed non-backtracking loops of length `m` at `v`, in the form of the
Challenge statement. -/
def loops (v : V) (m : ℕ) [NeZero m] : Set (Fin m → V) :=
  {f | f 0 = v ∧ ∀ i, f (i + 1) ∈ nbr (f i) ∧ f (i + 2) ≠ f i}

theorem fin_val_add_one {m : ℕ} [NeZero m] (i : Fin m) : ((i + 1 : Fin m) : ℕ) = (i + 1) % m := by
  rw [Fin.val_add, Fin.val_one', Nat.add_mod_mod]

theorem fin_val_add_two {m : ℕ} [NeZero m] (i : Fin m) : ((i + 2 : Fin m) : ℕ) = (i + 2) % m := by
  rw [Fin.val_add]
  show (i.val + 2 % m) % m = _
  rw [Nat.add_mod_mod]

theorem loops_ncard {m : ℕ} [NeZero m] (hm : 3 ≤ m) (v : V) :
    (loops nbr v m).Finite ∧ (loops nbr v m).ncard = ∑ b ∈ nbr v, F nbr m v b v b := by
  classical
  set S : Finset (Fin (m + 2) → V) := (nbr v).biUnion fun b =>
    (nbw nbr m v b).filter (fun w => w ⟨m, by omega⟩ = v ∧ w ⟨m + 1, by omega⟩ = b) with hS
  have hcard : S.card = ∑ b ∈ nbr v, F nbr m v b v b := by
    rw [hS, card_biUnion]
    · exact sum_congr rfl (fun b _ => card_filter_nbw m v b v b)
    · intro b₁ _ b₂ _ hb
      simp only [Function.onFun]
      rw [disjoint_left]
      intro w hw₁ hw₂
      rw [mem_filter] at hw₁ hw₂
      exact hb ((nbw_one hw₁.1).symm.trans (nbw_one hw₂.1))
  have hm0 : 0 < m := by omega
  let Φ : (Fin m → V) → (Fin (m + 2) → V) := fun f j => f ⟨j.val % m, Nat.mod_lt _ hm0⟩
  have hΦ : Function.Injective Φ := by
    intro f g h
    funext i
    have := congrFun h ⟨i.val, by omega⟩
    simpa [Φ, Nat.mod_eq_of_lt i.isLt] using this
  -- the extension of `f` with period `m`
  have hg : ∀ (f : Fin m → V) (n : ℕ) (h : n < m + 2), Φ f ⟨n, h⟩ = f ⟨n % m, Nat.mod_lt _ hm0⟩ :=
    fun _ _ _ => rfl
  have hrange : (S : Set (Fin (m + 2) → V)) ⊆ Set.range Φ := by
    intro w hw
    rw [hS, coe_biUnion] at hw
    simp only [Set.mem_iUnion, coe_filter, Set.mem_setOf_eq, mem_coe] at hw
    obtain ⟨b, -, hwb, hm1, hm2⟩ := hw
    refine ⟨fun i => w ⟨i.val, by omega⟩, ?_⟩
    funext j
    obtain ⟨j, hj⟩ := j
    show w ⟨j % m, _⟩ = w ⟨j, hj⟩
    rcases Nat.lt_or_ge j m with h | h
    · simp [Nat.mod_eq_of_lt h]
    · rcases (show j = m ∨ j = m + 1 by omega) with h' | h'
      · subst h'
        simp only [Nat.mod_self]
        rw [hm1]; exact nbw_zero hwb
      · subst h'
        have e : (m + 1) % m = 1 := by
          rw [Nat.add_mod_left, Nat.mod_eq_of_lt (by omega)]
        simp only [e]
        rw [hm2]; exact nbw_one hwb
  have hpre : loops nbr v m = Φ ⁻¹' (S : Set (Fin (m + 2) → V)) := by
    ext f
    simp only [Set.mem_preimage, hS, coe_biUnion, coe_filter, Set.mem_iUnion, Set.mem_setOf_eq,
      mem_coe, exists_prop]
    -- everything in terms of `g n = f (n mod m)`
    set g : ℕ → V := fun n => f ⟨n % m, Nat.mod_lt _ hm0⟩ with hgdef
    have gper : ∀ n, g (n + m) = g n := by intro n; simp [hgdef, Nat.add_mod_right]
    have gm : g m = g 0 := by simpa using gper 0
    have gm1 : g (m + 1) = g 1 := by rw [add_comm]; exact gper 1
    have gf : ∀ i : Fin m, f i = g i.val := by intro i; simp [hgdef, Nat.mod_eq_of_lt i.isLt]
    have gf1 : ∀ i : Fin m, f (i + 1) = g (i.val + 1) := by
      intro i; simp only [hgdef]; congr 1; ext; exact fin_val_add_one i
    have gf2 : ∀ i : Fin m, f (i + 2) = g (i.val + 2) := by
      intro i; simp only [hgdef]; congr 1; ext; exact fin_val_add_two i
    have hloop : f ∈ loops nbr v m ↔
        g 0 = v ∧ ∀ n, n < m → g (n + 1) ∈ nbr (g n) ∧ g (n + 2) ≠ g n := by
      simp only [loops, Set.mem_setOf_eq]
      constructor
      · rintro ⟨h0, h⟩
        refine ⟨by rw [← h0, gf]; rfl, fun n hn => ?_⟩
        have := h ⟨n, hn⟩
        rwa [gf1, gf2, gf] at this
      · rintro ⟨h0, h⟩
        refine ⟨by rw [gf]; exact h0, fun i => ?_⟩
        rw [gf1, gf2, gf]
        exact h i.val i.isLt
    rw [hloop]
    have hΦg : ∀ n (h : n < m + 2), Φ f ⟨n, h⟩ = g n := fun _ _ => rfl
    constructor
    · rintro ⟨h0, h⟩
      refine ⟨g 1, ?_, ?_, ?_, ?_⟩
      · rw [← h0]; exact (h 0 hm0).1
      · rw [mem_nbw]
        refine ⟨by rw [show (0 : Fin (m + 2)) = ⟨0, by omega⟩ from rfl, hΦg]; exact h0,
          by rw [show (1 : Fin (m + 2)) = ⟨1, by omega⟩ from rfl, hΦg], ?_⟩
        intro i hi
        simp only [hΦg]
        refine ⟨?_, (h i (by omega)).2⟩
        rcases Nat.lt_or_ge (i + 1) m with h' | h'
        · exact (h (i + 1) h').1
        · have e1 : i + 1 = m := by omega
          have e2 : i + 2 = m + 1 := by omega
          rw [e1, e2, gm, gm1]
          exact (h 0 hm0).1
      · rw [hΦg, gm]; exact h0
      · rw [hΦg, gm1]
    · rintro ⟨b, hb, hw, hm1, hm2⟩
      rw [mem_nbw] at hw
      obtain ⟨h0, h1, hrest⟩ := hw
      rw [show (0 : Fin (m + 2)) = ⟨0, by omega⟩ from rfl, hΦg] at h0
      rw [show (1 : Fin (m + 2)) = ⟨1, by omega⟩ from rfl, hΦg] at h1
      refine ⟨h0, fun n hn => ?_⟩
      have hr := hrest n (by omega)
      simp only [hΦg] at hr
      refine ⟨?_, hr.2⟩
      rcases n with _ | n
      · rw [h0, h1]; exact hb
      · exact (hrest n (by omega)).1
  refine ⟨?_, ?_⟩
  · rw [hpre]; exact S.finite_toSet.preimage hΦ.injOn
  · rw [hpre, Set.ncard_preimage_of_injective_subset_range hΦ hrange, Set.ncard_coe_finset, hcard]

end LoopEqualityProof.Graph
