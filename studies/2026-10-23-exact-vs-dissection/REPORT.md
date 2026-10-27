# Exact vs cut-and-glue: the study

*DICTO's idea (2026-10-22); exact computation with Claude (Anthropic), 2026-10-23. DICTO · dictospheres.com*

The books describe several classical space-fillers by cutting and gluing: shave a belt off one solid, stick pyramids onto another, glue rhombohedra together. Kaleidohedra makes the same solids in one go, by moving the lattice: a shear (the six sliders), the Cell slider, and a stretch along one extra direction. Fedorov (1885) already named the moves (shear and stretch, Theorem 32, p. 239; shrinking a belt, § 83, p. 234). What this study adds: exact corners, exact slider values and exact checks, for five shapes. It complements the classical descriptions and does not correct them.

## Files

- `data/*.json`: one file per shape (the ED file holds the whole family). Each has exact and decimal corners, faces, the move in a form you can replay (`move_exact`), the lattice, the classical constructions (`classical_exact`), the published values compared (`expected`), credits and checks.
- `exact.py`: exact arithmetic in Q(√2), Q(√3) and Q(√5). Nothing is decided by floating point.
- `build.py` builds everything (93 of 93 build checks pass). `check.py` re-checks everything from the JSON alone. It prints **223 of 223 checks pass; corrupted copies caught: 54 of 54**. Six kinds of corruption are made in each of 9 solids. The run was on dicto-node; output is in `check.log`.
- `app_crosscheck.mjs`: the app's own krp-core code (pinned e5e5dbc), set to these slider values, gives the same cells: 12 of 12 (`app_crosscheck.log`).
- `renders/*.png`: each solid beside its classical construction, in the Targets-world colours: squares blue, rhombi pink, regular hexagons gold, other hexagons purple. Classical pieces are gold or purple.

What the checks cover, for every solid:
- it is closed, wound outward, has flat faces, is convex, and satisfies Euler's formula;
- its f-vector, faces, edges, symmetry and exact volume;
- the move, replayed from its parameters, gives exactly these corners;
- it tiles space: volume = |det| of the lattice, no lattice vector inside P − P (so no overlaps), and every face neighbour is a lattice vector;
- it is congruent to the classical construction by corner matching;
- the classical pieces really glue into one convex solid: they are disjoint, they lie inside it, and their volumes add up.

The corner-matching test rejects a known counterexample. Two point sets (homometric) have the same sorted distance list but are not congruent, and the test tells them apart.

## Per shape

