# Fable: does G′ tile by golden rhombohedra? (2026-10-16)

DICTO · dictospheres.com

DICTO's question: after the 24 GBPCs (Golden Bodhi Pyrochlore Corners) per cell, can the rest of the golden region, G′, be tiled exactly by golden rhombohedra, perhaps with Bodhi pieces?

Script: `scripts/gbpc_tiling.py` (exact, about 4 min on the Pi). Output: `data/gbpc-tiling.txt` and `data/gbpc-tiling.json`.
Float check of connectivity: `scripts/gbpc_connectivity.py` → `data/gbpc-connectivity.txt`.
Everything is exact in ℚ(√5) unless marked FLOAT. |v| is the five-fold vector, the icosahedron circumradius, as in FABLE-GOLDEN-FILL.md.

## Results first

1. **What G′ is (exact).** G′ is space minus the union of the *uncut* rhombic triacontahedra (RT) on the bcc sites. Each RT overlaps its 8 joined neighbours, each overlap has volume (−704 + 320√5)/729, and no three RTs share any volume. Each GBPC is the part of an RT corner that sticks out past the joint plane and is not inside the neighbour.
2. **Corner test (exact): passes.** G′ has 48 corners per cell. At every one, the free space splits exactly into corner cones of golden rhombohedra. No corner forbids them.
3. **Module test (exact): passes, and fixes the scale.** All corners lie in one copy of the icosahedral module λM, with λ = φ/9 (edge (φ/9)|v| = 0.1798|v|, the length of the 36° convex edges). The finer scales φ/(9k) also work.
4. **Wall test (exact): passes only at λ = rational × φ.** Each wall of G′ must be covered by rhombus faces of a single shape. That works only if λ is a rational multiple of φ; the coarsest is φ/9.
5. **Count test (exact): FAILS.** For a face-to-face tiling of one size, the numbers of prolates and oblates per cell are forced: at λ = φ/9 they must be **66 prolate and −30 oblate**. This holds for periodic and non-periodic tilings. At λ = φ/(9k) both numbers are multiplied by k³, so the oblate count is negative at every allowed scale.
   **So G′ has no face-to-face tiling by golden rhombohedra of one size, at any scale.**
6. **Smallest fix found:** a second size. Add oblate rhombohedra with edge |v|/9 (the same oblate scaled down by φ). The count then works, and it forces **at least 10 small oblates per cell**. With both sizes, none of our tests rules a tiling out. We did not build a tiling.

**Not covered:** tilings that are not face-to-face, and fills that use Bodhi pieces. Both stay open.

## 1. What G′ is (exact)

- Uncut RTs on the bcc sites: each one overlaps exactly its 8 joined neighbours.
- No three RTs overlap with positive volume.
- Union per cell = vol(RT) − ½ × (8 pair overlaps) = (−5824 + 3040√5)/729.
- K + 24 GBPC per cell has the same volume. K and every GBPC lie inside the uncut RT. So the two regions are equal, up to measure zero.
- So **G′ = space minus the union of the uncut RTs.** Its walls are the parts of the RT faces that no neighbour covers.
- FLOAT (72³ voxels): G′ is one connected periodic region. It holds 99.8% of the free voxels and wraps around the cell. The other 84 bits are 1–2 voxel slivers in the 36° wedges.

## 2. Corner test (exact)

- **Corners.** Every corner of G′ is a corner of some wall. That gives 48 corners modulo the lattice.
- **Chambers.** Every wall is a golden plane, and the 15 golden planes are the mirror planes of the icosahedral group. They cut every direction around a point into 120 chambers (exact).
- **Free cone.** At each corner, the free cone is a set of whole chambers.
- **Tile cones.** These are sets of chambers too:
  - 160 rhombohedron corner cones (any three five-fold rays, no opposite pair);
  - 240 edge wedges;
  - 30 half-spaces.
- **Search.** An exact-cover search, using only rhombohedron corner cones:

| Free cone (chambers of 120) | Corners | Splits into rhombohedron corner cones |
|---|---|---|
| 18 | 14 | yes |
| 60 | 5 | yes |
| 72 | 5 | yes |
| 78 | 11 | yes |
| 90 | 11 | yes |

No corner forbids golden rhombohedra.

## 3. Module check (exact)

- M is the ℤ-span of the six five-fold vectors (the Ammann–Kramer module). It has rank 6, and its rational span is all of ℚ(√5)³. So any finite set of exact points lies in some (1/N)M. **The module test can fix the scale, but it cannot forbid a tiling on its own.**
- M is not closed under multiplication by φ (exact). So the scale cannot be rescaled freely by powers of φ.
- All 48 corners, with all their lattice translates, lie in one coset x₀ + λM at λ = φ/9 (and at φ/(9k)).
- In a face-to-face tiling, every tile corner lies in that coset.

## 4. Wall test (exact, any arrangement of faces)

