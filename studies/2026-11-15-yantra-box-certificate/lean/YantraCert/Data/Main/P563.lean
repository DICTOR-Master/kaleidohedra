module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P563
open YantraCert

def cell : Cell := ⟨6, 49, 5, 14, 5, 16⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 0, 0, 9, 58, 0, 9, 0, 25, 25, 58, 0, 9, 0, 0, 0, 9, 0, 25, 25, 0, 9, 0, 0, 25, 25, 25, 0, 58, 0, 9, 0, 25, 25]

theorem ok : checkTree C 9 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P563
