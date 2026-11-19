# Candidate D2: a machine-checked canon of Dehn invariants on top of a set-level Dehn invariant (a Lean development)

## Abstract (neutral)

Base layer (candidate D1): in Lean 4 with Mathlib, `dehnSet P ∈ ℝ ⊗_ℚ (ℝ/ℚπ)` is defined from a set P ⊆ ℝ³ (edge angle = 2π × area share of the direction cone in the unit disc across the edge line; lengths by 1-dimensional Hausdorff measure), and scissors-congruent convex polytopes are proved to have equal `dehnSet`; Dehn's theorem follows. Hilbert's third problem is solved (Dehn 1901) and already formalized in Lean in FormalBook by a different route.

On this base the development evaluates `dehnSet` on a list of named solids, each given as an intersection of half-spaces with exact coordinates in ℚ or ℚ(√5):
- **zero**: the cubes; the rhombic dodecahedron; every solid {|xᵢ| ≤ s, |xᵢ ± xⱼ| ≤ c} (cube ∩ rhombic dodecahedron line); the truncated octahedron; the rhombic triacontahedron, and every solid whose face normals are two-fold axes of the icosahedral group; both golden rhombohedra;
- **nonzero**: dodecahedron, icosahedron, regular tetrahedron, octahedron, every cube ∩ octahedron solid {|xᵢ| ≤ 1, |x|+|y|+|z| ≤ t}, 1 < t < 2, t ≠ 3/2 (invariant 12√2(2t−3) ⊗ θ; t = 3/2 is the truncated octahedron), and CLEO, AXE (tetrahedra) and FUJI (six triangles at an apex and a hexagon), with θ = arccos(1/3), α = arccos(1/√5), γ = arccos(√5/3), β = 79.18…° (cos²β = 1/3 − 2√5/15), g = (√5−1)/2: CLEO = 3 ⊗ α + 3g ⊗ β, AXE = (1+g) ⊗ α + 6 ⊗ β, FUJI = (9−3g) ⊗ α + (12−3g) ⊗ β.

