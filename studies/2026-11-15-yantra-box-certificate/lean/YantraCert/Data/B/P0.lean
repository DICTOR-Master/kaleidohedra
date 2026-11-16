module

public import YantraCert.Data.B.Polys

@[expose] public section

namespace YantraCert.Data.B.P0
open YantraCert

def cell : Cell := ⟨0, 0, 0, 0, 0, 0⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 0, 1, 130, 66, 0, 0, 1, 130, 0, 1, 82, 0, 0, 130, 66, 0, 130, 0, 9, 1, 0, 0, 0, 0, 1, 66, 178, 0, 0, 1, 0, 82, 82, 178, 0, 0, 82, 178, 0, 0, 122, 1, 178, 0, 0, 0, 0, 0, 1, 0, 130, 138, 0, 1, 0, 82, 90, 0, 0, 1, 0, 138, 0, 34, 2, 0, 1, 0, 0, 2, 82, 0, 2, 0, 122, 114, 0, 0, 154, 0, 0, 9, 0, 9, 9, 1, 0, 0, 9, 1, 0, 0, 0, 9, 122, 0, 9, 122, 9, 0, 0, 0, 0, 1, 0, 0, 82, 0, 114, 114, 0, 0, 122, 114, 0, 9, 114, 178, 0, 0, 1, 0, 0, 0, 122, 114, 0, 9, 122, 0, 0, 9, 122, 0, 9, 122, 178, 0, 0, 0, 0, 122, 0, 122, 122, 9, 178, 0, 0, 0, 0, 122, 0, 9, 9, 0, 0, 9, 9, 0, 122, 9, 9, 178]

theorem ok : checkTree C 11 cell codes = true := by decide +kernel

end YantraCert.Data.B.P0
