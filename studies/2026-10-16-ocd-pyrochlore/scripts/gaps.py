# Step 3 (DICTO: "fill the gaps"). In the bcc packing every OCD has a Voronoi cell V (a truncated octahedron: bisectors of the
# 8 nearest neighbours +-t_i and the 6 next ones +-(t_i + t_j)). The OCD lies inside V and touches its 8 hexagons, so each copy's
# share of the gap is V minus the OCD. Fill it with cones from the centre over the OCD's free faces (convex pieces), exactly in
# Q(sqrt5); then: kinds, face shapes (rhombi?), and the exact check vol(pieces) = vol(V) - vol(OCD).
import sys, io, os, contextlib, itertools, json, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
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
St = dict(rev); OCD = St['dual of the Hecatodihedron']; Of = F(OCD)
def planes_of(V):
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
PO = planes_of(OCD); hexes = [p for p in PO if len(p[0]) == 6]
unit = lambda n: f(n) / np.linalg.norm(f(n))
tet = next(c for c in itertools.combinations(range(20), 4) if all(abs(unit(hexes[a][1]) @ unit(hexes[b][1]) + 1 / 3) < 1e-9 for a, b in itertools.combinations(c, 2)))
T = [sc(hexes[i][1], Q(2) * hexes[i][2] / dot(hexes[i][1], hexes[i][1])) for i in tet]
# Voronoi cell: bisector planes of the 14 neighbours  n.x = |n|^2 / 2  for n = +-t_i and +-(t_i + t_j)
nbrs = [t for t in T] + [sc(t, Q(-1)) for t in T] + [add(T[a], T[b]) for a, b in itertools.combinations(range(4), 2)][:3]
nbrs += [sc(n, Q(-1)) for n in nbrs[8:11]]
VP = [(n, dot(n, n) * Q(Fr(1, 2))) for n in nbrs]
def solve3(P3):
    (n1, d1), (n2, d2), (n3, d3) = P3; det = det3(n1, n2, n3)
    if det.f() == 0: return None
    return [det3(*[[(d1, d2, d3)[i] if j == k else (n1, n2, n3)[i][j] for j in range(3)] for i in range(3)]) / det for k in range(3)]
Vc = []
for P3 in itertools.combinations(VP, 3):
    x = solve3(P3)
    if x is None or any((dot(n, x) - d).f() > 1e-12 for n, d in VP): continue
    if not any(np.allclose(f(x), f(y), atol=1e-12) for y in Vc): Vc.append(x)
