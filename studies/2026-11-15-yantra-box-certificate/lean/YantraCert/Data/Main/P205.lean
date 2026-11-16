module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P205
open YantraCert

def cell : Cell := ⟨8, 85, 7, 1, 7, 31⟩
noncomputable def codes : TC := TC.ofList [0, 138, 0, 1, 0, 0, 0, 1, 0, 0, 0, 9, 0, 0, 66, 0, 0, 0, 25, 25, 9, 0, 0, 25, 25, 0, 25, 25, 0, 66, 0, 9, 0, 0, 0, 0, 25, 0, 25, 25, 9, 25, 0, 0, 0, 0, 25, 25, 9, 0, 0, 25, 25, 0, 66, 25, 25, 0, 9, 0, 0, 0, 0, 0, 41, 25, 9, 0, 0, 41, 41, 0, 41, 41, 41, 0, 0, 9, 0, 0, 41, 41, 0, 0, 41, 41, 41, 41, 0, 0, 1, 0, 0, 66, 0, 9, 0, 0, 0, 9, 0, 58, 66, 25, 0, 66, 25, 9, 0, 1, 0, 0, 0, 9, 0, 0, 0, 9, 0, 41, 0, 25, 25, 41, 0, 0, 9, 0, 0, 25, 25, 25, 41, 41, 9, 0, 1, 0, 0, 41, 25, 0, 41, 25, 9]

theorem ok : checkTree C 18 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P205
