module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P302
open YantraCert

def cell : Cell := ⟨5, 20, 5, 6, 4, 7⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 9, 0, 0, 0, 9, 25, 9, 0, 0, 9, 25, 9, 9, 0, 0, 9, 0, 0, 0, 9, 0, 25, 25, 9, 0, 0, 9, 0, 0, 0, 25, 25, 9, 0, 0, 0, 0, 41, 9, 41, 0, 25, 25, 9, 9, 9, 0, 0, 0, 0, 58, 0, 0, 25, 25, 25, 82, 0, 9, 82, 0, 0, 0, 0, 0, 25, 25, 0, 9, 25, 0, 0, 0, 25, 0, 25, 25, 25, 0, 9, 25, 0, 58, 0, 9, 0, 25, 25, 0, 9, 0, 58, 0, 0, 9, 25, 9, 9]

theorem ok : checkTree C 15 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P302
