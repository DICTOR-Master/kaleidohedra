module

public import Mathlib
public import LoopEquality.LetterLocal

@[expose] public section

/-!
# The list of shapes at l = 16 misses nothing

Every crossing set with a non-zero (6, 6) term carries a pair of far arcs (2 + 4 edges) that meet, at itself or at its
half-turn. Moving the start of the first arc to a fixed point `b₀` by a lattice vector, the pair appears in the explicit
list `candQuads`; a kernel check that every candidate's class (and its half-turn's) is in `Z` then gives completeness.

With Claude (Anthropic).
-/

namespace LoopEqualityProof

/-! ## Translating far paths by lattice vectors -/

theorem bondChain_map {σ : ℤ → ZMod 3} {t : ℤ × ℤ} (ht : GoodVec t) :
    ∀ l : List Atom, BondChain σ l → BondChain σ (l.map (posA t))
  | [], _ => trivial
  | [_], _ => trivial
  | x :: y :: r, h => by
    refine ⟨?_, bondChain_map ht (y :: r) h.2⟩
    have := bond_posA (s := 0) ⟨ht.1, ht.2⟩ h.1
    simpa using this

theorem farPaths_translate {τ : ℤ → ZMod 3} {k : ℤ} {a b : ℤ × ℤ} {i : ℕ} {t : ℤ × ℤ} (ht : GoodVec t)
    {l : List Atom} (hl : l ∈ FarPaths τ k a b i) : l.map (posA t) ∈ FarPaths τ k (a + t) (b + t) i := by
  obtain ⟨hh, hlast, hnd, hlen, hb, hf⟩ := hl
  have hinj : Function.Injective (posA t) := fun x y h => by
    have := congrArg (posA (-t)) h; rwa [posA_posA, posA_posA] at this
  refine ⟨by rw [List.head?_map, hh]; rfl, by rw [List.getLast?_map, hlast]; rfl, hnd.map hinj,
    by rw [List.length_map, hlen], (bondChain_iff_edges _).mp (bondChain_map ht l ((bondChain_iff_edges l).mpr hb)), ?_⟩
  intro y hy
  obtain ⟨z, hz, rfl⟩ := List.mem_map.mp hy
  have := hf z hz
  unfold IsFar at this ⊢; exact this

/-! ## The candidates -/

def endB (k : ℤ) (y : Atom) : Bool := y.1 == k && y.2.2 == 1
def headEnd (k : ℤ) (l : List Atom) : Bool := match l.head? with | some y => endB k y | none => false
def headPos (l : List Atom) : ℤ × ℤ := match l.head? with | some y => y.2.1 | none => (0, 0)

def offs : List ℤ := (List.range 25).map (fun n : ℕ => (n : ℤ) - 12)

/-- Points `b₀ + d` with `d` a lattice vector, `|d| ≤ 12` in both coordinates. -/
def boxPts (b₀ : ℤ × ℤ) : List (ℤ × ℤ) :=
  (offs.flatMap (fun dx => offs.map (fun dy => (b₀.1 + dx, b₀.2 + dy)))).filter
    (fun p => (p.1 - b₀.1) % 3 == 0 && (p.2 - b₀.2) % 3 == 0)

theorem mem_offs {d : ℤ} (h : |d| ≤ 12) : d ∈ offs := by
  rw [abs_le] at h
  exact List.mem_map.mpr ⟨(d + 12).toNat, List.mem_range.mpr (by omega), by omega⟩

/-- Crossing points `(a, b₀, e, f)` of meeting pairs: an arc from `b₀` to `a` and an arc from `f` to `e`. -/
def dist4B (q : (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ)) : Bool :=
  q.1 != q.2.1 && q.1 != q.2.2.1 && q.1 != q.2.2.2 && q.2.1 != q.2.2.1 && q.2.1 != q.2.2.2 && q.2.2.1 != q.2.2.2

def candQuads (τ : ℤ → ZMod 3) (k : ℤ) (b₀ : ℤ × ℤ) : List ((ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ)) :=
  ([2, 4].flatMap (fun i => ((ext τ k i [upA k b₀]).filter (headEnd k)).flatMap (fun l₁ =>
    (boxPts b₀).flatMap (fun f => ((((ext τ k (6 - i) [upA k f]).filter (headEnd k)).filter
      (fun l₂ => !disjB l₁ l₂)).map (fun l₂ => (headPos l₁, b₀, headPos l₂, f))))))).filter dist4B

