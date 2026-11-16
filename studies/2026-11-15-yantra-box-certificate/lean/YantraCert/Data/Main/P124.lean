module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P124
open YantraCert

def cell : Cell := ⟨9, 144, 9, 2, 8, 59⟩
noncomputable def codes : TC := TC.ofList [130]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P124
