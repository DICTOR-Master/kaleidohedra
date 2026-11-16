module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P277
open YantraCert

def cell : Cell := ⟨4, 8, 4, 0, 3, 2⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 226, 0, 0, 0, 226, 258, 0, 226, 266, 0, 0, 226, 274, 0, 226, 258, 0, 226, 0, 9, 138]

theorem ok : checkTree C 8 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P277
