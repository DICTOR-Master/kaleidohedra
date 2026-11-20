# Palomar entry E2: the Dehn–Hadwiger invariant in four dimensions (20 November 2026)

**Verdict: the whole brief is proved in Lean and packaged. Fourteen theorems depend only on `propext`,
`Classical.choice` and `Quot.sound`. The comparator accepts the Solution with all three kernels, and three altered
copies are each rejected with the right reason. The fit check at Palomar's real profile passes, Palomar's own parser
and the kit's preflight pass, and the blind re-score gives 4 / 4 (neutral) from both scorers. The repository is
assembled locally only: it was not created on GitHub and nothing was submitted. The names below are placeholders for
DICTO to approve.**

DICTO's brief (20 November): the bridge first, then the six regular 4-polytopes, the 5-cell against the 600-cell
(stated only if true), the credits, and packaging with the Palomar kit.

## What is proved (Lean 4 v4.35.0-rc2, Mathlib v4.35.0-rc2)

The invariant is read from the set, as the 3D Dehn invariant of the Dehn Canon is. At each point, take the tangent
cone and its lineality space. Where that space has codimension 2, take the cone's angle in the orthogonal plane,
modulo ℚπ. The invariant is the sum of (n − 2)-dimensional Hausdorff measure ⊗ angle class, in ℝ ⊗[ℚ] (ℝ/ℚπ), in
every finite dimension (`DH1Def`).

1. **The bridge.** `dehnHadwiger_eq_of_scissorsCongruent`: scissors-congruent convex polytopes have equal invariant,
   in every finite-dimensional real inner product space. `dehnHadwigerSum_eq_of_scissors` gives the same for finite
   unions of convex polytopes. Pieces are convex polytopes moved by isometries, reflections included.
2. **Zero invariant:** the tesseract, the 16-cell, the 24-cell and the 120-cell.
3. **The 5-cell:** `dehnHadwiger_cell5_eq` is A₅ ⊗ arccos(1/4), and `dehnHadwiger_cell5_ne_zero`.
4. **The 600-cell:** `dehnHadwiger_cell600_eq` is A₆₀₀ ⊗ (4π/3 − arccos(1/4)), and `dehnHadwiger_cell600_ne_zero`.
   The 600-cell's dihedral angle is 4π/3 minus the 5-cell's. This is true, proved in Lean (`adj_class`), and agrees
   with the exact values of study 2026-11-20-600cell-5cell-zero.
