# DICTO 2026-10-20: pictures of the sphere + filler set (sphere_octet.py). #18 standard: spheres purple, fillers gold.
import os, json, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = "if __name__ == " + "'__main__':"
exec(open(os.path.join(HERE, 'roundtet_octet.py')).read().split(MAIN)[0])
GOLD, PURPLE = '#d9a334', '#a77be0'
def part(mf, col):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3]); T = np.asarray(me.tri_verts).tolist()
    return {'v': np.round(P, 5).tolist(), 't': T, 'c': [col] * len(T), 'e': None, 'a': 1.0}
scenes = []; add = lambda t_, s_, parts: scenes.append({'title': t_, 'sub': s_, 'parts': parts})
S0 = sphere_piece((1, 0, 0)); F0 = filler(np.array([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)], float))
add('The ball', '8 dimples, meets its neighbours at 120 deg', [part(S0, PURPLE)])
add('The ball, turned', 'the other side', [part(S0.rotate([0, 0, 90]), PURPLE)])
add('The small rounded tetrahedron', '4 bumps', [part(F0, GOLD)])
add('The rounded tetrahedron, turned', 'rounded corners and edges', [part(F0.rotate([0, 0, 180]), GOLD)])
cen = np.array([1.0, 0, 0]); ps = [part(S0, PURPLE)]
for sg in itertools.product((1, -1), repeat=3):
    sgv = np.array(sg, float); V = [cen + sgv[j] * np.eye(3)[j] for j in range(3)] + [cen + sgv]
    ps.append(part(filler(np.array(V)).translate(list(sgv * 0.5)), GOLD))
add('One ball, eight rounded tetrahedra', 'drawn apart', ps)
blk = [part(filler(V).translate(list((b_ - 0.5) * 0.3)), GOLD) for b_, V in tets_in(range(0, 2))]
for p_ in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (2, 1, 0), (2, 0, 1), (1, 2, 0), (0, 2, 1), (1, 0, 2), (0, 1, 2), (2, 1, 2), (1, 2, 2), (2, 2, 1)]:
    blk.append(part(sphere_piece(p_).translate(list((np.array(p_, float) - 1) * 0.3)), PURPLE))
add('A block', 'balls and rounded tetrahedra, slightly apart', blk)
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts']]); ctr = (pts.max(0) + pts.min(0)) / 2
    for p in s['parts']: p['v'] = (np.array(p['v']) - ctr).round(5).tolist()
    s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.62, 0.48, 0.62); const _unused = new THREE.Vector3(')
html = html.replace('new THREE.HemisphereLight(0xffffff, 0xb8b0a0, 0.62)', 'new THREE.HemisphereLight(0xfff4e0, 0x3a2c1c, 0.42)').replace('new THREE.DirectionalLight(0xffffff, 0.62)', 'new THREE.DirectionalLight(0xfff0d8, 0.78)').replace('new THREE.DirectionalLight(0xffffff, 0.40)', 'new THREE.DirectionalLight(0xffffff, 0.22)')
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
open(os.path.join(HERE, 'renders', 'roundtet-octet.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'roundtet-octet-labels.json'), 'w'), indent=1)
print('roundtet-octet.html', len(scenes))
