module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P328
open YantraCert

def cell : Cell := ⟨3, 5, 3, 3, 2, 1⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 306, 306, 9, 0, 0, 306, 306, 0, 0, 0, 9, 9, 0, 0, 0, 0, 9, 9, 0, 0, 0, 26, 0, 25, 0, 25, 25, 26, 0, 0, 9, 0, 0, 0, 0, 25, 9, 0, 25, 25, 0, 25, 25, 0, 0, 9, 0, 0, 0, 9, 25, 25, 0, 0, 9, 0, 0, 25, 25, 9, 0, 9, 0, 25, 9, 0, 9, 0, 25, 0, 0, 9, 25, 25, 0, 9, 0, 0, 25, 25, 0, 0, 9, 0, 25, 25, 0, 9, 25, 0, 0, 9, 9, 0, 306, 0, 0, 9, 0, 25, 0, 25, 25, 26, 0, 0, 9, 0, 0, 0, 9, 0, 9, 9, 0, 9, 0, 9, 9, 9, 0, 9, 0, 0, 0, 9, 0, 9, 9, 0, 9, 0, 9, 9, 9, 0, 0, 9, 9, 0, 306, 0, 0, 9, 0, 0, 0, 9, 0, 9, 9, 26, 9, 0, 9, 0, 306, 9]

theorem ok : checkTree C 20 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P328
