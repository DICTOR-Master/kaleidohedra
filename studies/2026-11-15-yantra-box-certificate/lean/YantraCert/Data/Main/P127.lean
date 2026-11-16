module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P127
open YantraCert

def cell : Cell := ⟨9, 144, 9, 3, 9, 119⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 0, 9, 0, 258, 0, 0, 0, 0, 0, 9, 0, 0, 0, 9, 0, 66, 25, 1, 0, 0, 9, 0, 25, 25, 1, 1, 0, 0, 9, 0, 41, 25, 1, 0, 0, 0, 0, 0, 0, 0, 66, 25, 0, 66, 25, 1, 0, 0, 25, 25, 1, 0, 0, 0, 0, 41, 25, 0, 41, 58, 9, 25, 1, 0, 0, 0, 41, 25, 0, 41, 41, 1, 1, 1, 0, 0, 9, 0, 0, 0, 0, 25, 25, 0, 41, 25, 1, 25, 1]

theorem ok : checkTree C 16 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P127
