**Status (19 November 2026): set aside by DICTO as not viable for Palomar for now (pre-score 3). Not submitted.**

# Second Palomar entry, prepared locally: #43 Theorem 4, the octahedral constant 3 (15 November 2026)

**Conclusion.** The entry is packaged and mechanically green: build, comparator (Lean kernel, NanoDa, con-ron), axioms only `propext`, `Classical.choice`, `Quot.sound`, a wrong Challenge rejected, Palomar's Python metadata validator passed. The estimated score is **notability 2 out of 5, below the floor of 4, so it would be rejected**. Do not submit. Nothing was submitted, no repository was created, and nothing was pushed outside this research repository.

**Status:** closed as an estimate. Submission would need DICTO's word, and on this score it is not recommended.

## The result

Paper #43, *Kyushindo Cores* (version 3, doi:10.5281/zenodo.24153218), Theorem 4: a convex polytope S with octahedral rotational symmetry about O lies inside 3·P(S), where P(S) is the convex hull of the foot points of its face planes; 3 is sharp (cube). The Lean proof is the one of commit 909ad63a (study 2026-11-14-lean-loop-equality).

## What is new, honestly

- **Known:** the covering lemma (every octahedral orbit comes within arccos(1/√3) of every direction) is the upper bound for the diameter of the orbit space S²/O, recorded by Greenwald (2000) and Dunbar–Greenwald–McGowan–Searle (2009, Table 2).
- **Not found elsewhere:** the containment S ⊆ 3·P(S) for the foot-point hull. It follows from the known diameter in a few lines, so no stronger novelty claim is made.
- **Formalisation:** no earlier Lean formalisation of either statement was found.

## Files

- `entry/`: text copy of the package (Challenge.lean 89 lines, Solution.lean, Kyushindo/Proof.lean, comparator.json, formalization.yaml v0.4, README.md with the sources checked, lakefile, manifest, Apache-2.0 LICENSE from the template). The package itself is a local git repository with no remote.
- `PREFLIGHT.md`: every mechanical check, with results and what could not be run.
- `SCORE.md`: the blind replay of Palomar's seven policy steps, our own rubric reading, and the mathematics that could raise notability.
- `replay-review.json`: the replay's JSON for each step.

## Version (Palomar-ready) (16 November 2026)

Palomar now requires every committed Lean file of a submitted repository to use the module system (`module` first, module doc comments after it), with at most 10,000 physical lines per file and the Challenge within 1,000 lines and 100 KiB. DICTO approved making the work ready in this repository (16 Nov: "count them and do whichever fits").

- **Module form.** The 5 Lean files of `entry/` already start with `module` and use `public import` and `@[expose] public section`, so no file changed. `Challenge.lean` has 89 lines and 4,213 bytes.
- **Rebuild from the repository copy (job ymod-small2, FINAL ok).** Palomar's source check passes; the clean `lake build` completes (8,938 jobs); the comparator accepts the solution with con-ron (4 workers), NanoDa and Lean's kernel ("Your solution is okay!").
- **Whole repository.** `scripts/palomar_source_check.py` (repository root) checks every committed `.lean` file against these rules; it ends FINAL ok.
- The score estimate above is unchanged. Nothing was submitted, and no workflow or runner was added.
