module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P240
open YantraCert

def cell : Cell := ⟨5, 11, 5, 1, 4, 4⟩
noncomputable def codes : TC := TC.ofList [290]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P240
