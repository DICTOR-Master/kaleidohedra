# DICTO · dictospheres.com — writes the four short introductory papers (DICTO 2026-10-17: "a short introductory paper for each, with DOIs")
import os
HEAD = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="../../paper.css">
<style>.figs.two{{grid-template-columns:1fr 1fr}} td.n{{font-variant-numeric:tabular-nums}} table{{font-size:8.8pt}}</style></head><body>
<img class="watermark" src="../../dicto-logo.png" alt="">
<img class="logo" src="../../dicto-logo.png" alt="DICTO">
<h1>{title}</h1>
<p class="sub">{sub}</p>
<div class="meta">
<b>DICTO</b> (artist, Osaka, Japan) · contact@dictospheres.com · https://dictospheres.com<br>
{version} · DICTO DOI: 10.5281/zenodo.{doi} (all versions) · Licence CC BY 4.0 · An introduction to one solid; its parent paper: {parent}. Data and checks are included with this record.<br>
{credit}
</div>
'''
TAIL = '</body></html>\n'
P = {}
DOI = {'metaxy': '23430864', 'palin': '23430866', 'hecatogdo': '23430868', 'ocd-stella': '23430870'}
P['metaxy'] = dict(title='The DICTO Metaxyhexecontahedron', sub='The solid in the last gap of the golden cycle: a dodecahedron–icosahedron hull whose icosahedron edge is 9/φ⁴ times its dodecahedron edge',
  parent='Vajrayana, DICTO DOI: 10.5281/zenodo.23429911',
  credit="""The idea that one more solid fits the last gap of the cycle, and the name, are DICTO's; the exact computations and the text were done with an AI assistant (Claude, Anthropic).""",
  body='''<div class="abstract"><b>Abstract.</b> The DICTO Metaxyhexecontahedron M (Greek <i>metaxý</i>, "in-between", and 60 faces) is the convex hull of a regular icosahedron and a dodecahedron placed over its faces, at the one size where the icosahedron edge is exactly 9/φ⁴ ≈ 1.31308 times the dodecahedron edge. In closed form it is the hull of (0, ±1, ±φ) and (φ⁵/9)·{(±1, ±1, ±1), (0, ±φ, ±1/φ)} (cyclic). It has 32 corners, 90 edges and 60 congruent isosceles triangles, an insphere but no midsphere. In the twelve-station golden cycle of Vajrayana it is the station between the rhombic triacontahedron and the next icosahedron: its 12 five-fold corners are the triacontahedron's own, its 20 three-fold corners sit exactly on the centres of the next icosahedron's faces, and each of the two layers it makes is a single kind of piece. Everything here is exact in ℚ(√5).</div>

<figure><div class="figs two"><img src="figures/m-alone.png"><img src="figures/m-in-cycle.jpg"></div>
<figcaption><b>Figure 1.</b> Left: the DICTO Metaxyhexecontahedron. Right: in the twelve-station cycle (brick red), between the rhombic triacontahedron (orange) and the next icosahedron (glass), with the 60 pieces of one kind that fill the step outside it (sand). Drawn from exact corners.</figcaption></figure>

<h2>1. The solid</h2>
<p>Take the icosahedron with corners (0, ±1, ±φ) and their cyclic shifts (edge 2), and the dodecahedron with corners (±1, ±1, ±1) and the cyclic shifts of (0, ±φ, ±1/φ), placed so that its corners lie over the icosahedron's face centres (edge 2/φ). Scale the dodecahedron by k and take the convex hull. Its icosahedron edge is then φ/k times its dodecahedron edge. The DICTO Metaxyhexecontahedron is the member with k = φ⁵/9 = 11/18 + 5√5/18, so that the ratio is 9/φ⁴ (squared, 81/φ⁸).</p>
<table><tr><th>Property</th><th>Value (exact)</th></tr>
<tr><td>corners</td><td>32: 12 five-fold (the icosahedron's), 20 three-fold (the dodecahedron's)</td></tr>
<tr><td>faces, edges</td><td>60 congruent isosceles triangles, 90 edges; the combinatorics of the pentakis dodecahedron</td></tr>
<tr><td>squared edge lengths</td><td>94/81 + 14√5/27 (60 edges, five-fold to three-fold) and 14/9 + 2√5/27 (30 edges, three-fold to three-fold)</td></tr>
<tr><td>squared corner radii</td><td>5/2 + √5/2 (five-fold) and 41/18 + 55√5/54 (three-fold)</td></tr>
<tr><td>insphere</td><td>all 60 faces at squared distance 7249/4162 + 16209√5/20810</td></tr>
<tr><td>midsphere</td><td>none: the two kinds of edge lie at squared distances 2 + 20√5/27 and 161/81 + 8√5/9</td></tr>
<tr><td>volume</td><td>410/27 + 550√5/81 ≈ 30.3684 (in these units)</td></tr></table>
<p class="cap"><b>Table 1.</b> The DICTO Metaxyhexecontahedron in closed form (<code>scripts/hull_family_exact.py</code>, every face plane and every corner tested exactly).</p>

