module

public import Mathlib
public import LoopEquality.Path

@[expose] public section

/-!
# A verified enumeration of far paths

`nbrs σ w`: the bonded neighbours of `w`, as an explicit list; `ext σ k n p`: all extensions of the path `p`
(head = its newest atom) by `n` new far atoms, each bonded to the one before and new. These are computable, so the
kernel can evaluate them on concrete stackings; `mem_ext` proves they list exactly the simple far paths.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

instance bondDec (σ : ℤ → ZMod 3) (v w : Atom) : Decidable (Bond σ v w) := by
  unfold Bond IsSite; infer_instance

instance isFarDec (k : ℤ) (v : Atom) : Decidable (IsFar k v) := by unfold IsFar; infer_instance

def svList : List (ℤ × ℤ) := [(1, 1), (-2, 1), (1, -2), (-1, -1), (2, -1), (-1, 2)]

theorem mem_svList {d : ℤ × ℤ} : d ∈ svList ↔ d ∈ shortVecs := by simp [svList, shortVecs]

/-- The candidate neighbours of `w`: its vertical partner, and the six slanted atoms above and below. -/
def cand (w : Atom) : List Atom :=
  (w.1, w.2.1, 1 - w.2.2) ::
    (svList.map (fun d => (w.1 + 1, w.2.1 + d, (0 : Fin 2))) ++ svList.map (fun d => (w.1 - 1, w.2.1 - d, (1 : Fin 2))))

def nbrs (σ : ℤ → ZMod 3) (w : Atom) : List Atom := (cand w).filter (fun x => decide (Bond σ w x))

theorem bond_mem_cand {σ : ℤ → ZMod 3} {w x : Atom} (h : Bond σ w x) : x ∈ cand w := by
  obtain ⟨-, -, hb⟩ := h
  obtain ⟨j, p, u⟩ := w
  obtain ⟨j', p', u'⟩ := x
  simp only at hb
  unfold cand
  rcases hb with ⟨rfl, rfl, hu⟩ | ⟨rfl, -, rfl, hd⟩ | ⟨rfl, rfl, rfl, hd⟩
  · apply List.mem_cons.mpr; left
    have : u' = 1 - u := by fin_cases u <;> fin_cases u' <;> simp_all <;> decide
    rw [this]
  · apply List.mem_cons_of_mem; apply List.mem_append_left
    exact List.mem_map.mpr ⟨p' - p, mem_svList.mpr hd, by simp⟩
  · apply List.mem_cons_of_mem; apply List.mem_append_right
    exact List.mem_map.mpr ⟨p - p', mem_svList.mpr hd, by simp⟩

theorem mem_nbrs {σ : ℤ → ZMod 3} {w x : Atom} : x ∈ nbrs σ w ↔ Bond σ w x := by
  simp only [nbrs, List.mem_filter, decide_eq_true_eq]
  exact ⟨fun h => h.2, fun h => ⟨bond_mem_cand h, h⟩⟩

/-! ## Chains of bonds -/

def BondChain (σ : ℤ → ZMod 3) : List Atom → Prop
  | x :: y :: t => Bond σ x y ∧ BondChain σ (y :: t)
  | _ => True

theorem bondChain_cons2 {σ : ℤ → ZMod 3} {x y : Atom} {t : List Atom} :
    BondChain σ (x :: y :: t) ↔ Bond σ x y ∧ BondChain σ (y :: t) := Iff.rfl

theorem bondChain_append_right {σ : ℤ → ZMod 3} : ∀ (q m : List Atom), BondChain σ (q ++ m) → BondChain σ m
  | [], m, h => h
  | [x], [], _ => trivial
  | [x], y :: t, h => h.2
  | x :: y :: q, m, h => bondChain_append_right (y :: q) m h.2

theorem bondChain_iff_edges {σ : ℤ → ZMod 3} : ∀ l : List Atom, BondChain σ l ↔ ∀ e ∈ pathEdges l, BondS σ e
  | [] => by simp [BondChain, pathEdges]
  | [x] => by simp [BondChain, pathEdges]
  | x :: y :: t => by
    rw [bondChain_cons2, bondChain_iff_edges (y :: t), pathEdges_cons2]
    simp only [Finset.mem_insert, forall_eq_or_imp, bondS_mk]

/-! ## Extending paths -/

