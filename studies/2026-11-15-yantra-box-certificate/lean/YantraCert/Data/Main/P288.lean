module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P288
open YantraCert

def cell : Cell := ⟨3, 4, 3, 1, 3, 2⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 9, 0, 306, 0, 0, 9, 0, 26, 0, 0, 9, 0, 0, 0, 0, 25, 25, 0, 9, 25, 25, 0, 0, 9, 0, 0, 25, 25, 0, 0, 9, 41, 25, 0, 9, 0, 25, 25, 18, 306, 290, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 41, 9, 0, 9, 41, 9, 0, 9, 0, 0, 25, 25, 9, 9, 0, 9, 0, 0, 0, 9, 0, 25, 9, 25, 9, 9, 0, 9, 0, 26, 9, 9, 0, 9, 0, 306, 9]

theorem ok : checkTree C 18 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P288