5. **arccos(1/4) ∉ ℚπ** (`arccos_quarter_not_ratPi`, from Niven's theorem in Mathlib).
6. **Non-congruence across the split.** No similar copy of the 5-cell (`similarCell5_not_scissorsCongruent`) or of the
   600-cell (`similarCell600_not_scissorsCongruent`) is scissors congruent to a similar copy of the tesseract, the
   16-cell, the 24-cell or the 120-cell.
7. **The 5-cell against the 600-cell** (`similarCell5_not_scissorsCongruent_similarCell600`): no similar copies are
   scissors congruent. The two invariants are positive and negative multiples of A ⊗ arccos(1/4).

`#print axioms` for all fourteen theorems, seen from the Solution, gives `[propext, Classical.choice, Quot.sound]`
(`package/logs/axioms.log`). There is no `sorry` and no `native_decide` (`decide +kernel` only).

**How the 600-cell was done (new this session; parts 10 to 15).**
- The 600-cell is the polar of the 120-cell. Its 600 normals are given compactly in the Challenge by sign changes and
  coordinate orderings of seven ℤ[φ] vectors (`cell600Z`).
- At a ridge point the two tight facets must be neighbours across a triangle (`cell600_pair`). If a neighbour of
  facet p is tight, the equal-length lemma (`eq_of_mem_span_pair`) makes it the other tight normal. Otherwise the
  point is inside the facet: it is a positive barycentric combination of the four corners (`facet_bary`), and the
  second facet would contain all four corners, which is impossible.
- Exact data come from `scripts/gen600.py`, `emit600.py` and `make_dh12.py`: the 600 normals, the 120 corners and, for
  every facet, its four corners and four neighbours. They are checked in Lean by `decide +kernel` on flat integer
  records, with index tables against `cell600Z`.
- That every corner lies in the 600-cell is checked for three representative corners. The symmetry is three
  generators whose action on the normals is checked by tables.
- Positive area comes from a small square on one ridge (`area_pos_of_patch`, `chk_patch`).
- Lean's kernel time for these checks was cut from about 3 minutes to fit the 280 s step: flat records, index tables
  and the symmetry, in place of list scans and 72,000 dot products.

The development is in `lean/DehnHadwiger/` (DH1–DH15, 3,383 lines). The modules DH1–DH9 come from the stopped job:
the bridge, the zero cases and the 5-cell. All of them compiled; its only gap was the 600-cell. DH6 and DH8 lists
were reformatted for the line budget, and DH7 had deprecation and linter fixes. The library reuses 13 Dehn Canon
modules unchanged; `package/scripts/prep_library.py` puts them under `DehnHadwiger/Canon/`.

## The entry package (`package/`)

- **Challenge** (`package/Challenge/DehnHadwiger4D.lean`): 300 lines, 19,552 bytes, Mathlib only.
  `package/scripts/gen_challenge.py` writes it from the sources, copying every definition and statement character for
  character. Two sections share the opens and one `variable` line; one doc comment is reworded (`DOC_FIX`, the "line"
  of the 3D wording).
- **Solution:** the Challenge word for word, with each proof `exact DehnHadwiger.<name> …`.
- **Metadata** (`package/palomar/formalization.yaml`, `README.md`):
  - Source-based: Hadwiger 1954 `formalizes`. The background sources are Hadwiger 1957, Dehn 1901, Jessen 1968 and
    1972, Dupont–Sah 1990, Lagarias–Moews 1995, and DICTO's Dehn Canon paper (doi:10.5281/zenodo.24383552).
  - Person records: DICTO, ORCID 0009-0001-2620-2036, GitHub DICTOR-Master.
  - Request id `dehnhad4d001`.
  - Related formalizations, each pinned: the Dehn Canon entry (9ea20f6), FormalBook (54da1ce), atlas-lean (0ab82d4)
    and undergraduate-math-lean (fd2d40d).
- **Credits checked:**
  - Hadwiger 1954: Math. Ann. 127, 170–174, doi:10.1007/BF01361118 (Crossref). The DOI first guessed, BF01361117, is
    Carlitz's paper.
  - Hadwiger 1957: Springer, doi:10.1007/978-3-642-94702-5.
  - Dehn 1901: Math. Ann. 55, 465–478.
  - Jessen 1968: Math. Scand. 22, 241–256.
  - Jessen 1972: Nachr. Akad. Wiss. Göttingen II 1972, 47–53, Zbl 0262.52004 (zbMATH).
  - Dupont–Sah 1990: Acta Math. 164, 1–27.
  - Lagarias–Moews 1995: DCG 13, 573–583.
  - Each source is marked as cited only (not read). The citation of Coxeter's §8.7 was removed because it was not
    verified.
- **Build** from an empty build folder, in two foreground calls (89 s and 94 s): no warnings except the Challenge's
  14 intended `sorry` (`logs/build-clean-*.log`).
- **Comparator**, split into steps, each under 280 s (the kit's `run_comparator_split.sh`):
  - export: 21 s;
  - judge with Lean's kernel: "Your solution is okay!", 2 min 34 s, 9.5 GB;
  - Lean kernel alone: 2 min 37 s;
  - NanoDa accepts: 51 s, 6.7 GB;
  - con-ron accepts 54,301 declarations (`--verified`): 1 min 59 s at its own worker count, 31 GB.
  - At Palomar's `--jobs=2` con-ron does not finish within our 280 s limit. Palomar allows con-ron 1800 s; if it runs
    out of capacity there, Palomar records "declined" with a warning, not a rejection (checklist D).
  - The one-run template comparator does not fit 280 s (`comparator-template-cutoff.log`).
- **Fit check at Palomar's real profile** (`palomar-namespace-16x32-v1`, 16 CPUs, 30 GB cap; `logs/fit/SUMMARY.tsv`):
  - build: 1:30 and 1:26 (peak 9.1 GiB);
  - judge with Lean's kernel: 2:33 (8.9 GiB);
  - NanoDa: 0:51;
  - con-ron (own worker count): 2:02, at the 30 GiB cap.
- **Negative controls** (`logs/negative/`), all rejected:
  - (a) arccos(1/4) → arccos(1/5) in a statement: "theorem statement do not match";
  - (b) `thetaH` codimension 2 → 1: "Const does not match … 'DehnHadwiger4D.thetaH'";
  - (c) the proof of `dehnHadwiger_cell600_ne_zero` → `sorry`: "Illegal axiom detected: 'sorryAx'".
- **Palomar's parser and preflight** (`preflight_checks.py` at PalomarSubmission 14aa8d6): `FINAL ok`.
  - Parser: source-based, 8 sources, 4 related formalizations, ORCID read.
  - Challenge: 300 lines.
  - Lean scan and the axioms log: ok.
  - Privacy: no home paths, host names or e-mail addresses.
  - Git: 2 commits, author DICTO, no-reply address, no trailers.
  - The compute workspace matches the assembled repository file for file (40 checksums).
- **Repository:** assembled locally by `assemble_entry.py --git`, with two plain commits. It was not created on
  GitHub, not pushed and not submitted.

## Blind re-score (kit protocol, `blind/`)

Two fresh scorers each read the policy files (byte-identical to the kit's copy) and the input
`blind/inputs/E2b-dehn-hadwiger-4d.md`, which quotes the built Challenge in full. Their answers are kept verbatim in
`blind/raw/`.

| candidate | scorer A | scorer B |
|---|---|---|
| E2b (bridge + six 4-polytopes + non-congruence) | 4 / 4, neutral, 0 findings | 4 / 4, neutral, 0 findings |

**Where they are right**, with the action each needs (citations only; to do before any submission):
- Add the monographs: Boltianskii 1978, Sah 1979 and Dupont 2001. Cite a source for the "classical" result that the
  regular simplex is not scissors congruent to the cube.
- Note Lagarias–Moews: the tesseract, the 16-cell and the 24-cell tile ℝ⁴, so their zero invariant is expected. The
  120-cell and the 600-cell are the polytopes that do not tile.
- Say that Jessen 1972 and Dupont–Sah 1990 are both credited for completeness in dimension 4.
- Extend the formal search to the Isabelle AFP, Rocq, HOL Light and Mizar, with dates.
- Read Hadwiger 1954, or its Zbl review, and give the theorem number.

**Where they overstate:** nothing material. Scorer B's note on definition order does not apply, because the
configuration has no definition targets.

## Names for DICTO (placeholders)

- Entry and namespace: `DehnHadwiger4D`.
- Title: "The Dehn–Hadwiger invariant in four dimensions".
- Repository: `dehn-hadwiger-4d-lean`.
- Library: `DehnHadwiger`.
- Request id: `dehnhad4d001`.

## Kit fixes (two plain commits)

- c01b41d7: the comparator, fit-check, negative-control and watch scripts now exit non-zero on FINAL FAIL; before,
  they printed it and exited 0. Wrappers use the exit code. The judging binaries (lake, leanexport, leanchecker,
  nanoda_bin, con-ron) are checked in the entry's own toolchain, read from the workspace, before a step. The same
  exit fix is in the Grünbaum study's copies.
- e96e6d80: a negative control counts as rejected only when the comparator gives a rejection reason. A scratch
  folder on another filesystem had made the comparator fail on git, and the old script reported REJECTED. Checklist
  lessons were added.

## LEADS

- The citation additions above, then DICTO's word on the names, before creating the repository.
- Formalize the face-sum identity for every convex polytope in ℝ⁴ (both scorers' main lever for a higher score).
- Formalize Jessen's converse in ℝ⁴ (long term).

FINAL ok
