module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P4
open YantraCert

def cell : Cell := ⟨8, 64, 8, 0, 7, 28⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 25, 0, 1, 0, 0, 25, 0, 1, 0, 0, 25, 0, 9, 0, 0, 25, 258, 138, 138, 138, 9, 0, 0, 25, 0, 0, 9, 138, 1, 138]

theorem ok : checkTree C 14 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P4
