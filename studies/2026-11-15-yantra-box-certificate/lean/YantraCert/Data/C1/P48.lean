module

public import YantraCert.Data.C1.Polys

@[expose] public section

namespace YantraCert.Data.C1.P48
open YantraCert

def cell : Cell := ⟨7, 33, 7, 65, 6, 11⟩
noncomputable def codes : TC := TC.ofList [194]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.C1.P48
