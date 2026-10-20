# DICTO 2026-10-20: figures for the Sunstar paper. Float copies of the exact pieces of sunstar_exact.py / sunstar_clusters.py (raw frame:
# cells of edge 2 centred on 2(i,j,k)); the great star from the exact stellation cells (sunstar-exact.json). Colours as the app's Sunstar
# DICTO 2026-10-20: the #18 (DICTO Hexa) standard: dark ground, gold dodecahedra, purple gap pieces (Dogstars, the Key), strong side light;
# the great star pale gold, see-through. Writes renders/sunstar.html (window.show(i)) and
# renders/sunstar-labels.json; shots: jewel-shots.mjs (2x); compose: sunstar_compose.py.
import os, sys, json, itertools
import numpy as np, manifold3d as m3
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); PHI = (1 + 5 ** .5) / 2
GOLD, ORANGE, VIOLET, GREY = '#d9a334', '#a77be0', '#f0d48a', '#8f877a'   # ORANGE now holds the purple of the gap pieces
C8 = np.array(list(itertools.product((1, -1), repeat=3)), float)
RID = np.array([r for a in (1, -1) for b in (1, -1) for r in ([0, a / PHI, b * PHI], [a / PHI, b * PHI, 0], [b * PHI, 0, a / PHI])], float)
DOD = np.vstack([C8, RID])
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
at = lambda c: np.array(c, float) * 2
def dod_part(c, col=GOLD, s=1.0, ctr=None):
    """a regular dodecahedron as 12 pentagons with their edges"""
    V = DOD * s + (at(c) if ctr is None else ctr); h = ConvexHull(V); groups = {}
    for simp, eq in zip(h.simplices, h.equations): groups.setdefault(tuple(np.round(eq, 6)), set()).update(simp)
    tris, cols, edges = [], [], []
    for eq, idx in groups.items():
        idx = [int(i) for i in idx]; P = V[idx]; m = P.mean(0); n = np.array(eq[:3]); u = P[0] - m; u /= np.linalg.norm(u); w = np.cross(n, u)
        idx = [i for _, i in sorted(zip([np.arctan2((V[i] - m) @ w, (V[i] - m) @ u) for i in idx], idx))]
        for a, b in zip(idx[1:-1], idx[2:]): tris.append([idx[0], a, b]); cols.append(col)
        edges += [[idx[i], idx[(i + 1) % len(idx)]] for i in range(len(idx))]
    return {'v': np.round(V, 5).tolist(), 't': tris, 'c': cols, 'e': edges, 'a': 1.0}
def roof(cn, cq, s=1.0, base=None):
    ax = int(np.argmax(np.abs(np.array(cq, float) - np.array(cn, float)))); sg = np.sign(cq[ax] - cn[ax])
    o = at(cn) * s if base is None else base
    return hull(np.vstack([C8[C8[:, ax] == sg], RID[np.isclose(RID[:, ax], sg * PHI)]]) * s + o)
def dogstar_mf(c, s=1.0, off=np.zeros(3)):
    m = m3.Manifold.cube([2 * s] * 3).translate(list(at(c) * s - s + off))
    for k in range(3):
        for d in (1, -1):
            n = list(c); n[k] += d; m = m - roof(tuple(n), c, s, at(n) * s + off)
    return m
def mf_part(mf, col, alpha=1.0):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3]); T = np.asarray(me.tri_verts).tolist()
    return {'v': np.round(P, 5).tolist(), 't': T, 'c': [col] * len(T), 'e': None, 'a': alpha}
def union(ms):
    u = ms[0]
    for m in ms[1:]: u = u + m
    return u
cells = lambda pts: [tuple(p) for p in pts]
scenes = []
def add(title, sub, parts): scenes.append({'title': title, 'sub': sub, 'parts': parts})
E6 = [tuple(d * (i == k) for i in range(3)) for k in range(3) for d in (1, -1)]
# 0 the Dogstar, 1 the Sunstar, 2 the lattice
add('The Dogstar', 'the hole between the dodecahedra (Hart\'s stellation 8) · 12 face planes', [mf_part(dogstar_mf((1, 0, 0)), ORANGE)])
add('The Sunstar', 'a dodecahedron and the 6 Dogstars on its faces', [dod_part((0, 0, 0))] + [mf_part(dogstar_mf(e), ORANGE) for e in E6])
parts = []
for c in itertools.product((0, 1), repeat=3):
    sh = np.array(c, float) * 2 * 0.18
    parts.append(dod_part(c, ctr=at(c) + sh) if sum(c) % 2 == 0 else mf_part(dogstar_mf(c, off=sh), ORANGE))
