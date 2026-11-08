# Exact Śrī Yantras (study, 8 Nov 2026)

Outside the main plan. DICTO called the exact Śrī Yantra "a great one". DICTO proposed the
upright rhombus (8 Nov: "seems to be a big upright rhombus in the construction") and sent the
reference image (below).

**Conclusion.** Every rational choice of four natural parameters gives a Śrī Yantra in which all
18 marmas, the 6 corner touches, the 7 apex-on-base points and both inscribed triangles hold
exactly, with every coordinate in one quadratic field ℚ(√Δ) (Theorem Q). There is also a fully
**rational** Śrī Yantra, R1, where every vertex and every marma has rational coordinates. On
DICTO's rhombus the 3-4-5 shape (diagonals 3 : 4, rational inscribed triangles 9/25, 16/25,
12/25) together with the classical "t1 and t9 corners on the circle" gives an exact yantra, Rh345,
in a field of degree 20. Rh345 misses Kulaichev's fourth condition by only 2.4·10⁻⁵ of the
diameter.
**Status:** study done. Nothing has been published. R1 and Rh345 are placeholder names, and DICTO names them.

## 1. Prior art: what is known (sources checked)

Sources checked, by name:
- G. Huet, *Śrī Yantra Geometry*, Theoretical Computer Science 281 (2002) 609–628. The full text was not reachable. His model and numbers are taken as quoted by Chiodo 2021 and Kavi Mahesh 2023.
- A. Chiodo, *On the construction of the Śrī Yantra*, C. R. Math. 359 (2021) 377–397, doi 10.5802/crmath.163 (full text read).
- V.-V. Pustynski, *On mathematical complexity of Śrīyantra*, IJHS 49.3 (2014) 268–277 (full text read). The link DICTO gave (cahc.jainuniversity.ac.in) returns 404, and the copy read is insa.nic.in/writereaddata/UpLoadedFiles/IJHS/Vol49_3_5_Pustynski.pdf.
- A. P. Kulaichev, *Śrīyantra and its Mathematical Properties*, IJHS 19.3 (1984) 279–292. The INSA PDF is a scan with no text layer, so it is used as summarised by Pustynski and Chiodo.
- Kavi Mahesh, *Understanding the geometry of Sri Chakra*, Int. J. Sanskrit Research 9(6) (2023) 242–248, anantaajournal.com/archives/2023/vol9issue6/PartD/9-6-39-715.pdf (full text read).
- L. N. Gonçalves, M. Mádr, P. Stříž, *Drawing the Shree Yantra Core with Metapost*, Zpravodaj CSTUG 19 (2009) 212–221, DML-CZ 10338.dmlcz/150096 (abstract page only).
- B. Tripathi, texample.net/sri-yantra (TikZ, 30 Nov 2025).
- Web searches: "Pustynski Sri Yantra …", "Huet Sri Yantra Geometry … parameters", and "arXiv Sri Yantra exact construction concurrency algebraic". No arXiv paper was found. Chiodo's bibliography adds Bolton–Macleod 1977, Fonseca 1986, C. S. Rao 1998, Tahta 1992, Santhi et al. 2012 and Tularam 2012. These were not read.
- The reference library on dicto-big-brother (~/kaleidohedra-references, every MANIFEST.json and text file) was grepped for "yantra" and "Huet". It has no hits.