Vf = F(Vc); hV = ConvexHull(Vf)
assert len(Vc) == 24, ('Voronoi cell corners', len(Vc))           # a truncated octahedron has 24 corners
# the OCD lies inside V (all its corners satisfy every bisector), and its 8 contact hexagons lie in V's hexagon planes
assert all(all((dot(n, v) - d).f() <= 1e-12 for n, d in VP) for v in OCD)
# cone cut of V \ OCD over the OCD's faces (floats first), then exact corners
B = [(p[1], p[2]) for p in planes_of(Vc)]
pieces = []
for idx, n, d in PO:
    ring = idx; Fc = Of[ring].mean(0); u = Fc / np.linalg.norm(Fc); e = np.r_[f(n), -d.f()] / np.linalg.norm(f(n))
    Bf = np.array([np.r_[f(m), -dd.f()] / np.linalg.norm(f(m)) for m, dd in B])
    nu = Bf[:, :3] @ u; r1 = np.min(-Bf[nu > 1e-12, 3] / nu[nu > 1e-12]); r0 = np.linalg.norm(Fc)
    if r1 - r0 < 1e-9: continue                                      # a contact hexagon: no gap beyond it
    # cone planes through the centre and each edge of the face (ordered ring)
    Qp = Of[ring]; c = Qp.mean(0); a = Qp[0] - c; a /= np.linalg.norm(a); b = np.cross(u, a)
    order = [ring[i] for i in np.argsort(np.arctan2((Qp - c) @ b, (Qp - c) @ a))]
    hs = [np.r_[-e[:3], -e[3] * -1 if False else e[3] * -1]]           # beyond the face: -n.x + d <= 0
    hs = [np.r_[-f(n), d.f()]]
    cps = []
    for i in range(len(order)):
        p1, p2 = OCD[order[i]], OCD[order[(i + 1) % len(order)]]; m = cross(p1, p2)
        m = m if np.dot(f(m), Fc) > 0 else sc(m, Q(-1)); cps.append((m, Q(0))); hs.append(np.r_[-f(m), 0.0])
    hs += [np.r_[f(m), -dd.f()] for m, dd in B]
    pt = u * (r0 + r1) / 2
    X = HalfspaceIntersection(np.array(hs), pt).intersections; X = np.unique(np.round(X, 10), axis=0)
    planes = B + [(sc(n, Q(-1)), Q(0) - d)] + [(sc(m, Q(-1)), Q(0)) for m, _ in cps]     # all as n.x <= d
    Ve = []
    for v in X:
        act = [(m, dd) for m, dd in planes if abs(np.dot(f(m), v) - dd.f()) < 1e-7 * max(1, np.linalg.norm(f(m)))]
        sol = next((s for P3 in itertools.combinations(act, 3) if (s := solve3(P3)) is not None and np.abs(f(s) - v).max() < 1e-7), None)
        if sol is None:
            assert np.linalg.matrix_rank(np.array([f(m) for m, _ in act])) <= 2, ('no exact corner', v); continue
        if not any(all(sol[k] == w[k] for k in range(3)) for w in Ve): Ve.append(sol)
    pieces.append({'face': len(idx), 'V': Ve})
tot = sum((volume(p['V'], F(p['V'])) for p in pieces), Q(0)); gap = volume(Vc, Vf) - volume(OCD, Of)
G = gc.group(gc.icosa_axes(F(St['icosahedron'])))
kinds = gc.kinds([F(p['V']) for p in pieces], G)
def faceshapes(V):
    Vf_ = F(V); h = ConvexHull(Vf_); pl = []
    for e in h.equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
    out = []
    for e in pl:
        idx = [i for i in range(len(V)) if abs(Vf_[i] @ e[:3] + e[3]) < 1e-7]; Qp = Vf_[idx]; c = Qp.mean(0)
        a = Qp[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a); o = np.argsort(np.arctan2((Qp - c) @ b, (Qp - c) @ a)); Qp = Qp[o]
        L = [np.linalg.norm(Qp[i] - Qp[(i + 1) % len(Qp)]) for i in range(len(Qp))]
        rh = len(Qp) == 4 and max(L) - min(L) < 1e-9
        out.append(('rhombus' if rh else f'{len(Qp)}-gon'))
    return out
out = [f'Voronoi cell: {len(Vc)} corners (truncated octahedron), volume {volume(Vc, Vf)!r} = {volume(Vc, Vf).f():.6f}; OCD inside, touching its 8 hexagons',
       f'gap per copy: V - OCD = {gap!r} = {gap.f():.6f} ({gap.f() / volume(Vc, Vf).f() * 100:.2f}% of space)',
       f'cone cut: {len(pieces)} pieces (over {sum(1 for p in pieces if p["face"] == 6)} free hexagons and {sum(1 for p in pieces if p["face"] == 4)} kites); '
       f'sum - gap = {tot - gap!r} (exact)',
       f'kinds (congruence): {len(kinds)}; counts {sorted((c for c, _ in kinds), reverse=True)}']
for c, i in kinds:
    fs = faceshapes(pieces[i]['V']); out.append(f'   {c:2d} x  on a {"hexagon" if pieces[i]["face"] == 6 else "kite"}: {len(pieces[i]["V"])} corners, faces {dict((k, fs.count(k)) for k in sorted(set(fs)))}, volume {volume(pieces[i]["V"], F(pieces[i]["V"])).f():.6f}')
print('\n'.join(out)); open('data/gaps.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'V': Vf.tolist(), 'pieces': [F(p['V']).tolist() for p in pieces], 'face': [p['face'] for p in pieces]}, open('data/gaps.json', 'w'))
