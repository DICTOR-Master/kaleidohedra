# Candidate D1: Hilbert's third problem with the Dehn invariant defined on subsets of ℝ³ (a Lean development)

## Abstract (neutral)

Two solids are scissors congruent when one can be cut into finitely many polyhedral pieces that, moved by isometries, fill the other. Hilbert's third problem (1900) asked whether two tetrahedra of equal base and height are always scissors congruent; Dehn (1901) answered no, with an invariant (in Jessen's form, Σ length ⊗ dihedral angle in ℝ ⊗_ℚ (ℝ/ℚπ)) that cutting and regluing preserves and that separates the regular tetrahedron from the cube. The problem is solved, and it is already formalized in Lean (FormalBook, chapter 10, by a different route; see below).

This development proves Dehn's direction in Lean 4 with Mathlib with the invariant defined from the solid as a set, not from an edge list. For P ⊆ E (a 3-dimensional real inner product space): the cone of directions at x ∈ P; its lineality space; when that is a line K, the wedge angle 2π · area(cone ∩ unit disc of K^⊥) / area(unit disc of K^⊥); the angle class at x is that angle modulo ℚπ (0 at non-edge points); and `dehnSet P = Σ_θ μH[1]{x : class θ} ⊗ θ` (1-dimensional Hausdorff measure). It proves: (1) the plane-cut identity `dehnSet P = dehnSet (P ∩ H⁻) + dehnSet (P ∩ H⁺)` for every convex polytope (bounded intersection of finitely many closed half-spaces) and every plane, with no genericity condition; (2) invariance under every affine isometry (reflections included); (3) additivity over every dissection into convex polytopes with pairwise disjoint interiors (common refinement along facet planes, proved for any group-valued cut-additive set function); hence (4) the bridge: scissors-congruent convex polytopes have equal `dehnSet`, and for finite unions of convex polytopes the total over pieces is independent of the dissection and preserved; (5) the wedge angle of two half-spaces equals π − angle(normals), via a sector-area lemma from Mathlib's polar coordinates, so the area definition agrees with the usual dihedral angle; (6) evaluation on a model regular tetrahedron (six edges of length 2√2 at arccos(1/3)) and the cubes [−s,s]³ (zero); (7) scaling; (8) Dehn's theorem: no similar copy of the regular tetrahedron is scissors congruent to a similar copy of the cube. arccos(1/3) ∉ ℚπ comes from Mathlib's Niven theorem.

Facts on the proof: Lean v4.35.0-rc2, Mathlib pinned at 065356127b1dc0016f66b7283ce0ce2c4055aa55; `#print axioms` on every headline theorem gives only `propext`, `Classical.choice`, `Quot.sound`; no `sorry`, no `native_decide`, no added axiom. The chain for D1 is studies lean-dehn-1 to -4 of the development (19 files, 4,073 lines, axiom-check files included). One finite check in study 4 (not on D1's headline path to Dehn's theorem; it serves a zero-invariant family) uses `decide +kernel`. One optional file (`Dehn2Hull.lean`, convex hulls of finite sets = these polytopes) borrows FormalBook's Minkowski–Weyl theorem; nothing below depends on it. There is no Challenge file yet: the statements below are quoted verbatim from the development (proofs replaced by `sorry` here), and a Challenge file would be cut from them.

Limits stated by the author: dimension 3; pieces are convex polytopes, finitely many, moved by isometries including reflections; P, Q in the bridge are convex (the union form covers non-convex polyhedra given as unions); "regular tetrahedron" and "cube" mean similar copies of the two models below; Sydler's converse is not formalized.

Prior work by the same author (DICTO): an unpublished draft paper, "Dehn's Theorem from the Solids Up" (19 November 2026, not peer reviewed), which presents this development together with the canon of candidate D2. No earlier non-Lean publication on the bridge.

## The published problem and prior formalizations (sources, exact citations)

