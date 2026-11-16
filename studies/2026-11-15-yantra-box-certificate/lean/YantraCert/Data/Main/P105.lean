module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P105
open YantraCert

def cell : Cell := ⟨8, 70, 8, 1, 8, 59⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 0, 9, 0, 25, 0, 0, 9, 0, 25, 258, 1, 1, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 25, 0, 25, 25, 1, 25, 0, 0, 0, 0, 66, 25, 0, 41, 25, 9, 25, 1, 0, 0, 0, 25, 41, 0, 25, 41, 1, 0, 0, 0, 0, 0, 0, 58, 66, 9, 25, 0, 66, 25, 9, 0, 0, 0, 25, 41, 0, 25, 41, 9, 1, 0, 0, 0, 41, 25, 0, 41, 25, 1, 0, 0, 0, 0, 0, 0, 0, 66, 25, 0, 66, 25, 9, 0, 0, 0, 25, 41, 0, 25, 41, 9, 0, 0, 0, 0, 66, 25, 9, 0, 0, 66, 25, 0, 66, 25, 0, 0, 0, 25, 41, 9, 0, 0, 25, 41, 0, 25, 41, 9, 0, 0, 0, 41, 25, 0, 41, 25, 9, 1, 0, 0, 41, 0, 25, 25, 1, 1, 41, 1]

theorem ok : checkTree C 22 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P105
