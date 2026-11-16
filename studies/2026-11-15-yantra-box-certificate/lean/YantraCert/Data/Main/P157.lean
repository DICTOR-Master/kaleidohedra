module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P157
open YantraCert

def cell : Cell := ⟨7, 38, 7, 0, 6, 15⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 25, 0, 0, 0, 25, 0, 9, 0, 0, 41, 274, 0, 25, 258, 138, 0, 9, 138, 138, 9]

theorem ok : checkTree C 11 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P157
