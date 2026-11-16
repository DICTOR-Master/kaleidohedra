module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P476
open YantraCert

def cell : Cell := ⟨22, 3147567, 22, 1896713, 21, 1089789⟩
noncomputable def codes : TC := TC.ofList [0, 25, 0, 9, 0, 0, 0, 25, 0, 0, 25, 9, 25, 9, 25]

theorem ok : checkTree C 9 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P476
