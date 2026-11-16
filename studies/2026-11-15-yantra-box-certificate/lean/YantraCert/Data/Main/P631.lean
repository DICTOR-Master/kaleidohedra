module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P631
open YantraCert

def cell : Cell := ⟨9, 442, 8, 188, 8, 125⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 0, 0, 9, 0, 25, 0, 0, 25, 25, 25, 0, 9, 0, 25, 0, 25, 25, 0, 0, 0, 0, 0, 9, 0, 9, 0, 25, 25, 0, 9, 0, 9, 25, 0, 0, 0, 9, 41, 0, 41, 41, 0, 0, 9, 41, 0, 0, 41, 25, 41, 0, 0, 0, 0, 25, 0, 41, 25, 9, 0, 0, 25, 25, 9, 9, 0, 0, 0, 0, 9, 25, 25, 0, 0, 0, 9, 0, 41, 25, 0, 25, 0, 41, 25, 0, 0, 9, 25, 0, 25, 25, 0, 0, 0, 0, 25, 25, 9, 0, 25, 9, 9, 0, 9, 0, 0, 0, 9, 0, 25, 25, 0, 9, 0, 25, 25, 0, 0, 0, 0, 25, 25, 0, 0, 0, 9, 25, 0, 25, 25, 0, 25, 25, 0, 0, 25, 25, 9, 0, 0, 25, 0, 25, 25, 0, 25, 9]

theorem ok : checkTree C 12 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P631
