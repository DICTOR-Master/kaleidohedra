/-
Lean formalization of DICTO's paper #117 (Zenodo 10.5281/zenodo.24411660). Part 9: Theorem 4 for tilings by
copies, with no hypothesis.

* `theorem4a_copies`: **Theorem 4 (a).** In a tiling of 3-space by convex polytopes (not necessarily
  face-to-face), each a similar copy (rigid motion, reflection, positive scaling) of the dodecahedron centre
  pyramid, the truncated icosahedron, the dodecahedron, the icosahedron, the truncated octahedron or the truncated
  cuboctahedron, or a convex polytope whose dihedral angles are all nonnegative rational multiples of π, no tile is a copy of the pyramid or of
  the truncated icosahedron.
* `theorem4b_copies`: **Theorem 4 (b)**, the same with the icosahedron centre pyramid and the truncated
  dodecahedron.
The paper's helper list also has the truncated icosidodecahedron; it is not built from coordinates here
(`theorem4a_tiling` covers it given its angles).
No `sorry`.
-/
module

public import Packets.Solids

@[expose] public section

open Set Module

namespace Packets

open DehnCanon.Library (R3)

lemma allowed_copy {Q S : Set R3} {L : List ℝ} (hc : SimilarCopy Q S) (hS : ∀ θ, EdgeAngle S θ ↔ θ ∈ L) :
    (∀ θ ∈ L, EdgeAngle Q θ) ∧ ∀ θ, EdgeAngle Q θ → θ ∈ L :=
  ⟨fun θ h => (hc.edgeAngle_iff θ).2 ((hS θ).2 h), fun θ h => (hS θ).1 ((hc.edgeAngle_iff θ).1 h)⟩

/-- A convex piece whose dihedral angles, read from the set, are nonnegative rational multiples of π. -/
def RationalAngles (P : Set R3) : Prop := ∀ θ, EdgeAngle P θ → ∃ q : ℚ, 0 ≤ q ∧ θ = q * Real.pi

/-- **Theorem 4 (a)** for tilings by copies, with no hypothesis. -/
theorem theorem4a_copies {ι : Type*} (T : ConvexTiling ι R3)
    (hk : ∀ i, SimilarCopy (T.P i) pyrDSet ∨ SimilarCopy (T.P i) tiSet ∨ SimilarCopy (T.P i) dhSet ∨
      SimilarCopy (T.P i) ihSet ∨ SimilarCopy (T.P i) toSet ∨ SimilarCopy (T.P i) tcoSet ∨
      RationalAngles (T.P i)) (i : ι) :
    ¬ SimilarCopy (T.P i) pyrDSet ∧ ¬ SimilarCopy (T.P i) tiSet := by
  classical
  let ang : ι → List ℝ := fun j =>
    if SimilarCopy (T.P j) pyrDSet then pyrD else if SimilarCopy (T.P j) tiSet then ti else
    if SimilarCopy (T.P j) dhSet then dod else if SimilarCopy (T.P j) ihSet then ico else
    if SimilarCopy (T.P j) toSet then toA else if SimilarCopy (T.P j) tcoSet then tcoA else []
  have H : ∀ j, (∀ θ ∈ ang j, EdgeAngle (T.P j) θ) ∧ AllowedA (ang j) (EdgeAngle (T.P j)) := by
    intro j
    simp only [ang]
    split_ifs with h1 h2 h3 h4 h5 h6
    · obtain ⟨a, b⟩ := allowed_copy h1 pyrD_edgeAngle; exact ⟨a, Or.inl ⟨Or.inl rfl, b⟩⟩
    · obtain ⟨a, b⟩ := allowed_copy h2 ti_edgeAngle; exact ⟨a, Or.inl ⟨Or.inr (Or.inl rfl), b⟩⟩
    · obtain ⟨a, b⟩ := allowed_copy h3 dh_edgeAngle; exact ⟨a, Or.inl ⟨Or.inr (Or.inr (Or.inl rfl)), b⟩⟩
    · obtain ⟨a, b⟩ := allowed_copy h4 ih_edgeAngle; exact ⟨a, Or.inl ⟨Or.inr (Or.inr (Or.inr (Or.inl rfl))), b⟩⟩
    · obtain ⟨a, b⟩ := allowed_copy h5 to_edgeAngle; exact ⟨a, Or.inl ⟨Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl rfl))))), b⟩⟩
    · obtain ⟨a, b⟩ := allowed_copy h6 tco_edgeAngle
      exact ⟨a, Or.inl ⟨Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr rfl))))), b⟩⟩
    · refine ⟨by simp, Or.inr ?_⟩
      rcases hk j with h | h | h | h | h | h | h
      · exact absurd h h1
      · exact absurd h h2
      · exact absurd h h3
      · exact absurd h h4
      · exact absurd h h5
      · exact absurd h h6
      · exact h
  obtain ⟨n1, n2, -⟩ := theorem4a_tiling T ang (fun j => (H j).1) (fun j => (H j).2) i
  refine ⟨fun h => n1 (by simp only [ang, if_pos h]), fun h => ?_⟩
  by_cases h1 : SimilarCopy (T.P i) pyrDSet
  · exact n1 (by simp only [ang, if_pos h1])
  · exact n2 (by simp only [ang, if_neg h1, if_pos h])

