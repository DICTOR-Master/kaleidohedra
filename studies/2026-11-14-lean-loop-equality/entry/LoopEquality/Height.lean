module

public import Mathlib
public import LoopEquality.ArcLen

@[expose] public section

/-!
# Height along a path; arcs of at most four edges stay in two bilayers

With Claude (Anthropic).
-/

namespace LoopEqualityProof

theorem bondChain_prefix {σ : ℤ → ZMod 3} : ∀ (A B : List Atom), BondChain σ (A ++ B) → BondChain σ A
  | [], _, _ => trivial
  | [_], _, _ => trivial
  | x :: y :: t, B, h => ⟨h.1, bondChain_prefix (y :: t) B h.2⟩

theorem chain_ht_diff {σ : ℤ → ZMod 3} : ∀ (l : List Atom) (hne : l ≠ []), BondChain σ l →
    |ht (l.head hne) - ht (l.getLast hne)| ≤ (l.length - 1 : ℕ)
  | [x], _, _ => by simp
  | x :: z :: t, _, hc => by
    have ih := chain_ht_diff (z :: t) (List.cons_ne_nil _ _) hc.2
    have hlast : (x :: z :: t).getLast (List.cons_ne_nil _ _) = (z :: t).getLast (List.cons_ne_nil _ _) :=
      List.getLast_cons _
    rw [hlast]
    simp only [List.head_cons, List.length_cons] at ih ⊢
    rw [abs_le] at ih ⊢
    rcases bond_ht hc.1 with h | h <;> push_cast at ih ⊢ <;> constructor <;> omega

/-- **An atom of an arc with `i` edges is at most `i / 2` levels above its ends.** -/
theorem path_ht {τ : ℤ → ZMod 3} {k : ℤ} {a b : ℤ × ℤ} {i : ℕ} {l : List Atom} (hl : l ∈ FarPaths τ k a b i)
    {y : Atom} (hy : y ∈ l) : 2 * (ht y - ht (upA k a)) ≤ i := by
  obtain ⟨hh, hlast, -, hlen, hb, -⟩ := hl
  have hc : BondChain τ l := (bondChain_iff_edges l).mpr hb
  obtain ⟨A, B, rfl⟩ := List.append_of_mem hy
  -- the part up to y
  have h1 : ht y - ht (upA k a) ≤ A.length := by
    have hc1 : BondChain τ (A ++ [y]) := bondChain_prefix (A ++ [y]) B (by simpa using hc)
    have hne : A ++ [y] ≠ [] := by simp
    have d := chain_ht_diff _ hne hc1
    have hlast1 : (A ++ [y]).getLast hne = y := by simp
    have hhead1 : (A ++ [y]).head hne = upA k a := by
      cases A with
      | nil => simp at hh ⊢; exact hh
      | cons z A' => simp at hh ⊢; exact hh
    rw [hlast1, hhead1, abs_le] at d
    simp at d; omega
  -- the part from y
  have h2 : ht y - ht (upA k b) ≤ B.length := by
    have hc2 : BondChain τ (y :: B) := bondChain_append_right A (y :: B) hc
    have d := chain_ht_diff (y :: B) (List.cons_ne_nil _ _) hc2
    have hl2 : (y :: B).getLast (List.cons_ne_nil _ _) = upA k b := by
      have : (A ++ y :: B).getLast? = (y :: B).getLast? := by
        rw [List.getLast?_append, List.getLast?_eq_getLast (List.cons_ne_nil _ _)]; rfl
      rw [this, List.getLast?_eq_getLast (List.cons_ne_nil _ _)] at hlast
      exact Option.some.inj hlast
    rw [hl2, abs_le] at d
    simp at d; omega
  have hab : ht (upA k a) = ht (upA k b) := by simp [ht, upA]
  simp at hlen
  omega

/-- Atoms of arcs with at most four edges lie in bilayers `k` and `k + 1`. -/
theorem arc_layer {τ : ℤ → ZMod 3} {k : ℤ} {a b : ℤ × ℤ} {i : ℕ} (hi : i ≤ 4) {l : List Atom}
    (hl : l ∈ FarPaths τ k a b i) {y : Atom} (hy : y ∈ l) : k ≤ y.1 ∧ y.1 ≤ k + 1 := by
  have h := path_ht hl hy
  have hfar := hl.2.2.2.2.2 y hy
  have hu : (y.2.2.val : ℤ) ≤ 1 := by have := y.2.2.isLt; omega
  have hu0 : (0 : ℤ) ≤ y.2.2.val := by positivity
  simp only [ht, upA] at h
  unfold IsFar at hfar
  constructor
  · rcases hfar with h1 | ⟨h1, -⟩ <;> omega
  · simp at h; omega

end LoopEqualityProof
