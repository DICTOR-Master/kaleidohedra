# Step 5b: the big gap (RT -> D(phi^3)) cut around the great stellated dodecahedron (GSD). The GSD body is the chain's icosahedron plus
# 20 spikes (apex at a corner of D(phi^3)); its surface is 60 triangles T-a-b (T a point, a, b valley corners), each seen once from the
# centre. Each layer is cut by the cones over those 60 triangles:
#   inside the star:  cone(T,a,b) cut by RT, which is the tetrahedron T-K-a-b (K the triacontahedron corner on the spike's axis)
#   outside the star: cone(T,a,b) ∩ D(phi^3) ∩ beyond the triangle, convex by construction
# Corners are solved exactly in Q(sqrt5); exact volumes; sums against the layers.
import json, itertools, sys, io, contextlib, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())
St = dict(rev); DO, IC, RTx = St[rev[-1][0]], St['icosahedron'], St['rhombic triacontahedron']
f = lambda v: np.array([x.f() for x in v]); F = lambda V: np.array([f(v) for v in V])
dot = lambda n, v: sum((n[i] * v[i] for i in range(3)), Q(0))
cross = lambda u, w: [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
sub = lambda u, w: [u[i] - w[i] for i in range(3)]
def solve3(P3):
    (n1, d1), (n2, d2), (n3, d3) = P3; det = det3(n1, n2, n3)
    if det.f() == 0: return None
    return [det3(*[[(d1, d2, d3)[i] if j == k else (n1, n2, n3)[i][j] for j in range(3)] for i in range(3)]) / det for k in range(3)]
DOf, ICf, RTf = F(DO), F(IC), F(RTx)
hD = ConvexHull(DOf); PD = []
for e in hD.equations:
    idx = [i for i in range(20) if abs(DOf[i] @ e[:3] + e[3]) < 1e-7]
    n = cross(sub(DO[idx[1]], DO[idx[0]]), sub(DO[idx[2]], DO[idx[0]])); d = dot(n, DO[idx[0]])
    if d.f() < 0: n, d = [-x for x in n], -d
    if not any(abs(np.dot(f(n) / np.linalg.norm(f(n)), p[2]) - 1) < 1e-9 for p in PD): PD.append((n, d, f(n) / np.linalg.norm(f(n))))
hI = ConvexHull(ICf); faces = {tuple(sorted(s)) for s in hI.simplices}
inner, outer = [], []
for fa in faces:
    c = ICf[list(fa)].mean(0); u = c / np.linalg.norm(c)
    T = DO[int(np.argmax(DOf @ u))]; K = RTx[int(np.argmax(RTf @ u))]
    assert np.linalg.norm(np.cross(f(T), u)) < 1e-9 and np.linalg.norm(np.cross(f(K), u)) < 1e-9
    for i, j in [(0, 1), (1, 2), (2, 0)]:
        a, b = IC[fa[i]], IC[fa[j]]
        inner.append([T, K, a, b])
        n = cross(sub(a, T), sub(b, T)); d = dot(n, T)
        if d.f() < 0: n, d = [-x for x in n], -d                 # outward: beyond is n.x >= d
        cone = []
        for p, q, r in [(T, a, b), (T, b, a), (a, b, T)]:          # plane through O, p, q; keep the side of r
            m = cross(p, q); m = m if dot(m, r).f() > 0 else [-x for x in m]; cone.append((m, Q(0)))
        planes = [(nn, dd) for nn, dd, _ in PD] + [(n, d)] + cone   # inside D: n.x <= d ; beyond: n.x >= d ; cone: m.x >= 0
        hs = [np.r_[f(nn), -dd.f()] for nn, dd, _ in PD] + [np.r_[-f(n), d.f()]] + [np.r_[-f(m), 0.0] for m, _ in cone]
        cen = (f(T) + f(a) + f(b)) / 3; um = cen / np.linalg.norm(cen); pt = um * (np.linalg.norm(cen) * 1.0 + 1e-3)
        lo, hi = np.linalg.norm(cen), min((-h[3]) / (h[:3] @ um) for h in hs[:len(PD)] if h[:3] @ um > 1e-12); pt = um * (lo + hi) / 2
        HS = HalfspaceIntersection(np.array(hs), pt); Vf = np.unique(np.round(HS.intersections, 9), axis=0)
        Ve = []
        for v in Vf:
            act = [p for p in planes if abs(np.dot(f(p[0]), v) - p[1].f()) < 1e-7 * max(1, np.linalg.norm(f(p[0])))]
            sol = next((s for P3 in itertools.combinations(act, 3) if (s := solve3(P3)) is not None), None)
            assert sol is not None and np.abs(f(sol) - v).max() < 1e-7; Ve.append(sol)
        outer.append(Ve)
def vol(V): return volume(V, F(V))
def shape(V):
    Vf = F(V); h = ConvexHull(Vf); pl = []
    for e in h.equations:
        if not any(np.allclose(e, p, atol=1e-7) for p in pl): pl.append(e)
    sides = sorted(sum(abs(Vf @ e[:3] + e[3]) < 1e-7) for e in pl)
    return len(V), tuple(sides)
vI, vRT, vD = vol(IC), vol(RTx), vol(DO)
vGSD = vI + sum((vol([T, K, a, b]) * 0 for T, K, a, b in []), Q(0))
spikes = Q(0)
for fa in faces:
    c = ICf[list(fa)].mean(0); T = DO[int(np.argmax(DOf @ (c / np.linalg.norm(c))))]; spikes = spikes + vol([T] + [IC[i] for i in fa])
vGSD = vI + spikes
out = []
for name, L, lay in [('RT -> great stellated dodecahedron', inner, vGSD - vRT), ('great stellated dodecahedron -> D(phi^3)', outer, vD - vGSD)]:
    vs = [vol(V) for V in L]; sh = {shape(V) for V in L}
    out.append(f'{name}: {len(L)} pieces, kinds by shape {sorted(sh)}, one volume: {len(set(vs)) == 1}; piece volume {vs[0]!r} = {vs[0].f():.6f}; '
               f'sum - layer = {sum(vs, Q(0)) - lay!r}')
out.append(f'volumes: RT {vRT!r} = {vRT.f():.6f}, GSD {vGSD!r} = {vGSD.f():.6f}, D(phi^3) {vD!r} = {vD.f():.6f}')
print('\n'.join(out)); open('data/polar-gsd-pieces.txt', 'w').write('\n'.join(out) + '\n')
def solid(V):
    V = F(V); h = ConvexHull(V); Fs = []
    for e in h.equations:
        idx = [i for i in range(len(V)) if abs(V[i] @ e[:3] + e[3]) < 1e-7]
        if any(set(idx) == set(x) for x in Fs): continue
        Qp = V[idx]; c = Qp.mean(0); a = Qp[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a)
        Fs.append([idx[i] for i in np.argsort(np.arctan2((Qp - c) @ b, (Qp - c) @ a))])
    return {'v': V.tolist(), 'f': Fs, 'c': V.mean(0).tolist()}
R = json.load(open('data/polar-render.json'))
R['layers'] = R['layers'][:5] + [{'name': 'RT -> GSD', 'pieces': [solid(V) for V in inner]}, {'name': 'GSD -> D', 'pieces': [solid(V) for V in outer]}]
json.dump(R, open('data/polar-gsd-render.json', 'w'))
