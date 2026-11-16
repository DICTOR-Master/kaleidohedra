module

public import YantraCert.Data.Wtp.Polys

@[expose] public section

namespace YantraCert.Data.Wtp.P10
open YantraCert

def cell : Cell := ⟨2, 3, 2, 3, 2, 3⟩
noncomputable def codes : TC := TC.ofList [0, 0, 82, 0, 0, 0, 9, 0, 82, 9, 0, 82, 0, 0, 25, 25, 82, 82, 0, 82, 0, 0, 0, 82, 0, 0, 25, 25, 82, 0, 114, 0, 0, 25, 25, 0, 25, 25, 82]

theorem ok : checkTree C 9 cell codes = true := by decide +kernel

end YantraCert.Data.Wtp.P10
