# Independent exact recheck of Theorem 2 for the 14 shadow dice of study 2026-11-24-aequi-exact-dice.
# Own method: plane offsets recognised in Q(sqrt5) by PSLQ from the catalogue depths, then everything exact in
# Q(sqrt5): corners, face cycles, closed surface, every edge on a mirror, and the triangle count of each face by
# locating one interior point of each of the |G| mirror chambers (orbit of a generic point under the exactly
# generated reflection group) and finding the face its ray meets first (exact argmax of n.x/h).
import sys, json, os, itertools
from fractions import Fraction as F
import numpy as np, mpmath
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qr import Q, dot, cross, solve3
from dirs import directions, catalogue, REPS, family, ST

mpmath.mp.dps = 70
D, FAM = directions('set')
Df = np.array([[float(x) for x in v] for v in D])
S5 = mpmath.sqrt(5)


def mirrors(G):
    fams = {'Oh': ['C6', 'RD12'], 'IhA': ['C6', 'RT24'], 'IhB': ['C6', 'RT24p']}[G]
    M = []
    for f in fams:
        for v in [w for w, g in zip(D, FAM) if g == f]:
            if not any(all((a + b).iszero() for a, b in zip(v, m)) for m in M): M.append(v)
    return M


def reflect(m):
    mm = dot(m, m)
    return tuple(tuple((Q(1) if i == j else Q(0)) - 2 * m[i] * m[j] / mm for j in range(3)) for i in range(3))


def matmul(A, B): return tuple(tuple(sum((A[i][k] * B[k][j] for k in range(3)), Q(0)) for j in range(3)) for i in range(3))
def apply(A, x): return tuple(sum((A[i][k] * x[k] for k in range(3)), Q(0)) for i in range(3))


def group(M):
    gens = [reflect(m) for m in M]; I = tuple(tuple(Q(int(i == j)) for j in range(3)) for i in range(3))
    G = {I}; frontier = [I]
    while frontier:
        nxt = []
        for g in frontier:
            for r in gens:
                h = matmul(r, g)
                if h not in G: G.add(h); nxt.append(h)
        frontier = nxt
    return list(G)


def recognise(x, tol):
    """x real (mpf): find x = (p + q sqrt5)/r with small integers."""
    rel = mpmath.pslq([x, 1, S5], maxcoeff=10**4, maxsteps=10**6, tol=tol)
    if rel is None or rel[0] == 0: return None
    r, p, q = rel
    return Q(F(-p, r), F(-q, r))


def to_mp(q): return mpmath.mpf(q.a.numerator) / q.a.denominator + mpmath.mpf(q.b.numerator) / q.b.denominator * S5


