module

public import Mathlib
public import LoopEquality.Split
public import LoopEquality.Degree
public import LoopEquality.FourPoint

@[expose] public section

/-!
# Arcs are simple paths

The edges of a simple path `a = x₀, x₁, …, xₙ = z` (`n ≥ 1`) form a linkage on `{a, z}` with `n` edges in which `a`
and `z` are joined; conversely every such linkage is the edge set of exactly one simple path from `a`.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

open Classical

/-- The edges of a path given by its list of atoms. -/
def pathEdges : List Atom → Finset (Sym2 Atom)
  | a :: b :: t => insert s(a, b) (pathEdges (b :: t))
  | _ => ∅

theorem pathEdges_cons2 (a b : Atom) (t : List Atom) : pathEdges (a :: b :: t) = insert s(a, b) (pathEdges (b :: t)) := rfl

theorem atom_of_pathEdges : ∀ {l : List Atom} {e : Sym2 Atom}, e ∈ pathEdges l → ∀ w ∈ e, w ∈ l
  | [], e, he => by simp [pathEdges] at he
  | [_], e, he => by simp [pathEdges] at he
  | a :: b :: t, e, he => by
    intro w hw
    rw [pathEdges_cons2, Finset.mem_insert] at he
    rcases he with rfl | he
    · rcases Sym2.mem_iff.mp hw with rfl | rfl <;> simp
    · exact List.mem_cons_of_mem _ (atom_of_pathEdges he w hw)

theorem degS_pathEdges_out {l : List Atom} {w : Atom} (hw : w ∉ l) : degS (pathEdges l) w = 0 := by
  unfold degS; rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
  intro e he hwe; exact hw (atom_of_pathEdges he w hwe)