**1. Regular-hexagon elongated dodecahedron (F5).**
- Move: Towards Bain, stop 2 (shear A = diag(1, 1, √2); sliders a = 1, b = c = √(3/2), cos α = 2/3, cos β = cos γ = 1/√6). Then Cell = 1, which adds nothing here because the four edges are already equal. Then stretch along u = h₁ + h₂ = (1, 0, 0), length s = 1.
- Solid: 18 corners, 28 edges, 12 faces (Fedorov's counts). Faces: 4 regular hexagons, 4 squares, 4 rhombi of 60° (Grünbaum Fig. 2(b)). Symmetry D2h.
- Volume **4√2** at edge 1. This confirms the library check and TARGETS (5.65685).
- Classical: congruent to the uniform truncated octahedron with any one of its six zones shrunk to zero (Fedorov § 83; Wikipedia's "contraction"). Shrinking its fifth zone gives back the Bain RD.

**2. Bain rhombic dodecahedron (#4).**
- Move: the same Bain stop, Cell = 1, no stretch.
- Solid: 14 corners, 24 edges, 12 faces: 4 squares and 8 rhombi of 60°. Symmetry D4h. Volume **2√2**.
- Classical: congruent to the cuboctahedron with two equilateral square pyramids (the glue checked exactly: 5√2/3 + 2·√2/6). Also congruent to the truncated octahedron with a perpendicular pair of zones shrunk (Fedorov § 83). Shrinking a 60° pair instead gives a hexagonal prism.

**3. The elongated dodecahedron as a type.**
- The family, proved: an RD-type cell Z(h₁…h₄) has a dependency Σ μᵢhᵢ = 0 with all μᵢ > 0. It has exactly three free directions, u = μᵢhᵢ + μⱼhⱼ, one for each way of splitting the four edges into two pairs. Z(h, s·u) is an elongated dodecahedron for every s > 0. Any other direction leaves a belt of 8 faces, so that cell cannot tile.
- The parameters are: the six sliders, Cell, the pair split, and the stretch s.
- Classical equilateral ED (regular RD + square prism): plain FCC, Cell = 1, u = (1, 0, 0), s = the RD edge.
  - Faces: 8 rhombi of 70.53° and 4 equilateral hexagons with corners 125.26°/125.26°/109.47°. Symmetry D4h.
  - Volume at edge 1: **8/3 + 16√3/9 ≈ 5.7459**.
  - Congruent to Polyhedraverse's `elongatedDodecahedronVerts`. The "RD halves capping a square prism" glue checks exactly.
- Bain RD, other free line (z): TARGETS #23. Volume 2 + 2√2.
- F7: DICTO FCC stop 2, Cell = 1. DICTO's RD has μ = (φ, φ, 1, 1).
  - Free line 12|34 gives ED **#16**: volume φ² + 2, symmetry C2h.
  - Free line 14|23 gives ED **#18**: volume φ³ + ½, symmetry C2h.
  - Both lie on icosahedral two-fold (blue) axes. The third free line, 13|24, is not a blue axis (angles 37.76° and 82.24°). This is why there are exactly two, as in F7.
  - The app's `DICTO_SKEWED_ED_16/18` match.

**4. Bilinski dodecahedron: the move works.**
- Move: plain FCC sliders with **only γ moved from 60° to 36°** (a = b = c, α = β = 60°, cos γ = φ/2), then **Cell = 1**. The app's own code gives B, and 36.0° is on the slider grid. "Shear FCC, then Cell = 1" is therefore right.
- Cell = 1 is essential. At Cell = 0 the same shear gives an affine image of Kepler's RD, which is not B. B's dependency is (φ, φ, 1, 1), not 1:1:1:1, so B is not an affine image of Kepler's K. This agrees with Grünbaum p. 6.
- Solid: 12 golden rhombi (cos² = 1/5), edges² = φ + 2. Symmetry D2h.
- Volume 8 + 4√5 = 4φ³. At edge 1 this is **(4/5)√(5 + 2√5) ≈ 2.4621**.
- Classical:
  - Congruent to the triacontahedron with any two of its six zones deleted, for all 15 pairs (Grünbaum Fig. 4).
  - Glued exactly from **2 acute + 2 obtuse golden rhombohedra**, in two ways. The acute pieces have volume 2φ² each and the obtuse pieces 2φ each, both congruent to Grünbaum's Ha and Ho. Hafner–Zitko give no count; this supplies it.

**5. 60° rhombohedron (worked example).**
- Move: shear the cube lattice so that the edges meet at 60°. The result is the FCC lattice itself, and the solid is the app's FCC_BASIS parallelepiped.
- Solid: 8 corners, 12 edges, 6 faces, all rhombi of 60°. Symmetry D3d. Volume **1/√2**.
- Classical: congruent to Maurolico's tetrahedron + octahedron + tetrahedron (the glue checked exactly).

## Something found on the way

**DICTO's skewed RD (F1) is an exact linear image of Bilinski's dodecahedron.** Both have the dependency (φ, φ, 1, 1). The stored linear map carries B's 14 corners exactly onto F1's. This is stated in check.py and passes.
- It does not change F1's status: F1 is a different, non-congruent member.
- It does make "nearest known relative: Bilinski" in DISCOVERIES #1 more precise: same affine class, different shape.
- Not literature-checked.

## Disagreements with published values (reported, nothing changed)

1. **Wikipedia, "Elongated dodecahedron"** (read 2026-10-23) gives V = 6a³ and does not define a. At edge 1 the classical ED has volume 5.7459 and the regular-hexagon ED 4√2 ≈ 5.6569; neither is 6. Its "slicing into two halves … square prism" sentence fits the classical ED. For the regular-hexagon ED the inserted prism is rhombic (70.53°), which is checked exactly. The library check's row puts both descriptions under the regular-hexagon ED.
2. **DISCOVERIES #7 (our own, archived)** labels the hexagons of ED #16 as "36°/36°/72° corners" and those of #18 as "36°/72°/72° corners". Those are the angles between edge directions. The actual corners are 144/144/72 and 144/108/108, as TARGETS has them. This is wording only; the faces and volumes are right.

## Open questions for DICTO

1. Should the F1 = affine image of B observation go into the paper (or into a DISCOVERIES #1 note)?
2. Should DISCOVERIES #7's "corners" wording be fixed in the next version?
3. The fifth direction is not a live slider. It is computed in krp-core and shown in the Targets world. Should the app get a Stretch slider so all three moves are live? This is outside this study.
4. How to cite Wikipedia's 6a³: mention it, or leave it out?
5. Still unread, so their numbers are not compared: Bilinski 1960 (B's volume and coordinates) and the first describer of the Bain RD.
