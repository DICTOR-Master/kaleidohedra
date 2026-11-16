module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P458
open YantraCert

def cell : Cell := ⟨21, 1573782, 20, 474177, 20, 544894⟩
noncomputable def codes : TC := TC.ofList [0, 0, 25, 41, 25]

theorem ok : checkTree C 4 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P458
