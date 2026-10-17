# DICTO 2026-10-18 Project 2, Penrose-core octet -- 3D page from data/p2-meshes.json -> renders/p2-penrose-core-octet.html
import json, os, itertools, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); d = json.load(open(os.path.join(H, '..', 'data', 'p2-meshes.json'))); R = d['R']
P = {'no': dict(v=d['notched_octahedron']['v'], t=d['notched_octahedron']['t'], colour='#5b8fd0'),
     'mid': dict(v=d['middle_piece']['v'], t=d['middle_piece']['t'], colour='#c8382f'),
     'tet': dict(v=d['notched_tetrahedron']['v'], t=d['notched_tetrahedron']['t'], colour='#3f9a5b', colour2='#2a9d9a')}
ops = []
for pm in ([0, 1, 2], [1, 2, 0], [2, 0, 1]):
    for sg in itertools.product((1, -1), repeat=3):
        G = np.zeros((3, 3))
        for i in range(3): G[i, pm[i]] = sg[i]
        ops.append(G)
m = np.array(d['middle_centre']); mids, seen = [], set()
for G in ops:
    h = G @ m; k = tuple(np.round(h, 4))
    if k in seen: continue
    seen.add(k); mids.append(['mid', False, h.tolist(), G.ravel().tolist()])
def tets_near(r):
    return [['tet', ((sum(s) % 4) + 4) % 4 == 1, (np.array(s) * R / 2).tolist()] for s in itertools.product(range(-5, 6, 2), repeat=3) if np.linalg.norm(np.array(s) * R / 2) <= r]
octs = [['no', False, (np.array(c) * R).tolist()] for c in itertools.product(range(-3, 4), repeat=3) if sum(c) % 2 == 0 and np.linalg.norm(np.array(c) * R) <= R * 1.5]
views = {
    'set': dict(label='The set (3 shapes)', text='notched octahedron (blue) · middle piece (red) · notched tetrahedron, left (green) and right (teal)', radius=1.5,
                place=[['no', False, [-1.0, 0, 0]], ['mid', False, [0.55, 0.45, 0]], ['tet', False, [0.95, -0.2, 0]], ['tet', True, [0.95, -0.95, 0]]]),
    'round': dict(label='Round one octahedron', text='1 notched octahedron · its 12 middle pieces (one per edge) · 8 tetrahedra', radius=1.9,
                  place=[['no', False, [0, 0, 0]]] + mids + tets_near(R * 0.9)),
    'network': dict(label='Network (middle pieces hidden)', text='notched octahedra and tetrahedra on the octet; the notches are where the middle pieces go', radius=3.2,
                    place=octs + tets_near(R * 1.8)),
}
facts = ['Notched octahedron (the OCD and its 6 notched caps fused): exact 8/57 + 104√5/171 = 1.500299, sphericity 0.621, one solid.',
         'Middle piece (whole, DICTO): hull of two facing five-kite stars minus both OCDs, exact (310 + 26√5)/4617 = 0.079735, sphericity 0.579; one per octahedron edge (6 per cell). Its central thick Penrose rhombus prism and two flanking ones are not cut out in this set.',
         'Notched tetrahedron: exact 26/81 − 2√5/81 = 0.265776, sphericity 0.517; left and right.',
         'Per cell: 1 + 6 + 2 pieces = (32 + 16√5)/27 exactly. Keyless kit proved by Fable (exact construction, 4 M points sampled).']
html = open(os.path.join(H, 'kit_viewer_template.html')).read()
for k, v in {'__TITLE__': 'Penrose-Core Octet', '__SUB__': 'Project 2 of the space-filling kits (DICTO 2026-10-18): the octet with a middle piece between facing five-fold stars on every edge, 3 shapes. Drag to turn.',
             '__MARK__': 'studies/2026-10-18-p2-penrose-core-octet', '__FACTS__': ''.join(f'<li>{f}</li>' for f in facts),
             '__DATA__': json.dumps(dict(pieces=P, views=views), separators=(',', ':'))}.items(): html = html.replace(k, v)
open(os.path.join(H, '..', 'renders', 'p2-penrose-core-octet.html'), 'w').write(html); print('ok', len(html))
