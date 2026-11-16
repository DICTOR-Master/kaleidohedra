module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P788
open YantraCert

def cell : Cell := ⟨2, 3, 2, 3, 1, 1⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 306, 0, 0, 0, 306, 0, 0, 0, 0, 0, 0, 306, 26, 9, 306, 0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 9, 0, 9, 9, 0, 0, 306, 0, 0, 0, 9, 9, 9, 306, 0, 9, 9, 0, 306, 9, 0, 0, 306, 0, 306, 306, 0, 306, 9, 0, 306, 0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 9, 0, 0, 306, 0, 0, 0, 306, 306, 0, 306, 9, 306, 0, 306, 0, 0, 0, 9, 9, 9, 306, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 9, 9, 0, 9, 9, 0, 0, 0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 9, 9, 0, 9, 9, 0, 0, 0, 9, 9, 9, 0, 0, 9, 9, 9, 0, 0, 0, 9, 9, 0, 9, 9, 9, 19, 0, 0, 0, 0, 9, 9, 0, 9, 9, 0, 0, 9, 9, 0, 9, 9, 0, 0, 0, 9, 9, 0, 9, 9, 19]

theorem ok : checkTree C 16 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P788
