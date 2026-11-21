Mathlib PR kit: arccos of a rational is not a rational multiple of pi
=====================================================================

Status: ready; waiting for replies on the Lean Zulip (#mathlib4). No PR opened, no fork made.

Base: leanprover-community/mathlib4 master 3eae40f5eb25c5934211edf662d3b24c5afbe47a
      (20 Nov 2026), toolchain leanprover/lean4:v4.37.0-rc1.
File: Mathlib/NumberTheory/Niven.lean (patch: Niven.lean.patch, apply with `git apply`).

Contents of the patch
- New public import Mathlib.Analysis.SpecialFunctions.Trigonometric.Inverse (Real.arccos and
  Real.cos_arccos are not otherwise imported by Niven.lean; the build failed without it).
- Real.arccos_ne_rat_mul_pi {q : ℚ} (hq : |(q : ℝ)| ≤ 1)
    (h : q ∉ ({-1, -1 / 2, 0, 1 / 2, 1} : Set ℚ)) (r : ℚ) : arccos q ≠ r * π
  Proof: cos_arccos gives cos (arccos q) = q, then `niven`, then Rat.cast_injective.
- Real.irrational_arccos_div_pi {q : ℚ} (hq : |(q : ℝ)| ≤ 1)
    (h : q ∉ ({-1, -1 / 2, 0, 1 / 2, 1} : Set ℚ)) : Irrational (arccos q / π)
  (name follows `irrational_cos_rat_mul_pi` in the same file).
- Both in `namespace Real`, after the existing `irrational_cos_rat_mul_pi`, using the file's
  existing `open Real`.

The hypothesis |q| ≤ 1 cannot be dropped: for 1 ≤ q, arccos q = 0 = 0 * π (arccos_of_one_le),
and for q ≤ -1, arccos q = π = 1 * π (arccos_of_le_neg_one). The docstring says so.

Build log summary (fresh shallow clone of master, 21 Nov 2026)
- lake exe cache get: ok (only Niven and its dependents not in cache, as expected after the edit).
- lake build Mathlib.NumberTheory.Niven: "Build completed successfully (4718 jobs)", no warnings.
- Only downstream importer, Mathlib.Analysis.SpecialFunctions.Trigonometric.Chebyshev.RootsExtrema:
  builds successfully (5184 jobs).
- lake exe lint-style: exit 0, no style errors.
- Two fixes during development: the missing Inverse import; a cast step (`exact_mod_cast` could not
  move `1 / 2` between ℝ and ℚ; replaced by Rat.cast_injective.mem_set_image).

Questions reviewers may raise
- Whether the new import of Trigonometric.Inverse into Niven.lean is welcome, or the lemmas should
  live in a file importing both.
- Whether the hypothesis should be stated on ℚ (|q| ≤ 1) instead of on the cast (as posted on Zulip).

Draft PR (Mathlib conventions)
------------------------------
Title:
feat(NumberTheory/Niven): arccos of a rational is not a rational multiple of π

Description:
Add `Real.arccos_ne_rat_mul_pi`: for a rational `q` with `|q| ≤ 1` and
`q ∉ {-1, -1/2, 0, 1/2, 1}`, `arccos q` is not a rational multiple of `π`.
This follows from `niven` and `Real.cos_arccos`. Also add the corollary
`Real.irrational_arccos_div_pi`: under the same hypotheses `arccos q / π` is irrational.

The hypothesis `|q| ≤ 1` is needed: outside `[-1, 1]`, `arccos` takes the values `0` and `π`.

Discussed on Zulip: <link to the #mathlib4 thread>

---

Author: <DICTO to fill>