def toSet (q : (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ) × (ℤ × ℤ)) : Finset (ℤ × ℤ) := {q.1, q.2.1, q.2.2.1, q.2.2.2}

theorem mem_boxPts {b₀ p : ℤ × ℤ} (h1 : |p.1 - b₀.1| ≤ 12) (h2 : |p.2 - b₀.2| ≤ 12) (h3 : (p.1 - b₀.1) % 3 = 0)
    (h4 : (p.2 - b₀.2) % 3 = 0) : p ∈ boxPts b₀ := by
  unfold boxPts
  refine List.mem_filter.mpr ⟨List.mem_flatMap.mpr ⟨p.1 - b₀.1, mem_offs h1,
    List.mem_map.mpr ⟨p.2 - b₀.2, mem_offs h2, by ext <;> simp⟩⟩, by simp [h3, h4]⟩

theorem arcList_head {τ : ℤ → ZMod 3} {k : ℤ} {a b : ℤ × ℤ} {i : ℕ} {l : List Atom} (hl : l ∈ arcList τ k a b i) :
    headEnd k l = true ∧ headPos l = a := by
  have hh := (mem_arcList.mp hl).1
  simp only [headEnd, headPos, hh, endB, upA]; simp

theorem arcList_ext {τ : ℤ → ZMod 3} {k : ℤ} {a b : ℤ × ℤ} {i : ℕ} {l : List Atom} (hl : l ∈ arcList τ k a b i) :
    l ∈ ext τ k i [upA k b] := (List.mem_filter.mp hl).1

theorem disjB_map {t : ℤ × ℤ} (l₁ l₂ : List Atom) : disjB (l₁.map (posA t)) (l₂.map (posA t)) = disjB l₁ l₂ := by
  have hinj : Function.Injective (posA t) := fun x y h => by
    have := congrArg (posA (-t)) h; rwa [posA_posA, posA_posA] at this
  unfold disjB
  rw [List.all_map]
  congr 1; funext x
  simp only [Function.comp_apply]
  congr 1
  rw [Bool.eq_iff_iff, List.contains_iff_mem, List.contains_iff_mem, List.mem_map]
  exact ⟨fun ⟨y, hy, hxy⟩ => hinj hxy ▸ hy, fun h => ⟨x, h, rfl⟩⟩

/-- **A meeting pair, moved to start at `b₀`, is a candidate.** -/
theorem meet_in_cand {τ : ℤ → ZMod 3} {k : ℤ} {a b e f b₀ : ℤ × ℤ} (hD : Dist4 a b e f) {i : ℕ} (hi : i = 2 ∨ i = 4)
    {l₁ l₂ : List Atom} (h1 : l₁ ∈ arcList τ k a b i) (h2 : l₂ ∈ arcList τ k e f (6 - i)) (hm : disjB l₁ l₂ = false)
    (ht : GoodVec (b₀ - b)) (hf3 : ((f - b).1) % 3 = 0 ∧ ((f - b).2) % 3 = 0) :
    ∃ q ∈ candQuads τ k b₀, toSet q = trP (b₀ - b) {a, b, e, f} := by
  set t := b₀ - b
  have h1' : l₁.map (posA t) ∈ arcList τ k (a + t) b₀ i := by
    rw [mem_arcList]; have := farPaths_translate ht (mem_arcList.mp h1); rwa [show b + t = b₀ by simp [t]] at this
  have h2' : l₂.map (posA t) ∈ arcList τ k (e + t) (f + t) (6 - i) := by
    rw [mem_arcList]; exact farPaths_translate ht (mem_arcList.mp h2)
  -- the second arc starts within 12 of b₀
  obtain ⟨w, hw1, hw2⟩ : ∃ w, w ∈ l₁ ∧ w ∈ l₂ := by
    unfold disjB at hm
    simp only [List.all_eq_false, Bool.not_eq_eq_eq_not, Bool.not_false, List.contains_iff_mem] at hm
    obtain ⟨w, hw, h⟩ := hm
    exact ⟨w, hw, by simpa using h⟩
  obtain ⟨b1, b2⟩ := farPath_bound h1 hw1
  obtain ⟨c1, c2⟩ := farPath_bound h2 hw2
  have hbox : f + t ∈ boxPts b₀ := by
    apply mem_boxPts
    · simp only [Prod.fst_add, t, Prod.fst_sub]; rw [abs_le] at b1 c1 ⊢; push_cast at b1 c1; constructor <;> omega
    · simp only [Prod.snd_add, t, Prod.snd_sub]; rw [abs_le] at b2 c2 ⊢; push_cast at b2 c2; constructor <;> omega
    · simp only [Prod.fst_add, t, Prod.fst_sub]; simp only [Prod.fst_sub] at hf3; omega
    · simp only [Prod.snd_add, t, Prod.snd_sub]; simp only [Prod.snd_sub] at hf3; omega
  refine ⟨(a + t, b₀, e + t, f + t), ?_, ?_⟩
  · unfold candQuads
    refine List.mem_filter.mpr ⟨?_, ?_⟩
    swap
    · obtain ⟨h12, h13, h14, h23, h24, h34⟩ := hD
      have hb : b₀ = b + t := by simp [t]
      simp only [dist4B, Bool.and_eq_true, bne_iff_ne, ne_eq]
      rw [hb]
      refine ⟨⟨⟨⟨⟨?_, ?_⟩, ?_⟩, ?_⟩, ?_⟩, ?_⟩ <;> intro h <;> simp_all
    simp only [List.mem_flatMap, List.mem_map, List.mem_filter, Bool.not_eq_eq_eq_not, Bool.not_true]
    refine ⟨i, by rcases hi with rfl | rfl <;> simp, l₁.map (posA t), ⟨arcList_ext h1', (arcList_head h1').1⟩,
      f + t, hbox, l₂.map (posA t), ⟨⟨arcList_ext h2', (arcList_head h2').1⟩, by rw [disjB_map]; exact hm⟩, ?_⟩
    rw [(arcList_head h1').2, (arcList_head h2').2]
  · unfold toSet trP
    simp only [Finset.image_insert, Finset.image_singleton]
    rw [show b + t = b₀ by simp [t]]

