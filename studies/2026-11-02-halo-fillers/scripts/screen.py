# Halo fillers screen (DICTO 2026-11-02). Necessary condition for any tiling of space (face-to-face or not) by copies of the
# pieces of a set S: at an interior point of an edge of a piece with dihedral angle a, the pieces around it contribute their dihedral
# angles (a point on their edge) or pi (a point inside their face), total 2 pi; so 2 pi - a, or pi - a, must be a sum of dihedral
# angles of the pieces of S (non-negative integer combination). Here: numeric screen (1e-7 rad), survivors are re-proved exactly.
# Usage: screen.py <out json>   (env HALO_CENSUS, DATASET: data dirs; defaults on dicto-big-brother)
import json, os, sys, math, itertools, numpy as np
TOL = 1e-7; TAU = 2 * math.pi
HC = os.environ.get('HALO_CENSUS', os.path.expanduser('~/kres-tmp/halo-census/data')); DS = os.environ.get('DATASET', os.path.expanduser('~/kres-tmp/dataset-v7'))

def dihedrals(P, F=None):
    """dihedral angle at every edge of the convex hull of P (facets merged by plane; edge = two facets sharing two corners)."""
    from scipy.spatial import ConvexHull
    P = np.asarray(P, float); H = ConvexHull(P); g = {}
    for sm, eq in zip(H.simplices, H.equations):
        key = tuple(np.round(eq / np.linalg.norm(eq[:3]), 8)); g.setdefault(key, [eq[:3] / np.linalg.norm(eq[:3]), eq[3] / np.linalg.norm(eq[:3]), set()])
    G = list(g.values()); sc = max(1, np.abs(P).max())
    for n, d, ids in G: ids.update(i for i in range(len(P)) if abs(n @ P[i] + d) < 1e-9 * sc)
    out = []
    for (n1, d1, s1), (n2, d2, s2) in itertools.combinations(G, 2):
        if len(s1 & s2) >= 2: out.append(math.pi - math.acos(max(-1, min(1, float(n1 @ n2)))))
    return out
def dihedrals_faces(P, F):
    """interior dihedral angles (may exceed pi for a non-convex solid) from consistently oriented faces."""
    P = np.asarray(P, float); N = []
    for f in F:
        n = np.zeros(3)
        for k in range(len(f)): n += np.cross(P[f[k]], P[f[(k + 1) % len(f)]])
        N.append(n / np.linalg.norm(n))
    vol = sum(np.dot(P[f[0]], np.cross(P[f[k]], P[f[k + 1]])) for f in F for k in range(1, len(f) - 1))
    if vol < 0: N = [-n for n in N]
    E = {}
    for i, f in enumerate(F):
        for k in range(len(f)): E[(f[k], f[(k + 1) % len(f)])] = i
    out = []
    for (a, b), i in E.items():
        if a < b or (b, a) not in E: continue
        j = E[(b, a)]; n1, n2 = N[i], N[j]; e = P[b] - P[a]; e /= np.linalg.norm(e)
        th = math.atan2(float(np.cross(n1, n2) @ e), float(n1 @ n2))      # turning angle between outward normals
        if abs(th) < 1e-12: continue                                       # coplanar faces: no edge
        out.append(math.pi - th if (np.cross(n1, n2) @ e) * 0 == 0 else None)
    return out
def classes(angles):
    v = sorted(angles); cl = []
    for a in v:
        if cl and abs(a - cl[-1][0]) < 1e-9: cl[-1][1] += 1
        else: cl.append([a, 1])
    return cl                      # [angle, number of edges]
def reach(A):
    """all sums <= 2 pi + TOL of non-negative integer combinations of A (dict rounded key -> one combination)."""
    A = sorted(set(round(a, 10) for a in A)); R = {0.0: ()}
    for a in A:
        new = dict(R)
        for s, comb in R.items():
            m = 1
            while s + m * a <= TAU + TOL:
                t = round(s + m * a, 9)
                if t not in new: new[t] = comb + ((a, m),)
                m += 1
            if len(new) > 3_000_000: return None
        R = new
    return R
def ok_edge(a, R, keys):
    for target in (TAU - a, math.pi - a):
        i = np.searchsorted(keys, target - TOL)
        if i < len(keys) and abs(keys[i] - target) < TOL: return (target, R[keys[i]])
    return None
def test(own, pool):
    """own: angle classes of the piece whose edges are tested; pool: every angle available. Returns (pass, failing edges, witnesses)."""
    R = reach(pool)
    if R is None: return None, None, None
    keys = np.array(sorted(R)); bad = []; wit = []
    for a, n in own:
        w = ok_edge(a, R, keys)
        (wit.append((a, w)) if w else bad.append((a, n)))
    return not bad, bad, wit

