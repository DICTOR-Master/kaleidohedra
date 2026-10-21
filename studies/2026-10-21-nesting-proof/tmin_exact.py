# DICTO Kyushindo Cores (#43), 2026-10-21: exact containment constants of the OG downward family D_0 = OG, D_k = P(D_{k-1}).
# t_min(S) = least t with S inside t.P(S) = max over corners v of S and faces G of P(S) of (m_G.v)/h_G.  Golden nesting
# S_{k-1} = phi^{k-1} D_{k-1} inside S_k = phi^k D_k  <=>  t_min(D_{k-1}) <= phi.
# Exact in Q(sqrt5) (Fractions). Symmetry (60 exact rotations) cuts the exact work to orbit representatives; float is used only to
# guess hull faces and orbit classes, every face is then proved exactly (plane through 3 corners, all corners on the inner side).
# Also: R_k (corner radius), r_k (face distance), the bounds  max_v |v|^2/h_P(v) <= t_min <= R_k/r_{k+1} <= (R_k/r_k)^2,
# face kinds, corner degrees, foot points extreme (reverse step exactly undone), and the pole classification of the faces.
# usage: python3 tmin_exact.py <five-fold-octet dir> <golden-long-solids.pkl> [kmax]
import sys, os, json, time, pickle, itertools
from collections import Counter
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
src = open('exact_upward.py').read(); exec(src.split("def kinds(S)")[0])      # Q5, PHI, dot, solve3, fv, cross, sub, G (exact rotations), app, OG
import numpy as np
from exact_cycle import fv, solve3
from scipy.spatial import ConvexHull
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
D = pickle.load(open(sys.argv[2], 'rb'))
KMAX = int(sys.argv[3]) if len(sys.argv) > 3 else len(D) - 1
Gf = [np.array([[x.f() for x in row] for row in M]) for M in G]
PHIF = PHI.f()
def q5f(x): return x.f()

def orbit_reps(pts_f, keyf):
    """orbit classes of float points under the group (float canonical key); returns list of (rep index, class indices)."""
    cls = {}
    for i, p in enumerate(pts_f):
        key = min(tuple(np.round(M @ p, 6)) for M in Gf); cls.setdefault(key, []).append(i)
    return list(cls.values())

def facets(S):
    """Exact faces of hull(S): list of (n, d, sorted corner index list) with n.x <= d a supporting plane (proved exactly), every
    corner strictly inside or on it. Complete: every edge in two faces, Euler. Uses symmetry: exact work only on orbit reps."""
    idx = {v: i for i, v in enumerate(S)}; Sf = np.array([fv(v) for v in S])
    h = ConvexHull(Sf); tri = h.simplices
    cents = tri_c = Sf[tri].mean(1)
    classes = orbit_reps(cents, None)
    seen = {}; out = []
    for cl in classes:
        t = tri[cl[0]]; a, b, c = (S[j] for j in t)
        n = cross(sub(b, a), sub(c, a)); d = dot(n, a)
        if any((dot(n, v) - d).sign() > 0 for v in S): n, d = tuple(-x for x in n), -d
        sg = [(dot(n, v) - d).sign() for v in S]
        assert all(s <= 0 for s in sg), 'triangle plane is not supporting'
        mem = frozenset(j for j in range(len(S)) if sg[j] == 0)
        if mem in seen: continue
        for M in G:                                    # the orbit of this face, exactly
            n2 = app(M, n); mem2 = frozenset(idx[app(M, S[j])] for j in mem)
            if mem2 in seen: continue
            seen[mem2] = 1; out.append((n2, d, sorted(mem2)))
    # completeness: closed surface + Euler (combinatorial, on exactly proved faces)
    edges = Counter()
    for n, d, mem in out:
        P = Sf[mem]; c0 = P.mean(0); B = np.linalg.svd(P - c0)[2][:2]
        o = [mem[k] for k in np.argsort(np.arctan2((P - c0) @ B[1], (P - c0) @ B[0]))]
        for e in zip(o, o[1:] + o[:1]): edges[frozenset(e)] += 1
    assert all(m == 2 for m in edges.values()), 'surface not closed'
    deg = Counter(j for _, _, mem in out for j in mem)
    nonext = []                                        # points of the list that are NOT corners of the hull
    for j in range(len(S)):
        N = np.array([fv(n) for n, _, mem in out if j in mem])
        if deg[j] < 3 or np.linalg.matrix_rank(N, tol=1e-9) < 3:
            sg = [(dot(n, S[j]) - d).sign() for n, d, _ in out]
            nonext.append((j, 'strictly inside' if all(x < 0 for x in sg) else f'on {sum(x == 0 for x in sg)} face plane(s), not a corner'))
    assert len(S) - len(nonext) - len(edges) + len(out) == 2, 'Euler fails'
    if nonext: print(f'  NOTE: {len(nonext)} listed points are not corners of the hull: {Counter(w for _, w in nonext)}', flush=True)
    return out, len(edges), deg, nonext

def foot(n, d): k = d / dot(n, n); return tuple(k * x for x in n)

