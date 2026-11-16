module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P464
open YantraCert

def cell : Cell := ⟨22, 3147567, 21, 948354, 21, 1089789⟩
noncomputable def codes : TC := TC.ofList [25]

theorem ok : checkTree C 2 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P464
