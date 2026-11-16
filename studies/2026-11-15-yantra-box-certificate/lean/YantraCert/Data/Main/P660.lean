module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P660
open YantraCert

def cell : Cell := ⟨5, 27, 5, 25, 4, 7⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 306, 0, 0, 0, 9, 186, 0, 306, 0, 26, 306, 306]

theorem ok : checkTree C 8 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P660
