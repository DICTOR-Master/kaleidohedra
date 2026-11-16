module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P196
open YantraCert

def cell : Cell := ⟨8, 82, 8, 2, 8, 63⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 234, 0, 0, 0, 258, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 66, 25, 0, 41, 25, 1, 25, 0, 66, 25, 1, 0, 0, 0, 0, 0, 41, 41, 1, 41, 0, 0, 0, 0, 25, 41, 0, 25, 41, 9, 41, 1, 1, 0, 258, 0, 0, 0, 0, 0, 0, 66, 25, 0, 66, 0, 25, 25, 9, 0, 0, 0, 0, 0, 0, 25, 41, 0, 25, 41, 9, 41, 0, 0, 0, 0, 25, 41, 9, 0, 0, 25, 41, 0, 25, 25, 41, 9, 0, 0, 0, 0, 66, 0, 9, 0, 0, 25, 25, 0, 25, 25, 0, 66, 0, 1, 0, 0, 25, 25, 0, 66, 25, 0, 9, 0, 66, 0, 0, 9, 0, 66, 25, 1, 0, 0, 0, 0, 9, 0, 0, 25, 25, 0, 25, 25, 41, 0, 0, 1, 25, 41, 0, 9, 0, 25, 41, 9, 1]

theorem ok : checkTree C 16 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P196
