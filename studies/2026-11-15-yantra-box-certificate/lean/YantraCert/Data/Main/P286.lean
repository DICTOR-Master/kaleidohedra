module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P286
open YantraCert

def cell : Cell := ⟨4, 9, 3, 0, 3, 2⟩
noncomputable def codes : TC := TC.ofList [0, 226, 0, 9, 0, 0, 266, 0, 9, 0, 0, 82, 0, 9, 0, 0, 0, 9, 0, 0, 25, 0, 9, 25, 9, 0, 9, 0, 0, 0, 9, 0, 0, 25, 25, 9, 0, 9, 0, 0, 41, 41, 9, 9, 9, 9, 9]

theorem ok : checkTree C 18 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P286
