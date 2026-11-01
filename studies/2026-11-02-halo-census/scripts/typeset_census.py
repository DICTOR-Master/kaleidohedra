# Stars and Halos Census: the typeset page (HTML for papers/print.mjs) from data/census.json and data/thumbs.
# Usage: typeset_census.py <study dir> <out dir>   (then: node print.mjs <out dir name> stars-and-halos-census.pdf ...)
import json, html, os, shutil, collections, re, sys
ST, OUT = sys.argv[1:3]
C = json.load(open(os.path.join(ST, 'data/census.json'))); os.makedirs(OUT + '/thumbs', exist_ok=True)
def fbs(d): return ', '.join(f'{k}:{v}' for k, v in sorted(d.items(), key=lambda x: int(x[0])))
def sym(s):
    if s in ('Ih', 'I', 'Oh', 'O', 'Td', 'Th', 'T'): return s[0] + (f'<sub>{s[1:]}</sub>' if len(s) > 1 else '')
    return re.sub(r'([CDS])(\d+)([a-z]*)', r'\1<sub>\2\3</sub>', s)
def stat(c):
    if c['status'] == 'NEW': return f'<b>NEW</b>: {html.escape(c["placeholder"])}'
    if c['status'] == 'known':
        return html.escape('; '.join(m[4:] if m.startswith('v7: ') else m.split(': ', 1)[0] + ': ' + m.split(': ', 1)[1].replace('_', ' ').title() for m in c['matches']))
    return html.escape(c['status'])
def short(n): return html.escape(n.replace('DICTO ', '').split(' (')[0])
H = [c for c in C if c['part'] in ('centre_halo', 'polar_halo')]; S = [c for c in C if c['part'].startswith('star')]
rows_h = ''.join(f"<tr><td>{short(c['shape'])}</td><td>{'centre' if c['part'] == 'centre_halo' else 'polar'}</td><td class=n>{c['corners']}</td><td>{fbs(c['faces_by_sides'])}</td><td>{sym(c['symmetry'])}</td><td>{stat(c)}</td></tr>" for c in H)
rows_s = ''.join(f"<tr><td>{short(c['shape'])}</td><td>{'2' if c['part'] == 'star_2' else 'φ'}</td><td class=n>{c['corners']}</td><td class=n>{c['faces']}</td><td>{fbs(c['faces_by_sides'])}</td><td>{sym(c['symmetry'])}</td><td>{stat(c)}</td></tr>" for c in S)
thumbs = ''
for c in H:
    if c['status'] != 'NEW': continue
    fn = f"{c['slug']}-{c['part']}.png"; shutil.copy(os.path.join(ST, 'data/thumbs', fn), OUT + '/thumbs/' + fn)
    thumbs += f'<figure class=th><img src="thumbs/{fn}"><figcaption>{html.escape(c["placeholder"])}</figcaption></figure>'
