module

public import YantraCert.Data.Wtp.Polys

@[expose] public section

namespace YantraCert.Data.Wtp.P1
open YantraCert

def cell : Cell := ⟨1, 1, 1, 0, 0, 0⟩
noncomputable def codes : TC := TC.ofList [0, 0, 41, 98, 0, 98, 98]

theorem ok : checkTree C 4 cell codes = true := by decide +kernel

end YantraCert.Data.Wtp.P1
