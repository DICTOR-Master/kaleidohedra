module

public import YantraCert.Data.A.Polys

@[expose] public section

namespace YantraCert.Data.A.P0
open YantraCert

def cell : Cell := ⟨0, 0, 0, 0, 0, 0⟩
noncomputable def codes : TC := TC.ofList [18]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.A.P0
