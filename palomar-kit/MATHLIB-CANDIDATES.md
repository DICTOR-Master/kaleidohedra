# Candidate lemmas to offer to Mathlib

20 November 2026. A list only: no pull request was opened and no one at Mathlib was contacted.

**Read:** `YantraCert/` (kulaichev-yantra-lean, commit c167cf4); `DehnCanon/` (dehn-canon-lean, commit 9ea20f6, and the
workspace copy of the same library, which adds `Dehn2Hull.lean` and `Dehn9Same.lean`); `GET/` (grunbaum-k10-lean,
commit a6b16c2); `DehnHadwiger/` (study 2026-11-20-palomar-dehn4d, `lean/DehnHadwiger`).

**Mathlib searched:** a fresh clone of Mathlib master at bbb39fe (20 November 2026), by grep over `Mathlib/` for each
topic below (names, statements and docstrings). "Not found" means not found by these searches; it does not prove
absence. Before any offer, each item needs a search of open Mathlib pull requests and the Zulip archive, which was not
done here.

**Effort:** small = one file, under about 100 lines after generalising, no new definitions Mathlib must agree on;
medium = new definitions or a generalisation of a few hundred lines; large = a new theory needing design discussion.

## Ranking (value to others against effort)

| Rank | Candidate | Value | Effort |
|---:|---|---|---|
| 1 | arccos of a rational is not a rational multiple of π (Niven corollary) | high | small |
| 2 | Additivity of volume over convex pieces with disjoint interiors | medium | small |
| 3 | A pure tensor over a field vanishes only if a factor does; two-term variants | medium | small |
| 4 | Krawczyk test (existence and uniqueness of a zero in a box) | high | medium |
| 5 | Lattice translates of a compact set with volume = covolume tile space | medium–high | medium |
| 6 | Area of a circular sector | medium | small–medium |
| 7 | Radial homeomorphism of the frontier of a star-shaped compact body onto the sphere | medium | medium |
| 8 | Exact sign decision and order in ℤ[φ] | medium | medium |
| 9 | Segments are equal iff their endpoints agree; Hausdorff measure of sets in affine subspaces | low–medium | small |
| 10 | Dehn invariant read from the set, scissors congruence, and the bridge from dissections | high | large |
| 11 | Extension of cut-additive functions to dissections into convex polytopes | medium | medium (after 10) |
| 12 | Dehn–Hadwiger invariant in any dimension | medium | large (after 10) |
| — | Box-certificate checker; sparse polynomial normaliser | better as a separate library | — |

Items 1–3 can be offered on their own. Items 10–12 need a convex-polytope definition in Mathlib first; Mathlib's
polyhedral cone files (`Mathlib/Geometry/Convex/Cone/DualFinite.lean`, H-cones and V-cones) are the natural base and
should be followed rather than duplicated.

## The candidates

### 1. arccos of a rational is not a rational multiple of π

- **Statements and Lean names.** `DehnCanon.Library.tetDihedral_not_ratPi : arccos (1/3) ∉ ratPi`
  (`DehnCanon/DehnCanon1.lean`); `DehnHadwiger.arccos_quarter_not_ratPi : arccos (1/4) ∉ ratPi`
  (`DehnHadwiger/DH7Cell5.lean`); `DehnCanon.Library.wordAlpha_not_ratPi` (arccos(√5/5), through cos 2α = −3/5,
  `DehnCanon/Dehn4Words.lean`). Here `ratPi = Submodule.span ℚ {π}`.
- **General form to offer.** For `q : ℚ` with `|q| ≤ 1` and `q ∉ {−1, −1/2, 0, 1/2, 1}`: `arccos q / π` is irrational
  (equivalently `∀ r : ℚ, arccos q ≠ r * π`). Both proofs above are this statement for one value of `q`.
- **Why general.** It is the number-theoretic core of Dehn's theorem (dihedral angle of the regular tetrahedron and
  of the regular 5-cell) and of every non-tiling argument by dihedral angles; it is used wherever an angle with a
  rational cosine has to be shown incommensurable with π.
