module

public import GET.Data

@[expose] public section

/-! Kernel checks of the exact facts of GET B (pilot). Every proof is `decide +kernel`. -/

namespace GET

theorem oneRhombus_ok : oneRhombus = true := by decide +kernel
theorem threeIndependent_ok : threeIndependent = true := by decide +kernel


section B
theorem B_faces_boundary : facesAreBoundary cellsB facesB = true := by decide +kernel
theorem B_zones : ∀ c : Fin 6, zoneSize facesB c = 10 := by decide +kernel
theorem B_edgeManifold : edgeManifold facesB = true := by decide +kernel
theorem B_V : nVertices facesB = 32 := by decide +kernel
theorem B_E : nSides facesB = 60 := by decide +kernel
theorem B_adjacent : adjacentNotCoplanar facesB = true := by decide +kernel
theorem B_vol : volEqCovol cellsB basisB = true := by decide +kernel
theorem B_match : faceMatch facesB basisB matchB = true := by decide +kernel
theorem B_star : starFromCentre facesB = true := by decide +kernel
theorem B_cells_separated : cellsSeparated cellsB = true := by decide +kernel
end B

end GET
