/-
Alexandrov's theorem on prescribed curvature, polyhedral case: basic objects.
DICTO, with Claude (Anthropic).
-/
import Mathlib

/-!
# Polytopes with corners on given rays, and their curvature at a corner

* `E3` is Euclidean 3-space.
* `normalCone Q p` is the cone of outer normals of a set `Q` at a point `p`.
* `curvature Q p` is the integral Gauss curvature of `Q` at `p`: the area of the set of
  outer unit normals at `p`. Since the area of a region `ω` of the unit sphere is three
  times the volume of the cone over `ω` inside the unit ball, it is defined as
  `3 * volume (normalCone Q p ∩ ball 0 1)`.
* `rayPolytope n r` is the convex hull of the corners `r i • n i` on the rays `ℝ₊ n i`.

Main facts: at the corner `r k • n k` the normal cone is the cell
`{x | ∀ j, r j * ⟪n j, x⟫ ≤ r k * ⟪n k, x⟫}` (`normalCone_rayPolytope`), and the cell does
not change when all `r i` are multiplied by one positive number (`cell_smul`).
-/

open MeasureTheory Set Metric
open scoped RealInnerProductSpace ENNReal

namespace Alexandrov

/-- Euclidean 3-space. -/
abbrev E3 := EuclideanSpace ℝ (Fin 3)

variable {N : ℕ}

/-- The cone of outer normals of a set `Q` at a point `p`. -/
def normalCone (Q : Set E3) (p : E3) : Set E3 :=
  {x | ∀ q ∈ Q, ⟪q, x⟫ ≤ ⟪p, x⟫}

/-- Integral Gauss curvature of `Q` at `p`: the area of the set of outer unit normals at `p`,
computed as three times the volume of the normal cone inside the unit ball. -/
noncomputable def curvature (Q : Set E3) (p : E3) : ℝ≥0∞ :=
  3 * volume (normalCone Q p ∩ ball (0 : E3) 1)

/-- The corner on ray `i`: the point at distance `r i` along the unit vector `n i`. -/
def corner (n : Fin N → E3) (r : Fin N → ℝ) (i : Fin N) : E3 := r i • n i

/-- The polytope with its corners on the given rays. -/
def rayPolytope (n : Fin N → E3) (r : Fin N → ℝ) : Set E3 :=
  convexHull ℝ (range (corner n r))

/-- The cell of ray `k`: the directions `x` in which corner `k` reaches farthest. -/
def cell (n : Fin N → E3) (r : Fin N → ℝ) (k : Fin N) : Set E3 :=
  {x | ∀ j, r j * ⟪n j, x⟫ ≤ r k * ⟪n k, x⟫}

lemma inner_corner (n : Fin N → E3) (r : Fin N → ℝ) (j : Fin N) (x : E3) :
    ⟪corner n r j, x⟫ = r j * ⟪n j, x⟫ :=
  real_inner_smul_left _ _ _

/-- The normal cone of the ray polytope at a corner is the cell of that ray. -/
theorem normalCone_rayPolytope (n : Fin N → E3) (r : Fin N → ℝ) (k : Fin N) :
    normalCone (rayPolytope n r) (corner n r k) = cell n r k := by
  ext x
  simp only [normalCone, cell, mem_ofPred_eq]
  constructor
  · intro h j
    have := h _ (subset_convexHull ℝ _ ⟨j, rfl⟩)
    rwa [inner_corner, inner_corner] at this
  · intro h q hq
    have hlin : IsLinearMap ℝ (fun q : E3 => ⟪q, x⟫) :=
      ⟨fun a b => inner_add_left a b x, fun c a => by
        rw [real_inner_smul_left, smul_eq_mul]⟩
    have hconv : Convex ℝ {q : E3 | ⟪q, x⟫ ≤ ⟪corner n r k, x⟫} :=
      convex_halfSpace_le hlin _
    have hsub : range (corner n r) ⊆ {q : E3 | ⟪q, x⟫ ≤ ⟪corner n r k, x⟫} := by
      rintro _ ⟨j, rfl⟩
      simp only [mem_ofPred_eq, inner_corner]
      exact h j
    exact convexHull_min hsub hconv hq

/-- The curvature at corner `k` is three times the volume of its cell inside the unit ball. -/
theorem curvature_rayPolytope (n : Fin N → E3) (r : Fin N → ℝ) (k : Fin N) :
    curvature (rayPolytope n r) (corner n r k) = 3 * volume (cell n r k ∩ ball (0 : E3) 1) := by
  rw [curvature, normalCone_rayPolytope]

/-- Cells do not change when every `r i` is multiplied by the same positive number. -/
theorem cell_smul (n : Fin N → E3) (r : Fin N → ℝ) {c : ℝ} (hc : 0 < c) (k : Fin N) :
    cell n (c • r) k = cell n r k := by
  ext x
  simp only [cell, mem_ofPred_eq, Pi.smul_apply, smul_eq_mul]
  refine forall_congr' fun j => ?_
  rw [mul_assoc, mul_assoc]
  exact mul_le_mul_iff_of_pos_left hc

/-- Curvature is unchanged by scaling the polytope about the origin. -/
theorem curvature_smul (n : Fin N → E3) (r : Fin N → ℝ) {c : ℝ} (hc : 0 < c) (k : Fin N) :
    curvature (rayPolytope n (c • r)) (corner n (c • r) k) =
      curvature (rayPolytope n r) (corner n r k) := by
  rw [curvature_rayPolytope, curvature_rayPolytope, cell_smul n r hc]

/-- Cells are closed. -/
theorem isClosed_cell (n : Fin N → E3) (r : Fin N → ℝ) (k : Fin N) : IsClosed (cell n r k) := by
  simp only [cell, ofPred_forall]
  exact isClosed_iInter fun j => isClosed_le
    (continuous_const.mul (continuous_const.inner continuous_id))
    (continuous_const.mul (continuous_const.inner continuous_id))

/-- Two different rays carry different corners when the `r i` are positive. -/
theorem corner_injective {n : Fin N → E3} (hn : ∀ i, ‖n i‖ = 1) (hinj : Function.Injective n)
    {r : Fin N → ℝ} (hr : ∀ i, 0 < r i) : Function.Injective (corner n r) := by
  intro i j h
  have hnorm : r i = r j := by
    have := congrArg norm h
    simp only [corner, norm_smul, hn, mul_one, Real.norm_of_nonneg (hr i).le,
      Real.norm_of_nonneg (hr j).le] at this
    exact this
  apply hinj
  simp only [corner, hnorm] at h
  exact smul_right_injective E3 (hr j).ne' h

end Alexandrov
