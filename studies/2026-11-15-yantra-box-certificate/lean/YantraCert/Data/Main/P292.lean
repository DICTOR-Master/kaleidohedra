module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P292
open YantraCert

def cell : Cell := ⟨5, 18, 5, 4, 5, 13⟩
noncomputable def codes : TC := TC.ofList [0, 9, 9]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P292
