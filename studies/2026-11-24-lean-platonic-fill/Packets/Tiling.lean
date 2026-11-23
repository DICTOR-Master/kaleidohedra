/-
Lean formalization of DICTO's paper #117 (Zenodo 10.5281/zenodo.24411660). Part 3: Theorem 4 (a) and (b).

Here the tiles enter only through the ring condition `LocalAngleCondition`: each tile `t` comes with the list
`ang t` of its dihedral angles, and for every dihedral angle `θ` of every tile there is a ring, a finite set of
tiles `J ∋ t` with an angle `ω j` for each, `ω t = θ`, where each `ω j` is a dihedral angle of `j`, or `π` (a tile
with the point inside a face), or `2π`, and the angles add up to `2π`. This is Lemma 2 of the paper; it is
proved for tilings by convex polytopes in `Packets/Lemma2.lean` (`localAngleCondition_of_tiling`), with
`ok j` the set-defined dihedral angles of tile `j`.

* `theorem4a`: **Theorem 4 (a)**, from the ring condition. If every tile is a dodecahedron centre pyramid, a
  truncated icosahedron, a
  dodecahedron, an icosahedron, a truncated icosidodecahedron, a truncated octahedron, a truncated cuboctahedron,
  or a convex piece whose dihedral angles are all nonnegative rational multiples of π, and the local angle
  condition holds, then no tile is a dodecahedron centre pyramid or a truncated icosahedron (nor a dodecahedron,
  an icosahedron or a truncated icosidodecahedron).
* `theorem4b`: **Theorem 4 (b)**, the same with the icosahedron centre pyramid and the truncated dodecahedron.

Method: the paper's three steps, each done by one weight `q + u·a + v·b` (`ring_weight_le`): a piece is removed
when one of its angles has weight above 2 while every angle still possible has weight at least 0.
Lead 1: (u, v) = (0, −3/4) removes the truncated icosahedron and the icosahedron; (2, 5/4) the truncated
icosidodecahedron; (3, 0) the pyramid and the dodecahedron. Lead 2: (3/2, 3/4) removes the truncated dodecahedron
and the dodecahedron; (−1/4, −1) the truncated icosidodecahedron and the icosahedron; (0, −3) the pyramid.
No `sorry`.
-/
module

public import Packets.Rings

@[expose] public section

open Real

namespace Packets

/-- **The local angle condition** (Lemma 2 of the paper). -/
def LocalAngleCondition {ι : Type*} (ang : ι → List ℝ) (ok : ι → ℝ → Prop) : Prop :=
  ∀ t, ∀ θ ∈ ang t, ∃ (J : Finset ι) (ω : ι → ℝ), t ∈ J ∧ ω t = θ ∧
    (∀ j ∈ J, ok j (ω j) ∨ ω j = π ∨ ω j = 2 * π) ∧ ∑ j ∈ J, ω j = 2 * π

/-- A piece whose dihedral angles are all nonnegative rational multiples of π. -/
def RationalPiece (ok : ℝ → Prop) : Prop := ∀ θ, ok θ → ∃ q : ℚ, 0 ≤ q ∧ θ = q * π

lemma light_of_rational {ok : ℝ → Prop} (h : RationalPiece ok) (u v : ℚ) : ∀ θ, ok θ → Light u v θ := by
  intro θ hθ
  obtain ⟨q, hq, rfl⟩ := h θ hθ
  exact ⟨⟨q, 0, 0, 0⟩, by simp [Co.val], by simpa [Co.w] using hq⟩

lemma light_of_co {P : List Co} {u v : ℚ} (h : ∀ x ∈ P, 0 ≤ x.w u v) : ∀ θ ∈ P.map Co.val, Light u v θ := by
  intro θ hθ
  obtain ⟨x, hx, rfl⟩ := List.mem_map.1 hθ
  exact ⟨x, rfl, h x hx⟩

/-- **Pruning.** If every angle of every tile is `Light u v`, every angle of every tile has weight at most 2. -/
theorem prune {ι : Type*} {ang : ι → List ℝ} {ok : ι → ℝ → Prop} (hL : LocalAngleCondition ang ok)
    {u v : ℚ} (hg : ∀ t θ, ok t θ → Light u v θ) (t : ι) {x : Co} (hx : x.val ∈ ang t) : x.w u v ≤ 2 := by
  obtain ⟨J, ω, htJ, hωt, hcl, hsum⟩ := hL t x.val hx
  refine ring_weight_le (fun j hj => ?_) hsum htJ hωt
  rcases hcl j hj with h | h | h
  · exact hg j _ h
  · rw [h]; exact ⟨⟨1, 0, 0, 0⟩, by simp [Co.val], by simp [Co.w]⟩
  · rw [h]; exact ⟨⟨2, 0, 0, 0⟩, by simp [Co.val], by simp [Co.w]⟩

