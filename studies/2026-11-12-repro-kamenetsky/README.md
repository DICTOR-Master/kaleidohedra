# Reproduction: Kamenetsky, Towards Strongly Aperiodic Monotiles in Higher Dimensions (aiXiv 2610.00139, arXiv 2610.00916)
DICTO 12 Nov 2026: independent reproductions on aiXiv, closest to the Concordance first; "use our own runs as verifying methods".
**Verdict: REPRODUCED** (Theorem A, the N = 3 certificate: every number of the paper's Table 1 that we tested).
1. Author's code rerun (github.com/dimkadimon/Monotile-RN, commit b174f72; record in studies/2026-11-10-arxiv-scan): cert6.py N = 3 with
   the certified frames: closure 30 -> 44 -> 44, supertile poses = 2P*, |P*| 44, |F*| 135, 2388 touching, tight, 33 enclosures = 18
   dead + 15 live, 15/15 one supertile, 14 presence checks, 0 failures, CERTIFIED in 2 s. Wrong markings rejected (canonical; one child
   changed).
2. Independent recomputation (`scripts/recount.py`, our own code from the paper's definitions; none of his code imported): 2388
   touching lattice-registered poses; children partition 2C3, homochiral; |P0| = 30; closure 30 -> 44 -> 44 with Sigma(P*) = 2P*
   exactly and no offset pose; |F*| = 135; tight (the 44 poses are exactly those whose facet triples lie in F*). Control: the
   assignment with child (1,1,0) changed gives |P0| 47 and closure 47 -> 256 -> 1250 with offset poses (not closed), as his code.
   Enclosure analysis (`scripts/enclosures.py`, our own search): 33 enclosures of a tile, 18 dead, 15 live; exactly one compatible
   supertile in every live case; 1 already complete; 14 presence checks, 0 failures (39 s). Theorem B (`scripts/theoremB.py`, dbb,
   1107 s): of the 2187 homochiral assignments 3 close (each at 44), 6 fail by an offset pose, 2178 pass 300 poses; |Sigma(P0)| takes
   exactly the values 44, 62, 99, 103, 113, 114, 119, 158, 186, and the minimum 44 is attained by exactly the 3 closed ones.
   EVERY number of Theorems A and B is now recomputed with our own code (DICTO 12 Nov: "if we do something do it properly").
   One slip on the way: our first touching count (1902) used too small a search box; widened, 2388.
3. Cross-check with Grogan (aiXiv 2610.01307): his arithmetic child rule at p = 3 IS Kamenetsky's certified assignment after
   relabelling the axes (`scripts/grogan_p3.py`); |E| = 30, closure 30 -> 44 -> 44.
Run by Claude Code (Opus) for DICTO; Pi, under 10 s.

# Reproduction: Grogan, An Arithmetic Family of Aperiodic Tilings in Odd Prime Dimensions (aiXiv 2610.01307, Zenodo 23197680)
Scope (stated exactly): Proposition E, the least contact language of his arithmetic substitution, and its size formula.
Our own N-dimensional chair code (`scripts/grogan_pN.py`; none of his code run) with his child rule f_A(i) = mu g^|A| (i - z_A):
| p | g (ell) | our |E| | his formula | his data file | same set, contact by contact |
|---|---|---|---|---|---|
| 3 | 2 (2) | 30 | 30 | (none) | = Kamenetsky's certified marking up to axis relabelling |
| 5 | 2 (4) | 116 | 116 | p5_E.json, 116 | yes (0 only ours, 0 only his) |
| 7 | 6 (2) | 318 | 318 | p7_E.json, 318 | yes (0 only ours, 0 only his); dbb 348 s |
The children partition 2C_p and are proper rotations in all three. Not in scope: the CLARK polyhedral keys, the 5D Lean proof (already
independently kernel-checked per his package), the 7D physical result.
