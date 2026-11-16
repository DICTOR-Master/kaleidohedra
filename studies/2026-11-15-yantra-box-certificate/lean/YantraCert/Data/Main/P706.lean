module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P706
open YantraCert

def cell : Cell := ⟨4, 13, 4, 8, 3, 4⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 82, 0, 0, 0, 0, 0, 9, 82, 0, 0, 82, 0, 58, 58, 82, 0, 0, 9, 82, 0, 0, 0, 58, 58, 0, 0, 58, 58, 0, 58, 9, 82, 82, 0, 0, 0, 9, 9, 0, 9, 9, 9, 82, 0, 0, 82, 0, 9, 9, 9]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P706
