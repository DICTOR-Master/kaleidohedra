# Lean study 10 of the shape-language canon: Hilbert's own question, and the edge sum for every convex polytope (19 November 2026)

**Question (from the Palomar pre-score of the Lean Dehn work, `studies/2026-11-19-palomar-dehn`):** both blind scorers asked for two Lean points. (1) Hilbert's literal statement: two tetrahedra of equal bases and equal altitudes that are not scissors congruent. (2) The set-defined invariant `dehnSet` equals the classical sum over the edges, length ⊗ dihedral angle, for every convex polytope, so that the set definition can be audited against Jessen's form.

**Result:** both are proved, in full generality, with no hypothesis left over. Two new Lean files (1,322 lines) compile with Lean v4.35.0-rc2 and the pinned Mathlib. The thirty-one files of studies 1 to 9 are unchanged. There are no errors, no warnings and no `sorry`, and only the three standard axioms appear (`compile.log`; the whole chain of 33 files was recompiled).

## Proved in Lean (theorem names, statements)

### 1. Hilbert's third problem in Hilbert's words (`lean/Dehn10Hilbert.lean`, part AE)

Hilbert (1900) asked for "two tetrahedra of equal bases and equal altitudes which can in no way be split up into congruent tetrahedra, and which cannot be combined with congruent tetrahedra to form two polyhedra which themselves could be split up into congruent tetrahedra" (problem 3; English by Newson, 1902). Dehn (1901) gave such pairs.

The pair: Examples 2 and 3 of Aigner and Ziegler's chapter (their tetrahedra T₁ and T₂, edge length 1), placed here on one and the same base triangle.

| | corners | edges (length, interior angle) | Dehn invariant |
|---|---|---|---|
| base | A = (0,0,0), B = (1,0,0), C = (0,1,0) | | |
| `cornerTet` | A, B, C, D = (0,0,1) | 3 × (1, π/2), 3 × (√2, arccos(1/√3)) | 3√2 ⊗ arccos(1/√3), not zero |
| `orthoTet` | A, B, C, D′ = (0,1,1) | π/2, π/2, π/2, π/4, π/4, π/3 | 0 |

```lean
theorem hilbert_third_problem :
    ∃ A B C D D' : R3,
      Metric.infDist D (affineSpan ℝ ({A, B, C} : Set R3) : Set R3) = 1 ∧
      Metric.infDist D' (affineSpan ℝ ({A, B, C} : Set R3) : Set R3) = 1 ∧
      volume (convexHull ℝ ({A, B, C, D} : Set R3)) = ENNReal.ofReal (1 / 6) ∧
      volume (convexHull ℝ ({A, B, C, D'} : Set R3)) = ENNReal.ofReal (1 / 6) ∧
      ¬ ScissorsCongruent (convexHull ℝ ({A, B, C, D} : Set R3)) (convexHull ℝ ({A, B, C, D'} : Set R3)) ∧
      ¬ EquiComplementable (convexHull ℝ ({A, B, C, D} : Set R3))
        (convexHull ℝ ({A, B, C, D'} : Set R3))
```
The two tetrahedra stand on the same triangle A B C, both apexes are at distance 1 from its plane, both volumes are 1/6, and the two solids are neither scissors congruent nor equicomplementable. "Equal bases" holds in the strongest form: the base is the same triangle.

