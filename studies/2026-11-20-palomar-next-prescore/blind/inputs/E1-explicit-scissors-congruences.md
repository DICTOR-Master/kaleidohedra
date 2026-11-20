# Candidate E1: explicit scissors congruences to a cube for a family of zero-invariant solids (a proposed Lean entry)

## Abstract (neutral)

Two solids are scissors congruent when one can be cut into finitely many polyhedral pieces that, moved by isometries, fill the other. By Dehn (1901) and Sydler (1965), two polyhedra in ℝ³ are scissors congruent if and only if they have the same volume and the same Dehn invariant (Σ length ⊗ dihedral angle in ℝ ⊗_ℚ (ℝ/ℚπ), in Jessen's form). So every polyhedron with Dehn invariant zero is scissors congruent to a cube of the same volume; Sydler's proof (and Jessen's simplification) is not constructive in a way that gives the pieces. Debrunner (1980) proved that every polyhedron that tiles space by congruent copies has Dehn invariant zero and is scissors congruent to a cube.

The proposed entry builds on a registered Palomar entry, **PALOMAR-2026-11-20-000003, the Dehn invariant read from the solid, with the bridge from convex dissections**. That entry defines the Dehn invariant of a subset of a 3-dimensional real inner product space from the set itself (wedge angles from cones of directions, 1-dimensional Hausdorff measure of the edge points), proves it equals the classical edge sum for convex polytopes, and proves the bridge "scissors-congruent convex polytopes (and finite unions of convex polytopes) have equal invariant", with Hilbert's third problem for point sets and Dehn's theorem for the tetrahedron and the cube. Its `ScissorsCongruent P Q` is: P is a finite union of convex polytopes with pairwise disjoint interiors, each moved by an affine isometry, and the moved pieces fill Q with pairwise disjoint interiors.

The proposed entry proves the other direction, Sydler's, for one explicit family, by exhibiting the pieces. For each solid P below, with exact coordinates, it proves in Lean 4 / Mathlib

    ScissorsCongruent P (cube of side (volume P)^(1/3))

with every piece given by exact vertex coordinates (in ℚ(√2, √3, √5) and the cube root of the volume) and every isometry given exactly, so the dissection is fully explicit and checked by the kernel. The solids:

1. the rhombic dodecahedron;
2. the truncated octahedron;
3. both golden rhombohedra (prolate and oblate);
4. the intersections of a cube with a concentric rhombic dodecahedron (a one-parameter family; every dihedral angle is 90°, 120° or 135°, so the Dehn invariant is zero for every member);
5. the nine "most regular" space-fillers: the equal-edged space-filling zonohedra whose faces are squares, regular hexagons and 60° rhombi. These are four parallelepipeds, two hexagonal prisms, the Bain rhombic dodecahedron, the elongated dodecahedron with regular hexagons, and the truncated octahedron (counted again here as a member of the nine).

Route (planned): (i) each solid to a rectangular box of the same volume by explicit cuts (for the parallelohedra, cutting along the lattice translates of a fundamental parallelepiped and shearing it by cut-and-translate; for the cube ∩ rhombic dodecahedron solids, explicit pyramid and prism rearrangements); (ii) the box to a cube of the same volume by the classical rectangle-to-square dissection of the plane (as in the Wallace–Bolyai–Gerwien theorem), extruded and applied in two directions. Each step is a finite list of convex pieces and isometries; the Lean proof checks the cover, the disjoint interiors and the images. With the registered entry's bridge, each such theorem is a machine-checked instance of the equality of Dehn invariants with the cube's (zero).

Limits stated by the submitter: the general Dehn–Sydler theorem is not proved; only the listed solids are covered; the piece counts are not claimed minimal; the individual dissections are classical or follow from Sydler's theorem or Debrunner (1980); several are in the recreational dissection literature (rhombic dodecahedron into two cubes; truncated octahedron to a cube in 11–12 pieces by Hanegraaf and Theobald). What is claimed new is that the explicit dissections for this family are machine-checked.

Facts on the proof: not yet built. The statements below are the ones to be proved; they would reuse the registered entry's definitions verbatim (`IsPoly`, `ScissorsCongruent`, Lebesgue volume on `EuclideanSpace ℝ (Fin 3)`).

## Sources (exact citations)

- **M. Dehn**, "Über den Rauminhalt", *Math. Ann.* 55 (1901) 465–478.
- **J.-P. Sydler**, "Conditions nécessaires et suffisantes pour l'équivalence des polyèdres de l'espace euclidien à trois dimensions", *Comment. Math. Helv.* 40 (1965) 43–80.
- **B. Jessen**, "The algebra of polyhedra and the Dehn–Sydler theorem", *Math. Scand.* 22 (1968) 241–256.
- **H. E. Debrunner**, "Über Zerlegungsgleichheit von Pflasterpolyedern mit Würfeln", *Arch. Math.* 35 (1980) 583–587: space-filling polyhedra are scissors congruent to a cube (read through citations only).
- **J. C. Lagarias, D. Moews**, "Polytopes that fill ℝⁿ and scissors congruence", *Discrete Comput. Geom.* 13 (1995) 573–583, doi:10.1007/BF02574064 (abstract and corollaries seen).
- **C.-H. Sah**, *Hilbert's Third Problem: Scissors Congruence*, Pitman, 1979 (not read).
- **G. N. Frederickson**, *Dissections: Plane & Fancy*, Cambridge Univ. Press, 1997, ch. on solids; and his web updates to ch. 20 (Purdue): truncated octahedron to a cube in 12 pieces (Theobald, improving Hanegraaf) and 11 pieces (Theobald, Oct 2007) (web page seen).
- Wolfram Demonstrations (I. Hafner and others): "Dissecting a Rhombic Dodecahedron into Two Cubes"; "Dissection of Two Truncated Octahedra into a Cube" (six pieces, Paterson 1988 and Hanegraaf); "Dissecting a Truncated Octahedron to a Rectangular Solid" (titles seen).
- **J. H. Conway, C. Radin, L. Sadun**, "On angles whose squared trigonometric functions are rational", *Discrete Comput. Geom.* 22 (1999) 321–332: Dehn invariants of the Platonic and Archimedean solids (truncated octahedron and cube zero).

## Prior formalizations (searched 20 Nov 2026)

- The registered entry above (Lean): necessity direction only (equal invariants), no explicit dissection into a cube.
- FormalBook ch. 10 (Lean, *Proofs from THE BOOK*): non-equidecomposability (Bricard's condition) in an abstract segment-and-angle model; `GeomEquidecomposable` on sets; no explicit dissection of a solid into a cube found.
- Mathlib: no scissors congruence or Dehn invariant (code search). No formal proof of Sydler's theorem was found in Lean, Isabelle AFP (only Banach–Tarski's paradoxical decompositions), Coq/Rocq, HOL Light, Metamath or Mizar. No formal proof of the Wallace–Bolyai–Gerwien theorem was found either.

## What is claimed

Machine-checked explicit scissors congruences, with exact pieces, between each listed solid and a cube of the same volume. Not claimed: the Dehn–Sydler theorem; new dissections in the mathematical sense; minimal piece counts.

## Statement to score

E1. For each listed solid P (exact coordinates given as definitions): `ScissorsCongruent P (cube of side (volume P)^(1/3))`, the family of theorems scored as one result group, building on PALOMAR-2026-11-20-000003.
