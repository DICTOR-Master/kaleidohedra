# Lean study 3 of the shape-language canon: Dehn's theorem, end to end (19 November 2026)

**Question (DICTO's canon, continued from studies 1 and 2):** study 1 proved the arithmetic of the Dehn invariant, study 2 proved the bridge (cutting and regluing keeps the invariant) and left three evaluation gaps, each a stated theorem with `sorry`. Close them, so that Dehn's theorem compiles with no `sorry`.

**Result:** all three gaps are closed. Dehn's theorem compiles in Lean v4.35.0-rc2 with the pinned Mathlib: no errors, no warnings, no `sorry` in any file of its dependency chain, and only the three standard axioms (`compile.log`).

```lean
theorem tetra_not_scissorsCongruent_cube (s : ℝ) (hs : 0 < s) :
    ¬ ScissorsCongruent tetraSet (cubeSet s)
```

The regular tetrahedron with corners (−1,−1,−1), (1,1,−1), (1,−1,1), (−1,1,1) cannot be cut into finitely many convex polytopes that, moved by isometries of space, fill the cube [−s, s]³, for any s > 0.

## Proved in Lean (two new files, 901 lines; theorem names, statements)
File `lean/Dehn3Sector.lean` (gap 1):
1. `volume_sector`: for 0 < β < π/2, the sector of the open unit disc of the complex plane between the directions −β and β has area β.
2. `wedgeAngle_two_planes` (**gap 1**, same statement as in study 2): in 3-space, for two half-spaces with outward normals a₁, a₂ (linearly independent), `wedgeAngle (cone ![a₁, a₂] univ) (linCone ![a₁, a₂] univ) = π − angle a₁ a₂`. The angle that study 2 measures by area is the usual dihedral angle.
3. `finrank_linCone_pair`: the two planes meet in a line.

File `lean/Dehn3Solids.lean` (gaps 2 and 3, and the theorem):
4. `theta_pair`: at a point of a polytope where exactly two constraints i, j are tight (normals independent), the angle class is π − angle(aᵢ, aⱼ) modulo ℚπ.
5. `pair_of_finrank_one`: if the tight constraints at a point have a line as common direction space, and any three tight normals have no common perpendicular direction, then exactly two constraints are tight.
6. `edgeAngle_cube`, `dehnSet_cube` (**gap 2**): every point of the cube [−s, s]³ (s > 0) has angle class 0, so `dehnSet (cubeSet s) = 0`.
7. `tet_openSegment_iff`: for corners k ≠ l of the tetrahedron, the open segment between them is exactly the set of points of the solid where the two faces other than k, l are tight and no other.
8. `tet_theta`: where two faces of the tetrahedron meet the angle class is that of arccos(1/3). `tet_edge_length`: each open edge has 1-dimensional Hausdorff measure 2√2. `tetra_edge_set`, `tetra_edge_measure`: the points with angle class arccos(1/3) are the six open edges, total length 6 · 2√2.
9. `dehnSet_tetra` (**gap 3**, same statement as in study 2): `dehnSet tetraSet = dehn (tetrahedron (2 * √2))`, study 1's edge-list value.
10. `tetra_not_scissorsCongruent_cube` (**Dehn's theorem**), from 6 and 9, study 2's bridge `not_scissorsCongruent_of_dehnSet_ne` and study 1's `dehn_tetrahedron_ne_zero` (Niven's theorem).

## Method
- **Gap 1, by polar coordinates.** Of the routes considered (polar coordinates; additivity + rotation invariance + known values), polar coordinates was the cheapest in Lean: Mathlib already has the change of variables and the area of the disc, so the sector area is one integral over a rectangle; the additivity route would still have needed a proof that an additive monotone angle function is linear, and gives nothing for an angle like arccos(1/3) without it. Steps: the plane perpendicular to the edge gets the orthonormal pair e₁ = −(u₁+u₂)/‖u₁+u₂‖, e₂ = (u₁−u₂)/‖u₁−u₂‖ (u₁, u₂ the unit normals), so the wedge is symmetric about e₁ and no angle wraps around; `Complex.isometryOfOrthonormal` carries that plane onto ℂ, and linear isometries keep area (`LinearIsometryEquiv.measurePreserving`); the wedge becomes the sector with sin β = ‖u₁+u₂‖/2, cos β = ‖u₁−u₂‖/2; its area is β by `Complex.lintegral_comp_polarCoord_symm` and `MeasureTheory.lintegral_prod_mul`; the disc has area π (`Complex.volume_ball`); and π − angle(u₁, u₂) = 2β by `Real.arccos_cos`.
- **Gap 2.** Done with gap 1 rather than the quadrant shortcut, because the general lemma `theta_pair` was needed for the tetrahedron anyway and then gives the cube in a few lines: two tight faces of the cube have perpendicular normals, the angle is π − π/2, a rational multiple of π.
- **Gap 3.** Directly from the definition of `dehnSet` (lemma `dehnSet_eq_single`: one angle class besides 0), not through the edge list of study 2. In the coordinates h_m(x) = ⟨n_m, x⟩ of the four face normals (they sum to 0, Gram matrix 3 on the diagonal and −1 off it) every step is uniform in the corners, so there is no case-by-case work over the six edges; the finite facts about Fin 3 and Fin 4 are by `decide`. Lengths: `MeasureTheory.hausdorffMeasure_segment`.

## Credits (borrowed lemmas, at the point of use in the files)
Mathlib: `Complex.lintegral_comp_polarCoord_symm`, `Complex.polarCoord_symm_apply`, `Complex.volume_ball`, `Complex.isometryOfOrthonormal`, `LinearIsometryEquiv.measurePreserving`, `MeasureTheory.lintegral_prod_mul`, `integral_id`, `Real.arccos_cos`, `InnerProductGeometry.angle` and `inner_eq_zero_iff_angle_eq_pi_div_two`, `MeasureTheory.hausdorffMeasure_segment`, `Submodule.finrank_add_finrank_orthogonal`, `finrank_span_eq_card`; Niven's theorem through study 1. Mathematics: Dehn (1901); Jessen's tensor form. FormalBook ch. 10 (github mo271/FormalBook, PR #157): not used in this study.

## Sources checked
- Pinned Mathlib (grep for "sector", "polarCoord", "hausdorffMeasure_segment", segment closedness): polar coordinates, disc area and segment length are there; an area-of-a-sector statement was not found; a closedness lemma for `segment` was not found by name (proved here from `segment_eq_image`).
- Prior Lean work on Dehn's theorem: as listed in study 2's README (FormalBook PR #157 proves Hilbert's third problem in an abstract segment-and-angle model and states that it does not bridge geometric decompositions to that model). No new web search was made in this study. A machine-checked proof of Dehn's theorem for actual subsets of 3-space, from a set-level definition of the invariant: not found in the sources checked in study 2.

## `#print axioms` (from `compile.log`)
```
'DehnCanon.volume_sector' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.wedgeAngle_two_planes' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.theta_pair' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.dehnSet_cube' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.tet_openSegment_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.dehnSet_tetra' depends on axioms: [propext, Classical.choice, Quot.sound]
'DehnCanon.tetra_not_scissorsCongruent_cube' depends on axioms: [propext, Classical.choice, Quot.sound]
```
No `native_decide`, no added axioms. `grep sorry` over the eleven files of the chain finds only the header lines that say "No `sorry`".

## Limits of what is stated
Dimension 3. Pieces are convex polytopes (bounded intersections of finitely many closed half-spaces), finitely many, interiors pairwise disjoint; they are moved by isometries, reflections included. The tetrahedron is the one with the corners above (edge 2√2); other sizes and positions follow by similarity but are not stated here. The cube is [−s, s]³, every s > 0.

## Files and how to compile
`lean/Dehn3Sector.lean` (part I), `lean/Dehn3Solids.lean` (part J), `lean/Axioms3.lean`, `lean/compile_all.sh`, `compile.log`.
The files import study 2 (`DehnCanon.Dehn2R3` and what it imports) and study 1 unchanged; no file of studies 1 and 2 was edited or copied. Study 2's `DehnCanon2Gaps.lean` is not imported: its three `sorry` statements are now the theorems of the same names in this study, so it is superseded.
Compiled in the Lean workspace of studies 1 and 2, all files in the folder `DehnCanon/`, by `bash DehnCanon/compile_all.sh` from the workspace root: it compiles the eleven files of the chain in dependency order (study 1, study 2, study 3; 46 s in all), prints the axioms and greps for `sorry`. The files on the compute host and the copies here have the same SHA-256.

## Leads
- Delete study 2's `DehnCanon2Gaps.lean` (superseded) when the three studies are merged into one Lean folder for publication.
- State the theorem for every regular tetrahedron and every cube (any size, any position): `dehnSet_image` gives positions; sizes need a short scaling lemma for `dehnSet`.
- `theta_pair` + `pair_of_finrank_one` + `dehnSet_eq_single` evaluate any polytope whose edges all have one angle class; a version for several angle classes (through `dehnSet_eq_dehn_edgeList`) would give the octahedron, the rhombic dodecahedron (zero) and the other canon solids.
- Then our words (AXE, CLEO, FUJI: two independent angles, beyond Niven), as planned in study 1.
- Non-convex pieces: study 2's `dehnSum_eq_of_scissors` covers unions; a statement of Dehn's theorem with polyhedral pieces that need not be convex would combine it with this study.
- The sector-area lemma `volume_sector` and the two-plane angle `wedgeAngle_two_planes` are general and could be offered to Mathlib in a cleaned form.
