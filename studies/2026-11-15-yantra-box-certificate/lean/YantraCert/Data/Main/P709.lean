module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P709
open YantraCert

def cell : Cell := ⟨6, 52, 6, 39, 6, 32⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 9, 9, 0, 9, 9]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P709
