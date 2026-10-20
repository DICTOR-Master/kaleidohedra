# DICTO 2026-10-20: figures for the DICTO Jewel paper. Float copies of the exact pieces of jewel_exact.py (raw frame: cells of edge 2
# centred on 2(i,j,k)); the Jewel's faces as in studies/2026-10-19-og-gyrated-octet/jewel_twin.py; Hexa-Key and carved roofs with manifold3d.
# Jewel triangles gold, its windows (thick rhombi) blue, stellas violet, the Hexa-Key teal. Writes renders/jewel.html (window.show(i))
# and renders/jewel-labels.json; shots: ../2026-10-19-five-fold-octet/shots.mjs; compose: jewel_compose.py.
import os, sys, json, itertools
import numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__)); GYR = sys.argv[1]
exec(open(os.path.join(GYR, 'jewel_twin.py')).read().split("V = np.array(verts)")[0])
JV = np.array(verts); JF = faces                                     # 38 corners; 12 rhombi + 48 triangles
assert len(JV) == 38 and len(JF) == 60
GOLD, BLUE, VIOLET, TEAL, GREY = '#e0ae2c', '#4f8fd6', '#8e6cc9', '#2a9d9a', '#d8d2c4'
hull = lambda P: m3.Manifold.hull_points(np.asarray(P, float))
def jewel_part(c, gold=GOLD, blue=BLUE):
    V = JV + c; tris, cols, edges = [], [], []
    for o in JF:
        col = blue if len(o) == 4 else gold
        for a, b in zip(o[1:-1], o[2:]): tris.append([o[0], a, b]); cols.append(col)
        edges += [[o[i], o[(i + 1) % len(o)]] for i in range(len(o))]
    return {'v': np.round(V, 5).tolist(), 't': tris, 'c': cols, 'e': edges, 'a': 1.0}
def stella_mf(c):
    T1 = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]; T2 = [(-x, -y, -z) for x, y, z in T1]
    return hull(np.array(T1, float) + c) + hull(np.array(T2, float) + c)
def mf_part(mf, col, alpha=1.0):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3]); T = np.asarray(me.tri_verts).tolist()
    return {'v': np.round(P, 5).tolist(), 't': T, 'c': [col] * len(T), 'e': None, 'a': alpha}
def roof_toward(cnb, cq):
    """uncarved roof of the Jewel in cell cnb on its face toward cell cq (corners from the Jewel's own ridge points)"""
    ax = int(np.argmax(np.abs(cq - cnb))); s = np.sign(cq[ax] - cnb[ax])
    sq = [v for v in itertools.product((1, -1), repeat=3) if v[ax] == s]
    rid = [v for v in JV if abs(v[ax] - s * PHI) < 1e-9]
    return hull(np.vstack([np.array(sq, float), rid]) + cnb)
def carved_roof(cnb, cq): return roof_toward(cnb, cq) - stella_mf(cq)
def shift(p, d):
    q = dict(p); q['v'] = (np.array(p['v']) + d).tolist(); return q
cells = lambda pts: [np.array(c, float) * 2 for c in pts]
scenes = []
def add(title, sub, parts): scenes.append({'title': title, 'sub': sub, 'parts': parts})
# 0 the Jewel
add('The DICTO Jewel', '38 corners · 12 windows (thick rhombi) + 48 triangles · 3/16', [jewel_part(np.zeros(3))])
# 1 the odd cell: its stella and the 6 carved roofs of its Jewel neighbours, pulled apart
O = np.zeros(3); parts = [mf_part(stella_mf(O), VIOLET)]
for k in range(3):                                # the three roofs on the faces toward the viewer, drawn out (the other three are the same)
    nb = np.zeros(3); nb[k] = 2; cr = carved_roof(nb, O)
    parts.append(mf_part(cr.translate(list(np.eye(3)[k] * 1.6)), GOLD))
add('A stella cell, opened', 'the stella 1/16 and three of its six carved roofs, 1/96 each: together the cell, 1/8', parts)
# 2 the Stella–Jewel Lattice: a 2 x 2 x 2 block, slightly apart
parts = []
for c in itertools.product((0, 1), repeat=3):
    ctr = np.array(c, float) * 2 * 1.18
    parts.append(jewel_part(ctr) if sum(c) % 2 == 0 else mf_part(stella_mf(ctr), VIOLET))
