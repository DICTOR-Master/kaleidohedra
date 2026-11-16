module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P529
open YantraCert

def cell : Cell := ⟨13, 6149, 12, 1853, 12, 2128⟩
noncomputable def codes : TC := TC.ofList [0, 25, 0, 9, 0, 0, 25, 0, 9, 0, 41, 25, 25]

theorem ok : checkTree C 8 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P529
