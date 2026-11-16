module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P268
open YantraCert

def cell : Cell := ⟨5, 15, 4, 0, 4, 4⟩
noncomputable def codes : TC := TC.ofList [0, 226, 0, 9, 0, 0, 0, 9, 0, 266, 9, 0, 9, 0, 0, 0, 9, 9, 0, 9, 9, 9, 9]

theorem ok : checkTree C 10 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P268
