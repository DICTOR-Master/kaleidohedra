# Candidate K: uniqueness and existence of Kulaichev's Śrī Yantra (a finished Lean entry)

## Abstract (neutral)

The Śrī Yantra is drawn as nine isosceles triangles with a common vertical axis inside a circle. Huet's incidence conditions (in Chiodo's form) leave four free real parameters. In 1984 A. P. Kulaichev added four conditions that fix one rigid figure, and asked whether that figure is unique. This entry proves, in Lean 4 with Mathlib, that under Huet's conditions, Kulaichev's four conditions and a stated admissibility (non-degeneracy) condition there is exactly one figure (existence and uniqueness), and it isolates its slope w7/b7 in an interval of width 2^-21 around 0.7504385160222140…

The proof is computer-assisted and fully kernel-checked: no `sorry`, no `native_decide`; `#print axioms` gives only `propext`, `Classical.choice`, `Quot.sound`. It consists of: (1) a forced construction showing the conditions reduce to three polynomial equations in three box coordinates (u, τ, ρ) on [0,1]×[0,1]×[0,6], with identities checked by a verified sparse-polynomial normaliser; (2) a branch-and-bound interval certificate (64,613 rational boxes in 10 charts, including blow-up charts at two degenerate boundary corners), each box closed by a proved-sound sign test (monotone split or slope form) on an equation or on an admissibility inequality; (3) one remaining box of half-width 2^-22 in which a Krawczyk test proves exactly one zero (uniqueness by contraction, existence by Banach's fixed-point theorem); (4) a proof that the figure rebuilt from that zero meets every condition. The Challenge file is 116 lines and imports only Mathlib.

Prior work on this figure by the same author (a Zenodo preprint, not peer reviewed): the slope is a root of an explicit irreducible integer polynomial of degree 348, with certified existence of the configuration, and an earlier certified (non-Lean) uniqueness census by elimination (degree-1744 resultant). The Lean entry does not formalise the degree-348 minimal polynomial; it gives the isolating interval instead.

## The published problem (sources, exact citations)

- **A. P. Kulaichev**, "Śrīyantra and its mathematical properties", *Indian Journal of History of Science* 19.3 (1984) 279–292. Imposes conditions (a)–(d) below, argues for a solution by iterated approximation (p. 284), and asks whether it is unique (p. 285). He reduces the system to one polynomial "of a single variable with a power not higher than 12544" (as quoted by Pustynski 2014, p. 269). Note: the available scan has no text layer; the page references are as cited by Chiodo 2021.
- **A. Chiodo**, "On the construction of the Śrī Yantra", *Comptes Rendus Mathématique* 359 (2021) 377–397, doi:10.5802/crmath.163. French version, p. 384: Kulaichev "fournit un raisonnement qui indique l'existence d'une solution et il se pose la question (toujours ouverte) de l'unicité" (gives an argument that indicates a solution exists, and asks the question, still open, of uniqueness). English §1.2.4 "The search for a unique Śrī Yantra", p. 387: "This problem is not considered here." Chiodo also proves that every yantra meeting Huet's conditions is constructible by straightedge and compass from its four parameters.
- **V.-V. Pustynski**, "On mathematical complexity of Śrīyantra", *Indian Journal of History of Science* 49.3 (2014) 268–277. Solves the system numerically to 15 figures (Table 1, p. 274); argues uniqueness from residual plots on dense grids (pp. 273–274); writes (p. 275) that a "purely analytical solution of the final two steps is probably impossible since the corresponding equations are too unwieldy".
- **G. Huet**, "Sri Yantra Geometry", *Theoretical Computer Science* 281 (2002) 609–628: the incidence conditions.

No other published statement of the uniqueness question was found by the submitter. Chiodo's bibliography also names C. S. Rao (1998, IJHS 33) on the same constrained figure; not read by the submitter.

## The Lean statement (Challenge, verbatim definitions and theorems)

```lean
import Mathlib
namespace KulaichevYantra

/-- nine isosceles triangles with a common vertical axis: `t(i+1)` has base depth `b i`, base half-width `w i` and apex depth `a i` -/
structure Yantra where
  b : Fin 9 → ℝ
  w : Fin 9 → ℝ
  a : Fin 9 → ℝ

def lineThrough (x₁ d₁ x₂ d₂ : ℝ) : ℝ × ℝ × ℝ := (d₁ - d₂, x₂ - x₁, x₁ * d₂ - x₂ * d₁)

/-- three lines pass through one point (or are parallel): their coefficient determinant vanishes -/
def Concurrent (l₁ l₂ l₃ : ℝ × ℝ × ℝ) : Prop :=
  l₁.1 * (l₂.2.1 * l₃.2.2 - l₂.2.2 * l₃.2.1) - l₁.2.1 * (l₂.1 * l₃.2.2 - l₂.2.2 * l₃.1) +
    l₁.2.2 * (l₂.1 * l₃.2.1 - l₂.2.1 * l₃.1) = 0

def Yantra.leg (y : Yantra) (i : Fin 9) : ℝ × ℝ × ℝ := lineThrough (y.w i) (y.b i) 0 (y.a i)
def Yantra.base (y : Yantra) (i : Fin 9) : ℝ × ℝ × ℝ := lineThrough (-y.w i) (y.b i) (y.w i) (y.b i)
/-- circle of diameter 1 through the top point (0,0); depth d measured downwards -/
def OnCircle (x d : ℝ) : Prop := x ^ 2 + d ^ 2 - d = 0
def InDisc (x d : ℝ) : Prop := x ^ 2 + d ^ 2 - d ≤ 0

/-- Huet's conditions in Chiodo's form (indices are `i - 1` for `ti`) -/
def Yantra.Huet (y : Yantra) : Prop :=
  -- great triangles t3, t7 inscribed
  y.a 2 = 1 ∧ y.a 6 = 0 ∧ OnCircle (y.w 2) (y.b 2) ∧ OnCircle (y.w 6) (y.b 6) ∧
  -- seven apexes on bases
  y.a 7 = y.b 0 ∧ y.a 5 = y.b 1 ∧ y.a 8 = y.b 2 ∧ y.a 0 = y.b 5 ∧ y.a 4 = y.b 6 ∧ y.a 3 = y.b 7 ∧ y.a 1 = y.b 8 ∧
  -- nine marma pairs (leg of p, base of q, leg of r concur)
  Concurrent (y.leg 0) (y.base 1) (y.leg 6) ∧ Concurrent (y.leg 1) (y.base 2) (y.leg 6) ∧
  Concurrent (y.leg 0) (y.base 2) (y.leg 7) ∧ Concurrent (y.leg 0) (y.base 3) (y.leg 5) ∧
  Concurrent (y.leg 0) (y.base 4) (y.leg 8) ∧ Concurrent (y.leg 3) (y.base 5) (y.leg 8) ∧
  Concurrent (y.leg 1) (y.base 6) (y.leg 8) ∧ Concurrent (y.leg 2) (y.base 6) (y.leg 7) ∧
  Concurrent (y.leg 2) (y.base 7) (y.leg 8) ∧
  -- three corner touches
  Concurrent (y.leg 3) (y.base 3) (y.leg 7) ∧ Concurrent (y.leg 4) (y.base 4) (y.leg 5) ∧
  Concurrent (y.leg 1) (y.base 5) (y.leg 5)

/-- Kulaichev's conditions (a)–(d) -/
def Yantra.Kulaichev (y : Yantra) : Prop :=
  -- (a) t3 ≅ t7
  (y.a 2 - y.b 2 = y.b 6 - y.a 6 ∧ y.w 2 = y.w 6) ∧
  -- (b) corners of t1 on the circle
  OnCircle (y.w 0) (y.b 0) ∧
  -- (c) corners of t9 on the circle
  OnCircle (y.w 8) (y.b 8) ∧
  -- (d) the centre (0, 1/2) is the incentre of the triangle bounded by t1's legs and t5's base
  (y.b 4 < 1 / 2 ∧ 1 / 2 < y.a 0 ∧
    1 / 2 - y.b 4 = y.w 0 * (y.a 0 - 1 / 2) / Real.sqrt ((y.a 0 - y.b 0) ^ 2 + y.w 0 ^ 2))

/-- admissibility: bases strictly ordered, half-widths positive, apexes on the correct side
(t1–t5 point down), corners in the closed disc -/
def Yantra.Admissible (y : Yantra) : Prop :=
  (∀ i : Fin 8, y.b i.castSucc < y.b i.succ) ∧ (∀ i, 0 < y.w i) ∧
  (∀ i : Fin 9, (i : ℕ) < 5 → y.b i < y.a i) ∧ (∀ i : Fin 9, 5 ≤ (i : ℕ) → y.a i < y.b i) ∧
  (∀ i, InDisc (y.w i) (y.b i))

theorem kulaichev_unique : ∃! y : Yantra, y.Huet ∧ y.Kulaichev ∧ y.Admissible := by sorry

theorem kulaichev_slope (y : Yantra) (h : y.Huet ∧ y.Kulaichev ∧ y.Admissible) :
    (3379673547380287 : ℝ) / 4503599627370496 ≤ y.w 6 / y.b 6 ∧
      y.w 6 / y.b 6 ≤ (3379675694863935 : ℝ) / 4503599627370496 := by sorry

end KulaichevYantra
```

The frame (diameter 1, depth measured from the top point, t1–t5 pointing down, right half by mirror symmetry) fixes scale, orientation and labels, so "exactly one" means exactly one 27-tuple (b, w, a). Admissibility is the submitter's formalisation of a non-degenerate yantra; it is not taken verbatim from Kulaichev.

## Statements to score

K1. `kulaichev_unique` together with `kulaichev_slope` (score as one result group).
