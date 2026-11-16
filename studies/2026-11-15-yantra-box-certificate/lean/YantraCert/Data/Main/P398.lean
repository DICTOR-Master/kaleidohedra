module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P398
open YantraCert

def cell : Cell := ⟨12, 3072, 11, 925, 11, 1064⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 9, 0, 0, 0, 25, 0, 0, 0, 41, 0, 0, 0, 0, 0, 9, 0, 0, 0, 9, 0, 41, 41, 41, 9, 0, 9, 0, 41, 9, 9, 0, 0, 0, 0, 41, 25, 9, 0, 0, 41, 0, 0, 0, 41, 25, 9, 41, 9, 25, 0, 0, 41, 9, 0, 41, 0, 0, 0, 0, 0, 0, 41, 25, 9, 0, 0, 41, 0, 25, 41, 9, 25, 9, 0, 0, 41, 0, 25, 0, 0, 41, 9, 0, 41, 25, 9, 9, 0, 0, 25, 0, 0, 0, 25, 9, 41, 25, 9, 9, 41, 9, 25]

theorem ok : checkTree C 21 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P398
