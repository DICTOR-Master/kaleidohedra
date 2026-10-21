# DICTO 2026-10-21: pictures of the OG turned out, golden step (float copies of the exact solids in golden-exact.json), #18 standard.
# Adapted from cleo-towers/tower_figs.py. Extra scene: the 80 Aktis shortened to 1/phi and flipped out over the OG's faces.
# Each tower = cone from the centre over a face of the inner solid, cut by the outer solid. Scenes: the CLEO sphere core; each shell's towers
# on their inner solid; all five shells, half cut away, shells alternating gold and purple.
import os, sys, json, itertools
import numpy as np, manifold3d as m3
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(HERE, 'golden-exact.json')))
B = {k: np.array(v, float) for k, v in D['boundaries_float'].items()}; order = ['OG', 'phi TPH', 'phi^2 TQH', 'phi^4 TQHD']; D['beats'] = [1, 1, 2]
GOLD, PURPLE, CORE = '#d9a334', '#a77be0', '#f0d48a'
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
def faces(P):
    h = ConvexHull(P); groups = {}
    for simp, eq in zip(h.simplices, h.equations): groups.setdefault(tuple(np.round(eq, 6)), set()).update(simp)
    return [sorted(ix) for ix in groups.values()]
def towers(inner, outer):
    out = hull(outer); R = np.linalg.norm(outer, axis=1).max() * 3
    for ix in faces(inner):
        F = inner[ix]; cone = hull(np.vstack([F * 0.0001, F / np.linalg.norm(F, axis=1)[:, None] * R]))
        t = cone ^ out
        t = t - hull(np.vstack([np.zeros(3), F]))           # beyond the face: take away the pyramid from the centre to the face
        d = F.mean(0); d = d / np.linalg.norm(d)
        yield t, len(ix), d
def mf_part(mf, col, a=1.0):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3]); T = np.asarray(me.tri_verts).tolist()
    return {'v': np.round(P, 5).tolist(), 't': T, 'c': [col] * len(T), 'e': None, 'a': a}
scenes = []; add = lambda t, s, parts: scenes.append({'title': t, 'sub': s, 'parts': parts})
core = hull(B[order[0]])
add('The OG core', '20 Hex Aktis + 60 Deltoid Aktis, tips at the centre', [mf_part(core, CORE)])
phi = (1 + 5 ** .5) / 2; spikes = []
for ix in faces(B['OG']):
    F = B['OG'][ix]; n = np.cross(F[1] - F[0], F[2] - F[0]); n /= np.linalg.norm(n); n = n if n @ F[0] > 0 else -n
    tip = phi * (F[0] @ n) * n; spikes.append(mf_part(hull(np.vstack([F, tip])), GOLD if len(ix) == 6 else PURPLE))
add('The Aktis turned out', 'each Aktis at 1/phi height, flipped over its face', [mf_part(core, CORE)] + spikes)
cols = [PURPLE, GOLD, PURPLE, GOLD, PURPLE]; allparts = [mf_part(core, CORE)]
cut = m3.Manifold.cube([200, 200, 200]).translate([-100, -100, 0])        # keep z <= 0: half cut away
for k, (a, b) in enumerate(zip(order, order[1:])):
    ts = list(towers(B[a], B[b])); beats = D['beats'][k]; gap = 0.07 * np.linalg.norm(B[b], axis=1).max()
    add(f'Shell {k + 1}: {beats} beat{"s" if beats > 1 else ""}', f'{a} to {b} · {len(ts)} towers', [mf_part(core if k == 0 else hull(B[a]), CORE, 0.35)] + [mf_part(t.translate(list(d * gap)), cols[k]) for t, _, d in ts])
    shift = 0.035 * (k + 1) * np.linalg.norm(B[order[1]], axis=1).max()
    allparts += [mf_part((t - cut).translate(list(d * shift)), cols[k]) for t, _, d in ts if not (t - cut).is_empty()]
allparts[0] = mf_part(core - cut, CORE)
add('OG turned out, golden step', 'shells 1, 1, 2 beats, half cut away', allparts)
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts'] if p['v']]); ctr = (pts.max(0) + pts.min(0)) / 2
    for p in s['parts']: p['v'] = (np.array(p['v']) - ctr).round(5).tolist() if p['v'] else []
    s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.62, 0.48, 0.62); const _unused = new THREE.Vector3(')
html = html.replace('new THREE.HemisphereLight(0xffffff, 0xb8b0a0, 0.62)', 'new THREE.HemisphereLight(0xfff4e0, 0x3a2c1c, 0.42)').replace('new THREE.DirectionalLight(0xffffff, 0.62)', 'new THREE.DirectionalLight(0xfff0d8, 0.78)').replace('new THREE.DirectionalLight(0xffffff, 0.40)', 'new THREE.DirectionalLight(0xffffff, 0.22)')
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
open(os.path.join(HERE, 'renders', 'golden.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'golden-labels.json'), 'w'), indent=1)
print('golden.html', len(scenes))