lemma mem_val {P : List Co} {x : Co} (hx : x ∈ P) : x.val ∈ P.map Co.val := List.mem_map.2 ⟨x, hx, rfl⟩

/-! ### Theorem 4 (a) -/

/-- The pieces allowed in Theorem 4 (a). -/
def AllowedA (l : List ℝ) (ok : ℝ → Prop) : Prop :=
  (l = pyrD ∨ l = ti ∨ l = dod ∨ l = ico ∨ l = tid ∨ l = toA ∨ l = tcoA) ∧ (∀ θ, ok θ → θ ∈ l) ∨
    RationalPiece ok

/-- **Theorem 4 (a)**, from the local angle condition (Lemma 2). -/
theorem theorem4a {ι : Type*} (ang : ι → List ℝ) (ok : ι → ℝ → Prop)
    (hL : LocalAngleCondition ang ok) (hk : ∀ t, AllowedA (ang t) (ok t)) (t : ι) :
    ang t ≠ pyrD ∧ ang t ≠ ti ∧ ang t ≠ dod ∧ ang t ≠ ico ∧ ang t ≠ tid := by
  -- Step 1: no truncated icosahedron, no icosahedron.
  have g1 : ∀ s θ, ok s θ → Light 0 (-3/4) θ := by
    intro s
    rcases hk s with ⟨h | h | h | h | h | h | h, hok⟩ | h <;>
      first
      | exact light_of_rational h _ _
      | (intro θ hθ; have hm := hok θ hθ; rw [h] at hm; exact light_of_co (by
          norm_num [pyrDCo, tiCo, dodCo, icoCo, tidCo, toCo, tcoCo, Co.w]) θ hm)
  have x1 : ∀ s, (⟨3/2, 0, -2, 0⟩ : Co).val ∉ ang s := fun s hs => by
    have := prune hL g1 s hs; norm_num [Co.w] at this
  have nti : ∀ s, ang s ≠ ti := fun s h => x1 s (by rw [h]; exact mem_val (by simp [tiCo]))
  have nico : ∀ s, ang s ≠ ico := fun s h => x1 s (by rw [h]; exact mem_val (by simp [icoCo]))
  -- Step 2: no truncated icosidodecahedron.
  have g2 : ∀ s θ, ok s θ → Light 2 (5/4) θ := by
    intro s
    rcases hk s with ⟨h | h | h | h | h | h | h, hok⟩ | h <;>
      first
      | exact light_of_rational h _ _
      | exact absurd h (nti s)
      | exact absurd h (nico s)
      | (intro θ hθ; have hm := hok θ hθ; rw [h] at hm; exact light_of_co (by norm_num [pyrDCo, dodCo, tidCo, toCo, tcoCo, Co.w]) θ hm)
  have x2 : ∀ s, (⟨1/2, 1, 0, 0⟩ : Co).val ∉ ang s := fun s hs => by
    have := prune hL g2 s hs; norm_num [Co.w] at this
  have ntid : ∀ s, ang s ≠ tid := fun s h => x2 s (by rw [h]; exact mem_val (by simp [tidCo]))
  -- Step 3: no dodecahedron centre pyramid, no dodecahedron.
  have g3 : ∀ s θ, ok s θ → Light 3 0 θ := by
    intro s
    rcases hk s with ⟨h | h | h | h | h | h | h, hok⟩ | h <;>
      first
      | exact light_of_rational h _ _
      | exact absurd h (nti s)
      | exact absurd h (nico s)
      | exact absurd h (ntid s)
      | (intro θ hθ; have hm := hok θ hθ; rw [h] at hm; exact light_of_co (by norm_num [pyrDCo, dodCo, toCo, tcoCo, Co.w]) θ hm)
  have x3 : ∀ s, (⟨0, 1, 0, 0⟩ : Co).val ∉ ang s := fun s hs => by
    have := prune hL g3 s hs; norm_num [Co.w] at this
  have x3' : ∀ s, (⟨0, 2, 0, 0⟩ : Co).val ∉ ang s := fun s hs => by
    have := prune hL g3 s hs; norm_num [Co.w] at this
  exact ⟨fun h => x3 t (by rw [h]; exact mem_val (by simp [pyrDCo])), nti t,
    fun h => x3' t (by rw [h]; exact mem_val (by simp [dodCo])), nico t, ntid t⟩

