# Prior-art search, study 6 (star cores, exact): A1, A2, B, C

Date: 2026-10-31. Searcher: Claude (subagent), for DICTO.
Method: local reference library first (`~/bin/ask-library "QUERY" 8`, which runs on dicto-big-brother over the 302-reference library; note: the script lives on this machine at `~/bin/ask-library` and ssh-es to dicto-big-brother itself, so `ssh dicto-big-brother '~/bin/ask-library …'` fails because `~/bin` does not exist there), then web searches and page reads.
Marking: **read** = text of the source read by me; **abstract/snippet only** = only an abstract, search snippet or secondary description seen.

Setting recalled: T(S) = {x : v·x ≤ v·v for every corner v}. Each face plane of T(S) passes through a corner v perpendicular to Ov. T(S) is the Voronoi cell of O among the points 2v.

---

## A1. Polar-spike fill (pyramid over each corner, tetrahedron over each edge; flattening at the midsphere = Conway join)

**Verdict: partly known.** The midsphere case is known: the convex hull of an edge-tangent polyhedron and its polar has quadrilateral facets, one per edge, where the two edges cross (Eppstein 2001 slides; Conway join jX = daX; Wikipedia "Polytope compound": the hull of a dual compound is the dual of the rectification). Coxeter 1997 studies the hull Π+ and the core Π− of a regular polytope and its reciprocal in a concentric sphere of any suitable radius. I found no source that states the general-radius result: for ρ > R, the layer between the star and conv(S ∪ ρ-polar) is tiled exactly by one pyramid per corner and one tetrahedron per edge. Nothing found in the sources listed.

Sources found:
1. D. Eppstein (joint work with G. Ziegler and G. Kuperberg), *Triangles and Squares*, talk slides, COMB01, Barcelona, 2001. https://ics.uci.edu/~eppstein/pubs/Epp-COMB-01.pdf. **Read** (downloaded with curl; WebFetch failed with a certificate error). Slide "Convex Hull of (P union polar), P edge-tangent": "Edges cross at tangencies; hull facets are quadrilaterals". Next slide (4D): the polar has 2-faces tangent to the sphere, and the hull facets are dipyramids over those 2-faces. Only the midsphere case; no general radius; no decomposition of the layer.
2. H. S. M. Coxeter, "Reciprocating the regular polytopes", J. London Math. Soc. 55 (1997) 549–557, doi:10.1112/S0024610797004833. https://www.cambridge.org/core/journals/journal-of-the-london-mathematical-society/article/reciprocating-the-regular-polytopes/2D387F9B5EEE1B90439C27746AFCC1DC. **Abstract only.** Π and its reciprocal Π′ in a suitable concentric sphere "usually have together the same vertices as a third polytope"; "Π+ is the convex hull of Π and Π′, while Π− is their common content or 'core'." Regular polytopes only.
3. G. W. Hart, *Conway Notation for Polyhedra*. https://www.georgehart.com/virtual-polyhedra/conway_notation.html. **Read.** "The join operator is dual to ambo, so jX=dadX=daX"; one 4-sided face per edge of X; for mutually dual polyhedra with edges tangent to a common sphere, "the ambo of either is their intersection".
4. Wikipedia, "Polytope compound" (accessed 2026-10-31). https://en.wikipedia.org/wiki/Polytope_compound. **Read.** Dual compound: "The core is the rectification of both solids"; "The hull is the dual of this rectification", its rhombic faces have the crossing edges as diagonals. No inline source for this rule.
5. Wikipedia, "Dual polyhedron" (accessed 2026-10-31). https://en.wikipedia.org/wiki/Dual_polyhedron. **Read.** Polar reciprocation definition; "the resulting form of the dual will depend on the size and position of the sphere"; canonical dual about the midsphere shares the edge-tangency points. Cites Cundy & Rollett 1961 pp. 78–79, Wenninger *Dual Models* 1983, Barvinok 2002 p. 143, Grünbaum 2007 Thm 3.1.
6. Wikipedia, "Compound of cube and octahedron". https://en.wikipedia.org/wiki/Compound_of_cube_and_octahedron. **Read.** Intersection = cuboctahedron; hull = rhombic dodecahedron; first stellation of the cuboctahedron (Wenninger 43).
7. MathWorld, "Dual Polyhedron". https://mathworld.wolfram.com/DualPolyhedron.html. **Read.** Polar relation R r = ρ² (circumradius of one solid times inradius of its midsphere dual); cites Cundy & Rollett 3rd ed. Table II after p. 144.
8. Antiprism, `pol_recip` documentation. https://antiprism.com/programs/pol_recip.html. **Read.** Centre and radius options; the radius sets where the dual vertices sit; the default "tends to reciprocate in the midsphere, if it exists".
9. Antiprism, `conway` documentation (library item 170, link only). https://antiprism.com/programs/conway.html. Read in an earlier study (10-15); not re-read now.
10. Library: M. Firsching, "Computing maximal copies of polytopes contained in a polytope", Experimental Math. 24 (2015) 98–105, arXiv:1407.0683 (`papers/Firsching-2015-Maximal-copies-of-polytopes.pdf`). **Read** (the passage). "If P ⊂ Q are concentric … we can take polar reciprocals and get Q° ⊂ P°". Inclusion reversal only; background.
11. Library: P. W. Messer, "Stellations of the rhombic triacontahedron and beyond", Structural Topology 21 (1995) (`papers/Messer-1995-Stellations-rhombic-triacontahedron.pdf`), p. 2. **Read.** Defines the stellation core and the process. Background for B.