res = {'mark': 'DICTO Kyushindo Cores, exact containment constants of the OG downward family, 2026-10-21 · DICTO · dictospheres.com', 'k': {}}
F = {}; t0 = time.time()
for k in range(0, KMAX + 2):
    if k < len(D): S = D[k]
    else:
        S = list(dict.fromkeys(foot(n, d) for n, d, _ in F[k - 1][0]))                 # D_{KMAX+1} = P(D_KMAX)
        print(f'built D_{k} = P(D_{k-1}): {len(S)} foot points', flush=True)
    t = time.time(); F[k] = facets(S); fl, ne, deg, nonext = F[k]
    kinds = Counter(len(mem) for _, _, mem in fl); degs = Counter(deg.values())
    print(f'D_{k}: {len(S) - len(nonext)} corners ({len(S)} listed points), {len(fl)} faces, {ne} edges, faces by sides {dict(sorted(kinds.items()))}, corner degrees {dict(sorted(degs.items()))} ({time.time() - t:.0f} s)', flush=True)
    if k + 1 < len(D):
        fp = {foot(n, d) for n, d, _ in fl}
        ok(fp == set(D[k + 1]), f'foot points of D_{k} = the {len(fp)} listed points of D_{k + 1} exactly')
    res['k'][k] = {'corners': len(S) - len(nonext), 'listed_points': len(S), 'non_extreme_points': len(nonext), 'non_extreme_kinds': dict(Counter(w for _, w in nonext)), 'faces': len(fl), 'edges': ne, 'faces_by_sides': dict(sorted(kinds.items())), 'corner_degrees': dict(sorted(degs.items()))}
    if k >= 1:
        # t_min(D_{k-1}): corners v of D_{k-1} (orbit reps) against the faces of D_k
        V = D[k - 1]; Vf = np.array([fv(v) for v in V]); reps = [cl[0] for cl in orbit_reps(Vf, None)]
        best = None
        for i in reps:
            v = V[i]
            for n, d, mem in fl:
                num = dot(n, v); r = num / d                          # d > 0 (centre inside)
                if best is None or (r - best[0]).sign() > 0: best = (r, i, (n, d, mem))
        tm, i, (n, d, mem) = best
        chk = all(((dot(n2, V[i2]) - tm * d2).sign() <= 0) for i2 in reps for n2, d2, _ in fl)
        ok(chk, f't_min(D_{k-1}) = {tm.f():.12f} = {tm!r} is the exact max over corner reps x faces of D_{k}')
        # bounds: R, r, H of D_{k-1}; r of D_k; lower bound max_v |v|^2 / h_P(v)
        Rk = max(dot(v, v).f() for v in V) ** .5; rk = min((d * d / dot(n, n)).f() for n, d, _ in F[k - 1][0]) ** .5
        Hk = max((d * d / dot(n, n)).f() for n, d, _ in F[k - 1][0]) ** .5; rk1 = min((d * d / dot(n, n)).f() for n, d, _ in fl) ** .5
        lower = max(dot(V[i], V[i]).f() / max(dot(f, V[i]).f() for f in D[k]) for i in reps)
        sgn = (tm - PHI).sign(); pole_ring = 0
        Vset = set(V)
        for n2, d2, mem2 in fl:                                        # pole of the face: f.w = |f|^2 for 3 of its foot points
            f3 = [D[k][j] for j in mem2[:3]]; w = solve3([list(f) for f in f3], [dot(f, f) for f in f3]); pole_ring += w in Vset
        row = {'t_min': tm.f(), 't_min_exact': repr(tm), 't_min_le_phi_exact': sgn <= 0, 'phi_minus_t_min': PHIF - tm.f(),
               'argmax_corner': [x.f() for x in V[i]], 'argmax_corner_radius': dot(V[i], V[i]).f() ** .5, 'argmax_face_sides': len(mem),
               'R': Rk, 'r': rk, 'H_max_face_distance': Hk, 'r_next': rk1, 'lower_bound': lower, 'upper_R_over_r_next': Rk / rk1, 'upper_R_over_r_sq': (Rk / rk) ** 2,
               'faces_of_next_whose_pole_is_a_corner': pole_ring, 'faces_of_next': len(fl)}
        res['k'][k - 1].update(row)
        print(f'  t_min(D_{k-1}) = {tm.f():.9f}  phi - t = {PHIF - tm.f():+.6f}  [{ "<= phi" if sgn <= 0 else "> phi"} exactly]   bounds: {lower:.6f} <= t <= R/r_next {Rk/rk1:.6f} <= (R/r)^2 {(Rk/rk)**2:.6f};  R {Rk:.6f} r {rk:.6f} H {Hk:.6f} r_next {rk1:.6f}; faces of D_{k} with pole a corner of D_{k-1}: {pole_ring}/{len(fl)}', flush=True)
    json.dump(res, open(os.path.join(HERE, 'tmin-exact.json'), 'w'), indent=1)
print(f'done in {time.time() - t0:.0f} s')
