# DICTO 2026-10-18 golden octet adaptor -- 3D page -> renders/p4-golden-octet-adaptor.html
import json, os, itertools, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); d = json.load(open(os.path.join(H, '..', 'data', 'p4-mesh.json')))
O = os.path.join(H, '..', '..', '2026-10-18-ocd-octet', 'data'); e23 = json.load(open(os.path.join(O, 'step23-envelope-meshes.json'))); x27 = json.load(open(os.path.join(O, 'step27-expanded.json')))
R = json.load(open(os.path.join(O, 'step10-input.json')))['R']
rd = [[R * a, R * b, R * c] for a, b, c in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]] + [[R * a / 2, R * b / 2, R * c / 2] for a, b, c in itertools.product((1, -1), repeat=3)]
from scipy.spatial import ConvexHull
h = ConvexHull(np.array(rd)); rdt = []
for s in h.simplices:
    a, b, c = np.array(rd)[s]; n = np.cross(b - a, c - a); rdt.append(s.tolist() if n @ a > 0 else [s[0], s[2], s[1]])
P = {'rd': dict(v=rd, t=[list(map(int, t)) for t in rdt], colour='#d9a21b'),
     'rdglass': dict(v=rd, t=[list(map(int, t)) for t in rdt], colour='#8fb7e0', glass=True),
     'env': dict(v=d['envelope']['v'], t=d['envelope']['t'], colour='#e8c56a'),
     'half': dict(v=d['half']['v'], t=d['half']['t'], colour='#5b8fd0'),
     'adglass': dict(v=d['adaptor']['v'], t=d['adaptor']['t'], colour='#5b8fd0', glass=True),
     'ocd': dict(v=e23['ocd']['v'], t=e23['ocd']['t'], colour='#d9a21b'),
     'W': (lambda w: dict(v=w['v'], t=w['t'], colour='#26a69a'))(json.load(open(os.path.join(H, '..', 'data', 'p4-W.json')))),
     'Wo': (lambda w: dict(v=w['v'], t=w['t'], colour='#7e57c2'))(json.load(open(os.path.join(H, '..', 'data', 'p4-W-ocd.json')))),
     'grown': dict(v=x27['mesh']['v'], t=x27['mesh']['t'], colour='#3f9a5b', colour2='#2a9d9a')}
