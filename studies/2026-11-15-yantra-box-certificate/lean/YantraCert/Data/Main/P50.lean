module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P50
open YantraCert

def cell : Cell := ⟨9, 132, 9, 2, 9, 114⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 1, 0, 0, 258, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 9, 0, 0, 66, 25, 0, 66, 25, 25, 0, 0, 9, 0, 0, 66, 25, 0, 66, 25, 25, 0, 1, 0, 0, 41, 25, 0, 41, 41, 0, 0, 1, 0, 0, 0, 1, 0, 0, 66, 25, 0, 66, 25, 25, 9, 0, 1, 0, 0, 41, 41, 9, 0, 1, 0, 0, 25, 25, 0, 41, 25, 9, 9, 290, 9]

theorem ok : checkTree C 19 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P50
