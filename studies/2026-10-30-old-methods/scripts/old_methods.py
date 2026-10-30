# Old methods, new shapes (DICTO 2026-10-30: "as we have new shapes old methods might be even more fruitful"). Every convex new shape of
# DICTO Solids (D-number, model) put through the classic operations, all from its centre (mean of corners) and its circumsphere radius R:
#   d  dual: the polar in the sphere of radius R;                 a  ambo: hull of the edge midpoints;
#   t  truncate: hull of the points 1/3 along every edge from each end;   k  kis: the dual of the truncation of the dual (Conway);
#   j  join: the dual of ambo;                                    e  expand: ambo of ambo;
#   K  Kepler's first stellation: over each face the region beyond it bounded by the planes of its neighbours (when bounded), added
#      to the solid; reported only when every face's region is bounded.
# Each result is described (corners, faces by sides, edge lengths, corner radii, face kinds up to congruence by sorted edge+diagonal
# lengths) and flagged: EQUAL-EDGED (one edge length), REGULAR-FACED (every face a regular polygon), ONE-SPHERE (all corners on one
# sphere), ONE-FACE-KIND (all faces congruent), MATCH (the same shape as a dataset solid or as the shape itself). Numerical, 1e-6.
import csv, json, os, sys, itertools, numpy as np, multiprocessing as mp
from scipy.spatial import ConvexHull, HalfspaceIntersection
DS, OUT = sys.argv[1:3]; JOBS = int(sys.argv[3]) if len(sys.argv) > 3 else 8
def hull_faces(P):
    h = ConvexHull(P); V = P[h.vertices]; h = ConvexHull(V); fam = {}
    for eq in h.equations: fam.setdefault(tuple(np.round(eq, 7)), (eq, [i for i, p in enumerate(V) if abs(eq[:3] @ p + eq[3]) < 1e-8]))
    F = []
    for eq, ids in fam.values():
        c = V[ids].mean(0); u = V[ids[0]] - c; w = np.cross(eq[:3], u)
        F.append((eq, [i for _, i in sorted((np.arctan2((V[i] - c) @ w, (V[i] - c) @ u), i) for i in ids)]))
    return V, F
def edges(F): return sorted({tuple(sorted((f[i], f[(i + 1) % len(f)]))) for _, f in F for i in range(len(f))})
def polar(V, F, R2): return np.array([R2 * eq[:3] / (-eq[3]) for eq, _ in F])
def op(name, V, F, R2):
    if name == 'd': return polar(V, F, R2)
    if name == 'a': return np.array([(V[a] + V[b]) / 2 for a, b in edges(F)])
    if name == 't': return np.array([p for a, b in edges(F) for p in (V[a] + (V[b] - V[a]) / 3, V[b] + (V[a] - V[b]) / 3)])
    if name == 'k':
        D, DF = hull_faces(polar(V, F, R2)); T, TF = hull_faces(op('t', D, DF, R2)); return polar(T, TF, R2)
    if name == 'j':
        A, AF = hull_faces(op('a', V, F, R2)); return polar(A, AF, R2)
    if name == 'e':
        A, AF = hull_faces(op('a', V, F, R2)); return op('a', A, AF, R2)
def kepler(V, F):
    nb = {i: set() for i in range(len(F))}
    for i, j in itertools.combinations(range(len(F)), 2):
        if len(set(F[i][1]) & set(F[j][1])) >= 2: nb[i].add(j); nb[j].add(i)
    pts = list(V)
    for i, (eq, f) in enumerate(F):
        H = [np.hstack([-eq[:3], eq[3]])] + [F[j][0] for j in nb[i]]          # beyond face i, inside its neighbours' planes
        c = V[f].mean(0) + 1e-3 * eq[:3]
        A = np.array([h[:3] for h in H]); b = np.array([h[3] for h in H])
        if np.any(A @ c + b >= 0): return None
        try: W = HalfspaceIntersection(np.array(H), c).intersections
        except Exception: return None
        if not np.all(np.isfinite(W)) or np.abs(W).max() > 1e3 * np.abs(V).max(): return None
        pts += list(W)
    return np.array(pts)   # (the union is non-convex; described by its outer corners: the stellation's tips)