- `EquiComplementable P Q` (defined here, the second half of Hilbert's sentence): finitely many convex polytopes can be added to `P`, and congruent copies of the same pieces to `Q` (interiors disjoint from each other and from `P`, from `Q`), so that the two enlarged solids are scissors congruent.
- `dehnSet_eq_of_equiComplementable`: **equicomplementable convex polytopes have the same Dehn invariant** (any 3-dimensional real inner product space).
- `cornerTet_eq_convexHull`, `orthoTet_eq_convexHull`: each solid, given by four half-spaces, is the convex hull of its four corners.
- `hil_height_corner`, `hil_height_ortho`: the two altitudes over the common base are 1 (distance from the apex to the plane through A, B, C).
- `volume_cornerTet`, `volume_orthoTet`: both volumes are 1/6.
- `dehnSet_cornerTet`: `dehnSet cornerTet = edgeTerm (3 * √2) (arccos (1 / √3))`. `arccos_inv_sqrt_three_not_ratPi`, `dehnSet_cornerTet_ne_zero`.
- `dehnSet_orthoTet`: `dehnSet orthoTet = 0`.
- `cornerTet_not_scissorsCongruent_orthoTet`, `cornerTet_not_equiComplementable_orthoTet`.

The pieces of a dissection are convex polytopes (tetrahedra among them), moved by isometries, reflections included. Both make the statement stronger than Hilbert's, who speaks of congruent tetrahedra.

### 2. The set-defined invariant is the classical edge sum (`lean/Dehn10Edges.lean`, part AF)

The edges, the facets through an edge and the dihedral angle are defined from the solid `P` as a set of points. No half-space description enters the definitions or the statements.
- `faceIn P n`: the points of `P` where ⟪n, ·⟫ is largest. `isExposed_faceIn`: it is an exposed face in Mathlib's sense (`IsExposed`).
- `IsEdge P F`: `F` is an exposed face of `P` (Mathlib's `IsExposed ℝ P F`) and a segment with two different ends. `edges P`: the set of the edges.
- `facetNormals P F`: the unit vectors `n` whose face `faceIn P n` contains `F` and is not contained in a line (Mathlib's `Collinear`). These are the outward unit normals of the facets through `F`.
- `dihedral P F`: π minus the largest angle between two vectors of `facetNormals P F`.

```lean
theorem dehnSet_eq_edge_sum {P : Set E} (hP : IsPoly P) (hint : (interior P).Nonempty) :
    dehnSet P = ∑ᶠ F ∈ edges P,
      (μH[1] F).toReal ⊗ₜ[ℚ] (Submodule.Quotient.mk (dihedral P F) : Angle)

theorem IsEdge.facetNormals_eq_pair {P F : Set E} (hP : IsPoly P) (hint : (interior P).Nonempty)
    (hF : IsEdge P F) :
    ∃ n₁ n₂ : E, LinearIndependent ℝ ![n₁, n₂] ∧ facetNormals P F = {n₁, n₂} ∧
      dihedral P F = π - InnerProductGeometry.angle n₁ n₂ ∧ 0 < dihedral P F ∧ dihedral P F < π

theorem edges_finite {P : Set E} (hP : IsPoly P) (hint : (interior P).Nonempty) : (edges P).Finite

theorem IsEdge.length {F : Set E} {u v : E} (hF : F = segment ℝ u v) : (μH[1] F).toReal = dist u v
```
Here `E` is any 3-dimensional real inner product space and `IsPoly P` is study 2's convex polytope: a bounded intersection of finitely many closed half-spaces. So for **every convex polytope with interior points**, `dehnSet P` is the sum over the edges of (length of the edge) ⊗ (interior dihedral angle modulo ℚπ), the invariant of Dehn (1901) in the tensor form of Jessen (1968). Through every edge pass exactly two facets, the angle is π minus the angle between their outward unit normals and lies strictly between 0 and π, and the sum is finite.

The half-space description that witnesses `IsPoly P` may be redundant in every way: repeated constraints, constraints that are never tight, constraints tight only along an edge or at a corner, zero normals. No general position is assumed. `dehnSet_sol_eq_edge_sum` is the same statement for `sol a b`.

## Method
- **Hilbert's pair.** Both tetrahedra satisfy study 4's `IsTetraData` (all weights 1), which gives the convex hulls, boundedness and the six-edge reading. The first solid's angles come from the Gram numbers of the normals (study 4's `theta_pair_of_gram`): 0 for two coordinate faces (angle π/2), and −1 with squared lengths 3 and 1 for the slanted face and a coordinate face (angle arccos(1/√3)). 2 arccos(1/√3) = π − arccos(1/3) (`arccos_inv_sqrt_three`, by cos 2x = 2cos²x − 1), so arccos(1/√3) is not a rational multiple of π by study 1's `tetDihedral_not_ratPi` (Mathlib's Niven theorem). The second solid has normals (1,1,0), (−1,0,0), (0,−1,1), (0,0,−1) whose pairwise angles are rational multiples of π (whole-number Gram table, `decide`), so study 4's `dehnSet_sol_eq_zero_of_rational` gives 0 with no edge reading.
- **Altitudes.** The plane through A, B, C lies in {z = 0} (`affineSpan_le`), a point with z = 1 is at distance ≥ 1 from every point with z = 0 (`PiLp.norm_apply_le`), and the foot (A, respectively C) is at distance 1.
- **Volumes.** The first solid is the corner simplex {u ≥ 0, u₀ + u₁ + u₂ ≤ 1}: three halvings of the ball of the sum norm of radius 1 (study 9's method), 4/3 → 1/6. The shear (u₀, u₁, u₂) ↦ (u₀, u₁ + u₂, u₂) has determinant 1 and carries the first solid onto the second (`Measure.addHaar_preimage_linearMap`). This is Cavalieri's principle in this one case, the limiting argument that Hilbert's question is about.
- **Equicomplementable.** Study 2's `dehnSum_eq_of_scissors` (finite unions, any two dissections) is applied to the two enlarged solids, each cut as the solid plus the added pieces. The added pieces carry the same invariant on both sides (`dehnSet_image`) and cancel.
- **The edge sum.** Study 4's `dehnSet_eq_sum_faceSet` gives `dehnSet (sol a b)` as a sum over the sets `A` of constraints: (length of the points where exactly `A` is tight) ⊗ (angle class of the cone of `A`). A set `A` contributes only if its common direction space is a line and it is the tight set of some point `x`. For such `A`:
  1. *A segment* (`tightSet_eq_segment`). The points where at least `A` is tight lie on the line through `x`. They are the image of a compact convex set of parameters containing a neighbourhood of 0, hence of an interval [t₀, t₁] with t₀ < 0 < t₁ (`eq_Icc_of_connected_compact`). Inside the segment exactly `A` is tight.
  2. *An exposed face* (`isExposed_tightSet`): exposed by the sum of the normals of `A`. So it is an edge.
  3. *Every edge arises so* (`exists_tight_of_edge`), from the tight set of its midpoint; different such `A` give different edges (`tightSet_inj`). This is a bijection (`bijOn_tightSet`), and the sum is re-indexed by `finsum_mem_eq_of_bijOn`.
  4. *Two constraints suffice* (`exists_pair_cone`). The normals of `A` lie in the plane perpendicular to the edge and, because the solid has an interior point, on one side of a line. Study 4's `two_extreme` picks two of them whose two half-planes cut out the whole cone. They are independent, because the direction space is a line. Study 3's `theta_pair` (the sector area) then gives the angle π − angle of the two normals.
  5. *They are the two facets* (`facetNormals_tightSet`). Each of the two normals, scaled to length 1, is a facet normal: its face contains the edge and a third point off the edge line (`unit_mem_facetNormals`). Conversely a facet normal at the edge is a combination α n_p + β n_q with α, β ≥ 0 (it is perpendicular to the edge and pairs ≤ 0 with the cone), and if both were positive its face would lie on the edge line (`eq_of_mem_facetNormals`).
- Independent check of the pair from its corners alone (`checks/hilbert_pair_check.py`, plain Python, run on the compute host): edge lengths, the twelve interior angles, 6 × volume = 1 and altitude 1 for both, and 2 arccos(1/√3) = π − arccos(1/3). It agrees with the table above.

## Credits (at the point of use in the files)
Mathematics: Hilbert (1900) for the question; Dehn (1901) for the answer and the invariant; Jessen (1968) for the form Σ length ⊗ angle; Aigner and Ziegler for the pair and its angles; Niven's theorem. Mathlib: `niven`, `IsExposed`, `Collinear`, `collinear_iff_of_mem`, `eq_Icc_of_connected_compact`, `Convex.isConnected`, `Convex.affine_preimage`, `image_segment`, `image_openSegment`, `segment_eq_Icc`, `openSegment_eq_Ioo`, `finrank_eq_one_iff'`, `finrank_span_eq_card`, `Submodule.eq_of_le_of_finrank_eq`, `Submodule.mem_span_pair`, `LinearIndependent.pair_symm_iff`, `LinearIndependent.pair_iff'`, `Finset.sum_eq_sum_iff_of_le`, `hausdorffMeasure_segment`, `finsum_mem_eq_of_bijOn`, `finsum_mem_inter_support_eq`, `InnerProductGeometry.angle_smul_left_of_pos`, `angle_smul_right_of_pos`, `angle_eq_zero_iff`, `angle_eq_pi_iff`, `MeasureTheory.volume_sum_rpow_le` (through study 9), `Measure.addHaar_preimage_linearMap`, `LinearMap.det_toLin'`, `Matrix.det_fin_three`, `PiLp.volume_preserving_ofLp`, `Metric.le_infDist`, `Metric.infDist_le_dist_of_mem`, `affineSpan_le`, `PiLp.norm_apply_le`, `Set.iUnion_option`, `Fintype.sum_option`. Studies 1 to 9 of this canon: `tetDihedral_not_ratPi`, `edgeTerm_ne_zero`, `tcone_sol`, `cone_lin`, `dehnSum_eq_of_scissors`, `dehnSet_image`, `dehn_bridge_R3`, `theta_pair`, `two_extreme`, `finrank_linCone_ne_one_of_perp`, `dehnSet_eq_sum_faceSet`, `hausdorff_openSegment`, `IsTetraData.dehnSet_eq`, `IsTetraData.eq_convexHull`, `theta_pair_of_gram`, `dehnSet_sol_eq_zero_of_rational`, `angle_mem_ratPi_of_gram`, `vol_half`, `vol_l1_le`, `vol_eq_of_sub_null`, `plane_null`.

Not used: the plane-cut argument of Hartshorne (Geometry: Euclid and Beyond, ch. 27). The edge sum is read off study 4's sum over tight sets, with no further cutting.

## Sources checked
- **D. Hilbert**, Mathematische Probleme, Nachr. Ges. Wiss. Göttingen (1900) 253–297, problem 3; English by M. W. Newson, Bull. Amer. Math. Soc. 8 (1902) 437–479. The quoted sentence was compared, fragment by fragment, with the Wikisource transcription of Newson's translation (en.wikisource.org/wiki/Mathematical_Problems, read 19 November 2026; that page says it is not backed by a scan). The Bulletin itself was not opened.
- **M. Aigner, G. M. Ziegler**, Proofs from THE BOOK, chapter "Hilbert's third problem: decomposing polyhedra". The book was not opened. Its Examples 2 and 3 (T₁: three orthogonal edges at one corner; T₂: the orthoscheme; angles π/2 × 3 and arccos(1/√3) × 3; π/2 × 3, π/4 × 2, π/3) were read from the docstrings of the FormalBook formalization of that chapter (below), and the angles were recomputed (`checks/hilbert_pair_check.out`).
- **FormalBook**, `FormalBook/Chapter_10.lean` (the copy in the Lean workspace). It has the same pair: `T₁`, `T₂`, `T₂_T₁` and a theorem headed "Hilbert's third problem", in its model of edge data (lengths and angles as lists, decompositions as an abstract structure). Its description says the bridge from geometric decompositions to that model is not established. So the pair and the theorem are on record in Lean in that model. What is added here is the pair as point sets, with base, altitude and volume proved for the sets, and non-congruence through the proved bridge of study 2.
- **M. Dehn**, Ueber den Rauminhalt, Math. Ann. 55 (1901) 465–478; **B. Jessen**, The algebra of polyhedra and the Dehn–Sydler theorem, Math. Scand. 22 (1968) 241–256: cited for the invariant and its tensor form, as in the reference list of the draft `papers/2026-11-19-dehn-canon`; not reread in this study.
- **Reference library** (manifests searched for Hilbert, Dehn, Sydler, Jessen, Aigner, Hartshorne, Boltianskii, scissors): held are the citation of Dehn (1901) and Sydler (1965, link only). Hilbert (1900), Jessen (1968), Aigner–Ziegler and Hartshorne are not held.
- **Pinned Mathlib** (grep): `IsExposed` (`Analysis/Convex/Exposed.lean`, with `Extreme.lean` and `KreinMilman.lean`) is the only notion of a face of a convex set; the edges or facets of a polytope, a dihedral angle of a solid, or a Dehn invariant: not found.
- **Web**: Wikipedia "Hilbert's third problem" (for the bibliographic data of Hilbert, Dehn, Sydler). No wider web search was made.
- A Lean proof that a set-defined Dehn invariant equals the edge sum for every convex polytope, or a Lean statement of Hilbert's wording for tetrahedra as point sets with a proved bridge: not found in the sources checked.

## `#print axioms` (from `compile.log`)
All 27 theorems listed in `lean/Axioms10.lean` print `[propext, Classical.choice, Quot.sound]`, among them `hilbert_third_problem`, `dehnSet_eq_of_equiComplementable`, `volume_cornerTet`, `volume_orthoTet`, `hil_height_corner`, `hil_height_ortho`, `dehnSet_cornerTet`, `dehnSet_orthoTet`, `dehnSet_eq_edge_sum`, `IsEdge.facetNormals_eq_pair`, `edges_finite`, `IsEdge.length`. No `native_decide`, no added axioms. One finite check uses plain `decide` (`hil2G_table`, a 4 × 4 table of whole numbers). `grep sorry` over the thirty-three files of the chain finds only the header lines that say "No `sorry`".

## Limits of what is stated
- Dimension 3. Pieces of a dissection are convex polytopes, finitely many, moved by isometries (reflections included), as in studies 2 to 9.
- The edge sum is for convex polytopes with interior points. A flat polytope has `dehnSet` zero and no facets in the sense used here. Solids that are not convex are covered only through study 2's sums over convex pieces.
- "Edge" means an exposed face that is a segment with two different ends. That every 1-dimensional face of a convex polytope is exposed is a known fact that is not needed and not proved here.
- "Equal bases" is proved as "the same base triangle", and "equal altitudes" as equal distances of the apexes from its plane. A general notion "area of the base of a tetrahedron" is not defined.
- Sydler's converse is not formalized, as before.

## Files and how to compile
`lean/Dehn10Hilbert.lean` (part AE, imports study 9), `lean/Dehn10Edges.lean` (part AF, imports study 4), `lean/Axioms10.lean`, `lean/compile_all10.sh`, `compile.log`; `checks/hilbert_pair_check.py` and its output.
Compiled in the Lean workspace of studies 1 to 9, all files in the folder `DehnCanon/`, by `bash DehnCanon/compile_all10.sh` from the workspace root (parts 1 to 6 and `check`, run one after the other so that each run stays short; `compile.log` is their outputs in order). It compiles the thirty-three files of the chain in dependency order, prints the axioms and greps for `sorry`, `native_decide` and `axiom`. The files on the compute host and the copies here have the same SHA-256.

## Leads
- **Palomar entry D1.** The two points the scorers asked for are now Lean theorems. The neutral input (`studies/2026-11-19-palomar-dehn/blind/inputs/D1-hilbert3-geometric.md`) can quote `hilbert_third_problem` and `dehnSet_eq_edge_sum` verbatim, and must say that FormalBook has the same pair in its edge-data model. A second blind score would show whether the notability moves.
- **The canon read from the set alone.** With `dehnSet_eq_edge_sum`, the invariant of any solid of the canon is fixed by its edges and facets as a set. Study 5's `IsEdgeData` (the hand-given table with its `cover` field) is now a way of computing, no longer part of what must be trusted.
- **Hilbert's sentence for every base and altitude.** The theorem gives one pair. Whether every base triangle and altitude carries two apexes with different invariants was not looked at here.
- **The corner tetrahedron against the regular one.** Both invariants are multiples of the class of arccos(1/3) (2 arccos(1/√3) = π − arccos(1/3)): `dehnSet cornerTet` = −(3√2/2) ⊗ arccos(1/3) by hand. So the corner tetrahedron joins study 9's family over arccos(1/3), where volume decides the pairs.
- **Exposed and extreme.** For a convex polytope every face is exposed; proving it would let `IsEdge` be stated with Mathlib's `IsExtreme` as well.
- From study 9, unchanged: Sydler's converse; one Lean folder for publication (now thirty-three files); a Challenge file and Comparator configuration for the Palomar entry.