- **In Mathlib?** `niven`, `niven_sin`, `niven_angle_eq`, `irrational_cos_rat_mul_pi` exist in
  `Mathlib/NumberTheory/Niven.lean`. No statement about `arccos` of a rational was found
  (`Mathlib/Analysis/SpecialFunctions/Trigonometric/Inverse.lean` and the Niven file searched).
- **Size and dependencies.** About 10 lines each; `niven`, `Real.cos_arccos`.
- **Effort.** Small: a corollary in `Mathlib/NumberTheory/Niven.lean`.

### 2. Volume of a union of convex pieces with disjoint interiors

- **Statement and Lean name.** `DehnCanon.Library.volume_iUnion_poly`: for finitely many convex polytopes `p k` in
  ℝ³ with pairwise disjoint interiors, `volume (⋃ k, p k) = ∑ k, volume (p k)` (`DehnCanon/Dehn9Vol.lean`, 19 lines).
  Also `DehnCanon.Library.volume_eq_of_scissorsCongruent` (7 lines, same file), which needs item 10's definition.
- **General form to offer.** For any additive Haar measure on a finite-dimensional real space and a finite (or
  countable) family of measurable convex sets, or of sets whose frontiers are null, with pairwise disjoint interiors:
  the measure of the union is the sum of the measures. The proof uses only that a convex set has a null frontier.
- **Why general.** Every dissection argument (areas, volumes, tilings, equidecomposition) needs it.
- **In Mathlib?** `Convex.addHaar_frontier` (`Mathlib/Analysis/Convex/Measure.lean`) and `measure_iUnion` with
  `AEDisjoint` exist; no lemma passing from disjoint interiors to `AEDisjoint` was found.
- **Size and dependencies.** About 20–30 lines; `Convex.addHaar_frontier`, `measure_biUnion_finset`/`measure_iUnion`.
- **Effort.** Small.

### 3. Pure tensors over a field

- **Statements and Lean names.** `DehnCanon.Library.edgeTerm_ne_zero` (`L ≠ 0`, `θ ∉ ℚπ` give
  `L ⊗ₜ[ℚ] θ ≠ 0` in ℝ ⊗[ℚ] ℝ/ℚπ; `DehnCanon/DehnCanon1.lean`, 16 lines); `DehnCanon.Library.tmul_add_tmul_ne_zero`
  (`L₁ ∉ span ℚ {L₂}`, `θ₁ ≠ 0` give `L₁ ⊗ θ₁ + L₂ ⊗ θ₂ ≠ 0`; `DehnCanon/Dehn4Simplex.lean`, 20 lines);
  `DehnCanon.Library.not_proportional` (two invariants over two independent angles are proportional only if their
  coefficient determinant vanishes; `DehnCanon/Dehn5Pairs.lean`, 30 lines).
- **General form to offer.** Over a field `K`, for vector spaces `V`, `W`: `v ⊗ₜ w = 0 ↔ v = 0 ∨ w = 0`, and the
  two-term criterion with linearly independent left factors. The proofs use dual functionals
  (`Submodule.exists_dual_map_eq_bot_of_notMem`).
- **Why general.** Linear algebra used by every tensor-valued invariant (Dehn, Hadwiger, Jessen), and elsewhere.
- **In Mathlib?** Not found under the names `tmul_ne_zero` or `tmul_eq_zero_iff` for vector spaces; Mathlib has the
  equational criterion for vanishing (`Mathlib/LinearAlgebra/TensorProduct/Vanishing.lean`) and
  `FaithfullyFlat.one_tmul_eq_zero_iff`, from which the first form may follow. To be checked carefully before offering:
  it may exist under another name.
- **Size and dependencies.** 15–30 lines each; `Module.Dual`, `TensorProduct.lift`.
- **Effort.** Small.

### 4. Krawczyk test

