# Palomar preflight: the octahedral constant 3 (#43 Theorem 4) (15 November 2026)

**Conclusion.** The entry package passes every Palomar check that can be run without a public repository. `lake comparator` accepts Solution against Challenge for all 4 compared theorems: Lean's kernel, NanoDa and con-ron all accept. The axioms are only `propext`, `Classical.choice` and `Quot.sound`. A deliberately wrong Challenge (constant 2 in place of 3) is rejected. Palomar's Python metadata validator accepts `formalization.yaml`. **Nothing was submitted.** No repository was created or pushed, and no issue or pull request was opened.

**Status:** package complete; mechanical checks green; local only. A copy of its text files is in `entry/`.

## What was run

All Lean work ran on the compute host through the job wrapper (job `palomar-kyu-entry`, ended FINAL ok). Toolchain `leanprover/lean4:v4.35.0-rc2`, Mathlib `v4.35.0-rc2` (065356127b1dc0016f66b7283ce0ce2c4055aa55), the template's manifest. Palomar sources: PalomarTemplate @ 2891de4, PalomarSubmission @ 14aa8d6, PalomarPolicy @ 28bd48b.

| Check | Palomar source | Result |
|---|---|---|
| Lean source requirements: module headers, ≤ 10,000 lines per file, Challenge ≤ 1,000 lines and 100 KiB | template `scripts/check-lean-sources.py` | pass. Challenge: 89 lines, 4,213 bytes, imports Mathlib only |
| No `sorry` or `native_decide` in `Kyushindo/` and `Solution.lean`; exactly 4 `sorry` in Challenge | job grep | pass |
| Clean build (`rm -rf .lake/build; lake build`) | template | "Build completed successfully (8938 jobs)" |
| Axioms of the library theorems | module `Kyushindo.Axioms` | all 5 (`covering`, `covering_general`, `octahedral_nesting`, `cube_admissible`, `octahedral_nesting_sharp`): `[propext, Classical.choice, Quot.sound]` |
| Axioms of the 4 compared theorems, as seen from `Solution` | `#print axioms` | all 4: `[propext, Classical.choice, Quot.sound]` |
| `formalization.yaml` mechanical minimum, including the arXiv and MSC taxonomies | PalomarSubmission `scripts/submission_contract.py`: `load_formalization_metadata`, `normalized_provenance` | pass; derived `result_origin: source-based`, `repository_role: substantive-development` |
| Source `type` values allowed by policy (CONTRIBUTING §3: paper, book, web discussion, folklore, original-proof, other) | policy text (the Python validator does not enforce it) | pass: `paper` (5) and `other` (Mathlib) |
| **Comparator**, with the toolchain's bundled kernels registered the way Palomar does it | template `scripts/verify-comparator.sh` | con-ron: "accepted 27772 declarations (--verified)"; "nanoda kernel accepts the solution"; "Lean default kernel accepts the solution"; **"Your solution is okay!"** (exit 0) |
| Negative control: Challenge changed to `halfspaceBody n h ⊆ (2 : ℝ) • footHull n h` | same script | rejected: "Challenge and solution theorem statement do not match: 'DictoKyushindo.octahedral_nesting'" (exit 1) |
| Licence | the template's `LICENSE`, byte-identical (`cmp`) | Apache-2.0, matching `project.license`. Not machine-detected: `licensee` (Ruby) is not installed |

## Layout (the lesson of the first entry applied)

The first entry's comparator fault (auxiliary proof terms shared between definitions in one file) was avoided from the start: `Solution.lean` is the Challenge word for word, with each `sorry` replaced by one `exact` that transfers the theorem from the proof library `Kyushindo.Proof` (namespace `KyushindoProof`, whose definitions are copies of the Challenge's). The transfers are by definitional unfolding. The comparator accepted on the first run.

The proof library is the proof file of commit 909ad63a (study 2026-11-14-lean-loop-equality, `lean/OctahedralNestingProof.lean`) with the namespace renamed and the header rewritten to credit sources at the point of use. The Challenge is that study's `lean/OctahedralNesting.lean` with credits added to the docstring of `covering`; no statement changed.

## What could not be run, and why

- **The PalomarSubmission reusable workflow** (`verify_submission.py prepare/execute`, profile `palomar-standard-v1`). It clones the entry from a public GitHub repository at a fixed commit and runs on GitHub Actions; creating or pushing a repository needs DICTO's word. Unrun as a result: the protected compile of the Challenge under a per-run alias, the export-based comparison, the bubblewrap/seccomp build sandbox, Challenge rendering with Verso, and the licence detector.
- **The Ruby metadata validator** (`scripts/validate-formalization.rb`): Ruby is not installed. Palomar's Python validator was run instead.
- **The doc build** (`docbuild/`): optional, not run.

## Warnings (not failures)

One unused-variable warning: `hh` (the positivity of the distances) in `KyushindoProof.octahedral_nesting`. It is kept on purpose, so that the statement matches #43; the proof does not need it.

## The package

- On the compute host: `lean/palomar-entry-kyushindo/`, a local git repository with **no remote**, head `d65b9774ee43fe6696753f5c8210b65c5b93bd03`; the second commit changed only text (README, formalization.yaml: the covering lemma described as the upper bound for the orbit-space diameter, after the replay review), not Lean, and the metadata validator was run again on it (pass). Its `.lake/` is not committed.
- Its text files are copied in `entry/` (same content as that commit).
- One Comparator configuration with 4 theorems, so one Palomar entry.
