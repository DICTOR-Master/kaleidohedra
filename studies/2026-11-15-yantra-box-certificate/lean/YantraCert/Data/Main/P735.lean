module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P735
open YantraCert

def cell : Cell := ⟨6, 52, 5, 21, 5, 16⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 9, 0, 0, 9, 9, 0, 9, 9, 0, 0, 0, 0, 26, 26, 0, 26, 9, 26, 0, 0, 0, 0, 0, 0, 9, 25, 0, 25, 25, 0, 0, 9, 25, 0, 25, 25, 0, 0, 0, 0, 25, 25, 0, 0, 25, 25, 25, 9, 0, 0, 25, 0, 25, 25, 9, 9, 0, 0, 0, 0, 0, 9, 25, 0, 25, 25, 26, 0, 0, 0, 25, 25, 9, 0, 0, 25, 25, 9, 9, 0, 0, 9, 0, 0, 9, 9, 26, 0, 306, 0, 0, 0, 26, 0, 0, 0, 25, 25, 9, 26, 9, 26]

theorem ok : checkTree C 13 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P735
