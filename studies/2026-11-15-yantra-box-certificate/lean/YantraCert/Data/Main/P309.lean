module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P309
open YantraCert

def cell : Cell := ⟨4, 10, 4, 4, 4, 6⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 9, 0, 26, 0, 0, 9, 0, 9, 9, 0, 9, 0, 9, 9, 26, 0, 0, 9, 9, 0, 9, 9]

theorem ok : checkTree C 9 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P309
