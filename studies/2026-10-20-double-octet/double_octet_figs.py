# DICTO 2026-10-20: pictures of the double octet set (faceted): the tetrahedron piece, the octahedron piece, an octahedron with its 8
# tetrahedra drawn apart, and a block of the octet. #18 standard: dark ground, tetrahedron pieces gold, octahedron pieces purple.
import os, json, itertools, numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'double_octet_patch.py')).read().split("pieces = []")[0])
GOLD, PURPLE = '#d9a334', '#a77be0'
def part(mf, col, a=1.0):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3]); T = np.asarray(me.tri_verts).tolist()
    return {'v': np.round(P, 5).tolist(), 't': T, 'c': [col] * len(T), 'e': None, 'a': a}
scenes = []; add = lambda t, s, parts: scenes.append({'title': t, 'sub': s, 'parts': parts})
T0 = tet_piece(np.array([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)], float)); O0 = oct_piece((1, 0, 0))
add('Tetrahedron piece, bump side', '2 convex faces, towards +x', [part(T0, GOLD)])
add('Tetrahedron piece, dent side', '2 concave faces, towards -x', [part(T0.rotate([0, 0, 180]), GOLD)])
add('Octahedron piece, bump side', '4 convex faces, towards +x', [part(O0, PURPLE)])
add('Octahedron piece, dent side', '4 concave faces, towards -x', [part(O0.rotate([0, 0, 180]), PURPLE)])
cen = np.array([1.0, 0, 0]); ps = [part(O0, PURPLE)]
for sg in itertools.product((1, -1), repeat=3):
    sg = np.array(sg, float); V = [cen + sg[j] * np.eye(3)[j] for j in range(3)] + [cen + sg]
    ps.append(part(tet_piece(np.array(V)).translate(list(sg * 0.45)), GOLD))
add('One octahedron, eight tetrahedra', 'drawn apart: every bump meets a dent', ps)
blk = []
for x, y, z in itertools.product(range(0, 2), repeat=3):
    base = np.array([x, y, z], float); corners = [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)] if (x + y + z) % 2 == 0 else [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]
    blk.append(part(tet_piece(base + np.array(corners, float)).translate(list((base - 0.5) * 0.25)), GOLD))
for x, y, z in itertools.product(range(0, 3), repeat=3):
    if (x + y + z) % 2 and max(x, y, z) <= 2 and (x, y, z) in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (2, 1, 0), (2, 0, 1), (1, 2, 0), (0, 2, 1), (1, 0, 2), (0, 1, 2), (2, 1, 2), (1, 2, 2), (2, 2, 1)]:
        c_ = np.array([x, y, z], float); blk.append(part(oct_piece((x, y, z)).translate(list((c_ - 1) * 0.25)), PURPLE))
add('A block of the octet', 'tetrahedron and octahedron pieces, slightly apart', blk)
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts']]); ctr = (pts.max(0) + pts.min(0)) / 2
    for p in s['parts']: p['v'] = (np.array(p['v']) - ctr).round(5).tolist()
    s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.62, 0.48, 0.62); const _unused = new THREE.Vector3(')
html = html.replace('new THREE.HemisphereLight(0xffffff, 0xb8b0a0, 0.62)', 'new THREE.HemisphereLight(0xfff4e0, 0x3a2c1c, 0.42)').replace('new THREE.DirectionalLight(0xffffff, 0.62)', 'new THREE.DirectionalLight(0xfff0d8, 0.78)').replace('new THREE.DirectionalLight(0xffffff, 0.40)', 'new THREE.DirectionalLight(0xffffff, 0.22)')
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
open(os.path.join(HERE, 'renders', 'double-octet.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'double-octet-labels.json'), 'w'), indent=1)
print('double-octet.html', len(scenes))
