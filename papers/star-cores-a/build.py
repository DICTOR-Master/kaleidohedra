# Paper A of Star Cores (#79): fills head.html's placeholders from the study data. Usage: python3 build.py
import json, os, html, collections
H = os.path.dirname(os.path.abspath(__file__)); K = os.path.dirname(os.path.dirname(H))
SC = os.path.join(K, 'studies/2026-10-30-star-cores/data'); EX = os.path.join(K, 'studies/2026-10-30-star-cores-exact/data')
CE = os.path.join(K, 'studies/2026-10-30-star-chain-census/data')
L = lambda d, f: json.load(open(os.path.join(d, f)))
sc = L(SC, 'star-cores.json'); pol = {r['D']: r for r in L(SC, 'polar-spikes.json')}; sl = L(SC, 'sloping-bases.json')
va = {(r['D'], r['t']): r for r in L(SC, 'star-valley.json')}; sv = {r['name']: r for r in L(CE, 'survey2.json')}
cores = {r.get('D'): r for r in L(EX, 'study2b.json')} if os.path.exists(os.path.join(EX, 'study2b.json')) else {}
e = html.escape
G = {'star fills; core returns (period two)': 'A', 'star fills; core does not return': 'B', 'star inside halo, layer does not fill': 'C', 'star outside its halo': 'D'}
nm = lambda r: r['name'].replace('DICTO ', '')
Dn = lambda r: int(r['D'][1:])
sc.sort(key=Dn)
def faces(r):
    m = json.load(open(os.path.join(K, 'datasets/2026-10-24-dicto-solids', r['file']))) if os.path.exists(os.path.join(K, 'datasets/2026-10-24-dicto-solids', r['file'])) else None
    return r['faces']
def grow(D, t):
    v = va.get((D, t))
    if not v: return None
    s = v['steps']; g = 1.0
    for x in s[1:]: g *= x['volume_over_last']
    return dict(freezes=len(s) >= 3 and abs(s[-1]['volume_over_last'] - 1) < 1e-3, growth23=g, steps=len(s))
out = open(os.path.join(H, 'head.html')).read()

# survey
cnt = collections.Counter((r['convex'], G[r['verdict']]) for r in sc)
byg = collections.defaultdict(list)
for r in sc: byg[(r['convex'], G[r['verdict']])].append(nm(r))
rows = ''.join(f"<tr><td class=c><b>{g}</b></td><td>{d}</td><td class=n>{cnt[(True, g)]}</td><td class=n>{cnt[(False, g)]}</td><td>{e(', '.join(byg[(True, g)]))}</td></tr>"
               for g, d in [('A', 'star fills, core comes back to the shape'), ('B', 'star fills, core does not come back to the shape'),
                            ('C', 'star inside halo, layer not filled by corner and edge pieces'), ('D', 'star sticks out of its halo')])
survey = f"""<p>Table 1 sorts the 54 shapes by what the centre rule gives at t = φ (t = 2 gives the same groups). Only 22 of the 48 convex shapes behave like TI. For the 26 others the tips at a fixed multiple of the face centres are wrong for the shape: where a solid's faces lie at very different distances from the centre, the near faces' tips fall short and the far faces' tips overshoot, so the star either sticks out of the hull of its own tips (group D) or leaves gaps round its high corners that the corner and edge pieces cannot reach (group C). The polar rule of the theorem has no such failure: with it every one of the 48 convex shapes fills, at both ρ² = φR² and ρ² = 2R², whichever group the centre rule put it in. For the faces that all lie at one distance from the centre (TI and the face-transitive shapes) the two rules give the same tips, up to scale.</p>
<table><thead><tr><th>Group</th><th>Centre rule (t = φ)</th><th class=n>Convex</th><th class=n>Non-convex</th><th>Convex shapes</th></tr></thead><tbody>{rows}</tbody></table>
<p class="dataref">Table 1. The 54 shapes of DICTO Solids v6 cut from their centre into face pyramids, by group under the centre rule. The non-convex six (the DICTO Jewel, Lotus Jewel Axes, Dodecaxes, Keyaxes, Kagemusha and the Golden TI Star) are left to a later paper: a pole needs a face plane that misses the centre, which holds, but the layer pieces can then cut into the solid.</p>"""
out = out.replace('<!--SURVEY-->', survey)

