# Candidate V2: Kulaichev's Śrī Yantra is unique, and so is the one with the golden slope product (Version 2 of a registered Lean entry)

<!-- Blind input, 20 Nov 2026. The submitter is never named. The submitter's own names for the fourth condition, for the yantra it gives and
     for the two solids are replaced by neutral words ("golden slope product", "golden-product yantra", "face pyramid of the icosahedron",
     "golden antiprism"). -->

## Abstract (neutral)

The Śrī Yantra is drawn as nine isosceles triangles with a common vertical axis inside a circle. Huet's incidence conditions (in Chiodo's form) leave four free real parameters. In 1984 A. P. Kulaichev added four conditions, (a) the two great triangles congruent, (b) and (c) the corners of the smallest top and bottom triangles on the circle, (d) the circle's centre at the incentre of the innermost triangle, to fix one rigid figure, and asked whether it is unique (p. 285); Chiodo (2021) calls that question still open.

Version 1 of this entry, already registered on Palomar, proves Kulaichev's uniqueness in Lean 4 with Mathlib: under Huet's conditions, Kulaichev's four conditions and a stated admissibility condition there is exactly one figure (existence and uniqueness), with slope w7/b7 in an interval of width 2⁻²¹ around 0.7504385160…. That figure is not the traditional yantra: it has 45 odd regions (4 of them four-sided) and 28 sandhis, not 43 triangles and 24 sandhis.

**Version 2** adds a second theorem to the same entry: replace Kulaichev's (a) by the **golden slope product** uv = 2/φ³ = 2√5 − 4 (u = w7/b7 the slope of the upper great triangle t7, v = w3/(1 − b3) that of the lower one, t3), keeping Huet's conditions, (b), (c), (d) and admissibility; then again exactly one figure exists, with w7/b7 in an interval of width 2⁻²¹ around 0.6793185887…. The fourth condition is the submitter's, from a construction with solids described below; no outside source asks for it. The figure it fixes has the traditional 43 triangles and 24 sandhis; those counts are certified in the submitter's paper and are **not** formalised. The two theorems together say: Kulaichev's conditions force one figure, which is not the traditional one; changing only the fourth condition to the golden product forces one figure, which is.

Facts on the Version 1 proof (Theorem 14, built and registered): Lean v4.35.0-rc2, Mathlib v4.35.0-rc2, module system; about 7,370 hand-written or generated top-level lines plus 1,369 generated data and derivation files; no `sorry`, no `native_decide`; axioms propext, Classical.choice, Quot.sound; the comparator accepts with Lean's kernel, NanoDa and con-ron; three negative controls rejected. Method: a forced construction reduces the conditions to three polynomial equations on a box, identities checked by a verified sparse-polynomial normaliser; a branch-and-bound interval certificate of 64,613 rational boxes in 10 charts (with blow-up charts at two degenerate corners), each box closed by a proved-sound sign test; one Krawczyk box proving exactly one zero; a proof that the rebuilt figure meets every condition.

Theorem 15 in Lean is **planned, not built**: score it as if proved exactly as stated. A statement pilot (the two new definitions and the two theorems, with `sorry`) compiles against Version 1's library; it also proves, by `Iff.rfl`, that Version 1's `Kulaichev` is exactly (a) ∧ `KulaichevBCD`, so (b), (c), (d) are reused word for word. The planned proof is the same method as Version 1, adapted: √5 in the coefficients, a box unbounded in u (split at u = 1, using v = c/u beyond it), and a new analysis of the degenerate corners.

Limits stated by the author: the counts (45 / 28 and 43 / 24) are outside Lean; admissibility is the submitter's formalisation of a non-degenerate yantra, not taken verbatim from Kulaichev; (d) must be read with the incircle (the strict inequality b5 < 1/2), since the equidistance reading alone admits a second, excentre solution at u = 0.57120 under the golden product.

## The published question and prior work (sources, exact citations)