- **Statements and Lean names.** `YantraCert.krawczyk_unique` (at most one zero of `F : ι → (ι → ℝ) → ℝ` in the box
  `InBox c r`, given slope enclosures `ℓ ≤ S ≤ h` and a preconditioner `Y` with weighted norm of `I − Y S` below 1)
  and `YantraCert.krawczyk_exists` (if moreover `|Y F(c)| + M r ≤ r` and `Y` is invertible, a zero exists, by
  `ContractingWith.fixedPoint`) (`YantraCert/Krawczyk.lean`, section `General`, lines 23–200: 34 and 83 lines plus
  helpers `InBox`, `kmap`, `kmap_diff`, `entry_bound`, `M_nonneg`).
- **Why general.** The standard certificate of existence and uniqueness of a zero of a system of equations in
  verified numerics (Krawczyk 1969, Moore 1977, Neumaier 1990); it turns floating-point root finding into a Lean
  theorem for any finite system. The statement is independent of the yantra and of the polynomial instance that
  follows it in the same file.
- **In Mathlib?** No Krawczyk test or interval Newton method found (`krawczyk`, `interval Newton`); Mathlib has
  interval arithmetic types (`Mathlib/Algebra/Order/Interval/Basic.lean`) and Banach's theorem
  (`Mathlib/Topology/MetricSpace/Contracting.lean`).
- **Size and dependencies.** About 175 lines; `Finset` sums, `ContractingWith`, `Metric.closedBall` in the sup norm.
  For Mathlib the statement should be stated with matrices (`Matrix ι ι ℝ`) and a slope hypothesis, perhaps also in
  the derivative form (mean value theorem).
- **Effort.** Medium (restatement and review; the proof is short).

### 5. Lattice translates of a set with volume = covolume tile space

- **Statements and Lean names.** `GET.PB_cover` (the lattice translates of GET B cover space; `GET/Cover.lean`, 53
  lines), with `GET.translates_null` (12 lines), `GET.translates_locallyFinite` (46 lines),
  `GET.isClosed_union_translates`, `GET.volume_F0`, and `GET.PB_disjoint` (`GET/Tiling.lean`).
- **General form to offer.** For a full lattice `L` (a `ZLattice`) in a finite-dimensional real inner product space
  and a compact set `P` with `volume P = covolume L` whose distinct `L`-translates meet in null sets: the translates
  cover the space (and, with disjoint interiors, tile it). The proof uses only Mathlib's fundamental domain
  `ZSpan.fundamentalDomain`, local finiteness of a lattice and the fact that an open null set is empty; the GET
  statements use nothing about GET B beyond these hypotheses.
- **Why general.** It is the usual way to prove that a candidate parallelohedron, or any lattice tile, really tiles,
  from a volume computation; it applies to every fundamental-domain argument for lattices.
- **In Mathlib?** `ZLattice.covolume`, `covolume_eq_measure_fundamentalDomain`, `ZSpan.isAddFundamentalDomain` and
  `IsAddFundamentalDomain.mk_of_measure_univ_le` (finite measures only, so not for a lattice in ℝⁿ) exist. The
  converse direction found here (volume = covolume and a.e. disjoint translates give a cover) was not found.
- **Size and dependencies.** About 120 lines once generalised; `Mathlib/Algebra/Module/ZLattice/*`,
  `Mathlib/MeasureTheory/Group/FundamentalDomain.lean`, `LocallyFinite.isClosed_iUnion`.
- **Effort.** Medium.

### 6. Area of a circular sector

- **Statement and Lean name.** `DehnCanon.Library.volume_sector`: for `0 < β < π/2`, the sector `{z : ℂ | ‖z‖ < 1,
  |arg z| ≤ β}` has area `β` (`DehnCanon/Dehn3Sector.lean`, 68 lines; the definition `sector` in the same file).
