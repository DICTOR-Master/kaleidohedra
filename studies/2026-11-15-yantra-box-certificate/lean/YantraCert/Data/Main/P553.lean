module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P553
open YantraCert

def cell : Cell := ⟨9, 384, 8, 117, 8, 133⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 25, 0, 25, 25, 9, 0, 25, 9]

theorem ok : checkTree C 6 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P553
