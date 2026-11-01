# DICTO Vacuus Solids: the typeset study note (HTML for print.mjs) from data/vacuus-census.json and renders/*.png.
# Usage: typeset.py <study dir> <out dir>   (then: node print.mjs <out dir name> dicto-vacuus-solids.pdf)
import json, html, os, shutil, sys, math
ST, OUT = sys.argv[1:3]; os.makedirs(OUT + '/plates', exist_ok=True)
C = json.load(open(os.path.join(ST, 'data/vacuus-census.json'))); R = C['rows']
def short(n):
    n = n.replace('DICTO ', '').split(' (')[0]
    return {'Truncated-Icosahedral Hecatodihedron': 'Hecatodihedron'}.get(n, n)
E = html.escape
def flags(r):
    f = []
    if not r['well_defined']: f.append(f'<b>not defined</b> ({r["faces_O_not_inside"]} faces)')
    if r['all_congruent']: f.append('<b>isofin</b>')
    if r['central_discs']: f.append('disc ' + ', '.join(f'{v}×{k}-gon' for k, v in r['central_discs'].items()))
    if r['apex_rational']: f.append('apex ' + ', '.join(x + 'π' if x != '1' else 'π' for x in r['apex_rational']) + ('' if r['exact'] else ' (float)'))
    if r['right']: f.append('right ∠ at ' + '/'.join(sorted({a for a, _ in r['right']})))
    if r['accidental']: f.append(f'acc. {r["fin_classes"]}&lt;{r["fin_orbits"]}')
    if r['convex'] is False and r['well_defined']: f.append('non-convex')
    return '; '.join(f)
def row(r):
    ap = r['apex_deg']; aps = f'{ap[0]:.2f}' if len(ap) == 1 else f'{ap[0]:.2f}–{ap[-1]:.2f}'
    fld = {'Q': 'Q', 'Q(sqrt(5))': 'Q(√5)', 'Q(sqrt(2))': 'Q(√2)', 'Q(sqrt(3))': 'Q(√3)'}.get(r['field'], 'float')
    bld = ' class=b' if r['strut_lengths'] <= 2 else ''
    return (f"<tr><td>{E(short(r['name']))}</td><td>{E(r['D'] or '')}</td><td>{fld}</td><td class=n>{r['E']}</td><td class=n>{r['fin_classes']}/{r['fin_orbits']}</td>"
            f"<td class=n>{aps}</td><td class=n>{r['flat_sheets']}</td><td class=n>{r['V']}</td><td class=n{bld}>{r['strut_lengths']}</td><td class=n>{r['edge_lengths']}</td>"
            f"<td class=n>{r['frame_lengths']}</td><td>{flags(r)}</td></tr>")
fams = [('Platonic', 'Platonic solids'), ('Archimedean', 'Archimedean solids'), ('Catalan', 'Catalan solids'), ('DICTO Solids v7', 'DICTO Solids v7')]
HEAD = '<thead><tr><th>Solid</th><th>D</th><th>Field</th><th class=n>Fins</th><th class=n>Shapes/orb.</th><th class=n>Apex °</th><th class=n>Sheets</th><th class=n>Struts</th><th class=n>Strut L</th><th class=n>Edge L</th><th class=n>Frame L</th><th>Flags</th></tr></thead>'
tables = ''
for fam, title in fams:
    tables += f'<table>{HEAD}<tbody><tr class=sec><td colspan=12>{title}</td></tr>' + ''.join(row(r) for r in R if r['family'] == fam) + '</tbody></table>'
by = {r['src'][:-5]: r for r in R}
PL = [('tetrahedron', 'Tetrahedron'), ('cube', 'Cube'), ('octahedron', 'Octahedron'), ('dodecahedron', 'Dodecahedron'), ('icosahedron', 'Icosahedron'),
      ('dicto-ogdoecontahedron', 'OG (D28)'), ('dicto-shadow-17', 'Kagemusha (D86)'), ('dicto-ti-star-core', 'TI Star core'), ('dicto-cube-pearl', 'Cube Pearl'),
      ('dicto-golden-clasp', 'Golden Clasp'), ('dicto-hamlet', 'Hamlet'), ('dicto-hecatodihedron', 'DICTO Hecatodihedron'), ('dicto-ocd-stella', 'OCD Stella'),
      ('dicto-gti', 'DICTO GTI'), ('dicto-lion', 'Lion'), ('dicto-dbt', 'DBT'), ('dicto-ott', 'DICTO OTT'), ('dicto-star-halo', 'Star Halo')]
