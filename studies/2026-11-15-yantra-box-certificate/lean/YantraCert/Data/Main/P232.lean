module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P232
open YantraCert

def cell : Cell := ⟨6, 23, 6, 0, 5, 8⟩
noncomputable def codes : TC := TC.ofList [0, 138, 138]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P232
