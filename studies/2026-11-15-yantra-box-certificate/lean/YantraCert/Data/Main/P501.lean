module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P501
open YantraCert

def cell : Cell := ⟨15, 24590, 15, 14819, 14, 8513⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 25, 9]

theorem ok : checkTree C 4 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P501