add('The Sunstar Lattice', 'dodecahedra on even cells, Dogstars on odd', parts)
# 3 the Dogstar round its core, 4 the Star Chain Reaction
J = json.load(open(os.path.join(HERE, 'sunstar-exact.json'))); G = [np.array(c) for c in J['gsd_cells_float']]
s3 = 1 / PHI ** 3
add('Dogstar and its core', 'a partial stellation of the dodecahedron 1/φ³ the size (core gold)',
    [dod_part((0, 0, 0), s=s3, ctr=np.zeros(3)), mf_part(dogstar_mf((0, 0, 0)), ORANGE, 0.42)])
gsd = union([hull(c) for c in G])
small = [dod_part((0, 0, 0), s=s3, ctr=np.zeros(3))] + [mf_part(dogstar_mf(e, s3), ORANGE) for e in E6]
add('Star Chain Reaction', 'a Sunstar 1/φ³ the size fits the great star exactly', small + [mf_part(gsd, VIOLET, 0.16)])
# 5-8 the clusters
tet = [(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)]; octa = [(2, 1, 1), (0, 1, 1), (1, 2, 1), (1, 0, 1), (1, 1, 2), (1, 1, 0)]
rh = [tuple(sum(x) for x in zip(*[v for v, s in zip([(1, 1, 0), (1, 0, 1), (0, 1, 1)], m) if s] or [(0, 0, 0)])) for m in itertools.product((0, 1), repeat=3)]
OC = at((1, 1, 1))
add('DICTO Sunstar-Tetra', '4 dodecahedra, one rhombus between each pair', [dod_part(c) for c in tet])
add('DICTO Sunstar-Octa, opened', '6 dodecahedra and the Dogstar that fills their hole', [mf_part(dogstar_mf((1, 1, 1)), ORANGE)] + [dod_part(c, ctr=OC + (at(c) - OC) * 1.3) for c in octa])
add('DICTO Sunstar-Rhombi', '8 dodecahedra on 18 rhombi, a Dogstar sealed inside', [dod_part(c) for c in rh])
nbr = lambda a, b: sorted(abs(x - y) for x, y in zip(a, b)) == [0, 1, 1]
capc = sorted({c for t in itertools.combinations(octa, 3) if all(nbr(a, b) for a, b in itertools.combinations(t, 2))
               for c in itertools.product(range(-1, 4), repeat=3) if sum(c) % 2 == 0 and c not in octa and all(nbr(c, x) for x in t)})
add('The octet pattern', 'a Sunstar-Octa and 8 grey dodecahedra that make its faces Sunstar-Tetras',
    [dod_part(c) for c in octa] + [dod_part(c, col=GREY, ctr=OC + (at(c) - OC) * 1.35) for c in capc])
# 9-11 the Sunstar-Hexa and Sunstar-Hexa-Key
blk = list(itertools.product((0, 1), repeat=3))
add('DICTO Sunstar-Hexa', '8 whole dodecahedra on a 2 x 2 x 2 block, one solid', [mf_part(union([hull(DOD + at(c)) for c in blk]), GOLD)])
def key_mf(off):
    kb = [tuple(c[i] + off[i] for i in range(3)) for c in blk]
    k = m3.Manifold.cube([4, 4, 4]).translate(list(at(kb[0]) - 1))
    for c in kb:
        for kk in range(3):
            for d in (1, -1):
                n = list(c); n[kk] += d; n = tuple(n)
                if n not in kb: k = k - roof(n, c)
    return k
K = key_mf((2, 0, 0)); assert abs(K.volume() - (56 - 8 * 5 ** .5)) < 1e-6, K.volume()
add('DICTO Sunstar-Hexa-Key', '8 Dogstars + 12 double roofs, one solid', [mf_part(K, ORANGE)])
add('Sunstar-Hexa and Sunstar-Hexa-Key', 'the Sunstar-Hexa\'s roofs fill the Key\'s recesses', [mf_part(union([hull(DOD + at(c)) for c in blk]), GOLD), mf_part(K.translate([1.6, 0, 0]), ORANGE)])
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts']]); ctr = (pts.max(0) + pts.min(0)) / 2
    for p in s['parts']: p['v'] = (np.array(p['v']) - ctr).round(5).tolist()
    s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.62, 0.48, 0.62); const _unused = new THREE.Vector3(')
html = html.replace('new THREE.HemisphereLight(0xffffff, 0xb8b0a0, 0.62)', 'new THREE.HemisphereLight(0xfff4e0, 0x3a2c1c, 0.42)').replace('new THREE.DirectionalLight(0xffffff, 0.62)', 'new THREE.DirectionalLight(0xfff0d8, 0.78)').replace('new THREE.DirectionalLight(0xffffff, 0.40)', 'new THREE.DirectionalLight(0xffffff, 0.22)')
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
open(os.path.join(HERE, 'renders', 'sunstar.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'sunstar-labels.json'), 'w'), indent=1, ensure_ascii=False)
print('sunstar.html', len(scenes), 'scenes')