def describe(P):
    V, F = hull_faces(P); Rr = np.linalg.norm(V, axis=1); V = V / Rr.max()
    E = edges(F); el = sorted({round(float(np.linalg.norm(V[a] - V[b])), 6) for a, b in E})
    kinds = set(); reg = True; fk = {}
    for _, f in F:
        fk[len(f)] = fk.get(len(f), 0) + 1
        dd = tuple(sorted(round(float(np.linalg.norm(V[a] - V[b])), 5) for a, b in itertools.combinations(f, 2))); kinds.add(dd)
        s = [np.linalg.norm(V[f[i]] - V[f[(i + 1) % len(f)]]) for i in range(len(f))]
        c = V[f].mean(0); rr = [np.linalg.norm(V[i] - c) for i in f]
        if max(s) - min(s) > 1e-6 or max(rr) - min(rr) > 1e-6: reg = False
    radii = sorted({round(float(x), 6) for x in np.linalg.norm(V, axis=1)})
    return dict(V=len(V), F=len(F), faces=dict(sorted(fk.items())), edge_lengths=len(el), radii=len(radii), face_kinds=len(kinds),
                flags=[x for x, ok in (('EQUAL-EDGED', len(el) == 1), ('REGULAR-FACED', reg), ('ONE-SPHERE', len(radii) == 1), ('ONE-FACE-KIND', len(kinds) == 1)) if ok],
                sig=(len(V), tuple(sorted(fk.items())), tuple(el), tuple(radii)))
def load(fn):
    d = json.load(open(os.path.join(DS, fn), encoding='utf8')); V = np.array([[float(x) for x in v['decimal']] for v in d['vertices']])
    return d, V - V.mean(0)
def run(item):
    name, dnum, fn = item
    try:
        d, V0 = load(fn); V, F = hull_faces(V0); R2 = float((np.linalg.norm(V, axis=1) ** 2).max()); out = dict(name=name, D=dnum, ops={})
        for o in 'datkje':
            try: out['ops'][o] = describe(op(o, V, F, R2))
            except Exception as e: out['ops'][o] = dict(error=type(e).__name__)
        K = kepler(V, F); out['ops']['K'] = describe(K) if K is not None else dict(note='some face region unbounded')
        return out
    except Exception as e: return dict(name=name, D=dnum, error=type(e).__name__ + ' ' + str(e)[:100])
if __name__ == '__main__':
    rows = [r for r in csv.DictReader(l for l in open(os.path.join(DS, 'index.csv'), encoding='utf8') if not l.startswith('#'))]
    sigs = {}
    for r in rows:
        if r['in_dataset'] == 'y' and r['dataset_file'].startswith('solids/'):
            try:
                d, V = load(r['dataset_file'])
                if d.get('checks', {}).get('convex', True): sigs[describe(V)['sig']] = r['name']
            except Exception: pass
    items = []
    for r in rows:
        if r['status'] == 'new' and r['in_dataset'] == 'y' and r['kind'] in ('solid', 'piece'):
            d, _ = load(r['dataset_file'])
            if d.get('checks', {}).get('convex', True): items.append((r['name'], r['universal_number'], r['dataset_file']))
    res = []
    with mp.Pool(JOBS) as pool:
        for r in pool.imap_unordered(run, items):
            for o, x in r.get('ops', {}).items():
                if 'sig' in x: x['match'] = sigs.get(x.pop('sig'))
            res.append(r)
            print(r['D'], r['name'][:30], '|', ' '.join(f"{o}:{x.get('V','-')}/{x.get('F','-')}{'['+','.join(f[:3] for f in x.get('flags', []))+']' if x.get('flags') else ''}{'='+x['match'][:14] if x.get('match') else ''}" for o, x in r.get('ops', {}).items()), flush=True)
            json.dump(res, open(os.path.join(OUT, 'old-methods.json'), 'w'), indent=1, default=float)
    print('done', len(res))
