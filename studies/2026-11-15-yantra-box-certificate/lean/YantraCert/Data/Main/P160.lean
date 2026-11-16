module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P160
open YantraCert

def cell : Cell := ⟨8, 76, 8, 2, 8, 61⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 66, 0, 0, 0, 66, 25, 0, 66, 25, 1, 1, 0, 0, 9, 0, 0, 0, 0, 25, 41, 0, 25, 41, 1, 41, 1, 1, 0, 0, 9, 0, 41, 25, 1, 1, 290]

theorem ok : checkTree C 16 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P160
