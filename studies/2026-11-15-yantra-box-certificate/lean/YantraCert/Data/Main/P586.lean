module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P586
open YantraCert

def cell : Cell := ⟨3, 6, 3, 4, 2, 1⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 9, 0, 0, 0, 9, 0, 0, 0, 9, 9, 0, 9, 9, 0, 0, 9, 9, 0, 9, 9, 0, 9, 0, 0, 0, 9, 9, 306, 0, 0, 9, 9, 0, 9, 9, 0, 0, 9, 0, 0, 82, 0, 9, 0, 9, 9, 82, 0, 9, 0, 0, 0, 9, 0, 9, 9, 0, 9, 0, 9, 9, 0, 82, 0, 9, 0, 0, 82, 0, 9, 0, 9, 82, 82]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P586
