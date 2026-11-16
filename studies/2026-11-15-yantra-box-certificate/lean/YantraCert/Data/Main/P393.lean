module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P393
open YantraCert

def cell : Cell := ⟨7, 96, 7, 56, 6, 33⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 25, 25, 0, 0, 25, 9, 0, 25, 25, 0, 25, 25, 0, 9, 9]

theorem ok : checkTree C 7 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P393
