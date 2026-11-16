module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P294
open YantraCert

def cell : Cell := ⟨5, 19, 5, 4, 4, 6⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 9, 0, 0, 66, 58, 66, 0, 9, 0, 0, 0, 9, 0, 0, 25, 25, 25, 0, 9, 0, 0, 25, 0, 0, 0, 25, 0, 25, 25, 25, 0, 9, 25, 0, 25, 25, 0, 58, 0, 9, 0, 25, 9, 9, 0, 0, 0, 0, 0, 66, 58, 66, 9, 0, 0, 0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 9, 0, 58, 0, 0, 25, 25, 9, 9, 0, 66, 0, 0, 0, 66, 58, 66, 0, 9, 66]

theorem ok : checkTree C 15 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P294
