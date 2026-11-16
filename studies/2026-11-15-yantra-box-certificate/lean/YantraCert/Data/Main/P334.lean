module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P334
open YantraCert

def cell : Cell := ⟨5, 22, 4, 6, 4, 8⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 0, 0, 9, 9, 25, 0, 0, 0, 0, 0, 25, 9, 25, 0, 0, 0, 41, 0, 0, 9, 0, 41, 9, 41, 0, 9, 0, 0, 0, 41, 41, 9, 41, 0, 0, 25, 41, 0, 9, 41, 9, 0, 0, 25, 0, 0, 25, 25, 25, 9, 9, 0, 0, 25, 0, 0, 0, 25, 25, 9, 25, 9, 9, 0, 0, 9, 0, 0, 0, 25, 25, 9, 0, 0, 25, 25, 9, 9, 9, 0, 0, 9, 0, 0, 0, 9, 0, 25, 25, 9, 26, 9]

theorem ok : checkTree C 20 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P334
