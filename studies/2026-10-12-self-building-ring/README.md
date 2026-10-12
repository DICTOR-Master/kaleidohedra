# The self-building ring (study, 2026-10-12)

**The question.** DICTO's pyramid rule: φ·P = P (the tip) + P(1/φ) point-mirrored through the centre of the tip's base (its apex
then touches the floor) + a side ring R, with vol R = 3 vol P and Dehn invariant 0 (proved in
[2026-10-11-self-building-kit](../2026-10-11-self-building-kit/)). Can R be cut into kit pieces at golden sizes, so that the kit
truly rebuilds itself? The cases that matter: P = J2 (pentagonal pyramid, all edges 1; 5-fold ring) and P = FUJI (3-fold ring).
Labels for new things are neutral; names are DICTO's.

**Kit used throughout** (all in the Lotus frame, the 120 turns of the icosahedral group, any golden size φ^k):
I, J2, J11, AP (the pentagonal antiprism = I minus two opposite J2 caps; a J11 part), AXE, CLEO, FUJI, Mosseri–Sadoc t1–t6 and
Kramer's T2. Danzer's A, B, C, K are listed in the local test but not in the main kit: they are not part of the Chain of Karma kit,
and their dihedral angles are rational multiples of π, so they would trivially balance every invariant below.

## Answer in short
1. **J2 rebuilds itself, at the φ² step, from kit pieces** (new, exact, 5-fold symmetric, 16 pieces):

   **J2(φ²) = J11(1) + 5 J2(1) + 5 AXE(1) + 5 FUJI(1)**, and since J11 = J2 + AP with the J2 at the apex,
   **φ²·J2 = J2 (the tip) + AP + 5 J2 + 5 AXE + 5 FUJI.**

   This is DICTO's tip idea at φ² instead of φ: the tip is kept whole, and no mirrored hole is needed. It is the cap of the Lotus
   seed at any of its 12 corners. The rest of the Lotus seed then gives J11(φ²) (103 pieces) and AP(φ²) (93 pieces) too, so
   **I, J2, J11 and AP all rebuild at φ²**.
2. **The φ-step side ring R stays open, for J2 and for FUJI.** There is no obstruction:
   - the local test at every point of R passes;
   - the Dehn invariant and its refinement for the frame's turns (computed here) both balance;
   - balanced piece mixes exist even using only pieces that fit inside the ring.

   There is also no construction: R is not a clean cut of the Lotus seed or of the 1,569-piece Chain of Karma step 2 at any golden
   size, and the symmetric searches over the stated placement sets found none.
3. **FUJI does not rebuild in the existing complexes**: no clean FUJI(φᵐ), m = 1, 2, 3, in the Lotus seed or in Chain step 2. AXE neither. CLEO(φ) = φ·t2 + AXE is clean but uses a larger t2, so it is no help.
4. **The rule cannot be used for AXE and CLEO in the frame.** The point-mirrored small tetrahedron does not fit inside the band
   (`logs/angles.log`, "hole inside band: False"). That matches the 2026-10-11 note that the point mirror fits only for the
   pentagon and FUJI's hexagon.

## 1. Structure of the problem (what makes it tractable)
- **One edge class.** Every edge of every kit piece lies along one of the icosahedron's 15 two-fold axes, and every face is
  perpendicular to a five-fold or a three-fold axis: 16 plane directions in all (`logs/hadwiger.log`, `logs/face_types.log`).
- **The faces that can lie on the floor or top of a ring** (perpendicular to a five-fold axis) are only these: regular pentagons
  (J2, J11, AP), golden triangles (1, 1, 1/φ), golden gnomons (1/φ, 1/φ, 1) and T2's (1, 1, φ). That is the
  Robinson/Penrose triangle family. The faces that can lie on the sloping sides (perpendicular to a three-fold axis) are
  equilateral triangles and FUJI's hexagon.
- **The kit's dihedral angles** are α = arccos(√5/3) = 41.81°, δ = 37.38°, and the integer combinations
  π − α − 2δ (63.43°), α + δ (79.19°), π − α − δ (100.81°), α + 2δ (116.57°), π − α (138.19°), π − δ (142.62°).
  - J2 ring: floor edges δ, top edges π − δ, side edges π − α, hole rim π − δ, hole edges π + α (reflex).
  - FUJI ring: floor edges α (long) and δ (short), side edges π − δ, hole edges π + δ (reflex).
