module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P221
open YantraCert

def cell : Cell := ⟨6, 21, 6, 1, 5, 8⟩
noncomputable def codes : TC := TC.ofList [0, 0, 306, 0, 0, 0, 306, 0, 0, 0, 306, 0, 0, 9, 0, 2, 0, 41, 25, 25, 0, 9, 0, 0, 0, 9, 0, 41, 25, 1, 25, 41, 9, 41, 9]

theorem ok : checkTree C 14 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P221
