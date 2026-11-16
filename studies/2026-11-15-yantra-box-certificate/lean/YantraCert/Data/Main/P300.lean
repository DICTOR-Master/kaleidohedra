module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P300
open YantraCert

def cell : Cell := ⟨4, 10, 4, 2, 3, 3⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 274, 0, 9, 0, 0, 82, 0, 9, 0, 0, 58, 0, 0, 25, 25, 0, 9, 25, 58, 82, 274, 0, 0, 274, 0, 0, 0, 82, 0, 0, 9, 58, 9, 82, 9, 274]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P300