nf = sum(1 for c in C if not c['exact']); N = len(C)
cnt = collections.Counter((c['part'].split('_')[0], c['status'].split(' ')[0]) for c in C)
doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Stars and Halos Census</title><link rel="stylesheet" href="../paper.css">
<style>table{{border-collapse:collapse;font-size:7pt;margin:2mm 0;width:100%}} td,th{{border-bottom:1px solid #ddd;padding:0.5mm 1mm;text-align:left;vertical-align:top}} td.n,th.n{{text-align:right}} thead{{display:table-header-group}} tr{{break-inside:avoid}} .thm{{border-left:3px solid #b8962e;padding-left:3mm;margin:2.5mm 0}} body,p,li{{font-size:8.6pt;line-height:1.38}} h1{{font-size:18pt}} .logo{{width:22mm}} h2{{font-size:11pt;margin:3.5mm 0 1mm}} .grid{{display:grid;grid-template-columns:repeat(6,1fr);gap:2mm}} figure.th{{margin:0;break-inside:avoid}} figure.th img{{width:100%;display:block}} figure.th figcaption{{font:6.4pt/1.2 "DejaVu Sans",sans-serif;text-align:center;color:#333}}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>Stars and Halos Census</h1>
<p class="sub">Every halo and every star of the 58 solids of the Star Cores book, matched against DICTO Solids v7, the classical families and each other</p>
<div class="meta"><b>DICTO</b> · dictospheres.com · 2 November 2026 · study 2026-11-02-halo-census (census.py, collect.py), DICTO Solids v7 · not published</div>
<div class="thm"><b>Conclusion.</b> Of the 110 halos, 84 are new: 42 centre halos and 42 polar halos. 22 are known solids, most of them other solids of DICTO Solids, such as the OG's halo, which is the TPH. 4 repeat another halo of the census. All 116 stars are new except one pair: the stars of the FPD and the Palintriacontahedron coincide, because these two dataset solids are the same shape up to similarity. No star equals a stellation in the registry, and no star's base solid is classical. The operations themselves are classical; the new objects are the halos and stars of DICTO's new solids.</div>
<h2>What was computed</h2>
<p>The census covers the 58 solids with cards in the Star Cores book. The two notch cards, Maedate and Kuwagata, are pieces, not solids with a star treatment, and are left out. Three objects were computed for each solid:</p>
<ul>
<li><b>Centre halo:</b> the hull of the spike tips t × (foot of the perpendicular from the centre O to each face plane). Its shape does not depend on t, so one census row covers both t = 2 and t = φ.</li>
<li><b>Polar halo:</b> the hull of the polar points of the face planes, i.e. the polar reciprocal (dual) of the solid about O. It was computed for the 52 convex solids with O inside every face plane, and its shape does not depend on ρ.</li>
<li><b>Stars at t = 2 and t = φ:</b> the solid with its face pyramids turned outwards, taken as a surface and with coplanar neighbouring faces merged.</li>
</ul>
<p>{N - nf} of the {N} objects come from solids in Q(√5) or Q and were computed exactly. Every hull facet was checked exactly: every facet point lies on the facet plane and every other point lies strictly inside. Star faces were merged only where they are exactly coplanar. The {nf} objects of the four solids in other fields (Q(t), Q(∛2), Q(√3)) were computed in float64.</p>
<p>A match means the same number of corners (and, for halos, the same faces by sides), the same scaled squared distances between corners, and an explicit orthogonal map of one corner set onto the other, all to 10<sup>−6</sup>. Mirror images count as the same shape. Symmetry is that of the corner set. The objects were compared against:</p>
<ul>
<li>DICTO Solids v7 (all solids);</li>
<li>the classical families, from krp-core's registry (closed-form coordinates): the 5 Platonic, 13 Archimedean and 13 Catalan solids and the 92 Johnson solids;</li>
<li>the uniform prisms and antiprisms for n = 3–40 and their duals, the bipyramids and trapezohedra, generated here;</li>
<li>for the stars, the 72 stellations in krp-core: the first four stellations of each Platonic and Catalan solid, together with the rhombic dodecahedron and rhombic triacontahedron.</li>
</ul>
<h2>Prior art</h2>
<p>The operations are classical, and only the objects they produce from new solids are new.</p>
<ul>
<li>Raising a pyramid on every face is the Kleetope (B. Grünbaum, Convex Polytopes, 1967, pp. 217, 227) and Conway's kis operator (G. W. Hart, “Conway Notation for Polyhedra”, georgehart.com; Antiprism “conway” documentation). A star is a kis with a chosen apex height, and a star of a classical solid would be a classical Kleetope; none of the 58 base solids is classical.</li>
<li>The polar halo is the polar reciprocal (dual) of the solid.</li>
<li>The hull of the feet of the perpendiculars to the face planes is the hull of the “face pedal” points, which arXiv:1003.2153 (Nine solved and nine open problems in elementary geometry) lists among open questions.</li>
</ul>
<p><b>Sources checked</b> (2 November 2026):</p>
<ul>
<li><i>Reference library</i> (ask-library, five hits each). Five queries: “hull of the feet of the perpendiculars from the centre to the face planes (pedal polyhedron)”, “polar reciprocal of a polyhedron, dual polyhedron, reciprocation in a sphere”, “Kleetope: raising a pyramid on every face”, “Conway kis operator pyramids on faces” and “convex hull of pyramid apexes over the faces of a polyhedron”. They returned Hynd 2023, Cesaroni–Novaga 2026, Richter-Gebert 2026, Montejano et al. 2019, Wikipedia “Goldberg polyhedron”, Koca et al. 2010, Wikipedia “Rhombic dodecahedron”, McMullen–Schulte 2005, Matteo 2014, Leppmeier 2019, O'Rourke 2010, Devadoss et al. 2026, Antiprism “conway”, Kabai 2010, Gosain–Grimmer 2025, Johnson 1966, He–Guest 2025, Hepworth 2022, Erdahl 1999 and Magazinov 2015, and the pages Pacioli 1509 p. 107, Firsching 2015 p. 10, Dutour Sikirić et al. 2008 p. 31 and Betke–Henk 2000 p. 35. None names any of these halos or stars.</li>
<li><i>Web</i> (three searches): “Kleetope Grünbaum Convex Polytopes”, which found Wikipedia “Kleetope” and arXiv:1509.08218 and 2004.08429; “polyhedron convex hull of feet of perpendiculars from centre to face planes pedal polyhedron”, which found arXiv:2108.08293 and 1003.2153 and the papers by Grace (1927) and Robinson (1939) on pedal tetrahedra; and “Conway polyhedron notation kis operator”, which found Hart's page, Wikipedia and Antiprism.</li>
</ul>
<p>No source lists any of the new halos or stars. A solid is “new” here only within these checks.</p>
<h2>Flag</h2>
<p>The FPD (flat pentakis dodecahedron) and the Palintriacontahedron are similar: same corner set up to scale, 32 corners, 60 faces, I<sub>h</sub>. DICTO Solids v7 holds them as two entries. By the one-name-per-shape rule, this is for DICTO to decide.</p>
<h2>Table 1. Halos ({len(H)})</h2>
<table><thead><tr><th>Solid</th><th>Halo</th><th class=n>Corners</th><th>Faces by sides</th><th>Symmetry</th><th>Known as / NEW (placeholder name)</th></tr></thead><tbody>{rows_h}</tbody></table>
<h2>Table 2. Stars ({len(S)})</h2>
<table><thead><tr><th>Solid</th><th>t</th><th class=n>Corners</th><th class=n>Faces</th><th>Faces by sides</th><th>Symmetry</th><th>Known as / NEW (placeholder name)</th></tr></thead><tbody>{rows_s}</tbody></table>
<h2>The {thumbs.count('<figure')} new halos</h2>
<p>Faces are coloured by number of sides: triangles violet, quadrilaterals teal, pentagons gold, hexagons orange, octagons blue, decagons red.</p>
<div class="grid">{thumbs}</div>
</body></html>'''
open(OUT + '/paper.html', 'w').write(doc); print(len(doc), dict(cnt))
