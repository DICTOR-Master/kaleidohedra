module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P371
open YantraCert

def cell : Cell := ⟨8, 191, 8, 114, 8, 133⟩
noncomputable def codes : TC := TC.ofList [0, 9, 0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 9]

theorem ok : checkTree C 6 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P371