What is known:
- **Huet (1980s, publ. 2002):** the yantra is an under-determined problem with **4 real parameters**: five starting values tied by one equation, solved by Newton iteration. His "classical" yantra has P, Q, R, S = 0.332, 0.537, 0.602, 0.835 in Chiodo's form.
- **Chiodo 2021:** the whole 4-parameter family is **constructible by straightedge and compass**. The closing step is Apollonius' circle–line–point problem. So for constructible P, Q, R, S every coordinate is a constructible number. Chiodo gives no explicit field, minimal polynomial or exact example.
- **Kulaichev 1984, Rao 1998, Pustynski 2014:** four extra conditions give a **unique** rigid yantra, known numerically to 15 figures (Pustynski Table 1). The conditions are (a) t3 ≅ t7, (b) t1's base corners on the circle, (c) t9's base corners on the circle, and (d) the incircle of the innermost triangle is concentric with the circle. Kulaichev bounded the degree by 12544. Pustynski: "purely analytical solution of the final two steps is probably impossible".
- **Kavi Mahesh 2023:** simple rational heights. 16 of the 18 marmas are exact by construction, and M11/M12 miss by 0.02 % of d.
- **Tripathi 2025 (texample):** numerical, and the author says residual errors remain.

So **constructibility is already published (Chiodo)**. In the sources above we found no explicit exact
yantra with its field and polynomials and a machine re-proof of every concurrency. We also found no rational
yantra and no treatment of the rhombus. These results look new as far as these sources go. They are
not claimed to be new beyond them.

## 2. Model (scripts/model.py)

The circle has diameter 1, and *d* is depth below the top point O. The nine triangles t1…t9 follow
Chiodo's numbering: bases top to bottom, t1–t5 apex down and t6–t9 apex up. Triangle ti has base
depth bᵢ, half-width wᵢ and apex aᵢ. The conditions are Chiodo's (i)–(iii), which are equivalent to Huet's:
- t3 and t7 are inscribed: a3 = 1 and a7 = 0, with their corners on the circle.
- Apex on base point: a8=b1, a6=b2, a9=b3, a1=b6, a5=b7, a4=b8, a2=b9.
- **18 marmas** (9 pairs) as (down-leg, base, up-leg) triples: (1,2,7) (2,3,7) (1,3,8) (1,4,6) (1,5,9) (4,6,9) (2,7,9) (3,7,8) (3,8,9). Their incidence per triangle (8,6,8,4,2,4,8,6,8) matches Kavi Mahesh's table.
- **6 corner touches**: (4,4,8), (5,5,6) and (2,6,6).

The free parameters are Chiodo's P = b3, Q = b6, R = b7, S = b9. Following Chiodo's Fig. 4, everything follows by
intersecting lines except one quadratic in b1. In this study P and R are replaced by the **leg slopes**
u (t7, from O) and v (t3, from T), with P = v²/(1+v²), R = 1/(1+u²), w3 = v/(1+v²) and w7 = u/(1+u²).
This is the rational parametrisation of the circle, so the big inscribed triangles are rational
whenever u and v are. The model reproduces Pustynski's Table 1 to 3.9·10⁻¹⁵, which is all 14 of his
significant figures (data/kulaichev-numeric-data.txt).

The 43 triangles are exactly the faces of the line arrangement that lie inside an **odd** number of
the nine triangles: 14 + 10 + 10 + 8 + 1 at containment depth 1, 3, 5, 7, 9. scripts/figure.py
checks this for every figure.

## 3. Results

**Theorem Q (quadratic yantras).** If u, v, Q, S are rational, every coordinate lies in ℚ(√Δ).
Δ(u,v,Q,S) is the discriminant of the closing quadratic. Its square-free part has degrees
(10, 20, 6, 6) in (u, v, Q, S), and the factor list is in data/discriminant-log-data.txt.
scripts/quadratic_family.py re-proves all 23 condition expressions **exactly** with pure Fraction
arithmetic in ℚ(√Δ), with no floats. The expressions cover the 18 marmas, the 6 corner touches, the 7
apex-on-base points and the circle conditions. Examples, with max |Δb| from Huet's classical depths:

| name | u, v, Q, S | field | max Δb vs Huet | 43 faces |
|---|---|---|---|---|
| **R1** | 19/24, 2/3, 8/15, 8/9 | **ℚ** (Δ a square) | 0.054 | 14,10,10,8,1 ✓ |
| Q1 | 13/16, 12/17, 29/54, 5/6 | ℚ(√Δ) | 0.0031 | ✓ |
| Q2 | 4/5, 7/10, 8/15, 5/6 | ℚ(√Δ) | 0.020 | ✓ |
| Q3 | 3/4, 3/4, 11/20, 11/12 (3-4-5 rhombus) | ℚ(√Δ) | 0.082 | 14,10,**12**,8,1 |

