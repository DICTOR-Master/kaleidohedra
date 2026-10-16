# Fable, pass 3: G′ when the tiling is not face to face (2026-10-16)

DICTO · dictospheres.com

The question: can G′ (the golden region minus the 24 GBPCs per bcc cell) be tiled by golden rhombohedra of any sizes when the tiles do not have to meet face to face?

Everything is exact in ℚ(√5) unless marked FLOAT. |v| is the five-fold vector (the icosahedron circumradius). λ = φ|v|/9 is the length of the 36° convex edges.

Scripts and outputs (in `scripts/` and `data/`):
- `gbpc_build.py` → `gbpc-build.txt`, `gbpc-build.json`: the greedy build.
- `gbpc_build_check.py` → `gbpc-build-check.txt`: FLOAT check of the build.
- `gbpc_periodic_count.py` → `gbpc-periodic-count.txt`: the periodic count.
- `gbpc_hadwiger.py` → `gbpc-hadwiger.txt`: the Hadwiger invariant and the lens.

## Results first

1. **No tiling found.** A greedy exact build (periodic, anchored at the corners of G′) fills **46.54%** of G′ and then stops. It uses 184 rhombohedra per cell: 12 oblates of edge λ, plus 143 oblates and 29 prolates of edge λ/2.
   - The placements are checked exactly: no overlaps, and none enter an RT.
   - The exact remainder is (8762 − 3892√5)/729 per cell = 0.0812, which is 53.46% of G′.
   - After this the build is stuck: no corner of G′ and no tile corner admits another tile of either size.
2. **Every tile that touches a wall has an edge in ℚφ·|v| (exact theorem; any arrangement, any sizes).** Each wall is covered by the faces of the tiles that lie in it. A face of a tile with edge s is an s × s square in the wall's frame. Take any ℚ-linear f with f(φ) = 0. The Dehn-type sum over a wall's corners, Σ c·f(x)f(y), is 0, because every wall-corner coordinate is a rational multiple of φ (pass 1). The same sum over the faces is Σ f(s)², so f(s) = 0 for every such face, which means s ∈ ℚφ.
3. **No periodic tiling uses only edges in ℚφ·|v| (exact; any number of sizes; face to face or not).** Per cell, G′ = (X + Yφ)·φ³·vol(oblate, edge |v|), where X sums r³ over the oblates (edge rφ|v|) and Y sums r³ over the prolates. The rational part is forced: **X = −10/243 < 0**. So a periodic tiling needs tiles whose edges are not rational multiples of φ|v|. By item 2, those tiles can never touch a wall with a face.
   - This covers attempt (b): periodic dissections of golden zonotopes, of the rhombic triacontahedron or of the hexecontahedron at ℚφ scales all fail on this count.
4. **The Hadwiger edge invariant does not obstruct (exact).**
   - **The invariant.** J_{ℓ,u} adds edge length × ([u in wedge] + [−u in wedge] − angle/π) over the edges in direction ℓ. It is additive under any dissection, and it is 0 on every parallelepiped. So it is 0 on any union of golden rhombohedra, face to face or not.
   - **Its value on G′.** For G′ it is 0 for all 6 five-fold directions (tested with 3 generic u each).
   - **Why it vanishes.** Each pair of joined RTs overlaps in **an oblate golden rhombohedron of edge 2λ = 2φ|v|/9** (exact: 12 five-fold edges, dihedral angles 36° and 144°, volume as the oblate's). The RT has edge 3λ = φ|v|/3. Zonotopes and rhombohedra all have J = 0.
5. **So the case that is not face to face is undecided after the cap.** It is not ruled out. A tiling would have to use edges in ℚφ·|v| at every wall. If it is periodic, it also needs other edge lengths somewhere inside.
6. **Bodhi pieces (attempt c) were not tested.** Their exact volumes and edge data are not in this pass. Unlike rhombohedra, they need not have J = 0, so they could matter.

## The greedy build (exact placements)

**Bodies.** Every body here has its face normals on the 15 two-fold axes and its edges on five-fold axes: the uncut RTs and golden rhombohedra of any size and orientation. So two bodies overlap exactly when their projections overlap on all 15 two-fold axes, which gives an exact and complete test.

**Method.**
- Anchors are the 48 corners of G′ plus the corners of tiles already placed (all reduced to the cell nearest the origin).
- At each anchor we try the 160 corner orientations and keep the one with the most face contacts.
- The fill is periodic: every tile stands for its lattice orbit.

| Stage | Tiles per cell | Filled |
|---|---|---|
| edge λ = φ\|v\|/9 | 12 oblates | 15.63% |
| + edge λ/2 | + 143 oblates, 29 prolates | 46.54% |

**Checks.**
- Exact: 0 overlapping pairs, including lattice translates, and 0 tiles entering an RT.
- FLOAT Monte Carlo inside the script: 0 sample points inside an RT or inside a second tile.
- FLOAT independent check (200,000 random points in the cell): tiles cover 46.9% of the free points, 0 points are covered twice, and 0 tile points lie inside an RT.

**What the stall means.** The order is greedy and corner-anchored, so stalling proves nothing about other orders. It does show that G′ is thin: only 12 oblates of edge λ fit per cell. Most of G′ needs smaller tiles.

## Physical build notes

- **The partial fill.** The 184 tiles per cell are an exact, overlap-free set. It is ready to build as a partial fill: coordinates in `data/gbpc-build.json`, in the frame of `golden-fill.json`.
- **The envelope skeleton.** Joined RT envelopes share exactly one oblate of edge 2λ. The RT has edge 3λ. So an envelope skeleton built from RTs with the shared oblates is commensurable at λ. We did not build or check a tiling of it.

## Paragraph for the paper

For tilings that are not face to face, the question stays open. A greedy exact build with golden rhombohedra of edges φ|v|/9 and φ|v|/18 fills 46.5% of G′ (184 tiles per bcc cell, overlap-free, exact) before no further corner admits a tile. Two exact constraints hold for any arrangement. Every tile with a face on a wall of G′ has its edge in ℚφ·|v| (a Dehn-type argument on the walls). And a periodic tiling cannot use only such edges: its count requires −10/243 for the oblates. The Hadwiger edge invariant gives no obstruction. It vanishes on G′ because each pair of joined envelopes overlaps in exactly one oblate golden rhombohedron of edge 2φ|v|/9, so G′ is, as a valuation, a combination of zonotopes. Whether G′ has a tiling that is not face to face, perhaps with Bodhi pieces, remains undecided.