/-! ## Completeness -/

section
open Classical

theorem goodVec_eq_sc {d : ℤ × ℤ} (h : GoodVec d) : d = sc (d.1 / 3, d.2 / 3) := by
  have h1 := (ZMod.intCast_zmod_eq_zero_iff_dvd d.1 3).mp h.1
  have h2 := (ZMod.intCast_zmod_eq_zero_iff_dvd d.2 3).mp h.2
  unfold sc; ext <;> simp <;> omega

theorem nrm_good {d : ℤ × ℤ} (h : GoodVec d) {P : Finset (ℤ × ℤ)} (hP : P.Nonempty) : nrm (trP d P) = nrm P := by
  rw [goodVec_eq_sc h]; exact nrm_trP hP _

theorem goodVec_of_res {σ : ℤ → ZMod 3} {k : ℤ} {x y : ℤ × ℤ} (hx : (x.1 : ZMod 3) = σ k ∧ (x.2 : ZMod 3) = σ k)
    (hy : (y.1 : ZMod 3) = σ k ∧ (y.2 : ZMod 3) = σ k) : GoodVec (x - y) := by
  unfold GoodVec; simp [hx.1, hx.2, hy.1, hy.2]

theorem mod3_of_res {σ : ℤ → ZMod 3} {k : ℤ} {x y : ℤ × ℤ} (hx : (x.1 : ZMod 3) = σ k ∧ (x.2 : ZMod 3) = σ k)
    (hy : (y.1 : ZMod 3) = σ k ∧ (y.2 : ZMod 3) = σ k) : (x - y).1 % 3 = 0 ∧ (x - y).2 % 3 = 0 := by
  have h := goodVec_of_res hx hy
  have h1 := (ZMod.intCast_zmod_eq_zero_iff_dvd (x - y).1 3).mp h.1
  have h2 := (ZMod.intCast_zmod_eq_zero_iff_dvd (x - y).2 3).mp h.2
  exact ⟨by omega, by omega⟩

