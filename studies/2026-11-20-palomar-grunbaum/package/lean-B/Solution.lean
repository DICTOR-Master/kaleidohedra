module

public import Mathlib
public import GET.Main

@[expose] public section

/-!
# Grünbaum's zone question at k = 10 (proved)

**Informal statement.** There is a polyhedron `P` in Euclidean 3-space with these properties.

* `P` is a polyhedron of spherical type in Grünbaum's sense (2010, author's version, p. 11): its surface is homeomorphic to a sphere and
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

**Witness.** DICTO's Grünbaum–Escher Triacontahedron (GET B): the
rhombic triacontahedron less four oblate golden rhombohedra, the union of 16 golden rhombohedra.
-/

namespace GrunbaumK10


/-- **Calibration: the zones of the cube have 4 faces.** -/
theorem cube_everyZoneHas : EveryZoneHas cubeFaces 4 := GET.cube_zones

/-- **Calibration: the zones of the rhombic dodecahedron have 6 faces.** -/
theorem rhombicDodecahedron_everyZoneHas : EveryZoneHas rhombicDodecahedronFaces 6 := GET.rd_zones

/-- **An example for Grünbaum's question at k = 10**: a polyhedron of spherical type with exactly 30 faces, all of
them congruent golden rhombi, every zone of exactly 10 faces, that tiles space face to face by the translates of a
lattice. -/
theorem grunbaum_k10 :
    ∃ (P : Set Space) (F : Fin 30 → Parallelogram) (b : Fin 3 → Space),
      IsSphericalPolyhedron P F ∧ IsRhombicMonohedral F ∧ (∀ i, (F i).IsGoldenRhombus) ∧
      EveryZoneHas F 10 ∧ LinearIndependent ℝ b ∧ TilesByTranslates P (lattice b) ∧
      FaceToFace F (lattice b) :=
  ⟨GET.PB, GET.FB, GET.bB, GET.PB_spherical, GET.FB_rhombicMonohedral, GET.FB_golden, GET.FB_zones, GET.bB_li,
    GET.PB_tiles, GET.FB_faceToFace⟩

/-- in Grünbaum's own terms: a rhombic monohedral parallelohedron of spherical type with every zone of 10 faces -/
theorem grunbaum_k10_parallelohedron :
    ∃ (m : ℕ) (P : Set Space) (F : Fin m → Parallelogram),
      IsSphericalPolyhedron P F ∧ IsRhombicMonohedral F ∧ EveryZoneHas F 10 ∧ IsParallelohedron P :=
  ⟨30, GET.PB, GET.FB, GET.PB_spherical, GET.FB_rhombicMonohedral, GET.FB_zones, ⟨lattice GET.bB, GET.PB_tiles⟩⟩

end GrunbaumK10
