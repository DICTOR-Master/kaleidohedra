module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P543
open YantraCert

def cell : Cell := ⟨7, 97, 6, 28, 6, 33⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 25, 25, 0, 25, 25, 0, 0, 0, 25, 25, 25, 0, 0, 25, 25, 25]

theorem ok : checkTree C 6 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P543
