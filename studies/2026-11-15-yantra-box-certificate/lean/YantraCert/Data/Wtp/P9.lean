module

public import YantraCert.Data.Wtp.Polys

@[expose] public section

namespace YantraCert.Data.Wtp.P9
open YantraCert

def cell : Cell := ⟨3, 7, 2, 3, 2, 2⟩
noncomputable def codes : TC := TC.ofList [0, 114, 0, 0, 0, 25, 25, 26, 0, 0, 18, 0, 0, 25, 25, 0, 25, 25, 0, 114, 26]

theorem ok : checkTree C 8 cell codes = true := by decide +kernel

end YantraCert.Data.Wtp.P9
