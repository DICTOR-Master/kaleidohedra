module

public import YantraCert.ExistFinal

@[expose] public section

/-!
# Kulaichev's Śrī Yantra is unique (library form)

Existence: the figure `ystar`, rebuilt from the zero of `F~` in the small Krawczyk box (`ExistFinal`). Uniqueness: `unique`
(`Unique4`). The slope: `slope`.
-/

namespace YantraCert.Y

theorem kulaichev_unique : ∃! y : Yantra, y.Huet ∧ y.Kulaichev ∧ y.Admissible :=
  ⟨ystar, ystar_ok, fun y' h' => unique y' ystar h' ystar_ok⟩

theorem kulaichev_slope (y : Yantra) (h : y.Huet ∧ y.Kulaichev ∧ y.Admissible) :
    (3379673547380287 : ℝ) / 4503599627370496 ≤ y.w 6 / y.b 6 ∧
      y.w 6 / y.b 6 ≤ (3379675694863935 : ℝ) / 4503599627370496 := slope y h

end YantraCert.Y
