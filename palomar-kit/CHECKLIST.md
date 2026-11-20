# Palomar entry checklist

Every lesson from the three entries so far, in the order of the work: Kulaichev's Śrī Yantra (published 17 Nov 2026),
the Dehn Canon (registered PALOMAR-2026-11-20-000003, 20 Nov 2026) and Grünbaum's zone question at k = 10 (preflight
passed, 20 Nov 2026). Study folders: `studies/2026-11-16-palomar-yantra`, `studies/2026-11-19-palomar-dehn`,
`studies/2026-11-20-palomar-grunbaum`, `studies/2026-11-20-palomar-grunbaum-prescore`.

## A. Choosing the result

- [ ] **Someone else's question or theorem.** Every entry that cleared notability 4 settles a question or proves a
      theorem that someone else put in print (Kulaichev 1984, Hilbert 1900 / Dehn 1901, Grünbaum 2010). Questions DICTO
      posed himself scored 2 to 3 (Loop Equality, Kyushindo, permutohedron).
- [ ] **Prior art and priority, before any building.** Search the literature and the web, including 3D-model and
      hobby sites (Sketchfab, vZome sharing pages, personal polyhedra pages, Wolfram Community). Grünbaum: the
      blind scorers found D. Hall's Sketchfab model of 2016, years before the source we had cited first.
- [ ] **Senechal-type check.** When a specialist has written on the same objects, read their paper by a free route.
      Their private reply is disclosed only as correspondence a reader cannot check, and no priority is claimed from it.
      A paper not read is marked "Not read" with the free routes tried. Never buy a paper.
- [ ] **Formal search, dated.** Mathlib, GitHub Lean code, the Isabelle AFP, and Rocq, HOL Light and Mizar by web
      search. Every related formalization is pinned to the commit of the file read (Dehn: FormalBook 54da1ce).
- [ ] **Exact citations.** Each page number is checked against the source itself (Yantra: Chiodo p. 381, not p. 384 as
      our files said). Each source in `formalization.yaml` says whether it was read, partly read or only cited.
- [ ] **Blind pre-score before building** (`prescore/`). Build only a candidate whose notability is 4 in both scores.
      A wider scope that does not raise notability stays in the paper (Dehn D2 scored 3; Grünbaum G2 did not move).

## B. The statement

- [ ] **Source rule** (`template/formalization.yaml.in`, top comment). Exactly one of ORIGINAL (one `original-proof`
      source, relationship `other`, everything else `background`/`other`) or SOURCE-BASED (no `original-proof`; at
      least one `formalizes` / `adapts` / `independently-proves`). If the Lean statement uses anything first stated in a
      cited paper, DICTO's own included, the entry is source-based and that paper is `formalizes`. Breaking this
      blocked the Yantra entry at review and cost a full resubmission (about 3.5 h of verification).
      Source types: paper, book, "web discussion", folklore, original-proof, other.
- [ ] **Names are DICTO's.** Entry name, namespace, title and repository name are his decisions. The library's
      namespace must differ from the entry's namespace, or the Solution declares every name twice (Dehn: library
      `DehnCanon.Library`, entry `DehnCanon`; `rename_namespace` in entry.toml).
- [ ] **DICTO's own paper first.** If the entry formalizes his paper, release the paper on Zenodo first so the entry
      cites it with a DOI (Dehn: #113).
- [ ] **Challenge size**: at most 300 lines and 32 KiB preferred (Palomar warns above this and records it in the
      trust reasons: Dehn's 333 lines), 1,000 lines and 100 KiB hard cap. Mathlib only, module form, every definition
      in full, every proof `sorry`.
- [ ] **Generated, not retyped.** Write the Challenge and the Solution mechanically from the library sources, so every
      definition and statement is the source text character for character (Dehn `gen_challenge.py`; GET
      `gen_statement.py`). The Solution is the Challenge word for word with imports added and each `sorry` replaced.
- [ ] **Calibration theorems** when a definition is new: show it gives the known answer on known objects (Grünbaum:
      the zone definition gives 4 for the cube and 6 for the rhombic dodecahedron).

## C. Metadata

- [ ] **ORCID from day one.** `authors` and `responsible_maintainers` are person records
      `{name: DICTO, orcid: 0009-0001-2620-2036, github: DICTOR-Master}` in the FIRST submission. Palomar validates the
      ORCID; adding it later means a resubmission.
- [ ] **Palomar's own parser** passes (`preflight_checks.py`: `load_formalization_metadata`, `normalized_provenance`,
      `declared_orcids` at the pinned commit) and reports the ORCID.
- [ ] **The abstract** (`project.description`) is also the form's Notes text: what is proved, who asked, what earlier
      work did and did not do, what is not formalized, the audience.
- [ ] **AI use** as in the three entries: method `agent`, models "Claude Opus (Anthropic)", framework "Claude Code
      (Opus)", subscription-based, no human line-by-line audit. Hardware "local Linux machines": no host names.

## D. Building and checking (compute host only; nothing heavy on the interface machine)

- [ ] **Build** from an empty build folder, every foreground call under 280 s (split a long build by targets; lake
      resumes). No warnings except the Challenge's intended `sorry`.
- [ ] **Axioms**: `#print axioms` of every theorem from the Solution gives only `propext`, `Classical.choice`,
      `Quot.sound`. No `sorry` and no `native_decide` anywhere outside the Challenge (`decide +kernel` is fine).
- [ ] **Split comparator** (`run_comparator_split.sh`) when the template run does not finish in 280 s: export once,
      then the judge with Lean's kernel, then NanoDa, then con-ron, each a separate step with wall time and peak memory.
- [ ] **Fit check at the real profile** (`fit_check.sh`, record both): Palomar ran the Dehn submission on
      `palomar-namespace-16x32-v1` (16 CPUs, 32 GB; peak 8.24 GiB); the workflow's `palomar-standard-v1` is 4 CPUs,
      16 GB. con-ron runs with `--jobs=2` and an 1800 s budget; if it runs out of capacity after Lean's kernel and NanoDa
      pass, Palomar records "declined" with a warning, not a rejection (Grünbaum: con-ron needs 28.7 GB at 16 workers).
      Lower the build's peak if a module exceeds the runner (Yantra: from over 16 GB to 8.2 GB by chaining heavy
      modules). Splitting heavy `decide +kernel` checks made Lean's kernel slower (Grünbaum): measure before keeping.
