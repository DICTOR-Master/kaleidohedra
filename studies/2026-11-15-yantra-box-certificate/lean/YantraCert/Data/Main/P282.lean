module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P282
open YantraCert

def cell : Cell := ⟨5, 17, 5, 2, 4, 5⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 258, 0, 0, 0, 0, 9, 0, 0, 66, 58, 66, 0, 9, 0, 0, 0, 25, 9, 0, 0, 0, 25, 25, 25, 9, 0, 58, 0, 0, 25, 9, 25, 0, 66, 0, 9, 0, 0, 66, 25, 9, 0, 9, 0, 66, 0, 0, 0, 66, 25, 82, 9, 274]

theorem ok : checkTree C 14 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P282
