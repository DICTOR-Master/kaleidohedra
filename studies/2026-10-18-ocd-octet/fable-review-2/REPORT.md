# Fable review 2 — the two-shape kit (steps 21–27) — 2026-10-18

DICTO · dictospheres.com — independent verification and critical review (Claude Fable 5.1) of `studies/2026-10-18-ocd-octet` Stage 4: golden envelopes in the octet, outer corners, φ⁻² vertex cuboctahedron, plane trick, and the **two-shape kit** (golden envelope + grown piece left/right). Research branch only.

Scripts: `scripts/fable2_exact.py` (own exact Q(√5) engine, `fable2_engine.py` = the engine of `fable-review/`, Pi, 164 s), `scripts/fable2_node.py` (dicto-node: manifold3d meshes, dihedral angles, 8 000 000 sample points), `scripts/fable2_cusp.py` (float, contact points of the outer corners). Data: `data/fable2-exact.json`, `data/fable2-node.json`, `data/fable2-cusp.json`, logs, `data/fable2-input.json`. "Exact" means Q(√5) arithmetic with the same rules as the first review (1e-7 float pre-screen only on which plane triples to solve; every corner, volume and facet re-proved exactly).

## 1. Verdict

| Claim | Verdict |
|---|---|
| **Two-shape kit fills space exactly once** (golden envelope at every OCD centre + grown piece G at every tetrahedron site) | **PROVED EXACTLY** (§1.1); sampling 2 000 000 uniform + 2 000 000 near-face points: 0 uncovered, 0 double |
| G is one solid | **PROVED EXACTLY** (84 convex cells, one adjacency component; mesh: 1 part, genus 0, no slivers) |
| G is chiral; the T− piece is its point reflection | **PROVED EXACTLY** (§1.2) — step 27b tested only the 24 cube turns; the missing completeness argument is supplied |
| Step 21 (no envelope overlap; RT = part in octahedron + 8 keys; share 90 − 40√5 = 10/φ⁶) | **PROVED EXACTLY** (re-derived) |
| Step 24 (pyramid = φ⁻² corner, 80.9 % of the outer corner; vertex cuboctahedron = ⅓ RT, outside all envelopes) | **PROVED EXACTLY** (re-derived); the cuboctahedron shares a whole rhombus face with each of its 6 envelopes |
| Step 26 central cell = 12-pentagon, 20-corner dodecahedron, "tetartoid-like" | **PROVED EXACTLY**: it *is* a tetartoid (§2.3); the 113-cell / 12-shape count of step 26 was not re-derived |

### 1.1 Proof structure (all exact)
1. **Regions.** Tetrahedron centres (R/2)(odd, odd, odd) form a cubic lattice of spacing R; their nearest-centre regions are the cubes of edge R, which tile space (trivial). The cube at (R/2)(1,1,1) is [0,R]³; its corners alternate: OCD centres (0,0,0), (R,R,0), (R,0,R), (0,R,R) and octet vertices (R,0,0), (0,R,0), (0,0,R), (R,R,R).
2. **Envelopes are interior-disjoint.** All 12 neighbours at distance R√2: exact intersection volume 0. (No other OCD centre is within 2 × circumradius 0.7837.)
3. **Exactly four envelopes meet a cube — its four OCD corners.** Every OCD centre within reach was tested; the four bites each have volume RT/8 = (−40 + 20√5)/27 (the RT's three coordinate mirror planes are the cube's faces at that corner), all others 0.
4. **G = cube − 4 bites**, so vol G = R³ − RT/2 = **(176 − 72√5)/27 = 0.555671** = (1 − 10/φ⁶)·cell/2, as claimed. The 84 convex cells of the exact decomposition sum to this.
5. **Once-and-only-once.** Every point lies in exactly one cube (up to measure zero); if it is in an envelope it is in exactly one (step 2) and in no G (G excludes the envelopes); otherwise it is in exactly one G. Pieces are closed, interiors disjoint, density 1.
6. **T− piece = −(T+ piece):** the cube at −m has OCD corners −c_k and RT = −RT (exact corner sets), so the piece is the exact point reflection.