- **Which faces cover a wall.** A wall lies in a golden plane, which holds two five-fold vectors a, b. So any rhombohedron face lying in a wall is the parallelogram λa × λb.
- **The invariant.** In (a, b) units, take F(x, y) = g(x)h(y) with g and h λ-periodic. Over each λ-square, the integral of ∂²F/∂x∂y is 0. Over a wall, it equals the sum of c·F over the wall's corners, where c = ±1 is the corner sign.
- **The condition.** So in every class of corners taken modulo λ in x and in y, the signs must add up to 0. This holds for any arrangement of the faces, edge-to-edge or not.
- **The walls.** There are 30 walls per cell, one on each RT face:
  - 6 are golden rhombi with side (φ/3)|v|;
  - 24 are L-shaped hexagons.
- **Result.** All wall-corner coordinates differ by rational multiples of φ. Every wall passes exactly when λ ∈ ℚφ, and the coarsest passing scale is λ = φ/9. Any λ that is not a rational multiple of φ fails on every wall.

## 5. Count test (exact; the obstruction)

**Setup.** Let σ be the Galois map a + b√5 ↦ a − b√5, applied coordinate by coordinate. It is the perp-space map of the module. Take a face-to-face tiling.
- Every tile corner lies in ℚ(√5)³, so σ is defined there. Extend it affinely over each tile.
- Then the image of a tile has signed volume σ(its volume).
- Let A be the linear map with σ(T) = A·T on the bcc lattice.

**Homotopy formula.** For the tiles in an N³ block of cells:

Σ σ(tile volumes) = det(A)·vol + (flux through the walls) + O(N²).

- On each wall, the map is fixed by the wall alone, so the wall flux per cell, Φ, is a fixed number.
- The O(N²) term holds because every tile corner is a bounded number of tile edges from a wall.

**Checks (exact).**
- The formula reproduces σ(vol RT) for one RT, both with A = 0 and with the bcc A.
- For G′, det(A)·vol(G′) + Φ = σ(vol G′) = 704/81 + 928√5/243.

**Result.** So the prolate and oblate densities p, o per cell satisfy two linear equations:
- p·vol(P) + o·vol(O) = vol(G′);
- p·σ(vol P) + o·σ(vol O) = σ(vol G′).

The two equations are independent, because φ ≠ σ(φ). At λ = φ/9 their unique solution is **p = 66, o = −30**. This is the same split as the periodic bookkeeping in the first pass, but now it binds every face-to-face tiling, periodic or not.

**Conclusion.** Since o < 0 at every allowed scale, no such tiling exists.

**Status.** The computations are exact. The analytic step (homotopy, O(N²) bound) is a proof sketch here and has not been independently checked.

## 6. Minimal additions (exact bookkeeping, λ = φ/9, units of the oblate volume, x = m + nφ)

G′ per cell = −30 + 66φ. In a face-to-face tiling, each piece contributes its own (m, n), and the m-values must add up to −30. Pieces with negative m are needed:

| Extra piece | m | n | Helps? |
|---|---|---|---|
| more GBPCs | +1/6 | 0 | no |
| oblate, edge \|v\|/9 (= λ/φ) | −3 | 2 | **yes** |
| prolate, edge \|v\|/9 | 2 | −1 | no |
| oblate / prolate, edge φλ | 1 / 2 | 2 / 3 | no |

**With both sizes:**
- The wall test gives no condition, because the periods φ/9 and 1/9 are incommensurable.
- The count becomes o − 3o′ + 2p′ = −30 and p + 2o′ − p′ = 66, where the primes count the small pieces.
- Non-negative solutions exist, for example o′ = 10, p = 46. Every solution has **o′ ≥ 10 small oblates per cell**.
- This removes every obstruction we know of. It does not prove that a tiling exists.

**Bodhi pieces.** These were not tested. Their faces bring two-fold and three-fold edges into the walls, and their volumes change the count, so they could also remove the obstruction. This needs their exact volumes.

## Not done (cap reached)

- **Step 3, the constructive tiling, was not attempted.** The count test rules out the one-size case, and the two-size case needs a new search.
- **Non-face-to-face tilings** (tiles sliding along a golden plane) are open. The wall test covers them, but the count test does not.

## Summary for the paper (3–5 lines)

After the 24 GBPCs per cell, the remaining golden region G′ is exactly space minus the union of the uncut rhombic triacontahedra, and every one of its 48 corners admits golden-rhombohedron corner cones (exact). Its walls force the edge length to be a rational multiple of φ|v| (coarsest φ|v|/9), and all corners lie in one Ammann–Kramer module at that scale. A Galois (perp-space) count then forces 66 prolate and −30 oblate rhombohedra per cell, so G′ has no face-to-face tiling by golden rhombohedra of one size, periodic or not (exact computation; proof sketch). Adding a second, φ-smaller oblate, at least 10 per cell, removes every obstruction we know of; whether a tiling then exists is open.
