module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P715
open YantraCert

def cell : Cell := ⟨5, 27, 4, 9, 4, 8⟩
noncomputable def codes : TC := TC.ofList [0, 82, 0, 0, 0, 82, 0, 0, 0, 82, 0, 0, 82, 82, 0, 82, 9, 82, 9, 82, 0, 9, 9]

theorem ok : checkTree C 11 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P715
