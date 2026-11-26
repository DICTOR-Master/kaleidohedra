/-
Step 6: the number of distinct Vacuus plates of the permutohedron (#120 Theorem 3 (iii), OEIS A402191).
DICTO, with Claude (Anthropic). Built on PermFaces.Coincide (`plate_eq_iff`).
-/
import PermFaces.Coincide

/-!
# Counting the plates (step 6)

A ridge is `key : Fin n → Fin 3` surjective, with block sizes `a, b, c`; `plateSet n` is the set of all ridge plates.
* `card_plateSet_struct`: the number of plates is `#{ridges with a < c} + #(middles n)`. `middles n` holds one middle block
  from each class of ridges with `a = c`: the sets `S` with `S ≠ ∅`, `n - |S|` even and at least `2`, and, for even `n`
  (when `S` and its complement give the same plate), coordinate `0` not in `S`.
* `card_middles_odd`, `card_middles_even`: `#(middles n) = 2^(n-1) - 1` (`n` odd), `2^(n-2) - 1` (`n` even), for `n ≥ 3`.
* `card_keysLt`: `#{ridges with a < c} = ∑_{a+b+c=n, a,b,c ≥ 1, a<c} n!/(a! b! c!)`.
* `card_plateSet`: the closed formula; `plates_three … plates_eight`: the values `3, 15, 65, 225, 770, 2443`.
-/

open Finset

namespace PermFaces

variable {n : ℕ}

/-! ### Blocks, sizes, and the plate of a ridge -/

/-- The plate of a ridge. -/
def plate (key : Fin n → Fin 3) : Submodule ℝ (Fin n → ℝ) :=
  VacuusResonus.permPlate (block key 0) (block key 1) (block key 2)

/-- The set of all ridge plates of the permutohedron in `Fin n → ℝ`. -/
def plateSet (n : ℕ) : Set (Submodule ℝ (Fin n → ℝ)) :=
  {P | ∃ key : Fin n → Fin 3, Function.Surjective key ∧
    VacuusResonus.permPlate (block key 0) (block key 1) (block key 2) = P}

/-- Block sizes as natural numbers. -/
def bc (key : Fin n → Fin 3) (b : Fin 3) : ℕ := (block key b).card

theorem mem_block {key : Fin n → Fin 3} {b : Fin 3} {i : Fin n} : i ∈ block key b ↔ key i = b := by
  simp only [block, mem_filter, mem_univ, true_and]

theorem bc_sum (key : Fin n → Fin 3) : bc key 0 + bc key 1 + bc key 2 = n := card_three (key := key)

theorem surj_iff (key : Fin n → Fin 3) : Function.Surjective key ↔ ∀ b, 1 ≤ bc key b := by
  constructor
  · intro h b
    obtain ⟨i, hi⟩ := h b
    exact Nat.succ_le_of_lt (card_pos.2 ⟨i, mem_block.2 hi⟩)
  · intro h b
    obtain ⟨i, hi⟩ := card_pos.1 (Nat.lt_of_succ_le (h b))
    exact ⟨i, mem_block.1 hi⟩

theorem bc_rev (key : Fin n → Fin 3) (b : Fin 3) : bc (Fin.rev ∘ key) b = bc key (Fin.rev b) := by
  have h := sz_rev key b
  simp only [sz, Nat.cast_inj] at h
  exact h

theorem bc_rev0 (key : Fin n → Fin 3) : bc (Fin.rev ∘ key) 0 = bc key 2 := bc_rev key 0
theorem bc_rev1 (key : Fin n → Fin 3) : bc (Fin.rev ∘ key) 1 = bc key 1 := bc_rev key 1
theorem bc_rev2 (key : Fin n → Fin 3) : bc (Fin.rev ∘ key) 2 = bc key 0 := bc_rev key 2

theorem surj_rev {key : Fin n → Fin 3} (hk : Function.Surjective key) : Function.Surjective (Fin.rev ∘ key) := by
  rw [surj_iff]; intro b; rw [bc_rev]; exact (surj_iff key).1 hk _

theorem plate_rev (key : Fin n → Fin 3) : plate (Fin.rev ∘ key) = plate key := by
  unfold plate; rw [permPlate_eq_plateOf_wt, permPlate_eq_plateOf_wt, wt_rev]

/-- `plate_eq_iff` with the block sizes as natural numbers. -/
theorem plate_eq_iff' {key key' : Fin n → Fin 3} (hk : Function.Surjective key) (hk' : Function.Surjective key') :
    plate key = plate key' ↔
      (bc key 0 ≠ bc key 2 ∧ (key' = key ∨ key' = Fin.rev ∘ key)) ∨
      (bc key 0 = bc key 2 ∧ bc key' 0 = bc key' 2 ∧
        (block key' 1 = block key 1 ∨ block key' 1 = (block key 1)ᶜ)) := by
  have h := plate_eq_iff hk hk'
  simp only [sz, Nat.cast_inj, ne_eq] at h
  exact h

