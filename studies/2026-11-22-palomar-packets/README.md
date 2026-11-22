# Palomar preflight: Dehn packets, Theorem 4 of #117 (22 November 2026)

DICTO asked (22 Nov) for a Palomar preflight of the Lean proof of Theorem 4 of #117 ("From Dehn Packets to Scutoids:
How the Fullerene Star Fills Space", DICTO DOI 10.5281/zenodo.24411660), following the kit (palomar-kit README steps
1-4, CHECKLIST). Source: the prepared repository `~/dehn-packets-lean` at commit ddb5f59 (study 2026-11-22-lean-packets).
Nothing is created on GitHub, pushed or dispatched: that is DICTO's step.

## Resume (22 Nov, exact-code generator; watched job `packets-fit` running)
- WHAT CHANGED: the generator (gen/gen_pieces.py, here and in studies/2026-11-22-lean-packets) now writes each solid as
  integer codes in Z[√d] (`Packets/Exact.lean`: `Zd`, `ev`, `zpos`, `Solid`, `Cert`) and proves `IsEdgeData`,
  boundedness, interior point, Gram values and independence of the normals from tables checked by `decide +kernel`
  (one generic soundness proof each). The per-corner `fin_cases <;> simp <;> grind` slack/sign/cover lemmas are gone.
  Measured before (GenTO): sign 414k, cover 276k, slack 267k proof objects; after: GenTO 159 lines (was 1806),
  .olean.private 1.8 MB (was 12.1 MB); the eight solids plus Solids build in 38 s on the host.
- The truncated icosidodecahedron is in (`GenTID.lean`, `SolidTID.lean`; helper in theorem4a/4b_copies; gen_challenge.py
  SOLIDS + "tid"). Warnings fixed: Copies `if_pos`/`if_neg` -> `↓reduceIte`; Solids unused simp args and `<;>`;
  generated files set the unused-tactic/seq-focus linters off as the Canon's generated files do.
- Run 1 of `packets-fit` FAILED (22 Nov 19:43): GenTID.lean timed out (200,000 heartbeats) elaborating its big
  `![...]` tables and the one-shot `tidN_eq`. Fixed in the generator for large solids: integer tables as flat
  `List ℤ` in chunks of 240 with `getD`, the bridge lemmas per face (code side by `decide +kernel`), and one top-level
  lemma per checked table. Pilot: the whole GenTID.lean compiles in 2 min 15 s in the foreground. Relaunched.
- JOB `packets-fit` (plan ~/dicto-alerts/plans/packets-fit.plan, cap 10 h, script package/scripts/run_fit_tid.sh):
  TID generation -> reference build -> library refresh (Canon imports renamed) -> gen_challenge -> run_checks.sh
  (namespace build, axioms, comparator, controls, standard profile) -> split con-ron timing. FINAL ok only if checks
  pass, standard profile passes and con-ron <= 15 min. Check: `tr -d "\000" < ~/dbb-logs/packets-fit.log | tail` on
  the compute host. Then: reassemble with the kit (assemble_entry.py --git) into a fresh folder, preflight_checks.py.

## Status box
- Job `packets-entry` ended FINAL ok (standard profile part stopped, see resume box).
- Assembled: `~/dehn-packets-lean` (commits d84010c entry, a9315d3 workflow); every built file identical (md5) to
  the copy built on the compute host. The prepared folder is kept as `~/dehn-packets-lean.ddb5f59`.
- Risks: con-ron took about 25 of Palomar's 30 minutes; the whole comparator 53 min (Dehn Canon: about 10 min in
  Palomar). The library warnings break the CHECKLIST's "no warnings" line; fixing them needs a rebuild and rerun.
- Names are placeholders for DICTO to approve: entry `DehnPackets`, title "Dehn Packets in Lean: two icosahedral
  pairs that cannot fill space", repository `dehn-packets-lean`, request id `dehnpacket01`.
- Step 1 (blind pre-score) NOT run: the frugal rule to 24 Nov allows no new agents. Notability risk: Theorem 4 is
  DICTO's own theorem; by the CHECKLIST pattern, entries of his own questions scored 2-3 (floor 4). Lemma 2 (behind
  Debrunner 1980) is the part someone else put in print.

## Decisions (kit gate)
- **The Canon is included, not a Git dependency.** Palomar allows pinned public GitHub dependencies for the Solution
  (PalomarSubmission README), but the Canon repository has root modules `Challenge.lean` and `Solution.lean`; an entry
  module `Challenge` would be shadowed (`challenge.module_root_shadowed`), and the kit (assemble_entry.py import guard,
  the comparator and control scripts) assumes `Challenge`/`Solution` and a Mathlib-only lakefile. So, as for the
  Dehn-Hadwiger 4D entry, `package/scripts/prep_library.py` copies the 26 Canon modules the library imports, unchanged
  from 9ea20f6, to `Packets/Canon/` (imports renamed `Packets.Canon.*`; namespace `DehnCanon.Library` kept).
  comparator.json then needs nothing special (Mathlib is the only requirement).
