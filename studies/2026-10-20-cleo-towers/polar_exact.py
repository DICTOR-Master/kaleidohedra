# DICTO 2026-10-20: the polar of the Cleo Towers, exact in Q(sqrt5) (DICTO's question: "what surprises does the polar of Fibonacci yield").
# Beats S_k of the Universal PiTet rule from the icosidodecahedron S_0 (radius phi), S_{k+4} = c S_k, c = 10/phi^4 (#38).
#   1. rho^2 := the GTI's circumradius squared = c * phi^2, i.e. 10/phi^4 times the CLEO sphere's radius squared;
#   2. polarity about the sphere of radius rho maps every beat k to beat 5 - k: polar(S_k) = S_{5-k} for k = 0..5 exactly (corners proved
#      as in exact_cycle.step: solved exactly, inside every half-space, closed surface, Euler), hence for every k by scaling;
#   3. the polar Cleo Towers: shells between beats -7 | -2 | 1 | 3 | 4 | 5 (5, 3, 2, 1, 1 beats from the centre), cut into towers over the
#      faces of each inner solid: each kind one shape, adding up to the shell exactly; and the core S_{-7} = RT / c^2.
#   usage: python3 polar_exact.py <studies/2026-10-19-five-fold-octet>
import sys, os, json, itertools
sys.path.insert(0, sys.argv[1]); os.chdir(sys.argv[1])
import numpy as np
from exact_cycle import Q5, Fr, PHI, dot, fv, step, solve3
import exact_shells as X
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open('exact_cycle.py').read().split("if __name__ == '__main__':")[1].split("    log = {")[0].replace('\n    ', '\n'))
ok = lambda cond, m: print(('PASS ' if cond else 'FAIL ') + m, flush=True) or cond
# The #38 helper picks three tight faces by a float determinant (> 1e-9); deep inside (scale 1/c^2) the walls' normals are small and
# that test can pass over every good triple. Here (not in the published #38 script) the triple is chosen by its EXACT determinant.
import inspect
src = inspect.getsource(X.polytope).replace("if abs(np.linalg.det(N[list(tri)])) > 1e-9: break",
    "if det3v(*[tuple(H[i][0]) for i in tri]) != Q5(0): break").replace(
    "        C.append(solve3([list(H[i][0]) for i in tri], [H[i][1] for i in tri]))",
    "        if det3v(*[tuple(H[i][0]) for i in tri]) == Q5(0): continue   # a float point on an edge, not a corner\n        C.append(solve3([list(H[i][0]) for i in tri], [H[i][1] for i in tri]))").replace(
    "abs(N[i] @ x - dd[i]) < 1e-7 * max(1, nr[i])", "abs(N[i] @ x - dd[i]) < 1e-6 * max(1, nr[i]) * max(1, abs(dd[i]))")
assert "a float point on an edge" in src and "det3v(*" in src and "1e-6 * max(1, nr[i])" in src
exec(src, X.__dict__)
G = X.rotations()
S = [ID]
for _ in range(4): S.append(step(S[-1])[0])
c = Q5(10) / (PHI * PHI * PHI * PHI)
assert set(S[4]) == {tuple(c * x for x in v) for v in S[0]}
def beat(j):
    q, r = divmod(j, 4); f = Q5(1)
    for _ in range(abs(q)): f = f * c if q > 0 else f / c
    return [tuple(f * x for x in v) for v in S[r]]
r2 = lambda v: dot(v, v)
rho2 = max(r2(v) for v in beat(2)) if False else None
g2 = [r2(v) for v in beat(2)]; rho2 = g2[0]
ok(all(x == rho2 for x in g2) and rho2 == c * PHI * PHI, f'the GTI\'s corners all lie at radius^2 {rho2!r} = (10/phi^4) * phi^2: 10/phi^4 times the CLEO sphere\'s radius^2')
def polar(V):
    """exact corners of {x : v.x <= rho^2 for every corner v}, proved as in exact_cycle.step"""
    P = [(v, rho2) for v in V]; Nf = np.array([fv(v) for v in V]); df = np.array([rho2.f()] * len(V))
    from scipy.spatial import HalfspaceIntersection
    Xs = HalfspaceIntersection(np.hstack([Nf, -df[:, None]]), np.zeros(3)).intersections
    Xs = Xs[np.unique(np.round(Xs, 8), axis=0, return_index=True)[1]]; C = []
    for x in Xs:
        tight = [i for i in range(len(P)) if abs(Nf[i] @ x - df[i]) < 1e-7]
        for tri in itertools.combinations(tight, 3):
            if abs(np.linalg.det(Nf[list(tri)])) > 1e-6: break
        C.append(tuple(solve3([list(P[i][0]) for i in tri], [P[i][1] for i in tri])))
    C = list(dict.fromkeys(C))
    T = [[(dot(v, x) - h).sign() for (v, h) in P] for x in C]
    assert all(t <= 0 for row in T for t in row) and all(sum(t == 0 for t in row) >= 3 for row in T)
    faces = [[j for j in range(len(C)) if T[j][i] == 0] for i in range(len(P))]; faces = [f for f in faces if len(f) >= 3]
    edges = {}
    for f in faces:
        pts = np.array([fv(C[j]) for j in f]); c0 = pts.mean(0); B = np.linalg.svd(pts - c0)[2][:2]
        o = [f[k] for k in np.argsort(np.arctan2((pts - c0) @ B[1], (pts - c0) @ B[0]))]
        for a, b in zip(o, o[1:] + o[:1]): edges[frozenset((a, b))] = edges.get(frozenset((a, b)), 0) + 1
    assert all(m == 2 for m in edges.values()) and len(C) - len(edges) + len(faces) == 2
    return C
names = ['ID', 'RT', 'GTI', 'FPD']
lab = lambda j: names[j % 4] + ('' if j // 4 == 0 else f' c^{j // 4}')
res = {'mark': 'DICTO polar Cleo Towers, exact, 2026-10-20 · DICTO · dictospheres.com', 'rho2': repr(rho2), 'polar': {}}
allok = True
for k in range(6):
    Pk = polar(beat(k)); same = set(Pk) == set(beat(5 - k)); allok &= same; res['polar'][lab(k)] = lab(5 - k) if same else None
ok(allok, 'polar(beat k) = beat 5 - k exactly for k = 0..5 (ID <-> RT c, RT <-> ID c, GTI <-> FPD), so for every k: polar(c S) = polar(S) / c')
bounds = [-7, -2, 1, 3, 4, 5]
ok([5 - b for b in reversed([0, 1, 2, 4, 7, 12])] == bounds, 'the Cleo Towers\' boundaries 0 | 1 | 2 | 4 | 7 | 12 go to -7 | -2 | 1 | 3 | 4 | 5: shells of 5, 3, 2, 1, 1 beats from the centre')
res['shells'] = []
for k, (a, b) in enumerate(zip(bounds, bounds[1:])):
    out = X.shell(beat(a), beat(b), G, f'polar shell {k + 1}: {lab(a)} -> {lab(b)} ({b - a} beats)'); res['shells'].append(out)
    ok(out['sum_equals_gap_exactly'] and out['one_volume_per_kind'] and all(out['one_symmetry_orbit_per_kind'].values()),
       f"polar shell {k + 1} ({b - a} beats, {lab(a)} -> {lab(b)}): towers {out['pieces']}, each kind one shape, adding up to the shell exactly")
json.dump(res, open(os.path.join(HERE, 'polar-exact.json'), 'w'), indent=1)
