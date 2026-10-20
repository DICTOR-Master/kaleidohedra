# DICTO 2026-10-21: a packing partner for the straightened B1NR ("it forms a kind of fat triangle, I wonder if there is a complementary
# shape"; chose "a partner that packs"). The fat triangles are laid like a floor of triangles: centres on a honeycomb, neighbours turned
# 180 degrees, every square face against a neighbour's square. Layers stack straight up, ring triangle on ring triangle. The space left
# gathers round the floor's corners (where 6 fat triangles meet); the partner is that space cut by the hexagonal cell round each corner
# (walls through the 6 B1NR centres, one layer high), so all partners are the same shape. Checks: no B1NR overlaps, one piece per cell,
# volumes add up to the cell.
import os, json, itertools, numpy as np, manifold3d as m3
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'b1nr_flat.py')).read(); exec(src[:src.index('def mvc')])
V = np.load(os.path.join(HERE, 'b1nr-flat.npy')); V = V - V.mean(0)                                           # centroid = symmetry centre
sq = [f for k, f in faces if k == 'sq']; N = []
for f in sq:
    c = V[f].mean(0); n = np.linalg.svd(V[f] - c)[2][-1]; n = n if n @ c > 0 else -n; N.append((n, c @ n))
assert all(abs(n[2]) < 1e-3 for n, _ in N), 'square faces should be upright'
d = np.mean([dd for _, dd in N]); a0 = np.arctan2(N[0][0][1], N[0][0][0])   # exact 120-degree directions (the numerical solid is D3h to ~1e-4)
n0, n1, n2 = [np.array([np.cos(a0 + s_ * 2 * np.pi / 3), np.sin(a0 + s_ * 2 * np.pi / 3), 0]) for s_ in (0, 1, 2)]; H = V[:, 2].max() - V[:, 2].min()
Rz180 = np.diag([-1., -1, 1])
body = m3.Manifold.hull_points(V.tolist()); flip = m3.Manifold.hull_points((V @ Rz180.T).tolist()); VOL = body.volume()
a1, a2 = 2 * d * (n0 - n1), 2 * d * (n0 - n2)               # lattice of the unturned B1NRs
def sites(r=3, layers=(-1, 0, 1)):
    out = []
    for i, j, k in itertools.product(range(-r, r + 1), range(-r, r + 1), layers):
        p = i * a1 + j * a2 + np.array([0, 0, k * H]); out += [(p, 0), (p + 2 * d * n0, 1)]
    return out
place = lambda p, t: (flip if t else body).translate(list(p))
# no overlaps among neighbours
A0 = place(np.zeros(3), 0)
ov = max((A0 ^ place(p, t)).volume() for p, t in sites(1) if np.linalg.norm(p) > 1e-9 and np.linalg.norm(p) < 2 * d + H + .1)
hole = -2 * d * n0                                          # a floor corner: 6 fat triangles meet here
ring = [p for p, t in sites(2, (0,)) if abs(np.linalg.norm((p - hole)[:2]) - 2 * d) < 1e-3]
assert len(ring) == 6, len(ring)
ang = np.argsort([np.arctan2(*(p - hole)[1::-1]) for p in ring]); ring = [ring[i] for i in ang]
cell = m3.Manifold.hull_points([list(p[:2]) + [z] for p in ring for z in (-H / 2, H / 2)])
solids = [place(p, t) for p, t in sites(2) if np.linalg.norm((p - hole)[:2]) < 2 * d + 2.5]
part = cell
for s in solids: part = part - s
pieces = part.decompose(); AREA = abs(np.cross(a1, a2)[2])
print('square-face distances', [round(dd, 5) for _, dd in N]); print(f'B1NR volume {VOL:.5f}, square-face distance {d:.5f}, height {H:.5f}, max overlap {ov:.2e}')
print(f'partner: {len(pieces)} piece(s), volume {part.volume():.5f}; cell {AREA * H:.5f} = 2 B1NR + partner {2 * VOL + part.volume():.5f}')
print(f'B1NRs fill {2 * VOL / (AREA * H) * 100:.2f}% of space, partner {part.volume() / (AREA * H) * 100:.2f}%')
GOLD, PURPLE, LILAC, TEAL = '#d9a441', '#6b3fa0', '#9a78c8', '#4f9e96'
def b1nr_part(p, t, shift):
    W = (V @ Rz180.T if t else V) + p + shift; v, tt, c = [], [], []
    for kind, ids in faces:
        o = len(v); v += W[ids].tolist(); tt += [[o, o + a, o + a + 1] for a in range(1, len(ids) - 1)]; c += [{'tri': GOLD, 'sq': LILAC, 'pent': PURPLE}[kind]] * (len(ids) - 2)
    o = len(v); v += W.tolist()
    return {'v': np.round(v, 5).tolist(), 't': tt, 'c': c, 'e': [[o + a, o + b] for a, b in edges], 'a': 1.0}