---

## A2. Iterating T (reciprocation with rescaling / iterated Voronoi cell) and return to a similar shape

**Verdict: partly known (in the plane and for simplices); nothing found for general polyhedra.** In the plane, T is exactly the classical *antipedal* (negative pedal) polygon with pedal point O. In each case the line through the vertex P_i is perpendicular to OP_i. Stewart (1940) proved that the n-th Miquel iterate (the pedal map is the case θ = π/2) of an n-gon is similar to it, with M as the self-homologous point. Because the pedal map is invertible, the n-th antipedal iterate is similar too (McDonald–Garcia–Reznik 2022, Corollaries 2–3). McDonald et al. also note that their "circumcenter map" (the circumcentres of M P_i P_{i+1}, i.e. the Voronoi vertices of M among the P_i) is the half-size M-antipedal polygon. That is DICTO's "Voronoi cell of O among the 2v", scaled by 1/2. For tetrahedra, Kostanyan (2026) states that the fourth pedal tetrahedron is similar to the original (abstract only). These results need the combinatorial type to stay fixed (n vertices ↔ n sides). For polyhedra whose corner count differs from their face count, as in DICTO's chains, I found no result. Hart's canonicalization iterates reciprocation of face planes, but as a numerical relaxation to one fixed point (the canonical form with unit midsphere). It does not study similarity orbits or gains. Hatch (2003) shows that reciprocating about varying centroids does not in general return the same shape, and that the radius of reciprocation does not affect his canonical centre.

