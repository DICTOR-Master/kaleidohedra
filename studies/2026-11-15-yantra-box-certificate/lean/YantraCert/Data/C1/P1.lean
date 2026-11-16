module

public import YantraCert.Data.C1.Polys

@[expose] public section

namespace YantraCert.Data.C1.P1
open YantraCert

def cell : Cell := ⟨2, 0, 1, 1, 1, 0⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 1, 3, 41, 0, 0, 1, 3, 194, 1, 194]

theorem ok : checkTree C 7 cell codes = true := by decide +kernel

end YantraCert.Data.C1.P1
