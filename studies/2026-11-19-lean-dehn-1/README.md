# Lean study 1 of the shape-language canon: Dehn's theorem, layer (a) (19 November 2026)

**Asked (DICTO):** "Dehn's own theorem in lean could prove to be the backbone" of a canon proved step by step in Lean studies. "Go".

**Result:** `lean/DehnCanon1.lean` compiles with Lean v4.35.0-rc2 and the pinned Mathlib: no errors, no warnings, no `sorry`; the main theorems use only the three standard axioms (propext, Classical.choice, Quot.sound) (`lean/compile.log`; `#print axioms` run on the compute host).

**Proved in Lean**
- `dehn`: the Dehn invariant of an edge list, Σ L ⊗ θ in ℝ ⊗[ℚ] (ℝ / ℚπ) (Jessen's form).
- `edgeTerm_ne_zero`: L ≠ 0 and θ not a rational multiple of π ⇒ L ⊗ θ ≠ 0 (dual functionals over ℚ).
- `dehn_eq_zero_of_rational`: all dihedrals rational in π ⇒ D = 0, any lengths.
- `dehn_cube`, `dehn_rhombicDodecahedron`, `dehn_cube_rd_family` (every solid with dihedrals among 90°, 120°, 135°, so the whole cube ∩ RD line incl. the fair 18-face die): D = 0.
- `tetDihedral_from_normals`: the tetrahedron's dihedral angle is arccos(1/3), derived from two face normals.
- `tetDihedral_not_ratPi`: arccos(1/3) is not a rational multiple of π (Niven's theorem, Mathlib `NumberTheory/Niven.lean`, Meiburg–Broshi 2025).
- `dehn_tetrahedron_ne_cube`: no regular tetrahedron has the Dehn invariant of any cube.

**Inputs, not yet proved in Lean:** the edge lists (lengths and dihedrals) of cube, RD and the 18-face family are given as data; only the tetrahedron's dihedral is derived from coordinates.

**Prior art (checked):** FormalBook PR #157 (mo271/FormalBook, merged 6 Oct 2026): Hilbert's third problem by the Proofs from THE BOOK route (pearl lemma, Bricard condition) in an abstract segment-and-angle decomposition model; its own description says it does not bridge arbitrary geometric decompositions to that model. Mathlib: no Dehn invariant or scissors congruence (grep of the pinned copy). Searches: web (standard and extended), 1000+ theorems list, the mathlib source.

## Layer (b), the bridge: scoping
What it must say: if a polyhedron P is cut into finitely many polyhedra that are moved by rigid motions and reassembled into Q, then dehn(P) = dehn(Q).
Needed and missing in Mathlib: polyhedra with faces and edges (Mathlib has convex hulls, not face lattices; FormalBook has Minkowski–Weyl), dissections, and the edge bookkeeping (on a common refinement, the dihedrals of the pieces along each edge segment sum to the solid's angle, π on a face or 2π inside, and π, 2π vanish in ℝ/ℚπ).
Proposed route for study 2: (1) read the FormalBook file and reuse its segment-and-angle model (toolchain v4.35.0-rc3 vs ours rc2: check); (2) prove the bridge first for dissections of convex polytopes into convex polytopes; (3) then our words (AXE, CLEO, FUJI need two independent angles: beyond Niven).
