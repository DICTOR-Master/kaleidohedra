module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P346
open YantraCert

def cell : Cell := ⟨7, 95, 6, 27, 6, 32⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 0, 0, 9, 9, 0, 9, 9, 9, 0, 9, 0, 0, 0, 9, 9, 0, 9, 9, 9]

theorem ok : checkTree C 7 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P346
