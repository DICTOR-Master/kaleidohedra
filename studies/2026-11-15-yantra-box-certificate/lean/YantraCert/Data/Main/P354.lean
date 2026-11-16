module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P354
open YantraCert

def cell : Cell := ⟨5, 22, 4, 7, 4, 8⟩
noncomputable def codes : TC := TC.ofList [306]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P354
