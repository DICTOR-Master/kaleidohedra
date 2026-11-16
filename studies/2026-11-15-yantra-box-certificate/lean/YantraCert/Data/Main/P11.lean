module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P11
open YantraCert

def cell : Cell := ⟨9, 128, 9, 3, 8, 56⟩
noncomputable def codes : TC := TC.ofList [41]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P11
