module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P422
open YantraCert

def cell : Cell := ⟨14, 12295, 14, 7408, 14, 8512⟩
noncomputable def codes : TC := TC.ofList [9]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P422
