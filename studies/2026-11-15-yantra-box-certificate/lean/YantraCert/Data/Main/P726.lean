module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P726
open YantraCert

def cell : Cell := ⟨7, 104, 6, 41, 6, 33⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 9, 0, 25, 25, 0, 9, 25, 0, 0, 9, 0, 25, 25, 0, 9, 0, 25, 25, 0, 0, 0, 0, 25, 9, 9, 0, 25, 9, 9, 0, 0, 26, 0, 0, 9, 0, 25, 25, 0, 9, 0, 25, 25, 0, 26, 9]

theorem ok : checkTree C 8 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P726
