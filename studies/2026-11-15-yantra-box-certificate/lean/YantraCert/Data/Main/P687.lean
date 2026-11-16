module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P687
open YantraCert

def cell : Cell := ⟨5, 24, 4, 9, 4, 8⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 306, 0, 0, 9, 0, 306, 0, 0, 9, 0, 25, 25, 26, 26, 0, 306, 0, 0, 0, 9, 9, 9, 26, 306]

theorem ok : checkTree C 11 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P687