def check(rec, depstr, sizes, G):
    src, sid, idx, dep, N = rec[:5]
    prec60 = len(depstr[0]) > 30 or len(depstr[-1]) > 30
    tol = mpmath.mpf(10) ** (-45 if prec60 else -11)
    depmp = [mpmath.mpf(dd) for dd, k in zip(depstr, sizes) for _ in range(k)]
    n = [D[i] for i in idx]
    h = []
    for i in range(N):
        nn = to_mp(dot(n[i], n[i])); hi = depmp[i] * mpmath.sqrt(nn)
        q = recognise(hi / (depmp[0] * mpmath.sqrt(to_mp(dot(n[0], n[0])))), tol)
        assert q is not None, ('offset not recognised in Q(sqrt5)', i)
        h.append(q)
    # h is now exact (with h_0 = 1).  Check the recognised offsets against the catalogue.
    agree = max(abs(to_mp(h[i]) / mpmath.sqrt(to_mp(dot(n[i], n[i]))) * mpmath.sqrt(to_mp(dot(n[0], n[0]))) - depmp[i] / depmp[0]) for i in range(N))
    # corners: float guide, exact solve
    U = Df[idx] / np.linalg.norm(Df[idx], axis=1)[:, None]; hf = np.array([float(x) for x in h])
    nf = np.array([[float(x) for x in v] for v in n])
    V = {}
    for i, j, k in itertools.combinations(range(N), 3):
        A = nf[[i, j, k]]
        if abs(np.linalg.det(A)) < 1e-9: continue
        xf = np.linalg.solve(A, hf[[i, j, k]])
        if np.all(nf @ xf <= hf + 1e-7):
            key = tuple(np.round(xf, 6))
            if key in V: continue
            x = solve3([n[i], n[j], n[k]], [h[i], h[j], h[k]]); V[key] = x
    V = list(dict.fromkeys(V.values()))
    for x in V: assert all((dot(n[i], x) - h[i]).sign() <= 0 for i in range(N)), 'corner outside a plane'
    tight = [[i for i in range(N) if (dot(n[i], x) - h[i]).iszero()] for x in V]
    faces = []
    for i in range(N):
        on = [a for a in range(len(V)) if i in tight[a]]
        assert len(on) >= 3, ('face missing', i)
        P = np.array([[float(c) for c in V[a]] for a in on]); c = P.mean(0)
        e1 = P[0] - c; e2 = np.cross(nf[i], e1)
        on = [on[a] for a in np.argsort(np.arctan2((P - c) @ e2, (P - c) @ e1))]
        k = len(on)
        for a in range(k):
            A_, B_, C_ = V[on[a]], V[on[(a + 1) % k]], V[on[(a + 2) % k]]
            assert dot(n[i], cross(tuple(B_[t] - A_[t] for t in range(3)), tuple(C_[t] - B_[t] for t in range(3)))).sign() > 0
        faces.append(on)
    edges = {}
    for i, f in enumerate(faces):
        for a in range(len(f)):
            e = tuple(sorted((f[a], f[(a + 1) % len(f)]))); edges.setdefault(e, []).append(i)
    closed = all(len(v) == 2 for v in edges.values())
    euler = len(V) - len(edges) + N
    M = mirrors(G)
    on_mirror = all(any(dot(m, V[a]).iszero() and dot(m, V[b]).iszero() for m in M) for a, b in edges)
    Gr = group(M); order = len(Gr)
    p0 = (Q(1), Q(F(3, 7)), Q(F(1, 11), F(1, 13)))
    assert all(not dot(m, p0).iszero() for m in M)
    pts = list(dict.fromkeys(apply(g, p0) for g in Gr))
    counts = [0] * N; ties = 0
    for x in pts:
        best = None
        for i in range(N):
            if best is None: best = i; continue
            # compare n_i.x / h_i with n_best.x / h_best (h > 0)
            s = (dot(n[i], x) * h[best] - dot(n[best], x) * h[i]).sign()
            if s > 0: best = i
            elif s == 0: ties += 1
        counts[best] += 1
    # depth ratios (unit normals) as exact squares: d_i^2 = h_i^2 / |n_i|^2, relative to face 0
    d2 = []
    for i in range(N):
        r = (h[i] * h[i] / dot(n[i], n[i])) / (h[0] * h[0] / dot(n[0], n[0]))
        if r not in d2: d2.append(r)
    fair = ties == 0 and len(set(counts)) == 1 and counts[0] * N == order
    return dict(src=src, sid=sid, G=G, N=N, corners=len(V), edges=len(edges), euler=euler, closed=closed,
                edges_on_mirrors=on_mirror, group_order=order, chambers=len(pts), ties=ties,
                triangles_per_face=sorted(set(counts)), fair_exact=fair, depth_ratio_squares=[str(r) for r in d2],
                depth_ratios_float=[float(r) ** .5 for r in d2], catalogue_agree=float(agree))


if __name__ == '__main__':
    hits = json.load(open(os.path.join(ST, '2026-11-24-aequi-exact-dice', 'data', 'shadow_hits.json')))
    cat = {(r[0], r[1]): r for r in catalogue()}
    out = []
    for hrec in hits:
        r = cat[(hrec['src'], hrec['sid'])]
        assert list(r[2]) == list(hrec['idx'])
        res = check(r, r[5], r[6], hrec['G']); res['label'] = hrec['label']; out.append(res)
        print(json.dumps(res), flush=True)
    json.dump(out, open(sys.argv[1], 'w'), indent=1)
    good = all(x['closed'] and x['euler'] == 2 and x['edges_on_mirrors'] and x['fair_exact'] and x['chambers'] == x['group_order'] for x in out)
    print('dice checked:', len(out), ' all exact checks pass:', good)
    print('FINAL ok' if good and len(out) == 14 else 'FINAL disagree')
