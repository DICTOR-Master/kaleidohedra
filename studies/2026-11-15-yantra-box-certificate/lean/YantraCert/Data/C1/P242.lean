module

public import YantraCert.Data.C1.Polys

@[expose] public section

namespace YantraCert.Data.C1.P242
open YantraCert

def cell : Cell := ⟨8, 121, 7, 64, 7, 24⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 9, 0, 0, 25, 25, 0, 25, 25, 25, 0, 0, 1, 0, 0, 25, 25, 0, 25, 25, 25, 0, 1, 0, 0, 25, 41, 0, 25, 41, 0, 0, 1, 0, 0, 0, 1, 0, 0, 25, 25, 0, 25, 25, 25, 0, 0, 1, 0, 0, 25, 25, 0, 25, 25, 25, 0, 1, 0, 0, 25, 41, 0, 25, 41, 1, 0, 0, 41, 41, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 25, 25, 0, 25, 25, 25, 0, 0, 1, 0, 0, 25, 25, 0, 25, 25, 25, 0, 1, 0, 0, 25, 41, 0, 25, 41, 0, 0, 1, 0, 0, 0, 1, 0, 0, 25, 25, 0, 25, 25, 25, 0, 0, 1, 0, 0, 25, 25, 0, 25, 25, 25, 0, 1, 0, 0, 25, 41, 0, 25, 41, 1, 0, 0, 41, 41, 1, 1, 0, 0, 41, 41, 1]

theorem ok : checkTree C 15 cell codes = true := by decide +kernel

end YantraCert.Data.C1.P242
