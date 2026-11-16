module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P0
open YantraCert

def cell : Cell := ⟨2, 0, 1, 0, 1, 0⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 1, 0, 0, 11, 33, 0, 11, 33, 290, 0, 0, 1, 0, 0, 11, 33, 0, 11, 290, 290, 0, 1, 9, 290]

theorem ok : checkTree C 9 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P0
