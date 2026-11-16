module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P314
open YantraCert

def cell : Cell := ⟨5, 21, 5, 9, 5, 14⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 0, 9, 25, 25, 9, 0, 0, 0, 25, 9, 25, 0, 0, 0, 25, 9, 0, 25, 0, 0, 0, 25, 25, 0, 9, 41, 25, 0, 0, 25, 9, 0, 25, 25, 0, 0, 25, 9, 0, 25, 0, 0, 25, 25, 25, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 0, 41, 41, 0, 0, 9, 0, 41, 25, 0, 9, 0, 41, 41, 0, 9, 0, 25, 0, 41, 41, 9, 0, 9, 0, 0, 0, 9, 0, 25, 25, 25, 9, 9, 0, 9, 0, 0, 0, 9, 0, 25, 9, 0, 9, 0, 25, 9, 9]

theorem ok : checkTree C 15 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P314
