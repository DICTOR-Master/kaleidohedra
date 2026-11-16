module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P387
open YantraCert

def cell : Cell := ⟨3, 5, 3, 3, 3, 5⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 9, 9, 0, 9, 9]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P387
