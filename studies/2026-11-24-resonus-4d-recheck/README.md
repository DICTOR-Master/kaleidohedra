# Independent recheck of "The Resonus in 4D" (24 Nov 2026)

DICTO · checker's study for the V SF A project. Checks the statements of study 2026-11-24-resonus-4d (README only; its
scripts were not read). Own code, own constructions, exact arithmetic in Q(√5) (`scripts/recheck.py`, `scripts/regular_all_dims.py`;
logs in `logs/`, 3443 + 983 exact checks, both FINAL ok; run on the compute host, 67 s and under a minute).

> **Status box.** Checker's note, not published. Every item below: **agrees**, with one wording point (item 2.3) and two
> prior-art points (items 3.2, 3.3).

## 1. Recomputation with different constructions — all agree

Constructions used (different from the study's):
- **600-cell**: the 120 unit icosians generated as a *group* by quaternion multiplication from ½(1,1,1,1) and
  ½(φ, 1, 1/φ, 0) (closure has exactly 120 elements, all of norm 1); its 600 cells found as the supporting 4-cliques of the
  nearest-neighbour graph (inner product φ/2, 12 neighbours each).
- **120-cell**: the polar {x : v·x ≤ 1 for the 120 icosians v}. Its facets *are* these 120 inequalities (each checked to cut a
  3-dimensional face); its 600 corners are the facet points of the 600-cell, computed, never listed.
- **25 inscribed 24-cells**: the sets g·T·h (g, h icosians, T the 24 Hurwitz units), by quaternion products, not as an orbit under
  reflections; exactly 25 distinct sets, each with all inner products in {0, ±½, ±1}.
- **Vacuus plates**: normal = exact null vector of the ridge's corners (the study used a_F − a_F′ as well; here only the null vector).
- **Mirrors**: exact reflection test of every candidate root b − w, b in a spanning set of corners (found directly for the 120-cell too,
  as well as checking each of the 600-cell's mirrors on its 600 corners).
- **Permutohedron**: from its inequalities Σ_{i∈S} x_i ≥ |S|(|S|+1)/2, each checked as a facet on the 120 permutations.
- Facets of every polytope checked exactly supporting with a tight set of dimension d − 1; every ridge in exactly two facets;
  f-vector and Euler's relation checked.

| item | study says | recheck | verdict |
|---|---|---|---|
| Resonus(120-cell) = the 60 H4 mirrors | 60 = 60, Resonus = Vacuus | 60 Resonus hyperplanes (2 cells each) = the 60 mirrors found directly | **agrees** |
| Resonus(600-cell) | 300, none a mirror | 300 (2 cells each), 0 on mirrors; normals = the 120-cell's corner lines | **agrees** |
| 300 = middle walls of the 25 inscribed 24-cells | 25 × 12, distinct, = Resonus(P) | 25 × 12 = 300 distinct, equal as sets to Resonus(600-cell); 12 corners of P on each | **agrees** |
| Vacuus(600-cell) | 60 = the mirrors, 20 triangles each | 60 plates = the mirrors, 20 each | **agrees** |
| Vacuus(120-cell) | 60 = the mirrors, 12 pentagons each | 60 plates = the mirrors, 12 each | **agrees** |
| 5-cell | 10 · 5(1) · 10(1) · 0 · 0 · 10 | same | **agrees** |
| tesseract | 16 · 4(2) · 12(2) · 0 · 4 · 12 | same | **agrees** |
| 16-cell | 16 · 8(2) · 4(8) · 0 · 0 · 4 | same | **agrees** |
| 24-cell | 24 · 12(2) · 12(8) · 12 · 12 · 12 | same; Resonus = Vacuus as sets | **agrees** |
| 4D permutohedron | 10 · 15(2) · 65(2 or 6) · 15 · 0 · 0 | same; Resonus ⊂ Vacuus | **agrees** |
| f-vectors | as listed | (5,10,10,5), (16,32,24,8), (8,24,32,16), (24,96,96,24), (120,720,1200,600), (600,1200,720,120), (120,240,150,30) | **agrees** |

(Columns: mirrors · Resonus (facets each) · Vacuus (ridges each) · Resonus ∩ Vacuus · Resonus on mirrors · Vacuus on mirrors.)

**#110 compared directly.** #110 v3 (paper.html, §2 and abstract) defines a cross wall as "a central section parallel to a pair
of opposite cells" of the 600-cell "that are not already mirrors", 300 of them, normals along the 120-cell's corners; and §2 (2)
already states that the 25 × 12 = 300 middle sections of the inscribed 24-cells are distinct and are exactly the cross walls, and
that "for the dual 120-cell the cell-parallel sections are the 60 mirrors". Since no cell-parallel section of the 600-cell is a
mirror (recomputed), #110's clause "not already mirrors" removes nothing: **cross walls = Resonus(600-cell), agrees.**

## 2. The two laws and the "only the 120-cell" claim

2.1 **Theorem 1 (Resonus law)** and **Theorem 2 (Vacuus law)**: proofs read line by line; both correct as stated (Theorem 2's
contradiction uses that the plate's normal a_F − a_F′ is non-zero and would lie in the plate). **Agrees.**
Corollary 1 (needs −1 ∈ G and the facet stabiliser inducing the facet's full symmetry group): proof correct. Corollary 2 (flag
reflection ρ_{d−1} swaps the two facets at the base ridge; ridge-transitivity): correct. **Agrees.**

2.2 **Every regular polytope, every dimension** (exact, `regular_all_dims.py`; general n by Corollary 1):

| family | mirrors | Resonus | Resonus on mirrors | Resonus = all mirrors? |
|---|---|---|---|---|
| segment (1D) | 1 | 1 | 1 | **yes** |
| m-gon, m odd | m | m | 0 | no (same count, disjoint) |
| m-gon, m even | m | m/2 | m/2 | no |
| n-simplex, n ≥ 2 | n(n+1)/2 | n+1 | 0 | no (no opposite facets) |
| n-cube, n ≥ 2 | n² | n | n | no |
| n-cross-polytope, n ≥ 3 | n² | 2^{n−1} | 0 | no (simplex facets) |
| dodecahedron, icosahedron | 15, 15 | 6, 10 | 0, 0 | no |
| cube, tetrahedron, octahedron | 9, 6, 9 | 3, 4, 4 | 3, 0, 0 | no |
| 24-cell, 600-cell | 24, 60 | 12, 300 | 12, 0 | no |
| 120-cell | 60 | 60 | 60 | **yes** |

Computed exactly for m = 3…40 (angles as rational multiples of π), the five Platonic solids, and simplex, cube and cross-polytope
for n = 2…7; the closed forms hold for all n by Corollary 1 (cubes: centrally symmetric facets, n of n²; cross-polytopes n ≥ 3 and
simplices: simplex facets, none; the 2-cross-polytope is the square).

2.3 **Verdict on the claim.** The study's own wording, "among the regular polytopes **of dimension ≥ 2** this happens only for
the 120-cell", is **exactly true (agrees)**. Stated as "in any dimension" it is false only through the trivial 1D case: the segment
[−1, 1] has one mirror (the point 0), which is its Resonus. True statement: *the 120-cell is the only convex regular polytope of
dimension ≥ 2 whose Resonus is its whole mirror arrangement; in dimension 1 the segment does so trivially.* Side note: odd polygons
have exactly as many Resonus lines as mirrors (m) but none in common.

## 3. Prior art

3.1 **Theorems 1 and 2** (central hyperplane parallel to a facet, or through a ridge, is a mirror exactly when a reflection maps
the facet to its opposite, or swaps the ridge's two facets): **not found** in the sources checked. They are short consequences of
polarity (a symmetry permutes the polar's corners); the closest statements found are Lemma 2 of arXiv math/0502108 (no mirror
cutting a reflection simplex is parallel to a facet) and the opposite-facet arguments for zonotopes in arXiv 1401.4749; neither is
the same statement. Classical inputs (flag reflections, Coxeter) are credited in the study.

3.2 **Resonus(120-cell) = H4 mirrors** is not new in content: the 120-cell's cell centres are the 600-cell's corners, which are the
H4 roots (Coxeter, *Regular Polytopes*; Humphreys), and #110 v3 §2 already states "for the dual 120-cell the cell-parallel sections are
the 60 mirrors". The study confirms it; it is not a new result.

3.3 **The 300 non-mirror walls as middle walls of the 25 inscribed 24-cells**: already stated in DICTO's own #110 (v2 and v3, §2 (2),
with data crosswalls_24cells.csv). In dual form it is also in **Denney, Hooker, Johnson, Robinson, Butler, Claiborne, "The Geometry
of H4 Polytopes", Adv. Geom. 20 (2020) 433–444, arXiv 1912.06156, §2**: the 600 corners of the 120-cell (the normals of the 300 walls)
split into 25 disjoint 24-cells g C h with C = 2A4·(2,2,0,0)·2A4 (2A4 = the Hurwitz units T). Since x ↦ g x h is orthogonal,
the 12 lines of g C h are exactly the cell normals of the inscribed 24-cell g T h, so
Denney et al. give the partition of the 300 normals into 25 sets of 12; they do not phrase it as hyperplanes or walls. The study
and #110 should cite them at this point, not only for the count 25.

3.4 Not found: the term or the use of "Resonus"; any statement that the 600-cell's 300 cell-parallel central hyperplanes are none of
them mirrors (immediate from Corollary 1). Marken and Wetzel's Grünbaum 4-arrangements of the 120-cell and 600-cell (facet
hyperplanes with some mirrors, not central) are a different arrangement: abstract only, full text not free.

**Sources checked:** #110 v3 paper.html (abstract, §2); Denney et al. 2020 (arXiv 1912.06156, full text); Wikipedia 600-cell,
120-cell, 24-cell, H4 polytope; Wikiversity 600-cell and 24-cell; arXiv math/0502108; arXiv 1401.4749; arXiv 1609.00591 (mirror
graphs); Marken–Wetzel, J. Geom. 45 (1992) 114–120 (record only); Waegell–Aravind KS sets (cited by #110; only the search listing seen here); web searches on the "resonance arrangement" (Kamiya–Takemura–Terao; Billera et al.: an
all-subset arrangement, no statement about facets of regular polytopes found). Coxeter, *Regular Polytopes*: no free full text
reached; the facts used from it are standard (cell centres of {5,3,3} = corners of {3,3,5}; flag reflections).

## LEADS

1. Add Denney et al. 2020 §2 as the dual source of the 25 × 12 partition in the study and in #110's next version.
2. In the study's conclusion, write "dimension ≥ 2" wherever the "only the 120-cell" claim appears (the segment is the 1D case).
3. Odd polygons: Resonus and mirrors have equal counts and are disjoint; the 600-cell is the 4D case with all of its Resonus off
   the mirrors. A remark, not a result.
