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
   Not recomputed independently: the enclosure analysis (33 / 18 / 15) and Theorem B (2187 assignments); the first came from his code.
   One slip on the way: our first touching count (1902) used too small a search box; widened, 2388.
Run by Claude Code (Opus) for DICTO; Pi, under 10 s.
