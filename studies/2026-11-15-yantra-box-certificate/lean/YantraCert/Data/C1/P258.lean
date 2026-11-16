module

public import YantraCert.Data.C1.Polys

@[expose] public section

namespace YantraCert.Data.C1.P258
open YantraCert

def cell : Cell := ⟨7, 63, 7, 65, 6, 12⟩
noncomputable def codes : TC := TC.ofList [0, 0, 41, 41, 1]

theorem ok : checkTree C 4 cell codes = true := by decide +kernel

end YantraCert.Data.C1.P258
