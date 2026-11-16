module

public import YantraCert.Data.C1.Polys

@[expose] public section

namespace YantraCert.Data.C1.P83
open YantraCert

def cell : Cell := ⟨7, 36, 7, 64, 7, 23⟩
noncomputable def codes : TC := TC.ofList [9]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.C1.P83