- **M. Dehn**, "Ueber den Rauminhalt", *Math. Ann.* 55 (1901) 465–478. The invariant and the theorem.
- **D. Hilbert**, "Mathematische Probleme", *Nachr. Ges. Wiss. Göttingen* (1900) 253–297, problem 3.
- **J.-P. Sydler**, "Conditions nécessaires et suffisantes pour l'équivalence des polyèdres de l'espace euclidien à trois dimensions", *Comment. Math. Helv.* 40 (1965) 43–80 (converse; quoted, not used).
- **B. Jessen**, "The algebra of polyhedra and the Dehn–Sydler theorem", *Math. Scand.* 22 (1968) 241–256 (tensor form).
- **M. Aigner, G. M. Ziegler**, *Proofs from THE BOOK*, Springer, chapter "Hilbert's third problem: decomposing polyhedra".
- **Mathlib**, `NumberTheory/Niven.lean` (Niven's theorem; Y. Meiburg, A. Broshi, 2025), used for arccos(1/3) ∉ ℚπ. Mathlib itself has no Dehn invariant or scissors congruence of polytopes (`Algebra/Group/Action/Equidecomp.lean` is equidecomposability under a group action).

Prior formalizations found by the submitter:
- **FormalBook**, Chapter 10 (Hilbert's third problem), https://github.com/mo271/FormalBook, pull request #157 (merged 6 October 2026), file `FormalBook/Chapter_10.lean` at commit 54da1ce. A complete, sorry-free Lean proof of Hilbert's third problem by the book's route (cone lemma, pearl lemma, Bricard's condition), including the book's tetrahedra and a tetrahedron vs the cube, in an abstract model of segments and angles (`EdgeData`, `Decomp`); it also has convex polytopes, faces and Minkowski–Weyl. Its description says "the file does not establish the bridge from arbitrary geometric decompositions to this model." It has no Dehn invariant.
- **facebookresearch/atlas-lean**, `MathlibExt/Geometry/Dissections/DehnInvariant.lean`: Dehn invariant of an edge list; cube zero; tetrahedron nonzero given the irrationality of arccos(1/3)/π as a hypothesis; no scissors congruence.
- **xiangyazi24/proof_in_the_book**, `ProofsInTheBook/Chapter09Final.lean`: non-equidecomposability of a regular tetrahedron and a subdivided cube with concrete pieces, with the pearl-lemma edge-count balance as a hypothesis.
- rjwalters/lean-genius `DissectionOfCubesOQ02.lean`: arccos(1/3)/π irrational; Dehn's theorem assumed.
- Not found: an entry in Isabelle AFP, Rocq/Coq, HOL Light, Metamath, Mizar, Naproche; Hilbert's third problem is not on Wiedijk's "Formalizing 100 Theorems" list.

What is claimed: a machine-checked proof of Dehn's theorem with the invariant defined from the solid as a set in ℝ³ and a proved bridge for every dissection into convex polytopes (and finite unions), "not found" in the sources above. The mathematics (Dehn, Jessen, the textbook plane-cut and refinement argument) is classical.

## The Lean statements (verbatim definitions and theorems)

```lean
import Mathlib
open Real TensorProduct
open scoped RealInnerProductSpace Pointwise
open Set MeasureTheory Measure Module
namespace DehnCanon

noncomputable def ratPi : Submodule ℚ ℝ := Submodule.span ℚ {π}
abbrev Angle := ℝ ⧸ ratPi
abbrev DehnSpace := ℝ ⊗[ℚ] Angle
noncomputable def edgeTerm (L θ : ℝ) : DehnSpace := L ⊗ₜ[ℚ] (Submodule.Quotient.mk θ : Angle)
noncomputable def tetDihedral : ℝ := arccos (1 / 3)

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

def sol {ι : Type} (a : ι → E) (b : ι → ℝ) : Set E := {x | ∀ i, ⟪a i, x⟫ ≤ b i}
def hsLe (c : E) (d : ℝ) : Set E := {x | ⟪c, x⟫ ≤ d}
def hsGe (c : E) (d : ℝ) : Set E := hsLe (-c) (-d)

/-- A convex polytope: a bounded intersection of finitely many closed half-spaces. -/
def IsPoly (P : Set E) : Prop :=
  Bornology.IsBounded P ∧ ∃ (ι : Type) (_ : Fintype ι) (a : ι → E) (b : ι → ℝ), P = sol a b

def tcone (P : Set E) (x : E) : Set E := {v | x ∈ P ∧ ∃ t : ℝ, 0 < t ∧ x + t • v ∈ P}
def linSpace (T : Set E) : Submodule ℝ E := Submodule.span ℝ {v | v ∈ T ∧ -v ∈ T}
def wedgeSet (T : Set E) (K : Submodule ℝ E) : Set Kᗮ := {w | (w : E) ∈ T ∧ ‖w‖ < 1}

/-- 2π × area(T ∩ unit disc of Kᗮ) / area(unit disc of Kᗮ). -/
noncomputable def wedgeAngle (T : Set E) (K : Submodule ℝ E) : ℝ :=
  2 * Real.pi * ((volume (wedgeSet T K)).toReal / (volume (Metric.ball (0 : Kᗮ) 1)).toReal)

noncomputable def theta (T : Set E) : Angle :=
  if finrank ℝ (linSpace T) = 1 then Submodule.Quotient.mk (wedgeAngle T (linSpace T)) else 0

noncomputable def edgeAngle (P : Set E) (x : E) : Angle := theta (tcone P x)

noncomputable def dehnSet (P : Set E) : DehnSpace :=
  ∑ᶠ θ : Angle, (μH[1] {x | edgeAngle P x = θ}).toReal ⊗ₜ[ℚ] θ

def ScissorsCongruent (P Q : Set E) : Prop :=
  ∃ (κ : Type) (_ : Fintype κ) (p : κ → Set E) (g : κ → E ≃ᵃⁱ[ℝ] E),
    (∀ k, IsPoly (p k)) ∧ (⋃ k, p k) = P ∧
    (Pairwise fun i j => Disjoint (interior (p i)) (interior (p j))) ∧
    (⋃ k, g k '' p k) = Q ∧
    (Pairwise fun i j => Disjoint (interior (g i '' p i)) (interior (g j '' p j)))

def IsSimilarCopy (P Q : Set E) : Prop := ∃ a : ℝ, 0 < a ∧ ∃ g : E ≃ᵃⁱ[ℝ] E, Q = g '' (a • P)

-- `cone`, `linCone`: the cone {v | ∀ i ∈ A, ⟪a i, v⟫ ≤ 0} and its lineality space {v | ∀ i ∈ A, ⟪a i, v⟫ = 0}
theorem wedgeAngle_two_planes [Fact (finrank ℝ E = 3)] (a₁ a₂ : E) (h : LinearIndependent ℝ ![a₁, a₂]) :
    wedgeAngle (cone ![a₁, a₂] Set.univ) (linCone ![a₁, a₂] Set.univ) =
      Real.pi - InnerProductGeometry.angle a₁ a₂ := by sorry

theorem dehnSet_cut [Fact (finrank ℝ E = 3)] {P : Set E} (hP : IsPoly P) (c : E) (d : ℝ) (hc : c ≠ 0) :
    dehnSet P = dehnSet (P ∩ hsLe c d) + dehnSet (P ∩ hsGe c d) := by sorry

theorem dehnSet_image (g : E ≃ᵃⁱ[ℝ] E) (P : Set E) : dehnSet (g '' P) = dehnSet P := by sorry

theorem dehnSet_eq_of_scissorsCongruent [Fact (finrank ℝ E = 3)] {P Q : Set E} (hP : IsPoly P)
    (hQ : IsPoly Q) (h : ScissorsCongruent P Q) : dehnSet P = dehnSet Q := by sorry

theorem dehnSum_eq_of_scissors [Fact (finrank ℝ E = 3)] {κ κ₁ κ₂ : Type} [Fintype κ] [Fintype κ₁]
    [Fintype κ₂] {p : κ → Set E} {g : κ → E ≃ᵃⁱ[ℝ] E} {p₁ : κ₁ → Set E} {p₂ : κ₂ → Set E}
    (hp : ∀ k, IsPoly (p k))
    (hdp : Pairwise fun i j => Disjoint (interior (p i)) (interior (p j)))
    (hdg : Pairwise fun i j => Disjoint (interior (g i '' p i)) (interior (g j '' p j)))
    (hp₁ : ∀ k, IsPoly (p₁ k))
    (hd₁ : Pairwise fun i j => Disjoint (interior (p₁ i)) (interior (p₁ j)))
    (hU₁ : (⋃ k, p₁ k) = ⋃ k, p k)
    (hp₂ : ∀ k, IsPoly (p₂ k))
    (hd₂ : Pairwise fun i j => Disjoint (interior (p₂ i)) (interior (p₂ j)))
    (hU₂ : (⋃ k, p₂ k) = ⋃ k, g k '' p k) :
    ∑ k, dehnSet (p₁ k) = ∑ k, dehnSet (p₂ k) := by sorry

theorem dehnSet_smul_set {a : ℝ} (ha : 0 < a) (P : Set E) : dehnSet (a • P) = a • dehnSet P := by sorry

abbrev R3 := EuclideanSpace ℝ (Fin 3)

theorem dehn_bridge_R3 {P Q : Set R3} (hP : IsPoly P) (hQ : IsPoly Q) (h : ScissorsCongruent P Q) :
    dehnSet P = dehnSet Q := by sorry

-- regular tetrahedron with corners (−1,−1,−1), (1,1,−1), (1,−1,1), (−1,1,1); cubeSet s = [−s, s]³
def tetN : Fin 4 → R3 := ![!₂[1, 1, 1], !₂[-1, -1, 1], !₂[-1, 1, -1], !₂[1, -1, -1]]
def tetraSet : Set R3 := sol tetN (fun _ => 1)
noncomputable def cubeN : Fin 3 × Bool → R3 :=
  fun p => if p.2 then EuclideanSpace.single p.1 1 else -EuclideanSpace.single p.1 1
def cubeSet (s : ℝ) : Set R3 := sol cubeN (fun _ => s)

theorem dehnSet_cube (s : ℝ) (hs : 0 < s) : dehnSet (cubeSet s) = 0 := by sorry

theorem tetra_not_scissorsCongruent_cube (s : ℝ) (hs : 0 < s) :
    ¬ ScissorsCongruent tetraSet (cubeSet s) := by sorry

theorem similarTetra_not_scissorsCongruent_similarCube {T Q : Set R3}
    (hT : IsSimilarCopy tetraSet T) (hQ : IsSimilarCopy (cubeSet 1) Q) : ¬ ScissorsCongruent T Q := by sorry

end DehnCanon
```

Notes on the quotation: the statements come from ten files of studies 1–4. Names, hypotheses and conclusions are copied exactly; instance binders are normalised to one `variable` line (in the files some lemmas `omit` unused instances, and the dimension hypothesis `[Fact (finrank ℝ E = 3)]` comes from a section `variable` or is written in the signature; it is shown inline here). `cone`/`linCone` (`Dehn2Cut.lean`) are summarised in a comment. Not quoted: `dehnSet_tetra : dehnSet tetraSet = dehn (tetrahedron (2 * √2))`, the value as study 1's edge-list sum (six edges of length 2√2 at `tetDihedral`).

## Statements to score

D1. `dehnSet_eq_of_scissorsCongruent` / `dehn_bridge_R3` with `dehnSet_cut`, `dehnSet_image`, `dehnSum_eq_of_scissors` (the bridge), together with `tetra_not_scissorsCongruent_cube` and `similarTetra_not_scissorsCongruent_similarCube` (Dehn's theorem) (score as one result group).
