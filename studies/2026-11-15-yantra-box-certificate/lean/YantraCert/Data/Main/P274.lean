module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P274
open YantraCert

def cell : Cell := ⟨1, 0, 1, 0, 1, 1⟩
noncomputable def codes : TC := TC.ofList [0, 194, 210]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P274
