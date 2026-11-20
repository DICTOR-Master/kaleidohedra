# Candidate G1: an example for Grünbaum's zone question at k = 10 (a Lean development)

## Abstract (neutral)

A parallelohedron (in Grünbaum's sense) is a polyhedron whose translated copies tile space. A zone (belt) of a polyhedron whose faces are parallelograms is the cyclic sequence of faces reached by crossing sides parallel to one direction. Grünbaum (2010) asked, for even k ≥ 4, whether there is a rhombic monohedral parallelohedron (all faces congruent rhombi) with every zone of exactly k faces; examples are classical for k = 4, 6 and were given by Grünbaum for k = 8, and he wrote that "no information is available for any k ≥ 10". Convex parallelohedra have zones of 4 or 6 only (Venkov, McMullen), so any example for k ≥ 8 is nonconvex.

The entry gives a Lean 4 / Mathlib proof of an example for k = 10. The witness, called GET A by the submitter, is the rhombic triacontahedron less four oblate golden rhombohedra: a union of 16 golden rhombohedra (10 prolate, 6 oblate) on the six 5-fold axes of the icosahedron, with 30 congruent golden rhombic faces, 32 vertices, 60 edges, six zones of exactly 10 faces each, surface homeomorphic to a sphere, no two adjacent faces coplanar, and a face-to-face lattice tiling of space by its translates (volume = covolume = 20 + 32φ in the units of the model). A second solid of the same kind, GET B, has the same lattice and the same 16 cell types arranged differently and is not congruent to GET A even allowing reflections (checked by exact computation outside Lean over the 120 symmetries of the six-axis star, which are the only candidate congruences because a congruence must preserve the six edge directions). This mirrors Grünbaum's k = 8 pair D1, D2.

Facts on the proof: Lean v4.35.0-rc2, Mathlib v4.35.0-rc2, module system; 4,174 Lean lines (861 generated from exact certificates by Python scripts; all certificates re-decided in the kernel with `decide +kernel`; no `native_decide`, no `sorry`, no added axiom). `#print axioms` on all four Comparator theorems gives only `propext`, `Classical.choice`, `Quot.sound`. Palomar's comparator template accepts the Solution with Lean's kernel, NanoDa and con-ron. Main proof steps: exact ℤ[φ] arithmetic with a verified embedding into ℝ; zone certificates with a generic soundness lemma; separation of the 16 cells and of the 26 neighbouring translates (6,656 cell pairs); volume = covolume and `ZSpan.isAddFundamentalDomain'` for the cover; frontier = union of the 30 faces via contact analysis; faces meet properly (870 ordered pairs); the sphere via a radial-projection homeomorphism from an interior point with 435 cone-separation certificates. Two calibration theorems check that the zone definition gives 4 for the cube and 6 for the rhombic dodecahedron, so it does not force the answer.

Limits stated by the author: the statement is existential (one witness, GET A); GET B is not in the Comparator theorems (its no-overlap checks are in the library as a side file); the non-congruence of GET A and GET B is verified by exact computation outside Lean; k ≥ 12 is not addressed; the lattice face-to-face tiling is stronger than Grünbaum's notion, and `FaceToFace` is a per-face condition; faces are modelled as parallelograms.

## The published question and prior work (sources, exact citations)

- **B. Grünbaum**, "The Bilinski dodecahedron, and assorted parallelohedra, zonohedra, monohedra, isozonohedra and otherhedra", *Math. Intelligencer* 32(4) (2010) 5–15, doi:10.1007/s00283-010-9138-7. Read in the author's version (University of Washington repository, hdl 1773/15593, version 2/3/10). Open problem (author's version p. 17): "Given an even integer k ≥ 4, is there a rhombic monohedral parallelohedron such that every zone has exactly k faces? … No information is available for any k ≥ 10." Known cases: k = 4 the cube; k = 6 the rhombic dodecahedra of Kepler and of Bilinski; k = 8 Grünbaum's two doubly indented rhombic icosahedra D1, D2 (the rhombic icosahedron less two oblate golden rhombohedra). On indentations (author's version p. 15): "An eightfold indentation of the triacontahedron T is shown in [Williams, Natural Structure, p. 196] … None of the other isozonohedra obtainable by indentation of F or T seem to be parallelohedra." Grünbaum's polyhedra are of spherical type, with adjacent faces never coplanar (p. 9).
- **B. Grünbaum**, "Tilings by some nonconvex parallelohedra", *Geombinatorics* 19 (2010) 100–107 (read in full): crosses and semicrosses of cubes; nothing for k ≥ 10.
- **G. Inchbald**, "A 3-D Quasicrystal Structure?", steelpillow.com (web page, updated 6 Dec 2024), section "Tilings and the dimpled rhombic triacontahedron" (read). The rhombic triacontahedron with four of its eight cube-corner vertex triplets dimpled, alternating with tetrahedral symmetry (an oblate golden rhombohedron scooped out at each), described as a space-filler with cubic periodicity. Internet Archive: the dimpling text is absent on 31 Mar 2022 and present on 23 Mar 2023. Inchbald does not mention zones or Grünbaum's question. **This solid is itself a k = 10 example of the same family (four corner indentations of the triacontahedron), published on the web before the submitter's work.** The submitter's computation identifies it as a third solid of that family, with the 12 rotations of the tetrahedral group; it is not congruent to GET A (4 symmetries) or GET B (3 rotations). The submitter's exact computation (in ℚ(φ), outside Lean) confirms that it tiles space by translation on a lattice. It is not the witness of this entry.
- **M. Senechal, J. Taylor**, "Parallelohedra, old and new", *Acta Cryst. A* 79 (2023) 273–279, doi:10.1107/S2053273323001444. **Not read** (closed access; no free copy found via Unpaywall, Europe PMC or arXiv). Abstract (read): three new nonconvex parallelohedra built from skeletons of Fedorov's five convex parallelohedra, and "a counterexample to a statement by Grünbaum". Private correspondence (20 November 2026): M. Senechal wrote to the submitter that GET A/B and the Senechal–Taylor solids only share similarities, i.e. GET A and GET B are not among their three. This is disclosed as unverifiable correspondence; no priority is claimed from it.
- **N. Hungerbühler, J. Hungerbühler, M. Pirron**, "New families of monohedral polyhedra", *J. Math. Arts* 19 (2025) 1–23 (read): monohedra and monohedral zonohedra; no parallelohedra or tilings.
- G. Hart, *Virtual Polyhedra*, page on the dissection of the rhombic triacontahedron into 20 golden rhombohedra (read); Hafner & Zitko, "Introduction to golden rhombic polyhedra" (VisMath, read): nothing on sub-assemblies that tile.
- **B. A. Venkov** (1954), **P. McMullen** (1980): a convex parallelohedron has belts (zones) of 4 or 6 faces only; so every example with k ≥ 8 is nonconvex.
- **R. Ammann** (1976), **P. Kramer** (1982): the prolate and oblate golden rhombohedra are the cells of the three-dimensional Penrose tiling.
- Not read: R. Williams, *Natural Structure* (1972), p. 196 (the eightfold indentation Grünbaum cites).
- Web searches used: "Senechal Taylor parallelohedra nonconvex arXiv"; "nonconvex parallelohedron golden rhombi rhombic triacontahedron indented"; "Hungerbühler Pirron New families of monohedral polyhedra"; "George Hart golden rhombohedra assemblies space filling"; OpenAlex citers of Grünbaum 2010 (none answers the question).

