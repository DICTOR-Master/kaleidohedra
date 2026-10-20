# DICTO 2026-10-20: pictures of the octet with an S across every face (sface_octet.py). Was: the S-curved double octet: the tetrahedron folding from its net of 2 domed (gold) and
# 2 hollow (cream) triangles, the folded piece from both sides, the octahedron (dome next to hollow) and a block of the octet. #18 standard.
import os, json, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = "if __name__ == " + "'__main__':"
exec(open(os.path.join(HERE, 'sface_octet.py')).read().split(MAIN)[0])
GOLD, CREAM, PURPLE = '#d9a334', '#f0d48a', '#a77be0'
def part(mf, col):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3]); T = np.asarray(me.tri_verts).tolist()
    return {'v': np.round(P, 5).tolist(), 't': T, 'c': [col] * len(T), 'e': None, 'a': 1.0}
def face_part(P, s, n, col):
    pts, tris = patch(np.array(P, float), s, n); return {'v': np.round(pts, 5).tolist(), 't': tris, 'c': [col] * len(tris), 'e': None, 'a': 1.0}
def rot(p, a, b, ang):
    u = (b - a) / np.linalg.norm(b - a); v = p - a
    return a + v * np.cos(ang) + np.cross(u, v) * np.sin(ang) + u * (u @ v) * (1 - np.cos(ang))
U = np.array([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)], float)
scenes = []; add = lambda t_, s_, parts: scenes.append({'title': t_, 'sub': s_, 'parts': parts})
Tp = tet(U)
add('Tetrahedron piece', 'every face half dome, half hollow', [part(Tp, GOLD)])
add('Tetrahedron piece, other side', 'the S on each face', [part(Tp.rotate([0, 0, 180]), GOLD)])
add('Octahedron piece', 'every face an S', [part(octa((1, 0, 0)), PURPLE)])
cen = np.array([1.0, 0, 0]); ps = [part(octa((1, 0, 0)), PURPLE)]
for sg in itertools.product((1, -1), repeat=3):
    sgv = np.array(sg, float); V = [cen + sgv[j] * np.eye(3)[j] for j in range(3)] + [cen + sgv]
    ps.append(part(tet(np.array(V)).translate(list(sgv * 0.45)), GOLD))
add('One octahedron, eight tetrahedra', 'drawn apart: every bump meets a dent', ps)
blk = [part(tet(V).translate(list((b_ - 0.5) * 0.25)), GOLD) for b_, V in tets_in(range(0, 2))]
for p_ in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (2, 1, 0), (2, 0, 1), (1, 2, 0), (0, 2, 1), (1, 0, 2), (0, 1, 2), (2, 1, 2), (1, 2, 2), (2, 2, 1)]:
    blk.append(part(octa(p_).translate(list((np.array(p_, float) - 1) * 0.25)), PURPLE))
add('A block of the octet', 'still filling space', blk)
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts']]); ctr = (pts.max(0) + pts.min(0)) / 2
    for p in s['parts']: p['v'] = (np.array(p['v']) - ctr).round(5).tolist()
    s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.62, 0.48, 0.62); const _unused = new THREE.Vector3(')
html = html.replace('new THREE.HemisphereLight(0xffffff, 0xb8b0a0, 0.62)', 'new THREE.HemisphereLight(0xfff4e0, 0x3a2c1c, 0.42)').replace('new THREE.DirectionalLight(0xffffff, 0.62)', 'new THREE.DirectionalLight(0xfff0d8, 0.78)').replace('new THREE.DirectionalLight(0xffffff, 0.40)', 'new THREE.DirectionalLight(0xffffff, 0.22)')
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
open(os.path.join(HERE, 'renders', 'sface-octet.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'sface-octet-labels.json'), 'w'), indent=1)
print('sface-octet.html', len(scenes))
