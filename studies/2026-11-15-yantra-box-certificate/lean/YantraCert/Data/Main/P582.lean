module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P582
open YantraCert

def cell : Cell := ⟨3, 7, 2, 1, 2, 2⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 266, 234, 0, 266, 9, 0, 0, 282, 282, 0, 282, 9]

theorem ok : checkTree C 5 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P582
