module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P390
open YantraCert

def cell : Cell := ⟨3, 6, 3, 2, 2, 2⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 282, 0, 0, 82, 82, 0, 9, 82, 282, 0, 0, 282, 0, 9, 9, 282]

theorem ok : checkTree C 7 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P390
