module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P213
open YantraCert

def cell : Cell := ⟨4, 4, 3, 0, 3, 2⟩
noncomputable def codes : TC := TC.ofList [210]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P213
