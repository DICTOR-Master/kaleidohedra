# DICTO Vacuus origami: the overview note (HTML for print.mjs) from data/*.json (fan.py), nets/*.json (nets.py) and renders/*.png.
# Usage: typeset.py <work dir> <out dir>   (then: node print.mjs <out dir name> vacuus-origami.pdf "<short title>" "study note" "2026-11-02")
import json, html, os, shutil, sys, math
WD, OUT = sys.argv[1:3]; os.makedirs(OUT + '/plates', exist_ok=True); E = html.escape
SOL = [('cube', 'cube', 'Cube'), ('cuboctahedron', 'cuboctahedron', 'Cuboctahedron'), ('dicto-david', 'david', 'David'),
       ('dicto-shadow-17', 'kagemusha', 'Kagemusha (D86)'), ('dicto-cube-pearl', 'cube-pearl', 'Cube Pearl'),
       ('dicto-golden-clasp', 'golden-clasp', 'Golden Clasp'), ('dicto-ti-star-core', 'ti-star-core', 'TI Star core')]
D = {}
for slug, short, nm in SOL:
    D[slug] = (json.load(open(f'{WD}/data/{slug}.json')), json.load(open(f'{WD}/nets/vacuus-origami-nets-{short}.json')))
    shutil.copy(f'{WD}/renders/{slug}.png', f'{OUT}/plates/{slug}.png')
def sq(x):
    if x is None: return 'float'
    return x.replace('*sqrt(5)', '√5').replace('(-', '(−').replace(' + (−', ' − (').replace('sqrt', '√')
def deg(x): return f'{math.degrees(x):.2f}°'
rows = ''; fold_worst = 0; close_worst = 0
for slug, short, nm in SOL:
    r, n = D[slug]; fold_worst = max(fold_worst, r['checks']['fold_err']); close_worst = max(close_worst, r['checks']['closure_err'])
    types = '; '.join(f"{t['name']} {t['face']} ×{t['count']}" for t in r['types'])
    sums = ', '.join(f"{t['fan_sum_deg']:.2f}°" for t in r['types'])
    psis = ', '.join('/'.join(sorted({f'{math.degrees(p):.2f}' for p in t['psi']})) for t in r['types'])
    fl = {'Q': 'Q', 'Q(sqrt(5))': 'Q(√5)'}.get(r['field'], r['field'])
    rows += (f"<tr><td>{E(nm)}</td><td>{fl}</td><td class=n>{r['F']}</td><td class=n>{2 * r['E']}</td><td>{types}</td><td class=n>{sums}</td><td class=n>{psis}</td>"
             f"<td class=n>{n['longest_strut_mm']}</td><td class=n>{2 * max(s[1] for s in n['struts_mm']):.0f}</td><td class=n>{n['pages']}</td>"
             f"<td class=n>{r['checks']['closure_err']:.0e}</td></tr>")
exact_rows = ''
for slug, short, nm in SOL:
    r, n = D[slug]
    fins = '<br>'.join(f"<b>{f['letter']}</b> ×{f['count']}: |OA|² = {sq(f['OA2_exact'])}, |OB|² = {sq(f['OB2_exact'])}, |AB|² = {sq(f['AB2_exact'])}; apex {f['apex_deg']:.4f}°"
                       + (' (central disc)' if f['disc'] else '') for f in r['fins'])
    folds = '<br>'.join(f"{t['name']}: " + ', '.join(sorted({f"cos²ψ = {sq(c)} (cos ψ {'&lt;' if s_ < 0 else '&gt;' if s_ > 0 else '='} 0), ψ = {math.degrees(p):.4f}°"
                                                         for c, s_, p in zip(t['cos2psi_exact'], t['sign_cos_psi'], t['psi'])})) for t in r['types'])
    exact_rows += f'<tr><td>{E(nm)}</td><td>{fins}</td><td>{folds}</td></tr>'
