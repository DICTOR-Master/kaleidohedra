module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P253
open YantraCert

def cell : Cell := ⟨5, 12, 5, 0, 5, 9⟩
noncomputable def codes : TC := TC.ofList [0, 9, 210]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P253
