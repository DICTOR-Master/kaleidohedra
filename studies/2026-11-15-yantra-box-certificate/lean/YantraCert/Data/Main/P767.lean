module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P767
open YantraCert

def cell : Cell := ⟨7, 108, 7, 88, 7, 65⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 9, 9, 0, 0, 25, 9, 9, 9, 9, 0, 0, 0, 0, 0, 25, 9, 9, 0, 25, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 25, 9, 25, 9, 9, 0, 0, 25, 9, 9, 9, 9, 9]

theorem ok : checkTree C 12 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P767
