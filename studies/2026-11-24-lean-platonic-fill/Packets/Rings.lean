/-
Lean formalization of DICTO's paper #117 (Zenodo 10.5281/zenodo.24411660). Part 2: Table 1 and the rings.

* `Co`: an angle q·π + a·α + b·β + c·γ given by its rational coordinates; `Co.val` its value.
* Table 1 of the paper: the dihedral angles of the pieces (`pyrD`, `ti`, `pyrI`, `td`, `dod`, `ico`, `tid`, `toA`,
  `tcoA`), each with its closed form (`ti_eq`, …). The edge counts of Table 1 play no part and are not recorded.
* `ring_weight_le`: if the angles of a ring all have coordinates with q + u·a + v·b ≥ 0 and the ring adds up to
  2π, then every angle of the ring has q + u·a + v·b ≤ 2 (Lemma 3 makes the coordinates add up exactly).
* `theorem4c_lead1`, `theorem4c_lead2`: **Theorem 4 (c)**: for each pair alone, a ring of its angles whose
  irrational parts cancel and which uses at least one irrational angle sums to at least 3π; 3π is attained
  (`ring3pi_lead1`, `ring3pi_lead2`); so no such ring is 2π or π (`no_ring_lead1`, `no_ring_lead2`).
No `sorry`.
-/
module

public import Packets.Angles

@[expose] public section

open Real

namespace Packets

/-- An angle `q·π + a·α + b·β + c·γ`, given by its rational coordinates. -/
structure Co where
  q : ℚ
  a : ℚ
  b : ℚ
  c : ℚ

/-- The value of an angle given by coordinates. -/
noncomputable def Co.val (x : Co) : ℝ := x.q * π + x.a * α + x.b * β + x.c * γ

/-- The weight `q + u·a + v·b` of an angle. -/
def Co.w (u v : ℚ) (x : Co) : ℚ := x.q + u * x.a + v * x.b

/-! ### Table 1 -/

/-- Dodecahedron centre pyramid: base–side `α`, side–side `2π/3`. -/
def pyrDCo : List Co := [⟨0, 1, 0, 0⟩, ⟨2/3, 0, 0, 0⟩]
/-- Truncated icosahedron: hexagon–hexagon `3π/2 − 2β`, pentagon–hexagon `3π/4 − α + β`. -/
def tiCo : List Co := [⟨3/2, 0, -2, 0⟩, ⟨3/4, -1, 1, 0⟩]
/-- Icosahedron centre pyramid: base–side `3π/4 − β`, side–side `2π/5`. -/
def pyrICo : List Co := [⟨3/4, 0, -1, 0⟩, ⟨2/5, 0, 0, 0⟩]
/-- Truncated dodecahedron: decagon–decagon `2α`, triangle–decagon `3π/4 − α + β`. -/
def tdCo : List Co := [⟨0, 2, 0, 0⟩, ⟨3/4, -1, 1, 0⟩]
/-- Dodecahedron: `2α`. -/
def dodCo : List Co := [⟨0, 2, 0, 0⟩]
/-- Icosahedron: `3π/2 − 2β`. -/
def icoCo : List Co := [⟨3/2, 0, -2, 0⟩]
/-- Truncated icosidodecahedron: square–hexagon `5π/4 − β`, square–decagon `π/2 + α`,
hexagon–decagon `3π/4 − α + β`. -/
def tidCo : List Co := [⟨5/4, 0, -1, 0⟩, ⟨1/2, 1, 0, 0⟩, ⟨3/4, -1, 1, 0⟩]
/-- Truncated octahedron: square–hexagon `π/2 + γ`, hexagon–hexagon `π − 2γ`. -/
def toCo : List Co := [⟨1/2, 0, 0, 1⟩, ⟨1, 0, 0, -2⟩]
/-- Truncated cuboctahedron: square–hexagon `π − γ`, square–octagon `3π/4`, hexagon–octagon `π/2 + γ`. -/
def tcoCo : List Co := [⟨1, 0, 0, -1⟩, ⟨3/4, 0, 0, 0⟩, ⟨1/2, 0, 0, 1⟩]

noncomputable def pyrD : List ℝ := pyrDCo.map Co.val
noncomputable def ti : List ℝ := tiCo.map Co.val
noncomputable def pyrI : List ℝ := pyrICo.map Co.val
noncomputable def td : List ℝ := tdCo.map Co.val
noncomputable def dod : List ℝ := dodCo.map Co.val
noncomputable def ico : List ℝ := icoCo.map Co.val
noncomputable def tid : List ℝ := tidCo.map Co.val
noncomputable def toA : List ℝ := toCo.map Co.val
noncomputable def tcoA : List ℝ := tcoCo.map Co.val

theorem pyrD_eq : pyrD = [α, 2 * π / 3] := by
  simp [pyrD, pyrDCo, Co.val]; ring
