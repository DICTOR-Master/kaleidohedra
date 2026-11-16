module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P558
open YantraCert

def cell : Cell := ⟨8, 192, 7, 59, 7, 66⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 25, 9, 0, 25, 0, 0, 0, 25, 0, 0, 9, 0, 25, 0, 0, 25, 0, 9, 25, 25, 25, 9, 0, 0, 25, 25, 9, 0, 0, 25, 9, 0, 25, 0, 25, 25]

theorem ok : checkTree C 14 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P558
