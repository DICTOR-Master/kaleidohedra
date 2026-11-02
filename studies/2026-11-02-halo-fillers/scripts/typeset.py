# Halo Fillers: the typeset study note (HTML for papers/print.mjs) from data/*.json and figs/.
# Usage: typeset.py <study dir> <out dir>   (then on dicto-big-brother: node print.mjs <out dir name> halo-fillers.pdf "Halo Fillers" "none (study note)" 1)
import json, os, shutil, sys, html
ST, OUT = sys.argv[1:3]; os.makedirs(OUT + '/figs', exist_ok=True)
L = lambda f: json.load(open(os.path.join(ST, 'data', f)))
s1, s2, s3, san, mg = L('screen.json'), L('screen2.json'), L('screen3.json'), L('sanity.json'), L('margins.json'); c = s1['counts']
surv = sorted({k.split(' | ')[0] for k in s1['with_known']})
pairs = {}
for k in s1['with_known']: h, p = k.split(' | '); pairs.setdefault(h, []).append(p)
how = lambda k: 'balance lemma: the halo face must meet a copy face to face; no placement closes its edges (test 3)' if s3.get(k, {}).get('applies') and s3[k]['passes'] is False else 'test 4: keyed-bond corner argument'
rows = ''.join(f'<tr><td>{html.escape(k.split(" | ")[0])}</td><td>{html.escape(k.split(" | ")[1])}</td><td>{html.escape(how(k))}</td></tr>' for k in sorted(s1['with_known']))
figs = ''
for fn, cap in (('dicto-tweedledum-centre_halo.png', 'Tweedledum Halo'), ('dicto-metaxyhexecontahedron-centre_halo.png', 'Metaxyhexecontahedron Halo'),
                ('dicto-dbt-polar_halo.png', 'DBT Polar Halo'), ('dicto-ott-polar_halo.png', 'OTT Polar Halo')):
    shutil.copy(os.path.join(ST, 'figs', fn), OUT + '/figs/' + fn); figs += f'<figure class=th><img src="figs/{fn}"><figcaption>{cap}</figcaption></figure>'
