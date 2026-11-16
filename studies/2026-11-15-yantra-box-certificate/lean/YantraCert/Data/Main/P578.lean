module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P578
open YantraCert

def cell : Cell := ⟨5, 25, 4, 7, 4, 8⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 82, 0, 9, 0, 58, 82, 82, 0, 0, 82, 0, 0, 9, 9, 9, 82, 0, 0, 0, 0, 9, 0, 0, 58, 0, 9, 0, 25, 25, 58, 0, 9, 0, 0, 0, 9, 0, 25, 25, 0, 9, 0, 25, 25, 0, 58, 0, 9, 58, 0, 82, 82, 0, 0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 9, 0, 82, 82]

theorem ok : checkTree C 11 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P578