Rx = [1, 0, 0, 0, -1, 0, 0, 0, -1]   # half-turn about x: the top half becomes the bottom half
fcc = [(np.array(c) * R).tolist() for c in itertools.product(range(-2, 3), repeat=3) if sum(c) % 2 == 0 and np.linalg.norm(np.array(c) * R) <= R * 1.5]
tets = [['grown', ((sum(s) % 4) + 4) % 4 == 1, (np.array(s) * R / 2).tolist()] for s in itertools.product(range(-3, 4, 2), repeat=3) if np.linalg.norm(np.array(s) * R / 2) <= R * 0.9]
ch = json.load(open(os.path.join(H, '..', 'data', 'p4-chamber.json'))); ci = ch['info']
Wsites = [(np.array(c) * R).tolist() for c in itertools.product(range(-2, 3), repeat=3) if sum(c) % 2 == 1 and np.linalg.norm(np.array(c) * R) <= R * 1.5]
views = {
    'ocdW': dict(label='OCD + W with OCD imprints', text='solid OCD with the 6 imprinted W pieces at its octahedron corners (purple) — two shapes, no mirror pair', radius=1.9,
                 place=[['ocd', False, [0, 0, 0]]] + [['Wo', False, (R * np.array(e) * s).tolist()] for e in np.eye(3) for s in (1, -1)]),
    'ocdWset': dict(label='OCD + W, the set', text='the two shapes: OCD (gold) and W with exact OCD imprints (purple), (2824 − 328√5)/1539 = 1.358395, sphericity 0.648', radius=1.3,
                    place=[['ocd', False, [-0.8, 0, 0]], ['Wo', False, [0.9, 0, 0]]]),
    'ocdWnet': dict(label='OCD + W network', text='OCDs on the octahedron sites, imprinted W on the octet vertices: fills space exactly', radius=3.2,
                    place=[['ocd', False, p] for p in fcc] + [['Wo', False, p] for p in Wsites]),
    'envW': dict(label='Envelope + W (Fable)', text='solid golden envelope with the 6 W glue pieces at its octahedron corners (teal) — two shapes, no mirror pair', radius=1.9,
                 place=[['env', False, [0, 0, 0]]] + [['W', False, (R * np.array(e) * s).tolist()] for e in np.eye(3) for s in (1, -1)]),
    'envWset': dict(label='Envelope + W, the set', text='the two shapes: golden envelope (gold) and W (teal), volume 2G = (352 − 144√5)/27 = 1.111341, sphericity 0.574', radius=1.3,
                    place=[['env', False, [-0.8, 0, 0]], ['W', False, [0.9, 0, 0]]]),
    'envWnet': dict(label='Envelope + W network', text='envelopes on the octahedron sites, W on the octet vertices: fills space exactly (Fable, proved)', radius=3.2,
                    place=[['env', False, p] for p in fcc] + [['W', False, p] for p in Wsites]),
    'two': dict(label='Two shapes: envelope + adaptor half', text='solid golden envelope · 2 identical adaptor halves (blue; one turned over) = rhombic dodecahedron. 2 shapes, no mirror images', radius=1.6,
                place=[['env', False, [0, 0, 0]], ['half', False, [0, 0, 0.35]], ['half', False, [0, 0, -0.35], Rx]]),
    'any': dict(label='Adaptor round any golden-envelope solid', text='glass adaptor; inside, any solid whose golden envelope this is — here the OCD', radius=1.6,
                place=[['adglass', False, [0, 0, 0]], ['ocd', False, [0, 0, 0]]]),
    'one': dict(label='One piece (fused) — network', text='envelope + adaptor fused = rhombic dodecahedron: one shape, fills space alone (fcc); 13 shown', radius=3.0,
                place=[['rd', False, p] for p in fcc]),
    'inside': dict(label='One piece, see-through', text='glass rhombic dodecahedra with their golden envelopes inside: the envelopes touch each face at one point (12 corners, the golden-section points)', radius=3.0,
                   place=[['rdglass', False, p] for p in fcc] + [['env', False, p] for p in fcc]),
    'chamber': dict(label='Chamber (outside the plan)', text=f"hollow spherical chamber, radii {ci['R_in']}–{ci['R_out']}: {ci['outer_cells']} outer and {ci['inner_surface_cells']} inner-surface cells half-open (golden envelopes exposed outside and inside), {ci['solid_cells']} full rhombic dodecahedra between", radius=7.5,
                    place=ch['full']),
    'chambercut': dict(label='Chamber, cut open', text='the same chamber cut in half: envelopes exposed on the outer skin and lining the hollow centre, solid rhombic dodecahedra between', radius=7.5, place=ch['cut']),
    'twosolid': dict(label='Two-shape set (3), solid envelope', text='solid golden envelope with its 8 grown core pieces (left green, right teal)', radius=1.9,
                     place=[['env', False, [0, 0, 0]]] + tets),
}
facts = ['Exact: the golden envelope (rhombic triacontahedron) lies inside the rhombic dodecahedron of its fcc site (the cell where every point goes to its nearest envelope) and touches each of its 12 faces at one corner — the golden-section corners on the octahedron edges.',
         'Adaptor = rhombic dodecahedron − envelope: exact 352/27 − 16√5/3 = 1.111341, centrosymmetric (no left/right). It is a closed shell (a cavity), so it opens in two identical halves along the plane z = 0 (0.555671 each, one solid, sphericity 0.37); the half-turn about the x axis maps one onto the other.',
         'So: one-piece golden octet = rhombic dodecahedron (envelope fused), fills space alone. Two-shape golden octet = envelope + adaptor half (×2). The cavity takes any solid whose golden envelope it is (the OCD, the envelope itself, …).',
         'Envelopes fill 10/φ⁶ = 55.73% of space; adaptors 44.27%.', 'Chamber views (outside the plan, DICTO): geometry only, nothing structural is claimed.', 'OCD + W (DICTO: "face could be exact imprint of OCD"): W = rhombic dodecahedron round each octet vertex minus the 6 OCDs biting into it; one solid, centrosymmetric (no mirror pair), sphericity 0.648; OCD + W fills space exactly because the vertex rhombic dodecahedra tile space.', 'Envelope + W (Fable review 2): W = rhombic dodecahedron round each octet vertex minus its 6 envelope bites; one solid, achiral, contains the φ⁻² cuboctahedron; proved exactly to fill space with the envelopes.']
html = open(os.path.join(H, 'kit_viewer_template.html')).read()
for k, v in {'__TITLE__': 'Golden Octet Adaptor', '__SUB__': 'DICTO 2026-10-18: all non-envelope pieces fused into one adaptor per golden envelope. Drag to turn.',
             '__MARK__': 'studies/2026-10-18-p4-golden-octet-adaptor', '__FACTS__': ''.join(f'<li>{f}</li>' for f in facts),
             '__DATA__': json.dumps(dict(pieces=P, views=views), separators=(',', ':'))}.items(): html = html.replace(k, v)
open(os.path.join(H, '..', 'renders', 'p4-golden-octet-adaptor.html'), 'w').write(html); print('ok', len(html))
