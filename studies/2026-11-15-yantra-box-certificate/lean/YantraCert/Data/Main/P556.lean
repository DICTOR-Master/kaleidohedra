module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P556
open YantraCert

def cell : Cell := ⟨8, 193, 7, 58, 7, 66⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 0, 25, 25, 25, 0, 9, 0, 0, 0, 0, 25, 25, 0, 9, 25, 0, 0, 0, 0, 9, 25, 0, 9, 0, 0, 25, 0, 9, 0, 0, 41, 0, 0, 41, 25, 9, 25, 25, 25, 0, 9, 25, 0, 25, 25]

theorem ok : checkTree C 17 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P556
