module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P289
open YantraCert

def cell : Cell := ⟨4, 8, 3, 1, 3, 3⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 0, 41, 9, 25, 9, 0, 0, 9, 25, 9, 9, 18, 9, 306, 9, 290]

theorem ok : checkTree C 16 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P289
