module

public import YantraCert.Data.Wtp.Polys

@[expose] public section

namespace YantraCert.Data.Wtp.P4
open YantraCert

def cell : Cell := ⟨3, 4, 2, 3, 2, 2⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 41, 41, 0, 25, 25, 0, 41, 41, 0, 0, 0, 41, 9, 0, 25, 9, 0, 0, 41, 0, 41, 41, 0, 41, 0, 0, 41, 41, 41]

theorem ok : checkTree C 8 cell codes = true := by decide +kernel

end YantraCert.Data.Wtp.P4
