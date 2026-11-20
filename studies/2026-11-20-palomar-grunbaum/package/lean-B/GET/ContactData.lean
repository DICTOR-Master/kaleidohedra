module

public import GET.Contact

@[expose] public section

/-! Kernel check: every contact between a cell of GET B and a cell of a neighbouring lattice translate is empty or
lies in one face of GET B (26 × 16 × 16 cell pairs). -/

namespace GET

/-- every contact between a cell of `PB` and a cell of a neighbouring translate lies in a face of `PB` -/
theorem B_contacts : ∀ a ∈ L3, ∀ b ∈ L3, ∀ c ∈ L3, ¬ (a = 0 ∧ b = 0 ∧ c = 0) →
    ∀ i j : Fin 16, contactOK (CB i) ((CB j).shift (lv ![a, b, c])) = true := by decide +kernel

end GET
