module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P377
open YantraCert

def cell : Cell := ⟨11, 1534, 10, 461, 10, 531⟩
noncomputable def codes : TC := TC.ofList [0, 25, 25]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P377
