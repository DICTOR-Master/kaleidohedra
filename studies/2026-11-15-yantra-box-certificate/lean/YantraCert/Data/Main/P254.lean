module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P254
open YantraCert

def cell : Cell := ⟨5, 12, 5, 1, 4, 4⟩
noncomputable def codes : TC := TC.ofList [0, 0, 306, 0, 0, 9, 0, 306, 0, 0, 9, 0, 306, 0, 0, 9, 0, 0, 25, 25, 0, 41, 25, 25, 290, 290, 0, 9, 210]

theorem ok : checkTree C 14 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P254
