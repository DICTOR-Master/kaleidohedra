module

public import YantraCert.Data.Wtp.Polys

@[expose] public section

namespace YantraCert.Data.Wtp.P8
open YantraCert

def cell : Cell := ⟨3, 6, 2, 3, 2, 2⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 25, 25, 0, 0, 25, 25, 114, 0, 0, 0, 25, 9, 0, 25, 9, 0, 0, 0, 25, 0, 25, 25, 0, 25, 0, 25, 25, 0, 0, 25, 25, 0, 25, 0, 25, 25]

theorem ok : checkTree C 8 cell codes = true := by decide +kernel

end YantraCert.Data.Wtp.P8
