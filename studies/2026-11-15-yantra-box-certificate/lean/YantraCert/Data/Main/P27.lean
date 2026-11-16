module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P27
open YantraCert

def cell : Cell := ⟨11, 521, 10, 4, 10, 228⟩
noncomputable def codes : TC := TC.ofList [0, 0, 1, 0, 0, 258, 0, 1, 0, 0, 0, 9, 0, 0, 0, 0, 0, 66, 0, 0, 25, 0, 25, 25, 9, 0, 41, 0, 0, 0, 25, 25, 9, 0, 0, 25, 25, 0, 25, 25, 9, 25, 0, 0, 0, 0, 41, 0, 9, 0, 0, 25, 25, 58, 66, 9, 25, 0, 9, 0, 0, 41, 41, 0, 41, 41, 0, 0, 9, 0, 0, 66, 25, 0, 66, 0, 9, 0, 25, 25, 0, 9, 0, 0, 41, 41, 0, 0, 9, 0, 41, 41, 41, 0, 258, 0, 1, 0, 0, 0, 1, 0, 0, 66, 0, 1, 0, 0, 25, 25, 0, 25, 25, 0, 66, 0, 1, 0, 0, 25, 25, 0, 25, 25, 0, 1, 0, 0, 0, 1, 0, 0, 25, 41, 0, 25, 41, 41, 0, 0, 1, 0, 0, 25, 41, 0, 25, 41, 41, 9, 0, 1, 0, 0, 0, 1, 0, 0, 41, 25, 0, 41, 25, 25, 0, 0, 1, 0, 0, 41, 25, 9, 25]

theorem ok : checkTree C 18 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P27
