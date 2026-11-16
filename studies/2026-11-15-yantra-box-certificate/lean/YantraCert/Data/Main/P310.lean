module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P310
open YantraCert

def cell : Cell := ⟨5, 20, 4, 4, 4, 7⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 18, 9, 306, 0, 0, 0, 0, 0, 0, 25, 25, 0, 9, 25, 25, 0, 0, 9, 0, 0, 25, 25, 0, 0, 9, 0, 25, 41, 0, 9, 0, 25, 25, 0, 9, 0, 25, 0, 25, 25, 0, 9, 0, 0, 0, 9, 0, 0, 9, 9, 0, 9, 9, 9, 0, 0, 9, 0, 25, 25, 9, 0, 0, 25, 0, 0, 9, 25, 25, 0, 9, 0, 0, 25, 9, 25, 9, 0, 26, 9]

theorem ok : checkTree C 14 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P310