Prior formalizations: Mathlib contains `ZSpan` fundamental domains but, to the submitter's knowledge, no parallelohedra and no zones of polyhedra. The submitter has not run a systematic search of other proof libraries.

Prior work by the same author: an unpublished computational study (15 November 2026, not peer reviewed), which found GET A and GET B and checked them in exact arithmetic in ℤ[φ]. No publication.

What is claimed: a machine-checked example of a rhombic monohedral parallelohedron of spherical type with every zone of exactly 10 faces (Grünbaum's question at k = 10), with a face-to-face lattice tiling. The witness GET A (and its non-congruent companion GET B) was not found in the sources checked above. It is not claimed to be the first k = 10 example: Inchbald's dimpled triacontahedron (web, by March 2023) is an earlier example of the same family, though it was not presented as an answer to Grünbaum's question and has no published proof.

## The Lean statements (the Challenge file, verbatim)

The full Challenge file follows. One word is changed: the witness docstring names the solid by the submitter's own name for it, replaced here by `the submitter's solid "GET A"`. The Comparator configuration lists the theorems `GrunbaumK10.cube_everyZoneHas`, `GrunbaumK10.rhombicDodecahedron_everyZoneHas`, `GrunbaumK10.grunbaum_k10`, `GrunbaumK10.grunbaum_k10_parallelohedron` (in this order), no definitions, axioms `propext`, `Quot.sound`, `Classical.choice`.

```lean
module

public import Mathlib

@[expose] public section

/-!
# Grünbaum's zone question at k = 10

**Informal statement.** There is a polyhedron `P` in Euclidean 3-space with these properties.

* `P` is a polyhedron of spherical type in Grünbaum's sense (2010, p. 9): its surface is homeomorphic to a sphere and
  adjacent faces are not coplanar. Here `P` is the solid: a compact set equal to the closure of its interior, whose
  frontier is the union of its 30 parallelogram faces; the 30 faces are distinct, and two faces meet in a common side,
  a common corner, or not at all.
* `P` is rhombic and monohedral: every face is a rhombus, any two faces are congruent, and the diagonals of every face
  are in the golden ratio.
* Every zone of `P` has exactly 10 faces. A zone is a belt: start from a face and one of its side directions `w`, and
  pass repeatedly to the face across a side parallel to `w`; the zone is the set of faces reached. The statement also
  says that each belt is the set of all faces with a side parallel to `w`. Two calibration theorems check this
  definition on known solids: it gives 4 for the cube and 6 for the rhombic dodecahedron.
* `P` is a parallelohedron: its translates by the vectors of a lattice cover space and have pairwise disjoint
  interiors. The tiling is moreover face to face, in the per-face sense of `FaceToFace`: every face of `P` is also a
  face of a translate of `P` by a non-zero lattice vector.

This gives an example for `k = 10` for the question of B. Grünbaum, "The Bilinski dodecahedron, and assorted
parallelohedra, zonohedra, monohedra, isozonohedra and otherhedra", *Math. Intelligencer* 32(4) (2010) 5–15: "Given an
even integer k ≥ 4, is there a rhombic monohedral parallelohedron such that every zone has exactly k faces?" Grünbaum
defines a parallelohedron as a polyhedron that admits a tiling of space by translated copies of itself; a lattice
tiling is a special case, so the main statement here is stronger. The second theorem states the result in his terms.

**Witness (in the Solution, not part of the statement).** the submitter's solid "GET A": the
rhombic triacontahedron less four oblate golden rhombohedra, the union of 16 golden rhombohedra.
-/

namespace GrunbaumK10

open Set
open scoped Pointwise

/-- Euclidean 3-space -/
abbrev Space := EuclideanSpace ℝ (Fin 3)

/-- a parallelogram `p + [0,1] u + [0,1] v` -/
structure Parallelogram where
  p : Space
  u : Space
  v : Space

namespace Parallelogram

/-- the closed parallelogram as a set -/
def carrier (F : Parallelogram) : Set Space :=
  {x | ∃ s ∈ Icc (0 : ℝ) 1, ∃ t ∈ Icc (0 : ℝ) 1, x = F.p + s • F.u + t • F.v}

/-- the four corners, in cyclic order -/
def corners (F : Parallelogram) : Fin 4 → Space :=
  ![F.p, F.p + F.u, F.p + F.u + F.v, F.p + F.v]

/-- the four sides, side `i` joining corner `i` to corner `i + 1` -/
def side (F : Parallelogram) (i : Fin 4) : Set Space :=
  segment ℝ (F.corners i) (F.corners (i + 1))

/-- the parallelogram is not degenerate -/
def Nondegenerate (F : Parallelogram) : Prop := LinearIndependent ℝ ![F.u, F.v]

/-- a rhombus: a non-degenerate parallelogram with equal sides -/
def IsRhombus (F : Parallelogram) : Prop := F.Nondegenerate ∧ ‖F.u‖ = ‖F.v‖

/-- a golden rhombus: a rhombus whose long diagonal is the golden ratio times its short diagonal -/
def IsGoldenRhombus (F : Parallelogram) : Prop :=
  F.IsRhombus ∧ (‖F.u + F.v‖ = Real.goldenRatio * ‖F.u - F.v‖ ∨ ‖F.u - F.v‖ = Real.goldenRatio * ‖F.u + F.v‖)

/-- `w` is parallel to a side of the parallelogram -/
def HasSideParallel (F : Parallelogram) (w : Space) : Prop :=
  (∃ c : ℝ, c ≠ 0 ∧ F.u = c • w) ∨ (∃ c : ℝ, c ≠ 0 ∧ F.v = c • w)

end Parallelogram

/-- Two parallelograms are congruent: their corners are congruent point sets (Mathlib's `Congruent`, after some
relabelling of the corners). -/
def FacesCongruent (F G : Parallelogram) : Prop :=
  ∃ σ : Equiv.Perm (Fin 4), Congruent (F.corners ∘ σ) G.corners

/-- the faces `F i` and `F j` share a side -/
def Adjacent {m : ℕ} (F : Fin m → Parallelogram) (i j : Fin m) : Prop :=
  ∃ a b : Fin 4, (F i).side a = (F j).side b

/-- two faces meet in a common side, in a common corner, or not at all -/
def MeetProperly (F G : Parallelogram) : Prop :=
  F.carrier ∩ G.carrier = ∅ ∨
  (∃ a b : Fin 4, F.corners a = G.corners b ∧ F.carrier ∩ G.carrier = {F.corners a}) ∨
  (∃ a b : Fin 4, F.side a = G.side b ∧ F.carrier ∩ G.carrier = F.side a)

/-- `P` is a polyhedron of spherical type with the faces `F`: a compact solid, the closure of its interior, whose
frontier is the union of the faces and is homeomorphic to a sphere; the faces are non-degenerate and distinct, meet
properly, and adjacent faces are not coplanar (Grünbaum 2010, p. 9). -/
structure IsSphericalPolyhedron {m : ℕ} (P : Set Space) (F : Fin m → Parallelogram) : Prop where
  compact : IsCompact P
  closure_interior : closure (interior P) = P
  frontier_eq : frontier P = ⋃ i, (F i).carrier
  nondegenerate : ∀ i, (F i).Nondegenerate
  distinct : ∀ i j, (F i).carrier = (F j).carrier → i = j
  meet : ∀ i j, i ≠ j → MeetProperly (F i) (F j)
  sphere : Nonempty (frontier P ≃ₜ Metric.sphere (0 : Space) 1)
  not_coplanar : ∀ i j, i ≠ j → Adjacent F i j →
    ¬ Coplanar ℝ (range (F i).corners ∪ range (F j).corners)

/-- rhombic and monohedral: every face is a rhombus and any two faces are congruent -/
def IsRhombicMonohedral {m : ℕ} (F : Fin m → Parallelogram) : Prop :=
  (∀ i, (F i).IsRhombus) ∧ ∀ i j, FacesCongruent (F i) (F j)

/-- faces `i` and `j` share a side parallel to `w` -/
def AcrossSideParallel {m : ℕ} (F : Fin m → Parallelogram) (w : Space) (i j : Fin m) : Prop :=
  ∃ a b : Fin 4, (F i).side a = (F j).side b ∧
    ∃ c : ℝ, c ≠ 0 ∧ (F i).corners (a + 1) - (F i).corners a = c • w

/-- the zone (belt) through face `i` in the direction `w`: the faces reached from `i` by crossing sides parallel
to `w` -/
def zone {m : ℕ} (F : Fin m → Parallelogram) (i : Fin m) (w : Space) : Set (Fin m) :=
  {j | Relation.ReflTransGen (AcrossSideParallel F w) i j}

/-- every zone has exactly `k` faces, and it consists of all faces with a side parallel to its direction -/
def EveryZoneHas {m : ℕ} (F : Fin m → Parallelogram) (k : ℕ) : Prop :=
  ∀ i, ∀ w ∈ ({(F i).u, (F i).v} : Set Space),
    (zone F i w).ncard = k ∧ zone F i w = {j | (F j).HasSideParallel w}

/-- the lattice spanned by `b` -/
def lattice (b : Fin 3 → Space) : Set Space := AddSubgroup.closure (range b)

/-- the translates `t + P`, `t ∈ T`, cover space and have pairwise disjoint interiors -/
def TilesByTranslates (P : Set Space) (T : Set Space) : Prop :=
  (⋃ t ∈ T, t +ᵥ P) = univ ∧ T.Pairwise fun s t => Disjoint (interior (s +ᵥ P)) (interior (t +ᵥ P))

/-- Grünbaum's parallelohedron: some set of translates of `P` tiles space -/
def IsParallelohedron (P : Set Space) : Prop := ∃ T : Set Space, TilesByTranslates P T

/-- face to face, per face: every face of `P` is also a face of a translate of `P` by a non-zero vector of `T`
(together with `MeetProperly`, the frontier condition and disjoint interiors this gives the usual notion) -/
def FaceToFace {m : ℕ} (F : Fin m → Parallelogram) (T : Set Space) : Prop :=
  ∀ i, ∃ t ∈ T, t ≠ 0 ∧ ∃ j, t +ᵥ (F j).carrier = (F i).carrier

/-- the six faces of the unit cube `[0,1]³` (calibration of `EveryZoneHas`) -/
def cubeFaces : Fin 6 → Parallelogram := ![
  ⟨!₂[0, 0, 0], !₂[0, 1, 0], !₂[0, 0, 1]⟩,
  ⟨!₂[1, 0, 0], !₂[0, 1, 0], !₂[0, 0, 1]⟩,
  ⟨!₂[0, 0, 0], !₂[1, 0, 0], !₂[0, 0, 1]⟩,
  ⟨!₂[0, 1, 0], !₂[1, 0, 0], !₂[0, 0, 1]⟩,
  ⟨!₂[0, 0, 0], !₂[1, 0, 0], !₂[0, 1, 0]⟩,
  ⟨!₂[0, 0, 1], !₂[1, 0, 0], !₂[0, 1, 0]⟩]

/-- the twelve faces of the rhombic dodecahedron with vertices `(±1, ±1, ±1)` and `(±2, 0, 0)`, `(0, ±2, 0)`,
`(0, 0, ±2)` (calibration of `EveryZoneHas`) -/
def rhombicDodecahedronFaces : Fin 12 → Parallelogram := ![
  ⟨!₂[1, 1, -1], !₂[1, -1, 1], !₂[-1, 1, 1]⟩,
  ⟨!₂[1, -1, -1], !₂[1, 1, 1], !₂[-1, -1, 1]⟩,
  ⟨!₂[-1, 1, -1], !₂[-1, -1, 1], !₂[1, 1, 1]⟩,
  ⟨!₂[-1, -1, -1], !₂[-1, 1, 1], !₂[1, -1, 1]⟩,
  ⟨!₂[1, -1, 1], !₂[1, 1, -1], !₂[-1, 1, 1]⟩,
  ⟨!₂[1, -1, -1], !₂[1, 1, 1], !₂[-1, 1, -1]⟩,
  ⟨!₂[-1, -1, 1], !₂[-1, 1, -1], !₂[1, 1, 1]⟩,
  ⟨!₂[-1, -1, -1], !₂[-1, 1, 1], !₂[1, 1, -1]⟩,
  ⟨!₂[-1, 1, 1], !₂[1, 1, -1], !₂[1, -1, 1]⟩,
  ⟨!₂[-1, 1, -1], !₂[1, 1, 1], !₂[1, -1, -1]⟩,
  ⟨!₂[-1, -1, 1], !₂[1, -1, -1], !₂[1, 1, 1]⟩,
  ⟨!₂[-1, -1, -1], !₂[1, -1, 1], !₂[1, 1, -1]⟩]

-- END DEFINITIONS

/-- **Calibration: the zones of the cube have 4 faces.** -/
theorem cube_everyZoneHas : EveryZoneHas cubeFaces 4 := by
  sorry

/-- **Calibration: the zones of the rhombic dodecahedron have 6 faces.** -/
theorem rhombicDodecahedron_everyZoneHas : EveryZoneHas rhombicDodecahedronFaces 6 := by
  sorry

/-- **An example for Grünbaum's question at k = 10**: a polyhedron of spherical type with exactly 30 faces, all of
them congruent golden rhombi, every zone of exactly 10 faces, that tiles space face to face by the translates of a
lattice. -/
theorem grunbaum_k10 :
    ∃ (P : Set Space) (F : Fin 30 → Parallelogram) (b : Fin 3 → Space),
      IsSphericalPolyhedron P F ∧ IsRhombicMonohedral F ∧ (∀ i, (F i).IsGoldenRhombus) ∧
      EveryZoneHas F 10 ∧ LinearIndependent ℝ b ∧ TilesByTranslates P (lattice b) ∧
      FaceToFace F (lattice b) := by
  sorry

/-- in Grünbaum's own terms: a rhombic monohedral parallelohedron of spherical type with every zone of 10 faces -/
theorem grunbaum_k10_parallelohedron :
    ∃ (m : ℕ) (P : Set Space) (F : Fin m → Parallelogram),
      IsSphericalPolyhedron P F ∧ IsRhombicMonohedral F ∧ EveryZoneHas F 10 ∧ IsParallelohedron P := by
  sorry

end GrunbaumK10
```

## Statement to score

G1. `grunbaum_k10` and `grunbaum_k10_parallelohedron` (the example for k = 10), with the calibration theorems `cube_everyZoneHas` and `rhombicDodecahedron_everyZoneHas` (score as one result group). The non-congruent second solid GET B is part of the informal account, not of the Comparator theorems.
