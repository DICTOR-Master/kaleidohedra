module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P707
open YantraCert

def cell : Cell := ⟨5, 26, 5, 18, 4, 8⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 9, 0, 0, 9, 9, 0, 9, 9, 0, 0, 0, 0, 0, 25, 25, 58, 0, 0, 25, 25, 9, 0, 0, 0, 0, 9, 25, 0, 9, 25, 0, 25, 25, 0, 0, 25, 0, 25, 9, 9, 0, 0, 0, 58, 82, 9, 0, 0, 58, 58, 9, 0, 0, 9, 0, 0, 9, 9, 0, 9, 9, 0, 0, 0, 0, 0, 0, 9, 25, 0, 9, 0, 25, 25, 0, 0, 9, 25, 0, 9, 25, 0, 0, 0, 25, 9, 0, 0, 25, 9, 9, 9, 0, 0, 0, 0, 9, 0, 25, 25, 0, 9, 0, 25, 25, 0, 0, 9, 25, 0, 9, 0, 25, 25, 0, 0, 0, 0, 25, 9, 9, 0, 0, 25, 9, 9, 9, 0, 0, 0, 0, 25, 25, 58, 9, 0, 0, 0, 0, 25, 25, 0, 25, 25, 0, 25, 58, 9, 0, 82, 0, 0, 0, 0, 9, 0, 58, 82, 0, 9, 0, 58, 82, 82, 0, 0, 0, 0, 58, 82, 9, 0, 0, 58, 82, 9, 9, 0, 0, 0, 9, 9, 0, 9, 9, 9]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P707
