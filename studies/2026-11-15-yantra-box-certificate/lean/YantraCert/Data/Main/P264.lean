module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P264
open YantraCert

def cell : Cell := ⟨5, 14, 5, 0, 4, 4⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 138, 226]

theorem ok : checkTree C 4 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P264
