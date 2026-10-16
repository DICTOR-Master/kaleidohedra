# Fable: golden fill of the Golden Bodhi Pyrochlore (2026-10-16)

DICTO's question (paper §7, "Open"): can the golden region of the bcc Ogdoecontahedron (OCD) packing be filled exactly by a small fixed set of pieces, namely golden rhombohedra, the five Bodhi pieces and adapters?

Script: `scripts/golden_fill.py` (about 20 s on the Pi). Output: `data/golden-fill.txt`; corners in `data/golden-fill.json`.
Everything is exact in ℚ(√5) unless it says "float". Angles in degrees are float. The axis types and the equalities behind them are exact.

## Results first

1. **Obstruction (proved).** The golden region G is 10.75% of space; per cell its exact volume is (5984 − 2624√5)/729. Its walls are golden planes, except for **24 small triangles per cell**. These are the star tips at the joints, and they lie in the 4 joint planes, whose normals are the three-fold axes along the cube diagonals. So golden rhombohedra and the Bodhi pieces alone cannot fill G. Any fill needs pieces with faces in those 4 three-fold planes. More precisely, it needs a piece edge with dihedral angle at most **20.905°** along a two-fold line, which is smaller than any golden piece's angle (36° at least).
2. **One adapter kind is enough to remove the obstruction (exact, constructive).** On each tip we put a flat triangular pyramid: its base is the tip, and its three sides are golden planes. Its shape is the **three-fold corner of a rhombic triacontahedron**, cut off through the corner's three neighbours. All 24 per cell are congruent and nothing overlaps. Together they fill 0.53% of space.
3. **What is left (G′, 10.22% of space) has only golden walls, and every edge of G′ runs along a five-fold axis.** These are the edge directions of the golden rhombohedra. The convex edges, 48 per cell, all open at 36°, and each one must hold the acute edge of exactly one oblate rhombohedron (or a 36° edge of a Mudra, Crown Jewel or Diadem). So **no local edge obstruction is left**. Whether G′ actually tiles by golden rhombohedra is still open; the pass ended before a tiling search.
4. **Larger region (22.6%, the non-golden shell included): impossible with golden pieces, Bodhi pieces and Cleo-Icos.** All 60 kites of every OCD face the gap. Kite normals lie on no symmetry axis, and none of those pieces has a face in a kite plane.
5. **The Cleo-Ico is not the tip adapter.** Its squared side-to-base ratio is (5+√5)/8; the tip adapter's is (5−√5)/8, the conjugate. The Cleo-Ico remains the candidate for the free OCD hexagons in the larger region (step 11).

## Part 1: the obstruction (exact)

**Setup.** OCD copies on the bcc lattice with basis t₀+t₁, t₀+t₂, t₀ (as in `golden_cut.py`), one copy per cell. The cell volume is (512 + 256√5)/729. Each copy's golden envelope is the circumscribed rhombic triacontahedron, with exact volume (−320 + 160√5)/27. Cut at the 8 joint planes it becomes the body K: 24 corners, 30 golden faces and 8 triangular joint faces, with volume (−608 + 320√5)/81. The per-cell split matches step 18: OCD 77.43%, shell 11.82%, G 10.75%.

**No overlaps, exact.** K is centrally symmetric, so K and K + c overlap exactly when c/2 lies inside K. Of the 14 neighbours that could reach, none overlaps and 8 touch: the 8 joined neighbours, one across each joint plane.

**The walls of G.** Every wall of G lies on the boundary of some envelope. The envelope faces are the 30 golden faces and the 8 joint faces, so the only possible non-golden walls are parts of joint faces. Across each joint face, exactly one neighbour touches. Its face there is the same triangle turned 180°.
- The two triangles overlap in the central hexagon, which is exactly **2/3** of the triangle.
- The remaining **1/3** is three equilateral tips, each with squared side (8/27 − 8√5/81).
- The covered and exposed areas add up to the whole face exactly.