/-- **A simple path is an arc.** -/
theorem path_linkage : ∀ (t : List Atom) (a b : Atom), (a :: b :: t).Nodup →
    IsLinkageOn (pathEdges (a :: b :: t)) {a, (b :: t).getLast (List.cons_ne_nil _ _)} ∧
      (pathEdges (a :: b :: t)).card = t.length + 1 ∧
      Conn (pathEdges (a :: b :: t)) a ((b :: t).getLast (List.cons_ne_nil _ _))
  | [], a, b, hnd => by
    have hab : a ≠ b := by intro h; simp [h] at hnd
    have hE : pathEdges [a, b] = {s(a, b)} := by simp [pathEdges]
    simp only [List.getLast_singleton]
    rw [hE]
    refine ⟨⟨?_, ?_, ?_, ?_⟩, by simp, ?_⟩
    · intro w hw
      unfold degS
      rw [Finset.card_eq_one]
      refine ⟨s(a, b), ?_⟩
      ext e; simp only [Finset.mem_filter, Finset.mem_singleton]
      constructor
      · rintro ⟨h, -⟩; exact h
      · rintro rfl
        refine ⟨rfl, ?_⟩
        rcases Finset.mem_insert.mp hw with rfl | hw
        · exact Sym2.mem_mk_left _ _
        · rw [Finset.mem_singleton.mp hw]; exact Sym2.mem_mk_right _ _
    · intro w hw; left
      unfold degS; rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
      intro e he hwe
      rw [Finset.mem_singleton.mp he] at hwe
      rcases Sym2.mem_iff.mp hwe with rfl | rfl <;> simp at hw
    · intro G hG hne hcl
      obtain ⟨e, he⟩ := hne
      have he' := Finset.mem_singleton.mp (hG he)
      have : degS G a = 1 := by
        unfold degS; rw [Finset.card_eq_one]
        refine ⟨e, ?_⟩
        ext f; simp only [Finset.mem_filter, Finset.mem_singleton]
        constructor
        · rintro ⟨hf, -⟩; rw [Finset.mem_singleton.mp (hG hf), he']
        · rintro rfl; exact ⟨he, by rw [he']; exact Sym2.mem_mk_left _ _⟩
      have h2 := hcl a; rw [this] at h2; exact (Nat.not_even_one) h2
    · intro e he; rw [Finset.mem_singleton.mp he]; exact Sym2.mk_isDiag_iff.not.mpr hab
    · exact Relation.ReflTransGen.single ⟨by simp, hab⟩
  | c :: t', a, b, hnd => by
    have hnd' : (b :: c :: t').Nodup := (List.nodup_cons.mp hnd).2
    have ha : a ∉ b :: c :: t' := (List.nodup_cons.mp hnd).1
    obtain ⟨hL, hcard, hconn⟩ := path_linkage t' b c hnd'
    set z := (c :: t').getLast (List.cons_ne_nil _ _) with hz
    have hlast : (b :: c :: t').getLast (List.cons_ne_nil _ _) = z := by rw [List.getLast_cons]
    rw [hlast]
    set L' := pathEdges (b :: c :: t')
    have hzmem : z ∈ c :: t' := List.getLast_mem _
    have hbz : b ≠ z := fun h => (List.nodup_cons.mp hnd').1 (h ▸ hzmem)
    have haz : a ≠ z := fun h => ha (List.mem_cons_of_mem _ (h ▸ hzmem))
    have hab : a ≠ b := fun h => ha (h ▸ List.mem_cons_self)
    have hnot : s(a, b) ∉ L' := fun h => ha (atom_of_pathEdges h a (Sym2.mem_mk_left _ _))
    have hdeg : ∀ w, degS (pathEdges (a :: b :: c :: t')) w = degS L' w + (if w ∈ s(a, b) then 1 else 0) :=
      fun w => by rw [pathEdges_cons2]; exact degS_insert L' hnot w
    have ha0 : degS L' a = 0 := degS_pathEdges_out ha
    refine ⟨⟨?_, ?_, ?_, ?_⟩, ?_, ?_⟩
    · intro w hw
      rw [hdeg]
      rcases Finset.mem_insert.mp hw with rfl | hw
      · rw [ha0, if_pos (Sym2.mem_mk_left _ _)]
      · rw [Finset.mem_singleton.mp hw, hL.1 z (by simp)]
        rw [if_neg]; intro hm
        rcases Sym2.mem_iff.mp hm with h | h
        · exact haz h.symm
        · exact hbz h.symm
    · intro w hw
      rw [hdeg]
      have hwa : w ≠ a := fun h => hw (by simp [h])
      have hwz : w ≠ z := fun h => hw (by simp [h])
      by_cases hwb : w = b
      · subst hwb
        rw [hL.1 w (by simp), if_pos (Sym2.mem_mk_right _ _)]; right; rfl
      · rw [if_neg (by intro hm; rcases Sym2.mem_iff.mp hm with h | h <;> contradiction), add_zero]
        exact hL.2.1 w (by simp [hwb, hwz])
    · intro G hG hne hcl
      have hGa : degS G a = 0 := by
        have h1 := degS_mono hG a
        rw [hdeg, ha0, if_pos (Sym2.mem_mk_left _ _)] at h1
        rcases Nat.le_one_iff_eq_zero_or_eq_one.mp h1 with h | h
        · exact h
        · have := hcl a; rw [h] at this; exact absurd this Nat.not_even_one
      have hsub : G ⊆ L' := by
        intro e he
        rcases Finset.mem_insert.mp (hG he) with rfl | h
        · exact absurd hGa (degS_pos_of' he (Sym2.mem_mk_left a b)).ne'
        · exact h
      exact hL.2.2.1 G hsub hne hcl
    · intro e he
      rw [pathEdges_cons2] at he
      rcases Finset.mem_insert.mp he with rfl | h
      · exact Sym2.mk_isDiag_iff.not.mpr hab
      · exact hL.2.2.2 e h
    · rw [pathEdges_cons2, Finset.card_insert_of_notMem hnot, hcard]; simp
    · rw [pathEdges_cons2]
      exact Relation.ReflTransGen.head ⟨Finset.mem_insert_self _ _, hab⟩ (conn_mono (Finset.subset_insert _ _) hconn)

/-! ## Every arc is a simple path -/

/-- In a linkage on two ends, the ends are joined. -/
theorem conn_two_ends {F : Finset (Sym2 Atom)} {x y : Atom} (hF : IsLinkageOn F {x, y}) (hxy : x ≠ y) :
    Conn F x y := by
  have hle : ∀ w, degS F w ≤ 2 := by
    intro w
    by_cases hw : w ∈ ({x, y} : Finset Atom)
    · rw [hF.1 w hw]; omega
    · rcases hF.2.1 w hw with h | h <;> omega
  obtain ⟨z, hzx, hz1, hc⟩ := partner_exists F hF.2.2.2 hle (hF.1 x (by simp))
  by_cases hz : z ∈ ({x, y} : Finset Atom)
  · rcases Finset.mem_insert.mp hz with rfl | hz
    · exact absurd rfl hzx
    · rwa [Finset.mem_singleton.mp hz] at hc
  · rcases hF.2.1 z hz with h | h <;> omega

theorem mem_path_deg : ∀ {l : List Atom}, 2 ≤ l.length → ∀ {w : Atom}, w ∈ l → 0 < degS (pathEdges l) w
  | a :: b :: t, _, w, hw => by
    rw [pathEdges_cons2]
    rcases List.mem_cons.mp hw with rfl | hw
    · exact degS_pos_of' (Finset.mem_insert_self _ _) (Sym2.mem_mk_left _ _)
    · rcases List.mem_cons.mp hw with rfl | hw
      · exact degS_pos_of' (Finset.mem_insert_self _ _) (Sym2.mem_mk_right _ _)
      · cases t with
        | nil => simp at hw
        | cons c t' =>
          have := mem_path_deg (l := b :: c :: t') (by simp) (List.mem_cons_of_mem _ hw)
          exact lt_of_lt_of_le this (degS_mono (Finset.subset_insert _ _) _)

/-- **Every arc is a simple path.** A linkage on two distinct ends `x, y` is the edge set of a simple path from `x`
to `y`. -/
theorem arc_to_path : ∀ (n : ℕ) (F : Finset (Sym2 Atom)) (x y : Atom), F.card = n → IsLinkageOn F {x, y} → x ≠ y →
    ∃ l : List Atom, l.head? = some x ∧ l.getLast? = some y ∧ l.Nodup ∧ 2 ≤ l.length ∧ pathEdges l = F := by
  intro n
  induction n using Nat.strong_induction_on with
  | _ n ih =>
  intro F x y hn hF hxy
  have hx1 : degS F x = 1 := hF.1 x (by simp)
  obtain ⟨e, he⟩ := Finset.card_eq_one.mp hx1
  have hmem : e ∈ F.filter (fun f => x ∈ f) := by rw [he]; exact Finset.mem_singleton_self e
  have heF : e ∈ F := (Finset.mem_filter.mp hmem).1
  have hxe : x ∈ e := (Finset.mem_filter.mp hmem).2
  obtain ⟨b, rfl⟩ : ∃ b, e = s(x, b) := by
    induction e using Sym2.ind with
    | _ u w => rcases Sym2.mem_iff.mp hxe with rfl | rfl
               · exact ⟨w, rfl⟩
               · exact ⟨u, Sym2.eq_swap⟩
  have hbx : b ≠ x := fun h => hF.2.2.2 _ heF (by rw [h]; exact Sym2.mk_isDiag_iff.mpr rfl)
  set F' := F.erase s(x, b)
  have hdeg : ∀ w, degS F' w + (if w ∈ s(x, b) then 1 else 0) = degS F w := degS_erase F heF
  have hF'x : degS F' x = 0 := by have := hdeg x; rw [if_pos (Sym2.mem_mk_left _ _), hx1] at this; omega
  have hins : insert s(x, b) F' = F := Finset.insert_erase heF
  have hcard' : F'.card + 1 = n := by rw [← hn]; exact Finset.card_erase_add_one heF
  by_cases hby : b = y
  · subst hby
    -- the rest is closed, hence empty
    have hcl : Closed F' := by
      intro w
      have := hdeg w
      by_cases hw : w ∈ ({x, b} : Finset Atom)
      · rcases Finset.mem_insert.mp hw with rfl | hw
        · rw [hF'x]; exact Even.zero
        · rw [Finset.mem_singleton.mp hw] at this ⊢
          rw [if_pos (Sym2.mem_mk_right _ _), hF.1 b (by simp)] at this
          have : degS F' b = 0 := by omega
          rw [this]; exact Even.zero
      · rw [if_neg (by intro hm; rcases Sym2.mem_iff.mp hm with rfl | rfl <;> simp at hw), add_zero] at this
        rw [this]
        rcases hF.2.1 w hw with h | h <;> rw [h]
        · exact Even.zero
        · exact even_two
    have hempty : F' = ∅ := by
      by_contra hne
      exact hF.2.2.1 F' (Finset.erase_subset _ _) (Finset.nonempty_iff_ne_empty.mpr hne) hcl
    refine ⟨[x, b], rfl, rfl, by simp [hbx.symm], by simp, ?_⟩
    rw [← hins, hempty]; simp [pathEdges]
  · -- the rest is an arc from b to y
    have hb1 : degS F' b = 1 := by
      have := hdeg b
      rw [if_pos (Sym2.mem_mk_right _ _)] at this
      have hbn : b ∉ ({x, y} : Finset Atom) := by simp [hbx, hby]
      rcases hF.2.1 b hbn with h | h
      · omega
      · omega
    have hF' : IsLinkageOn F' {b, y} := by
      refine ⟨?_, ?_, ?_, ?_⟩
      · intro w hw
        rcases Finset.mem_insert.mp hw with rfl | hw
        · exact hb1
        · rw [Finset.mem_singleton.mp hw]
          have := hdeg y
          have hyn : y ∉ s(x, b) := by
            intro hm; rcases Sym2.mem_iff.mp hm with h | h
            · exact hxy h.symm
            · exact hby h.symm
          rw [if_neg hyn, add_zero, hF.1 y (by simp)] at this
          exact this
      · intro w hw
        have := hdeg w
        by_cases hwx : w = x
        · subst hwx; left; exact hF'x
        · have hwn : w ∉ s(x, b) := by
            intro hm; rcases Sym2.mem_iff.mp hm with h | h
            · exact hwx h
            · exact hw (by simp [h])
          rw [if_neg hwn, add_zero] at this
          rw [this]; exact hF.2.1 w (by simp at hw ⊢; tauto)
      · intro G hG hne hcl; exact hF.2.2.1 G (hG.trans (Finset.erase_subset _ _)) hne hcl
      · intro e he; exact hF.2.2.2 e (Finset.mem_of_mem_erase he)
    obtain ⟨l, hh, hl, hnd, hlen, hE⟩ := ih F'.card (by omega) F' b y rfl hF' hby
    have hxl : x ∉ l := by
      intro hm
      have := mem_path_deg hlen hm
      rw [hE, hF'x] at this; omega
    obtain ⟨t, rfl⟩ : ∃ t, l = b :: t := by
      cases l with
      | nil => simp at hh
      | cons c t => simp at hh; exact ⟨t, by rw [hh]⟩
    refine ⟨x :: b :: t, rfl, ?_, List.nodup_cons.mpr ⟨hxl, hnd⟩, by simp, ?_⟩
    · rw [List.getLast?_cons_cons]; exact hl
    · rw [pathEdges_cons2, hE, hins]

/-! ## The path of an arc is unique -/

theorem pathEdges_ne_empty {l : List Atom} (h : 2 ≤ l.length) : pathEdges l ≠ ∅ := by
  match l, h with
  | a :: b :: t, _ => rw [pathEdges_cons2]; exact Finset.insert_ne_empty _ _

/-- **Uniqueness.** Two simple paths from the same atom with the same edges are equal. -/
theorem path_unique : ∀ (l₁ l₂ : List Atom) (x : Atom), l₁.head? = some x → l₂.head? = some x → l₁.Nodup → l₂.Nodup →
    2 ≤ l₁.length → 2 ≤ l₂.length → pathEdges l₁ = pathEdges l₂ → l₁ = l₂
  | y :: b₁ :: t₁, z :: b₂ :: t₂, x, h1, h2, n1, n2, _, _, hE => by
    simp only [List.head?_cons, Option.some.injEq] at h1 h2
    have hyz : z = y := h2.trans h1.symm
    rw [hyz] at n2 hE ⊢
    have hx1 : y ∉ b₁ :: t₁ := (List.nodup_cons.mp n1).1
    have hx2 : y ∉ b₂ :: t₂ := (List.nodup_cons.mp n2).1
    have hmem : s(y, b₁) ∈ pathEdges (y :: b₂ :: t₂) := by rw [← hE, pathEdges_cons2]; exact Finset.mem_insert_self _ _
    rw [pathEdges_cons2, Finset.mem_insert] at hmem
    have hb : b₁ = b₂ := by
      rcases hmem with h | h
      · rcases Sym2.eq_iff.mp h with ⟨-, h⟩ | ⟨h, -⟩
        · exact h
        · exact absurd (h ▸ List.mem_cons_self) hx2
      · exact absurd (atom_of_pathEdges h y (Sym2.mem_mk_left _ _)) hx2
    rw [← hb] at n2 hE hx2 ⊢
    have hn1 : s(y, b₁) ∉ pathEdges (b₁ :: t₁) := fun h => hx1 (atom_of_pathEdges h y (Sym2.mem_mk_left _ _))
    have hn2 : s(y, b₁) ∉ pathEdges (b₁ :: t₂) := fun h => hx2 (atom_of_pathEdges h y (Sym2.mem_mk_left _ _))
    have hE' : pathEdges (b₁ :: t₁) = pathEdges (b₁ :: t₂) := by
      have e1 := Finset.erase_insert hn1; have e2 := Finset.erase_insert hn2
      rw [pathEdges_cons2, pathEdges_cons2] at hE
      rw [← e1, ← e2, hE]
    cases t₁ with
    | nil =>
      cases t₂ with
      | nil => rfl
      | cons c t => exact absurd hE'.symm (pathEdges_ne_empty (l := b₁ :: c :: t) (by simp))
    | cons c t =>
      cases t₂ with
      | nil => exact absurd hE' (pathEdges_ne_empty (l := b₁ :: c :: t) (by simp))
      | cons c' t' =>
        have := path_unique (b₁ :: c :: t) (b₁ :: c' :: t') b₁ rfl rfl (List.nodup_cons.mp n1).2
          (List.nodup_cons.mp n2).2 (by simp) (by simp) hE'
        rw [this]

/-! ## Arcs are counted by paths -/

theorem exists_edge_of_degS' {F : Finset (Sym2 Atom)} {w : Atom} (h : 0 < degS F w) : ∃ e ∈ F, w ∈ e := by
  obtain ⟨e, he⟩ := Finset.card_pos.mp h
  exact ⟨e, (Finset.mem_filter.mp he).1, (Finset.mem_filter.mp he).2⟩

theorem path_linkage' {l : List Atom} {x y : Atom} (hlen : 2 ≤ l.length) (hnd : l.Nodup) (hh : l.head? = some x)
    (hl : l.getLast? = some y) :
    IsLinkageOn (pathEdges l) {x, y} ∧ (pathEdges l).card + 1 = l.length ∧ Conn (pathEdges l) x y := by
  match l, hlen with
  | a :: b :: t, _ =>
    simp only [List.head?_cons, Option.some.injEq] at hh
    subst hh
    have hy : (b :: t).getLast (List.cons_ne_nil _ _) = y := by
      rw [List.getLast?_cons_cons, List.getLast?_eq_getLast (List.cons_ne_nil _ _)] at hl
      exact Option.some.inj hl
    obtain ⟨h1, h2, h3⟩ := path_linkage t a b hnd
    rw [hy] at h1 h3
    exact ⟨h1, by rw [h2]; simp, h3⟩

/-- Simple far paths from `upA a` to `upA b` with `i` edges. -/
def FarPaths (τ : ℤ → ZMod 3) (k : ℤ) (a b : ℤ × ℤ) (i : ℕ) : Set (List Atom) :=
  {l | l.head? = some (upA k a) ∧ l.getLast? = some (upA k b) ∧ l.Nodup ∧ l.length = i + 1 ∧
    (∀ e ∈ pathEdges l, BondS τ e) ∧ ∀ w ∈ l, IsFar k w}

/-- **Arcs are counted by paths.** -/
theorem fc_two_paths {τ : ℤ → ZMod 3} {k : ℤ} {a b : ℤ × ℤ} (hab : a ≠ b) (i : ℕ) :
    Fc τ k {a, b} (pr2 a b) i = (FarPaths τ k a b i).ncard := by
  have hne : upA k a ≠ upA k b := upA_ne hab
  unfold Fc; congr 1; symm
  apply Set.ncard_congr (fun l _ => pathEdges l)
  · rintro l ⟨hh, hl, hnd, hlen, hb, hf⟩
    have h2 : 2 ≤ l.length := by
      rcases l with _ | ⟨x, _ | ⟨y, t⟩⟩
      · simp at hh
      · simp at hh hl; exact absurd (hh.symm.trans hl) hne
      · simp
    obtain ⟨hL, hc, hconn⟩ := path_linkage' h2 hnd hh hl
    refine ⟨⟨by rw [image_pair]; exact hL, fun e he w hw => hf w (atom_of_pathEdges he w hw), hb⟩, by omega,
      pairF_full hconn⟩
  · intro l₁ l₂ h1 h2 hE
    obtain ⟨hh1, hl1, hn1, -, -, -⟩ := h1
    obtain ⟨hh2, hl2, hn2, -, -, -⟩ := h2
    have len : ∀ l : List Atom, l.head? = some (upA k a) → l.getLast? = some (upA k b) → 2 ≤ l.length := by
      intro l hh hl
      rcases l with _ | ⟨x, _ | ⟨y, t⟩⟩
      · simp at hh
      · simp at hh hl; exact absurd (hh.symm.trans hl) hne
      · simp
    exact path_unique l₁ l₂ _ hh1 hh2 hn1 hn2 (len _ hh1 hl1) (len _ hh2 hl2) hE
  · rintro F ⟨⟨hL, hfar, hb⟩, hs, -⟩
    rw [image_pair] at hL
    obtain ⟨l, hh, hl, hnd, hlen, hE⟩ := arc_to_path F.card F _ _ rfl hL hne
    obtain ⟨-, hc, -⟩ := path_linkage' hlen hnd hh hl
    refine ⟨l, ⟨hh, hl, hnd, by rw [hE] at hc; omega, by rw [hE]; exact hb, ?_⟩, hE⟩
    intro w hw
    have := mem_path_deg hlen hw
    rw [hE] at this
    obtain ⟨e, he, hwe⟩ := exists_edge_of_degS' this
    exact hfar e he w hwe

end LoopEqualityProof
