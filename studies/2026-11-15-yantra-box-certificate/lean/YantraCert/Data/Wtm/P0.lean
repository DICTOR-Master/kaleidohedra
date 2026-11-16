module

public import YantraCert.Data.Wtm.Polys

@[expose] public section

namespace YantraCert.Data.Wtm.P0
open YantraCert

def cell : Cell := ⟨0, 0, 0, 0, 0, 0⟩
noncomputable def codes : TC := TC.ofList [0, 34, 0, 0, 34, 0, 66, 66, 0, 0, 42, 0, 66, 0, 2, 0, 42, 66, 0, 0, 34, 42, 0, 66, 0, 0, 42, 66, 0, 42, 66]

theorem ok : checkTree C 9 cell codes = true := by decide +kernel

end YantraCert.Data.Wtm.P0