/-! ### Theorem 4 (b) -/

/-- The pieces allowed in Theorem 4 (b). -/
def AllowedB (l : List ℝ) (ok : ℝ → Prop) : Prop :=
  (l = pyrI ∨ l = td ∨ l = dod ∨ l = ico ∨ l = tid ∨ l = toA ∨ l = tcoA) ∧ (∀ θ, ok θ → θ ∈ l) ∨
    RationalPiece ok

/-- **Theorem 4 (b)**, from the local angle condition (Lemma 2). -/
theorem theorem4b {ι : Type*} (ang : ι → List ℝ) (ok : ι → ℝ → Prop)
    (hL : LocalAngleCondition ang ok) (hk : ∀ t, AllowedB (ang t) (ok t)) (t : ι) :
    ang t ≠ pyrI ∧ ang t ≠ td ∧ ang t ≠ dod ∧ ang t ≠ ico ∧ ang t ≠ tid := by
  -- Step 1: no truncated dodecahedron, no dodecahedron.
  have g1 : ∀ s θ, ok s θ → Light (3/2) (3/4) θ := by
    intro s
    rcases hk s with ⟨h | h | h | h | h | h | h, hok⟩ | h <;>
      first
      | exact light_of_rational h _ _
      | (intro θ hθ; have hm := hok θ hθ; rw [h] at hm; exact light_of_co (by
          norm_num [pyrICo, tdCo, dodCo, icoCo, tidCo, toCo, tcoCo, Co.w]) θ hm)
  have x1 : ∀ s, (⟨0, 2, 0, 0⟩ : Co).val ∉ ang s := fun s hs => by
    have := prune hL g1 s hs; norm_num [Co.w] at this
  have ntd : ∀ s, ang s ≠ td := fun s h => x1 s (by rw [h]; exact mem_val (by simp [tdCo]))
  have ndod : ∀ s, ang s ≠ dod := fun s h => x1 s (by rw [h]; exact mem_val (by simp [dodCo]))
  -- Step 2: no truncated icosidodecahedron, no icosahedron.
  have g2 : ∀ s θ, ok s θ → Light (-1/4) (-1) θ := by
    intro s
    rcases hk s with ⟨h | h | h | h | h | h | h, hok⟩ | h <;>
      first
      | exact light_of_rational h _ _
      | exact absurd h (ntd s)
      | exact absurd h (ndod s)
      | (intro θ hθ; have hm := hok θ hθ; rw [h] at hm; exact light_of_co (by norm_num [pyrICo, icoCo, tidCo, toCo, tcoCo, Co.w]) θ hm)
  have x2 : ∀ s, (⟨5/4, 0, -1, 0⟩ : Co).val ∉ ang s := fun s hs => by
    have := prune hL g2 s hs; norm_num [Co.w] at this
  have x2' : ∀ s, (⟨3/2, 0, -2, 0⟩ : Co).val ∉ ang s := fun s hs => by
    have := prune hL g2 s hs; norm_num [Co.w] at this
  have ntid : ∀ s, ang s ≠ tid := fun s h => x2 s (by rw [h]; exact mem_val (by simp [tidCo]))
  have nico : ∀ s, ang s ≠ ico := fun s h => x2' s (by rw [h]; exact mem_val (by simp [icoCo]))
  -- Step 3: no icosahedron centre pyramid.
  have g3 : ∀ s θ, ok s θ → Light 0 (-3) θ := by
    intro s
    rcases hk s with ⟨h | h | h | h | h | h | h, hok⟩ | h <;>
      first
      | exact light_of_rational h _ _
      | exact absurd h (ntd s)
      | exact absurd h (ndod s)
      | exact absurd h (ntid s)
      | exact absurd h (nico s)
      | (intro θ hθ; have hm := hok θ hθ; rw [h] at hm; exact light_of_co (by norm_num [pyrICo, toCo, tcoCo, Co.w]) θ hm)
  have x3 : ∀ s, (⟨3/4, 0, -1, 0⟩ : Co).val ∉ ang s := fun s hs => by
    have := prune hL g3 s hs; norm_num [Co.w] at this
  exact ⟨fun h => x3 t (by rw [h]; exact mem_val (by simp [pyrICo])), ntd t, ndod t, nico t, ntid t⟩

end Packets
