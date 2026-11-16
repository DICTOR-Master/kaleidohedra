module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P225
open YantraCert

def cell : Cell := ⟨7, 45, 6, 0, 6, 16⟩
noncomputable def codes : TC := TC.ofList [0, 25, 0, 0, 0, 226, 0, 1, 0, 0, 130, 0, 9, 0, 0, 258, 0, 9, 0, 0, 66, 0, 0, 0, 66, 25, 0, 66, 25, 9, 0, 66, 0, 0, 0, 66, 25, 66, 0, 9, 66, 258, 0, 41, 258, 9, 0, 0, 226, 0, 0, 9, 0, 41, 258, 1, 138]

theorem ok : checkTree C 18 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P225