### 1.2 Chirality (exact)
Of the 48 cube symmetries about the cube centre, exactly the 12 rotations of the tetrahedral group T map the bite set (centres + 30 RT planes each) to itself; none of the 24 improper ones does, and no improper one even preserves G's 44-corner set. Completeness: conv(G) is the cube with its 4 OCD corners cut off at 2/3 along each edge (10 faces, exact), whose symmetry group is T_d; any isometry of G onto G or onto its mirror image preserves conv(G), hence is one of the 24 T_d operations tested. So **Sym(G) = T** and the T− piece is a genuine mirror partner. (This is forced by the lattice: the tetrahedral sites of Fm3̄ have site symmetry 23.)

### 1.3 Sampling (dicto-node)
| points | kit | n | no piece | exactly one | two or more | in two envelopes |
|---|---|---|---|---|---|---|
| uniform | envelope + G | 2 000 000 | 0 | 2 000 000 | 0 | 0 |
| near faces | envelope + G | 2 000 000 | 0 | 2 000 000 | 0 | 0 |
| uniform | envelope + W (§4, I1) | 2 000 000 | 0 | 2 000 000 | 0 | 0 |
| near faces | envelope + W | 2 000 000 | 0 | 2 000 000 | 0 | 0 |

Near-face points: moved onto a random envelope face plane or a random cut plane and pushed off by 10⁻⁶…10⁻² (log-uniform).

## 2. The grown piece G, exactly

### 2.1 Faces, corners, edges
- **30 faces, 44 corners, 72 edges** (V − E + F = 2; mesh agrees: 44 corners, genus 0).
- **Envelope faces = exactly half an RT surface (15 golden rhombi worth):** 12 whole golden rhombi (3 per bite, the rhombi round each bite's 3-fold corner (s,s,s)-type) + 12 quarter rhombi = right triangles with legs **s = R/φ² = 0.4120 and s/φ = 0.2546** (the three axis faces x,y,z = 2/3 of each bite, cut by the cube's coordinate planes).
- **Cube faces: 6 congruent non-convex 10-gons**, area (−10 + 6√5)/9 = 0.3796 each (square R² minus two pentagonal bite sections). Interior angles: **90° ×6, 211.72° ×2 (= 180° + 31.72°), 238.28° ×2 (= 270° − 31.72°)**; 31.72° = arctan(1/φ) = half the acute golden-rhombus angle. So the cube cuts are square cuts, but their outline is set by golden angles.
- Surface area 5.4252 (exact: (−20/3 + 4√5) + 15 rhombi of area (−16 + 8√5)/9); **ψ = 0.6025** (RT 0.9609); the mesh gives the same to 7 digits.
- **Dihedral angles (exact): 90° (36 edges: cube edges and triangle legs), 108° (12: a whole rhombus meets a cube face), 216° reflex (24: RT edges inside the bites). No edge sharper than 90°, no slivers.**
- conv(G) = cube truncated at the 4 OCD corners by planes through the points 2/3 along the edges (volume (32 + 24√5)/81).

### 2.2 Thin places — the envelope gap
- **Neighbouring envelopes do not touch: their gap is exactly gap² = 26/9 − 58√5/45, gap = 2/(3φ³√(φ√5)) = 0.08274 = 0.0767 R**, realised between two *parallel RT edges* lying in the common mirror plane z = 0: edge (2/3, s, 0)–(s/φ, 2/3, 0) of the envelope at 0 and its point reflection on the envelope at (R,R,0). Supporting plane x + y = R touches both (at one 5-fold corner each, 0.36 apart).
- On every cube face the two bite sections come this close: the 10-gon is two L-shaped lobes joined by a **diagonal strip 0.083 wide** (exactly the envelope gap). Beneath the strip G thickens inward with 72°-steep flanks (108° solid edges), so it is a narrow flat **ridge on the surface, not a thin wall**. This is inherent: any glue piece for the full envelopes must pass through these 12-per-cell gaps.
- Largest ball in G centred at the cube centre: radius 0.2205 (distance to the bites; cube faces are 0.539 away). G is a compact core (the tetartoid below, inradius s/2 = 0.206) with four arms to the octet-vertex corners.

