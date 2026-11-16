module

public import YantraCert.Data.C2.Polys

@[expose] public section

namespace YantraCert.Data.C2.P0
open YantraCert

def cell : Cell := ⟨0, 0, 0, 0, 0, 0⟩
noncomputable def codes : TC := TC.ofList [2]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.C2.P0
