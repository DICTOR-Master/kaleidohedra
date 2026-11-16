module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P664
open YantraCert

def cell : Cell := ⟨2, 2, 1, 1, 1, 1⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 210, 0, 0, 0, 306, 0, 0, 0, 306, 0, 0, 26, 26, 306, 0, 9, 9, 306, 0, 9, 0, 0, 9, 9, 306, 306, 0, 9, 210, 0, 0, 210, 0, 306, 306, 0, 9, 210]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P664
