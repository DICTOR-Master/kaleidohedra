module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P90
open YantraCert

def cell : Cell := ⟨9, 138, 9, 3, 8, 58⟩
noncomputable def codes : TC := TC.ofList [18]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P90
