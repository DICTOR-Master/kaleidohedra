# Optimality certificate for the fewest covers of #110 Theorem B′ (d)

Question (DICTO, 17 November 2026: "how can we have a proof that can't be verified?"): is the fewest number of dual copies
covering all 720 pentagons really 16 (A*), 16 (B*) and 22 (C3*)? Here a SAT solver writes a proof that no smaller cover
exists, and an independent proof checker verifies that proof.

## Method

- `make_cnf.py instance.json FAMILY K out.cnf` writes the statement "a cover with at most K copies" as a CNF formula: one
  variable per copy (120 copies for A* and B*, 60 for C3*), one clause per pentagon (some chosen copy covers it), and "at most K chosen" as a
  sequential counter (C. Sinz, *CP 2005*, LNCS 3709, pp. 827–831). There is no symmetry breaking, so the formula says exactly
  what the theorem says. The instance is `../dual_cover_instance.json`.
- CaDiCaL 3.0.1 (A. Biere et al.) proves the formulas at K = 15, 15 and 21 unsatisfiable (`--unsat`) and writes a DRAT proof.
- drat-trim (N. Wetzler, M. Heule and W. Hunt, *SAT 2014*, LNCS 8561, pp. 422–429) checks each proof against its formula.
- Controls: at K = 16, 16 and 22 the solver finds a model, and `verify_model.py` checks against the instance (not the CNF)
  that the chosen copies number at most K and cover all 720 pentagons. This shows the encoding admits real covers.
- `covercert.sh` runs all of these steps and ends with `FINAL ok` only if every control and every certificate passes.

## Result

| family | formula (vars / clauses) | solver | proof size | drat-trim | check time |
|---|---|---|---|---|---|
| A*, K = 15 | 1905 / 4394 | UNSAT | 1.0 GB | s VERIFIED | 860 s |
| B*, K = 15 | 1905 / 4394 | UNSAT | 4.6 GB | s VERIFIED | 7478 s |
| C3*, K = 21 | 1299 / 3236 | UNSAT | 63 MB | s VERIFIED | 35 s |

Controls A16, B16, C3-22: FINAL ok (real covers of 16, 16 and 22 copies). Overall: `FINAL ok`.

So there is no cover by 15 (A*), 15 (B*) or 21 (C3*) copies, and the covers of 16, 16 and 22 copies in the supporting data
are optimal. This agrees with HiGHS and CP-SAT (`../README.md`).

## To reproduce

Formulas are in `cnf/` (SHA-256: A15 `5a90214b…`, B15 `b1efeab8…`, C321 `6a08faff…`). The proofs are too large for the
repository (5.6 GB together). Regenerate them with `cadical --unsat cnf/X.cnf X.drat` and check them with
`drat-trim cnf/X.cnf X.drat`. The run logs are in `logs/`.
