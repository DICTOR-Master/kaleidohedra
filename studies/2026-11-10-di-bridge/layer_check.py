"""D–I bridge B, steps 4–5 (DICTO 10 Nov: "go on with the kit and full check").
(4) The Karma cell explicitly (#22): I = icosahedron of edge 1/phi, corners cyclic(0, ±1/2, ±1/(2phi)) (dual to the dodecahedron
    cube(±phi/2) + cyclic(0, ±1/2, ±phi^2/2)); 12 pentagonal pyramids (dodecahedron face + the icosahedron corner under it), 30 AXE
    (a dodecahedron edge + the icosahedron edge across it), 20 CLEO (an icosahedron face + the dodecahedron corner over it).
    Checks: counts, volumes add to the dodecahedron, random points covered exactly once. Then: which pieces the plane
    n.x = phi/(2 sqrt3) leaves whole below, whole above, or CUTS (crossed cell centred at level 0).
(5) Full check: in a window, every CLEO left by a crossed Dogstar gets an icosahedron face exactly, from ONE octet (edge phi/sqrt2,
    octahedron centres O0 + fcc lattice (phi/2)(a,b,c), a+b+c even; Pacioli mirror form in the octahedra over CLEOs).
Usage: python layer_check.py"""
import itertools, sys, os, numpy as np
sys.path.insert(0, os.path.expanduser('~/mslide/2026-10-22-platonic-mix-step1'))
from mixes3 import phi, CUBE, DOD, planes
from scipy.spatial import ConvexHull
n = np.ones(3) / 3 ** .5; c = phi / (2 * 3 ** .5); e = 1 / phi; h = phi / 2
def cyc(v): return [v, (v[2], v[0], v[1]), (v[1], v[2], v[0])]
def allsigns(base): return np.unique(np.round(np.array([np.array(w) * np.array(sg) for w in cyc(base) for sg in itertools.product((1, -1), repeat=3)]), 12), axis=0)
I = allsigns((0, 0.5, 1 / (2 * phi))); assert len(I) == 12
D = np.unique(np.round(DOD, 12), axis=0); assert len(D) == 20
dI = lambda: sorted({round(float(np.linalg.norm(p - q)), 9) for p, q in itertools.combinations(I, 2)})[0]
assert abs(dI() - e) < 1e-9
HD = ConvexHull(D); HI = ConvexHull(I)
# dodecahedron faces (12 pentagons) and their outward normals; icosahedron corner under each face = the one most along the normal
faces = {}
for eq in HD.equations:
    key = tuple(np.round(eq, 9));
    if key not in faces: faces[key] = [v for v in D if abs(eq[:3] @ v + eq[3]) < 1e-9]
pieces = []
for key, fv in faces.items():
    nrm = np.array(key[:3]); apex = I[np.argmax(I @ nrm)]; pieces.append(('pentagonal pyramid', np.vstack([fv, [apex]])))
Dedges = [(p, q) for p, q in itertools.combinations(D, 2) if abs(np.linalg.norm(p - q) - 1) < 1e-9]
Iedges = [(p, q) for p, q in itertools.combinations(I, 2) if abs(np.linalg.norm(p - q) - e) < 1e-9]
for p, q in Dedges:
    m = (p + q) / 2; best = max(Iedges, key=lambda t: ((t[0] + t[1]) / 2) @ m)
    pieces.append(('AXE', np.array([p, q, best[0], best[1]])))
for eq in HI.equations:
    fv = [v for v in I if abs(eq[:3] @ v + eq[3]) < 1e-9]
    if len(fv) != 3: continue
    apex = D[np.argmax(D @ eq[:3])]; pieces.append(('CLEO', np.vstack([fv, [apex]])))
pieces = [(k, V) for k, V in pieces]
uniq = {}
for k, V in pieces: uniq.setdefault(k, []).append(V)
cnt = {k: len(v) for k, v in uniq.items()}
# CLEO list may contain each face once per triangle of the hull's triangulation: icosahedron faces are triangles, so 20
vols = sum(ConvexHull(V).volume for k, V in pieces) + HI.volume
print(f'Karma cell: icosahedron + {cnt}; volumes add to {vols:.9f} (dodecahedron {HD.volume:.9f})')
rs = np.random.default_rng(5); X = rs.uniform(-1.5, 1.5, (200000, 3)); X = X[np.all(X @ HD.equations[:, :3].T + HD.equations[:, 3] < -1e-9, axis=1)]
tot = np.all(X @ HI.equations[:, :3].T + HI.equations[:, 3] < 1e-12, axis=1).astype(int)
for k, V in pieces:
    H = ConvexHull(V); tot += np.all(X @ H.equations[:, :3].T + H.equations[:, 3] < 1e-12, axis=1)
