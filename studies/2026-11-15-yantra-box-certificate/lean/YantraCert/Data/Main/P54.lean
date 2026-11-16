module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P54
open YantraCert

def cell : Cell := ⟨9, 133, 9, 2, 9, 114⟩
noncomputable def codes : TC := TC.ofList [9]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P54
