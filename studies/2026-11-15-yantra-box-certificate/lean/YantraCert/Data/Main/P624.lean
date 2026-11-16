module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P624
open YantraCert

def cell : Cell := ⟨8, 221, 7, 93, 7, 63⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 9, 9, 0, 0, 0, 25, 25, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 25, 9, 0, 0, 25, 9, 9, 9, 9, 0, 0, 0, 0, 0, 41, 9, 9, 0, 0, 41, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41, 9, 9, 0, 0, 41, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 41, 25, 9, 9, 0, 0, 25, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 25, 9, 9, 0, 0, 25, 9, 9, 9, 9, 0, 0, 0, 0, 25, 9, 25, 9, 9, 9, 9, 9, 9]

theorem ok : checkTree C 15 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P624