plates = ''
CAP = {'cube': 'Six identical square fans (four triangles, fan angle 282.12°, every fold ψ = 120° exactly).',
       'cuboctahedron': 'Eight triangle fans and six square fans; every fin has apex 60°, and all 24 fins lie in the four central hexagons.',
       'dicto-david': 'Four fans of fan angle 330° (exact): the flattest open pyramids of the set; fins of 120° and 90° (exact).',
       'dicto-shadow-17': 'Three net types of ten; the five 72° fins (exact) form the central regular pentagon, each a double wall between a pyramid above and one below.',
       'dicto-cube-pearl': '',
       'dicto-golden-clasp': 'Twelve quadrilateral, eight hexagon and six octagon fans; one strut length; fins b and c differ by 0.1 mm at this scale, so keep the letters apart.',
       'dicto-ti-star-core': 'Twelve regular-pentagon fans and twenty hexagon fans; one strut length.'}
CAP['dicto-cube-pearl'] = 'Six slender square fans (fan angle 88.77°) and twelve hexagon fans; all 32 struts have one length.'
for slug, short, nm in SOL:
    r, n = D[slug]
    plates += (f'<figure class=pl><img src="plates/{slug}.png"><figcaption><b>{E(nm)}</b>: {r["F"]} open pyramids, {2 * r["E"]} paper triangles, {r["E"]} double-walled fins. '
               f'{CAP[slug]} Left: folded (the gap between the two walls of each fin is drawn at 0.8 % of the longest strut so that both walls show at the rim). '
               f'Right: exploded, each open pyramid pulled out along its axis. Nets: vacuus-origami-nets-{short}.pdf ({n["pages"]} pages, longest strut {n["longest_strut_mm"]} mm).</figcaption></figure>')
doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>DICTO Vacuus origami</title><link rel="stylesheet" href="../paper.css">
<style>table{{border-collapse:collapse;font-size:6.8pt;margin:2mm 0;width:100%}} td,th{{border-bottom:1px solid #ddd;padding:0.4mm 0.8mm;text-align:left;vertical-align:top}}
td.n,th.n{{text-align:right}} thead{{display:table-header-group}} tr{{break-inside:avoid}}
.thm{{border-left:3px solid #b8962e;padding-left:3mm;margin:2.5mm 0}} body,p,li{{font-size:8.6pt;line-height:1.4}} h1{{font-size:18pt}} .logo{{width:22mm}} h2{{font-size:11pt;margin:3.5mm 0 1mm}}
figure.pl{{margin:0 0 4mm;break-inside:avoid}} figure.pl img{{width:100%;display:block}} figure.pl figcaption{{font:7.2pt/1.35 "DejaVu Sans",sans-serif;color:#222}}
table.ex td{{font-size:6.3pt}} .plates{{break-before:page}}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>DICTO Vacuus origami</h1>
<p class="sub">The DICTO Vacuus folded in paper: one open pyramid per face, nested at the centre, every fin a double wall</p>
<div class="meta"><b>DICTO</b> · dictospheres.com · 2 November 2026 · study 2026-11-02-vacuus-origami (fan.py, nets.py, render.py) · follows study 2026-11-02-dicto-vacuus · study note, not published</div>
<div class="thm"><b>Conclusion.</b> Every Vacuus whose centre lies strictly inside all face planes folds as modular origami from one flat fan per face. The seven
solids here (cube, cuboctahedron, David, Kagemusha, Cube Pearl, Golden Clasp, TI Star core) need 1 to 3 distinct nets each, with fan angles from 88.77° to 330°.
Folded by the computed dihedrals, every net returns to its true pyramid to within {max(fold_worst, close_worst):.0e} of the longest strut, so the nets close up.
Fold the <b>cube</b> first: six copies of one net, four triangles, every fold 120°.</div>
<h2>The idea</h2>
<p>The DICTO Vacuus of a solid (study 2026-11-02-dicto-vacuus) is the set of fins O–A–B, one for every edge AB, where O is the corner centroid.
On 2 November 2026 DICTO proposed making the Vacuus solids as <b>modular origami</b>. One sheet cannot fold the whole Vacuus, because three or more fins
meet along every strut O–v, and a folded sheet carries at most two faces along a crease. The open centre pyramid of one face does fold from one sheet. It has no base, and it is a fan of
triangles O–v<sub>k</sub>–v<sub>k+1</sub>, one per face edge, with its apex at O. When all the open pyramids are nested with their apices at O, the two pyramids
on the two sides of an edge meet back to back along the fin of that edge, so <b>every fin becomes a double wall</b>. The open faces point outwards, so
one looks into each pyramid from outside.</p>
<h2>Method</h2>
<ul>
<li><b>Fan geometry</b> (fan.py). For each face, with its corners counter-clockwise seen from outside: the strut lengths |Ov<sub>k</sub>|, the rim edges
|v<sub>k</sub>v<sub>k+1</sub>| and the fan angles θ<sub>k</sub> (the fin apex angles). Squared lengths and cos²θ are exact in Q or Q(√5), from the exact corners
of DICTO Solids v7 and the classical coordinates of the census. The flat net lays the triangles side by side around O, so the fan angle is Σθ<sub>k</sub>.</li>
<li><b>Fold angles.</b> At each strut the fold dihedral ψ<sub>k</sub> is the angle between the two neighbouring triangles inside the pyramid, given as exact cos²ψ with the sign of cos ψ.
All folds of these seven solids are valley folds seen from the printed side (all ψ &lt; 180°). The printed side is the inside of the open pyramid.</li>
<li><b>Net types.</b> Faces get the same net when their fans agree as cyclic sequences of (strut class, fin letter, neighbouring net type), read
counter-clockwise on the printed side, with the partition refined until stable. A sequence read clockwise would give a mirror net. None occurs here: every net type is its own mirror up to rotation.</li>
<li><b>Tab rule</b> (nets.py). Every fan triangle O–A–B, with A→B counter-clockwise on the printed side, carries a <b>rim half-tab</b> on the half of AB next to B.
The neighbouring pyramid runs the same edge B→A, so its half-tab lies on the other half. Each rim gets exactly two half-tabs, one from each pyramid of
the fin pair. Each folds 180° over the double rim (mountain) onto the neighbour's printed side. The rule depends only on orientation, so pyramids related
by a rotation get identical nets. One <b>seam tab</b> per fan, on the free strut edge of the last triangle, is glued under triangle 1 and closes the fan.
The fins themselves are glued back to back over their whole area.</li>
<li><b>Scale.</b> One true scale per solid: the largest net, tabs included, fills the printable area of A4 (186 × 249 mm). The scale is then rounded down so that the longest strut is a whole number of millimetres.
Each PDF holds every copy needed, so it is printed once at 100 %. A 50 mm bar on every sheet checks the print scale.</li>
<li><b>Labels.</b> Each triangle carries its fin letter and the net type behind it (the other wall). Rim corners carry the strut class, folds carry ψ, and each tab names its target.
Page 1 of each nets PDF is the assembly guide. The DICTO mark is on every sheet.</li>
</ul>
<h2>Checks</h2>
<ul>
<li><b>Flat:</b> every fan angle is &lt; 360° (largest: David, 330°). For a convex face with O strictly inside its plane, the cone from O over the face is a convex
cone, and the face angles at the apex of a convex polyhedral cone sum to less than 2π. Every net of a well-defined Vacuus with convex faces therefore lies flat without overlap.</li>
<li><b>Closes up:</b> each flat net was folded about its struts by the computed ψ, one triangle after another, and compared with the true corners of every face of
that type after a rigid motion. Largest deviation: {fold_worst:.1e} of the longest strut. Largest gap between the last strut and the first: {close_worst:.1e}. Largest
rim-edge error in the flat net against the exact |AB|²: {max(D[s][0]['checks']['side_err'] for s, _, _ in SOL):.0e}.</li>
<li><b>Counts:</b> Σ(face sides) = 2E for every solid, so the nested fans cover each fin exactly twice (one double wall per edge), and there are 2E half-tabs.</li>
<li><b>Cutting:</b> no two pieces of a net overlap (triangles, rim tabs and seam tab, checked with shapely to 10<sup>−6</sup> mm²). Every net is one piece and fits its page.
Every page of the seven nets PDFs (137 pages) was looked at.</li>
</ul>
<h2>Table 1. The seven solids</h2>
<table><thead><tr><th>Solid</th><th>Field</th><th class=n>Pyramids</th><th class=n>Triangles</th><th>Net types</th><th class=n>Fan angles</th><th class=n>Folds ψ (°)</th>
<th class=n>Longest strut (mm)</th><th class=n>Size (mm)</th><th class=n>Pages</th><th class=n>Closure</th></tr></thead><tbody>{rows}</tbody></table>
<p>Size is twice the longest strut, an upper bound on the finished width. Closure is the gap after folding the net, relative to the longest strut.</p>
<h2>Which solid to fold first</h2>
<p><b>The cube.</b> It needs six copies of one net with one fin shape. Each fan has four triangles, every fold is ψ = 120° (cos ψ = −1/2), and there are 7 pages. Then the
<b>cuboctahedron</b>, which has two nets, 60° fins and folds of arccos(1/3) and arccos(−1/3). It also shows the four central hexagons as flat double sheets.
<b>David</b> has only four pieces, but its 330° fans fold into very shallow pyramids. <b>Kagemusha</b> (30 pyramids, 3 nets) and the One-Strut solids
<b>Cube Pearl</b>, <b>Golden Clasp</b> and <b>TI Star core</b> (18 to 32 pyramids) come after that. In Kagemusha, build the five pyramids on one side of
the central pentagon first and check that the five disc fins lie flat.</p>
<h2>Prior art</h2>
<ul>
<li><b>Modular (unit) origami</b> builds polyhedra from many identical folded units that lock together without glue. Examples are the Sonobe unit, Tomoko Fuse's <i>Unit Origami: Multidimensional Transformations</i> (1990),
her <i>Unit Polyhedron Origami</i> (tetrahedron and octahedron stars from 6 and 12 units), and <i>The Complete Book of Origami Polyhedra</i> (Tuttle). Further
examples are Riskin's system of small polyhedra from Sonobe modules (2007) and Hartl and Kwickert's paper-folded snub cube and snub dodecahedron (Bridges 2012).
Sonobe "pyramid" models are augmentations: they cap each face of a polyhedron with an outward pyramid. The units make the outer surface, and nothing reaches the centre.</li>
<li><b>Paper models from nets with glue tabs</b>: Wenninger, <i>Polyhedron Models</i> (1971; 75 uniform polyhedra and 44 stellations, from face templates);
nets printed by the Stella software; the excavated dodecahedron (Wenninger model 28) is a closed solid with pits, not a fan of centre sheets.</li>
<li><b>Centre pyramids in paper.</b> Hans Walser (2020) folds the cube's six centre pyramids, each from a 1:√2 rectangle, and joins them into a cube
with clips and glue. His page shows single-layer pieces and does not mention open bases or double walls. Constantino and de Souza (<i>Química Nova</i> 1998) made a paper model of
the sp³ carbon atom from the four centre pyramids of a tetrahedron, to show the lines from the centre to the corners. A. Harry Wheeler's dissected-polyhedron
models (Smithsonian) include a rhombic dodecahedron as a cube with six pyramids. All of these are dissections into closed (or base-carrying) pieces.</li>
<li><b>Leonardo's vacuus</b> (Pacioli 1509) is a hollowed edge frame. George Hart rebuilt one in wood (<i>Duodecedron Abscisus Elevatus Vacuus</i>, NNJ, "In the Palm of Leonardo's Hand").
It has no centre sheets.</li>
<li><b>Computational origami</b>: Mitani's ORI-REVO (rotational-sweep 3D origami, 2009) and related tools; Lang's TreeMaker and <i>Origami Design Secrets</i>
(circle and river packing for uniaxial bases); Benbernou, Demaine, Demaine and Ovadya, a universal crease pattern for orthogonal shapes (2009); O'Rourke, folding a polygon
to a polyhedron (2010). These design one sheet for one shape. The Vacuus is not foldable from one sheet, so they do not apply directly.</li>
<li><b>What is known:</b> unit origami polyhedra, paper nets with tabs, paper dissections of a solid into its centre pyramids (the cube, the tetrahedron),
and the face fan of a polytope (classical; see the census).</li>
<li><b>What is new within the sources checked:</b> the open (baseless) centre pyramids, each folded from one fan, nested at the centre so that every 2-cone
of the face fan (every fin) is a double wall. This makes the Vacuus itself the folded object (DICTO's proposal). Also new are the orientation tab rule with two half-tabs per rim,
the exact fold dihedrals and closure check, and the printable nets for DICTO's solids.</li>
</ul>
<p><b>Sources checked</b> (2 November 2026):</p>
<ul>
<li><i>Reference library</i> (ask-library on dicto-big-brother, top 6 + page hits per query). Eight queries:
"modular origami units polyhedra Tomoko Fuse Sonobe unit"; "paper models of polyhedra nets glue tabs Wenninger"; "pyramid units star units origami polyhedral cones";
"computational origami Mitani design of folded paper"; "Lang TreeMaker origami design circle packing"; "excavated polyhedra non-convex solids paper model construction";
"dissection of a polyhedron into pyramids from the centre over the faces model"; "developable cone folded from a flat sector fan of triangles". Relevant catalogue hits:
Riskin 2007 (Sonobé modules); Hartl and Kwickert 2012 (Cubus simus, Dodecaedron simum by paper folding); Wenninger 1971 <i>Polyhedron Models</i>; O'Rourke 2010;
Benbernou, Demaine, Demaine and Ovadya 2009; Gu and Chen 2020 (origami cubes, one-DOF rigid foldability); Nawratil 2021 (origami-like quasi-mechanisms);
Royo Prieto and Tramuns 2014 (3D origami); Weber and Wu 2018 (biplanar foldings); Kabai 2010 (30 cubes on a rhombic triacontahedron, physical models).
Page hits: Pacioli 1509 pp. 9, 46, 101, 107, 115, 116, 132; Kepler 1619 pp. 87, 271; Dürer 1525 pp. 12, 17, 57, 62, 125, 142; Goldberg 1937 p. 1;
Grünbaum 2010 pp. 19–26; Akpanya et al. 2024. The library holds no Fuse, Mitani or Lang text; those were checked on the web. None of the hits describes open centre pyramids or double-walled centre sheets.</li>
<li><i>Web</i> (eight searches): "modular origami pyramid units open pyramid star polyhedron Tomoko Fuse Unit Origami" (Wikipedia <i>Modular origami</i>;
Tuttle, <i>The Complete Book of Origami Polyhedra</i>; Gilad's origami database); "paper model polyhedron dissected into pyramids from the centre…" (H. Walser,
<i>Cube pyramids</i> 2020 and <i>Star</i>; Smithsonian Wheeler models; Wolfram Demonstrations <i>Dissection of three polyhedra into two</i>); "Mitani computational origami
polyhedra design software ORI-REVO" (mitani.cs.tsukuba.ac.jp); "Wenninger Polyhedron Models paper models stellations nets non-convex excavated" (Wikipedia
<i>List of Wenninger polyhedron models</i>, <i>Excavated dodecahedron</i>; software3d.com Stella models); "origami open pyramids glued back to back cube centre interior walls
sculpture" (Walser; Mitchell <i>Abstract Fox</i>; Bridges 2023 p. 601; Tamatebako); "Robert Lang TreeMaker origami design algorithm circle packing uniaxial base" (MIT 6.849
lectures 4–5; Routledge <i>Origami Design Secrets</i>); "Sonobe unit modular origami polyhedra pyramid on each face stellated" (Wikipedia <i>Sonobe</i>; arXiv 0706.2433;
Make <i>Math Monday</i>; Bridges 2011 paper 92); "Vacuus OR hollow polyhedron model made from open pyramids apex at the centre fins double walls paper" (G. Hart, NNJ fig. 10;
Constantino and de Souza 1998, <i>Química Nova</i> 21(5); US 1,292,188; US 2002/0172928).</li>
</ul>
<p>"New" here means new only within these checks.</p>
<h2>Table 2. Exact fins and folds</h2>
<p>The squared lengths are in the units of the source coordinates (the census frame). Fin letters are the same as on the nets.</p>
<table class=ex><thead><tr><th>Solid</th><th>Fins</th><th>Folds (per net type, distinct values)</th></tr></thead><tbody>{exact_rows}</tbody></table>
<h2>Limits</h2>
<ul><li>The paper is assumed to have zero thickness. Real double walls are two sheets thick. Many apices meet at O (up to 32 here), so snipping 2 mm off each tip is advised.
The renders draw the wall gap at 0.8 % of the longest strut so that both walls can be seen.</li>
<li>O is the corner centroid, as in the census. Solids whose centre lies outside a face plane (Lotus Hexa) have no Vacuus and no nets.</li>
<li>Valley and mountain are seen from the printed side. Printed at a different scale, the angles stay the same and the lengths scale.</li></ul>
<div class=plates><h2>Pictures</h2>{plates}</div>
</body></html>'''
open(OUT + '/paper.html', 'w').write(doc); print(len(doc))
