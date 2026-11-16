module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P584
open YantraCert

def cell : Cell := ⟨2, 2, 1, 1, 1, 0⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 306, 9, 0, 306, 0, 0, 0, 306, 9, 0, 306, 0, 0, 0, 9, 9, 0, 306, 26, 306, 306, 0, 0, 290, 9, 0, 290, 0, 306, 306]

theorem ok : checkTree C 11 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P584