**R1, the rational Śrī Yantra** (depth from top, diameter 1). Every b, w and apex is rational:
b = 248/3611, 48/233, 4/13, 23/61, 86/197, 8/15, 576/937, 172/229, 8/9.
w = 836/3611, 3401/11883, 6/13, 1805/12444, 703/6698, 38/255, 456/937, 16245/50609, 323/1485.
Its inscribed triangles sit on Pythagorean triples 5-12-13 (t3) and 215-912-937 (t7). The marmas are listed in
data/quadratic-examples.json. R1 was the only rational yantra found in two searches: 9.7 million parameter sets
(denominators ≤ 40), then 627 million S-values over 14 336 (u, v, Q) slices (S denominators ≤ 1200,
rational_search2.py, with a self-test that re-finds R1). The fibres are genus-2 curves, so rational yantras are expected
to be rare. R1 is admissible but sits higher than the traditional drawing: t1's base is at 3.3/48 against 6/48 on the grid.

**Kaivalyāśrama's grid.** Taking P, Q, R, S = 17, 27, 30, 42 / 48, the positions Chiodo suggests for traditional
diagrams, puts t1's base corners **outside** the circle (power +0.031). The grid itself is not admissible.

**DICTO's rhombus (scripts/rhombus.py).** It is formed by the two legs of t7 (from O) and the two legs of t3
(from T), the four longest lines. They meet at E± = (±uv/(u+v), v/(u+v)). The figure O-E-T-E is a kite in
general and a rhombus **exactly when u = v**, which is Kulaichev's condition (a), t3 ≅ t7. Then the diagonals are 1 : u and the angle at O and T is 2·atan u.

| yantra | angle O | angle T | angle E | diagonal ratio | shape |
|---|---|---|---|---|---|
| Huet classical | 78.23° | 70.37° | 105.70° | 0.7552 | kite |
| Kaivalyāśrama grid | 75.52° | 73.04° | 105.72° | 0.7572 | kite |
| Kavi Mahesh | 78.46° | 70.53° | 105.50° | 0.7579 | kite |
| Kulaichev–Rao–Pustynski | 73.77° | 73.77° | 106.23° | 0.75044 | rhombus |
| R1 / Q1 / Q2 | 76.73 / 78.19 / 77.32° | 67.38 / 70.44 / 69.98° | — | 0.724 / 0.755 / 0.747 | kite |

The rhombus is used as an extra condition, completed by (b) and (c), the t1 and t9 corners on the circle:
- **3-4-5 rhombus (u = v = 3/4):** admissible and next to Kulaichev's yantra (u = 0.750439). **Exact** (rhombus345_exact.py):
  S = b9 = (21464 + 56√56869)/37825 (with 56869 = 29·37·53), and Q = b6 and b1 have irreducible minimal
  polynomials of degree 20 (data/rhombus345-exact-data.txt). The field of definition has degree 20. All 23 conditions are checked
  **exactly** in that number field. Kulaichev's (d), measured and not imposed, misses by 2.36·10⁻⁵.
- **Golden rhombus (diagonals 1 : φ)** and **60°/120° rhombus:** both are admissible but far from the classical figure. t1's base
  sits at 0.65/48 and 0.30/48, and the incircle is off by 0.017 and 0.024.
- **Square:** P = R = 1/2, the bases of t3 and t7 coincide, and there is no yantra.

So the natural special rhombus is the **3-4-5 rhombus**, not the golden one.

