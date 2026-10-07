# Euclid–Kepler–Pacioli Cell Network (v2): symmetry and overlap checks

*Statement for the Zenodo record of the alternative version 2, by DICTO. Draft, 2026-10-07. Not yet released.*

## Summary

Version 2 of the Euclid–Kepler–Pacioli (EKP) network (DISCOVERIES.md #8, #8b). Every cube of a cubic lattice holds the same seven pieces: the cube, the regular dodecahedron, the regular icosahedron, the great stellated dodecahedron (the star), the octahedron, the stella octangula and Pacioli's golden rectangles. Odd cubes are turned a quarter (90°) about the vertical axis as a whole, so neighbouring cubes alternate. In the app this is the world **Euclid–Kepler–Pacioli Cell Network (v2)** (Wizard → 3D+). The first version, the Icosahedral/Dodecahedral Transitions world, is unchanged.

## Definition

- Cube (i, j, k) is centred at 2(i, j, k) with edge 2 (the roof-fold units of `src/geometry-extensions/roof-fold.js`).
- Even cubes (i + j + k even) are unturned. Odd cubes are turned 90° about z, with all their pieces.
- The contents of every cube are identical up to that turn.

## Results

Each result is produced by a script in `scripts/ekp-v2/`. The outputs of one run are in `scripts/ekp-v2/RESULTS.txt`.

1. **Symmetry.** The structure has 48 point operations, the full cube group. Half of them (24) exchange even and odd cubes, and the translations form the face-centred lattice of even-sum cube vectors. The operations cannot all be taken about one common point, so the group is non-symmorphic.
2. **Mechanism.** The 24 exchanging operations are exactly the 90°-rotated pyritohedral operations. The turn moves the icosahedral fivefold axes: none of the six fivefold lines of the icosahedron coincides with an unturned line, so odd cubes realign their icosahedral axes.
3. **Per solid.** The octahedron and the stella octangula are unchanged by the quarter turn. The dodecahedron, the icosahedron, the great star and the Pacioli rectangles are realigned, but their cube-symmetry subgroup of 24 operations is the same before and after. The shared symmetry of all six is 24 operations in both cases.
4. **Overlap, per lattice cube (volume 8).** Exact convex intersections give a total of 18.10, which is 226% of the cube's volume. The six faces of every cube carry the same overlap (6.03 per face contact). The largest contributions per lattice cube are dodecahedron with dodecahedron 6.47, cube with dodecahedron 3.24, dodecahedron with stella 1.24 and dodecahedron with great star 0.81. Cubes do not overlap one another, and there is no overlap at FCC neighbours or at corners. The star with star across a face gives 0.0077 per lattice cube.
5. **Merged outer surface.** The turned merged surface is closed: its enclosed volume is the same from two reference points, to within 10⁻¹². All 1945 faces point outward, and their windings agree with their normals. The enclosed volume is 274.25, which agrees with a Monte Carlo estimate of the union (272.99 ± 0.89 turned; 274.62 ± 0.89 unturned).

## Caveats

- The overlap values are exact convex intersections, cross-checked by Monte Carlo (dodecahedron with icosahedron: 0.04350 exact, 0.04378 Monte Carlo). Two earlier faults in the routine are fixed: touching-only intersections were counted as volume, and an edge-plane test accepted spurious vertices. The figures here come from the fixed code.
- The structure is not a tiling. The solids overlap by design, and the totals measure that overlap.
- The symmetry check holds the contents fixed and uses cube symmetries and cube translations. A cubic lattice admits no other point group.
- Pacioli's golden rectangles are planar, so they have no volume and are left out of the volume totals. They are included in the symmetry check.
- The star with star face overlap, 0.0026 per contact, is small but not zero.

## Reproduce

```
node scripts/ekp-v2/symmetry-seven.mjs
node scripts/ekp-v2/content-symmetry.mjs
node scripts/ekp-v2/contents-totals.mjs
node scripts/ekp-v2/merged-orientation.mjs
```

The Monte Carlo lines change slightly from run to run, because they use random samples.

## Relation to the existing record

- Version 1 is the Icosahedral/Dodecahedral Transitions world and the EKP cell and network findings (DISCOVERIES.md #8 and #8b).
- Concept DOI of the Kaleidohedra record: 10.5281/zenodo.23173809.
- Credit: DICTO (the artist name).

## Suggested Zenodo fields

- **Title:** Euclid–Kepler–Pacioli Cell Network (v2): symmetry and overlap checks
- **Version:** v2026.10.07-alt2 (proposed)
- **Description:** Alternative version 2 of the EKP network. Every cube holds the same seven pieces, and odd cubes are turned 90° about the vertical axis. The checks give 48 point operations (half of them exchanging even and odd cubes), a non-symmorphic space group on a face-centred lattice, and exact per-cube overlaps. The merged outer surface is closed, with outward normals.
- **Keywords:** Euclid–Kepler–Pacioli cell; icosahedral symmetry; space-filling; non-symmorphic symmetry; stellated dodecahedron; stella octangula
- **Related identifiers:** 10.5281/zenodo.23173809 (Kaleidohedra concept DOI)

## Comparison with the original EKP (symmetry)

Output: `scripts/ekp-v2/RESULTS-compare.txt` (`node scripts/ekp-v2/symmetry-compare.mjs`).

| | Original (identical, unturned) | Network (stars and icosahedra) | v2 |
|---|---|---|---|
| Point operations | 24 (m-3) | 24 (m-3) | 48 (m-3m) |
| Translations (cube vectors) | all integer (primitive) | even-sum (face-centred) | even-sum (face-centred) |
| Operations per 2×2×2 supercell | 192 | 96 | 192 |
| Fixed point common to all operations | yes | yes | no (non-symmorphic) |
| Operations exchanging even and odd cubes | 96 (odd translations) | 0 | 96 |

- v2 has the full cube group as its point symmetry. The original has its pyritohedral subgroup.
- The total per supercell is the same (192): the symmetry moves from translations into point operations.
- The reflections of v2 include glide translations of quarter-cell size, which suggests diamond-type glides. The space-group symbol needs checking against the International Tables before publication.

## Roof construction

Against the roof construction, v1 matches more directly: its cells repeat by translation alone, as Euclid's roofs do on the cube. In v2 the odd cells are turned copies.
