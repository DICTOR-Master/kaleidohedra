module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P437
open YantraCert

def cell : Cell := ⟨19, 393445, 19, 237086, 18, 136223⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 41, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 25, 0, 9, 0, 0, 0, 9, 0, 0, 25, 0, 9, 0, 41, 25, 25, 0, 9, 0, 41, 0, 25, 0, 9, 0, 41, 9, 9, 9, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 25, 0, 0, 9, 0, 41, 9, 41, 41, 9, 0, 9, 0, 25, 9, 9, 9, 9, 0, 0, 25, 0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 9, 25, 9, 0, 0, 9, 0, 25, 0, 0, 41, 25, 9, 9, 25, 9, 25, 9, 0, 0, 0, 0, 0, 41, 0, 25, 0, 0, 0, 0, 0, 41, 25, 9, 41, 25, 9, 9, 0, 0, 25, 0, 0, 0, 41, 0, 0, 0, 41, 25, 0, 9, 25, 0, 0, 41, 0, 25, 41, 0, 9, 0, 25, 41, 9, 41, 9, 0, 25, 0, 0, 0, 25, 0, 0, 0, 0, 9, 25, 0, 9, 0, 41, 25, 25, 9, 25, 9, 9, 25, 9, 25]

theorem ok : checkTree C 20 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P437
