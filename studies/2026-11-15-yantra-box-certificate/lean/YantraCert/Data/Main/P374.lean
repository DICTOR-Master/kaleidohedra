module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P374
open YantraCert

def cell : Cell := ⟨10, 766, 9, 230, 9, 265⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 25, 25, 25]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P374