/-- All extensions of `p` (newest atom first) by `n` new far atoms, each bonded to the previous one. -/
def ext (σ : ℤ → ZMod 3) (k : ℤ) : ℕ → List Atom → List (List Atom)
  | 0, p => [p]
  | n + 1, [] => []
  | n + 1, h :: r => (nbrs σ h).flatMap (fun x => if IsFar k x ∧ x ∉ h :: r then ext σ k n (x :: h :: r) else [])

/-- What `ext` lists: the far, new, bonded extensions. -/
def ExtSpec (σ : ℤ → ZMod 3) (k : ℤ) (n : ℕ) (p l : List Atom) : Prop :=
  ∃ q : List Atom, l = q ++ p ∧ q.length = n ∧ l.Nodup ∧ (∀ x ∈ q, IsFar k x) ∧ BondChain σ l

theorem mem_ext {σ : ℤ → ZMod 3} {k : ℤ} : ∀ (n : ℕ) (p : List Atom), p ≠ [] → p.Nodup → BondChain σ p →
    ∀ l, l ∈ ext σ k n p ↔ ExtSpec σ k n p l
  | 0, p, _, hnd, hc, l => by
    simp only [ext, List.mem_singleton, ExtSpec]
    constructor
    · rintro rfl; exact ⟨[], rfl, rfl, hnd, by simp, hc⟩
    · rintro ⟨q, rfl, hq, -, -, -⟩; rw [List.length_eq_zero_iff.mp hq]; rfl
  | n + 1, [], hne, _, _, _ => absurd rfl hne
  | n + 1, h :: r, _, hnd, hc, l => by
    simp only [ext, List.mem_flatMap]
    constructor
    · rintro ⟨x, hx, hl⟩
      split_ifs at hl with hxf
      · have hb := mem_nbrs.mp hx
        have hnd' : (x :: h :: r).Nodup := List.nodup_cons.mpr ⟨hxf.2, hnd⟩
        have hc' : BondChain σ (x :: h :: r) := ⟨bond_symm hb, hc⟩
        obtain ⟨q, rfl, hq, hnd'', hf, hc''⟩ := (mem_ext n (x :: h :: r) (List.cons_ne_nil _ _) hnd' hc' l).mp hl
        refine ⟨q ++ [x], by simp, by simp [hq], by simpa using hnd'', ?_, by simpa using hc''⟩
        intro y hy
        rcases List.mem_append.mp hy with hy | hy
        · exact hf y hy
        · rw [List.mem_singleton.mp hy]; exact hxf.1
      · simp at hl
    · rintro ⟨q, rfl, hq, hnd', hf, hc'⟩
      obtain ⟨q', x, rfl⟩ : ∃ q' x, q = q' ++ [x] := by
        rcases List.eq_nil_or_concat q with h0 | ⟨q', x, h0⟩
        · rw [h0] at hq; simp at hq
        · exact ⟨q', x, by rw [h0, List.concat_eq_append]⟩
      have hrest : (q' ++ [x]) ++ h :: r = q' ++ (x :: h :: r) := by simp
      rw [hrest] at hnd' hc'
      have hcx : BondChain σ (x :: h :: r) := bondChain_append_right q' _ hc'
      have hxn : x ∉ h :: r := by
        have := (List.nodup_append.mp hnd').2.1
        exact (List.nodup_cons.mp this).1
      have hxf : IsFar k x := hf x (by simp)
      refine ⟨x, mem_nbrs.mpr (bond_symm hcx.1), ?_⟩
      rw [if_pos ⟨hxf, hxn⟩]
      have hnd'' : (x :: h :: r).Nodup := (List.nodup_append.mp hnd').2.1
      refine (mem_ext n (x :: h :: r) (List.cons_ne_nil _ _) hnd'' hcx _).mpr
        ⟨q', by rw [hrest], by simpa using hq, by rw [hrest]; exact hnd', fun y hy => hf y (by simp [hy]),
          by rw [hrest]; exact hc'⟩

/-! ## No path is listed twice -/

theorem cand_nodup (w : Atom) : (cand w).Nodup := by
  obtain ⟨j, p, u⟩ := w
  unfold cand
  simp only
  have hinj1 : Function.Injective (fun d : ℤ × ℤ => ((j + 1, p + d, (0 : Fin 2)) : Atom)) := by
    intro d e h; simpa using h
  have hinj2 : Function.Injective (fun d : ℤ × ℤ => ((j - 1, p - d, (1 : Fin 2)) : Atom)) := by
    intro d e h; simpa using h
  have hsv : svList.Nodup := by decide
  refine List.nodup_cons.mpr ⟨?_, List.nodup_append.mpr ⟨hsv.map hinj1, hsv.map hinj2, ?_⟩⟩
  · simp only [List.mem_append, List.mem_map, not_or, not_exists, not_and]
    constructor <;> intro d _ h <;> simp only [Prod.mk.injEq] at h <;> omega
  · intro x hx y hy hxy
    obtain ⟨d, -, rfl⟩ := List.mem_map.mp hx
    obtain ⟨e, -, rfl⟩ := List.mem_map.mp hy
    simp only [Prod.mk.injEq] at hxy; omega

theorem nbrs_nodup (σ : ℤ → ZMod 3) (w : Atom) : (nbrs σ w).Nodup := (cand_nodup w).filter _

theorem ext_nodup {σ : ℤ → ZMod 3} {k : ℤ} : ∀ (n : ℕ) (p : List Atom), p ≠ [] → p.Nodup → BondChain σ p →
    (ext σ k n p).Nodup
  | 0, p, _, _, _ => List.nodup_singleton _
  | n + 1, [], hne, _, _ => absurd rfl hne
  | n + 1, h :: r, _, hnd, hc => by
    simp only [ext]
    refine List.nodup_flatMap.mpr ⟨?_, ?_⟩
    · intro x hx
      split_ifs with hxf
      · exact ext_nodup n (x :: h :: r) (List.cons_ne_nil _ _) (List.nodup_cons.mpr ⟨hxf.2, hnd⟩)
          ⟨bond_symm (mem_nbrs.mp hx), hc⟩
      · exact List.nodup_nil
    · refine (nbrs_nodup σ h).imp_of_mem ?_
      intro x y hx hy hxy
      simp only [Function.onFun]
      split_ifs with h1 h2 h2
      · rw [List.disjoint_left]
        intro l hl1 hl2
        have s1 := (mem_ext n (x :: h :: r) (List.cons_ne_nil _ _) (List.nodup_cons.mpr ⟨h1.2, hnd⟩)
          ⟨bond_symm (mem_nbrs.mp hx), hc⟩ l).mp hl1
        have s2 := (mem_ext n (y :: h :: r) (List.cons_ne_nil _ _) (List.nodup_cons.mpr ⟨h2.2, hnd⟩)
          ⟨bond_symm (mem_nbrs.mp hy), hc⟩ l).mp hl2
        obtain ⟨q, e1, hq, -⟩ := s1
        obtain ⟨q', e2, hq', -⟩ := s2
        have := List.append_inj (e1.symm.trans e2) (hq.trans hq'.symm)
        exact hxy (List.cons.inj this.2).1
      all_goals simp

/-- **Arcs from the enumeration.** -/
theorem fc_two_enum {τ : ℤ → ZMod 3} {k : ℤ} {a b : ℤ × ℤ} (hab : a ≠ b) (i : ℕ) :
    Fc τ k {a, b} (pr2 a b) i = ((ext τ k i [upA k b]).filter (fun l => l.head? == some (upA k a))).length := by
  rw [fc_two_paths hab]
  have hnd := ext_nodup (σ := τ) (k := k) i [upA k b] (List.cons_ne_nil _ _) (List.nodup_singleton _) trivial
  rw [← List.toFinset_card_of_nodup (hnd.filter _), ← Set.ncard_coe_finset]
  congr 2; ext l
  simp only [FarPaths, Set.mem_setOf_eq, List.coe_toFinset, List.mem_filter, beq_iff_eq]
  rw [mem_ext i [upA k b] (List.cons_ne_nil _ _) (List.nodup_singleton _) trivial]
  constructor
  · rintro ⟨hh, hl, hnd', hlen, hbond, hfar⟩
    obtain ⟨q, rfl⟩ : ∃ q, l = q ++ [upA k b] := by
      rcases List.eq_nil_or_concat l with h0 | ⟨q, x, h0⟩
      · rw [h0] at hh; simp at hh
      · refine ⟨q, ?_⟩; rw [h0] at hl ⊢; simp at hl; rw [List.concat_eq_append, hl]
    refine ⟨⟨q, rfl, by simpa using hlen, hnd', fun x hx => hfar x (by simp [hx]), (bondChain_iff_edges _).mpr hbond⟩, hh⟩
  · rintro ⟨⟨q, rfl, hq, hnd', hfar, hc⟩, hh⟩
    refine ⟨hh, by simp, hnd', by simp [hq], (bondChain_iff_edges _).mp hc, ?_⟩
    intro x hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hfar x hx
    · rw [List.mem_singleton.mp hx]; exact isFar_upA k b

end LoopEqualityProof
