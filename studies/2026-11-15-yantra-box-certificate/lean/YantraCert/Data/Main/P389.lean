module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P389
open YantraCert

def cell : Cell := ⟨2, 3, 2, 0, 1, 1⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 226, 0, 0, 282, 266, 0, 282, 266, 226, 0, 0, 226, 0, 0, 9, 9, 0, 9, 9, 226]

theorem ok : checkTree C 7 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P389