- Ring sizes (`logs/angles.log`):

  | | J2 ring | FUJI ring |
  |---|---|---|
  | volume | 0.904508497 = 3 J2 | 0.963525492 = 3 FUJI |
  | thickness | h/φ = 0.3249 (J2 height 0.5257) | 1/(√3 φ) = 0.3568 (FUJI height 1/√3) |

- Identities seen on the way: AXE = t6 and CLEO = t4 (same shape, as credited before); the old data file's t3 was four coplanar
  points and is rebuilt here with all six edges on two-fold axes (`scripts/kit_exact.py`, checked against Mosseri–Sadoc's edges).

## 2. No obstruction
**Local test** (`scripts/local_cover.py`, `logs/local-*.log`). In any cut, the pieces touching a boundary point p of R must tile R's
tangent cone at p with their own tangent cones (a corner cone, an edge wedge or a face half-space). Tangent cones do not depend on
size, so with the pieces in the 120 frame turns the possible cones at p form a finite list (3,804). Tiling R's cone is then a
finite exact cover on the sphere, solved by MILP. A "no" at any point would have been a proof of impossibility for every size at
once.
- Tested points, for both rings: every kind of corner (floor, top, hole rim, the hole's apex on the floor) and the middle of every
  kind of edge.
- All pass, and most have many covers. The J2 floor corner has 4 (a J2 corner; CLEO + 2 t1; t1 + t2; ...), the top corners over
  400. Nothing is forced.

**Invariants** (`scripts/hadwiger.py`, `scripts/mixes.py`).
- With the pieces restricted to the frame's turns, the Dehn invariant refines to Hadwiger-type edge invariants: for each class of
  edge lines, an additive measure on the arc of directions round the edge that is zero on half-planes and unchanged by the turns
  keeping that line.
- Here there is a single class (the 15 two-fold lines) and the admissible measures form a 2-dimensional space. So the refined
  invariant is orientation-free and is the plain Dehn invariant again; no new information.
- The rings' invariant is exactly 0 (φ − 1 − 1/φ = 0).
- Integer programs over piece type × size find many balanced mixes (invariant 0, volume 3 P), also when only pieces of size
  φ⁻¹ or smaller are allowed:
  - J2 ring, 11 pieces: FUJI(1/φ²) + 4 FUJI(1/φ) + I(1/φ) + t3(1/φ²) + t3(1/φ) + 3 t6(1/φ);
  - FUJI ring, 13 pieces.

  Every type and size occurs in some balanced mix, so these necessary conditions prune nothing.

## 3. No construction found
- **Clean cuts of existing exact complexes** (`scripts/ring_blockcut.py`, `scripts/region_search.py`; logs `ring_blockcut-*`,
  `convex_blockcut-step2`, `region_search-step*`).
  - Method: for every frame turn and every golden size, put the target with a corner on a vertex of the complex. Accept it if every
    complex piece meets it in a kit piece (whole, or cut into a kit shape such as J2 or J11 from an icosahedron), with at least two
    parts.
  - Check of the method: it reproduces the known clean icosahedra in step 2 (1 at φ, 12 at φ²).
  - Results in the Lotus seed (step 1):
    - J2(φ²): clean at all 12 corners (the cap rule below).
    - CLEO(φ) = φ·t2 + AXE (480 placements).
    - Nothing else: no FUJI, AXE, J2 ring or FUJI ring at φ, φ², φ³.
  - Results in the Chain of Karma step 2 (1,569 pieces): no clean FUJI at φ, φ², φ³ (14,540 + 9,080 + 3,720 placements); the rings, J2, AXE and CLEO were still running at this commit (`logs/region_search-step2.log`).
- **Symmetric placement searches** (`scripts/ring_search.py`).
  - Method: kit pieces at φ⁻¹…φ⁻³ in the 120 turns, placed with a corner on a candidate point (two rounds of closure from the
    ring's corners), grouped into orbits of the ring's turns, exact cover of sample points by MILP. All separation tests are
    vectorised and exact over 715 frame axes, so these runs take minutes where the 2026-10-11 searches ran for hours.
  - J2 ring with its corners filled by J2(1/φ) (apex exactly at the band's top corner): 147,849 placements, 41,297 orbits, every sample point coverable, exact cover **infeasible** (MILP, 175 s; `logs/search-J2-fixedcorners.log`). The corner pieces are a choice, not forced (the local test allows 4 corner covers). The earlier runs `search-J2-r2.log` and `search-J2-r2-free.log` used the broken t3 (the second was stopped unfinished).
  - The FUJI-ring run with FUJI(1/φ) corners was invalid: those corner pieces overlap (`logs/residual-FUJI.log`: cell volume
    exceeds the residual). It is kept only as a log.
  - These are statements about the stated placement sets only, not proofs: pieces can sit off the candidate points
    (non face-to-face cuts), and the true placement set is not finite.
- **Residual after the corner pieces** (`scripts/residual.py`): no kit shapes. Its cells have 70.53°/109.47° dihedrals, which no
  kit piece has.

## 4. The φ² rule for J2 (exact)
`scripts/verify_cap.py`, `logs/verify_cap.log`, data `data/cap-rule-{J2,J11,AP}-{raw,unit}.json`, render
`renders/cap-rule-J2.png`.

| target (edge φ²) | parts | volume (parts = target) |
|---|---|---|
| J2(φ²) | J11 + 5 J2 + 5 AXE + 5 FUJI (16) | 5.410248806146 |
| J11(φ²) | I(1/φ) + J2 + 5 J11 + 6 I + 55 AXE + 15 FUJI + 20 CLEO (103) | 33.738679330311 |
| AP(φ²) | I(1/φ) + 2 J2 + 10 J11 + 50 AXE + 10 FUJI + 20 CLEO (93) | 28.328430524165 |

All parts are at size 1 unless marked.
- **Where it comes from.** The cap of the Lotus seed at a corner A (the plane through A's five neighbours) cuts the corner
  icosahedron at A into exactly J11 (it reaches down to the plane) and each neighbouring corner icosahedron into exactly J2(1).
  The 5 AXE and 5 FUJI round A lie wholly inside.
- **Checks.**
  - Every part is congruent to its kit piece (corner count and all distances).
  - All parts lie inside the target, and no two overlap (separating axes on face normals and edge cross products).
  - The volumes add up to the target's with a difference of 0 to 9e-16. In the identity J11 + 5 J2 + 5 AXE + 5 FUJI = φ⁶ J2,
    both sides are 5.410248806146.
- **Tip form.** The tip J2(1) at A lies inside the cap's J11, and J11 minus the tip is the antiprism AP (checked). So
  φ²·J2 = J2 + AP + 5 J2 + 5 AXE + 5 FUJI.
- **Pattern.** 5 J2 sit at the 5 floor corners, which is where the local test also puts J2 corners. The 5 FUJI sit along the
  floor's edges and the 5 AXE along the sloping edges.

## 5. What this means for the Chain of Karma kit
- **Rebuilds at φ²:** I (Lotus seed), J2, J11 and AP, all from {I, J2, J11, AP, AXE, CLEO, FUJI}.
- **Open:** FUJI, AXE and CLEO. FUJI's φ-step ring has no obstruction and no construction yet.

So the kit is not yet shown to be self-building. The new J2 rule moves the open problem from J2 to FUJI and AXE (CLEO).

## Open questions
- **The φ-step ring R.** Neither a cut nor an impossibility proof. Every invariant tried balances and every local test passes. A
  proof would need a global argument (no known invariant beyond Dehn applies here). A construction would need a complex in which
  φ·J2 or φ·FUJI occurs as a clean region; none of the known exact complexes contains one.
- **FUJI and AXE at φ² or φ³.** A cap-like rule like J2's, which came free from the Lotus seed, would need a complex that
  surrounds a three-fold point the way the Lotus seed surrounds a corner.

## Files
- `scripts/ring_core.py`, `kit_exact.py`: kit in the frame (snapped to the golden module, t3 rebuilt) and the rings.
- `scripts/angles.py`, `face_types.py`: dihedral angles, edge lengths, face types.
- `scripts/local_cover.py`: the tangent-cone test.
- `scripts/hadwiger.py`, `mixes.py`: refined invariants and balanced mixes.
- `scripts/ring_search.py`, `guided.py`, `residual.py`: placement searches.
- `scripts/ring_blockcut.py`, `region_search.py`, `cap_cut.py`, `verify_cap.py`: clean cuts of the Chain complexes and the
  exact φ² rule.
- `scripts/render.py`: renders.
- `data/`: the cap rule (raw: Lotus-frame coordinates; unit: target edge 1, apex at the origin), invariant rows, mixes, local
  covers, region-search hits for step 1.
- Inputs not copied: the kit (`../2026-10-11-self-building-kit/data/ms-kit-j2.json`) and the Chain complexes
  (`../2026-10-11-chain-of-karma/chain-of-karma-steps-1-2.json`).
- `renders/rings.png` (the two rings), `renders/cap-rule-J2.png` (the φ² rule, assembled and exploded).
- Heavy runs on dicto-node (`~/ring`).