/-- **Theorem 4 (b)** for tilings by copies, with no hypothesis. -/
theorem theorem4b_copies {ι : Type*} (T : ConvexTiling ι R3)
    (hk : ∀ i, SimilarCopy (T.P i) pyrISet ∨ SimilarCopy (T.P i) tdSet ∨ SimilarCopy (T.P i) dhSet ∨
      SimilarCopy (T.P i) ihSet ∨ SimilarCopy (T.P i) toSet ∨ SimilarCopy (T.P i) tcoSet ∨
      RationalAngles (T.P i)) (i : ι) :
    ¬ SimilarCopy (T.P i) pyrISet ∧ ¬ SimilarCopy (T.P i) tdSet := by
  classical
  let ang : ι → List ℝ := fun j =>
    if SimilarCopy (T.P j) pyrISet then pyrI else if SimilarCopy (T.P j) tdSet then td else
    if SimilarCopy (T.P j) dhSet then dod else if SimilarCopy (T.P j) ihSet then ico else
    if SimilarCopy (T.P j) toSet then toA else if SimilarCopy (T.P j) tcoSet then tcoA else []
  have H : ∀ j, (∀ θ ∈ ang j, EdgeAngle (T.P j) θ) ∧ AllowedB (ang j) (EdgeAngle (T.P j)) := by
    intro j
    simp only [ang]
    split_ifs with h1 h2 h3 h4 h5 h6
    · obtain ⟨a, b⟩ := allowed_copy h1 pyrI_edgeAngle; exact ⟨a, Or.inl ⟨Or.inl rfl, b⟩⟩
    · obtain ⟨a, b⟩ := allowed_copy h2 td_edgeAngle; exact ⟨a, Or.inl ⟨Or.inr (Or.inl rfl), b⟩⟩
    · obtain ⟨a, b⟩ := allowed_copy h3 dh_edgeAngle; exact ⟨a, Or.inl ⟨Or.inr (Or.inr (Or.inl rfl)), b⟩⟩
    · obtain ⟨a, b⟩ := allowed_copy h4 ih_edgeAngle; exact ⟨a, Or.inl ⟨Or.inr (Or.inr (Or.inr (Or.inl rfl))), b⟩⟩
    · obtain ⟨a, b⟩ := allowed_copy h5 to_edgeAngle; exact ⟨a, Or.inl ⟨Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl rfl))))), b⟩⟩
    · obtain ⟨a, b⟩ := allowed_copy h6 tco_edgeAngle
      exact ⟨a, Or.inl ⟨Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr rfl))))), b⟩⟩
    · refine ⟨by simp, Or.inr ?_⟩
      rcases hk j with h | h | h | h | h | h | h
      · exact absurd h h1
      · exact absurd h h2
      · exact absurd h h3
      · exact absurd h h4
      · exact absurd h h5
      · exact absurd h h6
      · exact h
  obtain ⟨n1, n2, -⟩ := theorem4b_tiling T ang (fun j => (H j).1) (fun j => (H j).2) i
  refine ⟨fun h => n1 (by simp only [ang, if_pos h]), fun h => ?_⟩
  by_cases h1 : SimilarCopy (T.P i) pyrISet
  · exact n1 (by simp only [ang, if_pos h1])
  · exact n2 (by simp only [ang, if_neg h1, if_pos h])

end Packets
