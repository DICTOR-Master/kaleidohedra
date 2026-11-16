module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P515
open YantraCert

def cell : Cell := ⟨13, 6147, 13, 3705, 13, 4256⟩
noncomputable def codes : TC := TC.ofList [0, 25, 0, 0, 9, 0, 25, 9, 0, 9, 25]

theorem ok : checkTree C 6 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P515
