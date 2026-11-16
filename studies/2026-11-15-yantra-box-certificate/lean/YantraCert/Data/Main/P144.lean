module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P144
open YantraCert

def cell : Cell := ⟨7, 36, 6, 0, 6, 15⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 9, 0, 226, 0, 0, 9, 0, 226, 0, 0, 9, 0, 266, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 0, 66, 0, 0, 9, 0, 25, 25, 1, 0, 66, 0, 0, 0, 25, 25, 0, 25, 25, 1, 1, 0, 0, 0, 0, 0, 9, 0, 25, 25, 1, 41, 0, 0, 0, 0, 25, 25, 0, 25, 25, 1, 41, 1, 1, 0, 0, 9, 0, 41, 25, 1, 1, 1, 1, 1, 306]

theorem ok : checkTree C 24 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P144
