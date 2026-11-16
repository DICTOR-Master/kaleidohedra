module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P587
open YantraCert

def cell : Cell := ⟨3, 6, 3, 5, 3, 2⟩
noncomputable def codes : TC := TC.ofList [0, 9, 9]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P587