theorem ti_eq : ti = [3 * π / 2 - 2 * β, 3 * π / 4 - α + β] := by
  simp [ti, tiCo, Co.val]; constructor <;> ring
theorem pyrI_eq : pyrI = [3 * π / 4 - β, 2 * π / 5] := by
  simp [pyrI, pyrICo, Co.val]; constructor <;> ring
theorem td_eq : td = [2 * α, 3 * π / 4 - α + β] := by
  simp [td, tdCo, Co.val]; ring
theorem dod_eq : dod = [2 * α] := by simp [dod, dodCo, Co.val]
theorem ico_eq : ico = [3 * π / 2 - 2 * β] := by simp [ico, icoCo, Co.val]; ring
theorem tid_eq : tid = [5 * π / 4 - β, π / 2 + α, 3 * π / 4 - α + β] := by
  simp [tid, tidCo, Co.val]; refine ⟨by ring, by ring, by ring⟩
theorem toA_eq : toA = [π / 2 + γ, π - 2 * γ] := by
  simp [toA, toCo, Co.val]; constructor <;> ring
theorem tcoA_eq : tcoA = [π - γ, 3 * π / 4, π / 2 + γ] := by
  simp [tcoA, tcoCo, Co.val]; refine ⟨by ring, by ring, by ring⟩

/-! ### Rings -/

/-- `θ` has coordinates of nonnegative weight for `(u, v)`. -/
def Light (u v : ℚ) (θ : ℝ) : Prop := ∃ x : Co, θ = x.val ∧ 0 ≤ x.w u v

lemma light_zero {u v : ℚ} : Light u v 0 := ⟨⟨0, 0, 0, 0⟩, by simp [Co.val], by simp [Co.w]⟩

lemma Light.add {u v : ℚ} {θ φ : ℝ} (h1 : Light u v θ) (h2 : Light u v φ) : Light u v (θ + φ) := by
  obtain ⟨x, hx, hx0⟩ := h1
  obtain ⟨y, hy, hy0⟩ := h2
  refine ⟨⟨x.q + y.q, x.a + y.a, x.b + y.b, x.c + y.c⟩, ?_, ?_⟩
  · rw [hx, hy]; simp only [Co.val]; push_cast; ring
  · have : Co.w u v ⟨x.q + y.q, x.a + y.a, x.b + y.b, x.c + y.c⟩ = x.w u v + y.w u v := by
      simp only [Co.w]; ring
    rw [this]; linarith

lemma light_sum {ι : Type*} {u v : ℚ} (J : Finset ι) (ω : ι → ℝ) (h : ∀ j ∈ J, Light u v (ω j)) :
    Light u v (∑ j ∈ J, ω j) :=
  Finset.sum_induction ω (Light u v) (fun _ _ h1 h2 => h1.add h2) light_zero h

/-- **The ring bound.** If every angle `ω j` of a ring `J` is `Light u v` and the ring adds up to `2π`, then
every angle of the ring has weight at most 2. -/
theorem ring_weight_le {ι : Type*} {u v : ℚ} {J : Finset ι} {ω : ι → ℝ} (hL : ∀ j ∈ J, Light u v (ω j))
    (hsum : ∑ j ∈ J, ω j = 2 * π) {t : ι} (ht : t ∈ J) {x : Co} (hx : ω t = x.val) : x.w u v ≤ 2 := by
  classical
  obtain ⟨y, hy, hy0⟩ := light_sum (J.erase t) ω (fun j hj => hL j (Finset.mem_of_mem_erase hj))
  rw [← Finset.add_sum_erase J ω ht, hx, hy] at hsum
  obtain ⟨h1, h2, h3, -⟩ := lemma3 (x.q + y.q - 2) (x.a + y.a) (x.b + y.b) (x.c + y.c) (by
    simp only [Co.val] at hsum; push_cast; linear_combination hsum)
  have hw : x.w u v + y.w u v = (x.q + y.q) + u * (x.a + y.a) + v * (x.b + y.b) := by
    simp only [Co.w]; ring
  rw [h2, h3, mul_zero, mul_zero] at hw; linarith

/-! ### Theorem 4 (c): the pairs alone need 3π -/

