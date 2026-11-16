module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P304
open YantraCert

def cell : Cell := ⟨5, 21, 4, 3, 4, 7⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 66, 0, 0, 58, 9, 0, 58, 82, 66, 0, 0, 66, 0, 0, 9, 9, 9, 66, 0, 0, 0, 0, 0, 0, 0, 9, 25, 0, 9, 0, 25, 9, 9, 0, 0, 0, 25, 9, 0, 0, 25, 25, 9, 58, 0, 0, 0, 0, 9, 0, 0, 25, 25, 9, 0, 9, 0, 0, 0, 9, 0, 25, 9, 0, 9, 0, 0, 25, 0, 9, 0, 41, 9, 9, 9, 9, 0, 0, 0, 0, 0, 25, 25, 25, 9, 0, 0, 0, 0, 0, 25, 25, 9, 0, 0, 0, 25, 0, 0, 41, 25, 9, 25, 9, 0, 25, 25, 9, 0, 0, 0, 25, 9, 25, 0, 0, 25, 9, 0, 25, 25, 0, 82, 0, 9, 0, 0, 58, 58, 9, 0, 0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 9, 0, 82, 0, 0, 58, 82, 9]

theorem ok : checkTree C 17 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P304
