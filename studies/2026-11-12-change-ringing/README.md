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
