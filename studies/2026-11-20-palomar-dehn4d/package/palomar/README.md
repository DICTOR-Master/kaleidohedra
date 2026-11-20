# The Dehn–Hadwiger invariant in four dimensions (Lean 4 + Mathlib)

Author: DICTO.

The Dehn–Hadwiger invariant `dehnHadwiger P` is defined from the set `P` alone, in every finite-dimensional real inner
product space. At a point of `P` the directions that stay in `P` form a cone; where the directions `v` with `v` and `-v`
in the cone span a subspace of codimension 2 (a ridge point), the class there is the angle of the cone in the
orthogonal plane, modulo rational multiples of π. `dehnHadwiger P` adds, over the classes θ, the (n − 2)-dimensional
Hausdorff measure of the ridge points of class θ, tensored with θ, in ℝ ⊗[ℚ] (ℝ/ℚπ). In ℝ⁴ this is Hadwiger's sum of
area ⊗ dihedral angle over the 2-faces (Hadwiger, Math. Ann. 127, 1954). The Challenge proves:

1. **The bridge** (`dehnHadwiger_eq_of_scissorsCongruent`, `dehnHadwigerSum_eq_of_scissors`): scissors-congruent
   convex polytopes, and finite unions of them, have the same invariant, in every dimension.
2. **The six regular 4-polytopes**: the tesseract, the 16-cell, the 24-cell and the 120-cell have invariant 0; the
   5-cell has A₅ ⊗ arccos(1/4) and the 600-cell A₆₀₀ ⊗ (4π/3 − arccos(1/4)), with A₅, A₆₀₀ > 0 the areas of the ridge
   points; arccos(1/4) is not a rational multiple of π.
3. **Non-congruence**: no similar copy of the 5-cell or of the 600-cell is scissors congruent to a similar copy of the
   tesseract, the 16-cell, the 24-cell or the 120-cell; no similar copy of the 5-cell is scissors congruent to a
   similar copy of the 600-cell (the 600-cell's dihedral angle is 4π/3 minus the 5-cell's, so the two invariants have
   opposite signs).

Pieces of a dissection are convex polytopes, finitely many, moved by isometries, reflections included. Jessen's
converse in ℝ⁴ is not stated.

- `Challenge.lean`: the definitions and the fourteen statements, every proof `sorry`; Mathlib only; every definition and
  statement copied, character for character, from the development by a script.
- `Solution.lean`: the Challenge word for word, with proofs that transfer the theorems of the development.
- `DehnHadwiger/`: the development. `DehnHadwiger/Canon/` holds the modules of the Dehn Canon entry
  (PALOMAR-2026-11-20-000003) that it uses: convex polytopes, tangent cones, wedge angles, cuts and dissections. The
  modules `DH1Def` to `DH15Results600` add the codimension-2 invariant, its cut identity and the bridge, scaling, the
  angle of a cone of constraints, and the six polytopes; the 600-cell's facet data are exact ℤ[φ] lists checked by
  `decide +kernel`.

Toolchain `leanprover/lean4:v4.35.0-rc2`, Mathlib `v4.35.0-rc2`. All fourteen theorems depend only on the axioms
`propext`, `Classical.choice` and `Quot.sound`. Neither `sorry` nor `native_decide` is used. Every Lean file uses the
module system.

## How it was made

DICTO posed the formalization and directed it; the Lean code was written by a Claude Code agent (Claude, Anthropic).
See `formalization.yaml` for the sources, the related formalizations and the checks.

Licence: Apache-2.0.
