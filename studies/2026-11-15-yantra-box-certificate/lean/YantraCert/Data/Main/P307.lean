module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P307
open YantraCert

def cell : Cell := ⟨3, 4, 2, 1, 2, 1⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 290, 306, 0, 290, 306, 290]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P307
