# DICTO 2026-10-20: pictures of the double octet set, ROUNDED (alternating octahedron faces; convex and hollow tetrahedra). Was: faceted: the tetrahedron piece, the octahedron piece, an octahedron with its 8
# tetrahedra drawn apart, and a block of the octet. #18 standard: dark ground, tetrahedron pieces gold, octahedron pieces purple.
import os, json, itertools, numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'domed_octet.py')).read().split("if __name__ == '__main__':")[0])
GOLD, PURPLE = '#d9a334', '#a77be0'
def part(mf, col, a=1.0):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3]); T = np.asarray(me.tri_verts).tolist()
    return {'v': np.round(P, 5).tolist(), 't': T, 'c': [col] * len(T), 'e': None, 'a': a}
scenes = []; add = lambda t, s, parts: scenes.append({'title': t, 'sub': s, 'parts': parts})
CREAM = '#f0d48a'
U = [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
Tv, Th, O0 = tet(U, True), tet(U, False), octa((1, 0, 0))
add('Rounded tetrahedron', 'all 4 faces domed (Meissner-like)', [part(Tv, GOLD)])
add('Hollow tetrahedron', 'all 4 faces hollowed, its opposite', [part(Th, CREAM)])
add('Octahedron, domed side', 'faces alternate: dome next to hollow', [part(O0, PURPLE)])
add('Octahedron, hollow side', 'the other 4 faces', [part(O0.rotate([0, 0, 90]), PURPLE)])
cen = np.array([1.0, 0, 0]); ps = [part(O0, PURPLE)]
for sg in itertools.product((1, -1), repeat=3):
    sgv = np.array(sg, float); V = [cen + sgv[j] * np.eye(3)[j] for j in range(3)] + [cen + sgv]
    cv = tuple(sg) not in T_PLUS                     # the octahedron's hollow faces take a rounded tetrahedron's dome
    ps.append(part(tet(V, cv).translate(list(sgv * 0.45)), GOLD if cv else CREAM))
add('One octahedron, eight tetrahedra', 'drawn apart: rounded (gold) and hollow (cream) in turn', ps)
blk = []
for x, y, z in itertools.product(range(0, 2), repeat=3):
    base = np.array([x, y, z], float); corners = [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)] if (x + y + z) % 2 == 0 else [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]
    V = base + np.array(corners, float); c = V.mean(0)
    normals = {tuple(int(v) for v in np.sign(np.array(V[list(f)]).mean(0) - c)) for f in itertools.combinations(range(4), 3)}
    cv = normals <= T_PLUS
    blk.append(part(tet(V, cv).translate(list((base - 0.5) * 0.25)), GOLD if cv else CREAM))
for p_ in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (2, 1, 0), (2, 0, 1), (1, 2, 0), (0, 2, 1), (1, 0, 2), (0, 1, 2), (2, 1, 2), (1, 2, 2), (2, 2, 1)]:
    c_ = np.array(p_, float); blk.append(part(octa(p_).translate(list((c_ - 1) * 0.25)), PURPLE))
add('A block of the octet', 'slightly apart', blk)
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts']]); ctr = (pts.max(0) + pts.min(0)) / 2
    for p in s['parts']: p['v'] = (np.array(p['v']) - ctr).round(5).tolist()
    s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.62, 0.48, 0.62); const _unused = new THREE.Vector3(')
html = html.replace('new THREE.HemisphereLight(0xffffff, 0xb8b0a0, 0.62)', 'new THREE.HemisphereLight(0xfff4e0, 0x3a2c1c, 0.42)').replace('new THREE.DirectionalLight(0xffffff, 0.62)', 'new THREE.DirectionalLight(0xfff0d8, 0.78)').replace('new THREE.DirectionalLight(0xffffff, 0.40)', 'new THREE.DirectionalLight(0xffffff, 0.22)')
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
open(os.path.join(HERE, 'renders', 'domed-octet.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'domed-octet-labels.json'), 'w'), indent=1)
print('domed-octet.html', len(scenes))