- **General form to offer.** The same for every `0 ≤ β ≤ π`, and for sectors of radius `r` (area `β r²`).
- **Why general.** Elementary measure theory that is missing; it ties angles to areas, which any definition of angle
  by measure (as in item 10) needs.
- **In Mathlib?** Not found: the volume of balls and discs is in `Mathlib/MeasureTheory/Measure/Lebesgue/VolumeOfBalls.lean`;
  sectors appear only in a private lemma of `Mathlib/MeasureTheory/Constructions/HaarToSphere.lean`.
- **Size and dependencies.** 70–100 lines; polar coordinates (`Complex.polarCoord` / `integral_comp_polarCoord_symm`).
- **Effort.** Small to medium.

### 7. Radial homeomorphism of a star-shaped frontier onto the sphere

- **Statement and Lean name.** `GET.sphere_of_radial`: for a compact `K` in ℝ³, a point `c ∈ K` not on the frontier,
  and the hypothesis that every ray from `c` meets the frontier at most once, `frontier K ≃ₜ Metric.sphere 0 1`
  (`GET/Sphere.lean`, 73 lines).
- **General form to offer.** The same in any finite-dimensional real normed space.
- **Why general.** It is the standard way to show that a nonconvex but star-shaped solid has the topology of a ball;
  it applies to every star-shaped polyhedron.
- **In Mathlib?** For convex bodies, `gaugeRescaleHomeomorph` (`Mathlib/Analysis/Convex/GaugeRescale.lean`) gives a
  homeomorphism taking interior to interior and closure to closure. The star-shaped version was not found.
- **Size and dependencies.** About 75 lines; compactness, `Continuous.subtype_mk`, continuity of the inverse on a
  compact set.
- **Effort.** Medium (generalisation, and fitting it to the gauge-rescale API).

### 8. Exact sign decision and order in ℤ[φ]

- **Statements and Lean names.** `GET.ZPhi` (pairs `a + bφ` with `+`, `−`, `*`), `GET.ZPhi.toReal` with
  `GET.ZPhi.toReal_add`, `toReal_mul` etc., the exact sign test `GET.ZPhi.pos` with `GET.ZPhi.pos_sound` (28 lines,
  `GET/ZPhi.lean`) and `GET.pos_complete` (37 lines, `GET/Solid.lean`); the same arithmetic as `DehnHadwiger.gmul`,
  `gval`, `gdot` (`DehnHadwiger/DH8Cell120.lean`) and as `DehnCanon.Library.q5`, `mul5` over ℤ[√5]
  (`DehnCanon/Dehn7Gold.lean`).
- **General form to offer.** For Mathlib's `QuadraticAlgebra ℤ a b` with positive non-square discriminant, the ring
  embedding into ℝ (for ℤ[φ]: `QuadraticAlgebra ℤ 1 1 → ℝ`, ω ↦ goldenRatio) and the induced decidable linear order,
  with a sign test that the kernel can evaluate.
- **Why general.** Exact computation in ℤ[φ] (icosahedral geometry, quasicrystals, Penrose tilings, the 120-cell and
  600-cell) by `decide`, without real-number reasoning.
- **In Mathlib?** `QuadraticAlgebra` exists (`Mathlib/Algebra/QuadraticAlgebra/`), with no order or embedding into ℝ
  found; `ℤ√d` (`Zsqrtd`) has a decidable `LinearOrder` (`Mathlib/NumberTheory/Zsqrtd/Basic.lean`), whose method
  is the model.
- **Size and dependencies.** 150–250 lines after generalising from the golden case.
- **Effort.** Medium.

### 9. Two small lemmas

- **Segments.** `GET.segment_eq_segment_iff`: for `x ≠ y`, `segment ℝ x y = segment ℝ x' y' ↔ (x = x' ∧ y = y') ∨
  (x = y' ∧ y = x')` (`GET/Zones.lean`, 53 lines). Not found in `Mathlib/Analysis/Convex/Segment.lean` (Mathlib has
  `segment_injective_of_ne` for paths). Small; the proof could be shortened with extreme points.
