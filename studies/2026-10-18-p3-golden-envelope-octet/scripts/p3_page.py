# DICTO 2026-10-18 Project 3, Golden envelope octet (sets 3, 3b, 3c) -- 3D page -> renders/p3-golden-envelope-octet.html
# Meshes from the octet study (step23 envelope, step25 cuboctahedron/wedges/cut-down tetrahedron, step27 grown piece) and data/p3c-split.json.
import json, os, itertools, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); O = os.path.join(H, '..', '..', '2026-10-18-ocd-octet', 'data')
J = lambda p: json.load(open(p))
e23 = J(os.path.join(O, 'step23-envelope-meshes.json')); r25 = J(os.path.join(O, 'step25-refined-meshes.json')); x27 = J(os.path.join(O, 'step27-expanded.json'))
s3c = J(os.path.join(H, '..', 'data', 'p3c-split.json')); R = J(os.path.join(H, '..', '..', '2026-10-18-ocd-octet', 'data', 'step10-input.json'))['R']
def centred(m):
    V = np.array(m['v']); c = V.mean(0); return dict(v=np.round(V - c, 6).tolist(), t=m['t']), c
P, C = {}, {}
for key, m, col, col2 in (('env', e23['envelope'], '#e8c56a', None), ('cubo', r25['cubo'], '#e07b39', None), ('w1', r25['wedge1'], '#c8382f', None), ('w2', r25['wedge2'], '#c8382f', None)):
    P[key], C[key] = centred(m); P[key]['colour'] = col
P['env']['glass'] = True; C['env'] = np.zeros(3); P['env']['v'] = np.round(np.array(e23['envelope']['v']), 6).tolist()
P['ocd'] = dict(v=e23['ocd']['v'], t=e23['ocd']['t'], colour='#d9a21b')
tc = np.array([R / 2] * 3)
P['tcut'] = dict(v=(np.round(np.array(r25['tet_trunc']['v']) - tc, 6)).tolist(), t=r25['tet_trunc']['t'], colour='#3f9a5b', colour2='#2a9d9a')
P['grown'] = dict(v=x27['mesh']['v'], t=x27['mesh']['t'], colour='#3f9a5b', colour2='#2a9d9a')
P['dode'] = dict(v=s3c['dodeca']['v'], t=s3c['dodeca']['t'], colour='#9575cd', colour2='#c792ea')
P['shell'] = dict(v=s3c['shell']['v'], t=s3c['shell']['t'], colour='#3f9a5b', colour2='#2a9d9a')
ops = []
for pm in ([0, 1, 2], [1, 2, 0], [2, 0, 1]):
    for sg in itertools.product((1, -1), repeat=3):
        G = np.zeros((3, 3))
        for i in range(3): G[i, pm[i]] = sg[i]
        ops.append(G)
def orbit(key):
    out, seen = [], set()
    for G in ops:
        h = G @ C[key]; k = tuple(np.round(h, 4))
        if k not in seen: seen.add(k); out.append([key, False, h.tolist(), G.ravel().tolist()])
    return out
def tets(key, r=R * 0.9):
    return [[key, ((sum(s) % 4) + 4) % 4 == 1, (np.array(s) * R / 2).tolist()] for s in itertools.product(range(-5, 6, 2), repeat=3) if np.linalg.norm(np.array(s) * R / 2) <= r]
core = [['env', False, [0, 0, 0]], ['ocd', False, [0, 0, 0]]]
views = {
    'two': dict(label='3 · Two-shape set', text='golden envelope (glass, OCD inside as a passenger) · grown core piece, left (green) and right (teal) — 8 round one envelope', radius=1.9,
                place=core + tets('grown')),
    'cubo': dict(label='3b · Cuboctahedron set', text='envelope · φ⁻² vertex cuboctahedra (orange; one per octahedron corner, shared by 6 octahedra) · wedges (red) · cut-down tetrahedra L/R', radius=2.0,
                 place=core + orbit('cubo') + orbit('w1') + orbit('w2') + tets('tcut')),
    'dode': dict(label='3c · Cuboctahedron + dodecahedron set', text='as 3b with each cut-down tetrahedron split: central 12-pentagon dodecahedron (purple, left/right) + shell (green/teal)', radius=2.0,
                 place=core + orbit('cubo') + orbit('w1') + orbit('w2') + tets('dode') + tets('shell')),
    'pieces3c': dict(label='3c pieces', text='envelope · cuboctahedron · wedge · dodecahedron (L, R) · shell (L, R)', radius=1.6,
                     place=[['env', False, [-1.1, 0, 0]], ['cubo', False, [0.3, 0.6, 0]], ['w1', False, [0.3, -0.3, 0]], ['dode', False, [1.0, 0.6, 0]], ['dode', True, [1.4, 0.6, 0]],
                            ['shell', False, [1.0, -0.4, 0]], ['shell', True, [1.6, -0.4, 0]]]),
}
facts = ['Golden envelope (rhombic triacontahedron) on every octahedron of the octet: envelopes never overlap and fill exactly 10/φ⁶ = 55.73% (exact). Prior art: none found so far (envelope-network note).',
         '3 · Two-shape set: envelope + grown core piece (cube of edge R minus envelopes), 0.555671 each, left and right. Fable review running.',
         '3b · Cuboctahedron set: envelope + φ⁻² vertex cuboctahedron (exactly ⅓ of the envelope, 18.58%) + wedge (0.005504) + cut-down tetrahedron L/R (256/81 − 104√5/81).',
         '3c · + dodecahedron: the cut-down tetrahedron = central dodecahedron (12 pentagons, 20 corners, exact (−146/27 + 22√5/9) = 0.058537, sphericity 0.855, only the 12 turns of the tetrahedron: left and right) + one-piece shell (0.230956, sphericity 0.48). Its pentagons carry golden angles 63.43°/116.57° with 90° and others.']
html = open(os.path.join(H, 'kit_viewer_template.html')).read()
for k, v in {'__TITLE__': 'Golden Envelope Octet', '__SUB__': 'Project 3 of the space-filling kits (DICTO 2026-10-18): golden envelopes in the octet, three sets. Drag to turn.',
             '__MARK__': 'studies/2026-10-18-p3-golden-envelope-octet', '__FACTS__': ''.join(f'<li>{f}</li>' for f in facts),
             '__DATA__': json.dumps(dict(pieces=P, views=views), separators=(',', ':'))}.items(): html = html.replace(k, v)
open(os.path.join(H, '..', 'renders', 'p3-golden-envelope-octet.html'), 'w').write(html); print('ok', len(html))