Sources found:
1. B. M. Stewart, "Cyclic properties of Miquel polygons", Amer. Math. Monthly 47 (1940) 462–466. **Secondary only** (statement read as quoted in McDonald–Garcia–Reznik, Theorem 2 of [9]): "Let P be a polygon with n sides. M^n(P) is similar to P with M as the self-homologous point."
2. N. McDonald, R. Garcia, D. Reznik, "Exploring the dynamics of the circumcenter map", arXiv:2202.02551v3 (2022). https://arxiv.org/abs/2202.02551. **Read** (§1–2 and references, from the downloaded PDF). The circumcenter map C_M "upon n iterations sends an n-gon to a scaled and rotated copy of itself". C_M(P) is the half-sized M-antipedal polygon, and M^{-n}_⊥(P) is similar to P.
3. Wikipedia, "Negative pedal curve". https://en.wikipedia.org/wiki/Negative_pedal_curve. **Read.** The envelope of the lines through X perpendicular to XP; the negative pedal of the pedal is the original. Cites Lockwood, *A Book of Curves* (1961), pp. 157–160; Edwards 1892 p. 165.
4. MathWorld, "Negative Pedal Curve". https://mathworld.wolfram.com/NegativePedalCurve.html. **Read.** Same definition; cites Ameseder 1879 ("Theorie der negativen Fusspunktencurven"), Lawrence 1972 pp. 46–49, Lockwood 1967 ch. 19.
5. L. G. Gheorghe, "Poristic virtues of a negative-pedal curve", arXiv:2012.12385 (2020). https://ar5iv.labs.arxiv.org/html/2012.12385. **Read** (Def. 2, Prop. 1). The negative pedal "is the polar dual of its inverse" (inversion centred at the pedal point), stated as classical without a source. This is the curve form of "T = polar reciprocation composed with inversion of the poles".
6. Wikipedia, "Pedal curve". https://en.wikipedia.org/wiki/Pedal_curve. **Read.** Iterated positive and negative pedals C_1, C_2, … for curves; plane curves only.
7. MathWorld, "Pedal Triangle". https://mathworld.wolfram.com/PedalTriangle.html. **Read.** "The third pedal triangle is similar to the original one"; "the nth pedal n-gon of any n-gon is similar to the original one" (no citation attached on the page).
8. MathWorld, "Antipedal Triangle". https://mathworld.wolfram.com/AntipedalTriangle.html. **Read.** "the triangle of which ΔABC is the pedal triangle with respect to P"; cites Gallatly, *Modern Geometry of the Triangle* (1913) ch. 7.
9. A. Kostanyan, "Pedal tetrahedrons", Mathematics in School (ASPU) 6(119) (2026). https://mathinschool.aspu.am/index.php/mathinschool/article/view/58. **Abstract only.** "Fourth pedal tetrahedron is similar to the original" for any point. The definition of the pedal tetrahedron was not seen.
10. C.-A. Hsu et al., "Topics on pedal polygons", arXiv:2108.08293 (2021). https://arxiv.org/abs/2108.08293. **Abstract only.** No iteration result.
11. G. W. Hart, "Calculating canonical polyhedra", Mathematica in Education and Research 6(3) (1997) 5–10; supplement https://georgehart.com/canonical/canonical-supplement.html. **Supplement read; paper not read.** The supplement says the existence proof gives no construction and does not describe the iteration.
12. A. Levskaya, *polyHédronisme* (JavaScript, "adapted from" G. W. Hart's Conway-notation code), `geo_operators.js`. https://github.com/levskaya/polyhedronisme. **Source read.** `canonicalXYZ` loops `dpoly.vertices = reciprocalN(poly); poly.vertices = reciprocalN(dpoly)`. `reciprocalN` maps each face to the unit-sphere reciprocal of its plane, times the edge-correction factor (1 + avgEdgeDist)/2. This is iterated reciprocation with a per-face rescale, used to converge to the canonical form. It is the nearest algorithmic relative of T∘T found; its aim is a fixed point, not similarity periods or gains.
13. Hart, Conway notation page (as A1 #3). **Read.** "Canonicalization … with my new iterative 'primal/dual' algorithm"; "The c operator does ten iterations".
14. Antiprism, `canonical` documentation. https://antiprism.com/programs/canonical.html. **Read.** The base/dual method "reciprocate on face normals"; planarize "reciprocate on face centroids magnitude squared"; the target is a unit midsphere.
15. D. Hatch, "A canonical reciprocation center for convex objects", draft, 2003. https://www.plunk.org/~hatch/CanonicalReciprocationCenter/html/CanonicalReciprocationCenter/. **Read** (HTML). Reciprocating about the centroid of P and then about the centroid of the result gives P′, which in general does not have the same shape as P. "the radius of reciprocation is irrelevant" to his centre. No study of repeated reciprocation in varying spheres.
16. N. P. Frank, S. Hart, "A dynamical system using the Voronoi tessellation", arXiv:0712.3736 (2007). https://arxiv.org/abs/0712.3736. **Abstract only.** A planar point set → the vertex set of its Voronoi tessellation; growth of set size under iteration. This is a different map (all Voronoi vertices, not one cell), but the same family.
17. J. Schreiber, A. Veselov, J. Ward, "In search for a perfect shape of polyhedra: Buffon transformation", arXiv:1402.5354. **Snippet only.** Another iterated polyhedron map with a limit shape; uses kis to make simplicial polyhedra. Different map.
18. Wikipedia, "Conway polyhedron notation". https://en.wikipedia.org/wiki/Conway_polyhedron_notation. **Read** (first 100 000 characters). Operator powers (j² = o, dd = S, kk); combinatorial only; no geometric iteration result.

---

## B. Core cycles (intersection of the hulls of spike tips grouped by face family; period two; scaling t² cos²θ)

**Verdict: the ingredients are classical; nothing found for the cycle or the scaling law.** The first step for the quasi-regular solids is classical: the cube ∩ octahedron core is the cuboctahedron, and the dodecahedron ∩ icosahedron core is the icosidodecahedron (the core of a dual compound is the rectification), and the stellation core is a standard notion. I found no source on iterating "hull of each family of polar tips → intersect" or on a period-two alternation, and none on the turn factor t² cos²θ. Nothing found in the sources listed.

Sources found:
1. Wikipedia, "Polytope compound" (as A1 #4). **Read.** The core of a compound is "the small central space common to all members of the compound", usable as the core for a set of stellations; for dual compounds the core is the rectification.
2. Wikipedia, "Compound of cube and octahedron" (A1 #6). **Read.**
3. Hart, Conway notation page (A1 #3). **Read.** For mutually dual polyhedra tangent to a common sphere, "the ambo of either is their intersection".
4. Coxeter 1997 (A1 #2). **Abstract only.** Π− = the common content or "core" of Π and its reciprocal.
5. Messer 1995 (A1 #11), p. 2. **Read.** The stellation core definition.
6. Search snippets only (not opened): Wikipedia "Compound of dodecahedron and icosahedron" (core = icosidodecahedron, Wenninger 47); Hart, "Compounds of Polyhedra" https://w.georgehart.com/virtual-polyhedra/compounds-info.html; Hart, "Stellations of the cuboctahedron".

---

## C. Gains ((R/r)² for Platonic solids; 10/(2cos(π/n))⁴ for the quasi-regular solids; primes in the norms)

**Verdict: the radius values are classical. The splitting criterion is a standard textbook fact (citable). Nothing found on gains of iterated duality.** Wikipedia gives R/r = tan(π/p) tan(π/q) for {p,q}, so (R/r)² = 9 (tetrahedron), 3 (cube and octahedron), and 3 tan²(π/5) = 15 − 6√5 (dodecahedron and icosahedron; norm 45 = 3²·5). MathWorld gives the cuboctahedron and icosidodecahedron radii from which the quasi-regular values can be checked. The splitting of rational primes in Q(√5) (p ≡ ±1 mod 5 split, ±2 inert, 5 ramified) and in Q(√2) ((2/p) = 1 iff p ≡ ±1 mod 8, so those split, ±3 inert, 2 ramified; disc 8) is standard. I found no source linking iterated reciprocation or Voronoi growth to these ratios or to the prime factors of their norms. Nothing found in the sources listed.
Caution for the paper: in a norm N(α), an inert prime can occur, but only to an even power (N(p) = p²). The accurate wording is "every prime ≠ 5 (resp. ≠ 2) that divides the norm to an odd power splits". The stronger claim "only split primes besides 5 and 2" is a fact about the particular gains and must be checked number by number.

Sources found:
1. Wikipedia, "Platonic solid" (accessed 2026-10-31), section on radii. https://en.wikipedia.org/wiki/Platonic_solid. **Read** (first 100 000 characters). R = (a/2) tan(π/q) tan(θ/2), r = (a/2) cot(π/p) tan(θ/2), "R/r = tan(π/p) tan(π/q)", and a table of r, ρ, R for a = 2. The page gives no source for the table in the part read.
2. MathWorld, "Cuboctahedron". https://mathworld.wolfram.com/Cuboctahedron.html. **Read.** Unit edge: r₃ = √6/3, r₄ = √2/2, ρ = √3/2, R = 1.
3. MathWorld, "Regular Icosidodecahedron". https://mathworld.wolfram.com/RegularIcosidodecahedron.html. **Read.** Unit edge: r₃ = √((7+3√5)/6), r₅ = √((5+2√5)/5), ρ = ½√(5+2√5), R = φ.
4. MathWorld, "Dual Polyhedron" (A1 #7). **Read.** R r = ρ² for dual pairs about the midsphere; Cundy & Rollett Table II.
5. Wikipedia, "Icosidodecahedron" and "Cuboctahedron". **Read** (first 100 000 characters each). Circumradius only (φ for unit edge; = edge), citing Williams 1979 p. 86 and Coxeter 1973 p. 69 §4.7.
6. Timothy Murphy(?), Trinity College Dublin Number Theory course notes, ch. 15 "Q(√5) and the golden ratio". https://www.maths.tcd.ie/pub/Maths/Courseware/NumberTheory/ch15.pdf. **Read** (downloaded PDF; the author's name is not on the chapter, attribution unconfirmed). Theorem 15.3: "If p ≡ ±1 mod 5 then p splits into conjugate primes in Z[φ]"; "If p ≡ ±2 mod 5 then p remains prime". Theorem 15.2: the units are ±φⁿ.
7. G. H. Hardy, E. M. Wright, *An Introduction to the Theory of Numbers*, 5th ed., OUP, ch. XV, Theorem 257(2), p. 222. **Secondary citation only** (via OEIS A003631, https://oeis.org/A003631, read). The book was not seen; check the theorem number against the edition before citing.
8. K. Ireland, M. Rosen, *A Classical Introduction to Modern Number Theory*, 2nd ed., Springer GTM 84 (1990), ch. 13 "Quadratic and Cyclotomic Fields". **Catalogue/TOC only** (Springer chapter record https://link.springer.com/chapter/10.1007/978-1-4757-2103-4_13, snippet). The proposition number was not verified.
9. Wikipedia, "Quadratic field". https://en.wikipedia.org/wiki/Quadratic_field. **Read.** Ramified iff p | D; otherwise the Kronecker symbol (D/p) decides split or inert; disc Q(√5) = 5, disc Q(√2) = 8. Cites Stevenhagen's "Number Rings" notes p. 36, Samuel 1972, Stewart & Tall 1979 §3.1.
10. Wikipedia, "Quadratic reciprocity". https://en.wikipedia.org/wiki/Quadratic_reciprocity. **Read** (first 100 000 characters). Second supplement: solvable iff p ≡ ±1 (mod 8); (5/p) = 1 iff p ≡ ±1 (mod 5) (stated from the table, §2.4).
11. L. Goldmakher, "Legendre, Jacobi, and Kronecker symbols", lecture notes, Williams College. https://web.williams.edu/Mathematics/lg5/Kronecker.pdf. **Read** (downloaded PDF). (2/p) = 1 if p ≡ ±1 (mod 8), −1 if ±3; (5/p) = −1 if p ≡ ±2 (mod 5).
12. Wikipedia, "Splitting of prime ideals in Galois extensions". **Read.** General ramification ⇔ divides the discriminant; worked example Q(i) only.
13. Library: J. H. Conway, C. Radin, L. Sadun, "On angles whose squared trigonometric functions are rational", Discrete Comput. Geom. 22 (1999) (`papers/Conway-Radin-Sadun-1999-Angles-squared-trig-rational.pdf`), pp. 4–8. **Read.** Splitting criteria (Theorems 5–6) for imaginary quadratic fields Q(√−d), cites Pollard & Diamond, *The Theory of Algebraic Numbers*. This is the imaginary case only, but it is the nearest library item using prime splitting for polyhedral angles.

Not found in the library: Ireland & Rosen, Hardy & Wright, Coxeter *Regular Polytopes* (catalogue entry only, no PDF; its Table I would be the classical citation for R, ρ, r, but it was not read).

---

## Full list of sources checked

### Library queries (`~/bin/ask-library "QUERY" 8`), verbatim, with top hits
1. "polar reciprocal convex hull" — catalogue: Hepworth 2022 *Groups of convex bodies*; O'Rourke 2023 *Polar zonohedra edge-unfold*; Matteo 2014 *Combinatorially two-orbit convex polytopes*; Cunningham–Mixer 2016 *Internal and external duality in abstract polytopes*. Pages: Betke–Henk 2000 p.35 (references); Bezdek–Lángi–Naszódi–Papez 2007 *Ball-polyhedra* pp. 7, 9, 30; Dutour Sikirić–Schürmann–Vallentin 2008 pp. 7, 31. Nothing on the hull of P and its polar.
2. "reciprocation dual polyhedron midsphere" — catalogue: Hynd 2023 *Reuleaux polyhedron*; Richter-Gebert 2026 *An almost trivial observation about the icosahedron*; Leppmeier 2019 *Dodecahedron as a Voronoi cell*; Wikipedia *Goldberg polyhedron*. Pages: Kepler 1619 *Harmonices mundi* p. 271 (Latin OCR, not usable); Hynd p. 31; Torquato–Jiao 2009 p. 5 (dual pairs, background); Al-Siyabi–Koca–Koca 2020 p. 6. Nothing relevant.
3. "Conway join operator" — catalogue: Antiprism `conway` docs (#170); Gosain–Grimmer 2025; Kun 2021. Pages: Kepler OCR. Only the Antiprism docs (link-only entry) are relevant.
4. "convex hull of a polyhedron and its dual compound" — catalogue: Cunningham–Mixer 2016; Hynd 2023; Hepworth 2022; Erdahl 1999 *Zonotopes, dicings*. Pages: Betke–Henk p.35; Dutour Sikirić et al. p.7; Grünbaum 2010 *Bilinski dodecahedron* p. 23; Torquato–Jiao p.5. Nothing relevant.
5. "kis kleetope pyramids on faces" — catalogue: *Face embeddings of Archimedean solids*; Wikipedia *Rhombic dodecahedron*; Richter-Gebert 2026; Leppmeier 2019. Pages: Dürer 1525 p. 78; Pacioli 1509 pp. 15, 43, 48. Nothing relevant.
6. "canonical polyhedron iterated reciprocation" — catalogue: Hynd 2023; *From the hyperbolic 24-cell to the cuboctahedron*; *Regular Sierpinski polyhedra*; *Unfolding overlaps of the exceptional regular polytopes*. Pages: Kepler p.271; Koskinen 2011 Bridges p.1; arXiv 1206.3716 p.21; Wikipedia *Goldberg polyhedron* p.1. Nothing relevant.
7. "iterated duality sequence of polyhedra converges" — catalogue: Cunningham–Mixer 2016; *Self-dual polyhedra of given degree sequence*; Baumbach–Freyer–Weigert–Winter 2025 *The canonical form, scissors congruence and adjoint degrees*; Delaunay classification paper. Pages: Bezdek et al. p.19; Garber 2019 p.33; Cutler–Schulte 2011 p.26. Nothing relevant.
8. "Voronoi cell of points" — catalogue: three hyperbolic Voronoi diagram papers; Leppmeier 2019; Aurenhammer-type survey *Voronoi diagrams: a survey of a fundamental geometric data structure*. Pages: Betke–Henk; Garber 2019 p.38; Hales 1998 p.8. Background only.
9. "compound of dual polyhedra intersection core" — catalogue: *Crystal structure generation … dual periodic graphs*; Cunningham–Mixer; Koca et al. *Quasi regular polyhedra and their duals … quaternions II*; *30 Cubes on a rhombic triacontahedron*. Pages: Torquato–Jiao p.5; Akpanya et al. 2024 p.27; Erdahl–Rybnikov 2001 p.18. Nothing relevant.
10. "stellation core kernel" — catalogue: Antiprism `conway`; Sonobé modules paper; power-diagram papers. Pages: **Messer 1995 p.2 (read: stellation core definition)**; Dürer pp. 9, 142, 157.
11. "circumradius inradius ratio Platonic solids" — catalogue: Hynd; Richter-Gebert; *Hexagons and the golden ratio*; *30 Cubes*; Datta–Maity 2018; Torquato–Jiao. Pages: Kepler pp. 271, 274, 279; Pacioli pp. 36, 38, 107 (historic, not usable as a modern citation). Nothing citable.
12. "splitting of primes quadratic field golden ratio" — catalogue: *Hexagons and the golden ratio*; *Proof of aperiodicity of hat tile using the golden ratio*; *Coincidence-site lattices*; Conway–Radin–Sadun 1999. Pages: **Conway–Radin–Sadun pp. 4–8 (read)**.
13. "midsphere edges tangent canonical" — catalogue: *Mutually equidistant spheres that intersect*; spline papers; O'Rourke 2023. Pages: Dürer, Kepler. Nothing relevant.
14. "pedal triangle iterated similar" — catalogue: *Hexagons and the golden ratio*; *G_δ circle squaring*; *Magic numbers in polygonal and polyhedral clusters*. Pages: Pacioli. Nothing relevant.
15. "negative pedal curve envelope perpendicular lines" — catalogue: *Scissors congruence of the line and the regulator*; *Half-space power diagrams and discrete surface offsets*. Pages: Dürer. Nothing relevant.
16. "dynamical system on polygons or polyhedra iteration similarity" — catalogue: *Tilings from tops of overlapping IFS*; *Regular Sierpinski polyhedra*; *On folding a polygon to a polyhedron*. Pages: Moody 2000 pp. 27–28; Goldberg 1937 p.1. Nothing relevant.
17. "Dedekind domain norm prime split ramified" — catalogue: SL₂ homology papers; Singer 1938. Pages: Conway–Radin–Sadun pp. 6–8, 12. Same item as query 12.
18. "quasi-regular polyhedra cuboctahedron icosidodecahedron radii" — catalogue: Koca et al. *Quasi regular polyhedra … II* (catalogue only); Wikipedia *Rhombic dodecahedron*. Pages: Al-Siyabi–Koca–Koca p.6; Wikipedia *Tetrahedral-octahedral honeycomb* p.13. Nothing on radii ratios.
Also grepped the library `INDEX.html` for: Hart, Coxeter, antiprism, canonical, reciproc, Ireland, Hardy, Wright, Cundy, Wenninger (found Firsching 2015 #155, read).

### Web queries (WebSearch), verbatim
1. Eppstein convex hull of a polytope and its polar slides
2. convex hull of polyhedron and its polar dual canonical midsphere edges cross at right angles
3. George Hart canonical polyhedra algorithm reciprocation iterate converge
4. polyhedronisme canonicalXYZ reciprocalN source
5. iterated polar reciprocation polyhedron different radius sequence similar shape periodic
6. "{x : v·x ≤ |v|^2}" OR "x·v ≤ |v|^2" polytope vertices tangent planes perpendicular radius "Voronoi cell" of 2v
7. polytope whose facets are perpendicular to the vertices of another polytope at the vertices "tangent planes" dual "pedal" polytope
8. n-th pedal polygon similar to original polygon theorem Langr Kingston Synge sequence of pedal triangles
9. pedal polyhedron OR "pedal polytope" iterated similar three dimensions
10. Stewart 1940 "Cyclic properties of Miquel polygons" American Mathematical Monthly nth pedal polygon similar
11. intersection of two dual polyhedra in a compound is the rectified (ambo) polyhedron, convex hull is the join
12. "stellation" "core" compound polyhedra common intersection "kernel" Wenninger polyhedron models
13. alternating sequence of polyhedra cube octahedron nested scale factor iteration dual compound inscribed limit
14. Hart "Calculating canonical polyhedra" Mathematica in Education and Research 1997 reciprocation algorithm
15. David Eppstein convex hull polytope union polar dual midsphere canonical polyhedra slides ics.uci.edu
16. 11011110 Eppstein blog polar dual convex hull "and its polar" polyhedron
17. convex hull of a polytope and its scaled polar reciprocal combinatorial type tetrahedra over edges pyramids over vertices
18. repeated Kleetope kis iteration polyhedron converge shape limit
19. "dual of the dual" polyhedron "circumradius" "inradius" ratio scale factor (R/r)^2 Platonic reciprocal unit sphere
20. iterated Voronoi cell map polytope "Voronoi cell" of reflected points fixed point similar polytope iteration
21. Hardy Wright "primes in k(√5)" theorem rational primes p ≡ ±1 mod 5 factorise golden ratio field chapter 15
22. Ireland Rosen "A Classical Introduction to Modern Number Theory" chapter 13 quadratic field prime decomposition Proposition 13.1.3 Legendre symbol

Queries that gave nothing usable: 1 (the Eppstein slides came from query 16), 5, 6, 7 (except that it led to the negative pedal), 13, 17 (except Coxeter's abstract), 19, 22 (TOC only).

### Pages read (WebFetch, or curl + pdftotext)
- https://antiprism.com/programs/canonical.html
- https://georgehart.com/canonical/canonical-supplement.html
- https://www.plunk.org/~hatch/CanonicalReciprocationCenter/html/CanonicalReciprocationCenter/
- https://en.wikipedia.org/wiki/Conway_polyhedron_notation (first 100 000 chars)
- https://www.georgehart.com/virtual-polyhedra/conway_notation.html
- https://en.wikipedia.org/wiki/Dual_polyhedron
- https://code.studioinfinity.org/glen/archematics/commit/cbe44238a181bca70465fca780dfe4d183b3f459.diff (gave garbage; no content)
- https://raw.githubusercontent.com/levskaya/polyhedronisme/master/geo_operators.js and geo.js (curl)
- https://en.wikipedia.org/wiki/Pedal_curve
- https://ar5iv.labs.arxiv.org/html/2012.12385
- https://en.wikipedia.org/wiki/Negative_pedal_curve
- https://mathworld.wolfram.com/NegativePedalCurve.html
- https://mathworld.wolfram.com/Reciprocation.html (nothing on pedals)
- https://mathworld.wolfram.com/PedalCurve.html (nothing on inversion)
- https://mathinschool.aspu.am/index.php/mathinschool/article/view/58 (abstract)
- https://mathworld.wolfram.com/PedalTriangle.html
- https://arxiv.org/abs/2108.08293 (abstract)
- https://mathworld.wolfram.com/AntipedalTriangle.html
- https://arxiv.org/pdf/2202.02551 (downloaded; read with pdftotext)
- https://en.wikipedia.org/wiki/Compound_of_cube_and_octahedron
- https://en.wikipedia.org/wiki/Polytope_compound
- https://en.wikipedia.org/wiki/Platonic_solid (first 100 000 chars)
- https://en.wikipedia.org/wiki/Icosidodecahedron (first 100 000 chars)
- https://en.wikipedia.org/wiki/Cuboctahedron (first 100 000 chars)
- https://mathworld.wolfram.com/Icosidodecahedron.html (no radii; pointed to the next page)
- https://mathworld.wolfram.com/RegularIcosidodecahedron.html
- https://mathworld.wolfram.com/Cuboctahedron.html
- https://en.wikipedia.org/wiki/Splitting_of_prime_ideals_in_Galois_extensions
- https://en.wikipedia.org/wiki/Quadratic_field
- https://en.wikipedia.org/wiki/Quadratic_reciprocity (first 100 000 chars)
- https://ics.uci.edu/~eppstein/pubs/Epp-COMB-01.pdf (WebFetch: certificate rejected; read via curl -k + pdftotext)
- https://www.cambridge.org/core/journals/journal-of-the-london-mathematical-society/article/reciprocating-the-regular-polytopes/2D387F9B5EEE1B90439C27746AFCC1DC (abstract)
- https://antiprism.com/programs/pol_recip.html
- https://arxiv.org/abs/0712.3736 (abstract)
- https://mathworld.wolfram.com/DualPolyhedron.html
- https://www.maths.tcd.ie/pub/Maths/Courseware/NumberTheory/ch15.pdf (downloaded; pdftotext)
- https://oeis.org/A003631
- https://web.williams.edu/Mathematics/lg5/Kronecker.pdf (downloaded; pdftotext)

Library PDFs read directly: Messer 1995 p. 2; Firsching 2015 (polar passage); Conway–Radin–Sadun 1999 pp. 4–8.

## Suggestions for the papers (from this search)
- A2: credit the planar case to Stewart 1940 (via McDonald–Garcia–Reznik 2022) and use the antipedal/negative-pedal name: T in the plane is the O-antipedal polygon, and T is the discrete negative pedal. State the paper's novelty only for polyhedra whose combinatorics change between steps, as "nothing found in the sources listed".
- A1: cite Eppstein 2001 and Hart/Conway (jX = daX) for the midsphere case and Coxeter 1997 for hull/core of reciprocal regular polytopes; claim only the general-ρ decomposition.
- C: cite Wikipedia/Coxeter for R/r = tan(π/p)tan(π/q); for the splitting, cite Hardy & Wright Thm 257 after checking it in the book (or Ireland & Rosen ch. 13). Fix the wording on inert primes (even powers) as noted under C.
