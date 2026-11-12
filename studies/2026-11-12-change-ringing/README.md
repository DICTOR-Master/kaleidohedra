# Change ringing on the permutohedron (12 Nov 2026) - Permutohedron Paradigm, Chapter 13

**Conclusion.** A row of n bells is a corner of the permutohedron (x_b = place of bell b); a change that swaps k disjoint pairs of
neighbouring bells joins opposite corners of a k-cube face (k = 1: an edge; k = 2: a square diagonal); no change crosses a hexagon.
The change graph R_n (all changes) has F(n+1) - 1 = 1, 2, 4, 7, 12, 20, ... strokes at every row. Extents = Hamiltonian cycles of R_n.
On four bells: the truncated octahedron itself has exactly 44 Hamiltonian cycles (4 classes under its 48 symmetries); R_4 (edges plus the
12 square diagonals) has exactly 5396 (162 classes); the automorphism group of R_4 is the 48 symmetries. 139 Minimus methods of the CCCBR
collection have a plain course that is an extent; they fill 43 of the 162 classes, including all 15 periodic classes and all 4 edge-only
classes. Highest symmetry of an extent of four: order 12 (D3d, central inversion, rounds opposite backrounds), exactly three classes:
Double Bob, Double Court Place and Double Canterbury Place Minimus; the last is also the class of the plain changes (SJT order).
Plain Bob Minimus uses all 12 square diagonals of R_4 (symmetry C3v, order 6). Rounds to backrounds: C(n,2) edge steps with
2, 16, 768, 292864 shortest paths (n = 3..6, Stanley 1984 reproduced); with ringing changes exactly n steps (proof in the chapter) and,
for n = 3..6, exactly two shortest ways: the two halves of the plain hunt. Doubles with standard calls: Plain Bob 12 extent callings
(fewest calls 3, bobs-only exists), Grandsire 10 (all need bobs and singles; fewest 6; Wenham's PBPBPS x2 among them), Stedman 10
(fewest 2 singles). Plain Bob Minor: no extent with bobs only (exhaustive over lead-end calls), one with bobs and singles found.

**Scripts** (`scripts/`): `extract_cccbr.py` (CCCBR XML, collection of 10 Nov 2026, downloaded 12 Nov 2026 from
https://methods.cccbr.org.uk/xml/CCCBR_methods.xml.zip -> `data/cccbr-methods-stage3-6.tsv`; the zip itself is not kept),
`hamcount.c` (Hamiltonian cycle counter, C), `ring.py` (all checks; log `data/ring.log`, data `data/ring.json`),
`figs.py` (figures, `figures/*.svg`). Plans: `scripts/ring-pilot.plan`, `scripts/ring.plan`.
Run: `gcc -O2 -o scripts/hamcount scripts/hamcount.c && python3 scripts/ring.py . && python3 scripts/figs.py .` (Python 3, stdlib only).
Pilot `data/ring-pilot.log` (18.5 s): one negative control (Plain Bob Minimus with lead end 34) turned out to be a true extent and was
replaced by a definite false one (two crosses in a row); full run 21.4 s, RING ok, FINAL ok.

**Controls.** Positive: Hamiltonian cycles hexagon 1, K4 3, cube 6, dodecahedron 30; an independent Python counter agrees with the C
counter (44, 5396); Stanley's reduced-word counts 2, 16, 768, 292864; face counts of the permutohedra (P4: 36 edges, 8 hexagons,
6 squares; P5: 240, 60, 90; P6: 1800, 480, 1080); every one of 9057 parsed CCCBR methods (stages 3-6) gives the lead head the collection
lists; Plain Bob Minimus plain course 24 rows (CCCBR); Grandsire Doubles P B P B P S twice is an extent (Wenham). Negative: Petersen
graph 0 cycles; Plain Bob Minimus with lead end 14 (plain hunt) and with lead end x, and the Plain Bob Doubles plain course rung to 120
rows, all fail as extents. 210 collection methods (132 on 3 bells, 76 on 4, 1 on 5, 1 on 6) contain a change in which no pair swaps
(a row is repeated), so cannot be extents; they are left out of the census.

**Credits and sources.** Method data: Central Council of Church Bell Ringers, Methods Library. Calls: Plain Bob Doubles bob 145,
single 123 (ringing-theory list, Aug 2010); Grandsire Doubles bob 3.1, single 3.123 and the PBPBPS extent, Stedman Doubles single
(P. D. Wenham, Bell Ringing by Instalments 05, 2021). Sources checked are listed in the chapter (papers/paradigm-ch13).
Topic: DICTO 12 Nov 2026, "chapter in the permutohedron book, go ahead on node": the three Kyushindo principles (Change, Rhythm, Harmony,
as in #43) read through change ringing.

## Conjecture 13.1 proved (13 Nov 2026): the plain hunt is the only shortest way across, for every n >= 3

**Conclusion.** For every n >= 3 the two halves of the plain hunt are the only shortest ways from rounds to backrounds in R_n. Exact
breadth-first search confirms it for n = 7 (5040 rows, 20 changes per row) and n = 8 (40320 rows, 33 changes per row): distance n, exactly
two shortest ways, 1.7.1.7.1.7.1 / 7.1.7.1.7.1.7 and x.18.x.18.x.18.x.18 / 18.x.18.x.18.x.18.x. Status: SETTLED (proof below; computed n = 3..8).

**Proof.** Take a way of L changes from rounds to backrounds. Let r_b be the number of changes at which bell b makes a place (rests),
S the total number of swaps, and u the number of swaps that undo a crossing (swap a pair that is already in reverse order). Each change
fixes n - 2k places when it swaps k pairs, so 2S = nL - sum_b r_b. Every swap changes the number of inverted pairs by 1, and backrounds
has all C(n, 2) pairs inverted, so S = C(n, 2) + 2u. Together: **sum_b r_b + 4u = n(L - n + 1).**
(i) L >= n. If L <= n - 1 the right side is <= 0, so L = n - 1, nobody rests and u = 0. For odd n a change always fixes a place, a
contradiction. For even n every change is x, and two x in a row undo each other (u > 0), a contradiction since L = n - 1 >= 3.
(ii) L = n. Bell b moves n - r_b times by one place and travels |n + 1 - 2b|, so n - r_b has the parity of n + 1: r_b is odd, r_b >= 1.
Then sum_b r_b + 4u = n forces r_b = 1 for every bell and u = 0. With u = 0, two consecutive changes share no swapped pair (the same two
bells would swap back). Let F_t be the set of places made at change t; sum_t |F_t| = sum_b r_b = n and |F_t| has the parity of n.
- n odd: |F_t| >= 1 is odd, so every change makes exactly one place p_t (p_t odd). If p_t < p_{t+1}, both changes swap the pairs left of
  p_t and the pairs right of p_{t+1}; since they share no pair, p_t = 1 and p_{t+1} = n (and the mirror case). So the places alternate
  1, n, 1, ... or n, 1, n, ...
- n even: |F_t| is even; two x cannot be consecutive (shared pairs), so at most n/2 changes are x and the others have |F_t| >= 2; the sum n
  forces exactly n/2 x changes, alternating, and |F_t| = 2 for the others. A change next to an x shares no pair with it, so it swaps only
  pairs 23, 45, ..., (n-2)(n-1) and makes places 1 and n: it is 1n. So the changes alternate x, 1n, ... or 1n, x, ...
These are the two halves of the plain hunt, and both reach backrounds in n changes. ∎

**Script** `scripts/geodesics.py` (stdlib, Python integers): R_n and P_n by breadth-first search with shortest-way counts, every shortest way
of R_n listed backwards from backrounds and compared with the two plain-hunt halves, the identity sum r_b + 4u = n checked on each way.
Log `data/geodesics.log` (main, n = 3..8, 1.2 s), `data/geodesics-pilot.log` (n = 3..6). Run on the compute node through the job gate, plans
`ring78-pilot`, `ring78`. **Controls:** n = 3..6 as in `ring.log` (distance n, 2 ways); changes per row F(n+1) - 1 = 20, 33; P_n shortest
edge paths C(n, 2) steps with Stanley's counts 2, 16, 768, 292864, 1100742656, 48608795688960 (n = 3..8; Stanley 1984, OEIS A005118);
negative: a 7-change way across on 5 bells with a detour obeys the identity with rests 11, u = 1, not the shortest-way pattern.
The first pilot's FINAL FAIL was a wrong check of mine (it required backrounds to be the only row at distance n); the rows at distance n
from rounds number 1, 3, 15, 61, 391, 2053 for n = 3..8, and no row is farther than n. Fixed and rerun: FINAL ok.
