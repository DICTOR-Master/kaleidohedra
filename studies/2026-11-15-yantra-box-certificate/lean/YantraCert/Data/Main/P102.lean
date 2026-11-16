module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P102
open YantraCert

def cell : Cell := ⟨9, 140, 9, 3, 8, 58⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 0, 0, 0, 0, 1, 0, 0, 41, 25, 0, 0, 1, 0, 41, 9, 25, 25, 9, 0, 0, 0, 0, 9, 0, 0, 0, 41, 0, 41, 25, 1, 25, 1, 25, 0, 0, 0, 0, 0, 0, 0, 41, 25, 0, 41, 25, 9, 25, 0, 0, 0, 0, 41, 25, 0, 41, 25, 9, 25, 1, 25, 41, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 41, 25, 0, 41, 25, 0, 9, 0, 41, 25, 25, 0, 0, 9, 0, 0, 41, 25, 0, 41, 25, 25, 9, 41, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 41, 9, 0, 41, 41, 25, 0, 0, 9, 0, 0, 41, 41, 0, 41, 41, 41, 41, 0, 0, 1, 0, 0, 0, 1, 0, 0, 41, 41, 0, 41, 41, 41, 0, 0, 1, 0, 0, 41, 41, 9, 41, 41, 0, 9, 0, 0, 0, 9, 0, 0, 0, 0, 41, 41, 0, 25, 41, 1, 41, 1, 41, 41, 41]

theorem ok : checkTree C 17 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P102
