module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P142
open YantraCert

def cell : Cell := ⟨7, 36, 7, 1, 6, 14⟩
noncomputable def codes : TC := TC.ofList [306]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P142
