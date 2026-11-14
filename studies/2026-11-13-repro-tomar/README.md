**Filed in our own records, 14 November 2026: not posted on aiXiv.** The reproduction form there needs the author's process record, and this paper has none. Status by the coverage gate: Reproduced.

# Reproduction: Tomar, The all-contact case of the 24-cell conjecture (aiXiv 2610.02329 v1)
Conclusion: REPRODUCED (scope gate: all 8 numbered results covered). The whole supplement was rerun from scratch and every number
agrees; every proof was read line by line; no mathematical error or gap found. Report draft written for DICTO's read (not posted).

Sources (source/): the paper PDF (kept untracked), the supplement README (Zenodo 10.5281/zenodo.23602667), and the supplement's
one_sidedness/PROOF.md (the proofs behind Lemma 4.1).

## What was run (on the compute host; the author's scripts, placeholders filled in)
0. sha256sum -c SHA256SUMS: all OK.
1. Julia 1.10.12 + LasserreSphericalCodes 0.1.0, instantiated from its manifest.
2. Zonal entries: all 60 signatures from scratch (their_entries_ref.jl, clean package copy, no cache): 490 dimension-4 entries,
   per-signature counts equal to the shipped zonal_compare.log. No author zonal cache is shipped (the reference cache came from the
   repository of arXiv:2609.25120), so no entry-by-entry comparison was possible; exactness is tested downstream (steps 3, 4).
   5 signatures ran under the author's zonal_run.sh, 55 under our own scheduler calling the same script. 7 runs were stopped
   part-way (2 by the memory guard, 5 by a planned pause); their partial files were purged and recomputed from scratch.
3. prep_zonal_cache.jl + zonal_degree_check.py: same line as the shipped zonal_degree_check.log.
4. gen_exact.jl, 40 chunks (20 at a time): ALL 209 row files IDENTICAL to ex1416.sha256.
5. check_cert.jl (22 threads): ALL CHECKS PASSED, 63 OK lines as in CHECK_RESULT.txt; 2 pi^2 - KFIX = 8.0387480021787...;
   checker's printed bound with eps2 = 2.81e-12: T3*(C) >= 8.036977001467787...; with the proved eps2 = 2.8111e-12 the paper's
   8.0369770014675... (author's CHECK_RESULT.txt explains this).
6. Lemma 4.1: S0r - S0 = 2.70e-15 > 0; proved eps2 = 2.8110732894564e-12 < 2.8111e-12; verify_p3.py (22 processes) complete cover,
   0 failed, proved eps3 = 9.999965e-7 < 1e-6. p3 summary equals the shipped JSON on 13 of 14 keys; only wall-clock "sec"
   differs (1266.7 vs 518.1).
7. Remark 6.2 polytope: exact file byte-identical; verify_polytope.py all checks true (99 vertices, f-vector (99,198,123,24),
   volume 7.965569708623931 by triangulation and by Lawrence's formula, unit ball inside, min normal angle 54.604 deg).
8. det_run.sh, 20 workers: the memory guard stopped workers 9-20; rerun with the author's det_run_range.sh (chunks resume).
   Final aggregate: 969 + 969 + 74613 identities exact, missing chunks 0, ALL IDENTITIES EXACT ON THE FULL LATTICES; equal to
   the shipped detcheck_aggregate.log except the time line (57.6 vs 54.1 core-hours).

Deviations (no mathematics): memory thresholds lowered for a shared machine (start above 25 GB instead of 300/100 GB, 15 instead
of 150 in det_run_range.sh; guard below 8 GB instead of 120/40 GB); fewer workers (22 threads/processes, 20 workers).

## Logs (compute host, under the run folder)
job logs repro-tomar.log, repro-tomar2.log, repro-tomar2-cage.log, repro-tomar3.log, repro-tomar4.log, repro-tomar5.log,
repro-tomar6.log; logs/00_sha.log, 01_instantiate.log, 03_prep.log, 03_degree.log, 04_gen_1..40.log, 04_sha.log,
05_check_cert.log, 06_p2.log, 06_eps2.log, 06_p3.log, 07_exact_cc.log, 07_verify_polytope.log, 08_det_aggregate.log (first,
incomplete), 08b_det_aggregate.log (final). Drivers: tomar_full.sh, tomar_resume.sh, tomar_cont.sh, tomar_det_rerun.sh.

## Coverage (coverage.json; repro_scope_gate.py STATUS: Reproduced)
- Proof read line by line: Theorem 1.1 (Section 5, with equality case), Proposition 2.1, Corollary 2.2, Proposition 2.3,
  Lemma 2.4, Proposition 3.1; also Lemma 2.5 (quoted from [2], reproved in the paper). All correct.
- Recomputed: Theorem 3.2 (steps 2-5, 8) and Lemma 4.1 (step 6; PROOF.md also read line by line).
- Assumed, as the paper states: kissing number 24 (Musin), D4 uniqueness and the PSD pairing (de Laat-Leijenhorst-de Muinck
  Keizer), correctness of the package and of Julia/FLINT/Arb/cddlib.
- Wording notes only: Table 1 "found identical" does not name the reference (BUILD.md does); the checker's last bound line uses
  eps2 = 2.81e-12 (disclosed by the author).

Run by Claude Code (Opus) for DICTO.
