module

public import YantraCert.Data.Main.Polys

@[expose] public section

namespace YantraCert.Data.Main.P779
open YantraCert

def cell : Cell := ⟨7, 109, 7, 91, 6, 32⟩
noncomputable def codes : TC := TC.ofList [0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 25, 0, 0, 0, 25, 25, 0, 25, 25, 0, 25, 25, 0, 0, 25, 25, 9, 0, 0, 25, 0, 0, 25, 25, 25, 0, 0, 25, 25, 9, 0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 25, 25, 9, 0, 25, 9, 9, 0, 0, 25, 0, 25, 25, 9, 9, 9, 0, 0, 0, 0, 0, 25, 25, 9, 0, 0, 25, 25, 9, 9, 9, 9, 0, 0, 0, 0, 0, 25, 0, 25, 25, 0, 25, 9, 0, 0, 25, 25, 0, 25, 9, 0, 0, 0, 0, 0, 25, 9, 25, 9, 9, 0, 0, 0, 25, 25, 9, 9, 9, 9, 9]

theorem ok : checkTree C 16 cell codes = true := by decide +kernel

end YantraCert.Data.Main.P779
