module

public import YantraCert.Data.C1.Polys

@[expose] public section

namespace YantraCert.Data.C1.P133
open YantraCert

def cell : Cell := ⟨7, 41, 7, 64, 7, 22⟩
noncomputable def codes : TC := TC.ofList [1]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.C1.P133
