module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P256
open YantraCert

def cell : Cell := ⟨5, 13, 5, 1, 5, 8⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 41, 25, 9, 41, 9, 290, 9, 290, 9]

theorem ok : checkTree C 14 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P256
