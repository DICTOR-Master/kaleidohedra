module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P316
open YantraCert

def cell : Cell := ⟨4, 10, 4, 5, 3, 3⟩
noncomputable def codes : TC := TC.ofList [0, 0, 306, 0, 0, 9, 9, 26, 0, 306, 0, 0, 0, 26, 0, 0, 9, 0, 0, 0, 9, 25, 25, 9, 0, 9, 0, 25, 9, 0, 26, 0, 0, 0, 0, 0, 25, 9, 25, 0, 0, 0, 25, 0, 0, 9, 0, 25, 9, 25, 0, 9, 0, 0, 0, 25, 25, 9, 25, 0, 0, 25, 25, 0, 9, 25, 9, 0, 0, 25, 0, 0, 25, 25, 25, 9, 0, 26, 0, 306, 0, 26, 306]

theorem ok : checkTree C 16 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P316
