module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P718
open YantraCert

def cell : Cell := ⟨4, 12, 3, 5, 3, 4⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 306, 0, 0, 0, 306, 0, 0, 9, 0, 26, 0, 0, 0, 9, 0, 0, 9, 0, 9, 9, 0, 9, 0, 9, 9, 0, 0, 0, 25, 9, 25, 0, 0, 0, 25, 25, 9, 0, 0, 25, 25, 9, 0, 0, 9, 0, 0, 9, 25, 0, 9, 25, 0, 26, 0, 0, 25, 9, 0, 25, 9, 0, 9, 0, 306, 26, 0, 306, 0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 9, 0, 0, 306, 306, 0, 306, 306, 0, 9, 0, 0, 9, 9, 0, 9, 9, 0, 0, 306, 306, 0, 9, 306]

theorem ok : checkTree C 17 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P718
