# Independent reproductions on aiXiv (DICTO 12 Nov 2026)
DICTO: verify results of other members that sit on aiXiv (and Zenodo), up to one a day, short runs, in his name; "try to do it with
people as close to our concordance as possible"; "we could maybe use our own runs as verifying methods".
Two kinds (DICTO 12 Nov: "choose our battles", author-code reruns are quicker): (A) AUTHOR-CODE RERUN of every computational claim,
reported as such; (B) INDEPENDENT RECOMPUTATION with our own code where short and close to us. Only short runs; skip what ties us up.
Papers labelled ai-discovered or ai-authored: an author-code rerun is enough (DICTO 12 Nov); no published code -> skip.
Selection (DICTO 12 Nov: "cherry pick code that could benefit us", "as many birds with one boulder as possible"): rank by how many of
standing + reusable code for a gap or aim + a check of what we build on + Concordance closeness + short one run gives.
Rules: choose by closeness to the Concordance strands, never by who returns the favour; state exactly what was done (author's code
rerun / independent recomputation with our own code / proof read); every report says "run by Claude Code (Opus) for DICTO"; if a result
does not reproduce, write to the author on the paper's discussion first. Filing is a form on the paper page (DICTO's login).
## Candidates by closeness (aiXiv search on Concordance strand terms, 12 Nov; keyword noise removed)
| aiXiv | paper | strand | plan |
|---|---|---|---|
| 2610.00139 | Kamenetsky, Towards Strongly Aperiodic Monotiles in Higher Dimensions | aim 1 (one piece) | author's code rerun done 12 Nov (Theorem A: every Table 1 number; 2 wrong markings rejected); add an independent recount with our own code, then file |
| 2609.02383 | Tsiokos, A Strongly Aperiodic Monotile in Three Dimensions (Chair44) | aim 1 | the 2388 / 44 / 30 / 33 / 15 statistics via our recount (same chair, frame rule) |
| 2610.01307 | Grogan, An Arithmetic Family of Aperiodic Tilings in Odd Prime Dimensions | aim 1 | read; check the 3D/5D key counts if code is public |
| 2610.00447 | Winter, A relation between Mahler volume and flag number for convex polytopes | polar sweep (aim 2) | check the relation on our exact sweep solids |
| 2611.00413 | Akhmedova, Lam, Yost-Wolff, Two examples in amplituhedron tilings | laws (aim 2) | small cell counts, checkable |
| 2609.00642 | Yaskin, Polyhedral Subspaces of L_p and Polars of Zonotopes | polar | read first |

