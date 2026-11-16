module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P155
open YantraCert

def cell : Cell := ⟨6, 18, 6, 1, 5, 7⟩
noncomputable def codes : TC := TC.ofList [290]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P155
