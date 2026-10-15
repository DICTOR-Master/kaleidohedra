# Step 21 (DICTO: "run the canonical cut and exact check"). The golden region round the central copy of the five-fold chorus,
# cut canonically (every golden plane crossing a piece splits it, so the result is independent of order), with every plane exact
# in Q(sqrt5); exact corners (three exact planes, checked against floats), exact volumes, the exact sum check against the cell,
# the five-fold symmetry check (a 72-degree turn maps the set of golden pieces onto itself), and comparison with the Bodhi pieces.
import sys, io, os, contextlib, itertools, json, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
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
St = dict(rev); OCD = St['dual of the Hecatodihedron']; Of = F(OCD); ICO = St['icosahedron']
def exact_planes(V):
    Vf = F(V); out = []
    for e in ConvexHull(Vf).equations:
        idx = [i for i in range(len(V)) if abs(Vf[i] @ e[:3] + e[3]) < 1e-7]
        if any(set(idx) == set(p[0]) for p in out): continue
        for i0, i1, i2 in itertools.combinations(idx, 3):
            n = cross(sub(V[i1], V[i0]), sub(V[i2], V[i0]))
            if any(x.f() != 0 for x in n): break
        d = dot(n, V[i0])
        if d.f() < 0: n, d = sc(n, Q(-1)), Q(0) - d
        out.append((idx, n, d))
    return out
PO = exact_planes(OCD)
hexes = [(n, d) for idx, n, d in PO if len(idx) == 6]
bond = [sc(n, Q(2) * d / dot(n, n)) for n, d in hexes]               # exact joint vectors along the 20 hexagon normals
# two-fold directions (exact): sums of adjacent icosahedron corners
If = F(ICO); twof = []
for a, b in itertools.combinations(range(12), 2):
    if abs(np.linalg.norm(If[a] - If[b]) - min(np.linalg.norm(If[0] - If[j]) for j in range(1, 12))) < 1e-9:
        v = add(ICO[a], ICO[b]); twof += [v, sc(v, Q(-1))]
supp = [max((dot(u, v) for v in OCD), key=lambda q: q.f()) for u in twof]   # envelope planes u.x <= supp (centred)
# the chorus sites, snapped to exact lattice points: integer combinations of exact joint vectors
Sf = np.array(json.load(open('data/chorus-space.json'))['sites'])
Bf = np.array([f(b) for b in bond])
cand = {}
for i, j, k in itertools.combinations(range(20), 3):
    M = np.array([Bf[i], Bf[j], Bf[k]]).T
    if abs(np.linalg.det(M)) < 1e-6: continue
    for s in Sf:
        if tuple(np.round(s, 6)) in cand: continue
        c = np.linalg.solve(M, s); ci = np.round(c)
        if np.allclose(c, ci, atol=1e-6) and np.abs(ci).max() <= 8:
            cand[tuple(np.round(s, 6))] = add(add(sc(bond[i], Q(int(ci[0]))), sc(bond[j], Q(int(ci[1])))), sc(bond[k], Q(int(ci[2]))))
    if len(cand) == len(Sf): break
assert len(cand) == len(Sf), ('sites not snapped', len(cand), len(Sf))
S = [cand[tuple(np.round(s, 6))] for s in Sf]; Sff = F(S)
assert np.allclose(Sff, Sf, atol=1e-6)
centre = int(np.argmin(np.linalg.norm(Sff, axis=1))); C0 = S[centre]
near = [i for i in range(len(S)) if i != centre and np.linalg.norm(Sff[i] - Sff[centre]) < 2.0]
# exact planes, all as (n, d) meaning n.x <= d
def env_planes(i):
    s = S[i]; P = [(u, supp[k] + dot(u, s)) for k, u in enumerate(twof)]
    for (n, d), t in zip(hexes, bond):
        if np.min(np.linalg.norm(Sff - f(add(s, t)), axis=1)) < 1e-6: P.append((n, d + dot(n, s)))   # cut at an actual joint
    return P
