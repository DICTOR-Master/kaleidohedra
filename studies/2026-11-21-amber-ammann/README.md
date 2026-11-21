# Amber-Ammann: icosahedral cores set in the 3D Penrose tiling (21 Nov 2026)

Study 2 of DICTO's scutoid thread. The idea is DICTO's: icosahedra "set in a never-repeating setting". Question: can icosahedral cores be
set in a non-periodic frame, the 3D Penrose tiling by the two golden rhombohedra, with the resin cut into scutoids by DICTO's combined
method, so that the cores sit in a never-repeating pattern? Method (combined method, Amber Cell): DICTO's. Names: Fullerene Star,
Rollerball, *-Amber Cell are DICTO's; "S0", "cen", "cproj" are working labels.

## Result in six lines

1. Frame: one core at the centre of every golden rhombohedron (prolate P, oblate O), all cores in one orientation, one size. Each
   rhombohedron's 3-fold axis is a 3-fold axis of the core, so every cell keeps D3d (order 12). The 10 P orientations are rotations of
   one another, and so are the 10 O orientations. Up to rotation there are exactly two cells.
2. Patch: 402 rhombohedra (278 P, 124 O), exact in Q(√5) by cut-and-project from Z^6. Checks: face to face, 360° round every interior
   edge, tile volume = volume inside the boundary (exact 0), all 20 orientations present.
3. Valid divisions in every cell of the patch (all 20 orientations, every one checked: closed embedded pieces, walls cancelling in pairs,
   exact volume, sampling): Rollerball at the common tightest scale S0 with centroid seeds: **72/72 pieces scutoids in both cells, 30 Y
   vertices per cell, 16 kinds over the patch (8 P + 8 O)**. Fullerene Star at S0 with projected seeds: 66/80 (P) and 72/80 (O) scutoids,
   18 kinds. Icosidodecahedron (6/5 S0): 20/32 and 18/32, 10 kinds. Icosahedron (cproj): 18/20 each, 6 kinds. Dodecahedron: 0 scutoids, 4 kinds.
4. No piece kind occurs in both cell types (in every valid setting). The kinds are finitely many and fixed by the cell type; their
   orientation is fixed by the rhombohedron's orientation.
5. The scutoid layer is never-repeating (proof below): the cells can be read back from the pieces, and P : O = φ (exact, from the window).
   A periodic pattern would need rational ratios.
6. Across cell walls: where two cells of the same type meet (380 of 998 shared faces) the two outer patterns agree exactly, so the
   pieces meet top to top. Where P meets O (618 faces) they never agree: the pieces still fill both cells, but their tops do not line up
   across those faces. Same in all 8 settings tested.

Verdict: yes. The cores can be set in the Ammann rhombohedra, every rhombohedron cut into true scutoids (Rollerball: all of them). The
scutoid layer carries the tiling's never-repeating order exactly: the piece kinds follow the arrangement of the rhombohedra one to one.

## Setting