part_ok = cnt == {'pentagonal pyramid': 12, 'AXE': 30, 'CLEO': 20} and abs(vols - HD.volume) < 1e-9 and np.all(tot == 1)
print(f'points in the cell covered exactly once: {(tot == 1).mean() * 100:.3f} %  -> Karma partition {"EXACT" if part_ok else "FAILED"}')
# (4) the cut at level c for a crossed Karma cell centred at level 0
lev = lambda V: (V @ n).min(), (V @ n).max()
cls = {}
for k, V in [('icosahedron', I)] + pieces:
    lo, hi = (V @ n).min(), (V @ n).max()
    where = 'below' if hi <= c + 1e-9 else 'above' if lo >= c - 1e-9 else 'CUT'
    cls.setdefault((k, where), 0); cls[(k, where)] += 1
print('crossed Karma cell, plane at the icosahedron inradius:', {f'{k} {w}': v for (k, w), v in sorted(cls.items())})
# (5) every CLEO from a crossed Dogstar in a window gets an icosahedron face from ONE octet
B0 = None; okall = True; m = 0
for i, j, k in itertools.product(range(-4, 5), repeat=3):
    if (i + j + k) % 2 == 0: continue
    ctr = phi * np.array([i, j, k]); A = ctr - h * np.ones(3)
    if abs(A @ n + c) > 1e-9: continue                     # Dogstars whose lowest corner is at level -c (these are the crossed ones)
    Dall = np.vstack([D + phi * np.array(p) for p in itertools.product(range(i - 1, i + 2), range(j - 1, j + 2), range(k - 1, k + 2)) if sum(p) % 2 == 0])
    nb = np.unique(np.round([v for v in Dall if abs(np.linalg.norm(v - A) - 1) < 1e-9 and np.all(np.abs(v - ctr) <= h + 1e-9)], 12), axis=0)
    if len(nb) != 3: okall = False; continue
    B = nb.mean(0); O = B + phi / 6 * np.ones(3)
    if B0 is None: B0 = O
    d = (O - B0) / (phi / 2); inlat = np.allclose(d, np.round(d), atol=1e-9) and int(round(d.sum())) % 2 == 0
    Ic = O + allsigns((0, phi, 1)) / (2 * phi); inpl = Ic[np.abs(Ic @ n - c) < 1e-9]
    face = len(inpl) == 3 and max(min(np.linalg.norm(q - b) for q in inpl) for b in nb) < 1e-9
    okall &= inlat and face; m += 1
print(f'CLEOs in the window: {m}; each meets an icosahedron face exactly, all from one octet: {okall}')
print('FINAL ok' if part_ok and okall and m > 20 else 'FINAL FAIL')
# (4b) congruence classes of the truncated (below-plane) parts of the cut Karma pieces
from scipy.spatial import HalfspaceIntersection
def below_part(V):
    H = ConvexHull(V); hs = np.vstack([H.equations, np.append(n, -c)])
    for t in np.linspace(0.05, 0.95, 19):
        for q in V:
            x0 = V.mean(0) * (1 - t) + q * t
            if np.all(hs[:, :3] @ x0 + hs[:, 3] < -1e-7):
                P = HalfspaceIntersection(hs, x0).intersections; return np.unique(np.round(P, 10), axis=0)
    return None
classes = {}
for k, V in pieces:
    lo, hi = (V @ n).min(), (V @ n).max()
    if not (lo < c - 1e-9 < hi - 1e-9): continue
    P = below_part(V); vol = ConvexHull(P).volume
    sig = (k, len(P), round(vol, 7), tuple(sorted(round(float(np.linalg.norm(a - b)), 6) for a, b in itertools.combinations(P, 2))))
    classes[sig] = classes.get(sig, 0) + 1
print('truncated parts below the plane (piece, corners, volume, x count):')
for (k, nv, vol, _), m_ in sorted(classes.items()): print(f'   {k}: {nv} corners, volume {vol}  x{m_}')
print(f'distinct truncated shapes (up to congruence by distances): {len(classes)}')
