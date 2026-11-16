module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P670
open YantraCert

def cell : Cell := ⟨7, 98, 6, 33, 6, 33⟩
noncomputable def codes : TC := TC.ofList [0, 0, 9, 0, 0, 25, 25, 0, 0, 0, 25, 25, 9, 0, 0, 25, 25, 9, 0, 9, 0, 25, 0, 0, 25, 9, 25]

theorem ok : checkTree C 8 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P670
