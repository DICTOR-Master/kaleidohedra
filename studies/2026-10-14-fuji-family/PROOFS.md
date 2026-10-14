# The FUJI family: proofs (DICTO, 2026-10-14)

FUJI(r): a pyramid whose base is a flat-ended triangle (an equiangular hexagon with sides 1 and r alternating, 0 ≤ r ≤ 1) and whose
six side edges all have length 1. Its side faces are three equilateral triangles (on the long sides) and three isosceles triangles
1, 1, r (on the short sides). Names and the family are DICTO's; computation and checking with Claude (Anthropic).

## 1. The two base angles

The flat-ended triangle is a big equilateral triangle of side s = 1 + 2r with an equilateral corner of side r cut off at each
corner. All six corners lie on one circle centred at the big triangle's centre O (circumradius² = (1 + r + r²)/3), so the apex sits
directly above O.

**Long sides.** Each long side lies along a side of the big triangle, centred on it, so its distance from O is the big triangle's
inradius, s/(2√3). The equilateral face on it has slant height √3/2, and the foot of that height is the long side's midpoint, which
is also the foot of the perpendicular from O. So the base angle L on the long sides satisfies

  cos L = (s/(2√3)) / (√3/2) = **(1 + 2r)/3**.

**Short sides.** A cut line lies at distance s/√3 − r√3/2 = (2 + r)/(2√3) from O, and the isosceles face on it has slant height
√(1 − r²/4). So the base angle S on the short sides satisfies

  cos² S = **(2 + r) / (3(2 − r))**.

Checks: r = 0 gives cos L = 1/3 (the regular tetrahedron); r = 1 gives cos L = 1 (flat); r = 1/φ gives cos L = (1 + 2/φ)/3 = √5/3,
the angle α = 41.81° of the Lotus seed.

**The r = 1/2 coincidence explained.** cos² S = 5/9 exactly when 9(2 + r) = 15(2 − r), i.e. r = 1/2; and cos² L = 5/9 at r = 1/φ.
So FUJI(1/2)'s short-side angle and FUJI(1/φ)'s long-side angle are both α = arccos(√5/3), exactly. (Found numerically to 40 digits
on 2026-10-14; this is the reason.)

## 2. Which member continues which solid's faces

Face-plane condition (defined): FUJI(r) is glued by one of its equilateral faces to a unit triangle of a solid X, and its base continues the plane of the face of X across that triangle's edge (triangle–triangle edges for the icosahedron, octahedron and antiprisms; triangle–square edges for the cuboctahedron and rhombicuboctahedron). This holds when L + D_X = 180°, i.e. cos L = −cos D_X, i.e.

  **r = (−3 cos D_X − 1)/2.**

- Icosahedron, cos D = −√5/3: r = (√5 − 1)/2 = 1/φ (**FUJI**).
- Cuboctahedron, triangle–square, cos D = −1/√3: r = (√3 − 1)/2.
- Rhombicuboctahedron, triangle–square, cos D = −√(2/3): r = (√6 − 1)/2.
- Octahedron, cos D = −1/3: r = 0 (the tetrahedron).

## 3. Proposition 1: the antiprisms

**For the n-gonal antiprism with unit edges (n ≥ 3), the member whose base continues the plane of its triangles is
r = 2 cos(π/n) − 1.**

By §2 it is enough to show that the dihedral angle D_n between two neighbouring side triangles of the antiprism satisfies

  cos D_n = (1 − 4 cos(π/n))/3.

*Proof.* Write θ = π/n, c = cos θ, s = sin θ. Put the top corners at T_k = (R cos 2kθ, R sin 2kθ, h) and the bottom corners at
B_k = (R cos (2k+1)θ, R sin (2k+1)θ, −h), with R = 1/(2s) so that the polygon edges have length 1. The side edge T₀B₀ has length 1
when 2R²(1 − c) + 4h² = 1; since 2R²(1 − c) = (1 − c)/(2(1 − c)(1 + c)) = 1/(2(1 + c)), this gives h² = (1 + 2c)/(8(1 + c)).

The two triangles on the side edge T₀B₀ are (T₀, B₀, T₁) and (T₀, B₀, B₋₁). Both are equilateral with side 1, so the perpendiculars
from T₁ and from B₋₁ to the edge meet it at its midpoint M = (R(1 + c)/2, Rs/2, 0), each of length √3/2, and

  cos D_n = (T₁ − M)·(B₋₁ − M) / (3/4).

With cos 2θ = 2c² − 1 and sin 2θ = 2sc:

  T₁ − M = ( R(4c + 3)(c − 1)/2, Rs(4c − 1)/2, h ),  B₋₁ − M = ( R(c − 1)/2, −3Rs/2, −h ).

Their dot product, using R² = 1/(4(1 − c)(1 + c)), is

  (4c + 3)(1 − c)/(16(1 + c)) − 3(4c − 1)/16 − (1 + 2c)/(8(1 + c))
  = [ (4c + 3)(1 − c) − 3(4c − 1)(1 + c) − 2(1 + 2c) ] / (16(1 + c))
  = (−16c² − 12c + 4)/(16(1 + c))
  = −(4c − 1)(c + 1)/(4(1 + c)) = −(4c − 1)/4.

So cos D_n = −(4c − 1)/3 = (1 − 4 cos(π/n))/3, and by §2, r = (−3 cos D_n − 1)/2 = (4c − 1 − 1)/2 = **2 cos(π/n) − 1**. ∎

Checks: n = 3, cos D = −1/3 (the octahedron), r = 0; n = 4, cos D = (1 − 2√2)/3 (the square antiprism, 127.55°), r = √2 − 1;
n = 5, cos D = (1 − 2φ)/3 = −√5/3 (the pentagonal antiprism, the icosahedron's middle), r = φ − 1 = 1/φ, **FUJI**; n = 6,
r = √3 − 1; as n → ∞, r → 1, the flat regular hexagon. The numerical check (`scripts/antiprisms.py`, n = 4 to 12) agrees to 10⁻¹⁵.

## 4. Breathing pyrochlore and the golden hexagon after Odom (for reference)

- In a pyrochlore whose two sets of tetrahedra have edges 1 and r, every kagome hexagon is the flat-ended triangle with sides 1 and r
  (its sides are alternately edges of the two sets, and its angles are 120° because the kagome triangles are equilateral): the
  breathing ratio is the family parameter. The tetrahedra and two kinds of truncated tetrahedra fill space for every r
  (`scripts/breathing_data.py`, `breathing-checks.json`).
- Extending each side of a unit equilateral triangle by e at both ends gives six points forming an equiangular hexagon with sides e
  and 1 + e (each corner angle is 120°, as the extensions run along the triangle's sides), i.e. r = e/(1 + e); e = φ gives 1/φ,
  FUJI's base (the golden hexagon after Odom).

DICTO · dictospheres.com
