module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P143
open YantraCert

def cell : Cell := ⟨7, 37, 6, 0, 6, 14⟩
noncomputable def codes : TC := TC.ofList [0, 0, 1, 0, 9, 9, 0, 1, 0, 9, 9]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P143