- **Hausdorff measure in affine subspaces.** `DehnHadwiger.hausdorff_affine_ne_top` (a bounded set in a translate of a
  subspace `W` has finite `dim W`-dimensional Hausdorff measure) and `DehnHadwiger.hausdorff_affine_null` (zero
  `d`-dimensional measure for `d > dim W`) (`DehnHadwiger/DH1Def.lean`, 29 and 18 lines). Mathlib has the pieces
  (`Isometry.hausdorffMeasure_image`, `hausdorffMeasure_of_dimH_lt`, `Real.dimH_univ_eq_finrank`); these two
  statements were not found. Small.
- **Value.** Low to medium; convenient API lemmas.

### 10. The Dehn invariant read from the set, scissors congruence and the bridge

- **Statements and Lean names** (namespace `DehnCanon.Library`). Definitions `ratPi`, `Angle`, `DehnSpace`,
  `edgeTerm`, `dehn` (`DehnCanon1.lean`); `sol`, `IsPoly` (`Dehn2Poly.lean`); `tcone`, `linSpace`, `wedgeAngle`,
  `theta`, `edgeAngle`, `dehnSet` (`Dehn2Local.lean`); `ScissorsCongruent` (`DehnCanon2.lean`); `edges`,
  `facetNormals`, `dihedral` (`Dehn10Edges.lean`); `EquiComplementable` (`Dehn10Hilbert.lean`). Theorems
  `dehnSet_cut` (`Dehn2Cut.lean`), `dehnSet_image` (`Dehn2Motion.lean`), `dehnSet_dissection`,
  `dehnSet_eq_of_scissorsCongruent`, `dehnSum_eq_of_scissors` (`DehnCanon2.lean`), `dehnSet_eq_edge_sum`
  (`Dehn10Edges.lean`), `wedgeAngle_two_planes` (`Dehn3Sector.lean`), `dehnSet_smul_set` (`Dehn4Similar.lean`),
  `hilbert_third_problem` (`Dehn10Hilbert.lean`), `similarTetra_not_scissorsCongruent_similarCube`
  (`Dehn4Similar.lean`).
