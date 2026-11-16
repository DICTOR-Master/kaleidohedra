module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P391
open YantraCert

def cell : Cell := ⟨4, 12, 4, 6, 3, 4⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 0, 0, 9, 0, 82, 82, 0, 9, 0, 0, 58, 58, 82, 82, 0, 0, 0, 9, 9, 0, 9, 9, 82, 0, 0, 0, 0, 9, 0, 0, 0, 0, 25, 25, 0, 9, 9, 0, 0, 25, 25, 0, 9, 9, 58, 0, 9, 0, 0, 0, 0, 25, 25, 0, 9, 9, 0, 0, 0, 25, 25, 25, 0, 9, 9, 0, 0, 0, 25, 25, 0, 25, 25, 0, 0, 25, 25, 0, 25, 25, 0, 82, 0, 9, 0, 58, 82, 0, 0, 0, 9, 9, 0, 9, 9, 0, 82, 0, 0, 9, 9, 9, 82, 0, 9, 82]

theorem ok : checkTree C 14 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P391