def load_halos():
    cen = json.load(open(os.path.join(HC, 'census.json'))); H = {}
    for r in cen:
        if 'halo' not in r['part'] or r['status'] != 'NEW': continue
        s = json.load(open(os.path.join(HC, 'shapes', r['slug'] + '.json')))[r['part']]
        H[r['placeholder']] = dict(slug=r['slug'], part=r['part'], P=s['points'], F=s['face_list'], sym=r['symmetry'], field=r['field'])
    return H
def solid(slug):
    d = json.load(open(os.path.join(DS, 'solids', slug + '.json')))
    return [[float(x) for x in v['decimal']] for v in d['vertices']], d['faces']
def prism(n):
    P = [[math.cos(TAU * k / n), math.sin(TAU * k / n), z] for z in (0, 1) for k in range(n)]
    return P, [list(range(n - 1, -1, -1)), list(range(n, 2 * n))] + [[k, (k + 1) % n, n + (k + 1) % n, n + k] for k in range(n)]
def hull(P):
    from scipy.spatial import ConvexHull
    P = np.array(P, float); H = ConvexHull(P); g = {}
    for sm, eq in zip(H.simplices, H.equations): g.setdefault(tuple(np.round(eq, 8)), set()).update(sm.tolist())
    F = []
    for eq, ids in g.items():
        n = np.array(eq[:3]); ids = list(ids); c = P[ids].mean(0); u = P[ids[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
        F.append(sorted(ids, key=lambda i: math.atan2((P[i] - c) @ w, (P[i] - c) @ u)))
    return P.tolist(), F
perm = lambda v: {p for s in itertools.product(*[(1, -1)] * 3) for p in itertools.permutations([a * b for a, b in zip(v, s)])}
KNOWN = {
    'cube': [hull(list(perm((1, 1, 1))))],
    'rhombic dodecahedron': [hull(list(perm((1, 1, 1)) | perm((2, 0, 0))))],
    'truncated octahedron': [hull(list(perm((0, 1, 2))))],
    'hexagonal prism': [prism(6)],
    'triangular prism': [prism(3)],
    'tetrahedron + octahedron': [hull([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]), hull(list(perm((1, 0, 0))))],
}
for name, slugs in (('Samson + Delilah (Delian bond)', ['dicto-samson', 'dicto-delilah']), ('Icosaxes + Unborn Axes (golden bond)', ['dicto-icosaxes', 'dicto-unborn-axes']),
                    ('Lotus Jewel Axes + Dodecaxes (keyed bond)', ['dicto-lotus-jewel-axes', 'dicto-dodecaxes']), ('skewed ED F16', ['dicto-skewed-ed-16']),
                    ('skewed ED F18', ['dicto-skewed-ed-18']), ('skewed rhombic dodecahedron', ['dicto-skewed-rhombic-dodecahedron'])):
    KNOWN[name] = [solid(s) for s in slugs]

if __name__ == '__main__':
    OUT = sys.argv[1]; H = load_halos(); print(len(H), 'new halos', flush=True)
    A = {k: classes(dihedrals(h['P'], h['F'])) for k, h in H.items()}
    KA = {k: [a for P, F in v for a in dihedrals_faces(P, F)] for k, v in KNOWN.items()}
    for k, v in KA.items(): print('known', k, sorted({round(math.degrees(a), 4) for a in v}), flush=True)
    # sanity: every known filler set passes its own test
    for k, v in KA.items():
        p = test(classes(v), v); print('sanity', k, p[0]); assert p[0]
    res = dict(single={}, with_known={}, halo_pairs={}, angles={k: [[math.degrees(a), n] for a, n in v] for k, v in A.items()})
    for k in H:
        p, bad, wit = test(A[k], [a for a, n in A[k]])
        res['single'][k] = dict(passes=p, failing=[[math.degrees(a), n] for a, n in (bad or [])], witnesses=[[math.degrees(a), str(w)] for a, w in (wit or [])])
        print('single', k, p, flush=True)
    for k in H:
        for kn, ka in KA.items():
            p, bad, wit = test(A[k], [a for a, n in A[k]] + ka)
            if p is None or p: res['with_known'][k + ' | ' + kn] = dict(passes=p, witnesses=[[math.degrees(a), str(w)] for a, w in (wit or [])])
    print('with_known survivors', len(res['with_known']), flush=True)
    ks = sorted(H); npair = 0
    for i, k1 in enumerate(ks):
        for k2 in ks[i + 1:]:
            pool = [a for a, n in A[k1]] + [a for a, n in A[k2]]; npair += 1
            p1 = test(A[k1], pool)[0]
            if p1 is False: continue
            p2 = test(A[k2], pool)[0]
            if p2 is False: continue
            res['halo_pairs'][k1 + ' | ' + k2] = dict(passes=(p1 and p2))
    res['counts'] = dict(halos=len(H), single_pass=sum(1 for v in res['single'].values() if v['passes']), known_sets=len(KA),
                         with_known_tested=len(H) * len(KA), with_known_pass=len(res['with_known']), halo_pairs_tested=npair, halo_pairs_pass=len(res['halo_pairs']))
    print(res['counts'])
    json.dump(res, open(OUT, 'w'), indent=1)
