module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P572
open YantraCert

def cell : Cell := ⟨6, 49, 6, 30, 5, 16⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 0, 9, 0, 0, 25, 0, 25, 9, 25, 0, 9, 0, 0, 0, 0, 25, 25, 9, 0, 0, 25, 25, 9, 0, 25, 0, 25, 9, 0, 0, 9, 0, 25, 25, 0, 9, 0, 25, 25]

theorem ok : checkTree C 10 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P572