add('The Stella–Jewel Lattice', 'Jewels on even cells, stellas on odd · 3 : 1 by volume', parts)
# 3 tetrahedral cluster, 4 octahedral cluster, 5 rhombohedron
add('DICTO Jewel-Tetra', '4 Jewels, one window between each pair · 228 faces · 3/4', [jewel_part(c) for c in cells([(0, 0, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1)])])
OC = np.array([2.0, 2, 2]); octc = [(2, 1, 1), (0, 1, 1), (1, 2, 1), (1, 0, 1), (1, 1, 2), (1, 1, 0)]
add('DICTO Jewel-Octa, opened', '6 Jewels and the stella that fills their hole · 288 faces · 19/16',
    [mf_part(stella_mf(OC), VIOLET)] + [jewel_part(OC + (c - OC) * 1.3) for c in cells(octc)])
rh = [tuple(sum(x) for x in zip(*[v for v, s in zip([(1, 1, 0), (1, 0, 1), (0, 1, 1)], m) if s] or [(0, 0, 0)])) for m in itertools.product((0, 1), repeat=3)]
add('DICTO Jewel-Rhombi', '8 Jewels on 18 windows, a stella sealed inside · 396 faces · 25/16', [jewel_part(c) for c in cells(rh)])
# 6 the Hexa, 7 the Hexa-Key, 8 a Hexa and a Hexa-Key side by side
cube_cells = list(itertools.product((0, 1), repeat=3))
add('DICTO Hexa', '8 Jewels on a 2 x 2 x 2 block, one solid · 24 roofs · 5/4', [jewel_part(c) for c in cells(cube_cells)])
def key_mf(off):
    B = m3.Manifold.cube([4, 4, 4]).translate([-1 + off[0], -1 + off[1], -1 + off[2]])
    cut = None; S = None
    for c in cube_cells:
        cc = np.array(c, float) * 2 + off; s_ = stella_mf(cc); S = s_ if S is None else S + s_
        for k in range(3):
            nb = cc.copy(); nb[k] += 2 * (1 if c[k] == 1 else -1); r_ = roof_toward(nb, cc)
            cut = r_ if cut is None else cut + r_
    return (B - cut) + S
K = key_mf(np.zeros(3)); assert abs(K.volume() - 48) < 1e-6, K.volume()
add('DICTO Hexa-Key', '8 stellas + 12 double roofs, one solid · 24 recesses · 3/4', [mf_part(K, TEAL)])
pair = [jewel_part(c) for c in cells(cube_cells)] + [mf_part(key_mf(np.array([4.0, 0, 0])).translate([1.6, 0, 0]), TEAL)]   # the Hexa-Key in its own place next to the Hexa, drawn out by 1.6
add('Hexa and Hexa-Key', 'the Hexa\'s roofs fit the Hexa-Key\'s recesses · 5 : 3', pair)
# 9 the octet pattern: a Jewel-Octa (its stella hidden inside) and the 8 Jewels that complete its faces to Jewel-Tetras
nbr = lambda a, b: sorted(abs(x - y) for x, y in zip(a, b)) == [0, 1, 1]
capc = sorted({c for t in itertools.combinations(octc, 3) if all(nbr(a, b) for a, b in itertools.combinations(t, 2))
               for c in itertools.product(range(-1, 4), repeat=3) if sum(c) % 2 == 0 and c not in octc and all(nbr(c, x) for x in t)})
assert len(capc) == 8
add('The octet pattern', 'a Jewel-Octa (gold) and the 8 Jewels (grey) completing its faces to Jewel-Tetras, drawn out', [jewel_part(c) for c in cells(octc)] + [jewel_part(OC + (c - OC) * 1.35, gold=GREY) for c in cells(capc)])
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts']]); ctr = (pts.max(0) + pts.min(0)) / 2
    for p in s['parts']: p['v'] = (np.array(p['v']) - ctr).round(5).tolist()
    s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.62, 0.48, 0.62); const _unused = new THREE.Vector3(')
html = html.replace('new THREE.HemisphereLight(0xffffff, 0xb8b0a0, 0.62)', 'new THREE.HemisphereLight(0xffffff, 0xa89f8c, 0.46)').replace('new THREE.DirectionalLight(0xffffff, 0.62)', 'new THREE.DirectionalLight(0xffffff, 0.9)')
os.makedirs(os.path.join(HERE, 'renders'), exist_ok=True)
open(os.path.join(HERE, 'renders', 'jewel.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'jewel-labels.json'), 'w'), indent=1, ensure_ascii=False)
print('jewel.html', len(scenes), 'scenes; key volume', round(K.volume(), 6))
