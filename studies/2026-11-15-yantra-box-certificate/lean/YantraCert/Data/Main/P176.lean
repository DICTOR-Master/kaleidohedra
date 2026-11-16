module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P176
open YantraCert

def cell : Cell := ⟨7, 39, 7, 1, 7, 31⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 258, 0, 0, 0, 66, 0, 0, 9, 0, 66, 0, 0, 9, 25, 1, 1, 0, 66, 0, 0, 0, 66, 0, 0, 0, 25, 25, 0, 25, 25, 9, 0, 66, 0, 0, 0, 25, 25, 0, 25, 25, 9, 9, 1, 1, 0, 0, 9, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 9, 0, 41, 41, 1, 41, 1, 41, 0, 0, 0, 0, 0, 0, 0, 41, 41, 0, 25, 41, 9, 41, 0, 0, 0, 0, 25, 41, 0, 25, 41, 9, 41, 9, 41, 1, 41, 1, 1, 290]

theorem ok : checkTree C 19 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P176
