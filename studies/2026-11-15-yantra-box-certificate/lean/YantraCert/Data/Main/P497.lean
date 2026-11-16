module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P497
open YantraCert

def cell : Cell := ⟨19, 393447, 18, 118545, 18, 136223⟩
noncomputable def codes : TC := TC.ofList [0, 25, 0, 9, 0, 0, 41, 0, 9, 0, 0, 0, 9, 0, 0, 41, 0, 0, 0, 0, 0, 0, 41, 25, 9, 0, 0, 41, 0, 0, 25, 41, 9, 41, 0, 0, 25, 9, 0, 25, 0, 41, 0, 0, 25, 41, 9, 41, 9, 25, 0, 9, 0, 0, 0, 0, 25, 0, 41, 0, 9, 0, 25, 41, 9, 0, 0, 25, 0, 0, 9, 0, 25, 0, 0, 9, 0, 25, 41, 25, 25, 9, 0, 41, 0, 0, 0, 41, 0, 9, 0, 0, 41, 25, 41, 9, 0, 0, 41, 0, 0, 9, 41, 9, 25, 25, 9]

theorem ok : checkTree C 20 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P497