<h2>2. Where it comes from: the last gap of the golden cycle</h2>
<p>The Spheres of Dharma (DICTO DOI: 10.5281/zenodo.23310833) nest icosahedral shells in a cycle that repeats every φ³; Progenitors (DICTO DOI: 10.5281/zenodo.23413184) set the DICTO Ogdoecontahedron into it, and Vajrayana (DICTO DOI: 10.5281/zenodo.23429911) closed its loose steps. In the step from the rhombic triacontahedron RT to the next icosahedron I·φ³, the triacontahedron reaches only 0.812 of the way. DICTO judged that one more solid should fit there. Among the convex icosahedral solids none touches both neighbours (Vajrayana, Table 3, float); this member of the dodecahedron–icosahedron hull family does. In the cycle's own units it is the hull of the triacontahedron's 12 five-fold corners and the 20 face centres of I·φ³ (squared radii 45/8 − 9√5/8 and 47/24 + 7√5/8; the same solid as Table 1, checked exactly). Cut by cones from the centre over the faces of the inner solid, the step RT → M is 30 pieces of one kind and M → I·φ³ is 60 pieces of one kind (a triangular-bipyramid shape); M takes 0.356 of the step's volume. Its polar, with 12 regular pentagons and 20 hexagons whose sides alternate in the ratio (14 + 9√5)/11, closes the matching step of the polar-reversed cycle.</p>

<h2>3. Its family</h2>
<p>The hulls of a dodecahedron and an icosahedron in dual position form a one-parameter family with the pentakis dodecahedron's combinatorics, fully symmetric for edge ratios from (5 + 3√5)/10 to φ. Its named members are the Catalan pentakis dodecahedron at 3(7 + 5√5)/38 ≈ 1.435, the DICTO Palintriacontahedron at 3/√5 ≈ 1.342 (DICTO DOI: 10.5281/zenodo.23430866), and the DICTO Metaxyhexecontahedron at 9/φ⁴ ≈ 1.313. We note without explanation that 9/φ⁴ is also the exact gain per round of the tightest progenitor cycle in Progenitors.</p>

<h2>4. Status</h2>

