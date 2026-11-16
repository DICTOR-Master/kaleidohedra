module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P306
open YantraCert

def cell : Cell := ⟨2, 2, 2, 1, 2, 0⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 1, 9, 290, 9]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P306
