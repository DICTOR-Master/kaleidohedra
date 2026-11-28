module

public import Mathlib
public import LoopEquality.ShapeVal

@[expose] public section

/-!
# Arc lengths at l = 16: only 2 and 4

A far arc between two end atoms has an even number of edges (each bond changes the height `2 j + u` by one), and at
least two when its ends differ. So in a pair of arcs with 6 edges in all, the lengths are 2 and 4; the sums of
`ArcCounts` reduce to these two terms (`wRootL_eq`, `meetCountL_eq`), which is what the kernel evaluates.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

def ht (y : Atom) : ℤ := 2 * y.1 + (y.2.2.val : ℤ)

theorem bond_ht {σ : ℤ → ZMod 3} {x y : Atom} (h : Bond σ x y) : ht y = ht x + 1 ∨ ht y = ht x - 1 := by
  obtain ⟨-, -, hb⟩ := h
  obtain ⟨j, p, u⟩ := x
  obtain ⟨j', p', u'⟩ := y
  simp only [ht] at *
  rcases hb with ⟨rfl, -, hu⟩ | ⟨rfl, rfl, rfl, -⟩ | ⟨rfl, rfl, rfl, -⟩
  · fin_cases u <;> fin_cases u' <;> simp_all
  · left; simp; ring
  · right; simp; ring

theorem chain_parity {σ : ℤ → ZMod 3} : ∀ (l : List Atom) (hne : l ≠ []), BondChain σ l →
    (ht (l.head hne) - ht (l.getLast hne)) % 2 = ((l.length - 1 : ℕ) : ℤ) % 2
  | [x], _, _ => by simp
  | x :: z :: t, _, hc => by
    have ih := chain_parity (z :: t) (List.cons_ne_nil _ _) hc.2
    have hlast : (x :: z :: t).getLast (List.cons_ne_nil _ _) = (z :: t).getLast (List.cons_ne_nil _ _) :=
      List.getLast_cons _
    rw [hlast]
    simp only [List.head_cons, List.length_cons] at ih ⊢
    rcases bond_ht hc.1 with h | h <;> push_cast at ih ⊢ <;> omega

theorem farPaths_even {τ : ℤ → ZMod 3} {k : ℤ} {a b : ℤ × ℤ} {i : ℕ} {l : List Atom} (hl : l ∈ FarPaths τ k a b i) :
    i % 2 = 0 := by
  obtain ⟨hh, hlast, -, hlen, hb, -⟩ := hl
  have hne : l ≠ [] := by rintro rfl; simp at hh
  have hc : BondChain τ l := (bondChain_iff_edges l).mpr hb
  have := chain_parity l hne hc
  rw [List.head?_eq_head hne] at hh; rw [List.getLast?_eq_getLast hne] at hlast
  rw [Option.some.inj hh, Option.some.inj hlast, hlen] at this
  simp [ht, upA] at this; omega

theorem farPaths_pos {τ : ℤ → ZMod 3} {k : ℤ} {a b : ℤ × ℤ} (hab : a ≠ b) {l : List Atom}
    (hl : l ∈ FarPaths τ k a b 0) : False := by
  have := farPaths_len hab hl
  rw [hl.2.2.2.1] at this; omega

theorem arcList_nil {τ : ℤ → ZMod 3} {k : ℤ} {a b : ℤ × ℤ} (hab : a ≠ b) {i : ℕ} (hi : i % 2 = 1 ∨ i = 0) :
    arcList τ k a b i = [] := by
  apply List.eq_nil_iff_forall_not_mem.mpr
  intro l hl
  rw [mem_arcList] at hl
  rcases hi with h | rfl
  · have := farPaths_even hl; omega
  · exact farPaths_pos hab hl

/-- The weighted root count over the arc lengths 2 and 4. -/
def wRoot4 (τ : ℤ → ZMod 3) (k : ℤ) (a b c d : ℤ × ℤ) (w : Atom) : ℤ :=
  ([2, 4].map (fun i => ((((arcList τ k a b i) ×ˢ (arcList τ k c d (6 - i))).filter
    (fun x => disjB x.1 x.2)).map (fun x => ((x.1 ++ x.2).countP (typB w) : ℤ))).sum)).sum

def meet4 (τ : ℤ → ZMod 3) (k : ℤ) (a b c d : ℤ × ℤ) : ℤ :=
  ([2, 4].map (fun i => ((((arcList τ k a b i) ×ˢ (arcList τ k c d (6 - i))).filter
    (fun x => !disjB x.1 x.2)).length : ℤ))).sum

theorem wRootL_eq {τ : ℤ → ZMod 3} {k : ℤ} {a b c d : ℤ × ℤ} (hab : a ≠ b) (hcd : c ≠ d) (w : Atom) :
    wRootL τ k a b c d 6 w = wRoot4 τ k a b c d w := by
  unfold wRootL wRoot4
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, List.map_cons, List.map_nil, List.sum_cons,
    List.sum_nil]
  rw [arcList_nil hab (Or.inr rfl), arcList_nil hab (by decide : 1 % 2 = 1 ∨ 1 = 0),
    arcList_nil hab (by decide : 3 % 2 = 1 ∨ 3 = 0), arcList_nil hcd (by decide : (6 - 5) % 2 = 1 ∨ 6 - 5 = 0),
    arcList_nil hcd (by decide : (6 - 6) % 2 = 1 ∨ 6 - 6 = 0)]
  simp

theorem meetCountL_eq {τ : ℤ → ZMod 3} {k : ℤ} {a b c d : ℤ × ℤ} (hab : a ≠ b) (hcd : c ≠ d) :
    meetCountL τ k a b c d 6 = meet4 τ k a b c d := by
  unfold meetCountL meet4
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, List.map_cons, List.map_nil, List.sum_cons,
    List.sum_nil]
  rw [arcList_nil hab (Or.inr rfl), arcList_nil hab (by decide : 1 % 2 = 1 ∨ 1 = 0),
    arcList_nil hab (by decide : 3 % 2 = 1 ∨ 3 = 0), arcList_nil hcd (by decide : (6 - 5) % 2 = 1 ∨ 6 - 5 = 0),
    arcList_nil hcd (by decide : (6 - 6) % 2 = 1 ∨ 6 - 6 = 0)]
  simp

end LoopEqualityProof
