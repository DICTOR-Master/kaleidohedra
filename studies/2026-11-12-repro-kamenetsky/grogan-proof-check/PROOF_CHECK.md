# Grogan, An Arithmetic Family of Aperiodic Tilings in Odd Prime Dimensions (aiXiv 2610.01307, Zenodo 23197680, v2): full check

Run by Claude Code (Opus) for DICTO, 12 Nov 2026. Earlier report (same day) covered only the contact-language result for p = 3, 5, 7
("Proposition E" in the v1 numbering; Proposition 3.2 in v2). This check covers all 26 numbered claims of v2
(coverage, claim by claim: ../grogan-coverage.json; scope gate STATUS: Reproduced).

## What was done
1. Lean, Theorem 1.3 (T5) and Theorem 1.4: both proofs rebuilt from the official toolchains (Lean 4.19.0 + mathlib v4.19.0; Lean
   4.35.0-rc2, commit 11acb17e, + mathlib 06535612; mathlib from its official cache, project modules compiled by us). Final declarations
   depend only on propext, Classical.choice, Quot.sound; no sorryAx; no sorry/admit/native_decide/custom axiom in the sources (one
   doc-comment mention of native_decide). The kernel-checked statements and definitions (IsTiling with arbitrary isometries, IsPeriod
   preserving the tile collection, EuclideanSymmetries, body = closure((carrier u bumps) \ dents)) match the paper. Our own parser
   confirms the Lean key literals equal the JSON specs + formula (14): 256 keys (T5), 1024 keys (T7).
2. Author code rerun (kind A), from the hash-checked package and its restored layout: package validation PASS (116 files); exact
   contact verifier d = 5: 36 204 candidates, 2 020 overlaps, 33 900 profile rejects, 284 proper mates, 0 improper; d = 7: 408 proper
   mates, 0 improper; both equal the frozen pose sets; certificate replay PASS; raw d = 5 enumeration PASS; finite-identity check PASS;
   contact-enumeration audit PASS (0 missing, 0 extra); quotient parent closure PASS (M = 284); uniform-prime and facet-closure checks
   PASS. Not runnable from the package: four audits of the author's working copies (Palomar source, recovered preprint) whose inputs are
   not shipped, a p = 3 calibration (no p = 3 spec shipped), and one deliberately bounded p = 5 geometry check (stops at its own CPU
   limit). None of these is a claim of the paper.
3. Own code (none of the author's): E for six (p, g, mu) choices = formula (6), sets equal the author's data at p = 5, 7, and the same
   set for mu = 1 and mu = 4 at p = 5; dissection at p = 3, 5, 7; all finite numbers of Lemma 7.1 from the JSON specs; the properness
   sign identity on all 256 CLARK keys; the Lean-literal binding above.
4. Line-by-line read of every proof (Sections 2-8, Appendix C), with the formulas lost in the PDF text read from the LaTeX source.

## Result
No error found; every computed number agrees. Limits stated by the paper itself and respected here: the seven-dimensional case
(HENRY) is proved in writing plus the exact 408-pose computation, not in Lean; the all-prime and dense-family theorems are ordinary
proofs. Mathlib's compiled library objects were taken from its official cache (the standard trusted base).

## Faults in our own checks during the run (none a mismatch with the paper)
See RUN_LOG.md: an emptied-path quoting fault, a missing-root build target, and two over-strict controls (axiom-line count; comment
mention of native_decide). Each was diagnosed, fixed, and the check rerun.
