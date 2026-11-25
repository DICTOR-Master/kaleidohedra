# Do the Vacuus and the Resonus make a web in tilings with more than one kind of cell? (25 Nov 2026)

DICTO · data study, V SF A project; the question is **DICTO's** ("what about the octahedron and tetrahedron … stella octangula and TRD too").
Follows study 2026-11-25-vacuus-resonus-lattice-webs, which covered lattice tilings by one cell.

> **Status box.** Study note, not published. Exact (rationals). Script `scripts/mixed_webs.py`, log `logs/mixed_webs.log` (FINAL ok).
> Controls: the same code reproduces the lattice-webs results for the cube (all 9 families continue) and the rhombic dodecahedron (all 6).

**Test.** A family is one plane direction n. Its planes are the central planes n·x = n·c of the cells that carry n in their Vacuus
(or Resonus). The family **continues** when every one of its planes that passes through the inside of a cell is that cell's own central
plane; otherwise it **breaks**. For the stella octangula (not convex) a plane passes through its inside when it cuts the octahedron or one
of the 8 tetrahedra, or runs along one of the 8 inner faces.

## Conclusion

| tiling | Vacuus | Resonus |
|---|---|---|
| tetrahedra + octahedra (honeycomb) | the octahedron's 3 coordinate planes continue; the tetrahedron's 6 planes x_i = ±x_j break | all 4 break |
| stellae octangulae + octahedra | all break (outer edges); with the 12 inner edges the 3 coordinate planes continue | all 4 break |
| trapezo-rhombic dodecahedra (hcp) | the 3 upright families continue; the 6 tilted ones break | the same 3 continue, 6 break |

1. **Tetrahedra + octahedra.** Only the octahedron's Vacuus (the coordinate planes x_i = integer) makes a web. The tetrahedron's
   planes x_i = ±x_j pass through the octahedra's centres, but they are not planes the octahedron owns (they are mirrors of the
   octahedron, not its Vacuus), so they cut it. The face-parallel planes (normals (±1, ±1, ±1)) of both solids break at once: the
   tetrahedron's central plane sits half-way between face layers and cuts the neighbouring octahedra.
2. **Stellae octangulae.** The tiling exists: every fourth octahedron (centres 2ℤ³ + (1, 0, 0)) with its 8 tetrahedra is a stella;
   each tetrahedron belongs to exactly one stella (checked for all 216 in |x| ≤ 3); the other octahedra fill the rest. Its Vacuus from
   the outer edges (x_i = ±x_j) and its Resonus break. If the 12 inner edges (where the two tetrahedra cross) count, the coordinate
   planes continue, as in 1.
3. **Trapezo-rhombic dodecahedra.** Its Vacuus and Resonus have the same 9 directions. The 3 upright families (perpendicular to the
   hexagonal layers) continue; the 6 tilted ones break, because the hcp stacking ABAB… turns every second layer.

**One-line conclusion.** Outside lattice tilings, the webs that survive are the coordinate-plane web (octahedra, and the stella if its
inner edges count) and the upright web of the TRD; every face-parallel family of the tetrahedron, octahedron and stella breaks.


## Second notion: continues through mirrors (DICTO: "it seems like continuing"; rule worded by a Fable review, 25 Nov)

**Rule.** A family continues through mirrors when every one of its planes that passes through the inside of a cell goes through that
cell's centre and is either the cell's own plane of the kind tested or a mirror plane of the cell. The family is still made only from the
cells that carry its direction. Mirrors need a metric (the identity for the cubic tilings, the hcp Gram matrix for the TRD).
Exact rerun (same script, `THROUGH MIRRORS` lines; the cube control is unchanged):

| tiling | Vacuus through mirrors | Resonus through mirrors |
|---|---|---|
| tetrahedra + octahedra | **all 9 continue**: the planes x_i ∈ ℤ and x_i ± x_j ∈ ℤ | all 4 break |
| stellae octangulae + octahedra | **all 9 continue** (the inner-edge question no longer matters) | all 4 break |
| trapezo-rhombic dodecahedra | 3 upright continue, 6 tilted break (unchanged) | the same |

The Vacuus web of both cubic mixed tilings is then the full mirror arrangement x_i, x_i ± x_j ∈ ℤ, the same arrangement as the cube's
Vacuus + Resonus web. In lattice tilings the two notions agree (every cell carries the same directions).
**Caution (from the review):** the second notion depends on symmetry, not only on DICTO's planes, and needs a metric; before any claim,
check that it says more than "the planes are mirrors of the tiling".

## LEADS
1. DONE: mirror crossing as a second notion (section above).
2. TRD: the upright web is the 2D web of the hexagonal layers (triangular arrangement) carried through all layers.
3. Lean: the coordinate-plane web of the honeycomb is Theorem 0 of M4 applied to the octahedra alone (they form a lattice); the
   tetrahedra need a two-kind version of `web_iff`.
