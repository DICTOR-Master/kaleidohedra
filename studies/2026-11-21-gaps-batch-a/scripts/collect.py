# Halo and star census, collection: match every halo and star of data/shapes/*.json (census.py) by similarity (reflections allowed)
# against (a) DICTO Solids v7, (b) the classical families (Platonic, Archimedean, Catalan, Johnson from krp-core's registry, closed-form
# coordinates in float64; uniform prisms and antiprisms n = 3..40 and their duals, bipyramids and trapezohedra, generated here), and for
# the stars the stellations in krp-core (first four stellations of the Platonic and Catalan solids and others, incl. the Kepler-Poinsot
# solids), (c) each other. A match: same number of corners (and, for halos, the same faces by sides), the same sorted scaled squared
# distances (1e-6), and an explicit orthogonal map of one corner set onto the other after scaling (1e-6). Writes data/census.json and
# thumbnails of the NEW halos (data/thumbs/*.png). Usage: collect.py <dataset dir> <data dir>
import json, os, sys, glob, math, numpy as np
from scipy.spatial import cKDTree, ConvexHull
DS, D = sys.argv[1:3]

def norm(P):
    P = np.asarray(P, float); P = P - P.mean(0); return P / np.linalg.norm(P, axis=1).max()
def key(P):
    P = norm(P); Dm = ((P[:, None] - P[None]) ** 2).sum(-1); v = np.sort(Dm[np.triu_indices(len(P), 1)]); return v / v[-1]
def corr(P, Q, tol=1e-6):
    P, Q = norm(P), norm(Q); r = np.linalg.norm(P, axis=1); rq = np.linalg.norm(Q, axis=1); T = cKDTree(Q)
    i1 = int(np.argmax(r)); i2 = next(i for i in np.argsort(-r) if np.linalg.norm(np.cross(P[i1], P[i])) > 1e-3)
    B = np.array([P[i1], P[i2], np.cross(P[i1], P[i2])]); d12 = np.linalg.norm(P[i1] - P[i2])
    for a in np.where(np.abs(rq - r[i1]) < tol)[0]:
        for b in np.where(np.abs(rq - r[i2]) < tol)[0]:
            if abs(np.linalg.norm(Q[a] - Q[b]) - d12) > tol: continue
            for sg in (1, -1):
                C = np.array([Q[a], Q[b], sg * np.cross(Q[a], Q[b])]); M = np.linalg.solve(B, C)
                if np.allclose(M @ M.T, np.eye(3), atol=1e-6) and np.all(T.query(P @ M)[0] < tol * 10): return True
    return False
class Obj:
    def __init__(s, label, P, sides=None, kind=None):
        s.label, s.P, s.sides, s.kind = label, np.asarray(P, float), sides, kind; s.n = len(P); s._k = None
    @property
    def k(s):
        if s._k is None: s._k = key(s.P)
        return s._k
def same(a, b, use_sides=True):
    if a.n != b.n: return False
    if use_sides and a.sides is not None and b.sides is not None and a.sides != b.sides: return False
    if a.n > 1600: return False
    if not np.allclose(a.k, b.k, atol=1e-6): return False
    return corr(a.P, b.P)
def sides_of(F): s = {}; [s.__setitem__(len(f), s.get(len(f), 0) + 1) for f in F]; return dict(sorted(s.items()))

# (b) classical
classical = []
for c in json.load(open(os.path.join(D, 'classical-krp.json'))):
    V = np.array(c['vertices'], float); kind = 'stellation' if c['family'] == 'stellation' else 'convex'
    classical.append(Obj(f"{c['family']}: {c['id']}", V, sides_of(c['faces']) if kind == 'convex' else None, kind))
def polar(V):
    H = ConvexHull(V); eqs = {tuple(np.round(e, 9)): e for e in H.equations}; return np.array([-e[:3] / e[3] for e in eqs.values()])
for n in range(3, 41):
    a = np.pi / n; R = 1 / (2 * math.sin(a))
    pr = np.array([[R * math.cos(2 * a * k), R * math.sin(2 * a * k), s * .5] for k in range(n) for s in (1, -1)])
    h = math.sqrt(max(0, 1 - (2 * R * math.sin(a / 2)) ** 2)) / 2
    ap = np.array([[R * math.cos(a * k), R * math.sin(a * k), (h if k % 2 else -h)] for k in range(2 * n)])
    if n != 4: classical.append(Obj(f'prism/antiprism: {n}-gonal prism', pr, {4: n, n: 2}, 'convex'))
    if n != 3: classical.append(Obj(f'prism/antiprism: {n}-gonal antiprism', ap, {3: 2 * n, n: 2} if n != 3 else None, 'convex'))
    if n != 4: classical.append(Obj(f'dual: {n}-gonal bipyramid (dual of the uniform prism)', polar(pr), {3: 2 * n} if n != 4 else None, 'convex'))
    if n != 3: classical.append(Obj(f'dual: {n}-gonal trapezohedron (dual of the uniform antiprism)', polar(ap), {4: 2 * n}, 'convex'))
