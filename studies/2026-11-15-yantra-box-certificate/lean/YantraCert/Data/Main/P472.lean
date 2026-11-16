module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P472
open YantraCert

def cell : Cell := ⟨22, 3147567, 22, 1896712, 22, 2179578⟩
noncomputable def codes : TC := TC.ofList [0, 25, 0, 0, 9, 0, 0, 0, 9, 0, 0, 3, 25, 9, 0, 9, 0, 25, 9, 9, 0, 9, 0, 25, 9]

theorem ok : checkTree C 10 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P472
