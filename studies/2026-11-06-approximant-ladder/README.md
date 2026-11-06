
## Rung 1 gaps filled (DICTO "fill the gaps", "can we grow golden skin inside"; scripts/rung1_gravel.py on dicto-big-brother, voxels N=48)
- Golden skin (golden rhombohedra along the icosahedra's six 5-fold axes, phi-steps 0.16, 0.099, 0.061): 82.2% of the gap filled ->
  96.8% of space (finer steps fall below the voxel size, so this is a lower bound).
- Platonic gravel (T, O, C, I, D at 0.5/phi^k): 54.1% of the gap (only tetrahedra fitted) -> 91.8% of space.
  The golden skin wins clearly: the gap round icosahedra is five-fold, like the rhombohedra.

## The ladder by cut-and-project (scripts/cutproject.py, tiles.py -> data-tiles.txt)
Physical directions golden (exact icosahedral angles), hidden directions rational (1/1 -> 1, 2/1 -> 1/2, 3/2 -> 2/3): exact periods.
| rung | cell | points / cell | full icosahedral stars / cell | rhombohedra / cell (prolate + oblate) |
|---|---|---|---|---|
| 1/1 | body-centred cubic, cube side 2 phi^2 (primitive volume 71.7771) | 16 | 1 | 10 + 6 |
| 2/1 | simple cubic, side 2 phi^3 = 8.4721 | 136 | 4 | 84 + 52 (ratio 1.615 -> phi) |
| 3/2 | simple cubic, side 2 phi^4 = 13.7082 | (dicto-big-brother, R = 5 and 6 agree) | 30 | 356 + 220 (ratio 1.6182; the run counts 358 + 222 with 2 + 2 on the cell boundary twice: volume 2592.92 = 2575.98 + 2 x 5.236 + 2 x 3.236) |
Each rung's cell is phi times the last. Every rung is tiled exactly by the two golden rhombohedra (tile volumes sum to the cell volume):
the golden skin is the whole lattice between the clusters. The star points do not yet carry full rhombic triacontahedra (3-5 prolate
round each at 1/1, 2/1); No full RT at 3/2 either (1-5 prolate round each of the 30 star points). Counts grow by phi^3 = 4.236 per rung (10 -> 84 -> 356; 6 -> 52 -> 220). 5/3 running (period search widened, PR = 5).
