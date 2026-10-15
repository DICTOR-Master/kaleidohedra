# Step 22 (DICTO: "run the exact larger radius chorus check"). The spatial five-fold chorus rebuilt to radius R with exact sites
# (integer combinations of exact joint vectors of each voice), wedges as before (start angle 59 deg), clashing copies silenced in
# whole five-fold orbits (float), then the EXACT packing check: copies at s, t do not overlap iff some face plane n.x = d of the
# OCD has n.(s - t) >= 2d (K - K = 2K); touching iff the best face gives equality. All in Q(sqrt5).
import sys, io, os, contextlib, itertools, json, numpy as np
RAD = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0          # read before polar.py replaces sys.argv
from scipy.spatial import ConvexHull
PD = '/home/dicto/kaleidohedra/studies/2026-10-16-polar-dharma'; here = os.getcwd(); os.chdir(PD)
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())
os.chdir(here)
sys.path.insert(0, '/home/dicto/kaleidohedra/studies/_lib'); import geomcheck as gc
f = lambda v: np.array([x.f() for x in v]); F = lambda V: np.array([f(v) for v in V])
dot = lambda a, b: sum((a[i] * b[i] for i in range(3)), Q(0))
cross = lambda u, w: [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
sub = lambda u, w: [u[i] - w[i] for i in range(3)]; add = lambda u, w: [u[i] + w[i] for i in range(3)]; sc = lambda u, k: [x * k for x in u]
OCD = dict(rev)['dual of the Hecatodihedron']; Of = F(OCD)
PO = []
for e in ConvexHull(Of).equations:
    idx = [i for i in range(len(OCD)) if abs(Of[i] @ e[:3] + e[3]) < 1e-7]
    if any(set(idx) == set(p[0]) for p in PO): continue
    for i0, i1, i2 in itertools.combinations(idx, 3):
        n = cross(sub(OCD[i1], OCD[i0]), sub(OCD[i2], OCD[i0]))
        if any(x.f() != 0 for x in n): break
    d = dot(n, OCD[i0])
    if d.f() < 0: n, d = sc(n, Q(-1)), Q(0) - d
    PO.append((idx, n, d))
hexes = [(n, d) for idx, n, d in PO if len(idx) == 6]
bond = [sc(n, Q(2) * d / dot(n, n)) for n, d in hexes]; Bf = np.array([f(b) for b in bond]); U = Bf / np.linalg.norm(Bf, axis=1)[:, None]
cubes = [list(S_) for S_ in itertools.combinations(range(20), 8)
         if np.all(np.isin(np.round((U[list(S_)] @ U[list(S_)].T)[~np.eye(8, dtype=bool)], 6), np.round([1 / 3, -1 / 3, -1.0], 6)))]
assert len(cubes) == 5
a5 = Of[np.argmax(np.linalg.norm(Of, axis=1))]; a5 = a5 / np.linalg.norm(a5); R72 = gc.rotation(a5, 2 * np.pi / 5)
order = [0]
while len(order) < 5:
    nxt = next(j for j in range(5) if all(np.min(np.linalg.norm(U[cubes[j]] - u, axis=1)) < 1e-6 for u in U[cubes[order[-1]]] @ R72.T)); order.append(nxt)
cubes = [cubes[k] for k in order]
# exact sites of each voice: integer combinations of a basis of three of its joint vectors
voice_sites = []
for k in range(5):
    for a, b, c in itertools.combinations(cubes[k], 3):
        M = np.array([Bf[a], Bf[b], Bf[c]]).T
        if abs(np.linalg.det(M)) > 1e-6 and all(np.allclose(np.linalg.solve(M, Bf[i]), np.round(np.linalg.solve(M, Bf[i])), atol=1e-6) for i in cubes[k]): break
    m = int(np.ceil(RAD / min(np.linalg.norm(M, axis=0)))) + 2; pts = []
    for ijk in itertools.product(range(-m, m + 1), repeat=3):
        x = M @ np.array(ijk, float)
        if np.linalg.norm(x) < RAD: pts.append((x, add(add(sc(bond[a], Q(ijk[0])), sc(bond[b], Q(ijk[1]))), sc(bond[c], Q(ijk[2])))))
    voice_sites.append(pts)
e1 = np.cross(a5, [1, 0, 0]); e1 = e1 / np.linalg.norm(e1); e2 = np.cross(a5, e1); th0 = np.radians(59.0)
def wedge(p): return int(((np.arctan2(p @ e2, p @ e1) - th0) % (2 * np.pi)) // (2 * np.pi / 5)) % 5
sites = []
for k in range(5):
    for x, X in voice_sites[k]:
        onaxis = np.linalg.norm(x - (x @ a5) * a5) < 1e-9
        if (onaxis or wedge(x) == k) and not any(np.allclose(x, y) for y, _ in sites): sites.append((x, X))
P = np.array([x for x, _ in sites]); n_f = np.array([f(n) / np.linalg.norm(f(n)) for _, n, d in PO]); d_f = np.array([d.f() / np.linalg.norm(f(n)) for _, n, d in PO])
g = lambda Dx: np.max((Dx @ n_f.T) / (2 * d_f), axis=-1)
alive = np.ones(len(P), bool)
def clash_pairs():
    out = []
    for i in np.where(alive)[0]:
        gx = g(P - P[i]); gx[i] = 9; gx[~alive] = 9
        out += [(i, j) for j in np.where(gx < 1 - 1e-9)[0] if j > i]
    return out
removed = 0
while True:
    cp = clash_pairs()
    if not cp: break
    cnt = {}
    for i, j in cp: cnt[i] = cnt.get(i, 0) + 1; cnt[j] = cnt.get(j, 0) + 1
    i = max(cnt, key=lambda i: (cnt[i], np.linalg.norm(P[i])))
    for q in [np.linalg.matrix_power(R72, s) @ P[i] for s in range(5)]:
        dd = np.linalg.norm(P - q, axis=1); j = int(np.argmin(dd))
        if dd[j] < 1e-6 and alive[j]: alive[j] = False; removed += 1
print(f'radius {RAD}: {len(P)} sites, {removed} silenced in five-fold orbits (float), now checking exactly', flush=True)
# exact check over all pairs closer than twice the circumradius
keep = [sites[i][1] for i in np.where(alive)[0]]; Kf = P[alive]; rmax = 2 * np.linalg.norm(Of, axis=1).max() + 1e-6
over = 0; touch = 0; pairs = 0
for a in range(len(keep)):
    for b in range(a + 1, len(keep)):
        if np.linalg.norm(Kf[a] - Kf[b]) > rmax: continue
        pairs += 1; Dx = sub(keep[a], keep[b])
        best = max((dot(n, Dx) - Q(2) * d for _, n, d in PO), key=lambda q: q.f())
        if best.f() < -1e-12 or (abs(best.f()) < 1e-9 and False): over += 1
        elif best == Q(0): touch += 1
        elif best.f() < 0: over += 1
silent = P[~alive]; dist = sorted(set(np.round(np.linalg.norm(silent - np.outer(silent @ a5, a5), axis=1), 3)))
out = [f'radius {RAD}: {len(P)} sites; silenced {removed} in five-fold orbits; kept {int(alive.sum())}',
       f'EXACT check over {pairs} nearby pairs: overlapping {over}; touching exactly (face to face or edge/corner) {touch}',
       f'silenced copies lie at these distances from the five-fold axis: {dist}',
       f'kept fraction by distance from the axis: ' + ', '.join(f'<{r0:.0f}: {np.mean(alive[np.linalg.norm(P - np.outer(P @ a5, a5), axis=1) < r0]):.2f}' for r0 in (1, 2, 3, 4))]
print('\n'.join(out)); open('data/chorus-exact-big.txt' if RAD == 5 else f'data/chorus-exact-r{RAD:g}.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'sites': Kf.tolist(), 'silenced': silent.tolist(), 'a5': a5.tolist(), 'e1': e1.tolist(), 'e2': e2.tolist(), 'th0': float(th0), 'RAD': RAD, 'all': P.tolist()},
          open('data/chorus-exact-big.json' if RAD == 5 else f'data/chorus-exact-r{RAD:g}.json', 'w'))