def sw(c): return f'<span class=sw style="background:{c}"></span>'
plates = ''
for slug, nm in PL:
    r = by[slug]; col = json.load(open(os.path.join(ST, 'renders', slug + '.colours.json')))
    shutil.copy(os.path.join(ST, 'renders', slug + '.png'), OUT + '/plates/' + slug + '.png')
    fins = '; '.join(f"{sw(col['fin_colours'][i])}{c['count']} × apex {c['apex_deg']:.4g}°" + (f" (= {c['apex_rational_pi']}π)" if c['apex_rational_pi'] else '')
                     + (f", right angle at {'the centre' if c['right_angle'] == ['O'] else 'a corner'}" if c['right_angle'] else '') for i, c in enumerate(r['classes'][:8]))
    if len(r['classes']) > 8: fins += f'; … {len(r["classes"]) - 8} more classes'
    st = '; '.join(f"{sw(col['strut_colours'][i])}{s['count']} × {math.sqrt(s['L2']):.4f} R" for i, s in enumerate(r['strut_classes'][:8]))
    if len(r['strut_classes']) > 8: st += f'; … {len(r["strut_classes"]) - 8} more'
    ex = []
    if r['central_discs']: ex.append('central discs: ' + ', '.join(f'{v} × {k} fins' for k, v in r['central_discs'].items()))
    if r['accidental']: ex.append(f'{r["fin_classes"]} fin shapes in {r["fin_orbits"]} symmetry orbits')
    plates += (f'<figure class=pl><img src="plates/{slug}.png"><figcaption><b>{E(nm)}</b> — {r["E"]} fins, {r["V"]} struts. '
               f'Left, SHEETS: {fins}. Right, STRUTS: {st} (R = the longest strut); grey: the solid\'s {r["E"]} edges in {r["edge_lengths"]} length(s)'
               + (f'. {"; ".join(ex)}' if ex else '') + '.</figcaption></figure>')