/-- **Theorem 4 (c), lead 1.** A ring of `n1` pyramid base angles `α`, `n2` pyramid side angles `2π/3`, `n3`
hexagon–hexagon angles `3π/2 − 2β` and `n4` pentagon–hexagon angles `3π/4 − α + β` of the truncated icosahedron,
with at least one irrational angle and irrational parts cancelling (sum `r·π`, `r` rational), has `r ≥ 3`. -/
theorem theorem4c_lead1 (n1 n2 n3 n4 : ℕ) (r : ℚ)
    (h : (n1 : ℝ) * α + n2 * (2 * π / 3) + n3 * (3 * π / 2 - 2 * β) + n4 * (3 * π / 4 - α + β) = r * π)
    (hn : 0 < n1 + n3 + n4) : 3 ≤ r := by
  obtain ⟨h1, h2, h3, -⟩ := lemma3 (2 / 3 * n2 + 3 / 2 * n3 + 3 / 4 * n4 - r) (n1 - n4) (n4 - 2 * n3) 0
    (by push_cast; linear_combination h)
  have e2 : n1 = n4 := by exact_mod_cast (show (n1 : ℚ) = n4 by linarith)
  have e3 : n4 = 2 * n3 := by exact_mod_cast (show (n4 : ℚ) = 2 * n3 by linarith)
  have h3' : (1 : ℚ) ≤ n3 := by exact_mod_cast (show 1 ≤ n3 by omega)
  have h4 : (n4 : ℚ) = 2 * n3 := by exact_mod_cast e3
  have h2' : (0 : ℚ) ≤ n2 := by positivity
  linarith

/-- **Theorem 4 (c), lead 2.** The same for `n1` icosahedron pyramid base angles `3π/4 − β`, `n2` side angles
`2π/5`, `n3` truncated dodecahedron decagon–decagon angles `2α` and `n4` triangle–decagon angles `3π/4 − α + β`. -/
theorem theorem4c_lead2 (n1 n2 n3 n4 : ℕ) (r : ℚ)
    (h : (n1 : ℝ) * (3 * π / 4 - β) + n2 * (2 * π / 5) + n3 * (2 * α) + n4 * (3 * π / 4 - α + β) = r * π)
    (hn : 0 < n1 + n3 + n4) : 3 ≤ r := by
  obtain ⟨h1, h2, h3, -⟩ := lemma3 (3 / 4 * n1 + 2 / 5 * n2 + 3 / 4 * n4 - r) (2 * n3 - n4) (n4 - n1) 0
    (by push_cast; linear_combination h)
  have e2 : n4 = 2 * n3 := by exact_mod_cast (show (n4 : ℚ) = 2 * n3 by linarith)
  have e3 : n1 = n4 := by exact_mod_cast (show (n1 : ℚ) = n4 by linarith)
  have h3' : (1 : ℚ) ≤ n3 := by exact_mod_cast (show 1 ≤ n3 by omega)
  have h4 : (n4 : ℚ) = 2 * n3 := by exact_mod_cast e2
  have h1' : (n1 : ℚ) = n4 := by exact_mod_cast e3
  have h2' : (0 : ℚ) ≤ n2 := by positivity
  linarith

/-- The 3π ring of lead 1 (Figure 1): two pyramid base angles, two pentagon–hexagon angles and one
hexagon–hexagon angle. -/
theorem ring3pi_lead1 : 2 * α + 2 * (3 * π / 4 - α + β) + (3 * π / 2 - 2 * β) = 3 * π := by ring

/-- The 3π ring of lead 2. -/
theorem ring3pi_lead2 : 2 * (3 * π / 4 - β) + 2 * (3 * π / 4 - α + β) + 2 * α = 3 * π := by ring

/-- **No ring of lead 1's angles closes**: with at least one irrational angle, the sum is never `2π` or `π`. -/
theorem no_ring_lead1 (n1 n2 n3 n4 : ℕ) (hn : 0 < n1 + n3 + n4) :
    (n1 : ℝ) * α + n2 * (2 * π / 3) + n3 * (3 * π / 2 - 2 * β) + n4 * (3 * π / 4 - α + β) ≠ 2 * π ∧
    (n1 : ℝ) * α + n2 * (2 * π / 3) + n3 * (3 * π / 2 - 2 * β) + n4 * (3 * π / 4 - α + β) ≠ π := by
  constructor
  · intro h; have := theorem4c_lead1 n1 n2 n3 n4 2 (by rw [h]; push_cast; ring) hn; norm_num at this
  · intro h; have := theorem4c_lead1 n1 n2 n3 n4 1 (by rw [h]; push_cast; ring) hn; norm_num at this

/-- **No ring of lead 2's angles closes.** -/
theorem no_ring_lead2 (n1 n2 n3 n4 : ℕ) (hn : 0 < n1 + n3 + n4) :
    (n1 : ℝ) * (3 * π / 4 - β) + n2 * (2 * π / 5) + n3 * (2 * α) + n4 * (3 * π / 4 - α + β) ≠ 2 * π ∧
    (n1 : ℝ) * (3 * π / 4 - β) + n2 * (2 * π / 5) + n3 * (2 * α) + n4 * (3 * π / 4 - α + β) ≠ π := by
  constructor
  · intro h; have := theorem4c_lead2 n1 n2 n3 n4 2 (by rw [h]; push_cast; ring) hn; norm_num at this
  · intro h; have := theorem4c_lead2 n1 n2 n3 n4 1 (by rw [h]; push_cast; ring) hn; norm_num at this

end Packets
