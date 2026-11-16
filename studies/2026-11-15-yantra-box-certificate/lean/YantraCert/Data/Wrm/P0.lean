module

public import YantraCert.Data.Wrm.Polys

@[expose] public section

namespace YantraCert.Data.Wrm.P0
open YantraCert

def cell : Cell := ⟨0, 0, 0, 0, 0, 0⟩
noncomputable def codes : TC := TC.ofList [1]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Wrm.P0
