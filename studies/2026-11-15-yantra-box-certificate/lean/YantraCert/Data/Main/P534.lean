module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P534
open YantraCert

def cell : Cell := ⟨12, 3074, 12, 1855, 11, 1064⟩
noncomputable def codes : TC := TC.ofList [0, 0, 25, 0, 0, 9, 0, 25, 0, 0, 9, 0, 25, 0, 0, 9, 0, 0, 0, 9, 0, 25, 41, 0, 9, 0, 25, 0, 0, 25, 9, 25, 41, 0, 9, 0, 25, 0, 0, 9, 0, 0, 0, 0, 25, 9, 0, 25, 41, 25, 41, 0, 9, 0, 25, 0, 41, 25, 25, 25, 9]

theorem ok : checkTree C 19 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P534
