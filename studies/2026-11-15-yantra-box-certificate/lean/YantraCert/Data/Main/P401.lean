module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P401
open YantraCert

def cell : Cell := ⟨13, 6147, 13, 3702, 12, 2128⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 25, 0, 9, 0, 25, 25, 25, 25]

theorem ok : checkTree C 7 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P401