## Filed
| date | paper | kind | link |
|---|---|---|---|
| 2026-11-12 | Kamenetsky 2610.00139 | B: independent recomputation, Theorems A and B complete (author's code also rerun) | https://aixiv.online/abs/2610.00139 |
| 2026-11-12 | Grogan 2610.01307 | B: independent recomputation, scope Proposition E (p = 3, 5, 7) | https://aixiv.online/abs/2610.01307 |
| 2026-11-12 | Tsiokos 2609.02383 (Chair44) | A: author's replay (all gates except the off-lattice packet, archive not public) + B: our census 2388 -> 44 | https://aixiv.online/abs/2609.02383 |
| 2026-11-12 | Winter 2610.00447 | B: proof checked + our 108-polytope test | https://aixiv.online/abs/2610.00447 |
| 2026-11-12 | Hofscheier–Nill 2611.00775 | B: independent exact recomputation, Theorems 2.1 and 2.2 | https://aixiv.online/abs/2611.00775 |
| 2026-11-12 | Cremer 2610.01289 | B: our own max-clique search on all 7 colourings + DS1.18 table check | https://aixiv.online/abs/2610.01289 |
| 2026-11-12 | OpenAI 2610.00950 | B: every proof checked + every claim recomputed exactly | https://aixiv.online/abs/2610.00950 |

## Friends table: what each reproduction gives our back catalogue and aims (12 Nov 2026; DICTO: "newfound friends from our duplication work")
Aims: 1 bridge (periodic <-> aperiodic), 2 laws (positive geometry / canonical form = volume of the polar), 3 one piece, any stacking.
| paper (status) | their method / result | connects to | concrete next use |
|---|---|---|---|
| Kamenetsky 2610.00139 (filed, B complete) | certified frame marking + Theorem A (P*-tilings uniquely hierarchical) | aim 3: the RD bridge (90 / 62 / 118 marked RDs), 3D Hat plan | already the backbone of the 90-RD result; next: his open point 2 (non-lattice carrier) = our c/h stacking question |
| Tsiokos 2609.02383 Chair44 (filed) | bumps on the 7-cube chair force aperiodicity | aim 3; #97 Narcissus Keyed | bump-and-dent template for keying the 90 RDs exactly |
| Grogan 2610.01307 (filed; scope correction ready) | arithmetic child rule f_A(i) = mu g^|A|(i - z_A); keyed chairs in odd prime dimension | aim 3 "fewer pieces" step | template for merging marked RDs into chair-sized keyed pieces; his p = 3 rule = Kamenetsky's marking (our check) |
| Winter 2610.00447 (filed) | Mahler volume vs flag number | aim 2; Concordance: Mahler product on the cube-octahedron and CO-RD sweeps (maxima at mu ~ 1.631, 1.600), #61 chamber map | test his relation along our sweeps: does the flag number jump at the Hopscotch walls where the canonical form kinks (canonical-sweep study)? |
| OpenAI 2610.00950 (filed) | exact projection-body volumes, product counterexample | aim 2 polar side (zonoids = polars of the sweeps' shadows) | projection bodies of the sweep solids S(mu): is the extremum at the turn's fixed point sqrt3? |
| Hofscheier-Nill 2611.00775 (filed) | reflexive polytopes with doubly exponentially many vertices | aim 2 (polar duality, a.x = 1 facets); #43 OG margin (lattice-free counts) | reflexivity test on our lattice solids (Kelvin TO, RD, the permutohedra of #105) and their polars |
| Tang, Lusztig 2611.01161 (correction ready: Partially) | Fourier matrices for H3, H4 families | Silent Queens (#107), 600-cell / 120-cell, Golden Ladder | the H4 family data (13 families, 104 unipotents) as a check list for our Queens' harmonic silences by degree |
| Tang, Grassmannian cluster variables 2611.00582 (filed) | positroid / cluster combinatorics | aim 2 (amplituhedron uses positroid cells) | entry point for chunk 4 (associahedron -> amplitudes) |
| Kilpatrick 2610.00204 (complete, ready to file) | smooth words, Kolakoski, FIFO shuffle certificates | aim 1 (Sturmian / Fibonacci c/h words, #66 Hexagonality Law); tangram parity = "n and S(n) even" | apply the parity/shuffle-square test to c/h stacking words: which stackings are 'shuffle squares' of two identical layer sequences? |
| Babanskyy 2610.01847 (complete, ready to file) | linear extensions tiling S_n = poset cones tiling the braid fan; order polytopes tile the cube | Permutohedron Paradigm (#104, #105 count and sweep, Swap Rule), aim 1 (a lattice-like tiling of a fan) | poset-cone tilings of the permutohedron's normal fan as a new 'cells of a fan' reading of #105; P038 (48 order polytopes in the 6-cube) as a figure |
| Cremer 2610.01289 (filed) | exact max-clique on large colourings | tools: our own max-clique code (scripts/maxclique.c) | reuse for contact-graph cliques in packing questions (Admiral Cap network, kissing configurations) |
| Blanco Gomez 2610.01408, centered Latin squares 2609.03275 (filed) | number theory / determinants | far from the aims | standing only |
| NOT reproduced, friends to read: Akhmedova-Lam-Yost-Wolff 2611.00413 | amplituhedron tiling with fewer tiles than the magic number (injective degree-2 cell) | aim 2 chunk 4-5 (tilings of positive geometries; sum of degrees conjecture) | no code; skipped as not quick (needs Stanley coefficients + numerical tiling for k = 3, n = 11); read for chunk 4 |
| NOT reproduced: OpenAI 2610.00861 | a translational tile in Z^3 with no fully periodic tiling (periodic tiling conjecture fails in 3D) | aim 3 directly (one piece, 3D, no periodic tiling) | proof only (80 KB, no code); cite in every aim-3 text; its word-rule / stacking sections are a second route for the c/h stacking carrier |
| NOT reproduced: Lian-Xue 2609.02669 | lattice covering density of the regular octahedron = 9/8 | octahedra in Vacuus (#87), octet | cite where octahedron coverings appear; proof paper |
