module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P602
open YantraCert

def cell : Cell := ⟨6, 55, 6, 45, 6, 30⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 9, 0, 9, 0, 0, 9, 0, 58, 58, 0, 9, 0, 0, 25, 58, 58, 0, 9, 0, 9, 0, 0, 9, 0, 0, 0, 9, 25, 0, 9, 25, 0, 58, 58, 0, 9, 0, 0, 0, 9, 25, 0, 9, 25, 0, 0, 25, 25, 0, 25, 25]

theorem ok : checkTree C 11 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P602
