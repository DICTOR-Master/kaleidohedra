# Palomar pre-score: the Lean Dehn work (19 November 2026)

**Verdict: D1 (Hilbert's third problem with the set-defined Dehn invariant and the geometric bridge) scores notability 4 / literature 4 from both blind scorers, at the floor. D2 (the complete canon) scores notability 3 (failure) from both. Submit D1, if at all; the canon belongs with it as worked corollaries, not as its own entry. Nothing was submitted; submission only on DICTO's word.**

Method as in studies/2026-11-16-palomar-yantra (copied policy files in blind/policy, byte-identical): neutral blind inputs (blind/inputs/D1-hilbert3-geometric.md, D2-dehn-canon.md) disclosing the prior Lean formalization (FormalBook ch. 10) and the results known on paper; two fresh scorers per candidate, each given only the policy and one input, web read-only; outputs summarised in blind/blind-{A,B}-{D1,D2}.json.

| candidate | scorer A | scorer B |
|---|---|---|
| D1 | 4 / 4, neutral | 4 / 4, neutral |
| D2 | 3 / 4, failure | 3 / 4, failure |

Why D1 holds 4 and not more: the theorem is classical and already formalized in Lean (FormalBook, abstract model); the contribution is the set-level invariant and the bridge FormalBook says it lacks; restricted scope (convex pieces, one tetrahedron model, the cube).
Why D2 fails: nearly all invariants and the angle independence are on paper (Conway–Radin–Sadun; Ogievetsky–Papadopolos); scorer B: β = (π + γ − α)/2, so the joint independence follows from Conway–Radin–Sadun directly (the paper should say so); the solid list is hand-picked; only FUJI is not on paper.

What would raise D1 (both scorers): Hilbert's literal statement (two tetrahedra of equal base and height not scissors congruent); the bridge as headline for finite unions; dehnSet = classical edge sum for every convex polytope; cite Hartshorne (Geometry: Euclid and Beyond, ch. 27), Boltianskii 1978, Sah 1979, Dupont 2001, Benko 2007, Zakharevich; credit Hadwiger/Groemer for the valuation extension; pin the other formalizations' commits; a real Challenge file and Comparator configuration; Sydler's converse (long term).

## The D1 entry package (19 November 2026)

**Result: the Challenge, the Comparator configuration and the metadata are built, and the comparator accepts the Solution with all three kernels (Lean's kernel, NanoDa, con-ron). Three altered copies are each rejected. Nothing was submitted and no repository was created.** Everything is in `package/`, laid out as the approved Yantra entry (`studies/2026-11-15-yantra-box-certificate/lean/Challenge`, `lean/palomar`).

**The Challenge** (`package/Challenge/HilbertThird.lean`; Mathlib only; 332 lines, 16,567 bytes; namespace `HilbertThird`, a placeholder name). `package/scripts/gen_challenge.py` writes it from the Lean sources of studies lean-dehn-1 to -10, as the GET study's `gen_statement.py` did: each definition and statement is copied character for character, with its file's `open` lines, the `variable` commands in scope at it and any `omit … in` line. One doc comment loses a reference to "study 2" (`DOC_FIX`); no statement or definition is changed. It holds every definition the statements need, in full: `ratPi`, `Angle`, `DehnSpace`, `sol`, `IsPoly`, `tcone`, `linSpace`, `wedgeSet`, `wedgeAngle`, `theta`, `edgeAngle`, `dehnSet`, `ScissorsCongruent`, `R3` and its `Fact (finrank ℝ R3 = 3)` instance, `tetN`, `tetraSet`, `cubeN`, `cubeSet`, `IsSimilarCopy`, `faceIn`, `IsEdge`, `edges`, `facetNormals`, `dihedral`, `EquiComplementable`. The five theorems:
1. `hilbert_third_problem` (study 10): two tetrahedra on one base triangle, both apexes at distance 1 from its plane, both volumes 1/6, neither scissors congruent nor equicomplementable;
2. `dehnSet_eq_edge_sum` (study 10): `dehnSet P` is the edge sum Σ length ⊗ dihedral angle for every convex polytope with interior points;
3. `dehnSet_eq_of_scissorsCongruent` (study 2): the bridge;
4. `dehnSum_eq_of_scissors` (study 2): the bridge for finite unions of convex polytopes (the scorers asked for this form as a headline);
5. `similarTetra_not_scissorsCongruent_similarCube` (study 4): Dehn's theorem for similar copies.

**The Solution** (`package/Solution/HilbertThird.lean`) is the Challenge word for word, with the imports of the development added and each `sorry` replaced by one line that applies the development's theorem (`exact DehnCanon.<name> …`); the transfer is by unfolding, since the definitions are the same texts. **The library** is the import closure of `Dehn10Hilbert` and `Dehn10Edges`: 32 of the 33 modules of studies 1 to 10 (not `Dehn9Same`; not the optional `Dehn2Hull`, which imports FormalBook), 15,521 lines, put in Palomar's module layout by `package/scripts/assemble_entry.py` (`module`, `public import`, `@[expose] public section`; nothing else changed). The script assembles the whole entry (lakefile, manifest, toolchain, comparator.json, LICENSE, README, formalization.yaml, scripts); `package/logs/entry-SHA256SUMS` lists the 47 assembled files.

**Comparator configuration** (`package/comparator.json`): the five theorems, no definition targets, axioms `propext`, `Quot.sound`, `Classical.choice`, as for GET.

**What was run** (a separate workspace on the compute host, with the Mathlib packages linked from the GET workspace; the canon workspace untouched; every command in the foreground under a 280 s limit and a 14 GB memory cap without swap):
- **Build** (`scripts/build.sh`, six chunks from an empty project build folder, Mathlib prebuilt): 4 min 22 s of wall time in all; the largest single Lean process peaked at 4.5 GB. No errors, no warnings except the five intended `sorry` of the Challenge (`logs/build-chunks.log`).
- **Axioms** (`logs/axioms.log`): all five theorems, seen from the Solution, give `[propext, Classical.choice, Quot.sound]`. No `sorry` and no `native_decide` in the library or the Solution.
- **Source rules**: Palomar's `check-lean-sources.py` passes (module headers, line limits, Challenge size). Palomar's own metadata parser (`submission_contract.py` of PalomarSubmission) loads `formalization.yaml` and derives `result_origin: source-based`.
- **Comparator, the template script unchanged** (`logs/comparator-template.log`): "Your solution is okay!". con-ron accepts 54,369 declarations (`--verified`), NanoDa accepts, Lean's default kernel accepts. **2 min 15 s** of wall time; **memory peak 2.98 GB** for the whole run (the cgroup's `memory.peak`), 0.88 GB for the largest single process. A second run with con-ron at 4 workers (`logs/comparator-conron4.log`) gives the same verdict in 3 min 23 s.
- **Calibration**: a copy whose Challenge only gains a comment line is accepted (`logs/positive-control-z.txt`).
- **Negative controls** (`scripts/run_negative_controls.sh`, each in its own scratch copy, through the unchanged template comparator; `logs/negative/`). **All three are rejected:**
  - (a) one constant in a Challenge statement changed (the first volume 1/6 of `hilbert_third_problem` → 1/7): "Challenge and solution theorem statement do not match: 'HilbertThird.hilbert_third_problem'" (51 s, 1.56 GB);
  - (b) one Challenge definition changed (`wedgeAngle` measures with π instead of 2π; no theorem text touched): "Const does not match between challenge and target 'HilbertThird.tetN'" (40 s, 1.56 GB). The name is `tetN`, not `wedgeAngle`, because Lean shares one auxiliary proof term between the two definitions: in the real Challenge `tetN` refers to `wedgeAngle._proof_1`, and once `wedgeAngle` no longer makes it, `tetN` makes its own (checked by `#print` with `pp.all`; `logs/negative/b-why-tetN.txt`). The rejection follows from the changed definition;
  - (c) one Solution proof (`dehnSet_eq_edge_sum`) replaced by `sorry`: `#print axioms` lists `sorryAx`, and the comparator says "Illegal axiom detected: 'sorryAx'" (1 min 20 s, 1.56 GB).
- Not run: a fit check under Palomar's runner limits (4 cores, 16 GB) like the Yantra entry's. The build here ran with lake's default parallelism; its largest process was 4.5 GB and the comparator's whole run 2.98 GB.

**Metadata** (`package/palomar/formalization.yaml`, `package/palomar/README.md`). Author DICTO; AI use declared as in the Yantra entry (method `agent`, models "Claude Opus (Anthropic)", framework "Claude Code (Opus)", subscription-based, no human line-by-line audit). Provenance: source-based; it `formalizes` Dehn (1901) and Hilbert (1900, problem 3, in Newson's translation). FormalBook chapter 10 (commit 54da1ce, the file read) is credited under `related_formalizations` as the first Lean formalization of the problem, with the same pair of tetrahedra in its abstract model; atlas-lean, proof_in_the_book and lean-genius follow, each pinned to the last commit touching its file up to 19 November 2026. Sources as in the paper's §9: Jessen, Aigner–Ziegler, Sydler, Hartshorne, Hadwiger, Groemer, Boltianskii, Sah, Dupont, Benko, Campbell–Zakharevich, Niven (with Mathlib's Meiburg–Broshi), and DICTO's draft paper; the DOIs of Dehn, Groemer and Benko were checked on Crossref. Each source says whether it was read, partly read or only cited.

**Open before any submission (DICTO's word only):** the namespace name `HilbertThird` (placeholder); whether the draft paper is published first (then it can be cited with a DOI); a second blind score of D1 with study 10's theorems; Sydler's converse stays out.

## Second pre-score: the finished entry D1b (19 November 2026, night)

Input blind/inputs/D1b-hilbert3-entry.md quotes the Challenge file in full. Two fresh scorers, same policy files.

| candidate | scorer A | scorer B |
|---|---|---|
| D1b (Hilbert's sentence for point sets, edge-sum identity, bridge incl. finite unions, Dehn's theorem) | 4 / 4, neutral | 4 / 4, neutral |

Both verified FormalBook (54da1ce, PR #157) and atlas-lean at the pinned commits and found our account accurate. Scorer A: the mathematics alone could support 5; held at 4 because the theorem is already in Lean (FormalBook). Still at the floor, but steady: four of four D1 scores are 4.
Cheap improvements both named (citations only): Dehn's 1900 Göttingen note "Über raumgleiche Polyeder" (Nachr. Ges. Wiss. Göttingen 1900, 345–354) and the Math. Ann. year; Bricard 1896; Aigner–Ziegler edition and pages; Newson's Bull. AMS scan page; a sentence naming the research audience (a base for Sydler's converse, Jessen's 4D case, valuations in Mathlib); make the paper public as a dated preprint; dated library/Zulip searches.

## The entry as DehnCanon, with the paper's DOI (20 November 2026)

**Result: the entry is renamed DehnCanon, cites the published paper (#113, DICTO DOI 10.5281/zenodo.24383552), and was rebuilt and re-verified from an empty build folder: the comparator accepts the Solution with all three kernels and rejects the three altered copies. Nothing was submitted.**

DICTO's decisions (20 November): namespace and entry name `DehnCanon`; title "The Dehn Canon: Hilbert's Third Problem, Machine-Checked", subtitle "From the solids up, deciding every pair of the canon"; the paper released on Zenodo first.

- **Renamed:** `Challenge/HilbertThird.lean` → `Challenge/DehnCanon.lean`, `Solution/HilbertThird.lean` → `Solution/DehnCanon.lean`; namespace `HilbertThird` → `DehnCanon` in the Challenge, the Solution, `comparator.json` (five theorem names), `formalization.yaml` (`alignment`), the scripts, and the Lake package name (`lakefile.toml`, `lake-manifest.json`).
- **The library's namespace is now `DehnCanon.Library`.** The development itself uses the namespace `DehnCanon`; with the entry's namespace also `DehnCanon`, the Solution (which imports the library and repeats the Challenge's definitions) would declare every name twice. `assemble_entry.py` therefore renames, in the assembled library only, `namespace DehnCanon`/`end DehnCanon` to `DehnCanon.Library` and the six qualified names `DehnCanon.x` (all in `Dehn6Pairs.lean`) to `DehnCanon.Library.x`; nothing else in the library changes, and module paths stay `DehnCanon.*`. The Solution's five proofs read `exact DehnCanon.Library.<name> …`.
- **Metadata:** `project.name` is the paper's title. The paper is a source with `relationship: formalizes` (type `paper`, id the concept DOI `doi:10.5281/zenodo.24383552`, location naming version 1, `doi:10.5281/zenodo.24383553`): its Theorem 4, Corollary 4′, Theorems 6, 6′ and 6″ are the five statements (checked against the published text). Under the source rule the entry stays source-based (Dehn 1900/1901 and Hilbert 1900 `formalizes`; no `original-proof` source). The entry README cites the paper.
- **Build** (`logs/build-chunks.log`, seven foreground chunks, each under the 280 s limit): 3 min 40 s in all, largest process 4.5 GB; no errors, no warnings except the five intended `sorry` of the Challenge.
- **Axioms** (`logs/axioms.log`): all five theorems from the Solution: `[propext, Classical.choice, Quot.sound]`. No `sorry` or `native_decide` in the library or the Solution. `check-lean-sources.py` passes.
- **Comparator, template script unchanged** (`logs/comparator-template.log`): "Your solution is okay!"; con-ron accepts 54,369 declarations (`--verified`), NanoDa accepts, Lean's kernel accepts; 2 min 6 s, memory peak 3.04 GB for the whole run, 0.89 GB for the largest process.
- **Negative controls** (`logs/negative/`), all rejected: (a) volume 1/6 → 1/7: "Challenge and solution theorem statement do not match: 'DehnCanon.hilbert_third_problem'" (39 s, 1.56 GB); (b) `wedgeAngle` with π for 2π: "Const does not match between challenge and target 'DehnCanon.tetN'" (41 s, 1.56 GB; why `tetN`: `b-why-tetN.txt`, from the earlier build, same mechanism); (c) `dehnSet_eq_edge_sum`'s proof → `sorry`: "Illegal axiom detected: 'sorryAx'" (42 s, 1.55 GB).
- **Palomar's parser** (`submission_contract.py`: `load_formalization_metadata`, `normalized_provenance`) loads the final `formalization.yaml`: `result_origin: source-based`, `repository_role: substantive-development`, 17 sources, 4 related formalizations.
- `logs/entry-SHA256SUMS` lists the 47 assembled files again. Not rerun this time: the con-ron 4-worker run and the comment-line calibration (their logs from the earlier build were removed).

## Fit check under Palomar's runner limits, and the repository (20 November 2026)

DICTO (20 November): keep `DehnCanon.Library`; "Fit check, then submit".

**Fit check: passes, far inside the limits** (`package/scripts/run_fit_check.sh`, logs `package/logs/fit/`). Every step ran on 4 CPUs (`taskset -c 0-3`, `LEAN_NUM_THREADS=4`) in a cgroup capped at 14 GB with no swap, from an empty build folder, each step in the foreground under 280 s:
- build, in four calls (lake resumes between them; the last is Palomar's `lake build Solution`): 36 s, 35 s, 2 min 28 s, 19 s, about 4 min in all; memory peak 2.78 GB (largest single process 4.5 GB RSS, shared pages included); at most 2 Lean processes at once;
- comparator, the template script with con-ron at 2 workers (Palomar's count): "Your solution is okay!" (con-ron, NanoDa and Lean's kernel accept) in 2 min 26 s, memory peak 2.50 GB.
The build in steps can only understate a peak if two heavy modules would run together across a step boundary; with peaks under 3 GB against 16 GB that margin does not matter.

**Repository: not created.** The standalone repository was assembled locally exactly like the Yantra entry's (the 47 entry files without SHA256SUMS; a second commit adds the manual-dispatch preflight workflow pinned to PalomarSubmission 14aa8d6, request id `dehncanon001`; author DICTO with the GitHub no-reply address), but creating the public GitHub repository was refused by the permission system, so nothing was pushed and nothing was submitted. Submission itself goes through Palomar's web form (submit.palomar-registry.org), which needs DICTO's GitHub login.

## Submission (20 Nov 2026)

Submitted by DICTO 02:19Z (repo DICTOR-Master/dehn-canon-lean, commit 9ea20f6, verification run 44659975000). Verification success 02:29Z; Challenge renderability check passed 03:45Z; automated review 03:48Z: "No problems were identified" (no suggestions; scores are not shown to the submitter); DICTO asked for registration 03:49Z. Palomar has no human sign-off on review outcomes.

Registered on Palomar as **PALOMAR-2026-11-20-000003** (version 1), 20 Nov 2026.
