# Palomar submission kit

DICTO's reusable framework for Lean entries in the Palomar registry, built from the three entries that went through it:
Kulaichev's Śrī Yantra (published), the Dehn Canon (PALOMAR-2026-11-20-000003) and Grünbaum's zone question at k = 10.
DICTO, 20 November 2026: "we build our own submittable submission framework as we go". Every lesson is in
[CHECKLIST.md](CHECKLIST.md); add new ones there, and a mechanical check to `scripts/preflight_checks.py` where possible.

## Start a new entry in five steps

1. **Choose and pre-score.** Make a study folder `studies/<date>-palomar-<subject>/`. Do the prior-art and priority
   checks (CHECKLIST A), then the blind pre-score of each candidate scope (`prescore/README.md`). Go on only with a
   candidate at notability 4 in both scores, and with DICTO's word.
2. **Configure and start.** Copy `entry.example.toml` to the study folder as `entry.toml` and fill in the names DICTO
   chose and the 12-character request id. Then
   `python3 -I palomar-kit/scripts/new_entry.py --config entry.toml <lean-folder>` writes the skeleton: lakefile,
   pinned toolchain, Challenge and Solution, comparator.json, formalization.yaml (with the source rule as comments),
   README, LICENSE, Palomar's template scripts and the pinned preflight workflow.
3. **Build and check on the compute host.** Write the library, the Challenge and the Solution (generated from the
   library sources), fill in `formalization.yaml`, then: build; `#print axioms`; the comparator in one run
   (`run_comparator_full.sh`) or in steps (`run_comparator_split.sh`); the fit check for both profiles
   (`fit_check.sh`); the three negative controls (`run_negative_controls.sh`). Each script takes `ENTRY=<folder>` and
   ends with `FINAL ok` or `FINAL FAIL`. Then the second blind pre-score.
4. **Assemble and preflight.** `python3 -I palomar-kit/scripts/assemble_entry.py --config entry.toml <repo-folder> --git`
   builds the repository (author DICTO, no-reply address, plain messages, no trailers). On the interface machine,
   `python3 -I palomar-kit/scripts/preflight_checks.py <repo-folder> --config entry.toml [--axioms-log <log>]` must end
   `FINAL ok`. With DICTO's approval, create the GitHub repository, push, dispatch the preflight workflow and follow it
   with `PREFLIGHT=<owner>/<repo> bash palomar-kit/scripts/watch_run.sh` (as a logged background job).
5. **Submit and record.** `python3 -I palomar-kit/scripts/form_answers.py <repo-folder> --config entry.toml` prints
   the form answers; DICTO submits at submit.palomar-registry.org. Follow the registry's runs with
   `read_report.py --find <owner>/<repo>`; after registration record the PALOMAR id, read the public record with
   `read_report.py --entry <ID>`, and cite it in the paper's next version.

## Contents

- `CHECKLIST.md`: every lesson, in workflow order.
- `entry.example.toml`: the entry configuration every script reads. `examples/`: the Grünbaum k = 10 and Dehn Canon
  configurations.
- `template/`: the repository layout. `lakefile.toml.in`, `lean-toolchain` (v4.35.0-rc2), `Challenge.lean.in`,
  `Solution.lean.in`, `comparator.json.in`, `README.md.in`, `formalization.yaml.in` (person records with ORCID; source
  rule as comments), `LICENSE` (Apache-2.0), `gitignore`, `scripts/` (Palomar's entry-template `check-lean-sources.py`
  and `verify-comparator.sh`), `.github/workflows/palomar-preflight.yml.in` (manual dispatch only, pinned to
  PalomarSubmission 14aa8d6, `@REQUEST_ID@` placeholder). Tokens `@NAME@`, `@TITLE@`, `@LIBRARY@`, `@THEOREM1@`,
  `@THEOREMS@`, `@DEFINITIONS@`, `@REQUEST_ID@` are filled from entry.toml.
- `scripts/` (Python scripts run with `python3 -I`; shell scripts on the compute host):
  - `new_entry.py`: the skeleton of a new entry from the template.
  - `assemble_entry.py`: the entry repository from a finished Lean project; `--git` makes the two commits.
  - `preflight_checks.py`: every check that needs no Lean build, including Palomar's own parser and source scan at the
    pinned commit (cloned once into `~/.cache/palomar-kit/`, or `$PALOMAR_SUBMISSION_DIR`).
  - `run_comparator_full.sh`, `run_comparator_split.sh`: the comparator in one run, or as export, judge and one step per
    kernel, each within a 280 s foreground limit, with wall time and peak memory.
  - `run_negative_controls.sh` with `mutate.py`: the three mutations, each of which must be rejected.
  - `fit_check.sh`: Palomar's runner profiles (`namespace` 16 CPUs / 32 GB, the profile actually used; `standard`
    4 CPUs / 16 GB), with a summary line per step in `logs/fit/SUMMARY.tsv`.
  - `watch_run.sh`, `read_report.py`: wait for a run, read its mechanical report from the artifact zip in memory
    (status, warnings, kernels, ORCID validation, resources), find a submission's runs by repository, read a public
    record.
  - `form_answers.py`: the submission form answers and the Notes text.
- `prescore/`: the blind pre-score step (policy files, scorer prompt, input template, `tally.py`).

## Settings outside the kit

- `PALOMAR_KIT_AUTHOR_EMAIL`: the author's commit address. If unset, the GitHub no-reply address is built from the
  account id GitHub reports, so no address is written into the kit.
- `~/.config/palomar-kit/private-words` (one word per line) and `PALOMAR_KIT_PRIVATE_WORDS` (comma-separated): extra
  private words for the privacy check. This machine's name and the `~/.ssh/config` hosts are always checked.
- Pins (`scripts/_kit.py`): PalomarSubmission 14aa8d6b3c2f14a8540605e37144560b9a00e7e7, Lean
  `leanprover/lean4:v4.35.0-rc2`, Mathlib `v4.35.0-rc2`, PalomarPolicy 28bd48b for the pre-score. Change a pin only
  after checking Palomar's current documentation, and note it in CHECKLIST.md.

Credit: `template/scripts/` come from Palomar's entry template, and the parser, source scan, profiles and report
format the scripts read are PalomarSubmission's (PalomarRegistry, MIT licence); the pre-score policy files are
PalomarPolicy's text, copied unchanged.
