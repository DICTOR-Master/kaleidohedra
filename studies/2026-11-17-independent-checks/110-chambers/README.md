# Independent check: #110 Walls of Silence, Theorem C (data a reader can audit)

Written from scratch on 17 November 2026, without opening any earlier scripts of #110 or its studies.
Definitions were taken from #110 §2 and Theorem B (c) only. Computation with Claude (Anthropic).

## What was checked

- A60: the 60 mirrors of the 600-cell P. Claim: χ(t) = (t−1)(t−11)(t−19)(t−29).
- A360 = W(P): the 60 mirrors and the 300 cross walls (normals along P's cell centres). Claim:
  χ(t) = (t−1)(t³ − 359t² + 45959t − 2099281) and 4,291,200 = 14400 × 298 chambers. 25 cross walls pass through one Coxeter chamber.
- A1560 = W(P1) ∪ … ∪ W(P10) for the 120-cell Q with its ten inscribed 600-cells. Claim: 593,236,800 = 14400 × 41,197
  chambers, with 174 walls passing through one Coxeter chamber.

## Method (exact in Z[φ]; no floating point anywhere)

1. `scripts/build_walls.py`: P0 has corners at radius 2: (±2,0,0,0), (±1,±1,±1,±1), and even permutations of (±φ,±1,±1/φ,0).
   Its cells are the 4-cliques of the 36° graph, giving 600. Q's corners are the 600 cell sums, and W(Q) = W(P0).
   P1 is grown from one corner of Q and one of its two sets of 12 neighbours at 36°. It is checked to be exactly
   closed under its own reflections. The ten Pi are its W-orbit, and every corner of Q lies in exactly 2 of them.
   Walls are stored as integer normals with an exact projective key (division by the first nonzero coordinate in Q(φ)).
   The simple roots are the positive roots whose reflection permutes the other positive roots.
2. `scripts/lattice.py` (Method A, the full intersection lattice):
   - rank 2: for every wall a, the other walls are grouped by the plane H_a ∩ H_b (exact key of the projection of n_b),
     which gives h_X for every pair; μ(X) = h_X − 1.
   - rank 3: the lines in a wall H are the intersections of pairs of planes in H, with direction cross3(n_H, n_A, n_B).
     For each line, S(L) is the set of walls with n·d = 0 exactly, and μ(L) = −1 + h − Σ_{X⊃L}(h_X − 1). Lines are
     counted wall by wall, Σ_H weight(H) · #(lines of a type in H) / h. Mode `all` uses every wall with weight 1.
     Mode `orbit` uses one wall per W-orbit, weighted by the orbit size; the two modes agree on A360. A completeness
     check holds for every line: each line in H arises from exactly C(k,2) plane pairs, where k is the number of planes
     in H through it.
   - μ(0) from χ(1) = 0, and chambers = |χ(−1)| (Zaslavsky).
3. `scripts/chamber.py` (Method B, independent of the global lattice and of the group action). Only the walls meeting
   the open Coxeter chamber C are used. Zaslavsky's count for an open convex set is
   #pieces of C = Σ over flats X meeting C of |μ(X)|. Planes and lines are built from those walls alone, and meeting C
   is tested exactly. Since all 60 mirrors are walls, #chambers = 14400 × #pieces of C.
4. `scripts/orbits.py`: W(H4)-orbits of planes (as sets of walls) and of lines (exact directions), by union-find
   over the four simple reflections.

## Commands (on the compute host, in this folder; 24 cores)

    python scripts/build_walls.py data/walls.npz
    python scripts/lattice.py data/walls.npz A60   orbit data/lattice_A60_orbit.json
    python scripts/lattice.py data/walls.npz A360  orbit data/lattice_A360_orbit.json
    python scripts/lattice.py data/walls.npz A360  all   data/lattice_A360_all.json      # 45 s
    python scripts/lattice.py data/walls.npz A1560 orbit data/lattice_A1560_orbit.json   # 30 s
    python scripts/chamber.py data/walls.npz A360  data/chamber_A360.json
    python scripts/chamber.py data/walls.npz A1560 data/chamber_A1560.json               # 2 min
    python scripts/orbits.py  data/walls.npz A360  data/orbits_A360.json lines           # 70 s
    python scripts/orbits.py  data/walls.npz A1560 data/orbits_A1560.json                # planes only

Every log in `logs/` ends `FINAL ok`.

## Results

| claim | result | verdict |
|---|---|---|
| Theorem B (c): 1560 walls = 60 (Q mirrors, cross wall of all ten Pi) + 300 (Q corner axes, mirror of 2 Pi) + 1200 (cross wall of 2 Pi) | exactly these classes (`logs/build_walls.log`) | MATCH |
| 60 mirrors: χ = (t−1)(t−11)(t−19)(t−29) | t⁴ − 60t³ + 1138t² − 7140t + 6061, which is this product; 14400 chambers | MATCH |
| 360 walls: χ = (t−1)(t³ − 359t² + 45959t − 2099281) | χ = t⁴ − 360t³ + 46318t² − 2145240t + 2099281; quotient by (t−1) as claimed | MATCH |
| 4,291,200 = 14400 × 298 | \|χ(−1)\| = 4,291,200 (Method A, both modes); Method B: 1 + 25 + 138 + 134 = 298 | MATCH |
| 25 cross walls through one chamber | 25 | MATCH |
| 593,236,800 = 14400 × 41,197 | χ = t⁴ − 1560t³ + 1026238t² − 296616840t + 295592161, \|χ(−1)\| = 593,236,800 (Method A); Method B: 1 + 174 + 5981 + 35041 = 41,197 | MATCH |
| 174 walls through one chamber | 174 | MATCH |

χ_1560(t) = (t − 1)(t³ − 1559t² + 1024679t − 295592161).

### Appendix table, 360 walls (μ = Möbius value; coefficient = Σ μ over the rank)

| rank | walls through the flat | flats | W-orbits (orbit sizes) | μ | Σ μ |
|---|---|---|---|---|---|
| 0 | 0 (whole space) | 1 | 1 | 1 | **1** |
| 1 | 1 | 360 | 2 (60, 300) | −1 | **−360** |
| 2 | 2 | 27000 | 8 (1×1800, 7×3600) | 1 | 27000 |
| 2 | 3 | 6600 | 4 (1200, 3×1800) | 2 | 13200 |
| 2 | 4 | 450 | 1 | 3 | 1350 |
| 2 | 5 | 792 | 2 (72, 720) | 4 | 3168 |
| 2 | 9 | 200 | 1 | 8 | 1600 |
| 2 | total | 35042 | 16 | | **46318** |
| 3 | 3 | 478800 | 68 | −1 | −478800 |
| 3 | 4 | 162000 | 31 | −3 (28800), −2 (133200) | −352800 |
| 3 | 5 | 72000 | 19 | −5 (7200), −4 (64800) | −295200 |
| 3 | 6 | 48600 | 11 | −8 (7200), −6 (12600), −4 (28800) | −248400 |
| 3 | 7 | 18000 | 3 | −10 (3600), −8 (14400) | −151200 |
| 3 | 8 | 7200 | 4 | −14 (5400), −12 (1800) | −97200 |
| 3 | 10 | 9840 | 5 | −20 (8640), −8 (1200) | −182400 |
| 3 | 12 | 4200 | 3 | −32 (1800), −24 (2400) | −115200 |
| 3 | 15 | 1200 | 1 | −48 | −57600 |
| 3 | 16 | 960 | 2 | −64 (360), −62 (600) | −60240 |
| 3 | 33 | 300 | 1 | −255 | −76500 |
| 3 | 45 | 60 | 1 | −495 | −29700 |
| 3 | total | 803160 | 149 | | **−2145240** |
| 4 | 360 (the centre) | 1 | 1 | 2099281 | **2099281** |

Regions = 1 + 360 + 46318 + 2145240 + 2099281 = 4,291,200. Inside one Coxeter chamber (Method B) the flats that meet it
are 25 walls, 124 planes (116 with 2 walls, 5 with 3, 3 with 5; Σμ = 138) and 86 lines (Σ|μ| = 134), giving
1 + 25 + 138 + 134 = 298. The full split of lines by μ and by the planes through them (23 types) is in
`data/lattice_A360_orbit.json`, and the orbit sizes are in `data/orbits_A360.json`.

### 1560 walls, summary

| rank | flats | Σ μ |
|---|---|---|
| 0 | 1 | 1 |
| 1 | 1560 (orbits 1200, 300, 60) | −1560 |
| 2 | 913922 in 183 orbits: h = 2: 837000; 3: 60600; 4: 4050; 5: 10872; 9: 1200; 15: 200 | 1026238 |
| 3 | 171959880 lines, 97 types (h from 3 to 105) | −296616840 |
| 4 | 1 | 295592161 |

Inside one Coxeter chamber: 174 walls (25 of Q's corner-axis walls and 149 of the 1200), 5610 planes meeting it
(Σμ = 5981) and 23223 lines meeting it (Σ|μ| = 35041), so 41,197 pieces. Full data: `data/lattice_A1560_orbit.json`,
`data/chamber_A1560.json`, `data/orbits_A1560.json`.

### Comparison with earlier outputs (made after these results were logged)

The earlier study's χ for 60 and 360 walls (queens-chambers `data/chambers.log`) is identical. The red-queen-cats
`data/chambers.json` has 174 walls, 5610 planes and 23223 points inside one chamber, and 41,197 pieces, the same as
Method B here. No earlier global χ for 1560 walls was found. The polynomial above is new and agrees with 14400 × 41,197.

## Not covered

- The 15 combinatorial types of the 298 pieces, the "no two congruent" claim and the pyramid description.
- Line orbits for the 1560 arrangement (172 million lines). Only plane orbits were computed for it.
- Zaslavsky's theorem for an open convex set (Method B) is used as stated in the literature. It is not reproved here.
