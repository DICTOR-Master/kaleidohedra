module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P557
open YantraCert

def cell : Cell := ⟨7, 96, 7, 58, 7, 67⟩
noncomputable def codes : TC := TC.ofList [0, 9, 9]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P557