# sloping bases
srow = ''.join(f"<tr><td>{r['D']}</td><td>{e(nm(r))}</td><td class=n>{r['phi']['corner_pyramids']}</td><td class=n>{r['phi']['edge_tetrahedra']}</td><td class=n>{r['phi']['volume_over_solid']:.4f}</td><td class=n>{r['phi']['hull_of_tips_over_solid']:.4f}</td><td>{'fills the halo' if r['phi']['fills_hull'] else 'own skin, inside the halo'}</td></tr>" for r in sl)
sloping = f"""<p>For the twelve shapes with high-degree corners that the centre rule leaves unfilled (group C) and that DICTO named, we tested his sloping bases at t = φ and t = 2: the centre-rule tips are kept, and round each corner a ring of pyramids from the corner is laid in order, each with a triangular base on three tips, so that neighbouring pyramids meet along the lines between tips; edge tetrahedra close the gaps over the edges. No two pieces overlap in any of the 24 runs. For the OCD Stella, the Belted Triacontahedron and the OTT the pieces fill the convex hull of the tips exactly. For the nine Queens' slices of #76 they close up into a solid of their own, slightly inside the hull (0.2 to 4 per cent less in volume): a new outer solid for each slice, its faces the sloping bases.</p>
<table><thead><tr><th>D</th><th>Shape</th><th class=n>Corner pyramids</th><th class=n>Edge tetrahedra</th><th class=n>Star + pieces / solid</th><th class=n>Hull of tips / solid</th><th>Result</th></tr></thead><tbody>{srow}</tbody></table>
<p class="dataref">Table 2. DICTO's sloping bases at t = φ (t = 2 gives the same results, with other volumes). Volumes as multiples of the solid's; float64, overlaps by the separating-axis test.</p>"""
out = out.replace('<!--SLOPING-->', sloping)

# valley
fz = {t: [nm(r) for r in sc if (grow(r['D'], t) or {}).get('freezes')] for t in ('phi', '2')}
gr = sorted(((grow(r['D'], '2') or {}).get('growth23', 0), nm(r)) for r in sc if grow(r['D'], '2'))[::-1][:7]
nrun = len(va); clash = 0
valley = f"""<p>Taking the star itself as the next solid, its triangles are spiked in turn. With the tips over the triangles' centres (the centre rule), or over the nearest corner of the star below (a local rule), the new spikes of neighbouring triangles cross in the valleys between the old spikes at the second step, for every shape tested. DICTO's valley rule shortens each spike just enough to clear its neighbours: the ridges keep full spikes and the valleys flatten. With it all {nrun} runs (50 shapes, t = φ and t = 2, at most 200 faces to start and 2,500 triangles in all) end with no clash, and all but one reach the third step (DPHP at t = φ reaches the cap after two).</p>
<!--FIG3-->
<p><b>The symmetric shapes freeze.</b> At the third step they add less than 0.1 per cent of volume: they are finished stars. At t = φ, {len(fz['phi'])} shapes freeze ({e(', '.join(fz['phi']))}); at t = 2, {len(fz['2'])}. <b>The eccentric pieces keep growing</b>, in volume (their radius levels off by the third step). Over steps two and three at t = 2 the largest growth in volume is {e('; '.join(f'{n} ×{g:.2f}' for g, n in gr))}. These are the pieces DICTO built as parts rather than as whole symmetric solids, and they are the subject of the closing chapter of the book.</p>"""
out = out.replace('<!--VALLEY-->', valley)

# cores
if cores:
    cv = [cores[r['D']] for r in sc if r['convex'] and r['D'] in cores]
    cyc = [c for c in cv if c.get('period')]; enters = collections.Counter(c['enters_cycle_at_turn'] for c in cyc)
    corestext = f"""<p class="hook">Take the hull of each family's tips and keep only what lies inside all of them: that is the core of the turn. Turn after turn, the cores of most shapes settle into a pair that swaps back and forth.</p>
<p>The core of a turn (#78, Proposition 5) was followed exactly, turn after turn, for all {len(cv)} convex shapes (with the tips at the feet of the face perpendiculars; a factor t only scales the core). Every one of the {len(cyc)} shapes whose cores keep forming settles into a <b>cycle of period two</b>: {enters[0]} at once (the GTI and the TI Star core, whose cores bring back the shape itself), {enters[1]} after one turn and {enters[2]} after two. The other {len(cv) - len(cyc)} reach a turn where no family of tips spans a solid (every family has fewer than four tips or lies in one plane; for Fang the centre is not strictly inside one family's hull): the low-symmetry shapes at the first turn, seven Queens' slices at the second and Tweedledee at the third. The two-turn scale in radius is t² cos²θ, with θ the angle between the two kinds of symmetry axis carrying the cores' faces: t²(5 + 2√5)/15 for the icosahedral shapes, t²/3 for the octahedral (OCD Stella, OTT, Lahdeli) and t²/9 for the tetrahedral (Samson, the Triskelion Tetrahedron, Alice, the White Rabbit). The Belted Triacontahedron alone has another value, because only one family of its cores is solid at each turn. Paper B proves the period two for cores with two families on two kinds of axis and studies the exceptions.</p>
<p class="dataref">An earlier float survey reported a returning core only for the GTI and the TI Star core: it asked whether the core of the core is the shape itself, which is the case of a cycle entered at once. The exact run (study 2b) confirms both and finds the cycles entered later.</p>"""
else:
    corestext = "<p>[The exact core cycles of all convex shapes are being computed; this section is filled from that run.]</p>"