**Two extra tiny faces.** Kulaichev's yantra, Rh345 and Q3, all with u = v, have **45** odd faces and not 43.
The third ring holds 12 faces, two of them non-triangles. This independently confirms Pustynski's remark
(2014, §2.5) about "two additional tiny triangles". The non-rhombus examples R1, Q1 and Q2 have exactly 43.

**Kulaichev's yantra exactly:** not reached. scripts/kulaichev_exact.py (resultants with u free) did not finish
within its 20-minute limit. It reached Res_t(core, Eb) and Res_t(core, Ed), of degrees (56, 10, 12) and (54, 11, 12)
in (u, Q, S), and stopped in the Res_Q step. Its 60-digit numeric values are in data/kulaichev-numeric-data.txt, with
u = 0.750438516022214024406084657051234510340891003639790315415314.

**DICTO's reference image** (gold embossed yantra, Screenshot 2026-11-08 14-40-18, 338 px, tilted). The layout
matches the model: t7's apex at the top of the circle, t3's apex at the bottom, 9 horizontal lines and 4 + 5
triangles. A rough reading (±0.05, perspective) gives P ≈ 0.39, R ≈ 0.63 and u ≈ v ≈ 0.8. That is a near-rhombus
with diagonal ratio ≈ 0.8 and top angle ≈ 77°, in the classical range. It is not precise enough to separate the kite from the rhombus.

## 4. Figures
- figures/sri-yantra-rational-R1.svg / .png is the main figure. It shows R1 exactly, the 43 triangles shaded by ring, the 18 marmas, the 6 corner touches and DICTO's rhombus dashed.
- figures/sri-yantra-345-rhombus.svg / .png shows Rh345, with the two extra tiny faces visible near the centre.

## 5. Scripts and data (each script ends with a checked FINAL line; heavy runs on dicto-big-brother)
model.py (shared model) · quadfield.py (exact ℚ(√D)) · quadratic_family.py → data/quadratic-examples.json, quadratic-family-data.txt ·
discriminant.py → discriminant-data.txt · rational_search.py → rational-search-data-den40.txt · rational_search2.py → rational-search2-data.txt ·
kulaichev_numeric.py → kulaichev-numeric-data.txt · kulaichev_exact.py (did not finish) · rhombus.py → rhombus-data.txt, rhombus345-coordinates.json ·
rhombus345_exact.py → rhombus345-exact-data.txt · figure.py → figure-*-data.txt and figures/.

