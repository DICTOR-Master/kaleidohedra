module

public import YantraCert.Data.Wtp.Polys

@[expose] public section

namespace YantraCert.Data.Wtp.P3
open YantraCert

def cell : Cell := ⟨2, 2, 2, 2, 1, 1⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 41, 41, 0, 41, 0, 41, 41, 82]

theorem ok : checkTree C 6 cell codes = true := by decide +kernel

end YantraCert.Data.Wtp.P3
