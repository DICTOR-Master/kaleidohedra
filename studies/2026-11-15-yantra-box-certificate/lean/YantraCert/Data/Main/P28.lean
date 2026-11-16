module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P28
open YantraCert

def cell : Cell := ⟨10, 260, 10, 4, 10, 229⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 0, 9, 0, 258, 0, 0, 0, 0, 0, 9, 0, 66, 0, 0, 9, 0, 25, 25, 1, 1, 0, 0, 9, 0, 0, 0, 9, 0, 25, 41, 1, 41, 1, 0, 0, 0, 0, 66, 0, 0, 0, 25, 25, 0, 25, 25, 1, 0, 66, 0, 0, 0, 25, 25, 0, 25, 25, 9, 1, 0, 0, 0, 0, 0, 0, 25, 41, 0, 25, 41, 1, 41, 0, 0, 0, 0, 25, 41, 0, 25, 41, 9, 41, 1, 1, 1, 0, 0, 9, 0, 0, 0, 0, 41, 25, 0, 41, 25, 1, 25, 1]

theorem ok : checkTree C 16 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P28
