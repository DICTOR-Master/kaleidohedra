module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P782
open YantraCert

def cell : Cell := ⟨5, 27, 5, 22, 5, 17⟩
noncomputable def codes : TC := TC.ofList [0, 9, 9]

theorem ok : checkTree C 3 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P782
