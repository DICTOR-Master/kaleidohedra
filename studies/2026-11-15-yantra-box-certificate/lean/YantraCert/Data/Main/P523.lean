module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P523
open YantraCert

def cell : Cell := ⟨12, 3073, 12, 1853, 11, 1064⟩
noncomputable def codes : TC := TC.ofList [0, 25, 9]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P523
