# Reproduction: Tsiokos, A Strongly Aperiodic Monotile in Three Dimensions (Chair44 / R44; aiXiv 2609.02383, arXiv 2609.19214)
DICTO 12 Nov 2026 (reproductions closest to the Concordance; many birds: we build our RD bridge on this chair).
## A. Author's code rerun (github.com/ioannist/six-birds-tiles, commit d53d224; code read first: standard library, no network, writes
only its own reports; run by DICTO in this session, 12 Nov)
- verify/replay.py: boundary_sphere PASS (V 2138, E 6408, F 4272, chi 2); tube_formula_controls PASS (4800 cases);
  substitution_modular_coincidence PASS (168 labels, primitive exponent 3, coincidence depth 3); seed_language_closure PASS (closure
  168 -> 600 -> 1278 -> 1398 -> 1410, stable; 27 fixed seeds; frame commutation 12096 + 576 checks).
- Packet einstein_macrostate (verify.py + edge_audit.py) PASS; its asserted numbers: contact closure 21 -> 30; 372 signed rows, 12
  components; 2388 raw contacts, 44 legal, all proper; orientation group 24; 33 first shells; central completion 14 pass / 18 dead;
  parent census 697 -> 116 -> 44 equal to the fine atlas; closed triangle mesh, chi 2.
- Packet r44_unrestricted_alignment (the off-lattice companion census, 6862 -> 44): COULD NOT RUN from the public repository: its input
  upstream/einstein_r44_proof_submission.zip is excluded by the release's .gitignore ("duplicate upstream ZIPs"), so replay.py stops
  there. Not a failure of the result; a gap in the public package (to tell the author).
## B. Independent recomputation (our own code, `scripts/census.py`, from the paper's §2 recipe and his panel table)
- Our 192 feature apexes = the 192 apexes of his exact solid file.
- 2388 touching lattice-registered poses (all 48 signed frames); exactly 44 legal (every bump meets a dent of equal size); all 44
  proper rotations (homochiral). Control: one feature's sign flipped -> 34 legal.
- The combinatorial certificate behind these 44 (closure 30 -> 44 -> 44, 135 face rules, 33 / 18 / 15 shells, unique parents) was
  recomputed independently in studies/2026-11-12-repro-kamenetsky (Kamenetsky's frame-marking reproduces the Chair44 statistics).
- Slip on the way: our first touching count (1902) used too small a box (same fault as recount.py); fixed and guarded (no pose may lie
  on the box edge).
Not covered: the Lean development; the unrestricted (off-lattice) alignment census (archive missing from the public release).
Run by Claude Code (Opus) for DICTO.
