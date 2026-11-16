module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P521
open YantraCert

def cell : Cell := ⟨14, 12295, 14, 7411, 13, 4257⟩
noncomputable def codes : TC := TC.ofList [0, 0, 25, 0, 0, 0, 25, 0, 0, 0, 25, 9, 0, 25, 0, 0, 0, 25, 0, 0, 0, 25, 0, 0, 9, 0, 25, 41, 25, 0, 9, 0, 0, 0, 9, 41, 9, 0, 0, 9, 0, 41, 25, 9, 25, 9, 25, 25, 9, 25, 9]

theorem ok : checkTree C 20 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P521
