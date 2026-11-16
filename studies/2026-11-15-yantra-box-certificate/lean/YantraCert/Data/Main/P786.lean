module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P786
open YantraCert

def cell : Cell := ⟨3, 7, 2, 2, 2, 2⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 90, 90, 0, 282, 0, 282, 9, 0, 0, 90, 90, 9, 0, 0, 0, 0, 0, 0, 82, 0, 0, 9, 9, 9, 9, 0, 9, 9, 0, 0, 0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 9, 9, 0, 9, 9, 0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 9, 0, 0, 0, 9, 9, 0, 9, 9, 9]

theorem ok : checkTree C 11 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P786
