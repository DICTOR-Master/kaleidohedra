# RT centre pyramids: exact SAT search for periodic tilings, 21 Nov 2026

## Question
Do the centre pyramids of the rhombic triacontahedron (RT) fill space? This is the last real empty cell of the Concordance grid (ledger [19], UNDECIDED).
The pyramid has its apex at the RT centre and a golden rhombus face as base. Dihedral angles: 72° at the base edges, 72° at the lateral edges
to the 5-fold corners, 120° at the lateral edges to the 3-fold corners. The Dehn invariant is zero (the RT dihedral is 4π/5), so Dehn does not
forbid a tiling (Debrunner 1980: zero Dehn invariant is necessary for a tiling).
The edge-to-edge depth-first search of 4 Nov (studies/2026-11-04-rt-pyramids) reached 31-piece patches round 11 centres; the 21 Nov reruns
to 60/100/150 pieces stayed undecided after 3 h 20 min. This study sets up the exact SAT method (one Boolean variable per placement on a
torus, in the manner of Kaplan's monotile searches) and runs it.

## Two facts that fix the encoding
1. **Angles.** 360° = 5 × 72° = 3 × 120°, and 72a + 120b = 360 has no solution with a, b > 0; 180° is not a sum of 72s and 120s.
   So round a generic point of any edge sit either five 72° wedges or three 120° wedges, and no edge lies inside a face of another piece.
2. **Orientations.** Turning a piece about one of its edges keeps it among the 30 pyramids of an RT with the same axes: RT edges are
   parallel to the 5-fold axes, the lateral edges lie on 5-fold and 3-fold axes, and the wedge planes are mirror planes of the icosahedral
   group. Only the *swapped-end* placement (the neighbour holds the shared edge the other way round) leaves this set: it turns the RT frame
   by 36° about a 5-fold axis or by 60° about a 3-fold axis. Check (scripts/check_swapped_end.py, logs/check_swapped_end.log): the moves of
   the 4 Nov search give 22 → 30 orientations without swapped ends (closed at the 30 of one RT), and 52 → 780 (→ 8222 after 3 rounds) with them.
   The rotations generated are dense, so an icosahedral piece has infinitely many reachable orientations; a periodic tiling uses finitely many.

Hence the search space must be chosen. We call **class O** the tilings in which every piece is a translate of one of the 30 pyramids of a
single fixed RT (all pieces parallel to the pyramids of one RT).

## Result 1 (exact, all tilings, periodic or not): no edge-to-edge tiling in class O
scripts/classO_e2e.py: depth-first search over exact positions (coordinates in Z[φ], φ = golden ratio). Edge to edge means: two pieces that
meet along a segment of an edge share that whole edge with the same end points. By fact 1 every other sector at an edge (4 of 72° or 2 of
120°) must then be filled by a piece with the same segment as an edge of the same kind (base and 5-fold lateral edges have the same angle
but different lengths, 3.804 and 6.155 in the units used, so they cannot share a segment). Candidates: every class-O piece (all 30 templates,
both directions of the edge) with that edge in that sector; exact overlap test (separating axes, Z[φ] arithmetic).
- RT: **every branch dies**: 428 search nodes, largest patch 25 pieces. So no tiling of space by RT centre pyramids all parallel to
  the pyramids of one RT and meeting edge to edge exists.
- Control: cube pyramids (C6) in their class: search alive to 60 pieces.
- Independent check: the 4 Nov floating-point code restricted to class O (scripts/explore_classO_dfs.py) also dies (160 nodes, largest patch 21).
So the 31-piece patches of 4 Nov live only because they use swapped-end pieces from other RT frames.

## Result 2: SAT on tori (class O, edge to edge NOT assumed)
scripts/tsat.py. Search space S(Λ, R):
- pieces: the 30 class-O pyramids, translations only;
- apexes in one coset of the module M spanned by the vertex vectors. In coordinates n ∈ Z^6 over the six 5-fold vectors
  e = (0, ±1, φ), (±1, φ, 0), (φ, 0, ±1) (cyclic), M = {n : all n_i of one parity}; the RT used has corners Σ ±e_i (5-fold) etc.
  Every tiling in which any two pieces are joined by a chain of pieces sharing a corner has all apexes in one coset of M;
- period lattice Λ spanned by three vectors of M; a placement is (template, class of the apex in M/Λ); one apex at the origin;
- M is dense in space (rank 6), so the classes are bounded by their height h = distance in R^6 from n to the real span of Λ
  (constant on a class): only classes with h² ≤ R2, reached from the origin by single vertex-vector steps without leaving h² ≤ R2.
Clauses (each a necessary condition of a tiling in S(Λ, R), so UNSAT proves there is none):
every sample point lies in at least one chosen closed piece; no sample point lies in the interiors of two chosen pieces; exactly
N = vol(Λ)/vol(pyramid) pieces (exact; N must be a whole number); some piece has its apex at the origin. Sample points start as the
centroids of all placements; any model is checked exactly for overlaps on the torus, and each overlap adds an interior point of it as a new
sample point (counterexample loop). N pieces with disjoint interiors and total volume vol(Λ) tile the torus, so a model that passes is a
periodic tiling. Geometry decisions are exact in Z[φ] (floating point only skips cases decided by more than 1e-9). Solver: CaDiCaL 1.9.5 (pysat).

**What an UNSAT covers:** there is no tiling of space by class-O RT pyramids that is invariant under the translations Λ, has all apexes in one
coset of M, and has every apex class (mod Λ, origin at one apex) of height h² ≤ R2. A tiling with a larger period lattice Λ' ⊃ Λ is
Λ-periodic too and is covered when its classes satisfy the height bound.

Volume arithmetic: vol(RT) = 160 φ³ in these units (6 vol(pyramid) = 32 + 64φ); a lattice in M has N = vol(Λ)/vol(pyramid) whole only for
N = 3m. Lattices tried: the cube lattice 4φZ³ (N = 12), and all 34 lattices spanned by three vectors of M with 6D norm² ≤ 8 and N ≤ 30, up to
change of basis and the 120 icosahedral symmetries (scripts/rt_lattices.py, data/rt_lattices_n8_N30.json: 20 with N = 3, 12 with N = 6,
1 with N = 9, 1 with N = 12).

### Controls (all must pass)
Watched job rt-sat (logs/rt-sat.log, ends FINAL ok; 125 instances, 21 min for all but the two capped frame searches):
| control | lattice | N | expected | result |
|---|---|---|---|---|
| cube pyramids C6 | 2Z³ / 4Z³ | 6 / 48 | SAT | SAT, SAT |
| RD pyramids | fcc / 4Z³ | 12 / 48 | SAT | SAT, SAT |
| regular tetrahedron (with its point reflection) | fcc / 2Z³ / 4Z³ | 6 / 3 / 24 | UNSAT | UNSAT ×3 |
| acute golden rhombohedron, 10 icosahedral orientations (tests the 6D module and the height bound) | twice its own lattice, R2 = 0 and 8 | 8 | SAT | SAT, SAT |
| C6 edge-to-edge search (Result 1 code) | – | – | alive | alive to 60 |
Every SAT tiling was checked exactly (pairwise disjoint interiors on the torus, N·vol = vol(Λ)) and by 3000 random points (each in exactly one closed piece).

### RT results
All 112 RT instances: **UNSAT** (none undecided).
| lattice | N | height bounds R2 | placements (largest) | result |
|---|---|---|---|---|
| cube lattice 4φZ³ | 12 | 2, 4, 6, 8, 10, 12, 14, 16, 18, 20 | 8820 (R2 = 20, 1192 s) | UNSAT ×10 |
| 20 lattices | 3 | 4, 8, 12 | 1782 | UNSAT ×60 (in 3 of these lattices no single pyramid fits the torus without meeting its own translates) |
| 12 lattices | 6 | 4, 8, 12 | 4212 | UNSAT ×36 |
| 1 lattice | 9 | 4, 8, 12 | 2970 | UNSAT ×3 |
| 1 lattice | 12 | 4, 8, 12 | 4860 | UNSAT ×3 |
Per-instance data: data/RT-*.json, logs/RT-*.log; table: data/summary.json.

Floating exploration (not a proof): the 4 Nov edge-to-edge search allowed pieces from 17 RT frames (class O plus the 16 frames one
swapped-end move away), and from the frames two moves away: both still running at the 1 h cap (no verdict).

## Verdict
Not decided for the RT pyramid in general. Decided exactly:
1. No tiling of space at all (periodic or not) by RT centre pyramids all parallel to the pyramids of one RT and meeting edge to edge.
2. No periodic tiling by such pieces (edge to edge not assumed) for any of the 35 period lattices tried, with apex classes of height up to the
   bounds listed (R2 ≤ 20 on 4φZ³, R2 ≤ 12 on the 34 short lattices).
So any tiling by RT centre pyramids must use pieces from more than one RT frame (swapped-end neighbours, turned 36° about a 5-fold or 60° about a
3-fold axis) or, within one frame, break edge-to-edge contact and avoid every lattice and height tested here. The 31-piece patches of 4 Nov are of
the first kind.

## 1. Several frames on the torus: add the 16 frames one swapped-end move away (rotation entries in Q(√5), coordinates with denominator 4) to
   tsat.py; same clauses. This is the decided next method (plan rt-sat, if_fail_or_cap).
2. Exact frame-restricted edge-to-edge search: port classO_e2e.py to the 17 frames (exact Q(√5)/4 arithmetic) and run without a node cap
  ; if every branch dies, the next frame layer.
3. Class O without edge to edge: the line argument (wedges round a 3-fold line all of one type, so each sector is stacked end to end along
   the line) may give a proof for all class-O tilings, not only periodic ones.
4. Larger lattice lists (6D norm² ≤ 12, N ≤ 24) and higher height bounds, if lead 1 does not settle it.
1. Several frames on the torus: add the 16 frames one swapped-end move away (rotation entries in Q(√5), coordinates with denominator 4) to
   tsat.py; same clauses. This is the decided next method (plan rt-sat, if_fail_or_cap).
2. Exact frame-restricted edge-to-edge search: port classO_e2e.py to the 17 frames (exact Q(√5)/4 arithmetic) and run without a node cap
  ; if every branch dies, the next frame layer.
3. Class O without edge to edge: the line argument (wedges round a 3-fold line all of one type, so each sector is stacked end to end along
   the line) may give a proof for all class-O tilings, not only periodic ones.
4. Larger lattice lists (6D norm² ≤ 12, N ≤ 24) and higher height bounds, if lead 1 does not settle it.

## Files
- scripts/geom.py (exact Z[φ] geometry, templates), tsat.py (torus SAT), rt_lattices.py, classO_e2e.py (exact edge-to-edge check),
  run_all.py (watched job rt-sat), check_swapped_end.py, explore_orient.py, explore_classO_dfs.py, explore_frames_dfs.py (floating explorations
  built on the 4 Nov code), pilot_explore.py
- data/: one JSON per instance (verdict, sizes, and the tiling if SAT), summary.json, rt_lattices_n8_N30.json, classO-e2e-*.json
- logs/: one log per instance; rt-sat.log (the watched job, ends FINAL ok)
