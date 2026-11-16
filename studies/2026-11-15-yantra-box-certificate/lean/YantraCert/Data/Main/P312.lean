module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P312
open YantraCert

def cell : Cell := ⟨6, 43, 5, 8, 5, 14⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 0, 0, 9, 0, 25, 9, 0, 9, 0, 25, 9, 9, 0, 9, 0, 0, 0, 9, 0, 0, 25, 0, 9, 25, 9, 0, 9, 0, 0, 0, 9, 0, 0, 25, 0, 0, 25, 9, 25, 25, 0, 9, 0, 0, 0, 0, 41, 9, 0, 41, 25, 0, 0, 41, 9, 41, 0, 25, 0, 9, 0, 25, 25, 9, 9]

theorem ok : checkTree C 14 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P312
