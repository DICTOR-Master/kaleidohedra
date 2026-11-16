module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P531
open YantraCert

def cell : Cell := ⟨12, 3075, 11, 926, 11, 1064⟩
noncomputable def codes : TC := TC.ofList [25]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P531