ENV = {i: env_planes(i) for i in [centre] + near}
CELL = [(sub(S[j], C0), (dot(S[j], S[j]) - dot(C0, C0)) * Q(Fr(1, 2))) for j in range(len(S)) if j != centre]
fl = lambda P: np.array([np.r_[f(n), -d.f()] for n, d in P])           # float halfspaces n.x - d <= 0
def poly(H):
    H = np.array(H); nrm = np.linalg.norm(H[:, :3], axis=1)
    rr = linprog([0, 0, 0, -1], A_ub=np.c_[H[:, :3], nrm], b_ub=-H[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
    if rr.status != 0 or rr.x[3] < 1e-8: return None
    X = np.unique(np.round(HalfspaceIntersection(H, rr.x[:3]).intersections, 11), axis=0)
    return X if len(X) >= 4 and ConvexHull(X).volume > 1e-12 else None
cellH = fl(CELL); cellX = poly(cellH)
# the golden planes that matter: envelope planes crossing the cell; duplicates merged (exactly)
allp = []
for i in ENV:
    for n, d in ENV[i]:
        nf = f(n); s_ = cellX @ nf - d.f()
        if s_.max() > 1e-9 and s_.min() < -1e-9:
            k = np.r_[nf, -d.f()] / np.linalg.norm(nf)
            if not any(np.allclose(k, np.r_[f(m), -e.f()] / np.linalg.norm(f(m)), atol=1e-10) for m, e in allp): allp.append((n, d))
print(f'{len(S)} chorus sites snapped to exact lattice points; {len(near)} neighbours; {len(allp)} distinct envelope planes cross the central cell', flush=True)
# canonical arrangement: split by every crossing plane, in a fixed order; a cell's sign vector is order-free
cells, stack = [], [(list(cellH), [])]
while stack:
    H, hist = stack.pop(); X = poly(H)
    if X is None: continue
    for k, (n, d) in enumerate(allp):
        if k in [h[0] for h in hist]: continue
        s_ = X @ f(n) - d.f()
        if s_.max() > 1e-9 and s_.min() < -1e-9:
            stack.append((H + [np.r_[f(n), -d.f()]], hist + [(k, 1)])); stack.append((H + [-np.r_[f(n), -d.f()]], hist + [(k, -1)])); break
    else: cells.append((H, X, hist))
envf = {i: fl(ENV[i]) for i in ENV}
golden = [c for c in cells if not any(np.all(envf[i][:, :3] @ c[1].mean(0) + envf[i][:, 3] < 0) for i in envf)]
print(f'canonical arrangement: {len(cells)} cells in the central cell, {len(golden)} golden (outside every envelope)', flush=True)
# exact corners and volumes for every cell (inside and outside), the exact sum check against the cell
def solve3(P3):
    (n1, d1), (n2, d2), (n3, d3) = P3; det = det3(n1, n2, n3)
    if det.f() == 0: return None
    return [det3(*[[(d1, d2, d3)[i] if j == k else (n1, n2, n3)[i][j] for j in range(3)] for i in range(3)]) / det for k in range(3)]
exactP = CELL + allp
def exact_cell(X):
    Ve = []
    for v in X:
        act = [p for p in exactP if abs(f(p[0]) @ v - p[1].f()) < 1e-8 * max(1, np.linalg.norm(f(p[0])))]
        sol = None
        for P3 in itertools.combinations(act, 3):
            s_ = solve3(P3)
            if s_ is not None and np.abs(f(s_) - v).max() < 1e-7: sol = s_; break
        if sol is None:
            rk = np.linalg.matrix_rank(np.array([f(p[0]) / np.linalg.norm(f(p[0])) for p in act]), tol=1e-7) if act else 0
            assert rk <= 2, ('no exact corner', v); continue
        if not any(all(sol[k] == w[k] for k in range(3)) for w in Ve): Ve.append(sol)
    return Ve
tot = Q(0); gold_exact = []
for H, X, hist in cells:
    Ve = exact_cell(X); v = volume(Ve, F(Ve)); tot = tot + v
    if any(c[1] is X for c in golden): gold_exact.append((Ve, v))
cellE = exact_cell(cellX); vcell = volume(cellE, F(cellE))
out = [f'central cell: exact volume {vcell!r} = {vcell.f():.6f}; sum of all {len(cells)} arrangement cells minus the cell = {tot - vcell!r} (exact)',
       f'golden region: {len(golden)} pieces, exact volume {sum((v for _, v in gold_exact), Q(0))!r} = {sum((v for _, v in gold_exact), Q(0)).f():.6f}']
# five-fold symmetry: the 72-degree turn about the axis maps the set of golden pieces onto itself
a5 = np.array(json.load(open('data/chorus-space.json'))['a5']); R72 = gc.rotation(a5, 2 * np.pi / 5)
cen = Sff[centre]
key = lambda X: tuple(sorted(tuple(np.round(p, 6)) for p in X))
keys = {key(c[1]) for c in golden}
sym = all(key((c[1] - cen) @ R72.T + cen) in keys for c in golden)
out.append(f'five-fold symmetry of the canonical golden cut: {sym}')
# kinds and Bodhi comparison
def sig(P):
    P = np.unique(np.round(P, 9), axis=0); E = sorted(np.linalg.norm(a - b) for a, b in itertools.combinations(P, 2)); return len(P), tuple(np.round(np.array(E) / E[-1], 4))
bodhi = {}
for b, nm in [('B1', 'Vajra (fine)'), ('B2', 'Chatra'), ('B3', 'Mudra'), ('B4', 'Crown Jewel'), ('B5', 'Diadem')]:
    bodhi[sig(np.array(json.load(open(f'../2026-10-12-bodhi-pieces/data/bodhi-{b}-unit.json'))['vertices']))] = nm
from collections import Counter
sigs = Counter(sig(c[1]) for c in golden); match = {bodhi[s]: n for s, n in sigs.items() if s in bodhi}
golden_walled = sum(1 for c in golden if all(np.max(np.abs(gc.icosa_axes(F(ICO))['2'] @ (e[:3] / np.linalg.norm(e[:3])))) > 1 - 1e-7 for e in ConvexHull(c[1]).equations))
out.append(f'kinds (shape up to scale): {len(sigs)}; purely golden-walled pieces: {golden_walled}; Bodhi pieces: {match if match else "none"}')
print('\n'.join(out)); open('data/chorus-exact.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'pieces': [c[1].tolist() for c in golden], 'bodhi': [bodhi.get(sig(c[1])) for c in golden], 'centre': cen.tolist(), 'a5': a5.tolist(),
           'neighbours': [Sff[i].tolist() for i in near]}, open('data/chorus-exact.json', 'w'))
