/-!
# Dehn packets: two icosahedral pairs that cannot fill space

**Informal statement.** A convex polytope is a bounded intersection of finitely many closed half-spaces (`IsPoly`).
A tiling (`ConvexTiling`) covers space with convex polytopes that have interior points and pairwise disjoint
interiors, finitely many near each point; it need not be face to face. Angles are read from the set alone, as in the
Dehn Canon: at `x` the directions that stay in the set form a cone (`tcone`); where the directions `v` with `v`, `-v`
both in it span a line `K` (`linSpace`), the angle is 2π times the share of the unit disc of `Kᗮ` in the cone
(`wedgeAngle`); `EdgeAngle P θ` says that `θ` occurs so. A similar copy (`SimilarCopy`) is the image of a positive
scaling under an isometry (reflections allowed).

1. `lemma3` (**Lemma 3**): π, α = arctan φ, β = arccos(1/√6), γ = arccos √(2/3) are linearly independent over ℚ.
2. `lemma2` (**Lemma 2**): at an edge point `x` of tile `i` there are finitely many tiles, `i` among them, with angles
   `ω` summing to 2π: `ω i` is the angle of tile `i` at `x`, each `ω j` a dihedral angle of tile `j`, or π, or 2π.
3. `theorem4a_copies` (**Theorem 4 (a)**): in a tiling of ℝ³ by similar copies of the dodecahedron centre pyramid
   (`pyrDSet`), the truncated icosahedron (`tiSet`), the dodecahedron (`dhSet`), the icosahedron (`ihSet`), the
   truncated octahedron (`toSet`), the truncated cuboctahedron (`tcoSet`), and convex polytopes whose dihedral angles
   are all nonnegative rational multiples of π (`RationalAngles`), no tile is a copy of the pyramid or of the
   truncated icosahedron.
4. `theorem4b_copies` (**Theorem 4 (b)**): the same for the icosahedron centre pyramid (`pyrISet`) and the truncated
   dodecahedron (`tdSet`).

Each solid is the solution set of its face inequalities `⟪N k, x⟫ ≤ B k`, exact in ℚ(√5) or ℚ(√2) (the pyramids'
apex is the origin). The truncated icosidodecahedron of the paper's helper list is not built here.

**Sources.** DICTO, *From Dehn Packets to Scutoids: How the Fullerene Star Fills Space*, Zenodo (2026),
doi:10.5281/zenodo.24411660: Lemmas 2, 3 and Theorem 4 (a), (b). The set-defined angle is that of DICTO's *The Dehn
Canon* (Palomar PALOMAR-2026-11-20-000003). Every definition and statement is copied character for character from
the Lean library (namespaces `DehnCanon.Library`, `Packets`, `PacketsGen`; the qualifier `DehnCanon.Library.`
dropped); the comment before each group names its file.
-/