# (a) dataset v7
dataset = []
for fn in sorted(glob.glob(os.path.join(DS, 'solids', '*.json'))):
    d = json.load(open(fn)); V = np.array([[float(x) for x in v['decimal']] for v in d['vertices']])
    cv = d.get('convex', d.get('checks', {}).get('convex', True))
    dataset.append(Obj(f"v7: {d['name']}" + (f" ({d['D']})" if d.get('D') else ''), V, sides_of(d['faces']), 'convex' if cv else 'nonconvex'))

shapes = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(D, 'shapes', '*.json')))]
rows = []; census = []
base_classical = {}
for s in shapes:                                               # is the base shape itself classical? (then its star is a classical Kleetope)
    d = json.load(open(os.path.join(DS, 'solids', s['slug'] + '.json'))); V = np.array([[float(x) for x in v['decimal']] for v in d['vertices']])
    b = Obj(s['name'], V, sides_of(d['faces'])); base_classical[s['slug']] = [c.label for c in classical if c.kind == 'convex' and same(b, c)]
def short(nm): return nm.replace('DICTO ', '').split(' (')[0]
for s in shapes:
    for part, kind in (('centre_halo', 'halo'), ('polar_halo', 'halo'), ('star_2', 'star'), ('star_phi', 'star')):
        if part not in s: continue
        h = s[part]; sides = {int(k): v for k, v in h['faces_by_sides'].items()}
        o = Obj(f"{s['name']} / {part}", h['points'], sides if kind == 'halo' else None, kind)
        o.meta = dict(shape=s['name'], D=s.get('D'), slug=s['slug'], part=part, corners=h['corners'], edges=h['edges'], faces=h['faces'],
                      faces_by_sides=h['faces_by_sides'], symmetry=h['symmetry'], symmetry_order=h['symmetry_order'], exact=s['exact'],
                      exact_check=h.get('exact_facets', h.get('exact_merge')), field=s['field'])
        m = []
        targets = [c for c in classical if (c.kind == 'convex') == (kind == 'halo')] + [x for x in dataset if (x.kind == 'convex') == (kind == 'halo') or kind == 'star']
        for c in targets:
            if same(o, c, use_sides=(kind == 'halo')): m.append(c.label)
        dup = [x.label for x in census if x.kind == kind and same(o, x, use_sides=(kind == 'halo'))]
        o.meta['matches'] = m; o.meta['same_as'] = dup
        nm = short(s['name'])
        ph = {'centre_halo': f'{nm} Halo', 'polar_halo': f'{nm} Polar Halo', 'star_2': f'{nm} Star', 'star_phi': f'Golden {nm} Star'}[part]
        o.meta['status'] = 'known' if m else ('same as ' + dup[0].split(' / ')[0] + ' ' + dup[0].split(' / ')[1].replace('_', ' ') if dup else 'NEW')
        o.meta['placeholder'] = ph if not m and not dup else None
        if kind == 'star': o.meta['base_is_classical'] = base_classical[s['slug']]
        census.append(o); print(o.label, '|', o.meta['status'], m[:2], flush=True)
json.dump([o.meta for o in census], open(os.path.join(D, 'census.json'), 'w'), indent=1, default=float)
# thumbnails of the NEW halos (render standard: solid faces, dark edges >= 1.5 px)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
os.makedirs(os.path.join(D, 'thumbs'), exist_ok=True)
COL = {3: '#8e5bd6', 4: '#2bb3a3', 5: '#d4af37', 6: '#e07a3f', 8: '#4a7fc1', 10: '#b8434e'}
light = np.array([.4, -.5, .75]); light /= np.linalg.norm(light)
by = {s['slug']: s for s in shapes}
for o in census:
    if o.kind != 'halo' or o.meta['status'] != 'NEW': continue
    h = by[o.meta['slug']][o.meta['part']]; P = np.array(h['points']); P = P - P.mean(0); P /= np.linalg.norm(P, axis=1).max()
    fig = plt.figure(figsize=(2.2, 2.2), dpi=200); ax = fig.add_subplot(projection='3d'); polys, fc = [], []
    for f in h['face_list']:
        Q = P[f]; n = np.cross(Q[1] - Q[0], Q[2] - Q[0]); n /= np.linalg.norm(n)
        if n @ Q.mean(0) < 0: n = -n
        sh = .55 + .45 * max(0, n @ light); polys.append(Q); fc.append(np.clip(np.array(matplotlib.colors.to_rgb(COL.get(len(f), '#9aa3b5'))) * sh, 0, 1))
    ax.add_collection3d(Poly3DCollection(polys, facecolors=fc, edgecolors='#1a1a1a', linewidths=0.8))
    ax.set_xlim(-.75, .75); ax.set_ylim(-.75, .75); ax.set_zlim(-.75, .75); ax.set_box_aspect((1, 1, 1)); ax.view_init(20, 30); ax.axis('off')
    plt.subplots_adjust(0, 0, 1, 1); fig.savefig(os.path.join(D, 'thumbs', f"{o.meta['slug']}-{o.meta['part']}.png"), facecolor='white'); plt.close(fig)
print('done', len(census))