- [ ] **Negative controls** (`run_negative_controls.sh`): a changed numeral in a statement, a weakened definition, a
      proof replaced by `sorry`; each must be REJECTED. A changed definition may be reported under another constant
      that shares an auxiliary proof term (Dehn: `wedgeAngle` changed, `tetN` reported); check why once.
- [ ] **Negative controls give a reason.** A control counts as rejected only when the comparator names a statement or
      constant mismatch or an illegal axiom; a build or git failure is no verdict (Dehn–Hadwiger 4D: a scratch folder
      on another filesystem broke the hard-linked packages, the comparator failed on git, and the old script reported
      REJECTED). Keep SCRATCH on the entry's filesystem.
- [ ] **Exit codes, not printed lines.** Every kit script exits non-zero with FINAL FAIL; wrappers use the exit code.
- [ ] **Kernel time of `decide +kernel` data.** The comparator replays every kernel check in each kernel; time Lean's
      kernel alone (`STEP=kernel K=lean`) early. Dehn–Hadwiger 4D: the 600-cell checks first cost about 3 min of kernel
      time (list membership by scanning, 72,000 dot products); flat integer records, index tables instead of
      membership scans, chunked lookups and a symmetry reduction (three generators, three representative corners)
      brought Lean's kernel step to 2 min 37 s.
- [ ] **Blind pre-score once after building**, with the real Challenge quoted in full and the literature corrected.

## E. Repository and submission

- [ ] **Assemble** (`assemble_entry.py --git`): author DICTO with the GitHub no-reply address, plain commit messages,
      no Co-Authored-By or session trailers, no SHA256SUMS in the repository.
- [ ] **Light preflight** on the interface machine (`preflight_checks.py`): request id, pins, Challenge size, parser,
      ORCID, Lean scan, privacy (no host names, home paths or e-mail addresses in any file or commit).
- [ ] **Request id** exactly 12 lowercase letters or digits (Palomar's `SUBMISSION_ID_RE`; Grünbaum's first id had 14
      characters and needed a fix commit).
- [ ] **Creating the public GitHub repository needs DICTO's approval** (the permission system refuses it otherwise).
      DICTO creates it or approves `gh repo create`; then push and dispatch the preflight workflow.
- [ ] **Preflight run passes** (`watch_run.sh PREFLIGHT=<owner>/<repo>`; report read with `read_report.py`, no
      extraction to disk). The commit that passed is the commit submitted.
- [ ] **Avoid resubmissions.** Every resubmission reruns verification, rendering and review from the start (Yantra:
      about 3.5 h). Everything above is checked before the first submission.
- [ ] **Submit** through the form at submit.palomar-registry.org with DICTO's GitHub login (`form_answers.py`:
      repository, full commit, `comparator.json`, relationship, the existing entry id for a new version, Notes).
- [ ] **Follow the run** (`read_report.py --find <owner>/<repo>`): verification (Dehn: about 10 min), Challenge
      renderability check, automated review. Review scores are not shown to the submitter.
- [ ] **Registration is final.** DICTO asks for registration after the review; there is no human sign-off.

## F. After registration

- [ ] **Record the PALOMAR id** (e.g. PALOMAR-2026-11-20-000003, version 1) in the study README, `concordance.json`
      and open-work.
- [ ] **The public record** is at `https://data.palomar-registry.org/entries/<ID>-v<N>.json`
      (`read_report.py --entry <ID> --version <N>`).
- [ ] **Paper version N+1** cites the Palomar entry (Dehn Canon Version 2, reference [33]).
- [ ] Add any new lesson to this checklist (and a check to `preflight_checks.py` where it can be checked mechanically).