- Star: e_i = (0,1,φ), (0,−1,φ), (1,φ,0), (−1,φ,0), (φ,0,1), (−φ,0,1) (one icosahedron vertex per 5-fold axis; the axes of the
  amber-cell sweep's solids). Perpendicular star e_i' = Galois conjugate (√5 → −√5). Checked exactly: Σ e_i e_i'^T = 0, so the two
  spaces are orthogonal in R^6. Tiles: n + C_A for a triple A is a tile iff γ lies in the open parallelepiped
  π'(n + 1_A/2) + Σ_{b∉A} [−½,½] e_b' (dual of the cubic complex). γ = (1234/10007, −567/10009, 891/10037), no boundary tie (exact).
  Patch = tiles with centre within 4 edges of the origin.
- With these e_i (|e|² = (5+√5)/2) the 10 triples of volume 3+√5 are prolate, the 10 of volume 1+√5 oblate (ratio φ, exact). Window frequency P : O = Σ|det e'_{A^c}| ratio = φ exactly (irrational).
  In the patch 278 : 124 (finite patch; at radius 6 edges 842 : 574).
- Cell = rhombohedron centred on the core's centre. Core: the amber-cell sweep's solid, its 5-fold axes on the e_i. The icosahedron
  and Fullerene Star are built that way; dodecahedron, icosidodecahedron and Rollerball are reflected in y = z first (the sweep fixes only
  the T_h axes; invariance under this I_h checked exactly).
- Scales (one core size in every cell): s0 = smallest mould scale with the core inside, exact, the same in all 10 orientations of a type.
  In every case s0(O) = φ·s0(P): the oblate cell binds. S0 = s0(O) (the O cell is tight, the P cell has room); also 6/5 S0, and
  "own" = each cell at its own s0 (two core sizes). Mould = rhombohedron on e_a/3, e_b/3, e_c/3 scaled by s; core unit size.

| core | s0 (P) | s0 (O) = S0 |
|---|---|---|
| icosahedron (edge 1) | 3 | (3+3√5)/2 |
| dodecahedron (edge 1) | (3+3√5)/2 | (9+3√5)/2 |
| icosidodecahedron (edge 1) | 6 | 3+3√5 |
| Fullerene Star | (15+3√5)/2 | (15+9√5)/2 |
| Rollerball | 6+3√5 | (21+9√5)/2 |

- Combined method: the amber-cell sweep's amber.py, unchanged except for the mould, the symmetry group used for orbits (D3d, computed
  exactly as the stabiliser of the mould in I_h), the sampling box, and keeping kind vertices (scripts/ammann_cell.py header lists the
  changes). Seeds: cen = face centroids; cproj = centroids projected from the core's centre onto the mould. Y rule, fins, triangulation
  and all checks as in the sweep.
- Every one of the 20 orientations was run directly (not transported by rotation): 5 cores × 20 orientations × 3 scales × 2 seeds = 600
  runs. Rotation check: within each type, all 10 orientations give congruent kinds with the same counts (passes everywhere).
- Kinds across the patch = congruence classes (isometry, proper or improper, plus equal volume) over both cell types.

## Table (all 20 orientations agree in every row; patch = 278 P + 124 O cells)

| core | scale | seeds | valid P / O | kinds P + O (shared) | scutoids per cell P, O | Y per cell P, O | patch: pieces, scutoids, Y |
|---|---|---|---|---|---|---|---|
| Rollerball | S0 | cen | 10/10, 10/10 | 8 + 8 (0) | 72/72, 72/72 | 30, 30 | 28944, 28944, 12060 |
| Rollerball | 6/5 S0 | cen, cproj | 10/10, 10/10 | 8 + 8 (0) | 72/72, 72/72 | 30, 30 | 28944, 28944, 12060 |
| Rollerball | own | cen | 10/10, 10/10 | 8 + 8 (0) | 72/72, 72/72 | 30, 30 | 28944, 28944, 12060 |
| Rollerball | S0 | cproj | 10/10, 0/10 (O self-intersecting) | | | | |
| Fullerene Star | S0, 6/5 S0 | cproj | 10/10, 10/10 | 9 + 9 (0) | 66/80, 72/80 | 48, 42 | 32160, 27276, 18552 |
| Fullerene Star | S0, 6/5 S0, own | cen | 0/10, 10/10 (P: empty outer cells) | | | | |
| icosidodecahedron | 6/5 S0 | cen, cproj | 10/10, 10/10 | 5 + 5 (0) | 20/32, 18/32 | 30, 30 | 12864, 7792, 12060 |
| icosidodecahedron | S0 | cen, cproj | 10/10, 0/10 (O: Y direction meets the mould at the core) | | | | |
| icosahedron | S0, 6/5 S0 | cproj | 10/10, 10/10 | 3 + 3 (0) | 18/20, 18/20 | 12, 12 | 8040, 7236, 4824 |
| icosahedron | S0, 6/5 S0, own | cen | 10/10, 10/10 | 3 + 3 (0) | 0/20, 0/20 | 0, 0 | 8040, 0, 0 |
| dodecahedron | S0, 6/5 S0, own | cen | 10/10, 10/10 | 2 + 2 (0) | 0/12, 0/12 | 0, 0 | 4824, 0, 0 |
| dodecahedron | 6/5 S0 | cproj | 10/10, 10/10 | 2 + 2 (0) | 0/12, 0/12 | 0, 0 | 4824, 0, 0 |