## 6. LEADS
- A rational yantra closer to the traditional drawing needs bigger searches, or rational points on the genus-2 fibres by Chabauty-type methods.
- A rational yantra on the rhombus (u = v rational) needs Δ to be a square on a 3-parameter slice.
- Kulaichev's exact degree needs a longer elimination run, or Rh345-style towers with u as a parameter.
- Kavi Mahesh's rational heights could be made exact: fix his P, R, S and Q, solve b1, and get the field ℚ(√2, √3, √Δ).
- Outside this study: the **spherical Śrī Yantra** (Gupta's kūrma form, C. S. Rao 1998), which is DICTO's queued "mandala spheres" idea. Lines become great-circle arcs, and the same exactness question applies.

## 7. The great pair from solids (DICTO, 8 Nov 2026, later)
DICTO proposed the tetrahedral yantra in a sphere (the triangles become tetrahedra, the rhombus becomes the stella octangula),
then spinning tetrahedra (each sweeps a cone; the flat yantra is the axial section of nine nested cones, its 9 mirror pairs of
marmas become 9 circles where two cones and one level disc meet), then the Cleo-Icos as the great pair.
- Stella yantra (scripts/stella_yantra.py): u = v = 1/sqrt2 (regular stella octangula spun), t1 and t9 corners on the circle:
  valid; P = 1/3 exactly, Q = 0.5643071201..., S = 0.9561723639...; misses Kulaichev's (d) by -3.4e-4 (squared form).
- Cleo yantra (scripts/cleo_yantra.py): u = v = 2/phi^2 = 3 - sqrt5 (the Cleo-Icos, icosahedron face pyramid, spun), t1 and t9
  corners on the circle: valid; Q = 0.5467623283..., S = 0.9051499328...; misses Kulaichev's (d) by +9.0e-5.
- Kulaichev's own yantra lies between them: u = 0.7504385160..., Q = 0.5507052329..., S = 0.9200601459... The Cleo yantra is the
  nearest of the three to it (differences 0.014, 0.004, 0.015). Exact forms: stella_algdep.py running; Kulaichev algdep running.
- DICTO named K1 the **DICTO Yantra** and its great pair (Cleo-Icos above, stella tetrahedron below) the **Cleo-Octangula** (8 Nov 2026).
- Kites (scripts/kites.py, DICTO 11-08: "distort the overall Cleo to the kite form proportion"): great pair with different slopes,
  t1 and t9 corners on the circle. K1 Cleo-Icos above / stella below (u = 2/phi^2, v = 1/sqrt2): valid, EXACTLY the traditional 43
  (14, 10, 10, 8, 1); P = 1/3, Q = 0.53625 (Huet classical 0.537), R = 0.63148, S = 0.93007; field contains sqrt2 and sqrt5 (as the
  Golden Cut Cubes). K2 stella above / Cleo below: valid, 43. K3, K4 with the golden slope phi/2 above: valid but 45 pieces, so the
  count depends on the slopes, not on kite vs rhombus alone. Huet's classical slopes from his depths: u = 0.813 (near phi/2 = 0.809),
  v = 0.705 (near 1/sqrt2): a hint only (his figures have three digits).
- Gnomon yantra (scripts/gnomon_yantra.py, render_gnomon.py; DICTO 11-08, "a gnomon like Julias", option A): if the bindu
  triangle's incircle is centred (Kulaichev's (d)), a copy of the whole yantra scaled to that incircle fits exactly, so the yantra
  minus that disc is a gnomon and the yantras nest without end. On the Cleo-Octangula with (b) and (d): G1, valid, 43 triangles,
  18 marmas, 24 sandhis; nesting ratio k = 0.0630741873 (1/k = 15.8543); t9 corners miss the circle by 0.066 (inside). With (c)
  and (d): no valid yantra. Figure: figures/gnomon-yantra.png. G1 is a placeholder name.
- Perfect yantras (scripts/perfect_yantra.py, DICTO 11-08 "can we split them to get perfection"): with both slopes fixed only two
  of (b), (c), (d) can hold, so one solid is kept exact and the other slope freed. PF1 (Cleo-Icos above exact): lower slope
  0.762114, all of (b)(c)(d) exact, k = 0.0561783, but 45 pieces / 28 sandhis (near-rhombus). PF2 (stella below exact): upper
  slope 0.695886, all of (b)(c)(d) exact, k = 0.0563429, and the traditional 43 triangles, 18 marmas, 24 sandhis: perfect in every
  condition, but its upper great triangle is no longer the Cleo-Icos (steeper: the kite turned the other way from Huet's).
- Viewpoint (scripts/viewpoint.py; DICTO 11-08: "perspective tilt or position ... viewpoint?!"): the projective maps that keep the
  circle a circle and keep the axis are the Klein-model translations along the axis (in older words, a tilted circle seen from the
  right point still looks round). They keep every line, every concurrency, every level base, every corner on the circle, and the
  counts (43, 18, 24); they change the slopes u -> u/lambda, v -> v*lambda (u v invariant) and move the bindu's centre. The DICTO
  Yantra (Cleo-Octangula) seen at beta = -0.0405464286 (lambda = 0.9602432222) has the bindu centred and both small triangles on the
  circle: every condition at once, 43 triangles, 18 marmas, 24 sandhis. Its slopes are 0.7335605 above and 0.7363830 below (product
  0.5401815 = (2/phi^2)(1/sqrt2) kept): the Cleo-Octangula in perspective. Figure: figures/viewpoint-V1.png.
