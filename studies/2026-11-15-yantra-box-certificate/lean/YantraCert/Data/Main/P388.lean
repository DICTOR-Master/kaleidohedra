module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P388
open YantraCert

def cell : Cell := ⟨2, 2, 2, 1, 2, 3⟩
noncomputable def codes : TC := TC.ofList [0, 9, 210]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P388
