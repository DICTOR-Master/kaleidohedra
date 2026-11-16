module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P327
open YantraCert

def cell : Cell := ⟨5, 23, 4, 5, 4, 7⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 0, 0, 9, 0, 9, 9, 0, 9, 0, 9, 9, 9, 0, 9, 0, 0, 0, 9, 0, 9, 9, 0, 9, 0, 9, 9, 9]

theorem ok : checkTree C 8 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P327
