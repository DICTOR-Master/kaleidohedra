module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P372
open YantraCert

def cell : Cell := ⟨9, 382, 8, 115, 8, 132⟩
noncomputable def codes : TC := TC.ofList [0, 25, 25]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P372