### 2.3 The central cell is a tetartoid (exact)
- C26 := the cell of the 12 whole-rhombus planes of G's four bites containing the cube centre. The 4 tetrahedron faces are redundant (all 20 corners strictly inside T+), so this is exactly step 26's central cell: **12 pentagons, 20 corners, 30 edges, volume (−146 + 66√5)/27 = 0.058537 = 10.5 % of G**, centroid = cube centre. **C26 ⊂ G** (every point beyond all three rhombus planes of a bite is outside that envelope) — it is the intersection of the 12 "beyond the golden rhombus" half-spaces.
- Symmetry exactly **T** (12 proper, 0 improper of the 48 cube ops); edge lengths in three classes with multiplicities **12, 12, 6** — the tetartoid pattern (a = b would make it a pyritohedron). Lengths 0.15738 = R/φ⁴, 0.24218, 0.29935; pentagon edges in order (R/φ⁴, 0.242, 0.242, 0.299, R/φ⁴).
- Pentagon angles: **90°, 121.72°, 116.57° (golden obtuse), 63.43° (golden acute), 148.28°** — the right angle plus both golden-rhombus angles plus 90° ± 31.72°. Inradius s/2 = R/(2φ²), ψ 0.855.

## 3. Critical review of steps 21–27

**R1 — Step 27's proof is sound but incomplete as written.** Space filling rests on envelope disjointness (step 21) and the cube tiling — fine — but the README does not say that exactly four envelopes meet a cube and why (§1.1 step 3), and step 27b's chirality test checks only the 24 cube turns without the argument that nothing else could work (§1.2). Both are now supplied; no result changes.

**R2 — "Kit" is honest with one caveat.** The grown piece is one solid, no slivers, sharpest edge 90°, ψ 0.60 (comparable to the dented tetrahedron 0.62, better than every cap/middle piece of stages 1–3). The non-golden faces (square cuts) are **G–G interfaces, invisible in a full assembly**; every visible face of a complete cluster is an envelope face or a cut face on the outer boundary. Caveat: the 6 surface ridges of width 0.083 (§2.2) are a feature a stonemason will notice; they are forced by the envelope gap, not by the cube cut (the cube cut actually passes through the thinnest part of the hourglass between two envelopes, the best place to cut).

**R3 — Steps 22–25 (outer corners, wedges) have cusps and slivers.** The envelope touches each octahedron edge at exactly one point, the golden point dividing it 1 : φ (exact: supporting plane x + z = R meets RT in the single corner (s, 0, 2/3)). The closures of the "6 separate" outer corners therefore **meet pairwise at 12 points**, and at such a point the nearer corner piece has a solid angle of 0.75 sr while the farther one arrives as a **spike of 0.13 sr** (regular-tetrahedron corner: 0.55 sr). The step-24 wedges are these spikes: tiny (0.0055), tapering to a point, attached to the pyramid base through slivers of width 0 → s/φ² = 0.157. The refined envelope kit of step 25 is not buildable in its wedge part; the two-shape kit supersedes it, and the README should say so.

