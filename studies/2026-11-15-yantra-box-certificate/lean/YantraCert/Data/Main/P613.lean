module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P613
open YantraCert

def cell : Cell := ⟨6, 54, 6, 47, 5, 15⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 9, 0, 0, 9, 0, 0, 0, 9, 0, 9, 0, 25, 25, 26, 0, 0, 0, 9, 0, 0, 9, 0, 9, 25, 0, 9, 0, 9, 25, 0, 0, 0, 25, 0, 25, 25, 0, 25, 25, 0, 0, 0, 25, 25, 9, 0, 0, 25, 25, 9, 0, 0, 9, 0, 0, 9, 0, 9, 25, 0, 9, 25, 0, 0, 0, 25, 25, 25, 0, 0, 0, 25, 25, 9, 0, 25, 9, 0, 9, 0, 26, 0, 0, 0, 9, 0, 0, 9, 25, 26, 0, 26, 0, 0, 25, 9, 26, 26]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P613