Other failures (logs/summary.txt has every row): icosahedron own cproj (P self-intersecting); dodecahedron S0/own cproj (O: collinear
wall); Fullerene Star own cproj (P self-intersecting); Rollerball own cproj (both self-intersecting); icosidodecahedron own (both: Y
direction meets the mould at the core). As in the sweep, these are failures of the one-Y-per-cluster cut rule, not proofs that no
division exists.

- Rollerball, S0, centroid seeds: per prolate cell 6+6 decagon pieces (2 kinds) and 60 triangle pieces (6 kinds); per oblate cell the
  same counts (6+6 decagon, 60 triangle pieces), 8 other kinds. Every piece is a true scutoid. Kind list with facets and volumes: logs/summary.txt.
- 157.7612° (λ*) was tested on every dihedral of every piece of the 440 valid runs: it occurs in none.

## Never-repeating order in the scutoid layer

1. Each piece touches exactly one core (its bottom is a face of that core), so the cell of a core = the union of the pieces touching it.
   The rhombohedra can be read back from the pieces. So any translation that maps the piece layer onto itself maps the tiling onto itself.
2. The tiling has no period: a periodic tiling has rational frequencies, but P : O = φ (exact, window volumes, tiling.py).
3. So the scutoid layer has no period. Directly, too: no kind occurs in both cell types, so a kind k occurs with frequency
   proportional to φ·mP(k) + mO(k). For a P-only kind and an O-only kind the ratio is irrational ("irrational kind frequencies True" in every
   valid row).
4. The piece arrangement is fixed by the rhombohedra: kind by cell type, orientation by the cell's orientation (10 rotations per type),
   position by the cell centre. The order of the pieces is the tiling's order, one to one.

## Across cell walls (scripts/facematch.py, exact)

For each of the 998 shared faces of the patch, the outer pattern of each neighbour on that face (Voronoi cells of its seeds cut by the
face) was computed exactly and compared after translation:

| setting | P–P | O–O | P–O |
|---|---|---|---|
| icosahedron S0 cen, S0 cproj; dodecahedron S0 cen; icosidodecahedron 6/5 S0 cen; Fullerene Star S0 and 6/5 S0 cproj; Rollerball S0 and 6/5 S0 cen | 319/319 agree | 61/61 agree | 0/618 agree |

So inside runs of one cell type, the pieces meet top to top across walls. Every prolate–oblate wall is a seam where the two patterns
differ. The division is valid all the same, because each cell is divided on its own.

## Sources checked

The private reference library: no entry on the Ammann rhombohedra, Kramer & Neri or Socolar & Steinhardt.
None was opened for this study. The construction here is the standard cut-and-project / dualisation, written and checked from scratch.
The tiling is attributed to Ammann (1976) and Kramer & Neri (1984) by name only: add full citations after opening them. The app's
quasicrystal world (k-mix src/app/world-quasicrystal.js) was looked at for conventions only; no code was taken from it.

## Files

- scripts/tiling.py: exact patch and checks → data/patch.json, logs/tiling.log (radius 4 edges).
- scripts/aligned.py: the sweep's solids with 5-fold axes on the star (reflection y = z where needed, checked).
- scripts/s0.py: exact s0 per type, common S0 → data/s0.txt.
- scripts/ammann_cell.py: the combined method in a rhombohedron mould (the sweep's amber.py with the listed changes).
- scripts/run_all.sh: the 600 runs (job amber-ammann on the compute host, logs/job.log ends FINAL ok); logs/runs/*.log; data/ammann_*.json.
- scripts/summary.py: re-checks and the table → logs/summary.txt (ends SUMMARY OK).
- scripts/facematch.py: wall matching → logs/facematch.log.

LEADS
1. Prolate–oblate seams: seeds chosen so that the two patterns agree on P–O faces (for example seeds placed on the shared face by a
   rule common to both cells) would make the whole scutoid layer meet top to top. That is a different seed rule, not tried here.
2. Vertex frame: cores at the tiling's vertices with their Voronoi cells as moulds (more cell shapes, all icosahedral directions). Not run.
3. Fewer kinds: the Rollerball gives 8 kinds per cell here against 4 in the bcc mould; D3d is smaller than T_h, so orbits split.
4. Fullerene Star with centroid seeds fails in the prolate cell (empty outer cells: the core is small there at the common scale).
   The cproj rule works there.
