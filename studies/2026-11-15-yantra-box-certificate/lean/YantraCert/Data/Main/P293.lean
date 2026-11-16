module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P293
open YantraCert

def cell : Cell := ⟨5, 18, 5, 5, 4, 6⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 26, 290, 0, 0, 0, 0, 0, 9, 0, 25, 25, 25, 9, 0, 0, 0, 0, 9, 0, 25, 25, 9, 25, 0, 0, 0, 0, 41, 25, 0, 0, 9, 0, 41, 41, 0, 9, 41, 0, 9, 0, 0, 0, 9, 41, 9, 0, 41, 9, 0, 0, 25, 0, 25, 25, 0, 9, 0, 25, 25, 0, 0, 25, 9, 0, 18, 0, 0, 25, 25, 25, 0, 9, 9]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P293
