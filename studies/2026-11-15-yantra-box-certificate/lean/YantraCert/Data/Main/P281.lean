module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P281
open YantraCert

def cell : Cell := ⟨5, 16, 5, 3, 4, 5⟩
noncomputable def codes : TC := TC.ofList [0, 0, 26, 0, 0, 9, 0, 0, 0, 9, 0, 0, 25, 25, 9, 25, 9, 18, 0, 26, 0, 0, 0, 0, 0, 0, 0, 25, 25, 0, 25, 25, 9, 18, 0, 0, 0, 0, 0, 0, 25, 9, 0, 25, 41, 25, 0, 0, 9, 0, 41, 0, 41, 41, 0, 9, 41, 0, 9, 0, 0, 0, 9, 0, 41, 41, 9, 0, 41, 9, 0, 0, 25, 0, 25, 25, 0, 9, 0, 25, 25, 9, 18]

theorem ok : checkTree C 14 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P281