Every tip faces the gap on the neighbour's side. That gives 8 joint faces × 3 tips = **24 tips per cell**, in 4 plane orientations (± the 4 three-fold axes on the cube diagonals).

**Proof of the obstruction.** Suppose G is cut into finitely many polyhedra in any bounded region. Then each tip, a planar region of positive area, must be covered by faces of pieces that lie in its own plane. A face in any other plane meets that plane in a line, which has zero area, and finitely many lines cannot cover a triangle. Every face of a golden rhombohedron and of each Bodhi piece is perpendicular to a two-fold axis. A tip's normal is a three-fold axis. So no such face lies in a tip plane, and these pieces alone cannot fill G. ∎

**Edge form (sharper).** Where a tip meets the neighbour's golden face, G has a convex edge along a two-fold line. Its opening angle is 20.905°, with cos² = φ²/3 (exact).
- At a convex edge, every piece must have an edge along that line. A point on a face of a piece would need an opening of 180°.
- The pieces' dihedral angles at that line must add up to 20.905°.
- Golden pieces have dihedral angles of 36° or more: rhombohedra 36°, 72°, 108°, 144°; Bodhi pieces 36° to 144°.

So the minimal non-golden piece has a face in a joint plane that meets a golden face at 20.905° along a two-fold edge.

## Part 2: the search pass (one pass)

**Candidate.** For each tip, take the joint plane plus the golden planes through the tip's three edges. Two of these planes are the copy's own faces extended past the cut. The third is the neighbour's face. Exact vertex enumeration gives a bounded tetrahedron:
- base: the tip;
- squared edges: base 8/27 − 8√5/81, sides 20/81 − 8√5/81;
- volume: (−44 + 20√5)/2187 = 3.30e-4;
- the three side edges lie along five-fold axes, with dihedral angles of 144° between the golden faces and 20.905° at the base (float).

Squared base over squared side is 2 + 2√5/5 = 4φ/√5 (exact). That is the long diagonal of a golden rhombus over its edge. So the piece is the rhombic triacontahedron's three-fold corner cut through its three neighbouring corners. This is the "hexagon junction" cap that step 10 predicted, and here it fits exactly. We know of no existing DICTO piece with this shape; it has no name yet.

**Fit (exact).** All 24 per cell are congruent. We ran a separating-axis test over 254 nearby pairs of envelopes and adapters: 0 overlaps, 176 touching pairs. Each adapter's base equals its tip exactly. Its two "own face" sides continue the copy's golden faces flat, so no new edge appears there. Its third side lies on the neighbour's golden face.

**What is left: G′.** G′ is G minus the adapters, with exact volume per cell (704/81 − 928√5/243) = 0.151971, which is 10.22% of space.
- **Walls:** all golden. Each joint face is now covered exactly by the 2/3 hexagon contact plus three adapter bases.
- **Edges:** We list every place where two bodies touch, reduced modulo the lattice, and test the opening of the free space at each edge.
  - The 120 contact-boundary segments per cell give exactly **48 convex edges, all along five-fold axes, all opening at 36.0°** (float). They are the two side edges of each adapter that border the neighbour's face, and each has length (φ/9)·|v| (exact), where |v| is the five-fold vector.
  - The body edges, sampled at 3 exact points each, are either closed, flat, or **reflex at 216°**. The reflex ones are the envelope's own triacontahedron edges and the third side edge of each adapter, all along five-fold axes.
  - The envelope's cut edges along two-fold lines are fully closed.
- **For golden rhombohedra:** their only dihedral angles along their five-fold edges are 36°, 72°, 108° and 144°. So each 36° convex edge takes exactly one oblate rhombohedron. No edge direction or angle forbids them. Before the adapters, the 24 convex edges per cell were two-fold at 20.905°, and they forbade every golden piece.

