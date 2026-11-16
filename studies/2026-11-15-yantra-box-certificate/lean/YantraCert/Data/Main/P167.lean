module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P167
open YantraCert

def cell : Cell := ⟨7, 39, 7, 0, 6, 15⟩
noncomputable def codes : TC := TC.ofList [226]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P167