<p><b>Known:</b> the family (the pentakis dodecahedron as the hull of a dodecahedron and an icosahedron, and its fully symmetric range: Polytope Wiki; the Catalan member: MathWorld, McCooey). <b>Not found, in the sources checked</b> (listed in Vajrayana §5 and its study's SEARCH-LOG.md): this member as a named or distinguished solid, or the 9/φ⁴ ratio as distinguished. The name returns no results. Every "not found" is limited to those sources.</p>
<p><b>Sources checked on the web (17 October 2026):</b></p><ul><li><b>Polytope Wiki</b>, "Pentakis dodecahedron": the hull of a dodecahedron and an icosahedron is fully symmetric for edge ratios from (5 + 3√5)/10 to φ; the only member given is 3(7 + 5√5)/38; neither 9/φ⁴ nor 3/√5 appears.</li><li><b>Wikipedia</b>, "Pentakis dodecahedron": the canonical form only (icosahedron scaled by (3φ + 12)/19); no other member.</li><li><b>MathWorld</b>, "Pentakis Dodecahedron" and "Dodecahedron–Small Triambic Icosahedron Compound" (whose hull has the pentakis connectivity: a different member).</li><li><b>McCooey, Visual Polyhedra</b>: Pentakis Dodecahedron, Great Pentakis Dodecahedron, Archimedean–Catalan Hulls, Biscribed Solids; no such member.</li><li><b>OEIS</b>: the digits of 9/φ⁴ match no sequence.</li><li><b>Bridges 2017</b> and <b>Wassell and Benito 2012</b> (edge ratios of dual pairs, φ/3 and φ²/√5); <b>arXiv</b> (nested golden shells, hulls of dual pairs; closest: arXiv:2008.00862, a tiling).</li><li><b>Web search</b> for the name: no results.</li></ul>
<p><b>Polyhedron software libraries (17 October 2026):</b></p><ul><li><b>SageMath</b> polytope library (<code>polytopes.*</code>): its icosahedral constructors are the icosahedron, dodecahedron, icosidodecahedron, truncated icosahedron and the other Archimedean solids, and the pentakis dodecahedron; none of the solids here.</li><li><b>netlib polyhedra database</b> (142 entries: Platonic, Archimedean and their duals, prisms, the 92 Johnson solids and five others): none of the solids here (the pentakis dodecahedron, file 41, is the canonical one).</li><li><b>Antiprism</b> 0.29 (A. Rossiter): used to recompute and check the structures independently (for Vajrayana and Progenitors, and the companion's type t3jD); its Conway-operator sweep is a generator, not a catalogue.</li><li><b>Not run:</b> Wolfram <code>PolyhedronData</code> (needs Mathematica) and Stella / Great Stella (R. Webb; its library beyond the uniform, Johnson and Stewart-toroid models is not listed online). No claim is made about them.</li></ul>
<p>The reference library: see the Appendix.</p>

<h2>5. Files</h2>
<p><code>scripts/hull_family_exact.py</code> and its output <code>data-hull-family-exact.txt</code> (this paper, exact). The cycle, the pieces and the dual: Vajrayana's record and the study at https://github.com/DICTOR-Master/kaleidohedra (branch research: studies/2026-10-16-progenitors: <code>gap_member.py</code>, <code>gap_pieces_exact.py</code>, <code>metaxy_dual.py</code>). See it in the app: Kaleidohedra, 3D+ → Vajrayana.</p>
''')
P['palin'] = dict(title='The DICTO Palintriacontahedron', sub='The rhombic triacontahedron turned inside out: the hull of the icosidodecahedron star at full height, its icosahedron edge 3/√5 times its dodecahedron edge',
  parent='Vajrayana, DICTO DOI: 10.5281/zenodo.23429911',
  credit="""Flipping the icosidodecahedron's own central pyramids out at full height ("shortening feels like cheating; one more solid is needed") and the name are DICTO's; the exact computations and the text were done with an AI assistant (Claude, Anthropic).""",
  body='''<div class="abstract"><b>Abstract.</b> Flip the icosidodecahedron's 32 central pyramids out at full height and take the hull of their tips: the result is the DICTO Palintriacontahedron X (Greek <i>pálin</i>, back), with 32 corners and 60 triangular faces, each half a rhombic-dodecahedron rhombus (cos² of its angles 1/9, 1/3, 1/3). It is the member of the dodecahedron–icosahedron hull family whose icosahedron edge is exactly 3/√5 times its dodecahedron edge, in closed form the hull of (0, ±1, ±φ) and ((5 + √5)/6)·{(±1, ±1, ±1), (0, ±φ, ±1/φ)} (cyclic). It has the rhombic triacontahedron's 32 axes with the reciprocal radius ratio: the triacontahedron turned inside out. Everything here is exact in ℚ(√5) unless marked float.</div>

<figure><div class="figs wide"><img src="figures/x-star.jpg"></div>
<figcaption><b>Figure 1.</b> The icosidodecahedron star (its central pyramids flipped out at full height), inside its hull, the DICTO Palintriacontahedron, and X interlocked with the next icosahedron. Drawn from exact corners.</figcaption></figure>

<h2>1. The solid</h2>
<p>With the icosahedron (0, ±1, ±φ) (cyclic, edge 2) and the dodecahedron (±1, ±1, ±1), (0, ±φ, ±1/φ) (cyclic) placed over its faces, the hull of the icosahedron and k times the dodecahedron has edge ratio φ/k. The DICTO Palintriacontahedron is k = φ√5/3 = 5/6 + √5/6, ratio 3/√5 (squared 9/5).</p>
<table><tr><th>Property</th><th>Value (exact)</th></tr>
<tr><td>corners</td><td>32: 12 five-fold, 20 three-fold, all tips of the full-height icosidodecahedron star</td></tr>
<tr><td>faces, edges</td><td>60 triangles, each half a rhombic-dodecahedron rhombus (cos² of the face angles 1/9, 1/3, 1/3); 90 edges</td></tr>
<tr><td>squared edge lengths</td><td>20/9 (60 edges) and 5/3 (30 edges)</td></tr>
<tr><td>squared corner radii</td><td>5/2 + √5/2 (five-fold) and 5/2 + 5√5/6 (three-fold)</td></tr>
<tr><td>insphere</td><td>all 60 faces at squared distance 7/4 + 3√5/4</td></tr>
<tr><td>midsphere</td><td>none (edges at squared distances 25/12 + 2√5/3 and 35/18 + 5√5/6)</td></tr>
<tr><td>volume</td><td>50/3 + 50√5/9 ≈ 29.0893 (in these units)</td></tr></table>
<p class="cap"><b>Table 1.</b> The DICTO Palintriacontahedron in closed form (<code>scripts/hull_family_exact.py</code>, exact).</p>

<h2>2. Where it comes from</h2>
<p>In the twelve-station golden cycle of Vajrayana (DICTO DOI: 10.5281/zenodo.23429911) the icosidodecahedron is the shell where the cycle's two progenitors meet. DICTO flipped its central pyramids outward at full height rather than shortening them; the hull of the 32 tips is X. It is the rhombic triacontahedron turned inside out: the same 32 axes, with the five-fold and three-fold corners at the reciprocal ratio of radii. Two float observations (labelled as such in Vajrayana): X lies inside the next turn's D′ and 99.46% of its volume (20,000 sample points) lies inside the next icosahedron's Cleo star, so it bridges one turn to the next; and the first stellation of the icosahedron puts its tips at 3/√5 times the face distance, the same number.</p>

<h2>3. Its family</h2>
<p>X belongs to the same hull family as the pentakis dodecahedron (Catalan, ratio 3(7 + 5√5)/38 ≈ 1.435) and the DICTO Metaxyhexecontahedron (9/φ⁴ ≈ 1.313; DICTO DOI: 10.5281/zenodo.23430864). Its ratio 3/√5 ≈ 1.342 lies between them.</p>

<h2>4. Status</h2>

<p><b>Known:</b> the hull family and its fully symmetric range (Polytope Wiki), the rhombic triacontahedron and the icosidodecahedron's central pyramids. <b>Not found, in the sources checked</b> (Vajrayana §5, SEARCH-LOG.md): this member as a named or distinguished solid, or the ratio 3/√5 as distinguished. The name returns no results. Every "not found" is limited to those sources.</p>
<p><b>Sources checked on the web (17 October 2026):</b></p><ul><li><b>Polytope Wiki</b>, "Pentakis dodecahedron": the hull of a dodecahedron and an icosahedron is fully symmetric for edge ratios from (5 + 3√5)/10 to φ; the only member given is 3(7 + 5√5)/38; neither 9/φ⁴ nor 3/√5 appears.</li><li><b>Wikipedia</b>, "Pentakis dodecahedron": the canonical form only (icosahedron scaled by (3φ + 12)/19); no other member.</li><li><b>MathWorld</b>, "Pentakis Dodecahedron" and "Dodecahedron–Small Triambic Icosahedron Compound" (whose hull has the pentakis connectivity: a different member).</li><li><b>McCooey, Visual Polyhedra</b>: Pentakis Dodecahedron, Great Pentakis Dodecahedron, Archimedean–Catalan Hulls, Biscribed Solids; no such member.</li><li><b>OEIS</b>: the digits of 9/φ⁴ match no sequence.</li><li><b>Bridges 2017</b> and <b>Wassell and Benito 2012</b> (edge ratios of dual pairs, φ/3 and φ²/√5); <b>arXiv</b> (nested golden shells, hulls of dual pairs; closest: arXiv:2008.00862, a tiling).</li><li><b>Web search</b> for the name: no results.</li><li><b>Messer 1995</b>, "Stellations of the rhombic triacontahedron and beyond" (in the library, text-searched): the stellations and their duals; not this hull.</li></ul>
<p><b>Polyhedron software libraries (17 October 2026):</b></p><ul><li><b>SageMath</b> polytope library (<code>polytopes.*</code>): its icosahedral constructors are the icosahedron, dodecahedron, icosidodecahedron, truncated icosahedron and the other Archimedean solids, and the pentakis dodecahedron; none of the solids here.</li><li><b>netlib polyhedra database</b> (142 entries: Platonic, Archimedean and their duals, prisms, the 92 Johnson solids and five others): none of the solids here (the pentakis dodecahedron, file 41, is the canonical one).</li><li><b>Antiprism</b> 0.29 (A. Rossiter): used to recompute and check the structures independently (for Vajrayana and Progenitors, and the companion's type t3jD); its Conway-operator sweep is a generator, not a catalogue.</li><li><b>Not run:</b> Wolfram <code>PolyhedronData</code> (needs Mathematica) and Stella / Great Stella (R. Webb; its library beyond the uniform, Johnson and Stewart-toroid models is not listed online). No claim is made about them.</li></ul>
<p>The reference library: see the Appendix.</p>

<h2>5. Files</h2>
<p><code>scripts/hull_family_exact.py</code>, <code>data-hull-family-exact.txt</code> (this paper, exact); <code>id_star.py</code> in the study (branch research: studies/2026-10-16-progenitors). See it in the app: Kaleidohedra, 3D+ → Vajrayana.</p>
''')
P['hecatogdo'] = dict(title='The DICTO Hecatogdoecontahedron', sub='The DICTO Hecatodihedron and the DICTO Ogdoecontahedron interlocked as a self-dual compound of 182 faces',
  parent='Progenitors, DICTO DOI: 10.5281/zenodo.23413184 (and The DICTO Truncated-Icosahedral Hecatodihedron, Version 2, DICTO DOI: 10.5281/zenodo.23360857)',
  credit="""The pairing and the name are DICTO's; the exact computations and the text were done with an AI assistant (Claude, Anthropic).""",
  body='''<div class="abstract"><b>Abstract.</b> The DICTO Hecatodihedron H (102 faces, 80 corners) and its polar, the DICTO Ogdoecontahedron O (80 faces, 102 corners), interlock in the truncated icosahedron's midsphere as one compound: the DICTO Hecatogdoecontahedron (the two names merged), 182 faces and 182 corners, self-dual. Its common core is the rectified truncated icosahedron and its hull the joined truncated icosahedron (the rhombic enneacontahedron), the core and hull of the classical truncated icosahedron–pentakis dodecahedron compound. We claim the pairing and the name only, not the core or the hull. Exact in ℚ(√5) unless marked float.</div>

<figure><div class="figs wide"><img src="figures/oh-compound.jpg"></div>
<figcaption><b>Figure 1.</b> The DICTO Hecatogdoecontahedron: H (gold) and O (teal) interlocked, with the truncated icosahedron and the common core and hull. Drawn from exact corners.</figcaption></figure>

<h2>1. The compound</h2>
<p>Take the Hecatodihedron H of the Spheres of Dharma (DICTO DOI: 10.5281/zenodo.23310833) and reciprocate it in the sphere of squared radius 9/4, the midsphere of the Dharma's truncated icosahedron, which touches H's 90 rhombi and triangles. The polar is the Ogdoecontahedron O at its compound size. Then (exact): the 90 corners of O on that sphere are exactly the 90 edge midpoints of the truncated icosahedron; no corner of H lies inside O and no corner of O inside H.</p>
<table><tr><th>Part</th><th>Corners</th><th>Faces</th></tr>
<tr><td>H, the DICTO Hecatodihedron</td><td class="n">80</td><td>102: 12 pentagons, 30 rhombi, 60 triangles</td></tr>
<tr><td>O, the DICTO Ogdoecontahedron</td><td class="n">102</td><td>80: 20 regular hexagons, 60 kites</td></tr>
<tr><td><b>the compound</b></td><td class="n"><b>182</b></td><td><b>182</b>; self-dual (a solid with its own polar)</td></tr>
<tr><td>common core H ∩ O</td><td class="n">90</td><td>92: the rectified truncated icosahedron (12 regular pentagons, 20 regular hexagons, 60 triangles), all corners on the midsphere</td></tr>
<tr><td>hull</td><td class="n">92</td><td>90 rhombi: the joined truncated icosahedron (rhombic enneacontahedron), the core's polar</td></tr></table>
<p class="cap"><b>Table 1.</b> The DICTO Hecatogdoecontahedron (<code>oh_compound.py</code>; corner and face counts exact, volumes float).</p>

<h2>2. Where it appears</h2>
<p>The compound was first described in Version 2 of the Hecatodihedron paper (DICTO DOI: 10.5281/zenodo.23360857). In Progenitors (DICTO DOI: 10.5281/zenodo.23413184) its core and hull, rTI and jtI, become stations of the golden cycle I ⊂ ID ⊂ O ⊂ rTI ⊂ TI ⊂ H ⊂ jtI ⊂ RT ⊂ I·φ³, so the cycle holds the core and hull of two dual compounds: the classical icosahedron–dodecahedron one (ID, RT) and this one. As the octahedron and cube are the core and hull of the stella octangula, the rectified truncated icosahedron and the rhombic enneacontahedron are those of the Hecatogdoecontahedron.</p>

<h2>3. Status</h2>

<p><b>Known:</b> compounds of a solid with its polar; the truncated icosahedron–pentakis dodecahedron compound, the rectified truncated icosahedron and the rhombic enneacontahedron (MathWorld; Wikipedia; McCooey; Hart). <b>Not found, in the sources checked</b> (Progenitors §4, SEARCH-LOG.md): the compound of H and O. The name returns no results. Every "not found" is limited to those sources.</p>
<p><b>Sources checked on the web (17 October 2026):</b></p><ul><li><b>MathWorld</b>, "Truncated Icosahedron–Pentakis Dodecahedron Compound": the classical compound; no core, hull or H–O compound.</li><li><b>Wikipedia</b>, "Rectified truncated icosahedron" (its dual is topologically the rhombic enneacontahedron) and "Truncated icosahedron".</li><li><b>McCooey, Visual Polyhedra</b>: Rectified and Truncated Archimedean Solids; no compounds are listed.</li><li><b>G. Hart, Virtual Polyhedra</b>: the compound list and the full alphabetic model list (read for Progenitors): compounds of the uniform solids with their duals; not this one.</li><li><b>Web search</b> for the name: no results.</li></ul>
<p><b>Polyhedron software libraries (17 October 2026):</b></p><ul><li><b>SageMath</b> polytope library (<code>polytopes.*</code>): its icosahedral constructors are the icosahedron, dodecahedron, icosidodecahedron, truncated icosahedron and the other Archimedean solids, and the pentakis dodecahedron; none of the solids here.</li><li><b>netlib polyhedra database</b> (142 entries: Platonic, Archimedean and their duals, prisms, the 92 Johnson solids and five others): none of the solids here (the pentakis dodecahedron, file 41, is the canonical one).</li><li><b>Antiprism</b> 0.29 (A. Rossiter): used to recompute and check the structures independently (for Vajrayana and Progenitors, and the companion's type t3jD); its Conway-operator sweep is a generator, not a catalogue.</li><li><b>Not run:</b> Wolfram <code>PolyhedronData</code> (needs Mathematica) and Stella / Great Stella (R. Webb; its library beyond the uniform, Johnson and Stewart-toroid models is not listed online). No claim is made about them.</li></ul>
<p>The reference library: see the Appendix.</p>

<h2>4. Files</h2>
<p>In the study (branch research: studies/2026-10-16-progenitors): <code>oh_compound.py</code> → <code>oh-compound.txt</code>, <code>core_hull_in_cycle.py</code>. See it in the app: Kaleidohedra, 3D+ → Vajrayana (its core and hull are stations) and Multi-shell chains.</p>
''')
P['ocd-stella'] = dict(title='The DICTO OCD Stella', sub="The Ogdoecontahedron's companion cut along its joints: a golden solid that fills 151/2 − 267√5/8 ≈ 87.12% of space in the Ogdoecontahedron's packing, copies meeting face to face",
  parent='The DICTO Ogdoecontahedron, DICTO DOI: 10.5281/zenodo.23404688',
  credit="""The companion ("a free gift from the way the adapters sat on the OCD"), the stella cut, the seed and the name are DICTO's; the exact computations and the text were done with an AI assistant (Claude, Anthropic).""",
  body='''<div class="abstract"><b>Abstract.</b> The DICTO Ogdoecontahedron (OCD) packs in a body-centred cubic arrangement, each copy joined to 8 neighbours on hexagons. The golden adapter pieces around one copy have an icosahedral hull, the OCD's companion C (72 corners: 30 hexagons in golden planes and 20 triangles). Cutting C along the 8 joints gives the DICTO OCD Stella S: 48 corners and 50 faces, golden except for the joint triangles, which are exactly the packing cell's hexagon walls. Copies of S meet face to face across all 8 joints and fill exactly 151/2 − 267√5/8 ≈ 87.12% of space. Twelve OCD Stellas around one small one fill an outer OCD Stella exactly at φ², the Bodhi seed's pattern, though S is only pyritohedral. Exact in ℚ(√5) unless marked float.</div>

<figure><div class="figs two"><img src="figures/ocd-stella-solid.jpg"><img src="figures/ocd-stella-pack.jpg"></div>
<figcaption><b>Figure 1.</b> Left: the DICTO OCD Stella. Right: copies in the OCD's packing, meeting face to face across the joints.</figcaption></figure>

<h2>1. The solid</h2>
<p>Around one OCD of its packing (cell volume 512/729 + 256√5/729), the 60 golden adapter pieces (the full orbit of the 24 per cell) have a convex hull C with 72 corners, 30 hexagons in the golden planes of the OCD's envelope and 20 triangles in the three-fold planes through the adapters' outer corners (squared distance 14/27 − 10√5/243), volume (−18880 + 9760√5)/2187. Its combinatorial type is Conway t3jD, the triacontahedron truncated at its 20 three-fold corners, here at the depth set by the OCD (Antiprism). The DICTO OCD Stella is S = C cut by the packing's Voronoi cell, that is, along the 8 joints.</p>
<table><tr><th>Property</th><th>Value (exact)</th></tr>
<tr><td>corners, faces</td><td>48 corners; 50 faces: 6 golden hexagons, 24 golden quadrilaterals, 12 triangles of C, 8 triangles in the OCD's joint hexagon planes (the cell's hexagon walls)</td></tr>
<tr><td>volume</td><td>(−4064 + 2240√5)/729 ≈ 1.296011</td></tr>
<tr><td>packing</td><td>fills 151/2 − 267√5/8 ≈ 87.12% of space in the OCD's packing; copies meet face to face across the 8 joints</td></tr>
<tr><td>symmetry</td><td>pyritohedral (the cut keeps the 24 symmetries the OCD shares with the cubic packing)</td></tr></table>
<p class="cap"><b>Table 1.</b> The DICTO OCD Stella (<code>stella_cut_exact.py</code> → <code>stella-cut-exact.txt</code>).</p>

<h2>2. The seed and the crystals</h2>
<p><b>The seed (exact).</b> An outer OCD Stella of scale φ² holds 12 OCD Stellas on its five-fold axes, each touching it, and one of scale 1/φ at the centre touching all 12. By the Minkowski argument the seed closes exactly when no two of the twelve overlap; of the 66 pairs, 30 have gauge exactly 1 (touching, each copy 5 others, along the icosahedron's edges) and 36 exactly φ. So it closes exactly at φ² with the centre at 1/φ, and the gap is −69 + 31√5 ≈ 31.8%: the pattern of the Bodhi Seed (DICTO DOI: 10.5281/zenodo.23311353), though the OCD Stella is only pyritohedral (<code>stella_seed_exact.py</code>).</p>
<p><b>Crystals.</b> On one network of the OCD's packing with a partner on the other: with icosahedra in the OCD's 20 hexagon planes, every solid meets its 8 joint neighbours face to face and the fill is 1523/32 − 669√5/32 ≈ 84.60% (exact); with regular octahedra, ≈ 96.33% (float); alone on both networks, 87.12% (exact). With icosahedra or octahedra the crystal has space group Fd-3 (No. 203).</p>

<h2>3. Status</h2>

<p><b>Known:</b> the combinatorial type of C (Conway t3jD, the chamfered icosahedron) and a related golden space-filler cut from the rhombic triacontahedron on a body-centred cubic lattice (Kabai, below). <b>Not found, in the sources checked:</b> the OCD Stella, its 87.12% packing, and its seed. Every "not found" is limited to the sources listed here and in the Appendix.</p>
<p><b>Sources checked on the web (17 October 2026):</b></p><ul><li><b>Related and known: S. Kabai, "54-Faced Space-Filling Polyhedron"</b> (Wolfram Demonstrations Project): a rhombic triacontahedron with 8 half oblate golden rhombohedra removed at the corners of an inscribed cube, 6 golden rhombi and 48 triangles, filling space with its centres on a body-centred cubic lattice. A golden solid cut from the triacontahedron to pack on bcc is therefore known; the OCD Stella is a different solid (48 corners, 50 faces with golden hexagons and quadrilaterals, cut by the packing's Voronoi cell) and fills 87.12%, not all, of space.</li><li><b>Wikipedia</b>, "Chamfer (geometry)": the chamfered icosahedron (tritruncated rhombic triacontahedron), its equilateral form; no packing and no cut by a cubic cell.</li><li><b>Klitzing</b>, "chike" (the truncated rhombic triacontahedron); <b>McCooey</b>, Chamfered Solids (no chamfered-icosahedron packing).</li><li><b>Web search</b> for the packing fraction 151/2 − 267√5/8 ≈ 87.12% and for the name: no results.</li></ul>
<p><b>Polyhedron software libraries (17 October 2026):</b></p><ul><li><b>SageMath</b> polytope library (<code>polytopes.*</code>): its icosahedral constructors are the icosahedron, dodecahedron, icosidodecahedron, truncated icosahedron and the other Archimedean solids, and the pentakis dodecahedron; none of the solids here.</li><li><b>netlib polyhedra database</b> (142 entries: Platonic, Archimedean and their duals, prisms, the 92 Johnson solids and five others): none of the solids here (the pentakis dodecahedron, file 41, is the canonical one).</li><li><b>Antiprism</b> 0.29 (A. Rossiter): used to recompute and check the structures independently (for Vajrayana and Progenitors, and the companion's type t3jD); its Conway-operator sweep is a generator, not a catalogue.</li><li><b>Not run:</b> Wolfram <code>PolyhedronData</code> (needs Mathematica) and Stella / Great Stella (R. Webb; its library beyond the uniform, Johnson and Stewart-toroid models is not listed online). No claim is made about them.</li></ul>
<p>The reference library: see the Appendix.</p>

<h2>4. Files</h2>
<p>In the study (branch research: studies/2026-10-16-ocd-pyrochlore): <code>stella_cut_exact.py</code> → <code>stella-cut-exact.txt</code>, <code>stella_seed_exact.py</code> → <code>stella-seed-exact.txt</code>, <code>ocd_gbpc_hull.py</code>, <code>companion_variants.py</code>. See it in the app: Kaleidohedra, 3D+ → OCD Stella Crystals.</p>
''')
for k, p in P.items():
    p['doi'] = DOI[k]
    p['version'] = 'Version 2 · 17 October 2026 (figure re-rendered with solid cut faces)' if k == 'metaxy' else 'Version 1 · 17 October 2026'
    html = HEAD.format(**p) + p['body'] + open('appendix-library.html').read() + TAIL
    open(os.path.join(k, 'paper.html'), 'w').write(html); print(k, len(html.split()))
