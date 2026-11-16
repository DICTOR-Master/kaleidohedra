module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P403
open YantraCert

def cell : Cell := ⟨14, 12294, 14, 7407, 14, 8512⟩
noncomputable def codes : TC := TC.ofList [9]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P403
