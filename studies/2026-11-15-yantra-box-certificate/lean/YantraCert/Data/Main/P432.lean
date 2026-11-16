module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P432
open YantraCert

def cell : Cell := ⟨17, 98361, 17, 59270, 16, 34055⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 25, 0, 9, 25, 25]

theorem ok : checkTree C 6 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P432
