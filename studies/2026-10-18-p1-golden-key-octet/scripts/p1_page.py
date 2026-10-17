# DICTO 2026-10-18 Project 1, Golden-key octet -- 3D page from data/p1-meshes.json -> renders/p1-golden-key-octet.html (kit_viewer_template.html)
import json, os, itertools, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); d = json.load(open(os.path.join(H, '..', 'data', 'p1-meshes.json'))); R = d['R']
P = {'ko': dict(v=d['keyed_octahedron']['v'], t=d['keyed_octahedron']['t'], colour='#d9a21b'),
     'tet': dict(v=d['dented_tetrahedron']['v'], t=d['dented_tetrahedron']['t'], colour='#3f9a5b', colour2='#2a9d9a')}
def tets_near(r):
    out = []
    for s in itertools.product(range(-5, 6, 2), repeat=3):
        p = np.array(s) * R / 2
        if np.linalg.norm(p) <= r: out.append(['tet', ((sum(s) % 4) + 4) % 4 == 1, p.tolist()])
    return out
def octs_near(r):
    return [['ko', False, (np.array(c) * R).tolist()] for c in itertools.product(range(-3, 4), repeat=3) if sum(c) % 2 == 0 and np.linalg.norm(np.array(c) * R) <= r]
views = {
    'set': dict(label='The set (2 shapes)', text='keyed octahedron (gold) · dented tetrahedron, left (green) and right (teal)', radius=1.4,
                place=[['ko', False, [-0.9, 0, 0]], ['tet', False, [0.75, 0.25, 0]], ['tet', True, [0.75, -0.75, 0]]]),
    'round': dict(label='Round one octahedron', text='1 keyed octahedron · its 8 tetrahedra (4 left, 4 right)', radius=1.8,
                  place=[['ko', False, [0, 0, 0]]] + [t for t in tets_near(R * 0.9)]),
    'network': dict(label='Network', text='keyed octahedra on the fcc lattice, tetrahedra between: fills space exactly', radius=3.2,
                    place=octs_near(R * 1.5) + tets_near(R * 1.8)),
}
facts = ['Keyed octahedron: the octahedron |x|+|y|+|z| ≤ 2φ/3 with its 8 golden-envelope corner keys, exact volume −32/9 + 64√5/27 = 1.744754, sphericity 0.852.',
         'Dented tetrahedron: regular tetrahedron with 4 key dents, exact 64/27 − 8√5/9 = 0.382754, sphericity 0.620; left and right (mirror images, Fable).',
         'Per cell: 1 keyed octahedron + 2 tetrahedra = (32 + 16√5)/27 exactly. The keys\' base corners sit at the golden-section points (φ : 1) of the octahedron edges.',
         'Tiling proved exactly by Fable (fable-review, ba28bd0); fusing the OCD and its caps into the octahedron does not change it.']
html = open(os.path.join(H, 'kit_viewer_template.html')).read()
for k, v in {'__TITLE__': 'Golden-Key Octet', '__SUB__': 'Project 1 of the space-filling kits (DICTO 2026-10-18): the octet truss with golden keys, 2 shapes. Drag to turn.',
             '__MARK__': 'studies/2026-10-18-p1-golden-key-octet', '__FACTS__': ''.join(f'<li>{f}</li>' for f in facts),
             '__DATA__': json.dumps(dict(pieces=P, views=views), separators=(',', ':'))}.items(): html = html.replace(k, v)
open(os.path.join(H, '..', 'renders', 'p1-golden-key-octet.html'), 'w').write(html); print('ok', len(html))