- **Challenge** (`package/scripts/gen_challenge.py`, header `challenge_header.md`): every definition and statement
  copied character for character from the library (the Canon's `sol`, `IsPoly`, `tcone`, `linSpace`, `wedgeSet`,
  `wedgeAngle`, `R3`; `α β γ`; `ConvexTiling`, `EdgeAngle`, `SimilarCopy`, `RationalAngles`; the eight solids' normals,
  offsets and sets), the qualifier `DehnCanon.Library.` dropped. Four theorems: `lemma3`, `lemma2`,
  `theorem4a_copies`, `theorem4b_copies` (the Canon entry had five, so several are fine). 300 lines, 16,013 bytes:
  within the preferred 300 / 32 KiB. To get there, the face-normal lists of the Gen files are written four to a line
  (whitespace only, checked in prep_library.py; `package/gen/gen_pieces.py` now writes them so).
- **Solution**: the Challenge word for word; each proof one `exact Packets.<name> ...`; a `ConvexTiling` is rebuilt
  from its fields as the library's structure (a structure is not unfolded like a definition).
- **formalization.yaml**: SOURCE-BASED, #117 `formalizes` (concept DOI, version 1 record 10.5281/zenodo.24411661);
  background: Aristotle's Pyramid #44 (Lemma 1), Debrunner 1980, Dehn 1901, Lagarias-Moews 1995, the Dehn Canon #113;
  related formalization: the Canon entry at 9ea20f6. The blueprint paper (draft #119) is not cited (unpublished).
  Automation section: Claude Code agent wrote the Lean; no human line-by-line audit.
- **Formal search** (22 Nov): GitHub code search of Lean files (Debrunner; dihedral angle tiling; truncated
  icosahedron; space-filling polyhedron; Dehn invariant tiling): nothing related; one hit
  (primaryhosting/brockian-mathematics @ 29426ff, aristotle/harvest_100/admin_8bae7410.lean) only names the truncated
  icosahedron's counts.
- **Repository**: the prepared commit ddb5f59 has a private e-mail as author, which the privacy check refuses; the
  entry is assembled fresh with the kit (author DICTO, no-reply address, no trailers) into `~/dehn-packets-lean`, the
  prepared folder kept beside it as `~/dehn-packets-lean.ddb5f59` (delete once DICTO agrees).

## Checks
| check | result |
|---|---|
| light preflight on a staging copy (no git) | FINAL ok (0 FAIL, 0 WARN) |
| build (namespace profile, 16 CPUs, clean) | ok: wall 15:29, peak 19.38 GiB; 63 linter/deprecation warnings in the library (Solids.lean 47, Copies.lean 8 `if_pos`/`if_neg`, one unused simp argument per Gen file), none in Challenge/Solution besides the 4 intended `sorry` |
| #print axioms (4 theorems, from the Solution) | ok: propext, Classical.choice, Quot.sound only (`package/logs/axioms.log`) |
| comparator, template run, namespace profile (con-ron --jobs=2) | ok "Your solution is okay": wall 52:42, peak 10.65 GiB; con-ron accepted 64,234 declarations in about 25 min (Palomar's con-ron cap: 30 min), then NanoDa and Lean's kernel |
| fit check | namespace profile (16 CPUs, 30 GB): build and comparator fit (peaks 19.38 / 10.65 GiB); standard profile (4 CPUs, 14 GB): first build stopped by SIGTERM (exit 143); rerun as job packets-standard |
| negative controls a, b, c | all REJECTED with the right reason: a (2π → 3π in lemma2) "theorem statement do not match: DehnPackets.lemma2"; b (`0 ≤ q ∧` dropped from RationalAngles) "Const does not match: DehnPackets.RationalAngles"; c (theorem4a_copies proof → sorry) "Illegal axiom detected: 'sorryAx'" |
| preflight_checks.py on ~/dehn-packets-lean (with --axioms-log) | FINAL ok: 0 FAIL, 0 WARN; git history 2 commits, DICTO, no-reply, no trailers |

## Files
- `package/entry.toml`: the kit configuration.
- `package/scripts/`: `prep_library.py`, `gen_challenge.py`, `challenge_header.md`, `run_checks.sh` (the dbb job).
- `package/gen/`: the solids' generator (copied into the entry's `scripts/`).
- `package/Challenge/`, `package/Solution/`, `package/palomar/` (formalization.yaml, README.md), `package/logs/`.
- `package/library/` is made by prep_library.py and not kept in git.