/-- A ridge is determined by its first two blocks. -/
theorem key_ext {key key' : Fin n → Fin 3} (h0 : block key 0 = block key' 0) (h1 : block key 1 = block key' 1) :
    key = key' := by
  funext i
  rcases fin3 (key i) with h | h | h
  · have m : i ∈ block key' 0 := by rw [← h0]; exact mem_block.2 h
    rw [h, mem_block.1 m]
  · have m : i ∈ block key' 1 := by rw [← h1]; exact mem_block.2 h
    rw [h, mem_block.1 m]
  · rcases fin3 (key' i) with h' | h' | h'
    · have m : i ∈ block key 0 := by rw [h0]; exact mem_block.2 h'
      have m' := mem_block.1 m; rw [h] at m'; exact absurd m' (by decide)
    · have m : i ∈ block key 1 := by rw [h1]; exact mem_block.2 h'
      have m' := mem_block.1 m; rw [h] at m'; exact absurd m' (by decide)
    · rw [h, h']

/-- The ridge with first block `S0`, second block `S1` (disjoint), third block the rest. -/
def keyOf (S0 S1 : Finset (Fin n)) : Fin n → Fin 3 := fun i => if i ∈ S0 then 0 else if i ∈ S1 then 1 else 2

theorem keyOf_apply (S0 S1 : Finset (Fin n)) (i : Fin n) :
    keyOf S0 S1 i = if i ∈ S0 then 0 else if i ∈ S1 then 1 else 2 := rfl

theorem block_keyOf0 (S0 S1 : Finset (Fin n)) : block (keyOf S0 S1) 0 = S0 := by
  ext i; rw [mem_block, keyOf_apply]
  by_cases h0 : i ∈ S0
  · rw [if_pos h0]; exact ⟨fun _ => h0, fun _ => rfl⟩
  · rw [if_neg h0]
    by_cases h1 : i ∈ S1
    · rw [if_pos h1]; exact ⟨fun e => absurd e (by decide), fun e => absurd e h0⟩
    · rw [if_neg h1]; exact ⟨fun e => absurd e (by decide), fun e => absurd e h0⟩

theorem block_keyOf1 {S0 S1 : Finset (Fin n)} (h : Disjoint S0 S1) : block (keyOf S0 S1) 1 = S1 := by
  ext i; rw [mem_block, keyOf_apply]
  by_cases h0 : i ∈ S0
  · rw [if_pos h0]; exact ⟨fun e => absurd e (by decide), fun e => absurd e (disjoint_left.1 h h0)⟩
  · rw [if_neg h0]
    by_cases h1 : i ∈ S1
    · rw [if_pos h1]; exact ⟨fun _ => h1, fun _ => rfl⟩
    · rw [if_neg h1]; exact ⟨fun e => absurd e (by decide), fun e => absurd e h1⟩

theorem bc_keyOf2 {S0 S1 : Finset (Fin n)} (h : Disjoint S0 S1) : bc (keyOf S0 S1) 2 = n - S0.card - S1.card := by
  have h3 := card_three (key := keyOf S0 S1)
  rw [block_keyOf0, block_keyOf1 h] at h3
  unfold bc; omega

/-! ### The index sets -/

/-- Ridges whose first block is smaller than the third. -/
def keysLt (n : ℕ) : Finset (Fin n → Fin 3) :=
  univ.filter fun key => Function.Surjective key ∧ bc key 0 < bc key 2

/-- Ridges whose outer blocks have equal size. -/
def keysEq (n : ℕ) : Finset (Fin n → Fin 3) :=
  univ.filter fun key => Function.Surjective key ∧ bc key 0 = bc key 2

/-- `S` does not contain coordinate `0`. -/
def AvoidsZero (S : Finset (Fin n)) : Prop := ∀ i : Fin n, (i : ℕ) = 0 → i ∉ S

/-- One middle block from each class of ridges with equal outer blocks: `S` nonempty, `n - |S|` even and at least `2`;
for even `n` (where `S` and its complement give the same plate) the one without coordinate `0`. -/
def middles (n : ℕ) : Finset (Finset (Fin n)) :=
  univ.filter fun S => S.Nonempty ∧ 2 ≤ n - S.card ∧ Even (n - S.card) ∧
    (Even n → ∀ i : Fin n, (i : ℕ) = 0 → i ∉ S)

theorem mem_keysLt {key : Fin n → Fin 3} : key ∈ keysLt n ↔ Function.Surjective key ∧ bc key 0 < bc key 2 := by
  simp only [keysLt, mem_filter, mem_univ, true_and]

theorem mem_keysEq {key : Fin n → Fin 3} : key ∈ keysEq n ↔ Function.Surjective key ∧ bc key 0 = bc key 2 := by
  simp only [keysEq, mem_filter, mem_univ, true_and]

theorem mem_middles {S : Finset (Fin n)} :
    S ∈ middles n ↔ S.Nonempty ∧ 2 ≤ n - S.card ∧ Even (n - S.card) ∧ (Even n → AvoidsZero S) := by
  simp only [middles, mem_filter, mem_univ, true_and, AvoidsZero]

theorem avoidsZero_iff (hn : 0 < n) (S : Finset (Fin n)) : AvoidsZero S ↔ (⟨0, hn⟩ : Fin n) ∉ S := by
  constructor
  · intro h; exact h _ rfl
  · intro h i hi
    have e : i = ⟨0, hn⟩ := Fin.ext hi
    rw [e]; exact h

theorem avoidsZero_compl (hn : 0 < n) (S : Finset (Fin n)) : AvoidsZero Sᶜ ↔ ¬ AvoidsZero S := by
  rw [avoidsZero_iff hn, avoidsZero_iff hn, mem_compl]

open Classical in
/-- The representative of a middle block in `middles n`: itself, or (even `n`, coordinate `0` inside) its complement. -/
noncomputable def canonMiddle (S : Finset (Fin n)) : Finset (Fin n) := if (Even n → AvoidsZero S) then S else Sᶜ

theorem canonMiddle_eq {B B' : Finset (Fin n)} (h : canonMiddle B = canonMiddle B') : B' = B ∨ B' = Bᶜ := by
  unfold canonMiddle at h
  by_cases c : (Even n → AvoidsZero B)
  · by_cases c' : (Even n → AvoidsZero B')
    · rw [if_pos c, if_pos c'] at h; exact Or.inl h.symm
    · rw [if_pos c, if_neg c'] at h; right; rw [h, compl_compl]
  · by_cases c' : (Even n → AvoidsZero B')
    · rw [if_neg c, if_pos c'] at h; exact Or.inr h.symm
    · rw [if_neg c, if_neg c'] at h; exact Or.inl (compl_injective h).symm

/-- Two ridges with equal outer blocks share a plate exactly when their middle blocks have the same representative. -/
theorem plate_eq_iff_canon {k k' : Fin n → Fin 3} (hk : k ∈ keysEq n) (hk' : k' ∈ keysEq n) :
    plate k = plate k' ↔ canonMiddle (block k 1) = canonMiddle (block k' 1) := by
  obtain ⟨hs, he⟩ := mem_keysEq.1 hk
  obtain ⟨hs', he'⟩ := mem_keysEq.1 hk'
  rw [plate_eq_iff' hs hs']
  constructor
  · rintro (⟨hne, -⟩ | ⟨-, -, hB | hB⟩)
    · exact absurd he hne
    · rw [hB]
    · have s1 := bc_sum k
      have s2 := bc_sum k'
      have hc : bc k' 1 = n - bc k 1 := by unfold bc; rw [hB, card_compl, Fintype.card_fin]
      have a1 := (surj_iff k).1 hs 0
      have hev : Even n := Nat.even_iff.2 (by omega)
      have hn : 0 < n := by omega
      rw [hB]
      by_cases c : AvoidsZero (block k 1)
      · have c2 : ¬ AvoidsZero (block k 1)ᶜ := fun h => (avoidsZero_compl hn _).1 h c
        unfold canonMiddle
        rw [if_pos (fun _ => c : Even n → AvoidsZero (block k 1)),
          if_neg (fun h => c2 (h hev) : ¬ (Even n → AvoidsZero (block k 1)ᶜ)), compl_compl]
      · have c2 : AvoidsZero (block k 1)ᶜ := (avoidsZero_compl hn _).2 c
        unfold canonMiddle
        rw [if_neg (fun h => c (h hev) : ¬ (Even n → AvoidsZero (block k 1))),
          if_pos (fun _ => c2 : Even n → AvoidsZero (block k 1)ᶜ)]
  · intro h
    exact Or.inr ⟨he, he', canonMiddle_eq h⟩

theorem canonMiddle_mem {k : Fin n → Fin 3} (hk : k ∈ keysEq n) : canonMiddle (block k 1) ∈ middles n := by
  obtain ⟨hs, he⟩ := mem_keysEq.1 hk
  have s1 := bc_sum k
  have a1 := (surj_iff k).1 hs 0
  have b1 := (surj_iff k).1 hs 1
  have hb : (block k 1).card = bc k 1 := rfl
  rw [mem_middles]
  by_cases c : (Even n → AvoidsZero (block k 1))
  · unfold canonMiddle; rw [if_pos c]
    exact ⟨card_pos.1 (by omega), by omega, Nat.even_iff.2 (by omega), c⟩
  · unfold canonMiddle; rw [if_neg c]
    have hev : Even n := by
      by_contra h; exact c (fun h' => absurd h' h)
    have hz : ¬ AvoidsZero (block k 1) := fun h => c (fun _ => h)
    have hev' := Nat.even_iff.1 hev
    have hcc : ((block k 1)ᶜ).card = n - bc k 1 := by rw [card_compl, Fintype.card_fin, hb]
    exact ⟨card_pos.1 (by omega), by omega, Nat.even_iff.2 (by omega),
      fun _ => (avoidsZero_compl (by omega) _).2 hz⟩

theorem image_canonMiddle : (keysEq n).image (fun key => canonMiddle (block key 1)) = middles n := by
  ext S
  constructor
  · intro h
    obtain ⟨k, hk, rfl⟩ := mem_image.1 h
    exact canonMiddle_mem hk
  · intro hS
    obtain ⟨hne, h2, hev, hz⟩ := mem_middles.1 hS
    have hcS : S.card ≤ n := by
      have := card_le_univ S; rwa [Fintype.card_fin] at this
    obtain ⟨m, hm⟩ := hev
    have hc : (Sᶜ).card = n - S.card := by rw [card_compl, Fintype.card_fin]
    have hex : ∃ U, U ⊆ Sᶜ ∧ U.card = m := exists_subset_card_eq (by omega)
    obtain ⟨U, hU, hUc⟩ := hex
    have hd : Disjoint U S := disjoint_left.2 fun i hi hiS => (mem_compl.1 (hU hi)) hiS
    have hpos := card_pos.2 hne
    refine mem_image.2 ⟨keyOf U S, mem_keysEq.2 ⟨(surj_iff _).2 ?_, ?_⟩, ?_⟩
    · intro b
      rcases fin3 b with rfl | rfl | rfl
      · unfold bc; rw [block_keyOf0]; omega
      · unfold bc; rw [block_keyOf1 hd]; omega
      · rw [bc_keyOf2 hd]; omega
    · rw [bc_keyOf2 hd]; unfold bc; rw [block_keyOf0]; omega
    · show canonMiddle (block (keyOf U S) 1) = S
      rw [block_keyOf1 hd]; unfold canonMiddle; exact if_pos hz

/-! ### Counting tools -/

/-- Two maps with the same fibres on `E` have images of the same size. -/
theorem card_image_eq_of_iff {α β γ : Type*} [DecidableEq β] [DecidableEq γ] (E : Finset α) (f : α → β) (g : α → γ)
    (h : ∀ x ∈ E, ∀ y ∈ E, f x = f y ↔ g x = g y) : (E.image f).card = (E.image g).card := by
  have h1 : E.image f = (E.image fun x => (f x, g x)).image Prod.fst := by
    rw [image_image]; rfl
  have h2 : E.image g = (E.image fun x => (f x, g x)).image Prod.snd := by
    rw [image_image]; rfl
  have i1 : Set.InjOn Prod.fst (↑(E.image fun x => (f x, g x)) : Set (β × γ)) := by
    intro p hp q hq e
    obtain ⟨x, hx, rfl⟩ := mem_image.1 (mem_coe.1 hp)
    obtain ⟨y, hy, rfl⟩ := mem_image.1 (mem_coe.1 hq)
    have e' : f x = f y := e
    rw [Prod.mk.injEq]; exact ⟨e', (h x hx y hy).1 e'⟩
  have i2 : Set.InjOn Prod.snd (↑(E.image fun x => (f x, g x)) : Set (β × γ)) := by
    intro p hp q hq e
    obtain ⟨x, hx, rfl⟩ := mem_image.1 (mem_coe.1 hp)
    obtain ⟨y, hy, rfl⟩ := mem_image.1 (mem_coe.1 hq)
    have e' : g x = g y := e
    rw [Prod.mk.injEq]; exact ⟨(h x hx y hy).2 e', e'⟩
  rw [h1, h2, card_image_of_injOn i1, card_image_of_injOn i2]

/-- Counting by fibres. -/
theorem card_fiberwise {α β : Type*} [DecidableEq β] (s : Finset α) (t : Finset β) (f : α → β)
    (H : ∀ x ∈ s, f x ∈ t) : s.card = ∑ b ∈ t, (s.filter fun a => f a = b).card := by
  rw [card_eq_sum_card_image f s]
  apply sum_subset
  · intro b hb
    obtain ⟨a, ha, rfl⟩ := mem_image.1 hb
    exact H a ha
  · intro b _ hb
    rw [card_eq_zero, filter_eq_empty_iff]
    intro a ha e
    exact hb (mem_image.2 ⟨a, ha, e⟩)

/-- In a nonempty set, half of the subsets have even size and half have odd size. -/
theorem card_even_odd_powerset {α : Type*} [DecidableEq α] (X : Finset α) (hX : X.Nonempty) :
    (X.powerset.filter (fun S => Even S.card)).card = 2 ^ (X.card - 1) ∧
      (X.powerset.filter (fun S => ¬ Even S.card)).card = 2 ^ (X.card - 1) := by
  have h0 := sum_filter_add_sum_filter_not X.powerset (fun S => Even S.card) (fun m => (-1 : ℤ) ^ m.card)
  rw [sum_powerset_neg_one_pow_card_of_nonempty hX] at h0
  have e1 : ∀ m ∈ X.powerset.filter (fun S => Even S.card), (-1 : ℤ) ^ m.card = 1 :=
    fun m hm => Even.neg_one_pow (mem_filter.1 hm).2
  have e2 : ∀ m ∈ X.powerset.filter (fun S => ¬ Even S.card), (-1 : ℤ) ^ m.card = -1 :=
    fun m hm => Odd.neg_one_pow (Nat.not_even_iff_odd.1 (mem_filter.1 hm).2)
  rw [sum_congr rfl e1, sum_congr rfl e2] at h0
  simp only [sum_const, nsmul_eq_mul] at h0
  have t := sum_filter_add_sum_filter_not X.powerset (fun S => Even S.card) (fun _ => (1 : ℕ))
  simp only [sum_const, smul_eq_mul, mul_one, card_powerset] at t
  have hp : 2 ^ X.card = 2 * 2 ^ (X.card - 1) := by
    rw [← pow_succ']; congr 1
    have := card_pos.2 hX; omega
  have h' : (((X.powerset.filter (fun S => Even S.card)).card : ℕ) : ℤ) =
      ((X.powerset.filter (fun S => ¬ Even S.card)).card : ℕ) := by linarith
  have h'' : (X.powerset.filter (fun S => Even S.card)).card = (X.powerset.filter (fun S => ¬ Even S.card)).card := by
    exact_mod_cast h'
  constructor <;> linarith

/-! ### Milestone 1: the structural count -/

/-- **The structural count.** The number of distinct plates is the number of ridges whose first block is smaller than
the third, plus the number of middle-block classes of the ridges with equal outer blocks. -/
theorem card_plateSet_struct (n : ℕ) : (plateSet n).ncard = (keysLt n).card + (middles n).card := by
  classical
  have hset : plateSet n = ↑((keysLt n).image plate ∪ (keysEq n).image plate) := by
    ext P
    constructor
    · rintro ⟨key, hk, rfl⟩
      rw [mem_coe, mem_union, mem_image, mem_image]
      rcases lt_trichotomy (bc key 0) (bc key 2) with h | h | h
      · exact Or.inl ⟨key, mem_keysLt.2 ⟨hk, h⟩, rfl⟩
      · exact Or.inr ⟨key, mem_keysEq.2 ⟨hk, h⟩, rfl⟩
      · exact Or.inl ⟨Fin.rev ∘ key, mem_keysLt.2 ⟨surj_rev hk, by rw [bc_rev0, bc_rev2]; exact h⟩, plate_rev key⟩
    · intro h
      rw [mem_coe, mem_union, mem_image, mem_image] at h
      rcases h with ⟨key, hk, rfl⟩ | ⟨key, hk, rfl⟩
      · exact ⟨key, (mem_keysLt.1 hk).1, rfl⟩
      · exact ⟨key, (mem_keysEq.1 hk).1, rfl⟩
  have hdisj : Disjoint ((keysLt n).image plate) ((keysEq n).image plate) := by
    rw [disjoint_left]
    intro P h1 h2
    obtain ⟨k, hk, rfl⟩ := mem_image.1 h1
    obtain ⟨k', hk', e⟩ := mem_image.1 h2
    obtain ⟨hs, hlt⟩ := mem_keysLt.1 hk
    obtain ⟨hs', heq⟩ := mem_keysEq.1 hk'
    rcases (plate_eq_iff' hs hs').1 e.symm with ⟨-, h | h⟩ | ⟨h0, -⟩
    · rw [h] at heq; omega
    · rw [h, bc_rev0, bc_rev2] at heq; omega
    · omega
  have hLt : ((keysLt n).image plate).card = (keysLt n).card := by
    apply card_image_of_injOn
    intro k hk k' hk' e
    obtain ⟨hs, hlt⟩ := mem_keysLt.1 (mem_coe.1 hk)
    obtain ⟨hs', hlt'⟩ := mem_keysLt.1 (mem_coe.1 hk')
    rcases (plate_eq_iff' hs hs').1 e with ⟨-, h | h⟩ | ⟨h0, -⟩
    · exact h.symm
    · rw [h, bc_rev0, bc_rev2] at hlt'; omega
    · omega
  have hEq : ((keysEq n).image plate).card = (middles n).card := by
    rw [card_image_eq_of_iff (keysEq n) plate (fun key => canonMiddle (block key 1))
      (fun x hx y hy => plate_eq_iff_canon hx hy), image_canonMiddle]
  rw [hset]
  have hn : (↑((keysLt n).image plate ∪ (keysEq n).image plate) : Set (Submodule ℝ (Fin n → ℝ))).ncard =
      ((keysLt n).image plate ∪ (keysEq n).image plate).card := Set.ncard_coe_finset _
  rw [hn, card_union_of_disjoint hdisj, hLt, hEq]

/-! ### Milestone 2a: the middle-block classes -/

/-- `n` odd: the classes are the subsets of odd size other than the whole set. -/
theorem card_middles_odd (hn : 3 ≤ n) (ho : ¬ Even n) : (middles n).card = 2 ^ (n - 1) - 1 := by
  have ho' : n % 2 = 1 := by rw [Nat.even_iff] at ho; omega
  have hM : middles n = ((univ : Finset (Fin n)).powerset.filter (fun S => ¬ Even S.card)).erase univ := by
    ext S
    have hcS : S.card ≤ n := by
      have := card_le_univ S; rwa [Fintype.card_fin] at this
    have huniv : S = univ ↔ S.card = n := by rw [← card_eq_iff_eq_univ, Fintype.card_fin]
    rw [mem_middles, mem_erase, mem_filter, mem_powerset]
    constructor
    · rintro ⟨h1, h2, h3, -⟩
      rw [Nat.even_iff] at h3
      refine ⟨fun e => ?_, subset_univ _, fun e => ?_⟩
      · rw [huniv] at e; omega
      · rw [Nat.even_iff] at e; omega
    · rintro ⟨h1, -, h3⟩
      rw [Nat.even_iff] at h3
      have h1' : S.card ≠ n := fun e => h1 (huniv.2 e)
      exact ⟨card_pos.1 (by omega), by omega, Nat.even_iff.2 (by omega), fun h => absurd h ho⟩
  have hu : (univ : Finset (Fin n)) ∈ (univ : Finset (Fin n)).powerset.filter (fun S => ¬ Even S.card) := by
    rw [mem_filter, mem_powerset, card_univ, Fintype.card_fin]; exact ⟨subset_rfl, ho⟩
  have hne : (univ : Finset (Fin n)).Nonempty := ⟨⟨0, by omega⟩, mem_univ _⟩
  rw [hM, card_erase_of_mem hu, (card_even_odd_powerset _ hne).2, card_univ, Fintype.card_fin]

/-- `n` even: the classes are the nonempty subsets of even size that avoid coordinate `0`. -/
theorem card_middles_even (hn : 3 ≤ n) (he : Even n) : (middles n).card = 2 ^ (n - 2) - 1 := by
  have he' : n % 2 = 0 := Nat.even_iff.1 he
  obtain ⟨z, hz⟩ : ∃ z : Fin n, (z : ℕ) = 0 := ⟨⟨0, by omega⟩, rfl⟩
  have hM : middles n = (((univ : Finset (Fin n)).erase z).powerset.filter (fun S => Even S.card)).erase ∅ := by
    ext S
    have hcS : S.card ≤ n := by
      have := card_le_univ S; rwa [Fintype.card_fin] at this
    rw [mem_middles, mem_erase, mem_filter, mem_powerset]
    constructor
    · rintro ⟨h1, h2, h3, h4⟩
      rw [Nat.even_iff] at h3
      refine ⟨h1.ne_empty, fun i hi => mem_erase.2 ⟨fun e => ?_, mem_univ _⟩, Nat.even_iff.2 (by omega)⟩
      rw [e] at hi
      exact h4 he z hz hi
    · rintro ⟨h1, h2, h3⟩
      rw [Nat.even_iff] at h3
      have hc : S.card ≤ n - 1 := by
        have := card_le_card h2
        rwa [card_erase_of_mem (mem_univ z), card_univ, Fintype.card_fin] at this
      refine ⟨nonempty_iff_ne_empty.2 h1, by omega, Nat.even_iff.2 (by omega), fun _ i hi his => ?_⟩
      exact (mem_erase.1 (h2 his)).1 (Fin.ext (by rw [hi, hz]))
  have hc : ((univ : Finset (Fin n)).erase z).card = n - 1 := by
    rw [card_erase_of_mem (mem_univ z), card_univ, Fintype.card_fin]
  have hE : ((univ : Finset (Fin n)).erase z).Nonempty := card_pos.1 (by rw [hc]; omega)
  have h0 : (∅ : Finset (Fin n)) ∈ ((univ : Finset (Fin n)).erase z).powerset.filter (fun S => Even S.card) := by
    rw [mem_filter, mem_powerset]; exact ⟨empty_subset _, by simp⟩
  have e2 : n - 1 - 1 = n - 2 := by omega
  rw [hM, card_erase_of_mem h0, (card_even_odd_powerset _ hE).1, hc, e2]

/-! ### Milestone 2b: the ridges with first block smaller than the third, by block sizes -/

/-- The ridges (and degenerate ones) with block sizes `t`. -/
def fibre (t : Fin 3 → ℕ) : Finset (Fin n → Fin 3) := univ.filter fun key => ∀ b, bc key b = t b

theorem mem_fibre {t : Fin 3 → ℕ} {key : Fin n → Fin 3} : key ∈ fibre t ↔ ∀ b, bc key b = t b := by
  simp only [fibre, mem_filter, mem_univ, true_and]

/-- The number of maps with block sizes `(t 0, t 1, t 2)`: choose the first block, then the second in the rest. -/
theorem card_fibre (t : Fin 3 → ℕ) (ht : t 0 + t 1 + t 2 = n) :
    (fibre (n := n) t).card = n.choose (t 0) * (n - t 0).choose (t 1) := by
  have hmaps : ∀ key ∈ fibre (n := n) t, block key 0 ∈ powersetCard (t 0) (univ : Finset (Fin n)) :=
    fun key hk => mem_powersetCard.2 ⟨subset_univ _, (mem_fibre.1 hk) 0⟩
  have hin : ∀ S ∈ powersetCard (t 0) (univ : Finset (Fin n)),
      ((fibre (n := n) t).filter (fun key => block key 0 = S)).card = (n - t 0).choose (t 1) := by
    intro S hS
    have hSc : S.card = t 0 := (mem_powersetCard.1 hS).2
    have e : (n - t 0).choose (t 1) = (powersetCard (t 1) Sᶜ).card := by
      rw [card_powersetCard, card_compl, Fintype.card_fin, hSc]
    rw [e]
    refine card_bij (fun key _ => block key 1) ?_ ?_ ?_
    · intro key hk
      obtain ⟨hF, h0⟩ := mem_filter.1 hk
      refine mem_powersetCard.2 ⟨fun i hi => mem_compl.2 fun hiS => ?_, (mem_fibre.1 hF) 1⟩
      rw [← h0] at hiS
      have a := mem_block.1 hi
      have b := mem_block.1 hiS
      rw [a] at b; exact absurd b (by decide)
    · intro key hk key' hk' e'
      exact key_ext ((mem_filter.1 hk).2.trans (mem_filter.1 hk').2.symm) e'
    · intro S1 hS1
      obtain ⟨hsub, hc1⟩ := mem_powersetCard.1 hS1
      have hd : Disjoint S S1 := disjoint_left.2 fun i hi hi1 => mem_compl.1 (hsub hi1) hi
      refine ⟨keyOf S S1, mem_filter.2 ⟨mem_fibre.2 fun b => ?_, block_keyOf0 S S1⟩, block_keyOf1 hd⟩
      rcases fin3 b with rfl | rfl | rfl
      · unfold bc; rw [block_keyOf0, hSc]
      · unfold bc; rw [block_keyOf1 hd, hc1]
      · rw [bc_keyOf2 hd, hSc, hc1]; omega
  rw [card_fiberwise (fibre (n := n) t) (powersetCard (t 0) (univ : Finset (Fin n))) (fun key => block key 0) hmaps,
    sum_congr rfl hin, sum_const, card_powersetCard, card_univ, Fintype.card_fin, smul_eq_mul]

/-- The admissible size triples: `a + b + c = n`, all at least `1`, `a < c`. -/
def sizes (n : ℕ) : Finset (Fin 3 → ℕ) :=
  (Finset.Nat.antidiagonalTuple 3 n).filter fun t => 1 ≤ t 0 ∧ 1 ≤ t 1 ∧ 1 ≤ t 2 ∧ t 0 < t 2

theorem mem_sizes {t : Fin 3 → ℕ} :
    t ∈ sizes n ↔ t 0 + t 1 + t 2 = n ∧ 1 ≤ t 0 ∧ 1 ≤ t 1 ∧ 1 ≤ t 2 ∧ t 0 < t 2 := by
  simp only [sizes, mem_filter, Finset.Nat.mem_antidiagonalTuple, Fin.sum_univ_three]

theorem card_keysLt_choose (n : ℕ) :
    (keysLt n).card = ∑ t ∈ sizes n, n.choose (t 0) * (n - t 0).choose (t 1) := by
  have H : ∀ key ∈ keysLt n, bc key ∈ sizes n := by
    intro key hk
    obtain ⟨hs, hlt⟩ := mem_keysLt.1 hk
    have s := (surj_iff key).1 hs
    exact mem_sizes.2 ⟨bc_sum key, s 0, s 1, s 2, hlt⟩
  have hfe : ∀ t ∈ sizes n, ((keysLt n).filter fun key => bc key = t).card =
      n.choose (t 0) * (n - t 0).choose (t 1) := by
    intro t ht
    obtain ⟨hsum, h0, h1, h2, hlt⟩ := mem_sizes.1 ht
    have e : ((keysLt n).filter fun key => bc key = t) = fibre t := by
      ext key
      rw [mem_filter, mem_keysLt, mem_fibre]
      constructor
      · rintro ⟨-, h⟩ b; exact congrFun h b
      · intro h
        refine ⟨⟨(surj_iff key).2 fun b => ?_, by rw [h 0, h 2]; exact hlt⟩, funext h⟩
        rw [h b]; rcases fin3 b with rfl | rfl | rfl <;> assumption
    rw [e, card_fibre t hsum]
  rw [card_fiberwise (keysLt n) (sizes n) bc H, sum_congr rfl hfe]

theorem choose_mul_choose_eq (a b c : ℕ) :
    (a + b + c).choose a * (b + c).choose b =
      (a + b + c).factorial / (a.factorial * b.factorial * c.factorial) := by
  have h1 := Nat.choose_mul_factorial_mul_factorial (Nat.le_add_right a (b + c))
  rw [Nat.add_sub_cancel_left] at h1
  have h2 := Nat.choose_mul_factorial_mul_factorial (Nat.le_add_right b c)
  rw [Nat.add_sub_cancel_left] at h2
  symm
  apply Nat.div_eq_of_eq_mul_left
    (Nat.mul_pos (Nat.mul_pos (Nat.factorial_pos _) (Nat.factorial_pos _)) (Nat.factorial_pos _))
  rw [add_assoc, ← h1, ← h2]; ring

/-- The ridges with first block smaller than the third, counted by block sizes. -/
theorem card_keysLt (n : ℕ) :
    (keysLt n).card =
      ∑ t ∈ sizes n, n.factorial / ((t 0).factorial * (t 1).factorial * (t 2).factorial) := by
  rw [card_keysLt_choose]
  apply sum_congr rfl
  intro t ht
  obtain ⟨hsum, -⟩ := mem_sizes.1 ht
  have h := choose_mul_choose_eq (t 0) (t 1) (t 2)
  rw [hsum] at h
  have e : n - t 0 = t 1 + t 2 := by omega
  rw [e]; exact h

/-! ### The closed formula (#120 Theorem 3 (iii), OEIS A402191) -/

/-- **The number of distinct Vacuus plates of the permutohedron** (`n ≥ 3`):
`∑_{a+b+c=n, a,b,c ≥ 1, a<c} n!/(a! b! c!) + T(n)`, with `T(n) = 2^(n-2) - 1` for `n` even and `2^(n-1) - 1` for `n` odd. -/
theorem card_plateSet (hn : 3 ≤ n) :
    (plateSet n).ncard =
      ∑ t ∈ sizes n, n.factorial / ((t 0).factorial * (t 1).factorial * (t 2).factorial) +
        (if Even n then 2 ^ (n - 2) - 1 else 2 ^ (n - 1) - 1) := by
  rw [card_plateSet_struct, card_keysLt]
  by_cases he : Even n
  · rw [if_pos he, card_middles_even hn he]
  · rw [if_neg he, card_middles_odd hn he]

/-! ### Milestone 3: the first values, `3, 15, 65, 225, 770, 2443` -/

theorem plates_three : (plateSet 3).ncard = 3 := by
  rw [card_plateSet (by norm_num)]; decide +kernel

theorem plates_four : (plateSet 4).ncard = 15 := by
  rw [card_plateSet (by norm_num)]; decide +kernel

theorem plates_five : (plateSet 5).ncard = 65 := by
  rw [card_plateSet (by norm_num)]; decide +kernel

theorem plates_six : (plateSet 6).ncard = 225 := by
  rw [card_plateSet (by norm_num)]; decide +kernel

theorem plates_seven : (plateSet 7).ncard = 770 := by
  rw [card_plateSet (by norm_num)]; decide +kernel

theorem plates_eight : (plateSet 8).ncard = 2443 := by
  rw [card_plateSet (by norm_num)]; decide +kernel

end PermFaces