**R4 — Filing errors.** `data/step24-outer-corner.json` carries `pyramid_plus_below_equals_outer: false` because its piece filter let a fifth tetrahedron through (the README's two wedges = A + B are right). `data/step24b-wedge.json` reports `volume: 28/81 − 4√5/27 = 0.0144` for each wedge — that is the volume of the wedge's convex *hull* (`volume()` of a non-convex corner set); the true wedge is `mesh_volume` 0.005504. The step-26 "float description" of the central cell can be upgraded to exact (§2.3) and "tetartoid-like" to **tetartoid**.

**R5 — Wording.** "2 shapes (3 counting the mirror pair)" → "two shapes, one of them in a left and a right version". "Grown core" is apt: G really is the tetartoid grown outward until the cubes meet. The cube cut is a Voronoi cut (nearest tetrahedron centre), which the README could name.

**R6 — Step 26's "12 different shapes / 113 cells" was not re-derived here** (only the central cell); its reading — key planes are the wrong knife for the tetrahedra — is supported by the result that C26 is just 10 % of G.

## 4. Improvements (ranked), toward few / chunky / golden / buildable

**I1 — Centre the glue on the octet vertices instead of the tetrahedron centres (tested, exact).** The Voronoi cell of an octet vertex in the vertex lattice is the fcc **rhombic dodecahedron** (RD) of volume = cell, whose 6 four-valent corners are OCD centres and 8 three-valent corners are tetrahedron centres. **W := RD − its 6 envelope bites** (each exactly RT/6) has volume cell − RT = **(352 − 144√5)/27 = 1.111341 = 2 G**, is **one solid** (183 exact cells, one component), **achiral** (full m3̄ site symmetry: 12 proper + 12 improper cube ops), contains the φ⁻² vertex cuboctahedron, and the kit **envelope + W** fills space exactly once (same proof as §1.1 with RD cells; sampled 4 000 000 points, 0/0). **Two shapes, no left/right.** Trade-offs, exact: ψ 0.574 (G: 0.602) because the six bites are deep, but the core ball is larger (radius s = 0.412 vs 0.22 for G); faces = 12 RD rhombus parts (Kepler √2 rhombi, each with a 0.085 neck) + one full RT surface worth (6 whole golden rhombi, 24 cut rhombi, 24 triangles); 80 corners, 144 edges, 66 faces; dihedral angles 77.4° (24), 102.6° (24), 120° (24), 216° (72) — the 77.4° edges are sharper than anything on G. One glue piece per cell instead of two.

**I2 — Do not split G further.** G minus its four cuboctahedron corners (the step-25 idea applied to G) was tested on the node: one solid, ψ 0.609, but **12 knife edges of exactly 36°** (total length 5.8) where the RT faces leave the shared plane x = 2/3 — because the cuboctahedron's square face contains the RT rhombus in the same plane. Splitting off the tetartoid core C26 likewise leaves 12 thin wedge shells. Keep G whole (or W whole).

**I3 — Retire the refined envelope kit (steps 24–25) from the kit list** (R3); keep the φ⁻² facts (pyramid, cuboctahedron = ⅓ RT, shared rhombus faces) as geometry.

**I4 — Golden facts to state** (exact, new): envelope gap 2/(3φ³√(φ√5)) between facing parallel RT edges; the cube-face 10-gon angles 180° + 31.72° and 270° − 31.72°; the tetartoid core with angles 90°, 63.43°, 116.57°, 90° ± 31.72° and short edge R/φ⁴; G carries exactly 15 golden rhombi of surface, W exactly 30.

**I5 — For the periodic↔aperiodic story (Fable's reading, not a finding):** the kit is an fcc packing of golden zonohedra at exactly 10/φ⁶ with a chiral tetrahedral-site glue (or an achiral vertex-site glue). Whether a *golden* glue exists is still open: any glue must thread the 0.083 gaps, and the only golden planes available there are the RT's own, which gave the 113-cell fragmentation of step 26.

## 5. Open questions for DICTO
1. Two pieces as a mirror pair with ψ 0.60 (G, cube cut) — or one achiral piece with ψ 0.57 and a fatter core (W, rhombic-dodecahedron cut)? Both fill exactly.
2. Are the square / √2-rhombus cut faces acceptable given they are hidden inside any complete cluster?
3. Is a 0.083-wide surface ridge (6 on G, 12 on W) acceptable for a stone or printed piece? It cannot be removed without changing the envelope.
4. Record the central cell as a tetartoid (exact) and retire the wedge kit in the README?
