module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P94
open YantraCert

def cell : Cell := ⟨9, 139, 9, 3, 8, 58⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 0, 0, 0, 0, 0, 18, 0, 25, 25, 9, 25, 0, 0, 0, 0, 41, 25, 0, 41, 25, 0, 9, 0, 41, 25, 25, 9, 25, 0, 0, 0, 0, 0, 9, 0, 0, 41, 25, 0, 41, 25, 25, 0, 0, 9, 0, 0, 41, 25, 0, 41, 25, 25, 9, 25]

theorem ok : checkTree C 11 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P94
