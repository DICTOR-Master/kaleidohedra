import sys
src = open(sys.argv[1], encoding="utf-8").read()
mode = sys.argv[2]  # v2 or alt
# neutralise the submitter's name in the header
src = src.replace("Finally, ask for admissibility as in DICTO's #103, Theorem 1:", "Finally, ask for admissibility as in #103 (the submitter's paper), Theorem 1:")
src = src.replace("DICTO, #103 (*The DICTO Yantra*), Theorem 1, gives admissibility.", "The submitter's #103 (Zenodo, 2026), Theorem 1, gives admissibility; its Theorems 14 and 15 are the two\ntheorems here.")
assert "DICTO" not in src
bcd = '''/-- **Kulaichev's conditions (b), (c), (d)**, word for word as in `Yantra.Kulaichev`, without (a) -/
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

'''
gthm = '''/-- **The golden-product Śrī Yantra is unique** (#103, Theorem 15). -/
theorem golden_unique : ∃! y : Yantra, y.Huet ∧ y.KulaichevBCD ∧ y.GoldenProduct ∧ y.Admissible := by
  sorry

/-- The unique yantra has slope `w7 / b7 = 0.67931858870677465738…` (#103, Theorem 9). -/
theorem golden_slope (y : Yantra) (h : y.Huet ∧ y.KulaichevBCD ∧ y.GoldenProduct ∧ y.Admissible) :
    (3059377869223857 : ℝ) / 4503599627370496 ≤ y.w 6 / y.b 6 ∧
      y.w 6 / y.b 6 ≤ (3059380016707505 : ℝ) / 4503599627370496 := by
  sorry

'''
second = '''**Second theorem (#103, Theorem 15).** Keep Huet's conditions, Kulaichev's (b), (c), (d) and admissibility, and
replace (a) by the golden slope product: the slope `u = w7/b7` of `t7` times the slope `v = w3/(1 - b3)` of `t3` is
`2/φ³ = 2√5 - 4`. Then again exactly one figure exists, with `w7/b7` in an interval of width `2⁻²¹` around
`0.6793185887…`. Its equations have three other real solutions with `u > 0` in range. One (`u = 0.57120…`) is
admissible, but the circle's centre is then the centre of an excircle of the innermost triangle, beyond `t5`'s base, so
`b5 > 1/2` and (d) as stated excludes it; the other two are not admissible. The product is not Kulaichev's: it is the
product of the slopes of a pair of solids in #103, §9.1. Unlike Kulaichev's yantra (45 odd regions, 28 sandhis), this
one has the traditional 43 triangles and 24 sandhis; #103, Proposition 11 certifies those counts, and they are not
formalised here.

'''
if mode == "v2":
    src = src.replace("# Kulaichev's Śrī Yantra is unique\n", "# Kulaichev's Śrī Yantra is unique, and so is the golden-product Śrī Yantra\n")
    src = src.replace("**Frame.**", second + "**Frame.**")
    src = src.replace("/-- **admissibility** (#103", bcd + "/-- **admissibility** (#103")
    src = src.replace("end KulaichevYantra", gthm + "end KulaichevYantra")
else:
    # Theorem 15 alone: Kulaichev's (a) and kulaichev_* theorems removed
    head, rest = src.split("/-!\n", 1)
    doc, body = rest.split("-/\n", 1)
    newdoc = '''# The golden-product Śrī Yantra is unique

**Informal statement.** Take a circle of diameter 1 and nine isosceles triangles `t1, …, t9` with a common vertical axis,
`t1–t5` pointing down and `t6–t9` pointing up. Suppose they meet Huet's conditions, in the form given by Chiodo:

* the two great triangles `t3` and `t7` are inscribed;
* seven apexes lie on bases;
* the 18 marmas (nine mirror pairs of triple points: a leg, a base and a leg pass through one point) and the 6 corner
  touches (three mirror pairs) hold.

Add three of Kulaichev's four conditions:

* (b) the corners of `t1` lie on the circle;
* (c) the corners of `t9` lie on the circle;
* (d) the centre of the circle is the incentre of the innermost triangle, the one bounded by the legs of `t1` and the base
  of `t5`;

and, in place of Kulaichev's (a) (the two great triangles congruent), the golden slope product: the slope `u = w7/b7` of
`t7` times the slope `v = w3/(1 - b3)` of `t3` is `2/φ³ = 2√5 - 4` (#103, the submitter's paper, §9.1: the product of
the slopes of a pair of solids). Finally, ask for admissibility as in #103, Theorem 1: the bases are strictly ordered,
every half-width is positive, every apex lies on the correct side of its base, and every corner lies in the closed disc.
Then exactly one such figure exists, with `w7/b7` in an interval of width `2⁻²¹` around `0.6793185887…`.

**Scope.** The same equations have three other real solutions with `u > 0` in range. One (`u = 0.57120…`) is
admissible, but the circle's centre is then the centre of an excircle of the innermost triangle, beyond `t5`'s base, so
`b5 > 1/2` and (d) as stated excludes it; the other two are not admissible. This yantra has the traditional 43
triangles and 24 sandhis (#103, Proposition 11, certified); those counts are not formalised here.

**Frame.** The axis is the line `x = 0`, and the depth `d` is measured downwards from the top point of the circle, so the
circle is `x² + d² - d = 0`. Triangle `t(i+1)` has base depth `b i`, base half-width `w i` and apex `(0, a i)`, for
`i : Fin 9`. By the mirror symmetry, each condition is stated on the right half. The labels, the orientation and the scale are
fixed by this frame, so "exactly one" means exactly one 27-tuple `(b, w, a)`.

**Sources.** G. Huet (*Theor. Comput. Sci.* 281, 2002) gave the conditions. A. Chiodo (*C. R. Math.* 359, 2021) gave
the form used here. A. P. Kulaichev (*IJHS* 19.3, 1984, pp. 284–285) added (a)–(d). The submitter's #103 (Zenodo,
2026), Theorem 1, gives admissibility, §9.1 the golden product, Theorem 15 this theorem.
'''
    body = body.replace("namespace KulaichevYantra", "namespace GoldenYantra")
    body = body.replace("end KulaichevYantra", "end GoldenYantra")
    # drop Kulaichev's full conditions and his theorems
    start = body.index("/-- **Kulaichev's conditions** (a)–(d) -/")
    stop = body.index("/-- **admissibility** (#103")
    body = body[:start] + bcd.replace("word for word as in `Yantra.Kulaichev`, without (a)", "(Kulaichev 1984)") + body[stop:]
    start = body.index("/-- **Kulaichev's Śrī Yantra is unique.** -/")
    stop = body.index("end GoldenYantra")
    body = body[:start] + gthm + body[stop:]
    src = head + "/-!\n" + newdoc + "-/\n" + body
assert "DICTO" not in src and "Cleo" not in src
sys.stdout.write(src)