- **Why general.** Scissors congruence and the Dehn invariant are standard (Hilbert's third problem, Sydler's
  theorem, Jessen's tensor form); defining the invariant from the set, with no edge list, and proving the bridge from
  geometric dissections in every 3-dimensional inner product space is the base on which Sydler's converse, the
  four-dimensional theory and valuations could be built.
- **In Mathlib?** No Dehn invariant (`dehn` matches only Dehn functions of groups), no scissors congruence and no
  convex polytope definition found. `Equidecomp` (`Mathlib/Algebra/Group/Action/Equidecomp.lean`) is
  equidecomposability under group actions, set-theoretic, not by polytopes. Hilbert's third problem is formalised
  outside Mathlib in FormalBook (chapter 10), in an abstract model of edges and angles.
- **Size and dependencies.** The development is 32 files and about 15,500 lines, most of it the worked solids; the
  general part (`DehnCanon1`, `Dehn2*`, `Dehn3Sector`, `DehnCanon2`, `Dehn4Similar`, `Dehn10Edges`) is about
  3,100 lines. Mathlib: tensor products over ℚ, quotients, Hausdorff measure `μH[1]`, finsums, inner product
  geometry, `IsExposed`.
- **Effort.** Large: a polytope API must be agreed first (H-description as here, V-description, and their
  equivalence, Minkowski–Weyl; our workspace copy borrows that from FormalBook in `Dehn2Hull.lean`), and the
  set-defined invariant is a design choice to discuss on Zulip.

### 11. Extension of cut-additive functions to dissections

- **Statement and Lean name.** `DehnCanon.Library.dissection_additive`: a function `D : Set E → A` into an additive
  group that is additive under every cut of a convex polytope by a hyperplane is additive over every dissection of a
  convex polytope into finitely many convex polytopes with disjoint interiors (`DehnCanon/Dehn2Poly.lean`, 72 lines;
  Hadwiger 1957, Groemer 1978).
- **Why general.** The usual route to valuations on polytopes (volume, Euler characteristic, Dehn invariant, mixed
  volumes) goes through it, in any finite dimension.
- **In Mathlib?** Not found (no polytopes, no valuations on polytopes).
- **Size and dependencies.** 72 lines plus `cells` and the refinement lemmas in the same file (about 290 lines in
  all); needs item 10's `IsPoly`.
- **Effort.** Medium, after a polytope definition exists.

### 12. The Dehn–Hadwiger invariant in any dimension

- **Statements and Lean names** (namespace `DehnHadwiger`). `thetaH`, `ridgeAngle`, `dehnHadwiger` (the invariant
  Σ (n−2)-dimensional measure ⊗ angle class, `DH1Def.lean`); `dehnHadwiger_cut` (`DH2Cut.lean`);
  `dehnHadwiger_image`, `dehnHadwiger_dissection`, `dehnHadwiger_eq_of_scissorsCongruent` (`DH3Bridge.lean`);
  `dehnHadwiger_sol_eq_zero_of_rational` (`DH4Pair.lean`); `dehnHadwiger_smul_set` (`DH5Scale.lean`).
- **Why general.** Hadwiger's invariant for scissors congruence in dimension n ≥ 3; with item 10 it covers the
  classical invariant in every dimension.
- **In Mathlib?** Not found.
- **Size and dependencies.** About 1,300 lines for the general part (`DH1`–`DH5`, `DH10`), the rest being the regular
  4-polytopes; builds on item 10.
- **Effort.** Large, after item 10.

### Better as separate libraries

- **Box-certificate checker** (`YantraCert/Check.lean`, `Sound.lean`, `Cover.lean`; about 850 lines;
  `SP.signMono_sound`, `checkTree_sound`, `Chart.good_of_root`). A kernel-evaluated branch-and-bound checker for sign
  conditions of three-variable polynomials on dyadic cells. General in purpose (certified global bounds), but its
  data format, three variables and natural-number encoding are tied to `decide +kernel`; Mathlib has no home for
  such checkers. Offer it as a standalone verified-numerics library instead.
- **Sparse polynomial normaliser** (`YantraCert/ZPoly.lean`, `ZPolySound.lean`, `ZPoly2*.lean`; about 400 lines;
  `ZP.eq_of_eqv`). A reflective normaliser checked by the kernel. Mathlib's `ring` and `grind` cover ordinary use;
  the reflective form is useful only for very large identities. Not a Mathlib candidate.
- **Not ours to offer:** the Minkowski–Weyl step `isPoly_iff_convexHull` (`Dehn2Hull.lean`) is borrowed from
  FormalBook's `Chapter10.isConvexPolytope_iff`.

## Next step, if DICTO wants one

Item 1 alone is a natural first offer: small, self-contained and next to Mathlib's existing `niven`. Before it, search
open Mathlib pull requests and Zulip for the same statement.

## Dehn packets and helpers (DICTO's idea, 21 Nov 2026)
- The Dehn invariant as a conserved "packet": additivity over dissections and the mixed-tiling condition n·D(P) + Σ m_i·D(H_i) = 0, with the octet (2 tetrahedra + 1 octahedron) as the worked example. Builds on #113's Lean base (invariant read from the set, the bridge to the edge sum).
- Centre pyramids: D(pyramid) = (base edges) ⊗ θ/2; zero exactly when θ/π is rational (cube, rhombic dodecahedron, rhombic triacontahedron among the isohedral solids).
- Each exact cancelling relation found by the packet screen (studies/2026-11-21-packet-screen) is a small, self-contained Lean lemma candidate.
- The shear ledger: volume-preserving affine maps change the packet by computable amounts; their sum from tetrahedron to cube is −6a ⊗ arccos(1/3).
