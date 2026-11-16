module

public import YantraCert.Data.Wtp.Polys

@[expose] public section

namespace YantraCert.Data.Wtp.P7
open YantraCert

def cell : Cell := ⟨2, 3, 2, 2, 1, 1⟩
noncomputable def codes : TC := TC.ofList [114]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Wtp.P7
