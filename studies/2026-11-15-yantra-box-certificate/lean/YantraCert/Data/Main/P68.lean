module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P68
open YantraCert

def cell : Cell := ⟨10, 270, 9, 2, 9, 116⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 9, 0, 25, 258, 1, 0, 0, 9, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 25, 25, 1, 25, 1, 0, 0, 9, 0, 41, 25, 1, 1, 41, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 25, 0, 25, 25, 1, 25, 0, 0, 0, 0, 25, 25, 0, 25, 25, 9, 25, 1, 0, 0, 0, 41, 25, 0, 41, 41, 1, 0, 0, 0, 0, 0, 0, 0, 66, 25, 0, 66, 25, 0, 9, 0, 66, 25, 25, 0, 0, 9, 0, 0, 66, 25, 0, 66, 25, 25, 9, 0, 0, 0, 41, 41, 0, 41, 41, 9, 1, 0, 0, 41, 0, 41, 25, 1, 1, 41, 1]

theorem ok : checkTree C 18 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P68
