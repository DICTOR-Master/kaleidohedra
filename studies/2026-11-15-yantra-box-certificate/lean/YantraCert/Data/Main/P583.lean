module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P583
open YantraCert

def cell : Cell := ⟨2, 3, 2, 1, 2, 3⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 9, 9, 0, 9, 9, 0, 0, 9, 9, 0, 9, 9, 0, 0, 0, 9, 9, 0, 9, 9, 0, 0, 9, 9, 0, 9, 9]

theorem ok : checkTree C 6 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P583
