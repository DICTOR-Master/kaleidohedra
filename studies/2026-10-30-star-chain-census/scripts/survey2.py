# Star Chain Survey v2 (DICTO 10-30: "continue a star chain survey for all likely discovered solids"). For every convex solid of the
# dataset DICTO Solids: Exact Geometry v5, centred at its dataset centre, follow DICTO's growth rule T of #38, T(S) = {x : v.x <= v.v for
# every corner v of S} (the star step of #78 is T read backwards), for up to 10 steps. Record each step's shape (corners, faces by sides,
# corner radii and edge lengths up to scale), whether it is the shape of a dataset solid, whether the chain returns to an earlier shape
# (period) and the gain in radius over one period, recognised where possible in the solid's field. The centre counts only when the
# symmetry fixes it (a group with inversion or with at least 12 rotations); others are listed separately.
# Usage: ~/geom/bin/python scripts/survey2.py <solids dir> <out.json>
import sys, os, json, glob, itertools, numpy as np, sympy as sp
from scipy.spatial import ConvexHull, HalfspaceIntersection
SOL, OUT = sys.argv[1], sys.argv[2]
def facelist(V):
    h = ConvexHull(V); W = V[h.vertices]; sc = np.abs(W).max(); out = {}
    for eq in h.equations:
        k = tuple(np.round(eq, 7))
        if k not in out: out[k] = (eq, [i for i, p in enumerate(W) if abs(eq[:3] @ p + eq[3]) < 1e-8 * sc])
    return W, list(out.values())
def edges(W, FL):
    E = set()
    for eq, ids in FL:
        R = W[ids]; c = R.mean(0); a = R[0] - c; a /= np.linalg.norm(a); b = np.cross(eq[:3], a)
        o = [ids[i] for i in np.argsort(np.arctan2((R - c) @ b, (R - c) @ a))]
        for i in range(len(o)): E.add(tuple(sorted((o[i], o[(i + 1) % len(o)]))))
    return E
def shape(V):
    W, FL = facelist(V); r = np.linalg.norm(W, axis=1); Rm = r.max()
    E = edges(W, FL); el = sorted({round(np.linalg.norm(W[a] - W[b]) / Rm, 5) for a, b in E})
    fk = {}
    for _, ids in FL: fk[len(ids)] = fk.get(len(ids), 0) + 1
    return (len(W), tuple(sorted(fk.items())), tuple(sorted({round(x / Rm, 5) for x in r})), tuple(el)), Rm
def T(V):
    W = V[ConvexHull(V).vertices]; H = np.hstack([W, -(W * W).sum(1)[:, None]])
    X = HalfspaceIntersection(H, np.zeros(3)).intersections; return X[ConvexHull(X).vertices]
solids = []
for js in sorted(glob.glob(os.path.join(SOL, '*.json'))):
    m = json.load(open(js))
    if str(m.get('convex')) != 'True' or not m.get('vertices'): continue
    V = np.array([[float(x) for x in v['decimal']] for v in m['vertices']])
    c = m.get('unit_volume', {}).get('centre', {}).get('decimal'); c = np.array([float(x) for x in c]) if c else V.mean(0)
    sym = m.get('symmetry', {}); rot = int(sym.get('rotations', 1) or 1); inv = bool(sym.get('contains_inversion'))
    solids.append(dict(name=m['name'], field=m.get('field'), sym=sym.get('schoenflies'), centred=inv or rot >= 12, V=V - c))
lib = {}
for s in solids:
    try: lib.setdefault(shape(s['V'])[0], s['name'])
    except Exception: pass
res = []
for s in solids:
    row = dict(name=s['name'], symmetry=s['sym'], field=s['field'], centre_meaningful=s['centred'], steps=[])
    try:
        sh0, R0 = shape(s['V']); shapes = [(sh0, R0)]; S = s['V']; period = None; gain = None
        for k in range(10):
            S = T(S)
            if len(S) > 4000: row['steps'].append(dict(note='over 4000 corners, stopped')); break
            sh, R = shape(S); rep = [i for i, (x, _) in enumerate(shapes) if x == sh]
            row['steps'].append(dict(step=k + 1, corners=sh[0], faces=dict(sh[1]), radius_kinds=len(sh[2]), edge_kinds=len(sh[3]),
                                     is_dataset_solid=lib.get(sh), returns_to_step=rep[0] if rep else None))
            shapes.append((sh, R))
            if rep:
                period = k + 1 - rep[0]; gain = R / shapes[rep[0]][1]; break
        row['period'] = period; row['gain_radius'] = gain
        if gain:
            try: row['gain_recognised'] = str(sp.nsimplify(gain, [sp.sqrt(5), sp.sqrt(2), sp.sqrt(3)], tolerance=1e-9))
            except Exception: row['gain_recognised'] = None
    except Exception as ex:
        row['error'] = str(ex)[:160]
    res.append(row)
    print(s['name'][:40].ljust(40), s['sym'], 'centred' if s['centred'] else 'NOCENTRE', 'period', row.get('period'), 'gain', row.get('gain_recognised') or row.get('gain_radius'),
          '| via', [st.get('is_dataset_solid') for st in row['steps'] if st.get('is_dataset_solid')], flush=True)
    json.dump(res, open(OUT, 'w'), indent=1, default=str)