- **A. P. Kulaichev**, "Śrīyantra and its mathematical properties", *Indian Journal of History of Science* 19.3 (1984) 279–292. Read from the publisher's (INSA) free scan as page images. Imposes conditions (a)–(d) on Huet's figure; p. 284: "it may be presumed that there is, at least, one real solution (root)"; p. 285: the system "may or may not possess other real roots. The modern theory (higher algebra) does not give a direct answer to this question", with a degree bound of 12544. Kulaichev's conditions are (a) the two great triangles congruent, (b) t1's corners on the circle, (c) t9's corners on the circle, (d) the centre is the incentre of the innermost triangle.
- **A. Chiodo**, "On the construction of the Śrī Yantra", *Comptes Rendus Mathématique* 359 (2021) 377–397, doi:10.5802/crmath.163 (open access, read in full). p. 381 (French): Kulaichev "fournit un raisonnement qui indique l'existence d'une solution et il se pose la question (toujours ouverte) de l'unicité". p. 387 (English, §1.2.4): Kulaichev "discusses whether the solution is unique (p. 285), estimates the complexity, and argues that the answer is out of reach. This problem is not considered here." Chiodo proves that every yantra meeting Huet's conditions is constructible by straightedge and compass from its four parameters.
- **V.-V. Pustynski**, "On mathematical complexity of Śrīyantra", *Indian Journal of History of Science* 49.3 (2014) 268–277 (read). Solves Kulaichev's system numerically; argues uniqueness from residual plots on grids of 10,000 points with no error bounds (p. 274: "This proves that Śrīyantra with restrictions set in (4) has a unique solution"); remarks on "two additional tiny triangles" in that figure (§2.5).
- **G. Huet**, "Sri Yantra Geometry", *Theoretical Computer Science* 281 (2002) 609–628 (author's version read, pp. 1–19): the incidence conditions; "a problem with 4 degrees of freedom, which admits several solutions" (p. 2).
- **C. S. Rao**, "Śrīyantra – a study of spherical and plane forms", *IJHS* 33.3 (1998) 203–227 (read, INSA scan): numerical solutions only; p. 224, his constraints 1, 2, 8, 9, 20 give Kulaichev's figure; p. 226: "an unlimited number of figures" meet the traditional specifications. No uniqueness claim.
- **G. D. Chapati, R. Chapati**, "Verified Reconstruction of the Śrī Yantra", Zenodo (2026), doi:10.5281/zenodo.23188650 (read): numerical reconstruction of Huet's yantra, the 43 counted as star points; states that the system has no closed-form solution.
- Read, nothing on uniqueness: B. Santhi et al. 2012 (*RJASET* 4(14)); G. A. Tularam 2012 (*IJMGTA* 20(2)); Kavi Mahesh 2023 (*Int. J. Sanskrit Research* 9(6)). Not read: D. Tahta 1992 (*Math. Gazette* 76, paywalled); Kulaichev's "Addition" (no accessible text); a Synapse pre-registration on Rao's constraint system (could not be opened; a search snippet describes a planned certified enumeration with no result); salahealer9, sri-yantra-constraint-engine (GitHub; Zenodo 10.5281/zenodo.20617730), a numerical reimplementation of Rao's system with no uniqueness claim (read only as a summary of the repository page).

**The golden product: where it comes from (#103, §9.1 and §§4–5; no outside source asks for it).** The submitter's paper #103 places solids on the yantra: spun about the axis, a solid with its tip on the axis sweeps a cone, and a great triangle of slope s is the section of such a cone. Two solids from the submitter's earlier Zenodo papers give the two slopes. (1) The face pyramid of the regular icosahedron (cut from its centre to one face; #29 of the submitter's series) sweeps a cone of slope 2/φ². (2) A golden antiprism (#44), the partner with which two of those pyramids fill the prolate golden rhombohedron, has side faces of slope exactly 1/φ. Their product is 2/φ³ = 2√5 − 4. #103's Theorem 5 (the viewpoint principle) shows that the perspective maps of the disc onto itself (translations of Klein's model along the axis) keep the incidences, (b), (c) and the region counts, multiply u by λ and divide v by λ, so they keep the product uv; they do not keep the incircle centre, so a viewpoint can win (d). The undistorted pair (u = 2/φ², v = 1/φ) with (b) and (c) does not meet (d) (its innermost triangle's incircle is centred 0.058 of the diameter above the circle's centre); the yantra of Theorem 15 is that pair seen from the one viewpoint that centres it, hence the condition is the product, not the two slopes. #103 states plainly (§10.1): "Equal great triangles (Kulaichev) and the [golden] product uv = 2/φ³ are two choices of that fourth condition, and the family cannot single out 'the' yantra by itself. What the choices give is a fact: Kulaichev's choice gives two extra tiny triangles, [the golden product] keeps the traditional 43 and 24." #103 also lists (Table 3, computed with 60-digit arithmetic, not certified) other fourth conditions from solids that meet every condition with 43 triangles: the product (2/φ²)(1/√2) of the icosahedron's face pyramid and the regular tetrahedron seen from a viewpoint, and v = 1/√2 (the stella octangula's tetrahedron) with u free. So the golden product is not the only fourth condition that gives the traditional form; it is the one #103 solves exactly (degree 160, Theorem 9) and proves unique (Theorem 15). #103 does not say the product was chosen to obtain the counts, and this account does not claim either way.

**The counts.** Theorem 14 (Kulaichev's yantra) and Theorem 15 differ only in the fourth condition. Kulaichev's unique yantra has 45 odd regions (41 triangles, 4 four-sided) and 28 two-line crossings ("sandhis"), confirming Pustynski's remark; the golden-product yantra has the traditional 43 triangles, 18 marmas and 24 sandhis. Both counts are certified in #103 (Proposition 11: the planar arrangement of 27 sides built in 560-digit interval arithmetic, near-zero concurrencies decided exactly). **The counts are not formalised in Lean** and are not part of any theorem scored here; the 18 marmas are in the Lean statement as Huet's concurrencies.

Prior formalizations (searched 16 November 2026, for Version 1): Mathlib has no Śrī Yantra; GitHub Lean code search and web searches for Isabelle AFP, Rocq, HOL Light and Mizar found none, other than the submitter's own registered Palomar entry for Kulaichev's uniqueness (Version 1; see the abstract).

Prior work by the same author: #103 (its title carries the submitter's name and is left out here), Zenodo preprint, Version 5 (2026), doi:10.5281/zenodo.24379694 (not peer reviewed), which states and proves Theorems 14 and 15 by certified computation (exact elimination over ℚ and ℚ(√5), certified real-root isolation, ball arithmetic and Krawczyk tests, each with an independent second census), and Theorem 9 (the golden-product yantra's slope is a root of an irreducible integer polynomial of degree 160). The solids are from the submitter's earlier Zenodo papers (#29, #44), not peer reviewed.

What is claimed: a kernel-checked proof of Kulaichev's uniqueness (Version 1, unchanged) and, in Version 2, of the companion theorem that Huet's conditions, Kulaichev's (b)–(d), admissibility and the golden slope product fix exactly one Śrī Yantra; that this one is the traditional form is certified outside Lean and not claimed by the entry.

## The Lean statements (the proposed Version 2 Challenge file, verbatim)

The full proposed Challenge file follows: Version 1's Challenge with a second-theorem paragraph in the header, two new definitions and two new theorems (not yet built; the statements are those of a compiled pilot). Words changed for blindness: the submitter's name for the fourth condition (here `GoldenProduct`) and for the new theorems (here `golden_unique`, `golden_slope`); "#103 (the submitter's paper)" in place of the submitter's name. The Comparator configuration would name `kulaichev_unique`, `kulaichev_slope`, `golden_unique`, `golden_slope`, axioms propext, Quot.sound, Classical.choice.

```lean
module

public import Mathlib

@[expose] public section

/-!
# Kulaichev's Śrī Yantra is unique, and so is the golden-product Śrī Yantra

**Informal statement.** Take a circle of diameter 1 and nine isosceles triangles `t1, …, t9` with a common vertical axis,
`t1–t5` pointing down and `t6–t9` pointing up. Suppose they meet Huet's conditions, in the form given by Chiodo:

* the two great triangles `t3` and `t7` are inscribed;
* seven apexes lie on bases;
* the 18 marmas (nine mirror pairs of triple points: a leg, a base and a leg pass through one point) and the 6 corner
  touches (three mirror pairs) hold.

Add Kulaichev's four conditions:

* (a) the two great triangles are congruent;
* (b) the corners of `t1` lie on the circle;
* (c) the corners of `t9` lie on the circle;
* (d) the centre of the circle is the incentre of the innermost triangle, the one bounded by the legs of `t1` and the base
  of `t5`.

Finally, ask for admissibility as in #103 (the submitter's paper), Theorem 1: the bases are strictly ordered, every half-width is positive,
every apex lies on the correct side of its base, and every corner lies in the closed disc. Then exactly one such figure
exists. A. P. Kulaichev asked this question in 1984 (*IJHS* 19.3, p. 285: system 2 "may or may not possess other real
roots"; p. 284: "at least, one real solution" is presumed). Chiodo (*C. R. Math.* 359, 2021) called it still open
("toujours ouverte", p. 381; in English, p. 387: Kulaichev "argues that the answer is out of reach").

**Scope.** The same equations have one other real root in the range that admissibility needs, at `w7/b7 = 0.66866…`.
It is not admissible (its bases are out of order and two half-widths are negative), so it is not a yantra.

**Second theorem (#103, Theorem 15).** Keep Huet's conditions, Kulaichev's (b), (c), (d) and admissibility, and
replace (a) by the golden slope product: the slope `u = w7/b7` of `t7` times the slope `v = w3/(1 - b3)` of `t3` is
`2/φ³ = 2√5 - 4`. Then again exactly one figure exists, with `w7/b7` in an interval of width `2⁻²¹` around
`0.6793185887…`. Its equations have three other real solutions with `u > 0` in range. One (`u = 0.57120…`) is
admissible, but the circle's centre is then the centre of an excircle of the innermost triangle, beyond `t5`'s base, so
`b5 > 1/2` and (d) as stated excludes it; the other two are not admissible. The product is not Kulaichev's: it is the
product of the slopes of a pair of solids in #103, §9.1. Unlike Kulaichev's yantra (45 odd regions, 28 sandhis), this
one has the traditional 43 triangles and 24 sandhis; #103, Proposition 11 certifies those counts, and they are not
formalised here.

**Frame.** The axis is the line `x = 0`, and the depth `d` is measured downwards from the top point of the circle, so the
circle is `x² + d² - d = 0`. Triangle `t(i+1)` has base depth `b i`, base half-width `w i` and apex `(0, a i)`, for
`i : Fin 9`. By the mirror symmetry, each condition is stated on the right half. The labels, the orientation and the scale are
fixed by this frame, so "exactly one" means exactly one 27-tuple `(b, w, a)`.

**Sources.** G. Huet (*Theor. Comput. Sci.* 281, 2002) gave the conditions: a problem "with 4 degrees of freedom, which
admits several solutions" (author's version, pp. 2–3). A. Chiodo (2021, pp. 381, 387) gave the form used here.
A. P. Kulaichev (1984, pp. 284–285) added (a)–(d). C. S. Rao (*IJHS* 33.3, 1998) computed the same figure numerically,
as his constraints 1, 2, 8, 9, 20 (p. 224, Table 3), with no claim of uniqueness. V.-V. Pustynski (*IJHS* 49.3,
2014) concluded uniqueness from plots of each step on grids of 10,000 points (pp. 273–275), with no error bounds.
The submitter's #103 (Zenodo, 2026), Theorem 1, gives admissibility; its Theorems 14 and 15 are the two
theorems here.
-/

namespace KulaichevYantra

/-- nine isosceles triangles with a common vertical axis: `t(i+1)` has base depth `b i`, base half-width `w i` and apex
depth `a i` -/
structure Yantra where
  b : Fin 9 → ℝ
  w : Fin 9 → ℝ
  a : Fin 9 → ℝ

/-- the line through two points `(x₁, d₁)` and `(x₂, d₂)`, as coefficients `(A, B, C)` of `A x + B d + C = 0` -/
def lineThrough (x₁ d₁ x₂ d₂ : ℝ) : ℝ × ℝ × ℝ := (d₁ - d₂, x₂ - x₁, x₁ * d₂ - x₂ * d₁)

/-- three lines pass through one point (or are parallel): their coefficient determinant vanishes -/
def Concurrent (l₁ l₂ l₃ : ℝ × ℝ × ℝ) : Prop :=
  l₁.1 * (l₂.2.1 * l₃.2.2 - l₂.2.2 * l₃.2.1) - l₁.2.1 * (l₂.1 * l₃.2.2 - l₂.2.2 * l₃.1) +
    l₁.2.2 * (l₂.1 * l₃.2.1 - l₂.2.1 * l₃.1) = 0

/-- the right leg of `t(i+1)`: from its right corner `(w i, b i)` to its apex `(0, a i)` -/
def Yantra.leg (y : Yantra) (i : Fin 9) : ℝ × ℝ × ℝ := lineThrough (y.w i) (y.b i) 0 (y.a i)

/-- the base line of `t(i+1)` -/
def Yantra.base (y : Yantra) (i : Fin 9) : ℝ × ℝ × ℝ := lineThrough (-y.w i) (y.b i) (y.w i) (y.b i)

/-- a point lies on the circle of diameter 1 through the top point `(0, 0)` -/
def OnCircle (x d : ℝ) : Prop := x ^ 2 + d ^ 2 - d = 0

/-- a point lies in the closed disc -/
def InDisc (x d : ℝ) : Prop := x ^ 2 + d ^ 2 - d ≤ 0

/-- **Huet's conditions** in Chiodo's form (indices are `i - 1` for `ti`) -/
def Yantra.Huet (y : Yantra) : Prop :=
  -- (i) the great triangles t3 and t7 are inscribed: apexes at the bottom and top points, corners on the circle
  y.a 2 = 1 ∧ y.a 6 = 0 ∧ OnCircle (y.w 2) (y.b 2) ∧ OnCircle (y.w 6) (y.b 6) ∧
  -- (ii) seven apexes on bases: a8 = b1, a6 = b2, a9 = b3, a1 = b6, a5 = b7, a4 = b8, a2 = b9
  y.a 7 = y.b 0 ∧ y.a 5 = y.b 1 ∧ y.a 8 = y.b 2 ∧ y.a 0 = y.b 5 ∧ y.a 4 = y.b 6 ∧ y.a 3 = y.b 7 ∧ y.a 1 = y.b 8 ∧
  -- (iii) the nine marma pairs (leg of p, base of q, leg of r concur):
  --       (1,2,7) (2,3,7) (1,3,8) (1,4,6) (1,5,9) (4,6,9) (2,7,9) (3,7,8) (3,8,9)
  Concurrent (y.leg 0) (y.base 1) (y.leg 6) ∧ Concurrent (y.leg 1) (y.base 2) (y.leg 6) ∧
  Concurrent (y.leg 0) (y.base 2) (y.leg 7) ∧ Concurrent (y.leg 0) (y.base 3) (y.leg 5) ∧
  Concurrent (y.leg 0) (y.base 4) (y.leg 8) ∧ Concurrent (y.leg 3) (y.base 5) (y.leg 8) ∧
  Concurrent (y.leg 1) (y.base 6) (y.leg 8) ∧ Concurrent (y.leg 2) (y.base 6) (y.leg 7) ∧
  Concurrent (y.leg 2) (y.base 7) (y.leg 8) ∧
  --       and the three corner touches (4,4,8) (5,5,6) (2,6,6)
  Concurrent (y.leg 3) (y.base 3) (y.leg 7) ∧ Concurrent (y.leg 4) (y.base 4) (y.leg 5) ∧
  Concurrent (y.leg 1) (y.base 5) (y.leg 5)

/-- **Kulaichev's conditions** (a)–(d) -/
def Yantra.Kulaichev (y : Yantra) : Prop :=
  -- (a) t3 and t7 are congruent: equal heights and equal base half-widths
  (y.a 2 - y.b 2 = y.b 6 - y.a 6 ∧ y.w 2 = y.w 6) ∧
  -- (b) the corners of t1 lie on the circle
  OnCircle (y.w 0) (y.b 0) ∧
  -- (c) the corners of t9 lie on the circle
  OnCircle (y.w 8) (y.b 8) ∧
  -- (d) the centre (0, 1/2) is the incentre of the triangle bounded by the legs of t1 and the base of t5: it lies strictly
  --     between that base and the apex of t1, and its distance to the base equals its distance to the leg of t1
  (y.b 4 < 1 / 2 ∧ 1 / 2 < y.a 0 ∧
    1 / 2 - y.b 4 = y.w 0 * (y.a 0 - 1 / 2) / Real.sqrt ((y.a 0 - y.b 0) ^ 2 + y.w 0 ^ 2))

/-- **Kulaichev's conditions (b), (c), (d)**, word for word as in `Yantra.Kulaichev`, without (a) -/
def Yantra.KulaichevBCD (y : Yantra) : Prop :=
  -- (b) the corners of t1 lie on the circle
  OnCircle (y.w 0) (y.b 0) ∧
  -- (c) the corners of t9 lie on the circle
  OnCircle (y.w 8) (y.b 8) ∧
  -- (d) the centre (0, 1/2) is the incentre of the triangle bounded by the legs of t1 and the base of t5
  (y.b 4 < 1 / 2 ∧ 1 / 2 < y.a 0 ∧
    1 / 2 - y.b 4 = y.w 0 * (y.a 0 - 1 / 2) / Real.sqrt ((y.a 0 - y.b 0) ^ 2 + y.w 0 ^ 2))

/-- **the golden slope product** (#103, §9.1): the slope `u = w7 / b7` of the upper great triangle t7 times the slope
`v = w3 / (1 - b3)` of the lower great triangle t3 is `2/φ³ = 2√5 - 4` -/
def Yantra.GoldenProduct (y : Yantra) : Prop :=
  (y.w 6 / y.b 6) * (y.w 2 / (1 - y.b 2)) = 2 * Real.sqrt 5 - 4

/-- **admissibility** (#103, Theorem 1): bases strictly ordered, half-widths positive, apexes on the correct side
(t1–t5 point down, so their apexes lie below their bases), corners in the closed disc -/
def Yantra.Admissible (y : Yantra) : Prop :=
  (∀ i : Fin 8, y.b i.castSucc < y.b i.succ) ∧ (∀ i, 0 < y.w i) ∧
  (∀ i : Fin 9, (i : ℕ) < 5 → y.b i < y.a i) ∧ (∀ i : Fin 9, 5 ≤ (i : ℕ) → y.a i < y.b i) ∧
  (∀ i, InDisc (y.w i) (y.b i))

/-- **Kulaichev's Śrī Yantra is unique.** -/
theorem kulaichev_unique : ∃! y : Yantra, y.Huet ∧ y.Kulaichev ∧ y.Admissible := by
  sorry

/-- The unique yantra has slope `w7 / b7 = 0.75043851602221402440…` (#103, Theorem 10). -/
theorem kulaichev_slope (y : Yantra) (h : y.Huet ∧ y.Kulaichev ∧ y.Admissible) :
    (3379673547380287 : ℝ) / 4503599627370496 ≤ y.w 6 / y.b 6 ∧
      y.w 6 / y.b 6 ≤ (3379675694863935 : ℝ) / 4503599627370496 := by
  sorry

/-- **The golden-product Śrī Yantra is unique** (#103, Theorem 15). -/
theorem golden_unique : ∃! y : Yantra, y.Huet ∧ y.KulaichevBCD ∧ y.GoldenProduct ∧ y.Admissible := by
  sorry

/-- The unique yantra has slope `w7 / b7 = 0.67931858870677465738…` (#103, Theorem 9). -/
theorem golden_slope (y : Yantra) (h : y.Huet ∧ y.KulaichevBCD ∧ y.GoldenProduct ∧ y.Admissible) :
    (3059377869223857 : ℝ) / 4503599627370496 ≤ y.w 6 / y.b 6 ∧
      y.w 6 / y.b 6 ≤ (3059380016707505 : ℝ) / 4503599627370496 := by
  sorry

end KulaichevYantra
```

## Statement to score

V2. `kulaichev_unique`, `kulaichev_slope`, `golden_unique` and `golden_slope` (score as one entry: Version 2 as a whole).