def partner_part(mf, shift):
    me = mf.to_mesh(); P = np.asarray(me.vert_properties[:, :3]) + shift; T = np.asarray(me.tri_verts)
    Nn = np.cross(P[T[:, 1]] - P[T[:, 0]], P[T[:, 2]] - P[T[:, 0]]); Nn /= np.linalg.norm(Nn, axis=1)[:, None] + 1e-12; by = {}
    for f, tri in enumerate(T):
        for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])): by.setdefault((min(a, b), max(a, b)), []).append(f)
    E = [[int(a), int(b)] for (a, b), fs in by.items() if len(fs) == 2 and Nn[fs[0]] @ Nn[fs[1]] < .985]
    return {'v': np.round(P, 5).tolist(), 't': T.tolist(), 'c': [TEAL] * len(T), 'e': E, 'a': 1.0}
scenes = [{'title': 'The partner', 'sub': 'the space round a corner of the floor', 'parts': [partner_part(part, -hole)]},
          {'title': 'With its six B1NRs', 'sub': 'one layer, drawn slightly apart',
           'parts': [partner_part(part, -hole)] + [b1nr_part(p, t, (p - hole) * np.array([.18, .18, 0]) - hole) for p, t in sites(2, (0,)) if any(np.allclose(p, q) for q in ring)]}]
blk = []
for k in (0, 1):
    z = np.array([0, 0, k * H])
    for p, t in sites(2, (0,)):
        if np.linalg.norm((p - hole)[:2]) < 2 * d * 1.9: blk.append(b1nr_part(p + z, t, (p - hole + z) * .12 - hole))
    for hh in [hole + i * a1 + j * a2 for i, j in [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, -1), (-1, 1)]]:
        if np.linalg.norm((hh - hole)[:2]) < 2 * d * 1.9: blk.append(partner_part(part, (hh - hole) + z + (hh - hole + z) * .12 - hole))
scenes.append({'title': 'A block', 'sub': 'two layers: fat triangles and partners, slightly apart', 'parts': blk})
for s in scenes:
    pts = np.vstack([np.array(p['v']) for p in s['parts']]); ctr = (pts.max(0) + pts.min(0)) / 2
    for p in s['parts']: p['v'] = (np.array(p['v']) - ctr).round(5).tolist()
    s['E'] = round(float(np.linalg.norm(pts - ctr, axis=1).max()) * 1.04, 4)
html = open(os.path.join(HERE, '..', '2026-10-19-five-fold-octet', 'renders', 'family.html')).read()
html = html[:html.index('const SC = ') + len('const SC = ')] + '__D__;' + html[html.index(';\nconst r = new'):].replace(';\nconst r = new', '\nconst r = new', 1)
html = html.replace('const ax = new THREE.Vector3(', 'const ax = new THREE.Vector3(0.75, 0.35, 0.55); const _unused = new THREE.Vector3(')   # a side-on view
open(os.path.join(HERE, 'renders', 'b1nr-partner.html'), 'w').write(html.replace('__D__', json.dumps(scenes, separators=(',', ':'))))
json.dump([{'title': s['title'], 'sub': s['sub']} for s in scenes], open(os.path.join(HERE, 'renders', 'b1nr-partner-labels.json'), 'w'), indent=1)
print('b1nr-partner.html', len(scenes))
