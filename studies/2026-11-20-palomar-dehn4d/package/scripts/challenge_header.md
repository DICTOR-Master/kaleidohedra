/-!
# The Dehn–Hadwiger invariant in four dimensions

**Informal statement.** Convex polytopes (`IsPoly`) are bounded intersections of finitely many closed half-spaces;
`ScissorsCongruent P Q`: `P` is cut into finitely many convex polytopes with disjoint interiors which, each moved by
an isometry (reflections allowed), fill `Q` with disjoint interiors.

The Dehn–Hadwiger invariant `dehnHadwiger P ∈ ℝ ⊗[ℚ] (ℝ / ℚπ)` is read from the set `P` alone, in any finite
dimension `n`. At a point `x` the directions that stay in `P` form a cone (`tcone`) with lineality space `linSpace`.
Where that space has codimension 2 (a ridge point), the class at `x` is the angle of the cone in the orthogonal plane
(`wedgeAngle`) modulo ℚπ (`thetaH`, `ridgeAngle`); elsewhere it is 0. `dehnHadwiger P` is the sum over classes `θ` of
((n − 2)-dimensional Hausdorff measure of the ridge points of class `θ`) ⊗ `θ`: in ℝ⁴, Hadwiger's sum of
area ⊗ dihedral angle over the 2-faces. Polytopes are cut out by facet normals `n` as `⟪n, x⟫ ≤ 1` (`sol`).

1. **The bridge**: scissors-congruent convex polytopes have the same invariant, in every finite dimension; the same
   for finite unions of convex polytopes (`dehnHadwigerSum_eq_of_scissors`).
2. The tesseract, the 16-cell, the 24-cell and the 120-cell have invariant 0; arccos(1/4) ∉ ℚπ.
3. The 5-cell's invariant is A₅ ⊗ arccos(1/4), the 600-cell's A₆₀₀ ⊗ (4π/3 − arccos(1/4)) (A: area of the ridge
   points; the 600-cell's dihedral angle is 4π/3 minus the 5-cell's); both are non-zero.
4. No similar copy (`IsSimilarCopy`) of the 5-cell or the 600-cell is scissors congruent to a similar copy of the
   tesseract, the 16-cell, the 24-cell or the 120-cell, nor a similar copy of the 5-cell to one of the 600-cell.

**Sources.** H. Hadwiger, *Math. Ann.* 127 (1954) 170–174, and *Vorlesungen über Inhalt, Oberfläche und
Isoperimetrie* (1957); M. Dehn, *Math. Ann.* 55 (1901) 465–478; B. Jessen, *Math. Scand.* 22 (1968) 241–256 and
*Nachr. Akad. Wiss. Göttingen* (1972) (the converse in ℝ⁴, not stated here).
Definitions and statements are copied character for character from the Lean development (comments name the files).
-/