Arithmetic: α + 2β − γ = π exactly; θ, α, β are ℚ-independent modulo π (α, β by an integer recurrence for 2·15ⁿcos(2nβ) with a divisibility-by-3 argument; θ against them by comparing sines in ℚ√2 and ℚ(√5); single irrationalities by Mathlib's Niven theorem). Volume: preserved by scissors congruence; volumes of the tetrahedron (8/3), octahedron (4/3) and cube ∩ octahedron solids ((4/3)(t³ − 3(t−1)³)) from Mathlib's ℓ¹-ball volume. Headline `canon_complete`: no similar copy of a nonzero solid is scissors congruent to one of a zero solid, and every two different nonzero solids of the list are not scissors congruent in any sizes (θ-family pairs with proportional invariants decided by the scale-free a³/volume).

Facts on the proof: Lean v4.35.0-rc2, Mathlib pinned at 065356127b1dc0016f66b7283ce0ce2c4055aa55; every headline theorem's `#print axioms` gives only `propext`, `Classical.choice`, `Quot.sound`; no `sorry`, no `native_decide`, no added axiom. 40 files, 14,527 lines (studies lean-dehn-1 to -9, axiom-check files included); study 7's files (7,504 lines) are mostly generated certificates, re-checked by Lean. `decide +kernel` (kernel evaluation, no extra axiom) checks two finite Gram tables: 324 integer pairs (study 4), 900 ℤ[√5] pairs (study 7). There is no Challenge file yet: the statements below are quoted verbatim from the development (proofs replaced by `sorry`), and a Challenge file would be cut from them.

Limits stated by the author: as D1 (dimension 3; convex pieces; reflections allowed); solids are the half-space sets in the files (equality with the hull of the corners is stated only for CLEO, AXE, golden rhombohedra); volumes only for the θ family; Sydler's converse not formalized.

Prior work by the same author (DICTO), not peer reviewed: an unpublished draft paper, "Dehn's Theorem from the Solids Up" (19 November 2026), presenting this development; "AXE, CLEO and FUJI" (#19), Zenodo, DOI 10.5281/zenodo.23351291 (the three solids). The names CLEO, AXE, FUJI are the author's; CLEO and AXE are Mosseri–Sadoc golden tetrahedra (F* and A* below).

## Published sources and prior formalizations (exact citations)

Base problem: M. Dehn, "Ueber den Rauminhalt", *Math. Ann.* 55 (1901) 465–478; D. Hilbert, "Mathematische Probleme", *Nachr. Ges. Wiss. Göttingen* (1900) 253–297, problem 3; J.-P. Sydler, *Comment. Math. Helv.* 40 (1965) 43–80; B. Jessen, "The algebra of polyhedra and the Dehn–Sydler theorem", *Math. Scand.* 22 (1968) 241–256.

Known on paper (disclosed; the development is a machine-checked version of these):
- **J. H. Conway, C. Radin, L. Sadun**, "On angles whose squared trigonometric functions are rational", *Discrete Comput. Geom.* 22 (1999) 321–332, arXiv:math-ph/9812019: Dehn invariants of the Platonic and non-snub Archimedean solids (Table 3); ℚ-independence modulo π of angles with rational squared cosine, including θ, α, γ (Theorem 1, Splitting Theorem §1). β (irrational cos²β) is outside their class.
- **O. Ogievetsky, Z. Papadopolos**, "On quasiperiodic space tilings, inflation and Dehn invariants", arXiv:math-ph/9910006 (1999), §3: golden tetrahedra with CLEO = their F* and AXE = their A*, with their Dehn invariants (eq. (8)), the angle relations (Lemma 1) and the independence of α and γ (Lemma 2, via Conway–Radin–Sadun). Together these give the α–β independence and θ against α, β on paper. A prior-art search by the submitter first missed this source and was corrected.
- **H. E. Debrunner**, *Arch. Math.* 35 (1980) 583–587, and **J. C. Lagarias, D. Moews**, "Polytopes that fill ℝⁿ and scissors congruence", *Discrete Comput. Geom.* 13 (1995) 573–583: space-fillers have zero invariant (cube, rhombic dodecahedron, truncated octahedron, golden rhombohedra). **D. Calegari**, "Homework 1: scissors congruence and equidecomposability in Euclidean space" (2001): rhombic triacontahedron zero by rational angles. Volume with the invariant is the classical Dehn–Sydler criterion.
- Not found on paper by the submitter: FUJI's invariant and the non-congruences involving FUJI.

Formal: **FormalBook** Chapter 10, https://github.com/mo271/FormalBook, PR #157 (merged 6 October 2026), `FormalBook/Chapter_10.lean` at commit 54da1ce: Hilbert's third problem by Bricard's condition in an abstract model ("does not establish the bridge from arbitrary geometric decompositions to this model"); arccos(1/√n)/π irrational for odd n ≥ 3, one angle at a time. atlas-lean `DehnInvariant.lean` (edge lists); proof_in_the_book `Chapter09Final.lean` (pearl-lemma balance as hypothesis). Mathlib: Niven's theorem (Meiburg–Broshi 2025); no Dehn invariant. Not found: machine-checked invariants of the solids above, of joint independence of angles modulo π, or of these non-congruences.

## The Lean statements (verbatim)

```lean
import Mathlib
open Real TensorProduct
open scoped RealInnerProductSpace Pointwise
open Set MeasureTheory Measure Module
namespace DehnCanon
abbrev R3 := EuclideanSpace ℝ (Fin 3)
noncomputable def ratPi : Submodule ℚ ℝ := Submodule.span ℚ {π}
abbrev Angle := ℝ ⧸ ratPi
abbrev DehnSpace := ℝ ⊗[ℚ] Angle
noncomputable def edgeTerm (L θ : ℝ) : DehnSpace := L ⊗ₜ[ℚ] (Submodule.Quotient.mk θ : Angle)
def sol {ι : Type} (a : ι → R3) (b : ι → ℝ) : Set R3 := {x | ∀ i, ⟪a i, x⟫ ≤ b i}
def IsPoly (P : Set R3) : Prop :=
  Bornology.IsBounded P ∧ ∃ (ι : Type) (_ : Fintype ι) (a : ι → R3) (b : ι → ℝ), P = sol a b
def tcone (P : Set R3) (x : R3) : Set R3 := {v | x ∈ P ∧ ∃ t : ℝ, 0 < t ∧ x + t • v ∈ P}
def linSpace (T : Set R3) : Submodule ℝ R3 := Submodule.span ℝ {v | v ∈ T ∧ -v ∈ T}
def wedgeSet (T : Set R3) (K : Submodule ℝ R3) : Set Kᗮ := {w | (w : R3) ∈ T ∧ ‖w‖ < 1}
noncomputable def wedgeAngle (T : Set R3) (K : Submodule ℝ R3) : ℝ :=
  2 * Real.pi * ((volume (wedgeSet T K)).toReal / (volume (Metric.ball (0 : Kᗮ) 1)).toReal)
noncomputable def theta (T : Set R3) : Angle :=
  if finrank ℝ (linSpace T) = 1 then Submodule.Quotient.mk (wedgeAngle T (linSpace T)) else 0
noncomputable def edgeAngle (P : Set R3) (x : R3) : Angle := theta (tcone P x)
noncomputable def dehnSet (P : Set R3) : DehnSpace :=
  ∑ᶠ θ : Angle, (μH[1] {x | edgeAngle P x = θ}).toReal ⊗ₜ[ℚ] θ
def ScissorsCongruent (P Q : Set R3) : Prop :=
  ∃ (κ : Type) (_ : Fintype κ) (p : κ → Set R3) (g : κ → R3 ≃ᵃⁱ[ℝ] R3),
    (∀ k, IsPoly (p k)) ∧ (⋃ k, p k) = P ∧
    (Pairwise fun i j => Disjoint (interior (p i)) (interior (p j))) ∧
    (⋃ k, g k '' p k) = Q ∧
    (Pairwise fun i j => Disjoint (interior (g i '' p i)) (interior (g j '' p j)))
def IsSimilarCopy (P Q : Set R3) : Prop := ∃ a : ℝ, 0 < a ∧ ∃ g : R3 ≃ᵃⁱ[ℝ] R3, Q = g '' (a • P)

noncomputable def tetDihedral : ℝ := arccos (1 / 3)
noncomputable def wordAlpha : ℝ := Real.arccos (√5 / 5)
noncomputable def wordBeta : ℝ := Real.arccos ((3 - √5) / √(3 * (10 - 2 * √5)))
noncomputable def wordGamma : ℝ := Real.arccos (√5 / 3)

-- solids (all `sol n b`): tetraSet (corners (−1,−1,−1),(1,1,−1),(1,−1,1),(−1,1,1)); cubeSet s = [−s,s]³;
-- octSet = {|x|+|y|+|z| ≤ 1}; coSet t = {|xᵢ| ≤ 1, |x|+|y|+|z| ≤ t}; truncOctSet = coSet (3/2);
-- rdSet c = {|xᵢ ± xⱼ| ≤ c}; cubeRDSet s c = {|xᵢ| ≤ s, |xᵢ ± xⱼ| ≤ c}; rtSet r: normals the 30 vectors
-- ±4eᵢ and cyclic permutations of (±(√5−1), ±(√5+1), ±2), offset r; goldProlateSet, goldOblateSet: six of
-- these normals (proved equal to the parallelepipeds on three five-fold axes); dodSet (normals cyclic perms of
-- (0, ±2, ±(1+√5)), offsets 6+2√5); icoSet (normals (±2,±2,±2) and cyclic perms of (0, ±(1+√5), ±(√5−1)),
-- offsets 6+2√5). Quoted exactly: the three named solids.
noncomputable def cleoN : Fin 4 → R3 :=
  ![!₂[1, 1, 1], !₂[0, -2, √5 - 1], !₂[-2, √5 - 1, 0], !₂[√5 - 1, 0, -2]]
noncomputable def cleoB : Fin 4 → ℝ := ![-(1 + √5) / 4, (√5 - 1) / 2, (√5 - 1) / 2, (√5 - 1) / 2]
def cleoSet : Set R3 := sol cleoN cleoB
noncomputable def axeN : Fin 4 → R3 :=
  ![!₂[√5 - 1, 0, -2], !₂[-2, 1 - √5, 0], !₂[1, -1, 1], !₂[1 - √5, 1 + √5, 0]]
noncomputable def axeB : Fin 4 → ℝ := ![(3 + √5) / 2, (3 + √5) / 2, -(1 + √5) / 4, -(1 + √5) / 2]
def axeSet : Set R3 := sol axeN axeB
noncomputable def fujiN : Fin 7 → R3 :=
  ![!₂[√5 - 1, √5 + 1, 0], !₂[2, √5 - 1, 0], !₂[0, 2, √5 - 1], !₂[√5 + 1, 0, √5 - 1],
    !₂[√5 - 1, 0, 2], !₂[0, √5 - 1, √5 + 1], !₂[-1, -1, -1]]
noncomputable def fujiB : Fin 7 → ℝ :=
  ![-(5 + √5) / 2, -(3 + √5) / 2, -(3 + √5) / 2, -(5 + √5) / 2, -(3 + √5) / 2, -(5 + √5) / 2,
    (7 + 3 * √5) / 4]
def fujiSet : Set R3 := sol fujiN fujiB

theorem dehnSet_eq_of_scissorsCongruent {P Q : Set R3} (hP : IsPoly P) (hQ : IsPoly Q)
    (h : ScissorsCongruent P Q) : dehnSet P = dehnSet Q := by sorry
theorem word_angle_relation : wordAlpha + 2 * wordBeta - wordGamma = π := by sorry
theorem tet_word_angles_indep (p q r : ℚ)
    (h : (p : ℝ) * tetDihedral + q * wordAlpha + r * wordBeta ∈ ratPi) : p = 0 ∧ q = 0 ∧ r = 0 := by sorry
theorem dehnSet_co {t : ℝ} (ht1 : 1 < t) (ht2 : t < 2) :
    dehnSet (coSet t) = edgeTerm (12 * √2 * (2 * t - 3)) tetDihedral := by sorry
theorem dehnSet_fuji_ab : dehnSet fujiSet =
    (9 - 3 * ((√5 - 1) / 2)) ⊗ₜ[ℚ] (Submodule.Quotient.mk wordAlpha : Angle) +
      (12 - 3 * ((√5 - 1) / 2)) ⊗ₜ[ℚ] (Submodule.Quotient.mk wordBeta : Angle) := by sorry
theorem volume_eq_of_scissorsCongruent {P Q : Set R3} (h : ScissorsCongruent P Q) :
    volume P = volume Q := by sorry

def IsZeroWord (P : Set R3) : Prop := IsPoly P ∧ dehnSet P = 0
def IsNonzeroWord (P : Set R3) : Prop := IsPoly P ∧ dehnSet P ≠ 0
theorem zeroWords (s c r : ℝ) (hs : 0 < s) :
    IsZeroWord (cubeSet s) ∧ IsZeroWord (rdSet c) ∧ IsZeroWord (cubeRDSet s c) ∧ IsZeroWord (rtSet r) ∧
    IsZeroWord goldProlateSet ∧ IsZeroWord goldOblateSet ∧ IsZeroWord truncOctSet := by sorry
theorem nonzeroWords {t : ℝ} (ht1 : 1 < t) (ht2 : t < 2) (ht : t ≠ 3 / 2) :
    IsNonzeroWord dodSet ∧ IsNonzeroWord icoSet ∧ IsNonzeroWord tetraSet ∧ IsNonzeroWord octSet ∧
    IsNonzeroWord (coSet t) ∧ IsNonzeroWord cleoSet ∧ IsNonzeroWord axeSet ∧ IsNonzeroWord fujiSet := by sorry
def TetFamily (P : Set R3) : Prop :=
  P = octSet ∨ P = tetraSet ∨ ∃ t : ℝ, 1 < t ∧ t < 2 ∧ t ≠ 3 / 2 ∧ P = coSet t
def abWord : Fin 5 → Set R3 := ![dodSet, icoSet, cleoSet, axeSet, fujiSet]
def ABFamily (Q : Set R3) : Prop := ∃ i, Q = abWord i
theorem canon_complete :
    (∀ {P Q P' Q' : Set R3}, IsNonzeroWord P → IsZeroWord Q → IsSimilarCopy P P' → IsSimilarCopy Q Q' →
      ¬ ScissorsCongruent P' Q') ∧
    (∀ {i j : Fin 5} {P' Q' : Set R3}, i ≠ j → IsSimilarCopy (abWord i) P' → IsSimilarCopy (abWord j) Q' →
      ¬ ScissorsCongruent P' Q') ∧
    (∀ {P Q P' Q' : Set R3}, TetFamily P → ABFamily Q → IsSimilarCopy P P' → IsSimilarCopy Q Q' →
      ¬ ScissorsCongruent P' Q') ∧
    (∀ {P Q P' Q' : Set R3}, TetFamily P → TetFamily Q → P ≠ Q → IsSimilarCopy P P' →
      IsSimilarCopy Q Q' → ¬ ScissorsCongruent P' Q') := by sorry
end DehnCanon
```

Notes on the quotation: names, hypotheses and conclusions are copied from the files of studies 1–9; the base definitions are stated there for a general inner product space E and specialised here to R3; solid data in comments are summarised, exact in the files. Other proved values, not quoted: `dehnSet_oct` (−12√2 ⊗ θ), `dehnSet_dod` (−30(2√5−2) ⊗ α), `dehnSet_ico` (−120 ⊗ γ), `dehnSet_cleo_ab`, `dehnSet_axe_ab`, `word_angles_int_indep`, `volume_tetra`, `volume_oct`, `volume_co`, `dehnSet_cubeRD`, `dehnSet_rtFamily` (every `sol` with normals among the 30 two-fold vectors has invariant 0).

## Statements to score

D2. `canon_complete` with `zeroWords`, `nonzeroWords`, `tet_word_angles_indep`, `word_angle_relation` and the invariant values (score as one result group; the bridge and Dehn's theorem of D1 are its base).
