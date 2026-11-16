module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P749
open YantraCert

def cell : Cell := ⟨7, 107, 7, 87, 7, 64⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 9, 0, 9, 0, 0, 9, 0, 9, 0, 0, 9, 0, 9, 25, 0, 9, 0, 9, 25, 0, 9, 0, 9, 0, 0, 9, 0, 9, 0, 41, 41, 0, 9, 0, 9, 0, 0, 9, 9, 0, 9, 9, 0, 9, 0, 9, 0, 0, 9, 0, 9, 0, 0, 9, 0, 9, 0, 0, 9, 9, 0, 9, 9, 0, 9, 0, 9, 0, 0, 9, 9, 0, 9, 9, 0, 9, 0, 9, 0, 0, 9, 0, 9, 0, 25, 25, 0, 9, 0, 9, 25]

theorem ok : checkTree C 14 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P749
