# Palomar preflight: Loop Equality entry (15 November 2026)

**Conclusion.** The entry package passes every Palomar check that can be run without a public repository. `lake comparator` accepts Solution against Challenge for all 17 compared theorems: Lean's kernel, NanoDa and con-ron all accept. The axioms are only `propext`, `Classical.choice` and `Quot.sound`. A deliberately wrong Challenge is rejected. **Nothing was submitted.** No repository was created or pushed, and no issue or pull request was opened.

**Status:** package complete; mechanical checks green; local only. A copy of its text files is in `entry/`.

## What was run

All Lean work ran on the compute host through the job wrapper (job `palomar-loop-entry`, ended FINAL ok). Toolchain `leanprover/lean4:v4.35.0-rc2`, Mathlib `v4.35.0-rc2` (065356127b1dc0016f66b7283ce0ce2c4055aa55), the template's manifest.

| Check | Palomar source | Result |
|---|---|---|
| Lean source requirements: module headers, ≤ 10,000 lines per file, Challenge ≤ 1,000 lines and 100 KiB | template `scripts/check-lean-sources.py` (it follows PalomarSubmission `source_requirements.py`) | pass. Challenge: 363 lines, 15,825 bytes, imports Mathlib only |
| No `sorry` or `native_decide` in the proofs; exactly 17 `sorry` in Challenge | job grep | pass |
| Clean build (`rm -rf .lake/build; lake build`) | template | "Build completed successfully (8947 jobs)" |
| Axioms of the 17 compared theorems, as seen from `Solution` | `#print axioms` | all 17: `[propext, Classical.choice, Quot.sound]` |
| Axioms of the library theorems | module `LoopEquality.Axioms` | all 15: `[propext, Classical.choice, Quot.sound]` |
| **Comparator**, with the toolchain's bundled kernels registered the way Palomar does it | template `scripts/verify-comparator.sh` | con-ron: "accepted 16858 declarations (--verified)"; "nanoda kernel accepts the solution"; "Lean default kernel accepts the solution"; **"Your solution is okay!"** (exit 0) |
| Negative control: Challenge changed to `loopCount 6 = 25` | same script | rejected: "Challenge and solution theorem statement do not match: 'DictoLoopEquality.loopCount_values'" (exit 1) |
| `formalization.yaml` mechanical minimum | PalomarSubmission `scripts/submission_contract.py`, `load_formalization_metadata` and `normalized_provenance` (@ 14aa8d6) | pass; derived `result_origin: source-based`, `repository_role: substantive-development`; the arXiv and MSC codes are accepted by its taxonomies |
| Source `type` values allowed by policy (CONTRIBUTING §3: paper, book, web discussion, folklore, original-proof, other) | policy text; the Python validator does not enforce it | first draft used `article` and `web post`, flagged by the replay below; fixed to `paper` and `web discussion` |
| Licence | the template's `LICENSE`, byte-identical | Apache-2.0, matching `project.license`. Not machine-detected: `licensee` (Ruby) is not installed on either machine |

## A fault found and fixed

The first comparator run failed: `Const does not match between challenge and target 'DictoLoopEquality.nbr'`. Lean shares auxiliary proof terms between definitions in the same file. In the single Challenge file, `nbr` reused `Bond._proof_1`; in the library, `nbr` sits in its own module and has its own `nbr._proof_1`. So a Solution that only re-exports the library can never match a one-file Challenge exactly.

**Fix:** the template layout. `Solution.lean` is now the Challenge, word for word, with proofs. The library moved to its own namespace, `LoopEqualityProof`. Each Solution proof transfers the library theorem by definitional unfolding. Five small transfer lemmas cover the recursive definitions (`W`, `cA`, `nbD`, `FD`, `dataW`), and `loopCount_eq_proof` covers the count. The values are checked again by `decide` and `decide +kernel`. The mathematics and every statement are unchanged.

This also settles the question left open in README ("check that the comparator accepts declarations proved in imported modules"). It does, for theorems. The definitions, though, must be the Solution's own.

## What could not be run, and why

- **The PalomarSubmission reusable workflow** (`verify_submission.py prepare/execute`, profile `palomar-standard-v1`). It clones the entry from a public GitHub repository at a 40-character commit and runs on GitHub Actions. The brief forbids creating or pushing a repository, so it was not run. Its pieces were run locally instead (table above). What remains unrun is the following:
  - the protected compile of the Challenge under a per-run alias;
  - the export-based comparison (`--challenge-from-export`);
  - the bubblewrap/seccomp sandbox of the build;
  - Challenge rendering with Verso;
  - the licence detector.
- **The Ruby metadata validator** (`scripts/validate-formalization.rb`): Ruby is not installed. Palomar's own Python validator was run instead.
- **The doc build** (`docbuild/`, doc-gen4): it is optional for submission and was not run.

## Warnings in the build (not failures)

The proof library uses some deprecated Mathlib names (`if_true`, `if_false`, `if_pos`-style lemmas renamed to `ite_true`, `ite_eq_left`, and so on), and there is one unused hypothesis. Lean prints warnings for these. They do not affect the check and could be tidied before a submission.

## The package

- On the compute host: `lean/palomar-entry-loop-equality/`. It is a local git repository with **no remote**. Its head is `26fc5846ddb240b8be60fab5e6837462a1f71970`; the second commit changed only text (README, formalization.yaml), not Lean. Its `.lake/` is not committed.
- Its text files are copied in `entry/`, which has the same content as that commit.
- The entry is one Comparator configuration (`comparator.json`) with 17 theorems, so it is one Palomar entry. The Fibonacci corollary is in the same entry because Palomar reviews a configuration as a whole and lets related corollaries be grouped (policy prompt 04). On its own the corollary would be judged an instance of the main theorem.
