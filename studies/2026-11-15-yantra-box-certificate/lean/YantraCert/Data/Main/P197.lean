module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P197
open YantraCert

def cell : Cell := ⟨8, 82, 8, 3, 7, 31⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 9, 0, 0, 0, 9, 41, 25, 0, 0, 9, 0, 41, 0, 25, 25, 25, 25, 0, 0, 1, 0, 0, 0, 1, 0, 0, 41, 25, 0, 41, 25, 25, 9, 41, 0, 9, 0, 0, 0, 0, 0, 0, 9, 0, 41, 25, 1, 25, 0, 0, 0, 0, 41, 25, 0, 41, 25, 9, 25, 1, 41]

theorem ok : checkTree C 11 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P197
