module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P618
open YantraCert

def cell : Cell := ⟨8, 221, 7, 92, 7, 63⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 0, 25, 9, 9, 0, 0, 0, 25, 25, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 25, 9, 0, 25, 9, 9, 9, 0, 0, 0, 0, 0, 25, 9, 9, 0, 0, 25, 9, 9, 9, 9, 9, 9]

theorem ok : checkTree C 11 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P618