**Volume bookkeeping (exact; only binding for periodic fills).** A golden rhombohedron spanned by three five-fold vectors scaled by λ has volume λ³·d. Here d is d_O for the oblate one and d_P = φ·d_O for the prolate one. φ is irrational, so the numbers of prolate and oblate pieces per cell are fixed by the volume. A periodic fill (any sublattice of the packing) has rational numbers per cell.
- **Brick edge (φ/9)|v|**, equal to the convex-edge length: this would need −30 oblates per cell. So **no periodic fill exists at this scale.** A non-periodic fill with irrational frequencies is not ruled out.
- **Brick edge |v|/9:** 138 prolate + 102 oblate per cell, whole and non-negative. This is consistent, but it does not prove a fill exists.
- **Edge |v|/18:** 1104 prolate + 816 oblate per cell. Edge (φ/18)|v| fails again (−240 oblates).

Nothing forces the brick edge to divide the convex-edge length: a brick's edge may run past an adapter's tip along the neighbour's face. So the scale is free, and these lines are checks, not a proof.

**Bodhi pieces (float data from the Bodhi study).** Between golden planes, the dihedral angle fixes the edge axis exactly: 36°, 72°, 108° or 144° means a five-fold edge, 60° or 120° three-fold, 90° two-fold. Each two-fold axis has 2 neighbours at 90°, 4 at 60° and 8 at 36° or 72°, which accounts for all 14. The angles are:

| Piece | Dihedral angles |
|---|---|
| Vajra (fine) | 72, 90, 108, 120 |
| Chatra | 60, 72, 90, 108, 120 |
| Mudra | 36, 120, 144 |
| Crown Jewel | 36, 90, 120, 144 |
| Diadem | 36, 60, 90, 108 |

So the Bodhi pieces bring two-fold and three-fold edges that G′ does not need, and Mudra, Crown Jewel and Diadem also have the 36° five-fold edge. The full set passes the edge test too.

**A wording correction.** Step 18 calls the Bodhi pieces "golden zonotopes". They have only golden face planes, but they are not zonotopes. The Vajra, for example, is a triangular bipyramid, which is not centrally symmetric. G′ is not a zonotope either: it is non-convex and periodic. So the classical dissection of a zonotope into parallelepipeds does not apply, and this report does not use it.

**Larger region (22.6%), exact.** OCD copies touch only on the 8 joint hexagons, with 8 touching neighbours per copy and no other contacts. So all 60 kites and the 12 free hexagons of every OCD face the gap. Kite normals lie on no symmetry axis (exact). By the same area argument, a fill must include pieces with faces in kite planes. Golden pieces, Bodhi pieces and Cleo-Icos have none, so that set cannot fill the larger region.

## Not done (the pass stopped here)

- No tiling of G′ was attempted, so tileability by golden rhombohedra, or by them plus Bodhi pieces, is still open. We did not check the conditions at G′'s corners (the cone of free space at each corner), and we did not check whether G′'s corners lie in a common module of rhombohedron edge vectors.
- The 20.905° edge test used float angles. The axis types, the 144° dihedrals (from the exact edge types) and the length and area ratios are exact.

## Summary for paper §7 (3–5 lines)

The golden region's walls are golden planes except for 24 star-tip triangles per cell in the four three-fold joint planes. These triangles form one third of each joint face, and they meet the neighbour's golden face at 20.905° (cos² = φ²/3), so golden rhombohedra and Bodhi pieces alone cannot fill the region (exact). One adapter kind removes this obstruction: the three-fold corner cap of a rhombic triacontahedron on each tip, 24 congruent per cell, with no overlaps (exact). What remains has only golden walls and only five-fold edges, and its convex edges all open at 36°, the acute edge of the oblate rhombohedron. So no local obstruction is left, but a tiling has not been found, and at the brick edge equal to the convex-edge length a periodic tiling is ruled out by volume. Including the non-golden shell needs pieces with faces in the OCD kite planes.
