# Fable review 3 — OCD + W_OCD and OCD + W_star — 2026-10-18

DICTO · dictospheres.com — independent exact verification and critical review (Claude Fable 5.1) of `studies/2026-10-18-p4-golden-octet-adaptor` steps 6–7: glue pieces with exact OCD imprints, centred on the octet vertices (W_OCD) and on the octahedron-edge midpoints / Penrose stars (W_star). Research branch only.

Scripts: `scripts/fable3_exact.py` (W_OCD, exact Q(√5), Pi 127 s), `scripts/fable3_star_exact.py` (W_star, exact, Pi 49 s), `scripts/fable3_exact_lib.py` + `fable3_engine.py` (the engine of the earlier reviews, unchanged), `scripts/fable3_node.py` (dicto-node: manifold3d meshes, dihedral histograms, W_star thickness map, 8 000 000 sample points). Data: `data/fable3-exact.json`, `data/fable3-star-exact.json`, `data/fable3-node.json`, logs, `data/fable3-input.json`. Exactness rules as in the earlier reviews. Scale for buildability: 60 mm octahedron edge ⇒ 1 unit = 39.33 mm (R = 42.4 mm).

## 1. Verdicts

| Claim | Verdict |
|---|---|
| **OCD + W_OCD fills space exactly once** | **PROVED EXACTLY** (§2); 2 000 000 uniform + 2 000 000 near-face points: 0 uncovered, 0 double |
| W_OCD volume (2824 − 328√5)/1539 = cell − OCD, one solid, genus 0, centrosymmetric, ψ 0.648 | **PROVED EXACTLY** (symmetry group exactly m3̄, order 24, nothing more) |
| **OCD + W_star fills space exactly once** | **PROVED EXACTLY** (§3); 2 000 000 + 2 000 000 points: 0 / 0 |
| W_star volume (1412 − 164√5)/4617 = (cell − OCD)/6, one solid, genus 0, centrosymmetric, ψ 0.690, 97.7 % of the middle piece inside | **PROVED EXACTLY** (symmetry group exactly 2/m, order 4; middle-piece share exactly (−1058 + 634√5)/4617 ÷ (310 + 26√5)/4617 = 0.97699) |
| The three Penrose cores (central + 2 flanks, step 19) lie wholly inside one W_star | **PROVED EXACTLY** (each core's volume inside the cell equals the core, to the last digit of Q(√5)) |

Facts about the OCD used below (exact): 102 corners — 90 at radius exactly 2/3 (the RT inradius) and 12 star centres at radius 0.6952; 80 faces = 60 quadrilaterals (area 0.04146) + 20 hexagons (area 0.14702, all equal); dihedral angles 156.20° (120 edges) and 156.72° (60); symmetry group exactly Th = m3̄ (12 + 12 of the 48 cube operations); OCD ⊂ octahedron with 48 corners on its faces, strictly inside every edge plane (max x + z = 0.9569 < R); inradius = octahedron inradius R/√3 = 0.6228 (the 8 joint hexagons are the nearest faces). The star centres are **not** on the 2-fold axes (example (0, −0.591, 0.365)), so facing stars face each other only through the inversion in the edge midpoint.

## 2. OCD + W_OCD (vertex-centred glue)

**Tiling, exact.** The Voronoi cell of the octet vertex v0 = (0,0,R) in the vertex lattice is the fcc rhombic dodecahedron RD (volume = cell; 4-valent corners = the 6 OCD centres at distance R, 3-valent corners = the 8 tetrahedron centres). Every OCD centre within reach was tested: **exactly the 6 at distance R meet the RD**, each bite = OCD ∩ (the RD's corner cone) = **OCD/6 = (−500 + 620√5)/4617 = 0.191978** (= the step-2 cap region), and the 6 vertex RDs round one OCD take exactly the whole OCD. So vol W_OCD = cell − OCD = **(2824 − 328√5)/1539 = 1.358395** as claimed; RDs tile space, OCDs are disjoint ⇒ once-and-only-once.

**Solid, symmetry.** Exact convex decomposition: 407 cells summing to vol W_OCD, one adjacency component. Of the 48 cube operations about v0 exactly 24 (12 proper + 12 improper, incl. the inversion) preserve the RD and the six OCD sockets: **Sym = m3̄, achiral, no extra symmetry** (none is possible: the OCD itself has exactly Th).

**Faces (exact).** 132 faces, 206 corners, 336 edges (V − E + F = 2; mesh agrees).
- **120 imprint faces = exactly one whole OCD surface** (area 5.4281): per socket 6 whole quadrilaterals, 2 whole hexagons, 8 cut quadrilaterals (4 corners) and 4 cut hexagons (pentagons = exact thirds of the joint hexagons: the RD's edge through the socket runs along the 3-fold axis and exits the OCD at the joint-hexagon centre, 2/3 of the way to the tetrahedron centre, so the three W's round a joint hexagon each take a third).
- **12 RD-face parts**: each Kepler rhombus (area 0.8228) minus two hexagonal OCD sections, part area 0.3103, the two sections separated by a **neck of exactly √(820/3 − 1100√5/9) = 0.19009 = 7.48 mm**.
- Surface 9.1522, **ψ = 0.6481** (claim confirmed; OCD 0.979, RD 0.905).
- **Dihedral angles (exact):** 86.88° (24 edges), 90° (48), 93.12° (24), 120° (24, RD edges), 203.28° (72) and 203.80° (144) reflex (the OCD's own edges seen from outside). **Sharpest 86.9°; no knife edge, no sliver.**

**Thin places.** Two neighbouring sockets in one W come no closer than the OCD–OCD gap: **exactly √(70/81 − 10√5/27) = 0.18980 = 7.47 mm** (attained in the common mirror plane of the two OCDs, off the RD face; the facing star centres are 0.363 apart, so the five-fold stars are not the closest features). The RD-face necks (7.48 mm) are surface ridges on the W–W interfaces, thickening inward at the OCD's face angles. Largest ball at the vertex: radius exactly R − 2/3 = R/φ² = 0.4120 = **16.2 mm** (the OCD's 2-fold points face the vertex). Overall size at 60 mm edge: 73.5 mm between opposite tetrahedron-site corners, RD edge 36.7 mm; OCD outer diameter 54.7 mm.

## 3. OCD + W_star (edge-midpoint / Penrose-star glue)

**Cell, exact.** The Voronoi cell of m = (0, R/2, R/2) among all edge midpoints (R/2)(a,b,c), exactly two odd, is the **octahedron with corners 0, (0,R,R) [OCD centres], (0,R,0), (0,0,R) [edge ends], (±R/2, R/2, R/2) [tetrahedron centres]**, volume (16 + 8√5)/81 = cell/6, 8 triangular faces **each passing through an OCD centre**. Exactly the 2 OCDs at the edge ends meet it, each bite **OCD/12 = (−250 + 310√5)/4617**; the 12 edge-midpoint cells round one OCD (rotated copies, not translates) take exactly the whole OCD. vol W_star = **(1412 − 164√5)/4617 = 0.226399** as claimed. Cells tile, OCDs disjoint ⇒ once-and-only-once.

**Solid, symmetry.** 91 exact cells, one component. Exactly 4 of the 48 operations about m preserve it: identity, inversion through m, the 2-fold turn about the x-axis through m, the mirror x = 0 — **Sym = 2/m (the Fm3̄ site symmetry of 24d), achiral, centrosymmetric** as claimed.

**Faces (exact).** 32 faces, 44 corners, 74 edges (Euler 2). **24 imprint faces = exactly one sixth of an OCD surface**: 6 whole quadrilaterals, 4 + 4 cut quadrilaterals (3 and 5 corners), 4 + 4 + 2 cut hexagons (3, 5, 6 corners); 8 cut-face parts (each cell triangle minus one OCD section, area 0.2124). Surface 2.6041, **ψ = 0.6898** (claim confirmed — the highest glue ψ so far). Dihedrals: 75.39° (4 cell edges, length 0.302), 86.88° (4), 90° (12), 93.12° (4), 104.61° (4), 120° (8), 203.28° (10), 203.80° (28). **Sharpest 75.4°, no knife edge.**

**Thin places — the one real issue.** The two OCDs stay on their own sides of the mid-plane y + z = R by exactly (R − 0.95686)/√2 = 0.0861 each (3.4 mm), so **W_star is a lens 60 mm across (edge end to edge end) × 42.4 mm (tetrahedron centre to centre) whose centre is only 0.1901 = 7.5 mm thick** (OCD surface to OCD surface along the edge axis; largest ball at m: radius 3.7 mm). Thickness along the axis grows with the distance ρ from it (node, exact planes): 7.5 mm at ρ = 0, 7.7–8.4 mm at ρ = 3.9 mm, 10.4–11.3 mm at ρ = 7.9 mm, 14.1–16.7 mm at ρ = 11.8 mm. The 7.5 mm waist is exactly where the Penrose cores sit.

**Penrose (exact).** H = hull of the two facing stars (volume 4√5/81); M0 = H − OCD₁ − OCD₂ = (310 + 26√5)/4617 (= step 19); **inside W_star: (−1058 + 634√5)/4617 = 0.077901 = 97.699 %** of M0 — 4 of H's 10 corners (star tips) lie outside the cell, which is where the 2.3 % goes. **The central core (−36734 + 16658√5)/50787 and both flank cores 4114/1539 − 9182√5/7695 lie wholly inside W_star** (exact equality of the in-cell volumes). So the statement "the Penrose link lives in the star piece" is exact for the three cores, approximate (97.7 %) for the whole middle piece.

## 4. Comparison for DICTO (both kits are exact; both pieces are achiral; both sockets are exact OCD imprints)

| | OCD + W_OCD | OCD + W_star |
|---|---|---|
| glue pieces per OCD (per cell) | 1 | 6 (12 round each OCD, 2 OCDs per piece) |
| symmetry of the glue | m3̄ (order 24) | 2/m (order 4) |
| volume | 1.3584 (54.1 % of space) | 0.2264 each (54.1 % together) |
| ψ | 0.648 | 0.690 |
| size at 60 mm edge | 73.5 mm across, RD edge 36.7 mm | lens 60 × 42 mm |
| thinnest place | 7.5 mm ridges on the 12 W–W faces; 7.5 mm between sockets; core ball 16 mm | **7.5 mm waist at the centre** (core ball 3.7 mm), thickening outward |
| sharpest edge | 86.9° | 75.4° |
| faces / corners | 132 / 206 (one full OCD surface in 6 sockets) | 32 / 44 (one sixth of an OCD surface in 2 half-sockets) |
| Penrose cores | cut between pieces | **all three wholly inside one piece** |

**Reading.** W_OCD is the stronger building block (thick everywhere, one piece per cell, 6 full sockets), but a complex object (132 faces). W_star is the simpler and more spherical piece and carries the Penrose link intact, at the price of a 7.5 mm waist and 6 pieces per cell; each W_star touches 8 neighbours (W_star–W_star contacts through the cell triangles minus sockets) and locks two OCDs. For a 60 mm print both are fine (7.5 mm minimum features, no edge below 75°); in stone W_star's waist is the weak spot and W_OCD's necks are only surface ridges.

## 5. Review points and improvements
- **R1 (p4 README):** both volume, solidity, symmetry and ψ claims are right; "centrosymmetric" can be sharpened to the exact groups m3̄ and 2/m. "Contains 97.7 % of the middle piece" is exact; add that the three cores are wholly inside.
- **R2:** the facing five-fold stars are **not** the closest approach of two OCDs (0.363 apart); the true gap 0.1898 is between other faces in the mirror plane of the pair. Any text saying the stars "almost touch" should say the OCD surfaces come within 7.5 mm (at 60 mm edge) near the edge midpoint.
- **I1 — If the waist matters, W_OCD is the answer, not a modified W_star:** the waist is fixed by the two OCD surfaces 0.19 apart; no cut can thicken it. A compromise with fewer pieces than W_star and smaller than W_OCD would be the **tetrahedron-site glue with OCD imprints** (cube of edge R minus 4 OCDs, the OCD analogue of the earlier grown piece G: chiral pair, 2 per cell) — not tested here.
- **I2 — Naming:** W_OCD = "vertex adaptor" (sockets for 6 OCDs), W_star = "edge link" (holds 2 OCDs and the Penrose cores). Both kits are two-shape kits with a single achiral glue.
- **I3 — Record exact facts:** OCD has 90 corners at radius exactly 2/3 and 12 at 0.6952; the vertex-to-OCD distance is R − 2/3 = R/φ²; the RD edge exits the OCD exactly at the joint-hexagon centre (2/3 of the way); W_OCD's hexagon imprints are exact thirds of the joint hexagons.

## 6. Open questions for DICTO
1. One big adaptor per cell (W_OCD, 7.5 mm ridges, 16 mm core) or six small links (W_star, 7.5 mm waist, Penrose cores inside)?
2. Is a 7.5 mm waist in a 60 mm lens acceptable for the intended material?
3. Should the chiral tetrahedron-site variant (cube − 4 OCDs) be tested as the middle option?
