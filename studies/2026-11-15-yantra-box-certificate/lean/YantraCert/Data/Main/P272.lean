module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P272
open YantraCert

def cell : Cell := ⟨3, 3, 3, 1, 2, 1⟩
noncomputable def codes : TC := TC.ofList [306]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P272