out = out.replace('<!--CORES-->', corestext)

# cards
def tchain(r):
    s = sv.get(r['name'])
    if not s: return '–'
    if s.get('period'): return f"period {s['period']}"
    return 'open (8 steps)' if s.get('centre_meaningful', True) else 'no centre'
crow = []
for r in sc:
    if not r['convex']: continue
    D = r['D']; p = pol.get(D); g2 = grow(D, '2'); gp = grow(D, 'phi'); c = cores.get(D)
    val = lambda x: '–' if not x else ('freezes' if x['freezes'] else f"×{x['growth23']:.2f}")
    core = '–' if not c else (f"period {c['period']}" + (' at once' if c.get('enters_cycle_at_turn') == 0 else f" from turn {c['enters_cycle_at_turn']}") if c.get('period') else 'no core at turn ' + c['outcome'].split('turn ')[1].split(':')[0])
    crow.append(f"<tr><td>{D}</td><td>{e(nm(r))}</td><td>{e(r['symmetry'])}</td><td class=n>{r['corners']}</td><td class=n>{r['faces']}</td><td class=c>{G[r['verdict']]}</td><td class=n>{p['phi']['halo_over_solid']:.3f}</td><td class=n>{r['corners'] + r['corners'] + r['faces'] - 2}</td><td>{core}</td><td>{tchain(r)}</td><td>{val(gp)}</td><td>{val(g2)}</td></tr>")
cards = f"""<p>One line per convex shape. Halo: the volume of the polar-spike halo at ρ² = φR² over the shape's. Pieces: corner pyramids plus edge tetrahedra of the polar fill (V + E). Core: the exact core cycle (paper B). T-chain: the star chain read as DICTO's rule T (#80). Valley: growth over steps two and three under DICTO's valley rule, or 'freezes'.</p>
<table class=cards><thead><tr><th>D</th><th>Shape</th><th>Sym.</th><th class=n>V</th><th class=n>F</th><th class=c>Group</th><th class=n>Halo</th><th class=n>Pieces</th><th>Core</th><th>T-chain</th><th>Valley φ</th><th>Valley ×2</th></tr></thead><tbody>{''.join(crow)}</tbody></table>
<p class="dataref">Table 3. The cards. Group: the centre rule's group of Table 1. V, F: corners and faces (pieces V + E = 2V + F − 2 by Euler). '–': not run (over 200 faces, or no data).</p>"""
out = out.replace('<!--CARDS-->', cards)
FIGS = {'<!--FIG1-->': ('polar-fill.png', 'The polar-spike fill', '<b>Figure 1.</b> The polar-spike fill at ρ² = φR². Top: the DICTO GTI (D40): its star with 32 polar spikes; the layer drawn apart, 60 corner pyramids (gold) and 90 edge tetrahedra (teal); the halo, the hull of the 32 tips, with one facet over each corner. Bottom: the same for the OCD Stella (D29): 50 spikes, 48 corner pyramids, 96 edge tetrahedra. In each row the star and the layer add up to the halo.'),
        '<!--FIG2-->': ('star-gallery.png', 'Twelve stars inside their halos', '<b>Figure 2.</b> Twelve of DICTO\'s shapes with polar spikes (ρ² = φR²) inside their see-through halos. Spikes on the largest family of faces violet, the others teal.'),
        '<!--FIG3-->': ('valley.png', 'The valley rule', '<b>Figure 3.</b> DICTO\'s valley rule at t = 2, steps one to three; each spike is shortened until it clears the pieces already built and its neighbours. Left: the FPD (D41) stops growing: its radius stays the same from step two and its volume from step three. Right: Lahdeli (D77), an eccentric piece, still adds a third of its volume at step three, although its radius no longer grows. Columns: the FPD, Lahdeli; rows: steps one to three. Spikes of step one violet, step two teal, step three lilac.')}
for k, (f, alt, cap) in FIGS.items(): out = out.replace(k, f'<figure{" class=full" if k == "<!--FIG3-->" else ""}><img src="figures/{f}" alt="{alt}"><figcaption>{cap}</figcaption></figure>')
open(os.path.join(H, 'paper.html'), 'w').write(out)
print('ok', len(crow), 'cards; cores', len(cores))
