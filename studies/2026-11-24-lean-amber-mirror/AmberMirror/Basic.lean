import Mathlib

/-!
# Mirror placements of cores in the 3D Penrose patch (paper #118, Theorem 3 (iv))

Points are `V3` (three real coordinates).  The tiling's vertices are 6D lattice points projected by `proj`
(the rows of the projection: e₀ = (0,1,φ), e₁ = (0,−1,φ), e₂ = (1,φ,0), e₃ = (−1,φ,0), e₄ = (φ,0,1),
e₅ = (−φ,0,1), φ = (1+√5)/2).  A wall is a rhombus with corners `c0 c1 c2 c3` (in order round it);
`mirror c0 c1 c3` is the reflection in the plane through `c0`, `c1`, `c3`, with normal
`nrm = (c1 − c0) × (c3 − c0)`: `u ↦ u − 2 (n·(u − c0))/(n·n) n`.  This is exactly `refl` of the study script
`seams_mirror.py` / `odd_edges.py`.
-/

namespace AmberMirror
noncomputable section

/-- s = √5 -/
abbrev s : ℝ := Real.sqrt 5

theorem hs : s ^ 2 = 5 := Real.sq_sqrt (by norm_num)

theorem s_lo : (2236/1000 : ℝ) < s := by
  nlinarith [hs, Real.sqrt_nonneg 5]

theorem s_hi : s < (2237/1000 : ℝ) := by
  nlinarith [hs, Real.sqrt_nonneg 5]

/-- the golden ratio -/
def φ : ℝ := (1 + s) / 2

@[ext] structure V3 where
  x : ℝ
  y : ℝ
  z : ℝ

namespace V3
def sub (a b : V3) : V3 := ⟨a.x - b.x, a.y - b.y, a.z - b.z⟩
def dot (a b : V3) : ℝ := a.x * b.x + a.y * b.y + a.z * b.z
def cross (a b : V3) : V3 := ⟨a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x⟩
end V3

/-- the projection of the 6D lattice point (v₀,…,v₅) (integer entries) to space: ∑ vᵢ eᵢ -/
def proj (v0 v1 v2 v3 v4 v5 : ℝ) : V3 :=
  ⟨v2 - v3 + φ * (v4 - v5), v0 - v1 + φ * (v2 + v3), φ * (v0 + v1) + v4 + v5⟩

/-- normal of the plane through c0, c1, c3 -/
def nrm (c0 c1 c3 : V3) : V3 := V3.cross (V3.sub c1 c0) (V3.sub c3 c0)

/-- reflection in the plane through c0, c1, c3 -/
def mirror (c0 c1 c3 u : V3) : V3 :=
  ⟨u.x - 2 * V3.dot (nrm c0 c1 c3) (V3.sub u c0) / V3.dot (nrm c0 c1 c3) (nrm c0 c1 c3) * (nrm c0 c1 c3).x,
   u.y - 2 * V3.dot (nrm c0 c1 c3) (V3.sub u c0) / V3.dot (nrm c0 c1 c3) (nrm c0 c1 c3) * (nrm c0 c1 c3).y,
   u.z - 2 * V3.dot (nrm c0 c1 c3) (V3.sub u c0) / V3.dot (nrm c0 c1 c3) (nrm c0 c1 c3) * (nrm c0 c1 c3).z⟩

/-- a wall of the patch: the two cells it joins (patch numbering) and its four corners -/
structure Wall where
  a : ℕ
  b : ℕ
  c0 : V3
  c1 : V3
  c2 : V3
  c3 : V3

/-- the mirror relation y = mirror(u), cleared of the denominator n·n = D -/
theorem mirror_poly {c0 c1 c3 u y : V3} {D : ℝ} (hy : y = mirror c0 c1 c3 u)
    (hD : V3.dot (nrm c0 c1 c3) (nrm c0 c1 c3) = D) (hD0 : D ≠ 0) :
    D * (y.x - u.x) = -2 * V3.dot (nrm c0 c1 c3) (V3.sub u c0) * (nrm c0 c1 c3).x ∧
    D * (y.y - u.y) = -2 * V3.dot (nrm c0 c1 c3) (V3.sub u c0) * (nrm c0 c1 c3).y ∧
    D * (y.z - u.z) = -2 * V3.dot (nrm c0 c1 c3) (V3.sub u c0) * (nrm c0 c1 c3).z := by
  subst hy
  simp only [mirror, hD]
  refine ⟨?_, ?_, ?_⟩ <;> field_simp <;> ring

/-- the mirror relation is symmetric: a reflection is an involution (for a non-degenerate plane) -/
theorem mirror_mirror (c0 c1 c3 u : V3) (h0 : V3.dot (nrm c0 c1 c3) (nrm c0 c1 c3) ≠ 0) :
    mirror c0 c1 c3 (mirror c0 c1 c3 u) = u := by
  have key : V3.dot (nrm c0 c1 c3) (V3.sub (mirror c0 c1 c3 u) c0) = - V3.dot (nrm c0 c1 c3) (V3.sub u c0) := by
    have e : V3.dot (nrm c0 c1 c3) (V3.sub (mirror c0 c1 c3 u) c0) = V3.dot (nrm c0 c1 c3) (V3.sub u c0) -
        2 * V3.dot (nrm c0 c1 c3) (V3.sub u c0) / V3.dot (nrm c0 c1 c3) (nrm c0 c1 c3) * V3.dot (nrm c0 c1 c3) (nrm c0 c1 c3) := by
      simp only [mirror, V3.dot, V3.sub]; ring
    rw [e, div_mul_cancel₀ _ h0]; ring
  apply V3.ext
  · show (mirror c0 c1 c3 u).x - 2 * V3.dot (nrm c0 c1 c3) (V3.sub (mirror c0 c1 c3 u) c0) / V3.dot (nrm c0 c1 c3) (nrm c0 c1 c3) * (nrm c0 c1 c3).x = u.x
    rw [key]; simp only [mirror]; ring
  · show (mirror c0 c1 c3 u).y - 2 * V3.dot (nrm c0 c1 c3) (V3.sub (mirror c0 c1 c3 u) c0) / V3.dot (nrm c0 c1 c3) (nrm c0 c1 c3) * (nrm c0 c1 c3).y = u.y
    rw [key]; simp only [mirror]; ring
  · show (mirror c0 c1 c3 u).z - 2 * V3.dot (nrm c0 c1 c3) (V3.sub (mirror c0 c1 c3 u) c0) / V3.dot (nrm c0 c1 c3) (nrm c0 c1 c3) * (nrm c0 c1 c3).z = u.z
    rw [key]; simp only [mirror]; ring

end
end AmberMirror