/-- From a non-zero far asymmetry at a labelled four-point set to the class being in `Z`. -/
theorem class_in_Z {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) {b₀ : ℤ × ℤ}
    (hb₀ : (b₀.1 : ZMod 3) = σ k ∧ (b₀.2 : ZMod 3) = σ k) {Z : Finset (Finset (ℤ × ℤ))}
    (hcheck : ∀ q ∈ candQuads σ k b₀, nrm (toSet q) ∈ Z ∧ nrm (gP c (toSet q)) ∈ Z)
    {x y z t : ℤ × ℤ} (hD : Dist4 x y z t)
    (hV : ∀ p ∈ ({x, y, z, t} : Finset (ℤ × ℤ)), (p.1 : ZMod 3) = σ k ∧ (p.2 : ZMod 3) = σ k)
    (hA : Af σ k c {x, y, z, t} (pr2 x y ∪ pr2 z t) 6 ≠ 0) : nrm {x, y, z, t} ∈ Z := by
  obtain ⟨hxy, hxz, hxt, hyz, hyt, hzt⟩ := hD
  have hdis : ∀ p ∈ ({x, y} : Finset (ℤ × ℤ)), ∀ q ∈ ({z, t} : Finset (ℤ × ℤ)), p ≠ q := by
    intro p hp q hq; simp only [Finset.mem_insert, Finset.mem_singleton] at hp hq
    rcases hp with rfl | rfl <;> rcases hq with rfl | rfl <;> assumption
  rw [Af_four_enum hc hV hdis hxy hzt] at hA
  have hne : ({x, y, z, t} : Finset (ℤ × ℤ)).Nonempty := ⟨x, by simp⟩
  -- residues of the points and of their half-turns
  have gc : ∀ p ∈ ({x, y, z, t} : Finset (ℤ × ℤ)), ((c - p).1 : ZMod 3) = σ k ∧ ((c - p).2 : ZMod 3) = σ k := by
    intro p hp; obtain ⟨h1, h2⟩ := hV p hp; unfold GoodCentre at hc
    simp only [Prod.fst_sub, Prod.snd_sub, Int.cast_sub, hc.1, hc.2, h1, h2]; constructor <;> ring
  -- a non-zero meeting count gives a meeting pair
  have pick : ∀ {a b e f : ℤ × ℤ}, a ≠ b → e ≠ f → meetCountL σ k a b e f 6 ≠ 0 →
      ∃ i, (i = 2 ∨ i = 4) ∧ ∃ l₁ ∈ arcList σ k a b i, ∃ l₂ ∈ arcList σ k e f (6 - i), disjB l₁ l₂ = false := by
    intro a b e f hab hef h
    rw [meetCountL_eq hab hef] at h
    unfold meet4 at h
    simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, add_zero] at h
    by_cases h2 : ((((arcList σ k a b 2) ×ˢ (arcList σ k e f (6 - 2))).filter (fun x => !disjB x.1 x.2)).length : ℤ) = 0
    · rw [h2, zero_add] at h
      obtain ⟨⟨l₁, l₂⟩, hm⟩ := List.exists_mem_of_length_pos (by exact_mod_cast Nat.pos_of_ne_zero (by exact_mod_cast h))
      obtain ⟨hp, hd⟩ := List.mem_filter.mp hm
      obtain ⟨h1, h2'⟩ := List.mem_product.mp hp
      exact ⟨4, Or.inr rfl, l₁, h1, l₂, h2', by simpa using hd⟩
    · obtain ⟨⟨l₁, l₂⟩, hm⟩ := List.exists_mem_of_length_pos (by exact_mod_cast Nat.pos_of_ne_zero (by exact_mod_cast h2))
      obtain ⟨hp, hd⟩ := List.mem_filter.mp hm
      obtain ⟨h1, h2'⟩ := List.mem_product.mp hp
      exact ⟨2, Or.inl rfl, l₁, h1, l₂, h2', by simpa using hd⟩
  by_cases hP : meetCountL σ k x y z t 6 = 0
  · -- the half-turned set carries the meeting pair
    rw [hP, sub_zero] at hA
    obtain ⟨i, hi, l₁, h1, l₂, h2, hm⟩ := pick (by intro h; exact hxy (by simpa using h))
      (by intro h; exact hzt (by simpa using h)) hA
    have hy' := gc y (by simp); have ht' := gc t (by simp)
    have hDg : Dist4 (c - x) (c - y) (c - z) (c - t) := dist4_g c ⟨hxy, hxz, hxt, hyz, hyt, hzt⟩
    obtain ⟨q, hq, hqs⟩ := meet_in_cand hDg hi h1 h2 hm (goodVec_of_res hb₀ hy') (mod3_of_res ht' hy')
    have := (hcheck q hq).2
    rw [hqs] at this
    have hg : gP c (trP (b₀ - (c - y)) {c - x, c - y, c - z, c - t}) = trP (-(b₀ - (c - y))) {x, y, z, t} := by
      rw [gP_trP, ← gP_quad, gP_gP]
    rw [hg, nrm_good (goodVec_neg (goodVec_of_res hb₀ hy')) hne] at this
    exact this
  · obtain ⟨i, hi, l₁, h1, l₂, h2, hm⟩ := pick hxy hzt hP
    have hy' := hV y (by simp); have ht' := hV t (by simp)
    obtain ⟨q, hq, hqs⟩ := meet_in_cand ⟨hxy, hxz, hxt, hyz, hyt, hzt⟩ hi h1 h2 hm (goodVec_of_res hb₀ hy')
      (mod3_of_res ht' hy')
    have := (hcheck q hq).1
    rwa [hqs, nrm_good (goodVec_of_res hb₀ hy') hne] at this

end

section
open Classical

theorem quad_perm2 (a b c d : ℤ × ℤ) : ({a, b, c, d} : Finset (ℤ × ℤ)) = {a, c, b, d} := by
  ext q; simp only [Finset.mem_insert, Finset.mem_singleton]; tauto

theorem quad_perm3 (a b c d : ℤ × ℤ) : ({a, b, c, d} : Finset (ℤ × ℤ)) = {a, d, b, c} := by
  ext q; simp only [Finset.mem_insert, Finset.mem_singleton]; tauto

theorem exists_four {P : Finset (ℤ × ℤ)} (h : P.card = 4) : ∃ a b c d, Dist4 a b c d ∧ P = {a, b, c, d} := by
  obtain ⟨a, T, haT, rfl, hT⟩ := Finset.card_eq_succ.mp h
  obtain ⟨b, c, d, hbc, hbd, hcd, rfl⟩ := Finset.card_eq_three.mp hT
  simp only [Finset.mem_insert, Finset.mem_singleton, not_or] at haT
  exact ⟨a, b, c, d, ⟨haT.1, haT.2.1, haT.2.2, hbc, hbd, hcd⟩, rfl⟩

/-- **Completeness of the shape list at l = 16.** -/
theorem G16_complete {σ : ℤ → ZMod 3} {k : ℤ} {c : ℤ × ℤ} (hc : GoodCentre σ k c) (v : Atom) {b₀ : ℤ × ℤ}
    (hb₀ : (b₀.1 : ZMod 3) = σ k ∧ (b₀.2 : ZMod 3) = σ k) {Z : Finset (Finset (ℤ × ℤ))}
    (hcheck : ∀ q ∈ candQuads σ k b₀, nrm (toSet q) ∈ Z ∧ nrm (gP c (toSet q)) ∈ Z) :
    ∀ P, G16 σ k c v P ≠ 0 → nrm P ∈ Z := by
  intro P h
  unfold G16 at h
  obtain ⟨x, -, hne⟩ := Finset.exists_ne_zero_of_sum_ne_zero h
  split_ifs at hne with hcond
  swap
  · exact absurd rfl hne
  have hW := left_ne_zero_of_mul hne
  have hA := right_ne_zero_of_mul hne
  rw [hcond.2.2] at hA
  obtain ⟨p₁, p₂, p₃, p₄, hD, rfl⟩ := exists_four hcond.1
  have hV : ∀ p ∈ ({p₁, p₂, p₃, p₄} : Finset (ℤ × ℤ)), (p.1 : ZMod 3) = σ k ∧ (p.2 : ZMod 3) = σ k :=
    fun p hp => bondS_vert_iff.mp (bonds_of_Wc hW p hp)
  have hN := Af_ne_zero_mem hD hA
  obtain ⟨h12, h13, h14, h23, h24, h34⟩ := hD
  unfold Mt at hN
  simp only [Finset.mem_insert, Finset.mem_singleton] at hN
  rcases hN with e | e | e <;> rw [e] at hA
  · exact class_in_Z hc hb₀ hcheck ⟨h12, h13, h14, h23, h24, h34⟩ hV hA
  · rw [quad_perm2] at hA hV ⊢
    exact class_in_Z hc hb₀ hcheck ⟨h13, h12, h14, h23.symm, h34, h24⟩ hV hA
  · rw [quad_perm3] at hA hV ⊢
    exact class_in_Z hc hb₀ hcheck ⟨h14, h12, h13, h24.symm, h34.symm, h23⟩ hV hA

end

end LoopEqualityProof