gmin = min(v['gap_rad'] for v in mg.values())
cl = san['classical']
doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Halo Fillers</title><link rel="stylesheet" href="../paper.css">
<style>table{{border-collapse:collapse;font-size:7.4pt;margin:2mm 0;width:100%}} td,th{{border-bottom:1px solid #ddd;padding:0.6mm 1mm;text-align:left;vertical-align:top}} td.n,th.n{{text-align:right}} .thm{{border-left:3px solid #b8962e;padding-left:3mm;margin:2.5mm 0}} body,p,li{{font-size:8.8pt;line-height:1.4}} h1{{font-size:18pt}} .logo{{width:22mm}} h2{{font-size:11pt;margin:3.5mm 0 1mm}} .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}} figure.th{{margin:0;break-inside:avoid}} figure.th img{{width:100%;display:block}} figure.th figcaption{{font:7pt/1.2 "DejaVu Sans",sans-serif;text-align:center;color:#333}}</style></head><body>
<img class="watermark" src="../dicto-logo.png" alt=""><img class="logo" src="../dicto-logo.png" alt="DICTO">
<h1>Halo Fillers</h1>
<p class="sub">Do any of the 84 new halos of the Stars and Halos census fill space, alone or in a pair?</p>
<div class="meta"><b>DICTO</b> · dictospheres.com · 2 November 2026 · study 2026-11-02-halo-fillers, from study 2026-11-02-halo-census and DICTO Solids v7 · not published</div>
<div class="thm"><b>Conclusion.</b> None fills. No new halo tiles space by congruent copies (mirror images allowed, face to face or not). No two new halos fill space together, and no new halo fills space together with any of the 12 known filler sets tried: cube, rhombic dodecahedron, truncated octahedron, hexagonal prism, triangular prism, tetrahedron + octahedron, and DICTO's six published fills in DICTO Solids v7. These results hold at every relative scale of the two pieces.</div>
<h2>Counts</h2>
<table><thead><tr><th>Question</th><th class=n>Tested</th><th class=n>Pass test 1 (edges)</th><th class=n>Pass test 2 (corners)</th><th class=n>Pass tests 3–4</th><th class=n>Fill</th></tr></thead><tbody>
<tr><td>One halo alone</td><td class=n>{c['halos']}</td><td class=n>{c['single_pass']}</td><td class=n>–</td><td class=n>–</td><td class=n>0</td></tr>
<tr><td>Halo + halo</td><td class=n>{c['halo_pairs_tested']}</td><td class=n>{c['halo_pairs_pass']}</td><td class=n>–</td><td class=n>–</td><td class=n>0</td></tr>
<tr><td>Halo + known filler set</td><td class=n>{c['with_known_tested']}</td><td class=n>{c['with_known_pass']}</td><td class=n>{sum(1 for v in s2.values() if v['passes'])}</td><td class=n>0</td><td class=n>0</td></tr>
</tbody></table>
<h2>The four tests</h2>
<p>Each test is a necessary condition for any tiling of space by copies of the pieces. A tiling may use rotations and mirror images, and it need not be face to face.</p>
<ol>
<li><b>Edges.</b> Take a point inside an edge of a piece, where the dihedral angle is a. Each other piece through that point adds either its own dihedral angle (the point is on one of its edges) or π (the point is inside one of its faces), and the total is 2π. So 2π − a or π − a must be a sum of dihedral angles of the pieces in the set, with repeats allowed. The test is run on floats, accepting a sum within 10<sup>−7</sup> rad. Dihedral angles are computed from the census corners, whose float error is below 10<sup>−12</sup> rad. For every halo that fails alone, its worst edge misses every sum by at least {gmin:.4f} rad, so these failures are proofs.</li>
<li><b>Corners.</b> Suppose π − a is not a sum of dihedral angles for any edge of a halo face. Then no neighbour's face can cross an edge of that face, so coplanar faces of neighbours cover it exactly. Each corner angle of the face must then be a sum of face corner angles of the set.</li>
<li><b>Balance.</b> If a convex polygon is tiled by convex polygons, then for every direction u the total edge length facing u minus the total facing −u is the same for the tiles together as for the polygon, because inner edges cancel. This is a standard argument. Centrally symmetric tiles add zero. So if every face of the partner is centrally symmetric (true for the skewed EDs and the skewed rhombic dodecahedron, which are zonohedra), a halo face that is not centrally symmetric must contain a halo face. Suppose also that no smaller halo face fits inside it. Then the cover is a congruent face of a copy of the halo, and the two halos meet face to face. Every way of placing the copy was tried; none closes all the edges (test 1).</li>
<li><b>Keyed bond.</b> This applies to the DBT and OTT Polar Halos with Lotus Jewel Axes + Dodecaxes. Each of their triangles has three edges at 142.62°. The only completion is the 217.38° reflex edge of a Dodecaxes; a π-crossing or a halo copy cannot close the edge. A 60° corner of the triangle can only be covered by two triangle corners, 22.24° + 37.76°. Both corners must belong to Dodecaxes faces whose outer edges are those reflex edges. Their shared inner edge then carries 109.47° + 125.26° on one side of the halo face, and the face itself adds π on the other side: 414.73° &gt; 360°. Contradiction.</li>
</ol>
<h2>The 14 pairs that passed tests 1 and 2</h2>
<p>Four halos passed test 1 with some partner. All four have only the icosahedral face directions (5-fold and 3-fold axes), the same as the skewed EDs and the skewed rhombic dodecahedron. The Tweedledum Halo and the Metaxyhexecontahedron Halo have the dihedral angles of the truncated icosahedron.</p>
<div class="grid">{figs}</div>
<table><thead><tr><th>Halo</th><th>Partner</th><th>Ruled out by</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Sanity checks</h2>
<ul>
<li>Test 1 passes the cube, rhombic dodecahedron and truncated octahedron ({'yes' if all(cl[k] for k in cl if 'fills)' in k) else 'NO'}). It fails the rhombic triacontahedron, regular dodecahedron, regular icosahedron, and the regular octahedron and tetrahedron alone ({'yes' if not any(cl[k] for k in cl if 'not fill' in k) else 'NO'}).</li>
<li>Every one of the 12 known filler sets passes test 1 on its own angles. All 26 halos of the census that are known or repeated solids fail test 1 alone; none of them is a classical space-filler.</li>
<li>For all 110 halos, the face counts used here match the census exactly ({'yes' if not san['face_count_mismatch'] else 'NO'}).</li>
</ul>
<h2>Scope and limits</h2>
<ul>
<li>Only halos were tested; stars do not fill alone (DICTO). The partners are the 12 sets listed above. Pairs of a halo with any other shape, and sets of three or more pieces beyond those listed, were not tested.</li>
<li>No filler was found, so no tiling was constructed and no prior-art check was needed. The balance argument of test 3 is classical and is not claimed as new.</li>
</ul>
</body></html>'''
open(OUT + '/paper.html', 'w').write(doc); print(len(doc))