n_all = len(R); n_dicto = sum(r['family'] == 'DICTO Solids v7' for r in R)
iso = [short(r['name']) for r in R if r['all_congruent']]
one_strut_d = [short(r['name']) for r in R if r['family'] == 'DICTO Solids v7' and r['strut_lengths'] == 1]
two_strut_d = [short(r['name']) for r in R if r['family'] == 'DICTO Solids v7' and r['strut_lengths'] == 2]
frame3_d = [short(r['name']) for r in R if r['family'] == 'DICTO Solids v7' and r['frame_lengths'] <= 3]
acc_d = [f"{short(r['name'])} ({r['fin_classes']}/{r['fin_orbits']})" for r in R if r['family'] == 'DICTO Solids v7' and r['accidental']]
doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>DICTO Vacuus Solids</title><link rel="stylesheet" href="../paper.css">
<style>table{{border-collapse:collapse;font-size:6.6pt;margin:2mm 0;width:100%}} td,th{{border-bottom:1px solid #ddd;padding:0.35mm 0.8mm;text-align:left;vertical-align:top}}
td.n,th.n{{text-align:right}} td.b{{font-weight:bold;color:#7a5c00}} tr.sec td{{font-weight:bold;background:#f3efe2;padding-top:1mm}} thead{{display:table-header-group}} tr{{break-inside:avoid}}
.thm{{border-left:3px solid #b8962e;padding-left:3mm;margin:2.5mm 0}} body,p,li{{font-size:8.6pt;line-height:1.38}} h1{{font-size:18pt}} .logo{{width:22mm}} h2{{font-size:11pt;margin:3.5mm 0 1mm}}
figure.pl{{margin:0 0 4mm;break-inside:avoid}} figure.pl img{{width:100%;display:block}} figure.pl figcaption{{font:7.2pt/1.35 "DejaVu Sans",sans-serif;color:#222}}
.sw{{display:inline-block;width:2.4mm;height:2.4mm;border:0.6px solid #222;margin:0 0.8mm 0 1.2mm;vertical-align:-0.3mm}} .plates{{break-before:page}}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>DICTO Vacuus Solids</h1>
<p class="sub">The centre pyramids of a solid, hollowed out: one fin from the centre to every edge, one strut from the centre to every corner</p>
<div class="meta"><b>DICTO</b> · dictospheres.com · 2 November 2026 · study 2026-11-02-dicto-vacuus (classical.py, vacuus.py, collect.py, render.py) · DICTO Solids v7 + 27 classical solids · study note, not published</div>
<div class="thm"><b>Conclusion.</b> The Vacuus is well defined for {n_all - 1} of the {n_all} solids. The only failure is Lotus Hexa, whose centre lies outside 24 face planes. All fins are congruent (isofin) only for the 5 Platonic solids, the 13 Archimedean solids, the rhombic dodecahedron, the rhombic triacontahedron and Delilah, which is an octahedron. No new DICTO solid is isofin. Among DICTO's new solids, Kagemusha (45°, 72°), Lion (36°), David (90°, 120°) and Lahdeli (90°, float64) have fin apex angles that are rational multiples of π. Lion carries six flat central decagons, and Kagemusha carries one flat central pentagon. {len(one_strut_d)} DICTO solids can be built with struts of one length from the centre. The underlying object is classical: it is the part of the face fan inside the solid, i.e. the cone from O over the edge skeleton. The new parts are DICTO's family, its two built forms (sheets and struts) and this census.</div>
<h2>The idea</h2>
<p>DICTO built a cube from his PET-bottle system B1NR, and the build showed him that a cube is six pyramids. Every solid with a centre O is filled by its centre pyramids, one on each face with apex O. DICTO proposed the <b>DICTO Vacuus</b> of a solid (DICTO, 2 November 2026; the family is the <b>DICTO Vacuus Solids</b>): keep only the interface sheets between neighbouring pyramids and remove the pyramids' outer faces. Two neighbouring pyramids meet in the flat triangle O–A–B over their common edge AB, called the <b>fin</b>. The Vacuus is therefore a star of thin fins, one per edge, radiating from the centre. The fins meet along the <b>struts</b>, the segments from O to the corners. DICTO asked for two views of every Vacuus:</p>
<ul><li><b>SHEETS</b>: the fins;</li><li><b>STRUTS</b>: the frame only, with one strut from O to every corner and, as an option, the solid's own edges (the fins' outer edges). This is the form he builds with bottles and struts (B1NR, DICTOspheres).</li></ul>
<h2>What was computed</h2>
<p>The census covers {n_all} solids: the {n_dicto} solids of DICTO Solids v7 (convex and non-convex) and 27 classical solids. Of these, 5 Platonic, 11 Archimedean and their 11 Catalan duals were generated exactly in Q, Q(√2) and Q(√5) from textbook coordinates, with the Catalan solids taken as exact polar reciprocals. Every hull was checked exactly, and each classical solid was matched against krp-core's registry. The two snub solids and their duals come from krp-core in float64. O is the corner centroid. For each solid we computed:</p>
<ul>
<li><b>Fins:</b> the squared sides |OA|², |OB|², |AB|², the apex angle AOB and any right angle, at O, A or B. Congruence classes are exact. Symmetry orbits use the orthogonal maps of the corner set, to 10<sup>−7</sup>.</li>
<li><b>Wedges:</b> the dihedral angle between two neighbouring fins along a strut, inside one pyramid. This is the angle of the face's central projection at that corner. Around a strut the wedges sum to 2π, and around a pyramid they sum to (n−2)π plus the pyramid's solid angle. Both sums were checked for every solid (largest error 1.2·10<sup>−13</sup>; Lotus Hexa excepted).</li>
<li><b>Flat sheets:</b> fins that share a strut and lie in one plane join into one sheet. A sheet that closes all the way round O is a <b>central disc</b>, a flat central polygon of the solid.</li>
<li><b>Struts:</b> the number of struts (= corners), their exact length classes, the edge-length classes and the total number of lengths in the frame (centre struts + edges).</li>
<li><b>Rational multiples of π</b> were tested exactly. If cos 2θ lies in a quadratic field, θ/π is rational only when cos 2θ is one of 0, ±½, ±1, (±1±√5)/4, ±√2/2 or ±√3/2 (denominators 1–6, 8, 10, 12), so the test is an exact field comparison. For the float64 solids (Delilah, Samson, Lahdeli, Sonsam and the snubs) it is a numerical test to 10<sup>−9</sup>.</li>
</ul>
<h2>Theorems</h2>
<div class="thm"><b>Theorem 1 (when the Vacuus exists).</b> Let P be a closed, oriented polyhedral surface around O. The centre pyramids fill P without overlap, and the fins are exactly the interfaces between them, if and only if O lies strictly on the inner side of every face plane. <i>Proof.</i> Each face with O strictly inside its plane is crossed positively by the rays from O through it. The winding number of the surface about O is 1, so every ray crosses it exactly once. Conversely, if O lies on or beyond a face plane, that pyramid is flat or inverted, so the pyramids do not fill P cleanly. □ This holds for {n_all - 1} of the {n_all} solids, including 7 non-convex ones: DICTO Jewel, Dodecaxes, Golden TI Star, Icosaxes Hexa, Kagemusha, Keyaxes and Lotus Jewel Axes. It fails only for Lotus Hexa (24 faces).</div>
<div class="thm"><b>Theorem 2 (isofin).</b> All fins are congruent if and only if every edge has the same length and the same pair of strut lengths {{|OA|, |OB|}} at its ends. This happens when all struts are equal and all edges are equal (Platonic and Archimedean solids), or when the edges join two strut lengths in a fixed way (rhombic dodecahedron, rhombic triacontahedron). In the census the isofin Vacuus are those of: {", ".join(iso)}. <i>Proof.</i> Triangles are congruent by SSS, and O is the common apex. □</div>
<div class="thm"><b>Theorem 3 (polar pairs).</b> Let P* be the polar reciprocal of P about O. Then (a) the apex angle of the fin of the dual edge e* is π minus the dihedral angle of P at e; (b) for convex P, the wedges of P* are π minus the face angles of P; (c) the fin of e and the fin of e* lie in perpendicular planes, which meet along the line from O through the foot of the perpendicular from O to e. These follow from the classical fact that the face fan of P is the normal fan of P*: the corners of the fin of e* are the poles of the two faces at e, i.e. their outward normals. <i>Check:</i> over the 92 convex solids, the largest error was 4.4·10<sup>−16</sup> for (a), 3.5·10<sup>−10</sup> for (b) and 2.0·10<sup>−10</sup> (|cos|) for (c). (a) and (c) also hold for the 7 non-convex well-defined solids. A solid and its dual therefore share no fin shapes; what they share is the angles of (a) and (b) and the crossed pairs of fins in (c). For example, the cube's dihedral angle of 90° becomes the octahedron's 90° fin apex, and the rhombic triacontahedron's dihedral angle of 144° becomes the icosidodecahedron's 36° fin apex.</div>
<h2>Findings</h2>
<ul>
<li><b>Same Vacuus.</b> Two pairs of solids share a fin multiset up to similarity. Octahedron = Delilah, because Delilah is an octahedron. FPD = Palintriacontahedron: these are the same shape held as two entries in DICTO Solids v7, as the halo census already flagged. DBT and DICTO OTT share their two fin shapes (apex 37.38°, the rhombic triacontahedron's fin, and apex 63.43°) but in different counts: 54 + 6 and 36 + 24. Both are cut from the rhombic triacontahedron.</li>
<li><b>Rational apex angles</b> (exact, π multiples). In classical solids: octahedron ½, cuboctahedron ⅓, icosidodecahedron ⅕, deltoidal icositetrahedron and disdyakis dodecahedron ¼, triakis octahedron ½. In DICTO solids: <b>Kagemusha</b> ¼ and ⅖ (10 fins of 45°, 5 fins of 72°), <b>Lion</b> ⅕ (60 fins of 36°), <b>David</b> ½ and ⅔, and Delilah ½. Lahdeli has 90° fins, but it lies in Q(t), so this result is float64 only. By Theorem 3(a), every rational apex angle in P* is a rational dihedral angle of P.</li>
<li><b>Rational wedges</b> are common: {sum(1 for r in R if r['wedge_rational'])} solids have at least one. Most are forced, because a strut with k equal wedges has wedges of 2π/k. For the Catalan solids, Theorem 3(b) gives π minus the regular face angles of the Archimedean solids.</li>
<li><b>Central discs</b> (a flat sheet that closes round O): octahedron (3 squares), cuboctahedron (4 hexagons), icosidodecahedron (6 decagons), deltoidal icositetrahedron (3 octagons), disdyakis dodecahedron (9 octagons), disdyakis triacontahedron (15 dodecagons), tetrakis hexahedron (6 hexagons), triakis octahedron (3 squares), Delilah. Among DICTO's new solids: <b>Lion</b>, with 6 central decagons (like the icosidodecahedron, in whose great decagons its 36° fins lie), and <b>Kagemusha</b>, with one central regular pentagon made of its five 72° fins.</li>
<li><b>Right-triangle fins.</b> These are fins of the OG (60 of 180, right angle at a corner, apex 16.47°), DICTO Jewel (24 of 96, at a corner, apex 54.74° = arctan √2), DICTO TQHD (60, at a corner, apex 1.84°), ED F18 (2), David (2, at O), Lahdeli (12, float64) and Lotus Hexa (48). Among the classical solids: octahedron and triakis octahedron (right angle at O).</li>
<li><b>Fins congruent across symmetry orbits</b> (fewer fin shapes than orbits) occur in all the non-quasiregular Archimedean solids and in these DICTO solids: {", ".join(acc_d)}.</li>
<li><b>Buildability (STRUTS).</b> DICTO solids whose centre struts all have one length: {", ".join(one_strut_d)}. With two lengths: {", ".join(two_strut_d)}. DICTO solids whose whole frame (centre struts + edges) uses at most three lengths: {", ".join(frame3_d)}. The cuboctahedron is the only solid in the census whose whole frame has a single length: struts = edges, Fuller's vector equilibrium.</li>
</ul>
<p><b>Placeholder names</b> (given now, for DICTO to confirm): <b>Isofin Vacuus</b> (all fins congruent); <b>Disc Vacuus</b> (contains a central disc, e.g. the Lion Disc Vacuus and the Kagemusha Pentagon Disc); <b>One-Strut Vacuus</b> (all centre struts one length, i.e. corners on one sphere about O).</p>
<h2>Prior art</h2>
<ul>
<li><b>Leonardo's vacuus solids.</b> In Pacioli's <i>De divina proportione</i> (1509), Leonardo da Vinci drew each body twice, <i>solidus</i> and <i>vacuus</i>. The vacuus form is an open frame of the faces' edges, a hollowed edge skeleton (e.g. “Octocedron planus vacuus”, “Duodecedron … vacuus”, “Septuaginta duarum basium vacuus”). It has no centre and no sheets or struts to the centre. DICTO's name continues Leonardo's word for a different hollowing: the solid is emptied down to the interfaces of its centre pyramids.</li>
<li><b>Face fan and the cone over the skeleton.</b> In polytope theory the <i>face fan</i> of a polytope with O inside is the set of cones from O over its faces, and it is the normal fan of the dual. Its two-dimensional cones are the cones over the edges. The Vacuus is exactly these cones cut off at the surface, i.e. the cone from O over the edge skeleton. As a mathematical object it is therefore classical, and so are the polar facts of Theorem 3. The dissection of a solid into face pyramids from an interior point is also classical (the volume formula V = ⅓ Σ area × height).</li>
<li><b>Excavated polyhedra</b> (Wenninger, <i>Polyhedron Models</i>, W28 excavated dodecahedron) are solids with pyramidal pits cut into the faces. They are closed solids, not fans of centre sheets.</li>
<li>No source found treats the fan of centre-to-edge triangles, or the centre struts with the edges, as a family of built or sculptural solids. No source has catalogued its fin shapes, wedges, central discs or strut lengths, for the classical solids or for DICTO's. The new parts are DICTO's family and its two built forms, and this census over DICTO Solids v7.</li>
</ul>
<p><b>Sources checked</b> (2 November 2026):</p>
<ul>
<li><i>Reference library</i> (ask-library, top 5 + page hits per query). Six queries: “Leonardo da Vinci vacuus open solids Pacioli De divina proportione”, “central dissection of a polyhedron into pyramids from the centre over the faces”, “cone over the edge skeleton of a polytope, triangles from centre to edges”, “face fan of a polytope, polyhedral fan, normal fan”, “excavated polyhedra Wenninger” and “planes through the centre and each edge of a polyhedron, central projection onto the sphere, spherical tiling”. They returned Pacioli 1509 (Divina proportione; pp. 9, 40, 76), Kepler 1619 (Harmonices mundi; pp. 51, 55, 64, 271), Apple Peel Unfolding of Archimedean and Catalan Solids, An Etruscan Dodecahedron, Ordine privo di periodicità, Hexagons and the golden ratio, Polar Zonohedra Edge-Unfold to Nets, On Folding a Polygon to a Polyhedron, Hynd 2023 (Reuleaux polyhedron), An almost trivial observation about the icosahedron, Extremal properties for dissections of convex 3-polytopes, Goldberg 1937, Grünbaum 2010 (Bilinski dodecahedron), Internal and external duality in abstract polytopes, The canonical form, scissors congruence and adjoint degrees of polytopes, On Delaunay's classification theorem, A new method for generalizing non-self-intersecting flexible polyhedra, Bianchi–Doná–Speziale 2011, Erdahl–Rybnikov 2001, Betke–Henk 2000, Integral Planes and Unit-Norm Polytopes, The orthogonal connectedness of polyhedral surfaces, Perfect and almost perfect homogeneous polytopes, Alexeev 2002, Garber–Gavrilyuk–Magazinov 2012, Polyhedron Models (Wenninger), Convex polyhedra with regular faces (Johnson 1966), Wikipedia Goldberg polyhedron, Wikipedia Tetrahedral-octahedral honeycomb, Two-orbit convex polytopes and tilings, Platonic solids, Archimedean solids and semi-equivelar maps on the sphere, Random hyperbolic polyhedra in horoballs, Tropical balls, geodesics and honeycomb, Characterization and Construction of a Family of Highly Symmetric Spherical Polyhedra, Cutler–Schulte 2011, Bezdek et al. 2007 (Ball-polyhedra), Koca et al. 2020 and Fedorov 1885 ch. 13. None describes the centre-to-edge fins as a solid or object.</li>
<li><i>Web</i> (four searches): “Leonardo da Vinci vacuus solids Pacioli De divina proportione open faces skeleton”. It found Wikipedia “Divina proportione”, Leonardo-online (MPIWG, book 86), Matemáticas Visuales (Leonardo's octahedron, dodecahedron and septuaginta pages), CityU Hong Kong “da Vinci session 1”, Nexus Network Journal (Monza models, fig. 7) and Redalyc 607973000008. The search on polyhedron triangles from the centre to each edge (central dissection / cone over edges) found arXiv:1909.02874, 2303.09702, 2307.06017 and 2209.08919, US patents 8,599,195, 11,697,058 and 4,608,653, the Bentley MicroStation polyhedron tool and a Domerama geodesic glossary. The search on the face fan and pyramidal decomposition found arXiv:2511.04322 (face fan = normal fan of the dual), the Macaulay2 Polyhedra/faceFan documentation and the OSCAR polyhedral fans documentation. The search on Wenninger and excavated polyhedra found Wikipedia “Excavated dodecahedron”, “List of Wenninger polyhedron models” and “Magnus Wenninger”, EPFL graphsearch, the Science Museum Group polyhedra-model drawings and Imaginary “Polyhedron Models”.</li>
</ul>
<p>“New” here means new only within these checks.</p>
<h2>Table 1. The Vacuus of {n_all} solids</h2>
<p>The columns are: fins (= edges); fin shapes / symmetry orbits; apex angles (range, °); flat sheets; struts (= corners); centre-strut lengths (bold if 1 or 2: easiest to build); edge lengths; frame lengths (struts + edges, distinct). Flags: isofin = all fins congruent; disc = central discs; apex = rational multiples of π; right ∠ = right-triangle fins; acc. = fin shapes &lt; orbits (congruent across orbits); not defined = Theorem 1 fails. Exact values (squared sides, cos 2θ, strut lengths) are in data/vacuus-census.json.</p>
{tables}
<div class=plates><h2>Plates</h2>
<p>Each plate shows two views of one Vacuus, both inside a translucent ghost of the solid. Left, SHEETS: the fins, coloured by shape (legend in the caption). Each face appears as a hollow pyramid opening towards the centre. Right, STRUTS: rods from the centre (dark ball) to every corner, coloured by length, with the solid's edges as thin grey rods. The views are orthographic, with elevation 20° and azimuth 24°. The renderer is a z-buffer, so hidden surfaces are drawn correctly, and edges are at least 2 px at 300 dpi. Cleo is a piece, not a solid of DICTO Solids v7, so it has no plate.</p>
{plates}</div>
</body></html>'''
open(OUT + '/paper.html', 'w').write(doc); print(len(doc))
